#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mapcreat
import mmstruct
import vecexapi
import maptype

HAICM     = ctypes.c_void_p
HARINC    = ctypes.c_void_p
HAIXM     = ctypes.c_void_p
HSHPLOAD  = ctypes.c_void_p
HMIFTOMAP = ctypes.c_void_p

PACK_WIDTH = 1

#-----------------------------
class PROCESSPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [
                                              # Обязательные параметры отмечены звездочками (***)
    ("Map"              , maptype.HMAP    ),  # *** Идентификатор открытых данных
    
    ("Map2"             , maptype.HMAP    ),  # Идентификатор открытых данных для записи результата
                                              # - если Map2 = 0, то Map2 = Map
    ("Map3"             , maptype.HMAP    ),  # Идентификатор открытых данных для записи неисправленных объектов
                                              # - если Map3 = 0, то Map3 = Map
                                              
    ("Site"             , maptype.HSITE   ),  # Исходная карта
                                              # - если Site = 0, то Site = Map
    ("Site2"            , maptype.HSITE   ),  # Новая карта для записи обработанных объектов
                                              # - если Site2 = 0, то Site2 = Map2
    ("Site3"            , maptype.HSITE   ),  # Карта ошибочных объектов (для записи неисправленных объектов)
                                              # - если Site3 = 0, то Site3 = Map3
                                              
    # Если Site2 = Site и Map2 = Map - обработанные объекты записываются в ИСХОДНУЮ карту,
    #                          иначе - в НОВУЮ карту (Map2, Site2) с нарезкой на листы
    # Если Site3 = Site и Map3 = Map - ошибочные объекты записываются в ИСХОДНУЮ карту,
    #                          иначе - в карту ОШИБОЧНЫХ объектов (Map3, Site3)
    
    ("Select"           , maptype.HSELECT ),  # Состав обрабатываемых объектов (пока не используется)
    ("Handle"           , maptype.HMESSAGE),  # Идентификатор окна сопровождения процесса обработки
                                              # - если Handle != 0, то функция cntCorrection() посылает сообщение
                                              #   WM_PROGRESSBARUN с текущим процентом выполнения (WPARAM от 0 до 100)
                                              #   и строку "Коррекция метрики объектов. Исправлено ошибок: XXX" (LPARAM)
    
    ("Free"             , ctypes.c_double  ), # Резерв (не используется)
    ("Precision"        , ctypes.c_double  ), # Точность (в метрах на местности), используемая для проверки равенства точек
    ("SheetNumber"      , ctypes.c_int     ), # Номер листа обрабатываемой карты (от 1)
                                              # (при обработке одного объекта игнорируеся)
    ("MultiPolygon"     , ctypes.c_int     ), # Формировать мультиполигон
    
    ("DoNotMatchPoints" , ctypes.c_char    ), # Не согласовывать точки эталонного объекта с точками редактируемого
    ("DoNotCheckObject1", ctypes.c_char    ), # Не проверять эталонный объект (1)
    ("DoNotCheckObject2", ctypes.c_char    ), # Не проверять редактируемый объект (2)
    ("DoNotCheckCross"  , ctypes.c_char    ), # Не выполнять предварительную проврку пересечения (уже проверено)
    ("Zero"             , ctypes.c_char*4  ),
    
    ("Status"           , ctypes.c_int     ), # Содержит состояние обработки (при выходе из функции), см. PROCESSING_STATUS
    ("Error"            , ctypes.c_int     ), # Содержит код ошибки (при выходе из функции): от OVL_ERR_NONE до OVL_ERR_END
                                              # -1 - ошибка обработки
    ("Reserve"          , ctypes.c_int*14  )  # Резерв (не используется)
    ]

#-----------------------------
class SETTING(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("IsUpdate",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("Charset",ctypes.c_int),
                ("Isdirect",ctypes.c_int),
                ("Isdivision",ctypes.c_int),
                ("Isosm",ctypes.c_int),
                ("IsBL",ctypes.c_int),
                ("IsSorted",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("IsFolder",ctypes.c_int),
                ("MapType",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("NumberField",maptype.WCHAR1*(16*2)),
                ("LabelField",maptype.WCHAR1*(16*2)),
                ("AngleField",maptype.WCHAR1*(16*2)),
                ("CodeField",maptype.WCHAR1*(16*2)),
                ("RscName",maptype.WCHAR1*(maptype.MAX_PATH*2)),
                ("Prefix",maptype.WCHAR1*(256*2)),
                ("Postfix",maptype.WCHAR1*(256*2))]
#-----------------------------


#-----------------------------
class RECORDLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DbfField",maptype.WCHAR1*(16*2)),
                ("FieldName",maptype.WCHAR1*(256*2)),
                ("FieldKey",maptype.WCHAR1*(256*2)),
                ("LayerName",maptype.WCHAR1*(256*2)),
                ("ObjectCode",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SEMFIELDS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("name",maptype.WCHAR1*(1024*2)),
                ("code",ctypes.c_int),
                ("zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RECORDHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Number",ctypes.c_int),
                ("Length",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MAPTOSHPPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hMap",maptype.HMAP),
                ("hSite",maptype.HSITE),
                ("hSelect",maptype.HSELECT),
                ("DBCode",ctypes.c_int),
                ("Isbl",ctypes.c_int),
                ("IsService",ctypes.c_int),
                ("IsDecode",ctypes.c_int),
                ("IsFolder",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class COLUMNS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*128),
                ("Format",ctypes.c_char*16),
                ("Code",ctypes.c_int),
                ("Zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SEMCOLUMNS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*128),
                ("ClsKey",ctypes.c_char*128)]
#-----------------------------


#-----------------------------
class DXF2MAPPARMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Scale",ctypes.c_int),
                ("Image",ctypes.c_int),
                ("fSemantic",ctypes.c_int),
                ("Unit",ctypes.c_int),
                ("fLayerName",ctypes.c_int),
                ("fMapAppend",ctypes.c_int),
                ("fBaseType",ctypes.c_int),
                ("f3DMetric",ctypes.c_int),
                ("fXAxis",ctypes.c_int),
                ("fGraphic",ctypes.c_int)]
#-----------------------------


#-----------------------------
class PARMDXF(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ImageType",ctypes.c_int),
                ("Semantic",ctypes.c_int),
                ("LayerType",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("Unicode",ctypes.c_int),
                ("RGBColor",ctypes.c_int),
                ("LineType",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TXTTRANSLATEPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("InHuser",ctypes.c_void_p),
                ("OutHuser",ctypes.c_void_p),
                ("InDelimiter",ctypes.c_char),
                ("OutDelimiter",ctypes.c_char),
                ("InUnit",ctypes.c_char),
                ("OutUnit",ctypes.c_char),
                ("InFormat",ctypes.c_char),
                ("OutFormat",ctypes.c_char),
                ("IsSaveH",ctypes.c_char),
                ("Reserve",ctypes.c_char*9)]
#-----------------------------


try:
    if os.environ['gisvecexdll']:
        gisvecexname = os.environ['gisvecexdll']
except KeyError:
    gisvecexname = 'gis64vecex.dll' 

try:
    vecexlib = mapsyst.LoadLibrary( gisvecexname )


# Исправить объект
#   obj  - обрабатывемый объект
#   parm - параметры обработки
# Если Site2 = Site и Map2 = Map - обработанные объекты записываются в ИСХОДНУЮ карту,
#                          иначе - в НОВУЮ карту (Map2, Site2) с нарезкой на листы
# Если Site3 = Site и Map3 = Map - ошибочные объекты записываются в ИСХОДНУЮ карту,
#                          иначе - в карту ОШИБОЧНЫХ объектов (Map3, Site3)
# При обработке линейного объекта выполняется:
#   1) удаление двойных точек в указанном допуске (parm.Precision);
#   2) преобразование мультилиний в простые линейные (с добавлением новых объектов);
#   3) разрезание контуров в точках примыкания (с добавлением новых объектов);
#   4) удаление выбросов;
#   5) удаление начальных и конечных совпадающих отрезков.
# При обработке площадного объекта выполняется:
#   1) удаление двойных точек в указанном допуске (parm.Precision);
#   2) удаление выбросов;
#   3) смещение точек близких и примыкающих отрезков;
#   4) разрезание контуров в точках примыкания и самопересечения (с добавлением новых подобъектов);
#   5) преобразование мультиполигонов в простые площадные объекты (с добавлением новых объектов).
# Состояние обработки записывается в поле parm->Status (см. PROCESSING_STATUS)
# Код ошибки записывается в поле parm->Error: от OVL_ERR_NONE до OVL_ERR_END
# Если объект обновлен на своей карте, то возвращает -1
# При ошибке возвращает 0

    cntCorrectTheObject_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'cntCorrectTheObject',maptype.HOBJ,ctypes.POINTER(PROCESSPARM))
    def cntCorrectTheObject(_hObj: maptype.HOBJ, _param: ctypes.POINTER(PROCESSPARM) ) -> int:
        return cntCorrectTheObject_t(_hObj,_param)

# Трансформирование векторной карты
# hmap        - идентификатор открытых данных
# hsite       - идентификатор открытой пользовательской карты
# outname     - полный путь к паспорту трансформированной карты
#               или путь к папке для размещения карты с тем же именем
# newname     - имя созданной карты
# newnamesize - размер буфера для newname в байтах
# mapregparm, datumparm, ellipsparm - параметры системы координат,
#               в которую трансформируется исходная карта
# ttypeparm, tparm - параметры локального преобразования координат
# handle      - идентификатор окна диалога процесса обработки (HWND для Windows)
#               Окну диалога посылаются следующие сообщения :
#   WM_OBJECT = 0x585   WPARAM - процент обработанных данных, LPARAM - число обработанных листов
#   WM_ERROR  = 0x587   - сообщение об ошибке для увеличения счетчика ошибок
# hevent      - адрес функции обратного вызова для получения процента выполнения задачи
# eventparam  - первый параметр функции обратного вызова
# error       - поле для записи кода ошибки выполнения функции
# При ошибке возвращает ноль

    vecModifyMapEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecModifyMapEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.HMESSAGE, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int))
    def vecModifyMapEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _newnamesize: int, _mapregparm: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttypeparm: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _handle: maptype.HMESSAGE, _hevent: maptype.EVENTSTATE, _eventparm: ctypes.POINTER(ctypes.c_void_p), _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecModifyMapEx_t (_hmap, _hsite, _outname.buffer(), _newname.buffer(), _newnamesize, _mapregparm, _datumparm, _ellipsparm, _ttypeparm, _tparm, _handle, _hevent, _eventparm, _error)

    vecModifyMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecModifyMap', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.HMESSAGE, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int))
    def vecModifyMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _mapregparm: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttypeparm: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _handle: maptype.HMESSAGE, _hevent: maptype.EVENTSTATE, _eventparm: ctypes.POINTER(ctypes.c_void_p), _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecModifyMap_t (_hmap, _hsite, _outname.buffer(), _mapregparm, _datumparm, _ellipsparm, _ttypeparm, _tparm, _handle, _hevent, _eventparm, _error)


# Запросить паспортные данные из файлов SXF, TXF, MAP, SIT, SITX
# по имени файла
# name - имя файла карты в одном из вышеперечисленных форматов
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# rscname - адрес буфера для записи имени классификатора (может быть 0)
# rsize - длина буфера в байтах
# sheetname - адрес буфера для записи длинного имени карты (может быть 0)
# ssize - длина буфера в байтах
# securitycode - адрес поля для записи кода степени секретности (может быть 0)
# ( 0 - не установлено, 1 - открытая информация (unclassified),
# 2 - информация с ограниченным доступом (restricted),
# 3 - информация для служебного пользования (confidential),
# 4 - секретная информация (secret), 5 - совершенно секретная информация (topsecret))
# Возвращает число объектов в карте, если число объектов равно 0, то возвращает -1
# При ошибке возвращает ноль

    mapGetAnySxfInfoMeta_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetAnySxfInfoMeta', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.METAINFO))
    def mapGetAnySxfInfoMeta(_name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _metainfo: ctypes.POINTER(mapcreat.METAINFO)) -> int:
        return mapGetAnySxfInfoMeta_t (_name.buffer(), _mapreg, _sheet, _metainfo)

    mapGetAnySxfInfoByNamePro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetAnySxfInfoByNamePro', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetAnySxfInfoByNamePro(_name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _rscname: mapsyst.WTEXT, _rsize: int, _sheetname: mapsyst.WTEXT, _ssize: int, _securitycode: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetAnySxfInfoByNamePro_t (_name.buffer(), _mapreg, _sheet, _rscname.buffer(), _rsize, _sheetname.buffer(), _ssize, _securitycode)

    mapGetAnySxfInfoByNameUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetAnySxfInfoByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapGetAnySxfInfoByNameUn(_name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapGetAnySxfInfoByNameUn_t (_name.buffer(), _mapreg, _sheet)

    mapGetAnySxfInfoByName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetAnySxfInfoByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapGetAnySxfInfoByName(_name: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapGetAnySxfInfoByName_t (_name, _mapreg, _sheet)


# Запросить имя классификатора (RSC) из файлов SXF, TXF, MAP (SIT)
# В файлах SXF и TXF имя классификатора (RSC) может отсутствовать
# rscname - адрес буфера для записи имени классификатора
# size - длина буфера в байтах
# При ошибке возвращает ноль

    GetRscNameFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetRscNameFromAnySxfUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def GetRscNameFromAnySxfUn(_name: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return GetRscNameFromAnySxfUn_t (_name.buffer(), _rscname.buffer(), _size)

    GetRscNameFromAnySxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetRscNameFromAnySxf', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def GetRscNameFromAnySxf(_name: ctypes.c_char_p, _rscname: ctypes.c_char_p, _size: int) -> int:
        return GetRscNameFromAnySxf_t (_name, _rscname, _size)

    GetRscNameFromSxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetRscNameFromSxfUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def GetRscNameFromSxfUn(_name: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return GetRscNameFromSxfUn_t (_name.buffer(), _rscname.buffer(), _size)

    GetRscNameFromSxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetRscNameFromSxf', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def GetRscNameFromSxf(_name: ctypes.c_char_p, _rscname: ctypes.c_char_p, _size: int) -> int:
        return GetRscNameFromSxf_t (_name, _rscname, _size)


# Запросить имя карты из файлов SXF, TXF, MAP (SIT)
# При ошибке возвращает ноль

    GetSheetNameFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetSheetNameFromAnySxfUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def GetSheetNameFromAnySxfUn(_name: mapsyst.WTEXT, _sheetname: mapsyst.WTEXT, _size: int) -> int:
        return GetSheetNameFromAnySxfUn_t (_name.buffer(), _sheetname.buffer(), _size)

    GetSheetNameFromAnySxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetSheetNameFromAnySxf', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def GetSheetNameFromAnySxf(_filename: ctypes.c_char_p, _sheetname: ctypes.c_char_p, _size: int) -> int:
        return GetSheetNameFromAnySxf_t (_filename, _sheetname, _size)


# Запросить контрольную сумму файла SXF
# name - имя файла SXF
# При ошибке возвращает ноль и выдает сообщение на экран
# Ноль - допустимое значение контрольной суммы

    GetSxfCheckSumUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetSxfCheckSumUn', maptype.PWCHAR)
    def GetSxfCheckSumUn(_name: mapsyst.WTEXT) -> int:
        return GetSxfCheckSumUn_t (_name.buffer())

    GetSxfCheckSum_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetSxfCheckSum', ctypes.c_char_p)
    def GetSxfCheckSum(_name: ctypes.c_char_p) -> int:
        return GetSxfCheckSum_t (_name)


# Проверить контрольную сумму файла SXF
# name - имя файла SXF
# При успешной проверке возвращает 1
# При несовпадении контрольной суммы возвращает -1
# При ошибке структуры файла возвращает -2
# При устаревшей версии структуры файла возвращает -3
# При ошибке доступа к данным возвращает ноль и выдает сообщение на экран (если выдача сообщений разрешена)

    SxfCheckSumUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SxfCheckSumUn', maptype.PWCHAR)
    def SxfCheckSumUn(_name: mapsyst.WTEXT) -> int:
        return SxfCheckSumUn_t (_name.buffer())


# Проверить контрольную сумму и корректность параметров системы координат файла SXF
# name - имя файла SXF
# При успешной проверке возвращает 1
# При несовпадении контрольной суммы возвращает -1
# При ошибке структуры файла возвращает -2
# При устаревшей версии структуры файла возвращает -3
# При ошибке параметров системы координат суммы возвращает -4 (если вместе с ошибкой контрольной суммы, то -5)
# Если для СК-42 не заданы параметры датума - возвращает 2
# При ошибке доступа к данным возвращает ноль и выдает сообщение на экран (если выдача сообщений разрешена)

    SxfCheckSumAndCoordinatesUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SxfCheckSumAndCoordinatesUn', maptype.PWCHAR)
    def SxfCheckSumAndCoordinatesUn(_name: mapsyst.WTEXT) -> int:
        return SxfCheckSumAndCoordinatesUn_t (_name.buffer())


# Выполнить контроль структуры данных карты
# hMap,hSite - идентификаторы карты (см.MAPAPI.H),
# mode       - режим работы (0 - контроль, 1 - редактирование),
# handle     - идентификатор окна диалога процесса обработки (HWND для Windows).
#
# Окну диалога посылаются следующие сообщения :
#  WM_LIST   = 0x586   WParam - количество листов в районе
#                      LParam - номер текущего листа
#  WM_OBJECT = 0x585   WParam - процент обработанных объектов
#  WM_ERROR  = 0x587   WParam - порядковый номер объекта или 0
#                      LParam = 1 - ошибка в карте
#                             = 2 - ошибка в классификаторе
#                             = 3 - ошибка в описании объекта
#                             = 4 - ошибка в метрике
#                             = 5 - ошибка в семантике
#                             = 6 - ошибка в графике
# Возвращает количество ошибок в районе

    mapStructControl_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapStructControl', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HMESSAGE)
    def mapStructControl(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mode: int, _handle: maptype.HMESSAGE) -> int:
        return mapStructControl_t (_hMap, _hSite, _mode, _handle)


# Сортировка всех карт, входящих в документ
# hmap   - идентификатор сортируемого документа
# handle - идентификатор окна диалога процесса обработки (HWND)
# mode   - комбинация флагов способа обработки карты:
#   0 - сортировать все листы,
#   1 - только несортированные;
#   2 - сохранять файлы отката;
#   4 - повысить точность хранения в метрах, число знаков максимальное;
#  16 - повысить точность хранения в метрах, формат - см  (2 знака);
#  32 - повысить точность хранения в метрах, формат - мм  (3 знака);
#  64 - повысить точность хранения в радианах, число знаков максимальное;
# При ошибке возвращает ноль

    MapSortProcess_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'MapSortProcess', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int)
    def MapSortProcess(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mode: int) -> int:
        return MapSortProcess_t (_hmap, _handle, _mode)


# Запрос числа элементов (SXF,TXF,MAP,...) в DIR
# В списке элементов файла DIR могуть быть растры и матрицы
# dirname - полное имя файла DIR
# При ошибке возвращает ноль

    GetDirItemCountUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirItemCountUn', maptype.PWCHAR)
    def GetDirItemCountUn(_dirname: mapsyst.WTEXT) -> int:
        return GetDirItemCountUn_t (_dirname.buffer())

    GetDirItemCount_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirItemCount', ctypes.c_char_p)
    def GetDirItemCount(_dirname: ctypes.c_char_p) -> int:
        return GetDirItemCount_t (_dirname)


# Запрос названия района или первой карты в списке (SXF,TXF,MAP,...) в DIR
# dirname - полное имя файла DIR
# name    - адрес буфера для размещения запрошенного имени
# size    - размер буфера
# При успешном выполнении возвращает число элементов в списке
# При ошибке возвращает ноль

    GetDirAreaNameUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirAreaNameUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def GetDirAreaNameUn(_namedir: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return GetDirAreaNameUn_t (_namedir.buffer(), _name.buffer(), _size)

    GetDirAreaName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirAreaName', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def GetDirAreaName(_dirname: ctypes.c_char_p, _name: ctypes.c_char_p, _size: int) -> int:
        return GetDirAreaName_t (_dirname, _name, _size)


# Запрос списка имен файлов данных (SXF,TXF,MAP,...) в DIR
# dirname - полное имя файла DIR
# items   - адрес буфера для размещения заполненной структуры NAMESARRAY
#           (см. mmstruct.h)
# size    - размер буфера; должен быть не меньше, чем размер струткруры
#           для числа элементов, равного GetDirItemCount()
#           size = sizeof(NAMESARRAY) + sizeof(LISTSNAME) # (count - 1);
# При успешном выполнении возвращает число элементов в списке
# При ошибке возвращает ноль

    GetDirItemListUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirItemListUn', maptype.PWCHAR, ctypes.POINTER(mmstruct.NAMESARRAY), ctypes.c_int)
    def GetDirItemListUn(_dirname: mapsyst.WTEXT, _items: ctypes.POINTER(mmstruct.NAMESARRAY), _size: int) -> int:
        return GetDirItemListUn_t (_dirname.buffer(), _items, _size)

    GetDirItemList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDirItemList', ctypes.c_char_p, ctypes.POINTER(mmstruct.NAMESARRAY), ctypes.c_int)
    def GetDirItemList(_dirname: ctypes.c_char_p, _items: ctypes.POINTER(mmstruct.NAMESARRAY), _size: int) -> int:
        return GetDirItemList_t (_dirname, _items, _size)


# Заполнить метрику объекта координатами рамки листа карты
# из файлов SXF, TXF, MAP, SIT, SITX
# name - имя файла карты в одном из вышеперечисленных форматов
# HOBJ - идентификатор объекта, созданного на той карте, где будет сохранен объект
# extend - признак вставки дополнительных точек на стороны рамки, если рамка состоит только из 4 угловых точек
# Координаты будут пересчитаны из системы координат файла к системе координат выходной карты
# Если объекта-рамки нет в наборе данных, то запишутся координаты габаритов набора данных
# Если у исходного объекта имелись координаты, то они будут удалены
# Объект-рамка ищется по коду SHEETFRAMEEXCODE (91000000)
# При ошибке возвращает ноль

    GetBorderMetricsFromAnySxfEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetBorderMetricsFromAnySxfEx', maptype.PWCHAR, maptype.HOBJ, ctypes.c_int)
    def GetBorderMetricsFromAnySxfEx(_name: mapsyst.WTEXT, _hobj: maptype.HOBJ, _extend: int) -> int:
        return GetBorderMetricsFromAnySxfEx_t (_name.buffer(), _hobj, _extend)

    GetBorderMetricsFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetBorderMetricsFromAnySxfUn', maptype.PWCHAR, maptype.HOBJ)
    def GetBorderMetricsFromAnySxfUn(_name: mapsyst.WTEXT, _hobj: maptype.HOBJ) -> int:
        return GetBorderMetricsFromAnySxfUn_t (_name.buffer(), _hobj)


# Сформировать обзорное изображение карты в формате PNG
# из файлов SXF, TXF, MAP, SIT, SITX
# Изображение строится из цетральной части карты в базовом масштабе карты
# sxfname - имя файла карты в одном из вышеперечисленных форматов
# imagename - имя файла PNG с обзорным изображением, если равно 0,
#           то к полному имени файла карты добавляется ".preview.png"
# width   - ширина изображения (обычно 512)
# height  - высота изображения (обычно 512)
# rscname - имя цифрового классификатора для карт формата SXF и TXF,
#           если равно нулю, то ищется в SXF или TXF
# hevent    - адрес функции обратного вызова для записи в протокол ошибок выполнени программы
# eventparam - первый параметр функции обратного вызова
# При ошибке возвращает ноль

    BuildPreviewImageFromAnySxfPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'BuildPreviewImageFromAnySxfPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.EVENTLOG, ctypes.POINTER(ctypes.c_void_p))
    def BuildPreviewImageFromAnySxfPro(_dataname: mapsyst.WTEXT, _imagename: mapsyst.WTEXT, _width: int, _height: int, _rscname: mapsyst.WTEXT, _hEvent: maptype.EVENTLOG, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return BuildPreviewImageFromAnySxfPro_t (_dataname.buffer(), _imagename.buffer(), _width, _height, _rscname.buffer(), _hEvent, _eventparam)

    BuildPreviewImageFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'BuildPreviewImageFromAnySxfUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def BuildPreviewImageFromAnySxfUn(_sxfname: mapsyst.WTEXT, _imagename: mapsyst.WTEXT, _width: int, _height: int, _rscname: mapsyst.WTEXT) -> int:
        return BuildPreviewImageFromAnySxfUn_t (_sxfname.buffer(), _imagename.buffer(), _width, _height, _rscname.buffer())


# Проверить имя папки на соответствие номенклатуре (международной разграфке)
# mapreg - параметры системы координат карты (для определения типа карты VN2000 c особенной номенклатурой)
# name   - проверяемая номенклатура
# size   - длина строки, в которую записана номенклатура (для обновления номенклатуры VN2000)
# При ошибке возвращает ноль

    vecCheckNomenclature_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecCheckNomenclature', ctypes.POINTER(mapcreat.MAPREGISTEREX), maptype.PWCHAR, ctypes.c_int)
    def vecCheckNomenclature(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _name: mapsyst.WTEXT, _size: int) -> int:
        return vecCheckNomenclature_t (_mapreg, _name.buffer(), _size)


#========================================================================
#   Функции импорта, экспорта и обновления карты для форматов SXF, TXF и DIR
#========================================================================
#  Окну диалога посылаются следующие сообщения :
#  WM_OBJECT = 0x585   WParam - процент обработанных объектов
#  WM_INFOLIST = 0x584 LParam - адрес структуры INFOLIST
# ----------------------------------------------------------------
# Загрузить (импортировать) карту из файла SXF, TXF или DIR с
# использованием Select с преобразованием топокарты к зоне документа
# Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
# hmap    - идентификатор открытой карты (рекомендуется указывать
#           для определения текущей зоны топокарты) или 0;
# sxfname - имя загружаемого файла типа SXF, TXF или DIR;
# rscname - имя файла классификатора, с которым загружается карта,
#           имя классификатора можно запросить из SXF (TXF) функцией GetRscNameFromSxf
#           или из карты; для файла DIR может быть 0;
# mapname - имя создаваемой карты (обычно совпадает с именем SXF (TXF))
#           или ноль или указатель на пустую строку (буфер размером MAX_PATH
#           c нулевым байтом равным нулю) или указатель на папку для размещения
#           карты. Если имя карты не задано или задана только папка, то карта
#           создается с именем SXF (TXF) и расширением ".sit". Если namemap
#           указывает на буфер достаточной длины (size), то в буфер записывается
#           имя созданной карты;
#           Для файла DIR тип общей карты - MPT (проект данных, включающий все
#           открытые карты из DIR) или MAP (многолистовая карта);
# size    - длина буфера, на который указывает переменная namemap, или 0. Обычно длина
#           равна MAX_PATH_LONG (1024);
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр загружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# frscfromsxf - значение флажка "разрешить использование
#               имени классификатора, указанного в файле sxf"
# typesit - тип создаваемых карт в проекте MPT при импорте DIR (1- SIT; -1- SITX)
# password - пароль для создания защищенного хранилища карты (SITX)
# psize    - длина пароля в байтах
# transform - признак необходимости трансформировать загружаемую карту в систему координат hmap
#             (если hmap и transform не равно 0)
# hevent    - адрес функции обратного вызова для записи в протокол ошибок выполнени программы
# eventparam - первый параметр функции обратного вызова
# Для добавления открытой карты в документ необходимо вызвать функцию
# mapAppendData(hmap, namemap). Если mapname содержит имя карты типа MAP и
# она содержит хотя бы один лист, то при импорте данных выполняется создание
# нового листа в карте MAP. В этом случае функция mapAppendData не должна вызываться.
# При ошибке возвращает ноль

    ImportFromAnySxfProEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ImportFromAnySxfProEx', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.EVENTLOG, ctypes.POINTER(ctypes.c_void_p))
    def ImportFromAnySxfProEx(_hmap: maptype.HMAP, _namesxf: mapsyst.WTEXT, _namersc: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _frscfromsxf: int, _typesit: int, _password: mapsyst.WTEXT, _psize: int, _transform: int, _hevent: maptype.EVENTLOG, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return ImportFromAnySxfProEx_t (_hmap, _namesxf.buffer(), _namersc.buffer(), _namemap.buffer(), _size, _handle, _select, _frscfromsxf, _typesit, _password.buffer(), _psize, _transform, _hevent, _eventparam)

    ImportFromAnySxfPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ImportFromAnySxfPro', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def ImportFromAnySxfPro(_hmap: maptype.HMAP, _namesxf: mapsyst.WTEXT, _namersc: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _frscfromsxf: int, _typesit: int, _password: mapsyst.WTEXT, _psize: int) -> int:
        return ImportFromAnySxfPro_t (_hmap, _namesxf.buffer(), _namersc.buffer(), _namemap.buffer(), _size, _handle, _select, _frscfromsxf, _typesit, _password.buffer(), _psize)


# Загрузить (импортировать) карту из файла DIR
# frscfromsxf - значение флажка "разрешить использование
# имени классификатора, указанного в файле sxf"
# При ошибке возвращает ноль

    ImportFromAnySxfEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ImportFromAnySxfEx', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int)
    def ImportFromAnySxfEx(_hmap: maptype.HMAP, _sxfname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _mapname: ctypes.c_char_p, _size: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _frscfromsxf: int) -> int:
        return ImportFromAnySxfEx_t (_hmap, _sxfname, _rscname, _mapname, _size, _handle, _select, _frscfromsxf)


# Загрузить карту из файла SXF, TXF или DIR с использованием Select
# с преобразованием топокарты к зоне документа
# Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
# namedir - имя загружаемого файла типа DIR;
# namemap - имя создаваемой карты
#           или ноль или указатель на пустую строку (буфер размером 1024 символа
#           c нулевым байтом равным нулю) или указатель на папку для размещения
#           карты. Если namemap указывает на буфер достаточной длины (size),
#           то в буфер записывается имя созданной карты;
#           Для файла DIR тип общей карты - MPT (проект данных, включающий все
#           открытые карты из DIR) или MAP (многолистовая карта);
# size    - длина буфера, на который указывает переменная namemap или 0. Обычно длина
#           равна 2048 байт;
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux) или 0;
# typesit  - тип создаваемых карт в проекте MPT при импорте DIR (1- SIT; -1- SITX)
# password - пароль доступа к данным, из которого формируется 256-битный код
#            для шифрования данных (при утрате данные не восстанавливаются) или 0
# psize    - длина пароля в байтах или 0
# crscode  - указатель на строку с кодом системы координат, к которой преобразуются
#            данные или 0. Примеры строки: "EPSG:3857", "crslist:80070050"
#            В первом случае преобразование выполняется в систему 3857 (проекция Меркатора на шаре),
#            во втором - к параметрам, считанным из файла crslist.xml по коду 80070050,
#            то есть, к некоторой пользовательской системе координат, описанной в файле crslist.xml.
# callevent - адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
# parm      - параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
# logfile   - путь к файлу журнала работы программы (может быть 0)
# При ошибке возвращает ноль

    ImportFromDirPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ImportFromDirPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_char_p, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR)
    def ImportFromDirPro(_namedir: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _typesit: int, _password: mapsyst.WTEXT, _psize: int, _crscode: ctypes.c_char_p, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT) -> int:
        return ImportFromDirPro_t (_namedir.buffer(), _namemap.buffer(), _size, _handle, _typesit, _password.buffer(), _psize, _crscode, _callevent, _parm, _logfile.buffer())


# Загрузить временную карту из буфера в памяти в формате TXF
# buffer  - адрес буфера, содержащего данные в формате TXF
# size    - размер буфера
# rscname - имя классификатора для создания временной карты,
#           если равно нулю, то используется service.rsc
# Возвращает идентификатор временной карты в памяти
# При закрытии карты все ее данные удаляются
# При ошибке возвращает ноль

    vecLoadTxfFromBuffer_t = mapsyst.GetProcAddress(vecexlib,maptype.HMAP,'vecLoadTxfFromBuffer', ctypes.c_char_p, ctypes.c_int, maptype.PWCHAR)
    def vecLoadTxfFromBuffer(_buffer: ctypes.c_char_p, _size: int, _rscname: mapsyst.WTEXT) -> maptype.HMAP:
        return vecLoadTxfFromBuffer_t (_buffer, _size, _rscname.buffer())


# Обновить карту из файла SXF, TXF или DIR с использованием Select
# с преобразованием топокарты к зоне документа
# Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
# hmap    - идентификатор открытой карты (для определения текущей
#           зоны топокарты) или 0;
# sxfname - имя загружаемого файла типа SXF, TXF или DIR;
# mapname - имя обновляемой карты; может быть ноль или указатель на пустую
#           строку, в этом случае обновляемая карта в документе ищется
#           по совпадению номенклатур.
#           Если namemap указывает на буфер достаточной длины (size),
#           то в буфер записывается имя обновленной карты;
#           Если карты не было в документе - она может быть создана (добавлена)
# size    - длина буфера, на который указывает переменная namemap или 0. Обычно длина
#           равна MAX_PATH (256);
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр загружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# mode    - режим обновления данных:
#           0 - поиск записей по совпадению уникального номера в карте и
#               исходном файле и обновление,
#               если объект не найден, то добавление объекта;
#           1 - добавление объектов с новыми уникальными номерами в те карты,
#               номенклатуры которых совпадают с номенклатурой SXF (TXF),
#               если - номенклатура не найдена, то добавляется новый лист (карта);
#           2 - добавление объектов с новыми уникальными номерами в заданную
#               карту без учета номенклатур
# При ошибке возвращает ноль

    UpdateFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateFromAnySxfUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int)
    def UpdateFromAnySxfUn(_hmap: maptype.HMAP, _sxfname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _mode: int) -> int:
        return UpdateFromAnySxfUn_t (_hmap, _sxfname.buffer(), _mapname.buffer(), _size, _handle, _select, _mode)

# Загрузить карту из файла SXF, TXF или DIR с использованием Select
# с преобразованием топокарты к зоне документа
# Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
# namedir - имя загружаемого файла типа DIR;
# namemap - имя создаваемой карты
#           или ноль или указатель на пустую строку (буфер размером 1024 символа
#           c нулевым байтом равным нулю) или указатель на папку для размещения
#           карты. Если namemap указывает на буфер достаточной длины (size),
#           то в буфер записывается имя созданной карты;
#           Для файла DIR тип общей карты - MPT (проект данных, включающий все
#           открытые карты из DIR) или MAP (многолистовая карта);
# size    - длина буфера, на который указывает переменная namemap или 0. Обычно длина
#           равна 2048 байт;
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux) или 0;
# callevent - адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
# parm      - параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
# logfile   - путь к файлу журнала работы программы (может быть 0)
# mode    - режим обновления данных:
#           0 - поиск записей по совпадению уникального номера в карте и
#               исходном файле и обновление,
#               если объект не найден, то добавление объекта;
#           1 - добавление объектов с новыми уникальными номерами в те карты,
#               номенклатуры которых совпадают с номенклатурой SXF (TXF);
#           2 - добавление объектов с новыми уникальными номерами в заданную
#               карту без учета номенклатур;
#           3 - замена листов или добавление новых листов (карт).
# При ошибке возвращает ноль

    UpdateFromDirPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateFromDirPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR)
    def UpdateFromDirPro(_namedir: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _mode: int, _handle: maptype.HMESSAGE, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT) -> int:
        return UpdateFromDirPro_t (_namedir.buffer(), _namemap.buffer(), _size, _mode, _handle, _callevent, _parm, _logfile.buffer())


# Сохранить (экспортировать) карту в двоичный формат SXF
# mapname - имя файла сохраняемой карты;
# list    - номер листа для многолистовой карты или 1;
# sxfname - имя создаваемого файла SXF, обычно совпадает с
#           именем карты, но имеет расширение SXF;
# flag    - вид хранимых координат (0 - метры, 4 - радианы, 8 - градусы,
#           для карты, поддерживающей геодезические координаты,
#           -1 - определить по виду координат на карте);
#           Если карты не было в документе - она может быть создана (добавлена)
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр выгружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# flserv  - записать служебный объект c датумом и эллипсоидом и имя классификатора
#           (поддерживается с версии 10.7 и выше)
# Для топокарт, хранящих координаты в метрах, координаты всегда хранятся
# в зоне, указанной в паспорте карты
# При ошибке возвращает ноль

    ExportToSxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToSxfUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int)
    def ExportToSxfUn(_mapname: mapsyst.WTEXT, _list: int, _sxfname: mapsyst.WTEXT, _flag: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _flserv: int) -> int:
        return ExportToSxfUn_t (_mapname.buffer(), _list, _sxfname.buffer(), _flag, _handle, _select, _flserv)

# Сохранить (экспортировать) карту в текстовый формат TXF
# mapname - имя файла сохраняемой карты;
# list    - номер листа для многолистовой карты или 1;
# txfname - имя создаваемого файла TXF, обычно совпадает с
#           именем карты, но имеет расширение SXF;
# flag    - вид хранимых координат (0 - метры, 4 - радианы, 8 - градусы,
#           для карты, поддерживающей геодезические координаты,
#           -1 - определить по виду координат на карте);
#           Если карты не было в документе - она может быть создана (добавлена)
# precision - число знаков после запятой для координат в метрах или 0;
#             если карта имеет паспортную точность в см (2 знака) или
#             в мм (3 знака), то precision игнорируется;
# isutf8    - признак записи названий файлов, имени листа карты, текстов подписей и
#             текстовых семантик в кодировке utf8 (если значение поля ненулевое,
#             иначе - в кодировке ANSI)
# handle    - идентификатор окна диалога, которому посылаются уведомительные
#             сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select    - фильтр выгружаемых объектов и слоев, если необходима выборочная
#             обработка данных;
# Для топокарт, хранящих координаты в метрах, координаты всегда хранятся
# в зоне, указанной в паспорте карты
# При ошибке возвращает ноль

    ExportToTxfPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToTxfPro', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT)
    def ExportToTxfPro(_mapname: mapsyst.WTEXT, _list: int, _txfname: mapsyst.WTEXT, _flag: int, _precision: int, _isutf8: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return ExportToTxfPro_t (_mapname.buffer(), _list, _txfname.buffer(), _flag, _precision, _isutf8, _handle, _select)

    ExportToTxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToTxfUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT)
    def ExportToTxfUn(_mapname: mapsyst.WTEXT, _list: int, _txfname: mapsyst.WTEXT, _flag: int, _precision: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return ExportToTxfUn_t (_mapname.buffer(), _list, _txfname.buffer(), _flag, _precision, _handle, _select)

# Сохранить (экспортировать) карту в формат DIR
# hmap    - идентификатор открытых данных
# dirname - имя создаваемого файла DIR, обычно совпадает с
#           именем открытого проекта или главной карты, но имеет расширение DIR;
# type    - тип создаваемых файлов (0 - SXF, 1 - TXF);
# flag    - вид хранимых координат (0 - метры, 4 - радианы, 8 - градусы,
#           для карты, поддерживающей геодезические координаты,
#           -1 - определить по виду координат на карте);
#           Если карты не было в документе - она может быть создана (добавлена)
# total   - признак сохранения в DIR только главной карты (0) или всех карт
#           документа (1);
# precision - для файлов TXF число знаков после запятой для координат в метрах или 0;
#           если карта имеет паспортную точность в см (2 знака) или
#           в мм (3 знака), то precision игнорируется;
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр выгружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# frsc    - записать имя классификатора в файл sxf (если не равно 0)
# utf8    - записать имена файлов и файлы TXF (если type равен 1) в кодировке UTF8
# logname - имя файла-протокола результатов сохранения карты в DIR или ноль
# Для топокарт, хранящих координаты в метрах, координаты всегда хранятся
# в зоне, указанной в паспорте карты
# При ошибке возвращает ноль

    ExportToDirPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToDirPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def ExportToDirPro(_hmap: maptype.HMAP, _dirname: mapsyst.WTEXT, _type: int, _flag: int, _total: int, _precision: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _frsc: int, _isutf8: int, _logname: mapsyst.WTEXT) -> int:
        return ExportToDirPro_t (_hmap, _dirname.buffer(), _type, _flag, _total, _precision, _handle, _select, _frsc, _isutf8, _logname.buffer())

    ExportToDirUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToDirUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def ExportToDirUn(_hmap: maptype.HMAP, _dirname: mapsyst.WTEXT, _type: int, _flag: int, _total: int, _precision: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _frsc: int, _isutf8: int) -> int:
        return ExportToDirUn_t (_hmap, _dirname.buffer(), _type, _flag, _total, _precision, _handle, _select, _frsc, _isutf8)

# Нарезать исходную карту по листам выходной карты
# hmap  - идентификатор открытых данных
# hsite -  идентификатор открытой пользовательской карты
# hmapout - идентификатор выходной карты (для ускорения загрузки установить mapSetLoadState)
# hselect - условия отбора объектов или 0 (обработать все объекты)
# Возвращает число обработанных объектов
# При прерывании задачи оператором возвращает -1
# При ошибке возвращает ноль

    vecCutSiteToSheets_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecCutSiteToSheets', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.HMAP, maptype.HSELECT)
    def vecCutSiteToSheets(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hmapout: maptype.HMAP, _hselect: maptype.HSELECT) -> int:
        return vecCutSiteToSheets_t (_handle, _hmap, _hsite, _hmapout, _hselect)


#========================================================================
#   Функции чтения формата ZIP
#========================================================================
# Проверить корректность архива в ZIP-файле
# (zip-архив может выдаваться по запросу из Банка данных ЦК и ДЗЗ)
# zipfile - путь к архиву
# error   - код ошибки (ошибка доступа может быть и при корректном архиве)
# При ошибке возвращает ноль

    CheckZipValidate_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'CheckZipValidate', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def CheckZipValidate(_zipfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return CheckZipValidate_t (_zipfile.buffer(), _error)


# Распаковать ZIP-файл в заданную папку
# zipfile - путь к архиву
# folder  - путь к папке для распаковки архива
# logfile - путь к текстововому файлу протоколу распаковки архива (может быть 0)
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# При ошибке возвращает ноль

    UnZipToFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipToFolder', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipToFolder(_zipfile: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> int:
        return UnZipToFolder_t (_zipfile.buffer(), _folder.buffer(), _logfile.buffer(), _error, _message)


# Распаковать список файлов из ZIP-файла в заданную папку
# zipfile - путь к архиву
# folder  - путь к папке для распаковки архива
# filelist - список указателей на имена файлов в кодировке UTF-8, которые нужно распаковать в заданную папку
# filecount - число указателей в списке (массиве указателей)
# logfile - путь к текстововому файлу протоколу распаковки архива (может быть 0)
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# При ошибке возвращает ноль

    UnZipToFolderEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipToFolderEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipToFolderEx(_zipfile: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _filelist: ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), _filecount: int, _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> int:
        return UnZipToFolderEx_t (_zipfile.buffer(), _folder.buffer(), _filelist, _filecount, _logfile.buffer(), _error, _message)


# Распаковать из архива в заданную папку файл RSC и записать полученное имя (путь)
# zipfile - путь к архиву
# folder  - путь к папке для распаковки архива
# extend  - строка со списком расширений (окончаний) файлов в кодировке UTF-8, разделенных запятой, или ноль
#           например: "sxf,txf,rsc,.meta.xml,.geojson,gml"
#           Окончания файлов могут быть в любом регистре
# count   - число расширений в списке или ноль
# error   - поле для записи кода ошибки распаковки архива
# При ошибке возвращает ноль

    UnZipFormatFilesToFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipFormatFilesToFolder', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def UnZipFormatFilesToFolder(_zipfile: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _extend: ctypes.c_char_p, _count: int, _filename: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return UnZipFormatFilesToFolder_t (_zipfile.buffer(), _folder.buffer(), _extend, _count, _filename.buffer(), _size, _error)


# Распаковать заданный файл из ZIP-файла в память
# zipfile  - путь к архиву
# filename - имя распаковываемого файла
# logfile - путь к текстововому файлу протоколу распаковки архива (может быть 0)
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# Для получения данных используется функция UnZipMemoryPoint
# После считывания данных необходимо освободить ресурсы функцией UnZipFreeMemory
# При ошибке возвращает ноль, иначе - идентификатор данных в памяти

    UnZipFileToMemory_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'UnZipFileToMemory', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipFileToMemory(_zipfile: mapsyst.WTEXT, _filename: mapsyst.WTEXT, _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> ctypes.c_void_p:
        return UnZipFileToMemory_t (_zipfile.buffer(), _filename.buffer(), _logfile.buffer(), _error, _message)


# Освободить буфер распакованного файла по идентификатору буфера

    UnZipFreeMemory_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'UnZipFreeMemory', ctypes.c_void_p)
    def UnZipFreeMemory(_hmemory: ctypes.c_void_p) -> ctypes.c_void_p:
        return UnZipFreeMemory_t (_hmemory)


# Запросить статистику по содержанию ZIP-архива (исходный размер, размер в zip,
# процент сжатия, дата и время создания файла, имя файла)
# zipfile - путь к архиву
# logfile - путь к текстововому файлу протоколу для записи статистики
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# При ошибке возвращает ноль

    UnZipInfo_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipInfo', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipInfo(_zipfile: mapsyst.WTEXT, _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> int:
        return UnZipInfo_t (_zipfile.buffer(), _logfile.buffer(), _error, _message)


# Запросить список файлов заданных форматов в ZIP-архиве
# zipfile - путь к архиву
# extend  - строка со списком расширений (окончаний) файлов, разделенных запятой, или ноль
#           например: "sxf,txf,rsc,.meta.xml,.geojson,gml"
#           Окончания файлов могут быть в любом регистре
# count   - число расширений в списке или ноль
# outcount - число записей в списке файлов (разделены символом \n)
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# При ошибке возвращает ноль, иначе - идентификатор данных в памяти

    UnZipFileListEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'UnZipFileListEx', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipFileListEx(_zipfile: mapsyst.WTEXT, _extend: ctypes.c_char_p, _count: int, _outcount: ctypes.POINTER(ctypes.c_int), _error: ctypes.POINTER(ctypes.c_int), _message: int) -> ctypes.c_void_p:
        return UnZipFileListEx_t (_zipfile.buffer(), _extend, _count, _outcount, _error, _message)

    UnZipFileList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'UnZipFileList', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipFileList(_zipfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> ctypes.c_void_p:
        return UnZipFileList_t (_zipfile.buffer(), _error, _message)


# Запросить кодировку списка файлов в ZIP-архиве, выдаваемую UnZipFileList
# через вызов UnZipMemoryPoint
# Если кодировка UTF-8, то возвращает 1
# Если кодировка ANSI (для Windows) или KOI-8R (Linux), то возвращает 0

    UnZipFileListCode_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipFileListCode')
    def UnZipFileListCode() -> int:
        return UnZipFileListCode_t ()


# Запросить наличие файлов заданного типа в ZIP-архиве
# zipfile - путь к архиву
# extend  - строка со списком расширений (окончаний) файлов, разделенных пробелом
#           например: "sxf,txf,rsc,meta.xml,geojson,gml"
#           Окончания файлов могут быть в любом регистре, длина строки до 2048 байт
# amounts - список счетчиков файлов с заданным расширением в zip-архиве
# count   - число счетчиков и число расширений в списке
# error   - поле для записи кода ошибки распаковки архива
# message - признак выдачи сообщения об ошибке на экран
# При ошибке возвращает ноль, иначе - число обработанных расширений

    UnZipFileCount_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UnZipFileCount', maptype.PWCHAR, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def UnZipFileCount(_zipfile: mapsyst.WTEXT, _extend: ctypes.c_char_p, _amounts: ctypes.POINTER(ctypes.c_int), _count: int, _error: ctypes.POINTER(ctypes.c_int), _message: int) -> int:
        return UnZipFileCount_t (_zipfile.buffer(), _extend, _amounts, _count, _error, _message)


# Проверить, что файл zip содержит файлы SHP
# Возвращает число найденных файлов SHP в архиве
# При ошибке возвращает ноль

    shpCheckZipContents_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpCheckZipContents', maptype.PWCHAR)
    def shpCheckZipContents(_shpzip: mapsyst.WTEXT) -> int:
        return shpCheckZipContents_t (_shpzip.buffer())


# Выполнить импорт наборов данных SHP из папки, запакованной в ZIP, в один лист карты
# hmap      - идентификатор карты, в которую дописываются листы или 0
#             (если hmap != 0, то mapname, rscname, iscreate игнорируются)
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# shpzip    - имя файла zip, содержащего слои листа карты в формате SHP (любой вложенности)
# mapname   - имя файла создаваемой/обновляемой карты
# rscname   - имя файла классификатора, с которым создается карта, или 0 (если карта существует)
# epsgcode  - код системы координат создаваемой карты или 0 (если карта существует или создается по PRJ)
# iscreate  - признак создания карты или 0 (если карта существует)
# При ошибке возвращает ноль

    shpLoadSheetFromZip_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpLoadSheetFromZip', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def shpLoadSheetFromZip(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _shpzip: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return shpLoadSheetFromZip_t (_hmap, _handle, _shpzip.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate, _error)


# Выполнить импорт наборов данных SHP из папки в один лист карты
# hmap      - идентификатор карты, в которую дописываются листы или 0
#             (если hmap != 0, то mapname, rscname, iscreate игнорируются)
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# shpfolder - имя папки, в которой размещены слои листа карты в формате SHP (любой вложенности)
# mapname   - имя файла создаваемой/обновляемой карты
# rscname   - имя файла классификатора, с которым создается карта, или 0 (если карта существует)
# epsgcode  - код системы координат создаваемой карты или 0 (если карта существует или создается по PRJ)
# iscreate  - признак создания карты или 0 (если карта существует)
# При ошибке возвращает ноль

    shpLoadSheetFromFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpLoadSheetFromFolder', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def shpLoadSheetFromFolder(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _shpfolder: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int) -> int:
        return shpLoadSheetFromFolder_t (_hmap, _handle, _shpfolder.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate)


# Определить параметры системы координат из файла PRJ
# Если задана геодезическая система координат в градусах, то возвращает 2
# Для координат в метрах возвращает 1
# Если параметры не были определены и координаты в метрах - возвращает -1
# При ошибке возвращает ноль

    shpShapeProcReadPrj_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpShapeProcReadPrj', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.c_int)
    def shpShapeProcReadPrj(_prjname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _csname: mapsyst.WTEXT, _size: int) -> int:
        return shpShapeProcReadPrj_t (_prjname.buffer(), _mapreg, _ellparm, _datumparm, _csname.buffer(), _size)


# Создать объект для импорта файлов SHP
# handle - идентификатор получателя сообщений WM_ERROR и WM_OBJECT
# mapname - имя паспорта создаваемой\обновляемой карты
# rscname - имя классификатора создаваемой карты или 0 (если имя не задано, то карта обновляется)
# name    - имя района (листа) карты
# mapreg, ellparm, datumparm - параметры системы координат исходных данных и создаваемой карты (если карта создается)
# nomenclature - номенклатура листа или 0 (используется и для формирования имени файлов листов карт с рамкой)
# recitem - список обрабатываемых атрибутов (имена полей DBF и их ключи в классификаторе - если они разные)
# semitem - список обрабатываемых полей атрибутов или 0 (если нужно обрабатывать не все поля DBF)
# ismap   - признак создания карты (1- многолистовая карта MAP, иначе 0)
# epsgcode - код системы координат, в которой создается карта или 0 (если система совпадает с системой исходных данных)
# При ошибке возвращает ноль

    shpShapeProcSheetInitEx_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HSHPLOAD,'shpShapeProcSheetInitEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.POINTER(RECORDLIST), ctypes.c_int, ctypes.POINTER(SEMFIELDS), ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def shpShapeProcSheetInitEx(_handle: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _nomenclature: mapsyst.WTEXT, _recitem: ctypes.POINTER(RECORDLIST), _recount: int, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int, _ismap: int, _epsgcode: int) -> vecexapi.HSHPLOAD:
        return shpShapeProcSheetInitEx_t (_handle, _mapname.buffer(), _rscname.buffer(), _name.buffer(), _mapreg, _ellparm, _datumparm, _nomenclature.buffer(), _recitem, _recount, _semitem, _semcount, _ismap, _epsgcode)

    shpShapeProcSheetInit_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HSHPLOAD,'shpShapeProcSheetInit', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.POINTER(RECORDLIST), ctypes.c_int, ctypes.POINTER(SEMFIELDS), ctypes.c_int, ctypes.c_int)
    def shpShapeProcSheetInit(_handle: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _nomenclature: mapsyst.WTEXT, _recitem: ctypes.POINTER(RECORDLIST), _recount: int, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int, _ismap: int) -> vecexapi.HSHPLOAD:
        return shpShapeProcSheetInit_t (_handle, _mapname.buffer(), _rscname.buffer(), _name.buffer(), _mapreg, _ellparm, _datumparm, _nomenclature.buffer(), _recitem, _recount, _semitem, _semcount, _ismap)

    shpShapeProcInit_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HSHPLOAD,'shpShapeProcInit', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(RECORDLIST), ctypes.c_int, ctypes.POINTER(SEMFIELDS), ctypes.c_int)
    def shpShapeProcInit(_handle: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _recitem: ctypes.POINTER(RECORDLIST), _recount: int, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int) -> vecexapi.HSHPLOAD:
        return shpShapeProcInit_t (_handle, _mapname.buffer(), _rscname.buffer(), _name.buffer(), _mapreg, _ellparm, _datumparm, _recitem, _recount, _semitem, _semcount)


# Создать объект для импорта файлов SHP
# hmap    - идентификатор карты, в которую дописываются листы
# handle  - идентификатор получателя сообщений WM_ERROR и WM_OBJECT
# nomenclature - номенклатура листа или 0 (используется и для формирования имени файлов листов карт с рамкой)
# mapreg, ellparm, datumparm - параметры системы координат исходных данных (если они отличаются от параметров карты)
# recitem - список обрабатываемых файлов SHP
# semitem - список обрабатываемых полей атрибутов
# При ошибке возвращает ноль

    shpShapeProcSheetForMap_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HSHPLOAD,'shpShapeProcSheetForMap', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.POINTER(RECORDLIST), ctypes.c_int, ctypes.POINTER(SEMFIELDS), ctypes.c_int)
    def shpShapeProcSheetForMap(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _nomenclature: mapsyst.WTEXT, _recitem: ctypes.POINTER(RECORDLIST), _recount: int, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int) -> vecexapi.HSHPLOAD:
        return shpShapeProcSheetForMap_t (_hmap, _handle, _mapreg, _ellparm, _datumparm, _nomenclature.buffer(), _recitem, _recount, _semitem, _semcount)


# Запросить идентификатор открытой карты
# hshpload - идентификатор объекта загрузки SHP
# При ошибке возвращает ноль

    shpGetShapeProcMapHandle_t = mapsyst.GetProcAddress(vecexlib,maptype.HMAP,'shpGetShapeProcMapHandle', vecexapi.HSHPLOAD)
    def shpGetShapeProcMapHandle(_hshpload: vecexapi.HSHPLOAD) -> maptype.HMAP:
        return shpGetShapeProcMapHandle_t (_hshpload)


# Загрузка  SHP-файла
# hshpload - идентификатор объекта загрузки SHP
# shpname  - имя входного файла SHP
# type     - тип объекта в наборе данных
# code     - код зарегистрированного объекта
# setting  - указатель на структуру настроек диалога SETTING (myform.h)
# error    - код ошибки при создании объектов
# При ошибке возвращает ноль

    shpShapeProcLoad_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpShapeProcLoad', vecexapi.HSHPLOAD, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(SETTING), ctypes.POINTER(ctypes.c_int))
    def shpShapeProcLoad(_hshpload: vecexapi.HSHPLOAD, _shpfilename: mapsyst.WTEXT, _code: int, _setting: ctypes.POINTER(SETTING), _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return shpShapeProcLoad_t (_hshpload, _shpfilename.buffer(), _code, _setting, _error)


# Загрузить список Shape файлов
# hshpload - идентификатор объекта загрузки SHP
# shplist  - список указателей на имена shp-файлов
# count    - число файлов в списке
# code     - массив кодов объектов для списка shp-файлов
# setting  - указатель на структуру настроек диалога SETTING (myform.h)
# При ошибке возвращает ноль

    shpShapeProcLoadList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpShapeProcLoadList', vecexapi.HSHPLOAD, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR1)), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(SETTING))
    def shpShapeProcLoadList(_hshpload: vecexapi.HSHPLOAD, _shplist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR1)), _count: int, _code: ctypes.POINTER(ctypes.c_int), _setting: ctypes.POINTER(SETTING)) -> int:
        return shpShapeProcLoadList_t (_hshpload, _shplist, _count, _code, _setting)


# Удалить объект для импорта файлов SHP
# При ошибке возвращает ноль

    shpShapeProcClose_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpShapeProcClose', vecexapi.HSHPLOAD)
    def shpShapeProcClose(_hshpload: vecexapi.HSHPLOAD) -> int:
        return shpShapeProcClose_t (_hshpload)


# Проверить совпадение параметров систем координат (PRJ) в разных папках (листах) с наборами SHP
# name - имя корневой папки с файлами SHP или с набором папок, содержащих отдельные листы карты
# Если файлы SHP расположены в корневой папке, то сравнивает файлы PRJ в корневой папке,
# если есть набор папок, то сравнивает по одному файлу PRJ в каждой папке, чтобы найти
# разные параметры СК (например, разные зоны)
# При совпадении параметров возвращает 1, иначе - нулевое значение

    shpCheckSheetProjectEquivalent_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpCheckSheetProjectEquivalent', maptype.PWCHAR)
    def shpCheckSheetProjectEquivalent(_name: mapsyst.WTEXT) -> int:
        return shpCheckSheetProjectEquivalent_t (_name.buffer())


# Запросить общие габариты набора файлов SHP в заданной папке, включая вложенные папки
# frame - габариты, запрашиваются в радианах в системе WGS-84
# Возвращает общее число объектов во всех файлах SHP
# Если для SHP не заданы параметры проекции (PRJ) - возвращает ноль
# При ошибке возвращает ноль

    shpGetShpBorderInFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpGetShpBorderInFolder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def shpGetShpBorderInFolder(_folder: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return shpGetShpBorderInFolder_t (_folder.buffer(), _frame)


# Выполнить импорт набора данных SHP в один лист карты
# hmap      - идентификатор карты, в которую дописываются листы или 0
#             (если hmap != 0, то mapname, rscname, iscreate игнорируются)
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# shpname   - имя файла в формате SHP
# mapname   - имя файла создаваемой карты или 0 (если карта существует)
# rscname   - имя файла классификатора, с которым создается карта, или 0 (если карта существует)
# epsgcode  - код системы координат создаваемой карты или 0 (если карта существует или создается по PRJ)
# iscreate  - признак создания карты или 0 (если карта существует)
# error     - поле для записи кода ошибки выполнения функции
# При ошибке возвращает ноль

    shpLoadOneShape_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'shpLoadOneShape', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def shpLoadOneShape(_hmap: maptype.HMAP, _shpname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int, _scale: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return shpLoadOneShape_t (_hmap, _shpname.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate, _scale, _error)


# Обновить описание объекта из SHP
# info    - идентификатор обновляемого объекта в памяти
# shpname - имя исходного файла SHP (полный путь)
# onlypoints - признак обновления только координат объекта
# error   - коды ошибок выполнения программы (см. maperr.rh)
# Объект изменяется без записи на карту
# При ошибке возвращает ноль

    vecUpdateObjectFromShp_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecUpdateObjectFromShp', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def vecUpdateObjectFromShp(_info: maptype.HOBJ, _shpname: mapsyst.WTEXT, _onlypoints: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecUpdateObjectFromShp_t (_info, _shpname.buffer(), _onlypoints, _error)


# dbffields - описание всех семантик, которые записываются в DBF и имена соответствующих полей
# folders   - описание папок для группировки слоев карты
# layer     - описание слоев, списка входящих объектов и включаемых в SHP атрибутов
# object    - описание объекта, включаемого в слой и его атрибутов (на исходной карте объект может быть в любом слое)
# Экспорт векторной карты в формат SHP
# hwnd    - идентификатор окна диалога для посылки сообщений WM_OBJECT, WM_ERROR, WM_LIST
# parm    - основные параметры для экспорта карты
# shppath - путь к папке для записи файлов SHP
# xmlparm - путь к файлу схемы, описывающей структуру файлов SHP
#           (если файл не задан, то структура слоев соответствует исходной карте)
# error   - коды ошибок выполнения программы (см. maperr.rh)
# ininame - имя файлов параметров экспорта в SHP
# logname - имя файла с протоколом ошибок процедуры
# При ошибке возвращает ноль

    vecSaveMapToShpPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecSaveMapToShpPro', maptype.HMESSAGE, ctypes.POINTER(MAPTOSHPPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, maptype.PWCHAR)
    def vecSaveMapToShpPro(_hwnd: maptype.HMESSAGE, _parm: ctypes.POINTER(MAPTOSHPPARM), _shppath: mapsyst.WTEXT, _xmlparm: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _ininame: mapsyst.WTEXT, _logname: mapsyst.WTEXT) -> int:
        return vecSaveMapToShpPro_t (_hwnd, _parm, _shppath.buffer(), _xmlparm.buffer(), _error, _ininame.buffer(), _logname.buffer())

    vecSaveMapToShp_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecSaveMapToShp', maptype.HMESSAGE, ctypes.POINTER(MAPTOSHPPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def vecSaveMapToShp(_hwnd: maptype.HMESSAGE, _parm: ctypes.POINTER(MAPTOSHPPARM), _shppath: mapsyst.WTEXT, _xmlparm: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecSaveMapToShp_t (_hwnd, _parm, _shppath.buffer(), _xmlparm.buffer(), _error)


# Сохранить описание объекта в SHP
# info    - идентификатор сохраняемого объекта в памяти
# shpname - имя файла SHP (полный путь), в который будет сохранен объект
# error   - коды ошибок выполнения программы (см. maperr.rh)
# При ошибке возвращает ноль

    vecSaveObjectToShp_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecSaveObjectToShp', maptype.HOBJ, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def vecSaveObjectToShp(_info: maptype.HOBJ, _shpname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecSaveObjectToShp_t (_info, _shpname.buffer(), _error)


# Проверить, что файл zip содержит файлы MIF\MID
# Возвращает число найденных файлов MIF в архиве
# При ошибке возвращает ноль

    mifCheckZipContents_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mifCheckZipContents', maptype.PWCHAR)
    def mifCheckZipContents(_mifzip: mapsyst.WTEXT) -> int:
        return mifCheckZipContents_t (_mifzip.buffer())


# Выполнить импорт наборов данных MIF\MID из папки, запакованной в ZIP, в один лист карты
# hmap      - идентификатор карты, в которую дописываются листы или 0
#             (если hmap != 0, то mapname, rscname, iscreate игнорируются)
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# mifzip    - имя папки, в которой размещены слои листа карты в формате MIF\MID (любой вложенности)
# mapname   - имя файла создаваемой/обновляемой карты
# rscname   - имя файла классификатора, с которым создается карта, или 0 (если карта существует)
# epsgcode  - код системы координат создаваемой карты или 0 (если карта существует или создается по своим параметрам)
# iscreate  - признак создания карты или 0 (если карта существует)
# При ошибке возвращает ноль

    mifLoadSheetFromZip_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mifLoadSheetFromZip', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mifLoadSheetFromZip(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mifzip: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mifLoadSheetFromZip_t (_hmap, _handle, _mifzip.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate, _error)


# Выполнить импорт наборов данных MIF\MID из папки в один лист карты
# hmap      - идентификатор карты, в которую дописываются листы или 0
#             (если hmap != 0, то mapname, rscname, iscreate игнорируются)
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# folder    - имя папки, в которой размещены слои листа карты в формате MIF\MID (любой вложенности)
# mapname   - имя файла создаваемой/обновляемой карты
# rscname   - имя файла классификатора, с которым создается карта, или 0 (если карта существует)
# epsgcode  - код системы координат создаваемой карты или 0 (если карта существует или создается по своим параметрам)
# iscreate  - признак создания карты или 0 (если карта существует)
# При ошибке возвращает ноль

    mifLoadSheetFromFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mifLoadSheetFromFolder', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mifLoadSheetFromFolder(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _folder: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int) -> int:
        return mifLoadSheetFromFolder_t (_hmap, _handle, _folder.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate)


# Инициализировать класс для импорта данных формата MIF\MID
# handle    - идентификатор обработчика сообщений о ходе выполнения импорта данных
# mifname   - полный путь к файлу формата MIF
# rscname   - имя файла классификатора, с которым создается карта
# prjname   - имя входного файла настроек INI с перечнем ключей и атрибутивных данных для загрузки объектов
# scale     - масштаб карты
# semnumber - указатель на номер поля настройки в записи файла MIF
# rscininame- имя файла классификатора в файле настроек (может отличаться от rscname, предпочтение у rscininame)
# codename  - имя поля настройки (ObjectCode, ObjectKey, ObjectName ...)
# incode    - указатель на массив внутренних кодов объектов (incode[0] - для линии, incode[1] - для полигона
#                                                            incode[2] - для точек, incode[3] - для текста
# codetype  - вид кода объекта (цифровой или символьный)
# При ошибке возвращает ноль

    mifInitLoadToMap_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HMIFTOMAP,'mifInitLoadToMap', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mifInitLoadToMap(_handle: maptype.HMESSAGE, _mifname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _prjname: mapsyst.WTEXT, _scale: ctypes.POINTER(ctypes.c_int), _semnumber: ctypes.POINTER(ctypes.c_int), _rscininame: mapsyst.WTEXT, _rscsize: int, _codename: ctypes.c_char_p, _codesize: int, _incode: ctypes.POINTER(ctypes.c_int)) -> vecexapi.HMIFTOMAP:
        return mifInitLoadToMap_t (_handle, _mifname.buffer(), _rscname.buffer(), _prjname.buffer(), _scale, _semnumber, _rscininame.buffer(), _rscsize, _codename, _codesize, _incode)

    mifInitLoadToMapEx_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HMIFTOMAP,'mifInitLoadToMapEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mifInitLoadToMapEx(_handle: maptype.HMESSAGE, _mifname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _prjname: mapsyst.WTEXT, _scale: ctypes.POINTER(ctypes.c_int), _semnumber: ctypes.POINTER(ctypes.c_int), _rscininame: mapsyst.WTEXT, _rscsize: int, _codename: ctypes.c_char_p, _codesize: int, _codetype: ctypes.POINTER(ctypes.c_int), _incode: ctypes.POINTER(ctypes.c_int)) -> vecexapi.HMIFTOMAP:
        return mifInitLoadToMapEx_t (_handle, _mifname.buffer(), _rscname.buffer(), _prjname.buffer(), _scale, _semnumber, _rscininame.buffer(), _rscsize, _codename, _codesize, _codetype, _incode)


# Инициализировать класс для импорта файла формата MIF\MID
# issavemif  - флаг записи имени MIF в семантику объекта
# isdrawsave - флаг записи в семантику данных графических примитивов
# При ошибке возвращает ноль

    mifSetupLoadToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mifSetupLoadToMap', vecexapi.HMIFTOMAP, maptype.PWCHAR, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
    def mifSetupLoadToMap(_hmif: vecexapi.HMIFTOMAP, _mifname: mapsyst.WTEXT, _codename: ctypes.c_char_p, _semnumber: ctypes.POINTER(ctypes.c_int), _incode: ctypes.POINTER(ctypes.c_int), _issavemif: int, _isdrawsave: int) -> int:
        return mifSetupLoadToMap_t (_hmif, _mifname.buffer(), _codename, _semnumber, _incode, _issavemif, _isdrawsave)


# Выполнить импорт файла формата MIF\MID
# При ошибке возвращает ноль

    mifLoadToMapUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mifLoadToMapUn', vecexapi.HMIFTOMAP, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mifLoadToMapUn(_hmif: vecexapi.HMIFTOMAP, _hmap: maptype.HMAP, _mifname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _regname: mapsyst.WTEXT, _scale: int, _semnumber: int, _addflag: int, _ischangexy: int, _frec: int, _isutf8: int) -> int:
        return mifLoadToMapUn_t (_hmif, _hmap, _mifname.buffer(), _mapname.buffer(), _rscname.buffer(), _regname.buffer(), _scale, _semnumber, _addflag, _ischangexy, _frec, _isutf8)


# Удалить класс импорта и освободить ресурсы

    mifFreeLoadToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'mifFreeLoadToMap',vecexapi.HMIFTOMAP)
    def mifFreeLoadToMap(_hmif: vecexapi.HMIFTOMAP) -> ctypes.c_void_p:
        return mifFreeLoadToMap_t (_hmif)


#========================================================================
#   Функции импорта и экспорта формата S57
#========================================================================
# Для работы программы требуется классификатор s57navy.rsc
# Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
# Импорт из формата S57 в формат MAP или SIT (без вызова диалога)
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения WM_OBJECT и WM_ERROR (HWND для Windows, CALLBACK-Функция для Linux) или 0
# s57name - полный путь к файлу формата S57 (#.000 или #.030)
# mapname - полный путь к файлу создаваемой карты
# size    - размер буфера имени создаваемой карты, если имя может быть изменено в функции
# rscname - полное имя файла классификатора (s57navy.rsc)
# regionname - условное название создаваемой карты ("Море Лаптевых" и т.п.)
# safelystate - флаг создания границ зон безопасности (длительный процесс оверлейного анализа данных)
# При ошибке в параметрах возвращает ноль

    vecLoadS57ToMapUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecLoadS57ToMapUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def vecLoadS57ToMapUn(_handle: maptype.HMESSAGE, _s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _rscname: mapsyst.WTEXT, _regionname: mapsyst.WTEXT, _safelystate: int) -> int:
        return vecLoadS57ToMapUn_t (_handle, _s57name.buffer(), _mapname.buffer(), _size, _rscname.buffer(), _regionname.buffer(), _safelystate)


# Импорт всех файлов S57 из заданной папки в формат MAP/MPT
# handle  - идентификатор окна, которому посылаются сообщения WM_OBJECT и WM_ERROR
# folders57 - путь к папке для поиска файлов формата S57
# namemap - полное имя создаваемой карты
# namersc - полное имя файла классификатора (обычно S57NAVY.RSC)
# sittype  - тип создаваемых карт в проекте MPT или MAP (1- SIT; -1- SITX, 0 - MAP)
# password - пароль доступа к данным, из которого формируется 256-битный код
#            для шифрования данных (при утрате данные не восстанавливаются) или 0
# psize    - длина пароля в байтах или 0
# callevent - адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
# parm      - параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
# logfile   - путь к файлу журнала работы программы (может быть 0)
# При ошибке в параметрах возвращает ноль

    LoadS57FolderToMapEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadS57FolderToMapEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR)
    def LoadS57FolderToMapEx(_handle: maptype.HMESSAGE, _folders57: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _namersc: mapsyst.WTEXT, _sittype: int, _password: mapsyst.WTEXT, _psize: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT) -> int:
        return LoadS57FolderToMapEx_t (_handle, _folders57.buffer(), _namemap.buffer(), _size, _namersc.buffer(), _sittype, _password.buffer(), _psize, _callevent, _parm, _logfile.buffer())

    LoadS57FolderToMapUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadS57FolderToMapUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR)
    def LoadS57FolderToMapUn(_handle: maptype.HMESSAGE, _folders57: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _namersc: mapsyst.WTEXT, _sittype: int, _password: mapsyst.WTEXT, _psize: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT) -> int:
        return LoadS57FolderToMapUn_t (_handle, _folders57.buffer(), _namemap.buffer(), _namersc.buffer(), _sittype, _password.buffer(), _psize, _callevent, _parm, _logfile.buffer())


# Экспорт карты в формата S57 из формата MAP или SIT для карт, которые были ранее импортированы из S57
# Экспорт в S57 выполняется только из главной карты (hsite = hmap), каждый лист карты сохраняется
# в отдельный набор
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux)
# hmap    - идентификатор открытого документа, содержащего векторную карту
# hselect - условия отбора листов карты, которые будут сохранены в S57
# hdepth  - условия отбора отметок глубин (обычно все точечные объекты с кодом 129)
# s57name - полное имя файла формата S57 (#.030 или #.000)
# При ошибке в параметрах возвращает ноль

    vecSaveMapToS57Un_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecSaveMapToS57Un', maptype.HMESSAGE, maptype.HMAP, maptype.HSELECT, maptype.HSELECT, maptype.PWCHAR)
    def vecSaveMapToS57Un(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hselect: maptype.HSELECT, _hdepth: maptype.HSELECT, _s57name: mapsyst.WTEXT) -> int:
        return vecSaveMapToS57Un_t (_handle, _hmap, _hselect, _hdepth, _s57name.buffer())


# Импорт векторной карты из формата DXF
# dxfname - имя текстового файла DXF
# mapname - имя создаваемой или обновляемой векторной карты
# rscname - имя файла классификатора
# regionname - условное название карты
# parm    - параметры для процедуры импорта DXF
# handle  - идентификатор окна диалога для посылки сообщений
# isutf   - признак кодировки текстовых данных в UTF-8
# error   - код ошибки выполнения импорта
# При ошибке возвращает ноль

    vecLoadDxfToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecLoadDxfToMap', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(DXF2MAPPARMS), maptype.PWCHAR, maptype.HMESSAGE, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def vecLoadDxfToMap(_dxfname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _regionname: mapsyst.WTEXT, _parm: ctypes.POINTER(DXF2MAPPARMS), _custname: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _isutf: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return vecLoadDxfToMap_t (_dxfname.buffer(), _mapname.buffer(), _rscname.buffer(), _regionname.buffer(), _parm, _custname.buffer(), _handle, _isutf, _error)


# Экспорт в формат DXF
# hmap    - идентификатор открытых данных
# hsite   - идентификатор открытой пользовательской карты
# list    - номер листа карты с 1
# dxfname - имя текстового файла DXF
# dxlname - имя файла знаков или 0
# dxkname - имя файла кодов или 0
# handle  - идентификатор окна диалога для посылки сообщений WM_OBJECT и WM_ERROR
# parm    - параметры формирования файла DXF
# hselect - условия отбора объектов карты или 0
# Возвращает число корректно обработанных объектов листа карты
# При ошибке возвращает ноль

    vecSaveMapToDxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecSaveMapToDxfUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.HMESSAGE, ctypes.POINTER(PARMDXF), maptype.HSELECT)
    def vecSaveMapToDxfUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _dxfname: mapsyst.WTEXT, _dxlname: mapsyst.WTEXT, _dxkname: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(PARMDXF), _hselect: maptype.HSELECT) -> int:
        return vecSaveMapToDxfUn_t (_hmap, _hsite, _list, _dxfname.buffer(), _dxlname.buffer(), _dxkname.buffer(), _handle, _parm, _hselect)


#========================================================================
#              ТЕРРИТОРИАЛЬНОЕ ПЛАНИРОВАНИЕ
#========================================================================
# Создать карту по коду EPSG
# mapFile  - полное имя файла карты (MAP, SIT, SITX)
# rscFile  - полное имя файла ресурсов (RSC)
# epsgcode - код EPSG, для СК-42 зоны 2-32 : 28402-28432, для СК-95 зоны 4-32: 20004-20032
# scale    - знаменатель масштаба
# При ошибке возвращает ноль
    if os.name == 'nt':
        vecCreateMapByEPSG_t = mapsyst.GetProcAddress(vecexlib,maptype.HMAP,'vecCreateMapByEPSG', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
        def vecCreateMapByEPSG(_mapFile: mapsyst.WTEXT, _rscFile: mapsyst.WTEXT, _epsgcode: int, _scale: int) -> maptype.HMAP:
            return vecCreateMapByEPSG_t (_mapFile.buffer(), _rscFile.buffer(), _epsgcode, _scale)


# Экспорт набора данных карты в формат территориального планирования (GML)
# hmap       - объект доступа к данным
# hsite      - пользовательская карта на которую выполняется импорт
# handle     - идентификатор окна, которому посылаются сообщения WM_PROGRESSBAR
# flags - флаги условий формирования GML:
#         2 - запрет деления файла gml при наличии объектов разных локализаций (Line, Polygon, Point) в одном слое
#         4 - запрет деления мультиполигонов на полигоны
# saveLog    - включить запись в протокол
# epsgcode   - код EPSG с которым будет создан набор (3857)
# gmlfile    - полное имя результирующего файла GML
# fgistpFile - полное имя файла главной схемы территориального планирования (fgistp.xsd)
# docXsdFile - полное имя файла схемы текущего документа (Doc.XXXXXXXXX.xsd)
# При ошибке возвращает ноль

    if os.name == 'nt':
        terTerrplanToGML_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'terTerrplanToGML', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
        def terTerrplanToGML(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _flags: int, _saveLog: int, _epsgcode: int, _gmlfile: mapsyst.WTEXT, _fgistpFile: mapsyst.WTEXT, _docXsdFile: mapsyst.WTEXT) -> int:
            return terTerrplanToGML_t (_hmap, _hsite, _handle, _flags, _saveLog, _epsgcode, _gmlfile.buffer(), _fgistpFile.buffer(), _docXsdFile.buffer())


# Проверка корректности главной схемы (fgistpFile) территориального планирования
# xsdfile   - название файла fgistpFile
# rscfile   - название файла классификатора, если не задано то проверяется
#             корректность главной схемы
# buff      - буфер для размещения версии для fgistpFile
# bsize     - размер буфера buff
# Возвращает статус загруженной схемы или -1 (сбой классификатора)
# При ошибке возвращает ноль

    if os.name == 'nt':
        terCheckCommonSchemeTerrplan_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'terCheckCommonSchemeTerrplan', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
        def terCheckCommonSchemeTerrplan(_xsdfile: mapsyst.WTEXT, _rscfile: mapsyst.WTEXT, _buff: mapsyst.WTEXT, _bsize: int) -> int:
            return terCheckCommonSchemeTerrplan_t (_xsdfile.buffer(), _rscfile.buffer(), _buff.buffer(), _bsize)

        terCheckCommonSchemeTerrplanRSC_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'terCheckCommonSchemeTerrplanRSC', maptype.PWCHAR, maptype.HRSC, maptype.PWCHAR, ctypes.c_int)
        def terCheckCommonSchemeTerrplanRSC(_xsdfile: mapsyst.WTEXT, _hrsc: maptype.HRSC, _buff: mapsyst.WTEXT, _bsize: int) -> int:
            return terCheckCommonSchemeTerrplanRSC_t (_xsdfile.buffer(), _hrsc, _buff.buffer(), _bsize)


# Проверка корректности схем документа территориального планирования XML
# xsdfile   - название файла
# buff      - буфер для размещения названия схемы для Doc.XXXX
# bsize     - размер буфера buff
# При ошибке возвращает ноль

    if os.name == 'nt':
        terCheckDocSchemeTerrplan_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'terCheckDocSchemeTerrplan', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
        def terCheckDocSchemeTerrplan(_xsdfile: mapsyst.WTEXT, _buff: mapsyst.WTEXT, _bsize: int) -> int:
            return terCheckDocSchemeTerrplan_t (_xsdfile.buffer(), _buff.buffer(), _bsize)


#==============================================================================
# КОНВЕРТОР AIXM
#==============================================================================
# Проверка классфикатора на предмет принадлежности АНИ

    aniCheckAniRsc_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'aniCheckAniRsc', maptype.HRSC)
    def aniCheckAniRsc(_hrsc: maptype.HRSC) -> int:
        return aniCheckAniRsc_t (_hrsc)


# Проверить структуру файла AIXM
# Результат - тип данных:
# 0 - ошибка в данных
# 1 - данные маршрутной карты
# 2 - данные инфраструктуры аэродрома (метрика)
# 4 - данные инфраструктуры аэродрома (службы)
# 8 - справочные и табличные данные
# Результат формируется как объединение через операцию OR

    aixmCheckFile_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'aixmCheckFile', maptype.HMESSAGE, maptype.PWCHAR)
    def aixmCheckFile(_handle: maptype.HMESSAGE, _xmlFile: mapsyst.WTEXT) -> int:
        return aixmCheckFile_t (_handle, _xmlFile.buffer())


# Импорт информации на карту
# hMap, hSite  - рабочая карта
# handle - окно для сообщений передаётся текущая информация о статистике через LParam
# xmlFileName - файл AIXM
# region - регион ИКАО
# longlat- признак того, что координаты "вывернуты"
# mrkPos - создание подписей - см TMarkerPosition. Если параметр 0 подписи не создаются
# mrkDistM  - дистанция до маркера
# mrkPrec - точность координат в маркере
# isScanned - признак анализа файла: 0 - файл сначала сканируется, 1 - уже отсканирован
# Возвращает  количество обработанных объектов, при ошибке возвращает ноль

    aixmImportDataToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'aixmImportDataToMap', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def aixmImportDataToMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hMandle: maptype.HMESSAGE, _xmlFileName: mapsyst.WTEXT, _region: mapsyst.WTEXT, _longlat: int, _mrkPos: int, _mrkDistM: int, _mrkPrec: int, _isScanned: int = 0) -> int:
        return aixmImportDataToMap_t (_hMap, _hSite, _hMandle, _xmlFileName.buffer(), _region.buffer(), _longlat, _mrkPos, _mrkDistM, _mrkPrec, _isScanned)


# Экспорт инфомации из карты в формат AIXM
# hMap, hSite  - рабочая карта
# hSelect - набор данных, если 0- выгружается вся карта
# handle - окно для сообщений передаётся текущая информация о ходку экспорта
# xmlFileName - имя выходного AIXM-файла (если 0 - работа с памятью)
# isWFS - формат данных: 0-AIXM, 1-WFS
# startIndex - начальное значение счётчика gml; при экспорте единого блока данных
#              в несколько источников (файлов) нумерация объектов gml должна быть сплошной
# language - язык экспорта, указывается в теге "lang"
# isLatLong - порядок следования широты/долготы, если 0 - сначала долгота, потом широта
# writeMode - режим записи файла: 0 - новый автономный файл, 1-создать для дополнения,
#             2-дополнить, 3-дополнить и закрыть
# addOptimal - добавлять необязательные теги
# Возвращает  крайний идентификатор GML, при ошибке возвращает ноль

    aixmExportDataFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'aixmExportDataFromMap', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def aixmExportDataFromMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT, _Handle: maptype.HMESSAGE, _xmlFileName: mapsyst.WTEXT, _isWFS: int, _startIndex: int, _writeMode: int, _language: int, _isLatLong: int, _addOptimal: int) -> int:
        return aixmExportDataFromMap_t (_hMap, _hSite, _hSelect, _Handle, _xmlFileName.buffer(), _isWFS, _startIndex, _writeMode, _language, _isLatLong, _addOptimal)


#==============================================================================
# КОНВЕРТОР ARINC
#==============================================================================
# Открыть и просканировать файл ARINC
# При ошибке возвращает ноль

    arincOpenFileEx_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HARINC,'arincOpenFileEx', maptype.PWCHAR, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def arincOpenFileEx(_filename: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _mode: int, _animask: mapsyst.WTEXT, _masksize: int, _error: ctypes.POINTER(ctypes.c_int)) -> vecexapi.HARINC:
        return arincOpenFileEx_t (_filename.buffer(), _handle, _mode, _animask.buffer(), _masksize, _error)

    arincOpenFile_t = mapsyst.GetProcAddress(vecexlib,vecexapi.HARINC,'arincOpenFile', maptype.PWCHAR, maptype.HMESSAGE, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def arincOpenFile(_filename: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _handleDB: maptype.HMESSAGE, _mode: int, _animask: mapsyst.WTEXT, _masksize: int, _error: ctypes.POINTER(ctypes.c_int)) -> vecexapi.HARINC:
        return arincOpenFile_t (_filename.buffer(), _handle, _handleDB, _mode, _animask.buffer(), _masksize, _error)


# Импорт информации ARINC на карту
# arinc - идентификатор файла ARINC, полученный из arincOpenFileEx
# hMap, hSite  - рабочая карта
# handle - окно для сообщений передаётся текущая информация
# fileName - файл ARINC
# mrkPos - создание подписей - см TMarkerPosition. Если параметр равен 0 подписи не создаются
# mrkDistM  - дистанция до маркера
# mrkPrec - точность координат в маркере
# Если сканирование уже выполнено функцией arincOpenFile рекомендуется установить в 0

    arincDataToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'arincDataToMap', vecexapi.HARINC, maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def arincDataToMap(_arinc: vecexapi.HARINC, _hMap: maptype.HMAP, _hSite: maptype.HSITE, _handle: maptype.HMESSAGE, _fileName: mapsyst.WTEXT, _mask: int, _speedKMH: int, _mrkPos: int, _mrkDistM: int, _mrkPrec: int) -> int:
        return arincDataToMap_t (_arinc, _hMap, _hSite, _handle, _fileName.buffer(), _mask, _speedKMH, _mrkPos, _mrkDistM, _mrkPrec)


# Экспорт инфомации из карты в формат ARINC
# hmap, hsite  - рабочая карта
# handle - окно для сообщений передаётся текущая информация о ходку экспорта
# filename - имя выходного AIXM-файла (если 0 - работа с памятью)
# animask - маска экспортирумых данных
# Возвращает  количество обработанных объектов или ноль

    arincMapToData_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'arincMapToData', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def arincMapToData(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _animask: int, _uniondata: int, _addLog: int) -> int:
        return arincMapToData_t (_hmap, _hsite, _handle, _filename.buffer(), _animask, _uniondata, _addLog)


# Закрыть файл ARINC и освободить объект

    arincCloseFile_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'arincCloseFile', vecexapi.HARINC)
    def arincCloseFile(_arinc: vecexapi.HARINC) -> ctypes.c_void_p:
        return arincCloseFile_t (_arinc)


# Получить раскодированную информацию об ошибке

    arincGetError_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'arincGetError', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def arincGetError(_code: int, _wBuffer: mapsyst.WTEXT, _size: int, _addInfo: mapsyst.WTEXT) -> ctypes.c_void_p:
        return arincGetError_t (_code, _wBuffer.buffer(), _size, _addInfo.buffer())


#========================================================================
#   Функции записи в двоичный протокол результатов контроля
#========================================================================
# Открыть файл протокола (файл #.erx в папке \Log)
# handle  - идентификатор диалога, которому посылаются сообщения WM_PROGRESSBARUN
# hmap    - идентификатор открытых данных
# hsite   - идентификатор открытой пользовательской карты
# После завершения записи протокол должен быть закрыт функцией vecCloseErrorLog
# При ошибке возвращает ноль

    vecOpenErrorLog_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'vecOpenErrorLog', maptype.HMAP, maptype.HSITE)
    def vecOpenErrorLog(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return vecOpenErrorLog_t (_hmap, _hsite)


# Запись информации в файл протокола
# hcntr - идентификатор протокола, открытого функцией vecOpenErrorLog
# error - описание ошибки
# parm  - признак вывода информации об ошибке в текстовый протокол (#.err.txt)
# При ошибке возвращает ноль

    vecWriteDocErrorUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecWriteDocErrorUn', ctypes.c_void_p, ctypes.POINTER(maptype.ERRORINFOUN), ctypes.c_int)
    def vecWriteDocErrorUn(_hcntr: ctypes.c_void_p, _error: ctypes.POINTER(maptype.ERRORINFOUN), _parm: int) -> int:
        return vecWriteDocErrorUn_t (_hcntr, _error, _parm)


# Запись заголовка в файл протокола
# hcntr - идентификатор протокола, открытого функцией vecOpenErrorLog
# parm  - признак вывода информации об ошибке в текстовый протокол (#.err.txt)
# При ошибке возвращает ноль

    vecWriteDocTitleUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecWriteDocTitleUn', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_int)
    def vecWriteDocTitleUn(_hcntr: ctypes.c_void_p, _text: mapsyst.WTEXT, _parm: int) -> int:
        return vecWriteDocTitleUn_t (_hcntr, _text.buffer(), _parm)


# Закрыть файл протокола
# hcntr - идентификатор протокола, открытого функцией vecOpenErrorLog

    vecCloseErrorLog_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'vecCloseErrorLog', ctypes.c_void_p)
    def vecCloseErrorLog(_hcntr: ctypes.c_void_p) -> ctypes.c_void_p:
        return vecCloseErrorLog_t (_hcntr)


# Удаление файла протокола
# hcntr - идентификатор протокола, открытого функцией vecOpenErrorLog
# При ошибке возвращает ноль

    vecDeleteFileDocError_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecDeleteFileDocError', ctypes.c_void_p)
    def vecDeleteFileDocError(_hcntr: ctypes.c_void_p) -> int:
        return vecDeleteFileDocError_t (_hcntr)


# Проверка наличия файла протокола
# hcntr - идентификатор протокола, открытого функцией vecOpenErrorLog
# При ошибке возвращает ноль

    vecExistFileDocError_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecExistFileDocError', ctypes.c_void_p)
    def vecExistFileDocError(_hcntr: ctypes.c_void_p) -> int:
        return vecExistFileDocError_t (_hcntr)


#========================================================================
#   Функции чтения навигационных данных
#========================================================================
# Импорт навигационных данных формата NMEA 0183 из текстового файла
# handle  - идентификатор диалога, которому посылаются сообщения WM_PROGRESSBARUN
# hmap    - идентификатор открытых данных
# hsite   - идентификатор открытой пользовательской карты
# name    - имя текстового файла NMEA 0183
# incode  - внутренний код объекта из классификатора карты, для присвоения условного знака
# isline  - признак нанесения линейного объекта (маршрута), если равен 0 - наносятся точечные знаки
# step    - шаг фильтрации точек в метрах
# При ошибке возвращает ноль

    vecLoadGps_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecLoadGps', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def vecLoadGps(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _incode: int, _isline: int, _step: float) -> int:
        return vecLoadGps_t (_handle, _hmap, _hsite, _name.buffer(), _incode, _isline, _step)


# Импорт навигационных данных формата GPX на карту
# handle  - идентификатор диалога, которому посылаются сообщения WM_PROGRESSBARUN
# hmap    - идентификатор открытых данных
# hsite   - идентификатор открытой пользовательской карты
# name    - имя файла gpx
# pointincode - внутренний код объекта (условного знака) для записи точек ("wpt")
# lineincode - внутренний код объекта (условного знака) для записи маршрута ("trk")
# При ошибке возвращает ноль

    vecLoadGpx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecLoadGpx', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def vecLoadGpx(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _gpxname: mapsyst.WTEXT, _pointincode: int, _lineincode: int) -> int:
        return vecLoadGpx_t (_handle, _hmap, _hsite, _gpxname.buffer(), _pointincode, _lineincode)


# Пересчёт координат в текстовых файлах
# inname       - входной текстовый файл
# outname      - выходной текстовый файл
# parm         - параметры пересчёта координат в текстовых файлах
# handle       - идентификатор окна диалога для посылки сообщений
# directdatum  - параметры перехода от пользовательской системы координат к геодезической системе
#                на заданном эллипсоиде (обратное преобразование Гельмерта, или Coordinate Frame Rotation;
#                EPSG dataset coordinate operation method code 1032)
# directoutellipsoid - параметры эллипсоида выходной системы координат (0, если не требуется пересчёт по прямому датуму)
# Структуры LOCALDATUMPARAM и ELLIPSOIDPARAM описаны в mapcreat.h
# Если пересчет выполняется между пользовательскими системами координат (parm->InHuser и parm->OutHuser) через
# систему WGS84, то параметры directdatum и directoutellipsoid должны быть равны нулю
# Возвращает число обработанных строк входного файла
# При ошибке возвращает ноль

    vecTxtTranslate_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecTxtTranslate', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(TXTTRANSLATEPARM), maptype.HMESSAGE, ctypes.POINTER(mapcreat.LOCALDATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def vecTxtTranslate(_inname: mapsyst.WTEXT, _outname: mapsyst.WTEXT, _parm: ctypes.POINTER(TXTTRANSLATEPARM), _handle: maptype.HMESSAGE, _directdatum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM), _directellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return vecTxtTranslate_t (_inname.buffer(), _outname.buffer(), _parm, _handle, _directdatum, _directellipsoid)


# ================================================================
#                      УСТАРЕВШИЕ ФУНКЦИИ
#              Реализованы через вызов новых функций
# ================================================================
# Загрузить карту из файла SXF
# При ошибке возвращает ноль

    LoadSxfToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadSxfToMap', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def LoadSxfToMap(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return LoadSxfToMap_t (_namesxf, _namemap, _namersc, _handle)


# Загрузить карту из файла SXF с использованием Select
# При ошибке возвращает ноль

    LoadSxfToMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadSxfToMapSelect', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def LoadSxfToMapSelect(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return LoadSxfToMapSelect_t (_namesxf, _namemap, _namersc, _handle, _select)


# Загрузить карту из файла SXF с использованием Select
# и изменением имени карты
# Параметры name и namehdr - не обрабатываются
# При ошибке возвращает ноль

    LoadSxfToMapSelectName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadSxfToMapSelectName', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p, ctypes.c_char_p)
    def LoadSxfToMapSelectName(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _name: ctypes.c_char_p, _namehdr: ctypes.c_char_p) -> int:
        return LoadSxfToMapSelectName_t (_namesxf, _namemap, _namersc, _handle, _select, _name, _namehdr)


# Загрузить карту из файла TXF
# При ошибке возвращает ноль

    LoadTxtToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadTxtToMap', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def LoadTxtToMap(_nametxt: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return LoadTxtToMap_t (_nametxt, _namemap, _namersc, _handle)


# Загрузить карту из файла TXF с испльзованием Select
# При ошибке возвращает ноль

    LoadTxtToMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadTxtToMapSelect', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def LoadTxtToMapSelect(_nametxt: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return LoadTxtToMapSelect_t (_nametxt, _namemap, _namersc, _handle, _select)


# Загрузить карту из файла TXF с испльзованием Select и изменением имени
# Параметры name и namehdr - не обрабатываются
# При ошибке возвращает ноль

    LoadTxtToMapSelectName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadTxtToMapSelectName', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p, ctypes.c_char_p)
    def LoadTxtToMapSelectName(_nametxt: ctypes.c_char_p, _namemap: ctypes.c_char_p, _namersc: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _name: ctypes.c_char_p, _namehdr: ctypes.c_char_p) -> int:
        return LoadTxtToMapSelectName_t (_nametxt, _namemap, _namersc, _handle, _select, _name, _namehdr)


# Загрузить карту по списку DIR
# При ошибке возвращает ноль

    LoadDirToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadDirToMap', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def LoadDirToMap(_namedir: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return LoadDirToMap_t (_namedir, _namemap, _handle)


# Загрузить карту по списку DIR с использованием  Select
# При ошибке возвращает ноль

    LoadDirToMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadDirToMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def LoadDirToMapSelect(_namedir: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return LoadDirToMapSelect_t (_namedir, _namemap, _handle, _select)


# Загрузить карту по списку DIR с использованием  Select и
# изменением имени района и имени файла ресурсов
# При ошибке возвращает ноль

    LoadDirToMapSelectName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadDirToMapSelectName', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p, ctypes.c_char_p)
    def LoadDirToMapSelectName(_namedir: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _name: ctypes.c_char_p, _namersc: ctypes.c_char_p) -> int:
        return LoadDirToMapSelectName_t (_namedir, _namemap, _handle, _select, _name, _namersc)


# Загрузить карту по данным из другого района
# При ошибке возвращает ноль

    LoadMapToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadMapToMap', maptype.HMAP, ctypes.c_char_p, maptype.HMESSAGE)
    def LoadMapToMap(_map: maptype.HMAP, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return LoadMapToMap_t (_map, _namemap, _handle)


# Загрузить карту по данным другого района с использованием  Select
# При ошибке возвращает ноль

    LoadMapToMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'LoadMapToMapSelect', maptype.HMAP, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def LoadMapToMapSelect(_map: maptype.HMAP, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return LoadMapToMapSelect_t (_map, _namemap, _handle, _select)


# Обновить карту из файла SXF
# При ошибке возвращает ноль

    UpdateMapFromSxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapFromSxf', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def UpdateMapFromSxf(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return UpdateMapFromSxf_t (_namesxf, _namemap, _handle)


# Обновить карту из файла SXF с использованием Select
# При ошибке возвращает ноль

    UpdateMapFromSxfSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapFromSxfSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def UpdateMapFromSxfSelect(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return UpdateMapFromSxfSelect_t (_namesxf, _namemap, _handle, _select)


# Обновить карту по данным другого района с использованием  Select
# При ошибке возвращает ноль

    UpdateMapToMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapToMapSelect', maptype.HMAP, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def UpdateMapToMapSelect(_map: maptype.HMAP, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return UpdateMapToMapSelect_t (_map, _namemap, _handle, _select)


# Добавить в карту данные из файла SXF с использованием Select
# При ошибке возвращает ноль

    AppendMapFromSxfSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'AppendMapFromSxfSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def AppendMapFromSxfSelect(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return AppendMapFromSxfSelect_t (_namesxf, _namemap, _handle, _select)


# Обновить карту из файла TXF
# При ошибке возвращает ноль

    UpdateMapFromTxt_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapFromTxt', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def UpdateMapFromTxt(_nametxt: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return UpdateMapFromTxt_t (_nametxt, _namemap, _handle)


# Обновить карту из файла TXF с использованием Select
# При ошибке возвращает ноль

    UpdateMapFromTxtSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapFromTxtSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def UpdateMapFromTxtSelect(_nametxt: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return UpdateMapFromTxtSelect_t (_nametxt, _namemap, _handle, _select)


# Добавить в карту данные из файла TXF с использованием Select
# При ошибке возвращает ноль

    AppendMapFromTxtSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'AppendMapFromTxtSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def AppendMapFromTxtSelect(_namesxf: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return AppendMapFromTxtSelect_t (_namesxf, _namemap, _handle, _select)


# Обновить карту из файла DIR с использованием Select
# При ошибке возвращает ноль

    UpdateMapFromDirSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'UpdateMapFromDirSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def UpdateMapFromDirSelect(_namedir: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return UpdateMapFromDirSelect_t (_namedir, _namemap, _handle, _select)


# Добавить в карту данные из файла DIR с использованием Select
# При ошибке возвращает ноль

    AppendMapFromDirSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'AppendMapFromDirSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def AppendMapFromDirSelect(_namedir: ctypes.c_char_p, _namemap: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return AppendMapFromDirSelect_t (_namedir, _namemap, _handle, _select)


# Запросить паспортные данные векторной карты
# по имени файла SXF
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# При ошибке возвращает ноль

    mapGetSxfInfoByName_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetSxfInfoByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTER), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapGetSxfInfoByName(_name: ctypes.c_char_p, _map: ctypes.POINTER(mapcreat.MAPREGISTER), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapGetSxfInfoByName_t (_name, _map, _sheet)

    mapGetSxfInfoByNameEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'mapGetSxfInfoByNameEx', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapGetSxfInfoByNameEx(_name: ctypes.c_char_p, _map: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapGetSxfInfoByNameEx_t (_name, _map, _sheet)


# Загрузить (импортировать) карту из файла SXF, TXF или DIR с
# использованием Select с преобразованием топокарты к зоне документа
# Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
# hmap    - идентификатор открытой карты (рекомендуется указывать
#           для определения текущей зоны топокарты) или 0;
# sxfname - имя загружаемого файла типа SXF, TXF или DIR;
# rscname - имя файла классификатора, с которым загружается карта,
#           имя классификатора можно запросить из SXF (TXF) функцией GetRscNameFromSxf
#           или из карты; для файла DIR может быть 0;
# mapname - имя создаваемой карты (обычно совпадает с именем SXF (TXF))
#           или ноль или указатель на пустую строку (буфер размером MAX_PATH
#           c нулевым байтом равным нулю) или указатель на папку для размещения
#           карты. Если имя карты не задано или задана только папка, то карта
#           создается с именем SXF (TXF) и расширением ".sit". Если namemap
#           указывает на буфер достаточной длины (size), то в буфер записывается
#           имя созданной карты;
#           Для файла DIR тип общей карты - MPT (проект данных, включающий все
#           открытые карты из DIR) или MAP (многолистовая карта);
# size    - длина буфера, на который указывает переменная namemap, или 0. Обычно длина
#           равна MAX_PATH_LONG (1024);
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр загружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# Для добавления открытой карты в документ необходимо вызвать функцию
# mapAppendData(hmap, namemap). Если mapname содержит имя карты типа MAP и
# она содержит хотя бы один лист, то при импорте данных выполняется создание
# нового листа в карте MAP. В этом случае функция mapAppendData не должна вызываться.
# При ошибке возвращает ноль

    ImportFromAnySxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ImportFromAnySxf', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT)
    def ImportFromAnySxf(_hmap: maptype.HMAP, _sxfname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _mapname: ctypes.c_char_p, _size: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return ImportFromAnySxf_t (_hmap, _sxfname, _rscname, _mapname, _size, _handle, _select)


# Идентификатору окна посылаются следующие сообщения :
# WM_OBJECT = 0x585   WParam - процент обработанных объектов
# Сохранить (экспортировать) карту в двоичный формат SXF
# mapname - имя файла сохраняемой карты;
# list    - номер листа для многолистовой карты или 1;
# sxfname - имя создаваемого файла SXF, обычно совпадает с
#           именем карты, но имеет расширение SXF;
# flag    - вид хранимых координат (0 - метры, 4 - радианы
#           для карты, поддерживающей геодезические координаты,
#           -1 - определить по виду координат на карте);
#           Если карты не было в документе - она может быть создана (добавлена)
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр выгружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# Для топокарт, хранящих координаты в метрах, координаты всегда хранятся
# в зоне, указанной в паспорте карты
# При ошибке возвращает ноль

    ExportToSxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToSxf', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT)
    def ExportToSxf(_mapname: ctypes.c_char_p, _list: int, _sxfname: ctypes.c_char_p, _flag: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return ExportToSxf_t (_mapname, _list, _sxfname, _flag, _handle, _select)


# Сохранить (экспортировать) карту в формат DIR
# hmap    - идентификатор открытых данных
# dirname - имя создаваемого файла DIR, обычно совпадает с
#           именем открытого проекта или главной карты, но имеет расширение DIR;
# type    - тип создаваемых файлов (0 - SXF, 1 - TXF);
# flag    - вид хранимых координат (0 - метры, 4 - радианы, 8 - градусы,
#           для карты, поддерживающей геодезические координаты,
#           -1 - определить по виду координат на карте);
#           Если карты не было в документе - она может быть создана (добавлена)
# total   - признак сохранения в DIR только главной карты (0) или всех карт
#           документа (1);
# precision - для файлов TXF число знаков после запятой для координат в метрах или 0;
#           если карта имеет паспортную точность в см (2 знака) или
#           в мм (3 знака), то precision игнорируется;
# handle  - идентификатор окна диалога, которому посылаются уведомительные
#           сообщения (HWND для Windows, CALLBACK-Функция для Linux);
# select  - фильтр выгружаемых объектов и слоев, если необходима выборочная
#           обработка данных;
# Для топокарт, хранящих координаты в метрах, координаты всегда хранятся
# в зоне, указанной в паспорте карты
# При ошибке возвращает ноль

    ExportToDir_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'ExportToDir', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.HSELECT)
    def ExportToDir(_hmap: maptype.HMAP, _dirname: ctypes.c_char_p, _type: int, _flag: int, _total: int, _precision: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return ExportToDir_t (_hmap, _dirname, _type, _flag, _total, _precision, _handle, _select)


# Выгрузка из внутреннего формата в формат SXF(Windows)
# При ошибке возвращает ноль

    SaveSxfFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveSxfFromMap', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveSxfFromMap(_namemap: ctypes.c_char_p, _list: int, _namesxf: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveSxfFromMap_t (_namemap, _list, _namesxf, _handle)


# Выгрузка из внутреннего формата в формат SXF(Windows) с
# использованием  Select
#  flag = 0 - данные в метрах
#  flag = 4 - данные в радианах
# При ошибке возвращает ноль

    SaveSxfFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveSxfFromMapSelect', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_char_p)
    def SaveSxfFromMapSelect(_namemap: ctypes.c_char_p, _list: int, _namesxf: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _flag: int = 0, _nameregion: ctypes.c_char_p = None) -> int:
        return SaveSxfFromMapSelect_t (_namemap, _list, _namesxf, _handle, _select, _flag, _nameregion)


# Выгрузка из внутреннего формата в формат SXF(Windows) с
# использованием  Select
# При ошибке возвращает ноль

    SaveSxfFromHMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveSxfFromHMapSelect', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, ctypes.c_char_p)
    def SaveSxfFromHMapSelect(_map: maptype.HMAP, _list: int, _namesxf: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _flag: int = 0, _nameregion: ctypes.c_char_p = None) -> int:
        return SaveSxfFromHMapSelect_t (_map, _list, _namesxf, _handle, _select, _flag, _nameregion)

    SaveSxfFromHMapSelectUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveSxfFromHMapSelectUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_int, maptype.PWCHAR)
    def SaveSxfFromHMapSelectUn(_map: maptype.HMAP, _list: int, _namesxf: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _flag: int = 0, _nameregion: mapsyst.WTEXT = None) -> int:
        return SaveSxfFromHMapSelectUn_t (_map, _list, _namesxf.buffer(), _handle, _select, _flag, _nameregion.buffer())


# Выгрузка из внутреннего формата в формат TXT(XY)
# При ошибке возвращает ноль

    SaveTxtFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtFromMap', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveTxtFromMap(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveTxtFromMap_t (_namemap, _list, _nametxt, _handle)


# Выгрузка из внутреннего формата в формат TXF(XY) с
# использованием Select
# При ошибке возвращает ноль

    SaveTxtFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtFromMapSelect', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p)
    def SaveTxtFromMapSelect(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _nameregion: ctypes.c_char_p = None) -> int:
        return SaveTxtFromMapSelect_t (_namemap, _list, _nametxt, _handle, _select, _nameregion)


# Выгрузка из внутреннего формата в формат TXF(XY) с
# использованием Select
# namemap - имя выгружаемой карты,
# list    - номер листа,
# nametxt - имя файла TXF,
# handle  - идентификатор окна, которому посылаются сообщения о ходе процесса
#           (WM_INFOLIST, WM_OBJECT)
# select  - идентификатор условий поиска объектов, определяющий список
#           экспортируемых в текстовый файл объектов,
# nameregion - имя района (карты),
# precision  - число знаков после запятой для прямоугольных координат
# При ошибке возвращает ноль

    SaveTxtFromMapSelectEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtFromMapSelectEx', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def SaveTxtFromMapSelectEx(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _nameregion: ctypes.c_char_p, _precision: int) -> int:
        return SaveTxtFromMapSelectEx_t (_namemap, _list, _nametxt, _handle, _select, _nameregion, _precision)


# Выгрузка из внутреннего формата в формат TXF(BL)
# При ошибке возвращает ноль

    SaveTxtGeoFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtGeoFromMap', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveTxtGeoFromMap(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveTxtGeoFromMap_t (_namemap, _list, _nametxt, _handle)


# Выгрузка из внутреннего формата в формат TXF(BL) с
# использованием Select
# При ошибке возвращает ноль

    SaveTxtGeoFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtGeoFromMapSelect', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p)
    def SaveTxtGeoFromMapSelect(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _nameregion: ctypes.c_char_p = None) -> int:
        return SaveTxtGeoFromMapSelect_t (_namemap, _list, _nametxt, _handle, _select, _nameregion)

    SaveTxtGeoGradFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveTxtGeoGradFromMapSelect', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_char_p)
    def SaveTxtGeoGradFromMapSelect(_namemap: ctypes.c_char_p, _list: int, _nametxt: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _nameregion: ctypes.c_char_p = None) -> int:
        return SaveTxtGeoGradFromMapSelect_t (_namemap, _list, _nametxt, _handle, _select, _nameregion)


# Выгрузка из внутреннего формата в формат SXF(WINDOWS) по DIR
# При ошибке возвращает ноль

    SaveDirSxfFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirSxfFromMap', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveDirSxfFromMap(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveDirSxfFromMap_t (_namemap, _namedir, _handle)


# Выгрузка из внутреннего формата в формат SXF(WINDOWS) по DIR
# с использованием Select
# При ошибке возвращает ноль

    SaveDirSxfFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirSxfFromMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def SaveDirSxfFromMapSelect(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return SaveDirSxfFromMapSelect_t (_namemap, _namedir, _handle, _select)


# Выгрузка из внутреннего формата в формат SXF(WINDOWS) по DIR
# с использованием Select
# При ошибке возвращает ноль

    SaveDirSxfIntFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirSxfIntFromMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def SaveDirSxfIntFromMapSelect(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return SaveDirSxfIntFromMapSelect_t (_namemap, _namedir, _handle, _select)


# Выгрузка из внутреннего формата в формат TXF(XY) по DIR
# При ошибке возвращает ноль

    SaveDirTxtFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirTxtFromMap', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveDirTxtFromMap(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveDirTxtFromMap_t (_namemap, _namedir, _handle)


# Выгрузка из внутреннего формата в формат TXF(XY) по DIR
# с использованием Select
# При ошибке возвращает ноль

    SaveDirTxtFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirTxtFromMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def SaveDirTxtFromMapSelect(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return SaveDirTxtFromMapSelect_t (_namemap, _namedir, _handle, _select)


# Выгрузка из внутреннего формата в формат TXF(BL) по DIR
# При ошибке возвращает ноль

    SaveDirTxtGeoFromMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirTxtGeoFromMap', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE)
    def SaveDirTxtGeoFromMap(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE) -> int:
        return SaveDirTxtGeoFromMap_t (_namemap, _namedir, _handle)


# Выгрузка из внутреннего формата в формат TXF(BL) по DIR
# с использованием Select
# При ошибке возвращает ноль

    SaveDirTxtGeoFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirTxtGeoFromMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def SaveDirTxtGeoFromMapSelect(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return SaveDirTxtGeoFromMapSelect_t (_namemap, _namedir, _handle, _select)


# Выгрузка из внутреннего формата в формат TXF(BL градусы) по DIR
# с использованием Select
# При ошибке возвращает ноль

    SaveDirTxtGeoGradFromMapSelect_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveDirTxtGeoGradFromMapSelect', ctypes.c_char_p, ctypes.c_char_p, maptype.HMESSAGE, maptype.HSELECT)
    def SaveDirTxtGeoGradFromMapSelect(_namemap: ctypes.c_char_p, _namedir: ctypes.c_char_p, _handle: maptype.HMESSAGE, _select: maptype.HSELECT) -> int:
        return SaveDirTxtGeoGradFromMapSelect_t (_namemap, _namedir, _handle, _select)


# Получение справочной информации о листе из SXF
# При ошибке возвращает ноль

    GetInfoSxf_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetInfoSxf', ctypes.c_char_p, ctypes.POINTER(mmstruct.INFOSXF))
    def GetInfoSxf(_namesxf: ctypes.c_char_p, _infosxf: ctypes.POINTER(mmstruct.INFOSXF)) -> int:
        return GetInfoSxf_t (_namesxf, _infosxf)


# Получение справочной информации из DIR
# При ошибке возвращает ноль

    GetInfoDir_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetInfoDir', ctypes.c_char_p, ctypes.POINTER(mmstruct.INFODIR))
    def GetInfoDir(_namedir: ctypes.c_char_p, _infodir: ctypes.POINTER(mmstruct.INFODIR)) -> int:
        return GetInfoDir_t (_namedir, _infodir)


# Получение списка файлов SXF в DIR
# При ошибке возвращает ноль

    GetDir_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'GetDir', ctypes.c_char_p, ctypes.POINTER(mmstruct.NAMESARRAY), ctypes.c_int)
    def GetDir(_namedir: ctypes.c_char_p, _sxfdir: ctypes.POINTER(mmstruct.NAMESARRAY), _length: int) -> int:
        return GetDir_t (_namedir, _sxfdir, _length)


# Загрузка фотографий в формате JPEG с координатной привязкой к местности
# hmap         - идентификатор открытых данных
# sourcedir    - исходная директория с фотографиями
# handle       - идентификатор окна диалога процесса обработки (HWND для Windows)
#                Окну диалога посылаются следующие сообщения :
# WM_PROGRESSBARUN
#                 WPARAM - текущее состояние процесса в процентах (0% - 100%)
# WM_ERROR      - сообщение об ошибке для увеличения счетчика ошибок
# AW_MESSAGEBOX - по завершению загрузки отображается всплывающее сообщение
#                 WPARAM - текст сообщения: количество добавленных фотографий,
#                 LPARAM - заголовок сообщения
# Карта с фотографиями автоматически создается и добавляется к списку карт
# Если карта уже существует, то перед загрузкой выдается сообщение: "Дополнить карту?" -
# При нажатии на кнопку «Да» новые фотографии будут добавлены к существующим фотографиям карты,
# иначе – существующие фотографии карты будут заменены на новые фотографии
# Для создания карты используется классификатор service.rsc
# Возвращает количество загруженных фотографий
# При ошибке возвращает 0

    vecLoadPhoto_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'vecLoadPhoto', maptype.HMAP, maptype.PWCHAR, maptype.HMESSAGE)
    def vecLoadPhoto(_hMap: maptype.HMAP, _sourcedir: mapsyst.WTEXT, _handle: maptype.HMESSAGE) -> int:
        return vecLoadPhoto_t (_hMap, _sourcedir.buffer(), _handle)

# Экспорт изображения карты в формат SVG
# Изображение формируется в базовом масштабе карты с заданным разрешением
# handle  - идентификатор диалога, которому посылаются сообщения WM_PROGRESSBARUN
# hmap    - идентификатор открытых данных
# hsite   - идентификатор открытой пользовательской карты
# hselect  - фильтр загружаемых объектов и слоев, если необходима выборочная обработка данных
# svgname - имя создаваемого файла SVG
# precision - число точек на метр изображения
# error - поле для записи кода ошибки (см. maperr.rh)
# При ошибке во входных данных возвращает ноль

    SaveMapToSVG_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_int,'SaveMapToSVG', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE , 
                        maptype.HSELECT, ctypes.POINTER(maptype.WCHAR),ctypes.c_double, ctypes.POINTER(ctypes.c_long))
    def SaveMapToSVG(_hMessage: maptype.HMESSAGE, _hMap: maptype.HMAP, _hSite:maptype.HSITE, 
                     _hSelect:maptype.HSELECT, _svgname:ctypes.POINTER(maptype.WCHAR), 
                     _precision: ctypes.c_double, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return SaveMapToSVG_t (_hMessage, _hMap, _hSite, _hSelect, _svgname, _precision, _error)

except Exception as e:
    print(e)
    vecexlib = 0
