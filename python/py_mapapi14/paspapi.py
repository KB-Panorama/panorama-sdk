#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class REFERENCESYSTEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("NameSystem",ctypes.c_char*512),
                ("Comment",ctypes.c_char*512),
                ("Ident",ctypes.c_char*64),
                ("CodeEpsg",ctypes.c_int)]
#-----------------------------


#-----------------------------
class REFERENCESYSTEMUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("NameSystem",maptype.WCHAR1*(512*2)),
                ("Comment",maptype.WCHAR1*(512*2)),
                ("Ident",maptype.WCHAR1*(64*2)),
                ("CodeEpsg",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ORGANIZATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*256),
                ("Phone",ctypes.c_char*32),
                ("Facsimile",ctypes.c_char*32),
                ("City",ctypes.c_char*32),
                ("Adminarea",ctypes.c_char*32),
                ("Postalcode",ctypes.c_char*32),
                ("Country",ctypes.c_char*32),
                ("Email",ctypes.c_char*64),
                ("Reserve",ctypes.c_char*256)]
#-----------------------------


#-----------------------------
class AGENT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Fio",ctypes.c_char*256),
                ("NameOrg",ctypes.c_char*256),
                ("Phone",ctypes.c_char*32),
                ("Facsimile",ctypes.c_char*32),
                ("Email",ctypes.c_char*64)]
#-----------------------------


#-----------------------------
class AGENTEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Fio",maptype.WCHAR1*(256*2)),
                ("NameOrg",maptype.WCHAR1*(256*2)),
                ("Position",maptype.WCHAR1*(256*2)),
                ("Phone",maptype.WCHAR1*(32*2)),
                ("Facsimile",maptype.WCHAR1*(32*2)),
                ("Email",maptype.WCHAR1*(64*2)),
                ("Reserve",maptype.WCHAR1*(256*2))]
#-----------------------------


#-----------------------------
class ORGANIZATIONEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",maptype.WCHAR1*(256*2)),
                ("Phone",maptype.WCHAR1*(32*2)),
                ("Facsimile",maptype.WCHAR1*(32*2)),
                ("City",maptype.WCHAR1*(32*2)),
                ("Adminarea",maptype.WCHAR1*(32*2)),
                ("Postalcode",maptype.WCHAR1*(32*2)),
                ("Country",maptype.WCHAR1*(32*2)),
                ("Email",maptype.WCHAR1*(64*2)),
                ("Reserve",maptype.WCHAR1*(256*2))]
#-----------------------------


#-----------------------------
class RMF_METADATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Totalsize",ctypes.c_double),
                ("Ident",maptype.WCHAR1*(64*2)),
                ("WestLongitude",maptype.WCHAR1*(32*2)),
                ("EastLongitude",maptype.WCHAR1*(32*2)),
                ("SouthLatitude",maptype.WCHAR1*(32*2)),
                ("NorthLatitude",maptype.WCHAR1*(32*2)),
                ("Scale",maptype.WCHAR1*(32*2)),
                ("Nomenclature",maptype.WCHAR1*(256*2)),
                ("Createdate",maptype.WCHAR1*(32*2)),
                ("Format",maptype.WCHAR1*(16*2)),
                ("Filename",maptype.WCHAR1*(1024*2)),
                ("Comment",maptype.WCHAR1*(256*2)),
                ("Lineage",maptype.WCHAR1*(512*2)),
                ("Areadate",maptype.WCHAR1*(32*2)),
                ("Security",maptype.WCHAR1*(128*2)),
                ("Datatype",maptype.WCHAR1*(128*2)),
                ("SatName",maptype.WCHAR1*(64*2)),
                ("CloudState",maptype.WCHAR1*(32*2)),
                ("SunAngle",maptype.WCHAR1*(32*2)),
                ("ScanAngle",maptype.WCHAR1*(32*2)),
                ("Epsgcode",ctypes.c_int),
                ("MinScale",ctypes.c_int),
                ("MaxScale",ctypes.c_int),
                ("Reserve",maptype.WCHAR1*(228*2))]
#-----------------------------

try:
    if os.environ['gispaspdll']:
        gispaspname = os.environ['gispaspdll']
except KeyError:
    gispaspname = 'gis64pasp.dll'

try:
    pasplib = mapsyst.LoadLibrary(gispaspname)

# Диалог создания карты
# hmap     - идентификатор открытой карты или 0
# mapname  - указатель на строку, содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться!
# size     - длина строки в байтах, содержащей имя карты (рекомендуется 1024 символа, т.е. 2048 байт в WCHAR)
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_MAP
# При ошибке возвращает ноль

    paspCreateMapUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreateMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreateMapUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspCreateMapUn_t (_hmap, _mapname.buffer(), _size, _parm)

    paspCreateMap_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreateMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreateMap(_hmap: maptype.HMAP, _mapname: ctypes.c_char_p, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspCreateMap_t (_hmap, _mapname, _size, _parm)


# Диалог создания карты
# hmap     - идентификатор открытой карты или 0
# mapname  - указатель на строку, содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# size     - длина строки в байтах, содержащей имя карты
# parm     - структура параметров для диалога (см. maptype.h)
# password - пароль доступа к данным из которого формируется 256-битный код
#            для шифрования данных (при утрате данные не восстанавливаются)
# sizepassw - длина поля пароля в байтах
# rscname  - имя классификатора, с которым создана карта
# sizersc  - длина поля имени классификатора в байтах
# epsgcode - код EPSG для начальной инициализации полей диалога или 0
#            при epsgcode = -1 устанавливается тип карты "Крупномасштабный план"
# Help вызывается из mappasp.chm, топик CREATE_MAP
# При ошибке возвращает ноль

    paspCreateMapProEx_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreateMapProEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def paspCreateMapProEx(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _password: mapsyst.WTEXT, _sizepassw: int, _rscname: mapsyst.WTEXT, _sizersc: int, _epsgcode: int) -> int:
        return paspCreateMapProEx_t (_hmap, _mapname.buffer(), _size, _parm, _password.buffer(), _sizepassw, _rscname.buffer(), _sizersc, _epsgcode)

    paspCreateMapPro_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreateMapPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int)
    def paspCreateMapPro(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _password: mapsyst.WTEXT, _sizepassw: int) -> int:
        return paspCreateMapPro_t (_hmap, _mapname.buffer(), _size, _parm, _password.buffer(), _sizepassw)


# Диалог создания крупномасштабного плана
# mapname  - указатель на строку, содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# size     - длина строки в байтах, содержащей имя карты
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_PLAN
# При ошибке возвращает ноль

    paspCreatePlanUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreatePlanUn', maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreatePlanUn(_mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspCreatePlanUn_t (_mapname.buffer(), _size, _parm)

    paspCreatePlan_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreatePlan', ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreatePlan(_mapname: ctypes.c_char_p, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspCreatePlan_t (_mapname, _size, _parm)


# Диалог создания пользовательской карты по открытой карте
# hmap     - идентификатор открытой карты
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_SITE
# При ошибке возвращает ноль

    paspCreateSite_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspCreateSite', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreateSite(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspCreateSite_t (_hmap, _parm)


# Диалог создания пользовательской карты с запросом имени файла
# hmap     - идентификатор открытой карты
# mapname  - буфер для записи имени созданной карты
# size     - длина буфера в байтах
# path     - директория в которой будет предложено создать файл
#            (пользователь может выбрать другую)
# parm     - структура параметров для диалога (см. maptype.h)
# При ошибке возвращает ноль

#   MapPaspSitDocUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitDocUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def MapPaspSitDocUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _path: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitDocUn_t (_hmap, _mapname.buffer(), _size, _path.buffer(), _parm)


# Диалог просмотра и редактирования паспорта
# hmap     - идентификатор открытой карты
# hsite    - пользовательская карта
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик PASP_EDID
# При ошибке возвращает ноль

    paspViewPasp_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspViewPasp', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.TASKPARMEX))
    def paspViewPasp(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspViewPasp_t (_hmap, _hsite, _parm)


# Диалог для изменения параметров местной системы координат
# Устанавливает параметры МСК для документа (HMAP),
# которые затем могут использоваться при пересчетах координат
# в функциях mapPlaneToWorkSystemPlane, mapWorkSystemPlaneToGeo и т.п.
# hmap       - идентификатор открытой карты (документа),
# taskparmex - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик MCK_PARAM
# При ошибке возвращает ноль

    paspSetWorkSystemParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetWorkSystemParameters', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspSetWorkSystemParameters(_hmap: maptype.HMAP, _taskparmex: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspSetWorkSystemParameters_t (_hmap, _taskparmex)


# Отображение и установка текущих параметров проекции документа
# для отображения, печати и расчета координат
# Устанавливать общие параметры проекции можно для документа
# поддерживающего пересчет геодезических координат (mapIsGeoSupported() != 0)
# После установки общих параметров проекции изображение карты формируется
# в заданной проекции. Векторные карты, имеющие другие параметры
# проекции, трансформируются в процессе отображения.
# Все операции с координатами (mapPlaneToGeo, mapGeoToPlane,
# mapPlaneToGeoWGS84, mapAppendPointPlane, mapInsertPointPlane,
# mapUpdatePointPlane, mapAppendPointGeo и другие) выполняются
# в системе координат документа, определяемой общими параметрами проекции
# При чтении\записи координат в конкретной карте выполняется пересчет
# из системы координат документа
# hmap       - идентификатор открытой карты (документа),
# taskparmex - структура параметров для диалога (см. maptype.h)
# Новые параметры устанавливаются функцией mapSetDocProjection(...)(см. mapapi.h)
# Help вызывается из mappasp.chm, топик DOCPROJECTION
# При ошибке возвращает ноль

    paspSetCurrentProjectionParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetCurrentProjectionParameters', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspSetCurrentProjectionParameters(_hmap: maptype.HMAP, _taskparm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspSetCurrentProjectionParameters_t (_hmap, _taskparm)


# Установить/Отобразить параметры проекции
# hmap - идентификатор открытых данных (или 0)
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# описаны в mapcreat.h
# Структура TASKPARMEX описана в maptype.h
# const char# title - заголовок диалога
# Исходные значения параметров проекции заданы в
# MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# iswrite           - флаг допустимости редактирования параметров проекции
#                     (0 - не редактировать / 1 - редактировать)
# Выход: установленные MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# При изменении значений параметров возвращает 1
# При отсутствии изменений и при ошибке возвращает ноль

    paspSetProjectionParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetProjectionParameters', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int)
    def paspSetProjectionParameters(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: ctypes.c_char_p, _iswrite: int) -> int:
        return paspSetProjectionParameters_t (_hmap, _mapregisterex, _datum, _spheroidparam, _parm, _title, _iswrite)


# Установить/Отобразить параметры проекции
# hmap - идентификатор открытых данных (или 0)
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# описаны в mapcreat.h
# Структура TASKPARMEX описана в maptype.h
# title             - заголовок диалога в кодировке UNICODE
# Исходные значения параметров проекции заданы в
# MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# ttype   -  тип преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# Структура LOCALTRANSFORM  описана в mapcreat.h
# iswrite           - флаг допустимости редактирования параметров проекции
#                     (0 - не редактировать / 1 - редактировать)
# Выход: установленные MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# При изменении значений параметров возвращает 1
# При отсутствии изменений и при ошибке возвращает ноль

    paspSetProjectionParametersPro_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetProjectionParametersPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int)
    def paspSetProjectionParametersPro(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT, _iswrite: int) -> int:
        return paspSetProjectionParametersPro_t (_hmap, _mapregisterex, _datum, _spheroidparam, _ttype, _tparm, _parm, _title.buffer(), _iswrite)

    paspSetProjectionParametersUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetProjectionParametersUn', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int)
    def paspSetProjectionParametersUn(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT, _iswrite: int) -> int:
        return paspSetProjectionParametersUn_t (_hmap, _mapregisterex, _datum, _spheroidparam, _parm, _title.buffer(), _iswrite)


# Установить параметры проекции списка растров, матриц
# hmap - идентификатор открытых данных
# datatype - тип файла (растры, матрицы)
# (см. maptype.h : FILE_RSW, FILE_MTW,...)
# chainnumber - номер в цепочке
# Структура TASKPARMEX описана в maptype.h
# title - заголовок диалога в кодировке UNICODE
# При ошибке возвращает ноль

    paspSetRmfProjectionParametersUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetRmfProjectionParametersUn', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def paspSetRmfProjectionParametersUn(_hmap: maptype.HMAP, _datatype: int, _chainnumber: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        return paspSetRmfProjectionParametersUn_t (_hmap, _datatype, _chainnumber, _parm, _title.buffer())

    paspSetRmfProjectionParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetRmfProjectionParameters', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p)
    def paspSetRmfProjectionParameters(_hmap: maptype.HMAP, _datatype: int, _chainnumber: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: ctypes.c_char_p) -> int:
        return paspSetRmfProjectionParameters_t (_hmap, _datatype, _chainnumber, _parm, _title)


# Установить/Отобразить параметры проекции для растра, матрицы
# hmap - идентификатор открытых данных
# datatype тип файла (растры, матрицы)
# (см. maptype.h : FILE_RSW, FILE_MTW,...)
# chainnumber номер в цепочке
# Структура TASKPARMEX описана в maptype.h
# title - заголовок диалога в кодировке UNICODE
# При установке измененных значений параметров возвращает 1
# При просмотре или при ошибке возвращает ноль

    paspSetProjectionData_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSetProjectionData', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def paspSetProjectionData(_hmap: maptype.HMAP, _datatype: int, _chainnumber: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        return paspSetProjectionData_t (_hmap, _datatype, _chainnumber, _parm, _title.buffer())


# Чтение XML-файла
# hmap - идентификатор открытых данных (при создании карты - hmap = 0)
# Структура REFERENCESYSTEMUN описана в paspapi.h
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM  описаны в mapcreat.h
# ttype   -  тип преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# Структура LOCALTRANSFORM  описана в mapcreat.h
# Структура TASKPARMEX описана в maptype.h
# regime  -  режимы работы с паспортом (создание, редактирование)
# Help вызывается из mappasp.chm, топик PARAMETERSXML
# При ошибке возвращает ноль

    paspReadFileXMLPro_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadFileXMLPro', maptype.HMAP, ctypes.POINTER(REFERENCESYSTEMUN), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspReadFileXMLPro(_hmap: maptype.HMAP, _referencesystem: ctypes.POINTER(REFERENCESYSTEMUN), _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspReadFileXMLPro_t (_hmap, _referencesystem, _mapregisterex, _datum, _ellipsoidparam, _ttype, _tparm, _parm, _regime)

    paspReadFileXML_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadFileXML', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspReadFileXML(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspReadFileXML_t (_hmap, _mapregisterex, _datum, _spheroidparam, _parm, _regime)

    paspReadFileXMLEx_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadFileXMLEx', maptype.HMAP, ctypes.POINTER(REFERENCESYSTEM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspReadFileXMLEx(_hmap: maptype.HMAP, _referencesystem: ctypes.POINTER(REFERENCESYSTEM), _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspReadFileXMLEx_t (_hmap, _referencesystem, _mapregisterex, _datum, _spheroidparam, _parm, _regime)

    paspReadFileXMLUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadFileXMLUn', maptype.HMAP, ctypes.POINTER(REFERENCESYSTEMUN), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspReadFileXMLUn(_hmap: maptype.HMAP, _referencesystem: ctypes.POINTER(REFERENCESYSTEMUN), _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspReadFileXMLUn_t (_hmap, _referencesystem, _mapregisterex, _datum, _spheroidparam, _parm, _regime)


# Чтение параметров из базы данных EPSG
# hmap - идентификатор открытых данных (при создании карты - hmap = 0)
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# описаны в mapcreat.h
# Структура TASKPARMEX описана в maptype.h
# в epsgcode возвращается код EPSG
# Файлы базы данных EPSG.CSG, EPSG.CSP, EPSG.CSU должны находиться
# в каталоге приложения
# При ошибке возвращает ноль

    paspReadEPSG_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadEPSG', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int))
    def paspReadEPSG(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _epsgcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return paspReadEPSG_t (_hmap, _mapregisterex, _datum, _ellipsoidparam, _parm, _epsgcode)


# Чтение параметров из базы данных EPSG
# hmap - идентификатор открытых данных (при создании карты - hmap = 0)
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM
# описаны в mapcreat.h
# Структура TASKPARMEX описана в maptype.h
# в epsgcode возвращается код EPSG
# Файлы базы данных EPSG.CSG, EPSG.CSP, EPSG.CSU должны находиться
# в каталоге приложения
# namesystem - строка длиной не менее 64 символов для размещения
# названия системы координат (идентификатора)
# size  - длина строки
# При ошибке возвращает ноль

    paspReadEPSGEx_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadEPSGEx', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int)
    def paspReadEPSGEx(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _epsgcode: ctypes.POINTER(ctypes.c_int), _namesystem: ctypes.c_char_p, _size: int) -> int:
        return paspReadEPSGEx_t (_hmap, _mapregisterex, _datum, _ellipsoidparam, _parm, _epsgcode, _namesystem, _size)

    paspReadEPSGExUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspReadEPSGExUn', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def paspReadEPSGExUn(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _epsgcode: ctypes.POINTER(ctypes.c_int), _namesystem: mapsyst.WTEXT, _size: int) -> int:
        return paspReadEPSGExUn_t (_hmap, _mapregisterex, _datum, _ellipsoidparam, _parm, _epsgcode, _namesystem.buffer(), _size)


# Создание и редактирование файла метаданных в формате XML
# filename - имя файла метаданных (0, если формировать для всех листов и всех карт)
# hmap - идентификатор открытых данных
# Структура TASKPARMEX описана в maptype.h
# regime - режимы работы с файлом метаданных (0 - создание,1- редактирование)
# При ошибке возвращает ноль

    paspWriteXMLMD_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspWriteXMLMD', ctypes.c_char_p, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspWriteXMLMD(_filename: ctypes.c_char_p, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspWriteXMLMD_t (_filename, _hmap, _parm, _regime)

    paspWriteXMLMDUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspWriteXMLMDUn', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def paspWriteXMLMDUn(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        return paspWriteXMLMDUn_t (_filename.buffer(), _hmap, _parm, _regime)


# Просмотр и редактирование файла метаданных
# filename - имя файла метаданных
# При ошибке возвращает ноль

    paspEditXMLMD_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspEditXMLMD', ctypes.c_char_p, ctypes.POINTER(maptype.TASKPARMEX))
    def paspEditXMLMD(_filename: ctypes.c_char_p, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspEditXMLMD_t (_filename, _parm)

    paspEditXMLMDUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspEditXMLMDUn', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def paspEditXMLMDUn(_filename: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return paspEditXMLMDUn_t (_filename.buffer(), _parm)


# Создание xml файла метаданных для одного листа (без вызова диалога)
# filename - имя файла метаданных
# Структуры MAPREGISTEREX, LISTREGISTER  описаны в mapcreat.h
# Структуры ORGAHIZATION, AGENT  описаны в paspapi.h
# rscname - имя файла классификатора (без пути)
# comment - комментарий, содержит краткое описание набора данных (до 256 символов)
# lineage - общие сведения об исходных данных и технологии их обработки (до 512 символов)
# security - гриф секретности:  1 - открытая информация
#                               2 - информация с ограниченным доступом
#                               3 - информация для служебного пользования
#                               4 - секретная информация
#                               5 - совершенно секретная информация
# codeepsg - код EPSG
# Обязательные для заполнения параметры: filename, mapreg, listreg
# При ошибке возвращает ноль

    paspSaveMetaData_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSaveMetaData', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(ORGANIZATION), ctypes.POINTER(AGENT), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def paspSaveMetaData(_filename: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _organization: ctypes.POINTER(ORGANIZATION), _agent: ctypes.POINTER(AGENT), _rscname: ctypes.c_char_p, _comment: ctypes.c_char_p, _lineage: ctypes.c_char_p, _security: int, _codeepsg: int) -> int:
        return paspSaveMetaData_t (_filename, _mapreg, _listreg, _organization, _agent, _rscname, _comment, _lineage, _security, _codeepsg)

    paspSaveMetaDataUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSaveMetaDataUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(ORGANIZATION), ctypes.POINTER(AGENT), maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def paspSaveMetaDataUn(_filename: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _organization: ctypes.POINTER(ORGANIZATION), _agent: ctypes.POINTER(AGENT), _rscname: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _lineage: mapsyst.WTEXT, _security: int, _codeepsg: int) -> int:
        return paspSaveMetaDataUn_t (_filename.buffer(), _mapreg, _listreg, _organization, _agent, _rscname.buffer(), _comment.buffer(), _lineage.buffer(), _security, _codeepsg)


# Создание и редактирование файла метаданных матриц и растров в формате XML
# filename - имя файла метаданных (или 0)
# hmap - идентификатор открытых данных
# Структура TASKPARMEX описана в maptype.h
# datatype тип файла (растры, матрицы)
# (см. maptype.h : FILE_RSW, FILE_MTW)
# При ошибке возвращает ноль

    paspMetaDataMtwRsw_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspMetaDataMtwRsw', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int)
    def paspMetaDataMtwRsw(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _datatype: int, _chainnumber: int) -> int:
        return paspMetaDataMtwRsw_t (_filename.buffer(), _hmap, _parm, _datatype, _chainnumber)


# Создание файла метаданных матриц и растров в формате XML (без вызова диалога)
# filename - имя файла метаданных
# Структуры RMF_METADATA, ORGANIZATIONEX, AGENTEX описаны в paspapi.h
# datatype - тип данных (растры, матрицы)
# (см. maptype.h : FILE_RSW, FILE_MTW)
# При ошибке возвращает ноль

    paspSaveMetaDataRmf_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSaveMetaDataRmf', maptype.PWCHAR, ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_int)
    def paspSaveMetaDataRmf(_filename: mapsyst.WTEXT, _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        return paspSaveMetaDataRmf_t (_filename.buffer(), _metadata, _organization, _agent, _datatype)


# Запросить метаданные для матриц и растров
# filename - имя файла метаданных
# Структуры RMF_METADATA, ORGANIZATIONEX, AGENTEX описаны в paspapi.h
# Структуры ORGANIZATIONEX, AGENTEX  необязательны для заполнения
# datatype - тип данных (растры, матрицы)
# (см. maptype.h : FILE_RSW, FILE_MTW)
# При ошибке возвращает ноль

    paspGetMetaDataRmf_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspGetMetaDataRmf', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_int)
    def paspGetMetaDataRmf(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        return paspGetMetaDataRmf_t (_filename.buffer(), _hmap, _parm, _metadata, _organization, _agent, _datatype)


# Создание файла метаданных матриц, растров, 3D моделей в формате XML
# filename - имя файла метаданных
# hmap - идентификатор открытых данных (или 0)
# parm - структура параметров для диалога (см. maptype.h)
# datatype - тип данных (растры, матрицы: FILE_RSW, FILE_MTW см. maptype.h )
# Структуры RMF_METADATA, ORGANIZATIONEX, AGENTEX описаны в paspapi.h
# При hmap = 0 структура RMF_METADATA должна быть заполнена
# Структуры ORGANIZATIONEX, AGENTEX могут быть 0 (заполнение в диалоге)
# При ошибке возвращает ноль

    paspSaveMetaDataMapFiles_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'paspSaveMetaDataMapFiles', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_int)
    def paspSaveMetaDataMapFiles(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        return paspSaveMetaDataMapFiles_t (_filename.buffer(), _hmap, _parm, _metadata, _organization, _agent, _datatype)


# Ввод пароля для хранения закодированных данных SITX
# mapname - путь к карте, для которой вводится пароль
# password - адрес буфера для сохранения пароля
# size     - размер буфера в байтах
# При ошибке возвращает ноль

    pspGetPassword_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'pspGetPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def pspGetPassword(_mapname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        return pspGetPassword_t (_mapname.buffer(), _password.buffer(), _size)


# ================================================================
#                      УСТАРЕВШИЕ ФУНКЦИИ
#              Реализованы через вызов новых функций
# ================================================================
# Редактирование паспорта
# hmap     - идентификатор открытой карты,
# mapname  - указатель на строку длиной 260 символов,
#            содержащую имя карты (файла паспорта)
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик PASP_EDID
# При ошибке возвращает ноль

#   MapPaspEdit_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspEdit', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(TASKPARM))
#   def MapPaspEdit(_hmap: maptype.HMAP, _mapname: ctypes.c_char_p, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspEdit_t (_hmap, _mapname, _parm)


# Просмотр паспорта карты
# hmap     - идентификатор открытой карты,
# taskparm - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик PASP_EDID
# При ошибке возвращает ноль

    mapPaspShow_t = mapsyst.GetProcAddress(pasplib,ctypes.c_int,'mapPaspShow', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def mapPaspShow(_hmap: maptype.HMAP, _taskparm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return mapPaspShow_t (_hmap, _taskparm)


# Создание плана
# mapname  - указатель на строку длиной 260 символов,
#            содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_PLAN
# При ошибке возвращает ноль

#   MapPaspPlan_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspPlan', ctypes.c_char_p, ctypes.POINTER(TASKPARM))
#   def MapPaspPlan(_mapname: ctypes.c_char_p, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspPlan_t (_mapname, _parm)


# Создание обстановки и добавление пользовательской карты
# в документ с запросом имени файла
# hmap     - идентификатор открытой карты,
# mapname  - указатель на строку длиной 1024 символов,
#            содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# path     - директория в которой будет предложено создать файл
#            (пользователь может выбрать другую)
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_MAP
# При ошибке возвращает ноль

#   MapPaspSitDoc_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitDoc', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(TASKPARM))
#   def MapPaspSitDoc(_hmap: maptype.HMAP, _mapname: ctypes.c_char_p, _path: ctypes.c_char_p, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitDoc_t (_hmap, _mapname, _path, _parm)


# Создание обстановки и добавление пользовательской карты
# в документ без запроса имени файла
# hmap     - идентификатор открытой карты,
# mapname  - указатель на строку длиной 260 символов,
#            содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_MAP
# При ошибке возвращает ноль

#   MapPaspSitDocByName_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitDocByName', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(TASKPARM))
#   def MapPaspSitDocByName(_hmap: maptype.HMAP, _mapname: ctypes.c_char_p, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitDocByName_t (_hmap, _mapname, _parm)

#   MapPaspSitDocByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitDocByNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def MapPaspSitDocByNameUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitDocByNameUn_t (_hmap, _mapname.buffer(), _parm)


# Создание пользовательской карты
# mapname  - указатель на строку длиной 260 символов,
#            содержащую имя карты (файла паспорта)
#            После вызова функции значение строки может измениться
# rscname  - имя файла классификатора (Rsc) (может быть 0)
# areaname - имя района (может быть 0)
# parm     - структура параметров для диалога (см. maptype.h)
# Help вызывается из mappasp.chm, топик CREATE_MAP
# При ошибке или отказе от ввода возвращает ноль

#   MapPaspSitCreate_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitCreate', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(TASKPARM))
#   def MapPaspSitCreate(_mapname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _areaname: ctypes.c_char_p, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitCreate_t (_mapname, _rscname, _areaname, _parm)

#   MapPaspSitCreateUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapPaspSitCreateUn', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def MapPaspSitCreateUn(_mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _areaname: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapPaspSitCreateUn_t (_mapname.buffer(), _rscname.buffer(), _areaname.buffer(), _parm)

except Exception as e:
    print(e)
    pasplib = 0