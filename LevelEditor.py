from Mapping import *
from General import *
import Mapping
import pygame
import SpriteGroups
import re
import os


HELP = '''Команды(в скобках сокращённый вариант):
open(o) path - открыть карту по пути path
new(n) path - создать новую карту по пути path
resolution(r) w h - изменить разрешение окна редактора на w x h
resolution(r) - вывести текущее разрешение
quit(q) - закрыть программу
Если в каком-то аргументе присутствуют пробелы, 
то вписывайте его в двойных кавычках'''


OPEN = 1
NEW = 2


SPEED = 150
SPEEDUP = 3


print(HELP)


size = 800, 600
Tile.set_image_size_multiplier(3)


def split_without_quotes(string, splitter=r'\s', quotes=r'[^\\][\'"]'):
    last_index = 0
    strings = []
    in_quotes = False
    for i in range(len(string)):
        if re.fullmatch(splitter, string[i]) and not in_quotes:
            strings += [string[last_index:i]]
            last_index = i + 1
        elif re.fullmatch(quotes, string[i]):
            in_quotes = not in_quotes
    if last_index <= len(string):
        strings += [string[last_index:]]
    return strings


def run_editor(path, mode):
    global size
    print('Запуск редактора...')
    pygame.init()

    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    Tile.load_images()

    if mode == OPEN:
        _, _, tiles = generate_level(load_level(path))
    else:
        tiles = {}

    total_dx, total_dy = 0, 0

    all_tiles_group = pygame.sprite.Group()
    all_tiles = pygame.sprite.Sprite(all_tiles_group)
    all_tiles.image = Tile.tile_images
    all_tiles.rect = all_tiles.image.get_rect()

    clock = pygame.time.Clock()

    is_choosing = False

    tile_type = None

    last_x, last_y = None, None

    lmb_pos = None, None

    running = True
    while running:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    is_choosing = not is_choosing
            elif event.type == pygame.VIDEORESIZE:
                old_surface_saved = screen
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)
                size = event.size
                screen.blit(old_surface_saved, (0, 0))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    lmb_pos = None, None
                    if is_choosing:
                        i = event.pos[0] // Mapping.tile_width
                        j = event.pos[1] // Mapping.tile_height
                        if i < Tile.sheet_size[0] and j < Tile.sheet_size[1]:
                            tile_type = j * Tile.sheet_size[0] + i + 1
                            print('Выбрана плитка:', tile_type)
                        is_choosing = False
                        last_x, last_y = None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if not is_choosing:
                        lmb_pos = event.pos
            elif event.type == pygame.MOUSEMOTION:
                if lmb_pos != (None, None):
                    lmb_pos = event.pos

        clear(screen)
        if is_choosing:
            all_tiles_group.draw(screen)
        else:
            if lmb_pos != (None, None):

                i = int((lmb_pos[0] - total_dx) // Mapping.tile_width)
                j = int((lmb_pos[1] - total_dy) // Mapping.tile_height)

                if (tile_type is not None and
                        (i != last_x or j != last_y)):
                    tiles_on_pos = tiles.get((i, j), [])
                    tile = Tile(tile_type, i, j, len(tiles_on_pos))
                    if (not tiles_on_pos or
                            tile_type != tiles_on_pos[-1].tile_type):
                        tile.x += total_dx
                        tile.y += total_dy
                        tiles[(i, j)] = tiles_on_pos + [tile]
                        last_x, last_y = i, j
                        print('placed')

            if is_pressed(pygame.K_LSHIFT):
                speed = SPEED * SPEEDUP
            else:
                speed = SPEED
            speed *= tick / 1000
            dx, dy = 0, 0
            if is_pressed(pygame.K_LEFT):
                dx += speed
            if is_pressed(pygame.K_RIGHT):
                dx -= speed
            if is_pressed(pygame.K_UP):
                dy += speed
            if is_pressed(pygame.K_DOWN):
                dy -= speed
            total_dx += dx
            total_dy += dy
            if is_pressed(pygame.K_SPACE):
                dx, dy = -total_dx, -total_dy
                total_dx, total_dy = 0, 0
            for sprite in SpriteGroups.tiles_group:
                sprite.x += dx
                sprite.y += dy
                # sprite.rect.topleft = sprite.x, sprite.y
            SpriteGroups.tiles_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
    print('Выход из редактора...')


def main():
    global size
    running = True
    while running:
        args = split_without_quotes(input('> '), ' ', '"')
        if len(args) < 1:
            print('Ошибка. Не указана команда.')
            continue
        command = args[0]
        if command in ('open', 'o'):
            if len(args) < 2:
                print('Ошибка. Не указан путь.')
            else:
                path = args[1]
                if os.path.isfile(os.path.join('data', path)):
                    run_editor(path, OPEN)
                else:
                    print('Ошибка. Файла не существует.')
        elif command in ('new', 'n'):
            if len(args) < 2:
                print('Ошибка. Не указан путь.')
            else:
                path = args[1]
                run_editor(path, NEW)
        elif command in ('resolution', 'r'):
            if len(args) == 1:
                print(', '.join(map(str, size)))
            elif len(args) == 3:
                w, h = args[1:]
                if w.isdigit() and h.isdigit():
                    size = int(w), int(h)
                else:
                    print('Ошибка. Аргументы должны являться целыми числами.')
        elif command in ('quit', 'q'):
            running = False
        else:
            print('Ошибка. Неизвестная команда.')


if __name__ == '__main__':
    main()
