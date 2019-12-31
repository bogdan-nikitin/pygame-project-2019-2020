# Проект для Я.Лицея по библиотеке pygame

Проект представляет собой игру, написанную на языке Python с использованием библиотеки Pygame. Жанр игры - метроидвания.

Спрайты для игры использовать отсюда https://opengameart.org/content/castle-platformer-assets

## О файле tile_config.json

Данный файл содержит информацию о тайлах.  
Данные записываются в формате  
"*номер*": {"isSolid": true/false,  
            "isPlatform": true/false,  
            "leverState": -1/0/1,  
            "damage": *число*}  
ИЛИ  
"*начало*:*конец*": {"isSolid": true/false,  
                     "isPlatform": true/false,  
                     "leverState": -1/0/1,  
                     "damage": *число*}  
Во втором случае всем тайлам, в промежутке от *начало* до *конец*,
присваиваются одинаковые характеристики.  
Некоторые характеристики можно не указывать, тогда им будет выставлено
стандартное значение - false (или 0 для damage и -1 для leverState).  
Тайлы, не объявленные в этом файле,
будут иметь стандартное значение для всех характеристик.