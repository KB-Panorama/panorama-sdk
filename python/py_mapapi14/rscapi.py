#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype
import mapgdi

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)

# Порядковый номер слоев начинается с 0. Нулевой слой - служебный.
# Идентификатором слоя служит его название. Название слоя уникально.
# Короткое имя слоя (ключ) - уникально.
# Внутренний код (порядковый номер ) объектов начинается с 1.
# Внутренний код объекта не более количества объектов.
# Ключ объекта - уникален.
# Идентификатором семантик служит код. Семантика с кодом 0 - служебная.
# Код семантики не является ее порядковым номером .
# Порядковый номер семантики начинается с 1.
# Короткое имя семантики (ключ) - уникально.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К КЛАССИФИКАТОРУ +++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Запросить идентификатор классификатора карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetRscIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetRscIdent', maptype.HMAP, maptype.HSITE)
    def mapGetRscIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> maptype.HRSC:
        return mapGetRscIdent_t (_hMap, _hSite)


# Запросить имя файла классификатора
# hRsc   - идентификатор классификатора карты,
# target - строка для размещения полного имени файла,
# size   - размер строки
# При ошибке возвращает ноль

    mapGetRscFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscFileName', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscFileName(_hRsc: maptype.HRSC, _target: ctypes.c_char_p, _size: int) -> int:
        return mapGetRscFileName_t (_hRsc, _target, _size)


# Запросить имя файла классификатора в кодировке UNICODE
# hRsc   - идентификатор классификатора карты,
# target - строка для размещения полного имени файла,
# size   - размер строки
# При ошибке возвращает ноль

    mapGetRscFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscFileNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscFileNameUn(_hRsc: maptype.HRSC, _target: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscFileNameUn_t (_hRsc, _target.buffer(), _size)


# Запросить имя файла классификатора в кодировке UNICODE
# hRsc    - идентификатор классификатора карты,
# rscname - строка для размещения имени файла и расширения без пути,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetRscNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscNameUn(_hRsc: maptype.HRSC, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscNameUn_t (_hRsc, _rscname.buffer(), _size)


# Запросить условное название классификатора
# hRsc    - идентификатор классификатора карты,
# name    - строка для размещения условного названия классификатора,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetRscUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscUserName', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscUserName(_hRsc: maptype.HRSC, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetRscUserName_t (_hRsc, _name, _size)


# Установить условное название классификатора
# hRsc    - идентификатор классификатора карты,
# name    - условное название классификатора,
# При ошибке возвращает ноль

    mapSetRscUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscUserName', maptype.HRSC, ctypes.c_char_p)
    def mapSetRscUserName(_hRsc: maptype.HRSC, _name: ctypes.c_char_p) -> int:
        return mapSetRscUserName_t (_hRsc, _name)


# Запросить описание классификатора в UNICODE
# hRsc    - идентификатор классификатора карты,
# name    - строка для размещения условного названия классификатора,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetRscDescriptionUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscDescriptionUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscDescriptionUn(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscDescriptionUn_t (_hRsc, _name.buffer(), _size)


# Установить описание классификатора в UNICODE
# hRsc    - идентификатор классификатора карты,
# str - описание классификатора

    mapSetRscDescriptionUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscDescriptionUn', maptype.HRSC, maptype.PWCHAR)
    def mapSetRscDescriptionUn(_hRsc: maptype.HRSC, _str: mapsyst.WTEXT) -> int:
        return mapSetRscDescriptionUn_t (_hRsc, _str.buffer())


# Запросить тип классификатора в UNICODE
# hRsc    - идентификатор классификатора карты,
# name    - строка для размещения условного названия классификатора,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetRscTypeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTypeUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscTypeUn(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscTypeUn_t (_hRsc, _name.buffer(), _size)


# Установить тип классификатора в UNICODE
# hRsc    - идентификатор классификатора карты,
# str - тип классификатора

    mapSetRscTypeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscTypeUn', maptype.HRSC, maptype.PWCHAR)
    def mapSetRscTypeUn(_hRsc: maptype.HRSC, _str: mapsyst.WTEXT) -> int:
        return mapSetRscTypeUn_t (_hRsc, _str.buffer())


# Запросить имя компьютера, с которого делали последние изменения
# hRsc    - идентификатор классификатора карты,
# name    - строка для размещения типа классификатора,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetRscComputerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscComputerNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscComputerNameUn(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscComputerNameUn_t (_hRsc, _name.buffer(), _size)


# Запросить код ошибки последней операции с классификатором карты
# hRsc - идентификатор классификатора карты
# Коды ошибок перечислены в maperr.rh

    mapGetRscError_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscError', maptype.HRSC)
    def mapGetRscError(_hRsc: maptype.HRSC) -> int:
        return mapGetRscError_t (_hRsc)


# Запросить флаг изменений классификатора карты
# hRsc - идентификатор классификатора карты
# При изменении флага внутренние коды объектов сохраняются

    mapGetRscMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscMode', maptype.HRSC)
    def mapGetRscMode(_hRsc: maptype.HRSC) -> int:
        return mapGetRscMode_t (_hRsc)


# Запросить наличие изменений классификатора карты
# hRsc - идентификатор классификатора карты
# 0 - изменений нет, 1 - классификатор изменен

    mapGetRscModify_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscModify', maptype.HRSC)
    def mapGetRscModify(_hRsc: maptype.HRSC) -> int:
        return mapGetRscModify_t (_hRsc)


# Запросить стиль классификатора карты
# hRsc - идентификатор классификатора карты
# При изменении стиля могут измениться внутренние коды объектов

    mapGetRscStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscStyle', maptype.HRSC)
    def mapGetRscStyle(_hRsc: maptype.HRSC) -> int:
        return mapGetRscStyle_t (_hRsc)


# Запросить возможность редактирования классификатора карты
# hRsc - идентификатор классификатора карты
# Если классификатор открыт только для чтения, то возвращает ноль

    mapGetRscIsWrite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscIsWrite', maptype.HRSC)
    def mapGetRscIsWrite(_hRsc: maptype.HRSC) -> int:
        return mapGetRscIsWrite_t (_hRsc)


# Запросить локально ли размещен классификатор
# Если классификатор открыт на ГИС Сервере, то возвращает ноль

    mapGetRscIsLocalPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscIsLocalPlace', maptype.HRSC)
    def mapGetRscIsLocalPlace(_hRsc: maptype.HRSC) -> int:
        return mapGetRscIsLocalPlace_t (_hRsc)


# Запросить номера таблицы масштабов
# hRsc - идентификатор классификатора карты
# Возвращает номер таблицы масштабов с 1 - общий список масштабов
# 2 - таблица масштабов для крупномасштабных карт

    mapGetRscScaleTableNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscScaleTableNumber', maptype.HRSC)
    def mapGetRscScaleTableNumber(_hRsc: maptype.HRSC) -> int:
        return mapGetRscScaleTableNumber_t (_hRsc)


# Установить номер таблицы масштабов
# hRsc - идентификатор классификатора карты
# 1 - таблица с общим списком масштабов
# 2 - таблица масштабов для крупномасштабных карт

    mapSetRscScaleTableNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscScaleTableNumber', maptype.HRSC, ctypes.c_int)
    def mapSetRscScaleTableNumber(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapSetRscScaleTableNumber_t (_hRsc, _number)


# Запросить масштаб карты для классификатора
# hRsc - идентификатор классификатора карты

    mapGetRscScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscScale', maptype.HRSC)
    def mapGetRscScale(_hRsc: maptype.HRSC) -> int:
        return mapGetRscScale_t (_hRsc)


# Установить масштаб карты для классификатора
# hRsc - идентификатор классификатора карты
# scale - знаменатель масштаба

    mapSetRscScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscScale', maptype.HRSC, ctypes.c_int)
    def mapSetRscScale(_hRsc: maptype.HRSC, _scale: int) -> int:
        return mapSetRscScale_t (_hRsc, _scale)


# Установить код классификатора
# hRsc - идентификатор классификатора карты
# code - код классификатора 7 символов

    mapSetRscClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClassificatorCode', maptype.HRSC, ctypes.c_char_p)
    def mapSetRscClassificatorCode(_hRsc: maptype.HRSC, _code: ctypes.c_char_p) -> int:
        return mapSetRscClassificatorCode_t (_hRsc, _code)


# Запросить число объектов описанных в классификаторе
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectCount', maptype.HRSC)
    def mapGetRscObjectCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscObjectCount_t (_hRsc)


# Запросить число объектов описанных в классификаторе
# в заданном слое
# hRsc - идентификатор классификатора карты
# layer - номер слоя
# При ошибке возвращает ноль

    mapGetRscObjectCountInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectCountInLayer', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectCountInLayer(_hRsc: maptype.HRSC, _layer: int) -> int:
        return mapGetRscObjectCountInLayer_t (_hRsc, _layer)


# Запросить название объекта по порядковому номеру
# в заданном слое
# hRsc   - идентификатор классификатора карты
# layer  - номер слоя
# number - номер объекта в слое
# name   - адрес строки для размещения результата
# size   - размер строки (не меньше 32 байт)
# При ошибке возвращает ноль

    mapGetRscObjectNameInLayerEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectNameInLayerEx', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscObjectNameInLayerEx(_hRsc: maptype.HRSC, _layer: int, _number: int, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetRscObjectNameInLayerEx_t (_hRsc, _layer, _number, _name, _size)

    mapGetRscObjectNameInLayerUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectNameInLayerUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscObjectNameInLayerUn(_hRsc: maptype.HRSC, _layer: int, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscObjectNameInLayerUn_t (_hRsc, _layer, _number, _name.buffer(), _size)


# Запросить классификационный код объекта
# по порядковому номеру в заданном слое
# hRsc - идентификатор классификатора карты
# layer - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapGetRscObjectExcodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectExcodeInLayer', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectExcodeInLayer(_hRsc: maptype.HRSC, _layer: int, _number: int) -> int:
        return mapGetRscObjectExcodeInLayer_t (_hRsc, _layer, _number)


# Запросить код локализации объекта
# по порядковому номеру в заданном слое
# hRsc - идентификатор классификатора карты
# layer - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль (ноль допустим)

    mapGetRscObjectLocalInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectLocalInLayer', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectLocalInLayer(_hRsc: maptype.HRSC, _layer: int, _number: int) -> int:
        return mapGetRscObjectLocalInLayer_t (_hRsc, _layer, _number)


# Запросить внутренний код (порядковый номер) объекта
# по порядковому номеру в заданном слое
# hRsc - идентификатор классификатора карты
# layer - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapGetRscObjectCodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectCodeInLayer', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectCodeInLayer(_hRsc: maptype.HRSC, _layer: int, _number: int) -> int:
        return mapGetRscObjectCodeInLayer_t (_hRsc, _layer, _number)


# Запросить размер текущей таблицы масштабов классификатора
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscScaleCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscScaleCount', maptype.HRSC)
    def mapGetRscScaleCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscScaleCount_t (_hRsc)


# Запросить значение (знаменатель масштаба) из текущей таблицы
# масштабов классификатора  по порядковому номеру (с 1)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscScaleItem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscScaleItem', maptype.HRSC, ctypes.c_int)
    def mapGetRscScaleItem(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscScaleItem_t (_hRsc, _number)


# Установка процента масштаба отображения знака в окнах - примерах
# scale - масштаб отображения в % от 10 до 100 уменьшение, более 100 увеличение

    mapSetRscExampleScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscExampleScale', maptype.HRSC, ctypes.c_int)
    def mapSetRscExampleScale(_hRsc: maptype.HRSC, _scale: int) -> int:
        return mapSetRscExampleScale_t (_hRsc, _scale)


# Запрос процента масштаба отображения знака в окнах - примерах,
# от 10 до 100 уменьшение, более 100 увеличение
# При ошибке возвращает ноль

    mapGetRscExampleScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscExampleScale', maptype.HRSC)
    def mapGetRscExampleScale(_hRsc: maptype.HRSC) -> int:
        return mapGetRscExampleScale_t (_hRsc)


# Поиск объектов классификатора
# oldnumber - номер объекта при предыдущем поиске, 0 - поиск с первого
# seektype - условия поиска  SEEK_RSCOBJECT (maptype.h)
# example - шаблон для поиска
# Возвращает порядковый номер объекта или 0, если такого нет

    mapGetRscSeekObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSeekObjectCode', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapGetRscSeekObjectCode(_hRsc: maptype.HRSC, _oldnumber: int, _seektype: int, _example: ctypes.c_char_p) -> int:
        return mapGetRscSeekObjectCode_t (_hRsc, _oldnumber, _seektype, _example)


# Запросить полное (с путем) имя P3D файла по коду библиотеки в кодировке
# UNICODE по порядковому номеру
# hRsc    - идентификатор классификатора карты,
# name - строка для размещения полного имени файла,
# size    - размер строки
# При ошибке возвращает ноль

    mapGetP3DNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetP3DNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetP3DNameUn(_hRsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetP3DNameUn_t (_hRsc, _number, _name.buffer(), _size)


# Создать классификатор векторной карты
# name - полный путь к файлу создаваемого классификатора
# RSCCREATE -   структура входных данных  (см. maptype.h)
# PALETTE256 -  при необходимости задается палитра (не более 32 цветов)
#               (см. maptype.h)
# При ошибке возвращает ноль

#   mapCreateRsc_t = mapsyst.GetProcAddress(curLib,maptype.HRSC,'mapCreateRsc', ctypes.c_char_p, ctypes.POINTER(RSCCREATE), ctypes.POINTER(maptype.PALETTE256))
#   def mapCreateRsc(_name: ctypes.c_char_p, _rsccreate: ctypes.POINTER(RSCCREATE), _palette: ctypes.POINTER(maptype.PALETTE256)) -> maptype.HRSC:
#       return mapCreateRsc_t (_name, _rsccreate, _palette)

#    mapCreateRscUn_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapCreateRscUn', maptype.PWCHAR, ctypes.POINTER(maptype.RSCCREATEUN), ctypes.POINTER(maptype.PALETTE256))
#    def mapCreateRscUn(_name: mapsyst.WTEXT, _rsccreate: ctypes.POINTER(maptype.RSCCREATEUN), _palette: ctypes.POINTER(maptype.PALETTE256)) -> maptype.HRSC:
#        return mapCreateRscUn_t (_name.buffer(), _rsccreate, _palette)


# Создать классификатор векторной карты c идентификацией кодов объекта
# по ключу (короткому имени объекта)
# name - имя создаваемого файла классификатора
# RSCCREATE -   структура входных данных  (см. maptype.h)
# PALETTE256 -  при необходимости задается палитра (не более 32 цветов)
#               (см. maptype.h)
# При ошибке возвращает ноль

#   mapCreateKeyObjectRsc_t = mapsyst.GetProcAddress(curLib,maptype.HRSC,'mapCreateKeyObjectRsc', ctypes.c_char_p, ctypes.POINTER(RSCCREATE), ctypes.POINTER(maptype.PALETTE256))
#   def mapCreateKeyObjectRsc(_name: ctypes.c_char_p, _rsccreate: ctypes.POINTER(RSCCREATE), _palette: ctypes.POINTER(maptype.PALETTE256)) -> maptype.HRSC:
#       return mapCreateKeyObjectRsc_t (_name, _rsccreate, _palette)


# Создать классификатор по XSD схеме из файла
# rscpath - путь для сохранения классификатора
# xsdpath - путь к схеме
# error   - адрес поля для записи кода ошибки или ноль
# При ошибке возвращает ноль, в противном случае количество добавленных слоев

    mapCreateRscFromXsdEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscFromXsdEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapCreateRscFromXsdEx(_rscpath: mapsyst.WTEXT, _xsdpath: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCreateRscFromXsdEx_t (_rscpath.buffer(), _xsdpath.buffer(), _error)

    mapCreateRscFromXsd_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscFromXsd', maptype.PWCHAR, maptype.PWCHAR)
    def mapCreateRscFromXsd(_rscpath: mapsyst.WTEXT, _xsdpath: mapsyst.WTEXT) -> int:
        return mapCreateRscFromXsd_t (_rscpath.buffer(), _xsdpath.buffer())


# Создать классификатор по XSD схеме из потока
# rscpath - путь для сохранения классификатора
# memory - данные, содержащие схему
# memory_size - размер данных со схемой
# error  - адрес поля для записи кода ошибки или ноль
# При ошибке возвращает ноль, в противном случае количество добавленных слоев

    mapCreateRscFromXsdStreamEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscFromXsdStreamEx', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int))
    def mapCreateRscFromXsdStreamEx(_rscpath: mapsyst.WTEXT, _memory: ctypes.c_char_p, _memory_size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCreateRscFromXsdStreamEx_t (_rscpath.buffer(), _memory, _memory_size, _error)

    mapCreateRscFromXsdStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscFromXsdStream', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_uint)
    def mapCreateRscFromXsdStream(_rscpath: mapsyst.WTEXT, _memory: ctypes.c_char_p, _memory_size: int) -> int:
        return mapCreateRscFromXsdStream_t (_rscpath.buffer(), _memory, _memory_size)


# Запросить данные по классификатору векторной карты
# hRsc - идентификатор классификатора карты
# RSCCREATE -  описание классификатора  (см. maptype.h)
# PALETTE256 - истинная палитра карты   (см. maptype.h)
# При ошибке возвращает ноль

#   mapGetRscDescribe_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetRscDescribe', maptype.HRSC, ctypes.POINTER(RSCCREATE), ctypes.POINTER(maptype.PALETTE256))
#   def mapGetRscDescribe(_hRsc: maptype.HRSC, _rsccreate: ctypes.POINTER(RSCCREATE), _palette: ctypes.POINTER(maptype.PALETTE256)) -> int:
#       return mapGetRscDescribe_t (_hRsc, _rsccreate, _palette)


# Открыть классификатор
# name - имя  файла классификатора в кодировке UNICODE
# mode - GENERIC_READ или GENERIC_WRITE (0 обрабатывается как GENERIC_WRITE)
# При ошибке возвращает ноль

    mapOpenRscEx_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenRscEx', maptype.PWCHAR, ctypes.c_int)
    def mapOpenRscEx(_name: mapsyst.WTEXT, _mode: int) -> maptype.HRSC:
        return mapOpenRscEx_t (_name.buffer(), _mode)

    mapOpenRscUn_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenRscUn', maptype.PWCHAR)
    def mapOpenRscUn(_name: mapsyst.WTEXT) -> maptype.HRSC:
        return mapOpenRscUn_t (_name.buffer())

    mapOpenRsc_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenRsc', ctypes.c_char_p)
    def mapOpenRsc(_name: ctypes.c_char_p) -> maptype.HRSC:
        return mapOpenRsc_t (_name)


# Открыть классификатор в общем списке классификаторов для ускорения
# последующего открытия/закрытия карт с этим классификаторов при потоковой обработке
# name - имя  файла классификатора
# При ошибке возвращает ноль, иначе идентификатор классификатора карты

    mapOpenCommonRscUn_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenCommonRscUn', maptype.PWCHAR)
    def mapOpenCommonRscUn(_name: mapsyst.WTEXT) -> maptype.HRSC:
        return mapOpenCommonRscUn_t (_name.buffer())


# Закрыть классификатор
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapCloseRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseRsc', maptype.HRSC)
    def mapCloseRsc(_hRsc: maptype.HRSC) -> int:
        return mapCloseRsc_t (_hRsc)


# Сохранить классификатор на диск или на сервер после обновления
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapCommitRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitRsc', maptype.HRSC)
    def mapCommitRsc(_hRsc: maptype.HRSC) -> int:
        return mapCommitRsc_t (_hRsc)


# Сохранить классификатор по указанному пути (включая имя)
# hRsc - идентификатор классификатора карты
# path - путь к создаваемому файлу (в UTF-16)
# При ошибке возвращает ноль

    mapSaveRscAs_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveRscAs', maptype.HRSC, maptype.PWCHAR)
    def mapSaveRscAs(_hRsc: maptype.HRSC, _path: mapsyst.WTEXT) -> int:
        return mapSaveRscAs_t (_hRsc, _path.buffer())


# Найти классификатор в текущей папке, папке приложения или общей папке классификаторов
# name - имя классификатора (только имя или полный путь, автоматически ищутся файлы rsc и rscz)
# size - размер буфера для записи полного пути найденного классификатора,
#        если размер равен нулю, то имя классификатора не перезаписывается найденным путем
# При ошибке возвращает ноль

    mapFindRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFindRsc', maptype.PWCHAR, ctypes.c_int)
    def mapFindRsc(_name: mapsyst.WTEXT, _size: int) -> int:
        return mapFindRsc_t (_name.buffer(), _size)


# Считать классификатор по указанному пути
# hRsc - идентификатор обновляемого классификатора карты
# path - путь к считываемому файлу (в UTF-16)
# Чтобы сразу сохранить считанный классификатор в тот, что был открыт
# изначально, необходимо вызвать mapCommitRsc
# Чтобы отменить результаты считывания нужно вызвать mapRevertRsc
# При ошибке возвращает ноль

    mapLoadRscFrom_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoadRscFrom', maptype.HRSC, maptype.PWCHAR)
    def mapLoadRscFrom(_hRsc: maptype.HRSC, _unpath: mapsyst.WTEXT) -> int:
        return mapLoadRscFrom_t (_hRsc, _unpath.buffer())


# Восстановить классификатор с диска
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapRevertRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRevertRsc', maptype.HRSC)
    def mapRevertRsc(_hRsc: maptype.HRSC) -> int:
        return mapRevertRsc_t (_hRsc)


# Сжать классификатор в памяти
# (удалить из таблиц удаленные записи)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapPressRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPressRsc', maptype.HRSC)
    def mapPressRsc(_hRsc: maptype.HRSC) -> int:
        return mapPressRsc_t (_hRsc)


# Сформировать имя XSD-схемы по заданному пути
# К имени папки дописывается имя классификатора с расширением ".xsd"
# Например: ...\schemas\map5000m\map5000m.xsd
# hRsc - идентификатор классификатора карты
# path - путь для размещения схемы
# name - буфер для записи полного пути к схеме
# size - длина буфера в байтах
# При ошибке возвращает ноль

    mapRscGetXSDName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscGetXSDName', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapRscGetXSDName(_hRsc: maptype.HRSC, _path: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapRscGetXSDName_t (_hRsc, _path.buffer(), _name.buffer(), _size)

# Создать или обновить XSD-схему для RSC
# По заданному пути создается папка с именем классификатора без расширения
# К имени папки дописывается имя классификатора с расширением ".xsd"
# Например: ...\schemas\map5000m\map5000m.xsd
# Если такого файла нет или он старее файла RSC, то выполняется создание файла схемы функцией mapRscSaveToXSD
# hRsc - идентификатор классификатора карты
# path - путь для размещения схемы
# name - буфер для записи полного пути к схеме
# size - длина буфера в байтах
# error - поле для записи кода ошибки (maperr.rh)
# Если схема не требует обновления, то возвращает -1
# При ошибке возвращает ноль

    mapRscUpdateXSD_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscUpdateXSD', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapRscUpdateXSD(_hRsc: maptype.HRSC, _path: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapRscUpdateXSD_t (_hRsc, _path.buffer(), _name.buffer(), _size, _error)


# Сохранить описание классификатора в виде прикладной XSD схемы
# hRsc   - идентификатор классификатора карты
# name   - имя создаваемой XSD схемы
# layers - имя XML файла, содержащего указания на переименование и
#          обобщение слоев в прикладной схеме
# comment - текст комментария для размещения в прикладной схеме
# isselectonly - признак вывода в схему только тех слоев, что заданы
#                в файле слоев (layers)
# prefix - префикс идентификатора схемы (targetnamespace),
#          если значение равно нулю, то в качества идентификатора присваивается
#          имя классификатора RSC без расширения
# (Например, для operator.rsc в схеме будут сгенерированы строки:
# "<xsd:schema "xmlns:operator=\"http:#www.gisinfo.net/bsd/operator"
#  targetNamespace="http:#www.gisinfo.net/bsd/operator">"
# Имена прикладных элементов в данной схеме будут начинаться с префикса "operator:"
# Подробнее о содержании прикладной схемы можно прочитать
# в документе "Спецификация GML для ЦТК"
# При ошибке возвращает ноль

    mapRscSaveToXSDPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscSaveToXSDPro', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def mapRscSaveToXSDPro(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _layers: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _isselectonly: int, _prefix: mapsyst.WTEXT) -> int:
        return mapRscSaveToXSDPro_t (_hRsc, _name.buffer(), _layers.buffer(), _comment.buffer(), _isselectonly, _prefix.buffer())

    mapRscSaveToXSDEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscSaveToXSDEx', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapRscSaveToXSDEx(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _layers: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _isselectonly: int) -> int:
        return mapRscSaveToXSDEx_t (_hRsc, _name.buffer(), _layers.buffer(), _comment.buffer(), _isselectonly)

    mapRscSaveToXSD_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscSaveToXSD', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def mapRscSaveToXSD(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT, _layers: mapsyst.WTEXT, _comment: mapsyst.WTEXT) -> int:
        return mapRscSaveToXSD_t (_hRsc, _name.buffer(), _layers.buffer(), _comment.buffer())


# Преобразовать формат двоичных числовых полей файла RSC к заданной платформе
# name   - полный путь к файлу преобразуемого классификатора
# tomips - признак платформы (Intel\Little endian - 0, Mips\Sparc\Big endian - 1)
# Преобразование классификатора к той платформе, на которой его открывают, выполняется
# автоматически
# При ошибке возвращает ноль

    mapTurnRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTurnRsc', maptype.PWCHAR, ctypes.c_int)
    def mapTurnRsc(_name: mapsyst.WTEXT, _tomips: int) -> int:
        return mapTurnRsc_t (_name.buffer(), _tomips)


# Запрос количества локализаций
# hRsc - идентификатор классификатора карты

    mapGetLocalCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLocalCount')
    def mapGetLocalCount() -> int:
        return mapGetLocalCount_t ()

    mapGetRscLocalCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscLocalCount', maptype.HRSC)
    def mapGetRscLocalCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscLocalCount_t (_hRsc)

    mapGetRscLocalNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscLocalNameEx', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapGetRscLocalNameEx(_hRsc: maptype.HRSC, _local: int, _name: ctypes.c_char_p, _size: int, _language = maptype.ML_RUSSIAN) -> int:
        return mapGetRscLocalNameEx_t (_hRsc, _local, _name, _size, _language)

    mapGetRscLocalNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscLocalNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetRscLocalNameUn(_hRsc: maptype.HRSC, _local: int, _name: mapsyst.WTEXT, _size: int, _language = maptype.ML_RUSSIAN) -> int:
        return mapGetRscLocalNameUn_t (_hRsc, _local, _name.buffer(), _size, _language)


# Запрос длины имени локализации
# hRsc - идентификатор классификатора карты
# (обычно все названия до 32 символов)

    mapGetRscLocalNameSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscLocalNameSize', maptype.HRSC)
    def mapGetRscLocalNameSize(_hRsc: maptype.HRSC) -> int:
        return mapGetRscLocalNameSize_t (_hRsc)


# При наличии открытой карты  с данным классификатором  после
# изменения порядка вывода слоев на экран, после перемещения объ-
# ектов из слоя в слой и после удаления слоев необходимо привести
# карту в соответствие с классификатором - вызвать mapAdjustData()
# и при необходимости перерисовать карту
# Запрос количества слоев
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscSegmentCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentCount', maptype.HRSC)
    def mapGetRscSegmentCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscSegmentCount_t (_hRsc)

# Запрос имени слоя в кодировке UNICODE по порядковому номеру слоя (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# name - адрес строки для размещения результата
# size - размер строки (может быть до 2048 байт)
# При ошибке возвращает 0

    mapGetRscSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSegmentNameUn(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSegmentNameUn_t (_hRsc, _incode, _name.buffer(), _size)

    mapGetRscSegmentNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSegmentNameUnicode(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSegmentNameUnicode_t (_hRsc, _incode, _name.buffer(), _size)


# Запрос порядкового номера слоя по имени
# Номера слоев начинаются с 0 !
# hRsc - идентификатор классификатора карты
# name - имя слоя
# При отсутствии слоя возвращает - 0, код ошибки IDS_NOTFOUND

    mapGetSegmentByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSegmentByName', maptype.HRSC, ctypes.c_char_p)
    def mapGetSegmentByName(_hRsc: maptype.HRSC, _name: ctypes.c_char_p) -> int:
        return mapGetSegmentByName_t (_hRsc, _name)

    mapGetSegmentByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSegmentByNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetSegmentByNameUn(_hRsc: maptype.HRSC, _name: mapsyst.WTEXT) -> int:
        return mapGetSegmentByNameUn_t (_hRsc, _name.buffer())

# Запрос максимальной длины имени слоя
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscSegmentNameSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentNameSize', maptype.HRSC)
    def mapGetRscSegmentNameSize(_hRsc: maptype.HRSC) -> int:
        return mapGetRscSegmentNameSize_t (_hRsc)


# Запрос порядка вывода слоя на экран по порядковому номеру (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# При ошибке возвращает ноль

    mapGetRscSegmentOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentOrder', maptype.HRSC, ctypes.c_int)
    def mapGetRscSegmentOrder(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscSegmentOrder_t (_hRsc, _incode)


# Запрос количества объектов слоя по  порядковому номеру слоя (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# При ошибке возвращает ноль

    mapGetRscSegmentObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentObjectCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSegmentObjectCount(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscSegmentObjectCount_t (_hRsc, _incode)


# Установка имени слоя по порядковому номеру слоя (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# name   - имя слоя
# При ошибке возвращает ноль, иначе порядковый номер слоя.
# Если вернулся 0, проверьте код последней ошибки функцией mapGetRscError.
# При установке уже имеющегося имени слоя
# функция mapGetRscError возвращает IDS_RSCEXITSEGMENTERROR (MAPERR.RH)

    mapSetRscSegmentName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentName', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscSegmentName(_hRsc: maptype.HRSC, _incode: int, _name: ctypes.c_char_p) -> int:
        return mapSetRscSegmentName_t (_hRsc, _incode, _name)


# Установка порядка вывода слоя по порядковому номеру слоя (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# order  - порядок вывода
# При ошибке возвращает ноль

    mapSetRscSegmentOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentOrder', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscSegmentOrder(_hRsc: maptype.HRSC, _incode: int, _order: int) -> int:
        return mapSetRscSegmentOrder_t (_hRsc, _incode, _order)


# Удалить слой по порядковому номеру слоя (с 0)
# Слой удаляется  вместе с объектами
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# При ошибке возвращает ноль

    mapDeleteRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscSegment', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscSegment(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapDeleteRscSegment_t (_hRsc, _incode)


# Перенести объекты из одного слоя в другой
# hRsc - идентификатор классификатора карты
# oldcode, newcode - номер слоя
# При ошибке возвращает ноль

    mapMoveRscSegmentObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveRscSegmentObjects', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapMoveRscSegmentObjects(_hRsc: maptype.HRSC, _oldcode: int, _newcode: int) -> int:
        return mapMoveRscSegmentObjects_t (_hRsc, _oldcode, _newcode)


# Создать слой в классификаторе карты
# RSCSEGMENT - структура входных данных  (см. maptype.h)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль, иначе порядковый номер слоя(с 0)
# Если вернулся 0, проверьте код последней ошибки функцией mapGetRscError.
# При установке уже имеющегося имени слоя
# функция mapGetRscError возвращает IDS_RSCEXITSEGMENTERROR (MAPERR.RH)

    mapAppendRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscSegment', maptype.HRSC, ctypes.POINTER(maptype.RSCSEGMENT))
    def mapAppendRscSegment(_hRsc: maptype.HRSC, _segment: ctypes.POINTER(maptype.RSCSEGMENT)) -> int:
        return mapAppendRscSegment_t (_hRsc, _segment)


# Заполнить структуру описания слоев
# RSCSEGMENT -  структура входных данных  (см. maptype.h)
# hRsc - идентификатор классификатора карты
# incode - порядковый номер слоя
# При ошибке возвращает ноль и код ошибки
# иначе порядковый номер слоя  (с 0)

    mapGetRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegment', maptype.HRSC, ctypes.POINTER(maptype.RSCSEGMENT), ctypes.c_int)
    def mapGetRscSegment(_hRsc: maptype.HRSC, _segment: ctypes.POINTER(maptype.RSCSEGMENT), _incode: int) -> int:
        return mapGetRscSegment_t (_hRsc, _segment, _incode)

    mapGetRscSegmentShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentShortNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSegmentShortNameUn(_hRsc: maptype.HRSC, _incode: int, _shortname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSegmentShortNameUn_t (_hRsc, _incode, _shortname.buffer(), _size)


# Установить короткое имя(ключ) слоя
# hRsc - идентификатор классификатора карты
# incode - порядковый номер слоя (с 0)
# При ошибке возвращает 0

    mapSetRscSegmentShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentShortName', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscSegmentShortName(_hRsc: maptype.HRSC, _incode: int, _shortname: ctypes.c_char_p) -> int:
        return mapSetRscSegmentShortName_t (_hRsc, _incode, _shortname)

    mapSetRscSegmentKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentKey', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscSegmentKey(_hRsc: maptype.HRSC, _incode: int, _key: ctypes.c_char_p) -> int:
        return mapSetRscSegmentKey_t (_hRsc, _incode, _key)


# Запросить порядковый номер слоя (с 0) по короткому имени(ключу) слоя
# hRsc - идентификатор классификатора карты
# shortname - короткое имя(ключ) слоя
# При ошибке возвращает ноль и код ошибки
# иначе порядковый номер слоя  (с 0)

    mapGetRscSegmentByShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentByShortName', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscSegmentByShortName(_hRsc: maptype.HRSC, _shortname: ctypes.c_char_p) -> int:
        return mapGetRscSegmentByShortName_t (_hRsc, _shortname)

    mapGetRscSegmentByShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentByShortNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSegmentByShortNameUn(_hRsc: maptype.HRSC, _shortname: mapsyst.WTEXT) -> int:
        return mapGetRscSegmentByShortNameUn_t (_hRsc, _shortname.buffer())

    mapGetRscSegmentByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentByKey', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscSegmentByKey(_hRsc: maptype.HRSC, _key: ctypes.c_char_p) -> int:
        return mapGetRscSegmentByKey_t (_hRsc, _key)


# Запросить количество семантик слоя
# hRsc - идентификатор классификатора карты
# incode - порядковый номер слоя (с 0)
# При ошибке возвращает 0

    mapGetRscSegmentSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentSemanticCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSegmentSemanticCount(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscSegmentSemanticCount_t (_hRsc, _incode)


# Запросить код семантики слоя по порядковому номеру
# number семантики в списке (с 1)
# hRsc - идентификатор классификатора карты
# layer - порядковый номер слоя (с 0)
# При ошибке возвращает 0

    mapGetRscSegmentSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentSemanticCode', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSegmentSemanticCode(_hRsc: maptype.HRSC, _layer: int, _number: int) -> int:
        return mapGetRscSegmentSemanticCode_t (_hRsc, _layer, _number)


# Добавить семантику слою
# semanticcode код добавляемой семантики
# hRsc - идентификатор классификатора карты
# layer - порядковый номер слоя (с 0)
# При ошибке возвращает 0

    mapAppendRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscSegmentSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapAppendRscSegmentSemantic(_hRsc: maptype.HRSC, _layer: int, _semanticcode: int) -> int:
        return mapAppendRscSegmentSemantic_t (_hRsc, _layer, _semanticcode)


# Удалить семантику из слоя
# semanticcode код удаляемой семантики
# hRsc - идентификатор классификатора карты
# layer - порядковый номер слоя (с 0)
# При ошибке возвращает 0

    mapDeleteRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscSegmentSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteRscSegmentSemantic(_hRsc: maptype.HRSC, _layer: int, _semanticcode: int) -> int:
        return mapDeleteRscSegmentSemantic_t (_hRsc, _layer, _semanticcode)


# Установить семантику для слоя
# hRsc - идентификатор классификатора карты
# layer - порядковый номер слоя (с 0)
# type = 0 - собрать всю семантику,1 - только обязательную
# При ошибке возвращает 0

    mapBuildRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRscSegmentSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapBuildRscSegmentSemantic(_hRsc: maptype.HRSC, _layer: int, _type: int) -> int:
        return mapBuildRscSegmentSemantic_t (_hRsc, _layer, _type)


# Установить имя слоя в кодировке UNICODE по порядковому номеру слоя (с 0)
# hRsc - идентификатор классификатора карты
# incode - номер слоя
# name - имя слоя в кодировке UNICODE
# При ошибке возвращает 0

    mapSetRscSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSegmentNameUn(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscSegmentNameUn_t (_hRsc, _incode, _name.buffer())

    mapSetRscSegmentNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSegmentNameUnicode(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscSegmentNameUnicode_t (_hRsc, _incode, _name.buffer())


# Запросить количество классов слоев
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscClassCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassCount', maptype.HRSC)
    def mapGetRscClassCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscClassCount_t (_hRsc)


# Запросить идентификатор класса слоя по порядковому номеру среди классов
# слоев (с 1)
# hRsc - идентификатор классификатора карты
# number - порядковый номер класса
# при ошибке возвращает 0 иначе идентификатор класса слоя

    mapGetRscClassIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassIdent', maptype.HRSC, ctypes.c_int)
    def mapGetRscClassIdent(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscClassIdent_t (_hRsc, _number)


# Запросить уровень класса слоя (больше равен 1)
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# при ошибке возвращает 0

    mapGetRscClassLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassLevel', maptype.HRSC, ctypes.c_int)
    def mapGetRscClassLevel(_hRsc: maptype.HRSC, _ident: int) -> int:
        return mapGetRscClassLevel_t (_hRsc, _ident)


# Запросить идентификатор родителя класса слоя
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# возвращает идентификатор класса или порядковый номер слоя (если класс 1 уровня)
# при ошибке возвращает 0 (для класса 1 уровня 0 допустим)

    mapGetRscClassParent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassParent', maptype.HRSC, ctypes.c_int)
    def mapGetRscClassParent(_hRsc: maptype.HRSC, _ident: int) -> int:
        return mapGetRscClassParent_t (_hRsc, _ident)


# Запросить имя класса слоя в кодировке UNICODE по идентификатору класса
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# name - адрес строки для размещения результата
# size - размер строки (может быть до 2048 байт)
# При ошибке возвращает 0

    mapGetRscClassNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscClassNameUnicode(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscClassNameUnicode_t (_hRsc, _incode, _name.buffer(), _size)


# Установить имя класса слоя в кодировке UNICODE по идентификатору класса
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# buffer - полное имя класса (в UNICODE)
# При ошибке возвращает 0

    mapSetRscClassNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClassNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscClassNameUnicode(_hRsc: maptype.HRSC, _ident: int, _buffer: mapsyst.WTEXT) -> int:
        return mapSetRscClassNameUnicode_t (_hRsc, _ident, _buffer.buffer())


# Создать новый класс слоя
# hRsc - идентификатор классификатора карты
# parent - идентификатор класса - родителя или порядковый номер основного слоя,
# key  - ключ, короткое имя класса (в в UNUCODE) (сохраняется как char[32],
#        c завершающим нулем - уникальное
# name - имя класса (в UNUCODE)
# возвращает идентификатор класса
# при ошибке возвращает 0

    mapAppendRscClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscClass', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendRscClass(_hRsc: maptype.HRSC, _parent: int, _key: mapsyst.WTEXT, _name: mapsyst.WTEXT) -> int:
        return mapAppendRscClass_t (_hRsc, _parent, _key.buffer(), _name.buffer())


# Удалить класс слоя
# класс удаляется со всеми классами - потомками, объекты переносятся в
# класс - родитель или в слой - родитель
# ident - идентификатор слоя
# при ошибке возвращает 0, иначе 1

    mapDeleteRscClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscClass', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscClass(_hRsc: maptype.HRSC, _ident: int) -> int:
        return mapDeleteRscClass_t (_hRsc, _ident)


# Запросить слой для класса слоя по идентификатору класса
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# возвращает номер слоя (может быть 0)

    mapGetRscClassGenericSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassGenericSegment', maptype.HRSC, ctypes.c_int)
    def mapGetRscClassGenericSegment(_hRsc: maptype.HRSC, _ident: int) -> int:
        return mapGetRscClassGenericSegment_t (_hRsc, _ident)

# Запросить ключ класса слоя в кодировке UNICODE по идентификатору класса
# hRsc - идентификатор классификатора карты
# ident - идентификатор класса
# name - адрес строки для размещения результата
# size - размер строки (не менее 64 байта)
# При ошибке возвращает 0

    mapGetRscClassKeyUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassKeyUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscClassKeyUnicode(_hRsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscClassKeyUnicode_t (_hRsc, _ident, _name.buffer(), _size)


# Запросить идентификатор класса по ключу класса(в UNICODE)
# buffer - уникальный ключ слоя
# Возвращает идентификатор класса или 0

    mapGetRscClassIdentbyKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClassIdentbyKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscClassIdentbyKeyUn(_hRsc: maptype.HRSC, _buffer: mapsyst.WTEXT) -> int:
        return mapGetRscClassIdentbyKeyUn_t (_hRsc, _buffer.buffer())


# Записать ключ класса(в UNICODE) по идентификатору класса
# ident - идентификатор класса(более 255)
# name - уникальный ключ слоя (в UNICODE) не более 31 символа
# (записывается в char[32])
# Возвращает длину ключа в байтах или 0

    mapSetRscClassKeyUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClassKeyUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscClassKeyUnicode(_hRsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscClassKeyUnicode_t (_hRsc, _ident, _name.buffer())


# Запрос количества дочерних классов слоя
# hRsc - идентификатор классификатора карты
# number - номер слоя (c 0)
# Возвращает количество дочерних классов слоя

    mapGetRscSegmentClassCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentClassCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSegmentClassCount(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscSegmentClassCount_t (_hRsc, _number)


# Запрос количества семантик - идентификаторов поиска для слоя
# hRsc - идентификатор классификатора карты
# number - номер слоя (c 0)
# Возвращает количество семантик - идентификаторов поиска

    mapGetRscSegmentSeekIdentCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentSeekIdentCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSegmentSeekIdentCount(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscSegmentSeekIdentCount_t (_hRsc, _number)


# Запрос кода семантик - идентификаторов поиска для слоя
# hRsc - идентификатор классификатора карты
# number - номер слоя (c 0)
# semnumber - порядковый номер семантики ( от 1 до 4)
# Возвращает код семантики - идентификатора поиска или 0

    mapGetRscSegmentSeekIdentCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentSeekIdentCode', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSegmentSeekIdentCode(_hRsc: maptype.HRSC, _number: int, _semnumber: int) -> int:
        return mapGetRscSegmentSeekIdentCode_t (_hRsc, _number, _semnumber)


# Запрос флага является ли семантика - идентификатором поиска для слоя
# hRsc - идентификатор классификатора карты
# number - номер слоя (c 0)
# semcode - код семантики
# возвращает 1 - является или 0 - не является

    mapGetRscSegmentSeekIdentFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSegmentSeekIdentFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSegmentSeekIdentFlag(_hRsc: maptype.HRSC, _number: int, _semcode: int) -> int:
        return mapGetRscSegmentSeekIdentFlag_t (_hRsc, _number, _semcode)


# Установить семантику как идентификатор поиска для слоя
# hRsc - идентификатор классификатора карты
# number - номер слоя (c 0)
# semnumber - код семантики
# flag - 1 назначить семантику идентификатором поиска для слоя
#      - 0 удалить семантику из списка семантик - идентификаторов поиска
# если у слоя уже 4 семантики - идентификатора семантика не устанавливается
# и возвращается 0
# если семантика не входит в список семантик слоя - семантика будет добавлена
# в список семантик слоя
# возвращает 1, при ошибке возвращает 0

    mapSetRscSegmentSeekIdentFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSegmentSeekIdentFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRscSegmentSeekIdentFlag(_hRsc: maptype.HRSC, _number: int, _semcode: int, _flag: int) -> int:
        return mapSetRscSegmentSeekIdentFlag_t (_hRsc, _number, _semcode, _flag)


# Создать объект
# RSCOBJECT -  структура входных данных  (см. maptype.h)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль , иначе порядковый номер объекта (с 1)

#   mapAppendRscObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapAppendRscObject', maptype.HRSC, ctypes.POINTER(RSCOBJECT))
#   def mapAppendRscObject(_hRsc: maptype.HRSC, _object: ctypes.POINTER(RSCOBJECT)) -> int:
#       return mapAppendRscObject_t (_hRsc, _object)


# Скопировать объект
# hRsc - идентификатор классификатора карты
# oldcode - порядковый номер объекта с которого копируют
# При ошибке возвращает ноль , иначе порядковый номер нового объекта (с 1)
# Копируется заголовок объекта,вид изображения,семантика объекта
# Код  FIRSTSERVEXCODE
# Для того,чтобы данный объект сохранился,
# пользователь должен переопределить внешний код

    mapCopyRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyRscObject', maptype.HRSC, ctypes.c_int)
    def mapCopyRscObject(_hRsc: maptype.HRSC, _oldcode: int) -> int:
        return mapCopyRscObject_t (_hRsc, _oldcode)


# Обновить объект
# RSCOBJECT -  структура входных данных  (см. maptype.h)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль , иначе порядковый номер объекта (с 1)
# При наличии серии внешний код и локализация и слой - не меняются
# Если внешний вид объекта не соответствует локализации - записывается
# умалчиваемый внешний вид

#   mapUpdateRscObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapUpdateRscObject', maptype.HRSC, ctypes.c_int, ctypes.POINTER(RSCOBJECT))
#   def mapUpdateRscObject(_hRsc: maptype.HRSC, _code: int, _object: ctypes.POINTER(RSCOBJECT)) -> int:
#       return mapUpdateRscObject_t (_hRsc, _code, _object)


# Удалить объект
# hRsc - идентификатор классификатора карты
# сode - порядковый номер объекта который удаляют (с 1)
# При ошибке возвращает ноль , иначе порядковый номер удаленного объекта
# если объект входит в серию - удаление не делается

    mapDeleteRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscObject', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscObject(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapDeleteRscObject_t (_hRsc, _code)


# Заполнить структуру описания объекта
# RSCOBJECT -  структура входных данных  (см. maptype.h)
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# При ошибке возвращает ноль , иначе порядковый номер объекта

#   mapGetRscObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetRscObject', maptype.HRSC, ctypes.c_int, ctypes.POINTER(RSCOBJECT))
#   def mapGetRscObject(_hRsc: maptype.HRSC, _incode: int, _object: ctypes.POINTER(RSCOBJECT)) -> int:
#       return mapGetRscObject_t (_hRsc, _incode, _object)


# Запросить порядковый номер объекта в серии однотипных
# объектов (с общим классификационным кодом и локализацией)
# по внутреннему коду объекта
# (Противоположная функция - mapGetRscObjectCodeByNumber)
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# При ошибке или отсутствии серии возвращает ноль ,
# иначе номер объекта в серии

    mapGetRscObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectNumber', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectNumber(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectNumber_t (_hRsc, _incode)


# Запросить размеры в микронах и свойства экранного вида объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# IMAGESIZE -  структура входных данных  (см. maptype.h)
# Строка string длиной length задается для
# определения горизонтального размера подписи
# При ошибке возвращает ноль

    mapGetRscImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImageSize', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.IMAGESIZE), ctypes.c_int, ctypes.c_char_p)
    def mapGetRscImageSize(_hRsc: maptype.HRSC, _incode: int, _imagesize: ctypes.POINTER(maptype.IMAGESIZE), _length, _string: ctypes.c_char_p) -> int:
        return mapGetRscImageSize_t (_hRsc, _incode, _imagesize, _length, _string)


# Запросить размеры в микронах и свойства принтерного вида объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# IMAGESIZE -  структура входных данных  (см. maptype.h)
# Строка string длиной length задается для
# определения горизонтального размера подписи
# При ошибке возвращает ноль

    mapGetRscPrnImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrnImageSize', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.IMAGESIZE), ctypes.c_int, ctypes.c_char_p)
    def mapGetRscPrnImageSize(_hRsc: maptype.HRSC, _incode: int, _imagesize: ctypes.POINTER(maptype.IMAGESIZE), _length, _string: ctypes.c_char_p) -> int:
        return mapGetRscPrnImageSize_t (_hRsc, _incode, _imagesize, _length, _string)


# Запросить габаритную рамку изображения объекта (точечный, векторный)
# с учетом поворота объекта (IMAGEFRAME - см. maptype.h)
# Все размеры в микронах на "бумажном" изображении (в базовом масштабе)
# относительно первой точки метрики объекта в картографической системе
# Для пересчета полученных координат в метры на местности нужно
# их поделить на 1 000 000, умножить на базовый масштаб карты
# и добавить координаты первой точки метрики
# number - номер функции отображения (mapgdi.h)
# param  - параметры отображения (mapgdi.h)
# angle  - угол поворота объекта в радианах по часовой стрелке
# При ошибке возвращает ноль

    mapGetRscMarkFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscMarkFrame', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.POINTER(maptype.IMAGEFRAME))
    def mapGetRscMarkFrame(_hRsc: maptype.HRSC, _number: int, _param: ctypes.c_char_p, _angle: float, _imageframe: ctypes.POINTER(maptype.IMAGEFRAME)) -> int:
        return mapGetRscMarkFrame_t (_hRsc, _number, _param, _angle, _imageframe)


# Запросить внутренний код (порядковый номер) объекта
# по внешнему коду, локализации  и порядковому номеру среди аналогичных
# объектов(с 1)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscObjectCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectCodeByNumber', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectCodeByNumber(_hRsc: maptype.HRSC, _excode: int, _local: int, _number = 1) -> int:
        return mapGetRscObjectCodeByNumber_t (_hRsc, _excode, _local, _number)


# Запросить количество объектов с заданным внешним кодом и локализацией
# hRsc - идентификатор классификатора карты
# excode - внешний код объекта
# local  - тип локализации
# При ошибке возвращает ноль

    mapGetRscObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectsCount', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectsCount(_hRsc: maptype.HRSC, _excode: int, _local: int) -> int:
        return mapGetRscObjectsCount_t (_hRsc, _excode, _local)


# Запросить имя объекта по внутреннему  коду (порядковому номеру) объекта (с 1)
# в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# name - адрес строки для размещения результата
# size - зарезервированный размер строки (может быть до 2048 байт)
# При ошибке возвращает ноль

    mapGetRscObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscObjectNameUn(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscObjectNameUn_t (_hRsc, _incode, _name.buffer(), _size)

    mapGetRscObjectNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscObjectNameUnicode(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscObjectNameUnicode_t (_hRsc, _incode, _name.buffer(), _size)


# Запросить ключ объекта по внутреннему  коду (порядковому номеру)
# объекта (с 1) в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает пустую строку

    mapGetRscObjectKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectKeyUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscObjectKeyUn(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscObjectKeyUn_t (_hRsc, _incode, _name.buffer(), _size)


# Запросить код локализации объекта по внутреннему  коду (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль (ноль допустим)

    mapGetRscObjectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectLocal', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectLocal(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectLocal_t (_hRsc, _incode)


# Запросить номер слоя объекта по внутреннему коду (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль (ноль допустим)

    mapGetRscObjectSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectSegment', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectSegment(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectSegment_t (_hRsc, _incode)


# Установить номер слоя объекта по внутреннему  коду (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# segment - номер слоя (с 0)
# При ошибке возвращает ноль

    mapSetRscObjectSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectSegment', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectSegment(_hRsc: maptype.HRSC, _incode: int, _segment: int) -> int:
        return mapSetRscObjectSegment_t (_hRsc, _incode, _segment)


# Запросить идентификатор класса слоя объекта по внутреннему  коду (порядковому номеру)
# объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectClass', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectClass(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectClass_t (_hRsc, _incode)


# Установить идентификатор класса слоя объекта по внутреннему  коду (порядковому номеру)
# объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# ident - идентификатор класса
# При ошибке возвращает ноль

    mapSetRscObjectClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectClass', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectClass(_hRsc: maptype.HRSC, _incode: int, _ident: int) -> int:
        return mapSetRscObjectClass_t (_hRsc, _incode, _ident)


# Запросить идентификатор объекта (постоянное уникальное значение
# в пределах данного классификатора) по внутреннему  коду (порядковому номеру)
# объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectIdent', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectIdent(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectIdent_t (_hRsc, _incode)


# Запросить внутренний код (порядковый номер) объекта по идентификатору
# hRsc - идентификатор классификатора карты
# ident - идентификатор объекта
# При ошибке возвращает ноль

    mapGetRscObjectIdentIncode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectIdentIncode', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectIdentIncode(_hRsc: maptype.HRSC, _ident: int) -> int:
        return mapGetRscObjectIdentIncode_t (_hRsc, _ident)


# Запросить внутренний код (порядковый номер) объекта по ключу
# hRsc - идентификатор классификатора карты
# key  - ключ объекта
# При ошибке возвращает ноль

    mapGetRscObjectCodeByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByKey', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscObjectCodeByKey(_hRsc: maptype.HRSC, _key: ctypes.c_char_p) -> int:
        return mapGetRscObjectCodeByKey_t (_hRsc, _key)

    mapGetRscObjectKeyIncode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectKeyIncode', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscObjectKeyIncode(_hRsc: maptype.HRSC, _key: ctypes.c_char_p) -> int:
        return mapGetRscObjectKeyIncode_t (_hRsc, _key)

    mapGetRscObjectCodeByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscObjectCodeByKeyUn(_hRsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        return mapGetRscObjectCodeByKeyUn_t (_hRsc, _key.buffer())


# Запросить внутренний код (порядковый номер) объекта по имени
# hRsc - идентификатор классификатора карты
# name - имя объекта
# При ошибке возвращает ноль

    mapGetRscObjectCodeByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByName', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscObjectCodeByName(_hRsc: maptype.HRSC, _name: ctypes.c_char_p) -> int:
        return mapGetRscObjectCodeByName_t (_hRsc, _name)


# Запросить внутренний  код (порядковый номер) объекта по имени
# hRsc - идентификатор классификатора карты
# name - имя объекта
# code - внутренний код объекта, за которым нужно продолжить поиск объекта по имени
# При ошибке возвращает ноль

    mapGetRscObjectCodeByNameAfterCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByNameAfterCode', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscObjectCodeByNameAfterCode(_hRsc: maptype.HRSC, _name: ctypes.c_char_p, _code: int) -> int:
        return mapGetRscObjectCodeByNameAfterCode_t (_hRsc, _name, _code)


# Запросить число семантик, влияющих на внещний вид объекта, по внутреннему
# коду (порядковому номеру)  объекта (с 1)
# incode - внутренний код объекта (номер по порядку)
# hRsc   - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscImageSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSemanticCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscImageSemanticCount(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscImageSemanticCount_t (_hRsc, _incode)


# Запрос кода семантики, влияющей на изображение, по внутреннему коду
# (порядковому номеру) объекта и порядковому номеру такой семантики (c 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# number - номер семантики
# При ошибке возвращает ноль

    mapGetRscImageSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSemanticCode', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscImageSemanticCode(_hRsc: maptype.HRSC, _incode: int, _number: int) -> int:
        return mapGetRscImageSemanticCode_t (_hRsc, _incode, _number)


# Запpосить количество связанных подписей объекта
# по внутреннему коду (порядковому номеру) объекта
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectRelateCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectRelateCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectRelateCount(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectRelateCount_t (_hRsc, _incode)


# Запpосить описание связанной подписи по внутреннему коду
# (порядковому номеру) объекта и по порядковому номеру связанной подписи (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# relate - описание связанной подписи (maptype.h)
# Order  - порядковый номер связанной подписи
# Возвращает идентификатор подписи,
# При ошибке возвращает ноль

    mapGetRscObjectRelateOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectRelateOrder', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RSCRELATION))
    def mapGetRscObjectRelateOrder(_hRsc: maptype.HRSC, _incode: int, _order: int, _relate: ctypes.POINTER(maptype.RSCRELATION)) -> int:
        return mapGetRscObjectRelateOrder_t (_hRsc, _incode, _order, _relate)


# Запросить параметры шрифта для подписи семантики объекта
# по внутреннему  коду (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# semanticcode - код семантики объекта
# viewtype - вид отображения объекта 0 - экранный, 1 - принтерный
# При ошибке или если в параметрах объекта нет подписи возвращает  0
# Удалить описание связанной подписи по внутреннему коду объекта и
# коду семантики
# Возвращает внутренний код объекта,
# При ошибке возвращает ноль

    mapDeleteRscObjectRelate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscObjectRelate', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteRscObjectRelate(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        return mapDeleteRscObjectRelate_t (_hRsc, _incode, _semanticcode)

    mapGetRscObjectSemanticFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectSemanticFont', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.LOGFONT), ctypes.c_int)
    def mapGetRscObjectSemanticFont(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _font: ctypes.POINTER(maptype.LOGFONT), _viewtype: int) -> int:
        return mapGetRscObjectSemanticFont_t (_hRsc, _incode, _semanticcode, _font, _viewtype)


# Установить имя объекта по внутреннему  коду (порядковому номеру) объекта (с 1)
# в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# name - имя объекта в кодировке UNICODE
# При ошибке возвращает ноль

    mapSetRscObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscObjectNameUn(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscObjectNameUn_t (_hRsc, _incode, _name.buffer())

    mapSetRscObjectNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscObjectNameUnicode(_hRsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscObjectNameUnicode_t (_hRsc, _incode, _name.buffer())


# Запросить буквенно-цифровой код объекта по внутреннему коду
# (порядковому номеру) объекта (с 1)
# в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectWCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectWCodeUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscObjectWCodeUn(_hRsc: maptype.HRSC, _incode: int, _wcode: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscObjectWCodeUn_t (_hRsc, _incode, _wcode.buffer(), _size)


# Запросить внутренний код (порядковый номер) объекта (с 1)
# по буквенно-цифровому коду объекта, локализации и порядковому номеру среди аналогичных
# объектов(с 1)(Количество объектов можно получить функцией
# mapGetRscObjectsCount(HRSC hRsc,long int excode, long int local)
# hRsc - идентификатор классификатора карты
# wcode - буквенно-цифровой код объекта
# При ошибке возвращает ноль, иначе incode объекта

    mapGetRscObjectIncodeByWCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectIncodeByWCode', maptype.HRSC, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectIncodeByWCode(_hRsc: maptype.HRSC, _wcode: mapsyst.WTEXT, _local: int, _number = 1) -> int:
        return mapGetRscObjectIncodeByWCode_t (_hRsc, _wcode.buffer(), _local, _number)


# Запросить внешний код объекта по его буквенно-цифровому коду
# hRsc - идентификатор классификатора карты
# wcode - буквенно-цифровой код объекта
# При ошибке возвращает ноль

    mapGetRscObjectExcodeByWCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectExcodeByWCode', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscObjectExcodeByWCode(_hRsc: maptype.HRSC, _wcode: mapsyst.WTEXT) -> int:
        return mapGetRscObjectExcodeByWCode_t (_hRsc, _wcode.buffer())


# Установить буквенно-цифровой код объекта в UNICODE по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# wname - буквенно-цифровой код в UNICODE
# При ошибке возвращает ноль

    mapSetRscObjectWCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectWCodeUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscObjectWCodeUn(_hRsc: maptype.HRSC, _incode: int, _wcode: mapsyst.WTEXT) -> int:
        return mapSetRscObjectWCodeUn_t (_hRsc, _incode, _wcode.buffer())


# Запросить внешний код объекта по порядковому номеру (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код (порядковый номер) объекта
# При ошибке возвращает 0

    mapGetRscObjectExcode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectExcode', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectExcode(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectExcode_t (_hRsc, _incode)


# Запросить признак устаревшего объекта
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# Возвращаемое значение:
# 0 - обычный объект,
# 1 - объект устарел и не должен отображаться в диалоге выбора создаваемого объекта
# При ошибке возвращает ноль

    mapGetRscObjOldFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjOldFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjOldFlag(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjOldFlag_t (_hRsc, _incode)


# Записать флаг объекта оформления
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# flag - признак устаревшего объекта:
# 0 - обычный объект,
# 1 - объект устарел и не должен отображаться в диалоге выбора создаваемого объекта
# При ошибке возвращает ноль

    mapSetRscObjOldFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjOldFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjOldFlag(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscObjOldFlag_t (_hRsc, _incode, _flag)


# Запросить порядoк вывода объекта в слое,
# в данной локализации
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# При ошибке возвращает ноль

    mapGetRscObjectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectOrder', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectOrder(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectOrder_t (_hRsc, _incode)


# Записать порядок вывода объекта в слое
# Устанавливает порядок вывода объекта в слое, в данной локализации
# order - порядок вывода с 0 до 255, где 0 - вывод в стандартном порядке
# При ошибке возвращает ноль

    mapSetRscObjectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectOrder', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectOrder(_hRsc: maptype.HRSC, _incode: int, _order: int) -> int:
        return mapSetRscObjectOrder_t (_hRsc, _incode, _order)


# Запросить направление цифрования объекта по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# При ошибке возвращает ноль

    mapGetRscObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectDirect', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectDirect(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectDirect_t (_hRsc, _incode)


# Запросить/Установить признак мультиконтурного объекта (полигон или линейный объект)
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# flag - признак мультиконтурного объекта 0/1 (при сортировке могут формироваться
#        упрощенные контура для отображения в мелких масштабах)
# При ошибке возвращает ноль

    mapGetRscObjectMultiContourFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectMultiContourFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectMultiContourFlag(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectMultiContourFlag_t (_hRsc, _incode)

    mapSetRscObjectMultiContourFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectMultiContourFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectMultiContourFlag(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscObjectMultiContourFlag_t (_hRsc, _incode, _flag)


# Запросить/Установить признак Полигон с подобъектом-точкой для отображения точечного знака
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# flag - признак полигона с подобъектом-точкой (0/1)
# При ошибке возвращает ноль

    mapGetRscObjectPolygonPointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectPolygonPointFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectPolygonPointFlag(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectPolygonPointFlag_t (_hRsc, _incode)

    mapSetRscObjectPolygonPointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectPolygonPointFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectPolygonPointFlag(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscObjectPolygonPointFlag_t (_hRsc, _incode, _flag)


# Запросить номер функции отображения объекта по внутреннему  коду
# (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectFunction', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectFunction(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectFunction_t (_hRsc, _incode)


# Запросить длину параметров отображения объекта по внутреннему  коду
# (порядковому номеру)объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscObjectParametersSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectParametersSize', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectParametersSize(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectParametersSize_t (_hRsc, _incode)

# Запросить параметры отображения объекта по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# При ошибке возвращает ноль

    mapGetRscObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetRscObjectParameters', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectParameters(_hRsc: maptype.HRSC, _incode: int) -> ctypes.c_void_p:
        return mapGetRscObjectParameters_t (_hRsc, _incode)


# Запросить количество примитивов в параметрах отображения объекта по
# внутреннему коду (порядковому номеру) объекта (с 1) и виду отображения
# viewtype: 0 - экранный, 1 - принтерный
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscPrimitiveCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrimitiveCount', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscPrimitiveCount(_hRsc: maptype.HRSC, _incode: int, _viewtype = 0) -> int:
        return mapGetRscPrimitiveCount_t (_hRsc, _incode, _viewtype)


# Запросить номер функции отображения примитива по порядковому
# номеру примитива в параметрах отображения объекта ,
# внутреннему коду (порядковому номеру) объекта (с 1) и виду отображения
# viewtype: 0 - экранный, 1 - принтерный
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscPrimitiveFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrimitiveFunction', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRscPrimitiveFunction(_hRsc: maptype.HRSC, _incode: int, _number: int, _viewtype = 0) -> int:
        return mapGetRscPrimitiveFunction_t (_hRsc, _incode, _number, _viewtype)


# Запросить длину параметров примитива по порядковому
# номеру примитива в параметрах отображения объекта ,
# внутреннему коду (порядковому номеру) объекта (с 1) и виду отображения
# viewtype: 0 - экранный, 1 - принтерный
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# number - номер примитива
# При ошибке возвращает ноль

    mapGetRscPrimitiveLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrimitiveLength', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRscPrimitiveLength(_hRsc: maptype.HRSC, _incode: int, _number: int, _viewtype = 0) -> int:
        return mapGetRscPrimitiveLength_t (_hRsc, _incode, _number, _viewtype)


# Проверка соответствия локализации и вида отображения объекта
# по внутреннему коду  объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscImageSuitable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImageSuitable', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscImageSuitable(_hRsc: maptype.HRSC, _local: int, _incode: int) -> int:
        return mapGetRscImageSuitable_t (_hRsc, _local, _incode)


# Установить внешний вид объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# length - длина параметров
# number - номер функции отображения
# param  - указатель на параметры функции
# При ошибке возвращает ноль , иначе порядковый номер объекта

    mapSetRscObjectImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectImage', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscObjectImage(_hRsc: maptype.HRSC, _incode: int, _length: int, _number: int, _param: ctypes.c_char_p) -> int:
        return mapSetRscObjectImage_t (_hRsc, _incode, _length, _number, _param)


# Запросить номер функции (принтерного) отображения объекта по внутреннему коду
# (порядковому номеру) объекта
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscPrintObjectFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrintObjectFunction', maptype.HRSC, ctypes.c_int)
    def mapGetRscPrintObjectFunction(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscPrintObjectFunction_t (_hRsc, _incode)


# Запросить длину параметров (принтерного)отображения объекта по внутреннему  коду
#(порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# При ошибке возвращает ноль

    mapGetRscPrintObjectParametersSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPrintObjectParametersSize', maptype.HRSC, ctypes.c_int)
    def mapGetRscPrintObjectParametersSize(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscPrintObjectParametersSize_t (_hRsc, _incode)

# Запросить параметры отображения (принтерного)объекта по внутреннему коду объекта
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# При ошибке возвращает ноль

    mapGetRscPrintObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetRscPrintObjectParameters', maptype.HRSC, ctypes.c_int)
    def mapGetRscPrintObjectParameters(_hRsc: maptype.HRSC, _incode: int) -> ctypes.c_void_p:
        return mapGetRscPrintObjectParameters_t (_hRsc, _incode)

# Установить принтерный вид объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# length - длина параметров
# number - номер функции отображения
# param  - указатель на параметры функции
# При ошибке возвращает ноль , иначе порядковый номер объекта

    mapSetRscPrintObjectImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscPrintObjectImage', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscPrintObjectImage(_hRsc: maptype.HRSC, _incode: int, _length: int, _number: int, _param: ctypes.c_char_p) -> int:
        return mapSetRscPrintObjectImage_t (_hRsc, _incode, _length, _number, _param)


# Найти "основной" цвет изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# viewtype - вид отображения  0 - экранный, 1 - принтерный
# При отсутствии цвета возвращает 0xFF000000
# При ошибке возвращает 0

    mapGetRscObjectBaseColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRscObjectBaseColor', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjectBaseColor(_hRsc: maptype.HRSC, _incode: int, _viewtype: int) -> maptype.COLORREF:
        return mapGetRscObjectBaseColor_t (_hRsc, _incode, _viewtype)


# Запросить параметры шрифта объекта по внутреннему  коду
# (порядковому номеру) объекта (с 1)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта (номер по порядку)
# viewtype -вид отображения  0 - экранный, 1 - принтерный
# При ошибке или если в параметрах объекта нет подписи возвращает ноль

    mapGetRscObjectFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectFont', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.LOGFONT), ctypes.c_int)
    def mapGetRscObjectFont(_hRsc: maptype.HRSC, _incode: int, _font: ctypes.POINTER(maptype.LOGFONT), _viewtype: int) -> int:
        return mapGetRscObjectFont_t (_hRsc, _incode, _font, _viewtype)


# Заполнить параметры шрифта по параметрам текста
# Параметры шрифта заполняются корректно, если среди открытых карт есть
# карта с переданным идентификатором классификатора
# Размер шрифта вычисляется для базового масштаба карты с текущим
# разрешением экрана
# hRsc - идентификатор классификатора карты
# text - параметры функции отображения текста
# font - возвращаемые параметры
# При ошибке возвращает ноль

    mapGetRscTextFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTextFont', maptype.HRSC, ctypes.POINTER(mapgdi.IMGTEXT), ctypes.POINTER(maptype.LOGFONT))
    def mapGetRscTextFont(_hRsc: maptype.HRSC, _text: ctypes.POINTER(mapgdi.IMGTEXT), _font: ctypes.POINTER(maptype.LOGFONT)) -> int:
        return mapGetRscTextFont_t (_hRsc, _text, _font)


# Запросить таблицу отображения шаблонов по внутреннему коду объекта
# hRsc   - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# table  - указатель на структуру TABLETEMPLATE (определено в Mapgdi.h)
# При ошибке возвращает 0

    mapGetRscTemplateTable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTemplateTable', maptype.HRSC, ctypes.c_int, ctypes.POINTER(mapgdi.TABLETEMPLATE))
    def mapGetRscTemplateTable(_hRsc: maptype.HRSC, _incode: int, _table: ctypes.POINTER(mapgdi.TABLETEMPLATE)) -> int:
        return mapGetRscTemplateTable_t (_hRsc, _incode, _table)


# Запросить список кодов семантик, формирующих подписи в векторных знаках,
# являющихся частью вида объекта
# incode - внутренний код (порядковый номер объекта с 1)
# size - размерность массива(количество элементов)
# code - адрес массива кодов семантики
# viewtype -вид отображения  0 - экранный, 1 - принтерный, 2 - все
# возвращает число семантик, от которых зависят подписи
# если размер массива меньше, чем число семантик "лишние" семантики не пишутся

    mapGetRscObjectLabelSemantics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectLabelSemantics', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetRscObjectLabelSemantics(_hrsc: maptype.HRSC, _incode: int, _viewtype: int, _size: int, _code: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRscObjectLabelSemantics_t (_hrsc, _incode, _viewtype, _size, _code)


# Удалить принтерный вид объекта
# incode - внутренний код (порядковый номер объекта с 1)
# При ошибке возвращает ноль

    mapDeleteRscPrintObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscPrintObjectParameters', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscPrintObjectParameters(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapDeleteRscPrintObjectParameters_t (_hRsc, _incode)


# Проверка в параметрах объекта наличия флага горизонтальности шрифта
# по внутреннему коду объекта
# Если в параметрах есть текст или векторный с признаком горизонтальности
# возвращает 1, иначе ноль

    mapCheckRscTextFlagHorizontal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRscTextFlagHorizontal', maptype.HRSC, ctypes.c_int)
    def mapCheckRscTextFlagHorizontal(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapCheckRscTextFlagHorizontal_t (_hRsc, _incode)


# Заполнение массива семантик, влияющих на подписи у объектов с функцией
# отображения IMG_VECTOREX по внутреннему коду объекта
# incode   - внутренний код объекта
# semcode  - буфер для записи внешних кодов семантик для текстов
#            (желательно выделять место не менее 16 # sizeof(int)
# buffsize - размер буфера в байтах
# Если в параметрах нет векторных или в них нет текстов по семантике возвращает 0
# Возвращает общее количество семантик влияющих на подписи, заполняет semcode.
# Если возвращаемое количество больше, чем входит в буфер - увеличьте буфер,
# сделайте повторный вызов

    mapFillRscTextSemanticBuff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFillRscTextSemanticBuff', maptype.HRSC, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapFillRscTextSemanticBuff(_hRsc: maptype.HRSC, _incode: int, _semcode: ctypes.POINTER(ctypes.c_int), _buffsize: int) -> int:
        return mapFillRscTextSemanticBuff_t (_hRsc, _incode, _semcode, _buffsize)


# Заполнение массива семантик по внутреннему коду объекта
# incode   - внутренний код объекта
# flag     - тип семантики (из maptype.h SEMANTIC_FOR_OBJECT)
# semcode  - буфер для записи внешних кодов семантик
#            (желательно выделять место не менее 16 # sizeof(int)
# buffsize - размер буфера в байтах
# Если нет семантик возвращает 0
# Возвращает общее количество семантик с учетом флага, заполняет semcode.
# Если возвращаемое количество больше, чем входит в буфер - увеличьте буфер,
# сделайте повторный вызов

    mapFillRscSemanticBuff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFillRscSemanticBuff', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapFillRscSemanticBuff(_hRsc: maptype.HRSC, _incode: int, _flag: int, _semcode: ctypes.POINTER(ctypes.c_int), _buffsize: int) -> int:
        return mapFillRscSemanticBuff_t (_hRsc, _incode, _flag, _semcode, _buffsize)


# Запросить флаг сжатия изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# Возвращает 0 - изображение сжимается, 1 - нет.

    mapGetRscObjectPressure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectPressure', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectPressure(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectPressure_t (_hRsc, _incode)


# Установить флаг сжатия изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# flag - флаг сжатия изображения 0 - сжимается, 1 - нет.
# При ошибке возвращает ноль

    mapSetRscObjectPressure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectPressure', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectPressure(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscObjectPressure_t (_hRsc, _incode, _flag)


# Запросить размер максимального сжатия изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# Возвращает коэффициент максимального сжатия, умноженный на 10.

    mapGetRscObjectPressLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectPressLimit', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectPressLimit(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectPressLimit_t (_hRsc, _incode)


# Установить размер максимального сжатия изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# presslimit - коэффмциент максимального сжатия, умноженный на 10.
#              в интервале от 10 до 250)
# При ошибке возвращает ноль

    mapSetRscObjectPressLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectPressLimit', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectPressLimit(_hRsc: maptype.HRSC, _incode: int, _presslimit: int) -> int:
        return mapSetRscObjectPressLimit_t (_hRsc, _incode, _presslimit)


# Запросить флаг масштабирования изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# Возвращает 1 - изображение масштабируется, 0 - нет.

    mapGetRscObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectScale', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectScale(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectScale_t (_hRsc, _incode)


# Установить флаг масштабирования изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# flag - флаг масштабирования изображения 1 - масштабируется, 0 - нет.
# При ошибке возвращает ноль

    mapSetRscObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectScale', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectScale(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscObjectScale_t (_hRsc, _incode, _flag)


# Запросить размер максимального увеличения изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# Возвращает коэффмциент максимального увеличения, умноженный на 10.

    mapGetRscObjectScaleLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectScaleLimit', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectScaleLimit(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectScaleLimit_t (_hRsc, _incode)


# Установить размер максимального увеличения изображения объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# scalelimit - коэффмциент максимального сжатия, умноженный на 10.
#              в интервале от 10 до 250)
# При ошибке возвращает ноль

    mapSetRscObjectScaleLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectScaleLimit', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectScaleLimit(_hRsc: maptype.HRSC, _incode: int, _scalelimit: int) -> int:
        return mapSetRscObjectScaleLimit_t (_hRsc, _incode, _scalelimit)


# Установить границы видимости объекта на карте (диапазон масштабов
# видимости объекта на карте
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (внутренний код в классификаторе)
# bottom - минимальное значение знаменателя масштаба при котором виден
#          объект
# top    - максимальное значение знаменателя масштаба при котором виден
#          объект
# При установке значений масштабов они округляются до ближайших
# значений из таблицы стандартных масштабов с установкой признака "включая"
# или "исключая" границу (в зависимости от устанавливаемого значения)
# Например, для значений bottom = 1, top = 199999, объект будет
# виден в масштабах крупнее 1:200 000 (при увеличении более 200 000),
# у другого объекта может быть bottom = 200000, top = 1000000 - он
# будет виден в масштабах 1:200 000 и мельче и может подменять предыдущий
# объект (вместе они никогда не отобразятся).
# Но если объектам поставить границы 160000 и 170000 - они приравняются
# к 200 000 то есть будут одинаковыми.
# При ошибке возвращает ноль

    mapSetRscObjectScaleBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectScaleBorder', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectScaleBorder(_hRsc: maptype.HRSC, _incode: int, _bottom: int, _top: int) -> int:
        return mapSetRscObjectScaleBorder_t (_hRsc, _incode, _bottom, _top)


# Запросить границы видимости объекта на карте (диапазон масштабов
# видимости объекта на карте
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (внутренний код в классификаторе)
# bottom - минимальное значение знаменателя масштаба при котором виден
#          объект
# top    - максимальное значение знаменателя масштаба при котором виден
#          объект
# При ошибке возвращает ноль

    mapGetRscObjectScaleBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectScaleBorder', maptype.HRSC, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetRscObjectScaleBorder(_hRsc: maptype.HRSC, _incode: int, _bottom: ctypes.POINTER(ctypes.c_int), _top: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRscObjectScaleBorder_t (_hRsc, _incode, _bottom, _top)


# Запросить вхождение верхней границы видимости объекта на карте
# в диапазон видимости
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (внутренний код в классификаторе)
# Входит - возвращает 1, иначе 0

    mapGetRscObjectBotScaleInclude_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectBotScaleInclude', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectBotScaleInclude(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectBotScaleInclude_t (_hRsc, _incode)


# Запросить вхождение нижней границы видимости объекта на карте
# в диапазон видимости
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (внутренний код в классификаторе)
# Входит - возвращает 1, иначе 0

    mapGetRscObjectTopScaleInclude_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectTopScaleInclude', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectTopScaleInclude(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectTopScaleInclude_t (_hRsc, _incode)


# Создать новую семантику - возвращает  код созданной семантики
# hRsc - идентификатор классификатора карты
# структура RSCSEMANTICEX описана в maptype.h
# При ошибке возвращает ноль

    mapAppendRscSemanticEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscSemanticEx', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX))
    def mapAppendRscSemanticEx(_hRsc: maptype.HRSC, _rsem: ctypes.POINTER(maptype.RSCSEMANTICEX)) -> int:
        return mapAppendRscSemanticEx_t (_hRsc, _rsem)


# Обновить семантику - возвращает  код обновленной семантики
# code - код обновляемой семантики
# classupdate - 1, классификатор семантики удаляется для последующего
# обновления(например при смене типа семантики), 0 - тип семантики остается
# прежний и обновления классификатора данной семантики не нужно.
# hRsc - идентификатор классификатора карты
# структура RSCSEMANTICEX описана в maptype.h
# При ошибке возвращает ноль

    mapUpdateRscSemanticEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscSemanticEx', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_int)
    def mapUpdateRscSemanticEx(_hRsc: maptype.HRSC, _code: int, _rsem: ctypes.POINTER(maptype.RSCSEMANTICEX), _classupdate: int) -> int:
        return mapUpdateRscSemanticEx_t (_hRsc, _code, _rsem, _classupdate)


# Удалить семантику
# code - код удаляемой семантики
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapDeleteRscSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscSemantic', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscSemantic(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapDeleteRscSemantic_t (_hRsc, _code)


# Запросить информацию о применении семантики для объектов карты
# code - код семантики
# applysemantic - структура для информации (maptype.h)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscApplySemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscApplySemantic', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.APPLYSEMANTIC))
    def mapGetRscApplySemantic(_hRsc: maptype.HRSC, _code: int, _applysemantic: ctypes.POINTER(maptype.APPLYSEMANTIC)) -> int:
        return mapGetRscApplySemantic_t (_hRsc, _code, _applysemantic)


# Объявить принадлежность семантики объекту
# hRsc - идентификатор классификатора карты
# objincode - внутренний код объекта,
# code      - код семантики,
# enable    - код доступа к семантике
# (2 - обязательная, 1 - возможная)
# При ошибке возвращает ноль

    mapEnableRscSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapEnableRscSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapEnableRscSemantic(_hRsc: maptype.HRSC, _objincode: int, _code: int, _enable: int) -> int:
        return mapEnableRscSemantic_t (_hRsc, _objincode, _code, _enable)


# Запросить количество семантик в классификаторе
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticCount', maptype.HRSC)
    def mapGetRscSemanticCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscSemanticCount_t (_hRsc)


# Запросить код семантики по порядковому номеру
# hRsc   - идентификатор классификатора карты
# number - порядковый номер семантики с 1
# При ошибке возвращает ноль

    mapGetRscSemanticCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticCodeByNumber', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemanticCodeByNumber(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscSemanticCodeByNumber_t (_hRsc, _number)


# Запросить код семантики по короткому имени (ключу)семантики
# (ключ семантики должен быть строкой символов латинского алфавита, цифр, знаков подчеркивания)
# hRsc      - идентификатор классификатора карты
# shortname - короткое имя семантики
# При ошибке возвращает ноль

    mapGetRscSemanticCodeByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticCodeByKey', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscSemanticCodeByKey(_hRsc: maptype.HRSC, _key: ctypes.c_char_p) -> int:
        return mapGetRscSemanticCodeByKey_t (_hRsc, _key)

    mapGetRscSemanticCodeByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticCodeByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticCodeByKeyUn(_hRsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        return mapGetRscSemanticCodeByKeyUn_t (_hRsc, _key.buffer())


# Запросить порядковый номер семантики
# по короткому имени (ключу)семантики
# hRsc      - идентификатор классификатора карты
# shortname - короткое имя семантики
# При ошибке возвращает ноль
# иначе порядковый номер семантики (с 1)

    mapGetRscSemanticByShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticByShortName', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscSemanticByShortName(_hRsc: maptype.HRSC, _shortname: ctypes.c_char_p) -> int:
        return mapGetRscSemanticByShortName_t (_hRsc, _shortname)

    mapGetRscSemanticByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticByKey', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscSemanticByKey(_hRsc: maptype.HRSC, _key: ctypes.c_char_p) -> int:
        return mapGetRscSemanticByKey_t (_hRsc, _key)

    mapGetRscSemanticByShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticByShortNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticByShortNameUn(_hRsc: maptype.HRSC, _shortname: mapsyst.WTEXT) -> int:
        return mapGetRscSemanticByShortNameUn_t (_hRsc, _shortname.buffer())

    mapGetRscSemanticByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticByKeyUn(_hRsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        return mapGetRscSemanticByKeyUn_t (_hRsc, _key.buffer())


# Запросить название семантики по порядковому номеру в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# number - номер семантики
# name   - адрес строки для размещения результата
# size   - максимальный размер выходной строки
# При ошибке возвращает пустую строку

    mapGetRscSemanticNameByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticNameByNumberUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticNameByNumberUn(_hRsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticNameByNumberUn_t (_hRsc, _number, _name.buffer(), _size)


# Запросить название семантики по коду в кодировке UTF-16
# hRsc - идентификатор классификатора карты
# code - код семантики
# name - адрес строки для размещения результата
# size - максимальный размер выходной строки в байтах (может быть до 2048 байт)
# При ошибке возвращает ноль

    mapGetRscSemanticNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticNameUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticNameUn_t (_hRsc, _code, _name.buffer(), _size)

    mapGetRscSemanticNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticNameUnicode(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticNameUnicode_t (_hRsc, _code, _name.buffer(), _size)


# Установить название семантики по коду в кодировке UTF-16
# hRsc - идентификатор классификатора карты
# code - код семантики
# name - адрес строки с новым названием
# При ошибке возвращает ноль

    mapSetRscSemanticNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSemanticNameUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscSemanticNameUn_t (_hRsc, _code, _name.buffer())

    mapSetRscSemanticNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticNameUnicode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSemanticNameUnicode(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscSemanticNameUnicode_t (_hRsc, _code, _name.buffer())


# Запросить тип семантики по ее внешнему коду
# Коды типов семантик - см. maptype.h (SEMTYPE)
# hRsc - идентификатор классификатора карты
# code - внешений код семантики
# При ошибке возвращает ноль (символьная семантика имеет тип ноль!)

    mapGetRscSemanticTypeByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticTypeByCode', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemanticTypeByCode(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscSemanticTypeByCode_t (_hRsc, _code)

    mapGetRscSemanticShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticShortNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticShortNameUn(_hRsc: maptype.HRSC, _code: int, _shortname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticShortNameUn_t (_hRsc, _code, _shortname.buffer(), _size)


# Запросить короткое имя (ключ) семантики в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# code - код семантики
# name   - адрес строки для размещения результата
# size   - максимальный размер строки
# При ошибке возвращает ноль

    mapGetRscSemanticKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticKeyUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticKeyUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticKeyUn_t (_hRsc, _code, _name.buffer(), _size)


# Установить короткое имя (ключ) семантики
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapSetRscSemanticShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticShortName', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscSemanticShortName(_hRsc: maptype.HRSC, _code: int, _shortname: ctypes.c_char_p) -> int:
        return mapSetRscSemanticShortName_t (_hRsc, _code, _shortname)

    mapSetRscSemanticKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticKey', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscSemanticKey(_hRsc: maptype.HRSC, _code: int, _key: ctypes.c_char_p) -> int:
        return mapSetRscSemanticKey_t (_hRsc, _code, _key)


# Установить короткое имя (ключ) семантики
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapSetRscSemanticShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticShortNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSemanticShortNameUn(_hRsc: maptype.HRSC, _code: int, _shortname: mapsyst.WTEXT) -> int:
        return mapSetRscSemanticShortNameUn_t (_hRsc, _code, _shortname.buffer())

    def mapSetRscSemanticKeyUn(_hRsc: maptype.HRSC, _code: int, _key: mapsyst.WTEXT) -> int:
        return mapSetRscSemanticShortNameUn_t (_hRsc, _code, _key.buffer())


# Установить размер и точность значения семантики
# hRsc - идентификатор классификатора карты
# size - размер значения семантики (включая десятичную точку)
# decimal - количество знаков после запятой (у символьных - 0)
# code - код семантики
# При ошибке возвращает ноль

    mapSetRscSemanticDecimal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticDecimal', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRscSemanticDecimal(_hRsc: maptype.HRSC, _code: int, _size: int, _decimal: int) -> int:
        return mapSetRscSemanticDecimal_t (_hRsc, _code, _size, _decimal)


# Заполнить расширенную структуру описания семантической характеристики
# по коду семантики и коду объекта
# hRsc - идентификатор классификатора карты
# objectcode - внутренний код объекта
# code - внешний код семантики
# При ошибке возвращает ноль

    mapGetRscSemanticForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticForObject', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticForObject(_hRsc: maptype.HRSC, _semtype: ctypes.POINTER(maptype.RSCSEMANTICEX), _semcode: int, _objectcode: int) -> int:
        return mapGetRscSemanticForObject_t (_hRsc, _semtype, _semcode, _objectcode)


# Заполнить структуру описания семантической характеристики по коду семантики
# hRsc - идентификатор классификатора карты
# code - внешний код семантики
# структура RSCSEMANTICEX описана в maptype.h
# При ошибке возвращает ноль

    mapGetRscSemanticExByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticExByCode', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_int)
    def mapGetRscSemanticExByCode(_hRsc: maptype.HRSC, _semtype: ctypes.POINTER(maptype.RSCSEMANTICEX), _code: int) -> int:
        return mapGetRscSemanticExByCode_t (_hRsc, _semtype, _code)


# Запросить количество значений классификатора семантической
# характеристики по коду семантики (если ее тип TCODE)
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapGetRscSemanticClassificatorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticClassificatorCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemanticClassificatorCount(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscSemanticClassificatorCount_t (_hRsc, _code)


# Запросить название значения характеристики из
# классификатора семантики по коду семантики и
# последовательному номеру в классификаторе в кодировке UNICODE
# hRsc - идентификатор классификатора карты
# code   - код семантики
# number - последовательный номер в классификаторе(1,2,3...)
# name   - адрес строки для размещения результата
# size   - максимальный размер строки (может быть до 2048 байт)
# При ошибке возвращает ноль

    mapGetRscSemanticClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticClassificatorNameUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticClassificatorNameUn(_hRsc: maptype.HRSC, _code: int, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticClassificatorNameUn_t (_hRsc, _code, _number, _name.buffer(), _size)


# Запросить код значения характеристики из
# классификатора семантики по коду семантики и
# последовательному номеру в классификаторе
# hRsc - идентификатор классификатора карты
# number - последовательный номер в классификаторе(1,2,3...)
# code - код семантики
# При ошибке возвращает ноль

    mapGetRscSemanticClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticClassificatorCode', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticClassificatorCode(_hRsc: maptype.HRSC, _code: int, _number: int) -> int:
        return mapGetRscSemanticClassificatorCode_t (_hRsc, _code, _number)


# Записать новую "строчку" классификатора
# (числовое значение и символьное) возвращает
# номер записанной строки с 1
# hRsc - идентификатор классификатора карты
# code - код семантической характеристики
# value - числовое значение
# name  - символьное значение семантической характеристики
# При ошибке возвращает ноль

    mapAppendRscClassificator_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscClassificator', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapAppendRscClassificator(_hRsc: maptype.HRSC, _code: int, _value: int, _name: ctypes.c_char_p) -> int:
        return mapAppendRscClassificator_t (_hRsc, _code, _value, _name)

    mapAppendRscClassificatorUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscClassificatorUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapAppendRscClassificatorUn(_hRsc: maptype.HRSC, _code: int, _value: int, _name: mapsyst.WTEXT) -> int:
        return mapAppendRscClassificatorUn_t (_hRsc, _code, _value, _name.buffer())


# Обновить символьное значение классификатора по номеру строки (с 1)
# Возвращает номер исправленной строки с 1
# hRsc - идентификатор классификатора карты
# code - код семантической характеристики
# index - номер строки
# name  - символьное значение семантической характеристики
# При ошибке возвращает ноль

    mapUpdateRscClassificatorName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscClassificatorName', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapUpdateRscClassificatorName(_hRsc: maptype.HRSC, _code: int, _index: int, _name: ctypes.c_char_p) -> int:
        return mapUpdateRscClassificatorName_t (_hRsc, _code, _index, _name)

    mapUpdateRscClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscClassificatorNameUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapUpdateRscClassificatorNameUn(_hRsc: maptype.HRSC, _code: int, _index: int, _name: mapsyst.WTEXT) -> int:
        return mapUpdateRscClassificatorNameUn_t (_hRsc, _code, _index, _name.buffer())


# Запрос сокращенного имени перечислимой семантики (в UNICODE)
# по коду семантики и значению перечислимой семантики ("Код из классификатора (список)")
# code   - код семантики
# value  - код перечислимой семантики
# size   - размер буфера для размещения строки
# buffer - буфер для размещения строки (64 байта)
# При ошибке возвращает ноль

    mapGetRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClsAbbreviationUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscClsAbbreviationUn(_hRsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscClsAbbreviationUn_t (_hRsc, _code, _value, _buffer.buffer(), _size)


# Записать сокращенное имя перечислимой семантики в UTF-16
# по коду семантики и значению перечислимой семантики ("Код из классификатора (список)")
# code   - код семантики
# value  - код перечислимой семантики
# buffer - сокращенное значение классификатора, не более 31 символа (в UNICODE)
# При ошибке возвращает ноль

    mapSetRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClsAbbreviationUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscClsAbbreviationUn(_hRsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT) -> int:
        return mapSetRscClsAbbreviationUn_t (_hRsc, _code, _value, _buffer.buffer())


# Удалить сокращенное имя перечислимой семантики в UTF-16
# по коду семантики и значению перечислимой семантики ("Код из классификатора (список)")
# code  - код семантики
# value - код перечислимой семантики
# При ошибке возвращает ноль

    mapDeleteRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscClsAbbreviationUn', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteRscClsAbbreviationUn(_hRsc: maptype.HRSC, _code: int, _value: int) -> int:
        return mapDeleteRscClsAbbreviationUn_t (_hRsc, _code, _value)


# Найти числовой идентификатор записи семантики-классификатора по строковому значению
# Поиск осуществляется по совпадению заданной строки с коротким и полным
# именем в семантике-классификаторе
# hRsc - идентификатор классификатора карты
# code - код семантической характеристики типа классификатор
# name  - символьное значение семантической характеристики, которое нужно найти
# Если не нашли возвращает 0, иначе - числовое значение классификатора семантики

    mapFindRscClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFindRscClassificatorCode', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapFindRscClassificatorCode(_hRsc: maptype.HRSC, _code: int, _name: ctypes.c_char_p) -> int:
        return mapFindRscClassificatorCode_t (_hRsc, _code, _name)

    mapFindRscClassificatorCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFindRscClassificatorCodeUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapFindRscClassificatorCodeUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        return mapFindRscClassificatorCodeUn_t (_hRsc, _code, _name.buffer())


# Записать ключ классификатора семантики
# Для одной семантики ключ классификатора должен быть уникален
# hRsc - идентификатор классификатора карты
# code - код семантики
# value - значение классификатора
# возвращает значение классификатора с данным ключом, если это значение
# не совпадает с входным - ключ повторялся и не записан
# При ошибке возвращает ноль

    mapSetRscClsKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClsKey', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscClsKey(_hRsc: maptype.HRSC, _code: int, _value: int, _key: ctypes.c_char_p) -> int:
        return mapSetRscClsKey_t (_hRsc, _code, _value, _key)


# Запрос полного имени классификатора семантики в UTF-16
# по коду семантики и значению классификатора
# hRsc - идентификатор классификатора карты
# code - код семантики
# value - значение классификатора
# size - размер буфера для размещения строки
# buffer - буфер для размещения строки
# возвращает длину полного имени
# При ошибке возвращает ноль

    mapGetRscSemanticClassificatorFullNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticClassificatorFullNameUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticClassificatorFullNameUn(_hRsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticClassificatorFullNameUn_t (_hRsc, _code, _value, _buffer.buffer(), _size)


# Записать полное имя классификатора семантики в UTF-16
# по коду семантики и значению классификатора
# hRsc - идентификатор классификатора карты
# code - код семантики
# value - значение классификатора
# buffer - полное имя объекта (в UNICODE)
# возвращает длину полного имени
# При ошибке возвращает ноль

    mapSetRscClsFullNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscClsFullNameUn', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscClsFullNameUn(_hRsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT) -> int:
        return mapSetRscClsFullNameUn_t (_hRsc, _code, _value, _buffer.buffer())


# Запросить значение классификатора семантики по ключу
# hRsc - идентификатор классификатора карты
# code - код семантики
# value - значение классификатора
# При ошибке возвращает ноль

    mapGetRscClsKeyValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscClsKeyValue', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapGetRscClsKeyValue(_hRsc: maptype.HRSC, _code: int, _key: ctypes.c_char_p) -> int:
        return mapGetRscClsKeyValue_t (_hRsc, _code, _key)


# Запросить является ли семантика списком 3D изображений по коду
# hRsc - идентификатор классификатора карты
# code - код семантики
# Если семантика - список 3D изображений возвращает 1,
# При ошибке возвращает ноль

    mapGetRscSemantic3DListFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemantic3DListFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemantic3DListFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscSemantic3DListFlag_t (_hRsc, _code)


# Установить признак семантики - список 3D изображений
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapSetRscSemantic3DListFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemantic3DListFlag', maptype.HRSC, ctypes.c_int)
    def mapSetRscSemantic3DListFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapSetRscSemantic3DListFlag_t (_hRsc, _code)


# Запросить флаг запрета редактирования семантики (ноль или не ноль)
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapGetRscSemanticNotEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticNotEditFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemanticNotEditFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscSemanticNotEditFlag_t (_hRsc, _code)


# Установить флаг запрета редактирования семантики
# hRsc - идентификатор классификатора карты
# code - код семантики
# flag - 1 - установить запрет, 0 - снять
# При ошибке возвращает ноль

    mapSetRscSemanticNotEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticNotEditFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscSemanticNotEditFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetRscSemanticNotEditFlag_t (_hRsc, _code, _flag)


# Запросить количество семантик - списков 3D изображений  в данной библиотеке
# libcode  - код библиотеки
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscSemantic3DListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemantic3DListCount', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemantic3DListCount(_hRsc: maptype.HRSC, _libcode: int) -> int:
        return mapGetRscSemantic3DListCount_t (_hRsc, _libcode)


# Запросить список кодов семантик - списков 3D изображений
# в данной библиотеке
# hRsc - идентификатор классификатора карты
# libcode  - код библиотеки
# code - адрес массива кодов семантик
# countlimit - размер массива
# Возвращает число записанных кодов семантики
# При ошибке возвращает ноль

    mapGetRscSemantic3DList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemantic3DList', maptype.HRSC, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapGetRscSemantic3DList(_hRsc: maptype.HRSC, _libcode: int, _code: ctypes.POINTER(ctypes.c_int), _countlimit: int) -> int:
        return mapGetRscSemantic3DList_t (_hRsc, _libcode, _code, _countlimit)


# Запросить флаг очистки семантики для семантик типа формула
# hRsc - идентификатор классификатора карты
# code - код семантики
# возвращает 0 или 1

    mapGetRscSemanticCleanValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticCleanValueFlag', maptype.HRSC, ctypes.c_int)
    def mapGetRscSemanticCleanValueFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscSemanticCleanValueFlag_t (_hRsc, _code)


# Установить флаг очистки семантики для семантик типа формула
# hRsc - идентификатор классификатора карты
# code - код семантики
# flag - флаг очистки семантики (ноль или не ноль)
# При ошибке возвращает ноль

    mapSetRscSemanticCleanValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticCleanValueFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscSemanticCleanValueFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetRscSemanticCleanValueFlag_t (_hRsc, _code, _flag)


# Запросить флаг уникальности значения семантики в листе карты
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает 0

    mapGetSemanticUniqueValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSemanticUniqueValueFlag', maptype.HRSC, ctypes.c_int)
    def mapGetSemanticUniqueValueFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetSemanticUniqueValueFlag_t (_hRsc, _code)


# Установить флаг уникальности значения семантики в листе карты
# hRsc - идентификатор классификатора карты
# code - код семантики
# flag - флаг уникальности значения семантики (ноль или не ноль)
# При ошибке возвращает 0

    mapSetSemanticUniqueValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticUniqueValueFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticUniqueValueFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetSemanticUniqueValueFlag_t (_hRsc, _code, _flag)


# Запросить флаг повторяемости значения семантики у объекта
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает 0

    mapGetSemanticRepeatValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSemanticRepeatValueFlag', maptype.HRSC, ctypes.c_int)
    def mapGetSemanticRepeatValueFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetSemanticRepeatValueFlag_t (_hRsc, _code)


# Установить флаг повторяемости значения семантики у объекта
# hRsc - идентификатор классификатора карты
# code - код семантики
# flag - флаг повторяемости значения семантики у объекта (ноль или не ноль)
# При ошибке возвращает 0

    mapSetSemanticRepeatValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticRepeatValueFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticRepeatValueFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetSemanticRepeatValueFlag_t (_hRsc, _code, _flag)


# Запросить флаг заполнения по другой семантике
# code - код семантики
# При ошибке возвращает 0

    mapGetSemanticRecodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSemanticRecodeFlag', maptype.HRSC, ctypes.c_int)
    def mapGetSemanticRecodeFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetSemanticRecodeFlag_t (_hRsc, _code)


# Установить флаг заполнения по другой семантике
# code - код семантики
# flag - флаг заполнения по другой семантике (ноль или не ноль)
# При ошибке возвращает 0

    mapSetSemanticRecodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticRecodeFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticRecodeFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetSemanticRecodeFlag_t (_hRsc, _code, _flag)


# Запросить флаг индексируемой семантики
# code - код семантики
# При ошибке возвращает 0

    mapGetSemanticIndexFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSemanticIndexFlag', maptype.HRSC, ctypes.c_int)
    def mapGetSemanticIndexFlag(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetSemanticIndexFlag_t (_hRsc, _code)


# Установить флаг индексируемой семантики
# code - код семантики
# flag - флаг индексируемой семантики (ноль или не ноль)
# При ошибке возвращает 0

    mapSetSemanticIndexFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticIndexFlag', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticIndexFlag(_hRsc: maptype.HRSC, _code: int, _flag: int) -> int:
        return mapSetSemanticIndexFlag_t (_hRsc, _code, _flag)


# Запросить название единиц измерения семантики по коду в кодировке UTF-16
# hRsc - идентификатор классификатора карты
# code - код семантики
# name - адрес строки для размещения результата
# size - максимальный размер выходной строки в байтах (может быть до 2048 байт)
# При ошибке возвращает ноль

    mapGetRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticUnitUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticUnitUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscSemanticUnitUn_t (_hRsc, _code, _name.buffer(), _size)


# Установить название единиц измерения семантики по коду в кодировке UTF-16
# hRsc - идентификатор классификатора карты
# code - код семантики
# name - адрес строки с новым названием
# При ошибке возвращает ноль

    mapSetRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscSemanticUnitUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscSemanticUnitUn(_hRsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        return mapSetRscSemanticUnitUn_t (_hRsc, _code, _name.buffer())


# Удалить название единиц измерения семантики по коду в кодировке UTF-16
# hRsc - идентификатор классификатора карты
# code - код семантики

    mapDeleteRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscSemanticUnitUn', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscSemanticUnitUn(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapDeleteRscSemanticUnitUn_t (_hRsc, _code)


# Добавить умолчания для семантики для объекта
# hRsc - идентификатор классификатора карты
# semcode - код семантики
# code - код объекта или 0 (для общих умолчаний семантики)
# objmin,objdef,objmax умолчания на объект или общие на семантику
# Возвращает код семантики
# При ошибке возвращает ноль

    mapAppendRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscDef', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapAppendRscDef(_hRsc: maptype.HRSC, _code: int, _semcode: int, _objmin: float, _objdef: float, _objmax: float) -> int:
        return mapAppendRscDef_t (_hRsc, _code, _semcode, _objmin, _objdef, _objmax)


# Заменить умолчания для семантики для объекта
# hRsc - идентификатор классификатора карты
# semcode - код семантики
# code - код объекта или 0 (для общих умолчаний семантики)
# objmin,objdef,objmax умолчания на объект или общие на семантику
# Возвращает код семантики
# При ошибке возвращает ноль

    mapUpdateRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscDef', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapUpdateRscDef(_hRsc: maptype.HRSC, _code: int, _semcode: int, _objmin: float, _objdef: float, _objmax: float) -> int:
        return mapUpdateRscDef_t (_hRsc, _code, _semcode, _objmin, _objdef, _objmax)


# Удалить умолчания для семантики для объекта
# hRsc - идентификатор классификатора карты
# semcode - код семантики
# code - код объекта или 0 (для общих умолчаний семантики)
# Возвращает код семантики
# При ошибке возвращает ноль

    mapDeleteRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscDef', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteRscDef(_hRsc: maptype.HRSC, _code: int, _semcode: int) -> int:
        return mapDeleteRscDef_t (_hRsc, _code, _semcode)


# Запросить количество семантик для данного объекта
# по значимости семантики - см. maptype.h (SEMANTIC_FOR_OBJECT )
# по внутреннему коду (порядковому номеру) объекта (c 1)
# hRsc - идентификатор классификатора карты
# Возвращает количество семантик требуемой значимости
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# importance - важность

    mapGetRscSemanticObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticObjectCount', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticObjectCount(_hRsc: maptype.HRSC, _incode: int, _importance: int) -> int:
        return mapGetRscSemanticObjectCount_t (_hRsc, _incode, _importance)


# Запросить использование семантики для данного объекта -
# incode - внутренний код (порядковый номер)объекта
# semanticcode - код семантики
# hRsc - идентификатор классификатора карты
# Возвращает значимость семантики  см. maptype.h (SEMANTIC_FOR_OBJECT )

    mapGetRscSemanticObjectUsed_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticObjectUsed', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticObjectUsed(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        return mapGetRscSemanticObjectUsed_t (_hRsc, _incode, _semanticcode)


# Запросить использование семантики для данного объекта -
# без учета общих семантик и семантик слоя
# incode - внутренний код(индекс)объекта
# semanticcode - код семантики
# hRsc - идентификатор классификатора карты
# Возвращает значимость семантики  см. maptype.h (SEMANTIC_FOR_OBJECT )

    mapGetRscSemanticOnlyObjectUsed_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticOnlyObjectUsed', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticOnlyObjectUsed(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        return mapGetRscSemanticOnlyObjectUsed_t (_hRsc, _incode, _semanticcode)


# Запросить код семантики  для данного объекта по порядковому номеру
# данной семантики для объекта (с 1) и значимости семантики
# см. maptype.h (SEMANTIC_FOR_OBJECT ) При значимости семантики
# ALL_SEMANTIC - возвращает семантику в порядке сортировки
# incode - внутренний код (порядковый номер) объекта
# importance - значимости семантики
# hRsc - идентификатор классификатора карты
# Возвращает код семантики
# При ошибке возвращает ноль

    mapGetRscSemanticObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticObjectCode', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRscSemanticObjectCode(_hRsc: maptype.HRSC, _incode: int, _number: int, _importance: int) -> int:
        return mapGetRscSemanticObjectCode_t (_hRsc, _incode, _number, _importance)


# Запросить список всех кодов семантики для данного объекта
# incode - внутренний код(индекс)объекта
# hRsc   - идентификатор классификатора карты
# code   - адрес массива семантик
# countlimit - размер массива
# Возвращает число считанных кодов семантики
# При ошибке возвращает ноль

    mapGetRscSemanticObjectCodeList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscSemanticObjectCodeList', maptype.HRSC, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapGetRscSemanticObjectCodeList(_hRsc: maptype.HRSC, _incode: int, _code: ctypes.POINTER(ctypes.c_int), _countlimit: int) -> int:
        return mapGetRscSemanticObjectCodeList_t (_hRsc, _incode, _code, _countlimit)


# Добавить код семантики  для данного объекта по значимости семантики
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC)
# semanticcode - код семантики
# incode - внутренний код (порядковый номер) объекта
# hRsc - идентификатор классификатора карты
# Возвращает номер добавленной семантики в семантиках данного типа
# При ошибке возвращает ноль

    mapAppendRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscSemanticObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapAppendRscSemanticObject(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        return mapAppendRscSemanticObject_t (_hRsc, _incode, _semanticcode, _importance)


# Изменить значимость семантики для данного объекта
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC)
# semanticcode - код семантики
# incode - внутренний код (порядковый номер) объекта
# hRsc - идентификатор классификатора карты
# Возвращает число семантик требуемой значимости
# При ошибке возвращает ноль

    mapUpdateRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscSemanticObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapUpdateRscSemanticObject(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        return mapUpdateRscSemanticObject_t (_hRsc, _incode, _semanticcode, _importance)


# Удалить семантику для данного объекта
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC)
# semanticcode - код семантики
# incode - внутренний код (порядковый номер) объекта
# hRsc - идентификатор классификатора карты
# Возвращает общее число семантик объекта
# При ошибке возвращает ноль

    mapDeleteRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscSemanticObject', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteRscSemanticObject(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        return mapDeleteRscSemanticObject_t (_hRsc, _incode, _semanticcode)


# Записать порядок семантик для объекта в соответствии с входным
# списком
# incode - внутренний код (порядковый номер) объекта
# hRsc - идентификатор классификатора карты
# count - размер массива семантик объекта
# semantics - указатель на сортированный список семантик объекта.
# Семантики которые не наначены объекту - пропускаются,
# Если какие - то семантики пропущены пишутся в конец списка
# при нормальном завершении возвращает количество семантик объекта

    mapSetRscObjSemanticOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjSemanticOrder', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapSetRscObjSemanticOrder(_hRsc: maptype.HRSC, _incode: int, _count: int, _semantics: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapSetRscObjSemanticOrder_t (_hRsc, _incode, _count, _semantics)


# Составить список всех объектов классификатора, использующих семантики с
# признаком - список 3D вида.
# hRsc - идентификатор классификатора карты
# buffer - указатель на массив байтов
# count - размер буфера в байтах (не менее количества объектов классификатора)
# Если для объекта разрешена семантика - список 3D видов, в буфер
# на место, определяемое внутренним кодом объекта заносится 1, иначе 0.
# при нормальном завершении возвращает количество объектов, для которых
# могут использоваться семантики - списки 3D видов

    mapGetRscAll3DSemObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscAll3DSemObjects', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscAll3DSemObjects(_hRsc: maptype.HRSC, _buffer: ctypes.c_char_p, _count: int) -> int:
        return mapGetRscAll3DSemObjects_t (_hRsc, _buffer, _count)


# Запросить цвет из палитры
# color - цвет в COLORREF
# index - порядковый номер цвета в палитре (с 1)
# number - порядковый номер палитры (с 1)
# hRsc - идентификатор классификатора карты
# возвращает цвет в COLORREF

    mapGetRscColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRscColor', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscColor(_hRsc: maptype.HRSC, _index: int, _number = 1) -> maptype.COLORREF:
        return mapGetRscColor_t (_hRsc, _index, _number)


# Установить цвет в данную палитру
# color - цвет в COLORREF
# index - порядковый номер цвета в палитре (с 1)
# number - порядковый номер палитры (с 1)
# hRsc - идентификатор классификатора карты
# возвращает единицу
# При ошибке возвращает ноль

    mapSetRscColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscColor', maptype.HRSC, maptype.COLORREF, ctypes.c_int, ctypes.c_int)
    def mapSetRscColor(_hRsc: maptype.HRSC, _color: maptype.COLORREF, _index: int, _number = 1) -> int:
        return mapSetRscColor_t (_hRsc, _color, _index, _number)


# Запросить количество цветов в палитре классификатора
# hRsc - идентификатор классификатора карты

    mapGetRscColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscColorCount', maptype.HRSC)
    def mapGetRscColorCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscColorCount_t (_hRsc)


# Запросить количество палитр классификатора
# hRsc - идентификатор классификатора карты

    mapGetRscPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPaletteCount', maptype.HRSC)
    def mapGetRscPaletteCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscPaletteCount_t (_hRsc)

    mapGetRscPaletteNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscPaletteNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscPaletteNameUn(_hRsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscPaletteNameUn_t (_hRsc, _number, _name.buffer(), _size)


# Запросить цвет из CMYK - палитры
# index - порядковый номер цвета в палитре (с 1)
# hRsc - идентификатор классификатора карты
# возвращает цвет из 4 составляющих (С,M,Y,K)
# (каждая в интервале от 0 до 255)

    mapGetRscCMYKColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRscCMYKColor', maptype.HRSC, ctypes.c_int)
    def mapGetRscCMYKColor(_hRsc: maptype.HRSC, _index: int) -> int:
        return mapGetRscCMYKColor_t (_hRsc, _index)


# Установить цвет в CMYK - палитру
# color - 4 составляющих (С,M,Y,K)
# (каждая в интервале от 0 до 255)
# index - порядковый номер цвета в палитре (с 1)
# hRsc - идентификатор классификатора карты
# возвращает единицу
# При ошибке возвращает ноль

    mapSetRscCMYKColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscCMYKColor', maptype.HRSC, ctypes.c_ulong, ctypes.c_int)
    def mapSetRscCMYKColor(_hRsc: maptype.HRSC, _color: int, _index: int) -> int:
        return mapSetRscCMYKColor_t (_hRsc, _color, _index)


# Удалить палитру по порядковому номеру
# если палитра одна, она не удаляется)
# При ошибке возвращает ноль

    mapDeleteRscPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscPalette', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscPalette(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapDeleteRscPalette_t (_hRsc, _number)


# Kод шрифта - проставляется в параметры объекта (IMGTEXT: поле Type)
# (см. mapgdi.h) для ссылки на таблицу шрифтов.
# Запрос количества шрифтов
# При ошибке возвращает ноль
# hRsc - идентификатор классификатора карты

    mapGetFontCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFontCount', maptype.HRSC)
    def mapGetFontCount(_hRsc: maptype.HRSC) -> int:
        return mapGetFontCount_t (_hRsc)


# Добавить шрифт - возвращает код шрифта
# hRsc - идентификатор классификатора карты
# RSCFONT - см. maptype.h
# При ошибке возвращает ноль

    mapAppendFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendFont', maptype.HRSC, ctypes.POINTER(maptype.RSCFONT))
    def mapAppendFont(_hRsc: maptype.HRSC, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        return mapAppendFont_t (_hRsc, _font)


# Заменить шрифт - возвращает код шрифта
# hRsc - идентификатор классификатора карты
# index - порядковый номер шрифта (с 1)
# RSCFONT - см. maptype.h
# При ошибке возвращает ноль

    mapReplaceFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReplaceFont', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.RSCFONT))
    def mapReplaceFont(_hRsc: maptype.HRSC, _index: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        return mapReplaceFont_t (_hRsc, _index, _font)


# Запрос кода шрифта по порядковому номеру(c 1)
# hRsc - идентификатор классификатора карты
# number - номер шрифта
# При ошибке возвращает ноль

    mapGetFontCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFontCode', maptype.HRSC, ctypes.c_int)
    def mapGetFontCode(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetFontCode_t (_hRsc, _number)


# Запрос шрифта по порядковому номеру (c 1)
# Возвращает код шрифта
# hRsc - идентификатор классификатора карты
# number - номер шрифта
# RSCFONT - см. maptype.h
# При ошибке возвращает ноль

    mapGetFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFont', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.RSCFONT))
    def mapGetFont(_hRsc: maptype.HRSC, _number: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        return mapGetFont_t (_hRsc, _number, _font)


# Запрос шрифта по коду
# Возвращает порядковый номер шрифта (с 1)
# hRsc - идентификатор классификатора карты
# code - код шрифта
# RSCFONT - см. maptype.h
# При ошибке возвращает ноль

    mapGetFontByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFontByCode', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.RSCFONT))
    def mapGetFontByCode(_hRsc: maptype.HRSC, _code: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        return mapGetFontByCode_t (_hRsc, _code, _font)


# Дополнение параметров шрифта
# hRsc - идентификатор классификатора карты
# code - код шрифта
# Возвращает порядковый номер шрифта в таблице шрифтов
# При ошибке возвращает ноль

    mapSetFontByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFontByCode', maptype.HRSC, ctypes.c_int)
    def mapSetFontByCode(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapSetFontByCode_t (_hRsc, _code)


# Удалить шрифт по ключу , если нужно переназначить шрифт во внешнем
# виде объектов , newkey - ключ другого шрифта. Если newkey = 0,
# будет назначен шрифт по умолчанию.
# hRsc - идентификатор классификатора карты
# key - ключ шрифта
# newkey - ключ другого шрифта или 0
# При ошибке возвращает ноль

    mapDeleteFontByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteFontByKey', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapDeleteFontByKey(_hRsc: maptype.HRSC, _key: int, _newkey: int) -> int:
        return mapDeleteFontByKey_t (_hRsc, _key, _newkey)


# Проверка символьной формулы и вычисление ее значений
# допустимые операции: +,  -,  #,  /,
# (разделитель между операндами запятая ,)
# MAX(... ,...,   ),MIN(... ,...,   )- максимум, минимум
# ARM(... ,...,   ) - среднее арифметическое
# (разделитель между операндами у MAX, MIN, ARM - запятая ,)
# SIN,COS,TG,CTG - тригонометрические функции от углов в градусах и долях градуса
# SQRT2(),SQRT3(),POW2(),POW3() - корень и возведение во 2,3 степень
# PI - число PI
# P - Периметр объекта,
# S - Площадь объекта
# # - Указывает, что дальше идет код семантики, в которой лежит значение,
#     далее в ()значение по умолчанию.
# (пример: #1(0) - взять значение семантики 1, при отсутствии взять 0)
# цифры 0- 9,(разделитель точка .)
# Скобки (),[],{}
# Возвращает 0 при ошибке, и в переменной errorcode - код ошибки
# Открыть формулу для выполнения множества вычислений по объектам
# hrsc - идентификатор цифрового классификатора карты (RSC)
# formula - строка, содержащая формулу
# errorcode - код ошибки
# После завершения вычислений необходимо закрыть формулу функцией mapCloseFormula
# При ошибке возвращает ноль

    mapOpenFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenFormula', ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
    def mapOpenFormula(_formula: ctypes.c_char_p, _errorcode: ctypes.POINTER(ctypes.c_int)) -> ctypes.c_void_p:
        return mapOpenFormula_t (_formula, _errorcode)


# Вычислить значение открытой формулы для объекта
# info - идентификатор объекта карты, для которого выполняется вычисление
# hformula - идентификкатор формулы, открытой в mapOpenFormula
# value - поле для записи вычисленного значения
# errorcode - поле для записи кода ошибки
# При ошибке возвращает ноль

    mapCalculateFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCalculateFormula', maptype.HOBJ, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def mapCalculateFormula(_info: maptype.HOBJ, _hformula: ctypes.c_void_p, _value: ctypes.POINTER(ctypes.c_double), _errorcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCalculateFormula_t (_info, _hformula, _value, _errorcode)


# Закрыть формулу после выполнения вычислений
# hformula - идентификкатор формулы, открытой в mapOpenFormula

    mapCloseFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseFormula', ctypes.c_void_p)
    def mapCloseFormula(_hformula: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseFormula_t (_hformula)


# Вычисление формулы
# info - идентификатор объекта карты, для которого выполняется вычисление
# formula - строка, содержащая формулу
# value - поле для записи вычисленного значения
# errorcode - поле для записи кода ошибки
# Возвращает 0 при ошибке, и в переменной errno - код ошибки

    GetFormulaValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'GetFormulaValue', maptype.HOBJ, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def GetFormulaValue(_info: maptype.HOBJ, _formula: ctypes.c_char_p, _value: ctypes.POINTER(ctypes.c_double), _errorcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return GetFormulaValue_t (_info, _formula, _value, _errorcode)


# Проверка синтаксиса формулы
# HRSC rsc - идентификатор классификатора карты
# formula - строка, содержащая формулу
# errorcode - поле для записи кода ошибки
# Возвращает 0 при ошибке, и в переменной errno - код ошибки

    CheckFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'CheckFormula', maptype.HRSC, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
    def CheckFormula(_rsc: maptype.HRSC, _formula: ctypes.c_char_p, _errorcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return CheckFormula_t (_rsc, _formula, _errorcode)


# Запросить число поддерживаемых элементов (операций) формулы ("ABS", "ARM", "COS", ... "()")

    mapGetFormulaItemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFormulaItemCount')
    def mapGetFormulaItemCount() -> int:
        return mapGetFormulaItemCount_t ()


# Создание символьной строки с вставками по значениям семантики
# formula - символьная строка любого содержания source, в которой указаны места
# для вставки семантики следующим образом
# # - Указывает, что дальше идет ключевое слово или код семантики, в которой лежит значение
#     любого типа
#     далее в ()значение по умолчанию.
# (пример: #9(без названия) - взять значение семантики 9, при отсутствии
# вставить строчку "без названия"
# dest - указатель на буфер для размещения строки
#        размер буфера - размер строки + 256#количество вставок
# Возвращает 0 при ошибке, и в переменной errcode - код ошибки

    AgregateStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'AgregateStringUn', maptype.HRSC, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def AgregateStringUn(_hrsc: maptype.HRSC, _info: maptype.HOBJ, _formula: mapsyst.WTEXT, _dest: mapsyst.WTEXT, _destlength: int, _errcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return AgregateStringUn_t (_hrsc, _info, _formula.buffer(), _dest.buffer(), _destlength, _errcode)


# Запросить количество формул в классификаторе
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscFormulaCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscFormulaCount', maptype.HRSC)
    def mapGetRscFormulaCount(_hrsc: maptype.HRSC) -> int:
        return mapGetRscFormulaCount_t (_hrsc)


# Запросить код формулы в классификаторе по порядковому номеру с 1
# hRsc   - идентификатор классификатора карты
# number - порядковый номер формулы
# При ошибке возвращает ноль

    mapGetRscFormulaCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscFormulaCodeByNumber', maptype.HRSC, ctypes.c_int)
    def mapGetRscFormulaCodeByNumber(_hrsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscFormulaCodeByNumber_t (_hrsc, _number)


# Заполнить структуру описания формулы по коду формулы
# hRsc - идентификатор классификатора карты
# структура RSCFORMULA описана в maptype.h
# formulacode - код формулы
# При ошибке возвращает ноль

    mapGetRscDescribeFormulaByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscDescribeFormulaByCode', maptype.HRSC, ctypes.POINTER(maptype.RSCFORMULA), ctypes.c_int)
    def mapGetRscDescribeFormulaByCode(_hrsc: maptype.HRSC, _form: ctypes.POINTER(maptype.RSCFORMULA), _formulacode: int) -> int:
        return mapGetRscDescribeFormulaByCode_t (_hrsc, _form, _formulacode)


# Заменить текст формулы по коду формулы
# Проверка на синтактическую правильность не делается
# hRsc - идентификатор классификатора карты
# formulacode - код формулы
# textlength - длина формулы в байтах
# text - текст формулы
# При ошибке возвращает ноль

    mapReplaceRscFormulaText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReplaceRscFormulaText', maptype.HRSC, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapReplaceRscFormulaText(_hrsc: maptype.HRSC, _formulacode: int, _textlength: int, _text: mapsyst.WTEXT) -> int:
        return mapReplaceRscFormulaText_t (_hrsc, _formulacode, _textlength, _text.buffer())


# Назначить семантике формулу для расчетов
# Возвращает код формулы или ноль

    mapSetRscFormulaToSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscFormulaToSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscFormulaToSemantic(_hrsc: maptype.HRSC, _formulacode: int, _semanticcode: int) -> int:
        return mapSetRscFormulaToSemantic_t (_hrsc, _formulacode, _semanticcode)


# Удалить формулу для расчетов по коду формулы
# При ошибке возвращает ноль

    mapDeleteRscFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscFormula', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscFormula(_hrsc: maptype.HRSC, _formulacode: int) -> int:
        return mapDeleteRscFormula_t (_hrsc, _formulacode)


# Записать новую формулу - возвращает код формулы (можно назначить семантике в mapSetRscFormulaToSemantic)
# form - описание формулы
# text - текст формулы
# errcode - код ошибки при проверке формулы (maperr.rh)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapAppendRscFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscFormula', maptype.HRSC, ctypes.POINTER(maptype.RSCFORMULA), maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapAppendRscFormula(_hrsc: maptype.HRSC, _form: ctypes.POINTER(maptype.RSCFORMULA), _text: mapsyst.WTEXT, _errcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapAppendRscFormula_t (_hrsc, _form, _text.buffer(), _errcode)


# Запросить количество библиотек формул для семантики
# hRsc - идентификатор классификатора карты

    mapCountRscFormulaLibraries_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCountRscFormulaLibraries', maptype.HRSC)
    def mapCountRscFormulaLibraries(_hrsc: maptype.HRSC) -> int:
        return mapCountRscFormulaLibraries_t (_hrsc)


# Добавить библиотеку в список для вычисления значений семантики
# hRsc - идентификатор классификатора карты
# name - имя библиотеки
# message - 0 не выдавать сообщений
# Возвращает номер библиотеки в списке (1,...)
# При ошибке возвращает ноль

    mapOpenRscFormulaLibrary_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenRscFormulaLibrary', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapOpenRscFormulaLibrary(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _message: int) -> int:
        return mapOpenRscFormulaLibrary_t (_hrsc, _name.buffer(), _message)


# Запросить число записей в таблице кластеров
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabCtrCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabCtrCount', maptype.HRSC)
    def mapGetRscTabCtrCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabCtrCount_t (_hRsc)


# Запросить размер всех записей в таблице кластеров
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabCtrLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabCtrLength', maptype.HRSC)
    def mapGetRscTabCtrLength(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabCtrLength_t (_hRsc)


# Добавить запись в таблицу кластеров
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль, иначе количество кластеров

    mapAppendRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscTabCtr', maptype.HRSC, ctypes.POINTER(mapgdi.TABCTR))
    def mapAppendRscTabCtr(_hRsc: maptype.HRSC, _tabctr: ctypes.POINTER(mapgdi.TABCTR)) -> int:
        return mapAppendRscTabCtr_t (_hRsc, _tabctr)


# Удалить запись в таблице кластеров
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapDeleteRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscTabCtr', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscTabCtr(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapDeleteRscTabCtr_t (_hRsc, _number)


# Обновить запись в таблице кластеров
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapUpdateRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscTabCtr', maptype.HRSC, ctypes.c_int, ctypes.POINTER(mapgdi.TABCTR))
    def mapUpdateRscTabCtr(_hRsc: maptype.HRSC, _number: int, _tabctr: ctypes.POINTER(mapgdi.TABCTR)) -> int:
        return mapUpdateRscTabCtr_t (_hRsc, _number, _tabctr)


# Запросить число записей в таблице перекодировки семантик
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabRecCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabRecCount', maptype.HRSC)
    def mapGetRscTabRecCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabRecCount_t (_hRsc)


# Запросить размер всех записей в таблице перекодировки семантик
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabRecLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabRecLength', maptype.HRSC)
    def mapGetRscTabRecLength(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabRecLength_t (_hRsc)


# Добавить запись в таблицу перекодировки семантик
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль, иначе количество записей

    mapAppendRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscTabRec', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapAppendRscTabRec(_hRsc: maptype.HRSC, _tabrec: ctypes.c_char_p, _length: int) -> int:
        return mapAppendRscTabRec_t (_hRsc, _tabrec, _length)


# Удалить запись в таблице перекодировки семантик
# hRsc - идентификатор классификатора карты
# number - номер удаляемой записи с 1
# При ошибке возвращает ноль

    mapDeleteRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscTabRec', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscTabRec(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapDeleteRscTabRec_t (_hRsc, _number)


# Обновить запись в таблице перекодировки семантик
# hRsc - идентификатор классификатора карты
# number - номер записи с 1
# При ошибке возвращает ноль

    mapUpdateRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscTabRec', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapUpdateRscTabRec(_hRsc: maptype.HRSC, _number: int, _tabrec: ctypes.c_char_p, _length: int) -> int:
        return mapUpdateRscTabRec_t (_hRsc, _number, _tabrec, _length)


# Запросить число записей в таблице семантик - ссылок на БД
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabSemDbCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabSemDbCount', maptype.HRSC)
    def mapGetRscTabSemDbCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabSemDbCount_t (_hRsc)


# Запросить размер всех записей в таблице семантик - ссылок на БД
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabSemDbLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabSemDbLength', maptype.HRSC)
    def mapGetRscTabSemDbLength(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabSemDbLength_t (_hRsc)


# Добавить запись в таблицу семантик - ссылок на БД
# hRsc - идентификатор классификатора карты
# tab  - адрес добавляемой записи TABSEMDB
# length - длина записи в байтах
# При ошибке возвращает ноль, иначе количество записей

    mapAppendRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscTabSemDb', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapAppendRscTabSemDb(_hRsc: maptype.HRSC, _tab: ctypes.c_char_p, _length: int) -> int:
        return mapAppendRscTabSemDb_t (_hRsc, _tab, _length)


# Удалить запись в таблице семантик - ссылок на БД
# hRsc - идентификатор классификатора карты
# number - номер удаляемой записи с 1
# При ошибке возвращает ноль

    mapDeleteRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscTabSemDb', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscTabSemDb(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapDeleteRscTabSemDb_t (_hRsc, _number)


# Обновить запись в таблице семантик - ссылок на БД
# hRsc - идентификатор классификатора карты
# number - номер обновляемой записи с 1
# tab    - адрес обновляемой записи
# length - длина записи
# При ошибке возвращает ноль

    mapUpdateRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscTabSemDb', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapUpdateRscTabSemDb(_hRsc: maptype.HRSC, _number: int, _tab: ctypes.c_char_p, _length: int) -> int:
        return mapUpdateRscTabSemDb_t (_hRsc, _number, _tab, _length)


# Запросить число записей в таблице семантик - шаблонов строк
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabSemTmpCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabSemTmpCount', maptype.HRSC)
    def mapGetRscTabSemTmpCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabSemTmpCount_t (_hRsc)


# Запросить размер всех записей в таблице семантик - шаблонов строк
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabSemTmpLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabSemTmpLength', maptype.HRSC)
    def mapGetRscTabSemTmpLength(_hRsc: maptype.HRSC) -> int:
        return mapGetRscTabSemTmpLength_t (_hRsc)


# Запросить порядковый номер записи в таблице семантик -
# шаблонов строк по коду семантики
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapGetRscTabSemTmpNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabSemTmpNumber', maptype.HRSC, ctypes.c_int)
    def mapGetRscTabSemTmpNumber(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscTabSemTmpNumber_t (_hRsc, _code)


# Установить текст шаблона текстовой строки по коду семантики
# hRsc - идентификатор классификатора карты
# code - код семантики
# При ошибке возвращает ноль

    mapSetRscTabSemTmpTextByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscTabSemTmpTextByCode', maptype.HRSC, ctypes.c_int, maptype.PWCHAR)
    def mapSetRscTabSemTmpTextByCode(_hRsc: maptype.HRSC, _code: int, _text: mapsyst.WTEXT) -> int:
        return mapSetRscTabSemTmpTextByCode_t (_hRsc, _code, _text.buffer())


# Добавить запись в таблицу семантик - шаблонов строк
# hRsc - идентификатор классификатора карты
# tab - адрес записи TABSEMTMP
# length - размер записи в байтах
# При ошибке возвращает ноль, иначе количество записей

    mapAppendRscTabSemTmp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscTabSemTmp', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapAppendRscTabSemTmp(_hRsc: maptype.HRSC, _tab: ctypes.c_char_p, _length: int) -> int:
        return mapAppendRscTabSemTmp_t (_hRsc, _tab, _length)


# Удалить запись в таблице семантик - шаблонов строк
# hRsc - идентификатор классификатора карты
# number - номер записи с 1
# При ошибке возвращает ноль

    mapDeleteRscTabSemTmp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscTabSemTmp', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscTabSemTmp(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapDeleteRscTabSemTmp_t (_hRsc, _number)


# Обновить запись в таблице семантик - шаблонов строк
# hRsc - идентификатор классификатора карты
# number - номер записи с 1
# tab - адрес записи TABSEMTMP
# length - размер записи в байтах
# При ошибке возвращает ноль

    mapUpdateRscTabSemTmp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscTabSemTmp', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapUpdateRscTabSemTmp(_hRsc: maptype.HRSC, _number: int, _tab: ctypes.c_char_p, _length: int) -> int:
        return mapUpdateRscTabSemTmp_t (_hRsc, _number, _tab, _length)


# Проверить соответствие строки и шаблона строки
# hRsc - идентификатор классификатора карты
# code - код семантики
# value - строка значения семантики для проверки
# position - поле для записи номера символа, не соответствующего шаблону
# При ошибке возвращает ноль

    mapCheckSemanticTemplate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckSemanticTemplate', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapCheckSemanticTemplate(_hRsc: maptype.HRSC, _code: int, _value: mapsyst.WTEXT, _position: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCheckSemanticTemplate_t (_hRsc, _code, _value.buffer(), _position)


except Exception as e:
    print(e)
    acceslib = 0
