#!/usr/bin/env python3

# ********************************************************************
# *                                                                  *
# *              Copyright (c) PANORAMA Group 1991-2026              *
# *                      All Rights Reserved                         *
# *                                                                  *
# ********************************************************************

import os
import ctypes
import mapsyst
import maptype

PACK_WIDTH = 1

#-----------------------------
class TEMPHOBJSET(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hObjSet",maptype.HOBJSET)]
    def __init__(self, value : maptype.HOBJSET = 0):
        super().__init__()
        self.hObjSet = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hObjSet != 0:
            mapFreeObjectSet(self.hMap)
        self.hObjSet = 0
    def HOBJSET(self):
        return self.hObjSet
    def __eq__(self, other):
        return self.hObjSet == other.hObjSet
    def __ne__(self, other):
        return self.hObjSet != other.hObjSet
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    curLib = mapsyst.LoadLibrary(gisaccesname)

# Найти видимые объекты в окрестности точки, заданной прямоугольной рамкой
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# frame - прямоугольная область поиска объекта в системе координат, заданной переменной place
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# place - система координат (PP_PLANE, PP_GEO, ...)
# hpaint - идентификатор контекста отображения для многопоточного вызова функции отображения,
#     создается функцией mapCreatePaintControl
# Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
# Координаты области пересчитываются в пикселы в текущем масштабе отображения
# В список выбранных могут попасть объекты, которые отображаются в текущем масштабе рядом с областью
# выбора в пределах нескольких пикселов
# Площадные объекты выбираются в пределах рамки размером 512х512 пикселов в текущем масштабе изображения
# Выбор объекта в "точке карты" рекомендуется начинать с последнего, который нарисован поверх остальных
# (это чуть медленнее прямого поиска)
# При поиске с флажками WO_NEXT, WO_BACK параметр hobj должен содержать результат предыдущего поиска
# Поиск выполнется среди тех объектов, которые видны на экране, если не установлен флаг WO_VISUALIGNORE
# Если объект найден - возвращает значение hobj, иначе - 0

    mapWhatObjectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapWhatObjectEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapWhatObjectEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _place: int, _hpaint: maptype.HPAINT) -> maptype.HOBJ:
        return mapWhatObjectEx_t (_hmap, _hobj, _frame, _flag, _place, _hpaint)


# Найти видимые объекты в окрестности точки, заданной прямоугольной рамкой, удовлетворяющие условиям поиска
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# frame - прямоугольная область поиска объекта в системе координат, заданной переменной place
# hselect - контекст условий отбора объектов
# flag  - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# place - система координат (PP_PLANE, PP_GEO, ...)
# hpaint - идентификатор контекста отображения для многопоточного вызова функции отображения,
#          создается функцией mapCreatePaintControl
# Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
# Если объект найден - возвращает значение hobj, иначе - 0

    mapWhatObjectBySelectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapWhatObjectBySelectEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapWhatObjectBySelectEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _hselect: maptype.HSELECT, _flag: int, _place: int, _hpaint: maptype.HPAINT) -> maptype.HOBJ:
        return mapWhatObjectBySelectEx_t (_hmap, _hobj, _frame, _hselect, _flag, _place, _hpaint)


# Найти активные видимые объекты в окрестности точки, заданной прямоугольной рамкой
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# frame - прямоугольная область поиска объекта в системе координат, заданной переменной place
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# place - система координат (PP_PLANE, PP_GEO, ...)
# Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
# Активные объекты - доступные для интерактивного выбора (оператором)
# Установка условий поиска выполняется функцией mapSetSiteActiveSelect
# Если объект найден - возвращает 1, иначе - 0

    mapWhatActiveObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWhatActiveObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long)
    def mapWhatActiveObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int = maptype.WO_LAST, _place: int = maptype.PP_PICTURE) -> int:
        return mapWhatActiveObject_t (_hmap, _hobj, _frame, _flag, _place)


# Установить порядок обнаружения подписей при поиске объектов в точке карты
# hmap - идентификатор открытых данных (документа)
# order - порядок выбора подписи
# Если order равен нулю, то при переборе в обратном порядке (WO_LAST, WO_PREV) сначала будут идти подписи
# Если order не равен нулю, то при переборе в обратном порядке подписи будут последними

    mapSetTextPlace_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTextPlace', maptype.HMAP, ctypes.c_long)
    def mapSetTextPlace(_hmap: maptype.HMAP, _order: int) -> ctypes.c_void_p:
        return mapSetTextPlace_t (_hmap, _order)


# Запросить порядок обнаружения подписей при поиске объектов в точке карты
# hmap - идентификатор открытых данных (документа)
# Если при переборе в обратном порядке (WO_LAST, WO_PREV) сначала будут идти подписи - возвращает 0
# Если при переборе в обратном порядке подписи будут последними - возвращает 1

    mapGetTextPlace_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextPlace', maptype.HMAP)
    def mapGetTextPlace(_hmap: maptype.HMAP) -> int:
        return mapGetTextPlace_t (_hmap)


# Установить флаг пропуска объектов оформления при поиске объектов в точке карты
# flag - флаг пропуска объектов оформления: 1 - пропускать, 0 - не пропускать

    mapSetSkipDesignObjectFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetSkipDesignObjectFlag', ctypes.c_long)
    def mapSetSkipDesignObjectFlag(_flag: int) -> ctypes.c_void_p:
        return mapSetSkipDesignObjectFlag_t (_flag)


# Запросить флаг пропуска объектов оформления при поиске объектов в точке карты
# Возвращает флаг пропуска объектов оформления: 1 - пропускать, 0 - не пропускать

    mapGetSkipDesignObjectFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSkipDesignObjectFlag')
    def mapGetSkipDesignObjectFlag() -> int:
        return mapGetSkipDesignObjectFlag_t ()


# Найти объект по уникальному номеру объекта в карте с заданным названием листа (номенклатуры)
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# Если объект найден - возвращает значение hobj, иначе - 0

    mapSeekObjectUn_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekObjectUn', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapSeekObjectUn(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _sheetname: mapsyst.WTEXT, _key: int) -> maptype.HOBJ:
        return mapSeekObjectUn_t (_hmap, _hobj, _sheetname.buffer(), _key)


# Найти объект по уникальному номеру объекта в заданном листе карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetnumber - номер листа карты (с 1)
# key - уникальный номер объекта в листе карты
# Если объект найден - возвращает значение hobj, иначе - 0

    mapSeekObjectInList_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekObjectInList', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSeekObjectInList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _key: int) -> maptype.HOBJ:
        return mapSeekObjectInList_t (_hmap, _hsite, _hobj, _sheetnumber, _key)


# Найти порядковый номер объекта по уникальному номеру объекта в карте с заданным названием листа (номенклатуры)
# hmap - идентификатор открытых данных (документа)
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов)
# (при сортировке карты записи удаленных объектов исключаются, порядковые номера объектов изменяются)
# При ошибке возвращает ноль

    mapSeekObjectNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekObjectNumberUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSeekObjectNumberUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapSeekObjectNumberUn_t (_hmap, _sheetname.buffer(), _key)


# Найти порядковый номер объекта по уникальному номеру объекта в заданном листе карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# sheetnumber - номер листа карты (с 1)
# key - уникальный номер объекта в листе карты
# Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов)
# (при сортировке карты записи удаленных объектов исключаются, порядковые номера объектов изменяются)
# При ошибке возвращает ноль

    mapSeekObjectNumberEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekObjectNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSeekObjectNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _sheetnumber: int, _key: int) -> int:
        return mapSeekObjectNumberEx_t (_hmap, _hsite, _sheetnumber, _key)


# Найти объект по GUID в листе (значение семантики с кодом OBJECTGUID = 32799)
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetnumber - номер листа карты (с 1)
# guid - структура, содержащая значение GUID в двоичной форме
# Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов)
# При ошибке возвращает ноль

    mapSeekObjectByGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekObjectByGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.INT64TWO))
    def mapSeekObjectByGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _guid: ctypes.POINTER(maptype.INT64TWO)) -> int:
        return mapSeekObjectByGUID_t (_hmap, _hsite, _hobj, _sheetnumber, _guid)


# Найти объект по GUID в листе (значение семантики OBJECTGUID 32799)
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetnumber - номер листа карты (с 1)
# guid - строка, содержащая значение GUID (32 или 36 символов, если с тире)
# Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов)
# При ошибке возвращает ноль

    mapSeekObjectByStringGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekObjectByStringGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_char_p)
    def mapSeekObjectByStringGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _guid: ctypes.c_char_p) -> int:
        return mapSeekObjectByStringGUID_t (_hmap, _hsite, _hobj, _sheetnumber, _guid)


# Найти объект по заданным условиям отбора среди всех объектов
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# hselect - контекст условий отбора объектов
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# При поиске с флажками WO_NEXT, WO_BACK параметр hobj должен содержать результат предыдущего поиска
# Если объект не найден - возвращает ноль

    mapSeekSelectObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSelectObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int = maptype.WO_FIRST) -> int:
        return mapSeekSelectObject_t (_hmap, _hobj, _hselect, _flag)


# Запросить число объектов на карте, удовлетворяющих условиям отбора
# hselect - контекст условий отбора объектов
# flag - флаг условий поиска:
#     WO_INMAP - подсчет выполняется на той карте, для которой был создан контекст поиска,
#     иначе - поиск по всем картам
# При ошибке возвращает ноль

    mapSeekSelectObjectCountEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSelectObjectCountEx', maptype.HMAP, maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectObjectCountEx(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _flag: int) -> int:
        return mapSeekSelectObjectCountEx_t (_hmap, _hselect, _flag)


# Найти ближайший объект по заданным условиям среди всех объектов
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# srcpoint - координаты исходной точки (в метрах), относительно которой выполняется поиск
# destpoint - поле для размещения координат ближайшей виртуальной точки на контуре объекта (в метрах документа)
# hselect - контекст условий отбора объектов
# flag - дополнительные условия поиска объектов: WO_CANCEL, WO_INMAP, WO_VISUAL (значения WO_FIRST, WO_NEXT не учитываются)
# Если flag равен 0, выполняется поиск по всем картам среди всех объектов
# Если объект не найден - возвращает ноль

    mapSeekSelectNearestObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSelectNearestObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectNearestObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _hselect: maptype.HSELECT, _flag: int = maptype.WO_INMAP | maptype.WO_VISUAL) -> int:
        return mapSeekSelectNearestObject_t (_hmap, _hobj, _srcpoint, _destpoint, _hselect, _flag)


# Найти объект, подходящий условиям поиска соседних объектов в первой и последней точках контура
# hobj - идентификатор объекта карты в памяти, для которого ищутся соседи
# side - сторона объекта, для которой ищутся соседи (0 - первая точка, иначе - последняя)
# hdest - идентификатор объекта карты в памяти, в котором будет размещен результат
# destpoint - поле для размещения координат ближайшей найденной точки (в метрах)
# radius - радиус поиска (максимальный радиус поиска = 7 км)
# Списки видов объектов для первой и последней точек контура и список семантик, которые должны иметь совпадающие значения
# с семантиками объекта, должны быть настроены в классификаторе заблаговременно
# Если поиск выполняется для второй точки (side != 0), то входное значение (hobj) будет пропущено при поиске
# Если условия для соседей заданы, но сосед не найден - возвращает -1
# Если у объекта отсутствуют семантики, которые должны совпадать с семантиками соседних объектов - возвращает -2
# Если условия не заданы - возвращает ноль

    mapFindAdjustObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFindAdjustObject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapFindAdjustObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _side: int, _hdest: maptype.HOBJ, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float) -> int:
        return mapFindAdjustObject_t (_hmap, _hobj, _side, _hdest, _destpoint, _radius)


# Найти объект по заданным условиям среди отображаемых объектов
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# hselect - контекст условий отбора объектов
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# При поиске с флажками WO_NEXT, WO_BACK параметр hobj должен содержать результат предыдущего поиска
# Если объект не найден - возвращает ноль

    mapSeekViewObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekViewObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekViewObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int = maptype.WO_FIRST) -> maptype.HOBJ:
        return mapSeekViewObject_t (_hmap, _hobj, _hselect, _flag)


# Найти объект, имеющий примыкающие участки контура с заданным объектом
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор существующего объекта, для которого надо найти примыкающие участки
# hdest - идентификатор существующего объекта, в котором будет размещен результат
# section - указатель на структуру для записи описания найденного участка
# hselect - контекст условий отбора объектов
# maxdistance - максимальное расстояние между точками участков в метрах
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# mode - режим поиска общих участков:
#     0 - искать общие участки только с внешним контуром,
#     1 - с учетом подобъектов (нумерация точек объекта и подобъектов MAPADJACENTSECTION::first и last - сквозная)
# Поиск выполняется в карте, на которой находится выбранный объект
# При поиске с флажками WO_NEXT, WO_BACK параметр hdest должен содержать результат предыдущего поиска
# Если объект не найден - возвращает ноль, иначе - возвращает номер участка

    mapSeekAdjacentObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekAdjacentObject', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTSECTION), maptype.HSELECT, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSeekAdjacentObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hdest: maptype.HOBJ, _section: ctypes.POINTER(maptype.MAPADJACENTSECTION), _hselect: maptype.HSELECT, _maxdistance: float = 0.0, _flag: int = maptype.WO_FIRST | maptype.WO_INMAP, _mode: int = 0) -> int:
        return mapSeekAdjacentObject_t (_hmap, _hobj, _hdest, _section, _hselect, _maxdistance, _flag, _mode)


# Найти объекты, имеющие примыкающие участки контура с заданным объектом
# Поиск ведется в карте, где находится выбранный объект
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор существующего объекта карты, для которого надо найти примыкающие участки
# sectionlist - память для записи общих участков контуров примыкающих объектов
# sectioncount - максимальное количество общих участков контуров
# hselect - контекст условий отбора объектов
# maxdistance - максимальное расстояние между точками участков в метрах
# excludereverse - признак исключения обратных примыкающих участков:
#     0 - записывать прямые и обратные примыкающие участки,
#     1 - обратные примыкающие участки (с одинаковой первой и последней точкой) не записывать
# mode - режим поиска общих участков:
#     0 - искать общие участки только с внешним контуром,
#     1 - с учетом подобъектов (нумерация точек объекта и подобъектов MAPADJACENTLISTEX::First и Last - сквозная)
# Поиск выполняется в карте, на которой находится выбранный объект
# Если соседи не найдены - возвращает ноль, иначе - количество соседей

    mapSeekAdjacentListEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekAdjacentListEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTLISTEX), ctypes.c_long, maptype.HSELECT, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSeekAdjacentListEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _sectionlist: ctypes.POINTER(maptype.MAPADJACENTLISTEX), _sectioncount: int, _hselect: maptype.HSELECT, _maxdistance: float = 0.0, _excludereverse: int = 0, _mode: int = 0) -> int:
        return mapSeekAdjacentListEx_t (_hmap, _hobj, _sectionlist, _sectioncount, _hselect, _maxdistance, _excludereverse, _mode)


# Создать процесс поиска примыкающих участков контура для заданного подобъекта
# hmap - идентификатор открытых данных (документа)
# hselect - контекст условий отбора объектов
# hobj - идентификатор существующего объекта, для которого надо найти примыкающие участки
# subject - номер подобъекта c 0
# hdest - идентификатор существующего объекта, в котором будет размещен результат
# maxdistance - максимальное расстояние между точками участков в метрах
# По окончании обработки необходимо вызвать mapFreeSeekConnectPath
# При ошибке возвращает 0

    mapCreateSeekConnectPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateSeekConnectPath', maptype.HMAP, maptype.HSELECT, maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_double)
    def mapCreateSeekConnectPath(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _hobj: maptype.HOBJ, _subject: int, _hdest: maptype.HOBJ, _maxdistance: float = maptype.DELTANULL) -> ctypes.c_void_p:
        return mapCreateSeekConnectPath_t (_hmap, _hselect, _hobj, _subject, _hdest, _maxdistance)


# Освободить ресурсы, выделенные в mapCreateSeekConnectPath
# seekconnect - идентификатор процесса поиска

    mapFreeSeekConnectPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeSeekConnectPath', ctypes.c_void_p)
    def mapFreeSeekConnectPath(_seekconnect: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSeekConnectPath_t (_seekconnect)


# Запросить следующий примыкающий участок для заданного подобъекта
# seekconnect - идентификатор процесса поиска
# section - указатель на структуру для записи описания найденного участка
# Возможен возврат участка из одной точки (касание в одной точке)
# Для замкнутых объектов участок может проходить через первую (последнюю) точку
# Направление участка на соседнем объекте всегда совпадает с направлением цифрования
# Направление на главном объекте устанавливается в CONNECTPATH::IsForward
# При ошибке или если смежный участок не найден возвращает ноль

    mapSeekConnectPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekConnectPath', ctypes.c_void_p, ctypes.POINTER(maptype.CONNECTPATH))
    def mapSeekConnectPath(_seekconnect: ctypes.c_void_p, _section: ctypes.POINTER(maptype.CONNECTPATH)) -> int:
        return mapSeekConnectPath_t (_seekconnect, _section)


# Проверить соответствие объекта условиям отбора объектов
# hobj - идентификатор существующего объекта карты
# hselect - контекст условий отбора объектов
# Если условия поиска не заданы (hselect = 0), возвращает 1
# Если соответствует - возвращает ненулевое значение, иначе - 0

    mapTestObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTestObject', maptype.HOBJ, maptype.HSELECT)
    def mapTestObject(_hobj: maptype.HOBJ, _hselect: maptype.HSELECT) -> int:
        return mapTestObject_t (_hobj, _hselect)


# Проверить соответствие объекта условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор существующего объекта карты
# Для установки условий обобщенного поиска объектов используются функции: mapSetTotalSeekMapRule,
# mapSetTotalSeekViewRule, mapTotalSeekSampleAppendObject, mapSetTotalSeekSampleUn, mapSetTotalSeekAccess
# Если соответствует - возвращает ненулевое значение, иначе - 0

    mapTotalTestObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalTestObject', maptype.HMAP, maptype.HOBJ)
    def mapTotalTestObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        return mapTotalTestObject_t (_hmap, _hobj)


# Выбор объекта по номеру листа и последовательному номеру объекта
# (прямой доступ к объекту без перебора)
# hMap     - идентификатор открытой карты,
# hSite    - идентификатор открытой пользовательской карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска;
# list     - номер листа (для пользовательской карты всегда 1);
# object   - последовательный номер объекта в листе
# (начиная с 1 до mapGetObjectCount(...) или mapGetSiteObjectCount(...)).
# Если объект имеет признак "удален" - возвращает 1 !
# При успешном выполнении возвращает значение info.
# При ошибке возвращает ноль

    mapReadObjectByNumber_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapReadObjectByNumber', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapReadObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _object: int) -> maptype.HOBJ:
        return mapReadObjectByNumber_t (_hmap, _hsite, _info, _list, _object)


# Найти объект по номеру листа и порядковому номеру объекта (прямой доступ к объекту без перебора)
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetnumber - номер листа карты, от 1 до mapGetSiteListCount(...)
# objectnumber - порядковый номер объекта в листе, от 1 до mapGetSiteObjectCount(...)
# Если объект имеет признак "удален", то функция возвращает 1
# При успешном выполнении возвращает значение 2
# При ошибке возвращает ноль

    mapReadObjectByNumberEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadObjectByNumberEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapReadObjectByNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _objectnumber: int) -> int:
        return mapReadObjectByNumberEx_t (_hmap, _hsite, _hobj, _sheetnumber, _objectnumber)


# Выбор объекта по номеру листа и уникальному номеру объекта
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# sheetnumber - номер листа карты, от 1 до mapGetSiteListCount(...)
# key - уникальный номер объекта в листе карты
# Если объект имеет признак "удален", то функция возвращает 1
# При успешном выполнении возвращает значение 2
# При ошибке возвращает ноль

    mapReadObjectByKeyEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadObjectByKeyEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapReadObjectByKeyEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _key: int) -> int:
        return mapReadObjectByKeyEx_t (_hmap, _hsite, _hobj, _sheetnumber, _key)


# Запросить правило обобщенного поиска объектов по картам
# hmap - идентификатор открытых данных (документа)
# Возвращает: от 0 до mapGetSiteCount(...) - номер карты, по которой будет выполняться поиск
#     (-1) - поиск будет выполняться по всем картам
# При ошибке возвращает число (-2)

    mapGetTotalSeekMapRule_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalSeekMapRule', maptype.HMAP)
    def mapGetTotalSeekMapRule(_hmap: maptype.HMAP) -> int:
        return mapGetTotalSeekMapRule_t (_hmap)


# Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# mapnumber - номер карты в открытых данных, от 0 до mapGetSiteCount(...)
# Если на карте есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapIsTotalSeekMapRule_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTotalSeekMapRule', maptype.HMAP, ctypes.c_long)
    def mapIsTotalSeekMapRule(_hmap: maptype.HMAP, _mapnumber: int) -> int:
        return mapIsTotalSeekMapRule_t (_hmap, _mapnumber)


# Установить правило обобщенного поиска объектов по картам
# hmap - идентификатор открытых данных (документа)
# mapnumber - номер карты, по которой выполняется поиск
# Если number = -1, то поиск будет выполняться по всем картам

    mapSetTotalSeekMapRule_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTotalSeekMapRule', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekMapRule(_hmap: maptype.HMAP, _mapnumber: int) -> ctypes.c_void_p:
        return mapSetTotalSeekMapRule_t (_hmap, _mapnumber)


# Установить правило обобщенного поиска объектов для отображаемых объектов карты
# hmap - идентификатор открытых данных (документа)
# view - признак поиска среди отображаемых объектов (1), использовать mapSeekViewObject
# Если view = 0, то поиск будет выполняться среди всех объектов, использовать mapSeekSelectObject

    mapSetTotalSeekViewRule_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTotalSeekViewRule', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekViewRule(_hmap: maptype.HMAP, _view: int = 0) -> ctypes.c_void_p:
        return mapSetTotalSeekViewRule_t (_hmap, _view)


# Запросить правило обобщенного поиска для отображаемых объектов карты
# hmap - идентификатор открытых данных (документа)
# Возвращает: 1 - поиск среди отображаемых объектов
#             0 - поиск среди всех объектов

    mapGetTotalSeekViewRule_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalSeekViewRule', maptype.HMAP)
    def mapGetTotalSeekViewRule(_hmap: maptype.HMAP) -> int:
        return mapGetTotalSeekViewRule_t (_hmap)


# Добавить объект в список условий обобщенного поиска по уникальному номеру объекта и названию листа
# hmap - идентификатор открытых данных (документа)
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# Если для карты установлены условия поиска по номерам объектов, то остальные условия (слой, локализация...) игнорируются
# Если карта не найдена - возвращает ноль

    mapSetTotalSeekSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetTotalSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSetTotalSeekSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapSetTotalSeekSampleUn_t (_hmap, _sheetname.buffer(), _key)


# Добавить объект в список условий обобщенного поиска
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapTotalSeekSampleAppendObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalSeekSampleAppendObject', maptype.HOBJ)
    def mapTotalSeekSampleAppendObject(_hobj: maptype.HOBJ) -> int:
        return mapTotalSeekSampleAppendObject_t (_hobj)


# Установить условия обобщенного поиска объектов по всем картам
# hmap - идентификатор открытых данных (документа)
# acceess - признак отбора объектов:
#     0 - отключить отбор всех объектов всех карт (отключает все локализации и чистит списки)
#     1 - все объекты доступны при поиске с помощью mapTotalSeekObject
# Альтернатива перебору условий поиска для всех карт
# (перед применением mapSetTotalSeekSample доступ может быть отключен)
# При ошибке возвращает ноль

    mapSetTotalSeekAccess_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetTotalSeekAccess', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekAccess(_hmap: maptype.HMAP, _access: int) -> int:
        return mapSetTotalSeekAccess_t (_hmap, _access)


# Выделить на карте объекты, соответствующие условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# hdc - идентификатор контекста устройства отображения
# rect - координаты прямоугольной области отображения (в пикселах)
# color - цвет, которым будут выделяться объекты на карте
# hpaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# При ошибке возвращает ноль

    mapTotalPaintSelectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalPaintSelectEx', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.COLORREF, maptype.HPAINT)
    def mapTotalPaintSelectEx(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _color: maptype.COLORREF, _hpaint: maptype.HPAINT) -> int:
        return mapTotalPaintSelectEx_t (_hmap, _hdc, _rect, _color, _hpaint)


# Выделить на карте объекты, соответствующие условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# hwnd - идентификатор окна вывода
# color - цвет, которым будут выделяться объекты на карте,
# point - координаты верхнего левого угла окна на карте в системе координат, заданной переменной place
# place - система координат (PP_PLANE, PP_GEO, ...)
# При ошибке возвращает ноль

    mapTotalViewSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalViewSelect', maptype.HMAP, maptype.HWND, ctypes.POINTER(maptype.DOUBLEPOINT), maptype.COLORREF, ctypes.c_long)
    def mapTotalViewSelect(_hmap: maptype.HMAP, _hwnd: maptype.HWND, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _color: maptype.COLORREF, _place: int) -> int:
        return mapTotalViewSelect_t (_hmap, _hwnd, _point, _color, _place)


# Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если на карте есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapIsTotalSeekSiteObjectNotEmpty_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTotalSeekSiteObjectNotEmpty', maptype.HMAP, maptype.HSITE)
    def mapIsTotalSeekSiteObjectNotEmpty(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsTotalSeekSiteObjectNotEmpty_t (_hmap, _hsite)


# Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapIsTotalSeekObjectNotEmpty_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTotalSeekObjectNotEmpty', maptype.HMAP)
    def mapIsTotalSeekObjectNotEmpty(_hmap: maptype.HMAP) -> int:
        return mapIsTotalSeekObjectNotEmpty_t (_hmap)


# Запросить количество объектов, соответствующих условиям обобщенного поиска
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapTotalSeekObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalSeekObjectCount', maptype.HMAP)
    def mapTotalSeekObjectCount(_hmap: maptype.HMAP) -> int:
        return mapTotalSeekObjectCount_t (_hmap)


# Запросить количество объектов, соответствующих условиям обобщенного поиска
# hmap - идентификатор открытых данных (документа)
# flag - дополнительные условия поиска (например, WO_VISUALIGNORE - поиск без учета заданных условий отображения)
# При ошибке возвращает ноль

    mapTotalSeekObjectCountEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTotalSeekObjectCountEx', maptype.HMAP, ctypes.c_long)
    def mapTotalSeekObjectCountEx(_hmap: maptype.HMAP, _flag: int) -> int:
        return mapTotalSeekObjectCountEx_t (_hmap, _flag)


# Обобщенный поиск объектов по заданным условиям
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# При поиске с флажками WO_NEXT, WO_BACK параметр hobj должен указывать на результат предыдущего поиска
# Условия обобщенного поиска вводятся предварительно (используются функции mapGetSiteViewSelect, mapGetSiteSeekSelect()...)
# Если объект не найден - возвращает ноль

    mapTotalSeekObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapTotalSeekObject', maptype.HMAP, maptype.HOBJ, ctypes.c_long)
    def mapTotalSeekObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _flag: int) -> maptype.HOBJ:
        return mapTotalSeekObject_t (_hmap, _hobj, _flag)


# Обобщенный поиск объектов по заданным условиям
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT, WO_BACK, ...)
# mapnumber - номер карты в открытых данных, от 0 до mapGetSiteCount(...)
# sheetnumber - номер листа карты (с 1)
# objectnumber - номер объекта (с 1), с которого будет продолжен поиск
# Если flag = WO_NEXT, то поиск следующего продолжается с objectnumber + 1
# Если flag = WO_BACK, то поиск следующего продолжается с objectnumber - 1
# При поиске с флажками WO_NEXT, WO_BACK параметры mapnumber, sheetnumber, objectnumber должны быть заданы
# Если объект не найден - возвращает ноль

    mapTotalSeekObjectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapTotalSeekObjectEx', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapTotalSeekObjectEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _flag: int, _mapnumber: int, _sheetnumber: int, _objectnumber: int) -> maptype.HOBJ:
        return mapTotalSeekObjectEx_t (_hmap, _hobj, _flag, _mapnumber, _sheetnumber, _objectnumber)


# Запросить состояние условий поиска
# hmap - идентификатор открытых данных (документа)
# При любом изменении условий поиска значение состояния увеличивается
# При ошибке возвращает ноль

    mapGetTotalSeekState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalSeekState', maptype.HMAP)
    def mapGetTotalSeekState(_hmap: maptype.HMAP) -> int:
        return mapGetTotalSeekState_t (_hmap)


# Установить признак отбора объектов карты по обобщенным условиям поиска
# hmap - идентификатор открытых данных (документа)
# flag - признак выделения объектов по обобщенным условиям поиска: 1 - включить, 0 - отключить
# Перед вызовом функций mapTotalPaintSelectEx или mapTotalSeekObjectEx рекомендуется установить flag = 1
# Никакого действия, кроме установки значения, не производит
# Применяется для связи между различными модулями

    mapSetTotalSelectFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTotalSelectFlag', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSelectFlag(_hmap: maptype.HMAP, _flag: int) -> ctypes.c_void_p:
        return mapSetTotalSelectFlag_t (_hmap, _flag)


# Запросить признак отбора объектов карты по обобщенным условиям поиска
# hmap - идентификатор открытых данных (документа)
# Если результат равен нулю, отбор объектов карты по обобщенным условиям поиска не выполняется

    mapGetTotalSelectFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalSelectFlag', maptype.HMAP)
    def mapGetTotalSelectFlag(_hmap: maptype.HMAP) -> int:
        return mapGetTotalSelectFlag_t (_hmap)


# Определить общие габариты объектов, соответствующих обобщенным условиям поиска
# hmap - идентификатор открытых данных (документа)
# border - указатель на структуру для размещения координат общих габаритов объектов в метрах
# При ошибке возвращает ноль

    mapGetTotalSeekBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalSeekBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapGetTotalSeekBorder(_hmap: maptype.HMAP, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetTotalSeekBorder_t (_hmap, _border)


# Проверить наличие списка объектов в контекстах обобщенных условий поиска хотя бы для одной карты
# hmap - идентификатор открытых данных (документа)
# Если в контекстах условий есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapIsTotalSeekSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTotalSeekSample', maptype.HMAP)
    def mapIsTotalSeekSample(_hmap: maptype.HMAP) -> int:
        return mapIsTotalSeekSample_t (_hmap)


# Инвертировать выделение объектов
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapInversionTotalSeek_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInversionTotalSeek', maptype.HMAP)
    def mapInversionTotalSeek(_hmap: maptype.HMAP) -> int:
        return mapInversionTotalSeek_t (_hmap)


# Определить общие габариты объектов, соответствующие заданным условиям на карте
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# sheetnumber - номер листа карты (с 1)
# hselect - контекст условий отбора объектов
# border - указатель на структуру для размещения координат общих габаритов объектов в системе координат, заданной переменной place
# place - система координат (PP_PLANE, PP_GEO, ...)
# При ошибке возвращает ноль

    mapGetSiteSeekBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteSeekBorder', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetSiteSeekBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _sheetnumber: int, _hselect: maptype.HSELECT, _border: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetSiteSeekBorder_t (_hmap, _hsite, _sheetnumber, _hselect, _border, _place)


# Установить имя текущей записи списка объектов условий отбора
# hmap - идентификатор открытых данных (документа)
# name - условное имя текущих условий отбора, задаваемых прикладной задачей, или по имени записи списка объектов
# При ошибке возвращает ноль

    mapSetTotalSelectRecordName_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTotalSelectRecordName', maptype.HMAP, maptype.PWCHAR)
    def mapSetTotalSelectRecordName(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetTotalSelectRecordName_t (_hmap, _name.buffer())


# Запросить имя текущей записи списка объектов условий отбора
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetTotalSelectRecordName_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetTotalSelectRecordName', maptype.HMAP)
    def mapGetTotalSelectRecordName(_hmap: maptype.HMAP) -> ctypes.POINTER(maptype.WCHAR):
        return mapGetTotalSelectRecordName_t (_hmap)


# Создать контекст условий отбора объектов карты для поиска/отображения
# hmap - идентификатор открытых данных (документа)
# В состав условий отбора объектов входят : лист, слой, локализация, диапазон номеров объектов,
# характеристики (семантика) объекта, область расположения (метрика) объекта и другие свойства
# В созданном контексте доступны все объекты карты без исключений
# Каждый созданный контекст должен быть удален вызовом mapDeleteSelectContext, когда он больше не используется
# Рекомендуется удалять контекст условий отбора объектов до закрытия карты (классификатора), с которыми он был создан
# При ошибке возвращает ноль

    mapCreateSelectContext_t = mapsyst.GetProcAddress(curLib,maptype.HSELECT,'mapCreateSelectContext', maptype.HMAP)
    def mapCreateSelectContext(_hmap: maptype.HMAP) -> maptype.HSELECT:
        return mapCreateSelectContext_t (_hmap)


# Создать копию контекста условий отбора объектов
# hselect - контекст условий отбора объектов
# Каждый созданный контекст должен быть удален, когда он больше не используется
# При ошибке возвращает ноль

    mapCreateCopySelectContext_t = mapsyst.GetProcAddress(curLib,maptype.HSELECT,'mapCreateCopySelectContext', maptype.HSELECT)
    def mapCreateCopySelectContext(_hselect: maptype.HSELECT) -> maptype.HSELECT:
        return mapCreateCopySelectContext_t (_hselect)


# Копировать контекст условий отбора объектов в существующий контекст условий
# target - контекст условий отбора, куда выполняется копирование
# source - копируемый контекст условий отбора (источник)
# При копировании контекста выполняется также смена карты (классификатора) из контекста источника
# При ошибке возвращает ноль

    mapCopySelectContext_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopySelectContext', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContext(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapCopySelectContext_t (_target, _source)


# Копировать контекст условий отбора объектов в существующий контекст условий с сохранением связи с картой исходного контекста
# target - контекст условий отбора, куда выполняется копирование
# source - копируемый контекст условий отбора (источник)
# При копировании контекста сохраняется связь с картой (с классификатором) исходного контекста
# При ошибке возвращает ноль

    mapCopySelectContextEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopySelectContextEx', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContextEx(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapCopySelectContextEx_t (_target, _source)


# Запросить идентификатор классификатора для условий отбора объектов
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapGetSelectContextRscIdent_t = mapsyst.GetProcAddress(curLib,maptype.HRSC,'mapGetSelectContextRscIdent', maptype.HSELECT)
    def mapGetSelectContextRscIdent(_hselect: maptype.HSELECT) -> maptype.HRSC:
        return mapGetSelectContextRscIdent_t (_hselect)


# Установить доступ ко всем видам данных контекста условий отбора объектов
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapClearSelectContext_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearSelectContext', maptype.HSELECT)
    def mapClearSelectContext(_hselect: maptype.HSELECT) -> int:
        return mapClearSelectContext_t (_hselect)


# Установить доступ ко всем видам данных контекста условий отбора объектов для заданной карты
# hselect - контекст условий отбора объектов
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapClearSelectContextEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearSelectContextEx', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapClearSelectContextEx(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapClearSelectContextEx_t (_hselect, _hmap, _hsite)


# Удалить контекст условий отбора объектов
# hselect - контекст условий отбора объектов

    mapDeleteSelectContext_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapDeleteSelectContext', maptype.HSELECT)
    def mapDeleteSelectContext(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapDeleteSelectContext_t (_hselect)


# Установить признак инвертирования условий отбора объектов
# hselect - контекст условий отбора объектов
# flag - признак инвертирования: 1 - включен, 0 - отключен
# Возвращает установленное значение

    mapSetInversionSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetInversionSelect', maptype.HSELECT, ctypes.c_long)
    def mapSetInversionSelect(_hselect: maptype.HSELECT, _flag: int) -> int:
        return mapSetInversionSelect_t (_hselect, _flag)


# Запросить признак инвертирования условий отбора объектов
# hselect - контекст условий отбора объектов
# Возвращает признак инвертирования: 1 - включен, 0 - отключен

    mapGetInversionSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetInversionSelect', maptype.HSELECT)
    def mapGetInversionSelect(_hselect: maptype.HSELECT) -> int:
        return mapGetInversionSelect_t (_hselect)


# Установить пересечение условий отбора объектов (target = target & source)
# target - контекст условий отбора, в который помещается результат
# source - контекст поиска с дополнительными условиями
# При выполнении операции учитываются только коды объектов, локализация, номера слоев,
# листов и списки объектов. Семантика и измерения не обрабатываются
# При ошибке возвращает ноль

    mapSelectAndSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectAndSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectAndSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapSelectAndSelect_t (_target, _source)


# Установить пересечение условий отбора объектов (target = target & source), с добавлением семантики
# target - контекст условий отбора объектов, в который помещается результат
# source - контекст условий отбора объектов с дополнительными условиями
# При выполнении операции учитываются только коды объектов, локализация и номер слоя
# Семантика из source добавляется в target
# При ошибке возвращает ноль

    mapSelectAndSelectAppendSemantics_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectAndSelectAppendSemantics', maptype.HSELECT, maptype.HSELECT)
    def mapSelectAndSelectAppendSemantics(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapSelectAndSelectAppendSemantics_t (_target, _source)


# Установить пересечение условий отбора объектов (target = target & used) c составом объектов карты
# hselect - контекст условий отбора объектов, в который помещается результат
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Результат аналогичен вызову функций mapGetSiteUsedSelect и mapSelectAndUsedSelect
# В исходном контексте условий отбора объектов будут отключены коды объектов,
# локализация, номера слоев и листов, которых нет на заданной карте
# Семантика и измерения не обрабатываются
# При ошибке возвращает ноль

    mapSelectAndUsedSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectAndUsedSelect', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSelectAndUsedSelect(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapSelectAndUsedSelect_t (_hselect, _hmap, _hsite)


# Объединить условия отбора объектов (target = target OR source)
# target - контекст условий отбора объектов, в который помещается результат
# source - контекст условий отбора объектов с дополнительными условиями
# При выполнении операции учитываются только коды объектов, локализация, номер слоя и списки объектов
# Семантика и измерения не обрабатываются
# При ошибке возвращает ноль

    mapSelectOrSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectOrSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectOrSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapSelectOrSelect_t (_target, _source)


# Проверить наличие активных условий отбора объектов
# hselect - контекст условий отбора объектов
# Если по условиям поиска все объекты выбираются без исключений - возвращает ноль, иначе - ненулевое значение

    mapIsSelectActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSelectActive', maptype.HSELECT)
    def mapIsSelectActive(_hselect: maptype.HSELECT) -> int:
        return mapIsSelectActive_t (_hselect)


# Установить признак доступности объектов слоя
# hselect - контекст условий отбора объектов
# layer - номер слоя, начинается с 0
# check - признак доступности слоя: 1 - включен, 0 - отключен
# Если layer = -1, то устанавливается доступ ко всем слоям

    mapSelectLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectLayer', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectLayer(_hselect: maptype.HSELECT, _layer: int, _check: int) -> ctypes.c_void_p:
        return mapSelectLayer_t (_hselect, _layer, _check)


# Запросить признак доступности объектов слоя
# hselect - контекст условий отбора объектов
# layer - номер слоя, начинается с 0. Если layer = -1, то проверяется доступ ко всем слоям
# Если при layer = -1 возвращает 0 - один или более слоев недоступны, иначе - доступны все слои
# Возвращает признак доступности слоя: 1 - включен, 0 - отключен

    mapCheckLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckLayer', maptype.HSELECT, ctypes.c_long)
    def mapCheckLayer(_hselect: maptype.HSELECT, _layer: int) -> int:
        return mapCheckLayer_t (_hselect, _layer)


# Установить признак доступности объектов расширенного слоя (класса) из дерева слоев
# hselect - контекст условий отбора объектов
# layer - номер расширенного слоя (класса) из дерева слоев, начинается с 256
# check - признак доступности слоя: 1 - включен, 0 - отключен
# Если layer = -1, то устанавливается доступ ко всем слоям

    mapSelectClass_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectClass', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectClass(_hselect: maptype.HSELECT, _layer: int, _check: int) -> ctypes.c_void_p:
        return mapSelectClass_t (_hselect, _layer, _check)


# Запросить признак доступности объектов расширенного слоя (класса) из дерева слоев
# hselect - контекст условий отбора объектов
# layer - номер расширенного слоя (класса) из дерева слоев, начинается с 256
# Если при layer = -1 возвращает 0 - один или более слоев недоступны, иначе - доступны все слои
# Возвращает признак доступности слоя: 1 - включен, 0 - отключен

    mapCheckClass_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckClass', maptype.HSELECT, ctypes.c_long)
    def mapCheckClass(_hselect: maptype.HSELECT, _layer: int) -> int:
        return mapCheckClass_t (_hselect, _layer)


# Установить признак доступности объектов листа карты
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1). Если равен -1, то устанавливается доступ ко всем листам
# check - признак доступности листа: 1 - включен, 0 - отключен

    mapSelectList_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectList', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectList(_hselect: maptype.HSELECT, _sheetnumber: int, _check: int) -> ctypes.c_void_p:
        return mapSelectList_t (_hselect, _sheetnumber, _check)


# Запросить признак доступности объектов листа карты
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1). Если равен -1, то проверяется доступ ко всем листам
# Если при sheetnumber = -1 возвращает 0 - один или более листов недоступны, иначе - доступны все листы
# Возвращает признак доступности листа: 1 - включен, 0 - отключен

    mapCheckList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckList', maptype.HSELECT, ctypes.c_long)
    def mapCheckList(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        return mapCheckList_t (_hselect, _sheetnumber)


# Включить доступ к объектам c листом, слоем, локализацией и кодом, как у переданного объекта
# hselect - контекст условий отбора объектов
# hobj - идентификатор существующего объекта карты

    mapSelectMapObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectMapObject', maptype.HSELECT, maptype.HOBJ)
    def mapSelectMapObject(_hselect: maptype.HSELECT, _hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapSelectMapObject_t (_hselect, _hobj)


# Установить признак доступности объектов c заданным внутренним кодом в классификаторе
# hselect - контекст условий отбора объектов
# code - внутренний код (порядковый номер объекта в классификаторе), от 1 до mapGetRscObjectCount(...)
# check - признак доступности объекта: 1 - включен, 0 - отключен
# Если code = -1, то устанавливается доступ ко всем объектам

    mapSelectObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectObject', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectObject(_hselect: maptype.HSELECT, _code: int, _check: int) -> ctypes.c_void_p:
        return mapSelectObject_t (_hselect, _code, _check)


# Установить признак доступности объектов c заданным внешним кодом и локализацией в классификаторе
# hselect - контекст условий отбора объектов
# excode - внешний код объекта (объекты серии имеют общий внешний код)
# local - код локализации объекта (LOCAL_LINE, LOCAL_SQUARE ...)
# check - признак доступности объекта: 1 - включен, 0 - отключен
# Если check != 0, то устанавливается доступ ко всем объектам серии (или одному коду объекта),
# путем включения внутренних кодов и локализации
# Если check == 0, то отключаются только внутренние коды объектов (состояние локализации не меняется)

    mapSelectObjectExcode_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectObjectExcode', maptype.HSELECT, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectObjectExcode(_hselect: maptype.HSELECT, _excode: int, _local: int, _check: int) -> ctypes.c_void_p:
        return mapSelectObjectExcode_t (_hselect, _excode, _local, _check)


# Запросить признак доступности объектов c заданным внутренним кодом в классификаторе
# hselect - контекст условий отбора объектов
# code - внутренний код (порядковый номер объекта в классификаторе), от 1 до mapGetRscObjectCount(...)
# Если code = -1, то проверяется доступ ко всем объектам
# Если при code = -1 возвращает 0 - один или более объектов недоступны, иначе - доступны все объекты
# Возвращает признак доступности объекта: 1 - включен, 0 - отключен

    mapCheckObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckObject', maptype.HSELECT, ctypes.c_long)
    def mapCheckObject(_hselect: maptype.HSELECT, _code: int) -> int:
        return mapCheckObject_t (_hselect, _code)


# Запросить признак доступности объектов c заданным внутренним кодом в классификаторе с учетом локализации и слоя
# hselect - контекст условий отбора объектов
# code - внутренний код (порядковый номер объекта в классификаторе), от 1 до mapGetRscObjectCount(...)
# Если code = -1, то проверяется доступ ко всем объектам
# Если при code = -1 возвращает 0 - один или более объектов недоступны, иначе - доступны все объекты
# Возвращает признак доступности объекта: 1 - включен, 0 - отключен

    mapCheckObjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckObjectEx', maptype.HSELECT, ctypes.c_long)
    def mapCheckObjectEx(_hselect: maptype.HSELECT, _code: int) -> int:
        return mapCheckObjectEx_t (_hselect, _code)


# Установить признак доступности объектов c заданной локализацией
# hselect - контекст условий отбора объектов
# local - код локализации объекта (LOCAL_LINE, LOCAL_SQUARE ...)
# check - признак доступности локализации: 1 - включен, 0 - отключен
# Если local = -1, то устанавливается доступ ко всем локализациям

    mapSelectLocal_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectLocal', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectLocal(_hselect: maptype.HSELECT, _local: int, _check: int) -> ctypes.c_void_p:
        return mapSelectLocal_t (_hselect, _local, _check)


# Запросить признак доступности объектов с заданной локализацией
# hselect - контекст условий отбора объектов
# local - код локализации объекта (LOCAL_LINE, LOCAL_SQUARE ...)
# Если local = -1, то проверяется доступ ко всем локализациям
# Если при local = -1 возвращает 0 - одна или более локализаций недоступны, иначе - доступны все локализации
# Возвращает признак доступности локализации: 1 - включен, 0 - отключен

    mapCheckLocal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckLocal', maptype.HSELECT, ctypes.c_long)
    def mapCheckLocal(_hselect: maptype.HSELECT, _local: int) -> int:
        return mapCheckLocal_t (_hselect, _local)


# Включить доступ к объектам заданного диапазона уникальных номеров
# hselect - контекст условий отбора объектов
# minkey - минимальное значение диапазона номеров, начинается с 0
# maxkey - максимальное значение диапазона номеров, начинается с minkey
# Если minkey и maxkey = -1, то устанавливается доступ ко всем объектам по номерам
# Применяется для отбора объектов конкретного листа карты

    mapSelectKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectKey', maptype.HSELECT, ctypes.c_ulong, ctypes.c_ulong)
    def mapSelectKey(_hselect: maptype.HSELECT, _minkey: int, _maxkey: int) -> ctypes.c_void_p:
        return mapSelectKey_t (_hselect, _minkey, _maxkey)


# Запросить доступность объекта карты с заданным уникальным номером
# hselect - контекст условий отбора объектов
# key - уникальный номер объекта в листе карты
# Если key = -1, то проверяется доступ ко всем объектам по номерам
# Если при key = -1 возвращает 0 - один или более объектов недоступны, иначе - доступны все объекты
# Возвращает признак доступности объектов по номерам: 1 - включен, 0 - отключен

    mapCheckKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckKey', maptype.HSELECT, ctypes.c_ulong)
    def mapCheckKey(_hselect: maptype.HSELECT, _key: int) -> int:
        return mapCheckKey_t (_hselect, _key)


# Запросить минимальный уникальный номер диапазона доступных объектов
# hselect - контекст условий отбора объектов
# Может равняться 0, когда доступны все номера объектов

    mapGetMinKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_ulong,'mapGetMinKey', maptype.HSELECT)
    def mapGetMinKey(_hselect: maptype.HSELECT) -> int:
        return mapGetMinKey_t (_hselect)


# Запросить максимальный уникальный номер диапазона доступных объектов
# hselect - контекст условий отбора объектов

    mapGetMaxKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_ulong,'mapGetMaxKey', maptype.HSELECT)
    def mapGetMaxKey(_hselect: maptype.HSELECT) -> int:
        return mapGetMaxKey_t (_hselect)


# Установить доступ к объектам с заданным GUID
# hselect - контекст условий отбора объектов
# guid - строка, содержащая GUID в виде строки шестнадцатеричных цифр длиной 36 символов (с черточками) или 32 символа (без черточек)

    mapSelectGuid_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectGuid', maptype.HSELECT, ctypes.c_char_p)
    def mapSelectGuid(_hselect: maptype.HSELECT, _guid: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapSelectGuid_t (_hselect, _guid)


# Запросить условие доступа к объектам с заданным GUID
# hselect - контекст условий отбора объектов
# guid - адрес строки длиной не менее 37 байт, в которую запишется guid (с черточками)
# Если условие поиска не установлено, возвращает ноль и в поле guid записывается ноль

    mapGetSelectGuid_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectGuid', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapGetSelectGuid(_hselect: maptype.HSELECT, _guid: ctypes.c_char_p, _size: int) -> int:
        return mapGetSelectGuid_t (_hselect, _guid, _size)


# Установить/Отменить условие отбора объектов по тексту подписи
# hselect - контекст условий отбора объектов
# value - значение строки для поиска (может включать служебные символы '#' и '?')
# isspecial - признак обработки специальных символов при поиске ('#' и '?'): 1 - включен, 0 - отключен
# Символ % или # в начале строки означает поиск подстроки, которая следует за управляющим символом
# Символ % означает поиск подстроки строго в конце или в начале строки (если в конце стоит два символа %%)
# Символ # означает поиск подстроки в любом месте строки
# Символ ? означает возможность подстановки любого символа, может применяться вместе с символом #
# Например: шаблон поиска "#ушк#" или "#ушк" или "%ушк%%" найдет значение "Пушкино",
# шаблон "%ушк" будет искать строки строго оканчивающиеся заданным шаблоном ("ушк");
# шаблон "#39%" или "%39%" найдет строку "139%"; шаблон "се??й" найдет строки - "серый", "седой"
# Если value равно нулю, то условие отбора по тексту подписи отменяется
# При ошибке возвращает ноль, иначе - номер условия

    mapSelectTitlePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectTitlePro', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapSelectTitlePro(_hselect: maptype.HSELECT, _value: mapsyst.WTEXT, _isspecial: int) -> int:
        return mapSelectTitlePro_t (_hselect, _value.buffer(), _isspecial)


# Добавить условие отбора объектов по семантике в список (узла)
# hselect - контекст условий отбора объектов
# condition - код условия для проверки значения семантики (CMLESS, CMEQUAL, CMMORE ...)
# semcode - код семантики, от 1 до mapGetRscSemanticCount(...)
# value - значение для условия (если code = CMANY, value игнорируется)
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль, иначе - номер условия

    mapSelectSemanticAppendExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticAppendExUn', maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSemanticAppendExUn(_hselect: maptype.HSELECT, _condition: int, _semcode: int, _value: mapsyst.WTEXT, _node: int) -> int:
        return mapSelectSemanticAppendExUn_t (_hselect, _condition, _semcode, _value.buffer(), _node)


# Добавить список строк из текстового файла в условия отбора объектов по семантике
# hselect - контекст условий отбора объектов
# condition - код условия для проверки значения семантики (CMLESS, CMEQUAL, CMMORE ...)
# semcode - код семантики, от 1 до mapGetRscSemanticCount(...)
# buffer - буфер для размещения списка строк, разделенных символом '\n' (при обработке строк символ '\n' будет заменен на ноль)
# size - размер буфера в байтах
# istitle - признак отбора подписей по тексту: 1 - включен, 0 - отключен
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectAppendStringArrayUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectAppendStringArrayUn', maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectAppendStringArrayUn(_hselect: maptype.HSELECT, _condition: int, _semcode: int, _buffer: mapsyst.WTEXT, _size: int, _istitle: int, _node: int) -> int:
        return mapSelectAppendStringArrayUn_t (_hselect, _condition, _semcode, _buffer.buffer(), _size, _istitle, _node)


# Заполнить буфер списка строк в кодировке UTF8, установленных в контекст условий отбора объектов по семантике
# hselect - контекст условий отбора объектов
# condition - поле для записи кода условия для проверки значения семантики (CMLESS, CMEQUAL, CMMORE ...)
# semcode - поле для записи кода семантики
# istitle - поле для записи признака отбора подписей по тексту
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapGetSelectStringArrayHandle_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapGetSelectStringArrayHandle', maptype.HSELECT, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapGetSelectStringArrayHandle(_hselect: maptype.HSELECT, _condition: ctypes.POINTER(ctypes.c_long), _semcode: ctypes.POINTER(ctypes.c_long), _istitle: ctypes.POINTER(ctypes.c_long), _node: int) -> ctypes.c_void_p:
        return mapGetSelectStringArrayHandle_t (_hselect, _condition, _semcode, _istitle, _node)


# Получить указатель на список строк в кодировке UTF8 по идентификатору буфера
# record - идентификатор буфера списка строк
# size - поле для записи длины записи в байтах
# Возвращает указатель на список строк в кодировке UTF8, разделенных символом '\n'
# При ошибке возвращает ноль

    mapGetSelectStringArrayPoint_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetSelectStringArrayPoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetSelectStringArrayPoint(_record: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetSelectStringArrayPoint_t (_record, _size)


# Освободить ресурсы, выделенные в mapGetSelectStringArrayHandle
# record - идентификатор записи в памяти

    mapFreeSelectStringArrayHandle_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeSelectStringArrayHandle', ctypes.c_void_p)
    def mapFreeSelectStringArrayHandle(_record: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSelectStringArrayHandle_t (_record)


# Удалить все условия отбора объектов по семантике
# hselect - контекст условий отбора объектов

    mapSelectSemanticClear_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectSemanticClear', maptype.HSELECT)
    def mapSelectSemanticClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectSemanticClear_t (_hselect)


# Запросить количество узлов в дереве с условиями отбора объектов по семантике
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapSelectSemanticNodeCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticNodeCount', maptype.HSELECT)
    def mapSelectSemanticNodeCount(_hselect: maptype.HSELECT) -> int:
        return mapSelectSemanticNodeCount_t (_hselect)


# Запросить количество установленных условий отбора объектов по семантике в списке (узла)
# hselect - контекст условий отбора объектов
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectSemanticCountEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticCountEx', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticCountEx(_hselect: maptype.HSELECT, _node: int) -> int:
        return mapSelectSemanticCountEx_t (_hselect, _node)


# Запросить код условия отбора объектов для семантики по порядковому номеру в списке (узла)
# hselect - контекст условий отбора объектов
# number - порядковый номер семантики
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectSemanticConditionEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticConditionEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticConditionEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticConditionEx_t (_hselect, _number, _node)


# Запросить код семантики по порядковому номеру в списке (узла) условий отбора объектов
# hselect - контекст условий отбора объектов
# number - порядковый номер семантики
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# Примеры кодов семантики: 4 - абсолютная высота, 9 - название, ...
# При ошибке возвращает ноль

    mapSelectSemanticCodeEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticCodeEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticCodeEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticCodeEx_t (_hselect, _number, _node)


# Удалить список условий отбора объектов по семантике (узла)
# hselect - контекст условий отбора объектов
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectSemanticDeleteNode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticDeleteNode', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticDeleteNode(_hselect: maptype.HSELECT, _node: int) -> int:
        return mapSelectSemanticDeleteNode_t (_hselect, _node)


# Удалить условие отбора объектов из списка (узла)
# hselect - контекст условий отбора объектов
# number - номер условия в списке, от 1 до mapSelectSemanticCountEx(...)
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectSemanticDeleteEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticDeleteEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticDeleteEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticDeleteEx_t (_hselect, _number, _node)


# Установить обобщающее условие отбора объектов для списка семантик (узла)
# hselect - контекст условий отбора объектов
# condition - код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике

    mapSelectSemanticLinkEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticLinkEx(_hselect: maptype.HSELECT, _condition: int, _node: int) -> ctypes.c_void_p:
        return mapSelectSemanticLinkEx_t (_hselect, _condition, _node)


# Запросить обобщающее условие отбора объектов для списка семантик (узла)
# hselect - контекст условий отбора объектов
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# Возвращает код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapGetSelectSemanticLinkEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectSemanticLinkEx(_hselect: maptype.HSELECT, _node: int) -> int:
        return mapGetSelectSemanticLinkEx_t (_hselect, _node)


# Установить обобщающее условие отбора объектов для списка узлов
# hselect - контекст условий отбора объектов
# condition - код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)

    mapSelectSemanticListLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectSemanticListLink', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticListLink(_hselect: maptype.HSELECT, _condition: int) -> ctypes.c_void_p:
        return mapSelectSemanticListLink_t (_hselect, _condition)


# Запросить обобщающее условие отбора объектов для списка узлов
# hselect - контекст условий отбора объектов
# Возвращает код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapGetSelectSemanticListLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectSemanticListLink', maptype.HSELECT)
    def mapGetSelectSemanticListLink(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectSemanticListLink_t (_hselect)


# Запросить значение семантики по порядковому номеру в списке (узла) условий отбора объектов
# hselect - контекст условий отбора объектов
# number - порядковый номер семантики
# place - адрес строки для размещения результата
# size - размер строки для размещения результата в байтах
# node - номер списка условий узла (c 1) в дереве условий отбора по семантике
# При ошибке возвращает ноль

    mapSelectSemanticValueExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSemanticValueExUn', maptype.HSELECT, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticValueExUn(_hselect: maptype.HSELECT, _number: int, _place: mapsyst.WTEXT, _size: int, _node: int) -> int:
        return mapSelectSemanticValueExUn_t (_hselect, _number, _place.buffer(), _size, _node)


# Запросить количество установленных условий отбора объектов по измерениям
# hselect - контекст условий отбора объектов
# Для установки условий по измерениям используются: длина, периметр, площадь, высота

    mapSelectMeasureCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectMeasureCount', maptype.HSELECT)
    def mapSelectMeasureCount(_hselect: maptype.HSELECT) -> int:
        return mapSelectMeasureCount_t (_hselect)


# Удалить все условия отбора объектов по измерениям объектов
# hselect - контекст условий отбора объектов

    mapSelectMeasureClear_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectMeasureClear', maptype.HSELECT)
    def mapSelectMeasureClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectMeasureClear_t (_hselect)


# Добавить условия отбора объектов по измерениям в список
# hselect - контекст условий отбора объектов
# measurecode - код измерения объекта: MEASURE_LENGTH, MEASURE_PERIMETER, MEASURE_SQUARE, MEASURE_HEIGHT
# condition1 - код первого условия для проверки значения (CMLESS, CMEQUAL, CMMORE ...)
# value1 - значение измерения в метрах, для площади - в кв.метрах (для проверки первого условия)
# condition2 - код второго условия для проверки значения (CMLESS, CMEQUAL, CMMORE ...)
# value2 - значение измерения в метрах, для площади - в кв.метрах (для проверки второго условия)
# Для задания диапазона значений condition1 должно равняться CMMOREEQ (>=) или CMMORE (>),
# condition2 должно равняться CMLESSEQ (<=) или CMLESS (<)
# Если condition2 = 0, то значение value2 игнорируется
# При ошибке возвращает ноль, иначе - номер условия в списке

    mapSelectMeasureAppend_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectMeasureAppend', maptype.HSELECT, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_double)
    def mapSelectMeasureAppend(_hselect: maptype.HSELECT, _measurecode: int, _condition1: int, _value1: float, _condition2: int, _value2: float) -> int:
        return mapSelectMeasureAppend_t (_hselect, _measurecode, _condition1, _value1, _condition2, _value2)


# Запросить количество условий проверки значения измерения по порядковому номеру в списке
# hselect - контекст условий отбора объектов
# number - номер измерения
# Возвращает: 1 или 2 условия (для диапазона), 0 - при ошибке

    mapIsSelectMeasureRange_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSelectMeasureRange', maptype.HSELECT, ctypes.c_long)
    def mapIsSelectMeasureRange(_hselect: maptype.HSELECT, _number: int) -> int:
        return mapIsSelectMeasureRange_t (_hselect, _number)


# Установить обобщающее условие для списка условий отбора объектов по измерениям
# hselect - контекст условий отбора объектов
# condition - код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)

    mapSelectMeasureLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectMeasureLink', maptype.HSELECT, ctypes.c_long)
    def mapSelectMeasureLink(_hselect: maptype.HSELECT, _condition: int) -> ctypes.c_void_p:
        return mapSelectMeasureLink_t (_hselect, _condition)


# Запросить обобщающее условие для списка условий отбора объектов по измерениям
# hselect - контекст условий отбора объектов
# Возвращает код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapGetSelectMeasureLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectMeasureLink', maptype.HSELECT)
    def mapGetSelectMeasureLink(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectMeasureLink_t (_hselect)


# Запросить код измерения по порядковому номеру в списке условий отбора объектов
# hselect - контекст условий отбора объектов
# number - номер измерения
# Возвращает код измерения объекта: MEASURE_LENGTH, MEASURE_PERIMETER, MEASURE_SQUARE, MEASURE_HEIGHT
# При ошибке возвращает ноль

    mapSelectMeasureCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectMeasureCode', maptype.HSELECT, ctypes.c_long)
    def mapSelectMeasureCode(_hselect: maptype.HSELECT, _number: int) -> int:
        return mapSelectMeasureCode_t (_hselect, _number)


# Запросить значение измерения по порядковому номеру в списке условий отбора объектов
# hselect - контекст условий отбора объектов
# number - номер измерения
# value1 - поле для размещения значения измерения 1
# value2 - поле для размещения значения измерения 2
# Возвращает: 1 или 2 условия (для диапазона), 0 - при ошибке

    mapSelectMeasureValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectMeasureValue', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapSelectMeasureValue(_hselect: maptype.HSELECT, _number: int, _value1: ctypes.POINTER(ctypes.c_double), _value2: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSelectMeasureValue_t (_hselect, _number, _value1, _value2)


# Запросить код условия проверки измерения по порядковому номеру в списке условий отбора объектов
# hselect - контекст условий отбора объектов
# number - номер измерения
# condition1 - поле для размещения кода условия 1
# condition2 - поле для размещения кода условия 2
# Возвращает: 1 или 2 условия (для диапазона), 0 - при ошибке

    mapSelectMeasureCondition_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectMeasureCondition', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapSelectMeasureCondition(_hselect: maptype.HSELECT, _number: int, _condition1: ctypes.POINTER(ctypes.c_long), _condition2: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapSelectMeasureCondition_t (_hselect, _number, _condition1, _condition2)


# Удалить все условия отбора объектов по формулам
# hselect - контекст условий отбора объектов

    mapSelectFormulaClear_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSelectFormulaClear', maptype.HSELECT)
    def mapSelectFormulaClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectFormulaClear_t (_hselect)


# Запросить количество групп формул условий отбора объектов
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapGetSelectGroupFormulaCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectGroupFormulaCount', maptype.HSELECT)
    def mapGetSelectGroupFormulaCount(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectGroupFormulaCount_t (_hselect)


# Запросить количество формул в списке группы условий отбора объектов
# hselect - контекст условий отбора объектов
# group - номер группы формул
# При ошибке возвращает ноль

    mapGetSelectFormulaCountEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectFormulaCountEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectFormulaCountEx(_hselect: maptype.HSELECT, _group: int) -> int:
        return mapGetSelectFormulaCountEx_t (_hselect, _group)


# Запросить описание формулы по номеру в списке группы условий отбора объектов
# hselect - контекст условий отбора объектов
# number - номер формулы в списке с 1
# minvalue - поле для записи нижней границы допустимого диапазона для значения формулы
# maxvalue - поле для записи верхней границы допустимого диапазона для значения формулы
# group - номер группы формул
# Возвращает адрес строки с математическим выражением над семантиками и свойствами объекта
# При ошибке возвращает ноль

    mapGetSelectFormulaEx_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetSelectFormulaEx', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapGetSelectFormulaEx(_hselect: maptype.HSELECT, _number: int, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double), _group: int) -> ctypes.POINTER(ctypes.c_char):
        return mapGetSelectFormulaEx_t (_hselect, _number, _minvalue, _maxvalue, _group)


# Добавить описание формулы в список группы условий отбора объектов
# hselect - контекст условий отбора объектов
# formula - строка с математическим выражением над семантиками и свойствами объекта
# minvalue - нижняя граница допустимого диапазона для значения формулы
# maxvalue - верхняя граница допустимого диапазона для значения формулы
# group - номер группы формул
# При ошибке возвращает ноль

    mapAppendSelectFormulaEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSelectFormulaEx', maptype.HSELECT, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendSelectFormulaEx(_hselect: maptype.HSELECT, _formula: ctypes.c_char_p, _minvalue: float, _maxvalue: float, _group: int) -> int:
        return mapAppendSelectFormulaEx_t (_hselect, _formula, _minvalue, _maxvalue, _group)


# Удалить формулу из списка формул группы условий отбора объектов
# hselect - контекст условий отбора объектов
# number - номер формулы в списке с 1
# group - номер группы формул

    mapDeleteSelectFormulaEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapDeleteSelectFormulaEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapDeleteSelectFormulaEx(_hselect: maptype.HSELECT, _number: int, _group: int) -> ctypes.c_void_p:
        return mapDeleteSelectFormulaEx_t (_hselect, _number, _group)


# Установить обобщающее условие для списка группы условий отбора объектов по формулам
# hselect - контекст условий отбора объектов
# condition - код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# group - номер группы формул
# При ошибке возвращает ноль

    mapSetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSetSelectFormulaLinkEx(_hselect: maptype.HSELECT, _condition: int, _group: int) -> int:
        return mapSetSelectFormulaLinkEx_t (_hselect, _condition, _group)


# Запросить обобщающее условие для списка группы условий отбора объектов по формулам
# hselect - контекст условий отбора объектов
# group - номер группы формул
# Возвращает код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapGetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectFormulaLinkEx(_hselect: maptype.HSELECT, _group: int) -> int:
        return mapGetSelectFormulaLinkEx_t (_hselect, _group)


# Установить обобщающее условие для групп условий отбора объектов по формулам
# hselect - контекст условий отбора объектов
# condition - код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapSetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSelectFormulaGroupLink', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectFormulaGroupLink(_hselect: maptype.HSELECT, _condition: int) -> int:
        return mapSetSelectFormulaGroupLink_t (_hselect, _condition)


# Запросить обобщающее условие для групп условий отбора объектов по формулам
# hselect - контекст условий отбора объектов
# Возвращает код условия: 16 - CMOR (выполняется хотя бы одно), 32 - CMAND (выполняются все)
# При ошибке возвращает ноль

    mapGetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectFormulaGroupLink', maptype.HSELECT)
    def mapGetSelectFormulaGroupLink(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectFormulaGroupLink_t (_hselect)


# Установить значение знаменателя условного масштаба отображения для которого проверяются границы видимости объектов
# hselect - контекст условий отбора объектов
# scale - знаменатель масштаба отображения для проверки видимости объекта при поиске с флажком WO_VISUALSCALE
# Если значение масштаба отображения не установлено, то при данном поиске проверяется текущий масштаб отображения документа
# При ошибке возвращает ноль

    mapSetSelectShowScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSelectShowScale', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectShowScale(_hselect: maptype.HSELECT, _scale: int) -> int:
        return mapSetSelectShowScale_t (_hselect, _scale)


# Запросить размер записи, необходимый для сохранения условий поиска
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapGetSelectRecordSize_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectRecordSize', maptype.HSELECT)
    def mapGetSelectRecordSize(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectRecordSize_t (_hselect)


# Сформировать запись для сохранения условий поиска
# hselect - контекст условий отбора объектов
# buffer - буфер для размещения условий поиска
# size - размер буфера в байтах
# При ошибке возвращает ноль, иначе - длину выходной строки в байтах

    mapGetSelectRecord_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectRecord', maptype.HSELECT, ctypes.c_char_p, ctypes.c_long)
    def mapGetSelectRecord(_hselect: maptype.HSELECT, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetSelectRecord_t (_hselect, _buffer, _size)


# Сформировать запись для сохранения условий поиска в формате XML
# hselect - контекст условий отбора объектов
# name - имя модели условий поиска или ноль
# realset - признак записи реально выбранных объектов и слоев (1);
#     eсли realset = 0, то формируется минимальная по размеру запись,
#     которая содержит списки выбранных или отключенных объектов, слоев,
#     локализаций с указанием признаков отбора (выбраны или отключены)
# isexcode - признак записи внешних кодов объектов (1);
#     если isexcode = 0, то записываются ключи объектов
# issample - признак записи списка уникальных номеров объектов в листе карты (1)
#     если issample = 0, записываются списки видов объектов (ключи или коды), слоев, локализаций
# Возвращает идентификатор записи формата XML в памяти
# Для получения указателя на запись применяется функция mapGetSelectRecordXMLPoint
# Для удаления записи в памяти применяется функция mapFreeSelectRecordXML
# При ошибке возвращает ноль

    mapGetSelectRecordHandle_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapGetSelectRecordHandle', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetSelectRecordHandle(_hselect: maptype.HSELECT, _name: mapsyst.WTEXT, _realset: int, _isexcode: int = 0, _issample: int = 0) -> ctypes.c_void_p:
        return mapGetSelectRecordHandle_t (_hselect, _name.buffer(), _realset, _isexcode, _issample)


# Получить указатель на запись XML для сохранения условий поиска в формате XML
# hselect - контекст условий отбора объектов
# record - идентификатор записи формата XML в памяти
# size - поле для получения длины записи в байтах
# name - имя модели (условий поиска) или ноль
# Возвращает указатель на запись XML в кодировке UTF8
# Для удаления записи в памяти применяются функция mapFreeSelectRecordXML
# При ошибке возвращает ноль

    mapGetSelectRecordXMLPoint_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetSelectRecordXMLPoint', maptype.HSELECT, ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetSelectRecordXMLPoint(_hselect: maptype.HSELECT, _record: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetSelectRecordXMLPoint_t (_hselect, _record, _size)


# Освободить ресурсы, выделенные в mapGetSelectRecordXML или mapGetSelectRecordHandle
# hselect - контекст условий отбора объектов
# record - идентификатор записи формата XML в памяти

    mapFreeSelectRecordXML_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeSelectRecordXML', maptype.HSELECT, ctypes.c_void_p)
    def mapFreeSelectRecordXML(_hselect: maptype.HSELECT, _record: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSelectRecordXML_t (_hselect, _record)


# Заполнить условия поиска из записи XML
# hselect - контекст условий отбора объектов
# buffer - адрес записи
# size - размер записи в памяти, содержащего запись (не меньше записи)
# При ошибке возвращает ноль

    mapPutSelectRecordXML_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutSelectRecordXML', maptype.HSELECT, ctypes.c_char_p, ctypes.c_long)
    def mapPutSelectRecordXML(_hselect: maptype.HSELECT, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapPutSelectRecordXML_t (_hselect, _buffer, _size)


# Проверить наличие списка объектов в контексте условий отбора объектов
# hselect - контекст условий отбора объектов
# Список объектов содержит номер листа и номер объекта в листе
# Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapIsSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSample', maptype.HSELECT)
    def mapIsSample(_hselect: maptype.HSELECT) -> int:
        return mapIsSample_t (_hselect)


# Запросить число объектов в списке для указанного листа карты
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# Если список объектов не установлен - возвращает ноль

    mapGetSampleCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSampleCount', maptype.HSELECT, ctypes.c_long)
    def mapGetSampleCount(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        return mapGetSampleCount_t (_hselect, _sheetnumber)


# Запросить уникальный номер объекта из списка для указанного листа по номеру в списке
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# number - порядковый номер объекта в списке выбранных объектов листа
# Если список объектов не установлен, то возвращает ноль

    mapGetSampleByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapGetSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _number: int) -> int:
        return mapGetSampleByNumber_t (_hselect, _sheetnumber, _number)


# Очистить список объектов в контексте условий отбора объектов
# hselect - контекст условий отбора объектов
# Применяется для отбора объектов, атрибуты которых расположены во внешних базах данных

    mapClearSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearSample', maptype.HSELECT)
    def mapClearSample(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapClearSample_t (_hselect)


# Установить признак совместной обработки номеров объектов с условиями по локализации, слоям, семантике и измерениям
# hselect - контекст условий отбора объектов
# complex - признак совместной обработки:  1 - включен, 0 - отключен
# Возвращает предыдущее значение

    mapSetSampleComplex_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSampleComplex', maptype.HSELECT, ctypes.c_long)
    def mapSetSampleComplex(_hselect: maptype.HSELECT, _complex: int) -> int:
        return mapSetSampleComplex_t (_hselect, _complex)


# Инвертировать список отобранных объектов в контексте условий отбора объектов
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapInvertSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInvertSample', maptype.HSELECT)
    def mapInvertSample(_hselect: maptype.HSELECT) -> int:
        return mapInvertSample_t (_hselect)


# Заполнить список объектов всеми номерами объектов, которые есть на листе
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext)
# или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
# Возвращает число объектов, занесенных в список для листа
# При ошибке возвращает ноль

    mapSetSampleAllObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSampleAllObjects', maptype.HSELECT, ctypes.c_long)
    def mapSetSampleAllObjects(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        return mapSetSampleAllObjects_t (_hselect, _sheetnumber)


# Заполнить список объектов всеми номерами объектов, которые имеют заданный внутренний код
# hselect - контекст условий отбора объектов
# code - внутренний код объекта (mapObjectCode)
# Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext)
# или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
# При ошибке возвращает ноль

    mapSelectSampleByObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSampleByObject', maptype.HSELECT, ctypes.c_long)
    def mapSelectSampleByObject(_hselect: maptype.HSELECT, _code: int) -> int:
        return mapSelectSampleByObject_t (_hselect, _code)


# Удалить из списка объектов все номера объектов, которые имеют заданный внутренний код
# hselect - контекст условий отбора объектов
# code - внутренний код объекта (mapObjectCode)
# Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext)
# или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
# При ошибке возвращает ноль

    mapUnselectSampleByObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUnselectSampleByObject', maptype.HSELECT, ctypes.c_long)
    def mapUnselectSampleByObject(_hselect: maptype.HSELECT, _code: int) -> int:
        return mapUnselectSampleByObject_t (_hselect, _code)


# Заполнить список отобранных объектов по объектам, отобранным по локализации, слоям, семантике и измерениям
# hselect - контекст условий отбора объектов
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapSelectSampleBySelectObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSampleBySelectObjects', maptype.HSELECT)
    def mapSelectSampleBySelectObjects(_hselect: maptype.HSELECT) -> int:
        return mapSelectSampleBySelectObjects_t (_hselect)


# Установить условия отображения объекта по названию листа карты и уникальному номеру объекта
# hmap - идентификатор открытых данных (документа)
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# При ошибке возвращает ноль

    mapSelectViewSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectViewSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSelectViewSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectViewSampleUn_t (_hmap, _sheetname.buffer(), _key)


# Проверить наличие списка объектов в контексте условий отображения для карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapCheckViewSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckViewSample', maptype.HMAP, maptype.HSITE)
    def mapCheckViewSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapCheckViewSample_t (_hmap, _hsite)


# Проверить наличие списка объектов в контексте условий поиска для карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение

    mapCheckSeekSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckSeekSample', maptype.HMAP, maptype.HSITE)
    def mapCheckSeekSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapCheckSeekSample_t (_hmap, _hsite)


# Установить условия поиска объекта по названию листа карты и уникальному номеру объекта
# hmap - идентификатор открытых данных (документа)
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# При ошибке возвращает ноль

    mapSelectSeekSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSeekSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectSeekSampleUn_t (_hmap, _sheetname.buffer(), _key)


# Установить доступ к объекту по названию листа карты и уникальному номеру объекта
# hselect - контекст условий отбора объектов
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapSelectSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectSampleUn_t (_hselect, _sheetname.buffer(), _key)


# Установить доступ к объекту по названию листа карты и уникальному номеру объекта
# hselect - контекст условий отбора объектов
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# Выполняется без проверки повторных значений номеров объектов для ускорения формирования списков
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapFastSelectSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFastSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapFastSelectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapFastSelectSampleUn_t (_hselect, _sheetname.buffer(), _key)


# Установить доступ к объекту по номеру листа карты и уникальному номеру объекта
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# key - уникальный номер объекта в листе карты
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapSelectSampleByKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSampleByKey', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSampleByKey(_hselect: maptype.HSELECT, _sheetnumber: int, _key: int) -> int:
        return mapSelectSampleByKey_t (_hselect, _sheetnumber, _key)


# Установить доступ к объекту по номеру листа карты и порядковому номеру объекта
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# objectnumber - номер объекта в листе
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapSelectSampleByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _objectnumber: int) -> int:
        return mapSelectSampleByNumber_t (_hselect, _sheetnumber, _objectnumber)


# Исключить из списка объект по названию листа карты и уникальному номеру объекта
# hselect - контекст условий отбора объектов
# sheetname - название листа карты
# key - уникальный номер объекта в листе карты
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapUnselectSampleUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUnselectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapUnselectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        return mapUnselectSampleUn_t (_hselect, _sheetname.buffer(), _key)


# Исключить из списка объект по номеру листа карты и уникальному номеру объекта
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# key - уникальный номер объекта в листе карты
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapUnselectSampleByKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUnselectSampleByKey', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapUnselectSampleByKey(_select: maptype.HSELECT, _sheetnumber: int, _key: int) -> int:
        return mapUnselectSampleByKey_t (_select, _sheetnumber, _key)


# Исключить из списка объект по номеру листа карты и порядковому номеру объекта
# hselect - контекст условий отбора объектов
# sheetnumber - номер листа карты (с 1)
# objectnumber - номер объекта в листе
# В контексте условий отбора объектов должна быть установлена карта
# При ошибке возвращает ноль

    mapUnselectSampleByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUnselectSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapUnselectSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _objectnumber: int) -> int:
        return mapUnselectSampleByNumber_t (_hselect, _sheetnumber, _objectnumber)


# Установить параметры поиска объектов по области для карты с заданным номером
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, содержащий область поиска
# distance - расстояние поиска в метрах
# filter - признак учета фильтра объектов (условий отбора): 1 - включен, 0 - отключен
# inside - условия поиска объектов по области: 0 - по расстоянию, 1 - внутри области,
#      2 - целиком внутри области, 4 - целиком снаружи области
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# fastlist - признак создания быстрого списка отобранных объектов: 1 - включен, 0 - отключен
# mapnumber - номер карты поиска. Если mapnumber = -1, поиск по всем картам
# subjectflag - признак учета подобъектов области поиска: 1 - включен, 0 - отключен
# samplelistflag - при наличии списка объектов в контексте условий отбора выполнить операцию
#      над объектами из этого списка (SLF_AND, SLF_OR, ...)
# Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается WM_PROGRESSBAR)
# Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
# При ошибке возвращает ноль

    mapSelectDocArea_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectDocArea', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectDocArea(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _fastlist: int, _mapnumber: int, _subjectflag: int, _samplelistflag: int) -> int:
        return mapSelectDocArea_t (_hmap, _hobj, _distance, _filter, _inside, _visible, _fastlist, _mapnumber, _subjectflag, _samplelistflag)


# Установить параметры поиска объектов по области для карты с заданным именем
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, содержащий область поиска
# distance - расстояние поиска в метрах
# filter - признак учета фильтра объектов (условий отбора): 1 - включен, 0 - отключен
# inside - условия поиска объектов по области: 0 - по расстоянию, 1 - внутри области,
#      2 - целиком внутри области, 4 - целиком снаружи области
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# sheetname - название листа карты
# fastlist - признак создания быстрого списка отобранных объектов: 1 - включен, 0 - отключен
# Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается WM_PROGRESSBAR)
# Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
# При ошибке возвращает ноль

    mapSelectAreaUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectAreaUn', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSelectAreaUn(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _sheetname: mapsyst.WTEXT = None, _fastlist: int = 0) -> int:
        return mapSelectAreaUn_t (_hmap, _hobj, _distance, _filter, _inside, _visible, _sheetname.buffer(), _fastlist)


# Сбросить параметры поиска объектов по области
# hmap - идентификатор открытых данных (документа)

    mapUnselectArea_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUnselectArea', maptype.HMAP)
    def mapUnselectArea(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapUnselectArea_t (_hmap)


# Установить в контексте условий отбора параметры поиска объектов по области
# hselect - контекст условий отбора объектов
# hobj - идентификатор объекта карты в памяти, содержащий область поиска
# distance - расстояние поиска в метрах
# filter - признак учета фильтра объектов (условий отбора): 1 - включен, 0 - отключен
# inside - условия поиска объектов по области: 0 - по расстоянию, 1 - внутри области,
#      2 - целиком внутри области, 4 - целиком снаружи области
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# fastlist - признак создания быстрого списка отобранных объектов: 1 - включен, 0 - отключен
# subjectflag - признак учета подобъектов области поиска: 1 - включен, 0 - отключен
# samplelistflag - при наличии списка объектов в контексте условий отбора выполнить операцию
#      над объектами из этого списка (SLF_AND, SLF_OR, ...)
# Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается WM_PROGRESSBAR)
# Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
# При ошибке возвращает ноль

    mapSelectSeekAreaEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSeekAreaEx', maptype.HSELECT, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectSeekAreaEx(_hselect: maptype.HSELECT, _hobj: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _fastlist: int = 0, _subjectflag: int = 0, _samplelistflag: int = 0) -> int:
        return mapSelectSeekAreaEx_t (_hselect, _hobj, _distance, _filter, _inside, _visible, _fastlist, _subjectflag, _samplelistflag)


# Установить в контексте условий отбора параметры поиска объектов по прямоугольной области
# hselect - контекст условий отбора объектов
# dframe - габариты области поиска в метрах
# distance - расстояние поиска в метрах (симметрично расширяет область dframe)
# filter - признак учета фильтра объектов (условий отбора): 1 - включен, 0 - отключен
# inside - условия поиска объектов по области: 0 - по расстоянию, 1 - внутри области, 2 - целиком внутри области
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# fastlist - признак создания быстрого списка отобранных объектов: 1 - включен, 0 - отключен
# Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается WM_PROGRESSBAR)
# Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
# При ошибке возвращает ноль

    mapSelectSeekAreaFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSelectSeekAreaFrame', maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectSeekAreaFrame(_hselect: maptype.HSELECT, _dframe: ctypes.POINTER(maptype.DFRAME), _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _fastlist: int = 0) -> int:
        return mapSelectSeekAreaFrame_t (_hselect, _dframe, _distance, _filter, _inside, _visible, _fastlist)


# Сбросить в контексте условий отбора параметры поиска объектов по области
# hselect - контекст условий отбора объектов

    mapUnselectSeekArea_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUnselectSeekArea', maptype.HSELECT)
    def mapUnselectSeekArea(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapUnselectSeekArea_t (_hselect)


# Проверить в контексте условий отбора наличие установленных параметров поиска по области
# hselect - контекст условий отбора объектов
# Если в контексте условий установлены параметры поиска по области - возвращает ненулевое значение

    mapGetAreaSelectFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetAreaSelectFlag', maptype.HSELECT)
    def mapGetAreaSelectFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetAreaSelectFlag_t (_hselect)


# Запросить в контексте условий отбора признак отбора графических объектов
# hselect - контекст условий отбора объектов
# Возвращает:
#        MSL_DRAW_ON (0)   - отбор по "общему" фильтру,
#        MSL_DRAW_ONLY (1) - отобрать только графические объекты,
#        MSL_DRAW_OFF (2)  - не отбирать графические объекты

    mapGetDrawObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDrawObjectsFlag', maptype.HSELECT)
    def mapGetDrawObjectsFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetDrawObjectsFlag_t (_hselect)


# Установить в контексте условий отбора признак отбора графических объектов
# hselect - контекст условий отбора объектов
# flag - условия отбора графических объектов:
#        MSL_DRAW_ON (0)   - отбор по "общему" фильтру,
#        MSL_DRAW_ONLY (1) - отобрать только графические объекты,
#        MSL_DRAW_OFF (2)  - не отбирать графические объекты

    mapSetDrawObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetDrawObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetDrawObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetDrawObjectsFlag_t (_hselect, _flag)


# Запросить в контексте условий отбора признак отбора метаобъектов
# hselect - контекст условий отбора объектов
# Возвращает:
#        MSL_META_OFF (0)  - исключить отбор метаобъектов
#        MSL_META_ON (1)   - отбирать метаобъекты наряду с другими
#        MSL_META_ONLY (2) - отбирать только метаобъекты

    mapGetMetaObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMetaObjectsFlag', maptype.HSELECT)
    def mapGetMetaObjectsFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetMetaObjectsFlag_t (_hselect)


# Установить в контексте условий отбора признак отбора метаобъектов
# hselect - контекст условий отбора объектов
# flag - условия отбора метаобъектов:
#        MSL_META_OFF (0)  - исключить отбор метаобъектов
#        MSL_META_ON (1)   - отбирать метаобъекты наряду с другими
#        MSL_META_ONLY (2) - отбирать только метаобъекты

    mapSetMetaObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetMetaObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetMetaObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetMetaObjectsFlag_t (_hselect, _flag)


# Установить в контексте условий отбора уровень доступа к объектам по значимости
# hselect - контекст условий отбора объектов
# flag - уровень значимости: 0 - все объекты,
#        1 - отобрать только основные объекты (которые отображаются в базовом масштабе карты),
#        2 - отобрать только дополнительные объекты (которые не отображаются в базовом масштабе карты)

    mapSetLevelObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetLevelObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetLevelObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetLevelObjectsFlag_t (_hselect, _flag)


# Запросить в контексте условий отбора уровень доступа к объектам по значимости
# hselect - контекст условий отбора объектов
# Возвращает: 0 - все объекты,
#        1 - отобрать только основные объекты (которые отображаются в базовом масштабе карты),
#        2 - отобрать только дополнительные объекты (которые не отображаются в базовом масштабе карты)

    mapGetLevelObjectsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLevelObjectsFlag', maptype.HSELECT)
    def mapGetLevelObjectsFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetLevelObjectsFlag_t (_hselect)


# Установить в контексте условий отбора признак отбора групп объектов при поиске по области
# hselect - контекст условий отбора объектов
# flag - признак отбора групп объектов при поиске по области: 1 - включен, 0 - отключен
# В этом случае при отборе любого объекта группы включается вся группа (аналогично мультиполигону)

    mapSetSelectGroupFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetSelectGroupFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectGroupFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetSelectGroupFlag_t (_hselect, _flag)


# Запросить в контексте условий отбора признак отбора групп объектов при поиске по области
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapGetSelectGroupFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSelectGroupFlag', maptype.HSELECT)
    def mapGetSelectGroupFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectGroupFlag_t (_hselect)


# Запросить в контексте условий отбора флаг отображения кластеров
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapGetShowClusterFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetShowClusterFlag', maptype.HSELECT)
    def mapGetShowClusterFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetShowClusterFlag_t (_hselect)


# Установить в контексте условий отбора флаг отображения кластеров
# hselect - контекст условий отбора объектов
# flag - признак отображения кластеров точечных объектов: 1 - включен, 0 - отключен
# При ошибке возвращает ноль

    mapSetShowClusterFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetShowClusterFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetShowClusterFlag(_hselect: maptype.HSELECT, _flag: int) -> int:
        return mapSetShowClusterFlag_t (_hselect, _flag)


# Зафиксировать в контексте поиска количественный состав карты
# hmap - идентификатор открытых данных (документа)
# Используется при редактировании карты для исключения из поиска вновь созданных объектов
# При ошибке возвращает ноль

    mapFreezeMapContents_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFreezeMapContents', maptype.HMAP)
    def mapFreezeMapContents(_hmap: maptype.HMAP) -> int:
        return mapFreezeMapContents_t (_hmap)


# Сбросить в контексте поиска данные о количественном составе карты
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapDefreezeMapContents_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDefreezeMapContents', maptype.HMAP)
    def mapDefreezeMapContents(_hmap: maptype.HMAP) -> int:
        return mapDefreezeMapContents_t (_hmap)


# Найти номер точки на контурах объекта и подобъектов, ближайшей к заданной
# hobj - идентификатор объекта карты в памяти
# srcpoint - координаты исходной точки (в метрах), относительно которой выполняется поиск
# subject - номер подобъекта c 0 (если равен -1 - поиск по всей метрике)
# Возвращает номер точки (номер первой точки равен 1)
# Для определения номера найденного подобъекта при поиске по всей метрике применяется mapGetCurrentSubject()
# При ошибке возвращает ноль

    mapSeekNearPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekNearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekNearPoint(_hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekNearPoint_t (_hobj, _srcpoint, _subject)


# Найти координаты точки на контурах объекта и подобъектов, ближайшей к заданной
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# srcpoint - координаты исходной точки (в метрах), относительно которой выполняется поиск
# destpoint - поле для размещения координат точки (в метрах), ближайшей к заданной
# Возвращает номер точки, после которой находится или c которой совпадает найденная точка
# Для определения номера найденного подобъекта при поиске по всей метрике применяется mapGetCurrentSubject()
# При ошибке возвращает ноль

    mapSeekNearVirtualPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekNearVirtualPoint', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPoint(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekNearVirtualPoint_t (_hmap, _hobj, _srcpoint, _destpoint)


# Запросить у объекта номер текущего подобъекта
# hObj - идентификатор объекта в памяти
# Вызывать сразу после поиска точки с помощью функций mapSeekNearPoint, mapSeekNearVirtualPoint
# Возвращает номер подобъекта (начиная с 1) или ноль, если текущим контуром является главный контур объекта

    mapGetCurrentSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCurrentSubject', maptype.HOBJ)
    def mapGetCurrentSubject(_hobj: maptype.HOBJ) -> int:
        return mapGetCurrentSubject_t (_hobj)


# Найти координаты точки на контуре подобъекта, ближайшей к заданной
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта с 0
# srcpoint - координаты исходной точки (в метрах), относительно которой выполняется поиск
# destpoint - поле для размещения координат точки (в метрах), ближайшей к заданной
# Возвращает номер точки, после которой находится или c которой совпадает найденная точка
# При ошибке возвращает ноль

    mapSeekNearVirtualPointSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekNearVirtualPointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPointSubject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _subject: int, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekNearVirtualPointSubject_t (_hmap, _hobj, _subject, _srcpoint, _destpoint)


# Найти координаты точки, лежащей на заданном расстоянии вдоль контура от заданной точки на контуре
# hobj - идентификатор объекта карты в памяти
# number - номер начальной точки
# distance - расстояние в метрах (если distance > 0 - поиск по направлению цифрования, иначе - в обратном направлении)
# destpoint - поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
# subject - номер подобъекта c 0
# tail - поле для записи длины остатка (в метрах), для которого не нашлось места на контуре объекта
#        Пример: если длина контура = 150, distance = 100, то tail = 50
# Если поле tail не задано, то функция вернет ноль при превышении длины объекта
# Возвращает номер точки, после которой находится или c которой совпадает найденная точка
# Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки
# Если запрошенное расстояние превышает длину объекта - возвращает ноль
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistanceEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekVirtualPointByDistanceEx', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSeekVirtualPointByDistanceEx(_hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int, _tail: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSeekVirtualPointByDistanceEx_t (_hobj, _number, _distance, _destpoint, _subject, _tail)


# Найти координаты точки, лежащей на заданном расстоянии (без учета проекции) вдоль контура от заданной точки на контуре
# hobj - идентификатор объекта карты в памяти
# number - номер начальной точки
# distance - расстояние в метрах (если distance > 0 - поиск по направлению цифрования, иначе - в обратном направлении)
# destpoint - поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
# subject - номер подобъекта c 0
# Расчеты выполняются в системе координат карты без учета проекции
# Возвращает номер точки, после которой находится или c которой совпадает найденная точка
# Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки
# Если запрошенное расстояние превышает длину объекта - возвращает ноль
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistanceInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekVirtualPointByDistanceInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekVirtualPointByDistanceInMap(_hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekVirtualPointByDistanceInMap_t (_hobj, _number, _distance, _destpoint, _subject)


# Найти координаты точки, лежащей на заданном расстоянии (с учетом рельефа) вдоль контура от заданной точки на контуре
# hmap - идентификатор открытых данных (документа)
# number - номер начальной точки
# distance - расстояние в метрах (если distance > 0 - поиск по направлению цифрования, иначе - в обратном направлении)
# destpoint - поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
# subject - номер подобъекта c 0
# Возвращает номер точки, после которой находится или c которой совпадает найденная точка
# Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки
# При отсутствии рельефа (матрицы высот, слоев, модели рельефа) определяет точку без учета рельефа (mapSeekVirtualPointByDistance)
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistanceWithHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekVirtualPointByDistanceWithHeight', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekVirtualPointByDistanceWithHeight(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekVirtualPointByDistanceWithHeight_t (_hmap, _hobj, _number, _distance, _destpoint, _subject)


# Найти точечный объект на заданной карте вблизи заданной точки
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# srcpoint - координаты исходной точки (в метрах), относительно которой выполняется поиск
# radius - радиус области поиска в метрах (от 1 мкм до метров)
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# При ошибке возвращает ноль

    mapSeekPointObjectByDistance_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekPointObjectByDistance', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_long)
    def mapSeekPointObjectByDistance(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float, _visible: int = 0) -> int:
        return mapSeekPointObjectByDistance_t (_hmap, _hsite, _hobj, _srcpoint, _radius, _visible)


# Найти точечный объект на заданной карте вблизи заданного объекта при наличии у объекта семантики с заданным кодом
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hsrcobj - идентификатор объекта, вокруг точек которого выполняется поиск
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# radius - радиус области поиска в метрах (от 1 мкм до метров)
# semcode - код семантики, который должен быть у найденного объекта (если semcode = 0 - семантика не учитывается)
# value - значение семантики, которое должно быть у найденного объекта (если value = 0 - значение может быть любое)
# visible - признак учета видимости объектов на карте: 1 - включен, 0 - отключен
# При ошибке возвращает ноль

    mapSeekPointObjectByDistanceAndName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekPointObjectByDistanceAndName', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSeekPointObjectByDistanceAndName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hsrcobj: maptype.HOBJ, _hobj: maptype.HOBJ, _radius: float, _semcode: int, _value: mapsyst.WTEXT, _visible: int = 0) -> int:
        return mapSeekPointObjectByDistanceAndName_t (_hmap, _hsite, _hsrcobj, _hobj, _radius, _semcode, _value.buffer(), _visible)


# Объединение (сшивка) двух объектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# hdest - идентификатор объекта карты в памяти, в котором будет размещен результат
# method - метод сшивки (тип результирующего объекта):
#          LOCAL_SQUARE - площадной (на входе только два площадных или линейных замкнутых объекта),
#          LOCAL_LINE - линейный (на входе два линейных незамкнутых объекта)
# delta - допуск при дотягивании (в метрах) или 0. Если delta = 0,
#         то для карт масштаба <= 500000 устанавливается значение 0.001, иначе - 0.01
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# Не допускается сшивать замкнутый и незамкнутый объекты
# При успешном выполнении возвращает значение hobj, иначе - 0

    mapGetObjectsUnion_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapGetObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapGetObjectsUnion(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _hobj: maptype.HOBJ, _method: int, _delta: float) -> maptype.HOBJ:
        return mapGetObjectsUnion_t (_hobj1, _hobj2, _hobj, _method, _delta)


# Объединение (сшивка) двух площадных объектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# hdest - идентификатор объекта карты в памяти, в котором будет размещен результат
# delta - допуск при дотягивании (в метрах)
# flag - флаг обработки:
#        0 - сшить с предварительной проверкой на пересечение;
#        1 - добавить точки пересечения (требуется дополниетльное время на проверку) и сшить;
#        2 - сшить непересекающиеся объекты, расположенные на расстоянии до delta (без предварительной проверки)
# При превышении допуска между объектами сшивка выполняется через три ближайших точки (точка одного объекта, отрезок - другого)
# Если вторая пара ближайших точек ближе delta, то сшивка выполняется по всем точкам, попавшим в допуск delta
# При успешном выполнении возвращает значение hobj, иначе - 0

    mapSquareObjectsUnion_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSquareObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapSquareObjectsUnion(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _hdest: maptype.HOBJ, _delta: float, _flag: int) -> maptype.HOBJ:
        return mapSquareObjectsUnion_t (_hobj1, _hobj2, _hdest, _delta, _flag)


# Создать процесс согласования двух объектов
# htemp - идентификатор существующего объекта-шаблона (замкнутый контур без подобъектов),
#         по которому согласовывают внешний контур второго объекта
# hobj - идентификатор объекта карты (линейный или площадной объект с подобъектами),
#        у которого нужно найти внешнюю часть, примыкающую к контуру шаблона
# method - тип результирующих объектов: LOCAL_SQUARE - площадной, LOCAL_LINE - линейный
# delta - допуск при дотягивании (в метрах) или 0. Если delta = 0,
#         то для карт масштаба <= 500000 устанавливается значение 0.001, иначе - 0.01
# Тип результирующих объектов зависит от типа второго объекта:
# - если второй объект незамкнутый, то тип только LOCAL_LINE;
# - если второй объект замкнутый, то тип может быть LOCAL_LINE или LOCAL_SQUARE
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# По окончании обработки необходимо вызвать mapFreeObjectsConsent
# При ошибке возвращает ноль

    mapCreateObjectsConsent_t = mapsyst.GetProcAddress(curLib,maptype.HCROSSCONS,'mapCreateObjectsConsent', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapCreateObjectsConsent(_htemp: maptype.HOBJ, _hobj: maptype.HOBJ, _method: int, _delta: float) -> maptype.HCROSSCONS:
        return mapCreateObjectsConsent_t (_htemp, _hobj, _method, _delta)


# Освободить ресурсы, выделенные в mapCreateObjectsConsent
# hcross - идентификатор процесса согласования

    mapFreeObjectsConsent_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeObjectsConsent', maptype.HCROSSCONS)
    def mapFreeObjectsConsent(_hcross: maptype.HCROSSCONS) -> ctypes.c_void_p:
        return mapFreeObjectsConsent_t (_hcross)


# Запросить общую часть контура
# hcross - идентификатор процесса согласования
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# При ошибке возвращает ноль

    mapGetNextConsent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetNextConsent', maptype.HCROSSCONS, maptype.HOBJ)
    def mapGetNextConsent(_hcross: maptype.HCROSSCONS, _hobj: maptype.HOBJ) -> int:
        return mapGetNextConsent_t (_hcross, _hobj)


# Согласовать метрику объектов, имеющих одну систему координат
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# precision - точность согласования (в метрах)
# error - поле для размещения кода ошибки: OVL_ERR_NONE, ... OVL_ERR_END (crossapi.h)
# Возвращает: 0 - объекты не могут быть согласованы
#             1 - изменена метрика объекта 1
#             2 - изменена метрика объекта 2
#             3 - изменена метрика объектов 1 и 2

    mapAdjustObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAdjustObjects', maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.POINTER(ctypes.c_long))
    def mapAdjustObjects(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _precision: float, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapAdjustObjects_t (_hobj1, _hobj2, _precision, _error)


# Проверить совпадение контуров по отрезкам
# hobj1    - идентификатор первого объекта
# hobj2    - идентификатор второго объекта
# subject1 - подобъект объекта hobj1. Если subject1 = -1, то проверяются все подобъекты
# subject2 - подобъект объекта hobj2. Если subject2 = -1, то проверяются все подобъекты
# delta - допуск для сравнения координат точек на совпадение (в метрах)
# mode - режим обработки двух площадных объектов:
#        1 - определение числа пар совпадающих внешних контуров,
#        2 - определение числа пар совпадающих внутренних контуров,
#        3 - определение числа пар совпадающих внешних и внутренних контуров,
#        0 - определение наличия хотя бы одной пары совпадающих любых контуров,
#       -1 - определение наличия хотя бы одной пары совпадающих внешних контуров,
#       -2 - определение наличия хотя бы одной пары совпадающих внутренних контуров,
#       -3 - определение наличия хотя бы одной пары совпадающих внешних и внутренних контуров
# Анализ контуров площадных объектов может выполняться с учетом признаков внешних и внутренних контуров
# Каждая пара контуров, все отрезки которых совпадают, считаются совпадающими
# (независимо от направления цифрования, положения начальных точек и последовательности контуров)
# Возвращает число пар совпадающих контуров
# При ошибке возвращает ноль

    mapCompareMetrics_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareMetrics', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long)
    def mapCompareMetrics(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int, _delta: float, _mode: int) -> int:
        return mapCompareMetrics_t (_hobj1, _subject1, _hobj2, _subject2, _delta, _mode)


# Проверить точки объектов на совпадение в заданном допуске
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# delta - допуск для сравнения координат точек на совпадение (в метрах)
# Если число точек объектов совпадает и координаты отличаются в пределах заданного допуска, то возвращается ненулевое значения
# При ошибке возвращает ноль

    mapCompareObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCompareObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _delta: float) -> int:
        return mapCompareObject_t (_hobj1, _hobj2, _delta)


# Создать процесс поиска точек пересечения двух объектов
# hobj1 - идентификатор первого объекта (линейный или площадной с подобъектами)
# hobj2 - идентификатор второго объекта (линейный или площадной с подобъектами)
# delta - допуск при дотягивании (в метрах) или 0. Если delta = 0,
#         то для карт масштаба <= 500000 устанавливается значение 0.001, иначе - 0.01
# По окончании обработки необходимо вызвать mapFreeCrossPoints
# При ошибке возвращает ноль

    mapCreateObjectCrossPointsEx_t = mapsyst.GetProcAddress(curLib,maptype.HCROSSPOINTS,'mapCreateObjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCreateObjectCrossPointsEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _delta: float) -> maptype.HCROSSPOINTS:
        return mapCreateObjectCrossPointsEx_t (_hobj1, _hobj2, _delta)


# Создать процесс поиска точек пересечения двух объектов или подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# subject1 - номер подобъекта hobj1
# subject2 - номер подобъекта hobj2
# delta - допуск при дотягивании (в метрах) или 0. Если delta = 0,
#         то для карт масштаба <= 500000 устанавливается значение 0.001, иначе - 0.01
# По окончании обработки необходимо вызвать mapFreeCrossPoints
# При ошибке возвращает ноль

    mapCreateSubjectCrossPointsEx_t = mapsyst.GetProcAddress(curLib,maptype.HCROSSPOINTS,'mapCreateSubjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCreateSubjectCrossPointsEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _subject1: int, _subject2: int, _delta: float) -> maptype.HCROSSPOINTS:
        return mapCreateSubjectCrossPointsEx_t (_hobj1, _hobj2, _subject1, _subject2, _delta)


# Запросить количество точек пересечения
# hcross - идентификатор процесса поиска точек пересечения
# При ошибке возвращает ноль

    mapGetCrossCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCrossCount', maptype.HCROSSPOINTS)
    def mapGetCrossCount(_hcross: maptype.HCROSSPOINTS) -> int:
        return mapGetCrossCount_t (_hcross)


# Запросить описание точки пересечения
# hcross - идентификатор процесса поиска точек пересечения
# number - номер точки (с 1)
# point - указатель на структуру для размещения результата запроса
# При ошибке возвращает ноль

    mapGetCrossPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCrossPoint', maptype.HCROSSPOINTS, ctypes.c_long, ctypes.POINTER(maptype.CROSSPOINT))
    def mapGetCrossPoint(_hcross: maptype.HCROSSPOINTS, _number: int, _point: ctypes.POINTER(maptype.CROSSPOINT)) -> int:
        return mapGetCrossPoint_t (_hcross, _number, _point)


# Освободить ресурсы, выделенные в mapCreateObjectCrossPointsEx
# hcross - идентификатор процесса поиска точек пересечения

    mapFreeCrossPoints_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeCrossPoints', maptype.HCROSSPOINTS)
    def mapFreeCrossPoints(_hcross: maptype.HCROSSPOINTS) -> ctypes.c_void_p:
        return mapFreeCrossPoints_t (_hcross)


# Добавить точки пересечения объектов в метрику
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# При вставке точек пересечения возвращает ненулевое значение
# При ошибке возвращает ноль

    mapInsertPointCross_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInsertPointCross', maptype.HOBJ, maptype.HOBJ)
    def mapInsertPointCross(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapInsertPointCross_t (_hobj1, _hobj2)


# Создать точки пересечений выделенных объектов
# hmap - идентификатор открытых данных (документа)
# precision - точность анализа близости точек (в метрах) или 0
# actioncode - код транзакции для формирования записи в журнале транзакций (MED_SEEKCROSS или 0)
# Обрабатываются попарно площадные и линейные объекты внутри своих карт с помощью функции mapTotalSeekObject
# При ошибке возвращает ноль

    mapCreateIntersectionPointsEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateIntersectionPointsEx', maptype.HMAP, ctypes.c_double, ctypes.c_long)
    def mapCreateIntersectionPointsEx(_hmap: maptype.HMAP, _precision: float, _actioncode: int) -> int:
        return mapCreateIntersectionPointsEx_t (_hmap, _precision, _actioncode)


# Создать процесс анализа пересечений базового объекта с остальными
# hbase - идентификатор базового объекта
# По окончании обработки необходимо вызвать mapCloseCheckInsideBaseObject
# При ошибке возвращает 0

    mapOpenCheckInsideBaseObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapOpenCheckInsideBaseObject', maptype.HOBJ)
    def mapOpenCheckInsideBaseObject(_hbase: maptype.HOBJ) -> ctypes.c_void_p:
        return mapOpenCheckInsideBaseObject_t (_hbase)


# Определить взаиморасположение двух объектов с учетом подобъектов
# hcheck - идентификатор просесса анализа пересечений, содержащего объект hbase
# hobj - идентификатор проверяемого объекта на пересечение
# list - поле для размещения указателя на отсортированный список номеров подобъектов,
#        с которыми пересекаются габариты шаблона
# count - поле для размещения количества номеров в списке list
# Возвращает: 1 - объект hbase внутри hobj всеми внешними контурами
#             2 - объект hobj внутри hbase всеми внешними контурами
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
#             5 - внешние контуры объекта hbase внутри и снаружи второго hobj
#             6 - внешние контуры объекта hobj внутри и снаружи hbase
#             7 - внешние контуры объекта hobj совпадают с подобъектами hbase
#             8 - касание, объект hobj внутри hbase
#             9 - касание, объект hobj снаружи hbase
#            10 - касание, объект hbase внутри hobj
# При ошибке возвращает ноль

    mapCheckInsideBaseObjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideBaseObjectEx', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_int))
    def mapCheckInsideBaseObjectEx(_hcheck: ctypes.c_void_p, _htest: maptype.HOBJ, _list: ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), _count: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCheckInsideBaseObjectEx_t (_hcheck, _htest, _list, _count)


# Обновить описание первого объекта после редактирования
# hcheck - идентификатор процесса анализа пересечений

    mapUpdateInsideBaseObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUpdateInsideBaseObject', ctypes.c_void_p)
    def mapUpdateInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapUpdateInsideBaseObject_t (_hcheck)


# Освободить ресурсы, выделенные в mapOpenCheckInsideBaseObject
# hcheck - идентификатор процесса анализа пересечений

    mapCloseCheckInsideBaseObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseCheckInsideBaseObject', ctypes.c_void_p)
    def mapCloseCheckInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseCheckInsideBaseObject_t (_hcheck)


# Определить взаиморасположение области и объекта
# hbase - идентификатор базового объекта (обязательно замкнута)
# hobj - идентификатор объекта карты в памяти
# precision - точность анализа близости точек (в метрах)
# Возвращает: 1 - область внутри замкнутого объекта
#             2 - объект внутри области
#             3 - область и объект пересекаются,
#             4 - область и объект не пересекаются
#             5 - объект касается области и лежит внутри нее
#             6 - объект касается области и лежит снаружи
# При ошибке возвращает ноль

    mapCheckOverlap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckOverlap', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckOverlap(_hbase: maptype.HOBJ, _hobj: maptype.HOBJ, _precision: float = 0) -> int:
        return mapCheckOverlap_t (_hbase, _hobj, _precision)


# Проверить наличие пересечения двух объектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# Если объекты пересекаются - возвращает ненулевое значение
# При ошибке или неверном типе объектов возвращает ноль

    mapGetObjectsCross_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectsCross', maptype.HOBJ, maptype.HOBJ)
    def mapGetObjectsCross(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapGetObjectsCross_t (_hobj1, _hobj2)


# Определить пересечение контуров (точек метрики) двух объектов с учетом подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# При наличии пересечений контуров возвращает ненулевое значение
# При ошибке возвращает 0

    mapCheckCrossObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckCrossObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckCrossObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapCheckCrossObject_t (_hobj1, _hobj2)


# Определить пересечение контуров (подобъектов) двух объектов
# hobj1    - идентификатор первого объекта
# hobj2    - идентификатор второго объекта (может быть равен hobj1)
# subject1 - номер подобъекта hobj1
# subject2 - номер подобъекта hobj2
# precision - точность анализа близости точек и контуров (в метрах)
# При наличии пересечений контуров возвращает ненулевое значение
# Если hobj1 = hobj2 и subject1 = subject2, то возвращает 1
# При ошибке возвращает 0

    mapCheckCrossSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckCrossSubject', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapCheckCrossSubject(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int, _precision: float) -> int:
        return mapCheckCrossSubject_t (_hobj1, _subject1, _hobj2, _subject2, _precision)


# Определить пересечение замкнутого контура объектом
# hobj1 - идентификатор первого объекта (замкнутый контур)
# hobj2 - идентификатор второго объекта (произвольный объект с подобъектами)
# precision - точность анализа близости точек и контуров (в метрах)
# Возвращает ненулевое значение, если в результате пересечения объект hobj2 разбивается на части
# При ошибке возвращает 0

    mapCheckCrossExclusiveObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckCrossExclusiveObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckCrossExclusiveObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _precision: float) -> int:
        return mapCheckCrossExclusiveObject_t (_hobj1, _hobj2, _precision)


# Определить взаиморасположение двух объектов без учета подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# Возвращает: 1 - первый объект внутри второго,
#             2 - второй объект внутри первого,
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
# Значение 3 возвращается всегда при наличии пересечения главных контуров (0)
# Значения 1 и 2 - только для замкнутых объектов
# При ошибке возвращает ноль

    mapCheckInsideObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapCheckInsideObject_t (_hobj1, _hobj2)


# Определить взаиморасположение двух контуров
# hobj1    - идентификатор первого объекта
# hobj2    - идентификатор второго объекта
# subject1 - номер подобъекта hobj1
# subject2 - номер подобъекта hobj2
# Возвращает: 1 - первый контур внутри второго,
#             2 - второй контур внутри первого,
#             3 - контуры пересекаются,
#             4 - контуры не пересекаются
# Значение 3 возвращается всегда при наличии пересечения контуров
# Значения 1 и 2 - только для замкнутых контуров
# При ошибке возвращает ноль

    mapCheckInsideSubjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideSubjectEx', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCheckInsideSubjectEx(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int) -> int:
        return mapCheckInsideSubjectEx_t (_hobj1, _subject1, _hobj2, _subject2)


# Определить вхождение первого объекта во второй (включая подобъекты)
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# Возвращает: 1 - первый объект внутри второго (второй объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - первый объект не внутри второго (возможно пересечение объектов)
# При ошибке возвращает ноль

    mapCheckInsideFirstObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideFirstObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideFirstObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapCheckInsideFirstObject_t (_hobj1, _hobj2)


# Определить взаиморасположение двух объектов с учетом подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# Возвращает: 1 - первый объект внутри внешнего контура второго,
#             2 - второй объект внутри внешнего контура первого,
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
# Значение 3 возвращается всегда при наличии пересечения любых контуров
# Значения 1 и 2 - только для замкнутых объектов
# Для мультиполигонов значения 1 и 2 возвращаются при выполнении условия для любой пары внешних контуров
# Попадание контура в подобъект внешнего контура считается внешним расположением
# При ошибке возвращает 0

    mapCheckInsideObjectAndSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideObjectAndSubject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectAndSubject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapCheckInsideObjectAndSubject_t (_hobj1, _hobj2)


# Определить взаиморасположение двух объектов с учетом подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# Возвращает: 1 - первый объект внутри второго всеми внешними контурами
#             2 - второй объект внутри первого всеми внешними контурами
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
#             5 - внешние контура первого объекта внутри и снаружи второго
#             6 - внешние контура второго объекта внутри и снаружи первого
# При ошибке возвращает 0

    mapCheckInsideObjectTotal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideObjectTotal', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectTotal(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        return mapCheckInsideObjectTotal_t (_hobj1, _hobj2)


# Определить взаиморасположение двух объектов с учетом подобъектов
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# subject - поле для размещения номера подобъекта внешнего контура мультиполигона (код 1 или 2)
# Возвращает: 1 - первый объект внутри второго (второй объект должен быть замкнутым),
#             2 - второй объект внутри первого (первый объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются,
#            -1 - первый объект внутри подобъекта второго объекта (второй объект должен быть замкнутым),
#            -2 - второй объект внутри подобъекта первого объекта (первый объект должен быть замкнутым)
# При ошибке возвращает ноль

    mapCheckInsideObjectPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideObjectPro', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCheckInsideObjectPro(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _subject: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCheckInsideObjectPro_t (_hobj1, _hobj2, _subject)


# Определить взаиморасположение двух объектов (включая подобъекты)
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# destpoint - поле для размещения координат первой точки пересечения (в метрах)
# Возвращает: 1 - первый объект внутри второго (второй объект должен быть замкнутым),
#             2 - второй объект внутри первого (первый объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются,
#             5 - объекты (подобъекты) имеют общие отрезки или общую точку,
#           - 1 - первый объект внутри подобъекта второго объекта (второй объект должен быть замкнутым),
#           - 2 - второй объект внутри подобъекта первого объекта (первый объект должен быть замкнутым)
# При ошибке возвращает ноль

    mapCheckInsideObjectPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideObjectPoint', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCheckInsideObjectPoint(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCheckInsideObjectPoint_t (_hobj1, _hobj2, _destpoint)


# Определить вхождение всех точек контура подобъекта в другой контур подобъекта
# hobj1 - идентификатор первого объекта
# hobj2 - идентификатор второго объекта
# subject1 - номер подобъекта объекта hobj1
# subject2 - номер подобъекта объекта hobj2
# Возвращает: 1 - все точки внутри объекта/подобъекта и на контуре,
#             2 - есть внешние точки (хотя бы одна, а может и все),
#             3 - все точки контуров совпадают,
#             4 - все точки лежат на отрезке метрики или совпадают
# При ошибке возвращает ноль

    mapCheckInsideSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsideSubject', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCheckInsideSubject(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int) -> int:
        return mapCheckInsideSubject_t (_hobj1, _subject1, _hobj2, _subject2)


# Определить положение точки относительно замкнутого объекта
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта с 0. Если равно -1, то проверяются все контура, учитывая
#           мультиполигоны. При попадании в подобъект возвращает 2 и заполняет номер
# point - координаты точки в прямоугольной системе координат (в метрах на местности)
# subjectnumber - поле для записи номера подобъекта, в который попадает точка (при возврате 2, 3, 4) или 0
# Возвращает: 1 - точка внутри объекта (подобъекта),
#             2 - точка за пределами объекта (подобъекта),
#             3 - точка совпадает с точкой метрики,
#             4 - точка лежит на отрезке
# При ошибке возвращает ноль

    mapCheckInsidePointEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckInsidePointEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_long))
    def mapCheckInsidePointEx(_hobj: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subjectnumber: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCheckInsidePointEx_t (_hobj, _subject, _point, _subjectnumber)


# Найти пересечение двух отрезков
# pounta1 - координаты точки 1 отрезка A
# pounta2 - координаты точки 2 отрезка A
# pountb1 - координаты точки 1 отрезка B
# pountb2 - координаты точки 2 отрезка B
# crosspoint1 - поле для размещения первой точки пересечения
# crosspoint2 - поле для размещения второй точки пересечения
# precision - точность анализа близости точек (в метрах)
# Возвращает: 1 - одна точка пересечения, 2 - отрезки A и B имеют общую часть или совпадают
# При отсутствии точки пересечения или ошибке возвращает ноль

    mapCrossCutData_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCrossCutData', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCrossCutData(_pounta1: ctypes.POINTER(maptype.DOUBLEPOINT), _pounta2: ctypes.POINTER(maptype.DOUBLEPOINT), _pountb1: ctypes.POINTER(maptype.DOUBLEPOINT), _pountb2: ctypes.POINTER(maptype.DOUBLEPOINT), _crosspoint1: ctypes.POINTER(maptype.DOUBLEPOINT), _crosspoint2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float = maptype.DELTANULL) -> int:
        return mapCrossCutData_t (_pounta1, _pounta2, _pountb1, _pountb2, _crosspoint1, _crosspoint2, _precision)


# Найти пересечение отрезка и участка контура подобъекта
# hobj - идентификатор объекта карты в памяти
# pount1 - координаты первой точки отрезка
# pount2 - координаты второй точки отрезка
# first - номер первой точки анализируемого участка
# last  - номер последней точки анализируемого участка
# dest1 - указатель на структуру для размещения описания первой точки пересечения
# dest2 - указатель на структуру для размещения описания второй точки пересечения
# subject - номер анализируемого подобъекта
# precision - точность анализа близости точек (в метрах)
# Если отрезок и участок контура имеют общую часть, то заполняются dest1 и dest2
# При отсутствии точек пересечения или ошибке возвращает ноль

    mapCrossCutAndSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCrossCutAndSubject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.NUMBERPOINT), ctypes.POINTER(maptype.NUMBERPOINT), ctypes.c_long, ctypes.c_double)
    def mapCrossCutAndSubject(_hobj: maptype.HOBJ, _pount1: ctypes.POINTER(maptype.DOUBLEPOINT), _pount2: ctypes.POINTER(maptype.DOUBLEPOINT), _first: int, _last: int, _dest1: ctypes.POINTER(maptype.NUMBERPOINT), _dest2: ctypes.POINTER(maptype.NUMBERPOINT), _subject: int, _precision: float = maptype.PS_FIRST) -> int:
        return mapCrossCutAndSubject_t (_hobj, _pount1, _pount2, _first, _last, _dest1, _dest2, _subject, _precision)


# Запросить признак положения точки относительно отрезка
# point - координаты анализируемой точки
# pount1 - координаты первой точки отрезка
# pount2 - координаты второй точки отрезка
# precision - точность анализа близости точек и отрезка (в метрах)
# Возвращает признак положения точки: PS_FIRST, PS_LEFT, ... (maptype.h)
# При ошибке возвращает 0

    mapGetPointPosition_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPointPosition', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapGetPointPosition(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _pount1: ctypes.POINTER(maptype.DOUBLEPOINT), _pount2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float = maptype.DELTANULL) -> int:
        return mapGetPointPosition_t (_point, _pount1, _pount2, _precision)


# Найти две точки перпендикуляра от отрезка на заданном расстоянии от произвольной точки
# pount1 - координаты первой точки отрезка
# pount2 - координаты второй точки отрезка
# dest1 - поле для размещения первой точки перпендикуляра
# dest2 - поле для размещения второй точки перпендикуляра
# point - координаты точки, от которой производится расчет (если point = 0, то point = pount1)
# distance - растояние от точки point
# При ошибке возвращает ноль

    mapSeekPointNormalLine_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekPointNormalLine', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointNormalLine(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _dest1: ctypes.POINTER(maptype.DOUBLEPOINT), _dest2: ctypes.POINTER(maptype.DOUBLEPOINT), _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT) = None) -> int:
        return mapSeekPointNormalLine_t (_point1, _point2, _dest1, _dest2, _distance, _point)


# Выполнить вырезание контуров одного набора площадных объектов из другого набора площадных объектов
# hmessage - идентификатор окна (для Windows - HWND), которое будет извещаться
#            (для отмены сообщений установить идентификатор в ноль)
# hmap - идентификатор открытых данных (документа)
# editset - номер набора редактируемых объектов в файле OBX карты в папке \LOG
# tempset - номер набора вырезаемых объектов в файле OBX карты в папке \LOG
# adjust - признак согласования контуров вырезаемых объектов с редактируемыми объектами: 1 - включен, 0 - отключен
# multi - признак формирования мультиполигона при делении контура редактируемого объекта на части: 1 - включен, 0 - отключен
# Процесс посылает сообщение WM_PROGRESSBARUN (wparm: процент обработки)
# Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# Возвращает число обработанных контуров, если ни в одном контуре не было вырезания - возвращает (-1)
# При ошибке возвращает ноль

    mapCutObjectListFromList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCutObjectListFromList', maptype.HMESSAGE, maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCutObjectListFromList(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _editset: int, _tempset: int, _adjust: int, _multi: int) -> int:
        return mapCutObjectListFromList_t (_hmessage, _hmap, _editset, _tempset, _adjust, _multi)


# Выполнить разрезание контуров одного набора площадных объектов по контурам другого набора объектов
# hmessage  - идентификатор окна (для Windows - HWND), которое будет извещаться
#             (для отмены сообщений установить идентификатор в ноль)
# hmap - идентификатор открытых данных (документа)
# editset - номер набора редактируемых объектов в файле OBX карты в папке \LOG
# tempset - номер набора объектов линий разрезания в файле OBX карты в папке \LOG
# adjust - признак согласования контуров набора tempset с редактируемыми объектами: 1 - включен, 0 - отключен
# Процесс посылает сообщение WM_PROGRESSBARUN (wparm: процент обработки)
# Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# Возвращает число обработанных контуров
# При ошибке возвращает ноль

    mapSplitObjectListByList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSplitObjectListByList', maptype.HMESSAGE, maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSplitObjectListByList(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _editset: int, _tempset: int, _adjust: int) -> int:
        return mapSplitObjectListByList_t (_hmessage, _hmap, _editset, _tempset, _adjust)


# Вырезать площадной или линейный объект по площадному объекту
# hobj - редактирумый объект (полигон, мультиполигон или мультилиния)
# htemp - идентификатор существующего объекта-шаблона для вырезания (полигон или мультиполигон)
# inside - признак сохраняемых частей объекта: 1 - сохранить внутренние части, 0 - внешние части
# adjust - признак согласования вырезающего объекта с редактируемым: 1 - включен, 0 - отключен
# hobjset - список объектов, дополнительно созданных при сохранении внешних частей внутри
#           подобъектов разрезаемого полигона (mapCreateObjectSet)
# precision - точность согласования вырезаемых контуров (в метрах)
# Возвращает число внешних частей, если объект удален - возвращает (-1)
# При ошибке или при отсутствии обработки возвращает ноль

    mapCutObjectPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCutObjectPro', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.HOBJSET, ctypes.c_double)
    def mapCutObjectPro(_hobj: maptype.HOBJ, _htemp: maptype.HOBJ, _inside: int, _adjust: int, _hobjset: maptype.HOBJSET = 0, _precision: float = 0.001) -> int:
        return mapCutObjectPro_t (_hobj, _htemp, _inside, _adjust, _hobjset, _precision)


# Вырезать карту по площадному объекту (вырезает объекты всех карт документа)
# hmessage - идентификатор окна (для Windows - HWND), которое будет извещаться или ноль
#            Процесс посылает сообщение WM_PROGRESSBARUN (wparam - процент обработки)
#            Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# hmap - идентификатор открытых данных (документа)
# hselect - контекст условий отбора объектов (если hselect = 0 - обработать все объекты)
# htemp - идентификатор существующего объекта-шаблона для вырезания (полигон или мультиполигон)
# name - адрес строки для размещения имени файла карты (sitx/sit/mpt) для записи результата,
# namesize - размер буфера с именем проекта (в байтах)
# inside - признак сохраняемых частей объектов: 1 - сохранить внутренние части, 0 - внешние части
# adjust - признак согласования вырезающего объекта с редактируемыми: 1 - включен, 0 - отключен
# error - поле для размещения кода ошибки: OVL_ERR_NONE, ... OVL_ERR_END (crossapi.h)
# Если если name и namesize != 0, то после вызова функции name содержит уточнённое имя файла проекта
# Если выходная карта содержит несколько карт, то результат сохраняется в виде проекта (mpt)
# При ошибке или при отсутствии обработки возвращает ноль

    mapCutMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCutMap', maptype.HMESSAGE, maptype.HMAP, maptype.HSELECT, maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCutMap(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _hselect: maptype.HSELECT, _templet: maptype.HOBJ, _name: mapsyst.WTEXT, _namesize: int, _inside: int, _adjust: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCutMap_t (_hmessage, _hmap, _hselect, _templet, _name.buffer(), _namesize, _inside, _adjust, _error)


# Создать процесс для построения пересечения мультиполигонов или простых полигонов
# hobj - идентификатор объекта карты в памяти, с которым будет строится пересечение другим объектом
# При построении пересечения данный объект не меняется
# По окончании обработки необходимо вызвать mapCloseCrossMultiPolygon
# При ошибке возвращает ноль

    mapOpenCrossMultiPolygon_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapOpenCrossMultiPolygon', maptype.HOBJ)
    def mapOpenCrossMultiPolygon(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapOpenCrossMultiPolygon_t (_hobj)


# Закрыть процесс построения пересечения мультиполигонов
# hcrossmultipolygon - идентификатор процесса, полученный при вызове mapOpenCrossMultiPolygon

    mapCloseCrossMultiPolygon_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseCrossMultiPolygon', ctypes.c_void_p)
    def mapCloseCrossMultiPolygon(_hcrossmultipolygon: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseCrossMultiPolygon_t (_hcrossmultipolygon)


# Заменить первый объект для построения пересечения мультиполигонов (или простых полигонов)
# hobj - идентификатор объекта карты в памяти, с которым будет строится пересечение другим объектом
# При ошибке возвращает ноль

    mapChangeCrossMultiPolygon_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeCrossMultiPolygon', ctypes.c_void_p, maptype.HOBJ)
    def mapChangeCrossMultiPolygon(_hcrossmultipolygon: ctypes.c_void_p, _hobj: maptype.HOBJ) -> int:
        return mapChangeCrossMultiPolygon_t (_hcrossmultipolygon, _hobj)


# Построить пересечение мультиполигонов в виде мультиполигона
# hcrossmultipolygon - идентификатор процесса, полученный при вызове mapOpenCrossMultiPolygon
# hdest - идентификатор объекта карты в памяти, с которым будет строится пересечение
# error - поле для размещения кода ошибки: OVL_ERR_NONE, ... OVL_ERR_END (crossapi.h)
# Результат построения при успешном выполнении записывается в этот же объект
# При успешном выполнении возвращает ненулевое значение
# При ошибке возвращает ноль

    mapBuildCrossMultiPolygonEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildCrossMultiPolygonEx', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapBuildCrossMultiPolygonEx(_hcrossmultipolygon: ctypes.c_void_p, _hdest: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapBuildCrossMultiPolygonEx_t (_hcrossmultipolygon, _hdest, _error)


# Определить допуск для удаления одинаковых точек
# hobj - идентификатор объекта карты в памяти
# precision - предлагаемый допуск для удаления одинаковых точек (в метрах) или 0
# Возвращает реальный допуск (с учетом параметров карты объекта)

    mapSetPrecision_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSetPrecision', maptype.HOBJ, ctypes.c_double)
    def mapSetPrecision(_hobj: maptype.HOBJ, _precision: float) -> float:
        return mapSetPrecision_t (_hobj, _precision)


# Создать контекст набора объектов, объединенных по групповой семантической характеристике
# Для связи объектов набора используется семантика GROUPLEADER, GROUPSLAVE, GROUPPARTNER
# При ошибке возвращает ноль

    mapCreateObjectSet_t = mapsyst.GetProcAddress(curLib,maptype.HOBJSET,'mapCreateObjectSet')
    def mapCreateObjectSet() -> maptype.HOBJSET:
        return mapCreateObjectSet_t ()


# Освободить ресурсы, выделенные в mapCreateObjectSet
# hobjset - идентификатор контекста набора объектов

    mapFreeObjectSet_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeObjectSet', maptype.HOBJSET)
    def mapFreeObjectSet(_hobjset: maptype.HOBJSET) -> ctypes.c_void_p:
        return mapFreeObjectSet_t (_hobjset)


# Создать набор объектов из объектов карты по существующей в объекте групповой семантике
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapBuildObjectSet_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildObjectSet', maptype.HOBJSET, maptype.HOBJ)
    def mapBuildObjectSet(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ) -> int:
        return mapBuildObjectSet_t (_hobjset, _hobj)


# Создать набор объектов из объектов карты по заданному типу существующей в объекте групповой семантике
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# type - тип семантической характеристики (GROUPLEADER, GROUPSLAVE, GROUPPARTNER) для поиска в hobj
# Если type = 0 - ищет первую попавшуюся групповую семантику
# При ошибке возвращает ноль

    mapBuildObjectSetByType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildObjectSetByType', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapBuildObjectSetByType(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int) -> int:
        return mapBuildObjectSetByType_t (_hobjset, _hobj, _type)


# Создать набор объектов из объектов карты по заданному типу существующей в объекте групповой семантике и номеру группы
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# type - тип семантической характеристики для поиска в hobj (GROUPLEADER, GROUPSLAVE, GROUPPARTNER)
# group - номер группы (объект может принадлежать нескольким группам)
# Если type = 0 - ищет первую попавшуюся групповую семантику
# При ошибке возвращает ноль

    mapBuildObjectSetByTypeGroup_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildObjectSetByTypeGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapBuildObjectSetByTypeGroup(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int, _group: int) -> int:
        return mapBuildObjectSetByTypeGroup_t (_hobjset, _hobj, _type, _group)


# Заполнить контекст поиска из объектов набора
# hobjset - идентификатор контекста набора объектов
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    mapBuildSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildSelect', maptype.HOBJSET, maptype.HSELECT)
    def mapBuildSelect(_hobjset: maptype.HOBJSET, _hselect: maptype.HSELECT) -> int:
        return mapBuildSelect_t (_hobjset, _hselect)


# Запросить количество объектов в наборе
# hobjset - идентификатор контекста набора объектов
# При ошибке возвращает ноль

    mapObjectSetCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetCount', maptype.HOBJSET)
    def mapObjectSetCount(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetCount_t (_hobjset)


# Запросить объект из набора по номеру в наборе
# hobjset - идентификатор контекста набора объектов
# number - порядковый номер объекта в наборе с 1
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат
# При ошибке возвращает ноль

    mapReadObjectSetObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapReadObjectSetObject', maptype.HOBJSET, ctypes.c_long, maptype.HOBJ)
    def mapReadObjectSetObject(_hobjset: maptype.HOBJSET, _number: int, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        return mapReadObjectSetObject_t (_hobjset, _number, _hobj)


# Запросить объект из набора по номеру в наборе
# hobjset - идентификатор контекста набора объектов
# number - порядковый номер объекта в наборе с 1
# Возвращает идентификатор объекта карты из набора
# При ошибке возвращает ноль

    mapObjectSetObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapObjectSetObject', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetObject(_hobjset: maptype.HOBJSET, _number: int) -> maptype.HOBJ:
        return mapObjectSetObject_t (_hobjset, _number)


# Запросить габариты объектов набора
# hobjset - идентификатор контекста набора объектов
# frame - указатель на структуру для размещения прямоугольной области габаритов набора (в метрах)
# При ошибке возвращает ноль

    mapObjectSetFramePlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetFramePlane', maptype.HOBJSET, ctypes.POINTER(maptype.DFRAME))
    def mapObjectSetFramePlane(_hobjset: maptype.HOBJSET, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectSetFramePlane_t (_hobjset, _frame)


# Назначить главный объект в наборе (добавить признак в семантику GROUPLEADER)
# hobjset - идентификатор контекста набора объектов
# number - порядковый номер объекта в листе (из числа объектов в наборе)
# Если number = 0, назначается первый попавшийся объект в наборе
# В семантику объекта GROUPLEADER записывает ключ самого объекта (mapObjectKey)
# При ошибке возвращает ноль

    mapObjectSetNominateLeader_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetNominateLeader', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetNominateLeader(_hobjset: maptype.HOBJSET, _number: int) -> int:
        return mapObjectSetNominateLeader_t (_hobjset, _number)


# Удалить объект из набора по номеру в наборе
# hobjset - идентификатор контекста набора объектов
# number - порядковый номер объекта в наборе с 1
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен
# Удаленный объект заменяется на последний из списка
# Если объект главный в группе (GROUPLEADER) - удаляется вся группа
# При ошибке возвращает ноль

    mapObjectSetClearObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetClearObject', maptype.HOBJSET, ctypes.c_long, ctypes.c_long)
    def mapObjectSetClearObject(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        return mapObjectSetClearObject_t (_hobjset, _number, _save)


# Удалить все объекты из набора
# hobjset - идентификатор контекста набора объектов
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен

    mapObjectSetClear_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapObjectSetClear', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetClear(_hobjset: maptype.HOBJSET, _save: int) -> ctypes.c_void_p:
        return mapObjectSetClear_t (_hobjset, _save)


# Запросить признак группового объекта (по семантике)
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# group - поле для размещения номера группы объекта (если он нужен) или 0
# Возвращает код групповой семантики (GROUPLEADER, GROUPSLAVE, GROUPPARTNER) или ноль

    mapObjectSetIsGroup_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetIsGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapObjectSetIsGroup(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _group: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapObjectSetIsGroup_t (_hobjset, _hobj, _group)


# Проверить наличие групповой семантики у объекта
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# type - тип групповой семантики GROUPLEADER, GROUPSLAVE, GROUPPARTNER
# Возвращает номер группы или ноль при отсутствии

    mapObjectSetGetTypeSemn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetGetTypeSemn', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetGetTypeSemn(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int) -> int:
        return mapObjectSetGetTypeSemn_t (_hobjset, _hobj, _type)


# Удалить все объекты набора с карты
# hobjset - идентификатор контекста набора объектов
# При ошибке возвращает ноль

    mapObjectSetDelete_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetDelete', maptype.HOBJSET)
    def mapObjectSetDelete(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetDelete_t (_hobjset)


# Удалить групповую семантику из объекта
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# group - номер группы
# Если group = 0, то используется текущий номер группы контекста набора объектов hobjset
# При ошибке возвращает ноль

    mapObjectSetDeleteSemantic_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetDeleteSemantic', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetDeleteSemantic(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _group: int) -> int:
        return mapObjectSetDeleteSemantic_t (_hobjset, _hobj, _group)


# Отобразить набор
# hobjset - идентификатор контекста набора объектов
# hmap - идентификатор открытых данных (документа)
# hdc - идентификатор контекста устройства отображения
# rect - координаты прямоугольной области отображения (в пикселах)
# При ошибке возвращает ноль

    mapPaintObjectSet_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintObjectSet', maptype.HOBJSET, maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT))
    def mapPaintObjectSet(_hobjset: maptype.HOBJSET, _hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        return mapPaintObjectSet_t (_hobjset, _hmap, _hdc, _rect)


# Сохранить набор
# hobjset - идентификатор контекста набора объектов
# always - признак сохранения: 1 - сохранять всегда, 0 - сохранять только, если были изменения
# При ошибке возвращает ноль

    mapObjectSetSave_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetSave', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetSave(_hobjset: maptype.HOBJSET, _always: int) -> int:
        return mapObjectSetSave_t (_hobjset, _always)


# Восстановить объекты группы на карте после операций удаления или перемещения
# hobjset - идентификатор контекста набора объектов
# Использовать, если не вызывали mapObjectSetSave
# Возвращает число обработанных объектов
# При ошибке возвращает ноль

    mapObjectSetRevert_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetRevert', maptype.HOBJSET)
    def mapObjectSetRevert(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetRevert_t (_hobjset)


# Удалить объект из группы по его номеру в листе
# hobjset - идентификатор контекста набора объектов
# number - порядковый номер объекта в листе с 1
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен
# При ошибке возвращает ноль

    mapObjectSetRemoveNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetRemoveNumber', maptype.HOBJSET, ctypes.c_long, ctypes.c_long)
    def mapObjectSetRemoveNumber(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        return mapObjectSetRemoveNumber_t (_hobjset, _number, _save)


# Добавить главный объект группу (добавить признак в семантику GROUPLEADER)
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен
# Если объект hobj не записан в карту (Key = 0) и (save = 1), то сначала объект будет сохранен, а потом добавлен в группу
# Если объект hobj содержит семантику GROUPLEADER, то объект добавляется в набор, не изменяя групповую семантику
# Если объект hobj содержит семантику GROUPSLAVE или GROUPPARTNER, то в объект добавляется семантика GROUPLEADER:
# создается новая группа, без удаления старой группы (объект может принадлежать нескольким группам)
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendGeneral_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetAppendGeneral', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetAppendGeneral(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendGeneral_t (_hobjset, _hobj, _save)


# Добавить подчиненный объект в группу (добавить признак в семантику GROUPSLAVE)
# hobjset - идентификатор контекста набора объектов
# hobj - идентификатор объекта карты в памяти
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен
# Если объект hobj не записан в карту (Key = 0) и (save = 1), то сначала объект будет сохранен, а потом добавлен в группу
# Если объект hobj содержит семантику GROUPLEADER, то в объект добавляется семантика GROUPSLAVE:
# создается новая группа, без удаления старой группы (объект может принадлежать нескольким группам)
# Если объект hobj содержит семантику GROUPSLAVE или GROUPPARTNER, то объект добавляется в набор,
# с добавлением семантики GROUPSLAVE
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendSubordinate_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetAppendSubordinate', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetAppendSubordinate(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendSubordinate_t (_hobjset, _hobj, _save)


# Найти главный объект в группе
# hobjset - идентификатор контекста набора объектов
# group - номер группы (если group = 0 - номер группы устанавливается из набора hobjset)
# Возвращает идентификатор объекта карты из набора
# При ошибке возвращает ноль

    mapObjectSetFindGeneral_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapObjectSetFindGeneral', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetFindGeneral(_hobjset: maptype.HOBJSET, _group: int) -> maptype.HOBJ:
        return mapObjectSetFindGeneral_t (_hobjset, _group)


# Объединить два набора объектов
# hdestset - идентификатор контекста набора объектов, в который добавляется набор hobjset
# hobjset - идентификатор добавляемого контекста набора объектов
# mode - режим добавления:
#        1 - добавить отдельный объект (если объект главный - создать иерархию, включив только его в набор hdestset,
#            если объект подчиненный или равноправный - включить его в текущий набор, удалив из hobjset),
#        2 - набор hobjset и все объекты включаются в набор hdestset, набор hobjset удаляется,
#        3 - найти главный объект набора hobjset и включить его как подчиненный в набор hdestset, создав иерархию
# hobj - идентификатор объекта карты в памяти, которой определяет способ обработки
# Результат помещается в набор hdestset
# save - признак сохранения изменений в файл OBX: 1 - включен, 0 - отключен
# При ошибке возвращает ноль

    mapObjectSetUnion_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectSetUnion', maptype.HOBJSET, maptype.HOBJSET, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetUnion(_hdestset: maptype.HOBJSET, _hobjset: maptype.HOBJSET, _mode: int, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetUnion_t (_hdestset, _hobjset, _mode, _hobj, _save)


# Вычисление значения характеристики в заданной точке по данным векторной карты
# hmap - идентификатор открытых данных (документа)
# point - координаты точки (в метрах)
# semcode - код семантической характеристики
# value - поле для размещения результата запроса
# Поиск характеристики выполняется по всем объектам векторной карты
# При ошибке возвращает ноль

    mapCalcCharacteristic_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCalcCharacteristic', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapCalcCharacteristic(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _semcode: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapCalcCharacteristic_t (_hmap, _point, _semcode, _value)


# Открыть процесс чтения/записи макетов условий отбора
# name - имя открываемого файла макетов (VCL)
# mode - режим чтения/записи: GENERIC_READ, GENERIC_WRITE или 0
# GENERIC_READ - все данные только на чтение
# По окончании обработки необходимо вызвать mapModelFree
# При ошибке возвращает ноль

    mapOpenModelFileUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapOpenModelFileUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenModelFileUn(_name: mapsyst.WTEXT, _mode: int) -> ctypes.c_void_p:
        return mapOpenModelFileUn_t (_name.buffer(), _mode)


# Запросить количество моделей в файле макетов условий отбора
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# При ошибке возвращает ноль

    mapModelCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapModelCount', ctypes.c_void_p)
    def mapModelCount(_hvcl: ctypes.c_void_p) -> int:
        return mapModelCount_t (_hvcl)


# Добавить модель в конец файла макетов условий отбора
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# hselect - контекст условий отбора объектов, который сохраняется в файл моделей
# name - имя модели
# Возвращает номер записи в файле или 0 при ошибке

    mapAddModelUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAddModelUn', ctypes.c_void_p, maptype.HSELECT, maptype.PWCHAR)
    def mapAddModelUn(_hvcl: ctypes.c_void_p, _hselect: maptype.HSELECT, _name: mapsyst.WTEXT) -> int:
        return mapAddModelUn_t (_hvcl, _hselect, _name.buffer())


# Удалить модель c заданным номером
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# number - номер модели в файле макетов условий отбора
# При ошибке возвращает ноль

    mapDeleteModelByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteModelByNumber', ctypes.c_void_p, ctypes.c_long)
    def mapDeleteModelByNumber(_hvcl: ctypes.c_void_p, _number: int) -> int:
        return mapDeleteModelByNumber_t (_hvcl, _number)


# Удалить модель c заданным именем
# name - имя модели
# При ошибке возвращает ноль

    mapDeleteModelByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteModelByNameUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapDeleteModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        return mapDeleteModelByNameUn_t (_hvcl, _name.buffer())


# Запросить номер модели по имени модели
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# name - имя модели
# При ошибке возвращает ноль

    mapModelNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapModelNumberUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapModelNumberUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        return mapModelNumberUn_t (_hvcl, _name.buffer())


# Запросить модель по номеру модели
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# number - номер модели в файле макетов условий отбора
# hselect - контекст условий отбора объектов, в который считывается модель из файла
# При ошибке возвращает ноль

    mapGetModelByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetModelByNumber', ctypes.c_void_p, ctypes.c_long, maptype.HSELECT)
    def mapGetModelByNumber(_hvcl: ctypes.c_void_p, _number: int, _hselect: maptype.HSELECT) -> int:
        return mapGetModelByNumber_t (_hvcl, _number, _hselect)


# Запросить модель по имени модели
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# name - имя модели
# hselect - контекст условий отбора объектов, в который считывается модель из файла
# При ошибке возвращает ноль

    mapGetModelByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapGetModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT, _hselect: maptype.HSELECT) -> int:
        return mapGetModelByNameUn_t (_hvcl, _name.buffer(), _hselect)


# Запросить имя модели по номеру
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# number - номер модели в файле макетов условий отбора
# name - адрес строки для размещения имени модели
# namesize - размер буфера для записи имени модели
# При ошибке возвращает ноль

    mapModelNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapModelNameUn', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapModelNameUn(_hvcl: ctypes.c_void_p, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapModelNameUn_t (_hvcl, _number, _name.buffer(), _namesize)


# Обновить модель с заданным именем
# hvcl - идентификатор процесса чтения/записи макетов условий отбора
# name - имя модели
# hselect - контекст условий отбора объектов, который записывается в файл моделей
# При ошибке возвращает ноль

    mapUpdateModelByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapUpdateModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT, _hselect: maptype.HSELECT) -> int:
        return mapUpdateModelByNameUn_t (_hvcl, _name.buffer(), _hselect)


# Закрыть файл макетов условий отбора
# hvcl - идентификатор процесса чтения/записи макетов условий отбора

    mapModelFree_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapModelFree', ctypes.c_void_p)
    def mapModelFree(_hvcl: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapModelFree_t (_hvcl)


# Восстановить параметры поиска и выделения объектов по области
# hmap - идентификатор открытых данных (документа)
# name - имя восстанавливаемой модели условий поиска для всех карт
# mode - режим сохранения состояния отбора объектов:
#     1 - записывать в модель список уникальных номеров объектов,
#     0 - записывать в модель списки видов объектов (ключи или коды), слоев, локализаций
# Зарезервированные имена моделей условий:
# "MarkParameters" - имя модели параметров поиска по рамке
# "AreaParameters" - имя модели параметров поиска по области
# "PySeekParameters" - имя модели сохраненных параметров поиска при запуске отладчика
# В результате устанавливаются и включаются условия поиска и выделения объектов в документе - mapSetTotalSelectFlag(hmap, 1);
# При ошибке возвращает ноль

    mapRestoreTotalSeekSelectModelEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRestoreTotalSeekSelectModelEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapRestoreTotalSeekSelectModelEx(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        return mapRestoreTotalSeekSelectModelEx_t (_hmap, _name.buffer(), _mode)


# Сохранить параметры поиска и выделения объектов
# hmap - идентификатор открытых данных (документа)
# name - имя восстанавливаемой модели условий поиска для всех карт
# Зарезервированные имена моделей условий:
# "MarkParameters" - имя модели параметров поиска по рамке
# "AreaParameters" - имя модели параметров поиска по области
# "PySeekParameters" - имя модели сохраненных параметров поиска при запуске отладчика
# При ошибке возвращает ноль

    mapSaveTotalSeekSelectModel_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveTotalSeekSelectModel', maptype.HMAP, maptype.PWCHAR)
    def mapSaveTotalSeekSelectModel(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapSaveTotalSeekSelectModel_t (_hmap, _name.buffer())


# Создать контекст поиска пересечений объектов по спискам объектов
# hmap - идентификатор открытых данных (документа)
# setname1 - имя списка объектов 1 в файле OBX (для карт открытого документа)
# setname2 - имя списка объектов 2 в файле OBX (для карт открытого документа)
# Если setname1 = 0 или setname2 = 0, то списки объектов устанавливаются
# с помощью функций olsAppendSelectToList1 и olsAppendSelectToList2 (для каждой карты)
# По окончании обработки необходимо вызвать olsFree
# При ошибке возвращает ноль

    olsCreate_t = mapsyst.GetProcAddress(curLib,maptype.HOBJLISTSEEK,'olsCreate', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR)
    def olsCreate(_hmap: maptype.HMAP, _setname1: mapsyst.WTEXT, _setname2: mapsyst.WTEXT) -> maptype.HOBJLISTSEEK:
        return olsCreate_t (_hmap, _setname1.buffer(), _setname2.buffer())


# Освободить ресурсы, выделенные в olsCreate
# hols - идентификатор контекста поиска пересечений
# При ошибке возвращает ноль

    olsFree_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'olsFree', maptype.HOBJLISTSEEK)
    def olsFree(_hols: maptype.HOBJLISTSEEK) -> int:
        return olsFree_t (_hols)


# Добавить условия отбора объектов карты в список 1
# hols - идентификатор контекста поиска пересечений
# mapnumber - номер карты в открытых данных, от 0 до mapGetSiteCount(...)
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    olsAppendSelectToList1_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'olsAppendSelectToList1', maptype.HOBJLISTSEEK, ctypes.c_int, maptype.HSELECT)
    def olsAppendSelectToList1(_hols: maptype.HOBJLISTSEEK, _mapnumber: int, _hselect: maptype.HSELECT) -> int:
        return olsAppendSelectToList1_t (_hols, _mapnumber, _hselect)


# Добавить условия отбора объектов карты в список 2
# hols - идентификатор контекста поиска пересечений
# mapnumber - номер карты в открытых данных, от 0 до mapGetSiteCount(...)
# hselect - контекст условий отбора объектов
# При ошибке возвращает ноль

    olsAppendSelectToList2_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'olsAppendSelectToList2', maptype.HOBJLISTSEEK, ctypes.c_int, maptype.HSELECT)
    def olsAppendSelectToList2(_hols: maptype.HOBJLISTSEEK, _mapnumber: int, _hselect: maptype.HSELECT) -> int:
        return olsAppendSelectToList2_t (_hols, _mapnumber, _hselect)


# Выполнить поиск по спискам объектов карты
# hols - идентификатор контекста поиска пересечений
# parm - параметры поиска
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных
# callparm - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы,
#            вторым параметром в вызываемой функции передается процент от 0 до 100)
# Возвращает количество найденных объектов
# При ошибке возвращает ноль

    olsRunSeekEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'olsRunSeekEx', maptype.HOBJLISTSEEK, ctypes.POINTER(maptype.SEEKDIALOGPARM), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def olsRunSeekEx(_hols: maptype.HOBJLISTSEEK, _parm: ctypes.POINTER(maptype.SEEKDIALOGPARM), _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return olsRunSeekEx_t (_hols, _parm, _callevent, _callparm)


# Запросить контекст условий отобранных объектов по номеру карты
# hols - идентификатор контекста поиска пересечений
# mapnumber - номер карты в открытых данных, от 0 до mapGetSiteCount(...)
# При ошибке возвращает ноль

    olsGetResultSelect_t = mapsyst.GetProcAddress(curLib,maptype.HSELECT,'olsGetResultSelect', maptype.HOBJLISTSEEK, ctypes.c_int)
    def olsGetResultSelect(_hols: maptype.HOBJLISTSEEK, _mapnumber: int) -> maptype.HSELECT:
        return olsGetResultSelect_t (_hols, _mapnumber)

except Exception as e:
    print(e)
    curLib = 0

def seekapi_healthcheck(): 
    return 1