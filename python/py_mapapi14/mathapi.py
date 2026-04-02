#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mathapi
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class COMPLEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("re",ctypes.c_double),
                ("im",ctypes.c_double)]
#-----------------------------


#-----------------------------
class OBJECT_CROSSING(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HWND),
                ("Hovl",maptype.HOVL),
                ("Map",maptype.HMAP),
                ("Map2",maptype.HMAP),
                ("Site",maptype.HSITE),
                ("Site2",maptype.HSITE),
                ("Precision",ctypes.c_double),
                ("SheetNumber",ctypes.c_int),
                ("SheetNumber2",ctypes.c_int),
                ("ObjectNumber",ctypes.c_int),
                ("ExcludeKey",ctypes.c_int),
                ("Function",ctypes.c_int),
                ("CodeInside",ctypes.c_int),
                ("CodeOutside",ctypes.c_int),
                ("FlagForOne",ctypes.c_int),
                ("FlagSelfcrossing",ctypes.c_int),
                ("FlagTempletSubject",ctypes.c_int),
                ("Flag3d",ctypes.c_int),
                ("TempletNumber",ctypes.c_int),
                ("Report",ctypes.c_int),
                ("FlagAdjustTemplet",ctypes.c_int),
                ("Reserve",ctypes.c_char*136),
                ("SmallArea",ctypes.c_double)]
#-----------------------------


#-----------------------------
class ROUGH(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Precision",ctypes.c_double),
                ("Scatter",ctypes.c_double),
                ("PrecisionFlag",ctypes.c_int),
                ("ScatterFlag",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GEN_CODESET(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Area",ctypes.c_int),
                ("Line1",ctypes.c_int),
                ("Line2",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GEN_HYDROGRAPHY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HMESSAGE),
                ("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("SelectAdjust",maptype.HSELECT),
                ("SelectBound",maptype.HSELECT),
                ("SelectPond",maptype.HSELECT),
                ("Width1",ctypes.c_double),
                ("Width2",ctypes.c_double),
                ("Precision",ctypes.c_double),
                ("Distance",ctypes.c_double),
                ("MinLength",ctypes.c_double),
                ("MinArea",ctypes.c_double),
                ("MinWidth",ctypes.c_double),
                ("DirectionLength",ctypes.c_double),
                ("DirectionOffset",ctypes.c_double),
                ("SelectAlluvion",maptype.HSELECT),
                ("SelectReserve",maptype.HSELECT),
                ("Reserve",ctypes.c_int*35),
                ("Code_WaterMark",ctypes.c_int),
                ("Code_Direction",ctypes.c_int),
                ("Code_ShoreLine",ctypes.c_int),
                ("Code_WaterLine",ctypes.c_int),
                ("Code_WaterBorder",ctypes.c_int),
                ("Code_WaterCover",ctypes.c_int),
                ("Code_Shallow",ctypes.c_int),
                ("Code_Pond",ctypes.c_int),
                ("Code_Bog",ctypes.c_int),
                ("Code_Reservoir",ctypes.c_int),
                ("Code_Aquaculture",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GEN_SQUARERIVEREX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HMESSAGE),
                ("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("SelectAdjust",maptype.HSELECT),
                ("Precision",ctypes.c_double),
                ("Width",ctypes.c_double*2),
                ("Code_RiverLine",ctypes.c_int*2),
                ("Code_River",ctypes.c_int),
                ("Code_ShoreLine",ctypes.c_int),
                ("Code_WaterLine",ctypes.c_int),
                ("Code_WaterBorder",ctypes.c_int),
                ("Code_WaterCover",ctypes.c_int),
                ("Code_Shallow",ctypes.c_int),
                ("Code_Pond",ctypes.c_int),
                ("Code_Bog",ctypes.c_int),
                ("Code_Reservoir",ctypes.c_int),
                ("Code_Aquaculture",ctypes.c_int),
                ("SelectBound",maptype.HSELECT),
                ("SelectPond",maptype.HSELECT),
                ("Code",ctypes.c_int*8),
                ("Reserve",ctypes.c_char*8),
                ("Distance",ctypes.c_double),
                ("MinLength",ctypes.c_double),
                ("MinArea",ctypes.c_double),
                ("MinWidth",ctypes.c_double)]
#-----------------------------


#-----------------------------
class GEN_SQUARERIVER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("Handle",maptype.HMESSAGE),
                ("DiapasonCount",ctypes.c_int),
                ("MinWidth",ctypes.c_double),
                ("Precision",ctypes.c_double),
                ("OldKey",ctypes.c_char*32),
                ("SelectAdjust",maptype.HSELECT),
                ("Reserve",ctypes.c_char*28)]
#-----------------------------


#-----------------------------
class GEN_SQUARERIVER_DIAPASON(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Width1",ctypes.c_int),
                ("Width2",ctypes.c_int),
                ("NewKey",ctypes.c_char*32)]
#-----------------------------


#-----------------------------
class RIVERGENERALIZATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("OldKey",ctypes.c_char*32),
                ("NewKey",ctypes.c_char*32),
                ("Width",ctypes.c_double),
                ("Precision",ctypes.c_double)]
#-----------------------------


#-----------------------------
class LINEARTRANSFPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("a",ctypes.c_double),
                ("b",ctypes.c_double),
                ("c",ctypes.c_double),
                ("d",ctypes.c_double),
                ("e",ctypes.c_double),
                ("f",ctypes.c_double),
                ("A",ctypes.c_double),
                ("B",ctypes.c_double),
                ("C",ctypes.c_double),
                ("D",ctypes.c_double),
                ("E",ctypes.c_double),
                ("F",ctypes.c_double),
                ("Scale",ctypes.c_double),
                ("Rotate",ctypes.c_double)]
#-----------------------------


#-----------------------------
class CALCTRANSMERCATORPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("IsCalcM",ctypes.c_int),
                ("IsSetM",ctypes.c_int),
                ("M",ctypes.c_double),
                ("IsCalcLo",ctypes.c_int),
                ("IsSetLo",ctypes.c_int),
                ("Lo",ctypes.c_double),
                ("IsCalcBo",ctypes.c_int),
                ("IsSetBo",ctypes.c_int),
                ("Bo",ctypes.c_double),
                ("IsCalcDx",ctypes.c_int),
                ("IsSetDx",ctypes.c_int),
                ("Dx",ctypes.c_double),
                ("IsCalcDy",ctypes.c_int),
                ("IsSetDy",ctypes.c_int),
                ("Dy",ctypes.c_double),
                ("IsCalcAn",ctypes.c_int),
                ("IsSetAn",ctypes.c_int),
                ("An",ctypes.c_double)]
#-----------------------------


#-----------------------------
class OBJVALUE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value",ctypes.c_double),
                ("Key",ctypes.c_uint),
                ("Color",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class RANGEITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("RealName",maptype.WCHAR1*(256*2)),
                ("Min",ctypes.c_double),
                ("Max",ctypes.c_double),
                ("Color",ctypes.c_int),
                ("Step",ctypes.c_int),
                ("Thick",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("Reserve",ctypes.c_int*2)]
#-----------------------------


#-----------------------------
class THEMATICPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hmap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Handle",maptype.HMESSAGE),
                ("SelectBound",maptype.HSELECT),
                ("ResMapName",maptype.WCHAR1*(128*2)),
                ("LegendName",maptype.WCHAR1*(128*2)),
                ("ValueFieldType",ctypes.c_int),
                ("ValueSem",ctypes.c_int),
                ("ImageType",ctypes.c_int),
                ("ConnectType",ctypes.c_int),
                ("ItemsCount",ctypes.c_int),
                ("SearchMode",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("ContourColor",ctypes.c_int),
                ("ContourThick",ctypes.c_int),
                ("Transparent",ctypes.c_int),
                ("DiaFontHeight",ctypes.c_int),
                ("DiaLabelColor",ctypes.c_int),
                ("DiaShadowColor",ctypes.c_int),
                ("DiaCircleColor",ctypes.c_int),
                ("EmptyCreate",ctypes.c_int),
                ("LegendToDiagram",ctypes.c_int),
                ("MakeNumberCheck",ctypes.c_int),
                ("RecodeCheck",ctypes.c_int),
                ("LineCutCheck",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("NoPress",ctypes.c_int),
                ("SetScale",ctypes.c_int),
                ("HatchingBgColor",ctypes.c_int),
                ("HatchingColor",ctypes.c_int),
                ("PlaceX",ctypes.c_double),
                ("PlaceY",ctypes.c_double),
                ("LegendLabelColor",ctypes.c_int),
                ("LegendLabelShadowColor",ctypes.c_int),
                ("LegendBarWide",ctypes.c_int),
                ("LegendBarHeight",ctypes.c_int),
                ("LegendInterval",ctypes.c_int),
                ("LegendFontHeight",ctypes.c_int),
                ("LegendColCount",ctypes.c_int),
                ("LegendRecodeCheck",ctypes.c_int),
                ("RegionColCount",ctypes.c_int),
                ("FlagTerritory",ctypes.c_int),
                ("NameSem",ctypes.c_int),
                ("Reserve2",ctypes.c_int),
                ("RegionX",ctypes.c_double),
                ("RegionY",ctypes.c_double),
                ("Reserve",ctypes.c_int*56)]
#-----------------------------


#-----------------------------
class THEMDIALOGPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ConnectField",ctypes.c_char*256),
                ("ValueField",ctypes.c_char*256),
                ("ConnectFieldType",ctypes.c_int),
                ("ConnectSem",ctypes.c_int),
                ("IndexDelimiter",ctypes.c_int),
                ("LinesBegin",ctypes.c_int),
                ("NumberConnectField",ctypes.c_int),
                ("NumberValueField",ctypes.c_int),
                ("DataType",ctypes.c_int),
                ("CodeType",ctypes.c_int),
                ("NumberColorField",ctypes.c_int),
                ("Reserve1",ctypes.c_int),
                ("Delimiter",ctypes.c_int),
                ("Quote",ctypes.c_int),
                ("Reserve",ctypes.c_int*4)]
#-----------------------------


#-----------------------------
class TEO_PARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Len_Limit",ctypes.c_double),
                ("Ds_Limit",ctypes.c_double),
                ("Da_Limit",ctypes.c_double),
                ("Da",ctypes.c_double),
                ("Dxy",ctypes.c_double),
                ("Sd",ctypes.c_double),
                ("ErrorCode",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class DIAOPTIONS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hmap",maptype.HMAP),
                ("TempMap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Houtsite",maptype.HSITE),
                ("Handle",maptype.HMESSAGE),
                ("ConnectType",ctypes.c_int),
                ("Typebase",ctypes.c_int),
                ("ValueType",ctypes.c_int),
                ("PercentType",ctypes.c_int),
                ("PercentCode",ctypes.c_int),
                ("SizeCode",ctypes.c_int),
                ("EmptyCreate",ctypes.c_int),
                ("OtherColor",ctypes.c_int),
                ("OtherValue",ctypes.c_double),
                ("ImageType",ctypes.c_int),
                ("Shadow",ctypes.c_int),
                ("ShadowColor",ctypes.c_int),
                ("ContourCreate",ctypes.c_int),
                ("ContourColor",ctypes.c_int),
                ("Ex3D",ctypes.c_int),
                ("GraphColor",ctypes.c_int),
                ("NetCheck",ctypes.c_int),
                ("NetColor",ctypes.c_int),
                ("AreaCheck",ctypes.c_int),
                ("IntegrCheck",ctypes.c_int),
                ("ExBorder",ctypes.c_int),
                ("ExBorderColor",ctypes.c_int),
                ("SizeColor",ctypes.c_int),
                ("ColWide",ctypes.c_double),
                ("ColInterval",ctypes.c_double),
                ("IsMakeLegend",ctypes.c_int),
                ("LegendType",ctypes.c_int),
                ("LegendColCount",ctypes.c_int),
                ("IsSizeLegend",ctypes.c_int),
                ("LegendRadius",ctypes.c_double),
                ("LegendBarWide",ctypes.c_double),
                ("LegendBarHeight",ctypes.c_double),
                ("LegendInterval",ctypes.c_double),
                ("ColorLegendX",ctypes.c_double),
                ("ColorLegendY",ctypes.c_double),
                ("SizeLegendX",ctypes.c_double),
                ("SizeLegendY",ctypes.c_double),
                ("LegendToDiagram",ctypes.c_int),
                ("ValueToDiagram",ctypes.c_int),
                ("PercToDiagram",ctypes.c_int),
                ("LegendLabelType",ctypes.c_int),
                ("LabelFromFill",ctypes.c_int),
                ("LegendLineColor",ctypes.c_int),
                ("LegendLabelColor",ctypes.c_int),
                ("LabelShadowCheck",ctypes.c_int),
                ("LabelShadowColor",ctypes.c_int),
                ("PlacePoint",ctypes.c_int),
                ("TopLabelScale",ctypes.c_int),
                ("BotLabelScale",ctypes.c_int),
                ("FontHeight",ctypes.c_double)]
#-----------------------------


#-----------------------------
class SEMANTICPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Title",maptype.WCHAR1*(maptype.MAX_PATH*2)),
                ("Code",ctypes.c_int),
                ("Color",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SIZEPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SizeType",ctypes.c_int),
                ("SizeScale",ctypes.c_int),
                ("Sizecount",ctypes.c_int),
                ("SizePrec",ctypes.c_int),
                ("FixSize",ctypes.c_double),
                ("MinRadius",ctypes.c_double),
                ("MaxRadius",ctypes.c_double)]
#-----------------------------

try:
    if os.environ['gismathdll']:
        gismathname = os.environ['gismathdll']
except KeyError:
    gismathname = 'gis64math.dll' 

try:
    mathlib = mapsyst.LoadLibrary( gismathname )


#------------------------------------------------------------------
# ПАРАМЕТРЫ ФУНКЦИИ ОБРАБОТКИ ПЕРЕСЕЧЕНИЙ ОБЪЕКТОВ КАРТЫ
#------------------------------------------------------------------

#   OBJECT_CROSSING_t = mapsyst.GetProcAddress(curLib,typedef struct,'OBJECT_CROSSING')
#   def OBJECT_CROSSING() -> typedef struct:
#       return OBJECT_CROSSING_t ()


# Отсечение элементарного треугольного объекта от сложного площадного бъекта карты
# Создание класса (Конструктор)
# info - площадной бъект карты
# Возвращает указатель на класс
# При ошибке возвращает 0

    mathCreateCutProcess_t = mapsyst.GetProcAddress(mathlib,mathapi.HCUT,'mathCreateCutProcess', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mathCreateCutProcess(_Map: maptype.HMAP, _info: maptype.HOBJ, _precision: float) -> mathapi.HCUT:
        return mathCreateCutProcess_t (_Map, _info, _precision)


# Отсечение элементарного треугольного объекта от сложного площадного бъекта карты
# Запросить следующий треугольный объект
# info - результат (треугольный объект)
# Для заполнения высот точек(если исходный объект имеет 3-х мерную метрику)
#     info необходимо создавать с 3-х мерной метрикой
# Возвращает остаток сложного площадного бъекта карты
# При ошибке возвращает 0

    mathGetNextTriangularObject_t = mapsyst.GetProcAddress(mathlib,maptype.HOBJ,'mathGetNextTriangularObject', mathapi.HCUT, maptype.HOBJ)
    def mathGetNextTriangularObject(_hcut: mathapi.HCUT, _info: maptype.HOBJ) -> maptype.HOBJ:
        return mathGetNextTriangularObject_t (_hcut, _info)


# Отсечение элементарного треугольного объекта от сложного площадного бъекта карты
# Освобождение класса (Деструктор)

    mathFreeCutProcess_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathFreeCutProcess', mathapi.HCUT)
    def mathFreeCutProcess(_hcut: mathapi.HCUT) -> int:
        return mathFreeCutProcess_t (_hcut)


###################################################################
#    ФУНКЦИИ ПРЕОБРАЗОВАНИЯ ПЛОЩАДНОГО ОБЪЕКТА С ПОДОБЪЕКТАМИ     #
#    1. В ОДИН КОНТУР                                             #
#    2. ДЕЛЕНИЕ НА ТРЕУГОЛЬНИКИ                                   #
###################################################################
# Преобразование объекта  in  и всех его подобъектов в общий контур,
# с сохранением в объект  out
# (объект без подобъектов не обрабатывает)
# При ошибке возвращает 0

    mathTransformSubjectsToObject_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathTransformSubjectsToObject', maptype.HOBJ, maptype.HOBJ)
    def mathTransformSubjectsToObject(_in: maptype.HOBJ, _out: maptype.HOBJ) -> int:
        return mathTransformSubjectsToObject_t (_in, _out)


# Нарезка контура объекта  in  на отдельные треугольники с размещением
# в объекте  out  в виде составных частей (объекта с подобъектами)
# При ошибке возвращает 0

    mathCutObjectToTriangles_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCutObjectToTriangles', maptype.HOBJ, maptype.HOBJ)
    def mathCutObjectToTriangles(_in: maptype.HOBJ, _out: maptype.HOBJ) -> int:
        return mathCutObjectToTriangles_t (_in, _out)


###################################################################
#        ФУНКЦИИ РАСЧЁТА ПОЛОЖЕНИЯ ТОЧКИ ДЛЯ НАНЕСЕНИЯ            #
#        НА ВЫБРАННЫЙ ПЛОЩАДНОЙ ОБЪЕКТ                            #
###################################################################
#  ИМПОРТИРОВАНИЕ ФУНКЦИЙ :                                       #
#                                                                 #
#  # Загрузка библиотеки                                         #
#  HINSTANCE libInst;                                             #
#                                                                 #
#  # Вызов функции                                               #
#  int (WINAPI #GetObjectCenter)(HMAP hmap, HOBJ info, double #x, #
#                                double #y);                      #
#                                                                 #
#  (FARPROC) GetObjectCenter = mapLoadLibrary("mapmath.dll",      #
#                                          &libInst,              #
#                                          "mathGetObjectCenter");#
#                                                                 #
#  int code = (GetObjectCenter#)(hmap,info,&x,&y);                #
#    ...                                                          #
#                                                                 #
#  # Выгрузка библиотеки                                         #
#  ::FreeLibrary(libInst);                                        #
#                                                                 #
###################################################################
# Пересечение линии с площадным объектом

    mathCreateLineCross_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreateLineCross', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mathCreateLineCross(_hMap: maptype.HMAP, _inobj: maptype.HOBJ, _outinfo: maptype.HOBJ, _step: float) -> int:
        return mathCreateLineCross_t (_hMap, _inobj, _outinfo, _step)


# Интерполирование линии

    mathLineInterpolate_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathLineInterpolate', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mathLineInterpolate(_inobj: maptype.HOBJ, _outobj: maptype.HOBJ, _step: float) -> int:
        return mathLineInterpolate_t (_inobj, _outobj, _step)


# Запросить центр площадного объекта

    mathGetObjectCenter_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathGetObjectCenter', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mathGetObjectCenter(_hmap: maptype.HMAP, _info: maptype.HOBJ, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mathGetObjectCenter_t (_hmap, _info, _x, _y)


# Установить заданную длину отрезка между точками с исходными
# координатами x1,y1 и x2,y2
# delta  - новое расстояние
# number - номер редактируемой точки (1- изменяются x1 и y1, 2- x2 и y2)
# При ошибке возвращает 0

    mathSetLineLength_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetLineLength', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_int)
    def mathSetLineLength(_x1: ctypes.POINTER(ctypes.c_double), _y1: ctypes.POINTER(ctypes.c_double), _x2: ctypes.POINTER(ctypes.c_double), _y2: ctypes.POINTER(ctypes.c_double), _delta: float, _number: int) -> int:
        return mathSetLineLength_t (_x1, _y1, _x2, _y2, _delta, _number)


# Создание списка номенклатур по заданным габаритам района
# hmap - идентификатор открытых данных
# info  - заданная область расчёта номенклатур листов карты (метрика
#                                              должна быть замкнутой)
# scale - знаменатель масштаба карты (25000 - 1000000)
# listreg - адрес массива структур паспортных данных листа карты
# sheet - максимальное число номенклатур
# Возвращаемое значение: при ошибке - 0,
# при нормальном завершении заполнятся поля структуры LISTREGISTER для
# каждого листа

    mathSheetFromFrame_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSheetFromFrame', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long)
    def mathSheetFromFrame(_hmap: maptype.HMAP, _info: maptype.HOBJ, _scale: int, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheet: int) -> int:
        return mathSheetFromFrame_t (_hmap, _info, _scale, _listreg, _sheet)


# Установить имя листа
# b,l    - координаты расчёта
# comp - признак сомпановки (сдвоенные, ...)
# name - номенклатура
# При ошибке возвращает 0

    mathSetSheetName_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetSheetName', ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_char_p)
    def mathSetSheetName(_scale: int, _b: float, _l: float, _comp: int, _name: ctypes.c_char_p) -> int:
        return mathSetSheetName_t (_scale, _b, _l, _comp, _name)


# Контроль габаритов района создания номенклатур
# info  - заданная область построения листов карты
# выходные параметры:
# frame - координаты 2-х углов области построения листа
# regim - параметр учёта прохождения через осевой меридиан
#                    (0 - осевой меридиан не пересекается
#                     1 - осевой меридиан пересекается)
# При ошибке возвращает 0

    mathCheckFrame_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCheckFrame', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.FRAME), ctypes.POINTER(ctypes.c_int))
    def mathCheckFrame(_hmap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.FRAME), _regim: ctypes.POINTER(ctypes.c_int)) -> int:
        return mathCheckFrame_t (_hmap, _info, _frame, _regim)


# Заполнение полей массива структур LISTREGISTER паспортных данных
# array - адрес списка номенклатур,рассчитанных по заданной области
# listreg - адрес массива структур паспортных данных листа карты
# scale   - знаменатель масштаба (25000 - 1000000)
# countname - число рассчитанных номенклатур
# При ошибке возвращает 0

    mathSetListRegister_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetListRegister', ctypes.c_char_p, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long, ctypes.c_long)
    def mathSetListRegister(_array: ctypes.c_char_p, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _scale: int, _countname: int) -> int:
        return mathSetListRegister_t (_array, _listreg, _scale, _countname)


# Отбраковка номенклатур,не принадлежащих заданной области
# info  - заданная область построения листов карты
# listreg - адрес массива структур паспортных данных листа карты
# count   - число рассчитанных номенклатур после отбраковки
# При ошибке возвращает 0, иначе  число номенклатур после отбраковки

    mathSetBelongNomenclature_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetBelongNomenclature', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long)
    def mathSetBelongNomenclature(_hmap: maptype.HMAP, _info: maptype.HOBJ, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _count: int) -> int:
        return mathSetBelongNomenclature_t (_hmap, _info, _listreg, _count)


# Типы номенклатур
# Определить номенклатуру листа по масштабу scale и геодезическим координатам
# scale    - масштаб карты (от 1000 000 до 2000)
# b,l      - геодезические координаты точки внутри листа (в градусах)
# name     - номенклатура листа (буфер для размещения результата)
# namesize - размер буфера в байтах
# united   - признак объединенного листа: 0 - одинарные листы; 1 - сдвоенные, строенные, счетверенные
# type     - тип номенклатуры топокарт: от NOM_FIRST до NOM_LAST
# При ошибке возвращает ноль

    mathGetRuleSheetNameEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathGetRuleSheetNameEx', ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mathGetRuleSheetNameEx(_scale: int, _b: float, _l: float, _name: mapsyst.WTEXT, _namesize: int, _united: int, _type: int) -> int:
        return mathGetRuleSheetNameEx_t (_scale, _b, _l, _name.buffer(), _namesize, _united, _type)


# Определить номенклатуру листа по масштабу и геодезическим координатам
# maptype  - тип карты
# scale    - масштаб карты (от 1000 000 до 2000)
# b,l      - геодезические координаты точки внутри листа (в градусах)
# name     - номенклатура листа (буфер для размещения результата)
# namesize - размер буфера в байтах
# united   - признак объединенного листа: 0 - одинарные листы; 1 - сдвоенные, строенные, счетверенные
# При ошибке возвращает ноль

    mathGetRuleSheetNameUn_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathGetRuleSheetNameUn', ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mathGetRuleSheetNameUn(_maptype: int, _scale: int, _b: float, _l: float, _name: mapsyst.WTEXT, _namesize: int, _united: int) -> int:
        return mathGetRuleSheetNameUn_t (_maptype, _scale, _b, _l, _name.buffer(), _namesize, _united)


###################################################################
#
#                   ФУНКЦИИ ГЕНЕРАЛИЗАЦИИ
#
#  Перенос объектов с вытягиванием на рамку
#  Сшивка объектов вдоль линии сводки
#  Генерализация изолиний рельефа
#
###################################################################
# Обработка пересечений объектов карты
# Функция выполняет задачи:
# - обрезка объектов карты заданных типов по шаблону (обрезка фрагментов
#   внутри или снаружи шаблона);
# - разрезание объектов карты заданных типов по шаблону (с сохранением
#   исходного вида разрезаемых объектов, либо с назначением новых видов);
# - создание линейных объектов, определяющих совпадающие контура
#   (создание границ между площадными объектами).
#
# templet - объект-шаблон (лекало) для обрезки объектов
# count   - количество типов (кодов) обрезаемых объектов
# codes   - массив кодов обрезаемых объектов: mapGetRscObjectCodeByKey()
#           (если коды не заданы - обработать все объекты)
# parm    - параметры обработки
#
# При ошибке возвращает 0

    mathObjectCrossing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathObjectCrossing', maptype.HOBJ, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(OBJECT_CROSSING))
    def mathObjectCrossing(_templet: maptype.HOBJ, _count: int, _codes: ctypes.POINTER(ctypes.c_int), _parm: ctypes.POINTER(OBJECT_CROSSING)) -> int:
        return mathObjectCrossing_t (_templet, _count, _codes, _parm)


# Копирование объектов листа с одной карты на лист карты производного масштаба
# (используется при выполнении первого этапа генерализации карты)
#
# handle    - диалог визуального сопровождения процесса обработки.
# mapin     - исходная карта
# numberin  - номер листа, на котором расположен объект
# mapout    - выходная карта
# numberout - номер листа, на который переносится объект
# hSelect   - фильтр копируемых объектов (если 0, то копируются все объекты)
#
# Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает 0

    mathObjectCopyingEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathObjectCopyingEx', maptype.HWND, maptype.HMAP, ctypes.c_int, maptype.HMAP, ctypes.c_int, maptype.HSELECT)
    def mathObjectCopyingEx(_handle: maptype.HWND, _mapin: maptype.HMAP, _numberin: int, _mapout: maptype.HMAP, _numberout: int, _hSelect: maptype.HSELECT) -> int:
        return mathObjectCopyingEx_t (_handle, _mapin, _numberin, _mapout, _numberout, _hSelect)

    mathObjectCopying_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathObjectCopying', maptype.HWND, maptype.HMAP, ctypes.c_int, maptype.HMAP, ctypes.c_int)
    def mathObjectCopying(_handle: maptype.HWND, _mapin: maptype.HMAP, _numberin: int, _mapout: maptype.HMAP, _numberout: int) -> int:
        return mathObjectCopying_t (_handle, _mapin, _numberin, _mapout, _numberout)


# Сшивка объектов вдоль линии сводки
# handle  - диалог визуального сопровождения процесса обработки.
# map     - исходная основная карта
# sit     - исходная пользовательская карта
# number  - номер листа карты
# delta   - допуск при дотягивании (в метрах)
#
# Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает 0

    mathObjectJoining_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathObjectJoining', maptype.HWND, maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mathObjectJoining(_handle: maptype.HWND, _hmap: maptype.HMAP, _number: int, _delta: float) -> int:
        return mathObjectJoining_t (_handle, _hmap, _number, _delta)

    mathObjectJoiningEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathObjectJoiningEx', maptype.HWND, maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_double)
    def mathObjectJoiningEx(_handle: maptype.HWND, _hmap: maptype.HMAP, _hsit: maptype.HSITE, _number: int, _delta: float) -> int:
        return mathObjectJoiningEx_t (_handle, _hmap, _hsit, _number, _delta)


# Генерализация опорных пунктов (округление, огрубление)
# map     - исходная карта
# keyfile - имя INI-файла
# handle  - диалог визуального сопровождения процесса обработки.

    mathDissemble_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathDissemble', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(ROUGH), maptype.HWND)
    def mathDissemble(_map: maptype.HMAP, _keyfile: ctypes.c_char_p, _rough: ctypes.POINTER(ROUGH), _handle: maptype.HWND) -> int:
        return mathDissemble_t (_map, _keyfile, _rough, _handle)


###################################################################
#                ГЕНЕРАЛИЗАЦИЯ ИЗОЛИНИЙ РЕЛЬЕФА
###################################################################
# Сообщение о проценте выполненных работ
# Генерализация изолиний рельефа

    mathIsolineGeneralization_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathIsolineGeneralization', maptype.HMAP, ctypes.c_char_p, maptype.HWND)
    def mathIsolineGeneralization(_hmap: maptype.HMAP, _txtname: ctypes.c_char_p, _handle: maptype.HWND) -> int:
        return mathIsolineGeneralization_t (_hmap, _txtname, _handle)

    mathIsolineGeneralizationUn_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathIsolineGeneralizationUn', maptype.HMAP, maptype.PWCHAR, maptype.HWND)
    def mathIsolineGeneralizationUn(_hmap: maptype.HMAP, _txtname: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        return mathIsolineGeneralizationUn_t (_hmap, _txtname.buffer(), _handle)


# Параметры генерализации площадной гидрографии

#   GEN_HYDROGRAPHY_t = mapsyst.GetProcAddress(curLib,typedef struct,'GEN_HYDROGRAPHY')
#   def GEN_HYDROGRAPHY() -> typedef struct:
#       return GEN_HYDROGRAPHY_t ()


# Генерализация площадной гидрографии
#  parm     - параметры генерализации
#  codeset  - массив наборов кодов
#  setcount - число наборов кодов (от 1 до RIVER_KIND_MAX)

    genHydrography_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'genHydrography', ctypes.POINTER(GEN_HYDROGRAPHY), ctypes.POINTER(GEN_CODESET), ctypes.c_int)
    def genHydrography(_parm: ctypes.POINTER(GEN_HYDROGRAPHY), _codeset: ctypes.POINTER(GEN_CODESET), _setcount: int) -> int:
        return genHydrography_t (_parm, _codeset, _setcount)


# Устаревшая структура ############################################

#   GEN_SQUARERIVEREX_t = mapsyst.GetProcAddress(curLib,typedef struct,'GEN_SQUARERIVEREX')
#   def GEN_SQUARERIVEREX() -> typedef struct:
#       return GEN_SQUARERIVEREX_t ()


# (устаревшая функция)
# Генерализация площадной гидрографии
#   parm - параметры функции

    genSquareRiversEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'genSquareRiversEx', ctypes.POINTER(GEN_SQUARERIVEREX))
    def genSquareRiversEx(_parm: ctypes.POINTER(GEN_SQUARERIVEREX)) -> int:
        return genSquareRiversEx_t (_parm)


# (устаревшая функция)
# Генерализация площадной гидрографии
# parm      - общие параметры функции
# diapasons - массив параметров диапазонов

    genSquareRivers_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'genSquareRivers', ctypes.POINTER(GEN_SQUARERIVER), ctypes.POINTER(GEN_SQUARERIVER_DIAPASON))
    def genSquareRivers(_parm: ctypes.POINTER(GEN_SQUARERIVER), _diapasons: ctypes.POINTER(GEN_SQUARERIVER_DIAPASON)) -> int:
        return genSquareRivers_t (_parm, _diapasons)


# (устаревшая функция)
# Генерализация площадной реки без учета диапазонов ее ширины

    mathRiverGeneralization_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathRiverGeneralization', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(RIVERGENERALIZATION))
    def mathRiverGeneralization(_hmap: maptype.HMAP, _select: maptype.HSELECT, _parm: ctypes.POINTER(RIVERGENERALIZATION)) -> int:
        return mathRiverGeneralization_t (_hmap, _select, _parm)


# Создание системы нормальных уравнений
# size  - количество неизвестных
# isMHK - 1 - количество уравнений больше количества неизвестных
#         0 - количество уравнений равно количеству неизвестных
# Возвращает идентификатор системы уравнений
# Для каждого полученного и больше не используемого
# идентификатора необходим вызов функции mapFreeEquations()
# При ошибке возвращает ноль

    mapCreateEquations_t = mapsyst.GetProcAddress(mathlib,mathapi.HEQUATIONS,'mapCreateEquations', ctypes.c_int, ctypes.c_int)
    def mapCreateEquations(_size: int, _isMHK: int) -> mathapi.HEQUATIONS:
        return mapCreateEquations_t (_size, _isMHK)


# Освобождение идентификатора системы нормальных уравнений
# hequations - идентификатор системы уравнений

    mapFreeEquations_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeEquations', mathapi.HEQUATIONS)
    def mapFreeEquations(_hequations: mathapi.HEQUATIONS) -> ctypes.c_void_p:
        return mapFreeEquations_t (_hequations)


# Добавление уравнения в систему нормальных уравнений
# hequations - идентификатор системы уравнений
# equation   - коэффициенты уравнения
#              длина = size + 1 (коэффициенты уравнения + остаток)
# При ошибке возвращает ноль

    mapAddEquation_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapAddEquation', mathapi.HEQUATIONS, ctypes.POINTER(ctypes.c_double))
    def mapAddEquation(_hequations: mathapi.HEQUATIONS, _equation: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapAddEquation_t (_hequations, _equation)


# Решение системы уравнений
# Перед вызовом система должна быть заполнена mapAddEquation
# hequations - идентификатор системы уравнений
# При ошибке возвращает ноль

    mapSolve_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapSolve', mathapi.HEQUATIONS)
    def mapSolve(_hequations: mathapi.HEQUATIONS) -> int:
        return mapSolve_t (_hequations)


# Возвращает результат решения системы нормальных уравнений
# Перед вызовом система должна быть решена mapSolve
# hequations - идентификатор системы уравнений
# num        - номер неизвестного (от 0 до size - 1)
# value      - возвращаемое значение
# При ошибке возвращает ноль

    mapGetResult_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapGetResult', mathapi.HEQUATIONS, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetResult(_hequations: mathapi.HEQUATIONS, _num: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetResult_t (_hequations, _num, _value)


# Создание класса трансформирования координат
# count - количество точек для расчета параметров трансформирования
#   В зависимости от типа трансформирования:
#    LT_OFFSET                             - минимальное количество точек = 1
#    LT_OFFSETROTATE, LT_OFFSETROTATESCALE - минимальное количество точек = 2
#    LT_AFFINE                             - минимальное количество точек = 3
# pointsin   - координаты точек в исходной системе координат
# pointsout  - координаты точек в выходной системе координат
# transftype - тип линейного трансформирования
#   LT_OFFSET - преобразование сдвиг
#       X = x0 + x
#       Y = y0 + y
#   LT_OFFSETROTATE - преобразование сдвиг, поворот
#       X = x0 + x # cos - y # sin
#       Y = y0 + x # sin + y # cos
#   LT_OFFSETROTATESCALE - преобразование масштаб, сдвиг, поворот
#       X = x0 + x # cos # m - y # sin # m
#       Y = y0 + x # sin # m + y # cos # m
#   LT_AFFINE - аффинное трансформирование (полином 1 степени)
#       X = a + x # b + y # c
#       Y = d + x # e + y # f
# Возвращает идентификатор класса трансформирования координат
# Для каждого полученного и больше не используемого идентификатора
# необходим вызов функции mapFreeTransform()
# При ошибке возвращает ноль

    mapCreateTransform_t = mapsyst.GetProcAddress(mathlib,mathapi.HTRANSF,'mapCreateTransform', ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapCreateTransform(_count: int, _pointsin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointsout: ctypes.POINTER(maptype.DOUBLEPOINT), _transftype: int) -> mathapi.HTRANSF:
        return mapCreateTransform_t (_count, _pointsin, _pointsout, _transftype)


# Освобождение класса трансформирования координат
# htransf - идентификатор класса трансформирования координат

    mapFreeTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeTransform', mathapi.HTRANSF)
    def mapFreeTransform(_htransf: mathapi.HTRANSF) -> ctypes.c_void_p:
        return mapFreeTransform_t (_htransf)


# Трансформирование координат из исходной системы координат в выходную
# htransf  - идентификатор класса трансформирования координат
# xin, yin   - координаты в исходной системе координат
# xout, yout - вычисленные координаты в выходной системе координат
# При ошибке возвращает ноль

    mapTransformIn2Out_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapTransformIn2Out', mathapi.HTRANSF, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapTransformIn2Out(_htransf: mathapi.HTRANSF, _xin: float, _yin: float, _xout: ctypes.POINTER(ctypes.c_double), _yout: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapTransformIn2Out_t (_htransf, _xin, _yin, _xout, _yout)


# Трансформирование координат из выходной системы координат в исходную
# htransf  - идентификатор класса трансформирования координат
# xout, yout - координаты в выходной системе координат
# xin, yin   - вычисленные координаты в исходной системе координат
# При ошибке возвращает ноль

    mapTransformOut2In_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapTransformOut2In', mathapi.HTRANSF, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapTransformOut2In(_htransf: mathapi.HTRANSF, _xout: float, _yout: float, _xin: ctypes.POINTER(ctypes.c_double), _yin: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapTransformOut2In_t (_htransf, _xout, _yout, _xin, _yin)


# Возвращает вычисленные параметры траснформирования
# htransf  - идентификатор класса трансформирования координат
# При ошибке возвращает ноль

    mapGetTransformParam_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapGetTransformParam', mathapi.HTRANSF, ctypes.POINTER(LINEARTRANSFPARM))
    def mapGetTransformParam(_htransf: mathapi.HTRANSF, _parm: ctypes.POINTER(LINEARTRANSFPARM)) -> int:
        return mapGetTransformParam_t (_htransf, _parm)


# Создание класса нелинейного трансформирования координат
# count     - количество точек для расчета параметров трансформирования
#   В зависимости от типа трансформирования:
#   NT_LINEARSHEET, NT_NONLINEARSHEET - минимальное количество точек = 3
#   NT_POLYNOM                        - минимальное количество точек = количеству коэффициентов
#   NT_POLYNOMRANK2                   - минимальное количество точек = 6
#   NT_POLYNOMRANK3                   - минимальное количество точек = 10
#   NT_POLYNOMRANK4                   - минимальное количество точек = 15
#   NT_POLYNOMRANK5                   - минимальное количество точек = 21
# pointsin  - координаты точек в исходной системе координат
# pointsout - координаты точек в выходной системе координат
# interestframe - область интереса, т.е. прямоугольник, ограничивающий область
#   применения функции mapNonlineTransformIn2Out.
#   Если = 0, то экстраполяция искажений вне области расположения опорных точек
#   не выполняется, в этом случае virtualpointcount должно быть равно 0
# virtualpointcount - количество виртуальных точек, добавляемых по границе
#   области интереса. Минимальное количество = 4. Если interestframe = 0, то
#   virtualpointcount должно быть равно 0.
# transftype - тип нелинейного трансформирования см. NONLINEARTRANSFTYPE
# Возвращает идентификатор класса нелинейного трансформирования координат
# Для каждого полученного и больше не используемого идентификатора
# необходим вызов функции mapFreeNonlineTransform()
# При ошибке возвращает ноль

    mapCreateNonlineTransform_t = mapsyst.GetProcAddress(mathlib,mathapi.HNONLINETRANSF,'mapCreateNonlineTransform', ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int)
    def mapCreateNonlineTransform(_count: int, _pointsin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointsout: ctypes.POINTER(maptype.DOUBLEPOINT), _interestframe: ctypes.POINTER(maptype.DFRAME), _virtualpointcount: int, _transftype: int) -> mathapi.HNONLINETRANSF:
        return mapCreateNonlineTransform_t (_count, _pointsin, _pointsout, _interestframe, _virtualpointcount, _transftype)


# Освобождение класса нелинейного трансформирования координат
# htransf - идентификатор класса трансформирования координат

    mapFreeNonlineTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeNonlineTransform', mathapi.HNONLINETRANSF)
    def mapFreeNonlineTransform(_htransf: mathapi.HNONLINETRANSF) -> ctypes.c_void_p:
        return mapFreeNonlineTransform_t (_htransf)


# Нелинейное трансформирование координат из исходной системы координат в выходную
# htransf  - идентификатор класса трансформирования координат
# xin, yin   - координаты в исходной системе координат
# xout, yout - вычисленные координаты в выходной системе координат
# При ошибке возвращает ноль

    mapNonlineTransformIn2Out_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapNonlineTransformIn2Out', mathapi.HNONLINETRANSF, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapNonlineTransformIn2Out(_htransf: mathapi.HNONLINETRANSF, _xin: float, _yin: float, _xout: ctypes.POINTER(ctypes.c_double), _yout: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapNonlineTransformIn2Out_t (_htransf, _xin, _yin, _xout, _yout)


# Возвращает координаты виртуальных точек
# Возвращает количество виртуальных точек, если возвращает 0, то виртуальных точек нет
# В virtualpointsin возвращается указатель на массив виртуальных точек в исходной СК
# В virtualpointsout возвращается указатель на массив виртуальных точек в выходной СК

    mapNonlineTransformGetVirtualPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapNonlineTransformGetVirtualPoints', mathapi.HNONLINETRANSF, ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)), ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)))
    def mapNonlineTransformGetVirtualPoints(_htransf: mathapi.HNONLINETRANSF, _virtualpointsin: ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)), _virtualpointsout: ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT))) -> int:
        return mapNonlineTransformGetVirtualPoints_t (_htransf, _virtualpointsin, _virtualpointsout)


# Вычисление датума
# pointcount - количество точек
# points     - геодезические координаты точек на эллипсоиде ellipsoid
#              b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
# wgspoints  - геодезические координаты точек на WGS84
#              b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
# ellipsoid  - эллипсоид, для которого вычисляется датум
# datum      - вычисленный датум
# При ошибке возвращает 0

    mapCalculateDatum_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapCalculateDatum', ctypes.c_int, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapCalculateDatum(_pointcount: int, _points: ctypes.POINTER(maptype.XYHDOUBLE), _wgspoints: ctypes.POINTER(maptype.XYHDOUBLE), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapCalculateDatum_t (_pointcount, _points, _wgspoints, _ellipsoid, _datum)


# Вычисление датума
# iscalcoffset - признак вычисления линейных коэффициентов смещения
# iscalcrotate - признак вычисления угловых коэффициентов вращения
# iscalcscale  - признак вычисления масштабного коэффициента
# pointcount   - количество точек
# points       - геодезические координаты точек на эллипсоиде ellipsoid
#                b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
# wgspoints    - геодезические координаты точек на WGS84
#                b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
# ellipsoid    - эллипсоид СК, для которой вычисляется датум
# datum        - вычисленный датум
# При ошибке возвращает 0

    mapCalculateDatumEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapCalculateDatumEx', ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapCalculateDatumEx(_iscalcoffset: int, _iscalcrotate: int, _iscalcscale: int, _pointcount: int, _points: ctypes.POINTER(maptype.XYHDOUBLE), _wgspoints: ctypes.POINTER(maptype.XYHDOUBLE), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapCalculateDatumEx_t (_iscalcoffset, _iscalcrotate, _iscalcscale, _pointcount, _points, _wgspoints, _ellipsoid, _datum)


# Вычисление параметров местной системы координат по набору точек
# (проекция Transverse Mercator + поворот)
# вычисляются : - масштаб на осевом меридиане
#               - долгота осевого меридиана
#               - широта точки отсчета
#               - поправка по Х
#               - поправка по Y
#               - угол поворота местной системы координат
# pointcount - количество точек
# points     - геодезические координаты точек
#              b, l - широта (радианы), долгота (радианы)
# points     - прямоугольные координаты точек в местной системе координат
#              система координат левая, координаты в метрах
# ellipsoid  - используемый эллипсоид
# parm       - вычисляемые параметры проекции (см. mathapi.h)
# При ошибке возвращает 0

    mapCalculateTransverseMercatorParam_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapCalculateTransverseMercatorParam', ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(CALCTRANSMERCATORPARM))
    def mapCalculateTransverseMercatorParam(_pointcount: int, _blpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _xypoints: ctypes.POINTER(maptype.DOUBLEPOINT), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(CALCTRANSMERCATORPARM)) -> int:
        return mapCalculateTransverseMercatorParam_t (_pointcount, _blpoints, _xypoints, _ellipsoid, _parm)


#---------------------------------------------------------------------------
# Преобразование Фурье (дискретное быстрое + модификация для произвольного count)
#---------------------------------------------------------------------------
# x - массив комплексных чисел
#   Для прямого преобразования Фурье
#   - на входе  - массив измерений
#                Обычно измерения являются действительными числами, в этом случае
#                значение измерения заносится в x.re, в x.im заносится 0
#   - на выходе - массив гармоник (комплексное число)
#     Частота гармоники V = i / T, где i - номер гармоники (от 1, в 0 среднее значение # count)
#                                      T - СУММАРНОЕ время измерения
#     Амплитуда гармоники A = sqrt(x[i].re^2 + x[i].im^2) / count
#     Фаза гармоники      F = atan2(x[i].im, x[i].re)
#   Для обратного преобразования Фурье
#   - на входе  - массив гармоник (комплексное число)
#                Обычно измерения являются действительными числами, в этом случае
#                значение измерения заносится в x.re, в x.im заносится 0
#   - на выходе - массив измерений (брать действительную часть)
# count - размер массива x
# isdirect = 1 - прямое преобразование Фурье
#          = 0 - обратное преобразование Фурье
# График спектра симметричен относительно центра графика, поэтому обычно
# график рисуют для 1 <= i < count / 2, в этом случае амплитуду умножают на 2
# При ошибке возвращает 0

    mapFourierTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mapFourierTransform', ctypes.POINTER(COMPLEX), ctypes.c_int, ctypes.c_int)
    def mapFourierTransform(_x: ctypes.POINTER(COMPLEX), _count: int, _isdirect: int) -> int:
        return mapFourierTransform_t (_x, _count, _isdirect)


# Обработка карты
# Перечень обрабатываемых процессов:
# - уточнение рамки листа;
# - ориентирование векторных знаков вдоль линейных (могут быть и площадные);
# - заполнение семантики "Расстояние до ближайшего объекта".
#
# handle    - диалог визуального сопровождения процесса обработки.
# hMap      - исходная основная карта
# hSite     - исходная пользовательская карта
# xmlPath   - xml-файл с параметрами обработки объектов
# Для обработки всей карты необходимо hSite = 0
#
# Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBARUN) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBARUN, то процесс завершается.
# При ошибке возвращает 0

    mathMapProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathMapProcessing', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mathMapProcessing(_handle: maptype.HMESSAGE, _hMap: maptype.HMAP, _hSite: maptype.HSITE, _xmlPath: mapsyst.WTEXT) -> int:
        return mathMapProcessing_t (_handle, _hMap, _hSite, _xmlPath.buffer())


# Запрос количества процессов в xml-файле
# xmlPath   - xml-файл с параметрами обработки объектов
# вызывается перед задачей mathMapProcessing
# При ошибке возвращает 0

    mathCountProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCountProcessing', maptype.PWCHAR)
    def mathCountProcessing(_xmlPath: mapsyst.WTEXT) -> int:
        return mathCountProcessing_t (_xmlPath.buffer())


# Запрос метода обработки генерализированных объектов

    mathGetObjectProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathGetObjectProcessing')
    def mathGetObjectProcessing() -> int:
        return mathGetObjectProcessing_t ()


# Установка метода обработки генерализированных объектов
# 0 - добавление в объект семантики SEMIMAGECOLOR
# 1 - удаление объекта

    mathSetObjectProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetObjectProcessing', ctypes.c_int)
    def mathSetObjectProcessing(_process_flag: int) -> int:
        return mathSetObjectProcessing_t (_process_flag)


# Уточнение восточных и западных рамок листов в соответствии с
# реальными габаритами объектов в листе (при несоответствии более чем на 10")
# handle    - диалог визуального сопровождения процесса обработки.
# hmap      - обрабатываемая карта
#
# Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBARUN) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBARUN, то процесс завершается.
# При ошибке возвращает 0

    mathSetMapRealBorder_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetMapRealBorder', maptype.HMESSAGE, maptype.HMAP)
    def mathSetMapRealBorder(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP) -> int:
        return mathSetMapRealBorder_t (_handle, _hmap)


# Создание проездов между кварталами
# handle  - идентификатор окна (для посылки сообщений о выполнении WM_PROGRESSBARUN)
#           LPARAM >= 0  - процент выполнения
#           WPARAM = -1  - комментарий (имя текущего процесса)
# map     - доступ к данным
# ininame - имя файла параметров (IST)
# code    - поле для возврата кода ошибки
# При ошибке возвращает 0

    mathCreatePassagesBetweenQuarters_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreatePassagesBetweenQuarters', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mathCreatePassagesBetweenQuarters(_handle: maptype.HMESSAGE, _map: maptype.HMAP, _ininame: mapsyst.WTEXT, _code: ctypes.POINTER(ctypes.c_int)) -> int:
        return mathCreatePassagesBetweenQuarters_t (_handle, _map, _ininame.buffer(), _code)


# Построение тематических картограмм
# sitename   - имя файла выходной карты (или 0)
# legendname - имя файла карты легенды (может совпадать с sitename,
#              0 - не создавать легенду)
# options    - параметры построения тематических картограмм
# values     - массив описаний диапазона (количество диапазонов ItemsCount указано в THEMATICPARM).
#              0 - если для файлов CSV указано поле с цветом (THEMDIALOGPARM::NumberColorField)
# objvalue   - массив описаний объектов
# objcount   - количество описаний объектов
# Возвращает количество построенных картограмм

    mathCreateThematicMap_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreateThematicMap', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(THEMATICPARM), ctypes.POINTER(RANGEITEM), ctypes.POINTER(OBJVALUE), ctypes.c_int)
    def mathCreateThematicMap(_sitename: mapsyst.WTEXT, _legendname: mapsyst.WTEXT, _options: ctypes.POINTER(THEMATICPARM), _values: ctypes.POINTER(RANGEITEM), _objvalue: ctypes.POINTER(OBJVALUE), _objcount: int) -> int:
        return mathCreateThematicMap_t (_sitename.buffer(), _legendname.buffer(), _options, _values, _objvalue, _objcount)


# Заполнение массива OBJVALUE для построения тематических картограмм
# (вызывать перед функцией mathCreateThematicMap в режимах построения
#  "раскраска по значениям семантики": THEMATICPARM::ConnectType = 0,1,2)
# filename   - имя файла таблицы (dbf, csv, txt)
# options    - параметры построения тематических картограмм
# paramdlg   - параметры из диалога построения тематических картограмм
# objvalue   - массив описаний объектов
# objcount   - количество описаний объектов
# Возвращает количество найденных объектов карты, соответствующих условиям отбора

    mathSetThematicData_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathSetThematicData', maptype.PWCHAR, ctypes.POINTER(THEMATICPARM), ctypes.POINTER(THEMDIALOGPARM), ctypes.POINTER(OBJVALUE), ctypes.c_int)
    def mathSetThematicData(_filename: mapsyst.WTEXT, _options: ctypes.POINTER(THEMATICPARM), _paramdlg: ctypes.POINTER(THEMDIALOGPARM), _objvalue: ctypes.POINTER(OBJVALUE), _objcount: int) -> int:
        return mathSetThematicData_t (_filename.buffer(), _options, _paramdlg, _objvalue, _objcount)


# Создать выпуклый полигон по точкам
# list  - указатель на список точек
# count - количество точек в списке
# info  - выходной объект, созданный по точкам из массива list
# Выходной объект должен быть создан заранее, внутри функции удаляется
# старая метрика и заполняется новая
# При ошибке функция возвращает 0

    mathCreateConvexPolygonByPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreateConvexPolygonByPoints', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, maptype.HOBJ)
    def mathCreateConvexPolygonByPoints(_list: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _info: maptype.HOBJ) -> int:
        return mathCreateConvexPolygonByPoints_t (_list, _count, _info)


# Создать звездчатый полигон по точкам
# list  - указатель на список точек
# count - количество точек в списке
# info  - выходной объект, созданный по точкам из массива list
# Выходной объект должен быть создан заранее, внутри функции удаляется
# старая метрика и заполняется новая
# При ошибке функция возвращает 0

    mathCreateStarPolygonByPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreateStarPolygonByPoints', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, maptype.HOBJ)
    def mathCreateStarPolygonByPoints(_list: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _info: maptype.HOBJ) -> int:
        return mathCreateStarPolygonByPoints_t (_list, _count, _info)


#------------------------------------------------------------------
# ПАРАМЕТРЫ ФУНКЦИИ УРАВНИВАНИЯ ТЕОДОЛИТНОГО ХОДА
#------------------------------------------------------------------

#   TEO_PARAM_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEO_PARAM')
#   def TEO_PARAM() -> typedef struct:
#       return TEO_PARAM_t ()


# Уравнивание теодолитного хода
# inputName  - имя исходного файла CSV с измерениями, колонки разделены символом ";"
#   первая строка исходного файла - заголовок таблицы, названия колонок:
#   ST_NAME - название точки (станции)
#   X       - координата X
#   Y       - координата Y
#   HOR     - горизотальный угол в фоормате: GGG MM SS.S
#   DIR     - дирекционный угол в фоормате:  GGG MM SS.S
#   DIST    - горизонтальное проложение (в м.)
# outputName - имя файла CSV с результатами уравнивания
# param      - параметры обработки
# При ошибке функция возвращает 0

    mathTheoAdjusting_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathTheoAdjusting', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(TEO_PARAM))
    def mathTheoAdjusting(_inputName: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _param: ctypes.POINTER(TEO_PARAM)) -> int:
        return mathTheoAdjusting_t (_inputName.buffer(), _outputname.buffer(), _param)


# Приведение объекта к прямоугольному виду
# info   - идентификатор объекта
# filter - уровень фильтрации объекта в метрах на местности
# mode   - режим проверки корректности преобразования
#        0 - проверять всегда
#        1 - проверять только при условии, что разница площадей меньше 10%
# pointnumber - номер точки объекта/подобъекта
# subject     - номер подобъекта
# Код возврата:
#             0 - ошибка
#             1 - объект преобразован
#            -1 - объект не преобразован

    mathMakeRectangleObject_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathMakeRectangleObject', maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mathMakeRectangleObject(_info: maptype.HOBJ, _filter: float, _mode: int = 0, _pointnumber: int = 0, _subject: int = 0) -> int:
        return mathMakeRectangleObject_t (_info, _filter, _mode, _pointnumber, _subject)


# Построение тематических диаграмм
# options       - общие параметры построения диаграммы
# sizeparam     - параметры для определения размера диаграммы
# semanticparam - список характеристик для построения диаграмм
# count         - число элементов списка характеристик
# Возвращает количество построенных диаграмм

    mathCreateDiagram_t = mapsyst.GetProcAddress(mathlib,ctypes.c_int,'mathCreateDiagram', ctypes.POINTER(DIAOPTIONS), ctypes.POINTER(SIZEPARAM), ctypes.POINTER(SEMANTICPARAM), ctypes.c_int)
    def mathCreateDiagram(_options: ctypes.POINTER(DIAOPTIONS), _sizeparam: ctypes.POINTER(SIZEPARAM), _semanticparam: ctypes.POINTER(SEMANTICPARAM), _count: int) -> int:
        return mathCreateDiagram_t (_options, _sizeparam, _semanticparam, _count)

except Exception as e:
    print(e)
    mathlib = 0
