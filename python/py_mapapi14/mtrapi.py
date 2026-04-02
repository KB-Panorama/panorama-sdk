#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class CALC_ABSOLUTE_HEIGHT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MethodMTW",ctypes.c_char),
                ("MethodMTL",ctypes.c_char),
                ("MethodMTD",ctypes.c_char),
                ("MethodTIN",ctypes.c_char),
                ("FilterMTD",ctypes.c_char),
                ("Reserve",ctypes.c_char*51),
                ("RadiusMTD",ctypes.c_double)]
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К МАТРИЦАМ +++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Открыть матричные данные
# Возвращает идентификатор открытой матричной карты (TMapAccess#)
# mtrname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenMtrUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtrUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtrUn(_mtrname: mapsyst.WTEXT, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtrUn_t (_mtrname.buffer(), _mode)

    mapOpenMtr_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtr', ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtr(_mtrname: ctypes.c_char_p, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtr_t (_mtrname, _mode)


# Открыть матричные данные в заданном районе работ
# (добавить в цепочку матриц)
# Возвращает номер файла в цепочке матриц
# hMap -  идентификатор открытых данных
# mtrname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenMtrForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtrForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtrForMapUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        return mapOpenMtrForMapUn_t (_hMap, _name.buffer(), _mode)

    mapOpenMtrForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtrForMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtrForMap(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mode: int) -> int:
        return mapOpenMtrForMap_t (_hMap, _mtrname, _mode)


# Закрыть матричные данные
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# если number == 0, закрываются все матрицы в окне
# ЧТОБЫ ОСВОБОДИТЬ ВСЕ РЕСУРСЫ - НУЖНО ВЫЗВАТЬ mapCloseData(hMap)

    mapCloseMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtr', maptype.HMAP, ctypes.c_int)
    def mapCloseMtr(_hMap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        return mapCloseMtr_t (_hMap, _number)


# Закрыть матричные данные в заданном районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Если number == 0, закрываются все матричные данные
# При ошибке возвращает ноль

    mapCloseMtrForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseMtrForMap', maptype.HMAP, ctypes.c_int)
    def mapCloseMtrForMap(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCloseMtrForMap_t (_hMap, _number)


# Установить признак обработки матрицы в потоках
# flag - признак обработки матрицы в потоках (если не равнен нулю)
# При ошибке возвращает ноль

    mapSetMtrMultiThreadFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrMultiThreadFlag', ctypes.c_int)
    def mapSetMtrMultiThreadFlag(_flag: int) -> int:
        return mapSetMtrMultiThreadFlag_t (_flag)


# Запросить время крайнего редактирования матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает системное время редактирования (создания) по Гринвичу
# При ошибке возвращает ноль

    mapGetMtrSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrSystemTime', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetMtrSystemTime(_hMap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        return mapGetMtrSystemTime_t (_hMap, _number, _time)


# Построение матрицы по векторной карте на заданный участок района работ
# При ошибке возвращает ноль
# hMap    - исходная карта для построения матрицы
# mtrname - полное имя создаваемой матрицы
# filtername - полное имя фильтра объектов
#   Вместе с картой может располагаться фильтр объектов -
#   текстовый файл MTRCREA.IMH, содержащий перечень кодов
#   объектов, используемых при построении матрицы (см. MAPAPI.DOC)
# Если filtername равно нулю - фильтр объектов не используется
# mtrparm - параметры создаваемой матрицы,
# handle   - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
# Если handle равно нулю - сообщения не посылаются.
# Параметр LPARAM (не равный 0) сообщения о ходе процесса содержит номер
# этапа построения матрицы :
#   1 - Заполнение матрицы абсолютными высотами объектов
#   2 - Обработка объектов гидрографии с постоянной высотой
#   3 - Обработка объектов гидрографии с переменной высотой
#   4 - Обработка точечных объектов с абсолютной высотой
#   5 - Определение минимальной и максимальной высоты
#   6 - Вычисление незаполненных элементов матрицы
#   9 - Заполнение матрицы относительными высотами объектов
#   10 - Создание матрицы выполнено
#   11 - Создание матрицы не выполнено
#   13 - Обработка пустых замкнутых горизонталей
#   14 - Вычисление элементов матрицы по сетке высотных точек
#   15 - Построение сетки треугольников по высотным точкам
#   16 - Сжатие матрицы
#   17 - Вычисление высот по трехмерной метрике площадных объектов

    mapBuildMtw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtw', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildMtw(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _filtername: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        return mapBuildMtw_t (_hMap, _mtrname, _filtername, _mtrparm, _handle)

    mapBuildMtwUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtwUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildMtwUn(_hMap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _txtname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        return mapBuildMtwUn_t (_hMap, _mtrname.buffer(), _txtname.buffer(), _mtrparm, _handle)


# Построение матрицы глубин по морской карте,
# созданной по классификатору с именем s57navy.rsc
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Объекты для построения матрицы глубин:
#  изобата (ключ DEPCNT_L), отметка глубины (ключ SOUNDG_P),
#  область суши (LNDARE_S), затонувшее судно (WRECKS_P1),
#  опасность (OBSTRN_S1), подводная осыхающая скала (UWTROC_P)
# mtrname - полное имя создаваемой матрицы
# mtrparm - параметры создаваемой матрицы
# handle   - идентификатор окна диалога, которому посылаются
#  сообщения о ходе процесса :
#   0x0589 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0589
# errorcode - код ошибки
#   IDS_PARM - ошибка входных параметров функции
#   IDS_NOMAP - нет открытых векторных карт
#   IDS_MEMORY - ошибка выделения памяти
#   IDS_RSCOPEN - ошибка открытия файла RSC
#   IDS_LOADLIBRARY - ошибка загрузки библиотеки
#   IDS_CREATE - ошибка создания файла
#   7300 - нет открытых морских карт
# При ошибке возвращает ноль

    mapBuildMtwDepth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtwDepth', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HMESSAGE, ctypes.POINTER(ctypes.c_int))
    def mapBuildMtwDepth(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HMESSAGE, _errorcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapBuildMtwDepth_t (_hmap, _hsite, _mtrname.buffer(), _mtrparm, _handle, _errorcode)


# Построение растра качеств по векторной карте на заданный
# участок района работ
# При ошибке возвращает ноль
# hMap    - исходная карта для построения растра,
# rstname - полное имя создаваемого растра,
# filtername - полное имя служебного текстового файла
#   Вместе с картой должен располагаться фильтр объектов -
#   служебный текстовый файл MАP2RSW.INI, содержащий перечень кодов
#   объектов, используемых при построении растра
# mtrparm - параметры создаваемого растра,
# handle   - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
# Если handle равно нулю - сообщения не посылаются

    mapBuildRsw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRsw', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildRsw(_hMap: maptype.HMAP, _rstname: ctypes.c_char_p, _filtername: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        return mapBuildRsw_t (_hMap, _rstname, _filtername, _mtrparm, _handle)

    mapBuildRswUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildRswUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildRswUn(_hMap: maptype.HMAP, _rstname: mapsyst.WTEXT, _filtername: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        return mapBuildRswUn_t (_hMap, _rstname.buffer(), _filtername.buffer(), _mtrparm, _handle)


# Очистить кэш матричных данных, открытых на ГИС Сервере
# hMap    - идентификатор открытой векторной карты
# number  - номер матрицы, для которой нужно очистить кэш, или -1 (все матрицы)
# При ошибке возвращает ноль

    mapClearMtrCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearMtrCache', maptype.HMAP, ctypes.c_int)
    def mapClearMtrCache(_hMap: maptype.HMAP, _number: int) -> int:
        return mapClearMtrCache_t (_hMap, _number)


# Запросить описание файла матричных данных
# hMap - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# describe - адрес структуры, в которой будет размещено
# описание матрицы
# При ошибке возвращает ноль

#   mapGetMtrDescribe_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetMtrDescribe', maptype.HMAP, ctypes.c_int, ctypes.POINTER(MTRDESCRIBE))
#   def mapGetMtrDescribe(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(MTRDESCRIBE)) -> int:
#       return mapGetMtrDescribe_t (_hMap, _number, _describe)

    mapGetMtrDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrDescribeUn', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.MTRDESCRIBEUN))
    def mapGetMtrDescribeUn(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(maptype.MTRDESCRIBEUN)) -> int:
        return mapGetMtrDescribeUn_t (_hMap, _number, _describe)


# Запросить описание диапазона высот матрицы с номером
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# colornumber - номер диапазона высот
# colordesc - адрес структуры, в которой будет размещено
# описание диапазона высот
# При ошибке возвращает ноль

    mapGetMtrColorDescEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrColorDescEx', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.MTRCOLORDESCEX))
    def mapGetMtrColorDescEx(_hMap: maptype.HMAP, _number: int, _colornumber: int, _colordesc: ctypes.POINTER(maptype.MTRCOLORDESCEX)) -> int:
        return mapGetMtrColorDescEx_t (_hMap, _number, _colornumber, _colordesc)


# Запросить имя файла матричных данных
# hMap - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# name - адрес строки для размещения результата
# size - размер строки
# При ошибке возвращает ноль

    mapGetMtrNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtrNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMtrNameUn_t (_hMap, _number, _name.buffer(), _size)


# Запросить число открытых файлов матричных данных
# hMap -  идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetMtrCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCount', maptype.HMAP)
    def mapGetMtrCount(_hMap: maptype.HMAP) -> int:
        return mapGetMtrCount_t (_hMap)


# Запросить число открытых файлов матричных данных
# hMap      - идентификатор открытых данных
# userLabel - метка файла MTW:
#             0               - выполняется запрос для матриц высот
#             LABEL_MTW_DEPTH - выполняется запрос для матриц глубин
#             LABEL_MTW_EGM   - выполняется запрос для матриц поправок высот геоида
# При ошибке возвращает ноль

    mapGetMtwCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtwCount', maptype.HMAP, ctypes.c_int)
    def mapGetMtwCount(_hMap: maptype.HMAP, _userLabel: int) -> int:
        return mapGetMtwCount_t (_hMap, _userLabel)


# Запросить номер матрицы в цепочке по имени файла
# name - имя файла матрицы
# В цепочке номера матриц начинаются с 1
# При ошибке возвращает ноль

    mapGetMtrNumberByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrNumberByName', maptype.HMAP, ctypes.c_char_p)
    def mapGetMtrNumberByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapGetMtrNumberByName_t (_hMap, _name)

    mapGetMtrNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtrNumberByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetMtrNumberByNameUn_t (_hMap, _name.buffer())


# Запросить фактические габариты отображаемой матрицы в метрах в системе координат документа
# При отображении матрицы по рамке возвращаются габариты рамки
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# frame  - адрес структуры, в которой будут размещены габариты матрицы в метрах
# При ошибке возвращает ноль

    mapGetActualMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActualMtrFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetActualMtrFrame(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetActualMtrFrame_t (_hMap, _frame, _number)


# Запросить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapGetMtrLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtrLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetMtrLocation_t (_hMap, _number, _location)


# Установить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapSetMtrLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtrLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSetMtrLocation_t (_hMap, _number, _location)


# Запросить минимальное значение высот всех матриц в метрах
# hMap -  идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetTotalMinHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTotalMinHeight', maptype.HMAP)
    def mapGetTotalMinHeight(_hMap: maptype.HMAP) -> float:
        return mapGetTotalMinHeight_t (_hMap)


# Запросить максимальное значение высот всех матриц в метрах
# hMap -  идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetTotalMaxHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTotalMaxHeight', maptype.HMAP)
    def mapGetTotalMaxHeight(_hMap: maptype.HMAP) -> float:
        return mapGetTotalMaxHeight_t (_hMap)


# Запрос наличия высот рельефа на заданном участке
# hMap  - идентификатор открытой основной векторной карты
# frame - адрес структуры, содержащей габариты заданного участка в метрах
# Если frame равно нулю, то заданный участок определяется габаритами карты
# При наличии высот рельефа возвращает 1, при отсутствии возвращает 0

    mapHeightValuePresence_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapHeightValuePresence', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapHeightValuePresence(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapHeightValuePresence_t (_hMap, _frame)


# Выбор значения абсолютной высоты в заданной точке.
# hMap   - идентификатор открытой основной векторной карты
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT

    mapGetHeightValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightValue', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetHeightValue(_hMap: maptype.HMAP, _x: float, _y: float) -> float:
        return mapGetHeightValue_t (_hMap, _x, _y)


# Выбор значения абсолютной высоты в заданной точке из матрицы
# с номером number в цепочке.
# hMap   - идентификатор открытой основной векторной карты
# number - номер матрицы в цепочке.
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# hpaint - контекст поддержки многопоточного вызова (см. mapCreatePaintControl)
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT

    mapGetHeightValueOfMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightValueOfMtr', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapGetHeightValueOfMtr(_hMap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        return mapGetHeightValueOfMtr_t (_hMap, _number, _x, _y)

    mapGetHeightValueOfMtrControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightValueOfMtrControl', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetHeightValueOfMtrControl(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _hPaint: maptype.HPAINT) -> float:
        return mapGetHeightValueOfMtrControl_t (_hMap, _number, _x, _y, _hPaint)


# Возвращает интерполированную высоту в заданной точке
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# interptype - тип интерполяции
#              1 - ближайший сосед
#              2 - интерполяция по ближайшим 3 элементам
#              3 - билинейная интерполяция по 4 ближайшим элементам
#              4 - бикубическая интерполяция по 16 ближайшим элементам
# x, y - координаты точки в метрах
# h    - возвращаемое значение в метрах (при ошибке устанавливается ERRORHEIGHT)
# При ошибке возвращает 0

    mapGetHeightValueOfMtrEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightValueOfMtrEx', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapGetHeightValueOfMtrEx(_hMap: maptype.HMAP, _number: int, _interptype: int, _x: float, _y: float, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetHeightValueOfMtrEx_t (_hMap, _number, _interptype, _x, _y, _h)


# Чтение элемента матрицы высот по абсолютным индексам
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# value  - полученное значение элемента в метрах
#          (при отсутствии высоты равно ERRORHEIGHT)
# string - индекс строки матрицы (значение от 0 до height-1, где height - высота
#          матрицы элементах, запрашиваемая функцией mapGetMtrHeightInElement)
# column - индекс колонки матрицы (значение от 0 до width-1, где width - ширина
#          матрицы элементах, запрашиваемая функцией mapGetMtrWidthInElement)
# hPaint - контекст поддержки многопоточного вызова (см. mapCreatePaintControl) или 0
# При ошибке и при отсутствии высоты возвращает ноль

    mapGetMtrPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrPoint', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)
    def mapGetMtrPoint(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double), _string: int, _column: int) -> int:
        return mapGetMtrPoint_t (_hMap, _number, _value, _string, _column)

    mapGetMtrPointEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrPointEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int, maptype.HPAINT)
    def mapGetMtrPointEx(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double), _string: int, _column: int, _hPaint: maptype.HPAINT) -> int:
        return mapGetMtrPointEx_t (_hMap, _number, _value, _string, _column, _hPaint)


# Запросить размер элемента матрицы в метрах по оси X
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# metinelemX - размер элемента матрицыв метрах на местности по оси X
# При ошибке возвращает ноль

    mapGetMtrMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrMeterInElementX', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetMtrMeterInElementX(_hMap: maptype.HMAP, _number: int, _metinelemX: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtrMeterInElementX_t (_hMap, _number, _metinelemX)


# Запросить размер элемента матрицы в метрах по оси Y
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# metinelemY - размер элемента матрицы в метрах на местности по оси Y
# При ошибке возвращает ноль

    mapGetMtrMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrMeterInElementY', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetMtrMeterInElementY(_hMap: maptype.HMAP, _number: int, _metinelemY: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtrMeterInElementY_t (_hMap, _number, _metinelemY)


# Занесение значения абсолютной высоты в элемент матрицы,
# соответствующий заданной точке.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Координаты точки (x,y) и значение высоты (h) задаются в метрах
# в системе координат векторной карты.
# В случае ошибки возвращает ноль

    mapPutHeightValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutHeightValue', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutHeightValue(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        return mapPutHeightValue_t (_hMap, _number, _x, _y, _h)


# Занесение значения абсолютной высоты в элемент матрицы,
# соответствующий заданной точке.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# x - номер строки элементов в матрице
# y - номер колонки элементов в матрице
# h - значение высоты в метрах
# в системе координат векторной карты.
# В случае ошибки возвращает ноль

    mapPutMtrPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutMtrPoint', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapPutMtrPoint(_hMap: maptype.HMAP, _number: int, _x: int, _y: int, _h: float) -> int:
        return mapPutMtrPoint_t (_hMap, _number, _x, _y, _h)


# Вычисление абсолютной высоты в заданной точке по открытым данным,
# содержащим модели рельефа: матрица высот MTW, матрица слоев MTL,
# облако точек MTD, триангуляционная нерегулярная сеть TIN.
# hMap - идентификатор открытой основной векторной карты
# x,y  - координаты точки, задаются в метрах в системе координат
#        векторной карты
# parm - параметры вычисления высоты (структура CALC_ABSOLUTE_HEIGHT)
#   Последовательность использования моделей рельефа: MTW, MTL, MTD, TIN.
#   Переход к использованию очередной модели рельефа выполняется
#   в случае ошибки при вычислении высоты и в случае необеспеченности
#   заданной точки данными модели. Использование модели рельефа
#   можно отключить, задавая в структуре CALC_ABSOLUTE_HEIGHT
#   метод вычисления высоты = -1.
#   Если parm == 0, то считается, что задана структура
#   CALC_ABSOLUTE_HEIGHT, содержащая элементы равные 0.
# hPaint - идентификатор контекста отображения для многопоточного вызова функций,
#          создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# Возвращает значение высоты в метрах.
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки данными моделей рельефа возвращает ERRORHEIGHT

    mapGetAbsoluteHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAbsoluteHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.POINTER(CALC_ABSOLUTE_HEIGHT), maptype.HPAINT)
    def mapGetAbsoluteHeight(_hMap: maptype.HMAP, _x: float, _y: float, _parm: ctypes.POINTER(CALC_ABSOLUTE_HEIGHT), _hPaint: maptype.HPAINT) -> float:
        return mapGetAbsoluteHeight_t (_hMap, _x, _y, _parm, _hPaint)


# Выбор значения абсолютной высоты в заданной точке из
# матрицы с наименьшим размером элемента (более точной)
# hMap   - идентификатор открытой основной векторной карты
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# hPaint - идентификатор контекста отображения для многопоточного вызова функций,
#          создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT

    mapGetPrecisionHeightValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightValue', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetPrecisionHeightValue(_hMap: maptype.HMAP, _x: float, _y: float) -> float:
        return mapGetPrecisionHeightValue_t (_hMap, _x, _y)

    mapGetPrecisionHeightValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightValueEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetPrecisionHeightValueEx(_hMap: maptype.HMAP, _x: float, _y: float, _hPaint: maptype.HPAINT) -> float:
        return mapGetPrecisionHeightValueEx_t (_hMap, _x, _y, _hPaint)


# Расчет абсолютной высоты методом треугольников в заданной точке
# по матрице с наименьшим размером элемента (более точной).
# В матрицах обрабатываются нормальные высоты
# Высота вычисляется по самой точной матрице высот,а в случае
# необеспеченности заданной точки данными матриц высот -
# по самой точной матрице слоев.
# hMap   - идентификатор открытой основной векторной карты
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# hPaint - идентификатор контекста отображения для многопоточного вызова функций,
#          создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT (-111111)

    mapGetPrecisionHeightTriangle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightTriangle', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetPrecisionHeightTriangle(_hMap: maptype.HMAP, _x: float, _y: float) -> float:
        return mapGetPrecisionHeightTriangle_t (_hMap, _x, _y)

    mapGetPrecisionHeightTriangleEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightTriangleEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetPrecisionHeightTriangleEx(_hMap: maptype.HMAP, _x: float, _y: float, _hPaint: maptype.HPAINT) -> float:
        return mapGetPrecisionHeightTriangleEx_t (_hMap, _x, _y, _hPaint)


# Расчет абсолютной высоты методом треугольников в заданной точке
# по матрице с номером number в цепочке
# Координаты точки (x,y) задаются в метрах в системе координат
# векторной карты. Возвращает значение высоты в метрах.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# В случае ошибки при выборе высоты и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT

    mapGetHeightTriangleOfMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightTriangleOfMtr', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapGetHeightTriangleOfMtr(_hMap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        return mapGetHeightTriangleOfMtr_t (_hMap, _number, _x, _y)


# Расчет среднего значения абсолютной высоты по высотам квадратной области
# Функция может использоваться для создания матрицы обобщенного рельефа
# xcenter, ycenter - координаты центра области в метрах
# size - размер стороны области в метрах (размер элемента матрицы обобщенного рельефа)
# Возвращает среднее значение высоты в метрах
# В случае ошибки при выборе высот и в случае необеспеченности
# заданной области матричными данными возвращает ERRORHEIGHT

    mapGetGeneralHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetGeneralHeight(_hMap: maptype.HMAP, _xcenter: float, _ycenter: float, _size: float) -> float:
        return mapGetGeneralHeight_t (_hMap, _xcenter, _ycenter, _size)


# Расчет среднего значения абсолютной высоты по высотам квадратной области
# матрицы с номером number в цепочке
# Функция может использоваться для создания матрицы обобщенного рельефа
# xcenter, ycenter - координаты центра области в метрах
# size - размер стороны области в метрах (размер элемента матрицы обобщенного рельефа)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает среднее значение высоты в метрах
# В случае ошибки при выборе высот и в случае необеспеченности
# заданной области матричными данными возвращает ERRORHEIGHT

    mapGetGeneralHeightOfMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralHeightOfMtr', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetGeneralHeightOfMtr(_hMap: maptype.HMAP, _number: int, _xcenter: float, _ycenter: float, _size: float) -> float:
        return mapGetGeneralHeightOfMtr_t (_hMap, _number, _xcenter, _ycenter, _size)


# Запросить номер в цепочке для матрицы, расположенной
# в заданной точке
# hMap   - идентификатор открытой основной векторной карты
# x,y    - координаты точки в метрах в системе документа
# number - порядковый номер, найденной матрицы в точке
# (1 - первая в данной точке, 2 - вторая ...)
# При ошибке возвращается ноль, иначе - порядковый номер открытой матрицы в цепочке с 1

    mapGetMtrNumberInPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrNumberInPoint', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapGetMtrNumberInPoint(_hMap: maptype.HMAP, _x: float, _y: float, _number: int) -> int:
        return mapGetMtrNumberInPoint_t (_hMap, _x, _y, _number)


# Вычисление значения массива элементов с применением метода треугольников
# по матрицам высот (применяется для обработки OGC WCS-запросов)
# hmap   - идентификатор документа, содержащего открытые матрицы высот (MTW)
# matrix - указатель на буфер выходной матрицы 4-ех байтовых целочисленных элементов
# width  - ширина выходной матрицы (число элементов в строке)
# hight  - высота выходной матрицы (число строк)
# unit   - единица измерения высоты в матрице (0 - метры, 1 - дециметры, 2 - сантиметры, 3 - миллиметры)
# dframe - габариты матрицы на местности в системе координат матрицы (и документа)
#          от юго-западного элемента матрицы до северо-восточного
# minvalue - поле для записи минимального значения элемента в выходной матрице
# maxvalue - поле для записи максимального значения элемента в выходной матрице
# hpaint - контекст поддержки многопоточного вызова (см. mapCreatePaintControl)
# В случае необеспеченности заданной точки матричными данными в элемент записывается ERRORHEIGHT (-111111)
# При ошибке возвращает ноль

    mapGetPrecisionHeightFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPrecisionHeightFrame', maptype.HMAP, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), maptype.HPAINT)
    def mapGetPrecisionHeightFrame(_hmap: maptype.HMAP, _matrix: ctypes.POINTER(ctypes.c_int), _width: int, _hight: int, _unit: int, _dframe: ctypes.POINTER(maptype.DFRAME), _minvalue: ctypes.POINTER(ctypes.c_int), _maxvalue: ctypes.POINTER(ctypes.c_int), _hpaint: maptype.HPAINT) -> int:
        return mapGetPrecisionHeightFrame_t (_hmap, _matrix, _width, _hight, _unit, _dframe, _minvalue, _maxvalue, _hpaint)


# Выбор массива значений абсолютных высот, соответствующих
# логическим элементам, лежащим на заданном отрезке
# hMap   - идентификатор открытой основной векторной карты
# Координаты точек, задающих начало и конец отрезка
# (first, second) задаются в метрах в системе координат документа
# Размер массива высот, заданного адресом heightArray,
# должен соответствовать запрашиваемому количеству высот
# (count), в противном случае возможны ошибки работы с памятью.
# Расчет абсолютной высоты в каждой промежуточной точке выполняется
# методом треугольников по матрице с наименьшим размером элемента (более точной)
# В случае необеспеченности логического элемента матричными
# данными его значение равно ERRORHEIGHT (-111111.0 м)
# В случае ошибки при выборе высот возвращает ноль

    mapGetHeightArray_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightArray', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetHeightArray(_hMap: maptype.HMAP, _heightArray: ctypes.POINTER(ctypes.c_double), _count: int, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetHeightArray_t (_hMap, _heightArray, _count, _first, _second)

    mapGetHeightArrayEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightArrayEx', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HPAINT)
    def mapGetHeightArrayEx(_hMap: maptype.HMAP, _heightArray: ctypes.POINTER(ctypes.c_double), _count: int, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _control: maptype.HPAINT) -> int:
        return mapGetHeightArrayEx_t (_hMap, _heightArray, _count, _first, _second, _control)


# Запросить размер полного блока матрицы в байтах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBlockSize', maptype.HMAP, ctypes.c_int)
    def mapGetMtrBlockSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrBlockSize_t (_hMap, _number)


# Запросить размер(тип) элемента матрицы в байтах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращаемое значение 1 соответствует типу "unsigned char".
# Возвращаемое значение 2 соответствует типу "short int".
# Возвращаемое значение 4 соответствует типу "long int".
# Возвращаемое значение 8 соответствует типу "double".
# При ошибке возвращает ноль

    mapGetMtrElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrElementSize', maptype.HMAP, ctypes.c_int)
    def mapGetMtrElementSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrElementSize_t (_hMap, _number)


# Запросить вертикальный размер блока матрицы в элементах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBlockSide', maptype.HMAP, ctypes.c_int)
    def mapGetMtrBlockSide(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrBlockSide_t (_hMap, _number)


# Запросить горизонтальный размер блока матрицы в элементах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBlockWidth', maptype.HMAP, ctypes.c_int)
    def mapGetMtrBlockWidth(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrBlockWidth_t (_hMap, _number)


# Запросить ширину текущего блока матрицы в элементах
# (с учетом усеченных блоков)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCurrentBlockWidth', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMtrCurrentBlockWidth(_hMap: maptype.HMAP, _number: int, _column: int) -> int:
        return mapGetMtrCurrentBlockWidth_t (_hMap, _number, _column)


# Запросить высоту текущего блока матрицы в элементах
# (с учетом усеченных блоков)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCurrentBlockHeight', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMtrCurrentBlockHeight(_hMap: maptype.HMAP, _number: int, _string: int) -> int:
        return mapGetMtrCurrentBlockHeight_t (_hMap, _number, _string)


# Запросить размер текущего блока матрицы в байтах
# (с учетом усеченных блоков)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# string, column - строка и столбец блока соотвественно
# При ошибке возвращает ноль

    mapGetMtrCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCurrentBlockSize', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetMtrCurrentBlockSize(_hMap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        return mapGetMtrCurrentBlockSize_t (_hMap, _number, _string, _column)


# Запись блока {string,column} в файл матрицы из памяти bits
# number   - номер файла в цепочке
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# bits     - указатель на начало изображения битовой области
# sizebits - размер области bits в байтах
# Возвращает количество записанных байт.
# При ошибке возвращает ноль

    mapWriteMtrBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWriteMtrBlock', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapWriteMtrBlock(_hMap: maptype.HMAP, _number: int, _string: int, _column: int, _bits: ctypes.c_char_p, _sizebits: int) -> int:
        return mapWriteMtrBlock_t (_hMap, _number, _string, _column, _bits, _sizebits)


# Возврат флага отображения блока матрицы
# (0 - не отображается, 1- отображается, 2 - разделен рамкой )
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# number - номер файла в цепочке
# i - порядковый номер (индекс) блока, i = str # blockColumnCount + col, где:
#     str - индекс строки блоков,
#     blockColumnCount - число столбцов блоков матрицы (функция mapGetMtrBlockColumn)
#     col - индекс столбца блоков
# При ошибке возвращает ноль

    mapCheckMtrBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckMtrBlockVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapCheckMtrBlockVisible(_hMap: maptype.HMAP, _number: int, _i: int) -> int:
        return mapCheckMtrBlockVisible_t (_hMap, _number, _i)


# Запросить число строк блоков матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBlockRow', maptype.HMAP, ctypes.c_int)
    def mapGetMtrBlockRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrBlockRow_t (_hMap, _number)


# Запросить число столбцов блоков матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBlockColumn', maptype.HMAP, ctypes.c_int)
    def mapGetMtrBlockColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrBlockColumn_t (_hMap, _number)


# Запросить число строк элементов в матрице
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrElementRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrElementRow', maptype.HMAP, ctypes.c_int)
    def mapGetMtrElementRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrElementRow_t (_hMap, _number)


# Запросить число столбцов элементов в матрице
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrElementColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrElementColumn', maptype.HMAP, ctypes.c_int)
    def mapGetMtrElementColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrElementColumn_t (_hMap, _number)


# Запросить масштаб матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrScale', maptype.HMAP, ctypes.c_int)
    def mapGetMtrScale(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrScale_t (_hMap, _number)


# Запросить значения масштаба нижней и верхней границ видимости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# По адресу bottomScale записывается знаменатель масштаба нижней границы видимости матрицы
# По адресу topScale записывается знаменатель масштаба верхней границы видимости матрицы
# При ошибке возвращает ноль

    mapGetMtrRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetMtrRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: ctypes.POINTER(ctypes.c_int), _topScale: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetMtrRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить значения масштаба нижней и верхней границ видимости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# bottomScale - знаменатель масштаба нижней границы видимости матрицы
# topScale    - знаменатель масштаба верхней границы видимости матрицы
#               bottomScale <= topScale, иначе возвращает 0
# При ошибке возвращает ноль

    mapSetMtrRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMtrRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: int, _topScale: int) -> int:
        return mapSetMtrRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Запросить тип исходной карты
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrMapType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrMapType', maptype.HMAP, ctypes.c_int)
    def mapGetMtrMapType(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrMapType_t (_hMap, _number)


# Запросить единицу измерения значений высот матрицы
# с номером number в цепочке.
# Возвращает значение поля Unit структуры параметров создания
# матрицы BUILDMTW
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращаемые значения :
#   0-метры, 1-дециметры, 2-сантиметры, 3-миллиметры
# При ошибке возвращает -1

    mapGetMtrMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrMeasure', maptype.HMAP, ctypes.c_int)
    def mapGetMtrMeasure(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrMeasure_t (_hMap, _number)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Если нет - возвращает ноль

    mapIsMtrGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMtrGeoSupported', maptype.HMAP, ctypes.c_int)
    def mapIsMtrGeoSupported(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsMtrGeoSupported_t (_hMap, _number)


# Запросить данные о проекции матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# projectiondata - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MTRPROJECTIONDATA описанa в maptype.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapGetMtrProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtrProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetMtrProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtrProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapGetMtrProjectionData(_hMap: maptype.HMAP, _number: int, _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapGetMtrProjectionData_t (_hMap, _number, _projectiondata)


# Запросить данные о проекции матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# mapregister - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MAPREGISTEREX описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtrProjectionDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProjectionDataEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtrProjectionDataEx(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetMtrProjectionDataEx_t (_hMap, _number, _mapregister)


# Запросить данные о проекции матрицы по имени файла
# name        - имя файла матрицы
# mapregister - адрес структуры, в которой будут размещены
# данные о проекции
# При ошибке возвращает ноль

    mapGetMtrProjectionDataByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProjectionDataByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtrProjectionDataByName(_name: ctypes.c_char_p, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetMtrProjectionDataByName_t (_name, _mapregister)

    mapGetMtrProjectionDataByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProjectionDataByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtrProjectionDataByNameUn(_name: mapsyst.WTEXT, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetMtrProjectionDataByNameUn_t (_name.buffer(), _mapregister)


# Установить данные о проекции матрицы
# ВНИМАНИЕ: помимо данных о проекции функция переносит маштаб mapregister->Scale
# в заголовок матрицы.
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# mapregister - адрес структуры, содержащей данные о проекции
# Структурa MAPREGISTEREX описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtrProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapSetMtrProjectionData(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapSetMtrProjectionData_t (_hMap, _number, _mapregister)


# Установить данные о проекции матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# mapregister, datumparam, ellipsoidparam - адреса структур, содержащих данные о проекции
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM описаны в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapSetMtrProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtrProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetMtrProjectionDataPro_t (_hMap, _number, _mapregisterex, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSetMtrProjectionDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrProjectionDataEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtrProjectionDataEx(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetMtrProjectionDataEx_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam)


# Записать изменения матрицы в файл
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapSaveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMtr', maptype.HMAP, ctypes.c_int)
    def mapSaveMtr(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSaveMtr_t (_hMap, _number)


# Запросить параметры эллипсоида матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# ellipsoidparam - адрес структуры, в которой будут размещены
# параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtrEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtrEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetMtrEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Установить параметры эллипсоида матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# ellipsoidparam - адрес структуры, содержащей параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtrEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtrEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetMtrEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Запросить коэффициенты трансформирования геодезических координат матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# datumparam - адрес структуры, в которой будут размещены
# коэффициенты трансформирования геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtrDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtrDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetMtrDatumParam_t (_hMap, _number, _datumparam)


# Установить коэффициенты трансформирования геодезических координат матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# datumparam - адрес структуры, содержащей коэффициенты трансформирования
# геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtrDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtrDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetMtrDatumParam_t (_hMap, _number, _datumparam)


# Вычисление значения абсолютной высоты (point->H) в заданной
# точке (point->X,point->Y) по данным векторной карты
# Координаты точки задаются в метрах в системе координат
# векторной карты
# В случае ошибки при вычислении высоты возвращает 0

    mapCalcAbsoluteHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCalcAbsoluteHeight', maptype.HMAP, ctypes.POINTER(maptype.XYHDOUBLE))
    def mapCalcAbsoluteHeight(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.XYHDOUBLE)) -> int:
        return mapCalcAbsoluteHeight_t (_hMap, _point)


# Вычисление значения абсолютной высоты в заданной
# точке (point->X,point->Y) по данным векторной карты
# Координаты точки задаются в метрах в системе координат
# векторной карты
# sectorcount - количество направлений для поиска окружающих высот
# (должно быть кратно 4, минимальное количество направлений = 4,
#  максимальное = 256)
# Возвращает значение высоты в метрах
# В случае ошибки при вычислении высоты возвращает ERRORHEIGHT

    mapCalcAbsoluteHeightBySectors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapCalcAbsoluteHeightBySectors', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapCalcAbsoluteHeightBySectors(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _sectorcount: int) -> float:
        return mapCalcAbsoluteHeightBySectors_t (_hMap, _point, _sectorcount)


# Запросить/Установить степень видимости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# view = 0 - не виден
# view = 1 - полная
# view = 2 - насыщенная
# view = 3 - полупрозрачная
# view = 4 - средняя
# view = 5 - прозрачная

    mapGetMtrView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrView', maptype.HMAP, ctypes.c_int)
    def mapGetMtrView(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrView_t (_hMap, _number)

    mapSetMtrView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtrView(_hMap: maptype.HMAP, _number: int, _view: int) -> int:
        return mapSetMtrView_t (_hMap, _number, _view)


# Запросить прозрачность палитры матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает степень прозрачности в процентах от 0 до 100

    mapGetMtrTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrTransparent', maptype.HMAP, ctypes.c_int)
    def mapGetMtrTransparent(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrTransparent_t (_hMap, _number)


# Установить прозрачность палитры матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# transparent - прозрачность в процентах от 0 до 100
# При ошибке возвращает ноль

    mapSetMtrTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrTransparent', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtrTransparent(_hMap: maptype.HMAP, _number: int, _transparent: int) -> int:
        return mapSetMtrTransparent_t (_hMap, _number, _transparent)


# Запросить/Установить порядок отображения матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# order  - порядок (0 - под картой, 1 - над картой)
# При ошибке возвращает ноль

    mapSetMtrViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtrViewOrder(_hMap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetMtrViewOrder_t (_hMap, _number, _order)

    mapGetMtrViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrViewOrder', maptype.HMAP, ctypes.c_int)
    def mapGetMtrViewOrder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrViewOrder_t (_hMap, _number)


# Поменять очередность отображения матриц (mtr) в цепочке
#   oldNumber - номер файла в цепочке
#   newNumber - устанавливаемый номер файла в цепочке
#  При ошибке возвращает ноль

    mapChangeOrderMtrShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeOrderMtrShow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangeOrderMtrShow(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangeOrderMtrShow_t (_hMap, _oldNumber, _newNumber)


# Запросить/Установить режим сглаживания растрово-матричных данных
#   mode - режим отображения (0 - быстрое, 1 - со сглаживанием)
# При ошибке возвращает ноль

    mapGetMatrixSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMatrixSmoothing', maptype.HMAP)
    def mapGetMatrixSmoothing(_hMap: maptype.HMAP) -> int:
        return mapGetMatrixSmoothing_t (_hMap)

    mapSetMatrixSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMatrixSmoothing', maptype.HMAP, ctypes.c_int)
    def mapSetMatrixSmoothing(_hMap: maptype.HMAP, _mode: int) -> int:
        return mapSetMatrixSmoothing_t (_hMap, _mode)


# Установить/Запросить глубину тени матрицы высот
#  hMap  - идентификатор открытой основной векторной карты
#  value - флаг наложения тени (от 0 до 16)
#   MTRSHADOW_NONE   =  0,   # Тень отсутствует
#   MTRSHADOW_PALE   =  1,   # Бледная
#   MTRSHADOW_WEAK   =  2,   # Слабая
#   MTRSHADOW_MIDDLE =  4,   # Средняя
#   MTRSHADOW_HEAVY  =  8,   # Сильная
#   MTRSHADOW_DEEP   = 16,   # Глубокая

    mapGetMtrShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrShadow', maptype.HMAP)
    def mapGetMtrShadow(_hMap: maptype.HMAP) -> int:
        return mapGetMtrShadow_t (_hMap)

    mapSetMtrShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrShadow', maptype.HMAP, ctypes.c_int)
    def mapSetMtrShadow(_hMap: maptype.HMAP, _value: int) -> int:
        return mapSetMtrShadow_t (_hMap, _value)


# Установить/Запросить интенсивность тени матрицы высот
#  hMap  - идентификатор открытой основной векторной карты
#  value - интенсивность тени (от 0 до 100)

    mapGetMtrShadowIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrShadowIntensity', maptype.HMAP)
    def mapGetMtrShadowIntensity(_hMap: maptype.HMAP) -> int:
        return mapGetMtrShadowIntensity_t (_hMap)

    mapSetMtrShadowIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrShadowIntensity', maptype.HMAP, ctypes.c_int)
    def mapSetMtrShadowIntensity(_hMap: maptype.HMAP, _value: int) -> int:
        return mapSetMtrShadowIntensity_t (_hMap, _value)


# Запросить число цветов в палитре матриц высот
# ВСЕ МАТРИЦЫ ВЫСОТ РАБОТАЮТ С ОДНОЙ ПАЛИТРОЙ
#  hMap   - идентификатор открытой основной векторной карты
# При ошибке возвращает ноль

    mapGetMtrPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrPaletteCount', maptype.HMAP)
    def mapGetMtrPaletteCount(_hMap: maptype.HMAP) -> int:
        return mapGetMtrPaletteCount_t (_hMap)


# Запросить текущую палитру матрицы высот
# (с учетом яркости/контрастности)
# hMap    - идентификатор открытой основной векторной карты
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetMtrPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapGetMtrPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetMtrPalette_t (_hMap, _palette, _count)


# Запросить эталонную палитру матрицы высот
# (без учета яркости/контрасности)
# hMap    - идентификатор открытой основной векторной карты
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetMtrStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapGetMtrStandardPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetMtrStandardPalette_t (_hMap, _palette, _count)


# Установить описание палитры матрицы высот
# hMap    - идентификатор открытой основной векторной карты
# palette - адрес устанавливаемой палитры
# count   - число элементов в новой палитре
# При ошибке возвращает ноль

    mapSetMtrPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapSetMtrPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapSetMtrPalette_t (_hMap, _palette, _count)


# Запросить яркость палитры матрицы высот
# hMap   - идентификатор открытой основной векторной карты

    mapGetMtrBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBright', maptype.HMAP)
    def mapGetMtrBright(_hMap: maptype.HMAP) -> int:
        return mapGetMtrBright_t (_hMap)


# Установить яркость палитры матрицы высот
# hMap   - идентификатор открытой основной векторной карты
# bright - значение яркости (-16..+16)
# При ошибке возвращает ноль

    mapSetMtrBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrBright', maptype.HMAP, ctypes.c_int)
    def mapSetMtrBright(_hMap: maptype.HMAP, _bright: int) -> int:
        return mapSetMtrBright_t (_hMap, _bright)


# Запросить контрастность палитры матрицы высот
# hMap     - идентификатор открытой основной векторной карты
# значение контраста (-16..+16)
# При ошибке возвращает ноль

    mapGetMtrContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrContrast', maptype.HMAP)
    def mapGetMtrContrast(_hMap: maptype.HMAP) -> int:
        return mapGetMtrContrast_t (_hMap)


# Установить контрастность палитры матрицы высот
# hMap     - идентификатор открытой основной векторной карты
# contrast - значение контраста (-16..+16)
# При ошибке возвращает ноль

    mapSetMtrContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrContrast', maptype.HMAP, ctypes.c_int)
    def mapSetMtrContrast(_hMap: maptype.HMAP, _contrast: int) -> int:
        return mapSetMtrContrast_t (_hMap, _contrast)


# Запросить параболическую яркость палитры матрицы высот
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetMtrGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrGamma', maptype.HMAP)
    def mapGetMtrGamma(_hMap: maptype.HMAP) -> int:
        return mapGetMtrGamma_t (_hMap)


# Установить параболическую яркость палитры матрицы высот
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# gamma  - параболическая яркость
# При ошибке возвращает ноль

    mapSetMtrGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrGamma', maptype.HMAP, ctypes.c_int)
    def mapSetMtrGamma(_hMap: maptype.HMAP, _gamma: int) -> int:
        return mapSetMtrGamma_t (_hMap, _gamma)


# Запросить стиль палитры матрицы высот
# hMap     - идентификатор открытой основной векторной карты
# Возвращаемое значение:
#  0  - полутоновая палитра
#  1  - цветная палитра
# -1  - отображаются только тени от рельефа

    mapGetMtrColorStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrColorStyle', maptype.HMAP)
    def mapGetMtrColorStyle(_hMap: maptype.HMAP) -> int:
        return mapGetMtrColorStyle_t (_hMap)


# Установить стиль палитры матрицы высот
# hMap       - идентификатор открытой основной векторной карты
# colorstyle - стиль отображения матрицы:
#  0  - полутоновая палитра
#  1  - цветная палитра
# -1  - отображаются только тени от рельефа
# При ошибке возвращает ноль

    mapSetMtrColorStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrColorStyle', maptype.HMAP, ctypes.c_int)
    def mapSetMtrColorStyle(_hMap: maptype.HMAP, _colorstyle: int) -> int:
        return mapSetMtrColorStyle_t (_hMap, _colorstyle)


# Установить цвет диапазона высот матрицы с номером
# number в цепочке
# hMap        - идентификатор открытой основной векторной карты
# colornumber - номер диапазона высот
# color       - цвет диапазона
# При ошибке возвращает ноль

    mapSetMtrColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrColor', maptype.HMAP, ctypes.c_int, ctypes.c_int, maptype.COLORREF)
    def mapSetMtrColor(_hMap: maptype.HMAP, _number: int, _colornumber: int, _color: maptype.COLORREF) -> int:
        return mapSetMtrColor_t (_hMap, _number, _colornumber, _color)


# Запросить флаг пользовательского диапазона цепочки матриц высот
# При ошибке возвращает ноль

    mapGetMtrUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrUserDiapason', maptype.HMAP)
    def mapGetMtrUserDiapason(_hMap: maptype.HMAP) -> int:
        return mapGetMtrUserDiapason_t (_hMap)


# Установить флаг пользовательского диапазона цепочки матриц высот
# При ошибке возвращает ноль

    mapSetMtrUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrUserDiapason', maptype.HMAP, ctypes.c_int)
    def mapSetMtrUserDiapason(_hMap: maptype.HMAP, _value: int) -> int:
        return mapSetMtrUserDiapason_t (_hMap, _value)


# Запросить флаг отображения высот вне пользовательского
# диапазона граничными цветами
# При ошибке возвращает ноль

    mapGetMtrViewOutUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrViewOutUserDiapason', maptype.HMAP)
    def mapGetMtrViewOutUserDiapason(_hMap: maptype.HMAP) -> int:
        return mapGetMtrViewOutUserDiapason_t (_hMap)


# Установить флаг отображения высот вне пользовательского
# диапазона граничными цветами
# При ошибке возвращает ноль

    mapSetMtrViewOutUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrViewOutUserDiapason', maptype.HMAP, ctypes.c_int)
    def mapSetMtrViewOutUserDiapason(_hMap: maptype.HMAP, _value: int) -> int:
        return mapSetMtrViewOutUserDiapason_t (_hMap, _value)


# Запросить количество цветов в палитре матрицы number
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц:
#             0   - возращает общее количество цветов для всех открытых
#                   матриц с меткой userLabel
#             > 0 - возвращает количество цветов матрицы с номером
#                   number и меткой userLabel
#             -1  - возвращает максимальное количество цветов для всех
#                   матриц с меткой userLabel
# userLabel - метка файла MTW (определяется функцией mapGetMtwUserLabel):
#             0               - выполняется запрос для матриц высот
#             LABEL_MTW_DEPTH - выполняется запрос для матриц глубин
#             LABEL_MTW_EGM   - выполняется запрос для матриц поправок высот геоида
# При ошибке возвращает ноль

    mapGetMtwPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtwPaletteCount', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMtwPaletteCount(_hMap: maptype.HMAP, _number: int, _userLabel: int) -> int:
        return mapGetMtwPaletteCount_t (_hMap, _number, _userLabel)


# Запросить для матрицы массив цветов палитры и массив граничных
# значений диапазонов высот
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц:
#             0   - заполняет массивы цветов и диапазонов для всех
#                   открытых матриц с меткой userLabel
#             > 0 - заполняет массивы цветов и диапазонов для матрицы
#                   с номером number и меткой userLabel
#             -1  - заполняет полные массивы цветов и диапазонов для всех
#                   матриц с меткой userLabel (полный массив диапазонов высот
#                   заполняется только для LABEL_MTW_DEPTH и LABEL_MTW_EGM)
# userLabel - метка файла MTW (определяется функцией mapGetMtwUserLabel):
#             0               - выполняется запрос для матриц высот
#             LABEL_MTW_DEPTH - выполняется запрос для матриц глубин
#             LABEL_MTW_EGM   - выполняется запрос для матриц поправок высот геоида
# count     - количество элементов в массиве цветов и массиве диапазонов
#             (определяется функцией mapGetMtwPaletteCount)
# Результаты запроса:
# minimum   - минимальное значение в метрах (если 0, то не заполняется)
# maximum   - максимальное значение в метрах (если 0, то не заполняется)
# Если number = 0 - minimum,maximum - общие для всех
#                   открытых матриц с меткой userLabel
#      number > 0 - minimum,maximum - для матрицы
#                   с номером number
#      number =-1 - minimum,maximum не заполняюся
# palette   - массив цветов палитры размером count # sizeof(COLORREF)
#             или более. Если palette = 0, то массив не заполняется
# diapason  - массив нижних граничных значений диапазонов в метрах
#             размером count # sizeof(double) или более.
#             Если diapason = 0, то массив не заполняется
# При ошибке возвращает ноль

    mapGetMtwPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtwPaletteDiapason', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_double))
    def mapGetMtwPaletteDiapason(_hMap: maptype.HMAP, _number: int, _userLabel: int, _count: int, _minimum: ctypes.POINTER(ctypes.c_double), _maximum: ctypes.POINTER(ctypes.c_double), _palette: ctypes.POINTER(maptype.COLORREF), _diapason: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtwPaletteDiapason_t (_hMap, _number, _userLabel, _count, _minimum, _maximum, _palette, _diapason)


# Установить рамку матрицы по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# info   - замкнутый объект карты
# После выполнения функции отображение матрицы ограничится заданной областью
# При ошибке возвращает ноль

    mapSetMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapSetMtrBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapSetMtrBorder_t (_hMap, _number, _info)


# Установить рамку матрицы по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# info   - замкнутый объект карты
# flagSubject- флаг использования подобъектов объекта при установке рамки матрицы  (0/1)
#              0 - в качестве рамки матрицы устанавливается контур объекта
#              1 - в качестве рамки матрицы устанавливается контур объекта с подобъектами
# После выполнения функции отображение растра ограничится заданной областью
# При ошибке возвращает 0

    mapSetMtrBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrBorderEx', maptype.HMAP, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapSetMtrBorderEx(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ, _flagSubject: int) -> int:
        return mapSetMtrBorderEx_t (_hMap, _number, _info, _flagSubject)


# Удалить рамку матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# После выполнения функции отображение матрицы будет полным
# При ошибке возвращает ноль

    mapDeleteMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtrBorder', maptype.HMAP, ctypes.c_int)
    def mapDeleteMtrBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteMtrBorder_t (_hMap, _number)


# Определение существования рамки матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapCheckExistenceMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckExistenceMtrBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckExistenceMtrBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckExistenceMtrBorder_t (_hMap, _number)


# Определение способа отображения матрицы(относительно рамки)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает 1 - при отображении матрицы по рамке
#            0 - при отображении матрицы без учета рамки
# При ошибке возвращает -1

    mapCheckShowMtrByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckShowMtrByBorder', maptype.HMAP, ctypes.c_int)
    def mapCheckShowMtrByBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCheckShowMtrByBorder_t (_hMap, _number)


# Установка отображения матрицы по рамке
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# value = 1 - отобразить матрицу по рамке
#       = 0 - отобразить матрицу без учета рамки

    mapShowMtrByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapShowMtrByBorder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapShowMtrByBorder(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapShowMtrByBorder_t (_hMap, _number, _value)


# Запросить объект рамки матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# info   - идентификатор объекта рамки матрицы
# При ошибке возвращает ноль

    mapGetMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapGetMtrBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapGetMtrBorder_t (_hMap, _number, _info)


# Определить координаты и порядковый номер точки рамки, которая
# входит в прямоугольник Габариты растра(матрицы) и
# имеет наименьшее удаление от точки pointIn (координаты в метрах).
# По адресу pointOut записываются координаты найденной точки в метрах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке или отсутствии рамки возвращает ноль

    mapGetImmediatePointOfMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImmediatePointOfMtrBorder', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtrBorder(_hMap: maptype.HMAP, _number: int, _pointIn: ctypes.POINTER(maptype.DOUBLEPOINT), _pointOut: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetImmediatePointOfMtrBorder_t (_hMap, _number, _pointIn, _pointOut)


# Запросить состояние матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращаемые значения:
#          0 - нет данных; или создание уменьшенных копий и сжатие не выполнялись
#          3 - создание всех уровней уменьшенных копий, сжатие RMF_COMPR_32 матрицы
#          4 - создание всех уровней уменьшенных копий матрицы

    mapGetMtrProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrProcessingState', maptype.HMAP, ctypes.c_int)
    def mapGetMtrProcessingState(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrProcessingState_t (_hMap, _number)


# Установить состояние матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# state  - состояние матрицы.
# Возможные значения состояния матрицы state:
#          0 - нет данных; или создание уменьшенных копий и сжатие не выполнялись
#          3 - создание всех уровней уменьшенных копий, сжатие RMF_COMPR_32 матрицы
#          4 - создание всех уровней уменьшенных копий матрицы
# При ошибке возвращает 0.

    mapSetMtrProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrProcessingState', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtrProcessingState(_hMap: maptype.HMAP, _number: int, _state: int) -> int:
        return mapSetMtrProcessingState_t (_hMap, _number, _state)


# Оптимизировать матрицу для открытия в ГИС Сервер
# Функция проверяет состояние матрицы и при необходимости выполняет для неё
# оптимизацию со сжатием и создание всех уровней уменьшенной копии.
# Необходимо закрыть матрицу из всех документов перед вызовом функции
# mtrName- имя файла матрицы
# handle - идентификатор окна, которое будет извещаться
# о ходе процесса (0x585 - 0x588)
# При ошибке возвращает 0

    mapOptimizationMtrByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOptimizationMtrByName', ctypes.c_char_p, maptype.HWND)
    def mapOptimizationMtrByName(_mtrName: ctypes.c_char_p, _handle: maptype.HWND) -> int:
        return mapOptimizationMtrByName_t (_mtrName, _handle)

    mapOptimizationMtrByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOptimizationMtrByNameUn', maptype.PWCHAR, maptype.HWND)
    def mapOptimizationMtrByNameUn(_mtrName: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        return mapOptimizationMtrByNameUn_t (_mtrName.buffer(), _handle)


# Запросить количество созданных уменьшенных копий в матрице
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает 0

    mapGetMtrDuplicatesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrDuplicatesCount', maptype.HMAP, ctypes.c_int)
    def mapGetMtrDuplicatesCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrDuplicatesCount_t (_hMap, _number)


# Обновить уменьшенную копию
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает 0

    mapUpdateMtrDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateMtrDuplicates', maptype.HMAP, ctypes.c_int)
    def mapUpdateMtrDuplicates(_hMap: maptype.HMAP, _number: int) -> int:
        return mapUpdateMtrDuplicates_t (_hMap, _number)


# Открыть сеанс трехмерной визуализации местности,
# обеспеченной открытыми матрицами высот
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# width  - ширина изображения,
# height - высота изображения.
# Возвращает идентификатор открытого сеанса (TMtr3D#)
# При ошибке возвращает ноль
# Закрыть сеанс трехмерной визуализации местности
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# Отобразить фрагмент местности в трехмерном виде
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# parm   - параметры отображения (см. MAPTYPE.H)
# hDC    - контекст отображения
# Устаревшая функция (рекомендуется пользоваться mapPaintMtr3Dx)
# Отобразить фрагмент местности в трехмерном виде
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# parm   - параметры отображения (см. MAPTYPE.H)
# hDC    - контекст отображения
# Установить уровень затопления
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# Построить BITMAP с изображением фрагмента местности в трехмерном виде
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# parm   - параметры отображения (см. MAPTYPE.H)
# При ошибке возвращает ноль
# Построить BITMAP с изображением фрагмента местности в трехмерном виде
# hMtr3D - идентификатор открытого сеанса 3D визуализации
# parm   - параметры отображения (см. MAPTYPE.H)
# При ошибке возвращает ноль
# Создать матричную карту
# mtrname - имя файла создаваемой матрицы
# Возвращает идентификатор открытой матричной карты
# Структуры BUILDMTW,MTRPROJECTIONDATA описаны в maptype.h
# При ошибке возвращает ноль

    mapCreateMtw_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtw', ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateMtw(_mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> maptype.HMAP:
        return mapCreateMtw_t (_mtrname, _mtrparm, _mtrprojectiondata)

    mapCreateMtwUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtwUn', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateMtwUn(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> maptype.HMAP:
        return mapCreateMtwUn_t (_mtrname.buffer(), _mtrparm, _mtrprojectiondata)


# Создать матричную карту для БД SQLite
# mtrname - имя создаваемой матрицы
# Структуры BUILDMTW,MTRPROJECTIONDATA описаны в maptype.h
# minvalue - минимальное значение данных в матрице
# maxvalue - максимальное значение данных в матрице
# При ошибке возвращает ноль

    mapCreateMtwForSqlite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateMtwForSqlite', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA), ctypes.c_double, ctypes.c_double)
    def mapCreateMtwForSqlite(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA), _minvalue: float, _maxvalue: float) -> int:
        return mapCreateMtwForSqlite_t (_mtrname.buffer(), _mtrparm, _mtrprojectiondata, _minvalue, _maxvalue)


# Вывод прямоугольного участка матрицы
#   hMap - идентификатор открытой матричной карты (TMapAccess #)
#   number - номер файла в цепочке
#   bits - адрес логического начала выводимого участка
#          (см. beginning)
#   left - смещение участка матрицы слева (в элементах)
#   top - смещение участка матрицы сверху (в элементах)
#   width - ширина участка матрицы (в элементах)
#   height - высота участка матрицы (в элементах)
#   beginning - определяет, на какую строку указывает bits :
#     если beginning == 0, то bits указывает
#       на начало верхней строки выводимого участка
#     если beginning == 1, то bits указывает
#       на начало нижней строки выводимого участка.
#   Размер участка, заданного адресом bits, должен быть не менее
#   (width # height # размер элемента матрицы в байтах),
#   в противном случае возможны ошибки работы с памятью.
#   Запрос размера элемента матрицы в байтах
#   - функция mapGetMtrElementSize.
#   Высоты выводимого участка должны быть записаны
#   в области bits в единицах измерения высот данной матрицы.
#   Запрос единицы измерения высоты матрицы
#   - функция mapGetMtrMeasure.
# При ошибке возвращает ноль

    mapPutMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutMtrFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapPutMtrFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _beginning: int) -> int:
        return mapPutMtrFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _beginning)


# Чтение прямоугольного участка матрицы в заданную область памяти
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# bits - указатель на начало области памяти
# left - смещение участка матрицы слева (в элементах)
# top - смещение участка матрицы сверху (в элементах)
# width - ширина участка матрицы (в элементах)
# height - высота участка матрицы (в элементах)
# widthinbyte - ширинa участка матрицы в байтах
# Размер участка, заданного адресом bits, должен быть не менее
# (width # height # размер элемента матрицы в байтах),
# в противном случае возможны ошибки работы с памятью.
# Запрос размера элемента матрицы в байтах - функция mapGetMtrElementSize.
# Высоты участка записываются в область bits в единицах измерения
# значений высот данной матрицы.
# Запрос единицы измерения значений высот матрицы - функция mapGetMtrMeasure.
# При ошибке возвращает ноль

    mapGetMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetMtrFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int = 0) -> int:
        return mapGetMtrFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _widthinbyte)


# Запросить диапазон высот рельефа (суммарный диапазон всех матриц
# высот, слоев, TIN-моделей)
# hMap     - идентификатор открытой карты (TMapAccess#)
# minvalue - минимальная высота диапазона в метрах
# maxvalue - максимальная высота диапазона в метрах
# При ошибке возвращает ноль

    mapGetReliefRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetReliefRange', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetReliefRange(_hMap: maptype.HMAP, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetReliefRange_t (_hMap, _minvalue, _maxvalue)


# Занести в матрицу диапазон значений высот
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# minvalue - минимальная высота диапазона в метрах
# maxvalue - максимальная высота диапазона в метрах
# При ошибке возвращает ноль

    mapSetMtrShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrShowRange', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapSetMtrShowRange(_hMap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        return mapSetMtrShowRange_t (_hMap, _number, _minvalue, _maxvalue)


# Запросить диапазон значений высот матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# minvalue - минимальная высота диапазона в метрах
# maxvalue - максимальная высота диапазона в метрах
# При ошибке возвращает ноль

    mapGetMtrShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrShowRange', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetMtrShowRange(_hMap: maptype.HMAP, _number: int, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtrShowRange_t (_hMap, _number, _minvalue, _maxvalue)


# Установить диапазон отображаемых высот всей цепочки матриц.
# Установленный диапазон в матрицу не заносится (сохраняется
# в INI-файл документа)
#   hMap - идентификатор открытой основной карты
#   minvalue - минимальная высота диапазона в метрах
#   maxvalue - максимальная высота диапазона в метрах
#   viewOutRange - отображать элементы матрицы, значения которых
#                  вне диапазона (0 или 1). Если viewOutRange == 0,
#                  то значения вне диапазона не отображаются.
#                  Если viewOutRange == 1, то:
#                - элементы, имеющие значения высот < minvalue,
#                  отображаются первым цветом палитры матрицы;
#                - элементы, имеющие значения высот > maxvalue,
#                  отображаются последним цветом палитры матрицы.
# При ошибке возвращает ноль

    mapSetMtrHeightRangeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrHeightRangeEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapSetMtrHeightRangeEx(_hMap: maptype.HMAP, _minvalue: float, _maxvalue: float, _viewOutRange: int) -> int:
        return mapSetMtrHeightRangeEx_t (_hMap, _minvalue, _maxvalue, _viewOutRange)


# Установить диапазон отображаемых высот всей цепочки матриц.
# Элемент матрицы не отображается, если он содержит высоту,
# не входящую в заданный диапазон.
# Установленный диапазон в матрицу не заносится (сохраняется
# в INI-файл документа)
#   hMap - идентификатор открытой основной карты
#   minvalue - минимальная высота диапазона в метрах
#   maxvalue - максимальная высота диапазона в метрах
# При ошибке возвращает ноль

    mapSetMtrHeightRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrHeightRange', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapSetMtrHeightRange(_hMap: maptype.HMAP, _minvalue: float, _maxvalue: float) -> int:
        return mapSetMtrHeightRange_t (_hMap, _minvalue, _maxvalue)


# Запросить диапазон высот отображаемых элементов
# цепочки матриц.
#   hMap - идентификатор открытой основной карты (TMapAccess #)
#   minvalue - минимальная высота диапазона в метрах
#   maxvalue - максимальная высота диапазона в метрах
# При ошибке возвращает ноль
# При успешном завершении возвращает: 1 - диапазон высот был вычислен по матрицам цепочки
#                                     2 - диапазон высот установлен пользователем

    mapGetMtrHeightRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrHeightRange', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetMtrHeightRange(_hMap: maptype.HMAP, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtrHeightRange_t (_hMap, _minvalue, _maxvalue)


# Установить суммарный диапазон высот отображаемых элементов
# цепочки матриц. Суммарный диапазон включает в себя диапазоны
# всех матриц цепочки.
# hMap - идентификатор открытой основной карты (TMapAccess #)
# При ошибке возвращает ноль

    mapResetMtrHeightRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapResetMtrHeightRange', maptype.HMAP)
    def mapResetMtrHeightRange(_hMap: maptype.HMAP) -> int:
        return mapResetMtrHeightRange_t (_hMap)


# Настроить параметры отображения цепочки матриц при изменении
# числа цветов палитры и диапазона отображаемых высот.
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ноль

    mapSetMtrShowVariables_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrShowVariables', maptype.HMAP)
    def mapSetMtrShowVariables(_hMap: maptype.HMAP) -> int:
        return mapSetMtrShowVariables_t (_hMap)


# Установить условное имя матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapSetMtrUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrUserName', maptype.HMAP, ctypes.c_int, ctypes.c_char_p)
    def mapSetMtrUserName(_hMap: maptype.HMAP, _number: int, _username: ctypes.c_char_p) -> int:
        return mapSetMtrUserName_t (_hMap, _number, _username)

    mapSetMtrUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrUserNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR)
    def mapSetMtrUserNameUn(_hMap: maptype.HMAP, _number: int, _username: mapsyst.WTEXT) -> int:
        return mapSetMtrUserNameUn_t (_hMap, _number, _username.buffer())


# Запросить условное имя матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# name   - адрес строки в которую записывается условное имя матрицы
# namesize - размер строки в БАЙТАХ
# При ошибке возвращает ноль

    mapGetMtrUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrUserNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtrUserNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetMtrUserNameUn_t (_hMap, _number, _name.buffer(), _namesize)


# Запросить пользовательскую метку матрицы (MTW)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Возвращает: 0               - метка матрицы высот
#             LABEL_MTW_DEPTH - метка матрицы глубин
#             LABEL_MTW_EGM   - метка матрицы поправок высот геоида
# При ошибке возвращает ноль

    mapGetMtwUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtwUserLabel', maptype.HMAP, ctypes.c_int)
    def mapGetMtwUserLabel(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtwUserLabel_t (_hMap, _number)


# Запросить координаты Юго-Западного угла матрицы в метрах
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# По адресу x,y записываются координаты найденной точки в метрах
# При ошибке возвращает 0

    mapGetSouthWestMtrPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSouthWestMtrPlane', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetSouthWestMtrPlane(_hMap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetSouthWestMtrPlane_t (_hMap, _number, _x, _y)


# Запросить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# При ошибке возвращает ноль

    mapGetActiveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActiveMtr', maptype.HMAP)
    def mapGetActiveMtr(_hMap: maptype.HMAP) -> int:
        return mapGetActiveMtr_t (_hMap)


# Установить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapSetActiveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveMtr', maptype.HMAP, ctypes.c_int)
    def mapSetActiveMtr(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSetActiveMtr_t (_hMap, _number)


# Открыта ли матрица с номером "number"
# Функция возвращает признак открытия указанной матрицы в документе - (1/0).
# При ошибке возвращает ноль.

    mapIsOpenMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsOpenMtr', maptype.HMAP, ctypes.c_int)
    def mapIsOpenMtr(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsOpenMtr_t (_hMap, _number)


# Запросить флаг редактируемости матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrEdit', maptype.HMAP, ctypes.c_int)
    def mapGetMtrEdit(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrEdit_t (_hMap, _number)


# Запросить - может ли матрица копироваться или экспортироваться
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCopyFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtrCopyFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrCopyFlag_t (_hMap, _number)


# Запросить - может ли матрица выводиться на печать
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения на печать
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrPrintFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtrPrintFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrPrintFlag_t (_hMap, _number)


# Запросить - можно ли показывать параметры паспорта
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет отображения параметров системы координат
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Если нет - возвращает ноль

    mapGetMtrHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrHidePassportFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtrHidePassportFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrHidePassportFlag_t (_hMap, _number)


# Запросить размер файла
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# По адресу fileSize записывается размер файла
# При ошибке возвращает ноль

    mapGetMtrFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrFileSize', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtrFileSize(_hMap: maptype.HMAP, _number: int, _fileSize: ctypes.POINTER(ctypes.c_int64)) -> int:
        return mapGetMtrFileSize_t (_hMap, _number, _fileSize)


# Запросить ширину матрицы (элементы)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrWidthInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtrWidthInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrWidthInElement_t (_hMap, _number)


# Запросить высоту матрицы (элементы)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrHeightInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtrHeightInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrHeightInElement_t (_hMap, _number)


# Запросить точность (метр/элем) матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrAccuracy', maptype.HMAP, ctypes.c_int)
    def mapGetMtrAccuracy(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrAccuracy_t (_hMap, _number)


# Установка ошибки наложения высот (в единицах матрицы)
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapSetAbsHeightDifference_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAbsHeightDifference', maptype.HMAP, ctypes.c_int, ctypes.c_double)
    def mapSetAbsHeightDifference(_hMap: maptype.HMAP, _number: int, _difference: float) -> int:
        return mapSetAbsHeightDifference_t (_hMap, _number, _difference)


# Запросить флаг изменения привязки (метры) матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrFlagLocationChanged', maptype.HMAP, ctypes.c_int)
    def mapGetMtrFlagLocationChanged(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrFlagLocationChanged_t (_hMap, _number)


# Запросить тип матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrType', maptype.HMAP, ctypes.c_int)
    def mapGetMtrType(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrType_t (_hMap, _number)


# Запросить значения псевдокода матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает 0

    maGetMtrPseudoCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'maGetMtrPseudoCode', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def maGetMtrPseudoCode(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return maGetMtrPseudoCode_t (_hMap, _number, _value)


# Запросить флаг сжатия матрицы
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# При ошибке возвращает ноль

    mapGetMtrCompress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtrCompress', maptype.HMAP, ctypes.c_int)
    def mapGetMtrCompress(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtrCompress_t (_hMap, _number)


# Занести в матрицу высот номер алгоритма сжатия блоков
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# compressnumber - номер алгоритма сжатия блоков
# При ошибке возвращает 0

    mapSetMtrCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtrCompressNumber', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtrCompressNumber(_hMap: maptype.HMAP, _number: int, _compressnumber: int) -> int:
        return mapSetMtrCompressNumber_t (_hMap, _number, _compressnumber)

    mapSetMtqCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqCompressNumber', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqCompressNumber(_hMap: maptype.HMAP, _number: int, _compressnumber: int) -> int:
        return mapSetMtqCompressNumber_t (_hMap, _number, _compressnumber)


# Сжать матрицу MTW по заданному алгоритму
# handle  - идентификатор диалога для передачи сообщений о проценте выполнения WM_PROGRESSBAR
# name    - имя сжимаемого файла MTW
# newname - имя сжатого файла MTW
# compressnumber - номер алгоритма сжатия (RMF_COMPR_32)
# borderflag - флаг удаления неотображаемых блоков (не попадающих в заданную рамку матрицы)
# При ошибке возвращает ноль

    mapMtrOptimizationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMtrOptimizationUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapMtrOptimizationUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int) -> int:
        return mapMtrOptimizationUn_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag)

    mapMtrOptimizationPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMtrOptimizationPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapMtrOptimizationPro(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mapMtrOptimizationPro_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag, _callevent, _parm)


# Удалить файл матрицы высот
# Функция предназначена для удаления матрицы высот и еe составных частей
# Матрица высот размером более 4Gb состоит из 2-х файлов: #.mtw и #.mtw.01
# Аналог функции DeleteTheFile()

    mapDeleteMtrFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtrFile', ctypes.c_char_p)
    def mapDeleteMtrFile(_name: ctypes.c_char_p) -> int:
        return mapDeleteMtrFile_t (_name)

    mapDeleteMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtrFileUn', maptype.PWCHAR)
    def mapDeleteMtrFileUn(_filename: mapsyst.WTEXT) -> int:
        return mapDeleteMtrFileUn_t (_filename.buffer())


# Переименовать имя файла матрицы высот
# Функция предназначена для переименовывания матрицы высот и её составных частей
# Матрица высот размером более 4Gb состоит из 2-х файлов: #.mtw и #.mtw.01
# Аналог функции MoveTheFile()

    mapMoveMtrFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveMtrFile', ctypes.c_char_p, ctypes.c_char_p)
    def mapMoveMtrFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p) -> int:
        return mapMoveMtrFile_t (_oldname, _newname)

    mapMoveMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveMtrFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveMtrFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        return mapMoveMtrFileUn_t (_oldname.buffer(), _newname.buffer())


# Скопировать файл матрицы высот
# Функция предназначена для копирования матрицы высот и её составных частей
# Матрица высот размером более 4Gb состоит из 2-х файлов: #.mtw и #.mtw.01
# Аналог функции CopyTheFile()

    mapCopyMtrFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMtrFile', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapCopyMtrFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p, _exist: int = 0) -> int:
        return mapCopyMtrFile_t (_oldname, _newname, _exist)

    mapCopyMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMtrFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyMtrFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int = 0) -> int:
        return mapCopyMtrFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)


# Функция подготовки легенды матрицы высот
# При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32)
# указать размер в параметре imgsize
# hmap      - идентификатор открытой векторной карты
# xmlname   - имя выходного xml-файла
# imgpath   - путь к изображениям формата png
# imgsize   - нестандартный размер изображения (сторона квадрата),
#             если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32)
# Максимальный размер изображения 1024x1024
# При ошибке возвращает 0

    mapCreateMtrLegendToXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateMtrLegendToXML', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCreateMtrLegendToXML(_hmap: maptype.HMAP, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _imgsize: int) -> int:
        return mapCreateMtrLegendToXML_t (_hmap, _xmlname.buffer(), _imgpath.buffer(), _imgsize)


# Сплайн сглаживание матрицы высот
# mtrname   - имя сглаживаемой матрицы
# smooth    - уровень сглаживания (от 0 до 1)
# hwnd      - идентификатор окна в которое послыается сообщение с процентом обработки
#             (если = 0, то сообщение не посылается)
# messageid - идентификатор сообщения с процентом обработки (WM_OBJECT)
# При ошибке возвращает 0

    mapSmoothMtrUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothMtrUn', maptype.PWCHAR, ctypes.c_double, maptype.HMESSAGE, ctypes.c_int)
    def mapSmoothMtrUn(_mtrname: mapsyst.WTEXT, _smooth: float, _hwnd: maptype.HMESSAGE, _messageid: int) -> int:
        return mapSmoothMtrUn_t (_mtrname.buffer(), _smooth, _hwnd, _messageid)


# Открыть матрицу качеств
# Возвращает идентификатор открытой матричной карты
# mtqname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# При ошибке возвращает ноль

    mapOpenMtq_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtq', ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtq(_mtqname: ctypes.c_char_p, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtq_t (_mtqname, _mode)

    mapOpenMtqUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtqUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtqUn(_mtqname: mapsyst.WTEXT, _mode: int = 0) -> maptype.HMAP:
        return mapOpenMtqUn_t (_mtqname.buffer(), _mode)


# Закрыть матрицу качеств
# hMap - идентификатор открытой основной карты
# number - номер закрываемой матрицы
# если number = 0, закрываются все матрицы в окне
# ЧТОБЫ ОСВОБОДИТЬ ВСЕ РЕСУРСЫ - НУЖНО ВЫЗВАТЬ mapCloseData(hMap)

    mapCloseMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtq', maptype.HMAP, ctypes.c_int)
    def mapCloseMtq(_hMap: maptype.HMAP, _number: int = 0) -> ctypes.c_void_p:
        return mapCloseMtq_t (_hMap, _number)


# Открыть данные матрицы качеств в заданном районе работ
# (добавить в цепочку матриц качеств)
# hMap - идентификатор открытой основной карты
# mtqname - имя открываемого файла
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение
# Возвращает номер файла в цепочке матриц
# При ошибке возвращает ноль

    mapOpenMtqForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtqForMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapOpenMtqForMap(_hMap: maptype.HMAP, _mtqname: ctypes.c_char_p, _mode: int) -> int:
        return mapOpenMtqForMap_t (_hMap, _mtqname, _mode)

    mapOpenMtqForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenMtqForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenMtqForMapUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        return mapOpenMtqForMapUn_t (_hMap, _name.buffer(), _mode)


# Закрыть данные матрицы качеств в заданном районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# Если number = 0, закрываются все матричные данные
# При ошибке возвращает ноль

    mapCloseMtqForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseMtqForMap', maptype.HMAP, ctypes.c_int)
    def mapCloseMtqForMap(_hMap: maptype.HMAP, _number: int) -> int:
        return mapCloseMtqForMap_t (_hMap, _number)

    mapGetMtqNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtqNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetMtqNameUn_t (_hMap, _number, _name.buffer(), _namesize)


# Запросить номер файла матрицы качеств в цепочке по имени файла
# В цепочке номера матриц качеств начинаются с 1
# name - имя файла матрицы качеств
# При отсутствии файла матрицы качеств в цепочке возвращает ноль

    mapGetMtqNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqNumber', maptype.HMAP, ctypes.c_char_p)
    def mapGetMtqNumber(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapGetMtqNumber_t (_hMap, _name)

    mapGetMtqNumberByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqNumberByName', maptype.HMAP, ctypes.c_char_p)
    def mapGetMtqNumberByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapGetMtqNumberByName_t (_hMap, _name)

    mapGetMtqNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqNumberUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtqNumberUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetMtqNumberUn_t (_hMap, _name.buffer())


# Запросить число открытых файлов матриц качеств
# hMap - идентификатор открытой основной карты
# При ошибке возвращает ноль

    mapGetMtqCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqCount', maptype.HMAP)
    def mapGetMtqCount(_hMap: maptype.HMAP) -> int:
        return mapGetMtqCount_t (_hMap)


# Запросить время крайнего редактирования матрицы
# hMap    - идентификатор открытых данных
# number  - номер матрицы
# Возвращает системное время редактирования (создания) по Гринвичу
# При ошибке возвращает ноль

    mapGetMtqSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqSystemTime', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetMtqSystemTime(_hMap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        return mapGetMtqSystemTime_t (_hMap, _number, _time)


# Запросить описание файла матрицы качеств
# hMap   - идентификатор открытой основной карты
# number - номер файла в цепочке
# describe - адрес структуры, в которой будет размещено
# описание матрицы
# При ошибке возвращает ноль

#   mapGetMtqDescribe_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetMtqDescribe', maptype.HMAP, ctypes.c_int, ctypes.POINTER(MTRDESCRIBE))
#   def mapGetMtqDescribe(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(MTRDESCRIBE)) -> int:
#       return mapGetMtqDescribe_t (_hMap, _number, _describe)

    mapGetMtqDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqDescribeUn', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.MTRDESCRIBEUN))
    def mapGetMtqDescribeUn(_hMap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(maptype.MTRDESCRIBEUN)) -> int:
        return mapGetMtqDescribeUn_t (_hMap, _number, _describe)


# Запросить размер элемента матрицы качеств в байтах
# hMap   - идентификатор открытой основной карты
# number - номер файла в цепочке
# Возвращаемое значение 1 соответствует типу "unsigned char".
# Возвращаемое значение 2 соответствует типу "short int".
# Возвращаемое значение 4 соответствует типу "long int".
# Возвращаемое значение 8 соответствует типу "double".
# При ошибке возвращает ноль

    mapGetMtqElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqElementSize', maptype.HMAP, ctypes.c_int)
    def mapGetMtqElementSize(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqElementSize_t (_hMap, _number)


# Запросить размер элемента матрицы в метрах по оси X
# number    - номер файла в цепочке
# metinelemX - размер элемента матрицыв метрах на местности по оси X
# При ошибке возвращает ноль

    mapGetMtqMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqMeterInElementX', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetMtqMeterInElementX(_hMap: maptype.HMAP, _number: int, _metinelemX: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtqMeterInElementX_t (_hMap, _number, _metinelemX)


# Запросить размер элемента матрицы в метрах по оси Y
# number    - номер файла в цепочке
# metinelemY - размер элемента матрицы в метрах на местности по оси Y
# При ошибке возвращает ноль

    mapGetMtqMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqMeterInElementY', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapGetMtqMeterInElementY(_hMap: maptype.HMAP, _number: int, _metinelemY: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtqMeterInElementY_t (_hMap, _number, _metinelemY)


# Запросить/Установить отображение матрицы качеств
# hMap - идентификатор открытой основной карты
# number - номер файла в цепочке
# view = 0 - не отображать
# view = 1 - полная
# view = 2 - насыщенная
# view = 3 - полупрозрачная
# view = 4 - средняя
# view = 5 - прозрачная

    mapGetMtqView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqView', maptype.HMAP, ctypes.c_int)
    def mapGetMtqView(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqView_t (_hMap, _number)

    mapSetMtqView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqView', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqView(_hMap: maptype.HMAP, _number: int, _view: int) -> int:
        return mapSetMtqView_t (_hMap, _number, _view)


# Запросить/Установить порядок отображения матрицы качеств
# hMap   - идентификатор открытой основной карты
# number - номер файла в цепочке
# order  - порядок отображения (0 - под картой, 1 - над картой)
# При ошибке возвращает ноль

    mapSetMtqViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqViewOrder(_hMap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetMtqViewOrder_t (_hMap, _number, _order)

    mapGetMtqViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqViewOrder', maptype.HMAP, ctypes.c_int)
    def mapGetMtqViewOrder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqViewOrder_t (_hMap, _number)


# Поменять очередность отображения матриц (mtq) в цепочке
# hMap   - идентификатор открытой основной карты
# oldNumber - номер файла в цепочке
# newNumber - устанавливаемый номер файла в цепочке
# При ошибке возвращает ноль

    mapChangeOrderMtqShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeOrderMtqShow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangeOrderMtqShow(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangeOrderMtqShow_t (_hMap, _oldNumber, _newNumber)


# Запросить/Установить тень матрицы качества
# hMap   - идентификатор открытой основной карты
# number - номер файла в цепочке
# value  - флаг наложения тени (1 - тень есть, 0 - нет тени)

    mapGetMtqShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqShadow', maptype.HMAP, ctypes.c_int)
    def mapGetMtqShadow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqShadow_t (_hMap, _number)

    mapSetMtqShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqShadow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqShadow(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapSetMtqShadow_t (_hMap, _number, _value)


# Создать матрицу качеств
# Возвращает идентификатор открытой матричной карты (TMapAccess#)
# Структуры BUILDMTW,MTRPROJECTIONDATA описаны в maptype.h
# palette - указатель на палитру
# countpalette - количество цветов в палитре
# name - имя файла создаваемой матрицы

    mapCreateMtq_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtq', ctypes.c_char_p, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA), ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapCreateMtq(_name: ctypes.c_char_p, _parm: ctypes.POINTER(maptype.BUILDMTW), _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA), _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int) -> maptype.HMAP:
        return mapCreateMtq_t (_name, _parm, _projectiondata, _palette, _countpalette)

    mapCreateMtqUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtqUn', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA), ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapCreateMtqUn(_name: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.BUILDMTW), _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA), _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int) -> maptype.HMAP:
        return mapCreateMtqUn_t (_name.buffer(), _parm, _projectiondata, _palette, _countpalette)


# Записать прямоугольный участок матрицы качеств из памяти
#   hMap - идентификатор открытой матричной карты
#   number - номер матрицы в цепочке.
#   bits - адрес логического начала записываемого участка
#          (см. beginning)
#   left - смещение участка матрицы слева (в элементах)
#   top - смещение участка матрицы сверху (в элементах)
#   width - ширина участка матрицы (в элементах)
#   height - высота участка матрицы (в элементах)
#   beginning - определяет, на какую строку указывает bits :
#     если beginning == 0, то bits указывает
#       на начало верхней строки выводимого участка
#     если beginning == 1, то bits указывает
#       на начало нижней строки выводимого участка
#   Размер участка, заданного адресом bits, должен быть не менее
#   (width # height # размер элемента матрицы в байтах),
#   в противном случае возможны ошибки работы с памятью.
#   Запрос размера элемента матрицы качеств в байтах
#   - функция mapGetMtqElementSize.
#   Значения элементов участка матрицы в области bits должны быть
#   записаны в единицах измерения значений данной матрицы качеств.
#   Запрос единицы измерения значений матрицы качеств
#   - функция mapGetMtqMeasure.
# При ошибке возвращает ноль

    mapPutMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutMtqFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapPutMtqFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _beginning: int) -> int:
        return mapPutMtqFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _beginning)


# Установить диапазон отображаемых элементов матрицы качеств
# hMap   - идентификатор открытой основной карты
# number - номер матрицы в цепочке.
# minvalue,maxvalue - границы диапазона
# При ошибке возвращает ноль

    mapSetMtqShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqShowRange', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapSetMtqShowRange(_hMap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        return mapSetMtqShowRange_t (_hMap, _number, _minvalue, _maxvalue)


# Установить флаги отображения элементов матрицы качеств
# вне границ диапазона, заданного в функции mapSetMtqShowRange
# hMap   - идентификатор открытой основной карты
# number - номер матрицы в цепочке.
# viewUp - отображать элементы, значения которых больше верхней
#          границы диапазона (параметр maxvalue функции mapSetMtqShowRange)
# viewDown - отображать элементы, значения которых меньше нижней
#          границы диапазона (параметр minvalue функции mapSetMtqShowRange)
# При ошибке возвращает ноль

    mapSetMtqViewOutRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqViewOutRange', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMtqViewOutRange(_hMap: maptype.HMAP, _number: int, _viewUp: int, _viewDown: int) -> int:
        return mapSetMtqViewOutRange_t (_hMap, _number, _viewUp, _viewDown)


# Запросить описание палитры матрицы качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetMtqPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetMtqPalette_t (_hMap, _palette, _count, _number)


# Запросить эталонную палитру матрицы качеств
# (без учета яркости и контрастности)
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# palette - адрес области для размещения палитры
# count   - число считываемых элементов палитры
# (размер области в байтах / 4)
# При ошибке возвращает ноль

    mapGetMtqStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetMtqStandardPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetMtqStandardPalette_t (_hMap, _palette, _count, _number)


# Установить описание палитры матрицы качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# palette - адрес устанавливаемой палитры
# count   - число элементов в новой палитре
# При ошибке возвращает ноль

    mapSetMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapSetMtqPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapSetMtqPalette_t (_hMap, _palette, _count, _number)


# Установить верхние значения диапазонов неравномерной палитры матрицы качеств
# hMap     - идентификатор открытой основной карты
# number   - номер матрицы в цепочке.
# diapason - адрес массива устанавливаемых значений диапазонов
# count    - число элементов в массиве значений диапазонов
# При ошибке возвращает ноль

    mapSetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqPaletteDiapason', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)
    def mapSetMtqPaletteDiapason(_hMap: maptype.HMAP, _diapason: ctypes.POINTER(ctypes.c_double), _count: int, _number: int) -> int:
        return mapSetMtqPaletteDiapason_t (_hMap, _diapason, _count, _number)


# Удалить верхние значения диапазонов неравномерной палитры матрицы качеств
# (палитра становится равномерной)
# hMap     - идентификатор открытой матричной карты
# number   - номер матрицы в цепочке.
# При ошибке возвращает ноль

    mapUnsetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUnsetMtqPaletteDiapason', maptype.HMAP, ctypes.c_int)
    def mapUnsetMtqPaletteDiapason(_hMap: maptype.HMAP, _number: int) -> int:
        return mapUnsetMtqPaletteDiapason_t (_hMap, _number)


# Запросить верхние значения диапазонов неравномерной палитры и минимальное
# значение элемента матрицы качеств
# hMap     - идентификатор открытой матричной карты
# minimum  - минимальное значение элемента матрицы (результат запроса)
# diapason - адрес массива верхних значений диапазонов (результат запроса)
# count    - число элементов в массиве значений диапазонов
# number   - номер матрицы в цепочке
# При ошибке и при неустановленных верхних значениях диапазонов возвращает ноль

    mapGetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqPaletteDiapason', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)
    def mapGetMtqPaletteDiapason(_hMap: maptype.HMAP, _minimum: ctypes.POINTER(ctypes.c_double), _diapason: ctypes.POINTER(ctypes.c_double), _count: int, _number: int) -> int:
        return mapGetMtqPaletteDiapason_t (_hMap, _minimum, _diapason, _count, _number)


# Сохранить в файле описание палитры матрицы качеств
# hMap    - идентификатор открытой основной карты
# palette - адрес сохраняемой палитры
#           (если palette = 0, то в файл записывается текущая
#            палитра матрицы, установленная функцией mapSetMtqPalette)
# count   - число элементов сохраняемой палитры
# number  - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapSaveMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMtqPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapSaveMtqPalette(_hMap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapSaveMtqPalette_t (_hMap, _palette, _count, _number)


# Установить описание двухинтервальной палитры матрицы качеств
# Двухинтервальная палитра формируется с использованием трёх
# цветов (начального, промежуточного, конечного), задающих границы
# двух интервалов. Составляющие интенсивности цветов внутри интервала
# равномерно изменяются от начального цвета интервала к конечному.
# hMap - идентификатор открытой основной карты
# firstColor - адрес начального цвета первого интервала
# mediumColor - адрес промежуточного цвета (конечного первого
#               интервала, начального второго интервала)
# lastColor - адрес конечного цвета второго интервала
# count  - число элементов в палитре
# mediumPosition - номер промежуточного цвета в палитре,
#                  (число от 0 до count-1)
# number - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapSetMtqTwoIntervalPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqTwoIntervalPalette', maptype.HMAP, maptype.COLORREF, maptype.COLORREF, maptype.COLORREF, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMtqTwoIntervalPalette(_hMap: maptype.HMAP, _firstColor: maptype.COLORREF, _mediumColor: maptype.COLORREF, _lastColor: maptype.COLORREF, _count: int, _mediumPosition: int, _number: int) -> int:
        return mapSetMtqTwoIntervalPalette_t (_hMap, _firstColor, _mediumColor, _lastColor, _count, _mediumPosition, _number)


# Запросить/Установить яркость палитры матрицы качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# bright  - яркость (-16..+16)

    mapGetMtqBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBright', maptype.HMAP, ctypes.c_int)
    def mapGetMtqBright(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqBright_t (_hMap, _number)

    mapSetMtqBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqBright', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqBright(_hMap: maptype.HMAP, _number: int, _bright: int) -> int:
        return mapSetMtqBright_t (_hMap, _number, _bright)


# Запросить/Установить контрастность палитры матрицы качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# contrast- контраст (-16..+16)

    mapGetMtqContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqContrast', maptype.HMAP, ctypes.c_int)
    def mapGetMtqContrast(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqContrast_t (_hMap, _number)

    mapSetMtqContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqContrast', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetMtqContrast(_hMap: maptype.HMAP, _number: int, _contrast: int) -> int:
        return mapSetMtqContrast_t (_hMap, _number, _contrast)


# Запросить число цветов в палитре матрицы качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# При ошибке возвращается 0

    mapGetMtqPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqPaletteCount', maptype.HMAP, ctypes.c_int)
    def mapGetMtqPaletteCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqPaletteCount_t (_hMap, _number)


# Запросить описание диапазона значений матрицы с номером
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# colornumber - номер диапазона значений
# colordesc - адрес структуры, в которой будет размещено
# описание диапазона значений
# При ошибке возвращает ноль

    mapGetMtqColorDescEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqColorDescEx', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.MTRCOLORDESCEX))
    def mapGetMtqColorDescEx(_hMap: maptype.HMAP, _number: int, _colornumber: int, _colordesc: ctypes.POINTER(maptype.MTRCOLORDESCEX)) -> int:
        return mapGetMtqColorDescEx_t (_hMap, _number, _colornumber, _colordesc)


# Установить цвет диапазона значений элементов матрицы с номером
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# colornumber - номер диапазона значений
# color - цвет для диапазона
# При ошибке возвращает ноль

    mapSetMtqColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqColor', maptype.HMAP, ctypes.c_int, ctypes.c_int, maptype.COLORREF)
    def mapSetMtqColor(_hMap: maptype.HMAP, _number: int, _colornumber: int, _color: maptype.COLORREF) -> int:
        return mapSetMtqColor_t (_hMap, _number, _colornumber, _color)


# Выбор значения в заданной точке из матрицы
# с номером number в цепочке.
# hMap   - идентификатор открытой основной карты
# number - номер матрицы в цепочке.
# Координаты точки (x,y) задаются в метрах.
# Возвращает значение элемента с учётом единицы измерения.
# Возвращаемое значение равно значению элемента из файла матрицы,
# делённому на 10 в степени n, где n = mapGetMtqMeasure().
# В случае ошибки при выборе значения и в случае необеспеченности
# заданной точки матричными данными возвращает ERRORHEIGHT.

    mapGetMtqValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqValue', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapGetMtqValue(_hMap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        return mapGetMtqValue_t (_hMap, _number, _x, _y)


# Возвращает интерполированное значение из матрицы качеств
# hMap   - идентификатор открытой основной карты
# number - номер матрицы качеств в цепочке
# interptype - тип интерполяции
#          1 - ближайший сосед
#          2 - интерполяция по ближайшим 3 элементам
#          3 - билинейная интерполяция по 4 ближайшим элементам
#          4 - бикубическая интерполяция по 16 ближайшим элементам
# x, y  - координаты точки в метрах
# value - возвращаемое значение (при ошибке устанавливается ERRORHEIGHT)
# hPaint - идентификатор контекста отображения для многопоточного вызова функций,
#          создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
# При ошибке возвращает 0

    mapGetMtqValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqValueEx', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapGetMtqValueEx(_hMap: maptype.HMAP, _number: int, _interptype: int, _x: float, _y: float, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetMtqValueEx_t (_hMap, _number, _interptype, _x, _y, _value)

    mapGetMtqValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqValuePro', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapGetMtqValuePro(_hMap: maptype.HMAP, _number: int, _interptype: int, _x: float, _y: float, _value: ctypes.POINTER(ctypes.c_double), _hPaint: maptype.HPAINT) -> float:
        return mapGetMtqValuePro_t (_hMap, _number, _interptype, _x, _y, _value, _hPaint)


# Чтение элемента матрицы качеств по абсолютным индексам
# hMap   - идентификатор открытой карты
# number - номер файла в цепочке
# value  - полученное значение элемента в метрах
# string - индекс строки матрицы (значение от 0 до height-1, где height - высота
#          матрицы элементах, запрашиваемая функцией mapGetMtqHeightInElement)
# column - индекс колонки матрицы (значение от 0 до width-1, где width - ширина
#          матрицы элементах, запрашиваемая функцией mapGetMtqWidthInElement)
# При ошибке возвращает ноль

    mapGetMtqPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqPoint', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)
    def mapGetMtqPoint(_hMap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double), _string: int, _column: int) -> int:
        return mapGetMtqPoint_t (_hMap, _number, _value, _string, _column)


# Занесение значения в элемент матрицы,
# соответствующий заданной точке.
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# Координаты точки (x,y) задаются в метрах
# В матрицу заносится значение элемента с учётом единицы измерения.
# Заносимое значение равно h, умноженному на 10 в степени n,
# где n = mapGetMtqMeasure().
# В случае ошибки возвращает ноль.

    mapPutMtqValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutMtqValue', maptype.HMAP, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutMtqValue(_hMap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        return mapPutMtqValue_t (_hMap, _number, _x, _y, _h)


# Запросить фактические габариты отображаемой матрицы в метрах в районе работ
# При отображение матрицы по рамке возвращаются габариты рамки
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# frame   - адрес для размещения результата
# При ошибке возвращает ноль

    mapGetActualMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActualMtqFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetActualMtqFrame(_hMap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        return mapGetActualMtqFrame_t (_hMap, _frame, _number)


# Запросить масштаб матрицы
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# При ошибке возвращает ноль

    mapGetMtqScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqScale', maptype.HMAP, ctypes.c_int)
    def mapGetMtqScale(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqScale_t (_hMap, _number)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hMap     - идентификатор открытой основной карты
# number   - номер файла в цепочке
# Если нет - возвращает ноль

    mapIsMtqGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMtqGeoSupported', maptype.HMAP, ctypes.c_int)
    def mapIsMtqGeoSupported(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsMtqGeoSupported_t (_hMap, _number)


# Запросить данные о проекции матричных данных
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# projectiondata - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MTRPROJECTIONDATA описанa в maptype.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapGetMtqProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtqProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetMtqProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtqProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapGetMtqProjectionData(_hMap: maptype.HMAP, _number: int, _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        return mapGetMtqProjectionData_t (_hMap, _number, _projectiondata)


# Установить данные о проекции матричных данных
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке.
# mapregister - адрес структуры, содержащей данные о проекции
# Структурa MAPREGISTEREX описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtqProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqProjectionData', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapSetMtqProjectionData(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapSetMtqProjectionData_t (_hMap, _number, _mapregister)


# Установить данные о проекции матрицы качеств
# hMap   - идентификатор открытой основной векторной карты
# number - номер матрицы в цепочке.
# mapregister, datumparam, ellipsoidparam - адреса структур, содержащих данные о проекции
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM описаны в mapcreat.h
# ttype  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapSetMtqProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqProjectionDataPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtqProjectionDataPro(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetMtqProjectionDataPro_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSetMtqProjectionDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqProjectionDataEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtqProjectionDataEx(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetMtqProjectionDataEx_t (_hMap, _number, _mapregister, _datumparam, _ellipsoidparam)


# Запросить данные о проекции матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# mapregister - адрес структуры, в которой будут размещены
# данные о проекции
# Структурa MAPREGISTEREX описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtqProjectionDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqProjectionDataEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtqProjectionDataEx(_hMap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapGetMtqProjectionDataEx_t (_hMap, _number, _mapregister)


# Запросить параметры эллипсоида матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла матрицы в цепочке
# ellipsoidparam - адрес структуры, в которой будут размещены
# параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtqEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtqEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetMtqEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Установить параметры эллипсоида матрицы
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла матрицы в цепочке.
# ellipsoidparam - адрес структуры, содержащей параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtqEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqEllipsoidParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtqEllipsoidParam(_hMap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetMtqEllipsoidParam_t (_hMap, _number, _ellipsoidparam)


# Запросить коэффициенты трансформирования геодезических координат матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла матрицы в цепочке
# datumparam - адрес структуры, в которой будут размещены
# коэффициенты трансформирования геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapGetMtqDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtqDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetMtqDatumParam_t (_hMap, _number, _datumparam)


# Установить коэффициенты трансформирования геодезических координат матрицы
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла матрицы в цепочке.
# datumparam - адрес структуры, содержащей коэффициенты трансформирования
# геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    mapSetMtqDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqDatumParam', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtqDatumParam(_hMap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetMtqDatumParam_t (_hMap, _number, _datumparam)


# Чтение прямоугольного участка матрицы качеств в заданную область памяти
#   hMap - идентификатор открытой основной карты (TMapAccess #)
#   number - номер матрицы в цепочке.
#   bits - указатель на начало области памяти
#   left - смещение участка матрицы слева (в элементах)
#   top - смещение участка матрицы сверху (в элементах)
#   width - ширина участка матрицы (в элементах)
#   height - высота участка матрицы (в элементах)
#   widthinbyte - ширинa участка матрицы в байтах
#   Размер участка, заданного адресом bits, должен быть не менее
#   (width # height # размер элемента матрицы в байтах),
#   в противном случае возможны ошибки работы с памятью.
#   Запрос размера элемента матрицы качеств в байтах
#   - функция mapGetMtqElementSize.
#   Значения элементов участка матрицы записываются в область bits
#   в единицах измерения значений данной матрицы качеств.
#   Запрос единицы измерения значений матрицы качеств
#   - функция mapGetMtqMeasure.
# При ошибке возвращает ноль

    mapGetMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqFrame', maptype.HMAP, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetMtqFrame(_hMap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int = 0) -> int:
        return mapGetMtqFrame_t (_hMap, _number, _bits, _left, _top, _width, _height, _widthinbyte)


# Запросить единицу измерения значений матрицы качеств
# hMap - идентификатор открытой основной карты (TMapAccess #)
# number - номер матрицы в цепочке.
# Значение элемента в файле матрицы равно значению качества,
# умноженному на 10 в степени n, где n - единица измерения.
# Функция возвращает значение поля Unit структуры параметров создания
# матрицы BUILDMTW
# Возвращаемые значения :
#   0-"метры", 1-"дециметры", 2-"сантиметры", 3-"миллиметры"
# При ошибке возвращает -1

    mapGetMtqMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqMeasure', maptype.HMAP, ctypes.c_int)
    def mapGetMtqMeasure(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqMeasure_t (_hMap, _number)


# Построение зоны затопления по набору отметок уровня воды
# Уровень воды задаётся величиной относительно поверхности рельефа
# В результате построения формируется матрица качеств, элементы
# которой содержат глубины в зоне затопления.
# Габариты матрицы качеств определяются координатами точек с
# отметками уровня воды (массив pointArray) и величиной расширения
# габаритов области (areaExtension).
# hMap    - исходная карта с матрицей высот для построения зоны затопления,
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
# handle - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
#   Если handle равно нулю - сообщения не посылаются.
# При ошибке возвращает ноль.

    mapBuildFloodZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildFloodZone', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZone(_hMap: maptype.HMAP, _mtqName: ctypes.c_char_p, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HWND) -> int:
        return mapBuildFloodZone_t (_hMap, _mtqName, _pointArray, _pointCount, _areaExtension, _minDepth, _handle)

    mapBuildFloodZoneUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildFloodZoneUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZoneUn(_hMap: maptype.HMAP, _mtqName: mapsyst.WTEXT, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HWND) -> int:
        return mapBuildFloodZoneUn_t (_hMap, _mtqName.buffer(), _pointArray, _pointCount, _areaExtension, _minDepth, _handle)


# Построение зоны затопления по набору отметок уровня воды
# Уровень воды задаётся абсолютным значением высоты
# В результате построения формируется матрица качеств, элементы
# которой содержат глубины в зоне затопления.
# Габариты матрицы качеств определяются координатами точек с
# отметками уровня воды (массив pointArray) и величиной расширения
# габаритов области (areaExtension).
# hMap    - исходная карта с матрицей высот для построения зоны затопления,
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
# handle - идентификатор окна диалога, которому посылаются
# сообщения о ходе процесса :
#   0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#   если процесс должен быть принудительно завершен, в ответ
#   должно вернуться значение 0x0581.
#   Если handle равно нулю - сообщения не посылаются.
# При ошибке возвращает ноль.

    mapBuildFloodZoneAbs_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildFloodZoneAbs', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZoneAbs(_hMap: maptype.HMAP, _mtqName: ctypes.c_char_p, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HWND) -> int:
        return mapBuildFloodZoneAbs_t (_hMap, _mtqName, _pointArray, _pointCount, _areaExtension, _minDepth, _handle)

    mapBuildFloodZoneAbsUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildFloodZoneAbsUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZoneAbsUn(_hMap: maptype.HMAP, _mtqName: mapsyst.WTEXT, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _areaExtension: float, _minDepth: float, _handle: maptype.HWND) -> int:
        return mapBuildFloodZoneAbsUn_t (_hMap, _mtqName.buffer(), _pointArray, _pointCount, _areaExtension, _minDepth, _handle)


# Построение матрицы качеств по массиву значений характеристики качества.
# hMap - идентификатор открытой исходной карты для построения матрицы качеств
# mtqName - полное имя создаваемой матрицы качеств
# palette - адрес палитры создаваемой матрицы качеств,
#           если palette равно нулю - используется палитра по умолчанию
# countpalette - количество цветов в палитре
# pointArray - адрес массива значений характеристики качества
#              Координаты точек (pointArray->X,pointArray->Y) задаются в метрах
#              в системе координат векторной карты
# pointCount - число точек в массиве pointArray
#              Размер в байтах массива, заданного адресом pointArray, должен
#              быть не менее pointCount # sizeof(XYHDOUBLE), в противном случае
#              возможны ошибки работы с памятью
# elemSizeMeters - размер стороны элементарного участка в метрах на местности
#                  (дискрет матрицы)
# minValue,maxValue - диапазон значений характеристики качества создаваемой матрицы
#                     качеств, если minValue >= maxValue - в матрицу заносится
#                     фактический диапазон значений из массива pointArray
# handle - идентификатор окна диалога, которому посылаются
#          сообщения о ходе процесса :
#          0x0581 - сообщение о проценте выполненных работ (в WPARAM),
#          если процесс должен быть принудительно завершен, в ответ
#          должно вернуться значение 0x0581.
#          Если handle равно нулю - сообщения не посылаются.
# При ошибке возвращает ноль.

    mapBuildMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtq', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildMtq(_hMap: maptype.HMAP, _mtqName: ctypes.c_char_p, _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _elemSizeMeters: float, _minValue: float, _maxValue: float, _handle: maptype.HWND) -> int:
        return mapBuildMtq_t (_hMap, _mtqName, _palette, _countpalette, _pointArray, _pointCount, _elemSizeMeters, _minValue, _maxValue, _handle)

    mapBuildMtqUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMtqUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildMtqUn(_hMap: maptype.HMAP, _mtqName: mapsyst.WTEXT, _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int, _pointArray: ctypes.POINTER(maptype.XYHDOUBLE), _pointCount: int, _elemSizeMeters: float, _minValue: float, _maxValue: float, _handle: maptype.HWND) -> int:
        return mapBuildMtqUn_t (_hMap, _mtqName.buffer(), _palette, _countpalette, _pointArray, _pointCount, _elemSizeMeters, _minValue, _maxValue, _handle)


# Формирование палитры матрицы качеств
# Для формирования результирующей палитры (resultPalette) используется исходная
# палитра (skeletPalette), количество цветов результирующей палитры
# (resultColorCount) и флаг плавного изменения цветов (smoothColorModification).
# skeletPalette - исходная (скелетная) палитра, массив размером sizeof(COLORREF)#256,
#                 содержащий граничные цвета интервалов, разделённые пустыми
#                 элементами (значение 0xFFFFFFFF);
# resultPalette - результирующая палитра, массив размером sizeof(COLORREF)#256;
# resultColorCount - количество формируемых цветов результирующей палитры
#                    (не более 256);
# smoothColorModification - флаг плавного изменения цветов результирующей палитры :
#   0 - внутренние цвета интервала повторяют начальный цвет интервала,
#   1 - составляющие интенсивности внутренних цветов интервала равномерно
#       изменяются от начального цвета интервала к конечному.
# Цвета исходной палитры переносятся в соответствующие позиции результирующей
# палитры, остальные цвета результирующей палитры заполняются поинтервально в
# зависимости от значения флага smoothColorModification.
# При ошибке возвращает ноль.

    mapMakeMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMakeMtqPalette', ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapMakeMtqPalette(_skeletPalette: ctypes.POINTER(maptype.COLORREF), _resultPalette: ctypes.POINTER(maptype.COLORREF), _resultColorCount: int, _smoothColorModification: int) -> int:
        return mapMakeMtqPalette_t (_skeletPalette, _resultPalette, _resultColorCount, _smoothColorModification)


# Построение матрицы поверхности (матрицы качеств или матрицы высот)
# по данным векторной карты. Если mtrparm->FileMtw равно 1, то строится
# матрица высот (#.mtw), иначе строится матрица качеств (#.mtq).
# hMap - идентификатор открытой исходной карты для построения матрицы
# mtrname - полное имя создаваемой матрицы
# mtrparm - параметры создаваемой матрицы (структура BUILDSURFACE описана в maptype.h)
# При ошибке возвращает ноль.

    mapBuildMatrixSurface_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMatrixSurface', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.BUILDSURFACE))
    def mapBuildMatrixSurface(_hMap: maptype.HMAP, _mtrname: ctypes.c_char_p, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        return mapBuildMatrixSurface_t (_hMap, _mtrname, _mtrparm)

    mapBuildMatrixSurfaceUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildMatrixSurfaceUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE))
    def mapBuildMatrixSurfaceUn(_hMap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        return mapBuildMatrixSurfaceUn_t (_hMap, _mtrname.buffer(), _mtrparm)


# Удалить матрицу качеств
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке
# При ошибке возвращает ноль

    mapDeleteMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtq', maptype.HMAP, ctypes.c_int)
    def mapDeleteMtq(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteMtq_t (_hMap, _number)


# Определение способа отображения матрицы (относительно рамки)
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке
# Возвращает 1 - при отображении матрицы по рамке
#            0 - при отображении матрицы без учета рамки

    mapGetShowMtqByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetShowMtqByBorder', maptype.HMAP, ctypes.c_int)
    def mapGetShowMtqByBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetShowMtqByBorder_t (_hMap, _number)


# Определение существования рамки матрицы
# hMap    - идентификатор открытой основной карты
# number  - номер матрицы в цепочке
# Если рамка матрицы существует возвращает 1, иначе возвращает 0.

    mapGetExistenceMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetExistenceMtqBorder', maptype.HMAP, ctypes.c_int)
    def mapGetExistenceMtqBorder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetExistenceMtqBorder_t (_hMap, _number)


# Установка отображения матрицы по рамке
# hMap      - идентификатор открытой основной карты
# number    - номер матрицы в цепочке
# value = 1 - отобразить матрицу  по рамке
#       = 0 - отобразить матрицу  без учета рамки
# При ошибке возвращает ноль

    mapSetShowMtqByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetShowMtqByBorder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetShowMtqByBorder(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapSetShowMtqByBorder_t (_hMap, _number, _value)

    mapShowMtqByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapShowMtqByBorder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapShowMtqByBorder(_hMap: maptype.HMAP, _number: int, _value: int) -> int:
        return mapShowMtqByBorder_t (_hMap, _number, _value)


# Запросить значения масштаба нижней и верхней границ видимости матрицы
# hMap   - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# По адресу bottomScale записывается знаменатель масштаба нижней границы видимости матрицы
# По адресу topScale записывается знаменатель масштаба верхней границы видимости матрицы
# При ошибке возвращает ноль

    mapGetMtqRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetMtqRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: ctypes.POINTER(ctypes.c_int), _topScale: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetMtqRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить значения масштаба нижней и верхней границ видимости матрицы
# hMap   - идентификатор открытой основной карты
# number - номер матрицы в цепочке
# bottomScale - знаменатель масштаба нижней границы видимости матрицы
# topScale    - знаменатель масштаба верхней границы видимости матрицы
#               bottomScale <= topScale, иначе возвращает 0
# При ошибке возвращает ноль

    mapSetMtqRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMtqRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: int, _topScale: int) -> int:
        return mapSetMtqRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Определить координаты и порядковый номер точки рамки, которая
# входит в прямоугольник Габариты растра(матрицы) и
# имеет наименьшее удаление от точки pointIn (координаты в метрах).
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла в цепочке
# По адресу pointOut записываются координаты найденной точки в метрах
# При ошибке или отсутствии рамки возвращает 0.

    mapGetImmediatePointOfMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImmediatePointOfMtqBorder', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtqBorder(_hMap: maptype.HMAP, _number: int, _pointIn: ctypes.POINTER(maptype.DOUBLEPOINT), _pointOut: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetImmediatePointOfMtqBorder_t (_hMap, _number, _pointIn, _pointOut)


# Запросить координаты Юго-Западного угла матрицы в метрах
# hMap    - идентификатор открытой основной векторной карты
# number  - номер файла в цепочке
# По адресу x,y записываются координаты найденной точки в метрах
# При ошибке возвращает 0

    mapGetSouthWestMtqPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSouthWestMtqPlane', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetSouthWestMtqPlane(_hMap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetSouthWestMtqPlane_t (_hMap, _number, _x, _y)


# Запросить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# При ошибке возвращает ноль

    mapGetActiveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActiveMtq', maptype.HMAP)
    def mapGetActiveMtq(_hMap: maptype.HMAP) -> int:
        return mapGetActiveMtq_t (_hMap)


# Установить активную матрицу
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapSetActiveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveMtq', maptype.HMAP, ctypes.c_int)
    def mapSetActiveMtq(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSetActiveMtq_t (_hMap, _number)


# Открыта ли матрица с номером "number"
# Функция возвращает признак открытия указанной матрицы в документе - (1/0).
# При ошибке возвращает ноль.

    mapIsOpenMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsOpenMtq', maptype.HMAP, ctypes.c_int)
    def mapIsOpenMtq(_hMap: maptype.HMAP, _number: int) -> int:
        return mapIsOpenMtq_t (_hMap, _number)


# Запросить флаг редактируемости матрицы
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqEdit', maptype.HMAP, ctypes.c_int)
    def mapGetMtqEdit(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqEdit_t (_hMap, _number)


# Запросить - может ли матрица копироваться или экспортироваться
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqCopyFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtqCopyFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqCopyFlag_t (_hMap, _number)


# Запросить - может ли матрица выводиться на печать
# Для данных, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения на печать
# hMap     - идентификатор открытых данных
# number   - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqPrintFlag', maptype.HMAP, ctypes.c_int)
    def mapGetMtqPrintFlag(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqPrintFlag_t (_hMap, _number)


# Запросить размер файла
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# По адресу fileSize записывается размер файла
# При ошибке возвращает ноль

    mapGetMtqFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqFileSize', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtqFileSize(_hMap: maptype.HMAP, _number: int, _fileSize: ctypes.POINTER(ctypes.c_int64)) -> int:
        return mapGetMtqFileSize_t (_hMap, _number, _fileSize)


# Запросить ширину матрицы (элементы)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqWidthInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtqWidthInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqWidthInElement_t (_hMap, _number)


# Запросить высоту матрицы (элементы)
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqHeightInElement', maptype.HMAP, ctypes.c_int)
    def mapGetMtqHeightInElement(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqHeightInElement_t (_hMap, _number)


# Запросить точность (метр/элем) матрицы
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqAccuracy', maptype.HMAP, ctypes.c_int)
    def mapGetMtqAccuracy(_hMap: maptype.HMAP, _number: int) -> float:
        return mapGetMtqAccuracy_t (_hMap, _number)


# Запросить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapGetMtqLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtqLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetMtqLocation_t (_hMap, _number, _location)


# Установить привязку матрицы  в метрах в районе работ
# hMap -  идентификатор открытых данных
# number - номер матрицы в списке открытых матриц
# location   - координаты юго-западного угла матрицы
# При ошибке возвращает ноль

    mapSetMtqLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqLocation', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtqLocation(_hMap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSetMtqLocation_t (_hMap, _number, _location)


# Запросить флаг изменения привязки (метры) матрицы
# hMap       - идентификатор открытой векторной карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqFlagLocationChanged', maptype.HMAP, ctypes.c_int)
    def mapGetMtqFlagLocationChanged(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqFlagLocationChanged_t (_hMap, _number)


# Установить условное имя матрицы качеств (имя пользователя)
# hMap   - идентификатор открытой основной карты (TMapAccess #)
# number - номер матрицы в цепочке
# username - имя пользователя
# При ошибке возвращает ноль

    mapSetMtqUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqUserName', maptype.HMAP, ctypes.c_int, ctypes.c_char_p)
    def mapSetMtqUserName(_hMap: maptype.HMAP, _number: int, _username: ctypes.c_char_p) -> int:
        return mapSetMtqUserName_t (_hMap, _number, _username)

    mapSetMtqUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqUserNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR)
    def mapSetMtqUserNameUn(_hMap: maptype.HMAP, _number: int, _username: mapsyst.WTEXT) -> int:
        return mapSetMtqUserNameUn_t (_hMap, _number, _username.buffer())

    mapGetMtqUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqUserNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtqUserNameUn(_hMap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetMtqUserNameUn_t (_hMap, _number, _name.buffer(), _namesize)


# Запросить число строк блоков матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBlockRow', maptype.HMAP, ctypes.c_int)
    def mapGetMtqBlockRow(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqBlockRow_t (_hMap, _number)


# Запросить число столбцов блоков матрицы
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBlockColumn', maptype.HMAP, ctypes.c_int)
    def mapGetMtqBlockColumn(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqBlockColumn_t (_hMap, _number)


# Запросить вертикальный размер блока матрицы в элементах
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBlockSide', maptype.HMAP, ctypes.c_int)
    def mapGetMtqBlockSide(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqBlockSide_t (_hMap, _number)


# Запросить ширину блока матрицы в элементах
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBlockWidth', maptype.HMAP, ctypes.c_int)
    def mapGetMtqBlockWidth(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetMtqBlockWidth_t (_hMap, _number)


# Возврат флага отображения блока матрицы
# (0 - не отображается, 1- отображается, 2 - разделен рамкой )
# number - номер файла в цепочке
# i - порядковый номер (индекс) блока, i = str # blockColumnCount + col, где:
#     str - индекс строки блоков,
#     blockColumnCount - число столбцов блоков матрицы (функция mapGetMtqBlockColumn)
#     col - индекс столбца блоков
# При ошибке возвращает ноль

    mapCheckMtqBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckMtqBlockVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapCheckMtqBlockVisible(_hMap: maptype.HMAP, _number: int, _i: int) -> int:
        return mapCheckMtqBlockVisible_t (_hMap, _number, _i)


# Установить рамку матрицы по метрике замкнутого объекта
# Замкнутый объект должен иметь не менее 4-х точек
# hMap   - идентификатор открытой основной векторной карты
# number - номер файла в цепочке
# info   - замкнутый объект карты
# После выполнения функции отображение матрицы ограничится заданной областью
# При ошибке возвращает ноль

    mapSetMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapSetMtqBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapSetMtqBorder_t (_hMap, _number, _info)


# Запросить объект рамки матрицы качеств
# hMap       - идентификатор открытой основной векторной карты
# number     - номер файла в цепочке
# info       - идентификатор объекта рамки матрицы
# При ошибке возвращает ноль

    mapGetMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqBorder', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapGetMtqBorder(_hMap: maptype.HMAP, _number: int, _info: maptype.HOBJ) -> int:
        return mapGetMtqBorder_t (_hMap, _number, _info)


# Запросить ширину текущего блока column матрицы в элементах
# (с учетом усеченных блоков)
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqCurrentBlockWidth', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMtqCurrentBlockWidth(_hMap: maptype.HMAP, _number: int, _column: int) -> int:
        return mapGetMtqCurrentBlockWidth_t (_hMap, _number, _column)


# Запросить высоту текущего блока string матрицы в элементах
# (с учетом усеченных блоков)
# number - номер файла в цепочке
# При ошибке возвращает ноль

    mapGetMtqCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqCurrentBlockHeight', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapGetMtqCurrentBlockHeight(_hMap: maptype.HMAP, _number: int, _string: int) -> int:
        return mapGetMtqCurrentBlockHeight_t (_hMap, _number, _string)


# Записать изменения матрицы в файл
# hMap       - идентификатор открытой карты
# number     - номер файла в цепочке
# При ошибке возвращает ноль

    mapSaveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMtq', maptype.HMAP, ctypes.c_int)
    def mapSaveMtq(_hMap: maptype.HMAP, _number: int) -> int:
        return mapSaveMtq_t (_hMap, _number)


# Удалить файл матрицы качеств
# Функция предназначена для удаления матрицы и еe составных частей
# Матрица размером более 4Gb состоит из 2-х файлов: #.mtq и #.mtq.01
# Аналог функции DeleteTheFile()
# При ошибке возвращает ноль

    mapDeleteMtqFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtqFile', ctypes.c_char_p)
    def mapDeleteMtqFile(_name: ctypes.c_char_p) -> int:
        return mapDeleteMtqFile_t (_name)

    mapDeleteMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMtqFileUn', maptype.PWCHAR)
    def mapDeleteMtqFileUn(_name: mapsyst.WTEXT) -> int:
        return mapDeleteMtqFileUn_t (_name.buffer())


# Переименовать имя файла матрицы качеств
# Функция предназначена для переименовывания матрицы и её составных частей
# Матрица размером более 4Gb состоит из 2-х файлов: #.mtq и #.mtq.01
# Аналог функции MoveTheFile()
# При ошибке возвращает ноль

    mapMoveMtqFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveMtqFile', ctypes.c_char_p, ctypes.c_char_p)
    def mapMoveMtqFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p) -> int:
        return mapMoveMtqFile_t (_oldname, _newname)

    mapMoveMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMoveMtqFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveMtqFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        return mapMoveMtqFileUn_t (_oldname.buffer(), _newname.buffer())


# Скопировать файл матрицы качеств
# Функция предназначена для копирования матрицы и её составных частей
# Матрица размером более 4Gb состоит из 2-х файлов: #.mtq и #.mtq.01
# Аналог функции CopyTheFile()
# При ошибке возвращает ноль

    mapCopyMtqFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMtqFile', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapCopyMtqFile(_oldname: ctypes.c_char_p, _newname: ctypes.c_char_p, _exist: int = 0) -> int:
        return mapCopyMtqFile_t (_oldname, _newname, _exist)

    mapCopyMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMtqFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyMtqFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int = 0) -> int:
        return mapCopyMtqFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)


# Запись блока {string,column} в файл матрицы из памяти bits.
# number    - номер файла в цепочке
#  bits     - указатель на начало изображения битовой области
#  sizebits - размер области bits в байтах
# Возвращает количество записанных байт.
# При ошибке возвращает ноль

    mapWriteMtqBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWriteMtqBlock', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapWriteMtqBlock(_hMap: maptype.HMAP, _number: int, _string: int, _column: int, _bits: ctypes.c_char_p, _sizebits: int) -> int:
        return mapWriteMtqBlock_t (_hMap, _number, _string, _column, _bits, _sizebits)


# Запросить размер текущего блока {string,column} матрицы в байтах
# (с учетом усеченных блоков)
# number - номер файла в цепочке
# string, column - строка и столбец блока соотвественно
# При ошибке возвращает ноль

    mapGetMtqCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqCurrentBlockSize', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetMtqCurrentBlockSize(_hMap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        return mapGetMtqCurrentBlockSize_t (_hMap, _number, _string, _column)


# Функция подготовки легенды матрицы качеств
# При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32)
# указать размер в параметре imgsize
# hmap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# xmlname   - имя выходного xml-файла
# imgpath   - путь к изображениям формата png
# imgsize   - нестандартный размер изображения (сторона квадрата),
#             если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32)
# Максимальный размер изображения 1024x1024
# При ошибке возвращает 0

    mapCreateMtqLegendToXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateMtqLegendToXML', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCreateMtqLegendToXML(_hmap: maptype.HMAP, _number: int, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _imgsize: int) -> int:
        return mapCreateMtqLegendToXML_t (_hmap, _number, _xmlname.buffer(), _imgpath.buffer(), _imgsize)


# Чтение названия характеристики матрицы качеств
# hmap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# При ошибке возвращает 0

    mapGetMtqValueName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqValueName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtqValueName(_hMap: maptype.HMAP, _number: int, _value: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMtqValueName_t (_hMap, _number, _value.buffer(), _size)


# Запись названия характеристики матрицы качеств
# hmap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# При ошибке возвращает 0

    mapSetMtqValueName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqValueName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR)
    def mapSetMtqValueName(_hMap: maptype.HMAP, _number: int, _value: mapsyst.WTEXT) -> int:
        return mapSetMtqValueName_t (_hMap, _number, _value.buffer())


# Чтение названия единицы измерения матрицы качеств
# hmap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# При ошибке возвращает 0

    mapGetMtqUnitName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtqUnitName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMtqUnitName(_hMap: maptype.HMAP, _number: int, _unit: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMtqUnitName_t (_hMap, _number, _unit.buffer(), _size)


# Запись названия единицы измерения матрицы качеств
# hmap      - идентификатор открытой векторной карты
# number    - номер файла в цепочке
# При ошибке возвращает 0

    mapSetMtqUnitName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMtqUnitName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR)
    def mapSetMtqUnitName(_hMap: maptype.HMAP, _number: int, _value: mapsyst.WTEXT) -> int:
        return mapSetMtqUnitName_t (_hMap, _number, _value.buffer())


# Обновить уменьшенную копию
# hMap       - идентификатор открытой основной векторной карты
# number     - номер матрицы качеств в цепочке
# При ошибке возвращает 0

    mapUpdateMtqDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateMtqDuplicates', maptype.HMAP, ctypes.c_int)
    def mapUpdateMtqDuplicates(_hMap: maptype.HMAP, _number: int) -> int:
        return mapUpdateMtqDuplicates_t (_hMap, _number)


# Преобразование матриц MTW/MTQ (MTW - матрица высот, MTQ - матрица качеств)
# name - полное имя исходной матрицы MTW или MTQ
#   если исходная матрица - MTW, то функция создаёт матрицу качеств,
#   имя результирующего файла формируется из исходного имени с заменой
#   расширения на mtq
#   если исходная матрица - MTQ, то функция создаёт матрицу высот
#   (файл с расширением mtw)
# minimum,maximum - минимальное,максимальное значение характеристики (высоты),
#   устанавливаемое в заголовок результирующей матрицы
#   если minimum = maximum = 0, то в заголовок результирующей матрицы
#   устанавливаются minimum,maximum исходной матрицы
# Параметры colorCount, scaleType, palette, diapason задают описание палитры
# результирующей матрицы качеств и используются только для преобразования MTW в MTQ
# (если исходная матрица - MTW). Если данные параметры не заданы (равны нулю),
# то создаваемый файл MTQ содержит палитру матрицы высот.
# Матрица высот, полученная в результате преобразования MTQ в MTW,
# отображается в текущей палитре матриц высот, установленной в документе.
# colorCount - кол-во цветов палитры результирующей матрицы качеств
# scaleType - тип шкалы палитры результирующей матрицы качеств:
#   1 - шкала с равномерными диапазонами
#   2 - шкала с неравномерными диапазонами (необходимо задать параметр diapason)
# Значения характеристики (высоты) матрицы разделяются на colorCount
# диапазонов значений, каждому из которых соответствует цвет палитры.
# Диапазоны значений и цвета палитры располагаются от минимального значения
# характеристики (высоты) к максимальному.
# palette - адрес массива цветов палитры результирующей матрицы качеств,
#           размер массива должен быть не менее colorCount,
#           иначе возможны ошибки работы с памятью
# diapason - адрес массива верхних значений диапазонов неравномерной палитры
#            матрицы качеств, используется при scaleType = 2,
#            размер массива должен быть не менее colorCount,
#            иначе возможны ошибки работы с памятью
# При успешном завершении возвращает значение 1
# При ошибке возвращает значение, меньшее 1 (код ошибки):
#   0 - ошибка входных параметров
#  -1 - ошибка открытия исходной матрицы
#  -2 - исходный файл не является матрицей
#  -3 - ошибка копирования исходной матрицы с заменой расширения
#  -4 - ошибка открытия результирующей матрицы

    mapConvertMatrix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapConvertMatrix', maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_double))
    def mapConvertMatrix(_name: mapsyst.WTEXT, _minimum: float = 0, _maximum: float = 0, _colorCount: int = 0, _scaleType: int = 0, _palette: ctypes.POINTER(maptype.COLORREF) = None, _diapason: ctypes.POINTER(ctypes.c_double) = None) -> int:
        return mapConvertMatrix_t (_name.buffer(), _minimum, _maximum, _colorCount, _scaleType, _palette, _diapason)


# Открытие матрицы (Egm2008 или другой)
# Если имя файла не задано (mtrname равно 0), то проверяется наличие следущих
# матриц в папке приложения:
# egm2008_1min.mtw  (размер элемента 1 минута)
# egm2008_2.5min.mtw (размер элемента 2.5 минуты)
# При нахождении матрицы выполняется ее открытие
# mtrname     - путь к открываемой модели геоида/квазигеоида (MTW) или 0
# multithread - признак применения матрицы в потоке (если не равен 0, то открывается отдельно,
# независимо от наличия уже открытой ранее матрицы, со своим буфером для чтения блоков)
# Каждый поток должен иметь свой идентификатор открытой матрицы,
# полученный с параметром multithread равным 1
# Возвращает идентификатор открытой матрицы Egm2008
# При ошибке возвращает 0

    mapOpenEgmPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEgmPro', maptype.PWCHAR, ctypes.c_int)
    def mapOpenEgmPro(_mtrname: mapsyst.WTEXT, _multithread: int) -> ctypes.c_void_p:
        return mapOpenEgmPro_t (_mtrname.buffer(), _multithread)

    mapOpenEgm2008Un_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEgm2008Un', maptype.PWCHAR)
    def mapOpenEgm2008Un(_mtrname: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapOpenEgm2008Un_t (_mtrname.buffer())

    mapOpenEgm2008_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEgm2008', ctypes.c_char_p)
    def mapOpenEgm2008(_mtrname: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapOpenEgm2008_t (_mtrname)


# Закрытие матрицы
# hmtr - идентификатор открытой матрицы

    mapCloseEgm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseEgm', ctypes.c_void_p)
    def mapCloseEgm(_hmtr: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseEgm_t (_hmtr)

    mapCloseEgm2008_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseEgm2008', ctypes.c_void_p)
    def mapCloseEgm2008(_hmtr: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseEgm2008_t (_hmtr)


# Чтение высоты геоида/квазигеоида над поверхностью эллипсоида wgs84
# по геодезическим координатам на эллипсоиде WGS84
# hmtr - идентификатор открытой матрицы
# interptype - тип интерполяциия
#          1 - ближайший сосед
#          2 - интерполяция по ближайшим 3 элементам
#          3 - билинейная интерполяция по 4 ближайшим элементам
#          4 - бикубическая интерполяция по 16 ближайшим элементам
# b - широта точки на эллипсоиде WGS84 в радианах
# l - долгота точки на эллипсоиде WGS84 в радианах
# h - возвращаемая высота геоида над эллипсоидом WGS84 в метрах (поправка)
# При переходе от геодезической высоты WGS84 к нормальной высоте (MSL)
# необходимо вычесть полученную поправку
# При ошибке возвращает 0

    mapReadEgm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadEgm', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapReadEgm(_hmtr: ctypes.c_void_p, _interptype: int, _b: float, _l: float, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapReadEgm_t (_hmtr, _interptype, _b, _l, _h)

    mapReadEgm2008_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadEgm2008', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapReadEgm2008(_hmtr: ctypes.c_void_p, _interptype: int, _b: float, _l: float, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapReadEgm2008_t (_hmtr, _interptype, _b, _l, _h)


# Запросить имя открытой матрицы
# hmtr - идентификатор открытой матрицы
# При ошибке возвращает 0

    mapGetEgmName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEgmName', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_int)
    def mapGetEgmName(_hmtr: ctypes.c_void_p, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetEgmName_t (_hmtr, _name.buffer(), _size)

except Exception as e:
    print(e)
    acceslib = 0
