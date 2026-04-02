#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype

PACK_WIDTH = 1

#-----------------------------
class ELEMTREEE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Depth",ctypes.c_int),
                ("LayerNumber",ctypes.c_int),
                ("ParentNumber",ctypes.c_int),
                ("PictureIndex",ctypes.c_int),
                ("Code",ctypes.c_char*28)]
#-----------------------------


#-----------------------------
class ELEMTREEEEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Incode",ctypes.c_int),
                ("Depth",ctypes.c_int),
                ("LayerNumber",ctypes.c_int),
                ("ParentNumber",ctypes.c_int),
                ("PictureIndex",ctypes.c_int),
                ("Code",ctypes.c_char*28)]
#-----------------------------


#-----------------------------
class SERIALIMIT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Value",ctypes.c_double*256)]
#-----------------------------


#-----------------------------
class SERIATYPE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Excode",ctypes.c_uint),
                ("Local",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("FirstCode",ctypes.c_int),
                ("FirstCount",ctypes.c_int),
                ("SecondCode",ctypes.c_int),
                ("SecondCount",ctypes.c_int),
                ("SeriaTypeZero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SERIAPLACE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FirstCode",ctypes.c_int),
                ("FirstNumber",ctypes.c_int),
                ("SecondCode",ctypes.c_int),
                ("SecondNumber",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TEMPHDRAW(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("handle",maptype.HDRAW)]
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К СЕРИИ ОБ'ЕКТОВ    ++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Создать серию
# hRsc - идентификатор классификатора карты
# RSCOBJECT -  описание объекта (см. maptype.h)
# first, second - интервалы значений семантик серии
# Если серия по одной семантике, second = 0
# При ошибке возвращает 0, иначе - внутренний код объекта

#   mapSeriaCreate_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaCreate', maptype.HRSC, ctypes.POINTER(SERIALIMIT), ctypes.POINTER(SERIALIMIT), ctypes.POINTER(RSCOBJECT))
#   def mapSeriaCreate(_hRsc: maptype.HRSC, _first: ctypes.POINTER(SERIALIMIT), _second: ctypes.POINTER(SERIALIMIT), _object: ctypes.POINTER(RSCOBJECT)) -> int:
#       return mapSeriaCreate_t (_hRsc, _first, _second, _object)


# Обновить серию
# hRsc - идентификатор классификатора карты
# code - классификационный код объектов входящих в cерию
# local - локализация объектов серии ( LOCAL_POINT, ...)
# first, second - интервалы значений семантик серии
# Если серия по одной семантике, second = 0
# Если серии с таким кодом и локализацией нет , она создается
# Если такой объект или серия уже была - по возможности согласуются
# с новой(у новой приоритет), при сильных расхождениях - старая серия
# удаляется, новая создается - все объекты сохраняются
# Если серия по одной семантике second = 0
# При ошибке возвращает 0, иначе - внутренний код объекта

    mapSeriaUpdate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaUpdate', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(SERIALIMIT), ctypes.POINTER(SERIALIMIT))
    def mapSeriaUpdate(_hRsc: maptype.HRSC, _code: int, _local: int, _first: ctypes.POINTER(SERIALIMIT), _second: ctypes.POINTER(SERIALIMIT)) -> int:
        return mapSeriaUpdate_t (_hRsc, _code, _local, _first, _second)


# Добавить объект в существующую серию
# hRsc   - идентификатор классификатора карты
# object -  описание объекта (см. maptype.h)
# place  - место объекта в серии
# error  - код ошибки выполнения функции (1 - ошибка входных параметров, 2 - объект не найден, 3 - серия не найдена,
#          4 - первая семантика не соответствует серии, 5 - вторая семантика не соответствует серии, 6 - ошибка в описании серии,
#          7 - ошибка в таблице семантики, 8 - ошибка при добавлении объекта
# При ошибке возвращает 0, иначе - внутренний код объекта

#   mapSeriaAppendObjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaAppendObjectEx', maptype.HRSC, ctypes.POINTER(RSCOBJECT), ctypes.POINTER(SERIAPLACE), ctypes.POINTER(ctypes.c_int))
#   def mapSeriaAppendObjectEx(_hrsc: maptype.HRSC, _object: ctypes.POINTER(RSCOBJECT), _place: ctypes.POINTER(SERIAPLACE), _error: ctypes.POINTER(ctypes.c_int)) -> int:
#       return mapSeriaAppendObjectEx_t (_hrsc, _object, _place, _error)

#   mapSeriaAppendObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaAppendObject', maptype.HRSC, ctypes.POINTER(RSCOBJECT), ctypes.POINTER(SERIAPLACE))
#   def mapSeriaAppendObject(_hRsc: maptype.HRSC, _object: ctypes.POINTER(RSCOBJECT), _place: ctypes.POINTER(SERIAPLACE)) -> int:
#       return mapSeriaAppendObject_t (_hRsc, _object, _place)


# Удалить серию
# hRsc - идентификатор классификатора карты
# code - классификационный код объектов входящих в cерию
# local - локализация объектов серии ( LOCAL_POINT, ...)
# При ошибке возвращает ноль

    mapSeriaDelete_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaDelete', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSeriaDelete(_hRsc: maptype.HRSC, _code: int, _local: int) -> int:
        return mapSeriaDelete_t (_hRsc, _code, _local)


# Запросить информацию по серии
# hRsc - идентификатор классификатора карты
# code - классификационный код объектов входящих в cерию
# local - локализация объектов серии ( LOCAL_POINT, ...)
# При ошибке возвращает ноль

    mapSeriaDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaDescribe', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(SERIATYPE))
    def mapSeriaDescribe(_hRsc: maptype.HRSC, _code: int, _local: int, _seria: ctypes.POINTER(SERIATYPE)) -> int:
        return mapSeriaDescribe_t (_hRsc, _code, _local, _seria)


# Запросить информацию по значениям ограничителей семантики серии
# hRsc - идентификатор классификатора карты
# incode - внутренний код ( индекс ) любого объекта серии
# limit->Code - код запрашиваемой семантики
# При ошибке возвращает ноль, иначе номер семантики в серии (1 или 2)
# по адресу limit - должно быть памяти  sizeof(SERIALIMIT)

    mapSeriaDescribeLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaDescribeLimit', maptype.HRSC, ctypes.c_int, ctypes.POINTER(SERIALIMIT))
    def mapSeriaDescribeLimit(_hRsc: maptype.HRSC, _incode: int, _limit: ctypes.POINTER(SERIALIMIT)) -> int:
        return mapSeriaDescribeLimit_t (_hRsc, _incode, _limit)


# Назначить место объекта в серии (объект может повторяться)
# hRsc - идентификатор классификатора карты
# incode - внутренний код ( индекс ) объекта
# При ошибке возвращает ноль, иначе - внутренний код объекта

    mapSeriaSetObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaSetObject', maptype.HRSC, ctypes.c_int, ctypes.POINTER(SERIAPLACE))
    def mapSeriaSetObject(_hRsc: maptype.HRSC, _incode: int, _place: ctypes.POINTER(SERIAPLACE)) -> int:
        return mapSeriaSetObject_t (_hRsc, _incode, _place)


# Запросить внутренний код объекта по месту в серии
# hRsc - идентификатор классификатора карты
# code - классификационный код объектов входящих в cерию
# local - локализация объектов серии ( LOCAL_POINT, ...)
# При ошибке возвращает ноль, иначе - внутренний код объекта

    mapSeriaGetObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaGetObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(SERIAPLACE))
    def mapSeriaGetObject(_hRsc: maptype.HRSC, _code: int, _local: int, _place: ctypes.POINTER(SERIAPLACE)) -> int:
        return mapSeriaGetObject_t (_hRsc, _code, _local, _place)


# Назначить семантику всем объектам серии (не видовую)
# hRsc - идентификатор классификатора карты
# code - классификационный код объектов входящих в cерию
# local - локализация объектов серии ( LOCAL_POINT, ...)
# semanticcode - код семантики
# importance значимость семантики  см. maptype.h
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC) )
# При ошибке возвращает ноль

    mapSeriaSetObjectSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaSetObjectSemantic', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSeriaSetObjectSemantic(_hRsc: maptype.HRSC, _code: int, _local: int, _semanticcode: int, _importance: int) -> int:
        return mapSeriaSetObjectSemantic_t (_hRsc, _code, _local, _semanticcode, _importance)


# Создание копии существующей серии объектов со служебным кодом
# incode - внутренний код одного из объектов серии - источника
# Возвращает внутренний код первого объекта серии,
# При ошибке возвращает ноль

    mapSeriaCopyObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaCopyObjects', maptype.HRSC, ctypes.c_int)
    def mapSeriaCopyObjects(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapSeriaCopyObjects_t (_hRsc, _incode)


# назначить семантику объектy серии (не видовую)
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# semanticcode - код семантики
# importance значимость семантики  см. maptype.h
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC) )
# При ошибке возвращает ноль

    mapSeriaAppendSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaAppendSemanticObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSeriaAppendSemanticObject(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        return mapSeriaAppendSemanticObject_t (_hRsc, _incode, _semanticcode, _importance)


# Изменить значимость семантики для данного объекта серии
# (POSSIBLE_SEMANTIC или MUST_SEMANTIC)
# semanticcode - код семантики
# incode - внутренний код(индекс)объекта
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapSeriaUpdateSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaUpdateSemanticObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSeriaUpdateSemanticObject(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        return mapSeriaUpdateSemanticObject_t (_hRsc, _incode, _semanticcode, _importance)


# Обновить семантику объектов серии по исправленному объекту
# incode - внутренний код объекта c новой семантикой
# При ошибке возвращает ноль

    mapSeriaUpdateSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaUpdateSemantic', maptype.HRSC, ctypes.c_int)
    def mapSeriaUpdateSemantic(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapSeriaUpdateSemantic_t (_hRsc, _incode)


# Обновить семантику объектов серии по исправленному объекту
# incode - внутренний код объекта c новой семантикой
# При ошибке возвращает ноль

    mapSeriaUpdateSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaUpdateSemantic', maptype.HRSC, ctypes.c_int)
    def mapSeriaUpdateSemantic(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapSeriaUpdateSemantic_t (_hRsc, _incode)


# Добавить объект серии
# hRsc - идентификатор классификатора карты
# RSCOBJ -  описание объекта (см. maprsc.h)
# При ошибке возвращает 0, иначе - внутренний код объекта

#   mapSeriaAddObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaAddObject', maptype.HRSC, ctypes.POINTER(RSCOBJ))
#   def mapSeriaAddObject(_hRsc: maptype.HRSC, _object: ctypes.POINTER(RSCOBJ)) -> int:
#       return mapSeriaAddObject_t (_hRsc, _object)


# Обновить локализацию код серии
# hRsc - идентификатор классификатора карты
# limit описание серии (см. rsc.h)
# При ошибке возвращает ноль

#   mapSeriaUpdateLocal_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaUpdateLocal', maptype.HRSC, ctypes.POINTER(TABLIM), ctypes.c_int)
#   def mapSeriaUpdateLocal(_hRsc: maptype.HRSC, _limit: ctypes.POINTER(TABLIM), _local: int) -> int:
#       return mapSeriaUpdateLocal_t (_hRsc, _limit, _local)


# Обновить внешний код серии
# hRsc - идентификатор классификатора карты
# limit описание серии (см. rsc.h)
# При ошибке возвращает ноль

#   mapSeriaUpdateCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaUpdateCode', maptype.HRSC, ctypes.POINTER(TABLIM), ctypes.c_int)
#   def mapSeriaUpdateCode(_hRsc: maptype.HRSC, _limit: ctypes.POINTER(TABLIM), _excode: int) -> int:
#       return mapSeriaUpdateCode_t (_hRsc, _limit, _excode)


# Обновить объект входящий в серию по внутреннему коду и общей информации
# серии - поставить назначенное расширение (контроля за однозначностью нет),
# не проверяет единственность сочетания кода и локализации
# При ошибке возвращает ноль

#   mapSeriaUpdateObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSeriaUpdateObject', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(TABLIM), ctypes.POINTER(TABPOS))
#   def mapSeriaUpdateObject(_hRsc: maptype.HRSC, _incode: int, _extend: int, _limit: ctypes.POINTER(TABLIM), _possemantic: ctypes.POINTER(TABPOS)) -> int:
#       return mapSeriaUpdateObject_t (_hRsc, _incode, _extend, _limit, _possemantic)


# Удалить объект из серии - возвращает внутренний код удаленного объекта
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта
# При ошибке возвращает ноль

    mapSeriaDeleteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeriaDeleteObject', maptype.HRSC, ctypes.c_int)
    def mapSeriaDeleteObject(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapSeriaDeleteObject_t (_hRsc, _incode)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ДОПОЛНИТЕЛЬНЫХ ФУНКЦИЙ ДОСТУПА К ПАЛИТРЕ    ++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Добавить палитру
# hRsc - идентификатор классификатора карты
# palette - цвета палитры,count - количество цветов в палитре (16,32,64,256)
# name    - название палитры
# При ошибке возвращает ноль иначе 1

    mapRscAppendPaletteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscAppendPaletteUn', maptype.HRSC, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, maptype.PWCHAR)
    def mapRscAppendPaletteUn(_hRsc: maptype.HRSC, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _wname: mapsyst.WTEXT) -> int:
        return mapRscAppendPaletteUn_t (_hRsc, _palette, _count, _wname.buffer())

    mapRscAppendPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscAppendPalette', maptype.HRSC, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_char_p)
    def mapRscAppendPalette(_hRsc: maptype.HRSC, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _name: ctypes.c_char_p) -> int:
        return mapRscAppendPalette_t (_hRsc, _palette, _count, _name)


# Установить количество цветов в классификаторе
# hRsc - идентификатор классификатора карты
# count - количество цветов в палитре (16,32,64,256)
# При ошибке возвращает ноль иначе 1

    mapRscSetColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscSetColorCount', maptype.HRSC, ctypes.c_int)
    def mapRscSetColorCount(_hRsc: maptype.HRSC, _count: int) -> int:
        return mapRscSetColorCount_t (_hRsc, _count)


# Проверить использование данного цвета в параметрах объекта
# hRsc - идентификатор классификатора карты
# color -  младший байт содержит номер индекса палитры карты (c 0 до 255),
#          старший байт равен 0x0F (признак указания индексного цвета)
# function - номер функции отображения (mapgdi.h)
# param - адрес параметров
# Возвращает: 1 - используется, 0 - не используется

    mapRscCheckParamColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscCheckParamColor', maptype.HRSC, maptype.COLORREF, ctypes.c_int, ctypes.c_char_p)
    def mapRscCheckParamColor(_hRsc: maptype.HRSC, _color: maptype.COLORREF, _function: int, _param: ctypes.c_char_p) -> int:
        return mapRscCheckParamColor_t (_hRsc, _color, _function, _param)


# Проверить параметры объекта на использование данного цвета
# hRsc - идентификатор классификатора карты
# colorindex - номер индекса палитры карты (c 1 до 256)
# incode - внутренний код (порядковый номер ) объекта (начинается с 1)
# viewtype -вид отображения  0 - экранный, 1 - принтерный
# возвращает 0 - цвет не используется, 1 - используется

    mapRscCheckObjectColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscCheckObjectColor', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapRscCheckObjectColor(_hRsc: maptype.HRSC, _colorindex: int, _incode: int, _viewtype: int) -> int:
        return mapRscCheckObjectColor_t (_hRsc, _colorindex, _incode, _viewtype)


# Проверить использование данного цвета в параметрах объекта
# hRsc - идентификатор классификатора карты
# color -  младший байт содержит номер индекса палитры карты (c 0 до 255),
#          старший байт равен 0x0F (признак указания индексного цвета)
# function - номер функции отображения (mapgdi.h)
# param - адрес параметров
# Возвращает: 1 - используется, 0 - не используется

    mapRscCheckParamColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscCheckParamColor', maptype.HRSC, maptype.COLORREF, ctypes.c_int, ctypes.c_char_p)
    def mapRscCheckParamColor(_hRsc: maptype.HRSC, _color: maptype.COLORREF, _function: int, _param: ctypes.c_char_p) -> int:
        return mapRscCheckParamColor_t (_hRsc, _color, _function, _param)


# Заменить в параметрах объекта указанный номер индекса палитры карты
# на другой
# hRsc - идентификатор классификатора карты
# oldcolorindex - существующий номер индекса палитры карты (c 1 до 256)
# newcolorindex - существующий номер индекса палитры карты (c 1 до 256)
# incode - внутренний код (порядковый номер ) объекта (начинается с 1)
# viewtype -вид отображения  0 - экранный, 1 - принтерный
# возвращает 0 - цвет не используется, 1 - используется
# При ошибке возвращает ноль

    mapRscReplaceObjectColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscReplaceObjectColor', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapRscReplaceObjectColor(_hRsc: maptype.HRSC, _oldcolorindex: int, _newcolorindex: int, _incode: int, _viewtype: int) -> int:
        return mapRscReplaceObjectColor_t (_hRsc, _oldcolorindex, _newcolorindex, _incode, _viewtype)


# Запрос значения цвета по индексу в палитре по умолчанию
# color - цвет в COLORREF
# index - порядковый номер цвета в палитре (с 1)
# hRsc - идентификатор классификатора карты
# возвращает цвет в COLORREF
# При ошибке возвращает ноль

    mapGetRscDefaultColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRscDefaultColor', maptype.HRSC, ctypes.c_int)
    def mapGetRscDefaultColor(_hRsc: maptype.HRSC, _index: int) -> maptype.COLORREF:
        return mapGetRscDefaultColor_t (_hRsc, _index)


# Преобразование палитры из RGB в CMYK
# count - количество цветов
# rgb - адрес палитры(COLORREF)
# cmyk - адрес, для размещения палитры CMYK (4 байта на цвет)
# При ошибке возвращает ноль

    mapCreateRscCMYK_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscCMYK', maptype.HRSC, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)
    def mapCreateRscCMYK(_hRsc: maptype.HRSC, _count: int, _rgb: ctypes.c_char_p, _cmyk: ctypes.c_char_p) -> int:
        return mapCreateRscCMYK_t (_hRsc, _count, _rgb, _cmyk)


# Установить палитру CMYK
# count - количество цветов
# cmyk - адрес палитры CMYK (4 байта на цвет)
# При ошибке возвращает ноль

    mapSetRscCMYK_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscCMYK', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscCMYK(_hRsc: maptype.HRSC, _count: int, _cmyk: ctypes.c_char_p) -> int:
        return mapSetRscCMYK_t (_hRsc, _count, _cmyk)


# Переустановить палитру
# number порядковый номер палитры (с 1 )
# colorref - цвета
# count количество цветов в colorref
# При ошибке возвращает ноль

    mapUpdateRscPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscPalette', maptype.HRSC, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapUpdateRscPalette(_hRsc: maptype.HRSC, _number: int, _colorref: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapUpdateRscPalette_t (_hRsc, _number, _colorref, _count)


# Установить имя существующей палитры в UNICODE по номеру (с 1)
# size длина имени в байтах
# Возвращает длину имени палитры

    mapSetRscPaletteNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscPaletteNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSetRscPaletteNameUn(_hRsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSetRscPaletteNameUn_t (_hRsc, _number, _name.buffer(), _size)


# Установить имя палитры по номеру (с 1)
# При ошибке возвращает ноль

    mapSetRscPaletteName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscPaletteName', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscPaletteName(_hRsc: maptype.HRSC, _number: int, _name: ctypes.c_char_p) -> int:
        return mapSetRscPaletteName_t (_hRsc, _number, _name)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++  ОПИСАНИЕ ДОПОЛНИТЕЛЬНЫХ ФУНКЦИЙ ДОСТУПА К БИБЛИОТЕКАМ  +++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Запросить количество библиотек пользователя
# hRsc - идентификатор классификатора карты
# При ошибке или отсутствии подключенных библиотек возвращает ноль

    mapGetRscImlCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlCount', maptype.HRSC)
    def mapGetRscImlCount(_hRsc: maptype.HRSC) -> int:
        return mapGetRscImlCount_t (_hRsc)


# Запросить порядковый номер библиотеки пользователя(с 1)
# hRsc - идентификатор классификатора карты
# соde - код библиотеки
# При ошибке возвращает ноль

    mapGetRscImlOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlOrder', maptype.HRSC, ctypes.c_int)
    def mapGetRscImlOrder(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapGetRscImlOrder_t (_hRsc, _code)


# Запрос индекса библиотеки (с 1) по порядковому номеру
# При ошибке возвращает ноль

    mapGetRscImlIndex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlIndex', maptype.HRSC, ctypes.c_int)
    def mapGetRscImlIndex(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscImlIndex_t (_hRsc, _number)


# Запрос кода по порядковому номеру библиотеки (c 1)
# При ошибке возвращает ноль

    mapGetRscImlCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlCode', maptype.HRSC, ctypes.c_int)
    def mapGetRscImlCode(_hRsc: maptype.HRSC, _number: int) -> int:
        return mapGetRscImlCode_t (_hRsc, _number)


# Запросить имя библиотеки по порядковому номеру (c 1)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает пустую строку

    mapGetRscImlNameDLLUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlNameDLLUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscImlNameDLLUn(_hRsc: maptype.HRSC, _number: int, _wname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscImlNameDLLUn_t (_hRsc, _number, _wname.buffer(), _size)


# Запросить условное имя библиотеки по порядковому номеру (c 1)
# hRsc - идентификатор классификатора карты
# При ошибке возвращает пустую строку

    mapGetRscImlNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscImlNameUn', maptype.HRSC, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscImlNameUn(_hRsc: maptype.HRSC, _number: int, _wname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRscImlNameUn_t (_hRsc, _number, _wname.buffer(), _size)


# Добавить библиотеку
# hRsc - идентификатор классификатора карты
# nameDll - имя библиотеки
# nameUser - условное имя
# Возвращает код библиотеки
# При ошибке возвращает 0

    mapAppendRscImlUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscImlUn', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendRscImlUn(_hRsc: maptype.HRSC, _wnameDll: mapsyst.WTEXT, _wnameUser: mapsyst.WTEXT) -> int:
        return mapAppendRscImlUn_t (_hRsc, _wnameDll.buffer(), _wnameUser.buffer())

    mapAppendRscIml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendRscIml', maptype.HRSC, ctypes.c_char_p, ctypes.c_char_p)
    def mapAppendRscIml(_hRsc: maptype.HRSC, _nameDll: ctypes.c_char_p, _nameUser: ctypes.c_char_p) -> int:
        return mapAppendRscIml_t (_hRsc, _nameDll, _nameUser)


# Удалить библиотеку по коду
# hRsc - идентификатор классификатора карты
# соde - код библиотеки
# При ошибке возвращает ноль

    mapDeleteRscIml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscIml', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscIml(_hRsc: maptype.HRSC, _code: int) -> int:
        return mapDeleteRscIml_t (_hRsc, _code)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ПОСТРОЕНИЯ ДЕРЕВА ОБЪЕКТОВ КЛАССИФИКАТОРА  ++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Для использования дерева объектов необходимо:
# Запросить максимальный размер
# Выделить память под размещение нужного количества структур ELEMTREEE/ELEMTREEEEX,
# Вызвать функцию построения дерева
# Заполнять элементы по порядку. Для слоя incode равно 0
# У каждого элемента указан номер элемента - родителя
# Посчитать максимальное число элементов дерева объектов

    mapCountRscTreeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCountRscTreeObject', maptype.HRSC)
    def mapCountRscTreeObject(_hRsc: maptype.HRSC) -> int:
        return mapCountRscTreeObject_t (_hRsc)


# Выгрузить дерево построенное по Rsc и фильтру в выделенную область памяти
# hRsc - идентификатор классификатора карты
# hSelect - идентификатор фильтра (может быть 0)
# size    - размер выделенной области для размещения дерева(в байтах)
# elemtree - указатель на выделенную область
# Возвращает точное количество элементов дерева
# При ошибке возвращает 0

    mapBuildRscTreeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRscTreeEx', maptype.HRSC, maptype.HSELECT, ctypes.c_int, ctypes.POINTER(ELEMTREEEEX))
    def mapBuildRscTreeEx(_hRsc: maptype.HRSC, _hSelect: maptype.HSELECT, _size: int, _elemtree: ctypes.POINTER(ELEMTREEEEX)) -> int:
        return mapBuildRscTreeEx_t (_hRsc, _hSelect, _size, _elemtree)

    mapBuildRscTree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRscTree', maptype.HRSC, maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ELEMTREEE))
    def mapBuildRscTree(_hRsc: maptype.HRSC, _hSelect: maptype.HSELECT, _size: int, _elemtree: ctypes.POINTER(ELEMTREEE)) -> int:
        return mapBuildRscTree_t (_hRsc, _hSelect, _size, _elemtree)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ РЕДАКТИРОВАНИЕ ПАРАМЕТРОВ ФУНКЦИИ ОТОБРАЖЕНИЯ ОБЪЕКТОВ      ++++
# +++++                 НАБОР ПРИМИТИВОВ DRAW                       ++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Создать идентификатор параметров набора примитивов
# HDRW - maptype.h
# Выделяет память для работы с набором примитивов
# После использования освободить с помощью функции mapFreeDraw()
# hDrw - идентификатор набора примитивов

    mapCreateDraw_t = mapsyst.GetProcAddress(acceslib,maptype.HDRAW,'mapCreateDraw')
    def mapCreateDraw() -> maptype.HDRAW:
        return mapCreateDraw_t ()


# Освободить параметры набора примитивов
# hDrw - идентификатор набора примитивов
# Освобождает память для работы с набором примитивов
# При ошибке возвращает 0

    mapFreeDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFreeDraw', maptype.HDRAW)
    def mapFreeDraw(_hDrw: maptype.HDRAW) -> int:
        return mapFreeDraw_t (_hDrw)


# Создать копию параметров набора примитивов
# HDRW - maptype.h
# Выделяет память для работы с набором примитивов
# После использования освободить с помощью функции mapFreeDraw()
# hDrw - идентификатор набора примитивов

    mapCreateCopyDraw_t = mapsyst.GetProcAddress(acceslib,maptype.HDRAW,'mapCreateCopyDraw', maptype.HDRAW)
    def mapCreateCopyDraw(_hDrw: maptype.HDRAW) -> maptype.HDRAW:
        return mapCreateCopyDraw_t (_hDrw)


# Прочитать копию набора графических примитивов
# dest - идентификатор набора примитивов, в который копируется графическое описание
# src - идентификатор набора примитивов, из которого копируется графическое описание
# При ошибке возвращает 0

    mapReadCopyDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadCopyDraw', maptype.HDRAW, maptype.HDRAW)
    def mapReadCopyDraw(_dest: maptype.HDRAW, _src: maptype.HDRAW) -> int:
        return mapReadCopyDraw_t (_dest, _src)


# Загрузить параметры в набор примитивов
# hDrw - идентификатор набора примитивов
# param - память, где находятся параметры
# number - номер функции типа IMG_XXXXXXX (см. MAPGDI.H)
# length - длина загружаемых параметров
# При ошибке возвращает 0

    mapCopyMemoryToDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMemoryToDraw', maptype.HDRAW, ctypes.c_int, ctypes.c_char_p)
    def mapCopyMemoryToDraw(_hDrw: maptype.HDRAW, _number: int, _param: ctypes.c_char_p) -> int:
        return mapCopyMemoryToDraw_t (_hDrw, _number, _param)


# Выгрузить набор примитивов в память
# hDrw - идентификатор набора примитивов
# buffer - адрес памяти куда выгружаются параметры
# length - размер памяти для выгрузки не менее mapDrawLength()
# При ошибке возвращает 0

    mapCopyDrawToMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyDrawToMemory', maptype.HDRAW, ctypes.c_char_p, ctypes.c_int)
    def mapCopyDrawToMemory(_hDrw: maptype.HDRAW, _buffer: ctypes.c_char_p, _length: int) -> int:
        return mapCopyDrawToMemory_t (_hDrw, _buffer, _length)


# Запросить общую длину набора примитивов
# hDrw - идентификатор набора примитивов
# При ошибке возвращает 0

    mapAllDrawLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAllDrawLength', maptype.HDRAW)
    def mapAllDrawLength(_hDrw: maptype.HDRAW) -> int:
        return mapAllDrawLength_t (_hDrw)


# Запросить количество элементов набора примитивов
# hDrw - идентификатор набора примитивов
# При ошибке возвращает 0

    mapDrawElementCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawElementCount', maptype.HDRAW)
    def mapDrawElementCount(_hDrw: maptype.HDRAW) -> int:
        return mapDrawElementCount_t (_hDrw)

    mapRscDrawCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscDrawCount', maptype.HDRAW)
    def mapRscDrawCount(_hDrw: maptype.HDRAW) -> int:
        return mapRscDrawCount_t (_hDrw)


# Запросить вид элемента набора примитивов
# по его номеру (от 1 до mapDrawCount())
# hDrw - идентификатор набора примитивов
# Возвращает номер функции типа IMG_XXXXXXX (см. MAPGDI.H)
# При ошибке возвращает 0

    mapDrawElementImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawElementImage', maptype.HDRAW, ctypes.c_int)
    def mapDrawElementImage(_hDrw: maptype.HDRAW, _number: int) -> int:
        return mapDrawElementImage_t (_hDrw, _number)


# Запросить длину параметров элемента набора примитивов
# по его номеру (от 1 до mapDrawCount())
# hDrw - идентификатор набора примитивов
# При ошибке возвращает 0

    mapDrawElementLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawElementLength', maptype.HDRAW, ctypes.c_int)
    def mapDrawElementLength(_hDrw: maptype.HDRAW, _number: int) -> int:
        return mapDrawElementLength_t (_hDrw, _number)


# Добавить элемент в набор примитивов
# hDrw - идентификатор набора примитивов
# image - вид элемента (см. MAPGDI.H)
# param - адрес параметров элемента
# При ошибке возвращает ноль,иначе - число элементов в записи

    mapAppendElementDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendElementDraw', maptype.HDRAW, ctypes.c_int, ctypes.c_char_p)
    def mapAppendElementDraw(_hDrw: maptype.HDRAW, _image: int, _parm: ctypes.c_char_p) -> int:
        return mapAppendElementDraw_t (_hDrw, _image, _parm)


# Добавить элемент в набор примитивов c инициализацией параметров
# hDrw - идентификатор набора примитивов
# image - вид элемента (см. MAPGDI.H)
# При ошибке возвращает ноль,иначе - число элементов в записи

    mapAppendElementDrawWithInit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendElementDrawWithInit', maptype.HDRAW, ctypes.c_int)
    def mapAppendElementDrawWithInit(_hDrw: maptype.HDRAW, _image: int) -> int:
        return mapAppendElementDrawWithInit_t (_hDrw, _image)


# Заменить примитив
# hDrw - идентификатор набора примитивов
# number - номер заменяемого примитива (от 1 до mapDrawCount())
# image - вид элемента (см. MAPGDI.H)
# param - адрес параметров элемента
# При ошибке возвращает ноль,иначе номер примитива в записи

    mapReplaceElementDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReplaceElementDraw', maptype.HDRAW, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapReplaceElementDraw(_hDrw: maptype.HDRAW, _number: int, _image: int, _parm: ctypes.c_char_p) -> int:
        return mapReplaceElementDraw_t (_hDrw, _number, _image, _parm)


# Заменить примитив  по номеру  c инициализацией параметров
# hDrw - идентификатор набора примитивов
# number - номер заменяемого примитива (от 1 до mapDrawCount())
# image - вид элемента (см. MAPGDI.H)
# При ошибке возвращает ноль,иначе номер примитива в записи

    mapReplaceElementWithInitDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReplaceElementWithInitDraw', maptype.HDRAW, ctypes.c_int, ctypes.c_int)
    def mapReplaceElementWithInitDraw(_hDrw: maptype.HDRAW, _number: int, _image: int) -> int:
        return mapReplaceElementWithInitDraw_t (_hDrw, _number, _image)


# Передвинуть примитив
# hDrw - идентификатор набора примитивов
# oldnumber - место откуда взять примитив (от 1 до mapDrawCount())
# newnumber - место куда положить примитив (от 1 до mapDrawCount())
# При ошибке возвращает 0

    mapMoveElementDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveElementDraw', maptype.HDRAW, ctypes.c_int, ctypes.c_int)
    def mapMoveElementDraw(_hDrw: maptype.HDRAW, _oldnumber: int, _newnumber: int) -> int:
        return mapMoveElementDraw_t (_hDrw, _oldnumber, _newnumber)


# Удалить все элементы графического описания объекта
# hDrw - идентификатор набора примитивов
# При ошибке возвращает ноль

    mapRscClearDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRscClearDraw', maptype.HDRAW)
    def mapRscClearDraw(_hDrw: maptype.HDRAW) -> int:
        return mapRscClearDraw_t (_hDrw)


# Удалить элемент графического описания объекта
# hDrw - идентификатор набора примитивов
# number - номер элемента (начиная с 1)
# При ошибке возвращает ноль

    mapDeleteElementDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteElementDraw', maptype.HDRAW, ctypes.c_int)
    def mapDeleteElementDraw(_hDrw: maptype.HDRAW, _number: int) -> int:
        return mapDeleteElementDraw_t (_hDrw, _number)


# Добавить элементом графического описания объекта точечный знак IMGMULTIMARK
# созданный по ВМР - файлу
# name - имя файла
# В BMP не более 256 цветов (не сжатое)
# Размеры более 32#32 - обрезаются
# При ошибке возвращает ноль

    mapAppendBMPtoDrawUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendBMPtoDrawUn', maptype.HDRAW, maptype.PWCHAR)
    def mapAppendBMPtoDrawUn(_hDrw: maptype.HDRAW, _name: mapsyst.WTEXT) -> int:
        return mapAppendBMPtoDrawUn_t (_hDrw, _name.buffer())

    mapAppendBMPtoDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendBMPtoDraw', maptype.HDRAW, ctypes.c_char_p)
    def mapAppendBMPtoDraw(_hDrw: maptype.HDRAW, _name: ctypes.c_char_p) -> int:
        return mapAppendBMPtoDraw_t (_hDrw, _name)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++                 Дополнительные функции                      ++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Запрос флага объекта из таблицы по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# При ошибке возвращает ноль

    mapGetRscTabObjectFlags_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscTabObjectFlags', maptype.HRSC, ctypes.c_int)
    def mapGetRscTabObjectFlags(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscTabObjectFlags_t (_hRsc, _incode)


# Установка флага объекта из таблицы по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# flag - комбинация флагов из FLFORRSC (maprsc.h)
# При ошибке возвращает ноль

    mapSetRscTabObjectFlags_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscTabObjectFlags', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscTabObjectFlags(_hRsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        return mapSetRscTabObjectFlags_t (_hRsc, _incode, _flag)


# Запрос индекса верхнeй границы видимости по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# Возвращает индекс от 0 до 15

    mapGetRscObjectTop_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectTop', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectTop(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectTop_t (_hRsc, _incode)


# Запрос индекса нижней границы видимости по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# Возвращает индекс от 0 до 15

    mapGetRscObjectBottom_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectBottom', maptype.HRSC, ctypes.c_int)
    def mapGetRscObjectBottom(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapGetRscObjectBottom_t (_hRsc, _incode)


# Установка индекса верхнeй границы видимости по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# bottom индекс от 0 до 15
# Возвращает bottom, либо 0

    mapSetRscObjectTop_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectTop', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectTop(_hRsc: maptype.HRSC, _incode: int, _bottom: int) -> int:
        return mapSetRscObjectTop_t (_hRsc, _incode, _bottom)


# Установка индекса нижней границы видимости по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# top индекс от 0 до 15
# Возвращает top, либо 0

    mapSetRscObjectBottom_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectBottom', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectBottom(_hRsc: maptype.HRSC, _incode: int, _top: int) -> int:
        return mapSetRscObjectBottom_t (_hRsc, _incode, _top)


# Записать флаг включения границ видимости объекта
# includetop - 0 - не включать верхнюю границу, 1 - включать
# includebot - 0 - не включать нижнюю границу, 1 - включать
# hRsc - идентификатор классификатора карты
# incode - внутренний код
# Возвращает 1, либо 0

    mapSetRscObjBotTopInclude_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjBotTopInclude', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjBotTopInclude(_hRsc: maptype.HRSC, _incode: int, _includetop: int, _includebottom: int) -> int:
        return mapSetRscObjBotTopInclude_t (_hRsc, _incode, _includetop, _includebottom)


# Установить направление цифрования объекта по внутреннему коду
# hRsc - идентификатор классификатора карты
# incode - порядковый номер объекта (с 1)
# direct - индекс от 0 до 4
# При ошибке возвращает ноль

    mapSetRscObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectDirect', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapSetRscObjectDirect(_hRsc: maptype.HRSC, _incode: int, _direct: int) -> int:
        return mapSetRscObjectDirect_t (_hRsc, _incode, _direct)


# Обновить описание либо добавить описание связанной подписи
# incode внутренний код объекта
# semanticcode - код семантики
# ident - идентификатор подписи (запрашивать mapGetRscObjectIdent)
# char # prefix (постоянный префикс для подписи 7 байт с 0) или 0
# decimal - количество знаков после, в подписи цифр
# Возвращает идентификатор подписи, либо 0

    mapUpdateRscObjectRelate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscObjectRelate', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapUpdateRscObjectRelate(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _ident: int, _prefix: ctypes.c_char_p, _decimal: int) -> int:
        return mapUpdateRscObjectRelate_t (_hRsc, _incode, _semanticcode, _ident, _prefix, _decimal)


# Обновить описание либо добавить описание связанной подписи
# incode - внутренний код объекта
# semanticcode - код семантики
# ident - идентификатор подписи (запрашивать mapGetRscObjectIdent)
# prefix - значениe из классификатора семантики 32858 - список сокращений или 0
# postfix - значениe из классификатора семантики 32858 - список сокращений или 0
# decimal - количество знаков после "," в подписи цифр
# Возвращает идентификатор подписи ident, либо 0

    mapUpdateRscObjectAbbrRelate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscObjectAbbrRelate', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapUpdateRscObjectAbbrRelate(_hRsc: maptype.HRSC, _incode: int, _semanticcode: int, _ident: int, _prefix: int, _postfix: int, _decimal: int) -> int:
        return mapUpdateRscObjectAbbrRelate_t (_hRsc, _incode, _semanticcode, _ident, _prefix, _postfix, _decimal)


# Запрос порядкового номера элемента классификатора по имени (порядковый номер с 0)
# Type - тип запроса : для слоя по имени - 1,
#                      для слоя по короткому имени - 2,
#                      для семантики по имени - 3,
#                      для семантики по короткому имени - 4,
#                      для объекта по короткому имени   - 5
# При отсутствии - 0, код ошибки IDS_NOTFOUND
# Возвращает порядковый номер элемента (для слоя с 0, для семантики и объекта с 1)

    mapGetRscElementbyName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscElementbyName', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscElementbyName(_hRsc: maptype.HRSC, _name: ctypes.c_char_p, _type: int) -> int:
        return mapGetRscElementbyName_t (_hRsc, _name, _type)


# Обновить локализацию и код объекта
# Проверка на наличие серии не делается
# Замещается локализация и код возможных и обязательных семантик,
# incode - внутренний код объекта
# code -  код объекта
# local - локализация объекта
# Возвращает порядковый номер объекта или 0

    mapUpdateRscObjectCodeLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscObjectCodeLocal', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapUpdateRscObjectCodeLocal(_hRsc: maptype.HRSC, _incode: int, _code: int, _local: int) -> int:
        return mapUpdateRscObjectCodeLocal_t (_hRsc, _incode, _code, _local)


# Запрос максимального идентификатора объектов
# При ошибке возвращает ноль

    mapGetRscMaxKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscMaxKey', maptype.HRSC)
    def mapGetRscMaxKey(_hRsc: maptype.HRSC) -> int:
        return mapGetRscMaxKey_t (_hRsc)


# Установить тип классификатора
# hRsc    - идентификатор классификатора карты,
# str - тип классификатора
# При ошибке возвращает ноль

    mapSetRscType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscType', maptype.HRSC, ctypes.c_char_p)
    def mapSetRscType(_hRsc: maptype.HRSC, _str: ctypes.c_char_p) -> int:
        return mapSetRscType_t (_hRsc, _str)


# Установка - возврат типа кодов объектов, используемых в классификаторе
# type 0 - код числовой, 1- в качестве кода, берется ключ(короткое имя объекта)
# При ошибке возвращает ноль

    mapSetRscObjectCodeType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectCodeType', maptype.HRSC, ctypes.c_int)
    def mapSetRscObjectCodeType(_hRsc: maptype.HRSC, _type: int) -> int:
        return mapSetRscObjectCodeType_t (_hRsc, _type)


# Запрос типа кодов объектов, используемых в классификаторе
# Возвращает 0 - код числовой, 1- в качестве кода, берется ключ(короткое имя объекта)

    mapGetRscObjectCodeType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjectCodeType', maptype.HRSC)
    def mapGetRscObjectCodeType(_hRsc: maptype.HRSC) -> int:
        return mapGetRscObjectCodeType_t (_hRsc)


# Установить стиль классификатора карты
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapSetRscStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscStyle', maptype.HRSC)
    def mapSetRscStyle(_hRsc: maptype.HRSC) -> int:
        return mapSetRscStyle_t (_hRsc)


# Установить изменения классификатора карты
# hRsc - идентификатор классификатора карты
# При ошибке возвращает ноль

    mapSetRscModifyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscModifyFlag', maptype.HRSC)
    def mapSetRscModifyFlag(_hRsc: maptype.HRSC) -> int:
        return mapSetRscModifyFlag_t (_hRsc)


# Запрос семантика объекта сортирована?
# 0 - нет, 1- да

    mapIsRscObjSemOrdered_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsRscObjSemOrdered', maptype.HRSC, ctypes.c_int)
    def mapIsRscObjSemOrdered(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapIsRscObjSemOrdered_t (_hRsc, _incode)


# Запрос порядка вывода кода семантики по внутреннему коду объекта
# с учетом сортировки пользователя
# Возвращает порядковый номер семантики в отсортированном списке (с 1)
# 0 - семантика не принадлежит объекту либо общая

    mapGetRscObjSemOrderNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjSemOrderNumber', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjSemOrderNumber(_hRsc: maptype.HRSC, _incode: int, _semcode: int) -> int:
        return mapGetRscObjSemOrderNumber_t (_hRsc, _incode, _semcode)


# Проверить наличие записи в таблице допустимых значений семантики
# по внутреннему коду объекта и коду семантики,
# если не нашли возвращает 0, иначе 1
# При ошибке возвращает ноль

    mapGetRscObjCheckTabDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscObjCheckTabDef', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapGetRscObjCheckTabDef(_hRsc: maptype.HRSC, _incode: int, _semcode: int) -> int:
        return mapGetRscObjCheckTabDef_t (_hRsc, _incode, _semcode)


# Заполняет минимум,умолчание и максимум значения семантики
# по внутреннему коду объекта и коду семантики
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# semcode код семантики
# При ошибке возвращает ноль

#   mapGetRscDefValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetRscDefValue', maptype.HRSC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(RSCDEF))
#   def mapGetRscDefValue(_hRsc: maptype.HRSC, _incode: int, _semcode: int, _valdef: ctypes.POINTER(RSCDEF)) -> int:
#       return mapGetRscDefValue_t (_hRsc, _incode, _semcode, _valdef)


# Записать имя объекта (для совместимости со старыми версиями)
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# name имя объекта не более 32 символов с завершающим 0
# При ошибке возвращает ноль

    mapSetRscObjectName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRscObjectName', maptype.HRSC, ctypes.c_int, ctypes.c_char_p)
    def mapSetRscObjectName(_hRsc: maptype.HRSC, _incode: int, _name: ctypes.c_char_p) -> int:
        return mapSetRscObjectName_t (_hRsc, _incode, _name)


# Переопределить внешний код объекта
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# newexcode - внутренний код объекта
# Замещается также внешний код умолчаний
# возвращает incode или 0

    mapUpdateRscObjectExcode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRscObjectExcode', maptype.HRSC, ctypes.c_int, ctypes.c_int)
    def mapUpdateRscObjectExcode(_hRsc: maptype.HRSC, _incode: int, _newexcode: int) -> int:
        return mapUpdateRscObjectExcode_t (_hRsc, _incode, _newexcode)


# Проверяет для объекта единственность сочетания буквенно-цифрового
# кода + локализации среди не удаленных объектов.
# Если уникален,возвращает 0, иначе incode порядковый номер
# объекта с совпадающим буквенно-цифровым кодом
# При ошибке возвращает ноль

    mapCheckRscObjectWCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRscObjectWCode', maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
    def mapCheckRscObjectWCode(_hRsc: maptype.HRSC, _wcode: mapsyst.WTEXT, _local: int) -> int:
        return mapCheckRscObjectWCode_t (_hRsc, _wcode.buffer(), _local)


# Создать внешний вид объекта по локализации
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# При ошибке возвращает ноль

    mapCreateRscObjectDefaultView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateRscObjectDefaultView', maptype.HRSC, ctypes.c_int)
    def mapCreateRscObjectDefaultView(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapCreateRscObjectDefaultView_t (_hRsc, _incode)


# Удалить умолчания на объект по любым семантикам
# hRsc - идентификатор классификатора карты
# incode - внутренний код объекта
# возвращает incode или 0

    mapDeleteRscDefaultObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRscDefaultObject', maptype.HRSC, ctypes.c_int)
    def mapDeleteRscDefaultObject(_hRsc: maptype.HRSC, _incode: int) -> int:
        return mapDeleteRscDefaultObject_t (_hRsc, _incode)


# Вернуть ширину линейного объекта в мм на карте в масштабе 1:1
# x - справа от метрики
# y - cлева от метрики
# При ошибке, если у объекта локализация не линейная - возвращает 0

    mapCountRscLineObjectWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCountRscLineObjectWidth', maptype.HRSC, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapCountRscLineObjectWidth(_hRsc: maptype.HRSC, _incode: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapCountRscLineObjectWidth_t (_hRsc, _incode, _x, _y)


# Создать список (DRAWOBJECT) примитивов для рисования объектов на карте
# Для освобождения памяти необходим вызов mapFreePaintDrawList
# При ошибке возвращает ноль

    mapCreatePaintDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreatePaintDrawList')
    def mapCreatePaintDrawList() -> ctypes.c_void_p:
        return mapCreatePaintDrawList_t ()


# Освободить список примитивов для рисования объектов на карте
# drawList - идентификатор списка, созданный функцией mapCreatePaintDrawList
# При вызове освобождает все HDRAW и HSLECT в спсике

    mapFreePaintDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreePaintDrawList', ctypes.c_void_p)
    def mapFreePaintDrawList(_drawList: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreePaintDrawList_t (_drawList)


# Добавить в список объект для отображения в новом виде на карте
# drawList - идентификатор списка, созданный функцией mapCreatePaintDrawList
# draw - примитив
# select - фильтр объектов, которые рисуются заданным примитивом
# При ошибке возвращает ноль

    mapAppendDrawToDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendDrawToDrawList', ctypes.c_void_p, maptype.HDRAW, maptype.HSELECT)
    def mapAppendDrawToDrawList(_drawList: ctypes.c_void_p, _draw: maptype.HDRAW, _select: maptype.HSELECT) -> int:
        return mapAppendDrawToDrawList_t (_drawList, _draw, _select)


# Запросить объект для отображения в новом виде на карте по номеру
# drawList - идентификатор списка, созданный функцией mapCreatePaintDrawList
# number - порядковый номер в списке, начиная с 1
# При ошибке возвращает ноль

    mapGetItemInDrawList_t = mapsyst.GetProcAddress(acceslib,maptype.HDRAW,'mapGetItemInDrawList', ctypes.c_void_p, ctypes.c_uint)
    def mapGetItemInDrawList(_drawList: ctypes.c_void_p, _number: int) -> maptype.HDRAW:
        return mapGetItemInDrawList_t (_drawList, _number)


# Запросить количество элeментов в списке
# drawList - идентификатор списка, созданный функцией mapCreatePaintDrawList
# При ошибке возвращает ноль

    mapGetDrawListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetDrawListCount', ctypes.c_void_p)
    def mapGetDrawListCount(_drawList: ctypes.c_void_p) -> int:
        return mapGetDrawListCount_t (_drawList)


# Очистить список
# drawList - идентификатор списка, созданный функцией mapCreatePaintDrawList
# При вызове освобождает все HDRAW и HSLECT в спсике

    mapClearDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearDrawList', ctypes.c_void_p)
    def mapClearDrawList(_drawList: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapClearDrawList_t (_drawList)

#   TEMPHDRAW_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEMPHDRAW', maptype.HDRAW)
#   def TEMPHDRAW(_value: maptype.HDRAW) -> typedef struct:
#       return TEMPHDRAW_t (_value)

except Exception as e:
    print(e)
    acceslib = 0