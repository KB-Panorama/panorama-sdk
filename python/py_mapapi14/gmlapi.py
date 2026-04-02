#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype

PACK_WIDTH = 1

#-----------------------------
class FEATURELIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Xmlns",ctypes.c_int),
                ("Hmap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Hselect",maptype.HSELECT),
                ("Hwnd",maptype.HMESSAGE),
                ("Hobj",maptype.HOBJ),
                ("SemCodeList",ctypes.POINTER(ctypes.c_int)),
                ("Statistic",ctypes.c_void_p),
                ("Dframe",maptype.DFRAME),
                ("Extend",maptype.DFRAME),
                ("Scale",ctypes.c_double),
                ("Flags",ctypes.c_int),
                ("List",ctypes.c_int),
                ("Completed",ctypes.c_int),
                ("Force",ctypes.c_int),
                ("Number",ctypes.c_uint),
                ("Count",ctypes.c_uint),
                ("Epsgcode",ctypes.c_uint),
                ("Format",ctypes.c_uint),
                ("ObjectCreateLastStep",ctypes.c_uint),
                ("MathMetod",ctypes.c_uint),
                ("ServiceVersion",ctypes.c_int),
                ("TransactionType",ctypes.c_int),
                ("FindDirection",ctypes.c_int),
                ("SemCodeListCount",ctypes.c_uint),
                ("PrintEpsg",ctypes.c_int),
                ("Test",ctypes.c_int),
                ("ClickPoint",maptype.DOUBLEPOINT),
                ("SortList",ctypes.c_void_p),
                ("SemSortCode",ctypes.c_int),
                ("MultyLevelScale",ctypes.c_int),
                ("ClickPointFrame",maptype.DFRAME),
                ("Reserve",ctypes.c_char*152)]
#-----------------------------


#-----------------------------
class GMLPARAMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hwnd",maptype.HMESSAGE),
                ("SquareCode",ctypes.c_int),
                ("PointCode",ctypes.c_int),
                ("LineCode",ctypes.c_int),
                ("TextCode",ctypes.c_int),
                ("Protocol",ctypes.c_int),
                ("SavedObjectNumber",ctypes.c_int),
                ("TurnCoordinate",ctypes.c_int),
                ("CutObjects",ctypes.c_int),
                ("Reserve",ctypes.c_char*84)]
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary( gisaccesname )

# Открыть доступ к схеме для потокового формирования GML\JSON
# Если классификатор размещен на ГИС Сервере, то схема открывается через
# идентификатор карты (gmlOpen, gmlOpenEx, gmlOpenUn)
# schemafilename - локальный путь к файлу XSD-схемы
# rscname        - локальный путь к файлу классификатору RSC,
#                  с которым связаны карты, планируемые к обработке
# hrsc - идентификатор классификатора (может быть получен в mapGetRscIdent, mapGetRscIdentByObject)
# Возвращает идентификатор доступа к GML данным
# При ошибке возвращает ноль

#   gmlOpenPro_t = mapsyst.GetProcAddress(acceslib,HGML,'gmlOpenPro', maptype.PWCHAR, maptype.PWCHAR)
#   def gmlOpenPro(_schemafilename: mapsyst.WTEXT, _rscname: mapsyst.WTEXT) -> HGML:
#       return gmlOpenPro_t (_schemafilename.buffer(), _rscname.buffer())

#   gmlOpenProEx_t = mapsyst.GetProcAddress(acceslib,HGML,'gmlOpenProEx', maptype.PWCHAR, maptype.HRSC)
#   def gmlOpenProEx(_schemafilename: mapsyst.WTEXT, _hrsc: maptype.HRSC) -> HGML:
#       return gmlOpenProEx_t (_schemafilename.buffer(), _hrsc)


# Открыть доступ к прикладной схеме для заданной карты
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# schemafilename - локальный путь к файлу XSD-схемы GML данных
# schemaURL      - URL к файлу XSD-схемы GML данных
#                  например: "http:#www.gisinfo.net/bsd/topomap.xsd"
# Возвращает идентификатор доступа к прикладной схеме
# Для записи набора (dataset) функцией gmlGetFeaturiesDataset
# доступ к схеме открывается gmlOpenEx
# По завершении работы необходимо освободить ресурсы вызовом gmlClose
# При ошибке возвращает ноль

#   gmlOpen_t = mapsyst.GetProcAddress(acceslib,HGML,'gmlOpen', maptype.HMAP, ctypes.c_char_p)
#   def gmlOpen(_hmap: maptype.HMAP, _schemafilename: ctypes.c_char_p) -> HGML:
#       return gmlOpen_t (_hmap, _schemafilename)

#   gmlOpenEx_t = mapsyst.GetProcAddress(acceslib,HGML,'gmlOpenEx', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_char_p)
#   def gmlOpenEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _schemafilename: ctypes.c_char_p, _schemaURL: ctypes.c_char_p) -> HGML:
#       return gmlOpenEx_t (_hmap, _hsite, _schemafilename, _schemaURL)

#   gmlOpenUn_t = mapsyst.GetProcAddress(acceslib,HGML,'gmlOpenUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR)
#   def gmlOpenUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _schemafilename: mapsyst.WTEXT, _schemaURL: mapsyst.WTEXT) -> HGML:
#       return gmlOpenUn_t (_hmap, _hsite, _schemafilename.buffer(), _schemaURL.buffer())


# Установить адрес схемы
# hgml - идентификатор
# schemaLocation - новый адрес схемы
# При ошибке возвращает ноль

#   gmlSetSchemaLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSetSchemaLocation', HGML, maptype.PWCHAR)
#   def gmlSetSchemaLocation(_hgml: HGML, _schemaLocation: mapsyst.WTEXT) -> int:
#       return gmlSetSchemaLocation_t (_hgml, _schemaLocation.buffer())


# Закрыть доступ к схеме и освободить ресурсы
# hgml - идентификатор GML данных

#   gmlClose_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlClose', HGML)
#   def gmlClose(_hgml: HGML) -> ctypes.c_void_p:
#       return gmlClose_t (_hgml)


# Запросить число типов объектов GML данных ("слоев")
# Возвращает число типов объектов GML, содержащихся в схеме
# При ошибке возвращает ноль

#   gmlFeatureTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlFeatureTypeCount', HGML)
#   def gmlFeatureTypeCount(_hgml: HGML) -> int:
#       return gmlFeatureTypeCount_t (_hgml)


# Запросить порядковый номер типа объекта по имени типа
# hgml - идентификатор открытой схемы для записи GML
# featuretypename - имя типа объекта GML данных
# Возвращает порядковый номер типа объекта в схеме
# При ошибке возвращает ноль

#   gmlFeatureTypeNameNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlFeatureTypeNameNumber', HGML, ctypes.c_char_p)
#   def gmlFeatureTypeNameNumber(_hgml: HGML, _featuretypename: ctypes.c_char_p) -> int:
#       return gmlFeatureTypeNameNumber_t (_hgml, _featuretypename)


# Запросить габариты объектов карты по списку номеров типов объектов
# hgml  - идентификатор GML данных
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# list  - номер обрабатываемого листа на многолистовой карте или 0 (все листы)
# hselect - идентификатор условий отбора объектов или 0
# epsgcode - код геодезической системы координат в базе данных EPSG, для GML по умолчанию - 4326
# dframe - габариты объектов карты в указанной системе координат
# При ошибке возвращает ноль.

#   gmlFeaturiesBoundsPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlFeaturiesBoundsPro', HGML, maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HSELECT, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
#   def gmlFeaturiesBoundsPro(_hgml: HGML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
#       return gmlFeaturiesBoundsPro_t (_hgml, _hmap, _hsite, _list, _hselect, _epsgcode, _dframe)


# Запросить данные объектов карты по заданным условиям в файле формата GML или JSON
# hgml - идентификатор открытой схемы для записи GML
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# list  - номер листа для многолистовой карты или 1, для конвертирования
#         в один GML-файл сразу всех листов необходимо указать "-1" или 0
# hselect - идентификатор условий отбора объектов или 0
# number - порядковый номер объекта, с которого начинать вывод в файл (с 1)
# count - число объектов, выводимых в файл, если равно 0, то выводятся все объекты
# epsgcode - код геодезической системы координат в базе данных EPSG,
# для GML по умолчанию - 4326
# dframe - бласть отбора объектов карты в указанной системе координат или 0 (левый нижний и правый верхний угол области)
# format - тип разметки или формат файла: GML, GML/WFS, JSON  (см. OGCSERVICETYPE)
# targetfilename - имя выходного файла
# flags - флажки вывода расширенных метаданных об объекте (см. OGCSERVICEFLAG)
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# mapid  - указатель на идентификатор карты, который записывается в каждый объект карты или 0
# completed - признак необходимости записи элементов начала и конца файла
#             (0 - не формировать, 1 - только закрывающий, 2 - только начальные теги, -1 - начало и конец данных)
#             при значении 0 и 1 файл для записи должен существовать, при значении 2 и -1 файл создается автоматически
# JSON - { "type": "FeatureCollection",    ... }
# GML  - <gml:FeatureCollection> ... </gml:FeatureCollection>
# WFS  - <wfs:FeatureCollection> ... </wfs:FeatureCollection>
# force - признак принудительной записи объектов, которые не описаны в прикладной схеме,
#         если равен нулю, то записываются только объекты, виды (коды) которых описаны в схеме
# hwnd - идентификатор окна для приема сообщений или ноль, посылаются сообщения WM_OBJECT (%, число объектов)
# requestId - идентификатор запроса
# xmlns - признак записи пространства имен в тег member для gml/wfs
# secondframe - дополнительные точки для области отбора объектов карты в указанной системе координат
# (подается дополнительно к dframe, левый верхний и правый нижний угол области)
# Возвращает число записанных объектов
# Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1
# Если условиям поиска не соответствует ни один объект, то возвращает -2
# Если выходной файл не может быть открыт, то возвращает -3
# Если произошел сбой при работе программы, то возвращает -4
# Если для карты запрещено копирование, то возвращает -5

#   gmlGetFeaturiesPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesPro', HGML, maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HSELECT, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int)
#   def gmlGetFeaturiesPro(_hgml: HGML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _metadata: mapsyst.WTEXT, _number: int, _count: int, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _force: int, _hwnd: maptype.HMESSAGE, _requestId: mapsyst.WTEXT = None, _xmlns: int = 0) -> int:
#       return gmlGetFeaturiesPro_t (_hgml, _hmap, _hsite, _list, _hselect, _metadata.buffer(), _number, _count, _epsgcode, _dframe, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _force, _hwnd, _requestId.buffer(), _xmlns)

#   gmlGetFeaturiesProEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesProEx', HGML, maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HSELECT, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
#   def gmlGetFeaturiesProEx(_hgml: HGML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _metadata: mapsyst.WTEXT, _number: int, _count: int, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _force: int, _hwnd: maptype.HMESSAGE, _requestId: mapsyst.WTEXT = None, _xmlns: int = 0, _secondframe: ctypes.POINTER(maptype.DFRAME) = None) -> int:
#       return gmlGetFeaturiesProEx_t (_hgml, _hmap, _hsite, _list, _hselect, _metadata.buffer(), _number, _count, _epsgcode, _dframe, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _force, _hwnd, _requestId.buffer(), _xmlns, _secondframe)

#   gmlGetFeaturiesList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesList', HGML, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(FEATURELIST))
#   def gmlGetFeaturiesList(_hgml: HGML, _metadata: mapsyst.WTEXT, _targetfilename: mapsyst.WTEXT, _requestId: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _featurelist: ctypes.POINTER(FEATURELIST)) -> int:
#       return gmlGetFeaturiesList_t (_hgml, _metadata.buffer(), _targetfilename.buffer(), _requestId.buffer(), _mapid.buffer(), _featurelist)


# Запросить данные объектов карты по заданным условиям в памяти в формате GML или JSON
# Для чтения из памяти результата необходимо вызвать gmlGetFeaturiesPoint
# После завершения чтения необходимо освободить память вызовом gmlFreeFeaturiesPoint
# Если объем данных слишком большой, то функция может занять всю память в системе
# Назначение параметров аналогично функции gmlGetFeaturiesPro
# xmlns - признак записи пространства имен в тег member для gml/wfs
# Возвращает в параметре retcode число записанных объектов или код ошибки
# Если заданы слои, содержащие объекты, которых нет на карте, то записывает -1
# Если условиям поиска не соответствует ни один объект, то записывает -2
# Если произошел сбой при работе программы, то записывает -4
# Если для карты запрещено копирование, то записывает -5
# При ошибке возвращает ноль иначе идентификатор данных в памяти

#   gmlGetFeaturiesProInMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlGetFeaturiesProInMemory', HGML, maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HSELECT, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
#   def gmlGetFeaturiesProInMemory(_hgml: HGML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _metadata: mapsyst.WTEXT, _number: int, _count: int, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flags: int, _format: int, _mapid: mapsyst.WTEXT, _completed: int, _force: int, _retcode: ctypes.POINTER(ctypes.c_int), _requestId: mapsyst.WTEXT = None, _xmlns: int = 0) -> ctypes.c_void_p:
#       return gmlGetFeaturiesProInMemory_t (_hgml, _hmap, _hsite, _list, _hselect, _metadata.buffer(), _number, _count, _epsgcode, _dframe, _flags, _format, _mapid.buffer(), _completed, _force, _retcode, _requestId.buffer(), _xmlns)


# Освободить память под данные по идентификатору данных,
# полученному из функции gmlGetFeaturiesProInMemory или gmlGetObjectFeatureProInMemory

    gmlFreeFeaturiesPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeFeaturiesPoint', ctypes.c_void_p)
    def gmlFreeFeaturiesPoint(_handle: ctypes.c_void_p) -> ctypes.c_void_p:
        return gmlFreeFeaturiesPoint_t (_handle)


# Запросить данные объекта карты в файле формата GML или JSON
# hgml - идентификатор открытой схемы для записи GML (может быть равен нулю)
# hobj - идентификатор объекта карты в памяти
# epsgcode - код геодезической системы координат в базе данных EPSG
# flags - флажки вывода расширенных метаданных об объекте (см. OGCSERVICEFLAG)
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# targetfilename - имя выходного GML или JSON файла
# mapid  - указатель на идентификатор карты, который записывается в каждый объект карты или 0
# requestId - идентификатор запроса для записи в метаданные
# xmlns - признак записи пространства имен в тег member для gml/wfs
# При ошибке возвращает ноль

#   gmlGetObjectFeaturePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetObjectFeaturePro', HGML, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
#   def gmlGetObjectFeaturePro(_hgml: HGML, _hobj: maptype.HOBJ, _epsgcode: int, _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _requestId: mapsyst.WTEXT = None, _xmlns: int = 0) -> int:
#       return gmlGetObjectFeaturePro_t (_hgml, _hobj, _epsgcode, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _requestId.buffer(), _xmlns)

#   gmlGetObjectFeatureList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetObjectFeatureList', HGML, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(FEATURELIST))
#   def gmlGetObjectFeatureList(_hgml: HGML, _metadata: mapsyst.WTEXT, _targetfilename: mapsyst.WTEXT, _requestId: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _featurelist: ctypes.POINTER(FEATURELIST)) -> int:
#       return gmlGetObjectFeatureList_t (_hgml, _metadata.buffer(), _targetfilename.buffer(), _requestId.buffer(), _mapid.buffer(), _featurelist)


# Запросить данные объекта карты в памяти в формате GML или JSON
# Для чтения из памяти результата необходимо вызвать gmlGetFeaturiesPoint
# После завершения чтения необходимо освободить память вызовом gmlFreeFeaturiesPoint
# Для дозаписи в память новых объектов параметр handle должен содержать
# значение, которая вернула функция при первом вызове, когда параметр handle был равен 0
# Возвращает в параметре retcode число записанных объектов или код ошибки
# Если заданы слои, содержащие объекты, которых нет на карте, то записывает -1
# Если условиям поиска не соответствует ни один объект, то записывает -2
# Если произошел сбой при работе программы, то записывает -4
# Если для карты запрещено копирование, то записывает -5
# При ошибке возвращает ноль иначе идентификатор данных в памяти

#   gmlGetObjectFeatureProInMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlGetObjectFeatureProInMemory', HGML, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
#   def gmlGetObjectFeatureProInMemory(_hgml: HGML, _hobj: maptype.HOBJ, _epsgcode: int, _flags: int, _format: int, _handle: ctypes.c_void_p, _mapid: mapsyst.WTEXT, _completed: int, _retcode: ctypes.POINTER(ctypes.c_int), _requestId: mapsyst.WTEXT = None, _xmlns: int = 0) -> ctypes.c_void_p:
#       return gmlGetObjectFeatureProInMemory_t (_hgml, _hobj, _epsgcode, _flags, _format, _handle, _mapid.buffer(), _completed, _retcode, _requestId.buffer(), _xmlns)


# Запросить данные объекта карты по GML-идентификатору
# hgml - идентификатор открытой схемы для записи GML
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# epsgcode - код геодезической системы координат в базе данных EPSG
# id - GML-идентификатор объекта
# flags - флажки вывода расширенных метаданных об объекте (см. OGCSERVICEFLAG)
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# targetfilename - имя выходного файла
# mapid  - указатель на идентификатор карты, который записывается в каждый объект карты или 0
# completed - признак необходимости записи элементов начала и конца файла
#             (0 - не формировать, 1 - только закрывающий, 2 - только начальные теги, -1 - начало и конец данных)
# JSON - { "type": "FeatureCollection",    ... }
# GML  - <gml:FeatureCollection> ... </gml:FeatureCollection>
# WFS  - <wfs:FeatureCollection> ... </wfs:FeatureCollection>
# При ошибке возвращает ноль

#   gmlGetFeatureByIdPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeatureByIdPro', HGML, maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
#   def gmlGetFeatureByIdPro(_hgml: HGML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _epsgcode: int, _id: ctypes.c_char_p, _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _requestId: mapsyst.WTEXT = None) -> int:
#       return gmlGetFeatureByIdPro_t (_hgml, _hmap, _hsite, _list, _epsgcode, _id, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _requestId.buffer())


# Преобразовать координаты рамки из одной геодезической системы координат
# в другую геодезическую систему координат
# epsgcodesource - код исходной геодезической системы координат в базе данных EPSG,
# epsgcodedest - код выходной геодезической системы координат в базе данных EPSG,
# Коды могут быть в диапазоне 4326 - 4937
# dframe - координаты рамки в исходной системе координат в радианах
# Возвращает по адресу dframe значения координат в СК epsgcodedest
# При ошибке возвращает ноль.

    gmlGeoToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGeoToGeo', ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def gmlGeoToGeo(_epsgcodesource: int, _epsgcodedest: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return gmlGeoToGeo_t (_epsgcodesource, _epsgcodedest, _dframe)


# Установить отбор объектов по идентификатору слоя
# hgml - идентификатор открытой схемы для записи GML
# hselect - идентификатор условий отбора объектов
# featuretype - идентификатор слоя в кодировке UTF-8
# При ошибке возвращает ноль

#   gmlSetSelectByFeaturieType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSetSelectByFeaturieType', HGML, maptype.HSELECT, ctypes.c_char_p)
#   def gmlSetSelectByFeaturieType(_hgml: HGML, _hselect: maptype.HSELECT, _featuretype: ctypes.c_char_p) -> int:
#       return gmlSetSelectByFeaturieType_t (_hgml, _hselect, _featuretype)


# Cоздание объектов из файла формата geoJSON
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты
# jsonname - имя файла формата GeoJSON
# Код создаваемого объекта ищется в поле code ("code": 115001010,)
# Если код не задан в объекте, то он выбирается из входных параметров
# squareCode - код создаваемых площадных объектов или 0
# pointCode  - код создаваемых точечных объектов или 0
# lineCode   - код создаваемых линейных объектов или 0
# textCode   - код создаваемых подписей или 0
# hwnd - идентификатор окна для приема сообщений или ноль, посылаются сообщения WM_PROGRESSBAR
# charset - кодировка текста (0 - UTF-8 или 1- ANSI)
# При ошибке возвращает ноль

    gmlCreateObjectsFromJSONPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCreateObjectsFromJSONPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int)
    def gmlCreateObjectsFromJSONPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _jsonname: mapsyst.WTEXT, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0, _hwnd: maptype.HMESSAGE = 0, _charset: int = 0) -> int:
        return gmlCreateObjectsFromJSONPro_t (_hmap, _hsite, _jsonname.buffer(), _squareCode, _pointCode, _lineCode, _textCode, _hwnd, _charset)

    gmlCreateObjectsFromJSONStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCreateObjectsFromJSONStream', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int)
    def gmlCreateObjectsFromJSONStream(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0, _hwnd: maptype.HMESSAGE = 0, _charset: int = 0) -> int:
        return gmlCreateObjectsFromJSONStream_t (_hmap, _hsite, _stream, _streamlength, _squareCode, _pointCode, _lineCode, _textCode, _hwnd, _charset)

    gmlCreateObjectsFromJSONEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCreateObjectsFromJSONEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE)
    def gmlCreateObjectsFromJSONEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _jsonname: mapsyst.WTEXT, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0, _hwnd: maptype.HMESSAGE = 0) -> int:
        return gmlCreateObjectsFromJSONEx_t (_hmap, _hsite, _jsonname.buffer(), _squareCode, _pointCode, _lineCode, _textCode, _hwnd)

    gmlCreateObjectsFromJSON_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCreateObjectsFromJSON', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def gmlCreateObjectsFromJSON(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _jsonname: mapsyst.WTEXT, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0) -> int:
        return gmlCreateObjectsFromJSON_t (_hmap, _hsite, _jsonname.buffer(), _squareCode, _pointCode, _lineCode, _textCode)


# Освободить идентификатор данных json
# hJson - идентификатор данных, полученный в функциях gmlLoadJsonTransactionToMap

#   gmlFreeJsonHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeJsonHandle', HJSON)
#   def gmlFreeJsonHandle(_hJson: HJSON) -> ctypes.c_void_p:
#       return gmlFreeJsonHandle_t (_hJson)


# Cоздание объектов из потока транзакций
# hMap, hSite - идентификатор карты
# stream - указатель на данные, в котором находится транзакции
# streamlength - длина потока
# protocol - флаг формирования лога ошибок
# При ошибке возвращает 0, иначе идентификатор данных

#   gmlLoadJsonTransactionToMap_t = mapsyst.GetProcAddress(acceslib,HJSON,'gmlLoadJsonTransactionToMap', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
#   def gmlLoadJsonTransactionToMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _protocol: int) -> HJSON:
#       return gmlLoadJsonTransactionToMap_t (_hMap, _hSite, _stream, _streamlength, _protocol)


# Запросить количество созданных объектов
# hJson - идентификатор данных
# Возвращает количество созданных объектов
# При ошибке возвращает 0

#   gmlGetJsonCreateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJsonCreateObjectsCount', HJSON)
#   def gmlGetJsonCreateObjectsCount(_hJson: HJSON) -> int:
#       return gmlGetJsonCreateObjectsCount_t (_hJson)


# Запросить количество обновленных объектов при выполнении транзакций
# hJson - идентификатор данных
# Возвращает количество обновленных объектов
# При ошибке возвращает 0

#   gmlGetJsonUpdateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJsonUpdateObjectsCount', HJSON)
#   def gmlGetJsonUpdateObjectsCount(_hJson: HJSON) -> int:
#       return gmlGetJsonUpdateObjectsCount_t (_hJson)


# Запросить количество удаленных объектов при выполнении транзакций
# hJson - идентификатор данных
# Возвращает количество удаленных объектов
# При ошибке возвращает 0

#   gmlGetJsonDeleteObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJsonDeleteObjectsCount', HJSON)
#   def gmlGetJsonDeleteObjectsCount(_hJson: HJSON) -> int:
#       return gmlGetJsonDeleteObjectsCount_t (_hJson)


# Запросить количество заменённых объектов при выполнении транзакций
# hJson - идентификатор данных
# Возвращает количество заменённых объектов
# При ошибке возвращает 0

#   gmlGetJsonReplaceObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJsonReplaceObjectsCount', HJSON)
#   def gmlGetJsonReplaceObjectsCount(_hJson: HJSON) -> int:
#       return gmlGetJsonReplaceObjectsCount_t (_hJson)


# Запросить кол-во объектов, присланных в транзакции
# hJson - идентификатор данных
# При ошибке возвращает 0, иначе кол-во присланных объектов

#   gmlGetJsonTransactionObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJsonTransactionObjectsCount', HJSON)
#   def gmlGetJsonTransactionObjectsCount(_hJson: HJSON) -> int:
#       return gmlGetJsonTransactionObjectsCount_t (_hJson)


# Записать завершающие теги
# hgml - идентификатор открытой схемы для записи GML
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# targetfilename - имя выходного файла
# matched  - количество найденных объектов
# returned - количество объектов, записанных в GML
# data - данные которые необходимо дописать в конец файла
# datasize - размер данных
# saveClosedTag - сохранять закрывающий тэг
# При ошибке возвращает ноль

    gmlSaveFileEnd_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSaveFileEnd', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def gmlSaveFileEnd(_format: int, _targetfilename: mapsyst.WTEXT, _matched: int, _returned: int) -> int:
        return gmlSaveFileEnd_t (_format, _targetfilename.buffer(), _matched, _returned)

    gmlSaveFileEndInMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSaveFileEndInMemory', ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
    def gmlSaveFileEndInMemory(_handle: ctypes.c_void_p, _matched: int, _returned: int) -> int:
        return gmlSaveFileEndInMemory_t (_handle, _matched, _returned)

    gmlSaveFileEndEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSaveFileEndEx', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def gmlSaveFileEndEx(_format: int, _targetfilename: mapsyst.WTEXT, _matched: int, _returned: int, _data: ctypes.c_char_p, _datasize: int) -> int:
        return gmlSaveFileEndEx_t (_format, _targetfilename.buffer(), _matched, _returned, _data, _datasize)

    gmlSaveFileEndPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSaveFileEndPro', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def gmlSaveFileEndPro(_format: int, _targetfilename: mapsyst.WTEXT, _matched: int, _returned: int, _data: ctypes.c_char_p, _datasize: int, _saveClosedTag: int = 1) -> int:
        return gmlSaveFileEndPro_t (_format, _targetfilename.buffer(), _matched, _returned, _data, _datasize, _saveClosedTag)


# Записать собранную статистику по запросу (кол-во объектов, семантик, слоёв и др.)
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# targetfilename - имя выходного GML-файла
# statistic - указатель на собранную статистику по предыдущим запросам

    gmlSaveStatistic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlSaveStatistic', ctypes.c_int, maptype.PWCHAR, ctypes.c_void_p)
    def gmlSaveStatistic(_format: int, _targetfilename: mapsyst.WTEXT, _statistic: ctypes.c_void_p) -> ctypes.c_void_p:
        return gmlSaveStatistic_t (_format, _targetfilename.buffer(), _statistic)


# Освободить собранную статистику по запросу
# statistic - указатель на собранную статистику по предыдущим запросам

    gmlFreeStatistic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeStatistic', ctypes.c_void_p)
    def gmlFreeStatistic(_statistic: ctypes.c_void_p) -> ctypes.c_void_p:
        return gmlFreeStatistic_t (_statistic)


# Записать отсортированный массив в файл
# format - формат вывода данных: GML, JSON (см. OGCSERVICETYPE)
# targetfilename - имя выходного GML-файла
# sortlist - указатель на массив объектов, собранный по предыдущим запросам
# number_begin - номер начльного объекта или 0
# count - вывод определенного количества объектов

    gmlSaveSortList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlSaveSortList', ctypes.c_void_p, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def gmlSaveSortList(_sortlist: ctypes.c_void_p, _format: int, _targetfilename: mapsyst.WTEXT, _number_begin: int = 0, _count: int = 0) -> int:
        return gmlSaveSortList_t (_sortlist, _format, _targetfilename.buffer(), _number_begin, _count)


# Освободить массив
# sortlist - указатель на массив объектов, собранный по предыдущим запросам

    gmlFreeSortList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeSortList', ctypes.c_void_p)
    def gmlFreeSortList(_sortlist: ctypes.c_void_p) -> ctypes.c_void_p:
        return gmlFreeSortList_t (_sortlist)


# Запрос габаритов объектов файла geojson и числа объектов
# name   - имя файла geojson
# border - габариты объектов в радианах в СК WGS-84
# Если число объектов не может быть определено, то возвращает -1
# При ошибке возвращает 0

    gmlGetJSONBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetJSONBorder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def gmlGetJSONBorder(_name: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        return gmlGetJSONBorder_t (_name.buffer(), _border)


# Проверить, что это geojson
# Функция ищет узел "type":"FeatureCollection"
# name   - имя файла geojson
# При ошибке возвращает 0

    gmlCheckJSON_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCheckJSON', maptype.PWCHAR)
    def gmlCheckJSON(_name: mapsyst.WTEXT) -> int:
        return gmlCheckJSON_t (_name.buffer())


# Проверить, что это geojson
# Функция ищет узел "type":"FeatureCollection"
# stream - входной файл в памяти
# streamlength - длина файла
# При ошибке возвращает 0

    gmlCheckJSONFromStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCheckJSONFromStream', ctypes.c_char_p, ctypes.c_int)
    def gmlCheckJSONFromStream(_stream: ctypes.c_char_p, _streamlength: int) -> int:
        return gmlCheckJSONFromStream_t (_stream, _streamlength)


# Импортировать данные из файла KML/KMZ на карту (без настройки ключей из RSC)
# kmlname - имя файла KML/KMLZ
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# hwnd  - идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса WM_PROGRESSBAR
# error   - поле для записи кода ошибки
# При ошибке возвращает ноль

    mapLoadKmlToMapEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoadKmlToMapEx', maptype.PWCHAR, maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(ctypes.c_int))
    def mapLoadKmlToMapEx(_kmlname: mapsyst.WTEXT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hwnd: maptype.HMESSAGE, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapLoadKmlToMapEx_t (_kmlname.buffer(), _hmap, _hsite, _hwnd, _error)


# Открыть файл KML/KMZ
# kmlname - имя файла KML
# При ошибке возвращает ноль, иначе - идентификатор открытого файла KML

#   mapOpenKml_t = mapsyst.GetProcAddress(acceslib,HKML,'mapOpenKml', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
#   def mapOpenKml(_kmlname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _selectstyle: int) -> HKML:
#       return mapOpenKml_t (_kmlname.buffer(), _error, _selectstyle)


# Закрыть доступ к файлу KML/KMZ и освободить ресурсы
# hkml - идентификатор доступа к файлу kml, созданный функцией mapOpenKml

#   mapCloseKml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseKml', HKML)
#   def mapCloseKml(_hkml: HKML) -> ctypes.c_void_p:
#       return mapCloseKml_t (_hkml)


# Запросить число стилей <Style>, найденных в файле
# hkml - идентификатор доступа к файлу kml, созданный функцией mapOpenKml
# При ошибке возвращает ноль, иначе - число найденных стилей

#   mapGetKmlStylesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetKmlStylesCount', HKML)
#   def mapGetKmlStylesCount(_hkml: HKML) -> int:
#       return mapGetKmlStylesCount_t (_hkml)


# Запросить идентификатор стиля по номеру
# hkml    - идентификатор доступа к файлу kml, созданный функцией mapOpenKml
# number  - номер стиля в списке от 1 до mapGetKmlStylesCount()
# styleid - буфер для записи строки-идентификатора стиля
# size    - размер буфера в байтах
# При ошибке возвращает ноль, иначе - идентификатор стиля

#   mapGetKmlStyleId_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetKmlStyleId', HKML, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
#   def mapGetKmlStyleId(_hkml: HKML, _number: int, _styleid: mapsyst.WTEXT, _size: int) -> int:
#       return mapGetKmlStyleId_t (_hkml, _number, _styleid.buffer(), _size)


# Установить ключ объекта для стиля по номеру
# hkml   - идентификатор доступа к файлу kml, созданный функцией mapOpenKml
# number - номер стиля в списке от 1 до mapGetKmlStylesCount(),
#          если номер равен -1, то устанавливается умалчиваемое значение для всех записей,
#          кроме тех, которым назначено значение через номер стиля
# key    - ключ объекта из RSC
# При ошибке возвращает ноль

#   mapSetKmlStyleObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetKmlStyleObjectKey', HKML, ctypes.c_int, ctypes.c_char_p)
#   def mapSetKmlStyleObjectKey(_hkml: HKML, _number: int, _key: ctypes.c_char_p) -> int:
#       return mapSetKmlStyleObjectKey_t (_hkml, _number, _key)


# Установить ключ объекта для стиля по идентификатору
# hkml   - идентификатор доступа к файлу kml, созданный функцией mapOpenKml
# number - номер стиля в списке от 1 до mapGetKmlStylesCount()
# key    - ключ объекта из RSC
# При ошибке возвращает ноль

#   mapSetKmlStyleObjectKeyForIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetKmlStyleObjectKeyForIdent', HKML, maptype.PWCHAR, ctypes.c_char_p)
#   def mapSetKmlStyleObjectKeyForIdent(_hkml: HKML, _styleid: mapsyst.WTEXT, _key: ctypes.c_char_p) -> int:
#       return mapSetKmlStyleObjectKeyForIdent_t (_hkml, _styleid.buffer(), _key)


# Импортировать данные из файла KML/KMZ на карту с учетом настроенных ключей объектов
# hkml  - идентификатор доступа к файлу kml, созданный функцией mapOpenKml
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# hwnd  - идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса WM_PROGRESSBAR
# errorcount - поле для записи числа ошибок при импорте файла KML
# objectcount - поле для записи числа созданных объектов
# При ошибке возвращает ноль

#   mapLoadKmlToMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoadKmlToMap', HKML, maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#   def mapLoadKmlToMap(_hkml: HKML, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hwnd: maptype.HMESSAGE, _errorcount: ctypes.POINTER(ctypes.c_int), _objectcount: ctypes.POINTER(ctypes.c_int)) -> int:
#       return mapLoadKmlToMap_t (_hkml, _hmap, _hsite, _hwnd, _errorcount, _objectcount)


# Экспортировать карту в файл формата KML/KMZ
# При формировании файла kml иконки сохраняются в формате png в папку "имя_файла.icons/" рядом с файлом kml
# Файл kmz содержит файл kml и все иконки в одном архиве
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# hselect - условия отбора объектов или 0 (вся карта)
# hwnd  - идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса WM_OBJECT
# kmlname - полный путь к файлу KML или KMZ
# imgsize - размер иконок в пикселах (например: 32, 48, 64, ...)
# semcodelist - указатель на список кодов семантик, которые нужно сохранить в KML, или 0
# semcodecount - число кодов семантик в списке или 0
# error   - поле для записи кода ошибки (см. maperr.rh)
# При ошибке возвращает ноль

    mapSaveMapToKmlEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMapToKmlEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapSaveMapToKmlEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _hwnd: maptype.HMESSAGE, _kmlname: mapsyst.WTEXT, _imgsize: int, _semcodelist: ctypes.POINTER(ctypes.c_int), _semcodecount: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapSaveMapToKmlEx_t (_hmap, _hsite, _hselect, _hwnd, _kmlname.buffer(), _imgsize, _semcodelist, _semcodecount, _error)

    mapSaveMapToKml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMapToKml', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapSaveMapToKml(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _hwnd: maptype.HMESSAGE, _kmlname: mapsyst.WTEXT, _imgsize: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapSaveMapToKml_t (_hmap, _hsite, _hselect, _hwnd, _kmlname.buffer(), _imgsize, _error)


# Cоздание объектов из потока транзакций по стандарту OGC WFS-T
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты
# stream - указатель на данные, в котором находится xml файл транзакции OGC WFS-T
# streamlength - длина потока
# squareCode - код создаваемых площадей
# pointCode  - код создаваемых точечных объектов
# lineCode - код создаваемых линий
# textCode - код создаваемых подписей
# flag - флаг формирования лога ошибок
# Возвращает идентификатор данных HGMLCLASS, который
# должен быть освобожден функцией mapFreeGmlClassHandle
# При ошибке возвращает 0

#   gmlLoadGmlTransactionToMap_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlLoadGmlTransactionToMap', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def gmlLoadGmlTransactionToMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0) -> HGMLCLASS:
#       return gmlLoadGmlTransactionToMap_t (_hmap, _hsite, _stream, _streamlength, _squareCode, _pointCode, _lineCode, _textCode)

#   gmlLoadGmlTransactionToMapEx_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlLoadGmlTransactionToMapEx', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def gmlLoadGmlTransactionToMapEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _flag: int = 0, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0) -> HGMLCLASS:
#       return gmlLoadGmlTransactionToMapEx_t (_hmap, _hsite, _stream, _streamlength, _flag, _squareCode, _pointCode, _lineCode, _textCode)


# Cоздание объектов из потока gml/xml файла
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# stream - указатель на данные, в котором находится gml/xml файл или файл gml OGC WFS
# streamlength - длина потока
# squareCode - код создаваемых площадей
# pointCode  - код создаваемых точечных объектов
# lineCode - код создаваемых линий
# textCode - код создаваемых подписей
# Возвращает идентификатор данных HGMLCLASS, который
# должен быть освобожден функцией mapFreeGmlClassHandle
# При ошибке возвращает 0

#   gmlCreateObjectsFromXmlStream_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlCreateObjectsFromXmlStream', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def gmlCreateObjectsFromXmlStream(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0) -> HGMLCLASS:
#       return gmlCreateObjectsFromXmlStream_t (_hmap, _hsite, _stream, _streamlength, _squareCode, _pointCode, _lineCode, _textCode)

#   gmlCreateObjectsFromXmlStreamPro_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlCreateObjectsFromXmlStreamPro', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE)
#   def gmlCreateObjectsFromXmlStreamPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _protocol: int, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0, _hwnd: maptype.HMESSAGE = 0) -> HGMLCLASS:
#       return gmlCreateObjectsFromXmlStreamPro_t (_hmap, _hsite, _stream, _streamlength, _protocol, _squareCode, _pointCode, _lineCode, _textCode, _hwnd)


# Cоздание объектов из файла gml/xml
# hmap -  идентификатор открытых данных (документа)
# hsite - идентификатор открытой пользовательской карты в документе
# xmlname - имя входного файла gml/xml или файла gml OGC WFS
# protocol   - признак ведения протокола ошибок в формате JSON (запрашивается gmlGetGmlReport)
# squareCode - код создаваемых площадей
# pointCode  - код создаваемых точечных объектов
# lineCode - код создаваемых линий
# textCode - код создаваемых подписей
# hwnd - идентификатор окна для приема сообщений или ноль, посылаются сообщения WM_PROGRESSBAR
# Возвращает идентификатор данных HGMLCLASS, который
# должен быть освобожден функцией mapFreeGmlClassHandle
# При ошибке возвращает 0

#   gmlCreateObjectsFromXmlPro_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlCreateObjectsFromXmlPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE)
#   def gmlCreateObjectsFromXmlPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlname: mapsyst.WTEXT, _protocol: int, _squareCode: int, _pointCode: int, _lineCode: int, _textCode: int, _hwnd: maptype.HMESSAGE = 0) -> HGMLCLASS:
#       return gmlCreateObjectsFromXmlPro_t (_hmap, _hsite, _xmlname.buffer(), _protocol, _squareCode, _pointCode, _lineCode, _textCode, _hwnd)

    gmlCreateObjectsFromXml_t = mapsyst.GetProcAddress(acceslib,maptype.HGMLCLASS,'gmlCreateObjectsFromXml', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def gmlCreateObjectsFromXml(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlname: mapsyst.WTEXT, _squareCode: int, _pointCode: int, _lineCode: int, _textCode: int) -> maptype.HGMLCLASS:
        return gmlCreateObjectsFromXml_t (_hmap, _hsite, _xmlname.buffer(), _squareCode, _pointCode, _lineCode, _textCode)

#   gmlCreateObjectsFromXmlEx_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlCreateObjectsFromXmlEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE)
#   def gmlCreateObjectsFromXmlEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlname: mapsyst.WTEXT, _squareCode: int = 0, _pointCode: int = 0, _lineCode: int = 0, _textCode: int = 0, _hwnd: maptype.HMESSAGE = 0) -> HGMLCLASS:
#       return gmlCreateObjectsFromXmlEx_t (_hmap, _hsite, _xmlname.buffer(), _squareCode, _pointCode, _lineCode, _textCode, _hwnd)

#   gmlCreateObjectsFromGml_t = mapsyst.GetProcAddress(acceslib,HGMLCLASS,'gmlCreateObjectsFromGml', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(GMLPARAMS))
#   def gmlCreateObjectsFromGml(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlname: mapsyst.WTEXT, _gmlparams: ctypes.POINTER(GMLPARAMS)) -> HGMLCLASS:
#       return gmlCreateObjectsFromGml_t (_hmap, _hsite, _xmlname.buffer(), _gmlparams)


# Освободить идентификатор данных gml/xml
# hGmlClass - идентификатор данных, полученный в функциях mapCreateObjFromXml,
# mapCreateObjFromXmlStream, mapLoadGmlTransactionToMap

    gmlFreeGmlClassHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeGmlClassHandle', maptype.HGMLCLASS)
    def gmlFreeGmlClassHandle(_hGmlClass: maptype.HGMLCLASS) -> ctypes.c_void_p:
        return gmlFreeGmlClassHandle_t (_hGmlClass)


# Запросить протокол ошибок в формате JSON при загрузке GML функцией gmlCreateObjectsFromXmlPro
# hGmlClass - идентификатор данных, полученный в функциях mapCreateObjFromXml,
# buffer    - адрес буфера для чтения протокола
# size      - размер буфера для чтения протокола
# Для запроса размера протокола параметр buffer должен быть равен нулю
# При ошибке возвращает 0

#   gmlGetGmlReport_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlReport', HGMLCLASS, ctypes.c_char_p, ctypes.c_int)
#   def gmlGetGmlReport(_hGmlClass: HGMLCLASS, _buffer: ctypes.c_char_p, _size: int) -> int:
#       return gmlGetGmlReport_t (_hGmlClass, _buffer, _size)


# Запросить количество созданных объектов
# hGmlClass - идентификатор данных
# Возвращает количество созданных объектов
# При ошибке возвращает 0

#   gmlGetGmlCreateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlCreateObjectsCount', HGMLCLASS)
#   def gmlGetGmlCreateObjectsCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlCreateObjectsCount_t (_hGmlClass)


# Запросить количество обновленных объектов при выполнении транзакций
# hGmlClass - идентификатор данных
# Возвращает количество обновленных объектов
# При ошибке возвращает 0

#   gmlGetGmlUpdateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlUpdateObjectsCount', HGMLCLASS)
#   def gmlGetGmlUpdateObjectsCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlUpdateObjectsCount_t (_hGmlClass)


# Запросить количество удаленных объектов при выполнении транзакций
# hGmlClass - идентификатор данных
# Возвращает количество удаленных объектов
# При ошибке возвращает 0

#   gmlGetGmlDeleteObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlDeleteObjectsCount', HGMLCLASS)
#   def gmlGetGmlDeleteObjectsCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlDeleteObjectsCount_t (_hGmlClass)


# Запросить количество заменённых объектов при выполнении транзакций
# hGmlClass - идентификатор данных
# Возвращает количество заменённых объектов
# При ошибке возвращает 0

#   gmlGetGmlReplaceObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlReplaceObjectsCount', HGMLCLASS)
#   def gmlGetGmlReplaceObjectsCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlReplaceObjectsCount_t (_hGmlClass)


# Запросить кол-во объектов, присланных в транзакции
# hGmlClass - идентификатор данных
# При ошибке возвращает 0, иначе кол-во присланных объектов

#   gmlGetGmlTransactionObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlTransactionObjectsCount', HGMLCLASS)
#   def gmlGetGmlTransactionObjectsCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlTransactionObjectsCount_t (_hGmlClass)


# Установить флаг сохранения сообщений в лог
# hGmlClass - идентификатор данных
# 0 - не формировать лог

#   gmlSetSaveErrorFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlSetSaveErrorFlag', HGMLCLASS, ctypes.c_int)
#   def gmlSetSaveErrorFlag(_hGmlClass: HGMLCLASS, _flag: int) -> ctypes.c_void_p:
#       return gmlSetSaveErrorFlag_t (_hGmlClass, _flag)


# Запросить кол-во ошибок при выполнении транзакции
# hGmlClass - идентификатор данных

#   gmlGetGmlErrorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlErrorCount', HGMLCLASS)
#   def gmlGetGmlErrorCount(_hGmlClass: HGMLCLASS) -> int:
#       return gmlGetGmlErrorCount_t (_hGmlClass)


# Запросить имя классификатора данных, по которому был создан gml
# xmlname - имя входного файла gml/xml или файла gml OGC WFS
# rscname - возвращаемое значение имени классификатора, по которому создан gml
# size - размер переменной rscname
# При ошибке возвращает 0

    gmlGetGmlRscName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlRscName', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def gmlGetGmlRscName(_xmlname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return gmlGetGmlRscName_t (_xmlname.buffer(), _rscname.buffer(), _size)


# Запросить габариты набора данных в формате GML и число объектов
# name   - имя gml-файла
# border - габариты набора данных в радианах в системе WGS-84
# Если число объектов не может быть определено, то возвращает -1
# При ошибке возвращает 0, иначе идентификатор данных

    gmlGetGmlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlBorder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def gmlGetGmlBorder(_name: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        return gmlGetGmlBorder_t (_name.buffer(), _border)


# Запрос габаритов объектов файла GML и кода EPSG
# xmlname - имя входного файла gml/xml или файла gml OGC WFS
# border   - габариты набора данных, заданные в наборе данных
# epsgcode - код системы координат, в которой заданы габариты
# Если код системы координат не соответствует габаритам набора данных - возвращает -1 (для CК-42)
# При ошибке возвращает 0

    gmlGetGmlBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlBorderEx', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(ctypes.c_int))
    def gmlGetGmlBorderEx(_xmlname: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME), _epsgcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return gmlGetGmlBorderEx_t (_xmlname.buffer(), _border, _epsgcode)


# Обновить описание объекта из файла gml/geojson
# info    - идентификатор обновляемого объекта в памяти
# filename - имя файла gml/geojson (полный путь)
# onlypoints - признак обновления только координат объекта
# error   - коды ошибок выполнения программы (см. maperr.rh)
# Объект изменяется без записи на карту
# При ошибке возвращает ноль

    gmlUpdateObjectFromGml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlUpdateObjectFromGml', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def gmlUpdateObjectFromGml(_info: maptype.HOBJ, _filename: mapsyst.WTEXT, _onlypoints: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return gmlUpdateObjectFromGml_t (_info, _filename.buffer(), _onlypoints, _error)


# Сформировать список стилей для рисования объектов по международным
# стандартам OGC 05-078r4 v.1.1.0 и OGC 02-070 v.1.0.0 - SLD (StyledLayerDescriptor)
# path - путь к файлу стилей, если path = 0 создает пустой список
# Каждый созданный список стилей должен быть удален (gmlFreeSld),
# когда он больше не используется.
# При ошибке возвращает ноль

    gmlCreateSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreateSld', maptype.PWCHAR)
    def gmlCreateSld(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        return gmlCreateSld_t (_path.buffer())


# Освободить список стилей
# hsld - список стилей, созданный gmlCreateSld

    gmlFreeSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeSld', ctypes.c_void_p)
    def gmlFreeSld(_hsld: ctypes.c_void_p) -> ctypes.c_void_p:
        return gmlFreeSld_t (_hsld)


# Добавить в список дополнительные SLD стили, которые будут учитываться при создании списка DRAWOBJECT
# hsld - список стилей, созданный gmlCreateSld
# addhsld - добавляемый список стилей
# При ошибке возвращает 0

    gmlAppendSldToSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlAppendSldToSld', ctypes.c_void_p, ctypes.c_void_p)
    def gmlAppendSldToSld(_hsld: ctypes.c_void_p, _addhsld: ctypes.c_void_p) -> int:
        return gmlAppendSldToSld_t (_hsld, _addhsld)


# Создать список (DRAWOBJECT) примитивов для рисования объектов на карте по стандарту OGC SLD
# hsld - список стилей, созданный gmlCreateSld или 0
# stream - xml файл стилей с фильтрами для объектов, загруженный в буфер
# size - размер буфера stream
# hmap, hsite - идентификатор текущей карты
# Каждый созданный список примитивов должен быть удален (mapFreePaintDrawList),
# когда он больше не используется.
# При ошибке возвращает 0

    gmlCreatePaintDrawListBySldStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreatePaintDrawListBySldStream', ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, maptype.HMAP, maptype.HSITE)
    def gmlCreatePaintDrawListBySldStream(_stream: ctypes.c_char_p, _size: int, _hsld: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return gmlCreatePaintDrawListBySldStream_t (_stream, _size, _hsld, _hmap, _hsite)


# Создать список (DRAWOBJECT) примитивов для рисования объектов на карте по стандарту OGC SLD
# hsld - список стилей, созданный gmlCreateSld или 0
# path - путь к файлу стилей с фильтрами для объектов
# hmap, hsite - идентификатор текущей карты
# Каждый созданный список примитивов должен быть удален (mapFreePaintDrawList),
# когда он больше не используется.
# При ошибке возвращает 0

    gmlCreatePaintDrawListBySld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreatePaintDrawListBySld', maptype.PWCHAR, ctypes.c_void_p, maptype.HMAP, maptype.HSITE)
    def gmlCreatePaintDrawListBySld(_path: mapsyst.WTEXT, _hsld: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return gmlCreatePaintDrawListBySld_t (_path.buffer(), _hsld, _hmap, _hsite)


# Запросить графическое описание в SLD схеме по имени стиля
# hsld - список стилей, созданный gmlCreateSld
# name - имя стиля в списке
# hdraw - заполняемое описание
# При ошибке возвращает 0

    gmlGetDrawObjectByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetDrawObjectByName', ctypes.c_void_p, ctypes.c_char_p, maptype.HDRAW)
    def gmlGetDrawObjectByName(_hsld: ctypes.c_void_p, _name: ctypes.c_char_p, _hdraw: maptype.HDRAW) -> int:
        return gmlGetDrawObjectByName_t (_hsld, _name, _hdraw)


# Запросить габариты объектов карты по списку номеров типов объектов
# hgml  - идентификатор GML данных
# epsgcode - код геодезической системы координат в базе данных EPSG, для GML по умолчанию - 4326
# dframe - габариты объектов карты в указанной системе координат
# При ошибке возвращает ноль

#   gmlFeaturiesBounds_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlFeaturiesBounds', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
#   def gmlFeaturiesBounds(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
#       return gmlFeaturiesBounds_t (_hgml, _featuretypenumbers, _epsgcode, _dframe)


# Запросить число объектов карты, отвечающих условиям отбора
# hgml - идентификатор открытой схемы для записи GML
# featuretypenumbers - список номеров типов объектов, разделенных запятой
# epsgcode - код геодезической системы координат в базе данных EPSG,
# для GML по умолчанию - 4326
# dframe - область отбора объектов карты в указанной системе координат или 0
# number - порядковый номер объекта, с которого начинать отбор (с 1)
# count - число объектов запроса
# Возвращает число объектов
# Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1
# Если условиям поиска не соответствует ни один объект, то возвращает -2
# Если произошел сбой при работе программы, то возвращает -4
# Если для карты запрещено копирование, то возвращает -5

#   gmlGetFeaturiesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesCount', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int)
#   def gmlGetFeaturiesCount(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _number: int, _count: int) -> int:
#       return gmlGetFeaturiesCount_t (_hgml, _featuretypenumbers, _epsgcode, _dframe, _number, _count)


# Запросить данные объектов карты по диапазону номеров
# hgml - идентификатор открытой схемы для записи GML
# featuretypenumbers - список номеров типов объектов, разделенных запятой
# epsgcode - код геодезической системы координат в базе данных EPSG,
# для GML по умолчанию - 4326
# dframe - область отбора объектов карты в указанной системе координат или 0
# service - тип разметки или формат файла: GML, GML/WFS, JSON  (см. OGCSERVICETYPE)
# number - порядковый номер объекта, с которого начинать вывод в файл (с 1)
# count - число объектов, выводимых в файл, если равно 0, то выводятся все объекты
# targetfilename - имя выходного GML-файла
# Возвращает число записанных объектов
# Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1
# Если условиям поиска не соответствует ни один объект, то возвращает -2
# Если выходной файл не может быть открыт, то возвращает -3
# Если произошел сбой при работе программы, то возвращает -4
# Если для карты запрещено копирование, то возвращает -5

#   gmlGetFeaturiesRangeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesRangeUn', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
#   def gmlGetFeaturiesRangeUn(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _service: int, _number: int, _count: int, _targetfilename: mapsyst.WTEXT) -> int:
#       return gmlGetFeaturiesRangeUn_t (_hgml, _featuretypenumbers, _epsgcode, _dframe, _service, _number, _count, _targetfilename.buffer())

#   gmlGetFeaturiesRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesRange', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
#   def gmlGetFeaturiesRange(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _service: int, _number: int, _count: int, _targetfilename: ctypes.c_char_p) -> int:
#       return gmlGetFeaturiesRange_t (_hgml, _featuretypenumbers, _epsgcode, _dframe, _service, _number, _count, _targetfilename)


# Запросить данные объекта карты по GML-идентификатору
# hgml - идентификатор открытой схемы для записи GML
# featuretypenumber - номер типа объекта
# epsgcode - код геодезической системы координат в базе данных EPSG
# id - GML-идентификатор объекта
# service - тип разметки файла: GML/WFS
# targetfilename - имя выходного GML-файла

#   gmlGetFeatureByIdUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeatureByIdUn', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, maptype.PWCHAR)
#   def gmlGetFeatureByIdUn(_hgml: HGML, _featuretypenumber: ctypes.c_char_p, _epsgcode: int, _id: ctypes.c_char_p, _service: int, _targetfilename: mapsyst.WTEXT) -> int:
#       return gmlGetFeatureByIdUn_t (_hgml, _featuretypenumber, _epsgcode, _id, _service, _targetfilename.buffer())

#   gmlGetFeatureById_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeatureById', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
#   def gmlGetFeatureById(_hgml: HGML, _featuretypenumber: ctypes.c_char_p, _epsgcode: int, _id: ctypes.c_char_p, _service: int, _targetfilename: ctypes.c_char_p) -> int:
#       return gmlGetFeatureById_t (_hgml, _featuretypenumber, _epsgcode, _id, _service, _targetfilename)


# Запросить данные объектов карты
# hgml - идентификатор открытой схемы для записи GML
# featuretypenumbers - список номеров типов объектов, разделенных запятой
# epsgcode - код геодезической системы координат в базе данных EPSG,
# для GML по умолчанию - 4326
# dframe - область отбора объектов карты в указанной системе координат или 0
# service - тип разметки файла: GML/WFS  (см. OGCSERVICETYPE)
# targetfilename - имя выходного GML-файла.
# При ошибке возвращает ноль, иначе - число записанных объектов
# Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1
# Если условиям поиска не соответствует ни один объект, то возвращает -2
# Если выходной файл не может быть открыт, то возвращает -3
# Если произошел сбой при работе программы, то возвращает -4
# Если для карты запрещено копирование, то возвращает -5

#   gmlGetFeaturies_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturies', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_char_p)
#   def gmlGetFeaturies(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _service: int, _targetfilename: ctypes.c_char_p) -> int:
#       return gmlGetFeaturies_t (_hgml, _featuretypenumbers, _epsgcode, _dframe, _service, _targetfilename)

#   gmlGetFeaturiesUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesUn', HGML, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, maptype.PWCHAR)
#   def gmlGetFeaturiesUn(_hgml: HGML, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _service: int, _targetfilename: mapsyst.WTEXT) -> int:
#       return gmlGetFeaturiesUn_t (_hgml, _featuretypenumbers, _epsgcode, _dframe, _service, _targetfilename.buffer())


# Сформировать набор данных (dataset) в формате GML
# hmap  - идентификатор открытого набора данных, содержащего векторные карты
# hsite - идентификатор карты в наборе данных
# list  - номер листа для многолистовой карты или 1, для конвертирования
#         в один GML-файл сразу всех листов необходимо указать "-1"
# hGml - идентификатор открытой схемы для записи GML
# (формируется функцией gmlOpenEx)
# featuretypenumbers - список номеров типов объектов, разделенных запятой,
#                      например: "1,5,11"
# metadata - URL для метаданных
# epsgcode - код геодезической системы координат в базе данных EPSG,
# по умолчанию - 4326
# targetfilename - имя выходного GML-файла
# force - признак принудительной записи объектов (1), даже если они не
#         описаны в прикладной схеме или 0
# hwnd - идентификатор для посылки сообщений о ходе выполнения процесса
# При ошибке возвращает ноль, иначе - число записанных объектов
# Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1
# Если условиям поиска не соответствует ни один объект, то возвращает -2
# Если выходной файл не может быть открыт, то возвращает -3
# Если произошел сбой при работе программы, то возвращает -4
# Если для карты запрещено копирование, то возвращает -5

#   gmlGetFeaturiesDataset_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesDataset', maptype.HMAP, maptype.HSITE, ctypes.c_int, HGML, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, maptype.HMESSAGE)
#   def gmlGetFeaturiesDataset(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hgml: HGML, _metadata: ctypes.c_char_p, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _targetfilename: ctypes.c_char_p, _force: int, _hwnd: maptype.HMESSAGE) -> int:
#       return gmlGetFeaturiesDataset_t (_hmap, _hsite, _list, _hgml, _metadata, _featuretypenumbers, _epsgcode, _targetfilename, _force, _hwnd)

#   gmlGetFeaturiesDatasetUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetFeaturiesDatasetUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, HGML, maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE)
#   def gmlGetFeaturiesDatasetUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hgml: HGML, _metadata: mapsyst.WTEXT, _featuretypenumbers: ctypes.c_char_p, _epsgcode: int, _targetfilename: mapsyst.WTEXT, _force: int, _hwnd: maptype.HMESSAGE) -> int:
#       return gmlGetFeaturiesDatasetUn_t (_hmap, _hsite, _list, _hgml, _metadata.buffer(), _featuretypenumbers, _epsgcode, _targetfilename.buffer(), _force, _hwnd)


# Проверить наличие семантики по коду
# hgml - идентификатор открытой схемы GML
# code - код семантики в классификаторе
# При ошибке возвращает ноль

#   gmlCheckSemanticByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlCheckSemanticByCode', HGML, ctypes.c_int)
#   def gmlCheckSemanticByCode(_hgml: HGML, _code: int) -> int:
#       return gmlCheckSemanticByCode_t (_hgml, _code)


# Запросить массив уникальных номеров созданных объектов
# hGmlClass - идентификатор данных
# ObjCrNum - массив уникальных номеров созданных объектов
# Возвращает указатель на класс THandleList
# При ошибке возвращает 0

#   gmlGetGmlObjectsNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlGetGmlObjectsNumber', HGMLCLASS)
#   def gmlGetGmlObjectsNumber(_hGmlClass: HGMLCLASS) -> ctypes.c_void_p:
#       return gmlGetGmlObjectsNumber_t (_hGmlClass)

except Exception as e:
    print(e)
    acceslib = 0