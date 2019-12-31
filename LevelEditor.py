from Mapping import *
from General import *
import Mapping
import pygame
import SpriteGroups
import re
import os
import csv


HELP = '''Команды(в скобках сокращённый вариант):
open(o) path - открыть карту по пути path
new(n) path - создать новую карту по пути path
openas(s) path1 path2 - загрузить карту по пути path1 
и сохранить её по пути path2
resolution(r) w h - изменить разрешение окна редактора на w x h
resolution(r) - вывести текущее разрешение
quit(q) - закрыть программу
Если в каком-то аргументе присутствуют пробелы, 
то вписывайте его в двойных кавычках'''


OPEN = 1
NEW = 2
OPEN_AS = 3


SPEED = 150
SPEEDUP = 3


print(HELP)


size = 800, 600
Tile.set_image_size_multiplier(3)


def save_map(tile_dict, path):
    xs = [k[0] for k in tile_dict.keys()]
    ys = [k[1] for k in tile_dict.keys()]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    tiles_matrix = []

    for x in range(min_x, max_x + 1):
        row = []
        for y in range(min_y, max_y + 1):
            row += [tiles_to_line(tile_dict.get((x, y), ''))]
        tiles_matrix += [row]

    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"')
        writer.writerows(tiles_matrix)


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


def tiles_to_line(tiles):
    """Переводит список плиток в строку для последующего составления csv таблицы
    и сохранения в файл."""
    if not tiles:
        return ''
    result = []
    for tile in tiles:
        if tile.lever_id is not None:
            result += [str(tile.tile_type) + ':' + str(tile.lever_id)]
        else:
            result += [str(tile.tile_type)]
    return ','.join(result)


def run_editor(*paths, mode):
    global size
    print('Запуск редактора...')
    pygame.init()

    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    Tile.load_images()

    if mode == OPEN or mode == OPEN_AS:
        _, _, tiles = generate_level(load_level(paths[0]))
    else:
        tiles = {}

    save_path = os.path.join('data', paths[-1])

    total_dx, total_dy = 0, 0

    all_tiles_group = pygame.sprite.Group()
    all_tiles = pygame.sprite.Sprite(SpriteGroups.all_sprites, all_tiles_group)
    w, h = Tile.tile_images.get_size()
    multiplier = Tile.image_size_multiplier
    tile_images = pygame.transform.scale(Tile.tile_images,
                                         (w * multiplier,
                                          h * multiplier))
    all_tiles.image = tile_images
    all_tiles.rect = all_tiles.image.get_rect()

    clock = pygame.time.Clock()

    is_choosing = False

    tile_type = None

    last_mouse_pos = None, None
    mouse_pos = None, None
    mouse_btn = None

    ctr_pressed = False
    s_pressed = False
    last_presses = [ctr_pressed, s_pressed]

    running = True
    while running:
        tick = clock.tick()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    ctr_pressed = True
                elif event.key == pygame.K_s:
                    s_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    is_choosing = not is_choosing
                elif event.key == pygame.K_LCTRL:
                    ctr_pressed = False
                elif event.key == pygame.K_s:
                    s_pressed = False

            elif event.type == pygame.VIDEORESIZE:
                old_surface_saved = screen
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)
                size = event.size
                screen.blit(old_surface_saved, (0, 0))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if not is_choosing:
                        mouse_pos = event.pos
                        mouse_btn = pygame.BUTTON_LEFT
                elif event.button == pygame.BUTTON_RIGHT:
                    if not is_choosing:
                        mouse_pos = event.pos
                        mouse_btn = pygame.BUTTON_RIGHT
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pos = None, None
                    last_mouse_pos = None, None
                    mouse_btn = None
                    if is_choosing:
                        i = event.pos[0] // Mapping.tile_width
                        j = event.pos[1] // Mapping.tile_height
                        if i < Tile.sheet_size[0] and j < Tile.sheet_size[1]:
                            tile_type = j * Tile.sheet_size[0] + i + 1
                            print('Выбрана плитка:', tile_type)
                        is_choosing = False
                elif event.button == pygame.BUTTON_RIGHT:
                    mouse_pos = None, None
                    last_mouse_pos = None, None
                    mouse_btn = None

            elif event.type == pygame.MOUSEMOTION:
                if mouse_btn is not None:
                    mouse_pos = event.pos

        clear(screen)
        if is_choosing:
            all_tiles_group.draw(screen)
        else:
            if mouse_pos != (None, None) and mouse_btn == pygame.BUTTON_LEFT:

                i = int((mouse_pos[0] - total_dx) // Mapping.tile_width)
                j = int((mouse_pos[1] - total_dy) // Mapping.tile_height)

                if (tile_type is not None and
                        (i != last_mouse_pos[0] or j != last_mouse_pos[1])):
                    tiles_on_pos = tiles.get((j, i), [])
                    if (not tiles_on_pos or
                            tile_type != tiles_on_pos[-1].tile_type):
                        tile = Tile(tile_type, i, j, len(tiles_on_pos))
                        tile.x += total_dx
                        tile.y += total_dy
                        tiles[(j, i)] = tiles_on_pos + [tile]
                        last_mouse_pos = i, j

            elif mouse_pos != (None, None) and mouse_btn == pygame.BUTTON_RIGHT:
                i = int((mouse_pos[0] - total_dx) // Mapping.tile_width)
                j = int((mouse_pos[1] - total_dy) // Mapping.tile_height)
                if i != last_mouse_pos[0] or j != last_mouse_pos[1]:
                    tiles_on_pos = tiles.get((j, i), [])
                    if tiles_on_pos:
                        last_sprite = tiles_on_pos[-1]
                        tiles[(j, i)] = tiles_on_pos[:-1]
                        SpriteGroups.tiles_group.remove(last_sprite)
                        last_mouse_pos = i, j

            if (ctr_pressed and s_pressed and
                    last_presses != [ctr_pressed, s_pressed]):
                save_map(tiles, save_path)
                print(f'Файл сохранен по пути {save_path}')
            last_presses = [ctr_pressed, s_pressed]

            if is_pressed(pygame.K_LSHIFT):
                speed = SPEED * SPEEDUP
            else:
                speed = SPEED
            speed *= tick / 1000
            dx, dy = 0, 0
            if is_pressed(pygame.K_a):
                dx += speed
            if is_pressed(pygame.K_d):
                dx -= speed
            if is_pressed(pygame.K_w):
                dy += speed
            if is_pressed(pygame.K_s) and not is_pressed(pygame.K_LCTRL):
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

    SpriteGroups.empty_all()
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
                    run_editor(path, mode=OPEN)
                else:
                    print('Ошибка. Файла не существует.')
        elif command in ('new', 'n'):
            if len(args) < 2:
                print('Ошибка. Не указан путь.')
            else:
                path = args[1]
                run_editor(path, mode=NEW)
        elif command in ('openas', 's'):
            if len(args) < 3:
                print('Ошибка. Не указаны пути.')
            else:
                path1, path2 = args[1:]
                if not os.path.isfile(os.path.join('data', path1)):
                    print(f'Ошибка. Файла по пути {path1} не существует.')
                else:
                    run_editor(path1, path2, mode=OPEN_AS)
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
