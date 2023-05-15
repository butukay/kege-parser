# KEGE Parser

This tool is capable of parsing tests from [https://inf-ege.sdamgia.ru](https://inf-ege.sdamgia.ru). It's main purpose was to simplify problem solving workflows, avoid distraction and focus only on the given tasks.

⚠️ Work in progress, may not work as expected ⚠️

### Example usage:

**Fetching problems into python files:**

```
$ kege download --python 13137266
``` 
Will parse all supported problems and write them into folder named "13137266". Parser is capable of scraping attached files and automaticly adding some boilerplate code to outputed files. You get something like this: 

```
Задание 24 - №47021
# [https://inf-ege.sdamgia.ru/problem?id=47021]
#
# Текстовый файл содержит только заглавные буквы латинского алфавита (ABC…Z).
# Определите количество групп из идущих подряд не менее 10 символов, которые
# начинаются и заканчиваются буквой A и не содержат других букв A (кроме первой
# и последней) и букв B.
#
# Для выполнения этого задания следует написать программу. Ниже приведён файл,
# который необходимо обработать с помощью данного алгоритма
#
# Условие загружено с помощью butukay-sdamgia-parser


f = open('Задание 24/input/47021.txt', 'r')
# Содержание файла: [https://inf-ege.sdamgia.ru/get_file?id=114004]
# TBQBNRXGZVPUNUICVCCLXMJLTJAOVFWKNGILPWQZFHNGIOEVLIDMJVNDLLRKMMVXYHFQNWNJJGCTEXC
# QUPAIDFDIGLODASCPTXPCJCQKYEEANGFCYIXWFJFMJDELCFAQVBHWUJTBXEFJKTZHTGQLBFDBFRWRAK
# BCZIBULBICJCJJYHXUWAFAUVIYYYLLLKDXCQWKLBMYPJBGKNMGWKPHMPEZAHMHZCNNKHFSAHWHYWHHD
# ...

# here goes your code
```
`13137266/03_47021.py` is a symlink to `Задание 24/47021.py`

**Test your code:**

```
$ kege run --test 13137266
```
You get a realtime dashboard with execution results of your code 

```
Запускаю тест №13137266...
 1 # Задание 24 - №40999  0.043 сек. [+]
 2 # Задание 24 - №27694  0.311 сек. [+]
 3 # Задание 24 - №47021  0.043 сек. [+]
 4 # Задание 24 - №37159  0.043 сек. [-]
 5 # Задание 24 - №27696  0.096 сек. [+]
 6 # Задание 25 - №27857  0.507 сек. [+]
 7 # Задание 25 - №37160  0.123 сек. [+]
 8 # Задание 25 - №36038  0.043 сек. [+]
 9 # Задание 25 - №33770 20.000 сек. [*] - TLE
10 # Задание 25 - №40741 20.000 сек. [*] - TLE
11 # Задание 26 - №33528  0.055 сек. [+]
12 # Задание 26 - №36000  2.307 сек. [+]
13 # Задание 26 - №33496  0.082 сек. [+]
14 # Задание 26 - №40742 20.000 сек. [*] - TLE
15 # Задание 26 - №27881 20.000 сек. [*] - TLE

```


**Fetching answers:**

```
$ kege -q answers 13137266

Ответы на тест №13137266
  №    Тип  Задание №  Ответ
  1    24     40999    275
  2    24     27694    24
  3    24     47021    11138
  4    24     37159    2252
  5    24     27696    7
  6    25     27857    72 84084
  7    25     37160    500002 178 500004 18 500016 48 500018 58 500020 4348
  8    25     36038    452025 150678 452029 23810 452034 226019 452048 226026 452062 226033
  9    25     33770    106084178 106492418 106784498 106842962
 10    25     40741    6876 6374 6924 8024 8358
 11    26     33528    5895 227
 12    26     36000    15 954387771
 13    26     33496    122 10000
 14    26     40742    5000 46
 15    26     27881    397 17
```

### TODO
- More task types support
- Saving tasks into different file types
- Proxy support

### Notes
```
EXAMPLES: 12265115, 12156423, 12156436, 12331229
```

