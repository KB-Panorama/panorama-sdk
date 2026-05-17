#!/usr/bin/env python3

# ********************************************************************
# *                                                                  *
# *              Copyright (c) PANORAMA Group 1991-2026              *
# *                      All Rights Reserved                         *
# *                                                                  *
# ********************************************************************
# *                                                                  *
# *                Библиотека геометрических функций                 *
# *                      и оверлейных операций                       *
# *                                                                  *
# *  Функции поиска точек пересечения отрезков:                      *
# *                                                                  *
# *    ovlGetCrossPoint           - Определение точек пересечения    *
# *                                 отрезков                         *
# *    ovlGetCrossPointRealCut    - Определение точек пересечения    *
# *                                 отрезков ненулевой длины         *
# *    ovlCrossTestFrame          - Тест пересечения отрезка         *
# *                                 с прямоугольной рамкой           *
# *    ovlDistance                - Вычисление расстояния между      *
# *                                 точкой и прямой                  *
# *    ovlDistance2               - Вычисление квадрата расстояния   *
# *                                 между точкой и прямой            *
# *    ovlSeekNearPointOnLine     - Поиск точки на линии, ближайшей  *
# *                                 к заданной                       *
# *                                                                  *
# *  Функции запроса положения точки:                                *
# *                                                                  *
# *    ovlGetLocationPoint        - Определение расположения точки   *
# *                                 относительно замкнутого объекта  *
# *                                                                  *
# *  Функции пересечения объектов:                                   *
# *                                                                  *
# *    ovlCreate            - Создать объект оверлейных операций     *
# *    ovlFree              - Освободить объект оверлейных операций  *
# *                                                                  *
# *    ovlSetTemplet        - Установить шаблон для оверлейных       *
# *                           операций                               *
# *    ovlSetObjectCross    - Установить обрабатываемый объект       *
# *                           и метод обработки                      *
# *    ovlGetNextObject     - Запросить очередную часть разрезаемого *
# *                           объекта                                *
# *                                                                  *
# *    ovlIsEditTemplet     - Запросить признак изменения метрики    *
# *                           шаблона                                *
# *    ovlIsEditObject      - Запросить признак изменения метрики    *
# *                           объекта                                *
# *    ovlGetAdjustTemplet  - Запросить метрику шаблона,             *
# *                           согласованную метрикой объекта         *
# *    ovlGetAdjustObject   - Запросить метрику объекта,             *
# *                           согласованную метрикой шаблона         *
# *    ovlGetCheckObject    - Запросить метрику проверенного объекта *
# *                           с удалением двойных точек              *
# *    ovlGetCrossPoints    - Запросить все точки пересечения        *
# *                           шаблона и объекта                      *
# *                                                                  *
# *  Функции запроса описания ошибок:                                *
# *                                                                  *
# *    ovlCreateCheckObject - Создать объект оверлейных операций     *
# *                           для выполения контроля метрики объекта *
# *    ovlGetErrorCode      - Запросить код ошибки                   *
# *    ovlGetError          - Запросить описание ошибки              *
# *    ovlGetErrorUn        - Запросить описание ошибки              *
# *    ovlGetErrorPointX    - Запросить координату X точки,          *
# *                           содержащей ошибку                      *
# *    ovlGetErrorPointY    - Запросить координату Y точки,          *
# *                           содержащей ошибку                      *
# *                                                                  *
# *    ovlGetErrorCount     - Запросить число ошибок                 *
# *                                                                  *
# *    ovlGetErrorCodeN     - Запросить код ошибки по номеру         *
# *    ovlGetErrorN         - Запросить описание ошибки по номеру    *
# *    ovlGetErrorNUn       - Запросить описание ошибки              *
# *    ovlGetErrorPointXN   - Запросить координаты точки,            *
# *    ovlGetErrorPointYN     содержащей ошибку по номеру            *
# *                                                                  *
# ********************************************************************

import os
import ctypes
import mapsyst
import maptype

PACK_WIDTH = 1

#-----------------------------
class ERRORDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",maptype.DOUBLEPOINT),
                ("Code",ctypes.c_int),
                ("Object",ctypes.c_int),
                ("SubjectA",ctypes.c_int),
                ("SubjectB",ctypes.c_int),
                ("NumberA",ctypes.c_int),
                ("NumberB",ctypes.c_int)]
#----------------------------- 


try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    curLib = mapsyst.LoadLibrary(gisaccesname)


# Найти точку пересечения двух отрезков
# a1, a2    - точки первого отрезка (A)
# b1, b2    - точки второго отрезка (B)
# cp1       - первая точка пересечения
# cp2       - вторая точка пересечения
# precision - точность, используемая для проверки равенства точек
#             (рекомендуется DOUBLENULL)
# force     - флаг выполнения дополнительного поиска
#             (если равно 1, то учесть наличие отрезков нулевой длины)
# Возвращает CROSS-коды (code: CROSS_0, CROSS_1, CROSS_2 и другие).
# Число пересечений = (code & CROSS_GETCOUNT) = 0,1,2
# При ошибке параметров возвращает 0

    ovlGetCrossPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetCrossPoint', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_long)
    def ovlGetCrossPoint(_a1: ctypes.POINTER(maptype.DOUBLEPOINT), _a2: ctypes.POINTER(maptype.DOUBLEPOINT), _b1: ctypes.POINTER(maptype.DOUBLEPOINT), _b2: ctypes.POINTER(maptype.DOUBLEPOINT), _cp1: ctypes.POINTER(maptype.DOUBLEPOINT), _cp2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float, _force: int) -> int:
        return ovlGetCrossPoint_t (_a1, _a2, _b1, _b2, _cp1, _cp2, _precision, _force)


# Найти точку пересечения двух отрезков ненулевой длины
# crossCode - код пересечения
# a1, a2    - точки первого отрезка (A)
# b1, b2    - точки второго отрезка (B)
# cp1       - первая точка пересечения
# cp2       - вторая точка пересечения
# precision - точность, используемая для проверки равенства точек
#             (рекомендуется DOUBLENULL для карты с максимальной точностью,
#              0.01 - сантиметровой точности, 0.001 - миллиметровой точности)
# Вызывать только если отсутствует равенство точек a1=a2 и b1=b2
# Возвращает CROSS-коды (code: CROSS_0, CROSS_1, CROSS_2 и другие).
# Число пересечений = (code & CROSS_GETCOUNT) = 0,1,2
# При ошибке параметров возвращает 0

    ovlGetCrossPointReal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetCrossPointReal', ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def ovlGetCrossPointReal(_crossCode: int, _a1: ctypes.POINTER(maptype.DOUBLEPOINT), _a2: ctypes.POINTER(maptype.DOUBLEPOINT), _b1: ctypes.POINTER(maptype.DOUBLEPOINT), _b2: ctypes.POINTER(maptype.DOUBLEPOINT), _cp1: ctypes.POINTER(maptype.DOUBLEPOINT), _cp2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float) -> int:
        return ovlGetCrossPointReal_t (_crossCode, _a1, _a2, _b1, _b2, _cp1, _cp2, _precision)


# Определить наличие пересечения отрезка p1p2 с прямоугольной рамкой dframe
# p1, p2    - точки отрезка
# dframe    - прямоугольная рамка
# precision - точность, используемая для проверки равенства точек
# (позднее можно оптимизировать: при пересечении габаритов и если все точки рамки справа
# или все точки слева относительно линии, то пересечений нет)
# Возвращает: 0 - пересечений нет, 1 - пересечения есть
# При ошибке параметров возвращает 0

    ovlCrossTestFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlCrossTestFrame', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DFRAME), ctypes.c_double)
    def ovlCrossTestFrame(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _dframe: ctypes.POINTER(maptype.DFRAME), _precision: float) -> int:
        return ovlCrossTestFrame_t (_p1, _p2, _dframe, _precision)


# Вычисление расстояния между точкой и прямой, заданной двумя точками
# point  - заданная точка
# p1, p2 - точки отрезка, определяющие линию
# При ошибке параметров возвращает 0

    ovlDistance_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'ovlDistance', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlDistance(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return ovlDistance_t (_point, _p1, _p2)


# Вычисление квадрата расстояния между точкой и прямой, заданной двумя точками
# point  - заданная точка
# p1, p2 - точки отрезка, определяющие линию
# Более быстрая функция по сравнению с ovlDistance
# При ошибке параметров возвращает 0

    ovlDistance2_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'ovlDistance2', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlDistance2(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return ovlDistance2_t (_point, _p1, _p2)


# Найти точку на линии, ближайшую к заданной
# point  - заданная точка
# p1, p2 - точки отрезка, определяющие линию
# pres   - точка на линии (p1, p2), ближайшая к заданной (p)
# При ошибке параметров возвращает 0

    ovlSeekNearPointOnLine_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlSeekNearPointOnLine', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlSeekNearPointOnLine(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _pres: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return ovlSeekNearPointOnLine_t (_point, _p1, _p2, _pres)


# Запросить расположение точки относительно замкнутого объекта (с учетом подобъектов)
# point     - координаты точки (в метрах)
# hobj      - замктутый площадной или линейный объект
# precision - точность, используемая для проверки равенства точек.
#             При precision <= 0 устанавливается DOUBLENULL
# Возвращает:
#   1 - точка внутри объекта
#   2 - точка вне объекта
#   3 - точка лежит на контуре объекта
# При ошибке возвращает 0

    ovlGetLocationPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetLocationPoint', ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HOBJ, ctypes.c_double)
    def ovlGetLocationPoint(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _hobj: maptype.HOBJ, _precision: float) -> int:
        return ovlGetLocationPoint_t (_point, _hobj, _precision)


# Создать объект оверлейных операций
# hmap      - идентификатор открытых данных (используется для запроса высоты при разрезании объекта с 3D-метрикой)
# flag      - флаг проверки контуров исходных объектов на самопересечение:
#             1 - проверка на самопересечение выполняется (рекомендуется)
#             0 - проверка на самопересечение отключена (используется для ускорения обработки в задачах визуализации).
#                 При использовании данного флага при обработке объектов, содержащих ошибки самопересечения, возвращается ошибка
#                 "Ошибка обработки. Отключена проверка на самопересечение"
# precision - точность, используемая для проверки равенства точек
#             При precision <= 0 устанавливается DOUBLENULL
# Объект позволяет:
# 1 Запросить расположение метрики объекта любой локализации относительно шаблона
# 2 Согласовать точки контура объекта с точками контура шаблона перед поиском пересечений (в пределах допуска)
# 3 Запросить метрику шаблона, топологически согласованную с частями разрезаемого объекта
# 4 Запросить все точки пересечения объектов
# 5 Запросить очередную часть разрезаемого объекта:
#   5.1 Рассечение контуров объектов по замкнутому контуру
#   5.2 Рассечение контуров объектов по незамкнутому контуру
#   5.3 Рассечение площадных объектов по замкнутому контуру
# При сохранении объектов в карту с точностью хуже precision результирующие контура могут содержать петли
# При округлении координат точек близко расположенные точки могут совпасть
# Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат
# Возвращает идентификатор объекта оверлейных операций
# Для выгрузки из памяти вызывать функцию ovlFree
# При ошибке возвращает 0

    ovlCreate_t = mapsyst.GetProcAddress(curLib,maptype.HOVL,'ovlCreate', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def ovlCreate(_hmap: maptype.HMAP, _flag: int, _precision: float) -> maptype.HOVL:
        return ovlCreate_t (_hmap, _flag, _precision)


# Создать объект оверлейных операций для выполения контроля метрики объекта
# hobj      - обрабатываемый объект
# test      - тип контроля (допустимо совместное использование флагов):
#    OVL_TEST_STANDARD (1 или 0) - поиск самопересечений и примыканий контуров:
#        OVL_ERR_NONE                      0 - "Ошибок нет"
#        ...
#        OVL_ERR_SELFCROSSING_ADJACENT2   44 - "Обнаружены примыкающие отрезки контуров объекта"
#
#    OVL_TEST_NEARPOINT (2) - поиск близких точек и выбросов:
#        OVL_ERR_CHECKING_NEARPOINT       45 - "Точки контура слишком близки"
#        OVL_ERR_CHECKING_NEARPOINT2      46 - "Точки контуров слишком близки"
#        OVL_ERR_CHECKING_PEAK            47 - "Выброс в точке контура"
#        OVL_ERR_CHECKING_DOUBLEPOINT     48 - "Обнаружены двойные точки"
#        OVL_ERR_CHECKING_DOUBLEPOINT2    49 - "Обнаружены двойные точки в допуске"
#
#    OVL_TEST_LOCATION (4) - определение расположения контуров:
#        OVL_ERR_CHECKING_OBJECTINSIDE    50 - "Площадной объект внутри подобъекта"
#        OVL_ERR_CHECKING_SUBJECTINSIDE   51 - "Подобъект площадного объекта внутри подобъекта"
#        OVL_ERR_CHECKING_SUBJECTOUTSIDE  52 - "Подобъект вне площадного объекта"
# precision - точность, используемая для проверки равенства точек.
#             При precision <= 0 устанавливается DOUBLENULL
# Обрабатываются только линейные или площадные объекты.
# Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат.
# Для запроса результатов контроля использовать функции:
#   ovlGetErrorCount, ovlGetErrorN, ovlGetErrorPointXN, ovlGetErrorPointYN
# Для выгрузки из памяти вызывать функцию ovlFree
# Возвращает идентификатор объекта оверлейных операций
# При ошибке возвращает ноль

    ovlCreateCheckObject_t = mapsyst.GetProcAddress(curLib,maptype.HOVL,'ovlCreateCheckObject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def ovlCreateCheckObject(_hobj: maptype.HOBJ, _test: int, _precision: float) -> maptype.HOVL:
        return ovlCreateCheckObject_t (_hobj, _test, _precision)


# Освободить объект оверлейных операций
# hovl - идентификатор объекта оверлейных операций

    ovlFree_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'ovlFree', maptype.HOVL)
    def ovlFree(_hovl: maptype.HOVL) -> ctypes.c_void_p:
        return ovlFree_t (_hovl)


# Установить шаблон для оверлейных операций
# hovl    - идентификатор объекта оверлейных операций
# templet - шаблон, объект по контуру которого выполняются оверлейные операции
# subject - номер контура, используемого в качестве шаблона (лекала)
#            0 - основной контур объекта templet,
#            от 1 и более - подобъект объекта templet
#            -1 - все контура объекта templet (используется только при обработке
#                 пересечений методом METHOD_LINE, подробнее при описании  ovlSetObjectCross)
# adjust  - флаг согласования метрики контура шаблона с пересекаемыми
#           объектами (0, 1). Выполняется вставка точек пересечений в контур
# Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат
# Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
# При ошибке возвращает ноль

    ovlSetTemplet_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlSetTemplet', maptype.HOVL, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def ovlSetTemplet(_hovl: maptype.HOVL, _templet: maptype.HOBJ, _subject: int, _adjust: int) -> int:
        return ovlSetTemplet_t (_hovl, _templet, _subject, _adjust)


# Установить шаблон для оверлейных операций по габаритам прямоугольника
# hovl    - идентификатор объекта оверлейных операций
# templet - шаблон, объект по контуру которого выполняются оверлейные операции
# Разрезаемый объект карты и шаблон должны быть в одной системе координат
# Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
# При ошибке возвращает 0

    ovlSetTempletByFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlSetTempletByFrame', maptype.HOVL, ctypes.POINTER(maptype.DFRAME))
    def ovlSetTempletByFrame(_hovl: maptype.HOVL, _templet: ctypes.POINTER(maptype.DFRAME)) -> int:
        return ovlSetTempletByFrame_t (_hovl, _templet)


# Установить обрабатываемый объект и метод обработки
# hovl      - идентификатор объекта оверлейных операций
# hobj      - обрабатываемый объект
# subject   - номер обрабатываемого контура:
#             -1 - обработать все контура
#             0 - основной контур объекта,
#             от 1 и более - подобъект объекта
# precision - точность согласования точек объекта с точками шаблона
#             (DOUBLENULL и выше). Выполняется обновление точек объекта.
#             Используется для сохранения контуров близлежащих объектов.
#             Рекомендуется precision = 0.001 (метров на местности)
# flag3d    - флаг формирования высоты в точках трехмерной метрики,
#             соответствующих участкам контуров шаблона:
#             FLAG3D_NONE    0 - результат не содержит трехмерной метрики
#             FLAG3D_TEMPLET 2 - третья координата выбирается из контура шаблона
#             FLAG3D_MATRIX  8 - третья координата выбирается из карты
#                                (по наиболее точной открытой матрице высот)
#             FLAG3D_LINE   32 - третья координата вычисляется по крайним точкам участка,
#                                не содержащего высоты (методом линейной интерполяции)
#             FLAG3D_ALL    42 - совместное использование всех флагов
#                                FLAG3D_TEMPLET|FLAG3D_MATRIX|FLAG3D_LINE
#             Допускается совместное использование флагов:
#             FLAG3D_TEMPLET|FLAG3D_MATRIX, FLAG3D_MATRIX|FLAG3D_LINE,
#             FLAG3D_TEMPLET|FLAG3D_LINE
#             При совместном использовании используется приоритет выполнения:
#             FLAG3D_TEMPLET -> FLAG3D_MATRIX -> FLAG3D_LINE
#             Если исходный объект не содержит трехмерную метрику, то допустим только метод 0
# method    - флаг типа результирующих контуров (флаги метода обработки):
#             METHOD_LINE   0 - замкнутые и незамкнутые контура линейных объектов
#             METHOD_SQUARE 1 - замкнутые контура (части hobj) площадных объектов
#             METHOD_FAST  16 - быстрый способ обработки - используется только
#                               для объектов, которые не содержат самопересечений
#             Если контур шаблона не замкнут, то допустим только метод METHOD_LINE.
#             Допускается совместное использование флагов:
#             METHOD_LINE|METHOD_FAST, METHOD_SQUARE|METHOD_FAST
# location  - флаги размещения результирующих контуров:
#             ANYOBJECT или 0 - поиск всех контуров
#             ANYOBJECT2      - поиск всех контуров, включая отрезки
#                               контура равные отрезкам шаблона
#             OBJECTINSIDE    - поиск контуров внутри шаблона
#             OBJECTINSIDE2   - поиск контуров внутри шаблона, включая
#                               отрезки контура равные отрезкам шаблона
#             OBJECTOUTSIDE   - поиск контуров вне шаблона
#             OBJECTOUTSIDE2  - поиск контуров вне шаблона, включая
#                               отрезки контура равные отрезкам шаблона
#             OBJECTOVERLAP   - поиск совпадающих участков контуров
#             Допускается совместное использование флагов:
#             OBJECTINSIDE|OBJECTOUTSIDE, OBJECTINSIDE2|OBJECTOUTSIDE,
#             OBJECTINSIDE|OBJECTOUTSIDE2, OBJECTINSIDE2|OBJECTOUTSIDE2
# Если объект точечный, векторный, подпись или шаблон, то параметры
#    precision, method, location игнорируются. Положение объекта определяется
#    по первой точке первого подобъекта, а функция ovlSetObjectCross возвращает:
#    1 - объект внутри шаблона
#    2 - объект вне шаблона (ovlGetNextObject не вызывать)
# Если контур шаблона НЕ ЗАМКНУТ, то ovlSetObjectCross возвращает:
#    1 - все контура объекта совпадают с шаблоном (лежат на шаблоне)
#    2 - все контура объекта вне шаблона
#    3 - один или несколько контуров объекта пересекаются с шаблоном
#    При возврате 3 вызывать ovlGetNextObject в цикле
# Если контур шаблона ЗАМКНУТ и method == 0, то ovlSetObjectCross возвращает:
#    1 - все контура объекта внутри шаблона либо совпадают
#    2 - все контура объекта вне шаблона
#    3 - один или несколько контуров объекта пересекаются с шаблоном,
#        либо обнаружены внутренние и внешние контура (относительно шаблона)
# Если контур шаблона ЗАМКНУТ и method == 1, то ovlSetObjectCross возвращает:
#    1 - все контура объекта внутри шаблона либо совпадают
#    2 - все контура объекта вне шаблона
#    3 - один или несколько контуров объекта пересекаются с шаблоном,
#        либо обнаружены внутренние и внешние контура (относительно шаблона)
#    4 - контур шаблона внутри контура объекта
#    При возврате 3 и 4 вызывать ovlGetNextObject в цикле
# Если location == OBJECTOVERLAP, то ovlSetObjectCross возвращает:
#    0 - число несовпадающих точек контура объекта < 2 (проверка не выполняется)
#    1 - все контура объекта совпадают с шаблоном (лежат на шаблоне)
#    2 - все контура объекта вне шаблона
#    3 - один или несколько контуров объекта пересекаются с шаблоном
# Для запроса кода ошибки вызывать функции GetErrorCode и GetError
# При ошибке возвращает 0

    ovlSetObjectCross_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlSetObjectCross', maptype.HOVL, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def ovlSetObjectCross(_hovl: maptype.HOVL, _hobj: maptype.HOBJ, _subject: int, _precision: float, _flag3d: int, _method: int, _location: int) -> int:
        return ovlSetObjectCross_t (_hovl, _hobj, _subject, _precision, _flag3d, _method, _location)


# Запросить очередную часть разрезаемого объекта
# hovl   - идентификатор объекта оверлейных операций
# hobj   - объект для возврата результата. Для получения
#          наилучших результатов тип метрики объекта должен быть
#          равен IDDOUBLE2 или IDDOUBLE3
# Вызывать после ovlSetObjectCross в цикле до тех пор, пока не вернет 0
# Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
# Если контур шаблона ЗАМКНУТ, то ovlGetNextObject возвращает:
#    1 - контур объекта внутри шаблона (часть контура может совпадать
#        с контуром шаблона), либо совпадает с контуром шаблона
#    2 - контур объекта вне шаблона (часть контура может совпадать с контуром шаблона)
#    0 - контуров больше нет, либо при ошибке
# Если контур шаблона НЕ ЗАМКНУТ, то ovlGetNextObject возвращает:
#    1 - контур объекта совпадает с контуром шаблона (лежит на шаблоне)
#    2 - контур объекта вне шаблона (контур может касаться шаблона
#        одной или двумя точками)
#    0 - контуров больше нет, либо при ошибке
# Если в функции ovlSetObjectCross установлено location == OBJECTOVERLAP,
#    то ovlGetNextObject возвращает:
#    1 - контур совпадает (Поиск совпадающих участков контуров)
#    2 - контур не совпадает
#    0 - контуров больше нет, либо при ошибке
# При возврате 0 необходимо проверить код ошибки.
# Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN

    ovlGetNextObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetNextObject', maptype.HOVL, maptype.HOBJ)
    def ovlGetNextObject(_hovl: maptype.HOVL, _hobj: maptype.HOBJ) -> int:
        return ovlGetNextObject_t (_hovl, _hobj)


# Запросить признак изменения метрики шаблона, согласованного с метрикой объекта
# hovl   - идентификатор объекта оверлейных операций
# При вызове функции ovlSetObjectCross в метрику шаблона
# вставляются точки пересечения контуров шаблона и объекта
# Возвращает: 1 - метрика изменена, 0 - метрика не изменена

    ovlIsEditTemplet_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlIsEditTemplet', maptype.HOVL)
    def ovlIsEditTemplet(_hovl: maptype.HOVL) -> int:
        return ovlIsEditTemplet_t (_hovl)


# Запросить признак изменения метрики объекта, согласованного с метрикой шаблона
# hovl   - идентификатор объекта оверлейных операций
# При вызове функции ovlSetObjectCross в метрику объекта
# вставляются точки пересечения контуров шаблона и объекта
# Возвращает: 1 - метрика изменена, 0 - метрика не изменена

    ovlIsEditObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlIsEditObject', maptype.HOVL)
    def ovlIsEditObject(_hovl: maptype.HOVL) -> int:
        return ovlIsEditObject_t (_hovl)


# Запросить метрику шаблона, согласованную с метрикой объекта
# hovl    - идентификатор объекта оверлейных операций
# templet - объект для возврата результата
# subject - номер сохраняемого подобъекта:
#           0 или больше - записать только один контур шаблона
#           -1 - записать все контура шаблона
# При вызове функции ovlSetObjectCross в метрику шаблона
# вставляются точки пересечения контуров шаблона и объекта
# Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
# При ошибке возвращает 0

    ovlGetAdjustTemplet_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetAdjustTemplet', maptype.HOVL, maptype.HOBJ, ctypes.c_long)
    def ovlGetAdjustTemplet(_hovl: maptype.HOVL, _templet: maptype.HOBJ, _subject: int) -> int:
        return ovlGetAdjustTemplet_t (_hovl, _templet, _subject)


# Запросить метрику объекта, согласованную с метрикой шаблона
# hovl    - идентификатор объекта оверлейных операций
# hobj    - объект для возврата результата
# subject - номер сохраняемого подобъекта:
#           0 или больше - записать только один контур объекта
#           -1 - записать все контура объекта
# При вызове функции ovlSetObjectCross в метрику объекта
# вставляются точки пересечения контуров шаблона и объекта
# Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
# При ошибке возвращает 0

    ovlGetAdjustObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetAdjustObject', maptype.HOVL, maptype.HOBJ, ctypes.c_long)
    def ovlGetAdjustObject(_hovl: maptype.HOVL, _hobj: maptype.HOBJ, _subject: int) -> int:
        return ovlGetAdjustObject_t (_hovl, _hobj, _subject)


# Запросить все точки пересечения объектов
# hovl - идентификатор объекта оверлейных операций
# hobj - объект для возврата результата
# Точки пересечения записываются в объект. Точки пересечения каждого контура
# обрабатываемого объекта записываются в отдельные контура
# Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
# При ошибке возвращает 0

    ovlGetCrossPoints_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetCrossPoints', maptype.HOVL, maptype.HOBJ)
    def ovlGetCrossPoints(_hovl: maptype.HOVL, _hobj: maptype.HOBJ) -> int:
        return ovlGetCrossPoints_t (_hovl, _hobj)


# Запросить код ошибки
# hovl - идентификатор объекта оверлейных операций
# Возвращает код ошибки (OVL_ERR_NONE, ...)

    ovlGetErrorCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorCode', maptype.HOVL)
    def ovlGetErrorCode(_hovl: maptype.HOVL) -> int:
        return ovlGetErrorCode_t (_hovl)


# Запросить описание ошибки
# hovl - идентификатор объекта оверлейных операций
# Ошибка обнуляется для дальнейшего использования объекта оверлейных операций
# Возвращает описание ошибки

    ovlGetErrorUn_t = mapsyst.GetProcAddress(curLib,maptype.PWCHAR,'ovlGetErrorUn', maptype.HOVL)
    def ovlGetErrorUn(_hovl: maptype.HOVL) -> mapsyst.WTEXT:
        return ovlGetErrorUn_t (_hovl)


# Запросить описание ошибки оверлейных операций по коду ошибки
# ovlerror - код ошибки, полученный из функции ovlGetErrorCode
# text - указатель на буфер для записи описания ошибки
# size - размер буфера в байтах
# Возвращает описание ошибки

    ovlGetErrorTextUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorTextUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def ovlGetErrorTextUn(_ovlerror: int, _text: mapsyst.WTEXT, _size: int) -> int:
        return ovlGetErrorTextUn_t (_ovlerror, _text.buffer(), _size)


# Запросить число ошибок
# hovl - идентификатор объекта оверлейных операций
# Возвращает число ошибок

    ovlGetErrorCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorCount', maptype.HOVL)
    def ovlGetErrorCount(_hovl: maptype.HOVL) -> int:
        return ovlGetErrorCount_t (_hovl)


# Запросить код ошибки
# hovl   - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# Возвращает код ошибки (OVL_ERR_NONE, ...)

    ovlGetErrorCodeN_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorCodeN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorCodeN(_hovl: maptype.HOVL, _number: int) -> int:
        return ovlGetErrorCodeN_t (_hovl, _number)


# Запросить описание ошибки
# hovl   - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# Ошибка обнуляется для дальнейшего использования объекта оверлейных операций
# Возвращает описание ошибки на русском языке

    ovlGetErrorNUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'ovlGetErrorNUn', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorNUn(_hovl: maptype.HOVL, _number: int) -> ctypes.POINTER(maptype.WCHAR):
        return ovlGetErrorNUn_t (_hovl, _number)


# Запросить координаты точки, содержащей ошибку в системе координат карты
# hovl   - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# point  - буфер для записи координат
# При ошибке возвращает 0

    ovlGetErrorMapPlanePoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorMapPlanePoint', maptype.HOVL, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlGetErrorMapPlanePoint(_hovl: maptype.HOVL, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return ovlGetErrorMapPlanePoint_t (_hovl, _number, _point)


# Запросить координаты точки, содержащей ошибку в системе координат документа
# hovl   - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# point  - буфер для записи координат
# При ошибке возвращает 0

    ovlGetErrorPlanePoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorPlanePoint', maptype.HOVL, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlGetErrorPlanePoint(_hovl: maptype.HOVL, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return ovlGetErrorPlanePoint_t (_hovl, _number, _point)


# Запросить координату X точки, содержащей ошибку в системе координат документа
# hovl - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# При обнаружении самопересечения контура возвращает точку, содержащую ошибку.
# При обнаружении ошибки при обработке шаблона возвращает первую точку шаблона.
# В остальных случаях возвращает первую точку обрабатываемого объекта
# При ошибке возвращает 0.0

    ovlGetErrorPointXN_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'ovlGetErrorPointXN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorPointXN(_hovl: maptype.HOVL, _number: int) -> float:
        return ovlGetErrorPointXN_t (_hovl, _number)


# Запросить координату Y точки, содержащей ошибку в системе координат документа
# hovl - идентификатор объекта оверлейных операций
# number - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# При обнаружении самопересечения контура возвращает точку, содержащую ошибку.
# При обнаружении ошибки при обработке шаблона возвращает первую точку шаблона.
# В остальных случаях возвращает первую точку обрабатываемого объекта
# При ошибке возвращает 0.0

    ovlGetErrorPointYN_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'ovlGetErrorPointYN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorPointYN(_hovl: maptype.HOVL, _number: int) -> float:
        return ovlGetErrorPointYN_t (_hovl, _number)


# Запросить данные об ошибке
# hovl      - идентификатор объекта оверлейных операций
# number    - порядковый номер ошибки (от 1 до ovlGetErrorCount)
# errordesc - данные об ошибке (заполняются только при обнаружении ошибки)
# Возвращает код ошибки (OVL_ERR_NONE, ...)
# При ошибке возвращает 0

    ovlGetErrorDesc_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ovlGetErrorDesc', maptype.HOVL, ctypes.c_long, ctypes.POINTER(ERRORDESC))
    def ovlGetErrorDesc(_hovl: maptype.HOVL, _number: int, _errordesc: ctypes.POINTER(ERRORDESC)) -> int:
        return ovlGetErrorDesc_t (_hovl, _number, _errordesc)

except Exception as e:
    print(e)
    curLib = 0

def crossapi_healthcheck(): 
    return 1