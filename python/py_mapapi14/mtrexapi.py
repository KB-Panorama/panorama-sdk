#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class PRIORMTRPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("AbsHeightDifference",ctypes.c_double),
                ("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("Reserve",ctypes.c_double*4)]
#-----------------------------


#-----------------------------
class SPREADPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("hWnd",maptype.HMESSAGE),
                ("IterCount",ctypes.c_int),
                ("Palette",maptype.COLORREF*256),
                ("PaletteCount",ctypes.c_int),
                ("IsIterMtq",ctypes.c_int),
                ("IsAllEject",ctypes.c_int),
                ("EjectSize",ctypes.c_double),
                ("AbsorbHeight",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("WaveHeight",ctypes.c_double),
                ("Point",maptype.DOUBLEPOINT),
                ("Reserve",ctypes.c_char*64)]
#-----------------------------


#-----------------------------
class WZONEPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("Wnd",maptype.HMESSAGE),
                ("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("Frame",maptype.DFRAME),
                ("ElemSize",ctypes.c_double),
                ("dH",ctypes.c_double),
                ("Reserved",ctypes.c_char*64)]
#-----------------------------


#-----------------------------
class DEPTHMTQPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("MatrixType",ctypes.c_int),
                ("MatrixNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("Level",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("UserLabel",ctypes.c_int),
                ("Free1",ctypes.c_int),
                ("Handle",maptype.HWND),
                ("Border",maptype.HOBJ),
                ("Reserve",ctypes.c_char*128),
                ("UserName",ctypes.c_char*32)]
#-----------------------------


#-----------------------------
class CALCMATRIXPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("MatrixType",ctypes.c_int),
                ("MatrixNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("Level",ctypes.c_double),
                ("Handle",maptype.HWND),
                ("Border",maptype.HOBJ),
                ("CalcSquare",ctypes.c_char),
                ("CalcVolume",ctypes.c_char),
                ("CalcMinimun",ctypes.c_char),
                ("CalcMaximun",ctypes.c_char),
                ("CalcAverage",ctypes.c_char),
                ("CalcSquareWater",ctypes.c_char),
                ("CalcVolumeLayer",ctypes.c_char),
                ("CalcTypeReserve",ctypes.c_char),
                ("Square",ctypes.c_double),
                ("Volume",ctypes.c_double),
                ("Minimun",ctypes.c_double),
                ("Maximun",ctypes.c_double),
                ("Average",ctypes.c_double),
                ("SquareWater",ctypes.c_double),
                ("SquareShallowWater",ctypes.c_double),
                ("VolumeLayer",ctypes.c_double),
                ("LevelWater",ctypes.c_double),
                ("LayerTop",ctypes.c_double),
                ("LayerBottom",ctypes.c_double),
                ("Reserve",ctypes.c_char*80)]
#-----------------------------


#-----------------------------
class BUILDZONEFLOODPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free1",ctypes.c_int),
                ("Handle",maptype.HWND),
                ("Point1",maptype.DOUBLEPOINT),
                ("Point2",maptype.DOUBLEPOINT),
                ("Height1",ctypes.c_double),
                ("Height2",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("ElementSize",ctypes.c_double),
                ("Object",maptype.HOBJ),
                ("Active",ctypes.c_int),
                ("Free2",ctypes.c_int),
                ("Reserve",ctypes.c_char*64)]
#-----------------------------


#-----------------------------
class BUILDFLOWPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FlowObject",maptype.HOBJ),
                ("W",ctypes.c_double),
                ("Rt",ctypes.c_double),
                ("Uo",ctypes.c_double),
                ("FlowWidth",ctypes.c_double),
                ("SoilCategory",ctypes.c_int),
                ("FlagLess35",ctypes.c_int),
                ("MinPress",ctypes.c_double),
                ("MaxPress",ctypes.c_double),
                ("FlowType",ctypes.c_int),
                ("ErrorCode",ctypes.c_int),
                ("Reserve",ctypes.c_char*80)]
#-----------------------------


#-----------------------------
class MTRCLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Min",ctypes.c_double),
                ("Max",ctypes.c_double),
                ("Excode",ctypes.c_int),
                ("Color",ctypes.c_int),
                ("SemanticNumber",ctypes.c_int),
                ("SemanticMin",ctypes.c_int),
                ("SemanticMax",ctypes.c_int),
                ("SemanticColor",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BUILDDENSITY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("Palette",maptype.COLORREF*256),
                ("PaletteCount",ctypes.c_int),
                ("Reserved",ctypes.c_int*63)]
#-----------------------------


#-----------------------------
class BUILDVISIBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("Color",maptype.COLORREF),
                ("Reserved",ctypes.c_int*63)]
#-----------------------------


try:
    if os.environ['gismtrexdll']:
        gismtrexname = os.environ['gismtrexdll']
except KeyError:
    gismtrexname = 'gis64mtrex.dll'


try:
    mtrexlib = mapsyst.LoadLibrary(gismtrexname)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++  ФУНКЦИИ БИБЛИОТЕКИ MAPMTREX.DLL  +++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Вычисление значения абсолютной высоты (point->H) в заданной
# точке (point->X,point->Y) по данным векторной карты.
# Координаты точки задаются в метрах в системе координат
# векторной карты.
# В случае ошибки при вычислении высоты возвращает 0.

    mtrCalcAbsoluteHeight_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCalcAbsoluteHeight', maptype.HMAP, ctypes.POINTER(maptype.XYHDOUBLE))
    def mtrCalcAbsoluteHeight(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.XYHDOUBLE)) -> int:
        return mtrCalcAbsoluteHeight_t (_hMap, _point)


# Вычисление значения абсолютной высоты в заданной
# точке (point->X,point->Y) по данным векторной карты.
# Координаты точки задаются в метрах в системе координат
# векторной карты.
# sectorcount - количество направлений для поиска окружающих высот
#  (должно быть кратно 4, минимальное количество направлений = 4,
#   максимальное = 256).
# Возвращает значение высоты в метрах.
# В случае ошибки при вычислении высоты возвращает ERRORHEIGHT.

    mtrCalcAbsoluteHeightBySectors_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_double,'mtrCalcAbsoluteHeightBySectors', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mtrCalcAbsoluteHeightBySectors(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _sectorcount: int) -> float:
        return mtrCalcAbsoluteHeightBySectors_t (_hMap, _point, _sectorcount)


# Вычисление значения характеристики в заданной точке
# по данным векторной карты.
# Характеристика задается кодом семантики - semanticCode.
# Координаты точки (point->X,point->Y) задаются в метрах в
# системе координат векторной карты.
# Вычисленное значение характеристики заносится в value.
# flagSelect - флаг использования условий отбора объектов карты.
# Если flagSelect = 0, то выполняется поиск заданной характеристики
# по всем объектам векторной карты.
# Если flagSelect = 1, то поиск заданной характеристики выполняется
# только по объектам, удовлетворяющим условиям отбора (HSELECT),
# установленным для векторной карты.
# В случае ошибки возвращает 0

    mtrCalcCharacteristic_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCalcCharacteristic', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mtrCalcCharacteristic(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _semanticCode: int, _flagSelect: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCalcCharacteristic_t (_hMap, _point, _semanticCode, _flagSelect, _value)


# Предварительная оценка характеристик матрицы, создаваемой
# по векторной карте на заданный участок района работ.
# В процессе оценки выполняется преобразование исходных
# векторных данных района в растровый вид.
# При ошибке возвращает ноль.
# hMap    - исходная карта для построения матрицы,
# filtername - полное имя фильтра объектов
#   Вместе с картой может располагаться фильтр объектов -
#   текстовый файл MTRCREA.IMH, содержащий перечень кодов
#   объектов, используемых при построении матрицы (см. MAPAPI.DOC)
#   Если filtername равно нулю - фильтр объектов не используется.
# buildparm - параметры создаваемой матрицы,
# priorparm - результаты предварительной оценки,
# handle   - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
#   Если handle равно нулю - сообщения не посылаются.

    mtrTryBuild_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrTryBuild', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(PRIORMTRPARM), maptype.HMESSAGE)
    def mtrTryBuild(_hMap: maptype.HMAP, _filtername: ctypes.c_char_p, _buildparm: ctypes.POINTER(maptype.BUILDMTW), _priorparm: ctypes.POINTER(PRIORMTRPARM), _handle: maptype.HMESSAGE) -> int:
        return mtrTryBuild_t (_hMap, _filtername, _buildparm, _priorparm, _handle)

    mtrTryBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrTryBuildUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(PRIORMTRPARM), maptype.HMESSAGE)
    def mtrTryBuildUn(_hMap: maptype.HMAP, _filtername: mapsyst.WTEXT, _buildparm: ctypes.POINTER(maptype.BUILDMTW), _priorparm: ctypes.POINTER(PRIORMTRPARM), _handle: maptype.HMESSAGE) -> int:
        return mtrTryBuildUn_t (_hMap, _filtername.buffer(), _buildparm, _priorparm, _handle)


# Вычисление значения максимального уклона и направления(азимут) максимального
# уклона в заданной точке (point) по данным матрицы высот.
# Координаты точки задаются в метрах в системе координат векторной карты.
# Возвращает:
#  incline - уклон в радианах
#  azimuth  - азимут радианах
# В случае ошибки при вычислении возвращает 0.

    mtrCalcInclineInPoint_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCalcInclineInPoint', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCalcInclineInPoint(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _incline: ctypes.POINTER(ctypes.c_double), _azimuth: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCalcInclineInPoint_t (_hMap, _point, _incline, _azimuth)


# Построение растра качеств по векторной карте на заданный
# участок района работ
# При ошибке возвращает ноль
# hMap    - исходная карта для построения растра,
# rstname - полное имя создаваемого растра,
# filtername - полное имя служебного текстового файла
#   Вместе с картой должен располагаться фильтр объектов -
#   служебный текстовый файл map2rsw.ini, содержащий перечень кодов
#   объектов, используемых при построении растра
# mtrparm - параметры создаваемого растра,
# handle   - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
# Если handle равно нулю - сообщения не посылаются.

    mtrBuildRasterUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildRasterUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HMESSAGE)
    def mtrBuildRasterUn(_hMap: maptype.HMAP, _rstname: mapsyst.WTEXT, _filtername: mapsyst.WTEXT, _rstparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HMESSAGE) -> int:
        return mtrBuildRasterUn_t (_hMap, _rstname.buffer(), _filtername.buffer(), _rstparm, _handle)

    mtrBuildRaster_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildRaster', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), maptype.HMESSAGE)
    def mtrBuildRaster(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _filtername: ctypes.c_char_p, _rstparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HMESSAGE) -> int:
        return mtrBuildRaster_t (_hMap, _rstname, _filtername, _rstparm, _handle)


# Построение зоны затопления по набору отметок уровня воды.
# В результате построения формируется матрица качеств, элементы
# которой содержат глубины в зоне затопления.
# Габариты матрицы качеств определяются координатами точек с
# отметками уровня воды (массив pointArray) и величиной расширения
# габаритов области (areaExtension).
# hMap    - исходная карта для построения зоны,
# mtqName - полное имя создаваемой матрицы качеств,
# pointArray - адрес массива точек с отметками уровня воды
#   Координаты точек (pointArray->X,pointArray->Y) и значения уровня
#   (pointArray->H) задаются в метрах в системе координат векторной
#   карты,
# pointCount - число точек в массиве pointArray
#   Размер в байтах массива, заданного адресом pointArray, должен
#   быть не менее pointCount # sizeof(XYHDOUBLE), в противном случае
#   возможны ошибки работы с памятью,
# areaExtension - положительное число, задающее величину
#   расширения габаритов области в метрах,
# minDepth - положительное число, задающее минимальную глубину
#   зоны затопления в метрах (глубины, меньшие minDepth в матрицу
#   качеств не заносятся),
# isFloodZoneAbs - признак того, что во входных данных заданы абсолютные
#   высоты (!=0), если 0, то высоты относительные (функции #ZoneAbs#
#   используют абсолютные высоты на входе);
# handle - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
# fcallback  - функция обратного вызова для сообщения статуса выполнения (процентов),
#   это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#   в нее будет возвращено значение eventparam, вторым - код сообщения (0x0581),
#   в третьем параметре  - процент выполненной обработки
#   в чевертом параметре - адрес строки с названием выполняемого этапа
#   Если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
# eventparam - параметр, передаваемый в функцию обратного вызова для идентификации
#   отклика на вызывающей стороне.
# При отправке сообщения WM_ERROR в первом параметре содержится целочисленный код ошибки,
# во втором параметре передается указатель на текст описания ошибки.
# Если handle (или fcallback) равно нулю - сообщения не посылаются.
# Текст передается в кодировке Unicode (UTF16).

    mtrBuildFloodZone_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildFloodZone', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HMESSAGE)
    def mtrBuildFloodZone(_hMap: maptype.HMAP, _mtqName: ctypes.c_char_p, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HMESSAGE) -> int:
        return mtrBuildFloodZone_t (_hMap, _mtqName, _pointArray, _pointCount, _areaExtension, _minDepth, _handle)

    mtrBuildFloodZoneCallback_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildFloodZoneCallback', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrBuildFloodZoneCallback(_hMap: maptype.HMAP, _isFloodZoneAbs: int, _mtqName: mapsyst.WTEXT, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mtrBuildFloodZoneCallback_t (_hMap, _isFloodZoneAbs, _mtqName.buffer(), _pointArray, _pointCount, _areaExtension, _minDepth, _fcallback, _eventparam)

    mtrBuildFloodZoneUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildFloodZoneUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HMESSAGE)
    def mtrBuildFloodZoneUn(_hMap: maptype.HMAP, _mtqName: mapsyst.WTEXT, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HMESSAGE) -> int:
        return mtrBuildFloodZoneUn_t (_hMap, _mtqName.buffer(), _pointArray, _pointCount, _areaExtension, _minDepth, _handle)

    mtrBuildFloodZoneAbsUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildFloodZoneAbsUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HMESSAGE)
    def mtrBuildFloodZoneAbsUn(_hMap: maptype.HMAP, _mtqName: mapsyst.WTEXT, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HMESSAGE) -> int:
        return mtrBuildFloodZoneAbsUn_t (_hMap, _mtqName.buffer(), _pointArray, _pointCount, _areaExtension, _minDepth, _handle)


# Построение зоны затопления по объекту методом створов.
# hMap - исходная карта, обеспеченная данными о рельефе,
# parm - параметры построения зоны затопления.
# mtqname - полное имя создаваемой матрицы качеств
# sitename - имя пользовательской карты для записи объектов - зон затопления
# В результате построения формируется матрица качеств, элементы
# которой содержат глубины в зоне затопления.
# В памяти создается пользовательская карта sitename с классификатором service.rsc.
# Классификатор service.rsc должен находиться в одном каталоге с приложением или с hMap.
# Если задано sitename и  Active > 0 (параметр Active из BUILDZONEFLOODPARM - флаг
# создания объектов), пользовательская карта будет записана на диск
# hPaint - идентификатор контекста отображения для многопоточного вызова функций,
#          создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# fcallback - функция обратного вызова для сообщения статуса выполнения (процентов),
#             это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#             в нее будет возвращено значение eventparam, вторым - тип сообщения
#             (WM_PROGRESSBARUN или WM_ERROR - см. описание в maptype.h),
#             третий и четвертый параметры - в зависимости от типа сообщения.
# Только для ОС Windows: В случаях, когда функция обратного вызова не задается
# значение параметра parm.Handle задает идентификатор окна (HWND), которому, если
# он указан (!=0), будет оправлятся сообщение WM_PROGRESSBARUN (см. maptype.h).
# Отправка уведомлений WM_PROGRESSBARUN, WM_ERROR и пр. с помощью функции обратного
# вызова и с помощью SendMessage (в ОС Windows) полностью аналогичны. При этом
# параметры WPARAM и LPARAM сообщения Windows являются соответственно аналогами
# параметров value2 и value3 функции обратного вызова.
# При отправке WM_PROGRESSBARUN со значением первого параметра -1, во втором параметре
# передается указатель на текст названия выполняемой задачи.
# Для остановки процесса выполенения в обработчике сообщения WM_PROGRESSBARUN следует
# установить результат (возвращаемое значение) равным значению WM_PROGRESSBARUN.
# При отправке WM_ERROR в первом параметре содержится целочисленный код ошибки,
# во втором параметре передается указатель на текст описания ошибки.
# Текст передается в кодировке Unicode (UTF16).
# В случае ошибки возвращает 0.

    mtrFloodZoneByObjectCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrFloodZoneByObjectCallBack', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDZONEFLOODPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrFloodZoneByObjectCallBack(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _sitename: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDZONEFLOODPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hPaint: maptype.HPAINT = 0) -> int:
        return mtrFloodZoneByObjectCallBack_t (_hMap, _mtqname.buffer(), _sitename.buffer(), _parm, _fcallback, _eventparam, _hPaint)

    mtrFloodZoneByObject_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrFloodZoneByObject', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(BUILDZONEFLOODPARM))
    def mtrFloodZoneByObject(_hMap: maptype.HMAP, _mtqname: ctypes.c_char_p, _sitename: ctypes.c_char_p, _parm: ctypes.POINTER(BUILDZONEFLOODPARM)) -> int:
        return mtrFloodZoneByObject_t (_hMap, _mtqname, _sitename, _parm)

    mtrFloodZoneByObjectUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrFloodZoneByObjectUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDZONEFLOODPARM))
    def mtrFloodZoneByObjectUn(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _sitename: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDZONEFLOODPARM)) -> int:
        return mtrFloodZoneByObjectUn_t (_hMap, _mtqname.buffer(), _sitename.buffer(), _parm)

    mtrFloodZoneByObjectEx_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrFloodZoneByObjectEx', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDZONEFLOODPARM), maptype.HPAINT)
    def mtrFloodZoneByObjectEx(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _sitename: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDZONEFLOODPARM), _hPaint: maptype.HPAINT) -> int:
        return mtrFloodZoneByObjectEx_t (_hMap, _mtqname.buffer(), _sitename.buffer(), _parm, _hPaint)


# Построениe матрицы давлений селевого потока
#   hMap - исходная карта, обеспеченная данными о рельефе
#   mtqname - имя матрицы давлений
#   parm - параметры построения матрицы давлений
#   fcallback - функция обратного вызова для сообщения процентов выполнения
#   eventparam - параметры функции обратного вызова
#   hpaint - контекст отображения для многопоточного вызова
# В случае ошибки возвращает 0 и заносит код ошибки в parm->ErrorCode
# Значения кода ошибки приведены в описании структуры BUILDFLOWPARM

    mtrBuildFlowMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildFlowMtq', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(BUILDFLOWPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrBuildFlowMtq(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDFLOWPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hpaint: maptype.HPAINT) -> int:
        return mtrBuildFlowMtq_t (_hMap, _mtqname.buffer(), _parm, _fcallback, _eventparam, _hpaint)


# Построениe линейного объекта русла потока
#   hMap - исходная карта, обеспеченная данными о рельефе
#   flowTrace - объект-контейнер для занесения метрики русла,
#     созданный функцией mapCreateObject
#     (для сохранения объекта русла вызвать mapCommitObjectAsNew)
#   p1 - точка начала русла, p2 - точка конца русла
#   Высота рельефа в точке p1 должна быть больше высоты в точке p2
#   fcallback - функция обратного вызова для сообщения процентов выполнения
#   eventparam - параметры функции обратного вызова
#   hpaint - контекст отображения для многопоточного вызова
# В случае ошибки возвращает 0 и заносит код ошибки в errorCode
# Значения кода ошибки:
#   1 - Ошибка входных параметров
#   2 - Заданные точки начала и конца русла не обеспечены высотами рельефа
#   3 - Расстояние между заданными точками начала и конца русла меньше элемента матрицы высот
#   4 - Высота в точке начала русла меньше высоты в точке конца русла
#   5 - Расстояние между точками начала и конца русла недостаточно для профилирования матрицы высот

    mtrMakeFlowTrace_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrMakeFlowTrace', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_int), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrMakeFlowTrace(_hMap: maptype.HMAP, _flowTrace: maptype.HOBJ, _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _errorCode: ctypes.POINTER(ctypes.c_int), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hpaint: maptype.HPAINT) -> int:
        return mtrMakeFlowTrace_t (_hMap, _flowTrace, _p1, _p2, _errorCode, _fcallback, _eventparam, _hpaint)


# Построение матрицы качеств по массиву значений характеристики качества.
# hMap - исходная карта для построения матрицы качеств,
# mtqName - полное имя создаваемой матрицы качеств,
# palette - адрес палитры создаваемой матрицы качеств,
# countpalette - количество цветов в палитре,
# pointArray - адрес массива значений характеристики качества
#   Координаты точек (pointArray->X,pointArray->Y) задаются в метрах
#   в системе координат векторной карты,
# pointCount - число точек в массиве pointArray
#   Размер в байтах массива, заданного адресом pointArray, должен
#   быть не менее pointCount # sizeof(XYHDOUBLE), в противном случае
#   возможны ошибки работы с памятью,
# elemSizeMeters - размер стороны элементарного участка в метрах на местности
#                  (дискрет матрицы)
# minValue,maxValue - диапазон значений характеристики качества создаваемой матрицы
#                     качеств, если minValue >= maxValue - в матрицу заносится
#                     фактический диапазон значений из массива pointArray
# handle - идентификатор окна диалога, которому посылаются
#   сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
#   Если handle равно нулю - сообщения не посылаются.

    mtrBuildMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildMtq', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, maptype.HMESSAGE)
    def mtrBuildMtq(_hMap: maptype.HMAP, _mtqName: ctypes.c_char_p, _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _elemSizeMeters: float, _minValue: float, _maxValue: float, _handle: maptype.HMESSAGE) -> int:
        return mtrBuildMtq_t (_hMap, _mtqName, _palette, _countpalette, _pointArray, _pointCount, _elemSizeMeters, _minValue, _maxValue, _handle)


# Построение матрицы поверхности (матрицы качеств или матрицы высот)
# по данным векторной карты. Если mtrparm->FileMtw равно 1, то строится
# матрица высот (#.mtw), иначе строится матрица качеств (#.mtq).
# hmap - исходная карта для построения матрицы
# mtrname - полное имя создаваемой матрицы
# mtrparm - параметры создаваемой матрицы (структура BUILDSURFACE описана в maptype.h)
# При ошибке возвращает 0.

    mtrBuildMatrixSurface_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildMatrixSurface', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDSURFACE))
    def mtrBuildMatrixSurface(_hmap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        return mtrBuildMatrixSurface_t (_hmap, _mtrname, _mtrparm)

    mtrBuildMatrixSurfaceUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildMatrixSurfaceUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE))
    def mtrBuildMatrixSurfaceUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        return mtrBuildMatrixSurfaceUn_t (_hmap, _mtrname.buffer(), _mtrparm)


# Занесение в матрицу качеств зоны вдоль линейного объекта
# hMap - идентификатор открытой матричной карты
# number - номер матрицы качеств в цепочке
# infoLine - линейный объект
# width - ширина зоны в метрах
# value - значение, заносимое в элементы зоны
# regime - режим занесения значения (0 - без учёта ранее занесённого значения)
# В случае ошибки возвращает 0

    mtrPutMtqLineZone_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrPutMtqLineZone', maptype.HMAP, ctypes.c_int, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mtrPutMtqLineZone(_hMap: maptype.HMAP, _number: int, _infoLine: maptype.HOBJ, _width: float, _value: float, _regime: int) -> int:
        return mtrPutMtqLineZone_t (_hMap, _number, _infoLine, _width, _value, _regime)


# Занесение в матрицу качеств зоны вдоль линейного объекта
# в границах площадного объекта
# hMap - идентификатор открытой матричной карты
# number - номер матрицы качеств в цепочке
# infoLine - линейный объект
# infoPolygon - площадной объект
# width - ширина зоны в метрах
# valueZone - значение, заносимое в элементы зоны
# valuePolygon - значение, заносимое в элементы площадного объекта
# regime - режим занесения значения (0 - без учёта ранее занесённого значения)
# В случае ошибки возвращает 0

    mtrPutMtqLineZoneForPolygon_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrPutMtqLineZoneForPolygon', maptype.HMAP, ctypes.c_int, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mtrPutMtqLineZoneForPolygon(_hMap: maptype.HMAP, _number: int, _infoLine: maptype.HOBJ, _infoPolygon: maptype.HOBJ, _width: float, _valueZone: float, _valuePolygon: float, _regime: int) -> int:
        return mtrPutMtqLineZoneForPolygon_t (_hMap, _number, _infoLine, _infoPolygon, _width, _valueZone, _valuePolygon, _regime)


# Создание матрицы качеств растекания жидкости
# Заполненные элементы матрицы содержат толщину слоя
# растекшейся жидкости
# hmap      - идентификатор открытых данных (должна быть открыта хотя бы одна матрица высот)
# mtqname   - имя создаваемой матрицы качеств растекания, если матрицы создаются на каждой итерации,
#             то в конце имени добавляется номер итерации (для первой = MtqName_1.mtq)
# parm      - параметры вызова
# hPaint    - идентификатор контекста отображения для многопоточного вызова функций,
#             создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# fcallback - функция обратного вызова для сообщения статуса выполнения (процентов),
#             это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#             в нее будет возвращено значение eventparam, вторым - код сообщения 0x0581
#             третий - процент выполнения;
# append    - признак необходимости добавить созданную матрицу к карте.
# Только для ОС Windows: В случаях, когда функция обратного вызова не задается
# значение параметра parm.Handle задает идентификатор окна (HWND), которому, если
# он указан (!=0), будет оправлятся сообщение 0x0581 со значением прокента выполнения в WParam.
# При успешном выполнении возвращает номер файла в цепочке матриц (или 1, если append = 0).
# При ошибке возвращает ноль

    mtrLiquidSpreading_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrLiquidSpreading', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(SPREADPARM))
    def mtrLiquidSpreading(_hMap: maptype.HMAP, _mtqname: ctypes.c_char_p, _parm: ctypes.POINTER(SPREADPARM)) -> int:
        return mtrLiquidSpreading_t (_hMap, _mtqname, _parm)

    mtrLiquidSpreadingUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrLiquidSpreadingUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(SPREADPARM))
    def mtrLiquidSpreadingUn(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(SPREADPARM)) -> int:
        return mtrLiquidSpreadingUn_t (_hMap, _mtqname.buffer(), _parm)

    mtrLiquidSpreadingCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrLiquidSpreadingCallBack', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(SPREADPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, maptype.HPAINT)
    def mtrLiquidSpreadingCallBack(_hMap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(SPREADPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _append: int, _hPaint: maptype.HPAINT = None) -> int:
        return mtrLiquidSpreadingCallBack_t (_hMap, _mtqname.buffer(), _parm, _fcallback, _eventparam, _append, _hPaint)


# Вычисление площади зоны по матрице качеств
# hMap - идентификатор открытой матричной карты
# number - номер матрицы качеств в цепочке
# minValue,maxValue - задают диапазон значений элементов,
# участвующих в вычислении площади
# если minValue > maxValue, то площадь вычисляется по всем
# заполненым элементам матрицы
# Вычисленное значение площади заносится в zoneSquare.
# В случае ошибки возвращает 0

    mtrCalcMtqZoneSquare_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCalcMtqZoneSquare', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrCalcMtqZoneSquare(_hMap: maptype.HMAP, _number: int, _minValue: float, _maxValue: float, _zoneSquare: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCalcMtqZoneSquare_t (_hMap, _number, _minValue, _maxValue, _zoneSquare)


# Преобразование матрицы высот (MTW) или матрицы качеств (MTQ) к заданной проекции
#  handle  - диалог визуального сопровождения процесса обработки,
#  namein  - имя исходной матрицы,
#  nameout - имя выходной матрицы,
#  mapreg  - адрес структуры с данными о заданной проекции,
#  datum   - параметры пересчета геодезических координат с заданного эллипсоида
#            на эллипсоид WGS-84 (может быть ноль),
#  ellparam - параметры пользовательского эллипсоида (может быть ноль).
#  ttype    - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
#  tparm    - параметры локального преобразования координат (см. mapcreat.h)
#
# Описание структур MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM - mapcreat.h
#  Диалогу визуального сопровождения процесса обработки посылаются сообщения WM_PROGRESSBAR/WM_PROGRESSBARUN:
#  Извещение об изменении состояния процесса, WPARAM - текущее состояние процесса в процентах (0% - 100%)
#  Если функция-отклик возвращает WM_PROGRESSBAR/WM_PROGRESSBARUN, то процесс завершается.
#  hEvent - адрес функции обратного вызова для уведомлении о процессе
#  eventparam - параметры функции обратного вызова
# При ошибке возвращает ноль, код ошибки возвращается функцией
# picexGetLastError (коды ошибок - maperr.rh)

    MtwProjectionReformingEvent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'MtwProjectionReformingEvent', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def MtwProjectionReformingEvent(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _hEvent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return MtwProjectionReformingEvent_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm, _hEvent, _eventparam)

    MtwProjectionReformingPro_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'MtwProjectionReformingPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def MtwProjectionReformingPro(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return MtwProjectionReformingPro_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm)

    MtwProjectionReformingEx_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'MtwProjectionReformingEx', maptype.HMESSAGE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def MtwProjectionReformingEx(_handle: maptype.HMESSAGE, _namein: ctypes.c_char_p, _nameout: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return MtwProjectionReformingEx_t (_handle, _namein, _nameout, _mapreg, _datum, _ellparam)

    MtwProjectionReformingUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'MtwProjectionReformingUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def MtwProjectionReformingUn(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return MtwProjectionReformingUn_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam)

    MtwProjectionReforming_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'MtwProjectionReforming', maptype.HMESSAGE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def MtwProjectionReforming(_handle: maptype.HMESSAGE, _namein: ctypes.c_char_p, _nameout: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return MtwProjectionReforming_t (_handle, _namein, _nameout, _mapreg)


# Cоздание матрицы водно-балансных бассейнов
# Элемент матрицы качеств содержит ключ объекта, к которому относится бассейн
# mtqname - имя создаваемой матрицы водно-балансных бассейнов
# parm    - параметры вызова
# При ошибке возвращает ноль

    mtrWaterZone_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrWaterZone', ctypes.c_char_p, ctypes.POINTER(WZONEPARM))
    def mtrWaterZone(_mtqname: ctypes.c_char_p, _parm: ctypes.POINTER(WZONEPARM)) -> int:
        return mtrWaterZone_t (_mtqname, _parm)

    mtrWaterZoneUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrWaterZoneUn', maptype.PWCHAR, ctypes.POINTER(WZONEPARM))
    def mtrWaterZoneUn(_mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(WZONEPARM)) -> int:
        return mtrWaterZoneUn_t (_mtqname.buffer(), _parm)


# Построение матрицы глубин (матрицы качеств mtq)
# hmap - исходная карта для построения матрицы,
# обеспеченная данными о рельефе дна
# depthmtqname - полное имя создаваемой матрицы
# depthmtqparm - параметры построения
# palette      - адрес палитры создаваемой матрицы
#                (если равен нулю, используется палитра по умолчанию)
# paletteCount - число цветов палитры
# fcallback    - функция обратного вызова для сообщения статуса выполнения (процентов),
#                это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#                в нее будет возвращено значение eventparam, вторым - тип сообщения
#                (AM_MTRNOTIFY (0x0581) или WM_ERROR - см. описание в maptype.h),
#                третий и четвертый параметры - в зависимости от типа сообщения.
# Только для ОС Windows: В случаях, когда функция обратного вызова не задается
# значение параметра depthmtqparm.Handle задает идентификатор окна (HWND), которому, если
# он указан (!=0), будет оправлятся сообщение AM_MTRNOTIFY (0x0581).
# Отправка уведомлений WM_PROGRESSBARUN, WM_ERROR и пр. с помощью функции обратного
# вызова и с помощью SendMessage (в ОС Windows) полностью аналогичны. При этом
# параметры WPARAM и LPARAM сообщения Windows являются соответственно аналогами
# параметров value2 и value3 функции обратного вызова.
# Для остановки процесса выполенения в обработчике сообщения AM_MTRNOTIFY следует
# установить результат (возвращаемое значение) равным значению AM_MTRNOTIFY.
# При отправке WM_ERROR в первом параметре содержится целочисленный код ошибки,
# во втором параметре передается указатель на текст описания ошибки.
# Текст передается в кодировке Unicode (UTF16).
# В случае ошибки возвращает 0.
# При ошибке возвращает 0.

    mtrBuildDepthMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildDepthMtq', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(DEPTHMTQPARM), ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mtrBuildDepthMtq(_hmap: maptype.HMAP, _depthmtqname: ctypes.c_char_p, _depthmtqparm: ctypes.POINTER(DEPTHMTQPARM), _palette: ctypes.POINTER(maptype.COLORREF), _paletteCount: int) -> int:
        return mtrBuildDepthMtq_t (_hmap, _depthmtqname, _depthmtqparm, _palette, _paletteCount)

    mtrBuildDepthMtqUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildDepthMtqUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(DEPTHMTQPARM), ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mtrBuildDepthMtqUn(_hmap: maptype.HMAP, _depthmtqname: mapsyst.WTEXT, _depthmtqparm: ctypes.POINTER(DEPTHMTQPARM), _palette: ctypes.POINTER(maptype.COLORREF), _paletteCount: int) -> int:
        return mtrBuildDepthMtqUn_t (_hmap, _depthmtqname.buffer(), _depthmtqparm, _palette, _paletteCount)

    mtrBuildDepthMtqCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildDepthMtqCallBack', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(DEPTHMTQPARM), ctypes.POINTER(maptype.COLORREF), ctypes.c_int, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrBuildDepthMtqCallBack(_hmap: maptype.HMAP, _depthmtqname: mapsyst.WTEXT, _depthmtqparm: ctypes.POINTER(DEPTHMTQPARM), _palette: ctypes.POINTER(maptype.COLORREF), _paletteCount: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mtrBuildDepthMtqCallBack_t (_hmap, _depthmtqname.buffer(), _depthmtqparm, _palette, _paletteCount, _fcallback, _eventparam)


# Вычисление статистики по матрице высот (mtw) или матрице качеств (mtq)
# hmap - исходная карта, обеспеченная матричными данными
# calcmatrixparm - параметры и результаты вычислений
# При наличии данных (значений качества) для вычисления статистики в области,
# заданной параметрами calcmatrixparm, возвращает 1.
# При отсутствии данных (значений качества) в заданной области возвращает 0.

    mtrCalcByMatrix_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCalcByMatrix', maptype.HMAP, ctypes.POINTER(CALCMATRIXPARM))
    def mtrCalcByMatrix(_hmap: maptype.HMAP, _calcmatrixparm: ctypes.POINTER(CALCMATRIXPARM)) -> int:
        return mtrCalcByMatrix_t (_hmap, _calcmatrixparm)


# Сплайн сглаживание матрицы высот
#  mtrName      - полное имя сглаживаемой матрицы
#  smoothFactor - уровень сглаживания (от 0 до 1, 0 - прямая линия,
#                 1 - кубический сплайн)
#  handle       - идентификатор окна диалога, которому посылаются
#                 сообщения о ходе процесса (процент обработки),
#                 если handle = 0, то сообщения не посылаются
#  messageId    - идентификатор сообщения с процентом обработки
# Для сглаживания матрицы запрашивается оперативная память в размере
# (RowCount#ColCount#16) байт, где RowCount - количество строк матрицы,
# ColCount - количество столбцов матрицы
# В случае ошибки возвращает 0

    mtrSmoothMtr_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrSmoothMtr', ctypes.c_char_p, ctypes.c_double, maptype.HMESSAGE, ctypes.c_int)
    def mtrSmoothMtr(_mtrName: ctypes.c_char_p, _smoothFactor: float, _handle: maptype.HMESSAGE, _messageId: int) -> int:
        return mtrSmoothMtr_t (_mtrName, _smoothFactor, _handle, _messageId)

    mtrSmoothMtrUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrSmoothMtrUn', maptype.PWCHAR, ctypes.c_double, maptype.HMESSAGE, ctypes.c_int)
    def mtrSmoothMtrUn(_mtrName: mapsyst.WTEXT, _smoothFactor: float, _handle: maptype.HMESSAGE, _messageId: int) -> int:
        return mtrSmoothMtrUn_t (_mtrName.buffer(), _smoothFactor, _handle, _messageId)


#####################################################################
# Кригинг
#####################################################################
# Последовательность вызова функций :
# hKriging = mapKrigingCreate(hmap, &MtrParm);
# Размер лага определяем, как максимальное расстояние между точками деленное
# на количество лагов. В этом случае будет перекрыт весь диапазон измерений.
# mapKrigingGetMinMaxDistance(hKriging, &MinDist, &MaxDist);
# double LagSize = MaxDist / LagCount;
# Вычисляем эмпирические вариограммы для лагов
# mapKrigingSetEmpiricalVariograms(hKriging, LagSize, LagCount);
# Показываем эмипирические вариограммы точками
#  for (int i = 0; i < LagCount; i++)
#    {
#      mapKrigingGetEmpiricalVariogram(Kriging, i, &Var, &Dist, &PointCount);
#      if (PointCount) Series2->AddXY(Dist, Var, IntToStr(PointCount), clGray);
#    }
# Вычисляем параметры модели
# Если параметр модели надо вычислить, то передаем в ф-цию -1
#  double Range  = -1;
#  double Sill   = -1;
#  double Nugget = -1;
#  if (! CalcRangeButton ->Down) Range  = atof(RangeEdit ->Text.c_str());
#  if (! CalcSillButton  ->Down) Sill   = atof(SillEdit  ->Text.c_str());
#  if (! CalcNuggetButton->Down) Nugget = atof(NuggetEdit->Text.c_str());
#  mapKrigingSetTeoreticalVariograms(hKriging, ModelType, &Range, &Sill, &Nugget))
#  Показываем вычисленные коэффициенты
#  RangeEdit ->Text = FloatToStr(Range);
#  SillEdit  ->Text = FloatToStr(Sill);
#  NuggetEdit->Text = FloatToStr(Nugget);
#  # Рисуем теоретическую вариограмму на графике линией
#  double LagsSize = LagSize # LagCount;
#  double Step = LagsSize / 100.;
#  for (double Dist = 0; Dist < LagsSize; Dist += Step)
#    {
#      mapKrigingGetTeoreticalVariogram(Kriging, Dist, &Var);
#      Series1->AddXY(Dist, Var / Divider, "", clGray);
#    }
# ...
#  После интерактивного подбора порога, самородка и радиуса строим матрицу
#  mapKrigingBuild(hKriging, MtrName);
# mapKrigingFree(hKriging);
#####################################################################
# Тип модели, применяемой для вычисления теоретичекой вариограммы
# Создание класса кригинга
# hmap - карта по объектам которой будет строится матрица
# mtrparm - параметры построения матрицы
# ranges  - для матриц качеств диапазон значений для палитры (при 0 не устанавливается)
# В случае ошибки возвращает 0

#   mtrKrigingCreate_t = mapsyst.GetProcAddress(curLib,,'mtrKrigingCreate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
#   def mtrKrigingCreate(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> :
#       return mtrKrigingCreate_t (_hmap, _hsit, _mtrparm, _ranges)


# Освобождение класса кригинга
# kriging - идентификатор созданного класса кригинга

    mtrKrigingFree_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrKrigingFree', ctypes.c_void_p)
    def mtrKrigingFree(_kriging: ctypes.c_void_p) -> ctypes.c_void_p:
        return mtrKrigingFree_t (_kriging)


# Возвращает минимальное и максимальное расстояние между точками
# kriging - идентификатор созданного класса кригинга
# min     - возвращаемое минимальное расстояние между точками (только узловыми)
# max     - возвращаемое максимальное расстояние между точками
# В случае ошибки возвращает 0

    mtrKrigingGetMinMaxDistance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingGetMinMaxDistance', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrKrigingGetMinMaxDistance(_kriging: ctypes.c_void_p, _min: ctypes.POINTER(ctypes.c_double), _max: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrKrigingGetMinMaxDistance_t (_kriging, _min, _max)


# Вычисляет эмпирическую вариограмму для лагов
# Лаг - диапазон расстояний между парами точек, для которых вычисляется эмпирическая вариограмма
# kriging - идентификатор созданного класса кригинга
# lagsize - размер лага в метрах (для всего диапазона LagSize = MaxDist / LagCount
# lagcount - количество лагов
# В случае ошибки возвращает 0

    mtrKrigingSetEmpiricalVariograms_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingSetEmpiricalVariograms', ctypes.c_void_p, ctypes.c_double, ctypes.c_int)
    def mtrKrigingSetEmpiricalVariograms(_kriging: ctypes.c_void_p, _lagsize: float, _lagcount: int) -> int:
        return mtrKrigingSetEmpiricalVariograms_t (_kriging, _lagsize, _lagcount)


# Возвращает параметры эмпирической вариограммы для лага
# kriging - идентификатор созданного класса кригинга
# lagnum  - номер лага, для которого возвращаются параметры
# variogram - эмпирическая вариограмма = sum(dH # dH) / 2
# dist      - центр лага по оси расстояний между парами точек = lagnum # lagsize + lagszie / 2
# pointcount - количество пар точек, попавших в диапазон лага
# В случае ошибки возвращает 0

    mtrKrigingGetEmpiricalVariogram_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingGetEmpiricalVariogram', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def mtrKrigingGetEmpiricalVariogram(_kriging: ctypes.c_void_p, _lagnum: int, _variogram: ctypes.POINTER(ctypes.c_double), _dist: ctypes.POINTER(ctypes.c_double), _pointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        return mtrKrigingGetEmpiricalVariogram_t (_kriging, _lagnum, _variogram, _dist, _pointcount)


# Вычисляет параметры модели, применяемой для вычисления теоретичекой вариограммы
# kriging - идентификатор созданного класса кригинга
# modeltype - тип модели (см. KM_SPHEROIDAL и др.)
# range     - радиус модели (метры) - точка на оси расстояний между точками
#             после которой кривая становится горизонтальной.
#             Если = -1 - то значение вычисляется, если > 0, то устанавливается
# sill      - порог - значение, которое принимает теоретическая вариограмма в
#             точке радиуса модели, из которого вычтено значение самородка
#             Если = -1 - то значение вычисляется, если > 0, то устанавливается
# nugget    - самородок - точка в которой кривая пересекает ось вариограммы.
#             Теоретически для нулевого расстояния между точками, изменение функции
#             должно быть равно 0. Однако при бесконечно малых расстояниях разница
#             между измерениями зачастую не стремится к нулю.
#             Если = -1 - то значение вычисляется, если >= 0, то устанавливается
# В случае ошибки возвращает 0

    mtrKrigingSetTeoreticalVariograms_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingSetTeoreticalVariograms', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrKrigingSetTeoreticalVariograms(_kriging: ctypes.c_void_p, _modeltype: int, _range: ctypes.POINTER(ctypes.c_double), _sill: ctypes.POINTER(ctypes.c_double), _nugget: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrKrigingSetTeoreticalVariograms_t (_kriging, _modeltype, _range, _sill, _nugget)


# Вычисляет значение теоретической вариограммы по расстоянию между двумя точками
# kriging - идентификатор созданного класса кригинга
# В случае ошибки возвращает 0

    mtrKrigingGetTeoreticalVariogram_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingGetTeoreticalVariogram', ctypes.c_void_p, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrKrigingGetTeoreticalVariogram(_kriging: ctypes.c_void_p, _dist: float, _var: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrKrigingGetTeoreticalVariogram_t (_kriging, _dist, _var)


# Строит матрицу
# kriging - идентификатор созданного класса кригинга
# mtrname - имя создаваемой маррицы высот или качеств
# В случае ошибки возвращает 0

    mtrKrigingBuild_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingBuild', ctypes.c_void_p, ctypes.c_char_p)
    def mtrKrigingBuild(_kriging: ctypes.c_void_p, _mtrname: ctypes.c_char_p) -> int:
        return mtrKrigingBuild_t (_kriging, _mtrname)

    mtrKrigingBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrKrigingBuildUn', ctypes.c_void_p, maptype.PWCHAR)
    def mtrKrigingBuildUn(_kriging: ctypes.c_void_p, _mtrname: mapsyst.WTEXT) -> int:
        return mtrKrigingBuildUn_t (_kriging, _mtrname.buffer())


#####################################################################
# Кокригинг
#####################################################################
# Признак (внутри которого или между которыми) вычисляется ковариация в кокригинге
# Создание класса кокригинга
# ranges  - для матриц качеств диапазон значений для палитры (при 0 не устанавливается)

#   mtrCokrigingCreate_t = mapsyst.GetProcAddress(curLib,,'mtrCokrigingCreate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
#   def mtrCokrigingCreate(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> :
#       return mtrCokrigingCreate_t (_hmap, _hsit, _mtrparm, _ranges)


# Освобождение класса кокригинга

    mtrCokrigingFree_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrCokrigingFree', ctypes.c_void_p)
    def mtrCokrigingFree(_cokriging: ctypes.c_void_p) -> ctypes.c_void_p:
        return mtrCokrigingFree_t (_cokriging)


# Возвращает минимальное и максимальное расстояние между точками

    mtrCokrigingGetMinMaxDistance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingGetMinMaxDistance', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetMinMaxDistance(_cokriging: ctypes.c_void_p, _feature: int, _min: ctypes.POINTER(ctypes.c_double), _max: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCokrigingGetMinMaxDistance_t (_cokriging, _feature, _min, _max)


# Вычисляет эмпирическую вариограмму

    mtrCokrigingSetEmpiricalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingSetEmpiricalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def mtrCokrigingSetEmpiricalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _lagsize: float, _lagcount: int) -> int:
        return mtrCokrigingSetEmpiricalCovariance_t (_cokriging, _feature, _lagsize, _lagcount)


# Возвращает значение эмпирической вариограммы для лага

    mtrCokrigingGetEmpiricalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingGetEmpiricalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def mtrCokrigingGetEmpiricalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _lagnum: int, _variogram: ctypes.POINTER(ctypes.c_double), _dist: ctypes.POINTER(ctypes.c_double), _pointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        return mtrCokrigingGetEmpiricalCovariance_t (_cokriging, _feature, _lagnum, _variogram, _dist, _pointcount)


# Возвращает значение дисперсии

    mtrCokrigingGetVariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingGetVariance', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetVariance(_cokriging: ctypes.c_void_p, _feature: int, _variance: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCokrigingGetVariance_t (_cokriging, _feature, _variance)


# Возвращает количество точек, по которым считалась дисперсия
# Для признаков - количество реальных исходных точек
# Для кросс - количество точек на которых одновременно выполнялись оба измерения

    mtrCokrigingGetVariancePointCount_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingGetVariancePointCount', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mtrCokrigingGetVariancePointCount(_cokriging: ctypes.c_void_p, _feature: int, _variancepointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        return mtrCokrigingGetVariancePointCount_t (_cokriging, _feature, _variancepointcount)


# Вычисляет теоретическую вариограмму

    mtrCokrigingSetTeoreticalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingSetTeoreticalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingSetTeoreticalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _modeltype: int, _range: ctypes.POINTER(ctypes.c_double), _sill: ctypes.POINTER(ctypes.c_double), _nugget: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCokrigingSetTeoreticalCovariance_t (_cokriging, _feature, _modeltype, _range, _sill, _nugget)


# Вычисляет значение теоретической вариограммы по расстоянию между двумя точками

    mtrCokrigingGetTeoreticalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingGetTeoreticalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetTeoreticalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _dist: float, _var: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrCokrigingGetTeoreticalCovariance_t (_cokriging, _feature, _dist, _var)


# Строит матрицу

    mtrCokrigingBuild_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingBuild', ctypes.c_void_p, ctypes.c_char_p)
    def mtrCokrigingBuild(_cokriging: ctypes.c_void_p, _mtrname: ctypes.c_char_p) -> int:
        return mtrCokrigingBuild_t (_cokriging, _mtrname)

    mtrCokrigingBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrCokrigingBuildUn', ctypes.c_void_p, maptype.PWCHAR)
    def mtrCokrigingBuildUn(_cokriging: ctypes.c_void_p, _mtrname: mapsyst.WTEXT) -> int:
        return mtrCokrigingBuildUn_t (_cokriging, _mtrname.buffer())


#####################################################################
# Логарифмическая интерполяция
#####################################################################

    mtrLogarithmBuild_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrLogarithmBuild', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
    def mtrLogarithmBuild(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrLogarithmBuild_t (_hmap, _hsit, _mtrname, _mtrparm, _ranges)

    mtrLogarithmBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrLogarithmBuildUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
    def mtrLogarithmBuildUn(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> int:
        return mtrLogarithmBuildUn_t (_hmap, _hsit, _mtrname.buffer(), _mtrparm, _ranges)


# Преобразование матрицы высот в вектор
# hmap       - основная карта
# hsit       - векторная карта в которую пишутся объекты
# mtrnum     - номер оконтуриваемой матрицы высот, добавленной к карте
# isfilter   - признак фильтрации точек, лежащих на одной прямой
# hselect    - содержит созданные объекты
#              если = 0, то не заполняется, ненулевое значение сильно замедляет обработку
# classes    - распознаваемые классы
# classcount - количество классов
# border     - объект, ограничивающий область преобразования матрицы в вектор
# iscuthole  - признак вырезания подобъектов
#              если = 0, то внутренний объект всегда имеет больший номер (Key), чем внешний
# handle     - идентификатор окна диалога, которому посылается cообщение 0x0581
#              в wParam - процент выполненной обработки
#              в lParam - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# fcallback  - функция обратного вызова для сообщения статуса выполнения (процентов),
#              это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#              в нее будет возвращено значение eventparam, вторым - код сообщения
#              (0x0581),
#              в третьем параметре  - процент выполненной обработки
#              в чевертом параметре - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# eventparam - параметр, передаваемый в функцию обратного вызова для идентификации
#              отклика на вызывающей стороне.
# Если handle (или fcallback) равно нулю - сообщения не посылаются.
# Текст передается в кодировке Unicode (UTF16).
# В случае ошибки возвращает 0

    mtrMtwToVector_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrMtwToVector', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.HMESSAGE)
    def mtrMtwToVector(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _handle: maptype.HMESSAGE) -> int:
        return mtrMtwToVector_t (_hmap, _hsit, _mtrnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _handle)

    mtrMtwToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrMtwToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrMtwToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mtrMtwToVectorCallBack_t (_hmap, _hsit, _mtrnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)


# Преобразование матрицы качеств в вектор
# hmap       - основная карта
# hsit       - векторная карта в которую пишутся объекты
# mtqnum     - номер исходной матрицы качеств, добавленной к карте
# isfilter   - признак фильтрации точек, лежащих на одной прямой (0..1)
# hselect    - содержит созданные объекты (если = 0, то не заполняется)
# classes    - распознаваемые классы
# classcount - количество классов
# border     - объект, ограничивающий область преобразования матрицы в вектор
# iscuthole  - признак вырезания подобъектов
#              если = 0, то внутренний объект всегда имеет больший номер (Key), чем внешний
# handle     - идентификатор окна диалога, которому посылается cообщение 0x0581
#              в wParam - процент выполненной обработки
#              в lParam - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# fcallback  - функция обратного вызова для сообщения статуса выполнения (процентов),
#              это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#              в нее будет возвращено значение eventparam, вторым - код сообщения
#              (0x0581),
#              в третьем параметре  - процент выполненной обработки
#              в чевертом параметре - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# eventparam - параметр, передаваемый в функцию обратного вызова для идентификации
#              отклика на вызывающей стороне.
# Если handle (или fcallback) равно нулю - сообщения не посылаются.
# Текст передается в кодировке Unicode (UTF16).
# В случае ошибки возвращает 0.

    mtrMtqToVector_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrMtqToVector', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.HMESSAGE)
    def mtrMtqToVector(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtqnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _handle: maptype.HMESSAGE) -> int:
        return mtrMtqToVector_t (_hmap, _hsit, _mtqnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _handle)

    mtrMtqToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrMtqToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrMtqToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtqnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mtrMtqToVectorCallBack_t (_hmap, _hsit, _mtqnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)


# Преобразование растра в вектор
# hmap       - основная карта
# hsit       - векторная карта в которую пишутся объекты
# rstnum     - номер исходного растра, добавленного к карте
# isfilter   - признак фильтрации точек, лежащих на одной прямой (0..1)
# hselect    - содержит созданные объекты (если = 0, то не заполняется)
# classes    - распознаваемые классы
# classcount - количество классов
# border     - объект, ограничивающий область преобразования растра в вектор
# iscuthole  - признак вырезания подобъектов
#              если = 0, то внутренний объект всегда имеет больший номер (Key), чем внешний
# handle     - идентификатор окна диалога, которому посылается cообщение 0x0581
#              в wParam - процент выполненной обработки
#              в lParam - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# fcallback  - функция обратного вызова для сообщения статуса выполнения (процентов),
#              это функция типа EVENTCALL (см. описание в maptype.h), первым параметром
#              в нее будет возвращено значение eventparam, вторым - код сообщения
#              (0x0581),
#              в третьем параметре  - процент выполненной обработки
#              в чевертом параметре - адрес строки с названием выполняемого этапа
#              Если процесс должен быть принудительно завершен, в ответ
#              должно вернуться значение 0x0581.
# eventparam - параметр, передаваемый в функцию обратного вызова для идентификации
#              отклика на вызывающей стороне.
# Если handle (или fcallback) равно нулю - сообщения не посылаются
# Текст передается в кодировке Unicode (UTF16)
# В случае ошибки возвращает 0

    mtrRstToVector_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrRstToVector', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.HMESSAGE)
    def mtrRstToVector(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _rstnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _handle: maptype.HMESSAGE) -> int:
        return mtrRstToVector_t (_hmap, _hsit, _rstnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _handle)

    mtrRstToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrRstToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_int, maptype.HOBJ, ctypes.c_int, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrRstToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _rstnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mtrRstToVectorCallBack_t (_hmap, _hsit, _rstnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)


# Построение матрицы плотности
# hmap    - основная карта
# hsit    - векторная карта с объектами, по которым строится матрица плотности
# mtqname - имя создаваемой матрицы
# hselect - объекты, по которым строится матрица (если = 0, то все объекты карты)
# parm    - параметры построения
# hwnd    - окно, которому посылаются сообщения WM_PROGRESSBAR с процентом
#           обработки в WPARAM (если = 0, то сообщения не посылаются)
# При ошибке возвращает 0

    mtrBuildDensityMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildDensityMtq', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.HSELECT, ctypes.POINTER(BUILDDENSITY), maptype.HMESSAGE)
    def mtrBuildDensityMtq(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtqname: mapsyst.WTEXT, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(BUILDDENSITY), _hwnd: maptype.HMESSAGE) -> int:
        return mtrBuildDensityMtq_t (_hmap, _hsit, _mtqname.buffer(), _hselect, _parm, _hwnd)


# Построение матрицы видимости
# hmap    - основная карта
# hsite    - векторная карта с объектами, по которым строится матрица плотности
# mtqname - имя создаваемой матрицы
# hselect - объекты, по которым строится матрица (если = 0, то все объекты карты)
# parm    - параметры построения
# hwnd    - окно, которому посылаются сообщения WM_PROGRESSBAR с процентом
#           обработки в WPARAM (если = 0, то сообщения не посылаются)
# При ошибке возвращает 0

    mtrBuildVisibleMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrBuildVisibleMtq', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.HSELECT, ctypes.POINTER(BUILDVISIBLE), maptype.HMESSAGE)
    def mtrBuildVisibleMtq(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mtqname: mapsyst.WTEXT, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(BUILDVISIBLE), _hwnd: maptype.HMESSAGE) -> int:
        return mtrBuildVisibleMtq_t (_hmap, _hsite, _mtqname.buffer(), _hselect, _parm, _hwnd)


#####################################################################
# Универсальные функции доступа к матрицам вывот, слоев и качеств
#####################################################################
# Запросить число открытых файлов матричных данных
# hMap -  идентификатор открытых данных
# matrixType - тип матрицы (FILE_MTW, FILE_MTL, FILE_MTQ)
# Если matrixType == 0, функция возвращает количество всех матриц документа
# При ошибке возвращает ноль

    mtrexGetMatrixCount_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixCount', maptype.HMAP, ctypes.c_int)
    def mtrexGetMatrixCount(_hMap: maptype.HMAP, _matrixType: int) -> int:
        return mtrexGetMatrixCount_t (_hMap, _matrixType)


# Запросить номер матрицы в цепочке по имени файла
# name - имя файла матрицы
# В цепочке номера матриц начинаются с 1
# При ошибке возвращает ноль

    mtrexGetMatrixNumberByNameUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixNumberByNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR)
    def mtrexGetMatrixNumberByNameUn(_hMap: maptype.HMAP, _matrixType: int, _name: mapsyst.WTEXT) -> int:
        return mtrexGetMatrixNumberByNameUn_t (_hMap, _matrixType, _name.buffer())


# Запросить имя файла матричных данных
# hMap       - идентификатор открытой основной векторной карты
# number     - номер файла в цепочке
# matrixType - тип матрицы (FILE_MTW, FILE_MTL, FILE_MTQ)
# name       - адрес строки для размещения результата
# size       - размер строки
# При ошибке возвращает ноль

    mtrexGetMatrixNameUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixNameUn', maptype.HMAP, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mtrexGetMatrixNameUn(_hMap: maptype.HMAP, _number: int, _matrixType: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mtrexGetMatrixNameUn_t (_hMap, _number, _matrixType, _name.buffer(), _size)


# Запросить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# matrixType - тип матрицы (FILE_MTW, FILE_MTL, FILE_MTQ)
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mtrexGetMatrixLocation_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixLocation', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mtrexGetMatrixLocation(_hMap: maptype.HMAP, _number: int, _matrixType: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mtrexGetMatrixLocation_t (_hMap, _number, _matrixType, _location)


# Установить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# matrixType - тип матрицы (FILE_MTW, FILE_MTL, FILE_MTQ)
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mtrexSetMatrixLocation_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexSetMatrixLocation', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mtrexSetMatrixLocation(_hMap: maptype.HMAP, _number: int, _matrixType: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mtrexSetMatrixLocation_t (_hMap, _number, _matrixType, _location)


# Запросить/Установить степень видимости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# view = 0 - не виден
# view = 1 - полная
# view = 2 - насыщенная
# view = 3 - полупрозрачная
# view = 4 - средняя
# view = 5 - прозрачная

    mtrexGetMatrixView_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mtrexGetMatrixView(_hMap: maptype.HMAP, _number: int, _matrixType: int) -> int:
        return mtrexGetMatrixView_t (_hMap, _number, _matrixType)

    mtrexSetMatrixView_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexSetMatrixView', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mtrexSetMatrixView(_hMap: maptype.HMAP, _number: int, _matrixType: int, _view: int) -> int:
        return mtrexSetMatrixView_t (_hMap, _number, _matrixType, _view)


# Запросить флаг редактируемости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mtrexGetMatrixEdit_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixEdit', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mtrexGetMatrixEdit(_hMap: maptype.HMAP, _number: int, _matrixType: int) -> int:
        return mtrexGetMatrixEdit_t (_hMap, _number, _matrixType)


# Запросить прозрачность палитры матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает степень прозрачности в процентах от 0 до 100

    mtrexGetMatrixTransparent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixTransparent', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mtrexGetMatrixTransparent(_hMap: maptype.HMAP, _number: int, _matrixType: int) -> int:
        return mtrexGetMatrixTransparent_t (_hMap, _number, _matrixType)


# Установить прозрачность палитры матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# transparent - прозрачность в процентах от 0 до 100
# При ошибке возвращает ноль

    mtrexSetMatrixTransparent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexSetMatrixTransparent', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mtrexSetMatrixTransparent(_hMap: maptype.HMAP, _number: int, _matrixType: int, _transparent: int) -> int:
        return mtrexSetMatrixTransparent_t (_hMap, _number, _matrixType, _transparent)


# Запросить/Установить порядок отображения матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# order  - порядок (0 - под картой, 1 - над картой)
# При ошибке возвращает ноль

    mtrexSetMatrixViewOrder_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexSetMatrixViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mtrexSetMatrixViewOrder(_hMap: maptype.HMAP, _number: int, _matrixType: int, _order: int) -> int:
        return mtrexSetMatrixViewOrder_t (_hMap, _number, _matrixType, _order)

    mtrexGetMatrixViewOrder_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexGetMatrixViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mtrexGetMatrixViewOrder(_hMap: maptype.HMAP, _number: int, _matrixType: int) -> int:
        return mtrexGetMatrixViewOrder_t (_hMap, _number, _matrixType)


# Поменять очередность отображения матриц в цепочке
#   oldNumber - номер файла в цепочке
#   newNumber - устанавливаемый номер файла в цепочке
#  При ошибке возвращает ноль

    mtrexChangeOrderMatrixShow_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexChangeOrderMatrixShow', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mtrexChangeOrderMatrixShow(_hMap: maptype.HMAP, _matrixType: int, _oldNumber: int, _newNumber: int) -> int:
        return mtrexChangeOrderMatrixShow_t (_hMap, _matrixType, _oldNumber, _newNumber)


# Закрыть матричные данные
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# если number == 0, закрываются все матрицы в окне
# ЧТОБЫ ОСВОБОДИТЬ ВСЕ РЕСУРСЫ - НУЖНО ВЫЗВАТЬ mapCloseData(hMap)

    mtrexCloseMatrix_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_int,'mtrexCloseMatrix', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mtrexCloseMatrix(_hMap: maptype.HMAP, _number: int, _matrixType: int) -> int:
        return mtrexCloseMatrix_t (_hMap, _number, _matrixType)

except Exception as e:
    print(e)
    mtrexlib = 0