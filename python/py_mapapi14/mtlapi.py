#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class BUILDMTL(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_uint),
                ("MtwNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("EndX",ctypes.c_double),
                ("EndY",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("LayerCount",ctypes.c_int),
                ("LayerForm",ctypes.c_int),
                ("HeightSizeBytes",ctypes.c_int),
                ("LayerSizeBytes",ctypes.c_int),
                ("HeightMeasure",ctypes.c_int),
                ("LayerMeasure",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("BlockSide",ctypes.c_int),
                ("CodeCount",ctypes.c_int),
                ("MtdPointFormat",ctypes.c_int),
                ("BigFormat",ctypes.c_int),
                ("Reserve",ctypes.c_char*64)]
#-----------------------------


#-----------------------------
class MTLBUILDPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_ulong),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("EndX",ctypes.c_double),
                ("EndY",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("LayerCount",ctypes.c_int),
                ("LayerForm",ctypes.c_int),
                ("HeightSizeBytes",ctypes.c_int),
                ("LayerSizeBytes",ctypes.c_int),
                ("HeightMeasure",ctypes.c_int),
                ("LayerMeasure",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("Reserve",ctypes.c_char*52)]
#-----------------------------


#-----------------------------
class MTLDESCRIBE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*260),
                ("MaterialFileName",ctypes.c_char*260),
                ("LayerCount",ctypes.c_long),
                ("MaterialCount",ctypes.c_long),
                ("ElementInPlane",ctypes.c_double),
                ("FrameMeters",maptype.DFRAME),
                ("MinHeightValue",ctypes.c_double),
                ("MaxHeightValue",ctypes.c_double),
                ("BotLevelHeight",ctypes.c_double),
                ("UserType",ctypes.c_long),
                ("View",ctypes.c_long),
                ("UserLabel",ctypes.c_long),
                ("ReliefPresence",ctypes.c_long),
                ("MaxSummaryPower",ctypes.c_double),
                ("Reserve",ctypes.c_char*408)]
#-----------------------------


#-----------------------------
class MTLDESCRIBEUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",maptype.WCHAR1*(maptype.MAX_PATH_LONG*2)),
                ("MaterialFileName",maptype.WCHAR1*(maptype.MAX_PATH_LONG*2)),
                ("FrameMeters",maptype.DFRAME),
                ("ElementInPlane",ctypes.c_double),
                ("MinHeightValue",ctypes.c_double),
                ("MaxHeightValue",ctypes.c_double),
                ("BotLevelHeight",ctypes.c_double),
                ("MaxSummaryPower",ctypes.c_double),
                ("LayerCount",ctypes.c_int),
                ("MaterialCount",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("View",ctypes.c_int),
                ("UserLabel",ctypes.c_int),
                ("ReliefPresence",ctypes.c_int),
                ("Reserve",ctypes.c_char*64)]
#-----------------------------


try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'


try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К МАТРИЦАМ СЛОЕВ +++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Открыть матричные данные
# Возвращает идентификатор открытой матричной карты (TMapAccess#)
# mtrname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenMtl_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtl', ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtl(_mtrname: ctypes.c_char_p, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtl_t (_mtrname, _mode)

    mapOpenMtlUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtlUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtlUn(_mtrname: mapsyst.WTEXT, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtlUn_t (_mtrname.buffer(), _mode)


# Открыть матричные данные в заданном районе работ
# (добавить в цепочку матриц)
# Возвращает номер файла в цепочке матриц
# hMap - идентификатор открытой основной карты
# mtrname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenMtlForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtlForMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtlForMap(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mode: int) -> int:
        return mapOpenMtlForMap_t (_hMap, _mtrname, _mode)

    mapOpenMtlForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtlForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtlForMapUn(_hMap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mode: int) -> int:
        return mapOpenMtlForMapUn_t (_hMap, _mtrname.buffer(), _mode)


# Закрыть матричные данные
# hMap - идентификатор открытой основной карты
# number - номер закрываемой матрицы в цепочке матриц
# если number == 0, закрываются все матричные данные

    mapCloseMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtl', maptype.HMAP, ctypes.c_int)
    def mapCloseMtl(_hMap: maptype.HMAP, _number: int = 0) -> ctypes.c_void_p:
        return mapCloseMtl_t (_hMap, _number)


# Закрыть матричные данные в заданном районе работ
# hMap - идентификатор открытой основной карты
# number - номер матричного файла в цепочке
# Если number == 0, закрываются все матричные данные
# При ошибке возвращает ноль

    mapCloseMtlForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseMtlForMap', maptype.HMAP, ctypes.c_int)
    def mapCloseMtlForMap(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCloseMtlForMap_t (_hMap, _number)


# Построение матрицы на заданный участок района работ
# При ошибке возвращает ноль
# hMap    - идентификатор исходной карты для построения матрицы,
# mtrname - полное имя файла создаваемой матрицы,
# ininame - полное имя файла легенды создаваемой матрицы,
# mtrparm - параметры создаваемой матрицы,
# Структурa BUILDMTL описанa в mtlapi.h
# hselect - идентификатор контекста отбора объектов карты,
# handle  - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#  0x0378 - сообщение о проценте выполненных работ (в WPARAM),
#  если процесс должен быть принудительно завершен, в ответ
#  должно вернуться значение 0x0378.
# Если handle равно нулю - сообщения не посылаются.

    mapBuildMtlEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtlEx', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(BUILDMTL), maptype.HSELECT, maptype.HWND)
    def mapBuildMtlEx(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _ininame: ctypes.c_char_p, _mtrparm: ctypes.POINTER(BUILDMTL), _hselect: maptype.HSELECT, _handle: maptype.HWND) -> int:
        return mapBuildMtlEx_t (_hMap, _mtrname, _ininame, _mtrparm, _hselect, _handle)

    mapBuildMtlUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtlUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDMTL), maptype.HSELECT, maptype.HWND)
    def mapBuildMtlUn(_hMap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _ininame: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL), _hselect: maptype.HSELECT, _handle: maptype.HWND) -> int:
        return mapBuildMtlUn_t (_hMap, _mtrname.buffer(), _ininame.buffer(), _mtrparm, _hselect, _handle)


# Построение матрицы на заданный участок района работ (устаревшая)
# При ошибке возвращает ноль
# hMap    - идентификатор исходной карты для построения матрицы,
# mtrname - полное имя файла создаваемой матрицы,
# ininame - полное имя файла легенды создаваемой матрицы,
# mtrparm - параметры создаваемой матрицы,
# Структурa MTLBUILDPARM описанa в mtlapi.h
# hselect - идентификатор контекста отбора объектов карты,
# handle  - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#  0x0378 - сообщение о проценте выполненных работ (в WPARAM),
#  если процесс должен быть принудительно завершен, в ответ
#  должно вернуться значение 0x0378.
# Если handle равно нулю - сообщения не посылаются.

    mapBuildMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtl', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(MTLBUILDPARM), maptype.HSELECT, maptype.HWND)
    def mapBuildMtl(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _ininame: ctypes.c_char_p, _mtrparm: ctypes.POINTER(MTLBUILDPARM), _hselect: maptype.HSELECT, _handle: maptype.HWND) -> int:
        return mapBuildMtl_t (_hMap, _mtrname, _ininame, _mtrparm, _hselect, _handle)


# Запросить описание файла матричных данных
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# describe - адрес структуры, в которой будет размещено
# описание матрицы
# Структурa MTLDESCRIBE описанa в mtlapi.h
# При ошибке возвращает ноль

    mapGetMtlDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlDescribe', maptype.HMAP, ctypes.c_int, ctypes.POINTER(MTLDESCRIBE))
    def mapGetMtlDescribe(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(MTLDESCRIBE)) -> int:
        return mapGetMtlDescribe_t (_hMap, _number, _describe)

    mapGetMtlDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlDescribeUn', maptype.HMAP, ctypes.c_int, ctypes.POINTER(MTLDESCRIBEUN))
    def mapGetMtlDescribeUn(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(MTLDESCRIBEUN)) -> int:
        return mapGetMtlDescribeUn_t (_hMap, _number, _describe)


# Запросить имя файла матричных данных
# hMap - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# name - адрес строки для размещения результата
# size - размер строки
# При ошибке возвращает ноль

    mapGetMtlNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtlNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMtlNameUn_t (_hMap, _number, _name.buffer(), _size)


# Запросить число открытых файлов матричных данных
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ноль

    mapGetMtlCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlCount', maptype.HMAP)
    def mapGetMtlCount(_hMap: maptype.HMAP) -> int:
        return mapGetMtlCount_t (_hMap)


# Запросить номер матрицы в цепочке по имени файла
# name - имя файла матрицы
# В цепочке номера растров начинаются с 1.
# При ошибке возвращает ноль

    mapGetMtlNumberByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlNumberByName', maptype.HMAP, ctypes.c_char_p)
    def mapGetMtlNumberByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapGetMtlNumberByName_t (_hMap, _name)

    mapGetMtlNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtlNumberByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetMtlNumberByNameUn_t (_hMap, _name.buffer())


# Запросить максимальное количество слоев всех матриц MTL-цепочки
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ноль

    mapGetMaxLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMaxLayerCount', maptype.HMAP)
    def mapGetMaxLayerCount(_hMap: maptype.HMAP) -> int:
        return mapGetMaxLayerCount_t (_hMap)


# Запросить количество слоев матрицы с номером number в цепочке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetLayerCountOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayerCountOfMtl', maptype.HMAP, ctypes.c_int)
    def mapGetLayerCountOfMtl(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetLayerCountOfMtl_t (_hMap, _number)


# Запросить минимальную высоту нижнего уровня
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ERRORHEIGHT

    mapGetMinBotLevelHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMinBotLevelHeight', maptype.HMAP)
    def mapGetMinBotLevelHeight(_hMap: maptype.HMAP) -> float:
        return mapGetMinBotLevelHeight_t (_hMap)


# Запросить максимальную суммарную мощность слоев
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ERRORPOWER

    mapGetMaxSummaryPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMaxSummaryPower', maptype.HMAP)
    def mapGetMaxSummaryPower(_hMap: maptype.HMAP) -> float:
        return mapGetMaxSummaryPower_t (_hMap)


# Выбор значения абсолютной высоты в заданной точке.
# hMap - идентификатор открытой основной карты
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT.

    mapGetElementHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetElementHeight(_hMap: maptype.HMAP, _x: float, _y: float) -> float:
        return mapGetElementHeight_t (_hMap, _x, _y)


# Выбор значения абсолютной высоты в заданной точке из матрицы
# с номером number в цепочке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT.

    mapGetElementHeightOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementHeightOfMtl', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapGetElementHeightOfMtl(_hMap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        return mapGetElementHeightOfMtl_t (_hMap, _number, _x, _y)


# Выбор значения мощности слоя в заданной точке.
# hMap - идентификатор открытой основной карты
# layernumber - номер слоя
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение мощности слоя в метрах.
# В случае ошибки и в случае необеспеченности заданной
# точки матричными данными возвращает ERRORPOWER.

    mapGetElementPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPower', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetElementPower(_hMap: maptype.HMAP, _x: float, _y: float, _layernumber: int) -> float:
        return mapGetElementPower_t (_hMap, _x, _y, _layernumber)


# Выбор значения мощности слоя в заданной точке из матрицы
# с номером number в цепочке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# layernumber - номер слоя
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение мощности слоя в метрах.
# В случае ошибки и в случае необеспеченности заданной
# точки матричными данными возвращает ERRORPOWER.

    mapGetElementPowerOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPowerOfMtl', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetElementPowerOfMtl(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _layernumber: int) -> float:
        return mapGetElementPowerOfMtl_t (_hMap, _number, _x, _y, _layernumber)


# Вычисление значений мощностей слоев в заданной точке
# методом треугольников по матрице с номером number в цепочке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Координаты точки задаются в метрах в системе координат
# векторной карты
# powers - адрес массива для записи вычисленных значений
#          мощностей (в метрах)
# count - размер массива, должен быть не менее mapGetLayerCountOfMtl()
# Возвращает количество заполненных элементов массива powers
# При ошибке возвращает ноль.

    mapGetElementPowersTriangleOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetElementPowersTriangleOfMtl', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int)
    def mapGetElementPowersTriangleOfMtl(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _powers: ctypes.POINTER(ctypes.c_double), _count: int) -> int:
        return mapGetElementPowersTriangleOfMtl_t (_hMap, _number, _x, _y, _powers, _count)


# Вычисление значения мощности слоя layernumber в заданной точке
# методом треугольников по матрице с номером number в цепочке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Координаты точки задаются в метрах в системе координат
# векторной карты
# layernumber - номер слоя
# Возвращает значение мощности слоя в метрах.
# При ошибке возвращает ERRORPOWER.

    mapGetElementPowerTriangleOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPowerTriangleOfMtl', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapGetElementPowerTriangleOfMtl(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _layernumber: int) -> float:
        return mapGetElementPowerTriangleOfMtl_t (_hMap, _number, _x, _y, _layernumber)


# Занесение значения абсолютной высоты в элемент матрицы,
# соответствующий заданной точке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Координаты точки (x,y) и значение высоты (h) задаются в метрах
# в системе координат векторной карты.
# В случае ошибки возвращает ноль.

    mapPutElementHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutElementHeight', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutElementHeight(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        return mapPutElementHeight_t (_hMap, _number, _x, _y, _h)


# Занесение значения мощности слоя layernumber в элемент,
# соответствующий заданной точке.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Координаты точки (x,y) и значение мощности (power) задаются
# в метрах в системе координат векторной карты
# layernumber - номер слоя
# В случае ошибки возвращает ноль.

    mapPutElementPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutElementPower', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapPutElementPower(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _power: float, _layernumber: int) -> int:
        return mapPutElementPower_t (_hMap, _number, _x, _y, _power, _layernumber)


# Запросить номер в цепочке для матрицы, расположенной
# в заданной точке
# hMap - идентификатор открытой основной карты
# number - порядковый номер, найденной матрицы в точке
# (1 - первая в данной точке, 2 - вторая ...)
# В случае ошибки возвращает ноль.

    mapGetMtlNumberInPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlNumberInPoint', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapGetMtlNumberInPoint(_hMap: maptype.HMAP, _x: float, _y: float, _number: int) -> int:
        return mapGetMtlNumberInPoint_t (_hMap, _x, _y, _number)


# Запросить номер в цепочке последней открытой матрицы
# с установленным (равным 1) признаком видимости.
# hMap - идентификатор открытой основной карты
# В случае ошибки возвращает ноль.

    mapGetMtlNumberLastVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlNumberLastVisible', maptype.HMAP)
    def mapGetMtlNumberLastVisible(_hMap: maptype.HMAP) -> int:
        return mapGetMtlNumberLastVisible_t (_hMap)


# Запросить размер полного блока матрицы в байтах
# hMap - идентификатор открытой основной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlBlockSize', maptype.HMAP, ctypes.c_int)
    def mapGetMtlBlockSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlBlockSize_t (_hMap, _number)


# Запросить вертикальный размер блока матрицы в элементах
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlBlockSide', maptype.HMAP, ctypes.c_int)
    def mapGetMtlBlockSide(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlBlockSide_t (_hMap, _number)


# Запросить число строк блоков матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlBlockRow', maptype.HMAP, ctypes.c_int)
    def mapGetMtlBlockRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlBlockRow_t (_hMap, _number)


# Запросить число столбцов блоков матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlBlockColumn', maptype.HMAP, ctypes.c_int)
    def mapGetMtlBlockColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlBlockColumn_t (_hMap, _number)


# Запросить число строк элементов в матрице
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlElementRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlElementRow', maptype.HMAP, ctypes.c_int)
    def mapGetMtlElementRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlElementRow_t (_hMap, _number)


# Запросить число столбцов элементов в матрице
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlElementColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlElementColumn', maptype.HMAP, ctypes.c_int)
    def mapGetMtlElementColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlElementColumn_t (_hMap, _number)


# Выбор массива значений абсолютных высот, соответствующих
# логическим элементам, лежащим на заданном отрезке.
# hMap - идентификатор открытой основной карты
# Координаты точек, задающих начало и конец отрезка
# (FirstPoint,SecondPoint) задаются в метрах в системе
# координат векторной карты.
# Размер массива высот, заданного адресом HeightArray,
# должен соответствовать запрашиваемому количеству высот
# (HeightCount), в противном случае возможны ошибки работы
# с памятью.
# В случае необеспеченности логического элемента матричными
# данными его значение равно ERRORHEIGHT (-111111.0 м)
# В случае ошибки при выборе высот возвращает ноль.

    mapGetHeightArrayFromMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightArrayFromMtl', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetHeightArrayFromMtl(_hMap: maptype.HMAP, _HeightArray: ctypes.POINTER(ctypes.c_double), _HeightCount: int, _FirstPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _SecondPoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetHeightArrayFromMtl_t (_hMap, _HeightArray, _HeightCount, _FirstPoint, _SecondPoint)


# Выбор значения цвета слоя layernumber
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# layernumber - номер слоя
# В случае ошибки возвращает ноль.

    mapGetLayerColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetLayerColor', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetLayerColor(_hMap: maptype.HMAP, _number: int, _layernumber: int) -> maptype.COLORREF:
        return mapGetLayerColor_t (_hMap, _number, _layernumber)


# Выбор максимальной мощности слоя layernumber в метрах.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# layernumber - номер слоя
# В случае ошибки возвращает ноль.

    mapGetMaxLayerHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMaxLayerHeight', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMaxLayerHeight(_hMap: maptype.HMAP, _number: int, _layernumber: int) -> int:
        return mapGetMaxLayerHeight_t (_hMap, _number, _layernumber)


# Установка максимальной мощности слоя layernumber в метрах.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# layernumber - номер слоя
# В случае ошибки возвращает ноль.

    mapSetMaxLayerHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMaxLayerHeight', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMaxLayerHeight(_hMap: maptype.HMAP, _number: int, _layernumber: int, _maxlayerheight: int) -> int:
        return mapSetMaxLayerHeight_t (_hMap, _number, _layernumber, _maxlayerheight)


# Установка значения цвета слоя layernumber.
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# layernumber - номер слоя
# В случае ошибки возвращает ноль.

    mapSetLayerColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetLayerColor', maptype.HMAP, ctypes.c_int, ctypes.c_int, maptype.COLORREF)
    def mapSetLayerColor(_hMap: maptype.HMAP, _number: int, _layernumber: int, _layercolor: maptype.COLORREF) -> int:
        return mapSetLayerColor_t (_hMap, _number, _layernumber, _layercolor)


# Запросить данные о проекции матричных данных
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# projectiondata - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MTRPROJECTIONDATA описанa в maptype.h
# При ошибке возвращает ноль

    mapGetMtlProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapGetMtlProjectionData(_hMap: maptype.HMAP, _number: int, _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapGetMtlProjectionData_t (_hMap, _number, _projectiondata)


# Создать матричную карту
# mtrname - полное имя файла матрицы
# mtrparm - параметры создаваемой матрицы
# Структурa BUILDMTL описанa в mtlapi.h
# Возвращает идентификатор открытой матричной карты (TMapAccess#)
# При ошибке возвращает ноль

    mapCreateMtlEx_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtlEx', ctypes.c_char_p, ctypes.POINTER(BUILDMTL))
    def mapCreateMtlEx(_mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(BUILDMTL)) -> maptype.HMAP:
        return mapCreateMtlEx_t (_mtrname, _mtrparm)

    mapCreateMtlUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtlUn', maptype.PWCHAR, ctypes.POINTER(BUILDMTL))
    def mapCreateMtlUn(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL)) -> maptype.HMAP:
        return mapCreateMtlUn_t (_mtrname.buffer(), _mtrparm)


# Создать файл матрицы
# hMap - идентификатор открытой основной карты
# mtrname - полное имя файла матрицы
# mtrparm - параметры создаваемой матрицы
# mtrprojectiondata - параметры проекции создаваемой матрицы
# Структурa BUILDMTL описанa в mtlapi.h
# Структурa MTRPROJECTIONDATA описанa в maptype.h
# Возвращает номер файла в цепочке матриц
# При ошибке возвращает ноль

    mapCreateAndAppendMtlEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendMtlEx', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(BUILDMTL), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateAndAppendMtlEx(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(BUILDMTL), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapCreateAndAppendMtlEx_t (_hMap, _mtrname, _mtrparm, _mtrprojectiondata)

    mapCreateAndAppendMtlUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendMtlUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(BUILDMTL), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateAndAppendMtlUn(_hMap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapCreateAndAppendMtlUn_t (_hMap, _mtrname.buffer(), _mtrparm, _mtrprojectiondata)


# Создать матричную карту (устаревшая)
# mtrname - полное имя файла матрицы
# mtrparm - параметры создаваемой матрицы
# Возвращает идентификатор открытой матричной карты (TMapAccess#)
# Структурa MTLBUILDPARM описанa в mtlapi.h
# При ошибке возвращает ноль

    mapCreateMtl_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtl', ctypes.c_char_p, ctypes.POINTER(MTLBUILDPARM))
    def mapCreateMtl(_mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(MTLBUILDPARM)) -> maptype.HMAP:
        return mapCreateMtl_t (_mtrname, _mtrparm)


# Создать файл матрицы (устаревшая)
# hMap - идентификатор открытой основной карты
# mtrname - полное имя файла матрицы
# mtrparm - параметры создаваемой матрицы
# mtrprojectiondata - параметры проекции создаваемой матрицы
# Структурa MTLBUILDPARM описанa в mtlapi.h
# Структурa MTRPROJECTIONDATA описанa в maptype.h
# Возвращает  номер файла в цепочке матриц
# При ошибке возвращает ноль

    mapCreateAndAppendMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateAndAppendMtl', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(MTLBUILDPARM), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateAndAppendMtl(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(MTLBUILDPARM), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapCreateAndAppendMtl_t (_hMap, _mtrname, _mtrparm, _mtrprojectiondata)


# Записать изменения матрицы в файл
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapSaveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMtl', maptype.HMAP, ctypes.c_int)
    def mapSaveMtl(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSaveMtl_t (_hMap, _number)


# Установить диапазон отображаемых элементов матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# minvalue - минимальное значение отображаемого элемента
#            в единицах матрицы
# maxvalue - максимальное значение отображаемого элемента
#            в единицах матрицы
# При ошибке возвращает 0

    mapSetMtlShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlShowRange', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapSetMtlShowRange(_hMap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        return mapSetMtlShowRange_t (_hMap, _number, _minvalue, _maxvalue)


# Установить нижний уровень слоев матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# botlevel - нижний уровень слоев в метрах
# При ошибке возвращает 0

    mapSetMtlBotLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlBotLevel', maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mapSetMtlBotLevel(_hMap: maptype.HMAP, _number: int, _botlevel: float) -> int:
        return mapSetMtlBotLevel_t (_hMap, _number, _botlevel)


# Установить максимальную суммарную мощность слоев матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# maxsummarypower - максимальная суммарная мощность в метрах
# При ошибке возвращает 0

    mapSetMtlMaxSummaryPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlMaxSummaryPower', maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mapSetMtlMaxSummaryPower(_hMap: maptype.HMAP, _number: int, _maxsummarypower: float) -> int:
        return mapSetMtlMaxSummaryPower_t (_hMap, _number, _maxsummarypower)


# Установить данные о проекции матричных данных
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# mapregister - адрес структуры, содержащей данные о проекции
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM описаны в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapSetMtlProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtlProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetMtlProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSetMtlProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapSetMtlProjectionData(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapSetMtlProjectionData_t (_hMap, _number, _mapregister)


# Запросить данные о проекции матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# mapregister - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MAPREGISTEREX описанa в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapGetMtlProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtlProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetMtlProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtlProjectionDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlProjectionDataEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtlProjectionDataEx(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetMtlProjectionDataEx_t (_hMap, _number, _mapregister)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hMap     - идентификатор открытой основной карты
# number   - номер файла в цепочке
# Если нет - возвращает ноль

    mapIsMtlGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMtlGeoSupported', maptype.HMAP, ctypes.c_int)
    def mapIsMtlGeoSupported(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsMtlGeoSupported_t (_hMap, _number)


# Запросить параметры эллипсоида матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла матрицы в цепочке
# ellipsoidparam - адрес структуры, в которой будут размещены
# параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtlEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtlEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetMtlEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Установить параметры эллипсоида матрицы
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла матрицы в цепочке.
# ellipsoidparam - адрес структуры, содержащей параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtlEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtlEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetMtlEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Запросить коэффициенты трансформирования геодезических координат матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла матрицы в цепочке
# datumparam - адрес структуры, в которой будут размещены
# коэффициенты трансформирования геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtlDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtlDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetMtlDatumParam_t (_hMap, _number, _datumparam)


# Установить коэффициенты трансформирования геодезических координат матрицы
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла матрицы в цепочке.
# datumparam - адрес структуры, содержащей коэффициенты трансформирования
# геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtlDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtlDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetMtlDatumParam_t (_hMap, _number, _datumparam)


# Установить рамку матрицы по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# number     - номер файла в цепочке
# info       - замкнутый объект карты
# После выполнения функции отображение матрицы ограничится заданной областью
# При ошибке возвращает ноль

    mapSetMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapSetMtlBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapSetMtlBorder_t (_hMap, _number, _info)


# Запросить объект рамки матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapGetMtlBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapGetMtlBorder_t (_hMap, _number, _info)


# Удалить рамку матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# После выполнения функции отображение матрицы будет полным
# При ошибке возвращает ноль

    mapDeleteMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtlBorder', maptype.HMAP, ctypes.c_int)
    def mapDeleteMtlBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteMtlBorder_t (_hMap, _number)


# Определение существования рамки матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Если рамка матрицы существует возвращает 1, иначе возвращает 0

    mapCheckExistenceMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckExistenceMtlBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckExistenceMtlBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckExistenceMtlBorder_t (_hMap, _number)


# Определение способа отображения матрицы(относительно рамки)
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# Возвращает 1 - при отображении матрицы по рамке
#            0 - при отображении матрицы без учета рамки
# При ошибке возвращает -1

    mapCheckShowMtlByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckShowMtlByBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckShowMtlByBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckShowMtlByBorder_t (_hMap, _number)


# Установка отображения матрицы по рамке
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# value = 1 - отобразить матрицы по рамке
#       = 0 - отобразить матрицы без учета рамки
#  При ошибке возвращает ноль

    mapShowMtlByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapShowMtlByBorder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapShowMtlByBorder(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapShowMtlByBorder_t (_hMap, _number, _value)


# Определить координаты и порядковый номер точки рамки, которая
# входит в прямоугольник Габариты растра(матрицы) и
# имеет наименьшее удаление от точки pointIn (координаты в метрах)
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# По адресу pointOut записываются координаты найденной точки в метрах
# При ошибке или отсутствии рамки возвращает ноль

    mapGetImmediatePointOfMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImmediatePointOfMtlBorder', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtlBorder(_hMap: maptype.HMAP, _number: int, _pointIn: ctypes.POINTER(maptype.DOUBLEPOINT), _pointOut: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetImmediatePointOfMtlBorder_t (_hMap, _number, _pointIn, _pointOut)


# Запросить координаты Юго-Западного угла матрицы в метрах
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла в цепочке
# По адресу x,y записываются координаты найденной точки в метрах
# При ошибке возвращает 0

    mapWhereSouthWestMtlPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhereSouthWestMtlPlane', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapWhereSouthWestMtlPlane(_hMap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapWhereSouthWestMtlPlane_t (_hMap, _number, _x, _y)


# Запросить фактические габариты отображаемой матрицы в метрах в районе работ
# При отображение матрицы по рамке возвращаются габариты рамки
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetActualMtlFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActualMtlFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetActualMtlFrame(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetActualMtlFrame_t (_hMap, _frame, _number)


# Запросить масштаб матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapGetMtlScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlScale', maptype.HMAP, ctypes.c_int)
    def mapGetMtlScale(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlScale_t (_hMap, _number)


# Запросить значения масштаба нижней и верхней границ видимости матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# По адресу bottomScale записывается знаменатель масштаба нижней границы видимости матрицы
# По адресу topScale записывается знаменатель масштаба верхней границы видимости матрицы
# При ошибке возвращает ноль

    mapGetMtlRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetMtlRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: ctypes.POINTER(ctypes.c_int), _topScale: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetMtlRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить значения масштаба нижней и верхней границ видимости матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# bottomScale - знаменатель масштаба нижней границы видимости матрицы
# topScale    - знаменатель масштаба верхней границы видимости матрицы
# при невыполнении условия bottomScale <= topScale возвращает ноль
# При ошибке возвращает ноль

    mapSetMtlRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMtlRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: int, _topScale: int) -> int:
        return mapSetMtlRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Запросить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# При ошибке возвращает ноль

    mapGetActiveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActiveMtl', maptype.HMAP)
    def mapGetActiveMtl(_hMap: maptype.HMAP) -> int:
        return mapGetActiveMtl_t (_hMap)


# Установить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapSetActiveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveMtl', maptype.HMAP, ctypes.c_int)
    def mapSetActiveMtl(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSetActiveMtl_t (_hMap, _number)


# Открыта ли матрица с номером "number"
# Функция возвращает признак открытия указанной матрицы в документе - (1/0).
# При ошибке возвращает ноль.

    mapIsOpenMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsOpenMtl', maptype.HMAP, ctypes.c_int)
    def mapIsOpenMtl(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsOpenMtl_t (_hMap, _number)


# Запросить флаг редактируемости матрицы
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlEdit', maptype.HMAP, ctypes.c_int)
    def mapGetMtlEdit(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlEdit_t (_hMap, _number)


# Запросить размер файла
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# По адресу fileSize записывается размер файла
# При ошибке возвращает ноль

    mapGetMtlFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlFileSize', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtlFileSize(_hMap: maptype.HMAP, _number: int, _fileSize: ctypes.POINTER(ctypes.c_int64)) -> int:
        return mapGetMtlFileSize_t (_hMap, _number, _fileSize)


# Запросить ширину матрицы (элементы)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlWidthInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtlWidthInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlWidthInElement_t (_hMap, _number)


# Запросить высоту матрицы (элементы)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlHeightInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtlHeightInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlHeightInElement_t (_hMap, _number)


# Запросить точность (метр/элем) матрицы
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtlAccuracy', maptype.HMAP, ctypes.c_int)
    def mapGetMtlAccuracy(_hMap: maptype.HMAP, _number: int) -> float:
        return mapGetMtlAccuracy_t (_hMap, _number)


# Запросить флаг изменения привязки (метры) матрицы             # 28/09/09
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtlFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlFlagLocationChanged', maptype.HMAP, ctypes.c_int)
    def mapGetMtlFlagLocationChanged(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlFlagLocationChanged_t (_hMap, _number)


# Запросить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapGetMtlLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtlLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetMtlLocation_t (_hMap, _number, _location)


# Установить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapSetMtlLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtlLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSetMtlLocation_t (_hMap, _number, _location)


# Запросить - может ли матрица копироваться или экспортироваться
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtlCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlCopyFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtlCopyFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlCopyFlag_t (_hMap, _number)


# Запросить - может ли матрица выводиться на печать
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения на печать
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtlPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlPrintFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtlPrintFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlPrintFlag_t (_hMap, _number)


# Запросить единицу измерения значений высот матрицы
# с номером number в цепочке.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращаемые значения :
#   0-метры, 1-дециметры, 2-сантиметры, 3-миллиметры
# При ошибке возвращает -1

    mapGetMtlMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlMeasure', maptype.HMAP, ctypes.c_int)
    def mapGetMtlMeasure(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlMeasure_t (_hMap, _number)


# Запросить единицу измерения мощности слоя матрицы
# с номером number в цепочке.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращаемые значения :
#   0-метры, 1-дециметры, 2-сантиметры, 3-миллиметры
# При ошибке возвращает -1

    mapGetMtlLayerMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlLayerMeasure', maptype.HMAP, ctypes.c_int)
    def mapGetMtlLayerMeasure(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlLayerMeasure_t (_hMap, _number)


# Запросить/Установить степень видимости матрицы
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# view = 0 - нет видимости
# view = 1 - полная
# view = 2 - насыщенная
# view = 3 - полупрозрачная
# view = 4 - средняя
# view = 5 - прозрачная

    mapGetMtlView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlView', maptype.HMAP, ctypes.c_int)
    def mapGetMtlView(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlView_t (_hMap, _number)

    mapSetMtlView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtlView(_hMap: maptype.HMAP, _number: int, _view: int) -> int:
        return mapSetMtlView_t (_hMap, _number, _view)


# Запросить/Установить порядок отображения матрицы        # 27/05/09
# hMap - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# order  - порядок отображения (0 - под картой, 1 - над картой)
# При ошибке возвращает 0

    mapSetMtlViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtlViewOrder(_hMap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetMtlViewOrder_t (_hMap, _number, _order)

    mapGetMtlViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlViewOrder', maptype.HMAP, ctypes.c_int)
    def mapGetMtlViewOrder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlViewOrder_t (_hMap, _number)


# Поменять очередность отображения матриц (mtl) в цепочке
# oldNumber - номер файла в цепочке
# newNumber - устанавливаемый номер файла в цепочке
# При ошибке возвращает ноль

    mapChangeOrderMtlShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeOrderMtlShow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangeOrderMtlShow(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangeOrderMtlShow_t (_hMap, _oldNumber, _newNumber)


# Запросить прозрачность палитры матрицы
# number - номер файла в цепочке
# Возвращает степень прозрачности в процентах от 0 до 100

    mapGetMtlTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtlTransparent', maptype.HMAP, ctypes.c_int)
    def mapGetMtlTransparent(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtlTransparent_t (_hMap, _number)


# Установить прозрачность палитры матрицы
# hMap   - идентификатор открытых данных
# number - номер файла в цепочке
# transparent - прозрачность в процентах от 0 до 100
# При ошибке возвращает ноль

    mapSetMtlTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtlTransparent', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtlTransparent(_hMap: maptype.HMAP, _number: int, _transparent: int) -> int:
        return mapSetMtlTransparent_t (_hMap, _number, _transparent)


# Создать объект отображения матрицы слоев в 3D
# hMap   - идентификатор открытых данных
# При ошибке возвращает ноль

    mapCreateMtl3D_t = mapsyst.GetProcAddress(acceslib,maptype.HMTL3D,'mapCreateMtl3D', maptype.HMAP)
    def mapCreateMtl3D(_hmap: maptype.HMAP) -> maptype.HMTL3D:
        return mapCreateMtl3D_t (_hmap)


# Удалить объект отображения матрицы слоев в 3D
# hmtl3d - идентификатор объекта отображения

    mapDeleteMtl3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteMtl3D', maptype.HMTL3D)
    def mapDeleteMtl3D(_hmtl3d: maptype.HMTL3D) -> ctypes.c_void_p:
        return mapDeleteMtl3D_t (_hmtl3d)


# Отобразить матрицу слоев в 3D
# hmtl3d - идентификатор объекта отображения
# При ошибке возвращает ноль

#   mapPaintMtl3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapPaintMtl3D', maptype.HMTL3D, maptype.HDC, ctypes.POINTER(MTL3DVIEWUN))
#   def mapPaintMtl3D(_hmtl3d: maptype.HMTL3D, _hdc: maptype.HDC, _parm: ctypes.POINTER(MTL3DVIEWUN)) -> int:
#       return mapPaintMtl3D_t (_hmtl3d, _hdc, _parm)

except Exception as e:
    print(e)
    acceslib = 0