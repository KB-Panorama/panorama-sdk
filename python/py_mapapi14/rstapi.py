#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype
import mapcreat

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К РАСТРОВОЙ КАРТЕ ++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Открыть растровые данные
# Возвращает идентификатор открытой растровой карты (TMapAccess#)
# rstname - имя файла растровой карты
# mode    - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenRst_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenRst', ctypes.c_char_p, ctypes.c_int)
    def mapOpenRst(_rstname: ctypes.c_char_p, _mode: int = 0) -> maptype.HMAP:
        return mapOpenRst_t (_rstname, _mode)

    mapOpenRstUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenRstUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenRstUn(_rstname: mapsyst.WTEXT, _mode: int) -> maptype.HMAP:
        return mapOpenRstUn_t (_rstname.buffer(), _mode)


# Открыть растровые данные в заданном районе работ
# (добавить в цепочку растров)
# Возвращает номер файла в цепочке растров
# hMap    - идентификатор открытых данных
# rstname - имя файла растровой карты
# mode    - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenRstForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenRstForMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapOpenRstForMap(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _mode: int) -> int:
        return mapOpenRstForMap_t (_hMap, _rstname, _mode)

    mapOpenRstForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenRstForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenRstForMapUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        return mapOpenRstForMapUn_t (_hMap, _name.buffer(), _mode)


# Создание файла растрового изображения
# rstname    - имя создаваемого файла
# width      - ширина растрового изображения в элементах
# height     - высота растрового изображения в элементах
# nbits      - размер элемента (бит на пиксел)
# palette    - адрес устанавливаемой палитры
# colorcount - число элементов в новой палитре
# scale      - масштаб
# precision  - разрешение растра
# При успешном завершении функция создает файл rstname с заполненным
# паспортом и палитрой растра.
# При ошибке возвращает 0

    mapCreateRst_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRst', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapCreateRst(_rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float = 0, _precision: float = 0) -> maptype.HMAP:
        return mapCreateRst_t (_rstname, _width, _height, _nbits, _palette, _colorcount, _scale, _precision)

    mapCreateRstUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRstUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapCreateRstUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float) -> maptype.HMAP:
        return mapCreateRstUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precision)


# Создание файла растровой карты
# name            - полное имя растра
# width           - ширина изображения в пикселях
# height          - высота изображения в пикселях
# nbits           - количество бит на пиксель (1,4,8,24)
# palette         - указатель на палитру растра (справедливо для 1,4,8 бит на пиксель)
# scale           - мастаб растра
# precisionMet    - разрешения растра (точек на метр)
# meterInElementX - размер пикселя растра в метрах на местности по оси X (по вертикали)
# meterInElementY - размер пикселя растра в метрах на местности по оси Y (по горизонтали)
#                   meterInElementX и meterInElementY могут иметь разные значения
# location        - координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
# mapregister     - проекции исходного материала
# Важно!!!
# Для корректного открытия растров в 10-ой и более ранних версиях необходимо выполнить условие:
#                            meterInElementX = scale/precisionMet;
# Иначе масштаб и разрешение будут пересчитаны!!!
# При ошибке возвращает 0

    mapCreateRstEx_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRstEx', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapCreateRstEx(_rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precisionMet: float, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> maptype.HMAP:
        return mapCreateRstEx_t (_rstname, _width, _height, _nbits, _palette, _colorcount, _scale, _precisionMet, _meterInElementX, _meterInElementY, _location, _mapregister)

    mapCreateRstExUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRstExUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapCreateRstExUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precisionMet: float, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> maptype.HMAP:
        return mapCreateRstExUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precisionMet, _meterInElementX, _meterInElementY, _location, _mapregister)


# Создание файла растровой карты
# name            - полное имя растра
# width           - ширина изображения в пикселях
# height          - высота изображения в пикселях
# nbits           - количество бит на пиксель (1,4,8,24)
# palette         - указатель на палитру растра (справедливо для 1,4,8 бит на пиксель)
# meterInElementX - размер пикселя растра в метрах на местности по оси X (по вертикали)
# meterInElementY - размер пикселя растра в метрах на местности по оси Y (по горизонтали)
#                   meterInElementX и meterInElementY могут иметь разные значения
# location        - координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
# mapregister     - указатель на структуру, содержащую параметры проекции исходного материала
# datumparam      - указатель на структуру, содержащую коэффициенты трансформирования геодезических координат
# ellipsoidparam  - указатель на структуру, содержащую параметры эллипсоида
# При ошибке возвращает 0

    mapCreateRaster_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRaster', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateRaster(_rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> maptype.HMAP:
        return mapCreateRaster_t (_rstname, _width, _height, _nbits, _palette, _colorcount, _meterInElementX, _meterInElementY, _location, _mapregister, _datum, _ellipsoid)

    mapCreateRasterUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRasterUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateRasterUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> maptype.HMAP:
        return mapCreateRasterUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _meterInElementX, _meterInElementY, _location, _mapregister, _datum, _ellipsoid)


# Создание файла растрового изображения
# hMap       - идентификатор открытых данных
# rstname    - имя создаваемого файла
# width      - ширина растрового изображения в элементах
# height     - высота растрового изображения в элементах
# nbits      - размер элемента (бит на пиксел)
# palette    - адрес устанавливаемой палитры
# colorcount - число элементов в новой палитре
# scale      - масштаб
# precision  - разрешение растра
# location   - привязка юго-западного угла растра в районе(в метрах)
# При успешном завершении функция создает файл rstname с заполненным
# паспортом и палитрой растра и добавляет его в цепочку растров
# открытой векторной карты (hMap).
# Возвращает  номер файла (начиная с 1) в цепочке растров открытой векторной карты
# При ошибке возвращает ноль

    mapCreateAndAppendRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRst', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.DOUBLEPOINT)
    def mapCreateAndAppendRst(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float, _location: maptype.DOUBLEPOINT) -> int:
        return mapCreateAndAppendRst_t (_hMap, _rstname, _width, _height, _nbits, _palette, _colorcount, _scale, _precision, _location)

    mapCreateAndAppendRstUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRstUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.DOUBLEPOINT)
    def mapCreateAndAppendRstUn(_hMap: maptype.HMAP, _rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float, _location: maptype.DOUBLEPOINT) -> int:
        return mapCreateAndAppendRstUn_t (_hMap, _rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precision, _location)


# Создание файла растрового изображения
# hMap       - идентификатор открытых данных
# rstname    - имя создаваемого файла
# width      - ширина растрового изображения в элементах
# height     - высота растрового изображения в элементах
# nbits      - размер элемента (бит на пиксел)
# palette    - адрес устанавливаемой палитры
# colorcount - число элементов в новой палитре
# scale      - масштаб
# precision  - разрешение растра (точек на метр)
# meterInElementX - размер пикселя растра в метрах на местности по оси X (по вертикали)
# meterInElementY - размер пикселя растра в метрах на местности по оси Y (по горизонтали)
#                   meterInElementX и meterInElementY могут иметь разные значения
# location        - координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
# mapregister     - проекции исходного материала
# Важно!!!
# Для корректного открытия растров в 10-ой и более ранних версиях необходимо выполнить условие:
#                            meterInElementX = scale/precision;
# Иначе масштаб и разрешение будут пересчитаны!!!
# При успешном завершении функция создает файл rstname с заполненным
# паспортом и палитрой растра и добавляет его в цепочку растров
# открытой векторной карты (hMap).
# Возвращает  номер файла (начиная с 1) в цепочке растров открытой векторной карты
# При ошибке возвращает ноль

    mapCreateAndAppendRstEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRstEx', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapCreateAndAppendRstEx(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapCreateAndAppendRstEx_t (_hMap, _rstname, _width, _height, _nbits, _palette, _colorcount, _scale, _precision, _meterInElementX, _meterInElementY, _location, _mapregister)

    mapCreateAndAppendRstExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRstExUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapCreateAndAppendRstExUn(_hMap: maptype.HMAP, _rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapCreateAndAppendRstExUn_t (_hMap, _rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precision, _meterInElementX, _meterInElementY, _location, _mapregister)


# Создание файла растрового изображения
# hMap       - идентификатор открытых данных
# rstname    - имя создаваемого файла
# width      - ширина растрового изображения в элементах
# height     - высота растрового изображения в элементах
# nbits      - размер элемента (бит на пиксел)
# palette    - адрес устанавливаемой палитры
# colorcount - число элементов в новой палитре
# scale      - масштаб
# precision  - разрешение растра (точек на метр)
# meterInElementX - размер пикселя растра в метрах на местности по оси X (по вертикали)
# meterInElementY - размер пикселя растра в метрах на местности по оси Y (по горизонтали)
#                   meterInElementX и meterInElementY могут иметь разные значения
# location        - координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
# mapregister     - указатель на структуру, содержащую параметры проекции исходного материала
# datumparam      - указатель на структуру, содержащую коэффициенты трансформирования геодезических координат
# ellipsoidparam  - указатель на структуру, содержащую параметры эллипсоида
# Важно!!!
# Для корректного открытия растров в 10-ой и более ранних версиях необходимо выполнить условие:
#                            meterInElementX = scale/precision;
# Иначе масштаб и разрешение будут пересчитаны!!!
# При успешном завершении функция создает файл rstname с заполненным
# паспортом и палитрой растра и добавляет его в цепочку растров
# открытой векторной карты (hMap).
# Возвращает  номер файла (начиная с 1) в цепочке растров открытой векторной карты
# При ошибке возвращает ноль

    mapCreateAndAppendRaster_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRaster', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateAndAppendRaster(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapCreateAndAppendRaster_t (_hMap, _rstname, _width, _height, _nbits, _palette, _colorcount, _meterInElementX, _meterInElementY, _location, _mapregister, _datum, _ellipsoid)

    mapCreateAndAppendRasterUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendRasterUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateAndAppendRasterUn(_hMap: maptype.HMAP, _rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterInElementX: float, _meterInElementY: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapCreateAndAppendRasterUn_t (_hMap, _rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _meterInElementX, _meterInElementY, _location, _mapregister, _datum, _ellipsoid)


# Оценка теорeтической длины файла растровой карты до ее создания
# hMap    - идентификатор открытых данных
# width   - ширина растрового изображения в элементах
# height  - высота растрового изображения в элементах
# nbits   - размер элемента (бит на пиксел)
# Возвращает  теорeтическую длину файла растровой карты (Байт)
# При ошибке возвращает ноль

    mapRstFileLengthCalculation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRstFileLengthCalculation', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapRstFileLengthCalculation(_hMap: maptype.HMAP, _width: int, _height: int, _nbits: int) -> float:
        return mapRstFileLengthCalculation_t (_hMap, _width, _height, _nbits)


# Устаревшая функция

    mapRtsFileLengthCalculation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRtsFileLengthCalculation', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapRtsFileLengthCalculation(_hMap: maptype.HMAP, _width: int, _height: int, _nbits: int) -> float:
        return mapRtsFileLengthCalculation_t (_hMap, _width, _height, _nbits)


# Запросить длину в байтах файла растровой карты
# Максимальный размер файла 8 ГБ.
# Растровая карта размером более 4Gb состоит из 2-х файлов: #.rsw и #.rsw.01
# hMap   - идентификатор открытых данных
# number - номер растрового файла в цепочке
# При ошибке возвращает ноль

    mapRstFileLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapRstFileLength', maptype.HMAP, ctypes.c_int)
    def mapRstFileLength(_hMap: maptype.HMAP, _number: int) -> int:
        return mapRstFileLength_t (_hMap, _number)


# Запросить номер растра в цепочке по имени файла
# hMap    - идентификатор открытых данных
# name    - имя файла растра
# В цепочке номера растров начинаются с 1.
# При ошибке возвращает ноль

    mapGetRstNumberByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstNumberByName', maptype.HMAP, ctypes.c_char_p)
    def mapGetRstNumberByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapGetRstNumberByName_t (_hMap, _name)

    mapGetRstNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetRstNumberByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetRstNumberByNameUn_t (_hMap, _name.buffer())


# Закрыть растровые данные в заданном районе работ
# hMap   - идентификатор открытых данных
# number - номер растрового файла в цепочке
# Если number равен 0, закрываются все растровые данные
# При ошибке возвращает ноль

    mapCloseRstForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseRstForMap', maptype.HMAP, ctypes.c_int)
    def mapCloseRstForMap(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCloseRstForMap_t (_hMap, _number)

    mapCloseRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseRst', maptype.HMAP, ctypes.c_int)
    def mapCloseRst(_hMap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        return mapCloseRst_t (_hMap, _number)


# Закрыть растровые данные и удалить файл
# hMap   - идентификатор открытых данных
# number - номер растрового файла в цепочке
# Если number равен 0, закрываются и удалаются все растровые данные
# При ошибке возвращает ноль

    mapDeleteRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRst', maptype.HMAP, ctypes.c_int)
    def mapDeleteRst(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteRst_t (_hMap, _number)


# Запросить имя файла растровых данных в кодировке UNICODE
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# name - адрес строки для размещения результата
# size - размер строки
# При ошибке возвращает пустую строку

    mapGetRstNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRstNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetRstNameUn_t (_hMap, _number, _name.buffer(), _size)


# Запросить число открытых файлов растровых данных
# hMap    - идентификатор открытой векторной карты
# При ошибке возвращает ноль

    mapGetRstCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCount', maptype.HMAP)
    def mapGetRstCount(_hMap: maptype.HMAP) -> int:
        return mapGetRstCount_t (_hMap)


# Запросить идентификатор растровых данных
# hMap    - идентификатор открытого документа
# При ошибке возвращает ноль

    mapGetRstIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstIdent', maptype.HMAP, ctypes.c_int)
    def mapGetRstIdent(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstIdent_t (_hMap, _number)


# Запросить номер растра по идентификатору
# При ошибке возвращается ноль

    mapGetRstNumberByIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstNumberByIdent', maptype.HMAP, ctypes.c_int)
    def mapGetRstNumberByIdent(_hMap: maptype.HMAP, _ident: int) -> int:
        return mapGetRstNumberByIdent_t (_hMap, _ident)


# Запрос текущего номера растра
# hMap    - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetRstCurrentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCurrentNumber', maptype.HMAP)
    def mapGetRstCurrentNumber(_hMap: maptype.HMAP) -> int:
        return mapGetRstCurrentNumber_t (_hMap)


# Установка текущего номера растра
# hMap    - идентификатор открытых данных
# number  - номер растра
# При ошибке возвращает ноль

    mapSetRstCurrentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstCurrentNumber', maptype.HMAP, ctypes.c_int)
    def mapSetRstCurrentNumber(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSetRstCurrentNumber_t (_hMap, _number)


# Открыт ли растр с номером "number"
# Функция возвращает признак открытия указанного растра в документе - (1/0).
# При ошибке возвращает ноль.

    mapIsOpenRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsOpenRst', maptype.HMAP, ctypes.c_int)
    def mapIsOpenRst(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsOpenRst_t (_hMap, _number)


# Очистить кэш растровых данных, открытых на ГИС Сервере
# hMap    - идентификатор открытых данных
# number  - номер растра, для которого нужно очистить кэш, или -1 (все растры)
# При ошибке возвращает ноль

    mapClearRstCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearRstCache', maptype.HMAP, ctypes.c_int)
    def mapClearRstCache(_hMap: maptype.HMAP, _number: int) -> int:
        return mapClearRstCache_t (_hMap, _number)


# Запросить время крайнего редактирования растра
# hMap    - идентификатор открытых данных
# number  - номер растра
# Возвращает системное время редактирования (создания) по Гринвичу
# При ошибке возвращает ноль

    mapGetRstSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstSystemTime', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetRstSystemTime(_hMap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        return mapGetRstSystemTime_t (_hMap, _number, _time)


# Запросить/Установить степень видимости растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# view = 0 - не виден
# view = 1 - полная видимость
# view = 2 - насыщенная
# view = 3 - полупрозрачная
# view = 4 - средняя
# view = 5 - прозрачная
# При ошибке возвращает ноль

    mapGetRstView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstView', maptype.HMAP, ctypes.c_int)
    def mapGetRstView(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstView_t (_hMap, _number)

    mapSetRstView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstView(_hMap: maptype.HMAP, _number: int, _view: int) -> int:
        return mapSetRstView_t (_hMap, _number, _view)


# Запросить прозрачность растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstTransparent', maptype.HMAP, ctypes.c_int)
    def mapGetRstTransparent(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstTransparent_t (_hMap, _number)


# Установить прозрачность растра
# hMap        - идентификатор открытых данных
# number      - номер файла в цепочке
# transparent - прозрачность в процентах от 0 до 100
# При ошибке возвращает ноль

    mapSetRstTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstTransparent', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstTransparent(_hMap: maptype.HMAP, _number: int, _transparent: int) -> int:
        return mapSetRstTransparent_t (_hMap, _number, _transparent)


# Установить степень видимости группы растров
# hMap       - идентификатор открытых данных
# userLabel  - пользовательская метка растра:
#                -1             - все растры
#                RSW_QUALITY    - растры качеств (создаются mtrBuildRasterUn)
#                RSW_VISIBILITY - растры зон видимости (создаются mapVisibilityZoneUn)
# view - степень видимости:
#                0 - не виден
#                1 - полная
#                2 - насыщенная
#                3 - полупрозрачная
#                4 - средняя
#                5 - прозрачная
# При ошибке возвращает 0

    mapSetRstGroupView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstGroupView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstGroupView(_hMap: maptype.HMAP, _userLabel: int, _view: int) -> int:
        return mapSetRstGroupView_t (_hMap, _userLabel, _view)


# Запросить/Установить порядок отображения растра
# hMap  - идентификатор открытых данных
# number - номер растрового файла в цепочке
#  (0 - под картой, 1 - над картой)
# При ошибке возвращает 0

    mapSetRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstViewOrder(_hMap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetRstViewOrder_t (_hMap, _number, _order)

    mapGetRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstViewOrder', maptype.HMAP, ctypes.c_int)
    def mapGetRstViewOrder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstViewOrder_t (_hMap, _number)


# Поменять очередность отображения растров (rst) в цепочке
# Последний растр в цепочке отображается в последнюю очередь
# Нумерация растров в цепочке начинается с 1 и заканчивается номером mapGetRstCount(..)
# hMap      - идентификатор открытых данных
# oldNumber - номер файла в цепочке
# newNumber - устанавливаемый номер файла в цепочке
# При ошибке возвращает 0

    mapChangeOrderRstShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeOrderRstShow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangeOrderRstShow(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangeOrderRstShow_t (_hMap, _oldNumber, _newNumber)

    mapChangOrderRstInChain_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangOrderRstInChain', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangOrderRstInChain(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangOrderRstInChain_t (_hMap, _oldNumber, _newNumber)


# Последовательный просмотр растров над картой
# Если все растры отображаются под картой, то
# первый растр будет отображен над картой. При следующем
# вызове второй растр будет отображен над картой, остальные -
# под картой. После последнего растра в списке над картой -
# все растры под картой. Далее - опять первый растр над картой.
# Возвращает номер растра отображаемого над картой или ноль.
# Для получения результата на экране - карту нужно перерисовать
# hMap    - идентификатор открытых данных
# При ошибке возвращается 0

    mapTurnRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTurnRstViewOrder', maptype.HMAP)
    def mapTurnRstViewOrder(_hMap: maptype.HMAP) -> int:
        return mapTurnRstViewOrder_t (_hMap)


# Запросить количество цветов в палитре растра
# hMap    - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращается 0

    mapGetRstColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstColorCount', maptype.HMAP, ctypes.c_int)
    def mapGetRstColorCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstColorCount_t (_hMap, _number)


# Запросить описание палитры растра
# hMap    - идентификатор открытых данных
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
#           (если count > 256, то возвращается ноль)
# number  - номер файла в цепочке
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetRstPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetRstPalette_t (_hMap, _palette, _count, _number)


# Установить описание палитры растра
# hMap    - идентификатор открытых данных
# palette - адрес устанавливаемой палитры
# count   - число элементов в новой палитре
# number  - номер файла в цепочке
# Если palette равно 0, устанавливается палитра из заголовка
# count не более 256
# При ошибке возвращает ноль

    mapSetRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapSetRstPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapSetRstPalette_t (_hMap, _palette, _count, _number)


# Запросить описание эталонной палитры растра
# (без учета яркости и контрасности)
# hMap    - идентификатор открытых данных
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
#           (если count > 256, то возвращается ноль)
# number  - номер файла в цепочке
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetRstStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetRstStandardPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetRstStandardPalette_t (_hMap, _palette, _count, _number)


# Запросить описание палитры из заголовка растра
# hMap    - идентификатор открытых данных
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
#           (если count > 256, то возвращается ноль)
# number  - номер файла в цепочке
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetRstPaletteFromHeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPaletteFromHeader', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetRstPaletteFromHeader(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetRstPaletteFromHeader_t (_hMap, _palette, _count, _number)


# Скопировать описание палитры в заголовок растра
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
#           (если count > 256, то возвращается ноль)
# number  - номер файла в цепочке
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapSetRstPaletteToHeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstPaletteToHeader', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapSetRstPaletteToHeader(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapSetRstPaletteToHeader_t (_hMap, _palette, _count, _number)


# Запросить яркость палитры растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBright', maptype.HMAP, ctypes.c_int)
    def mapGetRstBright(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBright_t (_hMap, _number)


# Запросить контрастность палитры растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstContrast', maptype.HMAP, ctypes.c_int)
    def mapGetRstContrast(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstContrast_t (_hMap, _number)


# Запросить параболическую яркость растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstGamma', maptype.HMAP, ctypes.c_int)
    def mapGetRstGamma(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstGamma_t (_hMap, _number)


# Установить яркость палитры растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# bright - яркость
# При ошибке возвращает ноль

    mapSetRstBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstBright', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstBright(_hMap: maptype.HMAP, _bright: int, _number: int) -> int:
        return mapSetRstBright_t (_hMap, _bright, _number)


# Установить контрастность палитры растра
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# contrast - контраст
# При ошибке возвращает ноль

    mapSetRstContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstContrast', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstContrast(_hMap: maptype.HMAP, _contrast: int, _number: int) -> int:
        return mapSetRstContrast_t (_hMap, _contrast, _number)


# Установить параболическую яркость растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# gamma  - параболическая яркость
# При ошибке возвращает ноль

    mapSetRstGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstGamma', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstGamma(_hMap: maptype.HMAP, _gamma: int, _number: int) -> int:
        return mapSetRstGamma_t (_hMap, _gamma, _number)


# Обновить активную палитру с нулевой яркостью и контрастностью
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapRestoreRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreRstPalette', maptype.HMAP, ctypes.c_int)
    def mapRestoreRstPalette(_hMap: maptype.HMAP, _number: int) -> int:
        return mapRestoreRstPalette_t (_hMap, _number)


# Запросить значение инверсии растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Если изображение растра позитивное - возвращает ноль
# Если изображение растра негативное - возвращает 1
# При ошибке возвращает -1

    mapCheckInversionRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInversionRst', maptype.HMAP, ctypes.c_int)
    def mapCheckInversionRst(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckInversionRst_t (_hMap, _number)


# Инвертировать растровую карту
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# value:
# 0 - установить изображение растра позитивным
# 1 - установить изображение растра негативным
# При ошибке возвращает 0

    mapInvertRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInvertRst', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapInvertRst(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapInvertRst_t (_hMap, _number, _value)


# Запросить видимость цвета (для 16- и 256-цветных растров)
# hMap       - идентификатор открытых данных
# number - номер файла в цепочке
# index  - индекс цвета в палитре растра(начиная с 0)
# Возвращает: 1 - цвет с данным индексом отображается
#             0 - цвет с данным индексом не отображается
# При ошибке возвращает -1

    mapCheckVisibilityColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckVisibilityColor', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapCheckVisibilityColor(_hMap: maptype.HMAP, _number: int, _index: int) -> int:
        return mapCheckVisibilityColor_t (_hMap, _number, _index)


# Установить видимость цвета (для 16- и 256-цветных растров)
# hMap       - идентификатор открытых данных
# number - номер файла в цепочке
# index  - индекс цвета в палитре растра(начиная с 0)
# value: 1 - включить отображение цвета с данным индексом
#        0 - отключить отображение цвета с данным индексом
# Сохранение видимости цветов в INI-файле (не заносится в заголовк файла растра)
# При ошибке возвращает 0

    mapSetVisibilityColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetVisibilityColor', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetVisibilityColor(_hMap: maptype.HMAP, _number: int, _index: int, _value: int) -> int:
        return mapSetVisibilityColor_t (_hMap, _number, _index, _value)


# Установить видимость цвета (для 16- и 256-цветных растров)
# hMap       - идентификатор открытых данных
# number - номер файла в цепочке
# index  - индекс цвета в палитре растра(начиная с 0)
# value: 1 - включить отображение цвета с данным индексом
#        0 - отключить отображение цвета с данным индексом
# Сохранение видимости цветов в заголовке файла растра(а также в INI-файле)
# При ошибке возвращает 0

    mapSetVisibilityColorInRstFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetVisibilityColorInRstFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetVisibilityColorInRstFile(_hMap: maptype.HMAP, _number: int, _index: int, _value: int) -> int:
        return mapSetVisibilityColorInRstFile_t (_hMap, _number, _index, _value)


# Установить прозрачный цвет растра (для 16-,24-,32-битных растров)
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# color  - значение прозрачного цвета в формате RGB (от 0 до 0x00FFFFFF)
# При установке IMGC_TRANSPARENT (0xFFFFFFFF) прозрачный цвет не используется
# При ошибке возвращает IMGC_TRANSPARENT

    mapSetRstTransparentColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapSetRstTransparentColor', maptype.HMAP, ctypes.c_int, maptype.COLORREF)
    def mapSetRstTransparentColor(_hMap: maptype.HMAP, _number: int, _color: maptype.COLORREF) -> maptype.COLORREF:
        return mapSetRstTransparentColor_t (_hMap, _number, _color)


# Запросить прозрачный цвет растра (для 16-,24-,32-битных растров)
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Возвращает цвет в формате RGB (от 0 до 0x00FFFFFF)
# При возврате IMGC_TRANSPARENT (0xFFFFFFFF) прозрачный цвет не используется
# При ошибке возвращает IMGC_TRANSPARENT

    mapGetRstTransparentColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRstTransparentColor', maptype.HMAP, ctypes.c_int)
    def mapGetRstTransparentColor(_hMap: maptype.HMAP, _number: int) -> maptype.COLORREF:
        return mapGetRstTransparentColor_t (_hMap, _number)


# Запросить типа и шаг маски растра
# hMap      - идентификатор открытых данных
# maskType  - типа маски(0 - маска отсутствует)
# maskStep  - шаг маски
# number - номер файла в цепочке

    mapGetRstMaskType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstMaskType', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetRstMaskType(_hMap: maptype.HMAP, _number: int, _maskType: ctypes.POINTER(ctypes.c_int), _maskStep: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRstMaskType_t (_hMap, _number, _maskType, _maskStep)


# Установить типа и шаг маски растра
# hMap      - идентификатор открытых данных
# maskType  - типа маски(0 - маска отсутствует)
# maskStep  - шаг маски
# number - номер файла в цепочке

    mapSetRstMaskType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstMaskType', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRstMaskType(_hMap: maptype.HMAP, _number: int, _maskType: int, _maskStep: int) -> int:
        return mapSetRstMaskType_t (_hMap, _number, _maskType, _maskStep)


# Установка взаимосвязанных параметров растра
# hMap            - идентификатор открытых данных
# scale           - знаменатель масштаба
# precision       - разрешение (точек на метр)
# meterinelementX - количества метров на элемент  ПО ОСИ X
# meterinelementY - количества метров на элемент  ПО ОСИ Y
# meterinelementX и meterinelementY могут отличаться
# Важно!!!
# Для правильного отображения растров в 10-ой и более ранних версиях необходимо:
#                         meterinelementX = scale / precision;
# Если условие не выполняется, то meterinelementX и meterinelementY игнорируются и расчитываются по формуле.

    mapSetRstParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstParameters', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapSetRstParameters(_hMap: maptype.HMAP, _number: int, _scale: float, _precision: float, _meterinelementX: float, _meterinelementY: float) -> int:
        return mapSetRstParameters_t (_hMap, _number, _scale, _precision, _meterinelementX, _meterinelementY)


# Установить масштаб растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# scale      - знаменатель масштаба
# При ошибке возвращает 0

    mapSetRstScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstScale', maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mapSetRstScale(_hMap: maptype.HMAP, _number: int, _scale: float) -> int:
        return mapSetRstScale_t (_hMap, _number, _scale)


# Запросить масштаб растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# scale      - указатель переменной, куда вносится значение масштаба
# При ошибке возвращает 0

    mapGetRstScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstScale', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetRstScale(_hMap: maptype.HMAP, _number: int, _scale: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetRstScale_t (_hMap, _number, _scale)


# Запросить значения масштаба нижней и верхней границ видимости растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# По адресу bottomScale записывается знаменатель масштаба нижней границы видимости растра
# По адресу topScale записывается знаменатель масштаба верхней границы видимости растра
# При ошибке возвращает 0

    mapGetRstRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetRstRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: ctypes.POINTER(ctypes.c_int), _topScale: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRstRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить значения масштаба нижней и верхней границ видимости растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# bottomScale   - знаменатель масштаба нижней границы видимости растра
# topScale   - знаменатель масштаба верхней границы видимости растра
#              bottomScale <= topScale, иначе возвращает 0
# При ошибке возвращает 0

    mapSetRstRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetRstRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: int, _topScale: int) -> int:
        return mapSetRstRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить разрешение растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# precision  - разрешение растра, полученное при сканировании (точек на метр)
# При ошибке возвращает 0

    mapSetRstPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstPrecision', maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mapSetRstPrecision(_hMap: maptype.HMAP, _number: int, _precision: float) -> int:
        return mapSetRstPrecision_t (_hMap, _number, _precision)


# Запросить разрешение растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# precision  - разрешение растра (точек на метр)
# При ошибке возвращает 0

    mapGetRstPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPrecision', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetRstPrecision(_hMap: maptype.HMAP, _number: int, _precision: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetRstPrecision_t (_hMap, _number, _precision)


# Установить рамку растра по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# info       - замкнутый объект карты
# После выполнения функции отображение растра ограничится заданной областью
# При ошибке возвращает 0

    mapSetRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapSetRstBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapSetRstBorder_t (_hMap, _number, _info)


# Установить рамку растра по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# info       - замкнутый объект карты
# flagSubject- флаг использования подобъектов объекта при установке рамки растра (0/1)
#              0 - в качестве рамки растра устанавливается контур объекта
#              1 - в качестве рамки растра устанавливается контур объекта с подобъектами
# После выполнения функции отображение растра ограничится заданной областью
# При ошибке возвращает 0

    mapSetRstBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstBorderEx', maptype.HMAP, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapSetRstBorderEx(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ, _flagSubject: int) -> int:
        return mapSetRstBorderEx_t (_hMap, _number, _info, _flagSubject)


# Запросить объект рамки растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# info   - идентификатор объекта рамки
# При ошибке возвращает ноль

    mapGetRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapGetRstBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapGetRstBorder_t (_hMap, _number, _info)


# Удалить рамку растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# После выполнения функции отображение растра будет полным
# При ошибке возвращает 0

    mapDeleteRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRstBorder', maptype.HMAP, ctypes.c_int)
    def mapDeleteRstBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteRstBorder_t (_hMap, _number)


# Определение существования маски растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstMask', maptype.HMAP, ctypes.c_int)
    def mapGetRstMask(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstMask_t (_hMap, _number)


# Определение способа отображения растра(относительно маски)
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Возвращает 1 - при отображении растра по маске
#            0 - при отображении растра без учета маски
# При ошибке возвращает 0

    mapGetShowRstByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetShowRstByMask', maptype.HMAP, ctypes.c_int)
    def mapGetShowRstByMask(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetShowRstByMask_t (_hMap, _number)


# Установка отображения растра по маске
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# value  = 1 - отобразить растр по маске
#        = 0 - отобразить растр без учета маски

    mapSetShowRstByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetShowRstByMask', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetShowRstByMask(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapSetShowRstByMask_t (_hMap, _number, _value)


# Определение существования рамки растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapCheckExistenceRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckExistenceRstBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckExistenceRstBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckExistenceRstBorder_t (_hMap, _number)


# Установка отображения растра по рамке
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# value  = 1 - отобразить растр по рамке
#        = 0 - отобразить растр без учета рамки

    mapShowRstByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapShowRstByBorder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapShowRstByBorder(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapShowRstByBorder_t (_hMap, _number, _value)


# Определение способа отображения растра(относительно рамки)
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Возвращает 1 - при отображении растра по рамке
#            0 - при отображении растра без учета рамки
# При ошибке возвращает -1

    mapCheckShowRstByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckShowRstByBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckShowRstByBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckShowRstByBorder_t (_hMap, _number)


# Определить координаты точки рамки, которая
# входит в прямоугольник Габариты растра(матрицы) и
# имеет наименьшее удаление от точки pointIn (координаты в метрах).
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# По адресу pointOut записываются координаты найденной точки в метрах
# При ошибке или отсутствии рамки возвращает 0

    mapGetImmediatePointOfRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImmediatePointOfRstBorder', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfRstBorder(_hMap: maptype.HMAP, _number: int, _pointIn: ctypes.POINTER(maptype.DOUBLEPOINT), _pointOut: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetImmediatePointOfRstBorder_t (_hMap, _number, _pointIn, _pointOut)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hMap     - идентификатор открытых данных
# number   - номер растра
# Если нет - возвращает ноль

    mapIsRstGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsRstGeoSupported', maptype.HMAP, ctypes.c_int)
    def mapIsRstGeoSupported(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsRstGeoSupported_t (_hMap, _number)


# Запросить данные о проекции растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM описаны в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapGetRstProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetRstProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetRstProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetRstProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetRstProjectionData(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetRstProjectionData_t (_hMap, _number, _mapregister)


# Запросить данные о проекции растра по имени файла
# name        - имя файла растра
# mapregister - адрес структуры, в которой будут размещены
# данные о проекции
# При ошибке возвращает ноль

    mapGetRstProjectionDataByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstProjectionDataByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetRstProjectionDataByName(_name: ctypes.c_char_p, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetRstProjectionDataByName_t (_name, _mapregister)

    mapGetRstProjectionDataByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstProjectionDataByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetRstProjectionDataByNameUn(_name: mapsyst.WTEXT, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetRstProjectionDataByNameUn_t (_name.buffer(), _mapregister)


# Установить данные о проекции растра
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM описаны в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapSetRstProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetRstProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetRstProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)


# Установить параметры проекции документа в растр
# hMap    - идентификатор открытого документа
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapSetRstProjectionDataFromDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstProjectionDataFromDoc', maptype.HMAP, ctypes.c_int)
    def mapSetRstProjectionDataFromDoc(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSetRstProjectionDataFromDoc_t (_hMap, _number)

    mapSetRstProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapSetRstProjectionData(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapSetRstProjectionData_t (_hMap, _number, _mapregister)


# Запросить параметры эллипсоида растра
# hMap   - идентификатор открытых данных
# number - номер файла растра в цепочке
# ellipsoidparam - адрес структуры, в которой будут размещены
# параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetRstEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetRstEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetRstEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Установить параметры эллипсоида растра
# hMap    - идентификатор открытых данных
# number  - номер файла растра в цепочке.
# ellipsoidparam - адрес структуры, содержащей параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetRstEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetRstEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetRstEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Запросить коэффициенты трансформирования геодезических координат растра
# hMap   - идентификатор открытых данных
# number - номер файла растра в цепочке
# datumparam - адрес структуры, в которой будут размещены
# коэффициенты трансформирования геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetRstDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetRstDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetRstDatumParam_t (_hMap, _number, _datumparam)


# Установить коэффициенты трансформирования геодезических координат растра
# hMap    - идентификатор открытых данных
# number  - номер файла растра в цепочке.
# datumparam - адрес структуры, содержащей коэффициенты трансформирования
# геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetRstDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetRstDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetRstDatumParam_t (_hMap, _number, _datumparam)


# Запросить габариты растра в метрах в районе работ
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# frame      - возвращаемые габариты растра
# При ошибке возвращает ноль

    mapGetRstFrameMeters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFrameMeters', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetRstFrameMeters(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetRstFrameMeters_t (_hMap, _frame, _number)


# Запросить габариты растра в метрах в текущей проекции
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# frame      - возвращаемые габариты растра
# При ошибке возвращает ноль

    mapGetRstFrameDocMeters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFrameDocMeters', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetRstFrameDocMeters(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetRstFrameDocMeters_t (_hMap, _frame, _number)


# Запросить фактические габариты отображаемого растра в метрах в районе работ
# При отображение растра по рамке возвращаются габариты рамки
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# frame      - возвращаемые габариты растра
# При ошибке возвращает ноль

    mapGetActualRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActualRstFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetActualRstFrame(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetActualRstFrame_t (_hMap, _frame, _number)


# Запросить фактические габариты отображаемого растра в метрах в текущей проекции
# При отображение растра по рамке возвращаются габариты рамки
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# frame      - возвращаемые габариты растра
# При ошибке возвращает ноль

    mapGetActualRstFrameDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActualRstFrameDoc', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetActualRstFrameDoc(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetActualRstFrameDoc_t (_hMap, _frame, _number)


# Установить привязку растра в районе работ(в метрах)
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# location   - координаты юго-западного угла растра(в метрах)
# При ошибке возвращает 0

    mapSetRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetRstLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSetRstLocation_t (_hMap, _number, _location)


# Запросить привязку растра в районе работ(в метрах)
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# location   - координаты юго-западного угла растра(в метрах)
# При ошибке возвращает 0

    mapGetRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetRstLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetRstLocation_t (_hMap, _number, _location)


# Запросить флаг существования привязки растра
# hMap      - идентификатор открытых данных
# number    - номер файла в цепочке
# При ошибке возвращает 0

    mapCheckExistenceRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckExistenceRstLocation', maptype.HMAP, ctypes.c_int)
    def mapCheckExistenceRstLocation(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckExistenceRstLocation_t (_hMap, _number)


# Запросить - может ли растр копироваться или экспортироваться
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# Если нет - возвращает ноль

    mapGetRstCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCopyFlag', maptype.HMAP, ctypes.c_int)
    def mapGetRstCopyFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstCopyFlag_t (_hMap, _number)


# Запросить - может ли растр выводиться на печать
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения на печать
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# Если нет - возвращает ноль

    mapGetRstPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPrintFlag', maptype.HMAP, ctypes.c_int)
    def mapGetRstPrintFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstPrintFlag_t (_hMap, _number)


# Запросить - можно ли показывать параметры паспорта
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет отображения параметров системы координат
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# Если нет - возвращает ноль

    mapGetRstHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstHidePassportFlag', maptype.HMAP, ctypes.c_int)
    def mapGetRstHidePassportFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstHidePassportFlag_t (_hMap, _number)


# Запросить/Установить признак запрета кэширования данных с ГИС Сервера
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# flag     - признак запрета кэширования данных с ГИС Сервера

    mapGetRstHideCacheFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstHideCacheFlag', maptype.HMAP, ctypes.c_int)
    def mapGetRstHideCacheFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstHideCacheFlag_t (_hMap, _number)

    mapSetRstHideCacheFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstHideCacheFlag', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstHideCacheFlag(_hMap: maptype.HMAP, _number: int, _hideflag: int) -> int:
        return mapSetRstHideCacheFlag_t (_hMap, _number, _hideflag)


# Запросить открыт ли растр на сервере или локально
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# Если растр открыт на сервере возвращает ненулевое значение

    mapIsRstFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsRstFromServer', maptype.HMAP, ctypes.c_int)
    def mapIsRstFromServer(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsRstFromServer_t (_hMap, _number)


#######################################################################
# Как подвинуть растр на отрезок (Dx,Dy)?
#    Запросите привязку растра - mapGetRstLocation(...)
#    Измените точку привязки на отрезок (Dx,Dy)
#    Установите новую точку привязки - mapSetRstLocation(...)
#    Перерисуйте окно.
#######################################################################
# Как подвинуть растр с изменением масштаба ?
#    Запросите привязку растра - mapGetRstLocation(...)
#    Запросите знаменатель масштаба растра - mapGetRstScale(...)
#    Измените точку привязки и расчитайте знаменатель масштаба
#    Установите новую точку привязки - mapSetRstLocation(...)
#    Установите новый знаменатель масштаба - mapSetRstScale(...)
#    Перерисуйте окно.
#######################################################################
# Устаревшая функция
# Запросить размер элемента растра в метрах на местности
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# metinelem  - размер элемента растра в метрах на местности
# При ошибке возвращает ноль

    mapGetRstMeterInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstMeterInElement', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetRstMeterInElement(_hMap: maptype.HMAP, _number: int, _metinelem: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetRstMeterInElement_t (_hMap, _number, _metinelem)


# Запросить размер элемента растра в метрах по оси X
# hMap      - идентификатор открытых данных
# number    - номер файла в цепочке
# metinelemX - размер элемента растра в метрах на местности по оси X
# При ошибке возвращает ноль

    mapGetRstMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstMeterInElementX', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetRstMeterInElementX(_hMap: maptype.HMAP, _number: int, _metinelemX: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetRstMeterInElementX_t (_hMap, _number, _metinelemX)


# Запросить размер элемента растра в метрах по оси Y
# hMap      - идентификатор открытых данных
# number    - номер файла в цепочке
# metinelemY - размер элемента растра в метрах на местности по оси Y
# При ошибке возвращает ноль

    mapGetRstMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstMeterInElementY', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetRstMeterInElementY(_hMap: maptype.HMAP, _number: int, _metinelemY: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetRstMeterInElementY_t (_hMap, _number, _metinelemY)


# Устаревшая функция
# Запросить размер точки экрана в элементах растра
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# eleminpix  - размер точки экрана в элементах растра
# При ошибке возвращает ноль

    mapGetSizeRstElemInPix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSizeRstElemInPix', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetSizeRstElemInPix(_hMap: maptype.HMAP, _number: int, _eleminpix: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetSizeRstElemInPix_t (_hMap, _number, _eleminpix)


# Запросить размер элемента растра в пикселах экрана по оси X
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetSizeRstElemXInPix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSizeRstElemXInPix', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetSizeRstElemXInPix(_hMap: maptype.HMAP, _number: int, _eleminpix: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetSizeRstElemXInPix_t (_hMap, _number, _eleminpix)


# Запросить размер элемента растра в пикселах экрана по оси Y
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetSizeRstElemYInPix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSizeRstElemYInPix', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetSizeRstElemYInPix(_hMap: maptype.HMAP, _number: int, _eleminpix: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetSizeRstElemYInPix_t (_hMap, _number, _eleminpix)


# Запросить ширину растра в элементах
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstWidth', maptype.HMAP, ctypes.c_int)
    def mapGetRstWidth(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstWidth_t (_hMap, _number)


# Запросить высоту растра в элементах
# hMap       - идентификатор открытых данных
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstHeight', maptype.HMAP, ctypes.c_int)
    def mapGetRstHeight(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstHeight_t (_hMap, _number)


# Запросить объем растра в байтах
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRstLength', maptype.HMAP, ctypes.c_int)
    def mapGetRstLength(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstLength_t (_hMap, _number)


# Запросить размер элемента растра в битах
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstElementSize', maptype.HMAP, ctypes.c_int)
    def mapGetRstElementSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstElementSize_t (_hMap, _number)


# Запросить флаг редактируемости растра
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstEdit', maptype.HMAP, ctypes.c_int)
    def mapGetRstEdit(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstEdit_t (_hMap, _number)

    mapCheckRstEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRstEdit', maptype.HMAP, ctypes.c_int)
    def mapCheckRstEdit(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckRstEdit_t (_hMap, _number)


# Запросить номер алгоритма сжатия растра (0 - растр не сжат, 1 - LZW, 2 - JPEG)
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# При ошибке возвращает ноль

    mapCheckRstCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRstCompressNumber', maptype.HMAP, ctypes.c_int)
    def mapCheckRstCompressNumber(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckRstCompressNumber_t (_hMap, _number)

    mapGetRstCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCompressNumber', maptype.HMAP, ctypes.c_int)
    def mapGetRstCompressNumber(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstCompressNumber_t (_hMap, _number)


# Установить в заголовок растра номер алгоритма сжатия(0 - растр не сжат, 1 - LZW, 2 - JPEG)
# ВНИМАНИЕ: Функция не выполняет сжатие изображения
# Для сжатия изображения по методу LZW воспользуйтесь функцией mapCompressLZW(), объявленной в mapapi.h
# Для сжатия изображения по методу JPEG воспользуйтесь функцией mapCompressJPEG(), объявленной в mapapi.h
# hMap    - идентификатор открытых данных
# number  - номер файла в цепочке
# value   - номер алгоритма сжатия(0 - растр не сжат, 1 - LZW, 2 - JPEG)
# При ошибке возвращает ноль

    mapSetRstCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstCompressNumber', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstCompressNumber(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapSetRstCompressNumber_t (_hMap, _number, _value)


# Запросить степень сжатия блока растра по алгоритму JPEG
# hMap       - идентификатор открытой карты
# number - номер файла в цепочке
# Возвращает степень сжатия изображения блока растра по алгоритму JPEG
#          (1-100, 1-максимальное сжатие, 100-сжатие без потери качества),
#          рекомендуемое значение 60.
# При ошибке возвращает ноль

    mapGetRstCompressJpegQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCompressJpegQuality', maptype.HMAP, ctypes.c_int)
    def mapGetRstCompressJpegQuality(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstCompressJpegQuality_t (_hMap, _number)


# Установить в заголовок растра степень сжатия блока растра по алгоритму JPEG
# Используйте для установки в заголовок растра номера алгоритма сжатия функцию mapSetRstCompressNumber()
# ВНИМАНИЕ: Функция не выполняет сжатие изображения
# Для сжатия изображения по методу JPEG воспользуйтесь функцией mapCompressJPEG(), объявленной в mapapi.h
# hMap       - идентификатор открытой карты
# number - номер файла в цепочке
# value  - степень сжатия изображения блока растра по алгоритму JPEG
#          (1-100, 1-максимальное сжатие, 100-сжатие без потери качества),
#          рекомендуемое значение 60.
# При ошибке возвращает ноль

    mapSetRstCompressJpegQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstCompressJpegQuality', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstCompressJpegQuality(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapSetRstCompressJpegQuality_t (_hMap, _number, _value)


# Сжать растр RSW по заданному алгоритму
# handle  - идентификатор диалога для передачи сообщений о проценте выполнения WM_PROGRESSBAR
# name    - имя сжимаемого файла RSW
# newname - имя сжатого файла RSW
# compressnumber - номер алгоритма сжатия (RMF_COMPR_LZW, RMF_COMPR_JPEG, 2416)
# borderflag - флаг удаления неотображаемых блоков (не попадающих в заданную рамку растра)
# quality    - степень сжатия растра по алгоритму RMF_COMPR_JPEG (рекомендуется 60) от 0 до 100
# При ошибке возвращает ноль

    mapRstOptimizationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRstOptimizationUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapRstOptimizationUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int, _quality: int) -> int:
        return mapRstOptimizationUn_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag, _quality)

    mapRstOptimizationPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRstOptimizationPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapRstOptimizationPro(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int, _quality: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mapRstOptimizationPro_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag, _quality, _callevent, _parm)


# Чтение элемента по абсолютным индексам
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string, column - строка и столбец элемента
# value      - значение элемента
# При ошибке возвращает ноль

    mapGetRstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPoint', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
    def mapGetRstPoint(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_int), _string: int, _column: int) -> int:
        return mapGetRstPoint_t (_hMap, _number, _value, _string, _column)


# Запись элемента по абсолютным индексам
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string, column - строка и столбец элемента
# value      - значение элемента
# При ошибке возвращает ноль

    mapPutRstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutRstPoint', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapPutRstPoint(_hMap: maptype.HMAP, _number: int, _value: int, _string: int, _column: int) -> int:
        return mapPutRstPoint_t (_hMap, _number, _value, _string, _column)


# Чтение элемента по его плоским прямоугольным координатам (в метрах) из буфера
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# x,y        - координаты элемента в метрах в системе координат растра
# value      - значение элемента
# При ошибке возвращает ноль

    mapGetRstPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPlanePoint', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePoint(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_int), _x: float, _y: float) -> int:
        return mapGetRstPlanePoint_t (_hMap, _number, _value, _x, _y)


# Чтение элемента по его плоским прямоугольным координатам по методу треугольников
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# x,y        - координаты точки в метрах в системе координат растра
# value      - значение элемента
# При ошибке возвращает ноль

    mapGetRstPlanePointTriangle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPlanePointTriangle', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePointTriangle(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_int), _x: float, _y: float) -> int:
        return mapGetRstPlanePointTriangle_t (_hMap, _number, _value, _x, _y)


# Определение цвета точки растра по прямоугольным координатам точки
# (в метрах)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# x,y        - координаты точки в метрах в системе координат растра
# color      - цвет элемента
# При ошибке возвращает ноль

    mapGetRstPlanePointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPlanePointColor', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePointColor(_hMap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _x: float, _y: float) -> int:
        return mapGetRstPlanePointColor_t (_hMap, _number, _color, _x, _y)


# Билинейная интерполяция - определение цвета точки по 4 соседним пикселям растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# color      - заполняется вычисленным цветом
# indexColor - заполняется индексом ближайшего цвета к вычисленному из палитры растра
#              (для 1,4 и 8 бит на пиксель)
# x, y       - прямоугольные координаты точки в системе координат растра в метрах на местности
# При попадании в крайние пиксели растра возвращается цвет ближайшего пикселя
# При ошибке возвращает ноль

    mapGetRstBilinearInterpolationColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBilinearInterpolationColor', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_double)
    def mapGetRstBilinearInterpolationColor(_hMap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _indexcolor: ctypes.POINTER(ctypes.c_int), _x: float, _y: float) -> int:
        return mapGetRstBilinearInterpolationColor_t (_hMap, _number, _color, _indexcolor, _x, _y)


# Бикубическая интерполяция - определение цвета точки по 16 соседним пикселям растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# color      - заполняется вычисленным цветом
# indexColor - заполняется индексом ближайшего цвета к вычисленному из палитры растра
#              (для 1,4 и 8 бит на пиксель)
# x, y       - прямоугольные координаты точки в системе координат растра в метрах на местности
# При попадании в крайних 2 пикселя растра возвращается цвет ближайшего пикселя
# При ошибке возвращает ноль

    mapGetRstBicubicInterpolationColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBicubicInterpolationColor', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_double)
    def mapGetRstBicubicInterpolationColor(_hMap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _indexcolor: ctypes.POINTER(ctypes.c_int), _x: float, _y: float) -> int:
        return mapGetRstBicubicInterpolationColor_t (_hMap, _number, _color, _indexcolor, _x, _y)


# Запись элемента  по его прямоугольным координатам
# (в метрах) в буфер
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# x,y        - координаты элемента
# value      - значение элемента
# При ошибке возвращает ноль

    mapPutRstPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutRstPlanePoint', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapPutRstPlanePoint(_hMap: maptype.HMAP, _number: int, _value: int, _x: float, _y: float) -> int:
        return mapPutRstPlanePoint_t (_hMap, _number, _value, _x, _y)


# Запись отрезка в изображение основного растра по прямоугольным координатам (в метрах)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# color  - цвет отрезка типа COLORREF для растров с 16,24,32 точек на пиксель;
#          индекс цвета в палитре для растров с 1,4,8 точек на пиксель.
# point1 - координаты начальной точки отрезка
# point2 - координаты конечной точки отрезка
# При ошибке возвращает ноль

    mapPutRstPlaneLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutRstPlaneLine', maptype.HMAP, ctypes.c_int, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapPutRstPlaneLine(_hMap: maptype.HMAP, _number: int, _color: int, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapPutRstPlaneLine_t (_hMap, _number, _color, _point1, _point2)


# Запросить количество блоков растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockCount', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockCount_t (_hMap, _number)


# Запросить число строк блоков растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockRow', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockRow_t (_hMap, _number)


# Запросить число столбцов блоков растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockColumn', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockColumn_t (_hMap, _number)


# Запросить размер неусеченного блока растра в байтах
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockSize', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockSize_t (_hMap, _number)


# Запросить размер текущего блока {string,column} растра в байтах
# (с учетом усеченных блоков)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string, column - координаты блока
# При ошибке возвращает ноль

    mapGetRstCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCurrentBlockSize', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRstCurrentBlockSize(_hMap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        return mapGetRstCurrentBlockSize_t (_hMap, _number, _string, _column)


# Запросить ширину неусеченного блока растра в элементах
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockWidth', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockWidth(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockWidth_t (_hMap, _number)


# Запросить высоту неусеченного блока растра в элементах
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockHeight', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockHeight(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockHeight_t (_hMap, _number)


# Запросить ширину текущего блока {string,column} растра в элементах
# (с учетом усеченных блоков)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# column     - столбец блока
# При ошибке возвращает ноль

    mapGetRstCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCurrentBlockWidth', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetRstCurrentBlockWidth(_hMap: maptype.HMAP, _number: int, _column: int) -> int:
        return mapGetRstCurrentBlockWidth_t (_hMap, _number, _column)


# Запросить высоту текущего блока {string,column} растра в элементах
# (с учетом усеченных блоков)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string     - строка блока
# При ошибке возвращает ноль

    mapGetRstCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstCurrentBlockHeight', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetRstCurrentBlockHeight(_hMap: maptype.HMAP, _number: int, _string: int) -> int:
        return mapGetRstCurrentBlockHeight_t (_hMap, _number, _string)


# Запросить наличие блока растра в файле
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# i          - порядковый номер блока
# При ошибке возвращает ноль

    mapCheckRstBlockExistence_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRstBlockExistence', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapCheckRstBlockExistence(_hMap: maptype.HMAP, _number: int, _i: int) -> int:
        return mapCheckRstBlockExistence_t (_hMap, _number, _i)


# Возврат флага отображения блока
# (0 - не отображается, 1- отображается, 2 - разделен рамкой )
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# i          - порядковый номер блока
# При ошибке возвращает ноль

    mapCheckRstBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckRstBlockVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapCheckRstBlockVisible(_hMap: maptype.HMAP, _number: int, _i: int) -> int:
        return mapCheckRstBlockVisible_t (_hMap, _number, _i)


# Запись блока {string,column} в файл растрового изображения  из памяти bits.
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string     - строка блока
# column     - столбец блока
# bits       - указатель на начало изображения битовой области
# sizebits   - размер области bits в байтах
# Возвращает количество записанных байт.
# При ошибке возвращает ноль.

    mapWriteRstBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWriteRstBlock', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapWriteRstBlock(_hMap: maptype.HMAP, _number: int, _string: int, _column: int, _bits: ctypes.c_char_p, _sizebits: int) -> int:
        return mapWriteRstBlock_t (_hMap, _number, _string, _column, _bits, _sizebits)


# Запись блока {string,column} размером "size" по DIB-маске "mask"
# индексом "value"
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string     - строка блока
# column     - столбец блока
# mask       - указатель на начало маски
# size       - размер области mask в байтах
# width      - ширина маски в байтах (1 байт соответствует элементу - 0/1)
# height     - число строк маски
# value      - значение, которое устанавливается в блок, если элемент маски равен 0
# При ошибке возвращает ноль

    mapPutRstBlockByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutRstBlockByMask', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long)
    def mapPutRstBlockByMask(_hMap: maptype.HMAP, _number: int, _string: int, _column: int, _mask: ctypes.c_char_p, _size: int, _width: int, _height: int, _value: int) -> int:
        return mapPutRstBlockByMask_t (_hMap, _number, _string, _column, _mask, _size, _width, _height, _value)


# Записать изменения растра в файл
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapSaveRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveRst', maptype.HMAP, ctypes.c_int)
    def mapSaveRst(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSaveRst_t (_hMap, _number)


# Запись прямоугольного участка растра
# hMap    - идентификатор открытой векторной карты
# number  - номер файла в цепочке
# bits    - указатель на начало изображения битовой области
# left    - смещение слева в элементах (выравнено на границу байта)
# top     - смещение сверху в элементах
# width   - ширина в элементах (выравнено на границу байта)
# height  - высота в элементах
# begining  - начало изображения:
#   ==  1  - (bits - указатель на первую строку битовой области)
#   == -1  - (bits - указатель на послелнюю строку битовой области,
#                          в BMP изображение хранится снизу - вверх)
# widthinbyte    - ширину прямоугольного участка растра в байтах
# Принцип выравнивания:
# при ElementSize() == 1 (бит) - left,width кратны 8,
#                   == 4 (бит) - left,width кратны 2
# При ошибке возвращает 0

    mapPutRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutRstFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapPutRstFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _begining: int, _widthinbyte: int) -> int:
        return mapPutRstFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _begining, _widthinbyte)


# Чтение прямоугольного участка растра
#  hMap       - идентификатор открытой векторной карты
#  number     - номер файла в цепочке
#  bits    - указатель на начало изображения битовой области
#  left    - смещение слева в элементах (выравнено на границу байта)
#  top     - смещение сверху в элементах
#  width   - ширина в элементах (выравнено на границу байта)
#  height  - высота в элементах
#  widthinbyte    - ширину прямоугольного участка растра в байтах
# Принцип выравнивания:
#  при ElementSize() == 1 (бит) - left,width кратны 8,
#                    == 4 (бит) - left,width кратны 2
# При ошибке возвращает 0

    mapGetRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRstFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int = 0) -> int:
        return mapGetRstFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _widthinbyte)


# Чтение цветовых плоскостей прямоугольного участка растра
#  hMap       - идентификатор открытой векторной карты
#  number     - номер файла в цепочке
#  bitsR,bitsG - указатели на начало изображения байтовых областей
#  bitsB         красной, зеленой и синей плоскости
#  left    - смещение слева в элементах
#  top     - смещение сверху в элементах
#  width   - ширина в элементах
#  height  - высота в элементах
#  Поддерживает только 8-битные растры (пока)
# При ошибке возвращает 0

    mapGetRstFrameRGB_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFrameRGB', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetRstFrameRGB(_hMap: maptype.HMAP, _number: int, _bitsR: ctypes.c_char_p, _bitsG: ctypes.c_char_p, _bitsB: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int) -> int:
        return mapGetRstFrameRGB_t (_hMap, _number, _bitsR, _bitsG, _bitsB, _left, _top, _width, _height)


# Отображение прямоугольного участка исходного растра
# в результирующем растре, расположенном в области памяти.
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# bits   - указатель на начало области памяти;
# width  - ширина области памяти в элементах COLORREF
#          (количество столбцов результирующего растра);
# height - высота области памяти в элементах
#          (количество строк результирующего растра);
# strL,colL,strR,colR - координаты левого и правого элементов исходного
#                       растра в элементах растра, которые определяют верхний граничный
#                       отрезок считываемого прямоугольного наклонного участка.
# При ошибке возвращает ноль

    mapGetRstFrameTurn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFrameTurn', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetRstFrameTurn(_hMap: maptype.HMAP, _number: int, _bits: ctypes.POINTER(maptype.COLORREF), _width: int, _height: int, _strL: float, _colL: float, _strR: float, _colR: float) -> int:
        return mapGetRstFrameTurn_t (_hMap, _number, _bits, _width, _height, _strL, _colL, _strR, _colR)


# Пересчитать элементы растра в пикселы
# для текущего масштаба отображения
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# element    - элементы растра
# pixel      - результат в пикселах
# При ошибке возвращает ноль

    mapRstElementToPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRstElementToPixel', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapRstElementToPixel(_hMap: maptype.HMAP, _number: int, _element: float, _pixel: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapRstElementToPixel_t (_hMap, _number, _element, _pixel)


# Пересчитать пикселы в элементы растра
# для текущего масштаба отображения
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# element    - результат в элементах растра
# pixel      - пикселы
# При ошибке возвращает ноль

    mapPixelToRstElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPixelToRstElement', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapPixelToRstElement(_hMap: maptype.HMAP, _number: int, _pixel: float, _element: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPixelToRstElement_t (_hMap, _number, _pixel, _element)


# Формирование битовой маски текущего блока {string,column} с учетом рамки растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# string     - строка блока
# column     - столбец блока
# bits       - область битовой маски
# size       - размер области битовой маски в байтах
# При ошибке возвращает ноль

    mapBuildRstBlockMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRstBlockMask', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapBuildRstBlockMask(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _size: int, _string: int, _column: int) -> int:
        return mapBuildRstBlockMask_t (_hMap, _number, _bits, _size, _string, _column)


# Установить маску изображения растра по метрике объекта
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# info       - объект карты с подобъектами
# После выполнения функции отображение растра ограничится заданной областью
# При ошибке возвращает 0

    mapSetRstMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstMask', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapSetRstMask(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapSetRstMask_t (_hMap, _number, _info)


# Заливка цветом части растра, ограниченной рамкой.
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает 0

    mapFillRstVisiblePart_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFillRstVisiblePart', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapFillRstVisiblePart(_hMap: maptype.HMAP, _number: int, _color: int) -> int:
        return mapFillRstVisiblePart_t (_hMap, _number, _color)


# Запросить состояние растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# Возвращаемые значения:
#          0 - нет данных; или создание уменьшенных копий и сжатие не выполнялись
#          1 - создание всех уровней уменьшенных копий, сжатие JPEG растра
#          2 - создание всех уровней уменьшенных копий, сжатие LZW растра
#          4 - создание всех уровней уменьшенных копий

    mapGetRstProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstProcessingState', maptype.HMAP, ctypes.c_int)
    def mapGetRstProcessingState(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstProcessingState_t (_hMap, _number)


# Установить состояние растра
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# state      - состояние растра.
# Возможные значения состояния растра state:
#          0 - нет данных; или создание уменьшенных копий и сжатие не выполнялись
#          1 - создание всех уровней уменьшенных копий, сжатие JPEG растра
#          2 - создание всех уровней уменьшенных копий, сжатие LZW растра
#          4 - создание всех уровней уменьшенных копий
# При ошибке возвращает 0

    mapSetRstProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstProcessingState', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstProcessingState(_hMap: maptype.HMAP, _number: int, _state: int) -> int:
        return mapSetRstProcessingState_t (_hMap, _number, _state)


# Оптимизировать растр для открытия в ГИС Сервере
# Функция проверяет состояние растра и при необходимости выполняет для растра
# оптимизацию со сжатием (JPEG - для 24-х битных растров, LZW - для всех остальных)
# и создание всех уровней уменьшенной копии.
# Необходимо закрыть растр из всех документов перед вызовом функции
# rswName- имя файла растра
# handle - идентификатор окна, которое будет извещаться
# о ходе процесса (0x585 - 0x588)
# При ошибке возвращает 0

    mapOptimizationRstByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOptimizationRstByName', ctypes.c_char_p, maptype.HWND)
    def mapOptimizationRstByName(_rswName: ctypes.c_char_p, _handle: maptype.HWND) -> int:
        return mapOptimizationRstByName_t (_rswName, _handle)

    mapOptimizationRstByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOptimizationRstByNameUn', maptype.PWCHAR, maptype.HWND)
    def mapOptimizationRstByNameUn(_rswName: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        return mapOptimizationRstByNameUn_t (_rswName.buffer(), _handle)


# Запросить количество созданных уменьшенных копий в растре
# hMap       - идентификатор открытой основной векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstDuplicatesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstDuplicatesCount', maptype.HMAP, ctypes.c_int)
    def mapGetRstDuplicatesCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstDuplicatesCount_t (_hMap, _number)


# Обновить уменьшенную копию
# Если уменьшенные копии не существуют, создаются ТРИ копии
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapUpdateRstDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRstDuplicates', maptype.HMAP, ctypes.c_int)
    def mapUpdateRstDuplicates(_hMap: maptype.HMAP, _number: int) -> int:
        return mapUpdateRstDuplicates_t (_hMap, _number)


# Обновить уменьшенную копию
# Если уменьшенные копии не существуют, создаются ДВЕ копии
# hmap - идентификатор открытых данных
# number - номер файла растра в списке растров (в цепочке)
# hpaint - контекст поддержки многопоточного вызова (см. mapCreatePaintControl)
# При ошибке возвращает ноль

    mapUpdateRstDuplicatesEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRstDuplicatesEx', maptype.HMAP, ctypes.c_int, maptype.HPAINT)
    def mapUpdateRstDuplicatesEx(_hMap: maptype.HMAP, _number: int, _hPaint: maptype.HPAINT) -> int:
        return mapUpdateRstDuplicatesEx_t (_hMap, _number, _hPaint)


# Обновить уменьшенную копию блока (string,column) растра
# При ошибке возвращает ноль

    mapUpdateRstDuplicateOfBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateRstDuplicateOfBlock', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapUpdateRstDuplicateOfBlock(_hMap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        return mapUpdateRstDuplicateOfBlock_t (_hMap, _number, _string, _column)


# Запросить пользовательский идентификатор растра
# number    - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstUserLabel', maptype.HMAP, ctypes.c_int)
    def mapGetRstUserLabel(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstUserLabel_t (_hMap, _number)


# Установить пользовательский идентификатор растра
# number    - номер файла в цепочке
# userLabel - идентификатор модели
# При ошибке возвращает ноль

    mapSetRstUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstUserLabel', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstUserLabel(_hMap: maptype.HMAP, _number: int, _userLabel: int) -> int:
        return mapSetRstUserLabel_t (_hMap, _number, _userLabel)


# Запросить координаты Юго-Западного угла растра в метрах
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла в цепочке
# По адресу x,y записываются координаты найденной точки в метрах
# При ошибке возвращает 0

    mapWhereSouthWestRstPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhereSouthWestRstPlane', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapWhereSouthWestRstPlane(_hMap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapWhereSouthWestRstPlane_t (_hMap, _number, _x, _y)


# Удалить файл RSW
# Функция предназначена для удаления растра и его составных частей
# Растровая карта размером более 4Gb состоит из 2-х файлов: #.rsw и #.rsw.01
# Анолог функции DeleteTheFile()

    mapDeleteRstFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRstFile', ctypes.c_char_p)
    def mapDeleteRstFile(_name: ctypes.c_char_p) -> int:
        return mapDeleteRstFile_t (_name)

    mapDeleteRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteRstFileUn', maptype.PWCHAR)
    def mapDeleteRstFileUn(_name: mapsyst.WTEXT) -> int:
        return mapDeleteRstFileUn_t (_name.buffer())


# Переименовать имя файла RSW
# Функция предназначена для переименовывания растра и его составных частей
# Растровая карта размером более 4Gb состоит из 2-х файлов: #.rsw и #.rsw.01
# Анолог функции MoveTheFile()

    mapMoveRstFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveRstFile', ctypes.c_char_p, ctypes.c_char_p)
    def mapMoveRstFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p) -> int:
        return mapMoveRstFile_t (_oldname, _newname)

    mapMoveRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveRstFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveRstFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        return mapMoveRstFileUn_t (_oldname.buffer(), _newname.buffer())


# Скопировать файл RSW
# Функция предназначена для копирования растра и его составных частей
# Растровая карта размером более 4Gb состоит из 2-х файлов: #.rsw и #.rsw.01
# Аналог функции CopyTheFile()

    mapCopyRstFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyRstFile', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapCopyRstFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p, _exist: int = 0) -> int:
        return mapCopyRstFile_t (_oldname, _newname, _exist)

    mapCopyRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyRstFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyRstFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int = 0) -> int:
        return mapCopyRstFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)


# Запросить тип растра
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# Возвращает: 0 - обычный растр
#             1 - растр-пустышка с прямым доступом к файлу TIFF

    mapRstIsAccessTiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRstIsAccessTiff', maptype.HMAP, ctypes.c_int)
    def mapRstIsAccessTiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapRstIsAccessTiff_t (_hMap, _number)


# Запросить имя TIFF-файла для растра с номером  number (макс. длина строки = MAX_PATH)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstFileName_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFileName_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_char_p)
    def mapGetRstFileName_Tiff(_hMap: maptype.HMAP, _number: int, _name: ctypes.c_char_p) -> int:
        return mapGetRstFileName_Tiff_t (_hMap, _number, _name)


# Запросить имя TIFF-файла для растра с номером  number
# hMap     - идентификатор открытой векторной карты
# number   - номер файла в цепочке
# name     - возвращаемое имя
# namesize - размер строки в БАЙТАХ

    mapGetRstFileName_TiffUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstFileName_TiffUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRstFileName_TiffUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetRstFileName_TiffUn_t (_hMap, _number, _name.buffer(), _namesize)


# Запросить матрицу аффинных коэффициентов привязки TIFF-файла
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# affincoef - возвращаемая матрица аффинных коэффициентов привязки
# При ошибке возвращает ноль

    mapGetRstAffinCoef_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstAffinCoef_Tiff', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.AFFINCOEF))
    def mapGetRstAffinCoef_Tiff(_hMap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        return mapGetRstAffinCoef_Tiff_t (_hMap, _number, _affincoef)


# Установить матрицу аффинных коэффициентов привязки TIFF-файла
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# affincoef - устанавливаемая матрица аффинных коэффициентов привязки
# При ошибке возвращает ноль

    mapSetRstAffinCoef_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstAffinCoef_Tiff', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetRstAffinCoef_Tiff(_hMap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        return mapSetRstAffinCoef_Tiff_t (_hMap, _number, _affincoef)


# Запросить количество каналов TIFF-растра с номером  number
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstBandCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBandCount_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBandCount_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBandCount_Tiff_t (_hMap, _number)


# Запросить номер канала TIFF-растра с номером  number, отображаемого красным
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstRedBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstRedBand_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstRedBand_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstRedBand_Tiff_t (_hMap, _number)


# Запросить номер канала TIFF-растра с номером  number, отображаемого зеленым
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstGreenBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstGreenBand_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstGreenBand_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstGreenBand_Tiff_t (_hMap, _number)


# Запросить номер канала TIFF-растра с номером  number, отображаемого синим
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstBlueBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlueBand_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlueBand_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlueBand_Tiff_t (_hMap, _number)


# Установить номер канала TIFF-растра с номером  number, отображаемого красным
# (если установить -1, то такой канал не используется)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstRedBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstRedBand_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstRedBand_Tiff(_hMap: maptype.HMAP, _number: int, _redband: int) -> int:
        return mapSetRstRedBand_Tiff_t (_hMap, _number, _redband)


# Установить номер канала TIFF-растра с номером  number, отображаемого зеленым
# (если установить -1, то такой канал не используется)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstGreenBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstGreenBand_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstGreenBand_Tiff(_hMap: maptype.HMAP, _number: int, _greenband: int) -> int:
        return mapSetRstGreenBand_Tiff_t (_hMap, _number, _greenband)


# Установить номер канала TIFF-растра с номером  number, отображаемого синим
# (если установить -1, то такой канал не используется)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstBlueBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstBlueBand_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstBlueBand_Tiff(_hMap: maptype.HMAP, _number: int, _blueband: int) -> int:
        return mapSetRstBlueBand_Tiff_t (_hMap, _number, _blueband)


# Установить отображение мультиспектрального растра по вегетационному индексу
# Перед вызовом необходимо убедиться при помощи функции mapRstIsAccessTiff, что
# для растра с номером number осуществляется прямой доступ к файлу TIFF
# Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_Tiff() >= 3)

    mapSetRstVegIndex_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstVegIndex_Tiff', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.VEGINDEX))
    def mapSetRstVegIndex_Tiff(_hMap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        return mapSetRstVegIndex_Tiff_t (_hMap, _number, _vegindex)


# Возвращает параметры отображения вегетационного индекса
# Если отображение по вегетационному индексу не установлено возвращает 0
# Перед вызовом необходимо убедиться при помощи функции mapRstIsAccessTiff, что
# для растра с номером number осуществляется прямой доступ к файлу TIFF
# Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_Tiff() >= 3)

    mapGetRstVegIndex_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstVegIndex_Tiff', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.VEGINDEX))
    def mapGetRstVegIndex_Tiff(_hMap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        return mapGetRstVegIndex_Tiff_t (_hMap, _number, _vegindex)


# Начинает буферизированное чтение пикселей функцией mapGetRstBandPixel_Tiff
# После завершения чтения пикселей необходимо вызвать mapEndRstPixelReading_Tiff

    mapBeginRstPixelReading_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBeginRstPixelReading_Tiff', maptype.HMAP, ctypes.c_int)
    def mapBeginRstPixelReading_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapBeginRstPixelReading_Tiff_t (_hMap, _number)


# Заканчивает буферизированное чтение пикселей функцией mapGetRstBandPixel_Tiff

    mapEndRstPixelReading_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapEndRstPixelReading_Tiff', maptype.HMAP, ctypes.c_int)
    def mapEndRstPixelReading_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapEndRstPixelReading_Tiff_t (_hMap, _number)


# Возвращает яркость пиксела изображения на канал bandnum
# Если вызвается не внутри блока mapBeginRstPixelReading_Tiff -
# mapEndRstPixelReading_Tiff, то чтение выполняется очень медленно
# x, y  - координаты пикселя в системе координат растра (в пикселях)
# color - возвращаемое значение реально записанное в растре (может быть 1,4,8,16 бит)
# bandnum - номер канала (от 0 до mapGetRstBandCount_Tiff - 1)
# При ошибке возвращает 0

    mapGetRstBandPixel_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBandPixel_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetRstBandPixel_Tiff(_hMap: maptype.HMAP, _number: int, _x: int, _y: int, _bandnum: int, _color: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRstBandPixel_Tiff_t (_hMap, _number, _x, _y, _bandnum, _color)


# Устанавливает радиус клетки в узлах которой пересчет координат выполняется
# по строгим формулам при отрисовке растра в системе координат, отличной от
# системы координат растра.
# Между узлами пересчет координат выполняется линейной интерполяцией. Коэффициенты
# линейного пересчета внутри клетки вычисляются по двум верхним узлам клетки.
# При увеличении радиуса увеличивается скорость отрисовки, но ухудшается качество
# изображения при значительной деформации системы координат отрисовки относительно
# системы координат растра (изображение сегментируется по размеру клетки).
# Этот параметр является глобальным, т.е. с момента установки все растры
# отрисовываются с использовнаием этого параметра
# radius - устанавливаемый радиус клетки в пикселях (не может быть меньше 0).
#          Если равен 0, то все пикселы вычисляются по строгим формулам.
#          Значение по умолчанию 3.
# При ошибке возвращает 0

    mapSetRstPaintCellRadius_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstPaintCellRadius_Tiff', ctypes.c_int)
    def mapSetRstPaintCellRadius_Tiff(_radius: int) -> int:
        return mapSetRstPaintCellRadius_Tiff_t (_radius)


# Возвращает радиус клетки в узлах которой пересчет координат выполняется
# по строгим формулам при отрисовке растра в системе координат, отличной от
# системы координат растра.

    mapGetRstPaintCellRadius_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPaintCellRadius_Tiff')
    def mapGetRstPaintCellRadius_Tiff() -> int:
        return mapGetRstPaintCellRadius_Tiff_t ()


# Возвращает глубину цвета на канал (1, 4, 8, 16)
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBitInBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBitInBand_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBitInBand_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBitInBand_Tiff_t (_hMap, _number)


# Возвращает гистограмму
# Гистограмма - поканальный массив количества пикселей, присутствующих в растре
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# count     - количество элементов в массиве histogram
#             количество элементов вычисляется по формуле
#             count = BandCount # (1 << BitInBand)
#             Для палитровых растров BandCount = 1
#             для 1 битных растров (палитровых) count = 2
#             для 4 битных растров (палитровых) count = 16
#             для 8 битных растров (палитровых) count = 256
#             для RGB                           count = 3 # 256 = 768
#             для 8  битных мультиспектральных  count = BandCount # 256
#             для 16 битных мультиспектральных  count = BandCount # 65536
# histogram - возвращаемая гистограмма
# При ошибке возвращает 0

    mapGetRstHistogram_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstHistogram_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DWORD))
    def mapGetRstHistogram_Tiff(_hMap: maptype.HMAP, _number: int, _count: int, _histogram: ctypes.POINTER(maptype.DWORD)) -> int:
        return mapGetRstHistogram_Tiff_t (_hMap, _number, _count, _histogram)


# Возвращает таблицу преобразования цвета для отображения панхроматических,
# RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# bandnum   - номер канала (от 0 до mapGetRstBandCount_Tiff - 1)
# table     - возвращаемая таблица преобразования
# tablesize - размер таблицы table (для 8 бит должно быть 256, для 16 бит - 65536)
# При ошибке возвращает 0

    mapGetRstLookupTable_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstLookupTable_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def mapGetRstLookupTable_Tiff(_hMap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        return mapGetRstLookupTable_Tiff_t (_hMap, _number, _bandnum, _table, _tablesize)


# Устанавливает таблицу преобразования цвета для отображения панхроматических,
# RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# bandnum   - номер канала (от 0 до mapGetRstBandCount_Tiff - 1)
# table     - возвращаемая таблица преобразования
# tablesize - размер таблицы table (для 8 бит должно быть не меньше 256,
#                                   для 16 бит - не меньше 65536)
# При ошибке возвращает 0

    mapSetRstLookupTable_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstLookupTable_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def mapSetRstLookupTable_Tiff(_hMap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        return mapSetRstLookupTable_Tiff_t (_hMap, _number, _bandnum, _table, _tablesize)


# Возвращает ширину блока в пикселях
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockWidth_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockWidth_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockWidth_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockWidth_Tiff_t (_hMap, _number)


# Возвращает высоту блока в пикселях
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockHeight_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockHeight_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockHeight_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockHeight_Tiff_t (_hMap, _number)


# Возвращает способ расположения цветовых составляющих пикселя в блоке
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# Возвращаемые значения:
# 0 - ошибка выполнения
# 1 - последовательно RGB RGB ...
# 2 - по цветовым плоскостям  RRR... GGG... BBB...

    mapGetRstBlockPixelType_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockPixelType_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockPixelType_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockPixelType_Tiff_t (_hMap, _number)


# Возвращает количество строк блоков
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockRowCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockRowCount_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockRowCount_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockRowCount_Tiff_t (_hMap, _number)


# Возвращает количество столбцов блоков
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockColCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockColCount_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockColCount_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockColCount_Tiff_t (_hMap, _number)


# Возвращает размер блока в байтах
# Для 1 и 4 битных растров в блок записывается 1 байт на пиксель
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockSize_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockSize_Tiff', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockSize_Tiff(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockSize_Tiff_t (_hMap, _number)


# Считывает блок из растра
# Для 1 и 4 битных растров в блок записывается 1 байт на пиксель
# hMap     - идентификатор открытой векторной карты
# number   - номер файла в цепочке
# blockrow - номер строки блоков
# blockcol - номер столбца блоков
# buf      - буфер, в который записывается изображение блока
# bifsize  - размер блока (должен быть равен mapGetRstBlockSize_Tiff)
# При ошибке возвращает 0

    mapGetRstBlock_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlock_Tiff', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetRstBlock_Tiff(_hMap: maptype.HMAP, _number: int, _blockrow: int, _blockcol: int, _buf: ctypes.c_char_p, _bufsize: int) -> int:
        return mapGetRstBlock_Tiff_t (_hMap, _number, _blockrow, _blockcol, _buf, _bufsize)


# Проверяет файл TIF на возможность открытия без преобразования в формат RSW
# При ошибке возвращает 0

    mapIsTiffOpenWithoutConvert_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTiffOpenWithoutConvert', ctypes.c_char_p)
    def mapIsTiffOpenWithoutConvert(_name: ctypes.c_char_p) -> int:
        return mapIsTiffOpenWithoutConvert_t (_name)

    mapIsTiffOpenWithoutConvertUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTiffOpenWithoutConvertUn', maptype.PWCHAR)
    def mapIsTiffOpenWithoutConvertUn(_name: mapsyst.WTEXT) -> int:
        return mapIsTiffOpenWithoutConvertUn_t (_name.buffer())


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ СОЗДАНИЯ TIFF ФАЙЛОВ +++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Создает TIFF файл
# filename - имя создаваемого TIFF файла
# width    - ширина растра в пикселях
# height   - высота растра в пикселях
# parm     - параметры создания растра
# Возвращает идентификатор созданного растра
# При ошибке возвращает 0

    mapCreateTiffEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateTiffEx', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.CREATETIFPARMEX))
    def mapCreateTiffEx(_filename: ctypes.c_char_p, _width: int, _height: int, _parm: ctypes.POINTER(maptype.CREATETIFPARMEX)) -> ctypes.c_void_p:
        return mapCreateTiffEx_t (_filename, _width, _height, _parm)

    mapCreateTiffExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateTiffExUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.CREATETIFPARMEX))
    def mapCreateTiffExUn(_filename: mapsyst.WTEXT, _width: int, _height: int, _parm: ctypes.POINTER(maptype.CREATETIFPARMEX)) -> ctypes.c_void_p:
        return mapCreateTiffExUn_t (_filename.buffer(), _width, _height, _parm)

#   mapCreateTiff_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateTiff', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(CREATETIFPARM))
#   def mapCreateTiff(_filename: ctypes.c_char_p, _width: int, _height: int, _parm: ctypes.POINTER(CREATETIFPARM)) -> ctypes.c_void_p:
#       return mapCreateTiff_t (_filename, _width, _height, _parm)

#   mapCreateTiffUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateTiffUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(CREATETIFPARM))
#   def mapCreateTiffUn(_filename: mapsyst.WTEXT, _width: int, _height: int, _parm: ctypes.POINTER(CREATETIFPARM)) -> ctypes.c_void_p:
#       return mapCreateTiffUn_t (_filename, _width, _height, _parm)


# Освобождает идентификатор создания TIFF файла
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx

    mapFreeTiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeTiff', ctypes.c_void_p)
    def mapFreeTiff(_tiff: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeTiff_t (_tiff)


# Возвращает ширину блока в пикселях
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapGetTiffBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTiffBlockWidth', ctypes.c_void_p)
    def mapGetTiffBlockWidth(_tiff: ctypes.c_void_p) -> int:
        return mapGetTiffBlockWidth_t (_tiff)


# Возвращает высоту блока в пикселях
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapGetTiffBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTiffBlockHeight', ctypes.c_void_p)
    def mapGetTiffBlockHeight(_tiff: ctypes.c_void_p) -> int:
        return mapGetTiffBlockHeight_t (_tiff)


# Возвращает количество строк блоков
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapGetTiffBlockRowCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTiffBlockRowCount', ctypes.c_void_p)
    def mapGetTiffBlockRowCount(_tiff: ctypes.c_void_p) -> int:
        return mapGetTiffBlockRowCount_t (_tiff)


# Возвращает количество столбцов блоков
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapGetTiffBlockColCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTiffBlockColCount', ctypes.c_void_p)
    def mapGetTiffBlockColCount(_tiff: ctypes.c_void_p) -> int:
        return mapGetTiffBlockColCount_t (_tiff)


# Возвращает тип пикселя на канал (см. PT_BYTE и т.д.)
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapGetTiffBandPixelType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTiffBandPixelType', ctypes.c_void_p)
    def mapGetTiffBandPixelType(_tiff: ctypes.c_void_p) -> int:
        return mapGetTiffBandPixelType_t (_tiff)


# Пишет блок в файл
# tiff    - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# bandnum - номер канала
# col     - номер столбца тайла
# row     - номер строки тайла
# image   - изображение тайла
#           Ширина, высота тайла запрашивается через mapGetTiffBlockWidth, mapGetTiffBlockHeight
#           Размер пикселя в байтах зависит от типа пикселя, определяемый через GetTiffBandPixelType
#           В последних строках и столбцах размер тайла не усеченный
# При ошибке возвращает 0

    mapWriteTiffBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWriteTiffBlock', ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
    def mapWriteTiffBlock(_tiff: ctypes.c_void_p, _bandnum: int, _col: int, _row: int, _image: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mapWriteTiffBlock_t (_tiff, _bandnum, _col, _row, _image)


# Устанавливает матрицу привязки растра
# tiff - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# coef - матрица, связывающая систему координат растра в пикселях с системой координат местности в метрах
#        Xmeter = coef->A0 + coef->A1 # Xpix + coef->A2 # Ypix
#        Ymeter = coef->B0 + coef->B1 # Xpix + coef->B2 # Ypix
#        Направление осей
#        -------------Xrst
#        |    Ymeter
#        |      |
#        Yrst   |
#               ---------- Xmeter
# При ошибке возвращает 0

    mapSetTiffLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTiffLocation', ctypes.c_void_p, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetTiffLocation(_tiff: ctypes.c_void_p, _coef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        return mapSetTiffLocation_t (_tiff, _coef)


# Устанавливает параметры системы координат растра
# tiff      - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# mapreg    - параметры проекции
# ellipsoid - параметры эллипсоида
# datum     - датум
# При ошибке возвращает 0

    mapSetTiffProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTiffProjection', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetTiffProjection(_tiff: ctypes.c_void_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetTiffProjection_t (_tiff, _mapreg, _ellipsoid, _datum)


# Тип системы координат соответствует геодезической СК?
# tiff      - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# При ошибке возвращает 0

    mapTiffIsGeographic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTiffIsGeographic', ctypes.c_void_p)
    def mapTiffIsGeographic(_tiff: ctypes.c_void_p) -> int:
        return mapTiffIsGeographic_t (_tiff)


# Устанавливает значение NoData для канала
# tiff    - идентификатор, полученный при создании TIFF файла функцией mapCreateTiffEx
# bandnum - номер канала
# value   - значение NoData
# При ошибке возвращает 0

    mapSetTiffNoDataValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTiffNoDataValue', ctypes.c_void_p, ctypes.c_int, ctypes.c_double)
    def mapSetTiffNoDataValue(_tiff: ctypes.c_void_p, _bandnum: int, _value: float) -> int:
        return mapSetTiffNoDataValue_t (_tiff, _bandnum, _value)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К ГРАФИЧЕСКИМ ФАЙЛАМ +++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Запросить тип растра
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# Возвращает: 0 - обычный растр
#             1 - растр-пустышка с прямым доступом к графическому файлу
#                 (TIFF, GeoTIFF, IMG, JPEG, PNG, GIF, BMP)
# При ошибке возвращает 0

    mapRstIsAccessGraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRstIsAccessGraphicFile', maptype.HMAP, ctypes.c_int)
    def mapRstIsAccessGraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapRstIsAccessGraphicFile_t (_hMap, _number)


# Запросить имя графического файла для растра с номером  number
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap     - идентификатор открытой векторной карты
# number   - номер файла в цепочке
# name     - возвращаемое имя
# namesize - размер строки в БАЙТАХ
# При ошибке возвращает 0

    mapGetRstGraphicFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstGraphicFileNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetRstGraphicFileNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetRstGraphicFileNameUn_t (_hMap, _number, _name.buffer(), _namesize)


# Запросить имя графического файла, применяемого для хранения канала изображения numberBand,
# для растра с номером  number
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# Количество графических файлов, применяемых для хранения каналов изображения,
# запрашивается вызом функции mapGetRstBandFilesCount_GraphicFile
# hMap     - идентификатор открытой векторной карты
# number   - номер файла в цепочке
# name     - возвращаемое имя
# namesize - размер строки в БАЙТАХ
# numberBand - номер канала изображения (начиная с 1)
# При ошибке возвращает 0

    mapGetRstGraphicBandFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstGraphicBandFileNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetRstGraphicBandFileNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int, _numberBand: int) -> int:
        return mapGetRstGraphicBandFileNameUn_t (_hMap, _number, _name.buffer(), _namesize, _numberBand)


# Запросить матрицу аффинных коэффициентов привязки графического файла
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# affincoef - возвращаемая матрица аффинных коэффициентов привязки
# При ошибке возвращает ноль

    mapGetRstAffinCoef_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstAffinCoef_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.AFFINCOEF))
    def mapGetRstAffinCoef_GraphicFile(_hMap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        return mapGetRstAffinCoef_GraphicFile_t (_hMap, _number, _affincoef)


# Установить матрицу аффинных коэффициентов привязки графического файла
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# affincoef - устанавливаемая матрица аффинных коэффициентов привязки
# При ошибке возвращает ноль

    mapSetRstAffinCoef_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstAffinCoef_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetRstAffinCoef_GraphicFile(_hMap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        return mapSetRstAffinCoef_GraphicFile_t (_hMap, _number, _affincoef)


# Запросить количество каналов графического файла с номером  number
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBandCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBandCount_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBandCount_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBandCount_GraphicFile_t (_hMap, _number)


# Запросить количество графических файлов, применяемых для хранения каналов изображения.
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetRstBandFilesCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBandFilesCount_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBandFilesCount_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBandFilesCount_GraphicFile_t (_hMap, _number)


# Запросить номер канала графического файла с номером  number, отображаемого красным
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstRedBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstRedBand_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstRedBand_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstRedBand_GraphicFile_t (_hMap, _number)


# Запросить номер канала графического файла с номером  number, отображаемого зеленым
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstGreenBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstGreenBand_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstGreenBand_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstGreenBand_GraphicFile_t (_hMap, _number)


# Запросить номер канала графического файла с номером  number, отображаемого синим
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapGetRstBlueBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlueBand_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlueBand_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlueBand_GraphicFile_t (_hMap, _number)


# Установить номер канала графического файла с номером  number, отображаемого красным
# (если установить -1, то такой канал не используется)
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstRedBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstRedBand_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstRedBand_GraphicFile(_hMap: maptype.HMAP, _number: int, _redband: int) -> int:
        return mapSetRstRedBand_GraphicFile_t (_hMap, _number, _redband)


# Установить номер канала графического файла с номером  number, отображаемого зеленым
# (если установить -1, то такой канал не используется)
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstGreenBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstGreenBand_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstGreenBand_GraphicFile(_hMap: maptype.HMAP, _number: int, _greenband: int) -> int:
        return mapSetRstGreenBand_GraphicFile_t (_hMap, _number, _greenband)


# Установить номер канала графического файла с номером  number, отображаемого синим
# (если установить -1, то такой канал не используется)
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке

    mapSetRstBlueBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstBlueBand_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetRstBlueBand_GraphicFile(_hMap: maptype.HMAP, _number: int, _blueband: int) -> int:
        return mapSetRstBlueBand_GraphicFile_t (_hMap, _number, _blueband)


# Установить отображение мультиспектрального растра по вегетационному индексу
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# Функция справедлива для мультиспектральных изображений
#                                     (mapGetRstBandCount_GraphicFile() >= 3)
# При ошибке возвращает 0

    mapSetRstVegIndex_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstVegIndex_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.VEGINDEX))
    def mapSetRstVegIndex_GraphicFile(_hMap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        return mapSetRstVegIndex_GraphicFile_t (_hMap, _number, _vegindex)


# Возвращает параметры отображения вегетационного индекса
# Если отображение по вегетационному индексу не установлено возвращает 0
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# Функция справедлива для мультиспектральных изображений
#                                     (mapGetRstBandCount_GraphicFile() >= 3)
# При ошибке возвращает 0

    mapGetRstVegIndex_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstVegIndex_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.VEGINDEX))
    def mapGetRstVegIndex_GraphicFile(_hMap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        return mapGetRstVegIndex_GraphicFile_t (_hMap, _number, _vegindex)


# Возвращает яркость пиксела изображения на канал bandnum
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# x, y  - координаты пикселя в системе координат растра (в пикселях)
# color - возвращаемое значение реально записанное в растре (может быть 1,4,8,16 бит)
# bandnum - номер канала (от 0 до mapGetRstBandCount_GraphicFile - 1)
# При ошибке возвращает 0

    mapGetRstBandPixel_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBandPixel_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetRstBandPixel_GraphicFile(_hMap: maptype.HMAP, _number: int, _x: int, _y: int, _bandnum: int, _color: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetRstBandPixel_GraphicFile_t (_hMap, _number, _x, _y, _bandnum, _color)


# Устанавливает радиус клетки в узлах которой пересчет координат выполняется
# по строгим формулам при отрисовке растра в системе координат, отличной от
# системы координат растра.
# Между узлами пересчет координат выполняется линейной интерполяцией. Коэффициенты
# линейного пересчета внутри клетки вычисляются по двум верхним узлам клетки.
# При увеличении радиуса увеличивается скорость отрисовки, но ухудшается качество
# изображения при значительной деформации системы координат отрисовки относительно
# системы координат растра (изображение сегментируется по размеру клетки).
# Этот параметр является глобальным, т.е. с момента установки все растры
# отрисовываются с использовнаием этого параметра
# radius - устанавливаемый радиус клетки в пикселях (не может быть меньше 0).
#          Если равен 0, то все пикселы вычисляются по строгим формулам.
#          Значение по умолчанию 3.

    mapSetRstPaintCellRadius_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstPaintCellRadius_GraphicFile', ctypes.c_int)
    def mapSetRstPaintCellRadius_GraphicFile(_radius: int) -> int:
        return mapSetRstPaintCellRadius_GraphicFile_t (_radius)


# Возвращает радиус клетки в узлах которой пересчет координат выполняется
# по строгим формулам при отрисовке растра в системе координат, отличной от
# системы координат растра.

    mapGetRstPaintCellRadius_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstPaintCellRadius_GraphicFile')
    def mapGetRstPaintCellRadius_GraphicFile() -> int:
        return mapGetRstPaintCellRadius_GraphicFile_t ()


# Возвращает глубину цвета на канал (1, 4, 8, 16)
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBitInBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBitInBand_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBitInBand_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBitInBand_GraphicFile_t (_hMap, _number)


# Возвращает гистограмму
# Гистограмма - поканальный массив количества пикселей, присутствующих в растре
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# count     - количество элементов в массиве histogram
#             количество элементов вычисляется по формуле
#             count = BandCount # (1 << BitInBand)
#             Для палитровых растров BandCount = 1
#             для 1 битных растров (палитровых) count = 2
#             для 4 битных растров (палитровых) count = 16
#             для 8 битных растров (палитровых) count = 256
#             для RGB                           count = 3 # 256 = 768
#             для 8  битных мультиспектральных  count = BandCount # 256
#             для 16 битных мультиспектральных  count = BandCount # 65536
# histogram - возвращаемая гистограмма
# При ошибке возвращает 0

    mapGetRstHistogram_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstHistogram_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DWORD))
    def mapGetRstHistogram_GraphicFile(_hMap: maptype.HMAP, _number: int, _count: int, _histogram: ctypes.POINTER(maptype.DWORD)) -> int:
        return mapGetRstHistogram_GraphicFile_t (_hMap, _number, _count, _histogram)


# Возвращает таблицу преобразования цвета для отображения панхроматических,
# RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# bandnum   - номер канала (от 0 до mapGetRstBandCount_GraphicFile - 1)
# table     - возвращаемая таблица преобразования
# tablesize - размер таблицы table (для 8 бит должно быть 256, для 16 бит - 65536)
# При ошибке возвращает 0

    mapGetRstLookupTable_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstLookupTable_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def mapGetRstLookupTable_GraphicFile(_hMap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        return mapGetRstLookupTable_GraphicFile_t (_hMap, _number, _bandnum, _table, _tablesize)


# Устанавливает таблицу преобразования цвета для отображения панхроматических,
# RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# bandnum   - номер канала (от 0 до mapGetRstBandCount_GraphicFile - 1)
# table     - возвращаемая таблица преобразования
# tablesize - размер таблицы table (для 8 бит должно быть не меньше 256,
#                                   для 16 бит - не меньше 65536)
# При ошибке возвращает 0

    mapSetRstLookupTable_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRstLookupTable_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def mapSetRstLookupTable_GraphicFile(_hMap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        return mapSetRstLookupTable_GraphicFile_t (_hMap, _number, _bandnum, _table, _tablesize)


# Возвращает ширину блока в пикселях
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockWidth_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockWidth_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockWidth_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockWidth_GraphicFile_t (_hMap, _number)


# Возвращает высоту блока в пикселях
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockHeight_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockHeight_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockHeight_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockHeight_GraphicFile_t (_hMap, _number)


# Возвращает способ расположения цветовых составляющих пикселя в блоке
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# Возвращаемые значения:
# 0 - ошибка выполнения
# 1 - последовательно RGB RGB ...
# 2 - по цветовым плоскостям  RRR... GGG... BBB...

    mapGetRstBlockPixelType_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockPixelType_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockPixelType_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockPixelType_GraphicFile_t (_hMap, _number)


# Возвращает количество строк блоков
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockRowCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockRowCount_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockRowCount_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockRowCount_GraphicFile_t (_hMap, _number)


# Возвращает количество столбцов блоков
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockColCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockColCount_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockColCount_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockColCount_GraphicFile_t (_hMap, _number)


# Возвращает размер блока в байтах
# Для 1 и 4 битных растров в блок записывается 1 байт на пиксель
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap   - идентификатор открытой векторной карты
# number - номер файла в цепочке
# При ошибке возвращает 0

    mapGetRstBlockSize_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlockSize_GraphicFile', maptype.HMAP, ctypes.c_int)
    def mapGetRstBlockSize_GraphicFile(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRstBlockSize_GraphicFile_t (_hMap, _number)


# Считывает блок из растра
# Для 1 и 4 битных растров в блок записывается 1 байт на пиксель
# Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
# что для растра с номером number осуществляется прямой доступ к графическому файлу
# hMap     - идентификатор открытой векторной карты
# number   - номер файла в цепочке
# blockrow - номер строки блоков
# blockcol - номер столбца блоков
# buf      - буфер, в который записывается изображение блока
# bifsize  - размер блока (должен быть равен mapGetRstBlockSize_GraphicFile)
# При ошибке возвращает 0

    mapGetRstBlock_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRstBlock_GraphicFile', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetRstBlock_GraphicFile(_hMap: maptype.HMAP, _number: int, _blockrow: int, _blockcol: int, _buf: ctypes.c_char_p, _bufsize: int) -> int:
        return mapGetRstBlock_GraphicFile_t (_hMap, _number, _blockrow, _blockcol, _buf, _bufsize)


# Проверяет графический файл на возможность открытия без преобразования в формат RSW

    mapIsGraphicFileOpenWithoutConvert_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsGraphicFileOpenWithoutConvert', ctypes.c_char_p)
    def mapIsGraphicFileOpenWithoutConvert(_name: ctypes.c_char_p) -> int:
        return mapIsGraphicFileOpenWithoutConvert_t (_name)

    mapIsGraphicFileOpenWithoutConvertUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsGraphicFileOpenWithoutConvertUn', maptype.PWCHAR)
    def mapIsGraphicFileOpenWithoutConvertUn(_name: mapsyst.WTEXT) -> int:
        return mapIsGraphicFileOpenWithoutConvertUn_t (_name.buffer())


# Запросить список файлов данных, относящихся к растру/матрице
# name  - имя файла данных формата RSW, MTW или MTQ
# error - указатель на поле для записи кода ошибки (см. maperr.rh)
# Если файл данных один - возвращает ноль
# Если список файлов сформирован - возвращает идентификатор списка,
# который нужно освободить после чтения списка - mapFreeRmfDataFiles
# При ошибке возвращает ноль

    mapGetRmfDataFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetRmfDataFiles', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapGetRmfDataFiles(_name: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> ctypes.c_void_p:
        return mapGetRmfDataFiles_t (_name.buffer(), _error)


# Запросить число элементов списка файлов данных, относящихся к растру/матрице
# handle - идентификатор списка, полученный в функции mapGetRmfDataFiles
# При ошибке возвращает ноль

    mapGetRmfDataFilesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRmfDataFilesCount', ctypes.c_void_p)
    def mapGetRmfDataFilesCount(_handle: ctypes.c_void_p) -> int:
        return mapGetRmfDataFilesCount_t (_handle)


# Освободить память под список файлов данных, относящихся к растру/матрице
# handle - идентификатор списка, полученный в функции mapGetRmfDataFiles

    mapFreeRmfDataFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeRmfDataFiles', ctypes.c_void_p)
    def mapFreeRmfDataFiles(_handle: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeRmfDataFiles_t (_handle)


# Сформировать имя выходного файла растровых данных
# inputFileName - имя исходного файла RSW
# postfix       - добавляемфй суффикс к имени файла
# ext           - расширение выходного файла
# outputName    - указатель для размещения имени выходного файла
# При ошибке возвращает ноль

    mapCreateOutputFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateOutputFileName', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCreateOutputFileName(_hMap: maptype.HMAP, _inputFileName: mapsyst.WTEXT, _postfix: mapsyst.WTEXT, _ext: mapsyst.WTEXT, _outputName: mapsyst.WTEXT, _sizeOutputName: int) -> int:
        return mapCreateOutputFileName_t (_hMap, _inputFileName.buffer(), _postfix.buffer(), _ext.buffer(), _outputName.buffer(), _sizeOutputName)

except Exception as e:
    print(e)
    acceslib = 0
