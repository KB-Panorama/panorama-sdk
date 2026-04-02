#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype

HNET  = ctypes.c_void_p
HPATH = ctypes.c_void_p
HDGR  = ctypes.c_void_p
HTSP  = ctypes.c_void_p

PACK_WIDTH = 1

#-----------------------------
class OPENNETPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Wnd",maptype.HWND),
                ("ParentMap",maptype.HMAP),
                ("Reserve",ctypes.c_char*128)]
#-----------------------------


#-----------------------------
class PATHPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point1",maptype.DOUBLEPOINT),
                ("Point2",maptype.DOUBLEPOINT),
                ("Wnd",maptype.HWND),
                ("NodeKey1",ctypes.c_int),
                ("NodeKey2",ctypes.c_int),
                ("IsWgs",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*128)]
#-----------------------------


#-----------------------------
class DISTGRAPHPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Dist",ctypes.c_double),
                ("Wnd",maptype.HWND),
                ("NodeKey",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*128)]
#-----------------------------


#-----------------------------
class TSPPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Wnd",maptype.HWND),
                ("PointCount",ctypes.c_int),
                ("Points",ctypes.POINTER(maptype.DOUBLEPOINT)),
                ("CalcType",ctypes.c_int),
                ("IsWgs",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*128)]
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary( gisaccesname )


# Открытие графа сети
# hmap, hsite - идентификатор открытой карты графа
# mapname - имя карты графа
# parm    - параметры открытия графа
# Возвращает идентификатор открытого графа
# При ошибке возвращает 0

    onOpenNetEx_t = mapsyst.GetProcAddress(acceslib,HNET,'onOpenNetEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(OPENNETPARM))
    def onOpenNetEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(OPENNETPARM)) -> HNET:
        return onOpenNetEx_t (_hmap, _hsite, _parm)

    onOpenNet_t = mapsyst.GetProcAddress(acceslib,HNET,'onOpenNet', maptype.PWCHAR, ctypes.POINTER(OPENNETPARM))
    def onOpenNet(_mapname: mapsyst.WTEXT, _parm: ctypes.POINTER(OPENNETPARM)) -> HNET:
        return onOpenNet_t (_mapname.buffer(), _parm)


# Закрытие графа сети
# hnet - идентификатор графа сети, полученный onOpenNet

    onCloseNet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCloseNet', HNET)
    def onCloseNet(_hnet: HNET) -> ctypes.c_void_p:
        return onCloseNet_t (_hnet)


# Закрытие графа сети по имени файла карты графа
# mapname - имя файла карты графа

    onCloseNetByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCloseNetByName', maptype.PWCHAR)
    def onCloseNetByName(_mapname: mapsyst.WTEXT) -> ctypes.c_void_p:
        return onCloseNetByName_t (_mapname.buffer())


# Возвращает идентификатор открытой карты графа
# hnet - идентификатор графа сети, полученный onOpenNet

    onGetHMAP_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'onGetHMAP', HNET)
    def onGetHMAP(_hnet: HNET) -> maptype.HMAP:
        return onGetHMAP_t (_hnet)

    onGetHSITE_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'onGetHSITE', HNET)
    def onGetHSITE(_hnet: HNET) -> maptype.HSITE:
        return onGetHSITE_t (_hnet)


# Возвращает документ, в котором открыты карты, по которым построен граф
# (поле ParentMap структуры OPENNETPARM, переданной при открытии графа)
# hnet - идентификатор графа сети, полученный onOpenNet

    onGetParentMap_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'onGetParentMap', HNET)
    def onGetParentMap(_hnet: HNET) -> maptype.HMAP:
        return onGetParentMap_t (_hnet)


# Возвращает количество типов дорог, участвующих в построении карты графа
# Тип дороги - значение семантики SEMNETROADTYPE в ребрах графа
# hnet - идентификатор графа сети, полученный onOpenNet
# При ошибке возвращает 0

    onGetParentRoadTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetParentRoadTypeCount', HNET)
    def onGetParentRoadTypeCount(_hnet: HNET) -> int:
        return onGetParentRoadTypeCount_t (_hnet)


# Возвращает имя типа дороги, участвовавшей в построении графа
# Тип дороги - значение семантики SEMNETROADTYPE в ребрах графа
# hnet   - идентификатор графа сети, полученный onOpenNet
# number - порядковый номер типа дороги (от 0)
# При ошибке возвращает 0

    onGetParentRoadTypeName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetParentRoadTypeName', HNET, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def onGetParentRoadTypeName(_hnet: HNET, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return onGetParentRoadTypeName_t (_hnet, _number, _name.buffer(), _namesize)


################################################################
#                    Кратчайший маршрут
################################################################
# Поиск кратчайшего маршрута по графу дорог
# Чтобы отобрать разрешенные ребра для построения маршрута и/или исключить
# отдельные ребра из построения маршрута необходимо в структуре PATHPARM
# установить условия отбора HSELECT (UseSelect и/или BanSelect)
# hnet - идентификатор графа сети, полученный onOpenNet
# parm - параметры определения маршрута
# Возвращает идентификатор маршрута
# При ошибке возвращает 0

    onCreatePath_t = mapsyst.GetProcAddress(acceslib,HPATH,'onCreatePath', HNET, ctypes.POINTER(PATHPARM))
    def onCreatePath(_hnet: HNET, _parm: ctypes.POINTER(PATHPARM)) -> HPATH:
        return onCreatePath_t (_hnet, _parm)


# Удалить маршрут
# hpath - идентификатор маршрута, полученный onCreatePath

    onFreePath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreePath', HPATH)
    def onFreePath(_hpath: HPATH) -> ctypes.c_void_p:
        return onFreePath_t (_hpath)


# Возвращает время проезда по всему маршруту в часах
# hpath  - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathTime', HPATH)
    def onGetPathTime(_hpath: HPATH) -> float:
        return onGetPathTime_t (_hpath)


# Возвращает длину всего маршрута в метрах
# hpath  - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathLength', HPATH)
    def onGetPathLength(_hpath: HPATH) -> float:
        return onGetPathLength_t (_hpath)


# Возвращает стоимость всего маршрута
# hpath  - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathCost_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathCost', HPATH)
    def onGetPathCost(_hpath: HPATH) -> float:
        return onGetPathCost_t (_hpath)


# Возвращает количество ребер в маршруте
# hpath - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathEdgeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeCount', HPATH)
    def onGetPathEdgeCount(_hpath: HPATH) -> int:
        return onGetPathEdgeCount_t (_hpath)


# Возвращает уникальный номер ребра маршрута на карте графа
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeKey', HPATH, ctypes.c_int)
    def onGetPathEdgeKey(_hpath: HPATH, _number: int) -> int:
        return onGetPathEdgeKey_t (_hpath, _number)


# Возвращает номер объекта ребра маршрута на карте графа
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathEdgeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeNum', HPATH, ctypes.c_int)
    def onGetPathEdgeNum(_hpath: HPATH, _number: int) -> int:
        return onGetPathEdgeNum_t (_hpath, _number)


# Возвращает номер типа дороги ребра маршрута в списке типов дорог,
# участвовавших в построении карты графа
# Для получения имени типа дороги используйте onGetParentRoadTypeName
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# ПРИ ОШИБКЕ ВОЗВРАЩАЕТ -1

    onGetPathParentEdgeType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathParentEdgeType', HPATH, ctypes.c_int)
    def onGetPathParentEdgeType(_hpath: HPATH, _number: int) -> int:
        return onGetPathParentEdgeType_t (_hpath, _number)


# Возвращает идентификатор карты, по объекту которой построено
# ребро маршрута при создании карты графа
# Для работы функции необходимо чтобы:
# - карта графа была построена с флагом "Сохранять связь с объектами исходной карты"
# - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathParentEdgeSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'onGetPathParentEdgeSite', HPATH, ctypes.c_int)
    def onGetPathParentEdgeSite(_hpath: HPATH, _number: int) -> maptype.HSITE:
        return onGetPathParentEdgeSite_t (_hpath, _number)


# Возвращает номер листа карты, по объекту которой построено ребро маршрута при создании карты графа
# Для работы функции необходимо чтобы:
# - карта графа была построена с флагом "Сохранять связь с объектами исходной карты"
# - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathParentEdgeSheetNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathParentEdgeSheetNum', HPATH, ctypes.c_int)
    def onGetPathParentEdgeSheetNum(_hpath: HPATH, _number: int) -> int:
        return onGetPathParentEdgeSheetNum_t (_hpath, _number)


# Возвращает уникальный номер объекта по которому построено ребро маршрута при создании карты графа
# Для работы функции необходимо чтобы карта графа была построена с флагом
# "Сохранять связь с объектами исходной карты"
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathParentEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathParentEdgeKey', HPATH, ctypes.c_int)
    def onGetPathParentEdgeKey(_hpath: HPATH, _number: int) -> int:
        return onGetPathParentEdgeKey_t (_hpath, _number)


# Считывает объект из которого нарезано ребро маршрута при создании карты графа
# Для работы функции необходимо чтобы:
# - карта графа была построена с флагом "Сохранять связь с объектами исходной карты"
# - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# obj    - идентификатор, в который будет считан родительский объект
# При ошибке возвращает 0

    onGetPathParentEdgeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathParentEdgeObject', HPATH, ctypes.c_int, maptype.HOBJ)
    def onGetPathParentEdgeObject(_hpath: HPATH, _number: int, _obj: maptype.HOBJ) -> int:
        return onGetPathParentEdgeObject_t (_hpath, _number, _obj)


# Возвращает длину ребра маршрута по порядковому номеру ребра в маршруте в метрах
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathEdgeLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeLength', HPATH, ctypes.c_int)
    def onGetPathEdgeLength(_hpath: HPATH, _number: int) -> float:
        return onGetPathEdgeLength_t (_hpath, _number)


# Возвращает время проезда ребра маршрута по порядковому номеру ребра в маршруте в часах
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathEdgeTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeTime', HPATH, ctypes.c_int)
    def onGetPathEdgeTime(_hpath: HPATH, _number: int) -> float:
        return onGetPathEdgeTime_t (_hpath, _number)


# Возвращает стоимость ребра маршрута по порядковому номеру ребра в маршруте
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# При ошибке возвращает 0

    onGetPathEdgeCost_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeCost', HPATH, ctypes.c_int)
    def onGetPathEdgeCost(_hpath: HPATH, _number: int) -> float:
        return onGetPathEdgeCost_t (_hpath, _number)


# Возвращает координаты первой точки ребра маршрута
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# point  - возвращаемые координаты первой точки ребра маршрута
#          Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
#          в системе координат карты графа
#          Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
#          широта, долгота в радианах на WGS84
# При ошибке возвращает 0

    onGetPathEdgeFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeFirstPoint', HPATH, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathEdgeFirstPoint(_hpath: HPATH, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return onGetPathEdgeFirstPoint_t (_hpath, _number, _point)


# Возвращает координаты последней точки ребра маршрута
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# point  - возвращаемые координаты последней точки ребра маршрута
#          Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
#          в системе координат карты графа
#          Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
#          широта, долгота в радианах на WGS84
# При ошибке возвращает 0

    onGetPathEdgeLastPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeLastPoint', HPATH, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathEdgeLastPoint(_hpath: HPATH, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return onGetPathEdgeLastPoint_t (_hpath, _number, _point)


# Возвращает угол поворота на последней точке ребра маршрута
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 2, НА ПОСЛЕДНЕМ РЕБРЕ НЕТ ПОВОРОТА)
# angle  - возвращаемый угол поворота на последней точке ребра маршрута
# При ошибке возвращает 0

    onGetPathEdgeLastPointAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeLastPointAngle', HPATH, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeLastPointAngle(_hpath: HPATH, _number: int, _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        return onGetPathEdgeLastPointAngle_t (_hpath, _number, _angle)


# Возвращает угол поворота на первой точке ребра маршрута
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 1 до onGetPathEdgeCount - 1, НА ПЕРВОМ РЕБРЕ НЕТ ПОВОРОТА)
# angle  - возвращаемый угол поворота на первой точке ребра маршрута
# При ошибке возвращает 0

    onGetPathEdgeFirstPointAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeFirstPointAngle', HPATH, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeFirstPointAngle(_hpath: HPATH, _number: int, _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        return onGetPathEdgeFirstPointAngle_t (_hpath, _number, _angle)


# Возвращает дирекционный угол первого отрезка ребра маршрута
# (угол на первой точке между направлением на север и на вторую точку против часовой стрелки)
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# dir    - возвращаемый дирекционный угол
# При ошибке возвращает 0

    onGetPathEdgeFirstSegmentDir_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeFirstSegmentDir', HPATH, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeFirstSegmentDir(_hpath: HPATH, _number: int, _dir: ctypes.POINTER(ctypes.c_double)) -> int:
        return onGetPathEdgeFirstSegmentDir_t (_hpath, _number, _dir)


# Возвращает дирекционный угол последнего отрезка ребра маршрута
# (угол на последней точке между направлением на север и на предпоследнюю точку против часовой стрелки)
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathEdgeCount - 1)
# dir    - возвращаемый дирекционный угол
# При ошибке возвращает 0

    onGetPathEdgeLastSegmentDir_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathEdgeLastSegmentDir', HPATH, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeLastSegmentDir(_hpath: HPATH, _number: int, _dir: ctypes.POINTER(ctypes.c_double)) -> int:
        return onGetPathEdgeLastSegmentDir_t (_hpath, _number, _dir)


# Возвращает количество узлов в маршруте (= количество ПОЛНЫХ ребер + 1)
# hpath - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathNodeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathNodeCount', HPATH)
    def onGetPathNodeCount(_hpath: HPATH) -> int:
        return onGetPathNodeCount_t (_hpath)


# Возвращает уникальный номер узла маршрута на карте графа
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathNodeCount - 1)
# При ошибке возвращает 0

    onGetPathNodeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathNodeKey', HPATH, ctypes.c_int)
    def onGetPathNodeKey(_hpath: HPATH, _number: int) -> int:
        return onGetPathNodeKey_t (_hpath, _number)


# Возвращает номер объекта узла маршрута на карте графа
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер ребра в маршруте (от 0 до onGetPathNodeCount - 1)
# При ошибке возвращает 0

    onGetPathNodeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathNodeNum', HPATH, ctypes.c_int)
    def onGetPathNodeNum(_hpath: HPATH, _number: int) -> int:
        return onGetPathNodeNum_t (_hpath, _number)


# Записывает в объект метрику маршрута
# hpath - идентификатор маршрута, полученный onCreatePath
# obj   - объект, в который записывается метрика маршрута
# При ошибке возвращает 0

    onGetPathObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathObject', HPATH, maptype.HOBJ)
    def onGetPathObject(_hpath: HPATH, _obj: maptype.HOBJ) -> int:
        return onGetPathObject_t (_hpath, _obj)


# Записывает в объект метрику маршрута
# hpath   - идентификатор маршрута, полученный onCreatePath
# obj     - объект, в который записывается метрика маршрута
# subject - номер подобъекта, в который записывается метрика маршрута
# При ошибке возвращает 0

    onGetPathSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathSubject', HPATH, maptype.HOBJ, ctypes.c_int)
    def onGetPathSubject(_hpath: HPATH, _obj: maptype.HOBJ, _subject: int) -> int:
        return onGetPathSubject_t (_hpath, _obj, _subject)


# Возвращает количество точек в маршруте
# hpath - идентификатор маршрута, полученный onCreatePath
# При ошибке возвращает 0

    onGetPathPointCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathPointCount', HPATH)
    def onGetPathPointCount(_hpath: HPATH) -> int:
        return onGetPathPointCount_t (_hpath)


# Возвращает координаты точки маршрута по порядковому номеру в маршруте
# hpath  - идентификатор маршрута, полученный onCreatePath
# number - номер точки в маршруте (от 0 до onGetPathPointCount - 1)
# point  - возвращаемые координтаы точки маршрута
#          Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
#          в системе координат карты графа
#          Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
#          широта, долгота в радианах на WGS84
# При ошибке возвращает 0

    onGetPathPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetPathPoint', HPATH, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathPoint(_hpath: HPATH, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return onGetPathPoint_t (_hpath, _number, _point)


################################################################
#                    Граф удаленности
################################################################
# Создание графа удаленности
# hnet - идентификатор графа сети
# parm - параметры построения графа удаленности
# Возвращает идентификатор графа удаленности
# При ошибке возвращает 0

    onCreateDistGraph_t = mapsyst.GetProcAddress(acceslib,HDGR,'onCreateDistGraph', HNET, ctypes.POINTER(DISTGRAPHPARM))
    def onCreateDistGraph(_hnet: HNET, _parm: ctypes.POINTER(DISTGRAPHPARM)) -> HDGR:
        return onCreateDistGraph_t (_hnet, _parm)


# Удаление графа удаленности
# hdgr - идентификатор графа удаленности

    onFreeDistGraph_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreeDistGraph', HDGR)
    def onFreeDistGraph(_hdgr: HDGR) -> ctypes.c_void_p:
        return onFreeDistGraph_t (_hdgr)


# Возвращает количество ребер в графе удаленности
# hdgr - идентификатор графа удаленности
# При ошибке возвращает 0

    onGetDistGraphEdgeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetDistGraphEdgeCount', HDGR)
    def onGetDistGraphEdgeCount(_hdgr: HDGR) -> int:
        return onGetDistGraphEdgeCount_t (_hdgr)


# Возвращает уникальный номер ребра графа удаленности на карте графа
# hdgr   - идентификатор графа удаленности
# number - номер ребра в графе удаленности (от 0 до onGetDistGraphEdgeCount - 1)
# При ошибке возвращает 0

    onGetDistGraphEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetDistGraphEdgeKey', HDGR, ctypes.c_int)
    def onGetDistGraphEdgeKey(_hdgr: HDGR, _number: int) -> int:
        return onGetDistGraphEdgeKey_t (_hdgr, _number)


# Возвращает номер объекта ребра графа удаленности на карте графа
# hdgr   - идентификатор графа удаленности
# number - номер ребра в графе удаленности (от 0 до onGetDistGraphEdgeCount - 1)
# При ошибке возвращает 0

    onGetDistGraphEdgeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetDistGraphEdgeNum', HDGR, ctypes.c_int)
    def onGetDistGraphEdgeNum(_hdgr: HDGR, _number: int) -> int:
        return onGetDistGraphEdgeNum_t (_hdgr, _number)


################################################################
#                    Задача коммивояжера
#  (поиск оптимального маршрута с посещением нескольких точек)
################################################################
# Создание тура проходящего через несколько точек (задача коммивояжера)
# hnet - идентификатор графа сети
# parm - параметры построения графа удаленности
# Возвращает идентификатор задачи коммивояжера
# При ошибке возвращает 0

    onCreateTSP_t = mapsyst.GetProcAddress(acceslib,HTSP,'onCreateTSP', HNET, ctypes.POINTER(TSPPARM))
    def onCreateTSP(_hnet: HNET, _parm: ctypes.POINTER(TSPPARM)) -> HTSP:
        return onCreateTSP_t (_hnet, _parm)


# Удаление задачи коммивояжера
# htsp - идентификатор задачи коммивояжера

    onFreeTSP_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreeTSP', HTSP)
    def onFreeTSP(_htsp: HTSP) -> ctypes.c_void_p:
        return onFreeTSP_t (_htsp)


# Возвращает количество маршрутов в туре
# htsp - идентификатор задачи коммивояжера

    onGetTSPPathCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetTSPPathCount', HTSP)
    def onGetTSPPathCount(_htsp: HTSP) -> int:
        return onGetTSPPathCount_t (_htsp)


# Возвращает маршрут между парой пунктов в туре
# Освобождать HPATH не надо, это делается автоматически в onFreeTSP
# htsp    - идентификатор задачи коммивояжера
# pathnum - номер маршрута в туре (от 0)
# При ошибке возвращает 0

    onGetTSPPath_t = mapsyst.GetProcAddress(acceslib,HPATH,'onGetTSPPath', HTSP, ctypes.c_int)
    def onGetTSPPath(_htsp: HTSP, _pathnum: int) -> HPATH:
        return onGetTSPPath_t (_htsp, _pathnum)


# Возвращает номер пункта в начале маршрута (от 0)
# htsp    - идентификатор задачи коммивояжера
# pathnum - номер маршрута в туре (от 0)
# При ошибке возвращает -1

    onGetTSPPathFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetTSPPathFirstPoint', HTSP, ctypes.c_int)
    def onGetTSPPathFirstPoint(_htsp: HTSP, _pathnum: int) -> int:
        return onGetTSPPathFirstPoint_t (_htsp, _pathnum)


# Возвращает номер пункта в конце маршрута
# htsp    - идентификатор задачи коммивояжера
# pathnum - номер маршрута в туре (от 0)
# При ошибке возвращает -1

    onGetTSPPathLastPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'onGetTSPPathLastPoint', HTSP, ctypes.c_int)
    def onGetTSPPathLastPoint(_htsp: HTSP, _pathnum: int) -> int:
        return onGetTSPPathLastPoint_t (_htsp, _pathnum)

except Exception as e:
    print(e)
    acceslib = 0