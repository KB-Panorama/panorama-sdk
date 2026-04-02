#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype

PACK_WIDTH = 1

#-----------------------------
class TEMPHOBJSET(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hobjset",maptype.HOBJSET)]
    def __init__(self, value : maptype.HOBJSET = 0):
        super().__init__()
        self.hobjset = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hobjset != 0:
            mapFreeObjectSet(self.hMap)
        self.hobjset = 0
    def HOBJSET(self):
        return self.hobjset
    def __eq__(self, other):
        return self.hobjset == other.hobjset
    def __ne__(self, other):
        return self.hobjset != other.hobjset
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)

# Флажки, определяющие ПОРЯДОК ПОИСКА ОБЪЕКТОВ:
# Первый в цепочке,последний,следующий за найденым ранее,
# предыдущий, вместе c удаленными, только в заданной карте
# Если указано WO_INMAP - номер карты определяется
# из HSELECT !
# Поиск начинается с флажков WO_FIRST или WO_LAST (если нет
# объекта с которого начинается поиск), затем применяются
# флажки WO_NEXT или WO_BACK (например, в цикле)
# enum SEEKTYPE             # ПОРЯДОК ПОИСКА ОБЪЕКТОВ
# {
#    WO_FIRST  = 0,         # Первый в цепочке
#    WO_LAST   = 2,         # Последний в цепочке
#    WO_NEXT   = 4,         # Следующий за найденным ранее
#    WO_BACK   = 8,         # Предыдущий от ранее найденного
#    WO_CANCEL = 16,        # Включая удаленные объекты
#    WO_INMAP  = 32,        # Только по одной карте (соответствующей HSELECT)
#    WO_VISUAL = 64,        # Поиск только среди видимых объектов
#    WO_VISUALIGNORE = 128, # Поиск среди всех объектов без учета видимости
# };
# Выбор видимых объектов в окрестности точки, заданной прямоугольной рамкой
# Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
# Не является функцией поиска объектов по области (см. mapSelectSeekAreaFrame и т.п.)
# hMap - идентификатор открытой карты.
# info - идентификатор объекта в памяти,
#        предварительно созданного функцией mapCreateObject()
#        или mapCreateSiteObject(),
#        в котором будет размещен результат поиска.
# frame - прямоугольная область поиска объекта в системе координат,
#         заданной переменной place (PP_PLANE,PP_GEO, ...)
# Координаты области пересчитываются в пикселы в текущем масштабе
# отображения. В список выбранных могут попасть объекты, которые
# отображаются в текущем масштабе рядом с областью выбора в
# пределах нескольких пикселов.
# Площадные объекты выбираются в пределах рамки
# размером 512х512 пикселов в текущем масштабе изображения
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# Выбор объекта в "точке" лучше начинать с последнего, то
# есть того, что нарисован поверх остальных (это чуть медленнее
# прямого поиска)
# При поиске с флажками WO_NEXT,WO_BACK параметр info должен
# содержать результат предыдущего поиска.
# Поиск выполнется среди тех объектов,которые видны на экране,
# если не установлен флаг WO_VISUALIGNORE
# place - система координат
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения,
# создается функцией mapCreatePaintControl
# Если объект не найден - возвращает ноль,
# иначе - возвращает значение info !

    mapWhatObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int)
    def mapWhatObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _place: int) -> maptype.HOBJ:
        return mapWhatObject_t (_hMap, _info, _frame, _flag, _place)

    mapWhatObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObjectEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, maptype.HPAINT)
    def mapWhatObjectEx(_hMap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _place: int, _hPaint: maptype.HPAINT) -> maptype.HOBJ:
        return mapWhatObjectEx_t (_hMap, _info, _frame, _flag, _place, _hPaint)


# Выбор видимых объектов в окрестности точки, заданной прямоугольной рамкой, среди активных объектов
# Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
# Не является функцией поиска объектов по области (см. mapSelectSeekAreaFrame и т.п.)
# Активные объекты - те, что доступны для интерактивного выбора (оператором)
# Установка условий поиска выполняется функцией mapSetSiteActiveSelect()
# hMap  - идентификатор открытой карты,
# info  - идентификатор объекта в памяти,
#         предварительно созданного функцией mapCreateObject()
#         или mapCreateSiteObject(),
#         в котором будет размещен результат поиска.
# frame - прямоугольная область поиска объекта в системе координат,
#         заданной переменной place (PP_PLANE,PP_GEO, ...)
# flag  - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# place - система координат
# Если объект не найден - возвращает ноль

    mapWhatActiveObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhatActiveObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int)
    def mapWhatActiveObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int = maptype.WO_LAST, _place: int = maptype.PP_PICTURE) -> int:
        return mapWhatActiveObject_t (_hMap, _info, _frame, _flag, _place)


# Установить порядок выбора подписей
# hMap  - идентификатор открытой карты
# place - порядок выбора подписи,
# если равен нулю, то при переборе в обратном порядке (WO_LAST,
# WO_PREV) сначала будут идти подписи,
# если не равен нулю, то при прямом выборе (WO_FIRST, WO_NEXT)
# подписи будут первыми
# По-умолчанию подписи в точке выбираются последними (для WO_LAST),
# т.е. place = 1

    mapSetTextPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTextPlace', maptype.HMAP, ctypes.c_int)
    def mapSetTextPlace(_hMap: maptype.HMAP, _place: int) -> ctypes.c_void_p:
        return mapSetTextPlace_t (_hMap, _place)

    mapGetTextPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextPlace', maptype.HMAP)
    def mapGetTextPlace(_hMap: maptype.HMAP) -> int:
        return mapGetTextPlace_t (_hMap)


# Выбор видимых объектов в окрестности точки, заданной прямоугольной рамкой,
# удовлетворяющих условиям поиска
# Не является функцией поиска объектов по области (см. mapSelectSeekAreaFrame и т.п.)
# Выбор выполнется среди тех объектов,которые соответствуют условиям, заданным в HSELECT
# hMap - идентификатор открытой карты.
# info - идентификатор объекта в памяти,
#        предварительно созданного функцией mapCreateObject()
#        или mapCreateSiteObject(),
#        в котором будет размещен результат поиска.
# frame - прямоугольная область поиска объекта в системе координат,
#         заданной переменной place (PP_PLANE,PP_GEO, ...)
# select- контекст условий выбора объектов,
# flag  - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# Выбор объекта в "точке" лучше начинать с последнего, то
# есть того, что нарисован поверх остальных (это чуть медленнее
# прямого поиска). При поиске с флажками WO_NEXT,WO_BACK параметр
# info должен содержать результат предыдущего поиска.
# place - система координат,
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения,
# создается функцией mapCreatePaintControl
# Если объект не найден - возвращает ноль,
# иначе - возвращает значение info !

    mapWhatObjectBySelect_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObjectBySelect', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapWhatObjectBySelect(_hMap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _select: maptype.HSELECT, _flag: int, _place: int) -> maptype.HOBJ:
        return mapWhatObjectBySelect_t (_hMap, _info, _frame, _select, _flag, _place)

    mapWhatObjectBySelectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObjectBySelectEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.HPAINT)
    def mapWhatObjectBySelectEx(_hMap: maptype.HMAP, _info: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _select: maptype.HSELECT, _flag: int, _place: int, _hPaint: maptype.HPAINT) -> maptype.HOBJ:
        return mapWhatObjectBySelectEx_t (_hMap, _info, _frame, _select, _flag, _place, _hPaint)


# Поиск объекта по номенклатуре и номеру объекта среди всех карт
# hMap - идентификатор открытой карты
# info - идентификатор объекта в памяти,
#        предварительно созданного функцией mapCreateObject()
#        или mapCreateSiteObject(),
#        в котором будет размещен результат поиска
# listname - название (номенклатура) листа,
# key      - идентификатор объекта в листе,
# При ошибке возвращает ноль

    mapSeekObjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekObjectUn', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapSeekObjectUn(_hMap: maptype.HMAP, _info: maptype.HOBJ, _listname: mapsyst.WTEXT, _key: int) -> maptype.HOBJ:
        return mapSeekObjectUn_t (_hMap, _info, _listname.buffer(), _key)

    mapSeekObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekObject', maptype.HMAP, maptype.HOBJ, ctypes.c_char_p, ctypes.c_int)
    def mapSeekObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _listname: ctypes.c_char_p, _key: int) -> maptype.HOBJ:
        return mapSeekObject_t (_hMap, _info, _listname, _key)

    mapSeekObjectInList_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekObjectInList', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSeekObjectInList(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _key: int) -> maptype.HOBJ:
        return mapSeekObjectInList_t (_hMap, _hSite, _info, _list, _key)


# Поиск номера объекта по номенклатуре и номеру объекта
# среди всех карт (в отличие от поиска объекта возвращает номер объекта
# и для удаленных объектов, пока не было сортировки карты)
# hMap     - идентификатор открытой карты,
# listname - название (номенклатура) листа,
# key      - идентификатор объекта в листе
# При ошибке возвращает ноль

    mapSeekObjectNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekObjectNumberUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapSeekObjectNumberUn(_hMap: maptype.HMAP, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapSeekObjectNumberUn_t (_hMap, _listname.buffer(), _key)

    mapSeekObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekObjectNumber', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapSeekObjectNumber(_hMap: maptype.HMAP, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapSeekObjectNumber_t (_hMap, _listname, _key)

    mapSeekObjectNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekObjectNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSeekObjectNumberEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _key: int) -> int:
        return mapSeekObjectNumberEx_t (_hMap, _hSite, _list, _key)


# Поиск объектов по GUID в листе (значение семантики OBJECTGUID 32799)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# info - идентификатор объекта в памяти,
#        предварительно созданного функцией mapCreateObject()
#        или mapCreateSiteObject(),
#        в котором будет размещен результат поиска
# list  - номер листа карты с 1 до числа листов
# guid  - структура, содержащая значение GUID в двоичной форме
# При успешном выполнении возвращает номер объекта в листе
# При ошибке возвращает ноль

    mapSeekObjectByGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekObjectByGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.INT64TWO))
    def mapSeekObjectByGUID(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _guid: ctypes.POINTER(maptype.INT64TWO)) -> int:
        return mapSeekObjectByGUID_t (_hMap, _hSite, _info, _list, _guid)


# Поиск объектов по GUID в листе (значение семантики OBJECTGUID 32799)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# info - идентификатор объекта в памяти,
#        предварительно созданного функцией mapCreateObject()
#        или mapCreateSiteObject(),
#        в котором будет размещен результат поиска
# list  - номер листа карты с 1 до числа листов
# guid  - строка, содержащая значение GUID (32 или 36 символов, если с тире)
# При успешном выполнении возвращает номер объекта в листе
# При ошибке возвращает ноль

    mapSeekObjectByStringGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekObjectByStringGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_char_p)
    def mapSeekObjectByStringGUID(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _guid: ctypes.c_char_p) -> int:
        return mapSeekObjectByStringGUID_t (_hMap, _hSite, _info, _list, _guid)


# Поиск объектов по заданным условиям среди всех объектов
# hMap     - идентификатор открытой карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска.
# select   - условия поиска объекта
# flag     - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# При поиске с флажками WO_NEXT,WO_BACK параметр info должен
# содержать результат предыдущего поиска
# Если объект не найден - возвращает ноль

    mapSeekSelectObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSelectObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_int)
    def mapSeekSelectObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _select: maptype.HSELECT, _flag: int = maptype.WO_FIRST) -> int:
        return mapSeekSelectObject_t (_hMap, _info, _select, _flag)


# Запрос числа объектов на карте, удовлетворяющих условиям поиска
# Подсчет выполняется на той карте, для которой был создан контекст поиска!
# select - условия поиска объекта
# При ошибке возвращает ноль

    mapSeekSelectObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSelectObjectCount', maptype.HMAP, maptype.HSELECT)
    def mapSeekSelectObjectCount(_hMap: maptype.HMAP, _select: maptype.HSELECT) -> int:
        return mapSeekSelectObjectCount_t (_hMap, _select)


# Запрос числа объектов на карте, удовлетворяющих условиям поиска
# Подсчет выполняется на той карте, для которой был создан контекст поиска!
# select - условия поиска объекта
# flag   - флаг условий поиска (VO_INMAP - поиск на той карте, для которой
#          был создан контекст поиска, иначе - поиск по всем картам)
# При ошибке возвращает ноль

    mapSeekSelectObjectCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSelectObjectCountEx', maptype.HMAP, maptype.HSELECT, ctypes.c_int)
    def mapSeekSelectObjectCountEx(_hMap: maptype.HMAP, _select: maptype.HSELECT, _flag: int) -> int:
        return mapSeekSelectObjectCountEx_t (_hMap, _select, _flag)


# Поиск ближайшего объекта по заданным условиям среди всех объектов
# hMap     - идентификатор открытой карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска;
# pointin  - координаты точки, относительно которой выполняется поиск;
# pointout - координаты ближайшей виртуальной точки на контуре объекта
#            в метрах документа;
# select   - условия поиска объекта;
# flag     - дополнительные условия поиска объектов: WO_CANCEL,
#            WO_INMAP, WO_VISUAL; флажки типа WO_FIRST, WO_NEXT не учитываются.
# Если flag равен 0, выполняется поиск по всем картам среди всех объектов
# Если объект не найден - возвращает ноль

    mapSeekSelectNearestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSelectNearestObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_int)
    def mapSeekSelectNearestObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT), _select: maptype.HSELECT, _flag: int = maptype.WO_INMAP|maptype.WO_VISUAL) -> int:
        return mapSeekSelectNearestObject_t (_hMap, _info, _pointin, _pointout, _select, _flag)


# Поиск объектов по заданным условиям среди отображаемых объектов
# (пересечение заданных условий с условиями отображения)
# hMap     - идентификатор открытой карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска.
# select   - условия поиска объекта
# flag     - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# Если объект не найден - возвращает ноль

    mapSeekViewObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekViewObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_int)
    def mapSeekViewObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _select: maptype.HSELECT, _flag: int = maptype.WO_FIRST) -> maptype.HOBJ:
        return mapSeekViewObject_t (_hMap, _info, _select, _flag)


#  Поиск объекта, имеющего смежный участок с заданным объектом
#  Поиск ведется в карте, где находится выбранный объект
#  hMap     - идентификатор открытой карты,
#  info     - идентификатор существующего объекта,
#             для которого надо найти смежные участки
#  target   - указатель на существующий объект TObjectInfo,
#             в котором будет размещен результат поиска.
#  При поиске с флажками WO_NEXT,WO_BACK параметр target должен
#  указывать на результат предыдущего поиска.
#  select   - условия поиска объекта (данная функция в select устанавливает
#             область поиска для info, поэтому после выполнения функции select изменяется!
#             При использовании функции с флажками WO_NEXT,WO_BACK не требуется
#             сохранение или переустановка условий поиска.
#             Если select используется далее в программе, то перед вызовом данной
#             функции нужно сделать его копию.)
#  delta    - допуск до объекта в метрах (может равняться 0)
#             в структуре MAPADJACENTSECTION поле number
#             для начального поиска должно быть равным 0.
#  flag     - порядок поиска объектов (WO_FIRST, WO_NEXT...)
#  При поиске с флажками WO_NEXT,WO_BACK параметр info должен
#  содержать результат предыдущего поиска.
#  Если объект не найден - возвращает ноль,
#  иначе - возвращает номер участка и заполненную структуру MAPADJACENTSECTION
#  (см. MAPTYPE.H)
#  subject = 0 искать соседей только с внешним контуром
# ( 1- с учетом подобъектов, нумерация точек объекта и подобъектов - сквозная)
#  Если объект не найден - возвращает ноль

    mapSeekAdjacentObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekAdjacentObject', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTSECTION), maptype.HSELECT, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSeekAdjacentObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _target: maptype.HOBJ, _section: ctypes.POINTER(maptype.MAPADJACENTSECTION), _select: maptype.HSELECT, _delta: float = 0.0, _flag: int = maptype.WO_FIRST | maptype.WO_INMAP, _subject: int = 0) -> int:
        return mapSeekAdjacentObject_t (_hMap, _info, _target, _section, _select, _delta, _flag, _subject)


#  Поиск объектов, имеющих смежный участок с заданным объектом
#  Поиск ведется в карте, где находится выбранный объект
#  hMap  - идентификатор открытой карты,
#  info  - идентификатор существующего объекта,
#          для которого надо найти смежные участки
#  MAPADJACENTLISTEX - память для соседей
#  count - максимальное количество смежных участков
#  select - условия поиска объектов для списка
#  delta - допуск до объекта в метрах
#  point - обработка сторон,образуемых повторяющимися точками:
#  0 - заносить в список, 1 - нет
#  subject - 0 искать соседей только с внешним контуром
# ( 1- с учетом подобъектов, нумерация точек объекта и подобъектов - сквозная)
#  Если соседи не найдены - возвращает ноль,
#  иначе - количество соседей

    mapSeekAdjacentListEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekAdjacentListEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTLISTEX), ctypes.c_int, maptype.HSELECT, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSeekAdjacentListEx(_hMap: maptype.HMAP, _info: maptype.HOBJ, _list: ctypes.POINTER(maptype.MAPADJACENTLISTEX), _count: int, _select: maptype.HSELECT, _delta: float = 0.0, _point: int = 0, _subject: int = 0) -> int:
        return mapSeekAdjacentListEx_t (_hMap, _info, _list, _count, _select, _delta, _point, _subject)


# Создание класса поиска смежного участка для заданного подобъекта
# map       - карта на которой выполняется поиск
# select    - условия поиска
# obj       - объект для которого ищутся соседи
# subject   - номер подобъекта для которого ищутся соседи
# nearobj   - объект в который будет помещен найденный сосед
# precision - точность поиска в метрах на местности
# Возвращает идентификатор поиска
# При ошибке возвращает 0

    mapCreateSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateSeekConnectPath', maptype.HMAP, maptype.HSELECT, maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_double)
    def mapCreateSeekConnectPath(_map: maptype.HMAP, _select: maptype.HSELECT, _obj: maptype.HOBJ, _subject: int, _nearobj: maptype.HOBJ, _precision: float = maptype.DELTANULL) -> ctypes.c_void_p:
        return mapCreateSeekConnectPath_t (_map, _select, _obj, _subject, _nearobj, _precision)


# Освобождение класса поиска смежного участка для заданного подобъекта
# seekconnect - класс поиска

    mapFreeSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSeekConnectPath', ctypes.c_void_p)
    def mapFreeSeekConnectPath(_seekconnect: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSeekConnectPath_t (_seekconnect)


# Поиск следующего смежного участка для заданного подобъекта
# Возможен возврат участка из одной точки (касание в одной точке)
# Для замкнутых объектов участок может проходить через первую (последнюю) точку
# Направление участка на соседнем объекте всегда совпадает с направлением
# цифрования, а направление на главном объекте устанавливается в path.IsForward
# seekconnect - идентификатор класса поиска смежного участка
# path        - найденный путь
# При ошибке или если смежный участок не найден возвращает ноль

    mapSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekConnectPath', ctypes.c_void_p, ctypes.POINTER(maptype.CONNECTPATH))
    def mapSeekConnectPath(_seekconnect: ctypes.c_void_p, _path: ctypes.POINTER(maptype.CONNECTPATH)) -> int:
        return mapSeekConnectPath_t (_seekconnect, _path)


# Проверить - подходит ли объект под условия поиска/отображения
# Если подходит возвращает ненулевое значение
# Если условия поиска не заданы (select = 0), возвращает 1
# info   - идентификатор существующего объекта,
# select - условия поиска/отображения
# При ошибке возвращает ноль

    mapTestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTestObject', maptype.HOBJ, maptype.HSELECT)
    def mapTestObject(_info: maptype.HOBJ, _select: maptype.HSELECT) -> int:
        return mapTestObject_t (_info, _select)


# Проверить - подходит ли объект под условия поиска/выделения
# заданные на карте
# Если подходит возвращает ненулевое значение
# hMap - идентификатор открытой карты,
# info - идентификатор существующего объекта,
# При ошибке возвращает ноль

    mapTotalTestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTotalTestObject', maptype.HMAP, maptype.HOBJ)
    def mapTotalTestObject(_hMap: maptype.HMAP, _info: maptype.HOBJ) -> int:
        return mapTotalTestObject_t (_hMap, _info)


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

    mapReadObjectByNumber_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapReadObjectByNumber', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapReadObjectByNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _object: int) -> maptype.HOBJ:
        return mapReadObjectByNumber_t (_hMap, _hSite, _info, _list, _object)


# Если объект имеет признак "удален", то функция возвращает 1
# При успешном выполнении возвращает значение 2
# При ошибке возвращает ноль

    mapReadObjectByNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadObjectByNumberEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapReadObjectByNumberEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _object: int) -> int:
        return mapReadObjectByNumberEx_t (_hMap, _hSite, _info, _list, _object)


# Выбор объекта по номеру листа и уникальному номеру объекта
# При успешном выполнении возвращает значение info
# hMap     - идентификатор открытой карты,
# hSite    - идентификатор открытой пользовательской карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска;
# list     - номер листа (для пользовательской карты всегда 1);
# key      - уникальный номер объекта.
# Если объект имеет признак "удален" - возвращает 1 !
# При ошибке возвращает ноль, иначе - значение info

    mapReadObjectByKey_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapReadObjectByKey', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapReadObjectByKey(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _key: int) -> maptype.HOBJ:
        return mapReadObjectByKey_t (_hMap, _hSite, _info, _list, _key)


# Если объект имеет признак "удален", то функция возвращает 1
# При успешном выполнении возвращает значение 2
# При ошибке возвращает ноль

    mapReadObjectByKeyEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadObjectByKeyEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapReadObjectByKeyEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _list: int, _key: int) -> int:
        return mapReadObjectByKeyEx_t (_hMap, _hSite, _info, _list, _key)


# Запросить правило обобщенного поиска по картам
# hMap - идентификатор открытой карты,
# если результат = -1, поиск будет выполняться по всем картам
# (0 - карта местности, 1...n - пользовательские карты)
# При ошибке возвращает число (-2)

    mapGetTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalSeekMapRule', maptype.HMAP)
    def mapGetTotalSeekMapRule(_hMap: maptype.HMAP) -> int:
        return mapGetTotalSeekMapRule_t (_hMap)


# Запросить имеются ли на основной или пользовательской карте объекты,
# удовлетворяющие заданным условиям поиска
# hMap   - идентификатор открытой карты,
# number - номер карты
# (0 - карта местности, 1...n - пользовательские карты)
# Если на карте есть подходящие объекты - возвращает ненулевое значение

    mapIsTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTotalSeekMapRule', maptype.HMAP, ctypes.c_int)
    def mapIsTotalSeekMapRule(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsTotalSeekMapRule_t (_hMap, _number)


# Установить правило обобщенного поиска по картам
# hMap     - идентификатор открытой карты,
# number   - номер карты, по которой выполняется поиск,
# если number == -1, поиск будет выполняться по всем картам
# (0 - карта местности, 1...n - пользовательские карты)

    mapSetTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSeekMapRule', maptype.HMAP, ctypes.c_int)
    def mapSetTotalSeekMapRule(_hMap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        return mapSetTotalSeekMapRule_t (_hMap, _number)


# Установить правило обобщенного поиска для
# отображаемых объектов карты
# hMap - идентификатор открытой карты,
# Если view == 0, поиск выполняется среди всех объектов
# карты, иначе - среди отображаемых (SeekViewObject())

    mapSetTotalSeekViewRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSeekViewRule', maptype.HMAP, ctypes.c_int)
    def mapSetTotalSeekViewRule(_hMap: maptype.HMAP, _view: int = 0) -> ctypes.c_void_p:
        return mapSetTotalSeekViewRule_t (_hMap, _view)

    mapGetTotalSeekViewRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalSeekViewRule', maptype.HMAP)
    def mapGetTotalSeekViewRule(_hMap: maptype.HMAP) -> int:
        return mapGetTotalSeekViewRule_t (_hMap)


# Установить условия поиска/выделения объектов по имени листа
# и номеру объекта в карте
# hMap     - идентификатор открытой карты,
# listname - имя листа карты (карта выбирается автоматически)
# key      - уникальный номер объекта в карте (BaseKey)
# Если для карты установлены условия поиска по номерам объектов,
# то остальные условия (слой,локализация...) игнорируются.
# Если карта не найдена - возвращает ноль

    mapSetTotalSeekSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTotalSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapSetTotalSeekSampleUn(_hMap: maptype.HMAP, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapSetTotalSeekSampleUn_t (_hMap, _listname.buffer(), _key)

    mapSetTotalSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTotalSeekSample', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapSetTotalSeekSample(_hMap: maptype.HMAP, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapSetTotalSeekSample_t (_hMap, _listname, _key)


# Установить условия поиска/выделения объектов по всем картам
# (пользовательским и карте местности)
# hMap     - идентификатор открытой карты,
# acceess  - признак отбора объектов :
# =  0 - отключить отбор всех объектов всех карт (отключает все локализации и чистит списки),
# != 0 - все объекты доступны при поиске в mapTotalSeekObject().
# (Альтернатива перебору условий поиска для всех карт;
#  перед применением mapSetTotalSeekSample доступ может быть отключен)
# При ошибке возвращает ноль

    mapSetTotalSeekAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTotalSeekAccess', maptype.HMAP, ctypes.c_int)
    def mapSetTotalSeekAccess(_hMap: maptype.HMAP, _access: int) -> int:
        return mapSetTotalSeekAccess_t (_hMap, _access)


# Выделить на карте объекты, удовлетворяющие условиям
# обобщенного поиска
# hMap     - идентификатор открытой карты,
# hDC      - контекст устройства отображения,
# rect     - координаты фрагмента карты (Draw) в изображении (Picture)
# color    - цвет, которым будут выделяться объекты на карте
# Требует перед вызовом установки
#              ::SetViewportOrgEx(hDC, dx , dy, 0),
# где dx,dy - положение отображаемого фрагмента в клиентной
# области !
# При ошибке возвращает ноль

    mapTotalPaintSelect95_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTotalPaintSelect95', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.COLORREF)
    def mapTotalPaintSelect95(_hMap: maptype.HMAP, _hDC: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _color: maptype.COLORREF) -> int:
        return mapTotalPaintSelect95_t (_hMap, _hDC, _rect, _color)


# Выделить на карте объекты, удовлетворяющие условиям
# обобщенного поиска
# hMap   - идентификатор открытых данных
# hwnd   - идентификатор окна вывода
# color  - цвет, которым будут выделяться объекты на карте,
# point - координаты верхнего левого угла окна на карте
# в соответсвующей параметру place системе координат
# При ошибке возвращает ноль

    mapTotalViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTotalViewSelect', maptype.HMAP, maptype.HWND, ctypes.POINTER(maptype.DOUBLEPOINT), maptype.COLORREF, ctypes.c_int)
    def mapTotalViewSelect(_hMap: maptype.HMAP, _hwnd: maptype.HWND, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _color: maptype.COLORREF, _place: int) -> int:
        return mapTotalViewSelect_t (_hMap, _hwnd, _point, _color, _place)


# Запросить - есть ли объекты, удовлетворяющие условиям поиска
# hMap  - идентификатор открытых данных
# При ошибке возвращает ноль

    mapIsTotalSeekObjectNotEmpty_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTotalSeekObjectNotEmpty', maptype.HMAP)
    def mapIsTotalSeekObjectNotEmpty(_hMap: maptype.HMAP) -> int:
        return mapIsTotalSeekObjectNotEmpty_t (_hMap)


# Запросить - есть ли объекты, удовлетворяющие условиям поиска
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты, для которой выполняется проверка
# При ошибке возвращает ноль

    mapIsTotalSeekSiteObjectNotEmpty_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTotalSeekSiteObjectNotEmpty', maptype.HMAP, maptype.HSITE)
    def mapIsTotalSeekSiteObjectNotEmpty(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsTotalSeekSiteObjectNotEmpty_t (_hMap, _hSite)


# Подсчитать сколько объектов удовлетворяет условиям
# обобщенного поиска
# hMap  - идентификатор открытых данных
# При ошибке возвращает ноль

    mapTotalSeekObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTotalSeekObjectCount', maptype.HMAP)
    def mapTotalSeekObjectCount(_hMap: maptype.HMAP) -> int:
        return mapTotalSeekObjectCount_t (_hMap)


# Обобщенный поиск объектов по заданным условиям
# Условия обобщенного поиска вводятся заранее
# (используются функции mapGetSiteViewSelect(),mapGetSiteSeekSelect()...)
# hMap  - идентификатор открытых данных
# info - указатель на существующий объект TObjectInfo
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# При поиске с флажками WO_NEXT,WO_BACK параметр info должен
# указывать на результат предыдущего поиска
# Если объект не найден - возвращает ноль

    mapTotalSeekObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapTotalSeekObject', maptype.HMAP, maptype.HOBJ, ctypes.c_int)
    def mapTotalSeekObject(_hMap: maptype.HMAP, _info: maptype.HOBJ, _flag: int) -> maptype.HOBJ:
        return mapTotalSeekObject_t (_hMap, _info, _flag)


# Обобщенный поиск объектов по заданным условиям
# hMap  - идентификатор открытых данных
# info - указатель на существующий объект TObjectInfo
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT, WO_BACK, ...)
# При поиске с флажками WO_NEXT, WO_BACK параметры map, list, object должны быть заданы
# map  - номер карты в открытых данных (с 0)
# list - номер листа карты (с 1)
# object - номер объекта (с 1), с которого будет продолжен поиск
# (за ним или перед ним - в зависимости от параметра flag)
# Если объект не найден - возвращает ноль

    mapTotalSeekObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapTotalSeekObjectEx', maptype.HMAP, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapTotalSeekObjectEx(_hMap: maptype.HMAP, _info: maptype.HOBJ, _flag: int, _map: int, _list: int, _object: int) -> maptype.HOBJ:
        return mapTotalSeekObjectEx_t (_hMap, _info, _flag, _map, _list, _object)


# Установить признак выделения объектов по обобщенным
# условиям поиска
# hMap   - идентификатор открытых данных
# flag = 0 - отключить выделение объектов на карте,
# иначе - выделять объекты по условиям поиска при перерисовке
# Никакого действия кроме сохранения значения не производит
# Применяется для связи между различными модулями

    mapSetTotalSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSelectFlag', maptype.HMAP, ctypes.c_int)
    def mapSetTotalSelectFlag(_hMap: maptype.HMAP, _flag: int) -> ctypes.c_void_p:
        return mapSetTotalSelectFlag_t (_hMap, _flag)


# Запросить признак выделения объектов по обобщенным
# условиям поиска
# hMap   - идентификатор открытых данных
# Если результат равен нулю, выделение объектов не выполняется

    mapGetTotalSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalSelectFlag', maptype.HMAP)
    def mapGetTotalSelectFlag(_hMap: maptype.HMAP) -> int:
        return mapGetTotalSelectFlag_t (_hMap)


# Определить общие габариты объектов, соответствующие заданным
# условиям
# Габариты рассчитываются в метрах
# hMap   - идентификатор открытых данных
# border - координаты габаритов прямоугольного участка, включающего все объекты,
#          удовлетворяющие заданным условиям
# При ошибке возвращает ноль

    mapGetTotalSeekBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalSeekBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapGetTotalSeekBorder(_hMap: maptype.HMAP, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetTotalSeekBorder_t (_hMap, _border)


# Опросить наличие списка объектов в контексте условий поиска/отображения хотя бы одной карты
# Список объектов содержит номер листа и номер объекта
# в листе
# hMap   - идентификатор открытых данных
# Если список объектов не установлен, возвращает ноль

    mapIsTotalSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTotalSeekSample', maptype.HMAP)
    def mapIsTotalSeekSample(_hMap: maptype.HMAP) -> int:
        return mapIsTotalSeekSample_t (_hMap)


# Инвертировать выделение объектов
# hMap   - идентификатор открытых данных
# При ошибке возвращает ноль

    mapInversionTotalSeek_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInversionTotalSeek', maptype.HMAP)
    def mapInversionTotalSeek(_hMap: maptype.HMAP) -> int:
        return mapInversionTotalSeek_t (_hMap)


# Определить общие габариты объектов, соответствующие заданным
# условиям на карте
# hMap   - идентификатор открытой карты,
# hSite  - идентификатор открытой пользовательской карты,
# list   - номер листа для многолистовой карты или 0
# border - координаты габаритов прямоугольного участка, включающего все объекты,
#          удовлетворяющие заданным условиям
# place  - система координат запрошенных габаритов (PP_PLANE, PP_GEO, PP_PICTURE)
# При ошибке возвращает ноль

    mapGetSiteSeekBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteSeekBorder', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetSiteSeekBorder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _hSelect: maptype.HSELECT, _border: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetSiteSeekBorder_t (_hMap, _hSite, _list, _hSelect, _border, _place)


# Создать контекст (описание условий) поиска/отображения
# объектов карты
# hMap   - идентификатор открытой карты,
# hRsc   - идентификатор открытого классификатора карты
# В состав условий отбора объектов входят : лист, слой,
# локализация, диапазон номеров объектов, характеристики
# (семантика) объекта, область расположения (метрика) объекта
# В созданном контексте доступны все объекты карты без исключений
# Запрашивается минимум 10 Кб памти,
# если заданы условия поиска по метрике и семантике - до 300 Кб
# Каждый созданный контекст должен быть удален (mapDeleteSelectContext),
# когда он больше не используется. Рекомендуется удалять контекст
# условий поиска до закрытия карты (классификатора) с которыми
# он был создан
# При ошибке возвращает ноль

    mapCreateMapSelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateMapSelectContext', maptype.HMAP)
    def mapCreateMapSelectContext(_hmap: maptype.HMAP) -> maptype.HSELECT:
        return mapCreateMapSelectContext_t (_hmap)

    mapCreateRscSelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateRscSelectContext', maptype.HRSC)
    def mapCreateRscSelectContext(_hrsc: maptype.HRSC) -> maptype.HSELECT:
        return mapCreateRscSelectContext_t (_hrsc)


# Создать копию контекста (описания условий) поиска/отображения
# объектов карты
# select - исходный контекст (описание условий) поиска/отображения.
# Каждый созданный контекст должен быть удален, когда
# он больше не используется
# При ошибке возвращает ноль

    mapCreateCopySelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateCopySelectContext', maptype.HSELECT)
    def mapCreateCopySelectContext(_select: maptype.HSELECT) -> maptype.HSELECT:
        return mapCreateCopySelectContext_t (_select)


# Копировать контекст (описание условий) поиска/отображения
# в существующий контекст поиска/отображения
# target - контекст условий поиска, куда выполняется копирование;
# source - копируемый контекст поиска (источник).
# (Каждый созданный контекст должен быть удален, когда
# он больше не используется)
# При копировании контекста выполняется также смена карты
# (классификатора) из контекста-источника
# При ошибке возвращает ноль

    mapCopySelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopySelectContext', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContext(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapCopySelectContext_t (_target, _source)


# Копировать контекст (описание условий) поиска/отображения
# в существующий контекст поиска/отображения
# с сохранением связи с картой исходного контекста поиска/отображения
# target - контекст условий поиска, куда выполняется копирование
# source - копируемый контекст поиска;
# (Каждый созданный контекст должен быть удален, когда
# он больше не используется)
# При ошибке возвращает ноль

    mapCopySelectContextEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopySelectContextEx', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContextEx(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapCopySelectContextEx_t (_target, _source)


# Запросить идентификатор классификатора HRSC для контекста
# select - контекст (описание условий) поиска/отображения
# При ошибке возвращает ноль

    mapGetSelectContextRscIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetSelectContextRscIdent', maptype.HSELECT)
    def mapGetSelectContextRscIdent(_select: maptype.HSELECT) -> maptype.HRSC:
        return mapGetSelectContextRscIdent_t (_select)


# Установить доступ ко всем видам данных
# контекста поиска/отображения
# select - контекст (описание условий) поиска/отображения
# При ошибке возвращает ноль

    mapClearSelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearSelectContext', maptype.HSELECT)
    def mapClearSelectContext(_select: maptype.HSELECT) -> int:
        return mapClearSelectContext_t (_select)


# Установить доступ ко всем видам данных
# контекста поиска/отображения для заданной карты
# hMap   - идентификатор открытой карты,
# hSite    - идентификатор открытой пользовательской карты,
# При ошибке возвращает ноль

    mapClearSelectContextEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearSelectContextEx', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapClearSelectContextEx(_select: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapClearSelectContextEx_t (_select, _hmap, _hsite)


# Удалить контекст (описание условий) поиска/отображения
# объектов карты
# select - контекст (описание условий) поиска/отображения.

    mapDeleteSelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteSelectContext', maptype.HSELECT)
    def mapDeleteSelectContext(_select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapDeleteSelectContext_t (_select)


# Установить/запросить признак инвертирования условий поиска
# select - контекст (описание условий) поиска/отображения
# flag   - признак инвертирования
# Возвращает установленное значение

    mapSetInversionSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetInversionSelect', maptype.HSELECT, ctypes.c_int)
    def mapSetInversionSelect(_select: maptype.HSELECT, _flag: int) -> int:
        return mapSetInversionSelect_t (_select, _flag)

    mapGetInversionSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInversionSelect', maptype.HSELECT)
    def mapGetInversionSelect(_select: maptype.HSELECT) -> int:
        return mapGetInversionSelect_t (_select)


# Установить пересечение условий поиска (target = target & source)
# При выполнении операции учитываются только коды объектов,
# локализация, номера слоев и листов!
# Семантика, измерения и списки объектов не обрабатываются
# target - контекст условий поиска, в который помещается результат
# source - контекст поиска с дополнительными условиями
# При ошибке возвращает ноль

    mapSelectAndSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAndSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectAndSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapSelectAndSelect_t (_target, _source)


# Установить пересечение условий поиска (target = target & used)
# c составом объектов карты
# Результат аналогичен вызову функций mapGetSiteUsedSelect и mapSelectAndUsedSelect
# В исходном контексте условий поиска будут отключены коды объектов,
# локализация, номера слоев и листов, которых нет на заданной карте
# Семантика, измерения и списки объектов не обрабатываются
# hSelect - контекст условий поиска, в который помещается результат
# hMap    - идентификатор открытого документа
# hSite   - идентификатор открытой пользовательской карты в документе
# При ошибке возвращает ноль

    mapSelectAndUsedSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAndUsedSelect', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSelectAndUsedSelect(_hSelect: maptype.HSELECT, _hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapSelectAndUsedSelect_t (_hSelect, _hMap, _hSite)


# Установить пересечение условий поиска с операцией OR (target = target | source)
# При выполнении операции учитываются только коды объектов,
# локализация и номер слоя!
# Семантика, измерения и списки объектов не обрабатываются.
# target - контекст условий поиска, в который помещается результат
# source - контекст поиска с дополнительными условиями
# При ошибке возвращает ноль

    mapSelectOrSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectOrSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectOrSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        return mapSelectOrSelect_t (_target, _source)


# Запросить установлены ли условия для проверки
# hselect - условия поиска/отображения
# Если по условиям поиска все объекты выбираются без исключений -
# возвращает ноль, иначе - ненулевое значение

    mapIsSelectActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSelectActive', maptype.HSELECT)
    def mapIsSelectActive(_hselect: maptype.HSELECT) -> int:
        return mapIsSelectActive_t (_hselect)


# Установить доступ к объектам с заданным номером
# слоя (сегмента)
# select - контекст условий поиска
# layer  - номер слоя (сегмента), начинается с 0 (!).
#          Если равен -1 , то устанавливается доступ ко всем слоям
# check  - доступность слоя (0 - нет доступа, != 0 - есть)
# Термин Layer явлется синонимом слова Segment

    mapSelectLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectLayer', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectLayer(_select: maptype.HSELECT, _layer: int, _check: int) -> ctypes.c_void_p:
        return mapSelectLayer_t (_select, _layer, _check)


# Запросить доступность объектов с заданным номером слоя (сегмента)
# select - контекст условий поиска
# layer  - номер слоя (сегмента). Если равен -1, то проверяется доступ ко всем слоям
#          (если возвращает 0 - один или более слоев недоступны)
# Термин Layer явлется синонимом слова Segment
# Возвращает доступность объектов слоя : 0 - нет доступа, != 0 - есть

    mapCheckLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckLayer', maptype.HSELECT, ctypes.c_int)
    def mapCheckLayer(_select: maptype.HSELECT, _layer: int) -> int:
        return mapCheckLayer_t (_select, _layer)


# Установить доступ к объектам в заданном листе
# select - контекст условий поиска
# list   - номер листа карты, начинается с 1. Если равен -1,
#          то устанавливается доступ ко всем листам
# check  - доступность листа (0 - нет доступа, != 0 - есть)

    mapSelectList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectList', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectList(_select: maptype.HSELECT, _list: int, _check: int) -> ctypes.c_void_p:
        return mapSelectList_t (_select, _list, _check)


# Запросить доступность объектов в заданном листе
# select - контекст условий поиска
# list   - номер листа карты, начинается с 1. Если равен -1,
#          то проверяется доступ ко всем листам
#          (если возвращает 0 - один или более листов недоступны)
# Возвращает доступность объектов листа : 0 - нет доступа, != 0 - есть

    mapCheckList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckList', maptype.HSELECT, ctypes.c_int)
    def mapCheckList(_select: maptype.HSELECT, _list: int) -> int:
        return mapCheckList_t (_select, _list)


# Установить доступ к объектам c листом, слоем, локализацией, и кодом, как у
# переданного объекта
# select - контекст условий поиска
# hobj   - идентификатор объектв в памяти

    mapSelectMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMapObject', maptype.HSELECT, maptype.HOBJ)
    def mapSelectMapObject(_select: maptype.HSELECT, _info: maptype.HOBJ) -> ctypes.c_void_p:
        return mapSelectMapObject_t (_select, _info)


# Установить доступ к объектам c заданным индексом в классификаторе
# select - контекст условий поиска
# object - индекс объекта (внутренний код), начинается с 1.
#          Если равен -1, то устанавливается доступ ко всем объектам
# check  - доступность объекта (0 - нет доступа, != 0 - есть)
# Возвращает доступность объектов по коду : 0 - нет доступа, != 0 - есть

    mapSelectObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectObject', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectObject(_select: maptype.HSELECT, _object: int, _check: int) -> ctypes.c_void_p:
        return mapSelectObject_t (_select, _object, _check)


# Запросить доступность объекта с заданным индексом в классификаторе
# (внутренним кодом)
# select - контекст условий поиска
# object - индекс объекта (внутренний код). Если равен -1,
#          то проверяется доступ ко всем объектам
#          (если возвращает 0 - один или более объектов недоступны)
# Возвращает доступность объекта : 0 - нет доступа, != 0 - есть

    mapCheckObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckObject', maptype.HSELECT, ctypes.c_int)
    def mapCheckObject(_select: maptype.HSELECT, _object: int) -> int:
        return mapCheckObject_t (_select, _object)


# Запросить доступность объекта c заданным индексом в классификаторе
# с учетом локализации и слоя
# select - контекст условий поиска
# object - индекс объекта (внутренний код). Если равен -1
#          то проверяется доступ ко всем объектам
#          (если возвращает 0 - один или более объектов недоступны)
# Использовать для определения доступности при настройке состава
# с помощью диалога selSetObjectFilter (см. mapselec.h)
# Возвращает доступность объекта : 0 - нет доступа, != 0 - есть

    mapCheckObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckObjectEx', maptype.HSELECT, ctypes.c_int)
    def mapCheckObjectEx(_select: maptype.HSELECT, _object: int) -> int:
        return mapCheckObjectEx_t (_select, _object)


# Установить доступ к объектам c заданной локализацией
#  0 - линейный, 1 - площадной, 2 - точечный, 3 - подпись,
#  4 - векторный (линия с 2-мя точками),
#  5 - шаблон (сложная подпись)
# select - контекст условий поиска
# local  - код локализации, начинается с 0 (LOCAL_LINE, LOCAL_SQUARE ...).
#          Если равен -1 , то устанавливается доступ ко всем локализациям
# check  - доступность локализации (0 - нет доступа, != 0 - есть)

    mapSelectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectLocal', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectLocal(_select: maptype.HSELECT, _local: int, _check: int) -> ctypes.c_void_p:
        return mapSelectLocal_t (_select, _local, _check)


# Запросить доступность объектов с заданной локализацией
# select - контекст условий поиска
# local  - код локализации, начинается с 0. Если равен -1, то проверяется доступ ко всем локализациям
#          (если возвращает 0 - один или более локализаций недоступны)
# Возвращает доступность локализации : 0 - нет доступа, != 0 - есть

    mapCheckLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckLocal', maptype.HSELECT, ctypes.c_int)
    def mapCheckLocal(_select: maptype.HSELECT, _local: int) -> int:
        return mapCheckLocal_t (_select, _local)


# Установить доступ к объектам с заданными номерами
# select  - контекст условий поиска
# min,max - диапазон номеров поиска, начинается с 0.
#           Если оба числа равны -1, то устанавливается
#           доступ ко всем объектам по номерам

    mapSelectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectKey', maptype.HSELECT, ctypes.c_ulong, ctypes.c_ulong)
    def mapSelectKey(_select: maptype.HSELECT, _min: int, _max: int) -> ctypes.c_void_p:
        return mapSelectKey_t (_select, _min, _max)


# Запросить доступность объекта карты с заданным номером
# select - контекст условий поиска
# key    - номер объекта, начинается с 0. Если равен -1,
#          то проверяется доступ ко всем объектам по номерам
#          (если возвращает 0 - один или более объектов недоступны)
# Возвращает доступность объекта : 0 - нет доступа, != 0 - есть

    mapCheckKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckKey', maptype.HSELECT, ctypes.c_ulong)
    def mapCheckKey(_select: maptype.HSELECT, _key: int) -> int:
        return mapCheckKey_t (_select, _key)


# Запросить минимальный номер в диапазоне поиска
# select - контекст условий поиска
# Может равняться 0, когда доступны все номера объектов

    mapGetMinKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetMinKey', maptype.HSELECT)
    def mapGetMinKey(_select: maptype.HSELECT) -> int:
        return mapGetMinKey_t (_select)


# Запросить максимальный номер в диапазоне поиска
# select - контекст условий поиска

    mapGetMaxKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetMaxKey', maptype.HSELECT)
    def mapGetMaxKey(_select: maptype.HSELECT) -> int:
        return mapGetMaxKey_t (_select)


# Установить/Отменить условие поиска по тексту подписи
# select - контекст условий поиска
# value  - значение строки для поиска (может включать служебные символы '#' и '?')
# isspecial - признак обработки специальных символов при поиске ('#' и '?')
# Символ % или # в начале строки означает поиск подстроки, которая следует за
# управляющим символом (символ % означает поиск строго в конце или
# в начале строки - если в конце стоит два символа %%, символ # означает
# поиск подстроки в любом месте строки).
# Символ ? означает возможность подстановки любого символа, может применяться
# вместе с символом #.
# Например: шаблон поиска "#ушк#" или "#ушк" или "%ушк%%" найдет значение "Пушкино",
# но "%ушк" будет искать строки строго оканчивающиеся заданным шаблоном ("ушк").
# Шаблон "#39%" или "%39%" найдет строку "139%",
# шаблон "се??й" найдет строки - "серый", "седой"
# Если value равно нулю, то условие поиска отменяется
# При ошибке возвращает ноль, иначе - номер условия

    mapSelectTitlePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectTitlePro', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int)
    def mapSelectTitlePro(_select: maptype.HSELECT, _value: mapsyst.WTEXT, _isspecial: int) -> int:
        return mapSelectTitlePro_t (_select, _value.buffer(), _isspecial)

    mapSelectTitleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectTitleUn', maptype.HSELECT, maptype.PWCHAR)
    def mapSelectTitleUn(_select: maptype.HSELECT, _value: mapsyst.WTEXT) -> int:
        return mapSelectTitleUn_t (_select, _value.buffer())

    mapSelectTitle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectTitle', maptype.HSELECT, ctypes.c_char_p)
    def mapSelectTitle(_select: maptype.HSELECT, _value: ctypes.c_char_p) -> int:
        return mapSelectTitle_t (_select, _value)


# Добавить условие поиска по семантике в список (в узел)
# select - контекст условий поиска
# code   - коды условий (1-CMLESS,4-CMMORE, ... - см. maptype.h)
# value  - значение для условия
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль, иначе - номер условия

    mapSelectSemanticAppendEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticAppendEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapSelectSemanticAppendEx(_select: maptype.HSELECT, _code: int, _semcode: int, _value: ctypes.c_char_p, _node: int) -> int:
        return mapSelectSemanticAppendEx_t (_select, _code, _semcode, _value, _node)

    mapSelectSemanticAppend_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticAppend', maptype.HSELECT, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapSelectSemanticAppend(_select: maptype.HSELECT, _code: int, _semcode: int, _value: ctypes.c_char_p) -> int:
        return mapSelectSemanticAppend_t (_select, _code, _semcode, _value)

    mapSelectSemanticAppendExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticAppendExUn', maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSelectSemanticAppendExUn(_select: maptype.HSELECT, _code: int, _semcode: int, _value: mapsyst.WTEXT, _node: int) -> int:
        return mapSelectSemanticAppendExUn_t (_select, _code, _semcode, _value.buffer(), _node)

    mapSelectSemanticAppendUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticAppendUn', maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def mapSelectSemanticAppendUn(_select: maptype.HSELECT, _code: int, _semcode: int, _value: mapsyst.WTEXT) -> int:
        return mapSelectSemanticAppendUn_t (_select, _code, _semcode, _value.buffer())


# Добавить список строк из текстового файла в условия поиска по семантике
# select - контекст условий поиска
# code - условие для проверки значения семантики (CMLEQUAL, CMLNOTEQ, CMLPARTEQUAL, ... - см. maptype.h)
# semcode - код семантики
# buffer - список строк в кодировке UTF8, разделенных символом \n,
#          при обработке строк символ \n будет заменен на ноль
# size - размер буфера со списком строк
# isutf8 - признак кодировки UTF8 (иначе - ANSI)
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике или 0
# При ошибке возвращает ноль

    mapSelectAppendStringArrayUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAppendStringArrayUn', maptype.HSELECT, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectAppendStringArrayUn(_select: maptype.HSELECT, _code: int, _semcode: int, _buffer: mapsyst.WTEXT, _size: int, _istitle: int, _node: int) -> int:
        return mapSelectAppendStringArrayUn_t (_select, _code, _semcode, _buffer.buffer(), _size, _istitle, _node)

    mapSelectAppendStringArray_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAppendStringArray', maptype.HSELECT, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectAppendStringArray(_select: maptype.HSELECT, _code: int, _semcode: int, _buffer: ctypes.c_char_p, _size: int, _isutf8: int, _istitle: int, _node: int) -> int:
        return mapSelectAppendStringArray_t (_select, _code, _semcode, _buffer, _size, _isutf8, _istitle, _node)


# Запросить список строк в кодировке UTF8 для поиска из условий поиска
# code - поле для запроса условия проверки значения семантики (CMLPARTEQUAL, ...)
# semcode - поле для запроса кода семантики
# istitle - поле для запроса признака дополнительного поиска по текстам подписей
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике или 0
# Возвращает идентификатор записи со списком строк
# При ошибке возвращает ноль

    mapGetSelectStringArrayHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectStringArrayHandle', maptype.HSELECT, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapGetSelectStringArrayHandle(_select: maptype.HSELECT, _code: ctypes.POINTER(ctypes.c_int), _semcode: ctypes.POINTER(ctypes.c_int), _istitle: ctypes.POINTER(ctypes.c_int), _node: int) -> ctypes.c_void_p:
        return mapGetSelectStringArrayHandle_t (_select, _code, _semcode, _istitle, _node)


# Удалить запись в памяти, созданную функцией mapGetSelectStringArrayHandle
# record - идентификатор записи в памяти

    mapFreeSelectStringArrayHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSelectStringArrayHandle', ctypes.c_void_p)
    def mapFreeSelectStringArrayHandle(_record: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSelectStringArrayHandle_t (_record)


# Удалить все условия поиска по семантике из списка (все узлы)
# select - контекст условий поиска

    mapSelectSemanticClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticClear', maptype.HSELECT)
    def mapSelectSemanticClear(_select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectSemanticClear_t (_select)


# Запросить количество узлов в дереве с условиями по семантике
# select - контекст условий поиска
# При ошибке возвращает ноль

    mapSelectSemanticNodeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticNodeCount', maptype.HSELECT)
    def mapSelectSemanticNodeCount(_select: maptype.HSELECT) -> int:
        return mapSelectSemanticNodeCount_t (_select)


# Запросить количество установленных условий по семантике в узле
# select - контекст условий поиска
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticCountEx', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticCountEx(_select: maptype.HSELECT, _node: int) -> int:
        return mapSelectSemanticCountEx_t (_select, _node)

    mapSelectSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticCount', maptype.HSELECT)
    def mapSelectSemanticCount(_select: maptype.HSELECT) -> int:
        return mapSelectSemanticCount_t (_select)


# Запросить код условия для семантики по последовательному номеру в узле
# select - контекст условий поиска
# number - последовательный номер семантики
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticConditionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticConditionEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticConditionEx(_select: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticConditionEx_t (_select, _number, _node)

    mapSelectSemanticCondition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticCondition', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticCondition(_select: maptype.HSELECT, _number: int) -> int:
        return mapSelectSemanticCondition_t (_select, _number)


# Запросить код семантики по последовательному номеру в узле
# Например : 4 - абс.высота, 9 - название, ...
# select - контекст условий поиска
# number - последовательный номер семантики
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticCodeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticCodeEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticCodeEx(_select: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticCodeEx_t (_select, _number, _node)

    mapSelectSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticCode', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticCode(_select: maptype.HSELECT, _number: int) -> int:
        return mapSelectSemanticCode_t (_select, _number)


# Удалить набор условий поиска по семантике (список условий - узел)
# select - контекст условий поиска
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticDeleteNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticDeleteNode', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticDeleteNode(_select: maptype.HSELECT, _node: int) -> int:
        return mapSelectSemanticDeleteNode_t (_select, _node)


# Удалить условие из списка (узла)
# select - контекст условий поиска
# number - номер условия в списке (от 1 до GetCount())
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticDeleteEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticDeleteEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticDeleteEx(_select: maptype.HSELECT, _number: int, _node: int) -> int:
        return mapSelectSemanticDeleteEx_t (_select, _number, _node)

    mapSelectSemanticDelete_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticDelete', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticDelete(_select: maptype.HSELECT, _number: int) -> int:
        return mapSelectSemanticDelete_t (_select, _number)


# Установить/Запросить обобщающее условие для набора семантик (узла)
# select - контекст условий поиска
# code - код условия :
# 16 - CMOR : выполняется хотя бы одно,
# 32 - CMAND : выполняются все, см. MAPTYPE.H
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике

    mapSelectSemanticLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticLinkEx(_select: maptype.HSELECT, _code: int, _node: int) -> ctypes.c_void_p:
        return mapSelectSemanticLinkEx_t (_select, _code, _node)

    mapSelectSemanticLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticLink', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticLink(_select: maptype.HSELECT, _code: int) -> ctypes.c_void_p:
        return mapSelectSemanticLink_t (_select, _code)

    mapGetSelectSemanticLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_int)
    def mapGetSelectSemanticLinkEx(_select: maptype.HSELECT, _node: int) -> int:
        return mapGetSelectSemanticLinkEx_t (_select, _node)

    mapGetSelectSemanticLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectSemanticLink', maptype.HSELECT)
    def mapGetSelectSemanticLink(_select: maptype.HSELECT) -> int:
        return mapGetSelectSemanticLink_t (_select)


# Установить обобщающее условие для списка наборов семантик (между узлами)
# code - код условия :
# 16 - CMOR : выполняется хотя бы одно,
# 32 - CMAND : выполняются все, см. MAPTYPE.H

    mapSelectSemanticListLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticListLink', maptype.HSELECT, ctypes.c_int)
    def mapSelectSemanticListLink(_select: maptype.HSELECT, _code: int) -> ctypes.c_void_p:
        return mapSelectSemanticListLink_t (_select, _code)


# Запросить обобщающее условие для списка наборов семантик (между узлами)
# code - код условия :
# 16 - CMOR : выполняется хотя бы одно,
# 32 - CMAND : выполняются все, см. MAPTYPE.H

    mapGetSelectSemanticListLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectSemanticListLink', maptype.HSELECT)
    def mapGetSelectSemanticListLink(_select: maptype.HSELECT) -> int:
        return mapGetSelectSemanticListLink_t (_select)


# Запросить значение семантики по последовательному номеру в узле
# select - контекст условий поиска
# number - последовательный номер семантики
# place  - адрес строки, в которой разместиться результат
# size   - размер выходной строки в байтах
# node   - номер c 1 списка условий (узла) в дереве условий поиска по семантике
# При ошибке возвращает ноль

    mapSelectSemanticValueExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticValueExUn', maptype.HSELECT, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticValueExUn(_select: maptype.HSELECT, _number: int, _place: mapsyst.WTEXT, _size: int, _node: int) -> int:
        return mapSelectSemanticValueExUn_t (_select, _number, _place.buffer(), _size, _node)

    mapSelectSemanticValueUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticValueUn', maptype.HSELECT, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSelectSemanticValueUn(_select: maptype.HSELECT, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapSelectSemanticValueUn_t (_select, _number, _place.buffer(), _size)

    mapSelectSemanticValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticValueEx', maptype.HSELECT, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapSelectSemanticValueEx(_select: maptype.HSELECT, _number: int, _place: ctypes.c_char_p, _size: int, _node: int) -> int:
        return mapSelectSemanticValueEx_t (_select, _number, _place, _size, _node)

    mapSelectSemanticValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSemanticValue', maptype.HSELECT, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapSelectSemanticValue(_select: maptype.HSELECT, _number: int, _place: ctypes.c_char_p, _size: int) -> int:
        return mapSelectSemanticValue_t (_select, _number, _place, _size)


# Запросить количество установленных условий по измерениям объектов
# select - контекст условий поиска
# (длина, периметр, площадь, высота)

    mapSelectMeasureCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectMeasureCount', maptype.HSELECT)
    def mapSelectMeasureCount(_select: maptype.HSELECT) -> int:
        return mapSelectMeasureCount_t (_select)


# Удалить все данные из списка измерений
# select - контекст условий поиска

    mapSelectMeasureClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMeasureClear', maptype.HSELECT)
    def mapSelectMeasureClear(_select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectMeasureClear_t (_select)


# Добавить измерение в список
# select - контекст условий поиска
# measurecode - код измерения объекта : длина, периметр, площадь, высота (см. MAPTYPE.H)
# condition - коды условий (1-CMLESS,3-CMMORE, ... - см. MAPTYPE.H)
# value - значение измерения в метрах, для площади - в кв. метрах.
# Если заданы только condition1 и value1, а condition2 = 0,
# добавляется единственное значение измерения.
# Для задания диапазона значений, дополнительно указываются condition2 и value2.
# В этом случае condition1 должно равняться CMMOREEQ (>=),
# condition2 - CMLESSEQ (<=) !
# При ошибке возвращает ноль, иначе - номер условия в списке

    mapSelectMeasureAppend_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectMeasureAppend', maptype.HSELECT, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_double)
    def mapSelectMeasureAppend(_select: maptype.HSELECT, _measurecode: int, _condition1: int, _value1: float, _condition2: int, _value2: float) -> int:
        return mapSelectMeasureAppend_t (_select, _measurecode, _condition1, _value1, _condition2, _value2)


# Запросить установлен ли для измерения диапазон значений
# по последовательному номеру в списке.
# select - контекст условий поиска
# number - номер измерения
# Возвращает 1 - установлено единственное значение;
#            2 - установлен диапазон значений;
#            0 - при ошибке.

    mapIsSelectMeasureRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSelectMeasureRange', maptype.HSELECT, ctypes.c_int)
    def mapIsSelectMeasureRange(_select: maptype.HSELECT, _number: int) -> int:
        return mapIsSelectMeasureRange_t (_select, _number)


# Установить/Запросить обобщающее условие для набора измерений
# select   - контекст условий поиска
# linkcode - код условия :
# 16 - CMOR : выполняется хотя бы одно,
# 32 - CMAND : выполняются все (см. MAPTYPE.H)

    mapSelectMeasureLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMeasureLink', maptype.HSELECT, ctypes.c_int)
    def mapSelectMeasureLink(_select: maptype.HSELECT, _linkcode: int) -> ctypes.c_void_p:
        return mapSelectMeasureLink_t (_select, _linkcode)

    mapGetSelectMeasureLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectMeasureLink', maptype.HSELECT)
    def mapGetSelectMeasureLink(_select: maptype.HSELECT) -> int:
        return mapGetSelectMeasureLink_t (_select)


# Запросить код измерения по последовательному номеру
# select - контекст условий поиска
# number - номер измерения
# Например : площадь, длина и т.д. (см. MAPTYPE.H)
# При ошибке возвращает ноль

    mapSelectMeasureCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectMeasureCode', maptype.HSELECT, ctypes.c_int)
    def mapSelectMeasureCode(_select: maptype.HSELECT, _number: int) -> int:
        return mapSelectMeasureCode_t (_select, _number)


# Запросить значение измерения по последовательному номеру в списке
# select - контекст условий поиска
# number - номер измерения
# pvalue1,pvalue2 - адреса для размещения результата.
# pvalue2 заполняется, если установлен диапазон значений
# Возвращает 1 - передается одно значение;
#            2 - передаются два значения;
#            0 - при ошибке.

    mapSelectMeasureValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectMeasureValue', maptype.HSELECT, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapSelectMeasureValue(_select: maptype.HSELECT, _number: int, _pvalue1: ctypes.POINTER(ctypes.c_double), _pvalue2: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSelectMeasureValue_t (_select, _number, _pvalue1, _pvalue2)


# Запросить код условия для измерения по последовательному номеру
# select - контекст условий поиска
# number - номер измерения
# pcondition1,pcondition2 - адреса для размещения результата.
# Возвращает 1 - передается одно значение;
#            2 - передаются два значения;
#            0 - при ошибке.

    mapSelectMeasureCondition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectMeasureCondition', maptype.HSELECT, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapSelectMeasureCondition(_select: maptype.HSELECT, _number: int, _pcondition1: ctypes.POINTER(ctypes.c_int), _pcondition2: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapSelectMeasureCondition_t (_select, _number, _pcondition1, _pcondition2)


# Отменить поиск по формулам и удалить все группы формул
# select - контекст условий поиска

    mapSelectFormulaClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectFormulaClear', maptype.HSELECT)
    def mapSelectFormulaClear(_select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSelectFormulaClear_t (_select)


# Запросить число групп формул в условиях поиска
# select - контекст условий поиска
# При ошибке возвращает ноль

    mapGetSelectGroupFormulaCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectGroupFormulaCount', maptype.HSELECT)
    def mapGetSelectGroupFormulaCount(_select: maptype.HSELECT) -> int:
        return mapGetSelectGroupFormulaCount_t (_select)


# Запросить в условиях поиска число формул в группе
# select - контекст условий поиска
# group  - номер группы формул
# При ошибке возвращает ноль

    mapGetSelectFormulaCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFormulaCountEx', maptype.HSELECT, ctypes.c_int)
    def mapGetSelectFormulaCountEx(_select: maptype.HSELECT, _group: int) -> int:
        return mapGetSelectFormulaCountEx_t (_select, _group)

    mapGetSelectFormulaCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFormulaCount', maptype.HSELECT)
    def mapGetSelectFormulaCount(_select: maptype.HSELECT) -> int:
        return mapGetSelectFormulaCount_t (_select)


# Добавить в условия поиска формулу в группу формул
# select - контекст условий поиска
# formula - строка с математическим выражением над семантиками и свойствами объекта
# minvalue - нижняя граница допустимого диапазона для значения формулы
# maxvalue - верхняя граница допустимого диапазона для значения формулы
# group    - номер группы формул, в которую добавляется формула
# При ошибке возвращает ноль

    mapAppendSelectFormulaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSelectFormulaEx', maptype.HSELECT, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendSelectFormulaEx(_select: maptype.HSELECT, _formula: ctypes.c_char_p, _minvalue: float, _maxvalue: float, _group: int) -> int:
        return mapAppendSelectFormulaEx_t (_select, _formula, _minvalue, _maxvalue, _group)

    mapAppendSelectFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSelectFormula', maptype.HSELECT, ctypes.c_char_p, ctypes.c_double, ctypes.c_double)
    def mapAppendSelectFormula(_select: maptype.HSELECT, _formula: ctypes.c_char_p, _minvalue: float, _maxvalue: float) -> int:
        return mapAppendSelectFormula_t (_select, _formula, _minvalue, _maxvalue)


# Удалить формулу из списка формул в условиях поиска
# select - контекст условий поиска
# number - номер формулы в списке с 1
# group  - номер группы формул, в которой удаляется формула

    mapDeleteSelectFormulaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteSelectFormulaEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapDeleteSelectFormulaEx(_select: maptype.HSELECT, _number: int, _group: int) -> ctypes.c_void_p:
        return mapDeleteSelectFormulaEx_t (_select, _number, _group)

    mapDeleteSelectFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteSelectFormula', maptype.HSELECT, ctypes.c_int)
    def mapDeleteSelectFormula(_select: maptype.HSELECT, _number: int) -> ctypes.c_void_p:
        return mapDeleteSelectFormula_t (_select, _number)


# Запросить/Установить обобщенное условие (CMOR или CMAND) для списка формул в группе
# select - контекст условий поиска
# flag - обобщенное условие поиска по формулам (выполняются проверки для всех формул - CMAND,
#        или хотя бы одна - CMOR)
# group  - номер группы формул
# При ошибке возвращает ноль

    mapGetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_int)
    def mapGetSelectFormulaLinkEx(_select: maptype.HSELECT, _group: int) -> int:
        return mapGetSelectFormulaLinkEx_t (_select, _group)

    mapSetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSetSelectFormulaLinkEx(_select: maptype.HSELECT, _flag: int, _group: int) -> int:
        return mapSetSelectFormulaLinkEx_t (_select, _flag, _group)

    mapGetSelectFormulaLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFormulaLink', maptype.HSELECT)
    def mapGetSelectFormulaLink(_select: maptype.HSELECT) -> int:
        return mapGetSelectFormulaLink_t (_select)

    mapSetSelectFormulaLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectFormulaLink', maptype.HSELECT, ctypes.c_int)
    def mapSetSelectFormulaLink(_select: maptype.HSELECT, _flag: int) -> int:
        return mapSetSelectFormulaLink_t (_select, _flag)


# Запросить/Установить обобщенное условие для групп формул
# select - контекст условий поиска
# flag - обобщенное условие поиска по формулам (выполняются проверки для всех групп - CMAND,
#        или хотя бы одна - CMOR)
# При ошибке возвращает ноль

    mapGetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFormulaGroupLink', maptype.HSELECT)
    def mapGetSelectFormulaGroupLink(_select: maptype.HSELECT) -> int:
        return mapGetSelectFormulaGroupLink_t (_select)

    mapSetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectFormulaGroupLink', maptype.HSELECT, ctypes.c_int)
    def mapSetSelectFormulaGroupLink(_select: maptype.HSELECT, _flag: int) -> int:
        return mapSetSelectFormulaGroupLink_t (_select, _flag)


# Запросить размер записи, необходимый для сохранения условий поиска
# select - контекст условий поиска
# При ошибке возвращает ноль

    mapGetSelectRecordSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectRecordSize', maptype.HSELECT)
    def mapGetSelectRecordSize(_select: maptype.HSELECT) -> int:
        return mapGetSelectRecordSize_t (_select)


# Сформировать запись для сохранения условий поиска
# select - контекст условий поиска
# buffer - адрес записи
# length - длина буфера,для размещения записи
# При ошибке возвращает ноль

    mapGetSelectRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectRecord', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapGetSelectRecord(_select: maptype.HSELECT, _buffer: ctypes.c_char_p, _length: int) -> int:
        return mapGetSelectRecord_t (_select, _buffer, _length)


# Сформировать запись для сохранения условий поиска в формате XML
# select  - контекст условий поиска
# name    - имя модели (условий поиска) или ноль
# realset - признак записи реально выбранных объектов и слоев,
#           если равен нулю, то пишутся выбранные или наоборот невыбранные -
#           смотря чего меньше и выставляется признак выбора
# Возвращает идентификатор записи формата XML в памяти
# Для получения указателя на запись применяются функция mapGetSelectRecordXMLPoint
# Для удаления записи в памяти применяются функция mapFreeSelectRecordXML
# При ошибке возвращает ноль

    mapGetSelectRecordXMLEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectRecordXMLEx', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int)
    def mapGetSelectRecordXMLEx(_select: maptype.HSELECT, _name: mapsyst.WTEXT, _realset: int) -> ctypes.c_void_p:
        return mapGetSelectRecordXMLEx_t (_select, _name.buffer(), _realset)

    mapGetSelectRecordXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectRecordXML', maptype.HSELECT, maptype.PWCHAR)
    def mapGetSelectRecordXML(_select: maptype.HSELECT, _name: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapGetSelectRecordXML_t (_select, _name.buffer())


# Сформировать запись для сохранения условий поиска
# name    - имя модели (условий поиска) или ноль
# realset     != 0  при сохранении типов объектов, которые используются в фильтрах,
#                   должны проверяться локализация и слой (для уменьшения размеров фильтров)
# isobjectcode = 0   в модель объектов записываются ключи объектов
#              != 0  в модель объектов записываются внешние коды объектов
# При ошибке возвращает ноль

    mapGetSelectRecordXMLPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectRecordXMLPro', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetSelectRecordXMLPro(_select: maptype.HSELECT, _name: mapsyst.WTEXT, _realset: int, _isobjectcode: int = 0) -> ctypes.c_void_p:
        return mapGetSelectRecordXMLPro_t (_select, _name.buffer(), _realset, _isobjectcode)


# Удалить запись в памяти, созданную функцией mapGetSelectRecordXML
# select - контекст условий поиска
# record - идентификатор записи формата XML в памяти

    mapFreeSelectRecordXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSelectRecordXML', maptype.HSELECT, ctypes.c_void_p)
    def mapFreeSelectRecordXML(_select: maptype.HSELECT, _record: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeSelectRecordXML_t (_select, _record)


# Заполнить условия поиска из записи
# select - контекст условий поиска
# buffer - адрес записи
# length - длина записи или буфера,содержащего запись (не меньше записи)
# При ошибке возвращает ноль

    mapPutSelectRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutSelectRecord', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapPutSelectRecord(_select: maptype.HSELECT, _buffer: ctypes.c_char_p, _length: int) -> int:
        return mapPutSelectRecord_t (_select, _buffer, _length)


# Заполнить условия поиска из записи XML
# select - контекст условий поиска
# buffer - адрес записи
# length - длина записи в памяти
# При ошибке возвращает ноль

    mapPutSelectRecordXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutSelectRecordXML', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapPutSelectRecordXML(_select: maptype.HSELECT, _buffer: ctypes.c_char_p, _length: int) -> int:
        return mapPutSelectRecordXML_t (_select, _buffer, _length)


# Опросить наличие списка объектов в контексте условий поиска/отображения
# Список объектов содержит номер листа и номер объекта
# в листе
# select - контекст условий поиска
# Если список объектов не установлен,возвращает ноль

    mapIsSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSample', maptype.HSELECT)
    def mapIsSample(_select: maptype.HSELECT) -> int:
        return mapIsSample_t (_select)


# Запросить число объектов в списке для указанного листа карты
# select - контекст условий поиска
# list   - номер листа
# Если список объектов не установлен,возвращает ноль

    mapGetSampleCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSampleCount', maptype.HSELECT, ctypes.c_int)
    def mapGetSampleCount(_select: maptype.HSELECT, _list: int) -> int:
        return mapGetSampleCount_t (_select, _list)


# Запросить уникальный номер объекта из списке по порядковому номеру и
# указанному листу карты
# select - контекст условий поиска
# list   - номер листа в карте
# number - порядковый номер объекта в списке выбранных объектов листа
# Если список объектов не установлен, то возвращает ноль

    mapGetSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSampleByNumber', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapGetSampleByNumber(_select: maptype.HSELECT, _list: int, _number: int) -> int:
        return mapGetSampleByNumber_t (_select, _list, _number)


# Очистить список объектов в контексте условий поиска/отображения
# Список объектов содержит номер листа и номер объекта
# в листе
# select - контекст условий поиска
# Применяется для отбора объектов,атрибуты которых расположены
# во внешних базах данных

    mapClearSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearSample', maptype.HSELECT)
    def mapClearSample(_select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapClearSample_t (_select)


# Установить признак совместной обработки номеров объектов с
# условиями по локализации, слоям, семантике и пр.
# select - контекст условий поиска
# complex - признак совместной обработки (0/1)
# Возвращает предыдущее значение

    mapSetSampleComplex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSampleComplex', maptype.HSELECT, ctypes.c_int)
    def mapSetSampleComplex(_select: maptype.HSELECT, _complex: int) -> int:
        return mapSetSampleComplex_t (_select, _complex)


# Инвертировать список отобранных объектов в контексте условий поиска
# select - контекст условий поиска
# При ошибке возвращает ноль

    mapInvertSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInvertSample', maptype.HSELECT)
    def mapInvertSample(_select: maptype.HSELECT) -> int:
        return mapInvertSample_t (_select)


# Заполнить список объектов всеми номерами объектов, которые есть
# на листе
# select - контекст условий поиска
# list   - номер листа, с которого берутся объекты
# Связь с картой (hMap, hSite) устанавливается при создании контекста
# или при чтении контекста с карты
# Возвращает число объектов, занесенных в список для листа
# При ошибке возвращает ноль

    mapSetSampleAllObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSampleAllObjects', maptype.HSELECT, ctypes.c_int)
    def mapSetSampleAllObjects(_select: maptype.HSELECT, _list: int) -> int:
        return mapSetSampleAllObjects_t (_select, _list)


# Заполнить список объектов всеми номерами объектов, которые имеют
# заданный внутренний код
# Поиск объектов выполняется на той карте, где был создан контекст
# условий поиска или с которой он был заполнен (mapGetSiteViewSelect(),
# mapGetSiteSeekSelect())
# select - контекст условий поиска
# code   - внутренний код объекта (mapObjectCode)
# При ошибке возвращает ноль

    mapSelectSampleByObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSampleByObject', maptype.HSELECT, ctypes.c_int)
    def mapSelectSampleByObject(_select: maptype.HSELECT, _code: int) -> int:
        return mapSelectSampleByObject_t (_select, _code)


# Заполнить список отобранных объектов по выделенным объектам
# select - контекст условий поиска
# При ошибке возвращает ноль

    mapSelectSampleBySelectObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSampleBySelectObjects', maptype.HSELECT)
    def mapSelectSampleBySelectObjects(_select: maptype.HSELECT) -> int:
        return mapSelectSampleBySelectObjects_t (_select)


# Удалить из списка объектов все номера объектов, которые имеют
# заданный внутренний код
# Поиск объектов выполняется на той карте, где был создан контекст
# условий поиска или с которой он был заполнен (mapGetSiteViewSelect(),
# mapGetSiteSeekSelect())
# select - контекст условий поиска
# code   - внутренний код объекта (mapObjectCode)
# При ошибке возвращает ноль

    mapUnselectSampleByObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnselectSampleByObject', maptype.HSELECT, ctypes.c_int)
    def mapUnselectSampleByObject(_select: maptype.HSELECT, _code: int) -> int:
        return mapUnselectSampleByObject_t (_select, _code)


# Установить условия отображения объекта по имени листа карты и номеру объекта в карте
# hMap     - идентификатор открытой карты,
# listname - имя листа карты,
# key - уникальный номер объекта в карте
# При ошибке возвращает ноль

    mapSelectViewSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectViewSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapSelectViewSampleUn(_hMap: maptype.HMAP, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectViewSampleUn_t (_hMap, _listname.buffer(), _key)

    mapSelectViewSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectViewSample', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapSelectViewSample(_hMap: maptype.HMAP, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapSelectViewSample_t (_hMap, _listname, _key)


# Опросить наличие списка объектов в контексте условий отображения для карты
# hMap  - идентификатор открытой карты,
# hSite - идентификатор открытой пользовательской карты,
# При ошибке возвращает ноль

    mapCheckViewSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckViewSample', maptype.HMAP, maptype.HSITE)
    def mapCheckViewSample(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapCheckViewSample_t (_hMap, _hSite)


# Опросить наличие списка объектов в контексте условий поиска для карты
# hMap  - идентификатор открытой карты,
# hSite - идентификатор пользовательской карты,
# При ошибке возвращает ноль

    mapCheckSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckSeekSample', maptype.HMAP, maptype.HSITE)
    def mapCheckSeekSample(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapCheckSeekSample_t (_hMap, _hSite)


# Установить условия поиска объекта по имени листа карты
# и номеру объекта в карте
# hMap     - идентификатор открытой карты,
# listname - имя листа карты,
# key - уникальный номер объекта в карте
# При ошибке возвращает ноль

    mapSelectSeekSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapSelectSeekSampleUn(_hMap: maptype.HMAP, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectSeekSampleUn_t (_hMap, _listname.buffer(), _key)

    mapSelectSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSeekSample', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapSelectSeekSample(_hMap: maptype.HMAP, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapSelectSeekSample_t (_hMap, _listname, _key)


# Установить доступ к заданному объекту заданного листа карты
# select   - контекст условий поиска
# listname - имя листа карты,
# key - уникальный номер объекта в карте
# При ошибке возвращает ноль

    mapSelectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int)
    def mapSelectSampleUn(_select: maptype.HSELECT, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapSelectSampleUn_t (_select, _listname.buffer(), _key)

    mapSelectSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSample', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapSelectSample(_select: maptype.HSELECT, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapSelectSample_t (_select, _listname, _key)


# Установить доступ к заданному объекту заданного листа карты
# Выполняется без проверки повторных значений номеров объектов для
# ускорения формирования списков
# select   - контекст условий поиска
# listname - имя листа карты,
# key - уникальный номер объекта в карте
# При ошибке возвращает ноль

    mapFastSelectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFastSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int)
    def mapFastSelectSampleUn(_select: maptype.HSELECT, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapFastSelectSampleUn_t (_select, _listname.buffer(), _key)

    mapFastSelectSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFastSelectSample', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapFastSelectSample(_select: maptype.HSELECT, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapFastSelectSample_t (_select, _listname, _key)


# Установить доступ к заданному объекту заданного листа карты
# select - контекст условий поиска
# list   - номер листа карты,
# key    - уникальный номер объекта в карте
# При ошибке возвращает ноль

    mapSelectSampleByList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSampleByList', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSampleByList(_select: maptype.HSELECT, _list: int, _key: int) -> int:
        return mapSelectSampleByList_t (_select, _list, _key)


# Установить доступ к заданному объекту заданного листа карты
# select - контекст условий поиска
# list   - номер листа карты,
# number - номер объекта в листе
# В контексте условий поиска должна быть установлена карта
# При ошибке возвращает ноль

    mapSelectSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSampleByNumber', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSelectSampleByNumber(_select: maptype.HSELECT, _list: int, _number: int) -> int:
        return mapSelectSampleByNumber_t (_select, _list, _number)


# Исключить по ключу объект заданного листа карты из списка,
# в который этот номер был ранее занесен (mapSetSampleAllObjects, mapSelectSampleByObject ...)
# select   - контекст условий поиска
# listname - имя листа карты
# key      - уникальный номер объекта в карте
# В контексте условий поиска должна быть установлена карта
# При ошибке возвращает ноль

    mapUnselectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnselectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_int)
    def mapUnselectSampleUn(_select: maptype.HSELECT, _listname: mapsyst.WTEXT, _key: int) -> int:
        return mapUnselectSampleUn_t (_select, _listname.buffer(), _key)

    mapUnselectSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnselectSample', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapUnselectSample(_select: maptype.HSELECT, _listname: ctypes.c_char_p, _key: int) -> int:
        return mapUnselectSample_t (_select, _listname, _key)


# Исключить по ключу объект заданного листа карты из списка,
# в который этот номер был ранее занесен (mapSetSampleAllObjects, mapSelectSampleByObject ...)
# select - контекст условий поиска
# list   - номер листа карты,
# key    - уникальный номер объекта в карте
# В контексте условий поиска должна быть установлена карта.
# При ошибке возвращает ноль

    mapUnselectSampleByList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnselectSampleByList', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapUnselectSampleByList(_select: maptype.HSELECT, _list: int, _key: int) -> int:
        return mapUnselectSampleByList_t (_select, _list, _key)


# Исключить по номеру объект заданного листа карты из списка,
# в который этот номер был ранее занесен (mapSetSampleAllObjects, mapSelectSampleByObject ...)
# select - контекст условий поиска
# list   - номер листа карты,
# number - номер объекта в листе
# В контексте условий поиска должна быть установлена карта
# При ошибке возвращает ноль

    mapUnselectSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnselectSampleByNumber', maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapUnselectSampleByNumber(_select: maptype.HSELECT, _list: int, _number: int) -> int:
        return mapUnselectSampleByNumber_t (_select, _list, _number)


# Установить параметры поиска объектов по области
# hMap     - идентификатор открытой карты,
# object   - объект-область поиска
# distance - расстояние поиска в метрах
# флажки,описывающие критерии поиска :
# filter  - учитывать/не учитывать(1/0) фильтр объектов
#           (параметры фильтра должны быть установлены заранее
#           в контексте поиска)
# inside  - границы поиска объектов по области :
#            0 - по расстоянию, 1 - внутри области, 2 - целиком внутри области,
#            4 - целиком снаружи области.
# visible - с учетом/без учета(1/0) видимости объектов на карте
# listname - имя карты поиска. listname = 0,если устанавливается
#            поиск по всем картам.
# action   - порядок поиска объектов :
#            0 - последовательный поиск по мере запроса объектов,
#            1 - предварительный отбор всех объектов (главному
#            окну приложения посылается WM_PROGRESSBAR - maptype.h),
#            ускоряет многократный запрос отобранных объектов;
# При ошибке возвращает ноль

    mapSelectArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectArea', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapSelectArea(_hMap: maptype.HMAP, _object: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _listname: ctypes.c_char_p = None, _action: int = 0) -> int:
        return mapSelectArea_t (_hMap, _object, _distance, _filter, _inside, _visible, _listname, _action)

    mapSelectAreaUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAreaUn', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSelectAreaUn(_hMap: maptype.HMAP, _object: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _listname: mapsyst.WTEXT = mapsyst.WTEXT(None), _action: int = 0) -> int:
        return mapSelectAreaUn_t (_hMap, _object, _distance, _filter, _inside, _visible, _listname.buffer(), _action)


# Установить параметры поиска объектов по области.
# hMap     - идентификатор открытой карты,
# object   - объект-область поиска
# distance - расстояние поиска в метрах
# nmap     - номер карты поиска; устанавливает границы поиска
#            по картам.Если nmap=-1,поиск по всем картам
# флажки,описывающие критерии поиска :
# filter  - учитывать/не учитывать(1/0) фильтр объектов
#           (параметры фильтра должны быть установлены заранее
#           в контексте поиска)
# inside  - границы поиска объектов по области :
#            0 - по расстоянию, 1 - внутри области, 2 - целиком внутри области,
#            4 - целиком снаружи области.
# visible - с учетом/без учета(1/0) видимости объектов на карте
# action   - порядок поиска объектов :
#            0 - последовательный поиск по мере запроса объектов,
#            1 - предварительный отбор всех объектов (главному
#            окну приложения посылается WM_PROGRESSBAR - maptype.h),
#            ускоряет многократный запрос отобранных объектов;
# При ошибке возвращает ноль

    mapSelectAreaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAreaEx', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectAreaEx(_hMap: maptype.HMAP, _object: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _action: int, _nmap: int) -> int:
        return mapSelectAreaEx_t (_hMap, _object, _distance, _filter, _inside, _visible, _action, _nmap)


# Установить параметры поиска объектов по области.
# hMap     - идентификатор открытой карты,
# object   - объект-область поиска
# distance - расстояние поиска в метрах
# nmap     - номер карты поиска; устанавливает границы поиска
#            по картам.Если nmap=-1,поиск по всем картам
# флажки,описывающие критерии поиска :
# filter  - учитывать/не учитывать(1/0) фильтр объектов
#           (параметры фильтра должны быть установлены заранее
#           в контексте поиска)
# inside  - границы поиска объектов по области :
#            0 - по расстоянию, 1 - внутри области, 2 - целиком внутри области,
#            4 - целиком снаружи области.
# visible - с учетом/без учета(1/0) видимости объектов на карте
# action   - порядок поиска объектов :
#            0 - последовательный поиск по мере запроса объектов,
#            1 - предварительный отбор всех объектов (главному
#            окну приложения посылается WM_PROGRESSBAR - maptype.h),
#            ускоряет многократный запрос отобранных объектов
# subjectflag - с учетом/без учета(1/0) подобъектов области поиска;
# При ошибке возвращает ноль

    mapSelectAreaPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectAreaPro', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectAreaPro(_hMap: maptype.HMAP, _object: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _action: int, _nmap: int, _subjectflag: int) -> int:
        return mapSelectAreaPro_t (_hMap, _object, _distance, _filter, _inside, _visible, _action, _nmap, _subjectflag)


# Сбросить параметры поиска объектов по области
# hMap     - идентификатор открытой карты

    mapUnselectArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnselectArea', maptype.HMAP)
    def mapUnselectArea(_hMap: maptype.HMAP) -> ctypes.c_void_p:
        return mapUnselectArea_t (_hMap)


# Установить в контексте параметры поиска объектов по области.
# hselect - контекст поиска об'ектов
# object - объект-область поиска
# distance - расстояние поиска в метрах
# флажки,описывающие критерии поиска :
# filter  - учитывать/не учитывать(1/0) фильтр объектов
#           (параметры фильтра должны быть установлены заранее
#           в контексте поиска)
# inside  - границы поиска объектов по области :
#           0 - внутри области по расстоянию от заданного объекта,
#           1 - внутри области от заданного объекта, включая пересечение границы,
#               если задано расстояние, то с учетом расстояния,
#           2 - целиком внутри области без касания или пересечения границы,
#           4 - целиком снаружи области без касания или пересечения границы,
# visible - с учетом/без учета(1/0) видимости объектов на карте
# action   - порядок поиска объектов :
#            0 - последовательный поиск по мере запроса объектов,
#            1 - предварительный отбор всех объектов (главному
#            окну приложения посылается WM_PROGRESSBAR - maptype.h),
#            ускоряет многократный запрос отобранных объектов;
# subjectflag - выполнять поиск с учетом подобъектов заданной области (исключать внутренние контура)
# samplelist - при наличии списка объектов (см. mapSelectSampleUn и т.п.) отбирать по области
#              только объекты из этого списка (можно выполнять пересечение условий отбора)
# При ошибке возвращает ноль

    mapSelectSeekAreaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSeekAreaEx', maptype.HSELECT, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectSeekAreaEx(_hselect: maptype.HSELECT, _object: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _action: int = 0, _subjectflag: int = 0, _samplelist: int = 0) -> int:
        return mapSelectSeekAreaEx_t (_hselect, _object, _distance, _filter, _inside, _visible, _action, _subjectflag, _samplelist)

    mapSelectSeekArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSeekArea', maptype.HSELECT, maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectSeekArea(_hselect: maptype.HSELECT, _object: maptype.HOBJ, _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _action: int = 0) -> int:
        return mapSelectSeekArea_t (_hselect, _object, _distance, _filter, _inside, _visible, _action)


# Установить в контексте параметры поиска объектов по прямоугольной
# области.
# hselect - контекст поиска об'ектов
# dframe  - габариты области поиска в метрах
# distance - расстояние поиска в метрах
# флажки,описывающие критерии поиска :
# filter  - учитывать/не учитывать(1/0) фильтр объектов
#           (параметры фильтра должны быть установлены заранее
#           в контексте поиска)
# inside  - границы поиска объектов по области :
#           1 - внутри области, 2 - целиком внутри области,
#           0 - по расстоянию.
# visible - с учетом/без учета(1/0) видимости объектов на карте
# action   - порядок поиска объектов :
#            0 - последовательный поиск по мере запроса объектов,
#            1 - предварительный отбор всех объектов (главному
#            окну приложения посылается WM_PROGRESSBAR - maptype.h),
#            ускоряет многократный запрос отобранных объектов;
# При ошибке возвращает ноль

    mapSelectSeekAreaFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSelectSeekAreaFrame', maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSelectSeekAreaFrame(_hselect: maptype.HSELECT, _dframe: ctypes.POINTER(maptype.DFRAME), _distance: float = 0.0, _filter: int = 0, _inside: int = 1, _visible: int = 0, _action: int = 0) -> int:
        return mapSelectSeekAreaFrame_t (_hselect, _dframe, _distance, _filter, _inside, _visible, _action)


# Сбросить в контексте параметры поиска объектов по области
# hselect - контекст поиска объектов

    mapUnselectSeekArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnselectSeekArea', maptype.HSELECT)
    def mapUnselectSeekArea(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapUnselectSeekArea_t (_hselect)


# Запросить установлена ли область поиска по области
# hselect - условия поиска/отображения
# если результат = 0 - область отсутствует
#                  1 - область установлена

    mapGetAreaSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAreaSelectFlag', maptype.HSELECT)
    def mapGetAreaSelectFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetAreaSelectFlag_t (_hselect)


# Запросить признак отбора графических объектов по обобщенным условиям поиска
# hselect - условия поиска/отображения
# если результат = 0 - отбор по "общему" фильтру,
#                  1 - отобрать только графические объекты,
#                  2 - не отбирать графические объекты

    mapGetDrawObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetDrawObjectsFlag', maptype.HSELECT)
    def mapGetDrawObjectsFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetDrawObjectsFlag_t (_hselect)


# Установить признак отбора графических объектов по обобщенным условиям поиска
# hselect - условия поиска/отображения
# flag = 0 - отбор по "общему" фильтру,
#        1 - отобрать только графические объекты,
#        2 - не отбирать графические объекты.

    mapSetDrawObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetDrawObjectsFlag', maptype.HSELECT, ctypes.c_int)
    def mapSetDrawObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetDrawObjectsFlag_t (_hselect, _flag)


# Установить условие доступа к объектам по уровню значимости
# hselect - контекст условий поиска/отображения
# flag    - уровень значимости:
# 0 - все объекты
# 1 - отобрать только основные объекты
#     (которые отображаются в базовом масштабе карты)
# 2 - отобрать только дополнительные объекты
#     (которые не отображаются в базовом масштабе карты)

    mapSetLevelObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetLevelObjectsFlag', maptype.HSELECT, ctypes.c_int)
    def mapSetLevelObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetLevelObjectsFlag_t (_hselect, _flag)


# Запросить условие доступа к объектам по уровню значимости
# hselect - контекст условий поиска/отображения
# flag    - уровень значимости:
#           0 - все объекты
#           1 - отобрать только основные объекты,
#               которые отображаются в базовом масштабе карты
#           2 - отобрать только дополнительные объекты,
#               которые не отображаются в базовом масштабе карты
# При ошибке возвращает ноль

    mapGetLevelObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLevelObjectsFlag', maptype.HSELECT)
    def mapGetLevelObjectsFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetLevelObjectsFlag_t (_hselect)


# Установить признак отбора групп объектов при поиске по области
# В этом случае при отборе любого объекта группы включается вся группа
# (аналогично мультиполигону)
# hselect - условия поиска/отображения

    mapSetSelectGroupFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetSelectGroupFlag', maptype.HSELECT, ctypes.c_int)
    def mapSetSelectGroupFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        return mapSetSelectGroupFlag_t (_hselect, _flag)


# Запросить признак отбора групп объектов при поиске по области
# hselect - условия поиска/отображения
# При ошибке возвращает ноль

    mapGetSelectGroupFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectGroupFlag', maptype.HSELECT)
    def mapGetSelectGroupFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetSelectGroupFlag_t (_hselect)


# Установить/Запросить флаг отображения кластеров
# hselect - условия поиска/отображения
# flag    - признак отображения кластеров точечных объектов, заданных в классификаторе RSC
# При ошибке возвращает ноль

    mapGetShowClusterFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetShowClusterFlag', maptype.HSELECT)
    def mapGetShowClusterFlag(_hselect: maptype.HSELECT) -> int:
        return mapGetShowClusterFlag_t (_hselect)

    mapSetShowClusterFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetShowClusterFlag', maptype.HSELECT, ctypes.c_int)
    def mapSetShowClusterFlag(_hselect: maptype.HSELECT, _flag: int) -> int:
        return mapSetShowClusterFlag_t (_hselect, _flag)


# Зафиксировать в контексте поиска количественный состав карты
# При ошибке возвращает ноль
# hMap     - идентификатор открытой карты,
# (Используется при редактировании карты для исключения из поиска вновь
# созданных объектов)

    mapFreezeMapContents_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFreezeMapContents', maptype.HMAP)
    def mapFreezeMapContents(_hMap: maptype.HMAP) -> int:
        return mapFreezeMapContents_t (_hMap)


# Сбросить в контексте поиска данные о количественном составе карты
# hMap     - идентификатор открытой карты,
# При ошибке возвращает ноль

    mapDefreezeMapContents_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDefreezeMapContents', maptype.HMAP)
    def mapDefreezeMapContents(_hMap: maptype.HMAP) -> int:
        return mapDefreezeMapContents_t (_hMap)


# Найти точку метрики подобъекта, ближайшую к заданной
# info    - идентификатор объекта в памяти
# point   - координаты точки в прямоугольной
#           системе координат , в метрах на местности
# subject - последовательный номер подобъекта
#           (0 - объект, 1 - первый подобъект и т.д.,
#           если равен -1  - поиск по всей метрике)
# Возвращает номер точки (номер первой точки равен 1)
# При ошибке возвращает 0
# Для определения номера найденного подобъекта при поиске
# по всей метрике применяется mapGetCurrentSubject()

    mapSeekNearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekNearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapSeekNearPoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekNearPoint_t (_info, _point, _subject)


# Найти точку на контурах объекта и подобъектов,
# ближайшую к заданной
# hMap    - идентификатор открытой карты,
# info    - идентификатор объекта в памяти
# pointin - координаты точки в прямоугольной
#           системе координат , в метрах на местности
# Возвращает номер точки метрики за которой расположена
# точка на контуре или ноль при ошибке
# Координаты точки (в метрах) помещаются по адресу pointout
# Для определения номера найденного подобъекта при поиске
# по всей метрике применяется mapGetCurrentSubject()

    mapSeekNearVirtualPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekNearVirtualPoint', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPoint(_hMap: maptype.HMAP, _info: maptype.HOBJ, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekNearVirtualPoint_t (_hMap, _info, _pointin, _pointout)


# Запросить у объекта номер текущего подобъекта
# Функция вызывается сразу после поиска точки в
# mapSeekNearPoint,  mapSeekNearVirtualPoint и т.п.
# hObj - идентификатор объекта в памяти
# Возвращает номер подобъекта (начиная с 1) или ноль,
# если текущим контуром является контур объекта

    mapGetCurrentSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCurrentSubject', maptype.HOBJ)
    def mapGetCurrentSubject(_hobj: maptype.HOBJ) -> int:
        return mapGetCurrentSubject_t (_hobj)


# Найти точку на контуре подобъекта,
# ближайшую к заданной
# координаты точки pointin заданы в прямоугольной
# системе координат , в метрах на местности
# hMap    - идентификатор открытой карты,
# info    - идентификатор объекта в памяти
# subject - последовательный номер подобъекта
# ( 0 - объект, 1 - первый подобъект и т.д.)
# Возвращает номер точки метрики за которой расположена
# точка на контуре или ноль при ошибке
# Координаты точки (в метрах) помещаются по адресу pointout

    mapSeekNearVirtualPointSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekNearVirtualPointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPointSubject(_hMap: maptype.HMAP, _obj: maptype.HOBJ, _subject: int, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekNearVirtualPointSubject_t (_hMap, _obj, _subject, _pointin, _pointout)


# Определение координат точки, лежащей на заданном
# расстоянии (по периметру) от заданной точки
# info   - идентификатор объекта в памяти
# number - номер начальной точки
# distance - расстояние
# если distance > = 0 - поиск по направлению цифрования
#               <   0 - поиск против направления цифрования
# point - координаты выходной точки
#         (в прямоугольной системе в метрах на местности)
# subject - номер подобъекта
# Возвращает номер точки, за которой находится или
# c которой совпадает найденная точка
# Если найденная точка в точности совпадает с точкой метрики,
# то возвращается отрицательный номер точки!
# Если запрошенное расстояние превышает длину объекта - возвращает ноль
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekVirtualPointByDistance', maptype.HOBJ, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapSeekVirtualPointByDistance(_info: maptype.HOBJ, _number: int, _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekVirtualPointByDistance_t (_info, _number, _distance, _point, _subject)


# Определение координат точки, лежащей на заданном
# расстоянии (по периметру) от заданной точки
# Расчеты выполняются в системе координат карты без учета проекции
# info   - идентификатор объекта в памяти
# number - номер начальной точки
# distance - расстояние
# если distance > = 0 - поиск по направлению цифрования
#               <   0 - поиск против направления цифрования
# point - координаты выходной точки
#         (в прямоугольной системе в метрах на местности)
# subject - номер подобъекта
# Возвращает номер точки, за которой находится или
# c которой совпадает найденная точка
# Если найденная точка в точности совпадает с точкой метрики,
# то возвращается отрицательный номер точки!
# Если запрошенное расстояние превышает длину объекта - возвращает ноль
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistanceInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekVirtualPointByDistanceInMap', maptype.HOBJ, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapSeekVirtualPointByDistanceInMap(_info: maptype.HOBJ, _number: int, _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekVirtualPointByDistanceInMap_t (_info, _number, _distance, _point, _subject)


# Определение координат точки, лежащей на заданном
# расстоянии (по периметру) от заданной точки с учетом рельефа
# hmap    - идентификатор открытой карты,
# number - номер начальной точки
# distance - расстояние
# если distance > = 0 - поиск по направлению цифрования
#               <   0 - поиск против направления цифрования
# point - координаты выходной точки
#         (в прямоугольной системе в метрах на местности)
# subject - номер подобъекта
# Возвращает номер точки, за которой находится или c которой совпадает
# Если найденная точка в точности совпадает с точкой метрики,
# то возвращается отрицательный номер точки!
# При отсутствии рельефа(матрицы высот,слоев ...) определяет точку без учета рельефа
# При ошибке возвращает ноль

    mapSeekVirtualPointByDistanceWithHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekVirtualPointByDistanceWithHeight', maptype.HMAP, maptype.HOBJ, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapSeekVirtualPointByDistanceWithHeight(_hmap: maptype.HMAP, _info: maptype.HOBJ, _number: int, _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        return mapSeekVirtualPointByDistanceWithHeight_t (_hmap, _info, _number, _distance, _point, _subject)


# Найти точечный объект на заданной карте в окрестности заданной
# точки
# hMap     - идентификатор открытого документа (карты),
# hSite    - идентификатор открытой в документе пользовательской карты,
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска;
# point    - координаты точки в метрах в системе координат документа,
# distance - радиус области поиска в метрах (от 1 мкм до метров)
# visible  - флаг поиска только среди видимых на карте объектов
# При ошибке возвращает ноль

    mapSeekPointObjectByDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekPointObjectByDistance', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_int)
    def mapSeekPointObjectByDistance(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _distance: float, _visible: int = 0) -> int:
        return mapSeekPointObjectByDistance_t (_hmap, _hsite, _info, _point, _distance, _visible)


# Найти точечный объект на заданной карте в окрестности точек
# контура заданного объекта при условии наличия у объекта
# семантики с заданным кодом и значением
# hMap     - идентификатор открытого документа (карты),
# hSite    - идентификатор открытой в документе пользовательской карты,
# source   - идентификатор объекта, вокруг точек которого выполняется поиск
# info     - идентификатор существующего объекта,
#            в котором будет размещен результат поиска;
# distance - радиус области поиска в метрах (от 1 мкм до метров)
# code     - код семантики, который должен быть у найденного объекта (при 0 семантика не учитывается)
# value    - значение семантики, которое должно быть у найденного объекта
#            (при 0 - значение может быть любое)
# visible  - флаг поиска только среди видимых на карте объектов
# При ошибке возвращает ноль

    mapSeekPointObjectByDistanceAndName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekPointObjectByDistanceAndName', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSeekPointObjectByDistanceAndName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _source: maptype.HOBJ, _info: maptype.HOBJ, _distance: float, _code: int, _value: mapsyst.WTEXT, _visible: int = 0) -> int:
        return mapSeekPointObjectByDistanceAndName_t (_hmap, _hsite, _source, _info, _distance, _code, _value.buffer(), _visible)


# #########################################################
#
# Схема запуска:
# =============
# HCROSS hCross = mapCreateObjectsCross(info1,info2,method,precision)
# if (hCross)
#    {
#    while(mapGetNextCross(hCross,info))
#         {
#         ...
#         }
#    mapFreeObjectsCross(hCross);
#    }
###########################################################
# Пересечение двух объектов - нахождение общей части объектов,
# один из которых (ПЕРВЫЙ объект карты) - РЕЗАК(по которому режут)
# другой (ВТОРОЙ объект карты) - ОБ'ЕКТ, КОТОРЫЙ РЕЖУТ.
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# info1 - первый объект карты - РЕЗАК (произвольный контур без подобъектов)
# info2 - второй объект карты (произвольный линейный или площадной объект с подобъектами)
# method - тип результирующих объектов
#          LOCAL_SQUARE - площадной, LOCAL_LINE - линейный
#          тип результирующих объектов зависит от типа второго объекта:
#          - если второй объект незамкнутый, то тип только LOCAL_LINE,
#          - если второй объект замкнутый, то тип может быть LOCAL_LINE или LOCAL_SQUARE.
# При логическом сложении method и флага проверки входимости (FLAGINSIDEOBJECTS = 32
# см. maptype.h) в класс пересечения будут добавлены объекты, которые полностью входят
# в объект - РЕЗАК  (напр. LOCAL_SQUARE | FLAGINSIDEOBJECTS)
# precision - точность при дотягивании (в метрах) или 0
# При отсутствии пересечения или при ошибке возвращает ноль

    mapCreateObjectsCross_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSS,'mapCreateObjectsCross', maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapCreateObjectsCross(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _method: int, _precision: float) -> maptype.HCROSS:
        return mapCreateObjectsCross_t (_info1, _info2, _method, _precision)


# Пересечение двух объектов
# Освобождение класса пересечения

    mapFreeObjectsCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectsCross', maptype.HCROSS)
    def mapFreeObjectsCross(_hCross: maptype.HCROSS) -> ctypes.c_void_p:
        return mapFreeObjectsCross_t (_hCross)


# Пересечение двух объектов
# Запросить объект
# info - результат
# При ошибке возвращает ноль

    mapGetNextCross_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapGetNextCross', maptype.HCROSS, maptype.HOBJ)
    def mapGetNextCross(_hCross: maptype.HCROSS, _info: maptype.HOBJ) -> maptype.HOBJ:
        return mapGetNextCross_t (_hCross, _info)


# Запрос на пересечение двух объектов
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# info1 - первый объект карты
# info2 - второй объект карты
# Если объекты пересекаются, возвращает 1
# При ошибке или неверном типе объектов возвращает ноль

    mapGetObjectsCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectsCross', maptype.HOBJ, maptype.HOBJ)
    def mapGetObjectsCross(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapGetObjectsCross_t (_info1, _info2)


# Объединение(сшивка) двух объектов
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# Не допускается сшивать замкнутый и незамкнутый объекты
# info1 - первый объект карты
# info2 - второй объект карты
# info -  идентификатор объекта, в который будет записана сшитая метрика двух объектов
# method - тип результирующего объекта
#          LOCAL_SQUARE - площадной
#          (на входе только два площадных или линейных замкнутых объекта),
#          LOCAL_LINE - линейный
#          (на входе два площадных или линейных замкнутых объекта или два незамкнутых объекта)
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# При успешном выполнении возвращает ненулевое значение (параметр info)
# При ошибке возвращает ноль

    mapGetObjectsUnion_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapGetObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapGetObjectsUnion(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _info: maptype.HOBJ, _method: int, _precision: float) -> maptype.HOBJ:
        return mapGetObjectsUnion_t (_info1, _info2, _info, _method, _precision)


# Объединение (сшивка) двух площадных объектов (типа "Кварталы")
# Только для ПЛОЩАДНЫХ (типа "Кварталы")
# Если вторая ближайшая связь меньше precision, то сшивка
# выполняется по всем точкам, попавшим в precision
# info1     - первый объект карты
# info2     - второй объект карты
# info      - идентификатор объекта, в который будет записан результат
# precision - допуск при дотягивании (в метрах);
#             при превышении допуска сшивка выполняется через три
#             ближайших точки (точка одного объекта, отрезок - другого)
# flag      - флаг обработки
#             0 - сшить с предварительной проверкой на пересечение
#             1 - не используется
#             2 - сшить непересекающиеся объекты, расположенные
#                 на расстоянии от 0 до precision (без предварительной проверки)
# При успешном выполнении возвращает ненулевое значение (параметр info)
# При ошибке возвращает ноль

    mapSquareObjectsUnion_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSquareObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_int)
    def mapSquareObjectsUnion(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _info: maptype.HOBJ, _precision: float, _flag: int) -> maptype.HOBJ:
        return mapSquareObjectsUnion_t (_info1, _info2, _info, _precision, _flag)


# Вырезать из полигона другой полигон
# hMap    - идентификатор открытого документа (карты),
# object  - обрабатываемый объект (если это мультиполигон, то на выходе - мультиполигон)
# templet - объект-шаблон для вырезания
# Если образуется более 1 внешнего контура, то создается мультиполигон
# Для сохранения объекта на карте вызвать mapCommitObject()
# Возвращает число сформированных контуров объекта
# При ошибке возвращает ноль

    mapCutPolygonByPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCutPolygonByPolygon', maptype.HMAP, maptype.HOBJ, maptype.HOBJ)
    def mapCutPolygonByPolygon(_hmap: maptype.HMAP, _object: maptype.HOBJ, _templet: maptype.HOBJ) -> int:
        return mapCutPolygonByPolygon_t (_hmap, _object, _templet)


# Создать точки пересечений выделенных объектов
# hMap      - идентификатор открытого документа (карты),
# precision - максимальное расстояние между точками, считающимися общими
# Обрабатываются площадные и линейные объекты с помощью функции mapTotalSeekObject
# При ошибке возвращает ноль

    mapCreateIntersectionPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateIntersectionPoints', maptype.HMAP, ctypes.c_double)
    def mapCreateIntersectionPoints(_hmap: maptype.HMAP, _precision: float) -> int:
        return mapCreateIntersectionPoints_t (_hmap, _precision)


# #########################################################
# Схема запуска:
# =============
# HCROSSCONS hCross = mapCreateObjectsConsent(info1,info2,method,precision)
# if (hCross)
# {
#   while(mapGetNextConsent(hCross,info))
#   {
#     ...
#   }
#   mapFreeObjectsConsent(hCross);
# }
# ##########################################################
# Согласование двух объектов, т.е. нахождение внешней части
# исходного объекта, которая примыкает к другому объекту и
# имеет с ним общую часть контура.
# Создание класса согласования
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
# info1 - первый объект карты, по которому согласовывают внешний контур второго объекта
#         (это произвольный замкнутый контур без подобъектов)
# info2 - второй объект карты, у которого нужно найти внешнюю часть,
#         примыкающую к первому объекту и имеющему с ним общую часть контура
#         (это произвольный линейный или площадной объект с подобъектами)
# method - тип результирующих объектов
#          LOCAL_SQUARE - площадной, LOCAL_LINE - линейный
#          тип результирующих объектов зависит от типа
#          второго объекта:
#          - если второй объект незамкнутый, то тип только LOCAL_LINE,
#          - если второй объект замкнутый, то тип может быть LOCAL_LINE или LOCAL_SQUARE.
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# Возвращает указатель на класс согласования
# При ошибке возвращает ноль

    mapCreateObjectsConsent_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSCONS,'mapCreateObjectsConsent', maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapCreateObjectsConsent(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _method: int, _precision: float) -> maptype.HCROSSCONS:
        return mapCreateObjectsConsent_t (_info1, _info2, _method, _precision)


# Согласование двух объектов
# Освобождение класса согласования
# hCross - указатель на класс согласования

    mapFreeObjectsConsent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectsConsent', maptype.HCROSSCONS)
    def mapFreeObjectsConsent(_hCross: maptype.HCROSSCONS) -> ctypes.c_void_p:
        return mapFreeObjectsConsent_t (_hCross)


# Согласование двух объектов
# Запросить объект
# hCross - указатель на класс согласования
# info   - результат
# При ошибке возвращает ноль

    mapGetNextConsent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetNextConsent', maptype.HCROSSCONS, maptype.HOBJ)
    def mapGetNextConsent(_hCross: maptype.HCROSSCONS, _info: maptype.HOBJ) -> int:
        return mapGetNextConsent_t (_hCross, _info)


# ##########################################################
# Схема запуска:
# =============
# HCROSSPOINTS hCross = mapCreateObjectCrossPoints(info1,info2)
# CROSSPOINT point;
# if (hCross)
# {
#   int count = mapGetCrossCount(hCross);
#   for(int i = 1; i <= count; i++)
#   {
#     mapGetCrossPoint(hCross,i,(HPOINT)&point);
#     ...
#   }
#   mapFreeCrossPoints(hCross);
# }
# ##########################################################
# Нахождение точек пересечения двух объектов
# Создание класса точек пересечения
# info1 - первый объект карты ( линейный,площадной )
# info2 - второй объект карты ( линейный,площадной )
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# Возвращает указатель на класс пересечения
# При ошибке возвращает ноль

    mapCreateObjectCrossPointsEx_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateObjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCreateObjectCrossPointsEx(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _precision: float) -> maptype.HCROSSPOINTS:
        return mapCreateObjectCrossPointsEx_t (_info1, _info2, _precision)


# Нахождение точек пересечения двух объектов
# Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов !!!
# Создание класса точек пересечения
# info1 - первый объект карты
# info2 - второй объект карты
# Возвращает указатель на класс пересечения
# При ошибке возвращает ноль

    mapCreateObjectCrossPoints_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateObjectCrossPoints', maptype.HOBJ, maptype.HOBJ)
    def mapCreateObjectCrossPoints(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> maptype.HCROSSPOINTS:
        return mapCreateObjectCrossPoints_t (_info1, _info2)


# Нахождение точек пересечения двух объектов
# Запросить количество точек пересечения
# hCross - указатель на класс согласования
# При ошибке возвращает ноль

    mapGetCrossCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCrossCount', maptype.HCROSSPOINTS)
    def mapGetCrossCount(_hCross: maptype.HCROSSPOINTS) -> int:
        return mapGetCrossCount_t (_hCross)


# Нахождение точек пересечения двух объектов
# Запросить точку
# hCross - указатель на класс согласования
# number - номер точки (с 1)
# point  - точка (КООРДИНАТЫ В МЕТРАХ НА МЕСТНОСТИ)
# При ошибке возвращает ноль

    mapGetCrossPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCrossPoint', maptype.HCROSSPOINTS, ctypes.c_int, maptype.HPOINT)
    def mapGetCrossPoint(_hCross: maptype.HCROSSPOINTS, _number: int, _point: maptype.HPOINT) -> int:
        return mapGetCrossPoint_t (_hCross, _number, _point)


# Нахождение точек пересечения двух объектов
# Освобождение класса
# hCross - указатель на класс согласования

    mapFreeCrossPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeCrossPoints', maptype.HCROSSPOINTS)
    def mapFreeCrossPoints(_hCross: maptype.HCROSSPOINTS) -> ctypes.c_void_p:
        return mapFreeCrossPoints_t (_hCross)


# #########################################################
# Схема запуска:
# =============
# HCROSSPOINTS hCross = mapCreateSubjectCrossPoints(info1,info2,
#                                                  subject1, subject2)
# CROSSPOINT point;
# if (hCross)
# {
#    int count = mapGetCrossCount(hCross);
#    for(int i = 1; i <= count; i++)
#    {
#      mapGetCrossPoint(hCross,i,(HPOINT)&point);
#      ...
#    }
#    mapFreeCrossPoints(hCross);
# }
###########################################################
# Нахождение точек пересечения двух объектов/подобъектов
# Создание класса точек пересечения
# info1 - первый объект карты
# info2 - второй объект карты
# subject1 - номер подобъекта info1
# subject2 - номер подобъекта info2
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# Возвращает указатель на класс пересечения
# При ошибке возвращает ноль

    mapCreateSubjectCrossPointsEx_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateSubjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapCreateSubjectCrossPointsEx(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _subject1: int, _subject2: int, _precision: float) -> maptype.HCROSSPOINTS:
        return mapCreateSubjectCrossPointsEx_t (_info1, _info2, _subject1, _subject2, _precision)


# Нахождение точек пересечения двух объектов/подобъектов
# Создание класса точек пересечения
# info1 - первый объект карты
# info2 - второй объект карты
# subject1 - номер подобъекта info1
# subject2 - номер подобъекта info2
# Возвращает указатель на класс пересечения
# При ошибке возвращает ноль

    mapCreateSubjectCrossPoints_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateSubjectCrossPoints', maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapCreateSubjectCrossPoints(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _subject1: int, _subject2: int) -> maptype.HCROSSPOINTS:
        return mapCreateSubjectCrossPoints_t (_info1, _info2, _subject1, _subject2)


# Добавить точки пересечения объектов в метрику
# При ошибке или отсутствии пересечения возвращает 0
# info1 - первый объект карты
# info2 - второй объект карты
# При ошибке возвращает ноль

    mapInsertPointCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsertPointCross', maptype.HOBJ, maptype.HOBJ)
    def mapInsertPointCross(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapInsertPointCross_t (_info1, _info2)


# Определить пересечение контуров (точек метрики) двух объектов с учетом подобъектов
# info1 - первый объект карты
# info2 - второй объект карты
# При наличии пересечений контуров возвращает ненулевое значение
# При ошибке возвращает 0

    mapCheckCrossObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckCrossObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckCrossObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckCrossObject_t (_info1, _info2)


# Определить пересечение контуров (подобъектов) двух объектов
# info1 - первый объект карты
# info2 - второй объект карты (может быть равен info1)
# subject1 - номер подобъекта info1
# subject2 - номер подобъекта info2
# precision - точность определения близости точек и контуров
# При наличии пересечений контуров возвращает ненулевое значение
# Если info1 = info2 и subject1 = subject2, то возвращает 1
# При ошибке возвращает 0

    mapCheckCrossSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckCrossSubject', maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapCheckCrossSubject(_info1: maptype.HOBJ, _subject1: int, _info2: maptype.HOBJ, _subject2: int, _precision: float) -> int:
        return mapCheckCrossSubject_t (_info1, _subject1, _info2, _subject2, _precision)


# Определить пересечение замкнутого контура объектом
# info1 - замкнутый контур
# info2 - произвольный объект с подобъектами
# precision - допуск для проверки совпадения точек
# Возвращает ненулевое значение, если в результате пересечения объект info2
# разбивается на части
# При ошибке возвращает 0

    mapCheckCrossExclusiveObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckCrossExclusiveObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckCrossExclusiveObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _precision: float) -> int:
        return mapCheckCrossExclusiveObject_t (_info1, _info2, _precision)


# Определить взаиморасположение двух объектов без учета подобъектов
# Учитываются только нулевые контура
# info1 - первый объект карты
# info2 - второй объект карты
# Возвращает: 1 - первый объект внутри второго,
#             2 - второй объект внутри первого,
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
# Значение 3 возвращается всегда при наличии пересечения нулевых контуров
# Значения 1 и 2 - только для замкнутых объектов
# При ошибке возвращает ноль

    mapCheckInsideObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckInsideObject_t (_info1, _info2)


# Определить взаиморасположение двух контуров
# info1    - первый объект карты
# subject1 - номер первого контура с нуля
# info2    - второй объект карты
# subject2 - номер второго контура с нуля
# Возвращает: 1 - первый контур внутри второго,
#             2 - второй контур внутри первого,
#             3 - контура пересекаются,
#             4 - контура не пересекаются
# Значение 3 возвращается всегда при наличии пересечения контуров
# Значения 1 и 2 - только для замкнутых контуров
# При ошибке возвращает ноль

    mapCheckInsideSubjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideSubjectEx', maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapCheckInsideSubjectEx(_info1: maptype.HOBJ, _subject1: int, _info2: maptype.HOBJ, _subject2: int) -> int:
        return mapCheckInsideSubjectEx_t (_info1, _subject1, _info2, _subject2)


# Определить вхождение первого объекта во второй (включая подобъекты)
# info1 - первый объект карты
# info2 - второй объект карты
# Возвращает: 1 - первый объект внутри второго (второй объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - первый объект не внутри второго (возможно пересечение объектов)
# При ошибке возвращает ноль

    mapCheckInsideFirstObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideFirstObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideFirstObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckInsideFirstObject_t (_info1, _info2)


# Определить взаиморасположение двух объектов с учетом подобъектов
# Попадание контура в подобъект внешнего контура считается внешним расположением
# Возвращает: 1 - первый объект внутри внешнего контура второго
#             2 - второй объект внутри внешнего контура первого
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
# Значение 3 возвращается всегда при наличии пересечения любых контуров
# Значения 1 и 2 - только для замкнутых объектов
# Для мультиполигонов значения 1 и 2 возвращаются при выполнении условия для
# любой пары внешних контуров
# При ошибке возвращает 0

    mapCheckInsideObjectAndSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideObjectAndSubject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectAndSubject(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckInsideObjectAndSubject_t (_info1, _info2)


# Определить взаиморасположение двух объектов с учетом подобъектов
# Возвращает: 1 - первый объект внутри второго всеми внешними контурами
#             2 - второй объект внутри первого всеми внешними контурами
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
#             5 - внешние контура первого объекта внутри и снаружи второго
#             6 - внешние контура второго объекта внутри и снаружи первого
# При ошибке возвращает 0

    mapCheckInsideObjectTotal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideObjectTotal', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectTotal(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckInsideObjectTotal_t (_info1, _info2)


# Определить взаиморасположение двух объектов (включая подобъекты)
# info1 - первый объект карты
# info2 - второй объект карты
# Возвращает: 1 - первый объект внутри второго
#                (второй объект должен быть замкнутым),
#           - 1 - первый объект внутри подобъекта второго объекта
#                (второй объект должен быть замкнутым),
#             2 - второй объект внутри первого
#                (первый объект должен быть замкнутым),
#           - 2 - второй объект внутри подобъекта первого объекта
#                (первый объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
# При ошибке возвращает ноль

    mapCheckInsideObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideObjectEx', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectEx(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> int:
        return mapCheckInsideObjectEx_t (_info1, _info2)


# Открыть класс для проверки пересечений пар объектов - базового с остальными
# info - идентификатор базового объекта
# Возвращает идентификатор открытого класса
# После завершения использования необходимо закрыть класс в mapCloseCheckInsideBaseObject
# При ошибке возвращает 0

    mapOpenCheckInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenCheckInsideBaseObject', maptype.HOBJ)
    def mapOpenCheckInsideBaseObject(_info: maptype.HOBJ) -> ctypes.c_void_p:
        return mapOpenCheckInsideBaseObject_t (_info)


# Определить взаиморасположение двух объектов с учетом подобъектов
# hcheck - идентификатор открытого класса проверки пересечений (первый объект)
# test   - идентификатор проверяемого объекта на пересечение (второй объект)
# list   - указатель на отсортированный список номеров подобъектов, с которыми пересекаются габариты шаблона
#          (устанавливается при выполнении функции mapCheckInsideBaseObjectEx)
# count  - указатель число номеров в списке
#          (устанавливается при выполнении функции mapCheckInsideBaseObjectEx)
# Возвращает: 1 - первый объект внутри второго всеми внешними контурами
#             2 - второй объект внутри первого всеми внешними контурами
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
#             5 - внешние контура первого объекта внутри и снаружи второго
#             6 - внешние контура второго объекта внутри и снаружи первого
#             7 - внешние контура второго объекта совпадают с подобъектами первого
# При ошибке возвращает 0

    mapCheckInsideBaseObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideBaseObjectEx', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_int))
    def mapCheckInsideBaseObjectEx(_hcheck: ctypes.c_void_p, _test: maptype.HOBJ, _list: ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), _count: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCheckInsideBaseObjectEx_t (_hcheck, _test, _list, _count)

    mapCheckInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideBaseObject', ctypes.c_void_p, maptype.HOBJ)
    def mapCheckInsideBaseObject(_hcheck: ctypes.c_void_p, _test: maptype.HOBJ) -> int:
        return mapCheckInsideBaseObject_t (_hcheck, _test)


# Обновить описание первого объекта после редактирования

    mapUpdateInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUpdateInsideBaseObject', ctypes.c_void_p)
    def mapUpdateInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapUpdateInsideBaseObject_t (_hcheck)


# Освободить ресурсы, выделенные в mapOpenCheckInsideBaseObject

    mapCloseCheckInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseCheckInsideBaseObject', ctypes.c_void_p)
    def mapCloseCheckInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseCheckInsideBaseObject_t (_hcheck)


# Проверить совпадение метрики
# Каждая пара контуров, все отрезки которых совпадают, считаются совпадающими
# (независимо от направления цифрования, положения начальных точек и
# последовательности контуров). Анализ контуров площадных объектов
# может выполняться с учетом признаков внешних и внутренних контуров
# info1     - объект 1
# info2     - объект 2
# subject1  - подобъект объекта 1. Если subject1 = -1, то проверяются все подобъекты
# subject2  - подобъект объекта 2. Если subject2 = -1, то проверяются все подобъекты
# precision - точность сравнения точек метрики
# flag      - тип обработки двух площадных объектов
#           Определение числа пар:
#             1 - совпадающих внешних контуров
#             2 - совпадающих внутренних контуров
#             3 - совпадающих внешних и внутренних контуров
#           Определение наличия хотя бы одной пары:
#            -1 - совпадающих внешних контуров
#            -2 - совпадающих внутренних контуров
#            -3 - совпадающих внешних и внутренних контуров
#           В остальных случаях тип обработки считается равным 0:
#             0 - определение наличия хотя бы одной пары совпадающих контуров
#                 (без учета признаков внешних и внутренних контуров)
# Возвращает число пар совпадающих контуров
# При ошибке возвращает ноль

    mapCompareMetrics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareMetrics', maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def mapCompareMetrics(_info1: maptype.HOBJ, _subject1: int, _info2: maptype.HOBJ, _subject2: int, _precision: float, _flag: int) -> int:
        return mapCompareMetrics_t (_info1, _subject1, _info2, _subject2, _precision, _flag)


# Проверить точки объектов на совпадение в заданном допуске
# info1 - идентификатор первого объекта,
# info2 - идентификатор второго объекта,
# delta - допуск в метрах на местности для сравнения координат точек объекта на совпадение
# Если число точек объектов совпадает и координаты отличаются в пределах заданного
# допуска, то возвращается ненулевое значения
# При ошибке возвращает ноль

    mapCompareObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCompareObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _delta: float) -> int:
        return mapCompareObject_t (_info1, _info2, _delta)


# Определить взаиморасположение двух объектов (включая подобъекты)
# Возвращает: 1 - первый объект внутри второго
#                (второй объект должен быть замкнутым),
#           - 1 - первый объект внутри подобъекта второго объекта
#                (второй объект должен быть замкнутым),
#             2 - второй объект внутри первого
#                (первый объект должен бытьо замкнутым),
#           - 2 - второй объект внутри подобъекта первого объекта
#                (первый объект должен быть замкнутым),
#             3 - объекты пересекаются,
#             4 - объекты не пересекаются
#             5 - объекты(подобъекты) имеют общие отрезки или общую точку
# в point возвращаются координаты в метрах первой точки пересечения
# При ошибке возвращает ноль

    mapCheckInsideObjectPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideObjectPoint', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCheckInsideObjectPoint(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCheckInsideObjectPoint_t (_info1, _info2, _point)


# Определить вхождение всех точек контура подобъекта в другой контур подобъекта
# info1    - идентификатор первого объекта,
# subject1 - номер подобъекта первого объекта (0 - контур объекта),
# info2    - идентификатор второго объекта,
# subject2 - номер подобъекта второго объекта (0 - контур объекта),
# Возвращает: 1 - все точки внутри объекта/подобъекта и на контуре,
#             2 - есть внешние точки (хотя бы одна, а может и все),
#             3 - все точки контуров совпадают,
#             4 - все точки лежат на отрезке метрики или совпадают,
# При ошибке возвращает ноль

    mapCheckInsideSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsideSubject', maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapCheckInsideSubject(_info1: maptype.HOBJ, _subject1: int, _info2: maptype.HOBJ, _subject2: int) -> int:
        return mapCheckInsideSubject_t (_info1, _subject1, _info2, _subject2)


# Определить взаиморасположение замкнутого объекта и точки
# info    - идентификатор объекта,
# subject - номер объекта(0) или подобъекта, если равно -1, то проверяются все контура,
#           учитывая мультиполигоны
# point   - координаты проверяемой точки в метрах.
# Возвращает: 1 - точка внутри объекта(подобъекта),
#             2 - точка за пределами объекта(подобъекта),
#             3 - точка совпадает с точкой метрики,
#             4 - точка лежит на отрезке.
# При ошибке возвращает ноль

    mapCheckInsidePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckInsidePoint', maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCheckInsidePoint(_info: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCheckInsidePoint_t (_info, _subject, _point)


# Определить взаиморасположение области и объекта
# info - идентификатор объекта,
# area - область (обязательно замкнута и без подобъектов,
#                 т.к. подобъекты области не учитываются )
# precision - точность (в метрах)
# Возвращает: 1 - область внутри объекта
#                (в этом случае объект д.б. обязательно замкнутым),
#             2 - объект внутри области
#             3 - область и объект пересекаются,
#             4 - область и объект не пересекаются
#             5 - объект касается области и лежит внутри нее
#             6 - объект касается области и лежит снаружи
# При ошибке возвращает ноль

    mapCheckOverlap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckOverlap', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckOverlap(_area: maptype.HOBJ, _info: maptype.HOBJ, _precision: float = 0) -> int:
        return mapCheckOverlap_t (_area, _info, _precision)


# Найти пересечение двух отрезков
# xy1,xy2 - первый отрезок,
# xy3,xy4 - второй отрезок
# point1,point2  - точки пересечения
# precision - точность (в метрах)
# Возврат : 1 - одна точка пересечения,
#           2 - отрезок xy1,xy2 лежит  на отрезке xy3,xy4
# При отсутствии точки пересечения или ошибке возвращает ноль

    mapCrossCutData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCrossCutData', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCrossCutData(_xy1: ctypes.POINTER(maptype.DOUBLEPOINT), _xy2: ctypes.POINTER(maptype.DOUBLEPOINT), _xy3: ctypes.POINTER(maptype.DOUBLEPOINT), _xy4: ctypes.POINTER(maptype.DOUBLEPOINT), _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float = maptype.DELTANULL) -> int:
        return mapCrossCutData_t (_xy1, _xy2, _xy3, _xy4, _point1, _point2, _precision)


# Пересечение отрезка и метрики объекта / подобъекта
# xy1, xy2 - координаты отрезка
# data - метрика объекта/подобъекта
# subject - номер объекта/подобъекта
# ( 0 - объект, 1 - первый подобъект и т.д.)
# first - номер первой точки участка
# last  - номер последней точки участка
# Возвращает две структуры NUMBERPOINT, включающие
# номер точки метрики, после которой
# находится точка пересечения и
# структуру DOUBLEPOINT - координаты точки пересечения
# Две структуры заполняются если отрезок xy1,xy2 лежит
# на отрезке метрики
# При отсутствии точек пересечения или ошибке возвращает ноль

    mapCrossCutAndSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCrossCutAndSubject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.NUMBERPOINT), ctypes.POINTER(maptype.NUMBERPOINT), ctypes.c_int, ctypes.c_double)
    def mapCrossCutAndSubject(_info: maptype.HOBJ, _xy1: ctypes.POINTER(maptype.DOUBLEPOINT), _xy2: ctypes.POINTER(maptype.DOUBLEPOINT), _first: int, _last: int, _point1: ctypes.POINTER(maptype.NUMBERPOINT), _point2: ctypes.POINTER(maptype.NUMBERPOINT), _subject: int, _precision: float) -> int:
        return mapCrossCutAndSubject_t (_info, _xy1, _xy2, _first, _last, _point1, _point2, _subject, _precision)


# Положение точки относительно отрезка
# point     - координаты
# xy1,xy2   - координаты концов отрезка
# precision - точность
# Возвращает POINTPOSITION (PS_FIRST, PS_LEFT... - maptype.h)
# При ошибке возвращает 0

    mapGetPointPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPointPosition', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapGetPointPosition(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _xy1: ctypes.POINTER(maptype.DOUBLEPOINT), _xy2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float = maptype.DELTANULL) -> int:
        return mapGetPointPosition_t (_point, _xy1, _xy2, _precision)


# Определение двух точек по перпендикуляру от отрезка (point1-point2)
# на расстоянии (+/-) distance от произвольной точки point (по умолчанию point1)
# pointout1, pointout2 - координаты требуемых точек
# point1,point2        - координаты концов отрезка
# point                - произвольная точка, от которой производиться расчет
# distance             - растояние от точки point
# При ошибке возвращает ноль

    mapSeekPointNormalLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekPointNormalLine', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointNormalLine(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout2: ctypes.POINTER(maptype.DOUBLEPOINT), _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT) = None) -> int:
        return mapSeekPointNormalLine_t (_point1, _point2, _pointout1, _pointout2, _distance, _point)


# #########################################################
# Схема запуска:
# =============
# HCROSS hCross = mapCreateObjectCutByLine(info1,info2,method,precision)
# if (hCross)
# {
#   while(mapGetNextCut(hCross,info))
#   {
#     ...
#   }
#   mapFreeObjectsCut(hCross);
# }
###########################################################
# Рассечение замкнутого объекта по линии
# Создание класса рассечения
# info1 - линия без подобъектов, по которой режут
# info2 - замкнутый объект, который режут (произвольный,c подобъектами)
# method - метод нарезки объектов:
#          LOCAL_LINE - линейный,
#          LOCAL_SQUARE - площадной
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# Возвращает указатель на класс разрезания
# При ошибке возвращает ноль

    mapCreateObjectCutByLine_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSS,'mapCreateObjectCutByLine', maptype.HOBJ, maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapCreateObjectCutByLine(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _method: int, _precision: float) -> maptype.HCROSS:
        return mapCreateObjectCutByLine_t (_info1, _info2, _method, _precision)


# Рассечение замкнутого объекта по линии
# Освобождение класса рассечения
# hCross - указатель на класс разрезания

    mapFreeObjectsCut_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectsCut', maptype.HCROSS)
    def mapFreeObjectsCut(_hCross: maptype.HCROSS) -> ctypes.c_void_p:
        return mapFreeObjectsCut_t (_hCross)


# Рассечение замкнутого объекта по линии
# Запросить объект
# hCross - указатель на класс разрезания
# info   - результат
# При ошибке возвращает ноль

    mapGetNextCut_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapGetNextCut', maptype.HCROSS, maptype.HOBJ)
    def mapGetNextCut(_hCross: maptype.HCROSS, _info: maptype.HOBJ) -> maptype.HOBJ:
        return mapGetNextCut_t (_hCross, _info)


# #########################################################
# Схема запуска:
# =============
# HCROSS hCross = mapCreateObjectsCrossSquare(info1,info2,method,precision)
# if (hCross)
#   {
#    while(mapGetNextCross(hCross,info))
#    {
#      ...
#    }
#    mapFreeObjectsCross(hCross);
#   }
###########################################################
# Создание класса пересечения двух площадных объектов(с учетом ВСЕХ подобъектов)
# Только для ПЛОЩАДНЫХ объектов !!!
# info1 - первый объект карты - РЕЗАК (произвольный площадной объект с подобъектами)
# info2 - второй объект карты (произвольный площадной объект с подобъектами)
# precision - точность при дотягивании (в метрах), при precision=0 устанавливается точность
#             0.001 для карт масштаба <= 500000,
#             0.01 для карт масштаба более 500000, если precision больше предложенной, то
#             устанавливается большее значение
# Возвращает указатель на класс пересечения
# При ошибке возвращает ноль

    mapCreateObjectsCrossSquare_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSS,'mapCreateObjectsCrossSquare', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCreateObjectsCrossSquare(_info1: maptype.HOBJ, _info2: maptype.HOBJ, _precision: float) -> maptype.HCROSS:
        return mapCreateObjectsCrossSquare_t (_info1, _info2, _precision)


# Установить допуск при удалении одинаковых точек
# info - объект карты
# precision - предлагаемый допуск или 0 (в метрах)
# возвращает реальный допуск

    mapSetPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetPrecision', maptype.HOBJ, ctypes.c_double)
    def mapSetPrecision(_info: maptype.HOBJ, _precision: float) -> float:
        return mapSetPrecision_t (_info, _precision)


# Выполнить вырезание контуров одного набора площадных объектов из другого набора площадных объектов
# hwnd      - идентификатор окна,которое будет извещаться
#             (для отмены сообщений установить идентификатор в ноль)
# Процесс посылает сообщение WM_PROGRESSBARUN
# wparm : процент обработки,
# Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# hmap - идентификатор открытого документа
# editset - номер набора редактируемых объектов в файле OBR карты в папке \LOG
# tempset - номер набора вырезаемых объектов в файле OBR карты в папке \LOG
# adjust  - признак согласования контуров вырезаемых объектов с редактируемыми объектами
# multi   - признак формирования мультиполигона при делении контура редактируемого объекта на части
# Возвращает число обработанных контуров, если ни в одном контуре не было вырезания - возвращает -1
# При ошибке возвращает ноль

    mapCutObjectListFromList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCutObjectListFromList', maptype.HMESSAGE, maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapCutObjectListFromList(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _editset: int, _tempset: int, _adjust: int, _multi: int) -> int:
        return mapCutObjectListFromList_t (_hmessage, _hmap, _editset, _tempset, _adjust, _multi)


# #########################################################
# Схема запуска:
# =============
# HOBJSET hObjSet = mapCreateObjectSet()
# if (hObjSet)
#   {
#     ... функции класса
#     mapFreeObjectSet(hObjSet);
#   }
###########################################################
# Создание класса набора объектов, объединенных по семантической
# характеристике
# При ошибке возвращает ноль

    mapCreateObjectSet_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJSET,'mapCreateObjectSet')
    def mapCreateObjectSet() -> maptype.HOBJSET:
        return mapCreateObjectSet_t ()


# Освобождение класса набора объектов, объединенных по семантической
# характеристике
# hobjset - указатель на набора объектов

    mapFreeObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectSet', maptype.HOBJSET)
    def mapFreeObjectSet(_hobjset: maptype.HOBJSET) -> ctypes.c_void_p:
        return mapFreeObjectSet_t (_hobjset)


# Построение группы из объектов карты
# по существующей в объекте групповой семантике
# hobjset - указатель на набора объектов
# info    - идентификатор объекта карты
# При ошибке возвращает ноль

    mapBuildObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildObjectSet', maptype.HOBJSET, maptype.HOBJ)
    def mapBuildObjectSet(_hobjset: maptype.HOBJSET, _info: maptype.HOBJ) -> int:
        return mapBuildObjectSet_t (_hobjset, _info)


# Построение группы из объектов карты
# по определенному типу существующей в объекте групповой семантике
# hobjset - указатель на набора объектов
# info    - идентификатор объекта карты
# type    - тип семантической характеристики для поиска в info
#           GROUPLEADER, GROUPSLAVE, GROUPPARTNER
# если type = 0 - ищет первую попавшуюся групповую семантику
# ( функция mapBuildObjectSet );
# При ошибке возвращает ноль

    mapBuildObjectSetByType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildObjectSetByType', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapBuildObjectSetByType(_hobjset: maptype.HOBJSET, _info: maptype.HOBJ, _type: int) -> int:
        return mapBuildObjectSetByType_t (_hobjset, _info, _type)


# Построение группы из объектов карты
# по определенному типу существующей в объекте групповой семантике
# и номеру группы (объект может принадлежать нескольким группам)
# hobjset - указатель на набора объектов
# info    - идентификатор объекта карты
# type    - тип семантической характеристики для поиска в info
#           GROUPLEADER, GROUPSLAVE, GROUPPARTNER
# если type = 0 - ищет первую попавшуюся групповую семантику
# ( функция mapBuildObjectSet );
# group   - номер группы
# При ошибке возвращает ноль

    mapBuildObjectSetByTypeGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildObjectSetByTypeGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapBuildObjectSetByTypeGroup(_hobjset: maptype.HOBJSET, _info: maptype.HOBJ, _type: int, _group: int) -> int:
        return mapBuildObjectSetByTypeGroup_t (_hobjset, _info, _type, _group)


# Заполнить контекст поиска из объектов набора
# hobjset - указатель на набора объектов
# hselect - условия поиска
# При ошибке возвращает ноль

    mapBuildSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildSelect', maptype.HOBJSET, maptype.HSELECT)
    def mapBuildSelect(_hobjset: maptype.HOBJSET, _hselect: maptype.HSELECT) -> int:
        return mapBuildSelect_t (_hobjset, _hselect)


# Запросить количество объектов в наборе
# hobjset - указатель на набора объектов
# При ошибке возвращает ноль

    mapObjectSetCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetCount', maptype.HOBJSET)
    def mapObjectSetCount(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetCount_t (_hobjset)


# Запросить объект из набора по номеру (начиная с 1)
# Объект HOBJ не нужно создавать !!!
# hobjset - указатель на набора объектов
# number  - номер объекта из набора
# При ошибке возвращает ноль

    mapObjectSetObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapObjectSetObject', maptype.HOBJSET, ctypes.c_int)
    def mapObjectSetObject(_hobjset: maptype.HOBJSET, _number: int) -> maptype.HOBJ:
        return mapObjectSetObject_t (_hobjset, _number)


# Запросить габариты объектов набора
# hobjset - указатель на набора объектов
# frame   - координаты (в метрах) прямоугольной области габаритов набора
# При ошибке возвращает ноль

    mapObjectSetFramePlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetFramePlane', maptype.HOBJSET, ctypes.POINTER(maptype.DFRAME))
    def mapObjectSetFramePlane(_hobjset: maptype.HOBJSET, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectSetFramePlane_t (_hobjset, _frame)


# Назначить главный объект в наборе (приписать семантику 32801)
# hobjset - указатель на набора объектов
# number - порядковый номер объекта в листе (из числа объектов в наборе)
# если number = 0, назначается первый попавшийся объект в наборе
# При ошибке возвращает ноль

    mapObjectSetNominateLeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetNominateLeader', maptype.HOBJSET, ctypes.c_int)
    def mapObjectSetNominateLeader(_hobjset: maptype.HOBJSET, _number: int) -> int:
        return mapObjectSetNominateLeader_t (_hobjset, _number)


# Удалить объект из набора по порядковому номеру (с 1)
# Удаленный заменяется на последний
# Если объект главный в группе - удаляется вся группа
# hobjset - указатель на набора объектов
# number - порядковый номер объекта
# save - сохранить изменения в файл
#  =  0 - не сохранять, 1 - сохранять
# При ошибке возвращает ноль

    mapObjectSetClearObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetClearObject', maptype.HOBJSET, ctypes.c_int, ctypes.c_int)
    def mapObjectSetClearObject(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        return mapObjectSetClearObject_t (_hobjset, _number, _save)


# Удалить все объекты из набора
# hobjset - указатель на набора объектов
# save    - сохранить изменения в файл
#           =  0 - не сохранять, 1 - сохранять

    mapObjectSetClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapObjectSetClear', maptype.HOBJSET, ctypes.c_int)
    def mapObjectSetClear(_hobjset: maptype.HOBJSET, _save: int) -> ctypes.c_void_p:
        return mapObjectSetClear_t (_hobjset, _save)


# Запрос признака группового объекта (по семантике)
# groupnumber - переменная, куда помещается номер группы
# (если он нужен) или 0
# hobjset - указатель на набора объектов
# hobj    - идентификатор объекта
# Возвращает код групповой семантики (GROUPLEADER,GROUPSLAVE,GROUPPARTNER) или ноль

    mapObjectSetIsGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetIsGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.POINTER(ctypes.c_int))
    def mapObjectSetIsGroup(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _groupnumber: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapObjectSetIsGroup_t (_hobjset, _hobj, _groupnumber)


# Запросить наличие групповой семантики данного типа у объекта
# hobjset - указатель на набора объектов
# hobj    - идентификатор объекта
# type -  тип групповой семантики
#        GROUPLEADER, GROUPSLAVE, GROUPPARTNER
# Возвращает номер группы или ноль при отсутствии

    mapObjectSetGetTypeSemn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetGetTypeSemn', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetGetTypeSemn(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int) -> int:
        return mapObjectSetGetTypeSemn_t (_hobjset, _hobj, _type)


# Удалить все объекты набора с карты
# hobjset - указатель на набор объектов
# При ошибке возвращает ноль

    mapObjectSetDelete_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetDelete', maptype.HOBJSET)
    def mapObjectSetDelete(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetDelete_t (_hobjset)


# Удалить групповую семантику из объекта
# group - номер набора
# если group == 0, то используется номер группы класса hobjset
# hobjset - указатель на набора объектов
# hobj    - идентификатор объекта
# При ошибке возвращает ноль

    mapObjectSetDeleteSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetDeleteSemantic', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetDeleteSemantic(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _group: int) -> int:
        return mapObjectSetDeleteSemantic_t (_hobjset, _hobj, _group)


# Отобразить набор
# hobjset - указатель на набор объектов
# hmap    - идентификатор открытой карты
# hDC     - контекст устройства отображения
# rect    - область отображения
# При ошибке возвращает ноль

    mapPaintObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintObjectSet', maptype.HOBJSET, maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT))
    def mapPaintObjectSet(_hobjset: maptype.HOBJSET, _hmap: maptype.HMAP, _hDC: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        return mapPaintObjectSet_t (_hobjset, _hmap, _hDC, _rect)


# Сохранить набор
# hobjset - указатель на набора объектов
# always  - сохранять всегда или только, если были изменения
#         = 0 - были изменения
#         = 1 - всегда
# При ошибке возвращает ноль

    mapObjectSetSave_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetSave', maptype.HOBJSET, ctypes.c_int)
    def mapObjectSetSave(_hobjset: maptype.HOBJSET, _always: int) -> int:
        return mapObjectSetSave_t (_hobjset, _always)


# Восстановить объекты группы на карте
# после операций удаления, перемещения (если не вызывали mapObjectSetSave)
# При ошибке возвращает ноль, иначе - число обработанных объектов
# При ошибке возвращает ноль

    mapObjectSetRevert_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetRevert', maptype.HOBJSET)
    def mapObjectSetRevert(_hobjset: maptype.HOBJSET) -> int:
        return mapObjectSetRevert_t (_hobjset)


# Удалить объект из группы по его номеру на листе (с 1)
# hobjset - указатель на набор объектов
# number  - порядковый номер объекта
# save - сохранение в файл (0 - не сохранять, 1 - сохранять)
# При ошибке возвращает ноль

    mapObjectSetRemoveNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetRemoveNumber', maptype.HOBJSET, ctypes.c_int, ctypes.c_int)
    def mapObjectSetRemoveNumber(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        return mapObjectSetRemoveNumber_t (_hobjset, _number, _save)


# Добавить главный объект группу (с приписыванием семантики 32801)
# hobjset - указатель на набор объектов
# save - сохранение в файл : = 0 - не сохранять, 1 - сохранять
# Если hobj - вновь созданный объект (Key = 0) и save = 1
#             вначале info будет сохранен, а потом добавлен в группу
# Если объект hobj содержит групповую семантику и является главным
# - добавляет в набор, не изменяя групповую семантику
# Если объект hobj содержит групповую семантику и является подчиненным
# - добавляет групповую семантику (создает новую группу не разрушая старую)
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendGeneral_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetAppendGeneral', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetAppendGeneral(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendGeneral_t (_hobjset, _hobj, _save)


# Добавить главный объект группу (с приписыванием семантики 32801) (УСТАРЕВШАЯ ФУНКЦИЯ)
# hobjset - указатель на набор объектов
# save - сохранение в файл : = 0 - не сохранять, 1 - сохранять
# Если hobj - вновь созданный объект (Key = 0) и save = 1
#             вначале info будет сохранен, а потом добавлен в группу
# Если объект hobj содержит групповую семантику и является главным
# - разрушает существующую группу и создает новую
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendGeneralNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetAppendGeneralNew', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetAppendGeneralNew(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendGeneralNew_t (_hobjset, _hobj, _save)


# Добавить подчиненный объект группу (с приписыванием семантики 32802)
# hobjset - указатель на набор объектов
# save - сохранение в файл : = 0 - не сохранять, 1 - сохранять
# Если hobj - вновь созданный объект (Key = 0) и save = 1
#             вначале info будет сохранен, а потом добавлен в группу
# Если объект hobj содержит групповую семантику и является главным
# - добавляет групповую семантику (создает новую группу не разрушая старую)
# Если объект hobj содержит групповую семантику и является подчиненным
# - добавляет в набор, изменяя групповую семантику
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendSubordinate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetAppendSubordinate', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetAppendSubordinate(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendSubordinate_t (_hobjset, _hobj, _save)


# Добавить подчиненный объект группу (с приписыванием семантики 32802) (УСТАРЕВШАЯ ФУНКЦИЯ)
# hobjset - указатель на набор объектов
# save - сохранение в файл : = 0 - не сохранять, 1 - сохранять
# Если hobj - вновь созданный объект (Key = 0) и save = 1
#             вначале info будет сохранен, а потом добавлен в группу
# Если объект hobj содержит групповую семантику и является подчиненным
# - разрушает существующую группу и создает новую
# Возвращает порядковый номер объекта или ноль

    mapObjectSetAppendSubordinateNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetAppendSubordinateNew', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetAppendSubordinateNew(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetAppendSubordinateNew_t (_hobjset, _hobj, _save)


# Найти главный объект в группе
# hobjset - указатель на набор объектов
# group - номер группы
#         при group = 0 - номер группы устанавливается из набора hobjset
# Объект HOBJ не нужно создавать !!!
# При ошибке возвращает ноль

    mapObjectSetFindGeneral_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapObjectSetFindGeneral', maptype.HOBJSET, ctypes.c_int)
    def mapObjectSetFindGeneral(_hobjset: maptype.HOBJSET, _group: int) -> maptype.HOBJ:
        return mapObjectSetFindGeneral_t (_hobjset, _group)


# Объединить наборы hobjset и set
# regime -
#    = 1 -  добавить отдельный объект
#           если объект главный - создать иерархию, включив только его
#           в текущий набор
#           если объект подчиненный или равноправный - включить его в текущий набор,
#           удалив из set
#    = 2 -  весь набор
#           разрушается набор set и все объекты включаются в текущий набор
#    = 3 -  создать иерархию
#           найти главный объект набора set и включить его как подчиненный
#           в текущий набор, создав иерархию
# info - по какому объекту набора set ориентироваться
# Результат помещается в набор hobjset
# save - сохранение в файл
#      =  0 - не сохранять, 1 - сохранять
# При ошибке возвращает ноль

    mapObjectSetUnion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectSetUnion', maptype.HOBJSET, maptype.HOBJSET, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapObjectSetUnion(_hobjset: maptype.HOBJSET, _set: maptype.HOBJSET, _regime: int, _info: maptype.HOBJ, _save: int) -> int:
        return mapObjectSetUnion_t (_hobjset, _set, _regime, _info, _save)


# Вычисление значения характеристики в заданной точке
# по данным векторной карты.]
# hMap - идентификатор открытой векторной карты,
# Характеристика задаётся кодом семантики - semanticCode,поиск заданной
# характеристики выполняется по всем объектам векторной карты.
# Координаты точки (point->X,point->Y) задаются в метрах в
# системе координат векторной карты.
# Вычисленное значение характеристики заносится в value.
# При ошибке возвращает ноль

    mapCalcCharacteristic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCalcCharacteristic', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapCalcCharacteristic(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _semanticCode: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapCalcCharacteristic_t (_hMap, _point, _semanticCode, _value)


# Открыть файл макетов
# name - имя открываемого файла макетов (VCL)
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# Возвращает идентификатор открытого процесса(HVCL)
# Для каждого инициированного и больше не используемого
# идентификатора HVCL необходим вызов функции mapModelFree
# При ошибке возвращает ноль

    mapOpenModelFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenModelFileUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenModelFileUn(_name: mapsyst.WTEXT, _mode: int) -> ctypes.c_void_p:
        return mapOpenModelFileUn_t (_name.buffer(), _mode)


# Запросить число моделей в файле
# При ошибке возвращает ноль

    mapModelCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapModelCount', ctypes.c_void_p)
    def mapModelCount(_hvcl: ctypes.c_void_p) -> int:
        return mapModelCount_t (_hvcl)


# Добавить модель в конец файла
# select - контекст условий поиска, который сохраняется в файл моделей
# name - имя модели
# Возвращает номер записи в файле или 0 при ошибке

    mapAddModelUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAddModelUn', ctypes.c_void_p, maptype.HSELECT, maptype.PWCHAR)
    def mapAddModelUn(_hvcl: ctypes.c_void_p, _hselect: maptype.HSELECT, _name: mapsyst.WTEXT) -> int:
        return mapAddModelUn_t (_hvcl, _hselect, _name.buffer())


# Удалить модель c заданным номером
# number - номер модели в файле
# При ошибке возвращает ноль

    mapDeleteModelByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteModelByNumber', ctypes.c_void_p, ctypes.c_int)
    def mapDeleteModelByNumber(_hvcl: ctypes.c_void_p, _number: int) -> int:
        return mapDeleteModelByNumber_t (_hvcl, _number)


# Удалить модель c заданным именем
# name - имя модели
# При ошибке возвращает ноль

    mapDeleteModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteModelByNameUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapDeleteModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        return mapDeleteModelByNameUn_t (_hvcl, _name.buffer())


# Запросить номер модели по имени модели
# Модель с именем name не найдена возврат = 0
# При ошибке возвращает 0

    mapModelNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapModelNumberUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapModelNumberUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        return mapModelNumberUn_t (_hvcl, _name.buffer())


# Запросить модель по номеру модели
# number - номер модели
# select - контекст условий поиска, в который считывается модель из файла
# При ошибке возвращает ноль

    mapGetModelByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetModelByNumber', ctypes.c_void_p, ctypes.c_int, maptype.HSELECT)
    def mapGetModelByNumber(_hvcl: ctypes.c_void_p, _number: int, _select: maptype.HSELECT) -> int:
        return mapGetModelByNumber_t (_hvcl, _number, _select)


# Запросить модель по имени модели
# name - имя модели
# select - контекст условий поиска, в который считывается модель из файла
# При ошибке возвращает ноль

    mapGetModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapGetModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT, _select: maptype.HSELECT) -> int:
        return mapGetModelByNameUn_t (_hvcl, _name.buffer(), _select)


# Запросить имя модели по номеру
#  1 <= number <= Head.Count
# При ошибке возвращает ноль

    mapModelNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapModelNameUn', ctypes.c_void_p, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapModelNameUn(_hvcl: ctypes.c_void_p, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapModelNameUn_t (_hvcl, _number, _name.buffer(), _namesize)


# Обновить модель с заданным именем
# select - контекст условий поиска, который записывается в файл моделей
# При ошибке возвращает ноль

    mapUpdateModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapUpdateModelByNameUn(_hvcl: ctypes.c_void_p, _modelname: mapsyst.WTEXT, _hselect: maptype.HSELECT) -> int:
        return mapUpdateModelByNameUn_t (_hvcl, _modelname.buffer(), _hselect)


# Закрыть файл макетов

    mapModelFree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapModelFree', ctypes.c_void_p)
    def mapModelFree(_hvcl: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapModelFree_t (_hvcl)


# Восстановить параметры поиска и выделения объектов по области
# hMap -  идентификатор открытых данных
# modelname - имя восстанавливаемой модели условий поиска для всех карт, в том числе:
# "MarkParameters" - имя модели параметров поиска по рамке
# "AreaParameters" - имя модели параметров поиска по области
# В результате устанавливаются и включаются условия поиска и выделения объектов в документе - mapSetTotalSelectFlag(hMap, 1);
# При ошибке возвращает ноль

    mapRestoreTotalSeekSelectModel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreTotalSeekSelectModel', maptype.HMAP, maptype.PWCHAR)
    def mapRestoreTotalSeekSelectModel(_hMap: maptype.HMAP, _modelname: mapsyst.WTEXT) -> int:
        return mapRestoreTotalSeekSelectModel_t (_hMap, _modelname.buffer())

#   TEMPHSELECT_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEMPHSELECT', maptype.HSELECT)
#   def TEMPHSELECT(_value: maptype.HSELECT) -> typedef struct:
#       return TEMPHSELECT_t (_value)

#   TEMPHCROSS_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEMPHCROSS', maptype.HCROSS)
#   def TEMPHCROSS(_value: maptype.HCROSS) -> typedef struct:
#       return TEMPHCROSS_t (_value)

#   TEMPHCROSSPOINTS_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEMPHCROSSPOINTS', maptype.HCROSSPOINTS)
#   def TEMPHCROSSPOINTS(_value: maptype.HCROSSPOINTS) -> typedef struct:
#       return TEMPHCROSSPOINTS_t (_value)

#   TEMPHCROSSCONS_t = mapsyst.GetProcAddress(curLib,typedef struct,'TEMPHCROSSCONS', maptype.HCROSSCONS)
#   def TEMPHCROSSCONS(_value: maptype.HCROSSCONS) -> typedef struct:
#       return TEMPHCROSSCONS_t (_value)

except Exception as e:
    print(e)
    acceslib = 0
