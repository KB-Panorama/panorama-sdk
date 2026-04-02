#!/usr/bin/env python3

#********************************************************************
#*                                                                  *
#*              Copyright (c) PANORAMA Group 1991-2025              *
#*                      All Rights Reserved                         *
#*                                                                  *
#********************************************************************
#*                                                                  *
#*     ОПИСАНИЕ ИНТЕРФЕЙСА ДОСТУПА К ОБЪЕКТУ "ЭЛЕКТРОННАЯ КАРТА"    *
#*     модуль mapapi.py - аналог mapapi.h из ГИС-ядра Панорама      *
#*                                                                  *
#********************************************************************

import os
import ctypes
import maptype
import mapsyst
import mapcreat
import mapgdi

PACK_WIDTH = 1

#-----------------------------
class TEMPHMAP(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hmap",maptype.HMAP)]
    def __init__(self, value: maptype.HMAP = 0):
        super().__init__()
        self.hmap = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hmap != 0:
            mapCloseData(self.hmap)
        self.hmap = 0
    def HMAP(self):
        return self.hmap
    def __eq__(self, other):
        return self.hmap == other.hmap
    def __ne__(self, other):
        return self.hmap != other.hmap
#-----------------------------


#-----------------------------
class TEMPHOBJ(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hobj",maptype.HOBJ)]
    def __init__(self, value: maptype.HOBJ = 0):
        super().__init__()
        self.hobj = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hobj != 0:
            mapFreeObject(self.hobj)
        self.hobj = 0
    def HOBJ(self):
        return self.hobj
    def __eq__(self, other):
        return self.hobj == other.hobj
    def __ne__(self, other):
        return self.hobj != other.hobj
#-----------------------------


#-----------------------------
class TEMPHUSER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("huser",ctypes.c_void_p)]
    def __init__(self, value: ctypes.c_void_p = 0):
        super().__init__()
        self.huser = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.huser != 0:
            mapDeleteUserSystemParameters(self.huser)
        self.huser = 0
    def HUSER(self):
        return self.huser
    def __eq__(self, other):
        return self.huser == other.huser
    def __ne__(self, other):
        return self.huser != other.huser
#-----------------------------


#-----------------------------
class TEMPCONNECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("connect",ctypes.c_int)]
    def __init__(self, value: ctypes.c_int = 0):
        super().__init__()
        self.connect = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.connect != 0:
            mapCloseConnect(self.connect)
        self.connect = 0
    def CONNECT(self):
        return self.connect
    def __eq__(self, other):
        return self.connect == other.connect
    def __ne__(self, other):
        return self.connect != other.connect
#-----------------------------


try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'


try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)
except Exception as e:
    print(e)
    acceslib = 0 

if acceslib == 0:
    print(gisaccesname)
else:

#   Программное обеспечение, применяющее интерфейс "MAPAPI",
# может выполняться в различных операционных системах
# (Windows, Linux, QNX, OC - PB и т.д.).
#   Все строковые параметры API - функций имеют кодировку
# ANSI для Windows и KOИ - 8 для UNIX-подобных систем.
# Параметры типа HWND и HDC в Windows являются идентификаторами
# окна и графического контекста соответственно.
#   Для систем, применяющих графику X-Window,
# параметры HWND и HDC определены как long int (mapsyst.h),
# но содержат указатели на структуру типа XCONTEXT.
#  typedef struct XCONTEXT
#  {
#   Display     xcDisplay;  #  Связь с Х - сервером
#   Window      xcWindow;   #  Идентификатор окна
#   GC          xcContext;  #  Графический контекст окна
#   DRAWPOINT   xcPoint;    #  Расположение области вывода в окне :
#                           #  верхний, левый  угол в пикселах
# }
#   XCONTEXT;
# Версия библиотеки MapAccess
# #define MAPACCESSVERSION ... см. maptype.h
# Версия интерфейса MAPAPI
# #define MAPAPIVERSION ... см. maptype.h
#enum PPLACE             # ПРИМЕНЯЕМАЯ СИСТЕМА КООРДИНАТ
#    {
#      PP_MAP     = 1,    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ КАРТЫ В ДИСКРЕТАХ
#      PP_PICTURE = 2,    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ ИЗОБРАЖЕНИЯ В ПИКСЕЛАХ
#      PP_PLANE   = 3,    # КООРДИНАТЫ ТОЧЕК В ПЛОСКОЙ ПРЯМОУГОЛЬНОЙ СИСТЕМЕ
#                         # НА МЕСТНОСТИ В МЕТРАХ
#      PP_GEO     = 4,    # КООРДИНАТЫ ТОЧЕК В ГЕОДЕЗИЧЕСКИХ КООРДИНАТАХ
#                         # В РАДИАНАХ
#    };
#enum VTYPE              # ТИП ОТОБРАЖЕНИЯ КАРТЫ
#    {
#      VT_SCREEN        = 1, # ЭКРАННЫЙ (ЧЕРЕЗ DIB)
#      VT_SCREENCONTOUR = 2, # ЭКРАННЫЙ КОНТУРНЫЙ
#      VT_PRINT         = 3, # ПРИНТЕРНЫЙ (ЧЕРЕЗ WIN API)
#      VT_PRINTGLASS    = 4, # ПРИНТЕРНЫЙ БЕЗ ЗАЛИВКИ ПОЛИГОНОВ
#      VT_PRINTCONTOUR  = 5, # ПРИНТЕРНЫЙ КОНТУРНЫЙ, БЕЗ УСЛОВНЫХ ЗНАКОВ
#      VT_PRINTRST      = 6, # ПРИНТЕРНЫЙ РАСТРИЗОВАННЫЙ (ЧЕРЕЗ WIN API)
#    };
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К ЭЛЕКТРОННОЙ КАРТЕ ++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Открыть данные с автоматическим определением их типа
# (векторные,растровые,матричные...)
# name - имя открываемого файла (MAP, SIT, MTW, RSW, MPT) в кодировке UNICODE
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# GENERIC_READ - все данные только на чтение, при этом не открываются
# файлы \Log\name.log и \Log\name.tac - протокол работы и журнал транзакций
# error - после выполнения функции переменная содержит код ошибки
#        (когда HMAP равен 0) или 0; коды ошибок приведены в maperr.rh
# password - пароль доступа к данным из которого формируется 256-битный код
#            для шифрования данных (при утрате пароля данные не восстанавливаются)
# size     - длина пароля в байтах !!!
# Передача пароля необходима, если при создании карты он был указан.
# Если пароль не передан, а он был указан при создании,
# то автоматически вызывается диалог scnGetMapPassword из mapscena.dll (gisdlgs.dll)
# Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
# не вызывается, а при отсутствии пароля происходит отказ открытия данных
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

    mapOpenAnyDataPro_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenAnyDataPro', maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def mapOpenAnyDataPro(_name: mapsyst.WTEXT, _mode = 0, _error = 0, _password = 0, _size = 0) -> maptype.HMAP:
        if _error == 0:
            etemp = ctypes.c_int(0)
            return mapOpenAnyDataPro_t (_name.buffer(), _mode, ctypes.byref(etemp), _password, _size)
        return mapOpenAnyDataPro_t (_name.buffer(), _mode, _error, _password, _size)


# Запросить является ли идентификатор данных корректным
# hMap -  идентификатор открытых данных
# При ошибке возвращает ноль

    mapIsMapHandleCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMapHandleCorrect', maptype.HMAP)
    def mapIsMapHandleCorrect(_hMap: maptype.HMAP) -> int:
        return mapIsMapHandleCorrect_t (_hMap)


# Запрос/установка разрешения выполнять структурный контроль карты
# после сбоев программы
# flag - нулевое значение запрещает выполнение контроля структуры
#        при открытии карты, ненулевое - разрешает
# Возвращает старое значение флага

    mapSetStructureControlFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetStructureControlFlag', ctypes.c_int)
    def mapSetStructureControlFlag(_flag: int) -> int:
        return mapSetStructureControlFlag_t (_flag)


# Установить ограничение на число разрешенных к использованию ядер (процессоров) в системе
# state - флаг ограничения числа ядер (процессоров) в системе
# 0   - не использовать многопоточность
# >1  - максимальное число потоков в выполняемых задачах
# <-1 - доля ядер (процессоров) разрешенных для выполнения потоков
# (например, -2 - использовать не более 1/2 ядер (процессоров) в системе
# Изначально потоки разрешены, но для серверного применения библиотеки,
# работающей в многопоточных приложениях, внутренние потоки понижают
# общую производительность (Например, внутренняя реализация функции
# отображения растра запускает до 8 потоков. Если функция отображения
# вызвана параллельно 10 потоками, одномоментно будет работать 90 потоков).
# Внутреннее число потоков не превышает число ядер процессора, включая
# виртуальные ядра
# Возвращает старое значение состояния разрешения внутренних потоков

    mapUseInsideThread_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUseInsideThread', ctypes.c_int)
    def mapUseInsideThread(_state: int) -> int:
        return mapUseInsideThread_t (_state)


# Запросить число ядер (процессоров) в системе, доступных для приложения
# с учетом установленных ограничений
# Минимальное возвращаемое значение равно 1 (не использовать многопоточность)

    mapGetProcessorNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProcessorNumber')
    def mapGetProcessorNumber() -> int:
        return mapGetProcessorNumber_t ()


# Установить режим добавления данных к карте
# hMap -  идентификатор открытых данных
# mode - режим добавления данных (1 - ускоренный, 0 - стандартный)
# При ускоренном режиме не пересчитываются габариты документа по
# всем открытым данным и не обновляется палитра, что существенно
# ускоряет процесс добавления данных потоком
# По окончанию добавления данных рекомендуется вернуть режим добавления
# к стандартному для обновления габаритов и палитры
# Габариты обновляются автоматически и при масштабировании документа,
# а палитра нужна при формировании изображений с ограниченным диапазоном
# цветов
# После вызова mapOpenProject или mapAppendProject автоматически устанавливает
# стандартный режим обновления данных
# Возвращает текущее значение режима

    mapSetAppendDataMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAppendDataMode', maptype.HMAP, ctypes.c_int)
    def mapSetAppendDataMode(_hMap: maptype.HMAP, _mode: int) -> int:
        return mapSetAppendDataMode_t (_hMap, _mode)


# Установить/Запросить для карты режим потоковой загрузки данных
# Применяется для ускорения загрузки данных из обменных форматов при создании карты
# В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
# hMap  -  идентификатор открытых данных
# hSite -  идентификатор открытой пользовательской карты
# state -  режим потоковой загрузки данных (1 - включен, 0 - выключен)
# В режиме потоковой загрузки данных отключается журналирование операций
# При ошибке возвращает ноль

    mapSetLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetLoadState', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetLoadState(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _state: int) -> int:
        return mapSetLoadState_t (_hMap, _hSite, _state)

    mapGetLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLoadState', maptype.HMAP, maptype.HSITE)
    def mapGetLoadState(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetLoadState_t (_hMap, _hSite)


# Проверить, есть ли в составе открытых данных карты в состоянии потоковой загрузки данных
# В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
# hMap  -  идентификатор открытых данных
# Возвращает ненулевое значение, если хотя бы одна из карт находится в режиме потоковой загрузки
# При ошибке возвращает ноль

    mapCheckLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckLoadState', maptype.HMAP)
    def mapCheckLoadState(_hMap: maptype.HMAP) -> int:
        return mapCheckLoadState_t (_hMap)


# Запросить процент загрузки данных
# Для локальных данных показывает процесс загрузки в оперативную память,
# для данных с ГИС Сервера - процесс загрузки в кэш,
# для баз данных - процесс формирования кэша
# hMap  -  идентификатор открытых данных
# hSite -  идентификатор открытой пользовательской карты
# Возвращает процент загрузки данных

    mapGetSitePercentLoad_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePercentLoad', maptype.HMAP, maptype.HSITE)
    def mapGetSitePercentLoad(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSitePercentLoad_t (_hMap, _hSite)


# Добавить данные к открытой карте (карту, растр, матрицу)
# hMap -  идентификатор открытых данных
# name - имя открываемого файла (MAP, SITX, SIT, MTW, MTQ, RSW, MPT) в кодировке UNICODE
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# transform - признак трансформирования пользовательской карты
#             к ранее открытым данным (если проекции разные):
#             0 - не трансформировать данные (преобразовывать "на лету"),
#             1 - трансформировать данные при открытии и сохранить карту
#                 в новой проекции,
#            -1 - задать вопрос пользователю.
# В серверной версии (-1) обрабатывается, как 0.
# password - пароль доступа к данным из которого формируется 256-битный код
#            для шифрования данных (при утрате данные не восстанавливаются)
# size     - длина пароля в байтах !!!
# Передача пароля необходима, если при создании карты он был указан.
# Если пароль не передан, а он был указан при создании,
# то автоматически вызывается диалог scnGetMapPassword из mapscena.dll (gis64dlgs.dll)
# Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
# не вызывается, а при отсутствии пароля происходит отказ открытия данных
# Возвращает идентификатор типа данных (FILE_MAP - для векторной
# карты, FILE_RSW - для растра, FILE_MTW - для матрицы, FILE_MTL - для
# матрицы слоев, FILE_MTQ - для матрицы качеств), данные добавляются в
# список последними, если данные уже были открыты, число открытых данных
# (карт, растров, матриц) не меняется
# При ошибке возвращает ноль

    mapAppendAnyDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendAnyDataPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapAppendAnyDataPro(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _mode = 0, _transform = -1, _password = 0, _size = 0) -> int:
        return mapAppendAnyDataPro_t (_hMap, _name.buffer(), _mode, _transform, _password, _size)

# Запросить соответствие систем координат добавляемой в документ карты и документа
# Если система координат карты не соответствует открытому району, функция возвращает 1
# hMap     - декриптор документа (открытого района)
# fileName - имя файла добавляемых данных (карты, растра, матрицы).
# При ошибке возвращает ноль.

    mapIsNeedTranslate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsNeedTranslate', maptype.HMAP, maptype.PWCHAR)
    def mapIsNeedTranslate(_hMap: maptype.HMAP, _fileName: mapsyst.WTEXT) -> int:
        return mapIsNeedTranslate_t (_hMap, _fileName.buffer())


# Запросить размер данных по имени файла
# При ошибке возвращает ноль

    mapGetDataSizeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDataSizeUn', maptype.PWCHAR)
    def mapGetDataSizeUn(_name: mapsyst.WTEXT) -> float:
        return mapGetDataSizeUn_t (_name.buffer())


# Установить/Запросить в кодировке UNICODE имя главной карты в документе
# или имя проекта, если открыт проект
# hMap -  идентификатор открытых данных
# name - адрес буфера для записи результата
# size - длина строки в байтах
# При ошибке возвращает ноль

    mapSetMainNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMainNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapSetMainNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapSetMainNameUn_t (_hMap, _name.buffer())

    mapGetMainNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMainNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMainNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMainNameUn_t (_hMap, _name.buffer(), _size)


# Запросить имя (полный путь к файлу) главной карты в документе
# или в проекте (MPT)
# hMap     -  идентификатор открытых данных
# name     - буфер для возвращаемой строки
# namesize - размер буфера в БАЙТАХ
# При ошибке возвращает 0

    mapGetMainMapNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMainMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMainMapNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetMainMapNameUn_t (_hMap, _name.buffer(), _namesize)


# Проверка корректности паспортных данных и, если надо, то заполнение
# координат по признаку приоритета 0 - расчет прямоугольных координат
#                                  1 - геодезических
# Структуры MAPREGISTEREX, LISTREGISTER описаны в mapcreat.h
# При ошибке возвращает ноль

    mapCheckAndUpdate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckAndUpdate', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_int)
    def mapCheckAndUpdate(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _priority: int) -> int:
        return mapCheckAndUpdate_t (_mapreg, _listreg, _priority)


# Заполнение справочных данных в зависимости от типа карты
# Структуры MAPREGISTEREX, LISTREGISTER описаны в mapcreat.h
# При ошибке возвращает ноль

    mapRegisterFromMapType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterFromMapType', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapRegisterFromMapType(_maptype: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapRegisterFromMapType_t (_maptype, _mapreg)


# Запросить допустимые параметры для проекции
# code - номер проекции из MAPPROJECTION (mapcreat.h)
# Возвращает комбинацию флагов PROJECTIONPARAMETERS (mapcreat.h)
# Например: значение 49 = EPP_AXISMERIDIAN|EPP_FALSEEASTING|EPP_FALSENORTHING
# При ошибке возвращает ноль

    mapGetProjectionParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProjectionParameters', ctypes.c_int)
    def mapGetProjectionParameters(_code: int) -> int:
        return mapGetProjectionParameters_t (_code)


# Создать новую векторную карту
# mapname - полное имя файла карты (MAP, SIT, SITX)
# rscname - полное имя файла ресурсов (RSC)
# Возвращает идентификатор открытой векторной карты
# Структуры MAPREGISTEREX и LISTREGISTER описаны в mapcreat.h
# sheetnames - название (UTF-16) листа карты, номенклатуры и файлов даных (для многолистовой карты),
# для пользовательской карты (не ограниченной рамкой) название листа и номенклатуры совпадает,
# а название файлов данных совпадает с названием паспорта карты
# mainname - главное название (UTF-16) многолистовой карты (MAP),
# для пользовательской карты совпадает с названием листа карты
# (Запросить главное название карты можно функцией mapGetSiteNameUn)
# password  - пароль доступа к данным из которого формируется 256-битный код
# для шифрования данных (при утрате пароля данные не восстанавливаются)
# (поддерживается для карт с расширением SITX - хранилище в одном файле) или 0
# size      - длина пароля в байтах (!) или 0
# hmap, hsite - идентификатор карты, из которой может быть скопирован пароль доступа к данным
# error     - поле для получения кода ошибки или 0; коды ошибок приведены в maperr.rh
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# Возвращает идентификатор открытой векторной карты
# При ошибке возвращает ноль

    mapCreateMapExp_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMapExp', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.HMAP, maptype.HSITE)
    def mapCreateMapExp(_mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int), _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HMAP:
        return mapCreateMapExp_t (_mapname.buffer(), _rscname.buffer(), _mapreg, _listreg, _sheetnames, _mainname.buffer(), _password.buffer(), _size, _error, _hmap, _hsite)


# Создать план (карта в местной системе координат)
# mapname - полное имя файла карты
# rscname - полное имя файла ресурсов
# Струтктуры MAPREGISTEREX, LISTREGISTER описаны в mapcreate.h
# Возвращает идентификатор открытой векторной карты
# Структура CREATEPLAN описана в maptype.h
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

#   mapCreatePlaneUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreatePlaneUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(CREATEPLANE))
#   def mapCreatePlaneUn(_mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _createplane: ctypes.POINTER(CREATEPLANE)) -> maptype.HMAP:
#       return mapCreatePlaneUn_t (_mapname, _rscname, _createplane)


# Создать временную пользовательскую карту
# Файлы карты размещаются в рабочей директории системы
# и имеют уникальные имена, генерируемые автоматически
# При закрытии карты все файлы данных удаляются
# Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
# и освобождаются при закрытии карты
# rscname - полное имя файла ресурсов RSC
# mapreg  - параметры проекции создаваемой временной карты или 0
# Если mapreg не задан, то создается Цилиндрическая прямая равноугольная Меркатора на шаре EPSG:3857
# datum   - параметры датума или 0
# ellipsoid - параметры эллипсоида или 0
# inmemory - признак создания карты в оперативной памяти или 0
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

    mapCreateTempSitePro_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateTempSitePro', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int)
    def mapCreateTempSitePro(_rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _inmemory: int) -> maptype.HMAP:
        return mapCreateTempSitePro_t (_rscname.buffer(), _mapreg, _datum, _ellipsoid, _inmemory)


# Создать временную пользовательскую карту с системой координат и классификатором, как у эталонной карты
# hmap     - идентификатор открытых данных
# hSite    - идентификатор пользовательской карты
# inmemory - признак создания карты в оперативной памяти или 0
# При ошибке возвращает ноль

    mapCreateTempSiteForMap_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateTempSiteForMap', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapCreateTempSiteForMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _inmemory: int) -> maptype.HMAP:
        return mapCreateTempSiteForMap_t (_hmap, _hsite, _inmemory)


# Создать временную пользовательскую карту по открытой карте
# hmap     - идентификатор открытых данных
# rscname  - полное имя файла ресурсов, если равно None - выбирается
#            из открытой карты
# inmemory - признак создания карты в оперативной памяти или 0
# Файлы карты размещаются в рабочей директории системы
# и имеют уникальные имена, генерируемые автоматически
# При закрытии пользовательской карты все файлы данных автоматически удаляются
# Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
# и освобождаются при закрытии карты
# Возвращает идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapCreateAndAppendTempSitePro_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapCreateAndAppendTempSitePro', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapCreateAndAppendTempSitePro(_hMap: maptype.HMAP, _rscname: mapsyst.WTEXT, _inmemory: int) -> maptype.HSITE:
        if (isinstance(_rscname, str)):
            return mapCreateAndAppendTempSitePro_t (_hMap, _rscname.buffer(), _inmemory)
        return mapCreateAndAppendTempSitePro_t (_hMap, _rscname, _inmemory)


# Переоткрыть главную карту
# Для специальных случаев. HMAP остается прежний, а карта открывается новая
# name     - имя открываемой карты
# password - пароль доступа к данным из которого формируется 256-битный код
#            для шифрования данных (при утрате данные не восстанавливаются)
# size     - длина пароля в байтах !!!
# isfast   - признак открытия карты для однократной операции (отобразили и закрыли и т.п.)
# При ошибке возвращает ноль (в этом случае может остаться
# открытой прежняя карта или никакой)

    mapOpenMapProEx_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMapProEx', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapOpenMapProEx(_name: mapsyst.WTEXT, _mode: int, _password: mapsyst.WTEXT, _size: int, _isfast: int) -> maptype.HMAP:
        return mapOpenMapProEx_t (_name.buffer(), _mode, _password.buffer(), _size, _isfast)


# Закрыть все данные электронной карты
# hmap -  идентификатор открытых данных
# Идентификатор HMAP становится недействительным !

    mapCloseData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseData', maptype.HMAP)
    def mapCloseData(_hMap: maptype.HMAP) -> ctypes.c_void_p:
        return mapCloseData_t (_hMap)


# Копирование (перемещение) векторной карты
# oldname - старое имя района
# newname - новое имя района
# ismove  - признак необходимости удаления старой копии карты (перемещения)
# error   - код ошибки при выполнении команды (см. maperr.rh)
# При ошибке возвращает ноль

    mapCopyMapPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyMapPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapCopyMapPro(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _ismove: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCopyMapPro_t (_oldname.buffer(), _newname.buffer(), _ismove, _error)


# Закрыть и Удалить векторную карту (все файлы данных)
# hmap - идентификатор открытых данных
# После удаления идентификатор hMap не должен использоваться,
# как после mapCloseData()
# При ошибке возвращает ноль

    mapDeleteMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMap', maptype.HMAP)
    def mapDeleteMap(_hMap: maptype.HMAP) -> int:
        return mapDeleteMap_t (_hMap)


# Удаление района работ
# name      - имя удаляемой карты
# rscdelete - признак удаления файла классификатора вместе с картой
# Классификатор необходимо удалить отдельно
# При ошибке возвращает ноль

    mapDeleteMapByNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMapByNameEx', maptype.PWCHAR, ctypes.c_int)
    def mapDeleteMapByNameEx(_name: mapsyst.WTEXT, _rscdelete: int) -> int:
        return mapDeleteMapByNameEx_t (_name.buffer(), _rscdelete)


# Открыть проект данных (карта, обстановки, растры, матрицы...)
# name - имя файла проекта (MPT : структура, как в INI)
# При ошибке возвращает ноль

    mapOpenProjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenProjectUn', maptype.PWCHAR)
    def mapOpenProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        return mapOpenProjectUn_t (_name.buffer())


# Добавить проект данных (карта, обстановки, растры, матрицы...)
# name - имя файла проекта (MPT : структура, как в INI)
# При ошибке возвращает ноль

    mapAppendProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapAppendProjectUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapAppendProjectUn_t (_hMap, _name.buffer())


# Открыть упакованный проект данных (карта, обстановки, растры, матрицы...)
# name - имя файла проекта MPTZ
# При ошибке возвращает ноль

    mapOpenZipProjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenZipProjectUn', maptype.PWCHAR)
    def mapOpenZipProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        return mapOpenZipProjectUn_t (_name.buffer())


# Запросить имя открытого проекта
# hmap     - идентификатор открытых данных
# name     - буфер для размещения возвращаемой строки
# namesize - размер буфера в БАЙТАХ
# При ошибке возвращает ноль

    mapGetProjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProjectNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetProjectNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetProjectNameUn_t (_hMap, _name.buffer(), _namesize)


# Сохранить список открытых наборов данных и их свойства в проекте данных MPT
# hmap - идентификатор открытых данных
# name - имя файла проекта MPT (структура, как INI-файла)
# При ошибке возвращает ноль

    mapSaveProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapSaveProjectUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapSaveProjectUn_t (_hMap, _name.buffer())


# Сохранить список открытых наборов данных, их свойства и упакованные наборы данных
# в проекте данных MPTZ
# В проект сохраняются упакованные векторные карты (SITZ\MAPZ), сжатые растры RSW и
# сжатые матрицы MTW, MTQ
# hmap - идентификатор открытых данных
# name - имя файла проекта MPTZ
# savefromserver - признак копирования в MPTZ наборов данных с ГИС Сервера,
#        если есть права на их копирование
# При ошибке возвращает ноль

    mapSaveZipProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveZipProjectUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapSaveZipProjectUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _savefromserver: int) -> int:
        return mapSaveZipProjectUn_t (_hMap, _name.buffer(), _savefromserver)


# Запросить - является ли документ проектом (MPT/MPTZ)
# hmap -  идентификатор открытых данных
# Если это проект - возвращает ненулевое значение,
# если это упакованный проект (MPTZ) - возвращает значение FILE_MPTZ

    mapIsDocProject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsDocProject', maptype.HMAP)
    def mapIsDocProject(_hMap: maptype.HMAP) -> int:
        return mapIsDocProject_t (_hMap)


# Сохранить текущие параметры окна карты в INI-файл карты,
# имя файла можно запросить через mapGetMapIniName()
# Вызывается перед закрытием окна карты
# Сохраняет описание открытых данных, масштаб, палитру, признаки видимости,
# редактируемости, состав отображаемых объектов...
# hmap  -  идентификатор открытых данных
# point -  координаты центра окна в метрах (может быть 0)
# При ошибке возвращает ноль

    mapSaveMapState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSaveMapState(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSaveMapState_t (_hMap, _point)


# Восстановить параметры окна карты из INI-файла карты,
# имя файла можно запросить через mapGetMapIniName()
# Вызывается после открытия карты
# Восстанавливает описание списка данных, масштаб, палитру, признаки видимости,
# редактируемости, состав отображаемых объектов...
# hmap  -  идентификатор открытых данных
# point -  координаты центра окна в метрах (может быть 0)
# При ошибке возвращает ноль

    mapRestoreMapState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRestoreMapState(_hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapRestoreMapState_t (_hMap, _point)


# Запросить - есть ли какие-либо открытые данные
# Данные - векторные, растровые, матричные...
# hmap -  идентификатор открытых данных
# Если открытых данных нет или ошибка - возвращает ноль

    mapIsActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsActive', maptype.HMAP)
    def mapIsActive(_hMap: maptype.HMAP) -> int:
        return mapIsActive_t (_hMap)


# Запросить - есть ли какие-либо открытые векторные карты
# Если открытых векторных карт нет или ошибка - возвращает ноль

    mapIsVectorMapActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsVectorMapActive', maptype.HMAP)
    def mapIsVectorMapActive(_hMap: maptype.HMAP) -> int:
        return mapIsVectorMapActive_t (_hMap)


# Запросить - есть ли какие-либо открытые векторные карты,
# доступные для редактирования
# Если доступных для редактирования векторных карт нет
# или ошибка - возвращает ноль

    mapIsVectorMapEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsVectorMapEdit', maptype.HMAP)
    def mapIsVectorMapEdit(_hMap: maptype.HMAP) -> int:
        return mapIsVectorMapEdit_t (_hMap)


# Запросить - есть ли в документе какие-либо открытые данные помимо указанного типа.
# Возвращает количество открытых данных в документе помимо указанного типа.
# dataType - идентификатор типа данных (FILE_MAP - для векторной
# карты, FILE_SITE - для пользовательской карты, FILE_RSW - для растра,
# FILE_MTW - для матрицы, FILE_MTL - для матрицы слоев, FILE_MTQ -
# для матрицы качеств, FILE_MTD - для модели "Облако точек",
# FILE_TIN - для TIN-модели ", FILE_WMS - для геопортала).
# Если dataType == 0, выполняется подсчет всех данных документа

    mapGetActiveDataCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActiveDataCount', maptype.HMAP, ctypes.c_int)
    def mapGetActiveDataCount(_hMap: maptype.HMAP, _dataType: int) -> int:
        return mapGetActiveDataCount_t (_hMap, _dataType)


# Выполнить согласование данных электронной карты
# в памяти и на диске (при многопользовательском доступе
# к данным)
# hmap -  идентификатор открытых данных
# Если состояние данных в памяти изменилось (по данным
# с диска) - возвращает ненулевое значение (1), иначе 0
# Если карта должна быть закрыта - возвращает 2
# (доступ на ГИС Сервер прекращен!)
# Если состояние изменилось - необходимо перерисовать
# изображение карты
# Опрос состояния целесообразно выполнять периодически
# в процессе работы приложения

    mapAdjustData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAdjustData', maptype.HMAP)
    def mapAdjustData(_hMap: maptype.HMAP) -> int:
        return mapAdjustData_t (_hMap)


# Установить доступность для выполнения команды Adjust
# mode - признак доступности обработки команды Adjust,
#        если равен 0 - команда не обрабатывается.
# При выполнении длительных процедур (отмена длинных
# транзакций, трансформирование данных и т.п.) целесообразно
# отключать команду Adjust, если она может быть вызвана из
# других потоков приложения. Команда Adjust может вызывать
# переоткрытие карт и перераспределение памяти.
# Возвращает прежнее значение

    mapSetAdjustMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAdjustMode', maptype.HMAP, ctypes.c_int)
    def mapSetAdjustMode(_hMap: maptype.HMAP, _mode: int) -> int:
        return mapSetAdjustMode_t (_hMap, _mode)


# Создать(добавить) новый лист в районе
# hmap -  идентификатор открытых данных
# Структура LISTREGISTER описана в mapcreat.h
# При ошибке возвращает ноль, иначе - номер созданного листа

    mapCreateListPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateListPro', maptype.HMAP, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapCreateListPro(_hMap: maptype.HMAP, _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        return mapCreateListPro_t (_hMap, _sheet, _sheetnames)


# Удалить указанный лист карты
# list - номер листа (с 1)
# При ошибке возвращает ноль

    mapDeleteList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteList', maptype.HMAP, ctypes.c_int)
    def mapDeleteList(_hmap: maptype.HMAP, _list: int) -> int:
        return mapDeleteList_t (_hmap, _list)


# Добавить листы из другого района работ в данный
# hmap -  идентификатор открытых данных
# mapname - добавляемый район,
# handle - идентификатор окна,которое будет извещаться
# о ходе процесса (0x585 - 0x588)
# При ошибке возвращает ноль

    mapAppendMapToMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendMapToMapUn', maptype.HMAP, maptype.PWCHAR, maptype.HWND)
    def mapAppendMapToMapUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        return mapAppendMapToMapUn_t (_hMap, _name.buffer(), _handle)


# Cоздать пустой объект векторной карты
# (создание подобъекта - см. редактирование метрики)
# hmap        - идентификатор открытых данных
# sheetnumber - номер листа в котором будет расположен
# kind        - тип создаваемой метрики, описан в maptype.h
# text        - признак метрики с текстом (объекты типа "подпись")
#               (устанавливается автоматически при вызове mapPutText(...))
# После вызова функций типа What...() и Seek...() все параметры
# полученного объекта могут измениться (text,kind,list и т.п.).
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции FreeObject()
# При ошибке возвращает ноль

    mapCreateObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateObject', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapCreateObject(_hMap: maptype.HMAP, _sheetnumber: int = 1, _kind: int = maptype.IDDOUBLE2, _text: int = 0) -> maptype.HOBJ:
        return mapCreateObject_t (_hMap, _sheetnumber, _kind, _text)


# Очистить содержимое объекта
# (для повторного заполнения, как пустого объекта)
# hmap - идентификатор открытых данных
# sheetnumber - номер листа в котором будет расположен
# kind - тип создаваемой метрики, описан в maptype.h
# При ошибке возвращает ноль

    mapClearObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapClearObject(_info: maptype.HOBJ, _sheetnumber: int = 1, _kind: int = maptype.IDDOUBLE2) -> int:
        return mapClearObject_t (_info, _sheetnumber, _kind)


# Запросить, корректное ли содержание объекта
# При ошибке возвращает ноль

    mapIsObjectCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectCorrect', maptype.HOBJ)
    def mapIsObjectCorrect(_info: maptype.HOBJ) -> int:
        return mapIsObjectCorrect_t (_info)


# Запросить, установлен ли признак удаленного объекта
# При ошибке возвращает ноль

    mapIsObjectDeleted_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectDeleted', maptype.HOBJ)
    def mapIsObjectDeleted(_info: maptype.HOBJ) -> int:
        return mapIsObjectDeleted_t (_info)


# Cоздать копию объекта векторной карты
# hmap - идентификатор открытых данных
# info - идентификатор объекта карты в памяти
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции mapFreeObject()
# При ошибке возвращает ноль

    mapCreateCopyObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateCopyObject', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObject(_hMap: maptype.HMAP, _info: maptype.HOBJ) -> maptype.HOBJ:
        return mapCreateCopyObject_t (_hMap, _info)


# Считать копию объекта векторной (src) карты в другой объект (dest)
# При ошибке возвращает ноль

    mapReadCopyObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadCopyObject', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObject(_dest: maptype.HOBJ, _src: maptype.HOBJ) -> int:
        return mapReadCopyObject_t (_dest, _src)


# Считать копию подобъекта векторной (src) карты в другой объект (dest)
# Копирует все данные объекта  src  в объект  dest,
# с сохранением только одного главного контура, полученного из subject
# При ошибке возвращает ноль

    mapReadCopySubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadCopySubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_int)
    def mapReadCopySubject(_dest: maptype.HOBJ, _src: maptype.HOBJ, _subject: int) -> int:
        return mapReadCopySubject_t (_dest, _src, _subject)


# Считать копию главного подобъекта мультиполигона вместе с его подобъектами в другой объект
# number - порядковый номер внешнего контура, начиная с 1
# При ошибке возвращает ноль

    mapReadCopyMultiSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadCopyMultiSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_int)
    def mapReadCopyMultiSubject(_dest: maptype.HOBJ, _src: maptype.HOBJ, _number: int) -> int:
        return mapReadCopyMultiSubject_t (_dest, _src, _number)


# Считать копию метрики объекта векторной (src) карты в другой объект (dest)
# При ошибке возвращает ноль

    mapReadCopyObjectData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadCopyObjectData', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObjectData(_dest: maptype.HOBJ, _src: maptype.HOBJ) -> int:
        return mapReadCopyObjectData_t (_dest, _src)


# Копировать метрику подобъекта
#   dest      - объект-приемник, в который добавляется подобъект
#   destSub   - номер подобъекта приемника (от 0)
#               -1 или несуществующий номер подобъекта - добавляется новый подобъект
#   source    - объект-источник (source и dest должны принадлежать одной карте)
#   sourceSub - номер подобъекта источника (от 0)
#               -1 - копировать все подобъекты (destSub игнорируется)
# Функция выполняет:
#   - добавление подобъекта;
#   - замену подобъекта;
#   - замену всех подобъектов.
# Пример (назначение последнего подобъекта главным):
#   int sub = mapPolyCount(obj)-1;           # Номер последнего контура
#   mapCopySubjectOneMap(obj, -1, obj, 0);   # Копировать главный контур в дополнительный
#   mapCopySubjectOneMap(obj, 0, obj, sub);  # Копировать контур в главный
#   mapDeleteSubject(obj, subject);          # Удалить старую копию контура
# При ошибке возвращает 0

    mapCopySubjectOneMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopySubjectOneMap', maptype.HOBJ, ctypes.c_int, maptype.HOBJ, ctypes.c_int)
    def mapCopySubjectOneMap(_dest: maptype.HOBJ, _destsub: int, _source: maptype.HOBJ, _sourcesub: int) -> int:
        return mapCopySubjectOneMap_t (_dest, _destsub, _source, _sourcesub)


# Cоздать копию объекта векторной карты, как нового объекта (!)
# hmap - идентификатор открытых данных
# info - идентификатор объекта карты в памяти
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции FreeObject()
# При ошибке возвращает ноль

    mapCreateCopyObjectAsNew_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateCopyObjectAsNew', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObjectAsNew(_hMap: maptype.HMAP, _info: maptype.HOBJ) -> maptype.HOBJ:
        return mapCreateCopyObjectAsNew_t (_hMap, _info)


# Считать копию объекта векторной карты, как нового объекта (с обновлением номера)
# src  - исходный объект,
# dest - копия объекта (при сохранении - будет создан новый)
# Предполагается, что до сохранения в копии что-то поменяют.
# Для сохранения объекта на карте необходимо выполнить функцию
# mapCommitObject(...)
# При ошибке возвращает ноль

    mapCopyObjectAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyObjectAsNew', maptype.HOBJ, maptype.HOBJ)
    def mapCopyObjectAsNew(_dest: maptype.HOBJ, _src: maptype.HOBJ) -> int:
        return mapCopyObjectAsNew_t (_dest, _src)


# Удалить описание объекта векторной карты из памяти
# info - идентификатор объекта карты в памяти
# Для сохранения объекта на карте необходимо
# до вызова mapFreeObject(...) выполнить функцию
# mapCommitObject(...)
# При ошибке возвращает ноль

    mapFreeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObject', maptype.HOBJ)
    def mapFreeObject(_info: maptype.HOBJ) -> ctypes.c_void_p:
        return mapFreeObject_t (_info)


# Запросить код ошибки последней операции доступа к данным
# Коды ошибок - см. maperr.rh

    mapGetAccessError_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAccessError')
    def mapGetAccessError() -> int:
        return mapGetAccessError_t ()


# Считать объект, который отображался последним перед возникновением
# сбоя отображения карт
# Применяется при попадании в секцию catch(..) при вызове отображения
# карты для вывода диагностической информации
# hmap - идентификатор открытых данных;
# info - идентификатор существующего объекта,
# в котором будет размещен результат поиска.
# Если такой объект не установлен - возвращает ноль

    mapReadLastViewObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadLastViewObject', maptype.HMAP, maptype.HOBJ)
    def mapReadLastViewObject(_hMap: maptype.HMAP, _info: maptype.HOBJ) -> int:
        return mapReadLastViewObject_t (_hMap, _info)


# Запросить, растягивается ли объект по метрике
# Данный признак может быть установлен у подписей
# и векторных объектов
# При ошибке возвращает ноль

    mapIsObjectStretch_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectStretch', maptype.HOBJ)
    def mapIsObjectStretch(_info: maptype.HOBJ) -> int:
        return mapIsObjectStretch_t (_info)


# Установить/Запросить признак записи в создаваемые и обновляемые объекты
# служебных семантик 32850-32855 (дата, время, автор операции)
# Признак устанавливается для всех открытых карт документа (HMAP)
# Запись семантик выполняется внешними задачами (Редактор карты, Выбор объекта и другими)
# hmap - идентификатор открытых данных
# flag - признак записи служебных семантик (если значение не равно 0 - записывать)
# При ошибке возвращает ноль

    mapSetObjectsDataAndUserFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectsDataAndUserFlag', maptype.HMAP, ctypes.c_int)
    def mapSetObjectsDataAndUserFlag(_hMap: maptype.HMAP, _flag: int) -> int:
        return mapSetObjectsDataAndUserFlag_t (_hMap, _flag)

    mapGetObjectsDataAndUserFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectsDataAndUserFlag', maptype.HMAP)
    def mapGetObjectsDataAndUserFlag(_hMap: maptype.HMAP) -> int:
        return mapGetObjectsDataAndUserFlag_t (_hMap)


# Запросить описание цвета палитры по индексу (index)
# hmap - идентификатор открытых данных
# Номер первого индекса равен нулю

    mapGetMapColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetMapColor', maptype.HMAP, ctypes.c_int)
    def mapGetMapColor(_hmap: maptype.HMAP, _index: int) -> maptype.COLORREF:
        return mapGetMapColor_t (_hmap, _index)


# Запросить число цветов логической палитры
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetColorCount', maptype.HMAP)
    def mapGetColorCount(_hmap: maptype.HMAP) -> int:
        return mapGetColorCount_t (_hmap)


# Запросить/Установить цветовую модель палитры для печати карты
# hmap - идентификатор открытых данных
# Возвращает: 0 - RGB, 1 - CMYK
# При ошибке возвращает ноль

    mapGetColorModel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetColorModel', maptype.HMAP)
    def mapGetColorModel(_hmap: maptype.HMAP) -> int:
        return mapGetColorModel_t (_hmap)

    mapSetColorModel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetColorModel', maptype.HMAP, ctypes.c_int)
    def mapSetColorModel(_hmap: maptype.HMAP, _model: int) -> int:
        return mapSetColorModel_t (_hmap, _model)


# Установить/Запросить цвет фона отображаемой карты
# hmap - идентификатор открытых данных
# color - цвет фона
# При изменении цвета фона необходимо перерисовать весь экран
# При ошибке возвращает 0x0FFFFFF (белый)

    mapSetBackColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapSetBackColor', maptype.HMAP, maptype.COLORREF)
    def mapSetBackColor(_hmap: maptype.HMAP, _color: maptype.COLORREF) -> maptype.COLORREF:
        return mapSetBackColor_t (_hmap, _color)

    mapGetBackColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetBackColor', maptype.HMAP)
    def mapGetBackColor(_hmap: maptype.HMAP) -> maptype.COLORREF:
        return mapGetBackColor_t (_hmap)


# Установить/Запросить цвет фона отображаемой карты
# при выводе в принтерном режиме на экран
# При изменении цвета фона необходимо перерисовать весь экран
# При ошибке возвращает 0x0FFFFFF (белый)

    mapSetBackPrintColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapSetBackPrintColor', maptype.HMAP, maptype.COLORREF)
    def mapSetBackPrintColor(_hmap: maptype.HMAP, _color: maptype.COLORREF) -> maptype.COLORREF:
        return mapSetBackPrintColor_t (_hmap, _color)

    mapGetBackPrintColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetBackPrintColor', maptype.HMAP)
    def mapGetBackPrintColor(_hmap: maptype.HMAP) -> maptype.COLORREF:
        return mapGetBackPrintColor_t (_hmap)


# Запросить/Установить способ отображения карты
# hmap - идентификатор открытых данных
# При установке нового способа отображения возвращается
# предыдущее значение
# (см. maptype.h : VT_SCREEN(1), VT_PRINT(3), VT_PRINTRST(6),...)
# При ошибке возвращает ноль

    mapGetViewType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetViewType', maptype.HMAP)
    def mapGetViewType(_hmap: maptype.HMAP) -> int:
        return mapGetViewType_t (_hmap)

    mapSetViewType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetViewType', maptype.HMAP, ctypes.c_int)
    def mapSetViewType(_hmap: maptype.HMAP, _type: int) -> int:
        return mapSetViewType_t (_hmap, _type)

    mapSetViewTypePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetViewTypePro', maptype.HMAP, ctypes.c_int, maptype.HPAINT)
    def mapSetViewTypePro(_hmap: maptype.HMAP, _type: int, _hPaint: maptype.HPAINT) -> int:
        return mapSetViewTypePro_t (_hmap, _type, _hPaint)


# Запросить яркость карты (от -16 до +16)
# hmap - идентификатор открытых данных

    mapGetBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetBright', maptype.HMAP)
    def mapGetBright(_hmap: maptype.HMAP) -> int:
        return mapGetBright_t (_hmap)


# Установить яркость карты (от -16 до +16)
# hmap - идентификатор открытых данных

    mapSetBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetBright', maptype.HMAP, ctypes.c_int)
    def mapSetBright(_hmap: maptype.HMAP, _bright: int) -> int:
        return mapSetBright_t (_hmap, _bright)


# Запросить контрастность (от -16 до +16)
# hmap - идентификатор открытых данных

    mapGetContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetContrast', maptype.HMAP)
    def mapGetContrast(_hmap: maptype.HMAP) -> int:
        return mapGetContrast_t (_hmap)


# Установить контрастность (от -16 до +16)
# hmap - идентификатор открытых данных

    mapSetContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetContrast', maptype.HMAP, ctypes.c_int)
    def mapSetContrast(_hmap: maptype.HMAP, _contrast: int) -> int:
        return mapSetContrast_t (_hmap, _contrast)


# Запросить интенсивность заливки площадей полигонов для
# принтерного отображения (от 0 до 100)
# hmap - идентификатор открытых данных

    mapGetIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetIntensity', maptype.HMAP)
    def mapGetIntensity(_hmap: maptype.HMAP) -> int:
        return mapGetIntensity_t (_hmap)


# Установить интенсивность заливки площадей полигонов для
# принтерного отображения (от 0 до 100)
# hMap  - идентификатор открытой карты
# Если mapGetTransparentSquare возвращает 0, то значения интенсивности
# соответствуют расслаблению цветов (кроме черного):
#   0 - заливок нет, 50 - полурасслабленные цвета, 100 - нормальные цвета
# Если mapGetTransparentSquare возвращает 1, то значения интенсивности
# соответствуют степени непрозрачности цветов:
#   0 - заливок нет, 50 - полупрозрачные заливки, 100 - нормальные цвета
# hmap - идентификатор открытых данных

    mapSetIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetIntensity', maptype.HMAP, ctypes.c_int)
    def mapSetIntensity(_hmap: maptype.HMAP, _intensity: int) -> int:
        return mapSetIntensity_t (_hmap, _intensity)


# Запросить флаг прозрачности заливки площадей полигонов
# hMap  - идентификатор открытой карты
# Возвращает значение флага

    mapGetTransparentSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTransparentSquare', maptype.HMAP)
    def mapGetTransparentSquare(_hMap: maptype.HMAP) -> int:
        return mapGetTransparentSquare_t (_hMap)


# Установить флаг прозрачности заливки площадей полигонов.
# Степень прозрачности устанавливается функцией mapSetIntensity
# hmap  - идентификатор открытой карты
# flag  - признак прозрачности:
#         0 - прозрачность отключена (заливки сплошным цветом),
#             использовать при обычном отображении или печати карты;
#             в принтерных режимах (VT_PRINT, VT_PRINTRST)
#         1 - прозрачность включена (заливки в виде цветного стекла),
#             использовать при отображении или печати карты поверх растров
#             в принтерном растровом режиме (VT_PRINTRST)

    mapSetTransparentSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTransparentSquare', maptype.HMAP, ctypes.c_int)
    def mapSetTransparentSquare(_hmap: maptype.HMAP, _flag: int) -> int:
        return mapSetTransparentSquare_t (_hmap, _flag)


# Выдать вид отображения карты
# hmap  - идентификатор открытой карты
# 1 - с узлами, 0 - без узлов

    mapGetNodeView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetNodeView', maptype.HMAP)
    def mapGetNodeView(_hmap: maptype.HMAP) -> int:
        return mapGetNodeView_t (_hmap)


# Установить отображение узлов на карте
# hmap - идентификатор открытой карты
# mode - признак отображения узлов контуров объектов маленькими квадратиками
# 0 - не отображать, 1 - отображать

    mapSetNodeView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetNodeView', maptype.HMAP, ctypes.c_int)
    def mapSetNodeView(_hmap: maptype.HMAP, _mode: int) -> ctypes.c_void_p:
        return mapSetNodeView_t (_hmap, _mode)


# Запросить/Установить цвет (RGB) отображения контура редактируемого объекта для режимов Редактора карты

    mapGetEditLineColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEditLineColor')
    def mapGetEditLineColor() -> int:
        return mapGetEditLineColor_t ()

    mapSetEditLineColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetEditLineColor', ctypes.c_int)
    def mapSetEditLineColor(_color: int) -> int:
        return mapSetEditLineColor_t (_color)


# Запросить/Установить толщину (мкм) отображения контура редактируемого объекта для режимов Редактора карты

    mapGetEditLineThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEditLineThick')
    def mapGetEditLineThick() -> int:
        return mapGetEditLineThick_t ()

    mapSetEditLineThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetEditLineThick', ctypes.c_int)
    def mapSetEditLineThick(_thick: int) -> int:
        return mapSetEditLineThick_t (_thick)


# Запросить/Установить цвет (RGB) отображения контура вспомогательного объекта для режимов Редактора карты

    mapGetSourceLineColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSourceLineColor')
    def mapGetSourceLineColor() -> int:
        return mapGetSourceLineColor_t ()

    mapSetSourceLineColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSourceLineColor', ctypes.c_int)
    def mapSetSourceLineColor(_color: int) -> int:
        return mapSetSourceLineColor_t (_color)


# Запросить/Установить толщину (мкм) отображения контура вспомогательного объекта для режимов Редактора карты

    mapGetSourceLineThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSourceLineThick')
    def mapGetSourceLineThick() -> int:
        return mapGetSourceLineThick_t ()

    mapSetSourceLineThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSourceLineThick', ctypes.c_int)
    def mapSetSourceLineThick(_thick: int) -> int:
        return mapSetSourceLineThick_t (_thick)


# Запросить/Установить цвет (RGB) отображения точки - узла контура

    mapGetSelectPointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectPointColor')
    def mapGetSelectPointColor() -> int:
        return mapGetSelectPointColor_t ()

    mapSetSelectPointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectPointColor', ctypes.c_int)
    def mapSetSelectPointColor(_color: int) -> int:
        return mapSetSelectPointColor_t (_color)


# Запросить/Установить цвет (RGB) отображения точки - виртуального узла контура (между реальными узлами)

    mapGetSelectVirtualPointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectVirtualPointColor')
    def mapGetSelectVirtualPointColor() -> int:
        return mapGetSelectVirtualPointColor_t ()

    mapSetSelectVirtualPointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectVirtualPointColor', ctypes.c_int)
    def mapSetSelectVirtualPointColor(_color: int) -> int:
        return mapSetSelectVirtualPointColor_t (_color)


# Запросить/Установить цвет (RGB) отображения линии рамки для выбора области

    mapGetSelectFrameColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFrameColor')
    def mapGetSelectFrameColor() -> int:
        return mapGetSelectFrameColor_t ()

    mapSetSelectFrameColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectFrameColor', ctypes.c_int)
    def mapSetSelectFrameColor(_color: int) -> int:
        return mapSetSelectFrameColor_t (_color)


# Запросить/Установить толщину (мкм) отображения линии рамки для выбора области

    mapGetSelectFrameThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectFrameThick')
    def mapGetSelectFrameThick() -> int:
        return mapGetSelectFrameThick_t ()

    mapSetSelectFrameThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectFrameThick', ctypes.c_int)
    def mapSetSelectFrameThick(_thick: int) -> int:
        return mapSetSelectFrameThick_t (_thick)


# Установить общие параметры проекции документа для отображения,
# печати и расчета координат
# hmap  - идентификатор открытых данных (документа)
# Структуры MAPREGISTER, DATUMPARAM и ELLIPSOIDPARAM описаны в mapcreat.h
# type  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# parm - параметры локального преобразования координат (см. mapcreat.h)
# Устанавливать общие параметры проекции можно для документа
# поддерживающего пересчет геодезических координат (mapIsGeoSupported() != 0)
# После установки общих параметров проекции изображение карты формируется
# в заданной проекции. Векторные карты, матрицы и растры, имеющие другие параметры
# трансформируются в процессе отображения.
# Все операции с координатами (mapPlaneToGeo, mapGeoToPlane,
# mapPlaneToGeoWGS84, mapAppendPointPlane, mapInsertPointPlane,
# mapUpdatePointPlane, mapAppendPointGeo и другие) выполняются
# в системе координат документа, определяемой общими параметрами проекции
# При чтении\записи координат в конкретной карте выполняется пересчет
# из системы координат документа
# Например, при записи координат из WGS84 на карту в СК-42 можно
# установить общие параметры документа, как "Широта/Долгота на WGS84"
# и выполнить запись координат функцией mapAppendPointGeo, не заботясь
# о дополнительном пересчете координат, или считать координаты функцией
# mapGetGeoPoint (или функцией mapGetGeoPointWGS84, игнорирующей параметры
# документа).
# Чтобы установить текущие параметры проекции и системы координат, как у первой
# карты в документе можно передать в качестве параметров (кроме hMap) нули,
# или вызвать mapClearDocProjection.
# При ошибке возвращает ноль

    mapSetDocProjectionPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetDocProjectionPro(_hMap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetDocProjectionPro_t (_hMap, _mapreg, _datum, _ellparm, _ttype, _tparm)


# Установить общие параметры проекции документа для отображения,
# печати и расчета координат из пользовательской системы координат
# hmap  - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат (см. mapCreateUserSystemParametersPro)
# При ошибке возвращает ноль

    mapSetDocProjectionFromUserSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetDocProjectionFromUserSystem', maptype.HMAP, ctypes.c_void_p)
    def mapSetDocProjectionFromUserSystem(_hMap: maptype.HMAP, _huser: ctypes.c_void_p) -> int:
        return mapSetDocProjectionFromUserSystem_t (_hMap, _huser)

    mapClearDocProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearDocProjection', maptype.HMAP)
    def mapClearDocProjection(_hMap: maptype.HMAP) -> int:
        return mapClearDocProjection_t (_hMap)


# Запросить общие параметры проекции документа для отображения,
# печати и расчета координат
# hmap  - идентификатор открытых данных (документа)
# Структуры MAPREGISTER, DATUMPARAM и ELLIPSOIDPARAM описаны в mapcreat.h
# type  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# parm - параметры локального преобразования координат (см. mapcreat.h)
# Если параметры не устанавливались функцией mapSetMapInfoEx,
# то они соответсвуют параметрам карты, открытой в документе первой
# При ошибке возвращает ноль

    mapGetDocProjectionPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetDocProjectionPro(_hMap: maptype.HMAP, _map: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetDocProjectionPro_t (_hMap, _map, _datum, _ellparm, _ttype, _tparm)


# Запросить - устанавливались ли общие параметры проекции документа
# для отображения, печати и расчета координат
# hmap  - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapIsDocProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsDocProjection', maptype.HMAP)
    def mapIsDocProjection(_hMap: maptype.HMAP) -> int:
        return mapIsDocProjection_t (_hMap)


# Запросить размеры общего изображения карты в пикселах для текущего масштаба
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetPictureHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPictureHeight', maptype.HMAP)
    def mapGetPictureHeight(_hMap: maptype.HMAP) -> int:
        return mapGetPictureHeight_t (_hMap)

    mapGetPictureWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPictureWidth', maptype.HMAP)
    def mapGetPictureWidth(_hMap: maptype.HMAP) -> int:
        return mapGetPictureWidth_t (_hMap)


# Запросить размеры общего изображения карты в пикселах для текущего масштаба
# hpaint - идентификатор контекста отображения для многопоточного вызова
# В переменную width заносится ширина изображения (dx),
# в переменную height - высота (dy)

    mapGetPictureSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetPictureSizeEx', ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), maptype.HPAINT)
    def mapGetPictureSizeEx(_width: ctypes.POINTER(ctypes.c_int), _height: ctypes.POINTER(ctypes.c_int), _hPaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapGetPictureSizeEx_t (_width, _height, _hPaint)


# Запросить ширину пиксела изображения карты в метрах на местности
# для текущего масштаба изображения
# При ошибке возвращает ноль

    mapGetPixelWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPixelWidth', maptype.HMAP)
    def mapGetPixelWidth(_hMap: maptype.HMAP) -> float:
        return mapGetPixelWidth_t (_hMap)


# Запросить высоту пиксела изображения карты в метрах на местности
# для текущего масштаба изображения
# При ошибке возвращает ноль

    mapGetPixelHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPixelHeight', maptype.HMAP)
    def mapGetPixelHeight(_hMap: maptype.HMAP) -> float:
        return mapGetPixelHeight_t (_hMap)


# Запросить текущее число пикселов на метр изображения - разрешение по вертикали
# При ошибке возвращает ноль

    mapGetVerticalPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetVerticalPixel', maptype.HMAP)
    def mapGetVerticalPixel(_hMap: maptype.HMAP) -> float:
        return mapGetVerticalPixel_t (_hMap)


# Запросить текущее число пикселов на метр изображения - разрешение по горизонтали
# При ошибке возвращает ноль

    mapGetHorizontalPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHorizontalPixel', maptype.HMAP)
    def mapGetHorizontalPixel(_hMap: maptype.HMAP) -> float:
        return mapGetHorizontalPixel_t (_hMap)


# Запретить/Разрешить построение дерева объектов для отображения всех карт
# Построение дерева замедляет (от долей секунды до нескольких секунд) открытие
# неотсортированных карт с большим числом объектов (от нескольких сот тысяч и более),
# но ускоряет (в 1,5 - 3 раза) отображение больших карт в крупных масштабах
# (отбор объектов для фрагмента)
# Дерево объектов обычно применяется для серверных приложений или индикаторов,
# длительно работающих с постоянным набором карт и интенсивным отображением
# flag - признак применения дерева объектов (если не ноль)
# Возвращает ранее установленное значение

    mapSetFrameTree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFrameTree', ctypes.c_int)
    def mapSetFrameTree(_flag: int) -> int:
        return mapSetFrameTree_t (_flag)


# Создать/Удалить контекст отображения для многопоточного вызова
# функций mapPaintByFramePro или mapPaintByFrameToXImagePro
# hmap - идентификатор открытых данных
# hpaint - контекст отображения для копирования параметров отображения\печати или 0
# Для каждого потока создается свой контекст и передается в качестве параметра функции
# В каждом контексте создается свой буфер отображения и выделяется память под служебные области
# Размер резервируемой памяти помимо буфера отображения может занимать 1-2 Мбайта,
# внутренний буфер отображения для размера 1920x1080 занимает 8 Мбайт
# Размер может устанавливаться программно - mapSetMaxScreenImageSize
# При ошибке возвращает ноль

    mapCreatePaintControlEx_t = mapsyst.GetProcAddress(acceslib,maptype.HPAINT,'mapCreatePaintControlEx', maptype.HMAP, maptype.HPAINT)
    def mapCreatePaintControlEx(_hmap: maptype.HMAP, _hpaint: maptype.HPAINT) -> maptype.HPAINT:
        return mapCreatePaintControlEx_t (_hmap, _hpaint)

    mapCreatePaintControl_t = mapsyst.GetProcAddress(acceslib,maptype.HPAINT,'mapCreatePaintControl', maptype.HMAP)
    def mapCreatePaintControl(_hmap: maptype.HMAP) -> maptype.HPAINT:
        return mapCreatePaintControl_t (_hmap)

    mapFreePaintControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreePaintControl', maptype.HPAINT)
    def mapFreePaintControl(_hPaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapFreePaintControl_t (_hPaint)


# Сменить идентификатор открытых данных в контексте отображения
# Применяется для последовательной отрисовки в многопоточном варианте
# в буфер изображения одного контекста из нескольких HMAP
# для наложения слоев
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapSetPaintControlMapHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetPaintControlMapHandle', maptype.HPAINT, maptype.HMAP)
    def mapSetPaintControlMapHandle(_hPaint: maptype.HPAINT, _hmap: maptype.HMAP) -> int:
        return mapSetPaintControlMapHandle_t (_hPaint, _hmap)


# Установить параметры системы координат документа в контексте отображения
# Применяется для установки системы координат формируемого изображения по коду EPSG
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# epsgcode - код EPSG для требуемой системы координат (например, 3395, 3857, 4326)
# Для геодезических систем координат возвращает 2,
# для плоских прямоугольных возвращает 1.
# При ошибке возвращает ноль

    mapSetPaintControlProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetPaintControlProjection', maptype.HPAINT, ctypes.c_int)
    def mapSetPaintControlProjection(_hPaint: maptype.HPAINT, _epsgcode: int) -> int:
        return mapSetPaintControlProjection_t (_hPaint, _epsgcode)


# Установить параметры системы координат документа в контексте отображения
# Применяется для установки системы координат формируемого изображения
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# При ошибке возвращает ноль

    mapSetPaintControlProjectionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetPaintControlProjectionEx', maptype.HPAINT, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetPaintControlProjectionEx(_hPaint: maptype.HPAINT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetPaintControlProjectionEx_t (_hPaint, _mapreg, _datum, _ellipsoid)


# Установить параметры рисования объектов новыми примитивами. Устанавливается для текущего контекста рисования.
# drawList - список (DRAWOBJECT) примитивов и условий их отбора для рисования объектов на карте.
# Создать drawList можно с помощью функции mapCreatePaintDrawList (maprscex.h).
# Объекты,не вошедшие в список, рисуются согласно условным знакам классификатора
# Добавить объекты в список можно с помощью функции mapAppendDrawToDrawList или в автоматическом режиме
# функцией gmlCreatePaintDrawListByOgcSld (gmlapi.h)
# Для отключения рисования объектов новыми примитивами необходим вызов mapSetPaintControlDrawList(hPaint, 0)
# При ошибке возвращает ноль

    mapSetPaintControlDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetPaintControlDrawList', maptype.HPAINT, ctypes.c_void_p)
    def mapSetPaintControlDrawList(_hPaint: maptype.HPAINT, _drawList: ctypes.c_void_p) -> int:
        return mapSetPaintControlDrawList_t (_hPaint, _drawList)


# Запросить идентификатор открытых данных, для которых создан контекст отображения
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# При ошибке возвращает ноль

    mapGetPaintControlMapHandle_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapGetPaintControlMapHandle', maptype.HPAINT)
    def mapGetPaintControlMapHandle(_hPaint: maptype.HPAINT) -> maptype.HMAP:
        return mapGetPaintControlMapHandle_t (_hPaint)


# Скопировать содержимое внутренниего буфера в заданную область
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# imagedesc - описание выходного буфера изображения
# При ошибке возвращает ноль

    mapCopyPaintControlToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyPaintControlToXImage', maptype.HPAINT, ctypes.POINTER(maptype.XIMAGEDESC))
    def mapCopyPaintControlToXImage(_hPaint: maptype.HPAINT, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC)) -> int:
        return mapCopyPaintControlToXImage_t (_hPaint, _imagedesc)


# Запросить код ошибки, возникшей при рисовании
# В случае успеха возвращает ноль, иначе код ошибки

    mapGetPaintErrorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPaintErrorCode', maptype.HPAINT)
    def mapGetPaintErrorCode(_hPaint: maptype.HPAINT) -> int:
        return mapGetPaintErrorCode_t (_hPaint)


# Отобразить фрагмент карты, смасштабировав до заданной ширины и высоты
# в текущем составе объектов (применяется для обработки OGC WMS-запросов)
# hmap - идентификатор открытых данных
# hdc   - идентификатор контекста устройства вывода,
#         если контекст устройства вывода равен 0, то отрисовка выполняется
#         во внутренний буфер контекста отображения (hPaint)
# erase - признак стирания фона перед выводом,
#        (0 - фон не стирать, !=0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает
#         цветом фона, кроме значения -2 (минус 2))
#         При последовательном отображении нескольких HMAP в один контекст
#         отображения, для второго HMAP и далее значение erase = -2 при hdc = 0
# frame  - координаты фрагмента карты в системе координат документа в метрах
# (см. mapSetDocProjection)
# width  - ширина изображения в пикселах
# height - высота изображения в пикселах
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# filename  - полное имя создаваемого файла формата png
# viewselect - условия отбора отображаемых объектов, если равно 0, то применяются
#           условия обобщенного поиска\выделения (внутренние)
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# Данная функция может изменять текущий масштаб отображения документа (если hPaint равен 0),
# для сохранения текущего масштаба можно применить функции mapGetRealShowScale/mapSetRealShowScale
# При ошибке возвращает ноль

    mapPaintByFramePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintByFramePro', maptype.HMAP, maptype.HDC, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFramePro(_hMap: maptype.HMAP, _hDC: maptype.HDC, _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hPaint: maptype.HPAINT) -> int:
        return mapPaintByFramePro_t (_hMap, _hDC, _erase, _frame, _width, _height, _alpha, _viewselect, _hPaint)

    mapPaintByFrameToFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintByFrameToFileUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int)
    def mapPaintByFrameToFileUn(_hMap: maptype.HMAP, _filename: mapsyst.WTEXT, _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int) -> int:
        return mapPaintByFrameToFileUn_t (_hMap, _filename.buffer(), _erase, _frame, _width, _height)


# Отобразить фрагмент карты на заданном устройстве
# в текущих масштабе и составе объектов
# Функция mapPaintDoc печатает карту и список врезок без необходимости
# дополнительного вызова mapPaintInset
# hmap  - идентификатор открытых данных
# hdc   - идентификатор контекста устройства вывода,
# erase - признак стирания фона перед выводом,
#        (0 - фон не стирать, !=0 - очистить фрагмент цветом фона,
#        для экранного способа вывода (VT_SCREEN) всегда стирает
#        цветом фона, кроме значения -2 (минус 2))
# rect - координаты фрагмента карты (Draw) в изображении (Picture)
# Корректно работает с большими изображениями под Windows95 и NT,
# но требует перед вызовом установки
#              ::SetViewportOrgEx(hDC, dx , dy, 0),
# где dx,dy - положение отображаемого фрагмента в клиентной
# области !
# Размер картинки, рисуемой за один вызов, не более
# текущих размеров экрана! Иначе - см. PaintToDib,PaintToImage...
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# filename  - полное имя создаваемого файла формата png
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# Если image != 0 и object != 0 дополнительно вызвается фукция
# mapPaintMapObject95Ex  (Отобразить произвольный объект в пределах фрагмента
# в условных знаках пользователя)
# image - описание вида объекта (см. MAPGDI.H),
# object - идентификатор объекта

    mapPaintDocEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintDocEx', maptype.HMAP, maptype.HDC, ctypes.c_int, ctypes.POINTER(maptype.LRECT), ctypes.c_int)
    def mapPaintDocEx(_hmap: maptype.HMAP, _hdc: maptype.HDC, _erase: int, _rect: ctypes.POINTER(maptype.LRECT), _alpha: int) -> int:
        return mapPaintDocEx_t (_hmap, _hdc, _erase, _rect, _alpha)

    mapPaintDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintDoc', maptype.HMAP, maptype.HDC, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int)
    def mapPaintDoc(_hmap: maptype.HMAP, _hdc: maptype.HDC, _erase: int, _rect: ctypes.POINTER(maptype.RECT), _alpha: int) -> int:
        return mapPaintDoc_t (_hmap, _hdc, _erase, _rect, _alpha)

    mapPaintDocToXImageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintDocToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.LRECT), ctypes.c_int)
    def mapPaintDocToXImageEx(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _x: int, _y: int, _rect: ctypes.POINTER(maptype.LRECT), _alpha: int) -> int:
        return mapPaintDocToXImageEx_t (_hmap, _imagedesc, _erase, _x, _y, _rect, _alpha)

    mapPaintDocToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintDocToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int)
    def mapPaintDocToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _alpha: int) -> int:
        return mapPaintDocToXImage_t (_hmap, _imagedesc, _erase, _x, _y, _rect, _alpha)

    mapPaint95Pro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaint95Pro', maptype.HMAP, maptype.HDC, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int, maptype.HPAINT)
    def mapPaint95Pro(_hmap: maptype.HMAP, _hdc: maptype.HDC, _erase: int, _rect: ctypes.POINTER(maptype.RECT), _alpha: int, _hPaint: maptype.HPAINT) -> int:
        return mapPaint95Pro_t (_hmap, _hdc, _erase, _rect, _alpha, _hPaint)
    if os.name == 'nt':
        mapPaint95ToFileUn_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapPaint95ToFileUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
        def mapPaint95ToFileUn(_hMap: maptype.HMAP, _filename: mapsyst.WTEXT, _erase: int, _rect: ctypes.POINTER(maptype.RECT), _alpha: int, _image: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ) -> int:
            return mapPaint95ToFileUn_t(_hMap, _filename.buffer(), _erase, _rect, _alpha, _image, _object)


# Отобразить фрагмент карты на заданном устройстве
# в текущих масштабе и составе объектов и
# выделить на карте объекты, удовлетворющие заданным условим
# hMap   - идентификатор открытых данных
# hdc    - контекст устройства
# erase  - признак стирания фона перед выводом,
#          (0 - фон не стирать, !=0 - очистить фрагмент цветом фона,
#          для экранного способа вывода (VT_SCREEN) всегда стирает
#          цветом фона, кроме значения -2 (минус 2))
# rect   - координаты фрагмента карты (Draw) в изображении (Picture)
# select - условия отбора объектов, если равны 0, то применяются
#          условия обобщенного поиска\выделения (см. mapTotalPaintSelect95).
# color  - цвет, которым будут выделяться объекты на карте
# Корректно работает с большими изображениями под Windows95 и NT,
# но требует перед вызовом установки
#              ::SetViewportOrgEx(hDC, dx , dy, 0),
# где dx,dy - положение отображаемого фрагмента в клиентной области !
# Размер картинки, рисуемой за один вызов, не более
# текущих размеров экрана!
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# filename  - полное имя создаваемого файла формата png
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# Если image != 0 и object != 0 дополнительно вызвается фукция
# mapPaintMapObject95Ex  (Отобразить произвольный объект в пределах фрагмента
# в условных знаках пользователя)
# image - описание вида объекта (см. MAPGDI.H),
# object - идентификатор объекта

    mapPaint95AndSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPaint95AndSelectEx', maptype.HMAP, maptype.HDC, ctypes.c_int, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF, ctypes.c_int)
    def mapPaint95AndSelectEx(_hMap: maptype.HMAP, _hDC: maptype.HDC, _erase: int, _rect: ctypes.POINTER(maptype.RECT), _select: maptype.HSELECT, _color: maptype.COLORREF, _alpha: int) -> ctypes.c_void_p:
        return mapPaint95AndSelectEx_t (_hMap, _hDC, _erase, _rect, _select, _color, _alpha)
    if os.name == 'nt':
        mapPaint95AndSelectToFileUn_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapPaint95AndSelectToFileUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF, ctypes.c_int, ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
        def mapPaint95AndSelectToFileUn(_hMap: maptype.HMAP, _filename: mapsyst.WTEXT, _erase: int, _rect: ctypes.POINTER(maptype.RECT), _select: maptype.HSELECT, _color: maptype.COLORREF, _alpha: int, _image: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ) -> int:
            return mapPaint95AndSelectToFileUn_t(_hMap, _filename.buffer(), _erase, _rect, _select, _color, _alpha, _image, _object)


# Установить толщину линии для отрисовки выделенных на карте
# объектов (при вызове mapPaint95AndSelect и т.п.)
# thick - толщина линии в mkm (из пикселов - PIX2MKM(pixel))
# Возвращает установленное ранее значение

    mapSetSelectLineThick_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectLineThick', maptype.HMAP, ctypes.c_int)
    def mapSetSelectLineThick(_hmap: maptype.HMAP, _thick: int) -> int:
        return mapSetSelectLineThick_t (_hmap, _thick)


# Отобразить отдельный объект карты в пределах фрагмента
# в условных знаках карты
# Может использоваться для вывода шаблонов объектов
# hmap - идентификатор открытых данных
# hdc   - идентификатор контекста устройства вывода,
# rect  - координаты фрагмента карты (Draw)
# info - идентификатор объекта карты в памяти
# Корректно работает с большими изображениями под Windows95 и NT,
# При ошибке в параметрах возвращает ноль
# Размер картинки, рисуемой за один вызов, не более
# текущих размеров экрана! Иначе - см. PaintToDib,PaintToImage...
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать

    mapPaintObject95Ex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintObject95Ex', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.HOBJ, ctypes.c_int)
    def mapPaintObject95Ex(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _info: maptype.HOBJ, _alpha: int) -> int:
        return mapPaintObject95Ex_t (_hmap, _hdc, _rect, _info, _alpha)


# Отобразить произвольный объект в пределах фрагмента окна (карты)
# в условных знаках пользователя
# hmap - идентификатор открытых данных
# hdc   - идентификатор контекста устройства вывода,
# rect  - координаты фрагмента карты (Draw)
# image - описание вида объекта (см. MAPGDI.H), если объект
# должен рисоваться своим условным знаком - значение параметра
# можно установить в ноль
# info - идентификатор объекта карты в памяти
# При ошибке в параметрах возвращает ноль
# Размер картинки, рисуемой за один вызов, не более
# текущих размеров экрана! Иначе - см. PaintToDib,PaintToImage...
# filename  - полное имя создаваемого файла формата png
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать

    mapPaintMapObject95L_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintMapObject95L', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ, ctypes.c_int)
    def mapPaintMapObject95L(_hMap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.LRECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ, _alpha: int = 0) -> int:
        return mapPaintMapObject95L_t (_hMap, _hdc, _rect, _image, _object, _alpha)

    mapPaintMapObject95Ex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintMapObject95Ex', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ, ctypes.c_int)
    def mapPaintMapObject95Ex(_hMap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ, _alpha: int) -> int:
        return mapPaintMapObject95Ex_t (_hMap, _hdc, _rect, _image, _object, _alpha)
    if os.name == 'nt':
        mapPaintMapObject95ToFileUn_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapPaintMapObject95ToFileUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ, ctypes.c_int)
        def mapPaintMapObject95ToFileUn(_hMap: maptype.HMAP, _filename: mapsyst.WTEXT, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ, _alpha: int) -> int:
            return mapPaintMapObject95ToFileUn_t(_hMap, _filename.buffer(), _rect, _image, _object, _alpha)


# Отобразить произвольный объект в пределах фрагмента
# в условных знаках пользователя
# hmap - идентификатор открытых данных
# hdc   - идентификатор контекста устройства вывода,
# rect - координаты фрагмента карты (Draw) в изображении (Picture)
# image - описание вида объекта (см. MAPGDI.H), если объект
# должен рисоваться своим условным знаком - значение параметра
# можно установить в ноль,
# info - идентификатор объекта карты в памяти
# offset - смещение координат объекта (в соответствии с place)
# place - вид системы координат (в точках экрана - PP_PICTURE, в метрах в
#         системе координат документа - PP_PLANE, в радианах на эллипсоиде
#         документа - PP_GEO)
# При ошибке в параметрах возвращает ноль

    mapPaintOffsetMapObject95_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintOffsetMapObject95', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapPaintOffsetMapObject95(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _info: maptype.HOBJ, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _place: int = maptype.PP_MAP) -> int:
        return mapPaintOffsetMapObject95_t (_hmap, _hdc, _rect, _image, _info, _offset, _place)


# Отобразить образец вида объекта по номеру записи в классификаторе объектов (incode)
# hmap - идентификатор открытой карты
# hrsc - идентификатор классификатора открытой карты
# hdc  - идентификатор контекста устройства вывода,
# rect - координаты клиентской области окна вывода (размер окна)
# incode - внутренний код объекта
# visualtype - тип визуализации (VT_SCREEN, VT_PRINT)
# text - образец текста для подписи
# factor - процент изменения размера знака для отображения больших знаков
#          в маленьких окошках (50 - сжать в 2 раза, 150 - увеличить в 1,5 раза)
# semvalue - запись семантики для формирования образца знака или ноль
# При ошибке возвращает ноль

    mapPaintExampleRscObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleRscObjectEx', maptype.HMAP, maptype.HRSC, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.SEMANTIC))
    def mapPaintExampleRscObjectEx(_hMap: maptype.HMAP, _hRsc: maptype.HRSC, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _visualtype: int, _text: mapsyst.WTEXT, _factor: int, _semvalue: ctypes.POINTER(maptype.SEMANTIC)) -> int:
        return mapPaintExampleRscObjectEx_t (_hMap, _hRsc, _hdc, _rect, _incode, _visualtype, _text.buffer(), _factor, _semvalue)


# Отобразить фрагмент карты, смасштабировав до заданной ширины и высоты
# в текущем составе объектов
# hmap  - идентификатор открытых данных
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом,
# (0 - фон не стирать, !=0 - очистить фрагмент цветом фона,
#  для экранного способа вывода (VT_SCREEN) всегда стирает
#  цветом фона, кроме значения -2 (минус 2))
# frame  - координаты фрагмента карты в системе координат документа в метрах
# (см. mapSetDocProjection)
# width  - ширина изображения в пикселах
# height - высота изображения в пикселах
# Описание структуры XIMAGEDESC в maptype.h
# alpha - флаг использования альфа канала 0 - не использовать 1 - использовать
# viewselect - условия отбора объектов, если равны 0, то применяются
# условия обобщенного поиска\выделения
# hPaint - идентификатор контекста отображения для многопоточного вызова функции отображения
# При ошибке возвращает ноль

    mapPaintByFrameToXImagePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintByFrameToXImagePro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFrameToXImagePro(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hPaint: maptype.HPAINT) -> int:
        return mapPaintByFrameToXImagePro_t (_hMap, _imagedesc, _erase, _frame, _width, _height, _alpha, _viewselect, _hPaint)


# Вывести изображение карты в XImage (массив)
# Данная функция реализована для XWindow !
# Описание структуры XIMAGEDESC в maptype.h
# erase - признак стирания фона перед выводом,
#        (-2 - рисовать поверх текущего изображения в буфере)
# x,y - координаты левого верхнего угла внутри
# битовой области XImage для размещения изображения
# rect - выводимый фрагмент карты
# При ошибке в параметрах возвращает ноль

    mapPaintToXImageProL_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintToXImageProL', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.LRECT), maptype.HPAINT)
    def mapPaintToXImageProL(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _x: int, _y: int, _rect: ctypes.POINTER(maptype.LRECT), _hPaint: maptype.HPAINT) -> int:
        return mapPaintToXImageProL_t (_hMap, _imagedesc, _erase, _x, _y, _rect, _hPaint)

    mapPaintToXImagePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintToXImagePro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), maptype.HPAINT)
    def mapPaintToXImagePro(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _hPaint: maptype.HPAINT) -> int:
        return mapPaintToXImagePro_t (_hMap, _imagedesc, _erase, _x, _y, _rect, _hPaint)


# Отобразить произвольный объект в пределах фрагмента
# в условных знаках пользователя в структуру XImage
# imagedesc - структура XIMAGEDESC (см. maptype.h)
# x,y   - координаты левого верхнего угла внутри
# rect  - выводимый фрагмент карты в пикселах текущего изображения карты
# image - описание вида объекта (см. mapgdi.h),
# data  - координаты объекта,
# place - вид системы координат (в точках экрана - PP_PICTURE, в метрах в
#         системе координат документа - PP_PLANE, в радианах на эллипсоиде
#         документа - PP_GEO)
# При ошибке в параметрах возвращает ноль

    mapPaintUserObjectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintUserObjectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_int)
    def mapPaintUserObjectToXImage(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapPaintUserObjectToXImage_t (_hMap, _imagedesc, _x, _y, _rect, _image, _data, _place)


# Вывести выделение объектов карты в XImage (массив)
# imagedesc - описание буфера вывода (см. maptype.h)
# x, y - координаты левого верхнего угла внутри буфера
# rect - выводимый фрагмент карты
# select - условие отбора выделенных объектов
# color - цвет выделения объектов
# alpha - флаг использования альфа-канала
# paintControl - идентификатор контекста отображения для многопоточного вызова функции отображения

    mapPaintSelectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintSelectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF, ctypes.c_long, maptype.HPAINT)
    def mapPaintSelectToXImage(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _select: maptype.HSELECT, _color: maptype.COLORREF, _alpha: int, _paintControl: maptype.HPAINT) -> int:
        return mapPaintSelectToXImage_t (_hMap, _imagedesc, _x, _y, _rect, _select, _color, _alpha, _paintControl)


# Вывести изображение выделенных объектов
# в текущем составе объектов
# frame  - координаты фрагмента карты в системе координат документа в метрах
# (см. mapSetDocProjection)
# width  - ширина изображения в пикселах
# height - высота изображения в пикселах
# Описание структуры XIMAGEDESC в maptype.h
# erase - признак стирания фона перед выводом,
# (0 - фон не стирать, 1 - очистить фрагмент цветом фона),
# -2 - рисовать поверх текущего изображения в буфере
# select - условие отбора для выделенных объектов
# color - цвет выделения объектов
# При ошибке возвращает ноль

    mapPaintSelectByFrameToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintSelectByFrameToXImage', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.HSELECT, maptype.HPAINT, maptype.COLORREF)
    def mapPaintSelectByFrameToXImage(_hMap: maptype.HMAP, _hsite: maptype.HSITE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hPaint: maptype.HPAINT, _color: maptype.COLORREF) -> int:
        return mapPaintSelectByFrameToXImage_t (_hMap, _hsite, _imagedesc, _erase, _frame, _width, _height, _alpha, _viewselect, _hPaint, _color)


# Вывести изображение карты в XImage (массив) и выделить
# на карте отобранные объекты
# Описание структуры XIMAGEDESC в maptype.h
# x,y - координаты левого верхнего угла внутри
# битовой области XImage для размещения изображения
# rect - выводимый фрагмент карты
# select - условия отбора объектов, если равны 0, то применяются
#          условия обобщенного поиска\выделения (см. mapTotalPaintSelect95).
# color  - цвет, которым будут выделяться объекты на карте
# При ошибке в параметрах возвращает ноль

    mapPaintAndSelectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintAndSelectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF)
    def mapPaintAndSelectToXImage(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _select: maptype.HSELECT, _color: maptype.COLORREF) -> int:
        return mapPaintAndSelectToXImage_t (_hMap, _imagedesc, _x, _y, _rect, _select, _color)


# Вывести изображение условного знака в XImage (массив)
# hmap  - идентификатор открытых данных
# imagedesc - параметры области для размещения изображения
# Описание структуры XIMAGEDESC в maptype.h
# erase - признак очистки области изображения (если равен -2, то изображение рисуется
#         поверх имеющегося рисунка без очистки)
# x,y - координаты левого верхнего угла внутри
# битовой области XImage для размещения изображения
# rect - фрагмент для вывода отображения
# func - функция отображения объекта
# parm - параметры изображения
# data - метрика для отображения
# colors - количество цветов
# palette - палитра
# При ошибке в параметрах возвращает ноль

    mapPaintExampleObjectByFuncDataToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleObjectByFuncDataToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(maptype.POLYDATAEX), ctypes.c_int, ctypes.POINTER(maptype.COLORREF))
    def mapPaintExampleObjectByFuncDataToXImage(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _func: int, _parm: ctypes.c_char_p, _data: ctypes.POINTER(maptype.POLYDATAEX), _colors: int, _palette: ctypes.POINTER(maptype.COLORREF)) -> int:
        return mapPaintExampleObjectByFuncDataToXImage_t (_hMap, _imagedesc, _x, _y, _rect, _func, _parm, _data, _colors, _palette)

    mapPaintExampleObjectByFuncDataToXImageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleObjectByFuncDataToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(maptype.POLYDATAEX))
    def mapPaintExampleObjectByFuncDataToXImageEx(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _x: int, _y: int, _rect: ctypes.POINTER(maptype.RECT), _func: int, _parm: ctypes.c_char_p, _data: ctypes.POINTER(maptype.POLYDATAEX)) -> int:
        return mapPaintExampleObjectByFuncDataToXImageEx_t (_hMap, _imagedesc, _erase, _x, _y, _rect, _func, _parm, _data)


# Вывести изображение условного знака в XImage (массив)
# Данная функция реализована для XWindow !
# Описание структуры XIMAGEDESC в maptype.h
# rect - фрагмент для вывода отображения
# func - функция отображения объекта
# parm - параметры изображения
# colors - количество цветов
# palette - палитра
# text - необходимый текст
# local - локализация
# При ошибке в параметрах возвращает ноль

    mapPaintExampleObjectByFuncToXImagePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleObjectByFuncToXImagePro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapPaintExampleObjectByFuncToXImagePro(_hMap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _func: int, _parm: ctypes.c_char_p, _colors: int, _palette: ctypes.POINTER(maptype.COLORREF), _text: mapsyst.WTEXT, _local: int, _erase: int) -> int:
        return mapPaintExampleObjectByFuncToXImagePro_t (_hMap, _imagedesc, _rect, _func, _parm, _colors, _palette, _text.buffer(), _local, _erase)


# Вывести изображение графического объекта в файл
# hobj - идентификатор объекта
# width - ширина изображения кратная 16
# height - высота изображения кратная 16
# filename - имя файла для сохранения
# transparentColor - цвет прозрачного фона
# При ошибке возвращает 0

    mapPaintDrawObjectToFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintDrawObjectToFile', maptype.HOBJ, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapPaintDrawObjectToFile(_hobj: maptype.HOBJ, _width: int, _height: int, _filename: mapsyst.WTEXT, _transparentColor: int) -> int:
        return mapPaintDrawObjectToFile_t (_hobj, _width, _height, _filename.buffer(), _transparentColor)


# Вывести изображение карты в метафайл
# Данные функции реализованы только для платформы Windows !
# При ошибке в параметрах возвращает ноль
    if os.name == 'nt':
        mapPaintToEmfExUn_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapPaintToEmfExUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.METAFILEBUILDPARMEX))
        def mapPaintToEmfExUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.METAFILEBUILDPARMEX)) -> int:
            return mapPaintToEmfExUn_t(_hMap, _name.buffer(), _parm)


# Отобразить образец вида объекта c учетом типа визуализации по
# номеру записи в классификаторе объектов (incode)
# Используется в диалогах выбора вида объекта
# hmap - идентификатор открытых данных
# hdc  - идентификатор контекста устройства вывода,
# rect - координаты фрагмента карты (Draw)
# в изображении (Picture),
# visualtype - тип визуализации (VT_SCREEN, VT_PRINT)
# text - текст для отображения знака типа подпись
# factor - процент изменения размера знака для отображения больших знаков
#          в маленьких окошках (50 - сжать в 2 раза, 150 - увеличить в 1,5 раза)
# При ошибке возвращает ноль

    mapPaintExampleObjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleObjectUn', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapPaintExampleObjectUn(_hMap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _visualtype: int, _text: mapsyst.WTEXT, _factor: int) -> int:
        return mapPaintExampleObjectUn_t (_hMap, _hdc, _rect, _incode, _visualtype, _text.buffer(), _factor)


# Установить/Запросить способ выделения площадных и линейных
# объектов на карте
# type - способ выделения (STF_CONTOUR - контур объекта,
# STF_OBJECT - весь объект)
# Возвращает значение, которое было ранее установлено

    mapSetSelectType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectType', ctypes.c_int)
    def mapSetSelectType(_type: int) -> int:
        return mapSetSelectType_t (_type)

    mapGetSelectType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSelectType')
    def mapGetSelectType() -> int:
        return mapGetSelectType_t ()


# Отобразить фрагмент карты на заданном устройстве с учетом калибровки
# в текущих масштабе и составе объектов
# hmap   - идентификатор открытых данных
# rect - координаты фрагмента карты (Draw) в изображении (Picture)
# parm - параметры печати
# При ошибке возвращает ноль

    mapPrint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPrint', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.PRINTPARM))
    def mapPrint(_hmap: maptype.HMAP, _hDC: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _parm: ctypes.POINTER(maptype.PRINTPARM)) -> int:
        return mapPrint_t (_hmap, _hDC, _rect, _parm)


# Установить пошаговый вывод DIB в окно
# flag - признак вывода промежуточных изображений в контекст вывода (0 или 1),
#        при нулевом значении изображение выводится один раз по готовности,
#        иначе - картинка выдается три раза в секунду пока формируется изображение
# Возвращает предыдущее значение

    mapSetPaintStepEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetPaintStepEx', maptype.HMAP, ctypes.c_int)
    def mapSetPaintStepEx(_hmap: maptype.HMAP, _millisec: int) -> int:
        return mapSetPaintStepEx_t (_hmap, _millisec)


# Запросить значение пошагового вывода DIB в окно
# Возвращает признак вывода промежуточных изображений в контекст вывода
# При нулевом значении изображение выводится один раз по готовности
# Если hmap равно нулю, то возвращает ноль

    mapGetPaintStepEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPaintStepEx', maptype.HMAP)
    def mapGetPaintStepEx(_hmap: maptype.HMAP) -> int:
        return mapGetPaintStepEx_t (_hmap)


# Установить режим качественного отображения подписей
# для строгого соблюдения размеров подписи при печати
# flag - ненулевое значение устанавливает режим качественного вывода
#        (при этом время отображения отдельной подписи увеличивается
#         примерно в 2 раза)
# При старте программы установлен режим качественного отображения
# Возвращает предыдущее значение

    mapSetTextQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTextQuality', ctypes.c_int)
    def mapSetTextQuality(_flag: int) -> int:
        return mapSetTextQuality_t (_flag)


# Запросить режим качественного отображения подписей
# для строгого соблюдения размеров подписи при печати

    mapGetTextQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextQuality')
    def mapGetTextQuality() -> int:
        return mapGetTextQuality_t ()


# Установить режим отображения графики с антиалиасингом
# flag - ненулевое значение устанавливает режим качественного вывода
# Если он включен в Windows, то рисование работает в однопоточном режиме из за
# локировок внутри библиотеки GDI+.
# При старте программы установлен режим отображения c антиалиасингом
# Возвращает предыдущее значение

    mapSetAntialiasedQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAntialiasedQuality', ctypes.c_int)
    def mapSetAntialiasedQuality(_flag: int) -> int:
        return mapSetAntialiasedQuality_t (_flag)


# Запросить режим отображения графики с антиалиасингом

    mapGetAntialiasedQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAntialiasedQuality')
    def mapGetAntialiasedQuality() -> int:
        return mapGetAntialiasedQuality_t ()


# Установить адрес функции, которая будет периодически
# вызываться при построении изображения карты и выводе
# его в заданный контекст отображения
# Устанавливать адрес рекомендуется перед каждым вызовом Paint,
# а по окончании отрисовки карты - отключать
# (устанавливать нулевой адрес).
# Вызываемая функция не должна сама вызывать Paint !
# call - адрес вызываемой функции (см. maptype.h),
# parm - параметр, который будет передан вызываемой функции.
# Кроме параметра parm вызываемой функции передается признак
# перерисовки карты (0/1) для ее пошагового обновления на экране
# Если вызываемая функция вернет ненулевое значение, то
# процесс отображения будет прерван (например, при анализе
# очереди сообщений вызванной функцией найден ввод с
# клавиатуры команды Esc, функция возвращает 1, отображение
# прерывается).

#    mapSetBreakCallAndParmEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetBreakCallAndParmEx', maptype.HMAP, maptype.BREAKCALLEX, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetBreakCallAndParmEx(_hMap: maptype.HMAP, _call: maptype.BREAKCALLEX, _parm: ctypes.POINTER(ctypes.c_void_p)) -> ctypes.c_void_p:
#        return mapSetBreakCallAndParmEx_t (_hMap, _call, _parm)


# Установить адрес функции, которая будет вызываться
# перед формированием изображения карты в области
# памяти или перед началом отображения карты на экран.
# Вызываемая функция не должна сама вызывать Paint !
# hmap   - идентификатор открытых данных
# call - адрес вызываемой функции (см. maptype.h),
# parm - параметр, который будет передан вызываемой функции.
# В вызываемой функции можно рисовать "под картой"
# с применением графических функций системы или функций
# типа PaintUserObject.

#    mapSetBeforePaintCallAndParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetBeforePaintCallAndParm', maptype.HMAP, maptype.BEFOREPAINT, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetBeforePaintCallAndParm(_hmap: maptype.HMAP, _call: maptype.BEFOREPAINT, _parm: ctypes.POINTER(ctypes.c_void_p)) -> ctypes.c_void_p:
#        return mapSetBeforePaintCallAndParm_t (_hmap, _call, _parm)


# Запросить число элементов в списке наборов данных
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetViewListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetViewListCount', maptype.HMAP)
    def mapGetViewListCount(_hMap: maptype.HMAP) -> int:
        return mapGetViewListCount_t (_hMap)


# Запросить название элемента (путь к набору данных) и тип в списке наборов данных
# hmap - идентификатор открытых данных
# itemname - указатель на буфер для записи пути к набору данных или алиаса данных
# size - размер буфера в байтах
# Возвращает один из следующих типов данных:
# FILE_MAP, FILE_RSW, FILE_MTW, FILE_MTQ, FILE_MTL, FILE_MTD, FILE_TIN, FILE_WMS
# При ошибке возвращает ноль

    mapGetViewListItemName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetViewListItemName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetViewListItemName(_hMap: maptype.HMAP, _index: int, _itemname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetViewListItemName_t (_hMap, _index, _itemname.buffer(), _size)


# Установить новое положение элемента в списке наборов данных
# hmap - идентификатор открытых данных
# index - номер элемента с 1 до mapGetViewListCount()
# position - новый номенр элемента в списке с 1 до mapGetViewListCount()
# При ошибке возвращает ноль

    mapSetItemPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetItemPosition', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetItemPosition(_hMap: maptype.HMAP, _index: int, _position: int) -> int:
        return mapSetItemPosition_t (_hMap, _index, _position)


# Запросить номер состояния списка наборов данных
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetViewListState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetViewListState', maptype.HMAP)
    def mapGetViewListState(_hMap: maptype.HMAP) -> int:
        return mapGetViewListState_t (_hMap)


# Функция настройки отображения карты с поворотом
#  hmap     - идентификатор открытых данных
#  angle    - угол поворота карты в плане с вершиной в
#             юго-западном углу карты (от -Pi до Pi)
#  fixation - угол сектора фиксации поворота отображения карты
#             относительно предыдущего положения (от 0 до Pi/6).
#             По умолчанию = Pi/18 (10 градусов)
# Угол fixation используется для минимизации дрожания изображения
# при движении по повернутой карте по прямой (или почти по прямой),
# когда при последовательном вызове функции подаются близкие
# значения угла поворота (angle). В случае, если разность между
# текущим углом поворота и требуемым будет меньше fixation,
# то новый угол поворота не устанавливается.
# Возвращает значение установленного угла поворота.
# При ошибке возвращает 0

    mapSetupTurn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetupTurn', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapSetupTurn(_hmap: maptype.HMAP, _angle: float, _fixation: float) -> float:
        return mapSetupTurn_t (_hmap, _angle, _fixation)


# Активен ли поворот ?
# hmap - идентификатор открытых данных
# Возвращает (1 - активен, 0 - нет)

    mapTurnIsActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTurnIsActive', maptype.HMAP)
    def mapTurnIsActive(_hmap: maptype.HMAP) -> int:
        return mapTurnIsActive_t (_hmap)


# Запросить угол поворота
# hmap - идентификатор открытых данных
# Возвращает значения от -Pi до Pi

    mapGetTurnAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTurnAngle', maptype.HMAP)
    def mapGetTurnAngle(_hmap: maptype.HMAP) -> float:
        return mapGetTurnAngle_t (_hmap)


# Установить масштаб отображения (знаменатель масштаба)
# hmap - идентификатор открытых данных
# x, y - координаты предполагаемого "центра изображения"
#        (любой точки привязки) в окне в текущем масштабе или нули
# scale - реальный масштаб отображения, который желают получить
# hpaint - идентификатор контекста отображения для многопоточного вызова
# Возвращает: 0 - масштаб не изменился, 1 - масштаб изменился
# x, y - координаты предполагаемого "центра изображения"
#        в окне относительно всей картинки в новом масштабе отображения
# При ошибке возвращает ноль

    mapSetRealScalePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRealScalePro', maptype.HMAP, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_double, maptype.HPAINT)
    def mapSetRealScalePro(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_int), _y: ctypes.POINTER(ctypes.c_int), _scale: float, _hPaint: maptype.HPAINT) -> int:
        return mapSetRealScalePro_t (_hmap, _x, _y, _scale, _hPaint)


# Запросить масштаб отображения (знаменатель масштаба)
# hpaint - идентификатор контекста отображения для многопоточного вызова
# При ошибке возвращает 1

    mapGetRealScalePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetRealScalePro', maptype.HPAINT)
    def mapGetRealScalePro(_hPaint: maptype.HPAINT) -> float:
        return mapGetRealScalePro_t (_hPaint)


# Установить масштаб отображения (знаменатель масштаба)
# hmap - идентификатор открытых данных
# scale - реальный масштаб отображения, который желают получить
# hpaint - идентификатор контекста отображения для многопоточного вызова
# horpix/verpix - число пикселов в метре по горизонтали и вертикали для устройства,
#        на которое будет вывод информации через hPaint, если указатели равны нулю,
#        то будет использовано разрешение, заданное в контексте отображения hpaint
# wmsscaleflag - признак согласования с масштабом геопортала
# Возвращает: 0 - масштаб не изменился, 1 - масштаб изменился
# При ошибке возвращает ноль

    mapSetRealScalePrint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetRealScalePrint', maptype.HMAP, ctypes.c_double, maptype.HPAINT, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)
    def mapSetRealScalePrint(_hmap: maptype.HMAP, _scale: float, _hpaint: maptype.HPAINT, _horpix: ctypes.POINTER(ctypes.c_double), _verpix: ctypes.POINTER(ctypes.c_double), _wmsscaleflag: int) -> int:
        return mapSetRealScalePrint_t (_hmap, _scale, _hpaint, _horpix, _verpix, _wmsscaleflag)


# Запросить точный масштаб отображения карты
# hmap - идентификатор открытых данных
# Возвращает значение знаменателя масштаба

    mapGetRealShowScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetRealShowScale', maptype.HMAP)
    def mapGetRealShowScale(_hmap: maptype.HMAP) -> float:
        return mapGetRealShowScale_t (_hmap)


# Установить точный масштаб отображения карты
# Возвращает значение знаменателя масштаба

    mapSetRealShowScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetRealShowScale', maptype.HMAP, ctypes.c_double)
    def mapSetRealShowScale(_hMap: maptype.HMAP, _scale: float) -> float:
        return mapSetRealShowScale_t (_hMap, _scale)


# Запросить текущий коэффициент масштабирования карты
# Например: 5 - растянута в 5 раз относительно базового масштаба,
#         0.1 - сжата в 10 раз.

    mapGetDrawScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDrawScale', maptype.HMAP)
    def mapGetDrawScale(_hmap: maptype.HMAP) -> float:
        return mapGetDrawScale_t (_hmap)


# Подобрать "стандартный" реальный масштаб, ближайший к заданному (scale)
# с учетом состава карты (для открытых данных WMTS могут быть
# другие стандартные масштабы)
# hmap - идентификатор открытых данных
# Возвращает новое реальное (неокругленное) значение знаменателя масштаба

    mapScaleToRoundScaleReal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapScaleToRoundScaleReal', maptype.HMAP, ctypes.c_double)
    def mapScaleToRoundScaleReal(_hmap: maptype.HMAP, _scale: float) -> float:
        return mapScaleToRoundScaleReal_t (_hmap, _scale)


# Установить способ масштабирования объектов карты при отображении
# method - способ масштабирования
# (0 - картографический "с запаздыванием увеличения", 1 - чертежный)
# Возвращает ранее установленное значение

    mapSetScaleMethod_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScaleMethod', ctypes.c_int)
    def mapSetScaleMethod(_method: int) -> int:
        return mapSetScaleMethod_t (_method)

    mapGetScaleMethod_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScaleMethod')
    def mapGetScaleMethod() -> int:
        return mapGetScaleMethod_t ()


# Установить/Запросить способ отображения векторных карт - Все объекты без учета границ видимости и состава
# flag - признак установки флага (1 - установить, 0 - сбросить)
# Доступно только для ГИС Панорама
# Возвращает ранее установленное значение
# Создать буфер образа окна карты в памяти для исключения мигания перемещаемых по карте объектов
# width  - ширина клиентской части окна карты в точках
# height - высота клиентской части окна карты в точках
# Создается первый буфер экрана, второй создается при первом вызове
# функции отображения объекта в буфер (Draw) -  для оптимального
# применения функций при отображении карты и без перемещаемых объектов
# Размер одного буфера в байтах - width # height # 4 (1920#1080#4 = 8 294 400, для 3 - 24 883 200)
# Всего может быть параллельно открыто до 1024 образов экранов одновременно
# Может применяться в паре с функцией mapChangeImageSizeEx
# При успешном выполнении возвращает идентификатор образа экрана
# При ошибке возвращает ноль

    mapCreateImageEx_t = mapsyst.GetProcAddress(acceslib,maptype.HIMAGE,'mapCreateImageEx', ctypes.c_int, ctypes.c_int)
    def mapCreateImageEx(_width: int, _height: int) -> maptype.HIMAGE:
        return mapCreateImageEx_t (_width, _height)



# Удалить буфер образа окна карты
# himage - идентификатор буфера окна

    mapCloseImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseImage', maptype.HIMAGE)
    def mapCloseImage(_image: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseImage_t (_image)


# Удалить буфер выделенных объектов в буфере образа окна карты
# himage - идентификатор буфера окна
# После удаления буфера выделенных объектов необходимо перерисовать буфер
# объектов, если он был открыт

    mapCloseTotalSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseTotalSelect', maptype.HIMAGE)
    def mapCloseTotalSelect(_image: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseTotalSelect_t (_image)


# Удалить буфер объектов в буфере образа окна карты для ускорения отображения
# himage - идентификатор буфера окна

    mapCloseObjectsImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseObjectsImage', maptype.HIMAGE)
    def mapCloseObjectsImage(_image: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseObjectsImage_t (_image)


# Запросить - открыт ли буфер объектов

    mapIsObjectsImageActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectsImageActive', maptype.HIMAGE)
    def mapIsObjectsImageActive(_image: maptype.HIMAGE) -> int:
        return mapIsObjectsImageActive_t (_image)


# Обновить размеры буфера образа окна карты
# himage - идентификатор буфера окна
# erase  - признак очистки окна, если равен 0 - содержимое сохраняется
# width  - новая ширина буфера
# height - новая высота буфера
# При ошибке возвращает ноль

    mapChangeImageSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeImageSizeEx', maptype.HIMAGE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapChangeImageSizeEx(_image: maptype.HIMAGE, _erase: int, _width: int, _height: int) -> int:
        return mapChangeImageSizeEx_t (_image, _erase, _width, _height)


# Очистить буфер образа окна карты
# himage - идентификатор буфера окна
# При ошибке во входных параметрах возвращает ноль

    mapClearMapImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearMapImage', maptype.HIMAGE)
    def mapClearMapImage(_image: maptype.HIMAGE) -> int:
        return mapClearMapImage_t (_image)


# Очистить буфер объектов в буфере образа окна карты
# himage - идентификатор буфера окна
# rect - область очистки или ноль (очистить весь буфер)

    mapClearObjectsImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearObjectsImage', maptype.HIMAGE, ctypes.POINTER(maptype.RECT))
    def mapClearObjectsImage(_image: maptype.HIMAGE, _rect: ctypes.POINTER(maptype.RECT)) -> ctypes.c_void_p:
        return mapClearObjectsImage_t (_image, _rect)


# Запросить размеры буфера образа окна карты
# При ошибке во входные параметрах возвращает ноль

    mapGetImageWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImageWidth', maptype.HIMAGE)
    def mapGetImageWidth(_image: maptype.HIMAGE) -> int:
        return mapGetImageWidth_t (_image)

    mapGetImageHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetImageHeight', maptype.HIMAGE)
    def mapGetImageHeight(_image: maptype.HIMAGE) -> int:
        return mapGetImageHeight_t (_image)


# Отобразить содержимое буфера образа окна карты в заданный контекст
# himage - идентификатор буфера окна
# hdc - контекст области отображения (окна),
# rect - координаты область отображения в буфере и контексте
# При ошибке возвращает ноль

    if os.name == 'nt':
        mapViewImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapViewImage', maptype.HIMAGE, maptype.HDC, ctypes.POINTER(maptype.RECT))
        def mapViewImage(_image: maptype.HIMAGE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
            return mapViewImage_t (_image, _hdc, _rect)


# Отобразить содержимое буфера в заданный внешний XImage
# rect - прямоугольник исходного изображения для копирования
#      = 0 - используется размер всего буфера
# offset - точка для размещения прямоугольника в XImage
#      = 0 - копируется с координатами {0, 0}
# При ошибке возвращает ноль

    mapViewImageToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapViewImageToXImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapViewImageToXImage(_image: maptype.HIMAGE, _ximage: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        return mapViewImageToXImage_t (_image, _ximage, _rect, _offset)


# Отобразить в буфер объектов содержимое внешнего XImage
# rect - прямоугольник исходного изображения для копирования
#      = 0 - используется размер всего буфера
# offset - точка для размещения прямоугольника в буфере объектов
#      = 0 - копируется с координатами {0, 0}
# При ошибке возвращает ноль

    mapCopyXImageToImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyXImageToImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapCopyXImageToImage(_image: maptype.HIMAGE, _ximage: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        return mapCopyXImageToImage_t (_image, _ximage, _rect, _offset)


# Скроллинг буфера образа окна карты
# himage - идентификатор буфера окна
# dx     - величина смещения окна по горизонтали (> 0 - слева направо, < 0 - справа налево)
# dy     - величина смещения окна по вертикали   (> 0 - сверху вниз, < 0 - снизу вверх)
# При ошибке возвращает ноль

    mapScrollImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapScrollImage', maptype.HIMAGE, ctypes.c_int, ctypes.c_int)
    def mapScrollImage(_himage: maptype.HIMAGE, _dx: int, _dy: int) -> int:
        return mapScrollImage_t (_himage, _dx, _dy)


# Обновить изображение заданного фрагмента карты в буфере образа окна карты
# После обновления карты изображение перемещаемых объектов стирается
# в пределах заданного фрагмента (для стирания объектов текущим видом карты достаточно вызвать mapClearObjectsImage)
# himage   - идентификатор буфера окна
# hMap     - идентификатор открытых данных
# rect     - обновляемый фрагмент карты, задается в пикселах в системе координат полного изображения карты (PICTURE)
# position - положение верхнего левого угла фрагмента в клиентской области окна карты (и образа экрана) или 0
# При ошибке возвращает ноль

    mapDrawImageMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageMap', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapDrawImageMap(_image: maptype.HIMAGE, _hMap: maptype.HMAP, _rect: ctypes.POINTER(maptype.RECT), _position: ctypes.POINTER(maptype.POINT)) -> int:
        return mapDrawImageMap_t (_image, _hMap, _rect, _position)


# Отобразить объект поверх карты местности в буфере объектов образа окна карты
# himage  - идентификатор буфера окна
# hMap - идентификатор открытых данных
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# object - идентификатор описания объекта в памяти
# При ошибке возвращает ноль

    mapDrawImageMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageMapObject(_himage: maptype.HIMAGE, _hMap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ) -> int:
        return mapDrawImageMapObject_t (_himage, _hMap, _parm, _object)



# Отобразить объект поверх карты местности в буфере объектов образа окна карты c учетом
# заданного сдвига метрики
# himage  - идентификатор буфера окна
# hMap - идентификатор открытых данных
# offset - величина смещения изображения объекта в буфере от его реальных
#          координат в метрах в текущей системе координат документа
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# object - идентификатор описания объекта в памяти
# При ошибке возвращает ноль

    mapDrawImageOffsetMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageOffsetMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageOffsetMapObject(_himage: maptype.HIMAGE, _hMap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _object: maptype.HOBJ) -> int:
        return mapDrawImageOffsetMapObject_t (_himage, _hMap, _offset, _parm, _object)


# Отобразить объект поверх карты местности в буфере образа окна карты
# himage  - идентификатор буфера окна
# hMap - идентификатор открытых данных
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# data - список координат объекта в системе координат, заданной параметром place
# place - вид системы координат (в точках экрана - PP_PICTURE, в метрах в
#         системе координат документа - PP_PLANE, в радианах на эллипсоиде документа - PP_GEO)
# При ошибке возвращает ноль

    mapDrawImageUserObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_int)
    def mapDrawImageUserObject(_himage: maptype.HIMAGE, _hMap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapDrawImageUserObject_t (_himage, _hMap, _parm, _data, _place)


# Отобразить объект поверх карты местности в буфере образа окна карты c учетом
# заданного сдвига метрики
# himage  - идентификатор буфера окна
# hMap - идентификатор открытых данных
# offset - величина смещения изображения объекта в буфере от его реальных
#          координат в системе координат, заданной параметром place
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# data - список координат объекта в системе координат, заданной параметром place
# place - вид системы координат (в точках экрана - PP_PICTURE, в метрах в
#         системе координат документа - PP_PLANE, в радианах на эллипсоиде документа - PP_GEO)
# При ошибке возвращает ноль

    mapDrawImageOffsetUserObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageOffsetUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_int)
    def mapDrawImageOffsetUserObject(_himage: maptype.HIMAGE, _hMap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapDrawImageOffsetUserObject_t (_himage, _hMap, _offset, _parm, _data, _place)


# Отобразить графические данные в буфере образа окна карты
# hScreen  - идентификатор образа экрана
# points   - координаты в пикселах
# count    - число координат
# image    - тип графического примитива (см. mapgdi.h)
# parm     - параметры графического примитива
# При ошибке возвращает ноль

    mapDrawImageGraphics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageGraphics', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def mapDrawImageGraphics(_image: maptype.HIMAGE, _hMap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _type: int, _parm: ctypes.c_char_p) -> int:
        return mapDrawImageGraphics_t (_image, _hMap, _points, _count, _type, _parm)


# Отобразить текстовую строку (Arial)
# image    - идентификатор образа экрана
# points   - координаты в пикселах
# count    - число координат
# text     - текст подписи
# height   - высота подписи в мкм
# color    - цвет подписи RGB
# align    - флажки выравнивания текста (для -1 - FA_BASELINE|FA_LEFT)
# При ошибке возвращает ноль

    mapDrawImageTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageTextUn', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapDrawImageTextUn(_image: maptype.HIMAGE, _hMap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _text: mapsyst.WTEXT, _height: int, _color: int, _align: int) -> int:
        return mapDrawImageTextUn_t (_image, _hMap, _points, _count, _text.buffer(), _height, _color, _align)


# Отобразить BMP в образ экрана
# image     - идентификатор образа экрана
# point     - координаты в пикселах
# bmpmemory - адрес массива байт, содержащего образ BMP-файла
# transparent - цвет RGB, который не должен отображаться
# При ошибке возвращает ноль

    mapDrawImageBitMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImageBitMap', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_char_p, ctypes.c_int)
    def mapDrawImageBitMap(_image: maptype.HIMAGE, _hMap: maptype.HMAP, _point: ctypes.POINTER(maptype.DRAWPOINT), _bmpmemory: ctypes.c_char_p, _transparent: int) -> int:
        return mapDrawImageBitMap_t (_image, _hMap, _point, _bmpmemory, _transparent)


# Включить отображение выделенных объектов и обновить буфер выделенных объектов
# При дальнешем обновлении буфера карты (Map) буфер выделенных объектов будет тоже обновляться
# Если выделение объектов не установлено (mapGetTotalSelectFlag() возвращает ноль) -
# буфер выделенных объектов автоматически закроется, а функия отображения вернет ноль
# image     - идентификатор образа экрана
# selectcolor - цвет выделения объектов на фоне карты (RGB)
# При ошибке возвращает ноль

    mapDrawTotalSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawTotalSelect', maptype.HIMAGE, maptype.HMAP, ctypes.c_int)
    def mapDrawTotalSelect(_image: maptype.HIMAGE, _hMap: maptype.HMAP, _selectcolor: int) -> int:
        return mapDrawTotalSelect_t (_image, _hMap, _selectcolor)


# Запросить базовый масштаб карты
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetMapScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapScale', maptype.HMAP)
    def mapGetMapScale(_hmap: maptype.HMAP) -> int:
        return mapGetMapScale_t (_hmap)


# Запросить название карты в формате UNICODE
# name - строка в кодировке UNICODE (2 байта на символ)
# size - размер строки в байтах
# При ошибке возвращает пустую строку

    mapGetMapNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapNameUn_t (_hMap, _name.buffer(), _size)


# Запросить полный путь к паспорту главной карты в формате UNICODE
# (функция вызывает mapGetMainMapName)
# hmap - идентификатор открытых данных
# При ошибке возвращает 0

    mapGetMapPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapPathUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapPathUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapPathUn_t (_hmap, _name.buffer(), _size)


# Запросить паспортные данные векторной карты
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# hmap - идентификатор открытых данных
# sheetnumber - номер листа карты для
# которого запрашиваются паспортные данные
# При ошибке возвращает ноль

    mapGetMapInfoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapInfoPro', maptype.HMAP, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapGetMapInfoPro(_hmap: maptype.HMAP, _sheetnumber: int, _map: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        return mapGetMapInfoPro_t (_hmap, _sheetnumber, _map, _sheet, _sheetnames)


# Запросить паспортные данные векторной карты по имени файла - паспорта карты
# name    - имя файла паспорта карты (MAP,SIT,SITX)
# sheetnumber - номер листа карты, для которого запрашиваются паспортные данные
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
# При ошибке возвращает ноль,
# иначе - число объектов на листе карты (если нет объектов, то возвращает -1)

    mapGetMapInfoByNameMeta_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapInfoByNameMeta', maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.METAINFO))
    def mapGetMapInfoByNameMeta(_name: mapsyst.WTEXT, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _metainfo: ctypes.POINTER(mapcreat.METAINFO)) -> int:
        return mapGetMapInfoByNameMeta_t (_name.buffer(), _sheetnumber, _mapreg, _sheet, _metainfo)

    mapGetMapInfoByNamePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapInfoByNamePro', maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetMapInfoByNamePro(_name: mapsyst.WTEXT, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _rscname: mapsyst.WTEXT, _rsize: int, _sheetname: mapsyst.WTEXT, _ssize: int, _securitycode: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetMapInfoByNamePro_t (_name.buffer(), _sheetnumber, _mapreg, _sheet, _rscname.buffer(), _rsize, _sheetname.buffer(), _ssize, _securitycode)


# Контроль номенклатуры карты
# nomenclature - строка с номенклатурой
# length - длина строки
# type - тип карты (из MAPTYPE)
# scale - масштаб  (1000000,500000,200000 и т.д.
#                   соответствующий типу карты)
# При ошибке возвращает ноль

    mapCheckNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckNomenclatureUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapCheckNomenclatureUn(_nomenclature: mapsyst.WTEXT, _type: int, _scale: int) -> int:
        return mapCheckNomenclatureUn_t (_nomenclature.buffer(), _type, _scale)


# Формирование имени файла по номенклатуре (удаляет точки, пробелы, -)
# filename - буфер для имени файла
# namesize - размер буфера в БАЙТАХ
# nomenclature - номенклатура листа
# При ошибке возвращает ноль

    mapSetFileNameFromNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFileNameFromNomenclatureUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def mapSetFileNameFromNomenclatureUn(_filename: mapsyst.WTEXT, _namesize: int, _nomenclature: mapsyst.WTEXT) -> int:
        return mapSetFileNameFromNomenclatureUn_t (_filename.buffer(), _namesize, _nomenclature.buffer())


# Расчет данных на лист топографической карты (СК-42, СК-95, UTM и т.п.)
# hmap - идентификатор открытых данных или ноль
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# Входные данные заполняются в mapreg: тип карты, масштаб,
# в sheet: номенклатура
# Выходные данные заполняются в mapreg: осевой меридиан,
# в sheet: геодезические координаты, прямоугольные координаты, сближение меридианов
# Если mapreg и sheet заполняются для создания карты (самый первый лист), то hmap равно 0
# Если mapreg заполняется для добавления листа в карту, то hmap не равно 0
# При ошибке возвращает ноль

    mapCalcTopographicSheetEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCalcTopographicSheetEx', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapCalcTopographicSheetEx(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapCalcTopographicSheetEx_t (_hmap, _mapreg, _sheet)


# Рассчитать осевой меридиан (от 0 до 360) по номенклатуре топокарты
# type - тип карты (TOPOGRAPHIC, CK_95, GCK_2011, Pulkovo2017 ...)
# nomenclature - номенклатура листа
# При ошибке возвращает 0

    mapGetAxisMeridianFromNomenclatureEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianFromNomenclatureEx', ctypes.c_int, ctypes.c_char_p)
    def mapGetAxisMeridianFromNomenclatureEx(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        return mapGetAxisMeridianFromNomenclatureEx_t (_type, _nomenclature)


# Рассчитать масштаб топокарты по номенклатуре
# type - тип карты (TOPOGRAPHIC, CK_95, GCK_2011, Pulkovo2017 ...)
# nomenclature - номенклатура листа
# При ошибке возвращает 0

    mapGetTopoScaleByNomenclature_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTopoScaleByNomenclature', ctypes.c_int, ctypes.c_char_p)
    def mapGetTopoScaleByNomenclature(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        return mapGetTopoScaleByNomenclature_t (_type, _nomenclature)


# Рассчитать осевой меридиан топокарты по долготе

    mapGetAxisMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridian', ctypes.c_double)
    def mapGetAxisMeridian(_longitude: float) -> float:
        return mapGetAxisMeridian_t (_longitude)


# Запросить признак повышенной точности хранения координат
# hmap -  идентификатор открытых данных
# Возвращает значения:
# 1 - максимальная точность хранения (метры или радианы),
# 2 - с точностью 2 знака (сантиметры),
# 3 - с точностью 3 знака (миллиметры)
# При ошибке или нормальной точности хранения координат возвращает ноль

    mapGetMapPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapPrecision', maptype.HMAP)
    def mapGetMapPrecision(_hmap: maptype.HMAP) -> int:
        return mapGetMapPrecision_t (_hmap)


# Запросить количество эллипсоидов в списке

    mapGetEllipsoidCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidCount')
    def mapGetEllipsoidCount() -> int:
        return mapGetEllipsoidCount_t ()


# Запросить название эллипсоида по коду
# Параметры  code  - код эллипсоида
#            name  - адрес строки для размещения названия эллипсоида
#            size  - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0
# name содержит значение "Не установлено"

    mapGetEllipsoidNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidNameByCodeUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetEllipsoidNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetEllipsoidNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия эллипсоида по номеру в таблице
# Параметры  number  - номер строки таблицы эллипсоидов (номер начинается с 1)
#            code    - код эллипсоида
#            name    - адрес строки для размещения названия эллипсоида
#            size    - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0

    mapGetEllipsoidByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidByNumberUn', ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def mapGetEllipsoidByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_int), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetEllipsoidByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запросить по коду EPSG номер эллипсоида (см. MAPCREAT.H)
# для заполнения структуры MAPREGISTEREX
# code - код EPSG
# При ошибке возвращает ноль

    mapGetEllipsoidByEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidByEPSGCode', ctypes.c_int)
    def mapGetEllipsoidByEPSGCode(_code: int) -> int:
        return mapGetEllipsoidByEPSGCode_t (_code)


# Запросить код EPSG эллипсоида по его коду (см. MAPCREAT.H)
# ellipsoid - номер эллипсоида (см. MAPCREAT.H, ELLIPSOIDKIND)
# При ошибке возвращает ноль

    mapGetEllipsoidEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidEPSGCode', ctypes.c_int)
    def mapGetEllipsoidEPSGCode(_code: int) -> int:
        return mapGetEllipsoidEPSGCode_t (_code)


# Запрос количества типов карт в списке

    mapGetMapTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapTypeCount')
    def mapGetMapTypeCount() -> int:
        return mapGetMapTypeCount_t ()


# Запрос названия типа карты по коду
# Параметры  code  - код типа карты
#            name  - адрес строки для размещения названия типа карты
#            size  - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0
# name содержит значение "Не установлено"

    mapGetMapTypeByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapTypeByCodeUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapTypeByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapTypeByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия типа карты по номеру в таблице
# Параметры  number  - номер строки таблицы типа карты (номер начинается с 1)
#            code    - код типа карты
#            name    - адрес строки для размещения названия типа карты
#            size    - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0

    mapGetMapTypeByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapTypeByNumberUn', ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def mapGetMapTypeByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_int), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapTypeByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запрос количества проекций в списке
# При ошибке возвращает 0

    mapGetProjectionCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProjectionCount')
    def mapGetProjectionCount() -> int:
        return mapGetProjectionCount_t ()


# Запрос названия проекции по коду
# Параметры  code  - код проекции
#            name  - адрес строки для размещения названия проекции
#            size  - длина выделенной области под строку в байтах
# При ошибке возвращает 0
# name содержит значение "Не установлено"

    mapGetProjectionNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProjectionNameByCodeUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetProjectionNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetProjectionNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия проекции по номеру в таблице
# Параметры  number  - номер строки таблицы проекций (номер начинается с 1)
#            code    - код проекции
#            name    - адрес строки для размещения названия проекции
#            size    - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0

    mapGetProjectionByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetProjectionByNumberUn', ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def mapGetProjectionByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_int), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetProjectionByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запрос количества систем высот в списке

    mapGetHeightSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightSystemCount')
    def mapGetHeightSystemCount() -> int:
        return mapGetHeightSystemCount_t ()


# Запрос названия системы высот по коду
# Параметры  code  - код системы высот
#            name  - адрес строки для размещения названия системы высот
#            size  - длина выделенной области под строку в байтах
# При ошибке возвращает 0
# name содержит значение "Не установлено"

    mapGetHeightSystemNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightSystemNameByCodeUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetHeightSystemNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetHeightSystemNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия системы высот по номеру в таблице
# Параметры  number  - номер строки таблицы систем высот (номер начинается с 1)
#            code    - код системы высот
#            name    - адрес строки для размещения названия проекции
#            size    - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает 0

    mapGetHeightSystemByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightSystemByNumberUn', ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR, ctypes.c_int)
    def mapGetHeightSystemByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_int), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetHeightSystemByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запросить число слоев на карте
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayerCount', maptype.HMAP)
    def mapGetLayerCount(_hmap: maptype.HMAP) -> int:
        return mapGetLayerCount_t (_hmap)


# Запросить название слоя по его номеру (number)
# hmap - идентификатор открытых данных
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# Номер первого слоя 0
# При ошибке возвращает ноль

    mapGetLayerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayerNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetLayerNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetLayerNameUn_t (_hmap, _number, _name.buffer(), _size)


# Определить собственный номер листа по заданным координатам (x,y).
# Система координат задана переменной place.
# Если лист не найден - возвращает ноль.
# Если в одной точке несколько листов :
# hmap - идентификатор открытых данных
# number - порядковый номер листа в перекрытии (начина с 1).
# Поиск всегда дает одинаковый порядок листов
# При ошибке возвращает ноль

    mapWhatListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhatListNumber', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapWhatListNumber(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int) -> int:
        return mapWhatListNumber_t (_hmap, _x, _y, _number, _place)


# Запросить номенклатуру листа по заданным координатам (x,y).
# hmap - идентификатор открытых данных
# name - адрес буфера для результата запроса
# size - размер буфера
# Система координат задана переменной place.
# Если лист не найден - возвращает ноль

    mapWhatListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhatListNameUn', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapWhatListNameUn(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapWhatListNameUn_t (_hmap, _x, _y, _number, _place, _name.buffer(), _size)


# Запросить имя листа по его номеру (number)
# hmap - идентификатор открытых данных
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetSheetNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSheetNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSheetNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetSheetNameUn_t (_hmap, _number, _name.buffer(), _namesize)


# Запросить номенклатуру листа по его номеру (number)
# hmap - идентификатор открытых данных
# name - адрес буфера для результата запроса
# size - размер буфера
# При ошибке возвращает ноль

    mapGetListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListNameUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetListNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetListNameUn_t (_hmap, _number, _name.buffer(), _size)


# Запросить общее число листов в районе
# hmap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapGetListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListCount', maptype.HMAP)
    def mapGetListCount(_hmap: maptype.HMAP) -> int:
        return mapGetListCount_t (_hmap)


# Запросить общее число объектов в листе
# hmap - идентификатор открытых данных
# list - номер листа
# При ошибке возвращает ноль

    mapGetObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectCount', maptype.HMAP, ctypes.c_int)
    def mapGetObjectCount(_hmap: maptype.HMAP, _list: int) -> int:
        return mapGetObjectCount_t (_hmap, _list)


# Запросить общее число объектов в листе, исключая удаленные
# number - номер листа
# При ошибке возвращает ноль

    mapGetRealObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRealObjectCount', maptype.HMAP, ctypes.c_int)
    def mapGetRealObjectCount(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetRealObjectCount_t (_hMap, _number)


# Запросить номер листа по его номенклатуре
# hmap - идентификатор открытых данных
# name - имя листа
# При ошибке возвращает ноль

    mapGetListNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetListNumberByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetListNumberByNameUn_t (_hMap, _name.buffer())


# Определить по номенклатуре листа его принадлежность карте
# hmap - идентификатор открытых данных
# listname - имя листа (номенклатура)
# Возвращает номер карты в цепочке карт,которой принадлежит
# лист по имени listname
# (0-фоновая карта, 1-первая пользовательская карта и т.д.)
# При ошибке возвращает "-1"

    mapWhatListLayoutIsUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWhatListLayoutIsUn', maptype.HMAP, maptype.PWCHAR)
    def mapWhatListLayoutIsUn(_hMap: maptype.HMAP, _listname: mapsyst.WTEXT) -> int:
        return mapWhatListLayoutIsUn_t (_hMap, _listname.buffer())


# Запросить объект "Рамка листа"
# hmap - идентификатор открытых данных
# list - номер листа (c 1)
# info - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListFrameObject', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapGetListFrameObject(_hmap: maptype.HMAP, _list: int, _info: maptype.HOBJ) -> int:
        return mapGetListFrameObject_t (_hmap, _list, _info)


# Запросить габариты объекта "Рамка листа" (если рамки нет -
# заполняются по габаритам из паспорта)
# hmap  - идентификатор открытых данных
# list  - номер листа
# frame - указатель на габариты листа в метрах
# При ошибке возвращает ноль

    mapGetListFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListFrame', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def mapGetListFrame(_hmap: maptype.HMAP, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetListFrame_t (_hmap, _list, _frame)


# Создать объект "Рамка листа"
# hmap - идентификатор открытых данных
# list - последовательный номер листа карты (c 1)
# info - идентификатор объекта карты в памяти
# HOBJ должен быть создан вызовом mapCreateObject
# при успешном выполнении HOBJ будет содержать созданную
# или существующую рамку листа
# Для пользовательской карты рамка создается, но не записывается
# Для карты местности созданная рамка сохраняется на карте
# При ошибке возвращает ноль

    mapCreateListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateListFrameObject', maptype.HMAP, ctypes.c_int, maptype.HOBJ)
    def mapCreateListFrameObject(_hmap: maptype.HMAP, _list: int, _info: maptype.HOBJ) -> int:
        return mapCreateListFrameObject_t (_hmap, _list, _info)


# Установить ограничение на число листов, открытых одновременно
# Применяется при работе с многолистовыми картами местности в
# ограниченной области памяти
# hmap - идентификатор открытых данных
# islimited - признак установки ограничения числа открытых листов,
# обычно от 8 до 32, но не менее числа потоков, обрабатывающих листы параллельно
# При ошибке возвращает ноль

    mapSetActiveListCountLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveListCountLimit', maptype.HMAP, ctypes.c_int)
    def mapSetActiveListCountLimit(_hmap: maptype.HMAP, _islimited: int = 32) -> int:
        return mapSetActiveListCountLimit_t (_hmap, _islimited)


# Установить ограничение на размер используемой памяти
# Применяется при работе с большими многолистовыми картами
# hmap - идентификатор открытых данных
# limit - размер разрешенной к использованию памяти
# Если лимит больше доступной приложению памяти,
# устанавливается доступный объем физической памяти
# Если лимит меньше 200 Мб, то устанавливается 200 Мб
# При ошибке возвращает 0

    mapSetMemoryLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapSetMemoryLimit', maptype.HMAP, ctypes.c_ulong)
    def mapSetMemoryLimit(_hmap: maptype.HMAP, _limit: int) -> int:
        return mapSetMemoryLimit_t (_hmap, _limit)


# Запросить габариты района (всех видов карт)
# hmap - идентификатор открытых данных
# dframe - указатель на заполняемую структуру
# Запрашиваются координаты углов района в метрах или радианах на местности
# в картографической системе или в пикселах относительно верхнего левого угла
# района
# place  - запрашиваемая система координат (PP_PICTURE, PP_PLANE, PP_GEO)
# При ошибке возвращает ноль

    mapGetTotalBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetTotalBorder(_hmap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetTotalBorder_t (_hmap, _dframe, _place)


# Запросить габариты района (всех видов карт) в системе координат,
# заданной кодом EPSG, в метрах и радианах на местности
# hmap - идентификатор открытых данных
# dframeplane - указатель на заполняемую структуру в метрах
# dframegeo   - указатель на заполняемую структуру в радианах
# epsgcode    - код системы координат (3395, 3857, 4326 и т.д.)
# При ошибке возвращает ноль

    mapGetTotalBorderByEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalBorderByEPSG', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetTotalBorderByEPSG(_hmap: maptype.HMAP, _dframeplane: ctypes.POINTER(maptype.DFRAME), _dframegeo: ctypes.POINTER(maptype.DFRAME), _epsgcode: int) -> int:
        return mapGetTotalBorderByEPSG_t (_hmap, _dframeplane, _dframegeo, _epsgcode)


# Преобразование из пикселов в изображении в координаты на местности в метрах
# hmap - идентификатор открытых данных
# x,y  - преобразуемые координаты

    mapPictureToPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPictureToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPictureToPlane(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapPictureToPlane_t (_hmap, _x, _y)


# Преобразование из метров на местности в пикселы на
# изображении
# hmap - идентификатор открытых данных
# x,y  - преобразуемые координаты

    mapPlaneToPicture_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPlaneToPicture', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPicture(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapPlaneToPicture_t (_hmap, _x, _y)

    mapPlaneToPicturePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPlaneToPicturePro', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapPlaneToPicturePro(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _hPaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapPlaneToPicturePro_t (_x, _y, _hPaint)


# Преобразование из метров на местности в геодезические
# координаты в радианах в соответствии с проекцией карты
# (поддерживаетс не для всех карт !)
# Применение :
# if (mapIsGeoSupported())   |  или :
#   {                        |  if (mapIsGeoSupported())
#     B = Xmet; L = Ymet;    |    {
#     mapPlan2Geo(B,L);      |      mapPlan2Geo(B=Xmet,L=Ymet);
#   }                        |    }
# hmap - идентификатор открытых данных
# Bx,Ly  - преобразуемые координаты
# на входе метры, на выходе - радианы
# При ошибке возвращает 0

    mapPlaneToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeo(_hmap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToGeo_t (_hmap, _Bx, _Ly)


# Преобразование из геодезических координат в радианах
# в метры на местности в соответствии с проекцией карты
# (поддерживается не для всех карт !)
# hmap - идентификатор открытых данных
# Bx,Ly  - преобразуемые координаты
# на входе радианы, на выходе - метры
# При ошибке возвращает 0

    mapGeoToPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToPlane(_hmap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToPlane_t (_hmap, _Bx, _Ly)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hmap - идентификатор открытых данных
# Если нет - возвращает ноль

    mapIsGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsGeoSupported', maptype.HMAP)
    def mapIsGeoSupported(_hmap: maptype.HMAP) -> int:
        return mapIsGeoSupported_t (_hmap)


# Преобразование из метров на местности (проекция карты)
# в геодезические координаты в радианах (общеземной эллипсоид WGS84)
# (поддерживается не для всех карт !)
# Наличие высоты повышает точность расчетов,
# функция mapPlaneToGeoWGS84() пытается
# определить высоту из матрицы
# Применение :
# if (mapIsGeoSupported())
#   {
#     B = Xmet; L = Ymet;
#     mapPlaneToGeoWGS84(hMap,B,L);
#   }
# hmap  - идентификатор открытых данных
# Bx,Ly - преобразуемые координаты
# на входе метры, на выходе - радианы
# H     - НОРМАЛЬНАЯ высота в точке (метры), не пересчитывается
# При ошибке возвращает 0

    mapPlaneToGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToGeoWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeoWGS84(_hmap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToGeoWGS84_t (_hmap, _Bx, _Ly)

    mapPlaneToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToGeoWGS843D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeoWGS843D(_hmap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToGeoWGS843D_t (_hmap, _Bx, _Ly, _H)


# Преобразование нормальной высоты (MSL) к геодезической (WGS84)
# B,L   - геодезические координаты (WGS-84) в радианах для точки, в которой пересчитывается высота
# hegm  - идентификатор модели геоида, открытой mapOpenEgmPro
# H     - высота в метрах
# При ошибке возвращает ноль

    mapNormalHeightToGeoHeightWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapNormalHeightToGeoHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapNormalHeightToGeoHeightWGS84(_B: float, _L: float, _H: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapNormalHeightToGeoHeightWGS84_t (_B, _L, _H, _hegm)


# Преобразование геодезической (WGS84) высоты к нормальной (MSL)
# B,L   - геодезические координаты (WGS84) в радианах для точки, в которой пересчитывается высота
# hegm  - идентификатор модели геоида, открытой mapOpenEgmPro
# H     - высота в метрах
# При ошибке возвращает ноль

    mapGeoHeightToNormalHeightWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoHeightToNormalHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoHeightToNormalHeightWGS84(_B: float, _L: float, _H: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapGeoHeightToNormalHeightWGS84_t (_B, _L, _H, _hegm)


# Преобразование координат из геодезической системы координат карты к
# геоцентрической системе координат для эллипсоида WGS84
# (поддерживается не для всех карт !)
# Bx,Ly,H  - преобразуемые координаты
# на входе радианы, на выходе - метры в геоцентрической системе
# H - геодезическая высота (WGS84), преобразуется в геоцентрическую координату
# Преобразование нормальной высоты к геодезической выполняет mapNormalHeightToGeoHeightWGS84
# или mapUserPlaneToGeoWGS84Pro
# При ошибке возвращает ноль

    mapGeoToXYZWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToXYZWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZWGS84(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToXYZWGS84_t (_hMap, _Bx, _Ly, _H)


# Преобразование координат из геодезической системы координат карты к
# геоцентрической системе координат
# (поддерживается не для всех карт !)
# Bx,Ly,H  - преобразуемые координаты
# на входе радианы, на выходе - метры в геоцентрической системе
# H - геодезическая высота, преобразуется в геоцентрическую координату
# При ошибке возвращает ноль

    mapGeoToXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToXYZ', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZ(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToXYZ_t (_hMap, _Bx, _Ly, _H)


# Преобразование координат из геоцентрической системы координат для WGS84 к
# геодезической системе координат карты
# (поддерживается не для всех карт !)
# Bx,Ly,H  - преобразуемые координаты
# на входе метры в геоцентрической системе, на выходе - радианы
# H - геоцентрическая координата, преобразуется в геодезическую высоту WGS84
# Преобразование геодезической высоты к нормальной выполняет mapGeoHeightToNormalHeightWGS84
# При ошибке возвращает ноль

    mapXYZWGS84ToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapXYZWGS84ToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToGeo(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZWGS84ToGeo_t (_hMap, _Bx, _Ly, _H)


# Преобразование координат из геоцентрической системы координат карты к
# геодезической системе координат
# (поддерживается не для всех карт !)
# Bx,Ly,H  - преобразуемые координаты
# на входе метры в геоцентрической системе, на выходе - радианы
# H - геоцентрическая координата, преобразуется в геодезическую высоту
# При ошибке возвращает ноль

    mapXYZToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapXYZToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZToGeo(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZToGeo_t (_hMap, _Bx, _Ly, _H)


# Пересчет геоцентрических координат по заданным параметрам преобразования
# между ними
# Обратное преобразование Гельмерта, или Coordinate Frame Rotation, EPSG:1032
# Знаки числовых значений должны быть заданы с учетом направления преобразования
# X, Y, Z - преобразуемые геоцентрические координаты в метрах
# При ошибке возвращает ноль

    mapTransformXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTransformXYZ', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM))
    def mapTransformXYZ(_X: ctypes.POINTER(ctypes.c_double), _Y: ctypes.POINTER(ctypes.c_double), _Z: ctypes.POINTER(ctypes.c_double), _datum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM)) -> int:
        return mapTransformXYZ_t (_X, _Y, _Z, _datum)


# Преобразование координат из геодезической системы координат карты к
# в геодезические координаты (общеземной эллипсоид WGS84)
# (поддерживается не для всех карт !)
# Bx,Ly - координаты в радианах
# H     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает ноль

    mapGeoToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToGeoWGS843D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToGeoWGS843D(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToGeoWGS843D_t (_hMap, _Bx, _Ly, _H)


# Преобразование координат из геодезической системы координат в радианах
# (общеземной эллипсоид WGS84) в геодезическую систему координат карты
# (поддерживается не для всех карт !)
# Bx,Ly - координаты в радианах
# H     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает ноль

    mapGeoWGS84ToGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToGeo3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToGeo3D(_hMap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToGeo3D_t (_hMap, _Bx, _Ly, _H)


# Преобразование из геодезических координат в радианах
# (общеземной эллипсоид WGS84)
# в метры на местности в проекции карты
# (поддерживается не для всех карт !)
# hmap  - идентификатор открытых данных
# Bx,Ly - преобразуемые координаты, на входе радианы, на выходе - метры
# H     - НОРМАЛЬНАЯ высота в точке (метры), не пересчитывается
# При ошибке возвращает ноль

    mapGeoWGS84ToPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToPlane3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToPlane3D(_hmap: maptype.HMAP, _Bx: ctypes.POINTER(ctypes.c_double), _Ly: ctypes.POINTER(ctypes.c_double), _H: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToPlane3D_t (_hmap, _Bx, _Ly, _H)


# Преобразование набора точек из одной системы
# координат в другую
# hmap  - идентификатор открытых данных
# src,tag - указатели на области размещения точек,
# могут указывать на одну и ту же область памяти;
# source,target - типы входной и выходной метрики (PP_MAP,PP_PLANE ...);
# count - число преобразуемых точек.
# Пересчет связанный с геодезическими координатами
# будет выполняться только,если IsGeoSupported() != 0.

    mapTransformPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapTransformPoints', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapTransformPoints(_hmap: maptype.HMAP, _src: ctypes.POINTER(maptype.DOUBLEPOINT), _source: int, _tag: ctypes.POINTER(maptype.DOUBLEPOINT), _target: int, _count: int) -> ctypes.c_void_p:
        return mapTransformPoints_t (_hmap, _src, _source, _tag, _target, _count)


# Преобразование координат из градусов в радианы
# (для положительного значения)
# degree - структура, содержащая координаты в градусах, минутах,
# секундах. Описана в maptype.h
# radian - значение в радианах

    mapDegreeToRadian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDegreeToRadian', ctypes.POINTER(maptype.GEODEGREE), ctypes.POINTER(ctypes.c_double))
    def mapDegreeToRadian(_degree: ctypes.POINTER(maptype.GEODEGREE), _radian: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapDegreeToRadian_t (_degree, _radian)


# Преобразование координат из радиан в градусы
# (для положительного значения)
# radian - значение в радианах
# degree - структура, содержащая координаты в градусах, минутах,
# секундах. Описана в maptype.h

    mapRadianToDegree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapRadianToDegree', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.GEODEGREE))
    def mapRadianToDegree(_radian: ctypes.POINTER(ctypes.c_double), _degree: ctypes.POINTER(maptype.GEODEGREE)) -> ctypes.c_void_p:
        return mapRadianToDegree_t (_radian, _degree)


# Преобразование координат из градусов в радианы с учетом знака
# degree - структура, содержащая координаты в градусах, минутах,
# секундах. Описана в maptype.h
# radian - значение в радианах

    mapSignDegreeToRadian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSignDegreeToRadian', ctypes.POINTER(maptype.SIGNDEGREE), ctypes.POINTER(ctypes.c_double))
    def mapSignDegreeToRadian(_degree: ctypes.POINTER(maptype.SIGNDEGREE), _radian: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapSignDegreeToRadian_t (_degree, _radian)


# Преобразование координат из радиан в градусы со знаком
# radian - значение в радианах
# degree - структура, содержащая координаты в градусах, минутах,
# секундах. Описана в maptype.h

    mapRadianToSignDegree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapRadianToSignDegree', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.SIGNDEGREE))
    def mapRadianToSignDegree(_radian: ctypes.POINTER(ctypes.c_double), _degree: ctypes.POINTER(maptype.SIGNDEGREE)) -> ctypes.c_void_p:
        return mapRadianToSignDegree_t (_radian, _degree)


# Вычисление осевого маридиана по номеру зоны для топокарт системы 42 года
# zone - номер зоны системы 42 года
# При ошибке возвращает ноль

    mapGetAxisMeridianByZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianByZone', ctypes.c_int)
    def mapGetAxisMeridianByZone(_zone: int) -> float:
        return mapGetAxisMeridianByZone_t (_zone)


# Вычисление осевого маридиана по номеру зоны для топокарт UTM
# zone - номер зоны UTM
# При ошибке возвращает ноль

    mapGetAxisMeridianByUTMZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianByUTMZone', ctypes.c_int)
    def mapGetAxisMeridianByUTMZone(_zone: int) -> float:
        return mapGetAxisMeridianByUTMZone_t (_zone)


# Вычисление номера зоны по геодезической долготе в радианах
# (меридиану) для топокарт системы 42 года
# meridian - значение меридиана в радианах
# При ошибке возвращает ноль

    mapGetZoneByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetZoneByMeridian', ctypes.c_double)
    def mapGetZoneByMeridian(_meridian: float) -> int:
        return mapGetZoneByMeridian_t (_meridian)


# Вычисление номера зоны UTM по геодезической долготе в радианах
# meridian - значение меридиана в радианах
# При ошибке возвращает ноль

    mapGetUTMZoneByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetUTMZoneByMeridian', ctypes.c_double)
    def mapGetUTMZoneByMeridian(_meridian: float) -> int:
        return mapGetUTMZoneByMeridian_t (_meridian)


# Заполнение осевого меридиана по геодезической долготе в
# радианах для топографических карт
# hmap - идентификатор открытых данных
# meridian - значение меридиана в радианах
# Не рекомендуется применять для карт уже содержащих объекты
# При ошибке возвращает ноль

    mapSetAxisMeridianByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAxisMeridianByMeridian', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByMeridian(_hmap: maptype.HMAP, _meridian: float) -> int:
        return mapSetAxisMeridianByMeridian_t (_hmap, _meridian)


# Заполнение осевого меридиана по координате Y для
# топографических карт системы 42 года
# Не рекомендуется применять для карт уже содержащих объекты
# hmap  - идентификатор открытых данных
# y     - координата Y в метрах произвольной точки,
#         попадающей на заданный лист
# При ошибке возвращает ноль

    mapSetAxisMeridianByPlaneY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAxisMeridianByPlaneY', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByPlaneY(_hmap: maptype.HMAP, _y: float) -> int:
        return mapSetAxisMeridianByPlaneY_t (_hmap, _y)


# Запросить параметры эллипсоида по его номеру (см. MAPCREAT.H)
# ellipsoid - номер эллипсоида (см. MAPCREAT.H, ELLIPSOIDKIND)
# parm      - параметры заданного эллипсоида
# При ошибке возвращает ноль

    mapGetEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEllipsoidParameters', ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetEllipsoidParameters(_ellipsoid: int, _parm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetEllipsoidParameters_t (_ellipsoid, _parm)


# Установить текущие параметры пользовательской системы координат
# parm      - параметры рабочей системы координат (см. MAPCREAT.H)
# datum     - параметры пересчета с эллипсоида рабочей системы координат к WGS84 (datum может быть 0)
# ellipsoid - параметры пользовательского эллипсоида для рабочей
#             системы координат, только когда поле EllipsoidKind в
#             MAPREGISTEREX равно USERELLIPSOID (ellipsoid может быть 0)
# ttype     - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm     - параметры локального преобразования координат (см. mapcreat.h)
# code      - код EPSG (для Широта\Долгота на WGS84: 4326),
#             для СК-42 зоны 1-60: 28401-28460, для СК-95 зоны 1-60: 20001-20060
#             для UTM на WGS84 зоны 1-60: 32601-32660
#             для Гаусса-Крюгера на ПЗ-90.11 зоны 1-60: 80011001-80011060
#             для ГСК-2011 зоны 1-60: 80201101-80201160
# Возвращает идентификатор пользовательской системы координат
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCreateUserSystemParametersPro(_parm: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersPro_t (_parm, _datum, _ellipsoid, _ttype, _tparm)

    mapCreateUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParameters', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateUserSystemParameters(_parm: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> ctypes.c_void_p:
        return mapCreateUserSystemParameters_t (_parm, _datum, _ellipsoid)

    mapCreateUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByEpsg', ctypes.c_int)
    def mapCreateUserSystemParametersByEpsg(_code: int) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByEpsg_t (_code)


# Установить текущие параметры пользовательской системы координат
# по текущим параметрам документа (их можно запросить через mapGetDocProjectionPro)
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersByDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByDoc', maptype.HMAP)
    def mapCreateUserSystemParametersByDoc(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByDoc_t (_hmap)


# Установить текущие параметры пользовательской системы координат
# по записи параметров в XML (их можно запросить через mapGetUserSystemXmlNode)
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersByXmlNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByXmlNode', ctypes.c_char_p)
    def mapCreateUserSystemParametersByXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByXmlNode_t (_point)


# Освободить ресурсы пользовательской системы координат

    mapDeleteUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteUserSystemParameters', ctypes.c_void_p)
    def mapDeleteUserSystemParameters(_huser: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapDeleteUserSystemParameters_t (_huser)


# Запросить текущие параметры пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# parm      - параметры рабочей системы координат (см. MAPCREAT.H)
# datum     - параметры пересчета с эллипсоида рабочей системы координат к WGS84 (datum может быть 0)
# ellipsoid - параметры пользовательского эллипсоида для рабочей
#             системы координат, только когда поле EllipsoidKind в
#             MAPREGISTEREX равно USERELLIPSOID (ellipsoid может быть 0)
# ttype     - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm     - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapGetUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetUserSystemParameters', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetUserSystemParameters(_huser: ctypes.c_void_p, _parm: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetUserSystemParameters_t (_huser, _parm, _datum, _ellipsoid, _ttype, _tparm)


# Изменить текущие параметры пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# code  - код EPSG (4326 - WGS84),
#         для СК-42 зоны 1-60 : 28401-28460, для СК-95 зоны 4-32: 20004-20032
# При ошибке возвращает ноль

    mapChangeUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeUserSystemParametersByEpsg', ctypes.c_void_p, ctypes.c_int)
    def mapChangeUserSystemParametersByEpsg(_huser: ctypes.c_void_p, _epsgcode: int) -> int:
        return mapChangeUserSystemParametersByEpsg_t (_huser, _epsgcode)


# Установить/Запросить тип системы координат
# (плоская прямоугольная - 1 или геодезическая - 2)
# huser - идентификатор пользовательской системы координат
# При отсутствии данных возвращает ноль

    mapSetUserSystemType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetUserSystemType', ctypes.c_void_p, ctypes.c_int)
    def mapSetUserSystemType(_huser: ctypes.c_void_p, _type: int) -> int:
        return mapSetUserSystemType_t (_huser, _type)

    mapGetUserSystemType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetUserSystemType', ctypes.c_void_p)
    def mapGetUserSystemType(_huser: ctypes.c_void_p) -> int:
        return mapGetUserSystemType_t (_huser)


# Запросить значение осевого меридиана для пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# При ошибке возвращает ноль

    mapGetUserSystemAxisMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetUserSystemAxisMeridian', ctypes.c_void_p)
    def mapGetUserSystemAxisMeridian(_huser: ctypes.c_void_p) -> float:
        return mapGetUserSystemAxisMeridian_t (_huser)


# Установить номер зоны для пользовательской системы координат и обновить осевой меридиан
# huser - идентификатор пользовательской системы координат
# zone  - номер зоны от 1 до 60
# isupdateaxis - признак необходимости пересчета осевого меридиана для заданного номера зоны
# При ошибке возвращает ноль

    mapSetUserSystemZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetUserSystemZone', ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
    def mapSetUserSystemZone(_huser: ctypes.c_void_p, _zone: int, _isupdateaxis: int) -> int:
        return mapSetUserSystemZone_t (_huser, _zone, _isupdateaxis)


# Запросить номер зоны для пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# При ошибке возвращает ноль

    mapGetUserSystemZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetUserSystemZone', ctypes.c_void_p)
    def mapGetUserSystemZone(_huser: ctypes.c_void_p) -> int:
        return mapGetUserSystemZone_t (_huser)


# Преобразование из геодезических координат (радианы) в пользовательской системе координат
# в геодезические координаты в радианах (общеземной эллипсоид WGS84)
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе радианы, на выходе - радианы
# h     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает 0

    mapUserGeoToGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToGeoWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeoWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeoWGS84_t (_huser, _bx, _ly)

    mapUserGeoToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToGeoWGS843D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeoWGS843D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeoWGS843D_t (_huser, _bx, _ly, _h)


# Преобразование из геодезических координат в радианах в пользовательской геодезической системе координат
# в геодезические координаты в радианах на заданном эллипсоиде и с заданными параметрами перехода
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе радианы, на выходе - радианы
# h     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# ldatum - параметры перехода от пользовательской системы координат к геодезической системе на заданном эллипсоиде
#          (обратное преобразование Гельмерта, или Coordinate Frame Rotation; EPSG dataset coordinate operation method code 1032)
# ellipsoid - параметры эллипсоида, на котором определяют геодезические координаты
# При ошибке возвращает 0

    mapUserGeoToLocalGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToLocalGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapUserGeoToLocalGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _ldatum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapUserGeoToLocalGeo3D_t (_huser, _bx, _ly, _h, _ldatum, _ellipsoid)


# Преобразование координат из пользовательской геодезической системы к
# геоцентрической системе координат для эллипсоида WGS84
# huser - идентификатор пользовательской системы координат
# bx,ly,h  - преобразуемые координаты
# на входе радианы, на выходе - метры в геоцентрической системе
# h - геодезическая высота (WGS84), преобразуется в геоцентрическую координату
# Преобразование нормальной высоты к геодезической выполняет mapNormalHeightToGeoHeightWGS84
# или mapUserPlaneToGeoWGS84Pro
# При ошибке возвращает ноль

    mapUserGeoToXYZWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToXYZWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToXYZWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToXYZWGS84_t (_huser, _bx, _ly, _h)


# Преобразование координат из геоцентрической системы координат для WGS84 к
# пользовательской геодезической системе координат
# huser - идентификатор пользовательской системы координат
# bx,ly,h  - преобразуемые координаты
# на входе метры в геоцентрической системе, на выходе - радианы
# h - геоцентрическая координата, преобразуется в геодезическую высоту WGS84
# Преобразование геодезической высоты к нормальной выполняет mapGeoHeightToNormalHeightWGS84
# При ошибке возвращает ноль

    mapXYZWGS84ToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapXYZWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZWGS84ToUserGeo_t (_huser, _bx, _ly, _h)


# Преобразование координат из пользовательской геодезической системы к
# геоцентрической системе координат для заданного эллипсоида
# bx,ly,h  - преобразуемые координаты
# на входе радианы, на выходе - метры в геоцентрической системе
# h - геодезическая высота, преобразуется в геоцентрическую координату
# При ошибке возвращает ноль

    mapUserGeoToUserXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToUserXYZ', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserXYZ(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToUserXYZ_t (_huser, _bx, _ly, _h)


# Преобразование координат из геоцентрической системы координат
# к пользовательской геодезической системе координат для заданного эллипсоида
# bx,ly,h  - преобразуемые координаты
# на входе метры в геоцентрической системе, на выходе - радианы
# h - геоцентрическая координата, преобразуется в геодезическую высоту
# При ошибке возвращает ноль

    mapUserXYZToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserXYZToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserXYZToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserXYZToUserGeo_t (_huser, _bx, _ly, _h)


# Преобразование из геодезических координат (радианы) в метры в пользовательской проекции
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе радианы, на выходе - метры
# h     - геодезическая высота в точке (метры), пересчитывается в НОРМАЛЬНУЮ (если задан hegm)
# hegm  - идентификатор модели геоида, открытой mapOpenEgmPro, необходим
#         для пересчета геодезической высоты в нормальную (геоид MSL)
# Балтийская система высот (квазигеоид) отличается от нормальной в среднем в пределах 1-2 метра
# Высота пересчитывается сначала из геодезической в геодезическую WGS84 и затем в нормальную
# При ошибке возвращает 0

    mapUserGeoToUserPlanePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserGeoToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserGeoToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)

    mapUserGeoToUserPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToUserPlane_t (_huser, _bx, _ly)

    mapUserGeoToPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToPlane_t (_huser, _bx, _ly)


# Преобразование из метров на местности в пользовательской проекции
# в геодезические координаты в радианах (общеземной эллипсоид WGS84)
# Наличие высоты повышает точность расчетов
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе метры, на выходе - радианы
# h     - НОРМАЛЬНАЯ высота в точке (метры), пересчитывается в геодезическую (если задан hegm)
# hegm  - идентификатор модели геоида, открытой mapOpenEgmPro, необходим
#         для пересчета нормальной высоты (геоид MSL) в геодезическую WGS84
# Балтийская система высот (квазигеоид) отличается от нормальной в среднем в пределах 1-2 метра
# При ошибке возвращает 0

    mapUserPlaneToGeoWGS84Pro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToGeoWGS84Pro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToGeoWGS84Pro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserPlaneToGeoWGS84Pro_t (_huser, _bx, _ly, _h, _hegm)


# Преобразование из метров на местности в пользовательской проекции
# в геодезические координаты в радианах (общеземной эллипсоид WGS84)
# Наличие высоты повышает точность расчетов
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе метры, на выходе - радианы
# h     - НОРМАЛЬНАЯ высота в точке (метры), не пересчитывается
# Балтийская система высот (квазигеоид) отличается от нормальной в среднем в пределах 1-2 метра
# При ошибке возвращает 0

    mapUserPlaneToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToGeoWGS843D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToGeoWGS843D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToGeoWGS843D_t (_huser, _bx, _ly, _h)

    mapUserPlaneToGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToGeoWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToGeoWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToGeoWGS84_t (_huser, _bx, _ly)


# Преобразование из метров на местности в пользовательской проекции
# в геодезические координаты в радианах на эллипсоиде в пользовательской проекции
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты,  на входе метры, на выходе - радианы
# h     - НОРМАЛЬНАЯ высота в точке (метры), пересчитывается в геодезическую (если задан hegm)
# hegm  - идентификатор модели геоида, открытой mapOpenEgmPro, необходим
#         для пересчета нормальной высоты (геоид MSL) в геодезическую на заданном эллипсоиде
# Высота пересчитывается сначала из нормальной в геодезическую WGS84 и затем на заданный эллипсоид
# При ошибке возвращает 0

    mapUserPlaneToUserGeoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToUserGeoPro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToUserGeoPro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserPlaneToUserGeoPro_t (_huser, _bx, _ly, _h, _hegm)

    mapUserPlaneToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToUserGeo_t (_huser, _bx, _ly)

    mapUserPlaneToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserPlaneToGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToGeo_t (_huser, _bx, _ly)


# Преобразование из геодезических координат в радианах (общеземной эллипсоид WGS84)
# в геодезические координаты в радианах на эллипсоиде в пользовательской проекции
# huser  - идентификатор пользовательской системы координат
# bx,ly  - преобразуемые координаты, на входе радианы, на выходе - радианы
# h      - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает ноль

    mapGeoWGS84ToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserGeo_t (_huser, _bx, _ly)

    mapGeoWGS84ToUserGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToUserGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserGeo3D_t (_huser, _bx, _ly, _h)


# Преобразование из геодезических координат в радианах
# (общеземной эллипсоид WGS84)
# в метры на местности в пользовательской проекции
# huser  - идентификатор пользовательской системы координат
# bx,ly  - преобразуемые координаты, на входе радианы, на выходе - метры
# h     - геодезическая высота в точке (метры), пересчитывается в НОРМАЛЬНУЮ (если задан hegm)
# hegm  - идентификатор модели геоида, открытой mapOpenEgmro, необходим
#         для пересчета геодезической высоты WGS84 в нормальную (MSL) относительно геоида
# При ошибке возвращает ноль

    mapGeoWGS84ToUserPlanePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoWGS84ToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapGeoWGS84ToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)

    mapGeoWGS84ToUserPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToUserPlane3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserPlane3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserPlane3D_t (_huser, _bx, _ly, _h)

    mapGeoWGS84ToUserPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoWGS84ToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserPlane_t (_huser, _bx, _ly)


# Преобразование из геодезических координат (радианы) в проекции документа
# в геодезические координаты в радианах на эллипсоиде в пользовательской проекции
# hmap  - идентификатор открытых данных
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе радианы, на выходе - радианы
# h     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает ноль

    mapGeoToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToUserGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToUserGeo_t (_hmap, _huser, _bx, _ly)

    mapGeoToUserGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeoToUserGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToUserGeo3D_t (_hmap, _huser, _bx, _ly, _h)


# Преобразование из геодезических координат (радианы) на эллипсоиде
# в пользовательской проекции в геодезические координаты (радианы) в проекции документа
# hmap  - идентификатор открытых данных
# huser - идентификатор пользовательской системы координат
# bx,ly - преобразуемые координаты, на входе радианы, на выходе - радианы
# h     - геодезическая высота в точке (метры), пересчитывается между эллипсоидами
# При ошибке возвращает ноль

    mapUserGeoToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeo_t (_hmap, _huser, _bx, _ly)

    mapUserGeoToGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUserGeoToGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeo3D_t (_hmap, _huser, _bx, _ly, _h)


# Сравнить параметры двух систем координат
# parm1      - параметры первой системы координат (см. MAPCREAT.H)
# datum1     - параметры пересчета с эллипсоида первой системы координат к WGS84 (datum может быть 0)
# ellipsoid1 - параметры пользовательского эллипсоида для первой
#              системы координат, только когда поле EllipsoidKind в
#              MAPREGISTEREX равно USERELLIPSOID (ellipsoid может быть 0)
# type1      - тип локального преобразования координат (см. TRANSFORMTYPE
#              в mapcreat.h) для первой системы координат
# tparm1     - параметры локального преобразования координат (см. mapcreat.h)
#              для первой системы координат
# parm2      - параметры второй системы координат (см. MAPCREAT.H)
# datum2     - параметры пересчета с эллипсоида второй системы координат к WGS84 (datum может быть 0)
# ellipsoid2 - параметры пользовательского эллипсоида для второй системы координат
# type2      - тип локального преобразования координат (см. TRANSFORMTYPE
#              в mapcreat.h) второй системы координат
# tparm2     - параметры локального преобразования координат (см. mapcreat.h)
#              второй системы координат
# При несовпадении каких-либо значений параметров возвращает ненулевое значение
# Некоторые несовпадающие параметры могут считаться идентичными
# (например, топографическая карта UTM и обзорно-географическая карта UTM)

    mapCompareSystemParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCompareSystemParametersPro(_parm1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype1: int, _tparm1: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _parm2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype2: int, _tparm2: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapCompareSystemParametersPro_t (_parm1, _datum1, _ellipsoid1, _ttype1, _tparm1, _parm2, _datum2, _ellipsoid2, _ttype2, _tparm2)

    mapCompareSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareSystemParameters', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCompareSystemParameters(_parm1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapCompareSystemParameters_t (_parm1, _datum1, _ellipsoid1, _parm2, _datum2, _ellipsoid2)


# Сравнить параметры двух систем координат
# huser1 - идентификатор первой пользовательской системы координат
# huser2 - идентификатор второй пользовательской системы координат
# При несовпадении каких-либо значений параметров возвращает ненулевое значение

    mapCompareUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareUserSystemParameters', ctypes.c_void_p, ctypes.c_void_p)
    def mapCompareUserSystemParameters(_huser1: ctypes.c_void_p, _huser2: ctypes.c_void_p) -> int:
        return mapCompareUserSystemParameters_t (_huser1, _huser2)


# Освободить память строки с описанием параметров системы координат
# point - адрес строки, полученной из mapGetUserSystemXmlNode

    mapFreeUserSystemXmlNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeUserSystemXmlNode', ctypes.c_char_p)
    def mapFreeUserSystemXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeUserSystemXmlNode_t (_point)


# Установить формат отображения текущих координат курсора
# hmap    - идентификатор открытых данных
# format -  номер формата отображения координат (см. maptype.h - CURRENTPOINTFORMAT)
# При ошибке возвращает ноль, иначе - установленное значение

    mapSetCurrentPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCurrentPointFormat', maptype.HMAP, ctypes.c_int)
    def mapSetCurrentPointFormat(_hmap: maptype.HMAP, _format: int) -> int:
        return mapSetCurrentPointFormat_t (_hmap, _format)


# Запросить формат отображения текущих координат курсора
# hmap    - идентификатор открытых данных
# Возвращает номер формата отображения координат (см. maptype.h - CURRENTPOINTFORMAT)
# При ошибке возвращает ноль

    mapGetCurrentPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCurrentPointFormat', maptype.HMAP)
    def mapGetCurrentPointFormat(_hmap: maptype.HMAP) -> int:
        return mapGetCurrentPointFormat_t (_hmap)


# Пересчитать значение координат из плоских прямоугольных координат документа (метры)
# в систему, определяемую форматом отображения текущих координат
# hmap    - идентификатор открытых данных
# x, y    - координаты точки в метрах в соответствии с текущими параметрами
#           проекции (mapGetDocProjection) - пересчитываются в новые значения
# h       - высота точки (указатель может быть равен нулю), если задано значение -
#           пересчитывается в новое значение
# maptype - тип карты, соответствующий координатам, если не равен нулю,
#           то добавляется строка с обозначением системы координат: "(СК42)", "(CR95)"...
# При ошибке возвращает ноль

    mapPlaneToPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToPointFormat', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPointFormat(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToPointFormat_t (_hmap, _x, _y, _h)


# Пересчитать значение координат из плоских прямоугольных координат документа (метры)
# в систему, определяемую форматом отображения текущих координат
# и сформировать строку
# hmap    - идентификатор открытых данных
# x, y    - координаты точки в метрах в соответствии с текущими параметрами
#           проекции (mapGetDocProjection)
# h       - нормальная высота точки (указатель может быть равен нулю)
# hegm    - идентификатор модели геоида, открытой mapOpenEgmPro, необходим
#           для пересчета нормальной высоты (геоид MSL) в геодезическую WGS84
# Балтийская система высот (квазигеоид) отличается от нормальной в среднем в пределах 1-2 метра
# place   - адрес строки для записи результата
# size    - размер выделеной строки (не менее 256 байт)
# Пример строки:
# B= -73° 27' 04.53"  L= 175° 51' 21.07"  H= 109.51 m (WGS84)
# X= 6 309 212.12 м   Y= 7 412 249.25 м (СК42)
# При ошибке возвращает ноль

    mapPlaneToPointFormatStringPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToPointFormatStringPro', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p, maptype.PWCHAR, ctypes.c_int)
    def mapPlaneToPointFormatStringPro(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapPlaneToPointFormatStringPro_t (_hmap, _x, _y, _h, _hegm, _place.buffer(), _size)

    mapPlaneToPointFormatStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToPointFormatStringUn', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_int)
    def mapPlaneToPointFormatStringUn(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int) -> int:
        return mapPlaneToPointFormatStringUn_t (_hmap, _x, _y, _h, _place.buffer(), _size)


# Вывод координат точки в строку
# x,y   - плоские прямоугольные координаты точки в метрах
# h     - высота в метрах или нулевой указатель
# place - адрес строки для размещения результата
# size  - размер строки в байтах (не менее 80 байт)
# maptype - тип карты, если не равен нулю, то добавляется строка
#           с обозначением системы координат: "   (СК42)", "   (CК95)",...
# Пример результата:
# "X=  438 145.27 m  Y= 6 230 513.03 m  H=  54.12 m"

    mapPlaneToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPlaneToStringUn', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapPlaneToStringUn(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int, _maptype: int) -> int:
        return mapPlaneToStringUn_t (_x, _y, _h, _place.buffer(), _size, _maptype)


# Вывод геоцентрических координат точки в строку
# x,y   - плоские прямоугольные координаты точки в метрах
# h     - высота в метрах или нулевой указатель
# place - адрес строки для размещения результата
# size  - размер строки в байтах (не менее 80 байт)
# Пример результата:
# "X= -4 438 145.271 Y= 3 230 513.034 H= 6 632 054.125 m"

    mapXYZToString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapXYZToString', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapXYZToString(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _z: ctypes.POINTER(ctypes.c_double), _place: ctypes.c_char_p, _size: int, _maptype: int) -> ctypes.c_void_p:
        return mapXYZToString_t (_x, _y, _z, _place, _size, _maptype)


# Запись вещественного числа в символьном виде с фиксированной точкой
# value  - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 32 !)
# precision - число знаков после точки (запятой)
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#   '.' или ',' - заменить десятичную точку на separator: '.' или ','
# При ошибке возвращает ноль

    mapDoubleFormatPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDoubleFormatPro', ctypes.c_double, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapDoubleFormatPro(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int, _separator: int) -> int:
        return mapDoubleFormatPro_t (_value, _string.buffer(), _size, _precision, _separator)


# Запись вещественного числа в символьном виде с фиксированной точкой
# value  - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 16 !)
# precision - число знаков после точки (запятой)
# При ошибке возвращает ноль

    mapDoubleFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDoubleFormat', ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapDoubleFormat(_value: float, _string: ctypes.c_char_p, _size: int, _precision: int) -> int:
        return mapDoubleFormat_t (_value, _string, _size, _precision)


# Запись вещественного числа в символьном виде с фиксированной точкой
# со вставкой разделяющих пробелов
# (разделение на тройки символов от конца строки к началу)
# Например: 7 390 621.458
# value  - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 16 !)
# precision - число знаков после точки (запятой)
# При ошибке возвращает ноль

    mapDoubleToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDoubleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapDoubleToStringUn(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int) -> int:
        return mapDoubleToStringUn_t (_value, _string.buffer(), _size, _precision)


# Запись целого числа в символьном виде со вставкой разделяющих пробелов
# (разделение на тройки символов от конца строки к началу)
# size - длина строки в байтах (не менее 16 !)
# При ошибке возвращает ноль

    mapLongToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLongToStringUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapLongToStringUn(_number: int, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapLongToStringUn_t (_number, _string.buffer(), _size)


# Запись целого числа типа __int64 в символьном виде
# со вставкой разделяющих пробелов
# (разделение на тройки символов от конца строки к началу)
# size - длина строки в байтах (не менее 32 !)
# При ошибке возвращает ноль

    mapInt64ToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInt64ToStringUn', ctypes.c_int64, maptype.PWCHAR, ctypes.c_int)
    def mapInt64ToStringUn(_number: int, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapInt64ToStringUn_t (_number, _string.buffer(), _size)


# Округлить дробную часть числа до заданного числа знаков
# Целая часть остается без изменения
# value - исходное значение
# count - число знаков после запятой (от 0 до 9)

    mapRoundDouble_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRoundDouble', ctypes.c_double, ctypes.c_int)
    def mapRoundDouble(_value: float, _count: int) -> float:
        return mapRoundDouble_t (_value, _count)


# Запись масштаба в символьном виде со вставкой разделяющих пробелов
# (например: "1 : 50 000","2 : 1" - если scale < 1)
# (разделение на тройки символов от конца строки к началу)
# size - длина строки в байтах (не менее 20 !)
# При ошибке возвращает ноль

    mapScaleToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapScaleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_int)
    def mapScaleToStringUn(_scale: float, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapScaleToStringUn_t (_scale, _string.buffer(), _size)


# Запросить параметры проекции и системы координат по коду EPSG
# Если код EPSG задает геодезическую или геоцентрическую систему координат,
# то устанавливается проекция Широта\Долгота и соответствующие
# параметры эллипсоида и датум
# Если код EPSG задает плоскую прямоугольную систему координат,
# то все параметры устанавливаются из базы EPSG
# epsgcode  - код EPSG, для СК-42 зоны 2-32 : 28402-28432, для СК-95 зоны 4-32: 20004-20032
# mapreg    - параметры системы координат и проекции
# datum     - параметры пересчета с эллипсоида рабочей системы координат к WGS84
# ellipsoid - параметры пользовательского эллипсоида для рабочей системы координат
# Для геодезических систем координат возвращает 2, для геоцентрических - 3,
# для плоских прямоугольных - 1
# При ошибке возвращает ноль

    mapGetParametersForEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetParametersForEPSG', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetParametersForEPSG(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetParametersForEPSG_t (_epsgcode, _mapreg, _datum, _ellipsoid)


# Зарегистрировать пользовательский код параметров Epsg
# epsg - регистрируемый код системы координат
# mapregister, datum, ellips - параметры региструруемой проекции
# При ошибке возвращает 0

    mapRegisterUserEpsgParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterUserEpsgParameters', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapRegisterUserEpsgParameters(_epsg: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellips: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapRegisterUserEpsgParameters_t (_epsg, _mapregister, _datum, _ellips)


# Открыть базу данных EPSG
# При успешном выполнении возвращает идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapOpenEPSGDatabase_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEPSGDatabase')
    def mapOpenEPSGDatabase() -> ctypes.c_void_p:
        return mapOpenEPSGDatabase_t ()


# Закрыть базу данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG

    mapCloseEPSGDatabase_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseEPSGDatabase', ctypes.c_void_p)
    def mapCloseEPSGDatabase(_epsgdata: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseEPSGDatabase_t (_epsgdata)


# Возвращает количество прямоугольных систем координат в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapGetEPSGProjectedSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGProjectedSystemCount', ctypes.c_void_p)
    def mapGetEPSGProjectedSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        return mapGetEPSGProjectedSystemCount_t (_epsgdata)


# Возвращает количество геодезических систем координат в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGGeodeticSystemCount', ctypes.c_void_p)
    def mapGetEPSGGeodeticSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        return mapGetEPSGGeodeticSystemCount_t (_epsgdata)


# Считать данные на текущую прямоугольную систему координат в базе данных EPSG
# После вызова функции текущей становится следующая система координат в базе данных EPSG
# epsgdata  - идентификатор открытой базы данных EPSG
# mapreg    - параметры проекции
# ellipsoid - эллипсоид
# datum     - датум
# rectsys   - параметры прямоугольной системы координат
# geodsys   - параметры базовой геодезической системы координат
# unit      - единицы измерения
# При ошибке или при выходе за границы набора данных возвращает ноль

    mapReadEPSGProjectedSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadEPSGProjectedSystem', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadEPSGProjectedSystem(_epsgdata: ctypes.c_void_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapReadEPSGProjectedSystem_t (_epsgdata, _mapreg, _ellipsoid, _datum, _rectsys, _geodsys, _unit)


# Считать данные на прямоугольную систему координат по номеру записи в базе данных EPSG
# После вызова функции текущей становится следующая система координат в базе данных EPSG
# epsgdata    - идентификатор открытой базы данных EPSG
# coordsysnum - номер записи в списке прямоугольных систем координат (от 1)
# mapreg      - параметры проекции
# ellipsoid   - эллипсоид
# datum       - датум
# rectsys     - параметры прямоугольной системы координат
# geodsys     - параметры базовой геодезической системы координат
# unit        - единицы измерения
# При ошибке или при выходе за границы набора данных возвращает ноль

    mapReadEPSGProjectedSystemByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadEPSGProjectedSystemByNumber', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadEPSGProjectedSystemByNumber(_epsgdata: ctypes.c_void_p, _coordsysnum: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapReadEPSGProjectedSystemByNumber_t (_epsgdata, _coordsysnum, _mapreg, _ellipsoid, _datum, _rectsys, _geodsys, _unit)


# Считать параметры геодезической системы координат по порядковому номеру в базе данных EPSG
# epsgdata    - идентификатор открытой базы данных EPSG
# coordsysnum - порядковый номер геодезической системы координат в базе данных EPSG (от 1)
# ellipsoid   - возвращаемые параметры эллипсоида (может быть равен 0)
# datum       - параметры эллипсоида (может быть равен 0)
# geodsys     - параметры геодезической СК (может быть равен 0)
# При ошибке возвращает ноль

    mapReadEPSGGeodeticSystemByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadEPSGGeodeticSystemByNumber', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapReadEPSGGeodeticSystemByNumber(_epsgdata: ctypes.c_void_p, _coordsysnum: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapReadEPSGGeodeticSystemByNumber_t (_epsgdata, _coordsysnum, _ellipsoid, _datum, _geodsys)


# Запросить параметры геодезической системы координат по коду в базе данных EPSG
# epsgcode  - код геодезической системы координат в базе данных EPSG
# ellipsoid - параметры эллипсоида
# datum     - параметры датума
# geodsys   - параметры геодезической СК
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGGeodeticSystem', ctypes.c_int, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystem(_epsgcode: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapGetEPSGGeodeticSystem_t (_epsgcode, _ellipsoid, _datum, _geodsys)


# Запросить параметры геодезической системы координат по имени в базе данных EPSG
# name      - имя геодезической системы координат
# ellipsoid - параметры эллипсоида
# datum     - параметры датума
# geodsys   - параметры геодезической СК
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystemByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGGeodeticSystemByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystemByName(_name: ctypes.c_char_p, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapGetEPSGGeodeticSystemByName_t (_name, _ellipsoid, _datum, _geodsys)


# Запросить параметры прямоугольной системы координат по коду в базе данных EPSG
# epsgcode - код прямоугольной системы координат в базе данных EPSG
# mapreg   - параметры проекции
# rectsys  - параметры прямоугольной СК
# При ошибке возвращает ноль

    mapGetEPSGProjectedSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGProjectedSystem', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.EPSGRECTSYS))
    def mapGetEPSGProjectedSystem(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS)) -> int:
        return mapGetEPSGProjectedSystem_t (_epsgcode, _mapreg, _rectsys)


# Запросить параметры единицы измерения по коду в базе данных EPSG
# epsgcode - код единицы измерения в базе данных EPSG
# unit     - параметры единицы измерения
# При ошибке возвращает ноль

    mapGetEPSGUnit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGUnit', ctypes.c_int, ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapGetEPSGUnit(_epsgcode: int, _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapGetEPSGUnit_t (_epsgcode, _unit)


# Заполнить WKT строку из MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM
# mapreg    - параметры проекции
# ellipsoid - параметры эллипсоида
# datum     - параметры датума
# wktstr    - заполняемая строка с описанием системы координат
# wktstrsize - зарезервированный размер строки (4 Кбайта достаточно)
# При ошибке возвращает ноль

    mapSetWKTString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetWKTString', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.c_char_p, ctypes.c_int)
    def mapSetWKTString(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _wktstr: ctypes.c_char_p, _wktstrsize: int) -> int:
        return mapSetWKTString_t (_mapreg, _ellipsoid, _datum, _wktstr, _wktstrsize)


# Заполнить MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM из WKT строки
# wktstr    - строка с описанием системы координат
# mapreg    - заполняемые параметры проекции
# ellipsoid - заполняемые параметры эллипсоида
# datum     - заполняемые параметры датума
# При ошибке возвращает ноль

    mapReadWKTString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadWKTString', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapReadWKTString(_wktstr: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapReadWKTString_t (_wktstr, _mapreg, _ellipsoid, _datum)


# Прочитать описание системы координат из строки WKT (стандарт OGC 12-063r5)
# и заполнить структуры MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM,
# EPSGRECTSYS, EPSGGEODSYS, EPSGMEASUNIT.
# Заполнены будут только те структуры, указатели на которые будут переданы в
# функцию.
# Параметры:
# wktstr       - WKT-строка с описанием системы координат
# isprojection - возвращает признак прямоугольной СК (1)
# mapreg       - заполняемые параметры проекции
# ellipsoid    - заполняемые параметры эллипсоида
# datum        - заполняемые параметры датума
# sysrect      - заполняемые параметры прямоугольной СК (при isprojection = 1)
# sysgeo       - заполняемые параметры геодзической СК (при isprojection = 0)
# unit         - заполняемые параметры единицы измерения
# При ошибке возвращает ноль

    mapReadWKTStringEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadWKTStringEx', ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadWKTStringEx(_wktstr: ctypes.c_char_p, _isprojection: ctypes.POINTER(ctypes.c_int), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _sysrect: ctypes.POINTER(mapcreat.EPSGRECTSYS), _sysgeo: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapReadWKTStringEx_t (_wktstr, _isprojection, _mapreg, _ellipsoid, _datum, _sysrect, _sysgeo, _unit)


# Определить EPSG код для некоторых систем координат
# При ошибке возвращает ноль

    mapFindEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFindEPSGCode', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapFindEPSGCode(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapFindEPSGCode_t (_mapreg, _ellipsoid, _datum)


# Открыть список параметров систем отсчета
# name - имя файла списка параметров
# При успешном выполнении возвращает идентификатор списка в памяти
# При ошибке возвращает ноль

    mapOpenMapRegisterListUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAPREG,'mapOpenMapRegisterListUn', maptype.PWCHAR)
    def mapOpenMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        return mapOpenMapRegisterListUn_t (_name.buffer())


# Создать список параметров систем отсчета
# name - имя файла списка параметров
# При успешном выполнении возвращает идентификатор списка в памяти
# При ошибке возвращает ноль

    mapCreateMapRegisterListUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAPREG,'mapCreateMapRegisterListUn', maptype.PWCHAR)
    def mapCreateMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        return mapCreateMapRegisterListUn_t (_name.buffer())


# Закрыть список параметров систем отсчета
# hmapreg - идентификатор списка параметров систем отсчета

    mapCloseMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMapRegisterList', maptype.HMAPREG)
    def mapCloseMapRegisterList(_hmapreg: maptype.HMAPREG) -> ctypes.c_void_p:
        return mapCloseMapRegisterList_t (_hmapreg)


# Запросить число систем отсчета, хранящихся в списке
# в виде файла XML (<ProjectList Version="1.0">
# Одной системе соответствует один тэг "Project"
# hmapreg - идентификатор списка параметров систем отсчета
# При успешном выполнении возвращает число записей параметров
# При ошибке возвращает ноль

    mapMapRegisterListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListCount', maptype.HMAPREG)
    def mapMapRegisterListCount(_hmapreg: maptype.HMAPREG) -> int:
        return mapMapRegisterListCount_t (_hmapreg)


# Запросить название системы отсчета по заданному порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# name    - адрес строки для размещения результата
# size    - размер выделенной строки в байтах
# При ошибке возвращает ноль

    mapMapRegisterListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _size)


# Запросить комментарий для системы отсчета по заданному порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# name    - адрес строки для размещения результата
# size    - длина выделенной строки для размещения результата
# При ошибке возвращает ноль

    mapMapRegisterListCommentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListCommentUn', maptype.HMAPREG, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapMapRegisterListCommentUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListCommentUn_t (_hmapreg, _number, _name.buffer(), _size)


# Запросить порядковый номер в списке (начиная с 1)
# по коду EPSG для системы отсчета (CRS)
# hmapreg - идентификатор списка параметров систем отсчета
# epsg    - код EPSG для системы отсчета (CRS)
# При ошибке возвращает ноль

    mapSeekMapRegisterListByEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekMapRegisterListByEPSG', maptype.HMAPREG, ctypes.c_int)
    def mapSeekMapRegisterListByEPSG(_hmapreg: maptype.HMAPREG, _epsg: int) -> int:
        return mapSeekMapRegisterListByEPSG_t (_hmapreg, _epsg)


# Запросить код EPSG для системы отсчета по заданному порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# Если код не задан - возвращает "-1"
# При ошибке возвращает ноль

    mapMapRegisterListEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListEPSG', maptype.HMAPREG, ctypes.c_int)
    def mapMapRegisterListEPSG(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        return mapMapRegisterListEPSG_t (_hmapreg, _number)


# Запросить идентификатор для системы отсчета
# по заданному порядковому номеру в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# ident   - адрес строки для размещения идентификатора
# size    - длина выделенной строки для размещения идентификатора
# При ошибке возвращает ноль

    mapMapRegisterListCrsIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListCrsIdentUn', maptype.HMAPREG, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapMapRegisterListCrsIdentUn(_hmapreg: maptype.HMAPREG, _number: int, _ident: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListCrsIdentUn_t (_hmapreg, _number, _ident.buffer(), _size)


# Запросить параметры системы отсчета по заданному порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# mapreg  - параметры проекции <Projection ...>
# datum   - параметры датума <Datum ...>
# ellparm - параметры эллипсоида <Spheroid ...>
# ttype   - адрес поля для записи типа локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm   - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapMapRegisterListParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMapRegisterListParametersPro', maptype.HMAPREG, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _number: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_int), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapMapRegisterListParametersPro_t (_hmapreg, _number, _mapreg, _datum, _ellparm, _ttype, _tparm)


# Добавить запись параметров системы отсчета
# hmapreg - идентификатор списка параметров систем отсчета
# name    - уникальное название системы отсчета (обязательно)
# comment - комментарий для системы отсчета (или ноль)
# epsgcode - код EPSG (или ноль)
# ident   - идентификатор системы отсчета (или ноль)
# mapreg  - описание параметров системы отсчета (обязательно)(см. mapcreat.h)
# datum   - описание параметров датума (или ноль) (см. mapcreat.h)
# ellparam - описание параметров эллипсоида (или ноль) (см. mapcreat.h)
# ttype   - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm   - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке возвращает ноль

    mapAppendMapRegisterListParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendMapRegisterListParametersPro', maptype.HMAPREG, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapAppendMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _epsgcode: int, _ident: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapAppendMapRegisterListParametersPro_t (_hmapreg, _name.buffer(), _comment.buffer(), _epsgcode, _ident.buffer(), _mapreg, _datum, _ellparm, _ttype, _tparm)


# Удалить запись параметров систем отсчета по порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# Для немедленного изменения данных в файле нужно вызвать
# функцию mapCommitMapRegisterList
# При ошибке возвращает ноль

    mapDeleteMapRegisterListParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteMapRegisterListParameters', maptype.HMAPREG, ctypes.c_int)
    def mapDeleteMapRegisterListParameters(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        return mapDeleteMapRegisterListParameters_t (_hmapreg, _number)


# Обновить название, комментарий и код системы отсчета по заданному порядковому номеру
# в списке (начиная с 1)
# hmapreg - идентификатор списка параметров систем отсчета
# number  - порядковый номер записи параметров
# name    - название системы отсчета или 0 (не менять)
# comment - комментарий к системе отсчета или 0 (не менять)
# code    - код EPSG или 0 (не менять)
# ident   - идентификатор системы отсчета или 0 (не менять)
# При ошибке возвращает ноль

    mapUpdateMapRegisterListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def mapUpdateMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _code: int, _ident: mapsyst.WTEXT) -> int:
        return mapUpdateMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _comment.buffer(), _code, _ident.buffer())


# Сохранить изменения списка параметров систем отсчета в файле
# hmapreg - идентификатор списка параметров систем отсчета
# При ошибке возвращает ноль

    mapCommitMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitMapRegisterList', maptype.HMAPREG)
    def mapCommitMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        return mapCommitMapRegisterList_t (_hmapreg)


# Отменить изменения списка параметров систем отсчета в памяти
# Отмена изменений может быть выполнена до вызова mapCommitMapRegisterList
# hmapreg - идентификатор списка параметров систем отсчета
# При ошибке возвращает ноль

    mapUndoMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUndoMapRegisterList', maptype.HMAPREG)
    def mapUndoMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        return mapUndoMapRegisterList_t (_hmapreg)


# Запросить название листа на котором расположен объект
# info - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapListNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapListNameUn(_info: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapListNameUn_t (_info, _name.buffer(), _size)


# Запросить номенклатуру листа на котором расположен объект
# info - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapNomenclatureUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapNomenclatureUn(_info: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapNomenclatureUn_t (_info, _name.buffer(), _size)


# Запросить базовый масштаб карты
# При ошибке возвращает ноль

    mapObjectMapScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectMapScale', maptype.HOBJ)
    def mapObjectMapScale(_info: maptype.HOBJ) -> int:
        return mapObjectMapScale_t (_info)


# Запросить идентификатор классификатора карты, содержащей объект
# info - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetRscIdentByObject_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetRscIdentByObject', maptype.HOBJ)
    def mapGetRscIdentByObject(_info: maptype.HOBJ) -> maptype.HRSC:
        return mapGetRscIdentByObject_t (_info)


# Запросить уникальный номер объекта
# info - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectKey', maptype.HOBJ)
    def mapObjectKey(_info: maptype.HOBJ) -> int:
        return mapObjectKey_t (_info)


# Установить уникальный номер объекта
# info - идентификатор объекта карты в памяти
# number - уникальный номер объекта в листе
# Программа, вызывающая данную функцию должна обеспечить
# уникальность номеров в листе !
# При ошибке возвращает 0

    mapSetObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectKey', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectKey(_info: maptype.HOBJ, _number: int) -> int:
        return mapSetObjectKey_t (_info, _number)


# Запросить классификационный код объекта
# info - идентификатор объекта карты в памяти
# При ошибке возвращает 0 (ноль допустим для нового объекта)

    mapObjectExcode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectExcode', maptype.HOBJ)
    def mapObjectExcode(_info: maptype.HOBJ) -> int:
        return mapObjectExcode_t (_info)


# Запросить характер локализации объекта
# info - идентификатор объекта карты в памяти
# При ошибке возвращает 0  (ноль допустим)

    mapObjectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectLocal', maptype.HOBJ)
    def mapObjectLocal(_info: maptype.HOBJ) -> int:
        return mapObjectLocal_t (_info)


# Запросить условное название объекта
# info - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapObjectNameUn(_info: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectNameUn_t (_info, _name.buffer(), _size)


# Сформировать строку с описанием объекта в виде
# "номер_объекта - имя_объекта - имя_слоя - имя_листа_карты"
# info - идентификатор объекта карты в памяти
# comment - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapObjectComment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectComment', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapObjectComment(_info: maptype.HOBJ, _comment: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectComment_t (_info, _comment.buffer(), _size)


# Запросить текущее направление цифрования контура объекта
# info - идентификатор объекта карты в памяти
# Возвращает:
#  OD_UNDEFINED (1) - не определено (незамкнутый контур или контур,
#                     вырожденный в точку или контур, имеющий "петли")
#  0D_RIGHT     (2) - объект справа (основной контур замкнутого объекта
#                     по часовой стрелке)
#  0D_LEFT      (4) - объект слева (основной контур замкнутого объекта
#                     против часовой стрелки)
# При ошибке возвращает ноль

    mapObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectDirect', maptype.HOBJ)
    def mapObjectDirect(_info: maptype.HOBJ) -> int:
        return mapObjectDirect_t (_info)


# Запросить текущее направление цифрования контура подобъекта
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта (для объекта - равен нулю)
# Возвращает:
#  OD_UNDEFINED (1) - не определено (незамкнутый контур или контур,
#                     вырожденный в точку или контур, имеющий "петли")
#  0D_RIGHT     (2) - объект справа (замкнутый контур объекта
#                     по часовой стрелке)
#  0D_LEFT      (4) - объект слева (замкнутый контур объекта
#                     против часовой стрелки)
# При ошибке возвращает ноль

    mapSubjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSubjectDirect', maptype.HOBJ, ctypes.c_int)
    def mapSubjectDirect(_info: maptype.HOBJ, _subject: int) -> int:
        return mapSubjectDirect_t (_info, _subject)


# Запросить номер слоя объекта ("Layer" = "Segment")
# Номера слоев начинаются с ноля !
# info - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapSegmentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSegmentNumber', maptype.HOBJ)
    def mapSegmentNumber(_info: maptype.HOBJ) -> int:
        return mapSegmentNumber_t (_info)


# Запросить название слоя объекта ("Layer" = "Segment")
# info - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера
# При ошибке возвращает ноль

    mapSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSegmentNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapSegmentNameUn(_info: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSegmentNameUn_t (_info, _name.buffer(), _size)


# Запросить индекс (внутренний код) объекта в классификаторе.
# При удалении объектов классификатора внутренние коды объектов
# могут изменяться. Внутренний код может использоваться для
# идентификации объекта классификатора только в течение одного
# сеанса работы с картой при неизменном классификаторе
# info - идентификатор объекта карты в памяти
# При ошибке возвращает 0 (ноль допустим для нового объекта)

    mapObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectCode', maptype.HOBJ)
    def mapObjectCode(_info: maptype.HOBJ) -> int:
        return mapObjectCode_t (_info)


# Запросить уникальный идентификатор объекта GUID
# Идентификатор GUID может автоматически присваиваться объектам карты,
# если установлен признак ведения GUID (mapSetAutoObjectGUID)
# info  - идентификатор объекта карты в памяти
# ident - поле для записи идентификатора (32 шестнадцатеричных символов от 0 до F)
# size  - размер поля в байтах
# Идентификатор хранится в семантике объекта с кодом 32799
# При ошибке возвращает 0

    mapObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectGUID', maptype.HOBJ, ctypes.c_char_p, ctypes.c_int)
    def mapObjectGUID(_info: maptype.HOBJ, _ident: ctypes.c_char_p, _size: int) -> int:
        return mapObjectGUID_t (_info, _ident, _size)


# Проверить наличие GUID и создать при необходимости
# info  - идентификатор объекта карты в памяти
# force - признак принудительного заполнения или замены GUID в семантике 32799
# Если значение семантики не соответствует формату GUID - выполняется принудительное обновление семантики
# Если изменений семантики нет - возвращает ноль

    mapCheckObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckObjectGUID', maptype.HOBJ, ctypes.c_int)
    def mapCheckObjectGUID(_info: maptype.HOBJ, _force: int) -> int:
        return mapCheckObjectGUID_t (_info, _force)


# Установить значение границ видимости по классификатору
# объектов
# info - идентификатор объекта карты в памяти

    mapClearBotTop_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearBotTop', maptype.HOBJ)
    def mapClearBotTop(_info: maptype.HOBJ) -> ctypes.c_void_p:
        return mapClearBotTop_t (_info)


# Установить/Запросить диапазон масштабов видимости объекта
# scale - масштаб отображения от 1:1 до 1:40 млн.
# info - идентификатор объекта карты в памяти

    mapObjectTopScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectTopScale', maptype.HOBJ)
    def mapObjectTopScale(_info: maptype.HOBJ) -> int:
        return mapObjectTopScale_t (_info)

    mapSetObjectTopScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectTopScale', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectTopScale(_info: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectTopScale_t (_info, _scale)

    mapObjectBotScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectBotScale', maptype.HOBJ)
    def mapObjectBotScale(_info: maptype.HOBJ) -> int:
        return mapObjectBotScale_t (_info)

    mapSetObjectBotScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectBotScale', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectBotScale(_info: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectBotScale_t (_info, _scale)


# Запросить - являются ли значения границ видимости у объекта
# уникальными (то есть установленными не из классификатора,
# а персональными для данного экземпляра)
# Если границы видимости беруться из классификатора - возвращает 0

    mapObjectBotTopUniqueness_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectBotTopUniqueness', maptype.HOBJ)
    def mapObjectBotTopUniqueness(_info: maptype.HOBJ) -> int:
        return mapObjectBotTopUniqueness_t (_info)


# Сформировать описание нового объекта по внешнему коду и локализации
# или изменить код существующего объекта на карте
# info - идентификатор объекта карты в памяти
# excode - внешний код объекта (числовой),
# local  - локализация (LOCAL_LINE, LOCAL_POINT...)
# Обычно вызывается после mapCreateObject(...) и добавления семантики
# (если она есть)
# При ошибке возвращает ноль

    mapRegisterObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapRegisterObject(_info: maptype.HOBJ, _excode: int, _local: int) -> int:
        return mapRegisterObject_t (_info, _excode, _local)


# Сформировать описание нового объекта по короткому имени объекта
# (ключу) или изменить код существующего объекта на карте
# info - идентификатор объекта карты в памяти
# name - символьный код объекта в классификаторе (до 31 символа)
# Обычно вызывается после mapCreateObject(...)
# При ошибке возвращает ноль

    mapRegisterObjectByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterObjectByKey', maptype.HOBJ, ctypes.c_char_p)
    def mapRegisterObjectByKey(_info: maptype.HOBJ, _name: ctypes.c_char_p) -> int:
        return mapRegisterObjectByKey_t (_info, _name)


# Сформировать описание нового объекта
# по внутреннему коду объекта (см. mapRscObjectCode() и т.п.)
# или изменить код существующего объекта на карте
# info - идентификатор объекта карты в памяти
# Обычно вызывается после mapCreateObject(...) и добавления
# семантики (если она есть)
# При ошибке возвращает ноль

    mapDescribeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDescribeObject', maptype.HOBJ, ctypes.c_int)
    def mapDescribeObject(_info: maptype.HOBJ, _code: int) -> int:
        return mapDescribeObject_t (_info, _code)


# Сформировать описание нового графического объекта
# по номеру слоя (из классификатора карты) и локализации
# info - идентификатор объекта карты в памяти
# layer - порядковый номер слоя в классификаторе
# local  - локализация (LOCAL_LINE, LOCAL_POINT..., см. maptype.h)
# Вызывается после mapCreateObject(...)
# Для формирования условного знака необходимо
# использовать функцию mapAppendDraw(...)
# При ошибке возвращает ноль

    mapRegisterDrawObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterDrawObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapRegisterDrawObject(_info: maptype.HOBJ, _layer: int, _local: int) -> int:
        return mapRegisterDrawObject_t (_info, _layer, _local)


# Установить номер листа для нового объекта
# info - идентификатор объекта карты в памяти
# list - последовательный номер листа (с 1)
# Обнуляет последовательный и уникальный номера объекта
# При ошибке возвращает ноль

    mapSetObjectListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectListNumber', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectListNumber(_info: maptype.HOBJ, _list: int) -> int:
        return mapSetObjectListNumber_t (_info, _list)


# Запросить номер листа для объекта
# info - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetListNumber', maptype.HOBJ)
    def mapGetListNumber(_info: maptype.HOBJ) -> int:
        return mapGetListNumber_t (_info)


#  Запросить формат хранения метрики (IDLONG2,...,IDDOUBLE3)
#  При ошибке возвращает ноль, иначе - тип формата хранения метрики

    mapGetObjectKind_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectKind', maptype.HOBJ)
    def mapGetObjectKind(_info: maptype.HOBJ) -> int:
        return mapGetObjectKind_t (_info)


# Установить тип и размерность метрики объекта
# info - идентификатор объекта карты в памяти
# kind - тип метрики, см. maptype.h
# (например : IDDOUBLE2, IDLONG2 и т.п.,
# объекты пользовательской карты и рамка листа всегда имеют тип DOUBLE)
# Преобразование метрики из типа IDDOUBLE4 и IDDOUBLE4F не выполняется,
# если число точек больше нуля
# Для удаления 4-го измерения применяется функция mapDeletePointMeasurement4D
# Пересчет выполняется с сохранением существующих координат
# При ошибке возвращает ноль

    mapSetObjectKind_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectKind', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectKind(_info: maptype.HOBJ, _kind: int) -> int:
        return mapSetObjectKind_t (_info, _kind)


# Удалить из метрики измерение 4D
# Метрика приводится к типу IDDOUBLE3
# При ошибке возвращает ноль

    mapDeletePointMeasurement4D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeletePointMeasurement4D', maptype.HOBJ)
    def mapDeletePointMeasurement4D(_info: maptype.HOBJ) -> int:
        return mapDeletePointMeasurement4D_t (_info)


# Запросить описание объекта в виде записи
# info - идентификатор объекта карты в памяти
# buffer - адрес памяти для размещения результата,
# size   - размер выделенной памяти для контроля.
# Может применяться для переноса объекта на другую карту
# той же проекции (!) (ограничение данной версии)
# Передача объекта может выполняться между различными
# потоками, процессами, компьютерами
# по соответствующим протоколам.
# При ошибке возвращает ноль

    mapGetObjectRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectRecord', maptype.HOBJ, ctypes.c_char_p, ctypes.c_int)
    def mapGetObjectRecord(_info: maptype.HOBJ, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetObjectRecord_t (_info, _buffer, _size)


# Запросить длину описания объекта в виде записи
# info - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectRecordLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectRecordLength', maptype.HOBJ)
    def mapGetObjectRecordLength(_info: maptype.HOBJ) -> int:
        return mapGetObjectRecordLength_t (_info)


# Создать объект на указанной карте из записи объекта
# hmap  - идентификатор открытых данных
# hsite - идентификатор открытой пользовательской карты
# buffer - адрес области памяти с записью объекта, созданной в mapGetObjectRecord
# mode  - режим создания
#  0 - записать,как новый;
#  1 - заменить объект при совпадении Key();
#  4 - создать в памяти,как новый,
#  5 - заменить объект при совпадении Key() в памяти;
# Для режимов 4 и 5 требуется последующий
# вызов mapCommitObject()
# При ошибке возвращает ноль, иначе - идентификатор созданного объекта
# Если объект не нужен, нужно освободить ресурсы функцией mapFreeObject

    mapPutObjectRecord_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapPutObjectRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapPutObjectRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int, _mode: int) -> maptype.HOBJ:
        return mapPutObjectRecord_t (_hmap, _hsite, _buffer, _size, _mode)


# Запросить порядковый номер объекта в карте
# info  - идентификатор объекта карты в памяти
# Если объект только создан и метод mapCommit... не вызывался -
# возвращает ноль
# При ошибке возвращает ноль

    mapGetObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectNumber', maptype.HOBJ)
    def mapGetObjectNumber(_info: maptype.HOBJ) -> int:
        return mapGetObjectNumber_t (_info)

    mapObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectNumber', maptype.HOBJ)
    def mapObjectNumber(_info: maptype.HOBJ) -> int:
        return mapObjectNumber_t (_info)


# Очистить порядковый номер объекта в карте
# Приводит к тому, что в mapCommitObject объект записывается как новый, но без изменения
# уникального номера объекта, который в этом случае должен устанавливаться через mapSetObjectKey
# При вызове mapCopyObjectAsNew уникальный номер объекта устанавливается автоматически
# как автоинкрементное поле от предыдущего максимального значения
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapClearObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearObjectNumber', maptype.HOBJ)
    def mapClearObjectNumber(_info: maptype.HOBJ) -> int:
        return mapClearObjectNumber_t (_info)


# Запросить положение объекта в документе (карта, лист, номер в листе)
# info  - идентификатор объекта карты в памяти
# desc  - положение объекта в документе (карта, лист, номер в листе)
# При ошибке возвращает ноль

    mapObjectDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectDescribe', maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapObjectDescribe(_info: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        return mapObjectDescribe_t (_info, _desc)


# Прочитать объект по заданному положению в документе
# hmap  - идентификатор открытых данных
# info  - идентификатор объекта карты в памяти
# desc  - положение объекта в документе (карта, лист, номер в листе)
# При ошибке возвращает ноль

    mapReadObjectByDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadObjectByDescribe', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapReadObjectByDescribe(_hmap: maptype.HMAP, _info: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        return mapReadObjectByDescribe_t (_hmap, _info, _desc)


# Запросить уникальный идентификатор вида объекта в классификаторе
# (короткое имя - строка длиной до 31 символа)
# info  - идентификатор объекта карты в памяти
# key  - адрес буфера для записи результата
# size - длина строки
# При ошибке возвращает ноль

    mapObjectRscKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectRscKeyUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapObjectRscKeyUn(_info: maptype.HOBJ, _key: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectRscKeyUn_t (_info, _key.buffer(), _size)


# Установить/Сбросить общую метрику объекта из объекта источника
# info   - идентификатор объекта карты в памяти
# source - идентификатор объекта c исходной (дублируемой) метрикой или 0
# Если после установки дублирования метрики будет отредактирована метрика
# клона, то изменится и метрика эталонного объекта
# При удалении эталонного объекта будет удаляться и клон
# При переносе объектов на другой лист (другую карту) признак клонирования сбрасывается
# (должен отслеживаться программой, выполняющей перенос - см.mapSetObjectMetricDuplication),
# в том числе для mapCommitWithPlace, кроме той части что остается в старом листе
# При ошибке возвращает ноль

    mapSetObjectMetricDuplicationForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectMetricDuplicationForObject', maptype.HOBJ, maptype.HOBJ)
    def mapSetObjectMetricDuplicationForObject(_info: maptype.HOBJ, _source: maptype.HOBJ) -> int:
        return mapSetObjectMetricDuplicationForObject_t (_info, _source)


# Запросить признак размещения записи метрики за 4 Гб от начала файла
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectBigMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectBigMetric', maptype.HOBJ)
    def mapGetObjectBigMetric(_info: maptype.HOBJ) -> int:
        return mapGetObjectBigMetric_t (_info)


# Установить идентификатор дубликата метрики, если метрика объекта дублируется в другом объекте
# Применяется при восстановлении признака клонирования метрики в различных процедурах обработки объектов
# info  - идентификатор объекта карты в памяти
# ismainclone - признак объекта - эталона метрики
# isbig - признак размещения записи на удалении более 4Гб от начала файла
# При ошибке возвращает ноль

    mapGetObjectMetricDuplication_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectMetricDuplication', maptype.HOBJ, ctypes.POINTER(ctypes.c_int))
    def mapGetObjectMetricDuplication(_info: maptype.HOBJ, _ismainclone: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetObjectMetricDuplication_t (_info, _ismainclone)


# Установить/Запросить масштабируемость объекта
# Применяется ТОЛЬКО для графических объектов, имеющих внутренний код равный нулю
# Для объектов из классификатора значение игнорируется
# scale = 1 для установки масштабируемости при увеличении карты
#         0 для сброса признака масштабируемости
# При ошибке возвращает ноль

    mapSetObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectScale', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectScale(_info: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectScale_t (_info, _scale)

    mapGetObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectScale', maptype.HOBJ)
    def mapGetObjectScale(_info: maptype.HOBJ) -> int:
        return mapGetObjectScale_t (_info)


# Установить/Запросить признак "Не сжимать" объекта
# Применяется ТОЛЬКО для графических объектов, имеющих внутренний код равный нулю
# press = 1 для установки признака "Не сжимать" при сжатии карты
#           относительного базового масштаба карты
#         0 для сброса признака
# При ошибке возвращает ноль

    mapSetObjectPress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectPress', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectPress(_info: maptype.HOBJ, _press: int) -> int:
        return mapSetObjectPress_t (_info, _press)

    mapGetObjectPress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectPress', maptype.HOBJ)
    def mapGetObjectPress(_info: maptype.HOBJ) -> int:
        return mapGetObjectPress_t (_info)


# Установить/Запросить способ отображения метрики объекта в виде
# динамического сплайна
# type - тип сплайна (SPLINETYPE_SMOOTH, SPLINETYPE_POINTS)
# При ошибке или отмене рисования сплайна возвращает ноль

    mapSetObjectSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectSpline', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectSpline(_info: maptype.HOBJ, _type: int) -> int:
        return mapSetObjectSpline_t (_info, _type)

    mapGetObjectSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectSpline', maptype.HOBJ)
    def mapGetObjectSpline(_info: maptype.HOBJ) -> int:
        return mapGetObjectSpline_t (_info)


# Установить/Запросить признак выравнивания подобъекта по вертикали
# При отображении первая точка метрики подобъекта выравнивается по вертикали
# по первой точке метрики объекта для векторных знаков и подписей
# При ошибке возвращает ноль

    mapSetObjectVerticalAlignment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectVerticalAlignment', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectVerticalAlignment(_info: maptype.HOBJ, _flag: int) -> int:
        return mapSetObjectVerticalAlignment_t (_info, _flag)

    mapGetObjectVerticalAlignment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectVerticalAlignment', maptype.HOBJ)
    def mapGetObjectVerticalAlignment(_info: maptype.HOBJ) -> int:
        return mapGetObjectVerticalAlignment_t (_info)


# Установить/Запросить признак формы объекта при его создании
# Установка формы не меняет метрику и не выполняет контроль реальной формы метрики,
# но может применяться в интерактивном редакторе для подбора инструментов редактирования
# 1 (OBM_RECTANGLE) - метрика имеет форму горизонтального (вертикального) прямоугольника
# 2 (OBM_CIRCLE) - метрика имеет форму окружности
# Если форма не установлена возвращает ноль

    mapSetObjectFormType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectFormType', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectFormType(_info: maptype.HOBJ, _type: int) -> int:
        return mapSetObjectFormType_t (_info, _type)

    mapGetObjectFormType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectFormType', maptype.HOBJ)
    def mapGetObjectFormType(_info: maptype.HOBJ) -> int:
        return mapGetObjectFormType_t (_info)


# Запросить/Установить признак использования семантики при отображении объекта
# info   - идентификатор объекта карты в памяти
# isview - признак использования семантики при отображении объекта
# При отображении объектов классификатора и присвоении служебных семантик,
# влияющих на вид объекта, использование семантики происходит автоматически
# При ошибке возвращает ноль

    mapSetObjectViewSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectViewSemantic', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectViewSemantic(_info: maptype.HOBJ, _isview: int) -> int:
        return mapSetObjectViewSemantic_t (_info, _isview)

    mapGetObjectViewSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectViewSemantic', maptype.HOBJ)
    def mapGetObjectViewSemantic(_info: maptype.HOBJ) -> int:
        return mapGetObjectViewSemantic_t (_info)


# Установить флаг запроса на формирование мультимасштабного объекта при mapCommitObject
# basescale - условное значение масштаба, для которого выполняется генерализация контура 1-го уровня или 0
#             масштаб 100000 (1 : 100 000) соответствует сетке с шагом 100 м
# Нулевое значение масштаба соответствует базовому масштабу карты
# Генерализация будет выполнена при вызове функции mapCommitObject с записью мультимасштабного объекта
# с набором контуров на карту

    mapSetMultiContourFlagForCommit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMultiContourFlagForCommit', maptype.HOBJ, ctypes.c_int)
    def mapSetMultiContourFlagForCommit(_info: maptype.HOBJ, _basescale: int) -> ctypes.c_void_p:
        return mapSetMultiContourFlagForCommit_t (_info, _basescale)


# ############################################################
#                                                            #
#         ЗАПРОС СЕМАНТИКИ (АТРИБУТОВ) ОБЪЕКТА               #
#                                                            #
# ############################################################
# Запросить число семантических характеристик у объекта
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapSemanticAmount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticAmount', maptype.HOBJ)
    def mapSemanticAmount(_info: maptype.HOBJ) -> int:
        return mapSemanticAmount_t (_info)


# Запросить - не является ли семантика строкой UNICODE
# info   - идентификатор объекта карты в памяти
# number - последовательный номер характеристики (c 1)
# Если семантика в кодировке Unicode - возврвщает ненулевое значение

    mapIsSemanticUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSemanticUnicode', maptype.HOBJ, ctypes.c_int)
    def mapIsSemanticUnicode(_info: maptype.HOBJ, _number: int) -> int:
        return mapIsSemanticUnicode_t (_info, _number)


# Запросить значение семантической характеристики объекта в UNICODE
# Значение преобразуется в символьный вид без раскодирования
# info   - идентификатор объекта карты в памяти
# number - последовательный номер характеристики (c 1),
# value  - адрес размещения строки,
# size   - максимальная длина строки в байтах
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# При ошибке возвращает ноль

    mapSemanticValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticValuePro', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapSemanticValuePro(_info: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int, _separator: int) -> int:
        return mapSemanticValuePro_t (_info, _number, _place.buffer(), _size, _separator)


# Запросить значение семантической характеристики объекта
# в виде числа с плавающей точкой двойной точности
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# Если значение семантики не может быть преобразовано
# к числовому виду или не найдено - возвращает ноль

    mapSemanticDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSemanticDoubleValue', maptype.HOBJ, ctypes.c_int)
    def mapSemanticDoubleValue(_info: maptype.HOBJ, _number: int) -> float:
        return mapSemanticDoubleValue_t (_info, _number)


# Запросить значение семантической характеристики объекта в виде целого числа
# number  - последовательный номер характеристики
# Если значение семантики не может быть преобразовано
# к числовому виду или - возвращает ноль

    mapSemanticLongIntValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticLongIntValue', maptype.HOBJ, ctypes.c_int)
    def mapSemanticLongIntValue(_info: maptype.HOBJ, _number: int) -> int:
        return mapSemanticLongIntValue_t (_info, _number)

    mapSemanticLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSemanticLongValue', maptype.HOBJ, ctypes.c_int)
    def mapSemanticLongValue(_info: maptype.HOBJ, _number: int) -> float:
        return mapSemanticLongValue_t (_info, _number)


# Запросить значение семантической характеристики объекта
# в символьном раскодированном виде
# Например: Для семантики "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# place   - адрес размещения строки,
# maxsize - максимальная длина строки в байтах
# При ошибке возвращает ноль, иначе - код семантики

    mapSemanticValueNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticValueNameUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSemanticValueNameUn(_info: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _maxsize: int) -> int:
        return mapSemanticValueNameUn_t (_info, _number, _place.buffer(), _maxsize)


# Запросить значение семантической характеристики объекта
# в символьном раскодированном виде с добавлением единицы
# измерения в символьном виде
# Например: Для семантики "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# Дл семантики "ВЫСОТА" значение "205,5" заменется на "205,5 м"
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# place   - адрес размещения строки,
# maxsize - максимальная длина строки
# При ошибке возвращает ноль

    mapSemanticValueFullNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticValueFullNameUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSemanticValueFullNameUn(_info: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _maxsize: int) -> int:
        return mapSemanticValueFullNameUn_t (_info, _number, _place.buffer(), _maxsize)


# Запросить значение семантической характеристики объекта
# Значение преобразуется в символьный вид
# info    - идентификатор объекта карты в памяти
# code    - код характеристики,для которой ищется значение,
# place   - адрес размещения строки,
# maxsize - максимальная длина строки
# number  - последовательный номер найденного значения,
#  не равен последовательному номеру характеристики !
#  например : код code имеют 3-я и 6-я характеристики,
#             соответственно для них number = 1 и 2,
#             а при number = 3  - код возврата будет ноль.
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# При ошибке возвращает ноль,
# при успешном выполнении - последовательный номер найденной характеристики

    mapSemanticCodeValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCodeValuePro', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSemanticCodeValuePro(_info: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _maxsize: int, _number: int, _separator: int) -> int:
        if _place is None:
           return mapSemanticCodeValuePro_t (_info, _code, 0, 0, _number, 0) # Поиск номера семантики с заданным кодом
        else:
           return mapSemanticCodeValuePro_t (_info, _code, _place.buffer(), _maxsize, _number, _separator)


# Запросить значение семантической характеристики объекта для подписывания
# (с учетом префикса и постфикса, указанных для данного типа объекта и кода семантики)
# Возвращает значение (place) в формате: "[префикс] <значение> [постфикс]".
# Если значение пусто, то префикс и постфикс не добавляются.
# Примеры - для озера может быть задан префикс "оз.":     "оз. Южное"
#         - для участка может быть задан постфикс "(га)": "1.2 (га)"
# При ошибке возвращает ноль,
# при успешном выполнении - последовательный номер
# найденной характеристики

    mapSemanticCodeLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCodeLabel', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSemanticCodeLabel(_info: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _maxsize: int, _number: int, _issystemdot: int) -> int:
        return mapSemanticCodeLabel_t (_info, _code, _place.buffer(), _maxsize, _number, _issystemdot)


# Запросить значение семантической характеристики объекта
# в виде числа с плавающей точкой двойной точности
# info    - идентификатор объекта карты в памяти
# code    - код характеристики,для которой ищется значение,
# number  - последовательный номер найденного значения,
#  не равен последовательному номеру характеристики !
#  например : код code имеют 3-я и 6-я характеристики,
#             соответственно для них number = 1 и 2,
#             а при number = 3  - код возврата будет ноль.
# Если значение семантики не может быть преобразовано
# к числовому виду или не найдено - возвращает ноль

    mapSemanticCodeDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSemanticCodeDoubleValue', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSemanticCodeDoubleValue(_info: maptype.HOBJ, _code: int, _number: int) -> float:
        return mapSemanticCodeDoubleValue_t (_info, _code, _number)


# Запросить значение семантической характеристики объекта в виде целого числа
# info    - идентификатор объекта карты в памяти
# code    - код характеристики,для которой ищется значение,
# number  - последовательный номер найденного значения,
#  не равен последовательному номеру характеристики !
#  например : код code имеют 3-я и 6-я характеристики,
#             соответственно для них number = 1 и 2,
#             а при number = 3  - код возврата будет ноль.
# Если значение семантики не может быть преобразовано
# к числовому виду или не найдено - возвращает ноль

    mapSemanticCodeLongValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCodeLongValueEx', maptype.HOBJ, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapSemanticCodeLongValueEx(_info: maptype.HOBJ, _code: int, _value: ctypes.POINTER(ctypes.c_int), _number: int) -> int:
        return mapSemanticCodeLongValueEx_t (_info, _code, _value, _number)

    mapSemanticCodeLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCodeLongValue', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSemanticCodeLongValue(_info: maptype.HOBJ, _code: int, _number: int) -> int:
        return mapSemanticCodeLongValue_t (_info, _code, _number)


# Запросить значение семантической характеристики объекта
# в символьном раскодированном виде
# info    - идентификатор объекта карты в памяти
# code    - код характеристики,для которой ищется значение,
# place   - адрес буфера для размещения строки,
# maxsize - размер буфера в байтах
# number  - последовательный номер найденного значения,
#  не равен последовательному номеру характеристики !
#  например : код code имеют 3-я и 6-я характеристики,
#             соответственно для них number = 1 и 2,
#             а при number = 3  - код возврата будет ноль.
# При ошибке возвращает ноль,
# при успешном выполнении - последовательный номер
# найденной характеристики

    mapSemanticCodeValueNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCodeValueNameUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapSemanticCodeValueNameUn(_info: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _maxsize: int, _number: int) -> int:
        return mapSemanticCodeValueNameUn_t (_info, _code, _place.buffer(), _maxsize, _number)


# Запросить название семантической характеристики объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapSemanticNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticNameUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSemanticNameUn(_info: maptype.HOBJ, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticNameUn_t (_info, _number, _name.buffer(), _size)


# Запросить полное название семантической характеристики объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapSemanticFullName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticFullName', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSemanticFullName(_info: maptype.HOBJ, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticFullName_t (_info, _number, _name.buffer(), _size)


# Запросить код семантической характеристики объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики (c 1)
# При ошибке возвращает ноль

    mapSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticCode', maptype.HOBJ, ctypes.c_int)
    def mapSemanticCode(_info: maptype.HOBJ, _number: int) -> int:
        return mapSemanticCode_t (_info, _number)


# Запросить последовательный номер кода семантической
# характеристики объекта (c 1)
# info    - идентификатор объекта карты в памяти
# code    - код семантической характеристики в классификаторе
# При ошибке возвращает ноль

    mapSemanticNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticNumber', maptype.HOBJ, ctypes.c_int)
    def mapSemanticNumber(_info: maptype.HOBJ, _code: int) -> int:
        return mapSemanticNumber_t (_info, _code)


# Запросить количество записей в классификаторе
# семантики по коду семантики
# info    - идентификатор объекта карты в памяти
# code - код семантики (семантика типа "TCODE")
# При ошибке возвращает ноль

    mapSemanticClassificatorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticClassificatorCount', maptype.HOBJ, ctypes.c_int)
    def mapSemanticClassificatorCount(_info: maptype.HOBJ, _code: int) -> int:
        return mapSemanticClassificatorCount_t (_info, _code)


# Запросить название значения характеристики из
# классификатора семантики по коду и
# последовательному номеру в классификаторе
# info    - идентификатор объекта карты в памяти
# number - последовательный номер в классификаторе(1,2,3...)
# code - код семантики
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает адрес пустой строки,
# при успешном выполнении - адрес строки

    mapSemanticClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticClassificatorNameUn', maptype.HOBJ, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSemanticClassificatorNameUn(_info: maptype.HOBJ, _code: int, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticClassificatorNameUn_t (_info, _code, _number, _name.buffer(), _size)


# Запросить код значения характеристики из
# классификатора семантики по коду и
# последовательному номеру в классификаторе
# info   - идентификатор объекта карты в памяти
# number - последовательный номер в классификаторе(1,2,3...)
# code   - внешний код семантики
# При ошибке возвращает ноль

    mapSemanticClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSemanticClassificatorCode', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSemanticClassificatorCode(_info: maptype.HOBJ, _code: int, _number: int) -> int:
        return mapSemanticClassificatorCode_t (_info, _code, _number)


# ############################################################
#                                                            #
#      РЕДАКТИРОВАНИЕ СЕМАНТИКИ (АТРИБУТОВ) ОБ'ЕКТА          #
#                                                            #
# ############################################################
# Запросить имеются ли семантики, которые еще могут быть
# добавлены для данного объекта
# Результат запроса изменяется в процессе редактирования семантики объекта !
# (некоторые характеристики могут присваиваться только один раз)
# При ошибке возвращает ноль

    mapIsAvailableSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsAvailableSemantic', maptype.HOBJ)
    def mapIsAvailableSemantic(_info: maptype.HOBJ) -> int:
        return mapIsAvailableSemantic_t (_info)


# Запросить количество видов семантик, которые еще могут быть
# добавлены для данного объекта
# Изменяется в процессе редактирования семантики объекта !
# (некоторые характеристики могут присваиваться только один раз)
# info    - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapAvailableSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAvailableSemanticCount', maptype.HOBJ)
    def mapAvailableSemanticCount(_info: maptype.HOBJ) -> int:
        return mapAvailableSemanticCount_t (_info)


# Запросить внешний код доступной семантики на объект
# по последовательному номеру доступных семантик
# Изменяется в процессе редактирования семантики объекта !
# info    - идентификатор объекта карты в памяти
# number - последовательный номер доступных семантик (1,2,3...)
# При ошибке возвращает ноль

    mapAvailableSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAvailableSemanticCode', maptype.HOBJ, ctypes.c_int)
    def mapAvailableSemanticCode(_info: maptype.HOBJ, _number: int) -> int:
        return mapAvailableSemanticCode_t (_info, _number)


# Запросить список внешних кодов доступных семантик на объект
# Изменяется в процессе редактирования семантики объекта !
# info    - идентификатор объекта карты в памяти
# buffer  - указатель на область памяти для размещения списка кодов семантик
# count   - максимальное число элементов в списке (размер буфера деленный на 4)
# При ошибке возвращает ноль

    mapAvailableSemanticList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAvailableSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapAvailableSemanticList(_info: maptype.HOBJ, _buffer: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
        return mapAvailableSemanticList_t (_info, _buffer, _count)


# Запросить список внешних кодов доступных обязательных семантик на объект
# Изменяется в процессе редактирования семантики объекта !
# info    - идентификатор объекта карты в памяти
# buffer  - указатель на область памяти для размещения списка кодов семантик
# count   - максимальное число элементов в списке (размер буфера деленный на sizeof(long int))
# При ошибке возвращает ноль

    mapAvailableMustSemanticList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAvailableMustSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapAvailableMustSemanticList(_info: maptype.HOBJ, _buffer: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
        return mapAvailableMustSemanticList_t (_info, _buffer, _count)


# Добавить новую характеристику в семантику объекта
# info    - идентификатор объекта карты в памяти
# code    - внешний код характеристики
# value   - адрес строки,содержащей новое значение
#           в символьном виде, числа с плавающей точкой могут иметь
#           разделителем только символ точка "."
# size    - длина добавляемой строки в байтах или ноль
# Для семантики числового типа значения будут преобразовываться в двоичный вид
# Если такая семантика была и она не повторяемая - значение заменяется
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSemantic', maptype.HOBJ, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapAppendSemantic(_info: maptype.HOBJ, _code: int, _value: ctypes.c_char_p, _size: int) -> int:
        return mapAppendSemantic_t (_info, _code, _value, _size)


# Добавить характеристику в семантику объекта в кодировке UTF-16
# info    - идентификатор объекта карты в памяти
# code    - внешний код характеристики
# value   - значение характеристики в кодировке UTF-16
# size    - длина добавляемой строки в байтах, если нужно добавить подстроку,
#           или ноль - размер будет определен автоматически до замыкающего нуля
# Если текст содержит латинские символы от 0x0001 до 0x007E
# или кириллицу (0x0400 - 0x045F) и на компьютере
# установлена русская Windows (OEM 866 или 1251), то текст
# автоматически запишется в ANSI, иначе строка сохранится в UTF-16
# Для семантики числового типа значения будут преобразовываться в двоичный вид
# Если такая семантика была и она не повторяемая - значение заменяется
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSemanticUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapAppendSemanticUn(_info: maptype.HOBJ, _code: int, _value: mapsyst.WTEXT, _size: int) -> int:
        return mapAppendSemanticUn_t (_info, _code, _value.buffer(), _size)


# Добавить произвольную характеристику в семантику объекта в кодировке UTF-16 с кодом 32862 (SEMSERVICECODE)
# Значение семантики запишется в виде строки "name:value"
# info    - идентификатор объекта карты в памяти
# name    - условное имя характеристики в кодировке UTF-16
# value   - значение характеристики в кодировке UTF-16
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendServiceSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendServiceSemantic', maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendServiceSemantic(_info: maptype.HOBJ, _name: mapsyst.WTEXT, _value: mapsyst.WTEXT) -> int:
        return mapAppendServiceSemantic_t (_info, _name.buffer(), _value.buffer())


# Добавить новую характеристику в семантику объекта,
# info    - идентификатор объекта карты в памяти
# code    - внешний код характеристики
# value   - значение в виде числа двойной точности
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticDouble_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSemanticDouble', maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapAppendSemanticDouble(_info: maptype.HOBJ, _code: int, _value: float) -> int:
        return mapAppendSemanticDouble_t (_info, _code, _value)


# Добавить новую характеристику в семантику объекта,
# info    - идентификатор объекта карты в памяти
# code    - внешний код характеристики
# value   - значение в виде целого числа
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticLong_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSemanticLong', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapAppendSemanticLong(_info: maptype.HOBJ, _code: int, _value: int) -> int:
        return mapAppendSemanticLong_t (_info, _code, _value)


# Удалить семантическую характеристику объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики,
#           если номер равен "-1", удаляются все характеристики
# При ошибке возвращает ноль

    mapDeleteSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSemantic', maptype.HOBJ, ctypes.c_int)
    def mapDeleteSemantic(_info: maptype.HOBJ, _number: int) -> int:
        return mapDeleteSemantic_t (_info, _number)


# Изменить значение кода семантической характеристики объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики
# code    - внешний код характеристики
# При ошибке возвращает ноль,
# иначе - внутренний код семантики

    mapSetSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticCode', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticCode(_info: maptype.HOBJ, _number: int, _code: int) -> int:
        return mapSetSemanticCode_t (_info, _number, _code)


# Изменить значение семантической характеристики объекта
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики,
# value   - новое значение семантики
# При ошибке возвращает ноль

    mapSetSemanticLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticLongValue', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetSemanticLongValue(_info: maptype.HOBJ, _number: int, _value: int) -> int:
        return mapSetSemanticLongValue_t (_info, _number, _value)

    mapSetSemanticDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticDoubleValue', maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapSetSemanticDoubleValue(_info: maptype.HOBJ, _number: int, _value: float) -> int:
        return mapSetSemanticDoubleValue_t (_info, _number, _value)


# Изменить значение семантической характеристики объекта в кодировке UNICODE
# info    - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики,
# place   - адрес строки, содержащей новое значение в UTF-16
#           Для семантики типа "классификатор" передается
#           код значения в виде числа в символьном виде.
# maxsize - длина добавляемой строки в байтах, если нужно добавить подстроку,
#           или ноль - размер будет определен автоматически до замыкающего нуля
# Семантика числового типа будет автоматически преобразовываться в двоичный вид
# При ошибке возвращает ноль

    mapSetSemanticValueUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSemanticValueUn', maptype.HOBJ, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSetSemanticValueUn(_info: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _maxsize: int) -> int:
        return mapSetSemanticValueUn_t (_info, _number, _place.buffer(), _maxsize)


# Изменить описание объекта при изменении семантических
# характеристик
# info    - идентификатор объекта карты в памяти
# Если вид объекта не изменился возвращает 0

    mapRedefineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRedefineObject', maptype.HOBJ)
    def mapRedefineObject(_info: maptype.HOBJ) -> int:
        return mapRedefineObject_t (_info)


# Обновить значения семантик типа формула при обновлении
# семантики или метрики объекта
# Данная функция автоматически вызывается при сохранении объекта (mapCommitObject)
# info    - идентификатор объекта карты в памяти
# mode - признак обновления семантики и метрики:
# 0 - обновилась только метрика, 1 - обновилась семантика
# При ошибке возвращает ноль

    mapUpdateSemanticByFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateSemanticByFormula', maptype.HOBJ, ctypes.c_int)
    def mapUpdateSemanticByFormula(_info: maptype.HOBJ, _mode: int) -> int:
        return mapUpdateSemanticByFormula_t (_info, _mode)


# #######################################################################
#      РЕДАКТИРОВАНИЕ СЕМАНТИКИ (АТРИБУТОВ) ОБ'ЕКТА -                   #
#  Создание символьной строки по форматированной строке                 #
#      с учетом значений семантики объекта                              #
# формат строки: после %# идет номер семантики, за ним в []- значение,  #
# которое будет вставлено в строку при отсутствии указанной семантики   #
# остальной текст в произвольной форме.                                 #
# Пример:входная строка - "дом N %#45[нет] сост. %#3[не заполнено]"     #
#     результат по значениям семантики для конкретного объекта          #
#     "дом N 5 сост. не заполнено" или "дом N 7-a сост. ЖИЛОЙ"          #
#      или  "дом N нет сост. не заполнено"                              #
# #######################################################################
# Разбор форматированной  строки на части
# value - входная строка,
# размеры строки не более 256.
# Нет символов форматирования или ошибки - возвращает 0,
# иначе идентификатор формулы в памяти (HFORMULA)
# Для каждого полученного и больше не используемого
# идентификатора HFORMULA необходим вызов функции mapFreeFormula()

    mapTakeStringToPiecesUn_t = mapsyst.GetProcAddress(acceslib,maptype.HFORMULA,'mapTakeStringToPiecesUn', maptype.PWCHAR)
    def mapTakeStringToPiecesUn(_value: mapsyst.WTEXT) -> maptype.HFORMULA:
        return mapTakeStringToPiecesUn_t (_value.buffer())


# Собрать символьную строку по идентификаторe HFORMULA
# с учетом семантик объекта
# info - идентификатор объекта карты в памяти
# outstring - строка для записи результата
# outsize   - размер строки
# При ошибке возвращает 0

    mapBuildFormulaStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildFormulaStringUn', maptype.HFORMULA, maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapBuildFormulaStringUn(_formula: maptype.HFORMULA, _info: maptype.HOBJ, _outstring: mapsyst.WTEXT, _outsize: int) -> int:
        return mapBuildFormulaStringUn_t (_formula, _info, _outstring.buffer(), _outsize)


# Освободить  идентификатор HFORMULA

    mapFreeFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeFormula', maptype.HFORMULA)
    def mapFreeFormula(_formula: maptype.HFORMULA) -> ctypes.c_void_p:
        return mapFreeFormula_t (_formula)


# ############################################################
#                                                            #
#         ЗАПРОС МЕТРИКИ (КООРДИНАТ) ОБ'ЕКТА                 #
#                                                            #
# ############################################################
# Запросить замкнутость объекта/подобъекта
# info   - идентификатор объекта карты в памяти
# number - номер подобъекта (для объекта - равен нулю)
# Возвращает:  0 - не замкнут, не 0 - замкнут

    mapGetExclusiveSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetExclusiveSubject', maptype.HOBJ, ctypes.c_int)
    def mapGetExclusiveSubject(_info: maptype.HOBJ, _number: int) -> int:
        return mapGetExclusiveSubject_t (_info, _number)


# Запрос габаритов объекта в метрах
# Габариты вычисляются по координатам объекта при каждом запросе
# info   - идентификатор объекта карты в памяти
# dframe - габариты метрики объекта в метрах в системе документа
# При ошибке возвращает ноль

    mapObjectFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectFrame', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrame(_info: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectFrame_t (_info, _dframe)


# Запрос габаритов объекта в радианах в системе WGS84
# Габариты вычисляются по координатам объекта при каждом запросе
# info   - идентификатор объекта карты в памяти
# dframe - габариты метрики объекта
# При ошибке возвращает ноль

    mapObjectFrameGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectFrameGeoWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrameGeoWGS84(_info: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectFrameGeoWGS84_t (_info, _dframe)


# Запросить габариты подобъекта в метрах (по метрике)
# Габариты вычисляются по координатам объекта при каждом запросе
# info   - идентификатор объекта карты в памяти
# dframe - габариты метрики объекта в метрах в системе документа
# subject - номер подобъекта (если = 0, обрабатывается контур объекта)
# При ошибке возвращает ноль

    mapSubjectFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSubjectFrame', maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def mapSubjectFrame(_info: maptype.HOBJ, _subject: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapSubjectFrame_t (_info, _subject, _dframe)


# Запрос/Пересчет габаритов изображения знака объекта (в метрах)
# Габариты считываются из заголовка объекта или перевычисляются по координатам объекта
# с учетом вида условного знака, если параметр force не равен нулю
# info   - идентификатор объекта карты в памяти
# dframe - габариты изображения объекта в метрах
# force  - признак принудительного пересчета габаритов (необходимо установить,
#          если объект редактировался, но не записан на карту)
# При ошибке возвращает ноль

    mapObjectViewFrameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectViewFrameEx', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapObjectViewFrameEx(_info: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME), _force: int) -> int:
        return mapObjectViewFrameEx_t (_info, _dframe, _force)


# Определяет габариты объектов (точечных, векторных и подписей) с учетом текущих
# условий отображения (см. функции mapGetRealShowScale/mapSetRealShowScale и
# mapGetScaleMethod/mapSetScaleMethod)
# Для каждого подобъекта подписи создается прямоугольный подобъект,
# ограничивающий текст подписи
# info    - исходный объект
# contour - объект, в который заносятся габариты исходного объекта
# hPaint  - идентификатор контекста отображения для многопоточного вызова функции
#           отображения (может быть ноль)
# При ошибке возвращает 0

    mapGetObjectContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectContour', maptype.HOBJ, maptype.HOBJ, maptype.HPAINT)
    def mapGetObjectContour(_info: maptype.HOBJ, _contour: maptype.HOBJ, _hPaint: maptype.HPAINT) -> int:
        return mapGetObjectContour_t (_info, _contour, _hPaint)


# Запрос числа точек метрики объекта/подобъекта
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта (если = 0, обрабатывается объект)
#           (если = -1, вернуть общее число точек всех контуров объекта)
# При ошибке возвращает ноль

    mapPointCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPointCount', maptype.HOBJ, ctypes.c_int)
    def mapPointCount(_info: maptype.HOBJ, _subject: int) -> int:
        return mapPointCount_t (_info, _subject)


# Запрос числа составных частей (подобъектов + 1)
# info    - идентификатор объекта карты в памяти
# Если подобъектов нет - возвращает 1 (только объект)
# При ошибке возвращает ноль

    mapPolyCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPolyCount', maptype.HOBJ)
    def mapPolyCount(_info: maptype.HOBJ) -> int:
        return mapPolyCount_t (_info)


# Запросить координаты точки в системе координат документа
# number - номер точки (начинается с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapGetPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapGetPlanePoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetPlanePoint_t (_info, _point, _number, _subject)


# Запрос координат точки в метрах в системе координат карты
# number - номер точки
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapGetMapPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapGetMapPlanePoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetMapPlanePoint_t (_info, _point, _number, _subject)


# Запрос координаты точки объекта в прямоугольной системе
# в метрах на местности
# info    - идентификатор объекта карты в памяти
# number - номер точки (начинается с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Функции реализованы через вызов mapGetPlanePoint()
# При ошибке возвращает ноль

    mapHPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapHPlane', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapHPlane(_info: maptype.HOBJ, _number: int = 1, _subject: int = 0) -> float:
        return mapHPlane_t (_info, _number, _subject)

    mapHPlaneEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapHPlaneEx', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapHPlaneEx(_info: maptype.HOBJ, _number: int, _subject: int, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapHPlaneEx_t (_info, _number, _subject, _h)


# Запросить измерение (свойство) точки метрики
# number - номер точки (начинается с 1)
# m       - измерение в формате double (для типа метрики IDDOUBLE4)
# f       - измерение в формате __int64 (для типа метрики IDDOUBLE4F)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapMValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapMValue', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapMValue(_info: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapMValue_t (_info, _number, _subject)

    mapFValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapFValue', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapFValue(_info: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapFValue_t (_info, _number, _subject)


# Запросить геодезические координаты точки в радианах в системе документа
# number - номер точки (начинается с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapGetGeoPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapGetGeoPoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetGeoPoint_t (_info, _point, _number, _subject)


# Запросить геодезические координаты точки в радианах в системе координат карты
# number - номер точки (начинается с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapGetMapGeoPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapGetMapGeoPoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetMapGeoPoint_t (_info, _point, _number, _subject)


# Запросить геодезические координаты точки в радианах на эллипсоиде WGS84
# number - номер точки (начинается с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapGetGeoPointWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetGeoPointWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def mapGetGeoPointWGS84(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetGeoPointWGS84_t (_info, _point, _number, _subject)

    mapGetGeoPointWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetGeoPointWGS843D', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)
    def mapGetGeoPointWGS843D(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _heigth: ctypes.POINTER(ctypes.c_double), _number: int, _subject: int) -> int:
        return mapGetGeoPointWGS843D_t (_info, _point, _heigth, _number, _subject)


# Запросить имеет ли объект 3-ехмерную метрику
# info    - идентификатор объекта карты в памяти
# Если да, возвращает ненулевое значение

    mapIsObject3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObject3D', maptype.HOBJ)
    def mapIsObject3D(_info: maptype.HOBJ) -> int:
        return mapIsObject3D_t (_info)


# Запросить является ли объект мультиполигоном
# Мультиполигон - это площадной объект, у которого некоторые подобъекты
# могут быть вне границ объекта
# При подсчете площади мультиполигона площадь внешних подобъектов
# будет добавляться к площади основного объекта, а площади
# внутренних подобъектов - вычитаться
# info    - идентификатор объекта карты в памяти
# Если да, возвращает ненулевое значение

    mapIsMultiPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMultiPolygon', maptype.HOBJ)
    def mapIsMultiPolygon(_info: maptype.HOBJ) -> int:
        return mapIsMultiPolygon_t (_info)


# Установить/Сбросить признак мультиполигона
# info  - идентификатор объекта карты в памяти
# multi - признак мультиполигона 0/1
# isautoset - признак автоматической расстановки флага размещения (входимости) 0/1
# При первой установке признака мультиполигона может выполняться автоматическая
# расстановка флага размещения подобъекта по первой точке метрики подобъекта -
# поиск входимости одних подобъектов в другие
# Если установку флагов размещения выполняет внешняя функция, то
# признак мультиполигона может устанавливаться после завершения создания
# объекта и всех подобъектов без автоматической расстановки,
# затем выполняется установка флагов подобъектов в функции mapSetSubjectMultiFlag
# ischeckobject - проверить, что объект не входит в какой-либо подобъект и
#                 перенести этот подобъект перед объектом при необходимости (сделать главным),
#                 если в главном (нулевом) контуре меньше 4 точек, то он удаляется.
# При ошибке возвращает ноль

    mapSetMultiPolygonAndCheckObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMultiPolygonAndCheckObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetMultiPolygonAndCheckObject(_info: maptype.HOBJ, _multi: int, _isautoset: int, _ischeckobject: int) -> int:
        return mapSetMultiPolygonAndCheckObject_t (_info, _multi, _isautoset, _ischeckobject)


# Запросить флаг размещения подобъекта вне объекта
# info  - идентификатор объекта карты в памяти
# subject - номер подобъекта, если 0 - запрос для объекта
# Для внешних подобъектов возвращает отрицательное значение (-1),
# для внутренних подобъектов возвращает номер внешнего подобъекта (c 0), в который
# входит данный подобъект
# При отсутствии описания возвращает ноль

    mapGetSubjectMultiFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSubjectMultiFlag', maptype.HOBJ, ctypes.c_int)
    def mapGetSubjectMultiFlag(_info: maptype.HOBJ, _subject: int) -> int:
        return mapGetSubjectMultiFlag_t (_info, _subject)


# Установить флаг размещения подобъекта вне объекта
# info  - идентификатор объекта карты в памяти
# subject - номер подобъекта, если 0 - запрос для объекта
# flag    - признак размещения (входимости) подобъекта
# Для внешних подобъектов устанавливается отрицательное значение (-1),
# для внутренних подобъектов устанавливается номер внешнего подобъекта (c 0), в который
# входит данный подобъект
# При отсутствии описания возвращает ноль

    mapSetSubjectMultiFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSubjectMultiFlag', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetSubjectMultiFlag(_info: maptype.HOBJ, _subject: int, _flag: int) -> int:
        return mapSetSubjectMultiFlag_t (_info, _subject, _flag)


# Запросить число внешних контуров в объекте
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetMultiSubjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMultiSubjectCount', maptype.HOBJ)
    def mapGetMultiSubjectCount(_info: maptype.HOBJ) -> int:
        return mapGetMultiSubjectCount_t (_info)


# Запросить - это мультимасштабный объект?
# Мультимасштабный объект имеет несколько контуров для разных масштабов
# Мультимасштабные объекты могут формироваться при сортировке карты,
# если задана соответствующая опция и в классификаторе карты объект
# имеет свойство "мультимасштабный"
# info    - идентификатор объекта карты в памяти
# Если да, возвращает ненулевое значение

    mapIsMultiContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMultiContour', maptype.HOBJ)
    def mapIsMultiContour(_info: maptype.HOBJ) -> int:
        return mapIsMultiContour_t (_info)


# Запросить является ли объект полигоном с центральной точкой
# Центральная точка - это подобъект с одной точкой, которая вычисляется
# в центре полигона, но может быть смещена оператором
# В этой точке отображается точечный знак, заданный в классификаторе
# info    - идентификатор объекта карты в памяти
# Если да, возвращает ненулевое значение

    mapIsPolygonWithPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsPolygonWithPoint', maptype.HOBJ)
    def mapIsPolygonWithPoint(_info: maptype.HOBJ) -> int:
        return mapIsPolygonWithPoint_t (_info)


# Запросить тип высоты в третьей координате
# Реально высота может быть и не задана
# (0 - абсолютная, иначе - относительная)

    mapGetHeightType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHeightType', maptype.HOBJ)
    def mapGetHeightType(_info: maptype.HOBJ) -> int:
        return mapGetHeightType_t (_info)


# Проверить, что третья координата метрики содержит допустимые значения абсолютной высоты
# (значения больше -111111.0)
# При отсутствии допустимых значений возвращает ноль

    mapCheckHeightCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckHeightCorrect', maptype.HOBJ)
    def mapCheckHeightCorrect(_info: maptype.HOBJ) -> int:
        return mapCheckHeightCorrect_t (_info)


# Установить тип высоты в третьей координате
# Значение высоты может быть установлено позднее
# (0 - абсолютная, иначе - относительная)
# Объекты с относительной высотой не влияют на построение матрицы высот
# Например - трубопроводы наземные и подземные

    mapSetHeightType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetHeightType', maptype.HOBJ, ctypes.c_int)
    def mapSetHeightType(_info: maptype.HOBJ, _type: int) -> int:
        return mapSetHeightType_t (_info, _type)


# Определить центр объекта
# info  - идентификатор объекта карты в памяти
# x, y  - расчитанные координаты центра объекта в метрах в системе документа
# type - тип алгоритма определения центра контура:
#        0 - для полигона строится линия сечения по центру вертикальных габаритов объекта
#            с поиском середины отрезка сечения; для линии ищется примерная середина контура по всей длине
#        1 - для полигона вычисляется геометрическое среднее значение контура объекта,
#            для остальных объектов вычисляется геометрическое среднее значение координат всех точек
# При ошибке возвращает ноль

    mapGetObjectCenterEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectCenterEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)
    def mapGetObjectCenterEx(_hmap: maptype.HMAP, _info: maptype.HOBJ, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _type: int = 0) -> int:
        return mapGetObjectCenterEx_t (_hmap, _info, _x, _y, _type)


# Запросить - совпадают ли координаты объектов (с точностью DELTANULL)
# info  - идентификатор исходного объекта карты в памяти
# another - идентификатор исходного объекта карты в памяти для сравнения метрики
# При совпадении возвращает ненулевое значение

    mapIsObjectDataEquivalent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectDataEquivalent', maptype.HOBJ, maptype.HOBJ)
    def mapIsObjectDataEquivalent(_info: maptype.HOBJ, _another: maptype.HOBJ) -> int:
        return mapIsObjectDataEquivalent_t (_info, _another)


# Запросить - используется ли общий буфер метрики для работы с векторными картами
# Общий буфер применяется на 32-разрядной платформе при работе с большим числом
# одновременно открытых векторных карт
# В этом случае многопоточный режим использования MAPAPI-функций не применим

    mapIsCommonBufferActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsCommonBufferActive')
    def mapIsCommonBufferActive() -> int:
        return mapIsCommonBufferActive_t ()


# Включить/Отключить доступ к общему буферу векторных карт для работы с большими объемами данных
# Общий буфер не рекомендуется применять для многопоточных приложений
# Возвращает значение флага доступа, который был до вызова функции

    mapHideCommonBuffer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapHideCommonBuffer', ctypes.c_int)
    def mapHideCommonBuffer(_hide: int) -> int:
        return mapHideCommonBuffer_t (_hide)


# ############################################################
#                                                            #
#      РЕДАКТИРОВАНИЕ МЕТРИКИ (КООРДИНАТ) ОБ'ЕКТА            #
#                                                            #
# ############################################################
# Добавить в конец метрики объекта точку
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат задано в метрах на местности
# Для изменения координаты Н необходимо далее
# выполнить функцию SetHPlane(...)
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointPlane(_info: maptype.HOBJ, _x: float, _y: float, _subject: int = 0) -> int:
        return mapAppendPointPlane_t (_info, _x, _y, _subject)


# Добавить в конец метрики объекта точку в прямоугольной системе в метрах на местности в проекции карты
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат задано в метрах на местности
# Для изменения координаты Н необходимо далее
# выполнить функцию SetHPlane(...)
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendMapPointPlane(_info: maptype.HOBJ, _x: float, _y: float, _subject: int = 0) -> int:
        return mapAppendMapPointPlane_t (_info, _x, _y, _subject)


# Добавить в конец метрики объекта точку
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# h       - высота (абсолютная или относительная) в метрах
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointPlane3D(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _subject: int = 0) -> int:
        return mapAppendPointPlane3D_t (_info, _x, _y, _h, _subject)


# Добавить в конец метрики объекта точку и измерение (свойство) в точке
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# h       - высота (абсолютная или относительная) в метрах
# m       - измерение в формате double (для типа метрики IDDOUBLE4)
# f       - измерение в формате __int64 (для типа метрики IDDOUBLE4F)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane4D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointPlane4D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointPlane4D(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _m: float, _subject: int) -> int:
        return mapAppendPointPlane4D_t (_info, _x, _y, _h, _m, _subject)

    mapAppendPointPlane4F_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointPlane4F', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int64, ctypes.c_int)
    def mapAppendPointPlane4F(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _f: int, _subject: int) -> int:
        return mapAppendPointPlane4F_t (_info, _x, _y, _h, _f, _subject)


# Удалить заданную точку метрики
# info    - идентификатор объекта карты в памяти
# number  - номер точки (с 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapDeletePointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeletePointPlane', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapDeletePointPlane(_info: maptype.HOBJ, _number: int, _subject: int = 0) -> int:
        return mapDeletePointPlane_t (_info, _number, _subject)


# Удаление из метрики одинаковых точек
# precision - величина расхождения значений координат в метрах на местности
# height    - признак учета трехмерной метрики (в этом случае две одинаковые
#             точки с разной высотой считаются разными)
# При ошибке возвращает 0

    mapDeleteEqualPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteEqualPoint', maptype.HOBJ, ctypes.c_double, ctypes.c_int)
    def mapDeleteEqualPoint(_info: maptype.HOBJ, _precision: float, _height: int) -> int:
        return mapDeleteEqualPoint_t (_info, _precision, _height)


# Удалить из объекта/подобъекта участок с точки number1 по точку number2
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Текущей становится точка следующая за удаленными
# При удалении всех точек объекта/подобъекта удаляется только метрика,
# объект/подобъект не удаляется

    mapDeletePartObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeletePartObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapDeletePartObject(_info: maptype.HOBJ, _number1: int, _number2: int, _subject: int = 0) -> int:
        return mapDeletePartObject_t (_info, _number1, _number2, _subject)


# Вставить в метрику объекта точку
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# number  - номер точки за которой будет добавлена новая точка
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат задано в метрах на местности
# Для изменени координаты Н необходимо далее
# выполнить функцию mapSetHPlane(...)
# При ошибке возвращает ноль

    mapInsertPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsertPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapInsertPointPlane(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapInsertPointPlane_t (_info, _x, _y, _number, _subject)


# Вставить в метрику объекта точку
# в прямоугольной системе в метрах на местности в проекции карты
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# number  - номер точки за которой будет добавлена новая точка
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат задано в метрах на местности
# Для изменени координаты Н необходимо далее
# выполнить функцию mapSetHPlane(...)
# При ошибке возвращает ноль

    mapInsertMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsertMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapInsertMapPointPlane(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapInsertMapPointPlane_t (_info, _x, _y, _number, _subject)


# Изменить координаты точки метрики
# Значение координат задано в метрах на местности
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# number  - номер точки (c 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapUpdatePointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlane(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane_t (_info, _x, _y, _number, _subject)

    mapUpdatePointPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlane3D(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3D_t (_info, _x, _y, _h, _number, _subject)


# Изменить координаты точки метрики
# в прямоугольной системе в метрах на местности в проекции карты
# info    - идентификатор объекта карты в памяти
# x,y     - координаты точки в метрах
# number  - номер точки
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapUpdateMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdateMapPointPlane(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        return mapUpdateMapPointPlane_t (_info, _x, _y, _number, _subject)


# Добавить в конец метрики объекта точку
# info    - идентификатор объекта карты в памяти
# b,l     - координаты точки в радианах в системе координат документа
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат должно соответствовать системе координат,
# проекции и эллипсоиду карты
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointGeo(_info: maptype.HOBJ, _b: float, _l: float, _subject: int = 0) -> int:
        return mapAppendPointGeo_t (_info, _b, _l, _subject)


# Добавить в конец метрики объекта точку
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат задано в радианах на эллипсоиде WGS84
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointGeoWGS84', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointGeoWGS84(_info: maptype.HOBJ, _b: float, _l: float, _subject: int) -> int:
        return mapAppendPointGeoWGS84_t (_info, _b, _l, _subject)

    mapAppendPointGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendPointGeoWGS843D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapAppendPointGeoWGS843D(_info: maptype.HOBJ, _b: float, _l: float, _h: float, _subject: int) -> int:
        return mapAppendPointGeoWGS843D_t (_info, _b, _l, _h, _subject)


# Вставить в метрику объекта точку
# info    - идентификатор объекта карты в памяти
# b,l     - координаты точки в радианах
# number - номер точки за которой будет добавлена новая точка
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат должно соответствовать системе координат,
# проекции и эллипсоиду карты
# Для изменения координаты Н необходимо далее
# выполнить функцию HPlane(...)
# При ошибке возвращает ноль

    mapInsertPointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsertPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapInsertPointGeo(_info: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int = 0) -> int:
        return mapInsertPointGeo_t (_info, _b, _l, _number, _subject)


# Изменить координаты точки метрики
# info    - идентификатор объекта карты в памяти
# b,l     - координаты точки в радианах
# number  - номер обновляемой точки
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Значение координат должно соответствовать системе координат,
# проекции и эллипсоиду карты
# При ошибке возвращает ноль

    mapUpdatePointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointGeo(_info: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointGeo_t (_info, _b, _l, _number, _subject)

    mapUpdatePointGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointGeo3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointGeo3D(_info: maptype.HOBJ, _b: float, _l: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointGeo3D_t (_info, _b, _l, _h, _number, _subject)


# Изменить координаты общей точки метрики у данного объекта и
# у всех объектов карты, имеющих такую точку
# Изменение выполняется после вызова mapCommitObject()
# или mapCommitWithPlace()
# Значение координат задано в метрах на местности
# info    - идентификатор объекта карты в памяти
# x,y,h   - координаты точки в метрах
# number  - номер точки (c 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapUpdatePointPlaneInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlaneInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlaneInMap(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlaneInMap_t (_info, _x, _y, _number, _subject)

    mapUpdatePointPlane3DInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlane3DInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlane3DInMap(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3DInMap_t (_info, _x, _y, _h, _number, _subject)


# Изменить координаты общей точки метрики у данного объекта и
# у всех объектов общего слоя,  имеющих такую точку
# Изменение выполняется после вызова mapCommitObject()
# или mapCommitWithPlace()
# Значение координат задано в метрах на местности
# info    - идентификатор объекта карты в памяти
# x,y,h   - координаты точки в метрах
# number  - номер точки
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapUpdatePointPlaneInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlaneInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlaneInLayer(_info: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlaneInLayer_t (_info, _x, _y, _number, _subject)

    mapUpdatePointPlane3DInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdatePointPlane3DInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapUpdatePointPlane3DInLayer(_info: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3DInLayer_t (_info, _x, _y, _h, _number, _subject)


# Редактирование координаты точки объекта/подобъекта
# в прямоугольной системе в метрах на местности
# info    - идентификатор объекта карты в памяти
# x,y,h   - координаты точки в метрах
# number  - номер точки (c 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapSetXPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetXPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSetXPlane(_info: maptype.HOBJ, _x: float, _number: int, _subject: int = 0) -> int:
        return mapSetXPlane_t (_info, _x, _number, _subject)

    mapSetYPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetYPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSetYPlane(_info: maptype.HOBJ, _y: float, _number: int, _subject: int = 0) -> int:
        return mapSetYPlane_t (_info, _y, _number, _subject)


# Редактирование высоты точки объекта/подобъекта в метрах
# Тип высоты может быть запрошен функцией mapGetHeightType
# Система высот устанавливается в паспорте карты (HEIGHTSYSTEM)
# info    - идентификатор объекта карты в памяти
# h       - высота точки в метрах
# number  - номер точки (c 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Если объект имеет двухмерную метрику (mapIsObject3D() == 0),
# состояние координат не изменяется
# При ошибке возвращает ноль

    mapSetHPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetHPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSetHPlane(_info: maptype.HOBJ, _h: float, _number: int, _subject: int = 0) -> int:
        return mapSetHPlane_t (_info, _h, _number, _subject)


# Изменить измерение (свойство) точки метрики
# info    - идентификатор объекта карты в памяти
# m       - измерение в формате double (для типа метрики IDDOUBLE4)
# f       - измерение в формате __int64 (для типа метрики IDDOUBLE4F)
# number  - номер точки (c 1)
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapSetMValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMValue', maptype.HOBJ, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def mapSetMValue(_info: maptype.HOBJ, _m: float, _number: int, _subject: int) -> int:
        return mapSetMValue_t (_info, _m, _number, _subject)

    mapSetFValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFValue', maptype.HOBJ, ctypes.c_int64, ctypes.c_int, ctypes.c_int)
    def mapSetFValue(_info: maptype.HOBJ, _f: int, _number: int, _subject: int) -> int:
        return mapSetFValue_t (_info, _f, _number, _subject)


# Создать дескриптор подобъекта в записи метрики
# В конец записи добавляется дескриптор подобъекта с нулевым числом точек
# Если предыдущий подобъект не содержит ни одной точки, то новый подобъект не
# будет создан
# info    - идентификатор объекта карты в памяти
# Возвращает номер созданного подобъекта (с 1)
# При ошибке возвращает ноль

    mapCreateSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateSubject', maptype.HOBJ)
    def mapCreateSubject(_info: maptype.HOBJ) -> int:
        return mapCreateSubject_t (_info)


# Удалить подобъект в записи метрики
# info   - идентификатор объекта карты в памяти
# number - номер удаляемого подобъекта (с 1),
# если равен (-1), то удаляется вся метрика объекта вместе с подобъектами
# Текущей становится первая точка объекта
# При ошибке возвращает ноль

    mapDeleteSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSubject', maptype.HOBJ, ctypes.c_int)
    def mapDeleteSubject(_info: maptype.HOBJ, _number: int) -> int:
        return mapDeleteSubject_t (_info, _number)


# Добавить подобъект из указанной записи
# info   - идентификатор объекта карты в памяти
# source - идентификатор объекта карты в памяти, из которого добавляют подобъет
# number - номер добавляемого подобъекта или -1 (добавить все подобъекты)
# При ошибке возвращает 0

    mapAppendSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_int)
    def mapAppendSubject(_info: maptype.HOBJ, _source: maptype.HOBJ, _number: int) -> int:
        return mapAppendSubject_t (_info, _source, _number)


# Сместить все координаты метрики объекта на заданную
# величину (delta) в метрах
# info   - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapRelocateObjectPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRelocateObjectPlane', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRelocateObjectPlane(_info: maptype.HOBJ, _delta: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapRelocateObjectPlane_t (_info, _delta)


# Изменить направление цифрования подобъекта
# info  - идентификатор объекта карты в памяти
# number - номер подобъекта (с 0),
# При ошибке возвращает ноль, иначе - новое значение
# (OD_RIGHT,OD_LEFT,... - см. Maptype.h)

    mapChangeSubjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeSubjectDirect', maptype.HOBJ, ctypes.c_int)
    def mapChangeSubjectDirect(_info: maptype.HOBJ, _number: int) -> int:
        return mapChangeSubjectDirect_t (_info, _number)


# Изменить направление цифрования объекта
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль, иначе - новое значение
# (OD_RIGHT,OD_LEFT,... - см. Maptype.h)

    mapChangeObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeObjectDirect', maptype.HOBJ)
    def mapChangeObjectDirect(_info: maptype.HOBJ) -> int:
        return mapChangeObjectDirect_t (_info)


# Переформировать объект (подобъект), установив первой заданную точку
# number - номер точки
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает ноль

    mapSetFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFirstPoint', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetFirstPoint(_info: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapSetFirstPoint_t (_info, _number, _subject)


# Линейная фильтрация метрики
# info  - идентификатор объекта карты в памяти
# precision - точность в метрах
# Удаляет: 1. двойные точки метрики;
#          2. незамкнутые подобъекты < 2 точек;
#          3. замкнутые подобъекты < 4 точек;
#          4. точки метрики, лежащие в середине отрезка прямой
#             на расстоянии precision от прямой.
# Объект не удаляет никогда !!!
# Возвращает общее число точек метрики
# При ошибках возвращает:
#    0 - ошибка структуры
#   -1 - объект состоит из одной точки
#   -2 - объект состоит из двух одинаковых точек
#   -3 - число точек замкнутого контура объекта равно 3
#  -10 - число точек метрики превышает длину записи метрики

    mapLinearFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLinearFilter', maptype.HOBJ, ctypes.c_double)
    def mapLinearFilter(_info: maptype.HOBJ, _precision: float) -> int:
        return mapLinearFilter_t (_info, _precision)


# Фильтрация объекта с учетом топологических связей с соседними
# объектами листа карты, которому принадлежит объект
# (фильтруются и соседние объекты, имеющие общие точки;
#  концевые общие точки не фильтруются)
# hMap      - идентификатор открытых данных
# info      - фильтруемый объект
# precision - точность в метрах на местности
#             (минимальное расстояние от точки до прямой,
#              соединяющей предыдущую и следующую точки)
# При ошибке возвращает 0

    mapGeneralFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeneralFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralFilter(_hMap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        return mapGeneralFilter_t (_hMap, _hobj, _precision)


# Фильтрация всех объектов одного листа карты с учетом
# топологических связей с соседними объектами того же листа
# той же карты (фильтруются и соседние объекты, имеющие общие точки;
# концевые общие точки не фильтруются)
# hMap      - идентификатор открытых данных
# hSite     - идентификатор обрабатываемой карты
# list      - номер листа
# precision - точность в метрах на местности
#             (минимальное расстояние от точки до прямой,
#              соединяющей предыдущую и следующую точки)
# hwnd      - идентификатор окна,которое будет извещаться
#             (для отмены сообщений установить идентификатор в ноль)
# Процесс посылает сообщение WM_PROGRESSBARUN
# wparm : процент обработки,
# Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# При ошибке возвращает 0

    mapGeneralFilterInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeneralFilterInMap', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_double, maptype.HMESSAGE)
    def mapGeneralFilterInMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _precision: float, _hwnd: maptype.HMESSAGE) -> int:
        return mapGeneralFilterInMap_t (_hMap, _hSite, _list, _precision, _hwnd)


# Фильтрация двойных точек с учетом топологических связей
# с соседними объектами листа карты, которому принадлежит объект
# (фильтруются и соседние объекты, имеющие общие точки,
#  концевые общие точки не фильтруются)
# hMap      - идентификатор открытых данных
# info      - фильтруемый объект
# precision - минимальное расстояние между точками
# При ошибке возвращает 0

    mapGeneralDuplicatePointFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeneralDuplicatePointFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralDuplicatePointFilter(_hMap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        return mapGeneralDuplicatePointFilter_t (_hMap, _hobj, _precision)


# Генерализация метрики линейного или площадного объекта для выбранного масштаба
# scale         - масштаб генерализации метрики (1 : 100 000 соответствует сетке с шагом 100 м для сетки в 1 мм)
# force         - признак формирования минимальной метрики при вырождении
# Возвращает: 1 - метрика генерализирована успешно
#             2 - метрика не изменилась (исходные точки достаточно разряжены для заданного масштаба)
#            -1 - метрика не изменилась (объект вырождается или максимальное число точек подобъектов меньше 64)
# При ошибке возвращает 0

    mapObjectGeneralization_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectGeneralization', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapObjectGeneralization(_info: maptype.HOBJ, _scale: int, _force: int) -> int:
        return mapObjectGeneralization_t (_info, _scale, _force)


# Установить/Запросить шаг сетки в мм для генерализации контуров объектов в масштабе карты
# Возвращает установленное значение

    mapGetGeneralizationGridStep_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralizationGridStep')
    def mapGetGeneralizationGridStep() -> float:
        return mapGetGeneralizationGridStep_t ()

    mapSetGeneralizationGridStep_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetGeneralizationGridStep', ctypes.c_double)
    def mapSetGeneralizationGridStep(_step: float) -> float:
        return mapSetGeneralizationGridStep_t (_step)


# Создание сплайна - сглаживание объекта и всех его подобъектов
# Это сплайн, который проходит только
# через первую и последнюю точки объекта(подобъекта) и как бы
# сглаживает (спиливает) углы ломаной, соединяющей точки объекта
# (метрику исходного объекта/подобъекта).
# info  - исходная метрика объекта, по которому строится сплайн
# cashion   - условный процент спиливания
#             углов ломаной линии объекта (1<= cashion <= 50)
#             (метрика исходного объекта/подобъекта).
#             Чем больше cashion, тем больше спиливается угол
# smooth    - плавность кривой сплайна
#             (число точек между узлами объекта smooth >= 3).
#             Чем больше smooth,тем глаже смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического
#             определения точности установить значение "-1".
# Если исходный объект имел 3-ю координату (высоту),то у сплайна
# также есть высота (интерполяция для новых точек).
# При ошибке возвращает ноль

    mapCashionSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCashionSpline', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapCashionSpline(_info: maptype.HOBJ, _cashion: int, _smooth: int, _precision: float) -> int:
        return mapCashionSpline_t (_info, _cashion, _smooth, _precision)


# Создание сплайна - сглаживание подобъекта
# Это сплайн, который проходит только
# через первую и последнюю точки подобъекта и как бы
# сглаживает (спиливает) углы ломаной, соединяющей точки объекта
# (метрику исходного подобъекта).
# info  - исходная метрика объекта, по подобъекту которого строится сплайн
# subject - номер обрабатываемого подобъекта (0,1,2...)
# cashion   - условный процент спиливания
#             углов ломаной линии объекта (1<= cashion <= 50)
#             (метрика исходного подобъекта).
#             Чем больше cashion, тем больше спиливается угол
# smooth    - плавность кривой сплайна
#             (число точек между узлами подобъекта smooth >= 3).
#             Чем больше smooth,тем глаже смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического
#             определения точности установить значение "-1".
# Если исходный подобъект имел 3-ю координату (высоту),то у сплайна
# также есть высота

    mapCashionSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCashionSplineSubject', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapCashionSplineSubject(_info: maptype.HOBJ, _subject: int, _cashion: int, _smooth: int, _precision: float) -> int:
        return mapCashionSplineSubject_t (_info, _subject, _cashion, _smooth, _precision)


# Создание сплайна - огибание объекта и всех его подобъектов
# Это сплайн, который проходит через все точки исходного объекта
# (метрика исходного объекта) и огибает его. Исходный объект
# как бы вписан в сплайн.
# info  - исходная метрика объекта, по которому строится сплайн
# press     - максимальная амплитуда
#             отхода кривой сплайна от отрезка
#             в процентах от длины отрезка ( >= 5 ).
#             Чем больше press, тем более сплайн может
#             удаляться от отрезка ломаной (метрики исходного
#             объекта/подобъекта).
# smooth    - плавность кривой сплайна
#             (число точек между узлами объекта smooth >= 3).
#             Чем больше smooth,тем глаже смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического
#             определения точности установить значение "-1".
# Если исходный объект имел 3-ю координату (высоту),то у сплайна
# также есть высота (интерполяция для новых точек).
# При ошибке возвращает ноль

    mapBendSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBendSpline', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapBendSpline(_info: maptype.HOBJ, _press: int, _smooth: int, _precision: float) -> int:
        return mapBendSpline_t (_info, _press, _smooth, _precision)


# Создание сплайна - огибание подобъекта
# Это сплайн, который проходит
# через все точки исходного подобъекта и огибает его.
# Исходный объект как бы вписан в сплайн.
# info  - исходная метрика объекта, по которому строится сплайн
# subject - номер обрабатываемого подобъекта (0,1,2...)
# press     - максимальная амплитуда
#             отхода кривой сплайна от отрезка
#             в процентах от длины отрезка ( >= 5 ).
#             Чем больше press, тем более сплайн может
#             удаляться от отрезка ломаной (метрики исходного
#             объекта/подобъекта).
# smooth    - плавность кривой сплайна
#             (число точек между узлами объекта smooth >= 3).
#             Чем больше smooth,тем глаже смотрится линия
# precision - порог (точность) при фильтрации точек
# Если исходный подобъект имел 3-ю координату (высоту),то у сплайна
# также есть высота

    mapBendSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBendSplineSubject', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double)
    def mapBendSplineSubject(_info: maptype.HOBJ, _subject: int, _press: int, _smooth: int, _precision: float) -> int:
        return mapBendSplineSubject_t (_info, _subject, _press, _smooth, _precision)


# Сглаживание объекта с учетом топологических связей с соседними
# объектами листа карты, которому принадлежит объект
# hMap       - идентификатор открытых данных
# info       - фильтруемый объект
# press      - максимальная амплитуда отхода кривой сплайна от отрезка
#              в процентах от длины отрезка (>= 5), чем больше press,
#              тем больше сплайн может оклоняться от исходного контура
# smooth     - плавность кривой сплайна (>= 3) число точек между узлами объекта,
#              чем больше smooth, тем более гладким будет сплайн
# adjustdist - допуск согласования - максимальное расстояние, при котором две соседние
#              точки считаются расположенными на одном месте
# filterprec - уровень фильтрации (минимальное расстояние от точки до прямой,
#              соединяющей предыдущую и следующую точки)
# При ошибке возвращает ноль

    mapGeneralBendSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGeneralBendSpline', maptype.HMAP, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapGeneralBendSpline(_hMap: maptype.HMAP, _info: maptype.HOBJ, _press: int, _smooth: int, _adjustdist: float, _filterprec: float) -> int:
        return mapGeneralBendSpline_t (_hMap, _info, _press, _smooth, _adjustdist, _filterprec)


# Одномерный сглаживающий сплайн
# points - массив точек (одна из координат)
# count  - количество точек
# smooth - уровень сглаживания (0..1; 0 - прямая линия, 1 - кубический сплайн)
# При ошибке возвращает ноль

    mapSmoothingSpline1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothingSpline1', ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double)
    def mapSmoothingSpline1(_points: ctypes.POINTER(ctypes.c_double), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline1_t (_points, _count, _smooth)


# Двухмерный сглаживающий сплайн
# points - массив точек (x, y)
# count  - количество точек
# smooth - уровень сглаживания (0..1; 0 - прямая линия, 1 - кубический сплайн)
# При ошибке возвращает ноль

    mapSmoothingSpline2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothingSpline2', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_double)
    def mapSmoothingSpline2(_points: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline2_t (_points, _count, _smooth)


# Трёхмерный сглаживающий сплайн
# points - массив точек (x, y, h)
# count  - количество точек
# smooth - уровень сглаживания (0..1; 0 - прямая линия, 1 - кубический сплайн)
# При ошибке возвращает ноль

    mapSmoothingSpline3_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothingSpline3', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_int, ctypes.c_double)
    def mapSmoothingSpline3(_points: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline3_t (_points, _count, _smooth)


# Cглаживающий сплайн (2-х или 3-х мерный в зависимости от наличия высоты)
# info    - сглаживаемый объект
# subject - сглаживаемый подобъект
# smooth  - уровень сглаживания (0..1; 0 - прямая линия, 1 - кубический сплайн)
# При ошибке возвращает ноль

    mapSmoothingSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothingSplineSubject', maptype.HOBJ, ctypes.c_int, ctypes.c_double)
    def mapSmoothingSplineSubject(_info: maptype.HOBJ, _subject: int, _smooth: float) -> int:
        return mapSmoothingSplineSubject_t (_info, _subject, _smooth)


# Cглаживающий сплайн (2-х или 3-х мерный в зависимости от наличия высоты)
# info   - сглаживаемый объект
# smooth - уровень сглаживания (0..1; 0 - прямая линия, 1 - кубический сплайн)
# При ошибке возвращает ноль

    mapSmoothingSplineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSmoothingSplineObject', maptype.HOBJ, ctypes.c_double)
    def mapSmoothingSplineObject(_info: maptype.HOBJ, _smooth: float) -> int:
        return mapSmoothingSplineObject_t (_info, _smooth)


# Построить дугу заданного радиуса с центром
# в точке point2 (в метрах на местности)
# точки point1 и point3 задаются для определения
# направлений (в метрах на местности)
# hmap   - идентификатор открытых данных
# info   - идентификатор объекта карты в памяти
# radius - в метрах на местности
# метрика строится в info
# При ошибке возвращает 0

    mapCreateArc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateArc', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCreateArc(_hmap: maptype.HMAP, _info: maptype.HOBJ, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _point3: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float) -> int:
        return mapCreateArc_t (_hmap, _info, _point1, _point2, _point3, _radius)


# Построение зоны вокруг подобъекта
# radius  - радиус создаваемой зоны (в метрах на местности)
# info    - идентификатор копии объекта, по метрике которого строится зона.
#           В этот объект будет записана метрика построенной зоны.
# subject - номер подобъекта, вокруг которого строится зона
# form    - тип угла 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности)
#           рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла (рекомендуется 3)
# Если задан прямой тип угла, то внешний угол обрезается по расстоянию от узла по
# допуску radius#cornerfactor для устранения длинных углов
# side    - направление построения зоны (1-справа, 2-слева, 3-с обеих сторон)
# При ошибке возвращает ноль

    mapZoneObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapZoneObjectEx', ctypes.c_double, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapZoneObjectEx(_radius: float, _info: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int) -> int:
        return mapZoneObjectEx_t (_radius, _info, _subject, _form, _arcdist, _cornerfactor, _side)


# Построение зоны снаружи/внутри подобъекта
# radius  - радиус создаваемой зоны (в метрах на местности)
#           отрицательное значение - внутри объекта
#           положительное значение - снаружи объекта
# info    - идентификатор копии объекта, по метрике которого строится зона.
#           В этот объект будет записана метрика построенной зоны.
# subject - номер подобъекта, вокруг которого строится зона
# form    - тип угла 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности)
#           рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла (рекомендуется 3)
# Если тип угла прямой, то внешний угол обрезается по расстоянию от узла по
# допуску radius#cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapInsideZoneObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsideZoneObjectEx', ctypes.c_double, maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
    def mapInsideZoneObjectEx(_radius: float, _info: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float) -> int:
        return mapInsideZoneObjectEx_t (_radius, _info, _subject, _form, _arcdist, _cornerfactor)


# Построение половины зоны вокруг объекта / подобъекта
# (справа от объекта по направлению цифрования)
# radius    - радиус создаваемой зоны (в метрах на местности)
# info - метрика объекта, по которому строится зона
# subject - номер подобъекта, вокруг которого строим зону
# При ошибке возвращает ноль

    mapHalfZoneObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapHalfZoneObject', ctypes.c_double, maptype.HOBJ, ctypes.c_int)
    def mapHalfZoneObject(_radius: float, _info: maptype.HOBJ, _subject: int) -> int:
        return mapHalfZoneObject_t (_radius, _info, _subject)


# Построение зоны вокруг основного контура линейного незамкнутого
# Устаревшая функция, соответствует вызову
# return mapZoneObjectEx(radius, info, 0, 1, 0.001 # mapGetMapScale(hmap), 3., 3);
# объекта вида "змейка" (без учета подобъектов)
# radius - радиус создаваемой зоны (в метрах на местности)
# info   - метрика объекта, по которому строится зона.
#          Исходный объект делится на части, вокруг каждой части строится зона.
#          Отдельные зоны объединяются в одну
# В info записывается площадной объект - зона
# При ошибке возвращает ноль

    mapZoneLineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapZoneLineObject', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapZoneLineObject(_hmap: maptype.HMAP, _info: maptype.HOBJ, _radius: float) -> int:
        return mapZoneLineObject_t (_hmap, _info, _radius)


# Замкнуть  метрику объект и все его подобъекты для
# площадного или линейного объекта
# info  - идентификатор объекта карты в памяти
# delta - порог замыкания в мм на карте
# если расстояние между первой и последней точкой меньше delta, то
# вместо последней точки пишем первую
# если расстояние между первой и последней точкой больше delta, то
# после последней точки добавляем первую
# возврат - 1 - нормальное завершение
# При ошибке возвращает ноль

    mapAbridge_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAbridge', maptype.HOBJ, ctypes.c_double)
    def mapAbridge(_info: maptype.HOBJ, _delta: float) -> int:
        return mapAbridge_t (_info, _delta)


# Округлить метрику объекта по установленной точности карты (мм, см)
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapRoundObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRoundObject', maptype.HOBJ)
    def mapRoundObject(_info: maptype.HOBJ) -> int:
        return mapRoundObject_t (_info)


# Построение ортодромии
# first - координаты первой точки в радианах
# second - координаты второй точки в радианах
# array - адрес массива координат построенной ортодромии,
#         размер массива равен count
# count - количество точек для построения ортодромии (если точки размещены ближе 10-6 радиан, заполняет 2 точки)
# Возвращает заполненное число точек в массиве
# При ошибке возвращает ноль

    mapOrthodrome_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOrthodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapOrthodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        return mapOrthodrome_t (_first, _second, _array, _count)


# Построение ортодромии (дуга на поверхности Земли, задающая кратчайшее расстояние)
# между заданными точками
# info   - идентификатор объекта карты в памяти
# first  - координаты первой точки в радианах на текущем эллипсоиде документа (SetDocProjection)
# second - координаты второй точки в радианах
# При больших расстояниях точки дуги формируются с шагом не более 0,5 градуса,
# при малых растояниях - не чаще 10 километров, что обеспечивает определение
# длин и углов с точностью триангуляции 1 класса
# При ошибке возвращает ноль

    mapOrthodromeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOrthodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapOrthodromeObject(_info: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapOrthodromeObject_t (_info, _first, _second)


# Построение локсодромии (кривая, пересекающая все меридианы под постоянным углом)
# first - координаты первой точки в радианах
# second - координаты второй точки в радианах
# array - адрес массива координат построенной локсодромии,
#         размер массива равен count
# count - количество точек для построения локсодромии
# При ошибке возвращает ноль

    mapLoxodrome_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoxodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapLoxodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        return mapLoxodrome_t (_first, _second, _array, _count)


# Построение локсодромии (кривая, пересекающая все меридианы под постоянным углом)
# info   - идентификатор объекта карты в памяти
# first  - координаты первой точки в радианах на текущем эллипсоиде документа (SetDocProjection)
# second - координаты второй точки в радианах
# При ошибке возвращает ноль

    mapLoxodromeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoxodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLoxodromeObject(_info: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapLoxodromeObject_t (_info, _first, _second)


# Построить эллипс по двум точкам и параметрам полуосей
# Координаты точек в метрах в системе документа
# centre - координаты центра эллипсоид в метрах на местности
# bigaxis - большая полуось в метрах на местности
# littleaxis - малая полуось в метрах на местности
# angle - угол поворота большой полуоси в радианах против часовой стрелки
#         от направления на восток
# count - число точек метрики (от 16 до 256)
# Создаваемому объекту присваивается признак отображения сплайном,
# что позволяет минимизировать число точек метрики
# При ошибке возвращает ноль

    mapBuildEllipse_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildEllipse', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def mapBuildEllipse(_info: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _bigaxis: float, _littleaxis: float, _angle: float, _count: int) -> int:
        return mapBuildEllipse_t (_info, _center, _bigaxis, _littleaxis, _angle, _count)


# Построение зоны видимости по матрице высот в виде растрового изображения
# hmap - идентификатор открытой векторной карты
# rstname - полное имя растра
# zoneparm - параметры построения зоны (см.maptype.h)
# hpaint - контекст поддержки многопоточного вызова (см. mapCreatePaintControl)
# flags - флаги режимов (1 - запретить нанесение границы зоны на растр)
# Построение производится при наличии открытой матрицы высот
# Результат записывается в файл namerst
# Возвращает номер растра в цепочке
# При ошибке возвращает ноль

    mapVisibilityZonePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapVisibilityZonePro', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), maptype.HPAINT, ctypes.c_int)
    def mapVisibilityZonePro(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _zoneparm: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), _hPaint: maptype.HPAINT, _flags: int) -> int:
        return mapVisibilityZonePro_t (_hmap, _rstname.buffer(), _zoneparm, _hPaint, _flags)


# Определение видимости из точки point1 (координаты в метрах на местности) точку point2
# deltaheight  - высота наблюдения (в метрах),
# добавляется к высоте в точке point1
# Вычисление производится при наличии открытой матрицы высот
# Возвращает 0 - point2 не видна из point1
#            1 - point2 видна из point1

    mapVisibilityFromPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapVisibilityFromPoint', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapVisibilityFromPoint(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _deltaheight: float) -> int:
        return mapVisibilityFromPoint_t (_hmap, _point1, _point2, _deltaheight)


# Создание объектов - пустот по выделенным объектам
# hmap - идентификатор открытой векторной карты с выделенными объектами
# hsite - идентификатор пользовательской карты для записи объектов - пустот
# info   - идентификатор объекта карты в памяти, граница области для создания объектов - пустот
# incode - внутренний код объекта для сохранения объектов - пустот
# Возвращает количество созданных объектов
# При ошибке возвращает ноль

    mapCreateObjectVoid_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateObjectVoid', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int)
    def mapCreateObjectVoid(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _info: maptype.HOBJ, _incode: int) -> int:
        return mapCreateObjectVoid_t (_hmap, _hsite, _info, _incode)


# Удалить петли у объекта
# При ошибке возвращает ноль

    mapDeleteLoop_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteLoop', maptype.HOBJ, ctypes.c_double)
    def mapDeleteLoop(_info: maptype.HOBJ, _precision: float) -> int:
        return mapDeleteLoop_t (_info, _precision)


# Повернуть объект вокруг заданной в прямоугольной системе точки
# на заданный угол
# info   - идентификатор объекта карты в памяти
# center - координаты точки, вокруг которой поворачивается объект (метры)
# angle  - угол поворота против часовой стрелки (радианы, от -PI до +PI)
# При ошибке возвращает 0

    mapRotateObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRotateObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapRotateObject(_info: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapRotateObject_t (_info, _center, _angle)


# Оконтуривание объектов, удовлетворяющих условиям обобщенного поиска,
# по всем открытым векторным картам
# hmap - идентификатор главной карты
# hobj - объект в который записывается определенный контур
# precision - допуск согласования объектов (должен быть >= DELTANULL)
# При ошибке возвращает 0

    mapContourTotalSeekObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapContourTotalSeekObjects', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapContourTotalSeekObjects(_hmap: maptype.HMAP, _info: maptype.HOBJ, _precision: float) -> int:
        return mapContourTotalSeekObjects_t (_hmap, _info, _precision)


# Установить текущую точку замкнутого контура первой
# info    - идентификатор объекта карты в памяти
# number  - номер текущей точки (начиная с 1)
# subject - номер текущего контура (начиная с 0)
# При ошибке возвращает 0

    mapSetFirstPointOfLockedContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetFirstPointOfLockedContour', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetFirstPointOfLockedContour(_info: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapSetFirstPointOfLockedContour_t (_info, _number, _subject)


# ############################################################
#                                                            #
#      РЕДАКТИРОВАНИЕ ТЕКСТА ПОДПИСИ                         #
#                                                            #
# ############################################################
# Запросить содержание текстовой строки
# info    - идентификатор объекта карты в памяти
# text    - адрес для размещения строки
# size    - длина выделенной области под строку в байтах
# subject - номер подобъекта
# При ошибке возвращает ноль

    mapGetTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetTextUn(_info: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        return mapGetTextUn_t (_info, _text.buffer(), _size, _subject)


# Запросить длину в байтах строки, возвращаемой функцией mapGetTextUn
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта
# При ошибке возвращает ноль

    mapGetTextUnSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextUnSize', maptype.HOBJ, ctypes.c_int)
    def mapGetTextUnSize(_info: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextUnSize_t (_info, _subject)


# Запросить текст подписи, который будет реально отображаться на карте
# info    - идентификатор объекта карты в памяти
# text    - адрес для размещения строки
# size    - длина выделенной области под строку
# subject - номер подобъекта
# При ошибке возвращает 0

    mapGetShowText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetShowText', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetShowText(_info: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        return mapGetShowText_t (_info, _text.buffer(), _size, _subject)


# Установить новое содержание текстовой строки
# info   - идентификатор объекта карты в памяти
# text   - адрес новой строки UNICODE UTF-16
# Если текст содержит латинские символы от 0x0001 до 0x007E
# или кириллицу (0x0400 - 0x045F) и на компьютере
# установлена русская Windows (OEM 866 или 1251), то текст
# автоматически запишется в ANSI,
# иначе новое значение сохранится в UTF-16
# subject - номер подобъекта
# При ошибке возвращает ноль

    mapPutTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapPutTextUn(_info: maptype.HOBJ, _text: mapsyst.WTEXT, _subject: int) -> int:
        return mapPutTextUn_t (_info, _text.buffer(), _subject)


# Запросить - хранится ли текст в кодировке UNICODE
# info   - идентификатор объекта карты в памяти
# Если текст в UNICODE - возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsTextUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTextUnicode', maptype.HOBJ)
    def mapIsTextUnicode(_info: maptype.HOBJ) -> int:
        return mapIsTextUnicode_t (_info)


# Запросить длину текста в микронах на карте
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта
# При масштабируемой подписи возвращает 0
# При ошибке возвращает ноль

    mapGetTextLengthMkm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextLengthMkm', maptype.HOBJ, ctypes.c_int)
    def mapGetTextLengthMkm(_info: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextLengthMkm_t (_info, _subject)


# Запросить высоту строки текста для объектов типа подпись
# в микронах на карте
# info    - идентификатор объекта карты в памяти
# При масштабируемой подписи возвращает 0
# При ошибке возвращает ноль

    mapGetTextHeightMkm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextHeightMkm', maptype.HOBJ)
    def mapGetTextHeightMkm(_info: maptype.HOBJ) -> int:
        return mapGetTextHeightMkm_t (_info)


# Запросить рамку подписи в пикселах для текущих условий отображения
# hMap    - идентификатор документа
# hdc     - идентификатор контекста, на котором рассчитывается размер рамки
#           (может быть равен нулю)
# rect    - положение области отображения, относительно которой считается рамка,
#           в пикселах на документе
# info    - идентификатор объекта типа подпись, параметры отображения должны быть типа IMG_TEXT
# box     - координаты 4-ех точек наклонной рамки относительно верхнего левого
#           угла области rect
# Подобъекты подписи не учитываются при расчете рамки
# При ошибке возвращает ноль

    mapGetPaintTextBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPaintTextBorder', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.HOBJ, ctypes.POINTER(maptype.DRAWBOX))
    def mapGetPaintTextBorder(_hMap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _info: maptype.HOBJ, _box: ctypes.POINTER(maptype.DRAWBOX)) -> int:
        return mapGetPaintTextBorder_t (_hMap, _hdc, _rect, _info, _box)


# Запросить способ выравнивания текста по горизонтали
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта
# (FA_LEFT,FA_RIGHT,FA_CENTER - см. mapgdi.h)

    mapGetTextHorizontalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextHorizontalAlign', maptype.HOBJ, ctypes.c_int)
    def mapGetTextHorizontalAlign(_info: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextHorizontalAlign_t (_info, _subject)


# Запросить способ выравнивания текста по вертикали
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта
# (FA_BOTTOM,FA_TOP,FA_BASELINE,FA_MIDDLE)

    mapGetTextVerticalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTextVerticalAlign', maptype.HOBJ, ctypes.c_int)
    def mapGetTextVerticalAlign(_info: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextVerticalAlign_t (_info, _subject)


# Установить способ выравнивания текста по горизонтали
# (FA_LEFT,FA_RIGHT,FA_CENTER)
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта (-1 - установить всем)
# По умолчанию имеет значение FA_LEFT
# При успешном выполнении возвращает установленное значение

    mapPutTextHorizontalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutTextHorizontalAlign', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapPutTextHorizontalAlign(_info: maptype.HOBJ, _align: int, _subject: int) -> int:
        return mapPutTextHorizontalAlign_t (_info, _align, _subject)


# Установить способ выравнивания текста по вертикали
# (FA_BOTTOM,FA_TOP,FA_BASELINE,FA_MIDDLE)
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта (-1 - установить всем)
# По умолчанию имеет значение FA_BASELINE
# При успешном выполнении возвращает установленное значение

    mapPutTextVerticalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPutTextVerticalAlign', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapPutTextVerticalAlign(_info: maptype.HOBJ, _align: int, _subject: int) -> int:
        return mapPutTextVerticalAlign_t (_info, _align, _subject)


# ############################################################
#                                                            #
#     РЕДАКТИРОВАНИЕ ГРАФИЧЕСКОГО ОПИСАНИЯ ОБ'ЕКТА           #
#                                                            #
#  (Графическое описание имеется, как правило, у объектов    #
#   пользовательской карты, не связанных с классификатором)  #
#                                                            #
# ############################################################
# Запросить - имеет ли объект графическое описание
# info    - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsDrawObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsDrawObject', maptype.HOBJ)
    def mapIsDrawObject(_info: maptype.HOBJ) -> int:
        return mapIsDrawObject_t (_info)


# Запросить количество элементов графического описания
# info    - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapDrawCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawCount', maptype.HOBJ)
    def mapDrawCount(_info: maptype.HOBJ) -> int:
        return mapDrawCount_t (_info)


# Запросить вид элемента графического описания
# по его номеру (number -  от 1 до DrawCount())
# info    - идентификатор объекта карты в памяти
# Возвращает номер функции типа IMG_XXXXXXX (см. MAPGDI.H)
# При ошибке возвращает ноль

    mapDrawImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawImage', maptype.HOBJ, ctypes.c_int)
    def mapDrawImage(_info: maptype.HOBJ, _number: int) -> int:
        return mapDrawImage_t (_info, _number)


# Запросить длину параметров элемента графического описания
# по его номеру ( от 1 до DrawCount())
# info    - идентификатор объекта карты в памяти
# Для запроса с 0 номером возвращает длину параметров
# графического описания объекта
# При ошибке возвращает ноль

    mapDrawLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDrawLength', maptype.HOBJ, ctypes.c_int)
    def mapDrawLength(_info: maptype.HOBJ, _number: int) -> int:
        return mapDrawLength_t (_info, _number)


# Добавить элемент графического описания объектов
# info  - идентификатор объекта карты в памяти
# image - номер функции типа IMG_XXXXXXX (см. MAPGDI.H)
# parm  - адрес структуры типа IMGXXXXXX
# При ошибке возвращает ноль,иначе - число элементов в записи

    mapAppendDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendDraw', maptype.HOBJ, ctypes.c_int, ctypes.c_char_p)
    def mapAppendDraw(_info: maptype.HOBJ, _image: int, _parm: ctypes.c_char_p) -> int:
        return mapAppendDraw_t (_info, _image, _parm)


# Удалить все элементы графического описания объекта
# info  - идентификатор объекта карты в памяти

    mapClearDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearDraw', maptype.HOBJ)
    def mapClearDraw(_info: maptype.HOBJ) -> int:
        return mapClearDraw_t (_info)


# Удалить элемент графического описания объекта
# info   - идентификатор объекта карты в памяти
# number - номер элемента (начиная с 1)
# При ошибке возвращает ноль

    mapDeleteDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteDraw', maptype.HOBJ, ctypes.c_int)
    def mapDeleteDraw(_info: maptype.HOBJ, _number: int) -> int:
        return mapDeleteDraw_t (_info, _number)


# Считать графические параметры объекта
# info   - идентификатор объекта карты
# hDrw   - идентификатор набора примитивов в памяти (создается функцией mapCreateDraw())
# При ошибке возвращает ноль

    mapReadObjectDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapReadObjectDraw(_info: maptype.HOBJ, _hDrw: maptype.HDRAW) -> int:
        return mapReadObjectDraw_t (_info, _hDrw)


# Записать графические параметры в объект
# info   - идентификатор объекта карты
# hDrw   - идентификатор записываемого набора примитивов в памяти
# При ошибке возвращает ноль

    mapWriteObjectDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapWriteObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapWriteObjectDraw(_info: maptype.HOBJ, _hDrw: maptype.HDRAW) -> int:
        return mapWriteObjectDraw_t (_info, _hDrw)


# Запросить обобщенные графические параметры для полигона
# info   - идентификатор объекта карты
# При ошибке возвращает ноль

    mapGetPolyStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPolyStyle', maptype.HOBJ, ctypes.POINTER(mapgdi.IMGSQUARE), ctypes.POINTER(mapgdi.IMGLINE))
    def mapGetPolyStyle(_info: maptype.HOBJ, _square: ctypes.POINTER(mapgdi.IMGSQUARE), _line: ctypes.POINTER(mapgdi.IMGLINE)) -> int:
        return mapGetPolyStyle_t (_info, _square, _line)


# ############################################################
#                                                            #
#         СОХРАНИТЬ/ВОССТАНОВИТЬ ДАННЫЕ ОБ'ЕКТА              #
#                                                            #
# ############################################################
# Запросить - является ли карта, которой принадлежит объект, редактируемой
# При ошибке возвращает ноль

    mapIsEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsEdit', maptype.HOBJ)
    def mapIsEdit(_info: maptype.HOBJ) -> int:
        return mapIsEdit_t (_info)


# Запросить - изменились ли какие-либо данные объекта в памяти:
# метрика, семантика, графика
# При изменении данных, которые не были сохранены функцией типа
# mapCommitObject, возвращает ненулевое значение
# Изменение кода объекта, границ видимости и других свойств
# эта функция не проверяет
# При наличии изменений возвращает флаг изменения (2 - метрика,
# 4 - семантика, 8 - графика).
# При ошибке возвращает ноль

    mapIsDirtyObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsDirtyObject', maptype.HOBJ)
    def mapIsDirtyObject(_info: maptype.HOBJ) -> int:
        return mapIsDirtyObject_t (_info)


# Сохранить данные об объекте в карту
# info  - идентификатор объекта карты в памяти
# isnewobject - признак записи нового объекта (аналог mapCommitObjectAsNew)
# isload - признак записи объекта без пересчета семантики-формула (аналог mapCommitObjectForLoad)
# isorder - признак записи объектов в порядке поступления (аналог mapCommitObjectByOrder)
# error - код ошибки (см. maperr.rh)
# Номер листа в районе должен быть установлен
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectPro', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapCommitObjectPro(_info: maptype.HOBJ, _isnewobject: int, _isload: int, _isorder: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCommitObjectPro_t (_info, _isnewobject, _isload, _isorder, _error)

    mapCommitObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObject', maptype.HOBJ)
    def mapCommitObject(_info: maptype.HOBJ) -> int:
        return mapCommitObject_t (_info)


# Сохранить данные об объекте в карту без пересчета семантики типа формула
# Это бывает необходимо при чтении данных из базы данных или наборов данных
# info  - идентификатор объекта карты в памяти
# error - код ошибки (см. maperr.rh)
# Номер листа в районе должен быть установлен
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObjectForLoad_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectForLoad', maptype.HOBJ)
    def mapCommitObjectForLoad(_info: maptype.HOBJ) -> int:
        return mapCommitObjectForLoad_t (_info)

    mapCommitObjectForLoadEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectForLoadEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_int))
    def mapCommitObjectForLoadEx(_info: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCommitObjectForLoadEx_t (_info, _error)


# Сохранить данные об объекте в файле
# info  - идентификатор объекта карты в памяти
# Объекты будут отображаться в порядке записи в файл
# Применяется для специальной сортировки объектов
# (например, линейный может быть под площадным)
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObjectByOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectByOrder', maptype.HOBJ)
    def mapCommitObjectByOrder(_info: maptype.HOBJ) -> int:
        return mapCommitObjectByOrder_t (_info)


# Сохранить данные об объекте в файле
# info  - идентификатор объекта карты в памяти
# error - код ошибки (см. maperr.rh)
# Если объект новый - выполняется функция mapCommitObject(),
# если такой объект уже был, то сохраняется копия
# объекта с новым уникальным номером (предполагается,
# что предварительно изменены координаты и т.п.)
# Номер листа в районе должен быть установлен
# Позволяет ускорить создание серии однотипных объектов
# (другой способ - mapCopyObjectAsNew()).
# При ошибке возвращает ноль

    mapCommitObjectAsNewEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectAsNewEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_int))
    def mapCommitObjectAsNewEx(_info: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCommitObjectAsNewEx_t (_info, _error)

    mapCommitObjectAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectAsNew', maptype.HOBJ)
    def mapCommitObjectAsNew(_info: maptype.HOBJ) -> int:
        return mapCommitObjectAsNew_t (_info)


# Сохранить данные об объекте в файле с выбором листа
# или делением объекта по листам (при необходимости)
# info  - идентификатор объекта карты в памяти
# Для объектов пользовательских карт (обстановки)
# достаточно mapCommitObject() - там один лист и нет границ.
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# Если объект не попал в габариты листа - возвращает -2
# При ошибке возвращает ноль

    mapCommitWithPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitWithPlace', maptype.HOBJ)
    def mapCommitWithPlace(_info: maptype.HOBJ) -> int:
        return mapCommitWithPlace_t (_info)


# Сохранить данные об объекте в файле с выбором листа
# или делением объекта по листам (при необходимости)
# Объект будет сохранен, как новый, с присвоением
# нового уникального номера
# info  - идентификатор объекта карты в памяти
# Для объектов пользовательских карт (обстановки)
# достаточно mapCommitObject() - там один лист и нет границ.
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitWithPlaceAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitWithPlaceAsNew', maptype.HOBJ)
    def mapCommitWithPlaceAsNew(_info: maptype.HOBJ) -> int:
        return mapCommitWithPlaceAsNew_t (_info)


# Сохранить данные об объекте в файле с
# обрезанием объекта по границам заданного листа
# info  - идентификатор объекта карты в памяти
# list  - номер листа ( > 0 ), по рамке которого скорректировать
# метрические данные объекта
# Для объектов пользовательских карт (обстановки)
# достаточно mapCommitObject() - там один лист и нет границ.
# При ошибке возвращает ноль

    mapCommitWithPlaceForList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitWithPlaceForList', maptype.HOBJ, ctypes.c_int)
    def mapCommitWithPlaceForList(_info: maptype.HOBJ, _list: int) -> int:
        return mapCommitWithPlaceForList_t (_info, _list)


# Запрость/Установить параметры обработки метрики линейных и площадных объектов,
# используемые при сохранении объектов с делением на листы в функциях:
# mapCommitWithPlace, mapCommitWithPlaceAsNew, mapCommitWithPlaceForList
# parm  - параметры, используемые для автоматического удаления малых отрезков,
#         малых линейных и вырожденных площадных объектов, которые получаются
#         при разрезания объектов по рамкам листов карты
# При ошибке возвращает ноль

    mapGetCommitObjectParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapGetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        return mapGetCommitObjectParm_t (_hmap, _parm)

    mapSetCommitObjectParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapSetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        return mapSetCommitObjectParm_t (_hmap, _parm)


# Сохранить объект в файле с разбиением мультигеометрии на простые объекты
# Если объект не содержит мультигеометрии, то он сохраняется как есть
# При успешном завершении в info останется основной контур объекта, а все его
# внешние подобъекты станут самостоятельными объектами, при необходимости объединенными
# в набор (параметр makeset)
# Параметры:
#  - info    - контекст описания класса объекта;
#  - forload - флаг режима загрузки: при сохранении объекта не пересчитываются семантики-формулы;
#  - makeset - флаг необходимости объединить полученные объекты в набор
#  - asnew   - флаг сохранения объекта как нового, если ноль, то объект в info будет заменен, иначе
#              все объекты, включая основной контур, будут сохранены новыми объектами, объект переданный
#              в info на карте останется без изменений;
#  - error   - буфер для возврата кода ошибки
# При ошибке возвращает ноль

    mapCommitObjectAsSimple_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectAsSimple', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapCommitObjectAsSimple(_info: maptype.HOBJ, _forload: int, _makeset: int, _asnew: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCommitObjectAsSimple_t (_info, _forload, _makeset, _asnew, _error)


# Запросить - выполняется ли загрузка объекта из базы данных или набора данных
# Применяется в функциях обратного вызова для определения того, что
# выполняется функция mapCommitObjectForLoad()
# При ошибке возвращает ноль

    mapIsObjectLoading_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectLoading', maptype.HOBJ)
    def mapIsObjectLoading(_info: maptype.HOBJ) -> int:
        return mapIsObjectLoading_t (_info)


# Удалить объект карты
# Предыдущее состояние объекта сохраняется в резервных
# файлах и может быть восстановлено
# info  - идентификатор объекта карты в памяти
# Признак удаления записывается в памяти и в файле
# При ошибке возвращает ноль

    mapDeleteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteObject', maptype.HOBJ)
    def mapDeleteObject(_info: maptype.HOBJ) -> int:
        return mapDeleteObject_t (_info)


# Удалить объект карты по его номеру (number)
# hMap   - идентификатор открытых данных
# list   - последовательный номер листа (с 1)
# number - последовательный ноиер объекта в листе
# Связь с номером - см. mapReadObjectByNumber,mapGetObjectNumber
# После удаления объекта по номеру вызов Сommit не должен выполняться
# для этого объекта
# При ошибке возвращает ноль

    mapDeleteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteObjectByNumber', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapDeleteObjectByNumber(_hmap: maptype.HMAP, _list: int, _number: int) -> int:
        return mapDeleteObjectByNumber_t (_hmap, _list, _number)


# Отменить удаление объекта карты
# info  - идентификатор объекта карты в памяти
# Признак удаления убирается в памяти и в файле
# При ошибке возвращает ноль

    mapUndeleteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUndeleteObject', maptype.HOBJ)
    def mapUndeleteObject(_info: maptype.HOBJ) -> int:
        return mapUndeleteObject_t (_info)


# Переместить объект в цепочке в конец (рисуется над всеми)
# Объекту присваивается признак "выше всех"
# info  - идентификатор объекта карты в памяти
# Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber()
# При ошибке возвращает ноль

    mapUpdateObjectUp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateObjectUp', maptype.HOBJ)
    def mapUpdateObjectUp(_info: maptype.HOBJ) -> int:
        return mapUpdateObjectUp_t (_info)


# Переместить объект в цепочке в начало (рисуется под всеми)
# Объекту присваивается признак "ниже всех"
# info  - идентификатор объекта карты в памяти
# Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber()
# При ошибке возвращает ноль

    mapUpdateObjectDown_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateObjectDown', maptype.HOBJ)
    def mapUpdateObjectDown(_info: maptype.HOBJ) -> int:
        return mapUpdateObjectDown_t (_info)


# Сбросить признаки "выше всех" и "ниже всех" в объекте
# Положение объекта в соответствии с его слоем и локализацией
# изменится после сортировки карты
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapUpdateObjectNormal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateObjectNormal', maptype.HOBJ)
    def mapUpdateObjectNormal(_info: maptype.HOBJ) -> int:
        return mapUpdateObjectNormal_t (_info)


# Запросить флаг размещения объекта (2 - над всеми, 3 - под всеми, 1 - не задано)
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapObjectUpDownState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectUpDownState', maptype.HOBJ)
    def mapObjectUpDownState(_info: maptype.HOBJ) -> int:
        return mapObjectUpDownState_t (_info)


# Отменить удаление объекта карты по его номеру (number)
# hmap   - идентификатор открытых данных
# hsite  - идентификатор пользовательской карты
#          (для фоновой карты равен hMap или 0)
# list   - последовательный номер листа (с 1)
# number - последовательный ноиер объекта в листе
# Связь с номером - см. mapReadObjectByNumber,mapGetObjectNumber
# Признак удаления убирается в файле
# При ошибке возвращает ноль

    mapUndeleteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUndeleteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapUndeleteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _number: int) -> int:
        return mapUndeleteObjectByNumber_t (_hmap, _hsite, _list, _number)


# Восстановить (в памяти) данные об объекте из файла
# info  - идентификатор объекта карты в памяти
# Номер листа в районе и номер объекта должны быть установлены
# При ошибке возвращает ноль

    mapRevertObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRevertObject', maptype.HOBJ)
    def mapRevertObject(_info: maptype.HOBJ) -> int:
        return mapRevertObject_t (_info)


# Восстановить копию объекта, по состоянию до выполнения транзакции
# info -  идентификатор существующего объекта,
# number - номер транзакции
# При ошибке возвращает ноль

    mapRestoreBackObjectByAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreBackObjectByAction', maptype.HOBJ, ctypes.c_int)
    def mapRestoreBackObjectByAction(_info: maptype.HOBJ, _number: int) -> int:
        return mapRestoreBackObjectByAction_t (_info, _number)


# Восстановить копию объекта, по состоянию до выполнения транзакции
# info -  идентификатор существующего объекта,
# number - номер транзакции
# При ошибке возвращает ноль

    mapRestoreBackObjectByTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreBackObjectByTime', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapRestoreBackObjectByTime(_info: maptype.HOBJ, _date: int, _time: int) -> int:
        return mapRestoreBackObjectByTime_t (_info, _date, _time)


# Считать в объект метрику мультимасштабного объекта заданного уровня
# level - уровень генерализации контура от 1 до 4
# Если для заданного уровня контура нет, то считывается соседний более сжатый
# контур, если его нет, то менее сжатый
# Если у объекта нет дополнительных контуров - возвращает ноль
# Возвращает номер считанного уровня
# При ошибке возвращает ноль

    mapLoadMulticontourLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoadMulticontourLevel', maptype.HOBJ, ctypes.c_int)
    def mapLoadMulticontourLevel(_info: maptype.HOBJ, _level: int) -> int:
        return mapLoadMulticontourLevel_t (_info, _level)


# Записать дату и время создания или последнего редактирования объекта и
# имя оператора, выполнившего операцию
# Для вновь создаваемого объекта пишется дата и время создания SEMOBJECTDATE
# и SEMOBJECTTIME, имя оператора пишется в семантику SEMOBJECTAUTHOR
# Для редактируемого объекта пишется (при отсутствии) или изменяется (при наличии)
# время последнего редактирования SEMOBJECTREDATE и SEMOBJECTRETIME,
# имя оператора пишется в семантику SEMOBJECTREAUTHOR (SEMOBJECTREAUTHOR)
# При ошибке возвращает 0

    mapSetObjectEditDateTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectEditDateTime', maptype.HOBJ)
    def mapSetObjectEditDateTime(_info: maptype.HOBJ) -> int:
        return mapSetObjectEditDateTime_t (_info)


# Установить адрес функции, которая будет вызываться
# при редактировании объекта карты
# Для отмены оповещения о редактировании необходимо вызвать
# данную функцию и передать в параметрах call и parm нулевые значения
# Вызываемая функция не должна сама редактировать карту !
# hmap   - идентификатор открытых данных
# hsite  - идентификатор пользовательской карты
#          (для фоновой карты равен hMap или 0)
# call - адрес вызываемой функции (см. maptype.h),
# parm - параметр, который будет передан вызываемой функции первым,
# вторым параметром будет адрес структуры CHANGEINFO (см. maptype.h).
# При ошибке возвращает ноль

#    mapSetChangeCallAndParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetChangeCallAndParm', maptype.HMAP, maptype.HSITE, maptype.CHANGECALL, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetChangeCallAndParm(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _call: maptype.CHANGECALL, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
#        return mapSetChangeCallAndParm_t (_hmap, _hsite, _call, _parm)


# Установить для всех открытых карт адрес функции, которая будет вызываться
# при редактировании объекта карты
# hmap   - идентификатор открытых данных
# call - адрес вызываемой функции (см. maptype.h),
# parm - параметр, который будет передан вызываемой функции первым,
# вторым параметром будет адрес структуры CHANGEINFO (см. maptype.h).
# При ошибке возвращает ноль

#    mapSetTotalChangeCallAndParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTotalChangeCallAndParm', maptype.HMAP, maptype.CHANGECALL, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetTotalChangeCallAndParm(_hmap: maptype.HMAP, _call: maptype.CHANGECALL, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
#        return mapSetTotalChangeCallAndParm_t (_hmap, _call, _parm)


# Запросить установлен ли общий адрес функции, которая будет вызываться
# при редактировании объекта карты
# При ошибке возвращает ноль

    mapIsTotalChangeCallAndParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTotalChangeCallAndParm', maptype.HMAP)
    def mapIsTotalChangeCallAndParm(_hmap: maptype.HMAP) -> int:
        return mapIsTotalChangeCallAndParm_t (_hmap)


# #############################################################
#                                                             #
#     ОБРАБОТКА РЕЗЕРВНЫХ ФАЙЛОВ ...\LOG\... ^DA,^SE,^HD      #
#      (СОДЕРЖАТ КОПИИ ВСЕХ ОБНОВЛЯЕМЫХ ОБ ЕКТОВ ЛИСТА)       #
#                                                             #
# #############################################################
# Последовательный перебор отредактированных копий объекта info
# info  - идентификатор объекта карты в памяти
# copynumber - последовательный номер копии данного объекта (1, 2, ...)
# в порядке от последней операции редактирования к предыдущей
# Вызывается с последовательным увеличением copynumber,
# пока не будет найдена нужная копия или копии закончатся
# Чтобы сделать найденную копию текущим состоянием объекта на карте,
# нужно удалить лишние копии объекта функцией
# mapDeleteObjectCopyToNumber, а затем вызвать функцию mapCommit.
# При ошибке возвращает ноль

    mapReadObjectCopyByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadObjectCopyByNumber', maptype.HOBJ, ctypes.c_int)
    def mapReadObjectCopyByNumber(_info: maptype.HOBJ, _copynumber: int) -> int:
        return mapReadObjectCopyByNumber_t (_info, _copynumber)


# Удалить отредактированные копии объекта info
# info  - идентификатор объекта карты в памяти
# Удаляет копии объекта от первой до copynumber из файлов отката
# Копия copynumber+1 становится первой
# Если вызывается после сохранения соответсвующей копии объекта
# на карте (mapCommit - отмена выполненных операций редактирования),
# то число удаляемых копий должно быть на 1 больше, чем номер
# восстанавливаемой копии. (т.к. mapCommit создает еще одну копию
# объекта и она становиться первой).
# При ошибке возвращает ноль

    mapDeleteObjectCopyToNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteObjectCopyToNumber', maptype.HOBJ, ctypes.c_int)
    def mapDeleteObjectCopyToNumber(_info: maptype.HOBJ, _copynumber: int) -> int:
        return mapDeleteObjectCopyToNumber_t (_info, _copynumber)


# ############################################################
#                                                            #
#         РАСЧЕТ ХАРАКТЕРИСТИК ОБ'ЕКТА                       #
#                                                            #
# ############################################################
# Вычисление длины участка объекта (стороны) на местности,
# начиная с указанной точки
# Для последней точки вычисляет расстояние до первой точки
# info  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает 0 (при совпадении точек также)

    mapSideLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideLength', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSideLength(_info: maptype.HOBJ, _number: int, _subject: int = 0) -> float:
        return mapSideLength_t (_info, _number, _subject)

    mapSideLengthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSideLengthEx', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapSideLengthEx(_info: maptype.HOBJ, _number: int, _subject: int, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSideLengthEx_t (_info, _number, _subject, _length)


# Вычисление длины участка объекта на карте (в проекции документа),
# начиная с указанной точки
# Для последней точки вычисляет расстояние до первой точки
# info  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает 0 (при совпадении точек также)

    mapSideLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideLengthInMap', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSideLengthInMap(_info: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideLengthInMap_t (_info, _number, _subject)


# Вычисление длины участка объекта (стороны) в проекции документа
# или на местности, в зависимости от текущего
# условия выполнения вычислений по карте -
# mapSetCalculationConventional
# info  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает 0

    mapConventionalSideLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSideLength', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapConventionalSideLength(_info: maptype.HOBJ, _number: int, _subject: int = 0) -> float:
        return mapConventionalSideLength_t (_info, _number, _subject)


# Вычисление азимута участка объекта (стороны)
# Возвращает величину угла в радианах
# Если геодезия не поддерживается, то вычисляется дирекционный угол
# Для последней точки вычисляет направление на первую точку
# У замкнутых объектов первая и последняя точки совпадают
# info  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает 0 (при совпадении точек также)

    mapSideAzimuth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideAzimuth', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSideAzimuth(_info: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideAzimuth_t (_info, _number, _subject)

    mapSideAzimuthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSideAzimuthEx', maptype.HOBJ, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mapSideAzimuthEx(_info: maptype.HOBJ, _number: int, _subject: int, _azimuth: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSideAzimuthEx_t (_info, _number, _subject, _azimuth)


# Вычисление дирекционного угла участка объекта (стороны)
# Возвращает величину угла в радианах
# Для последней точки вычисляет направление на первую точку
# У замкнутых объектов первая и последняя точки совпадают
# info  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# При ошибке возвращает 0 (при совпадении точек также)

    mapSideDirection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideDirection', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSideDirection(_info: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideDirection_t (_info, _number, _subject)


# Вычисление уточненной площади объекта на местности
# Для вычисления площади объекта его координаты пересчитываюся
# в проекцию топографической карты ближайшей зоны!
# mapPrecisionSquare выполняет деление полигона по участкам,
# занимающим по долготе не более 6 градусов для повышения точности
# вычислений (метрика не должна иметь самопересечений)
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquare', maptype.HOBJ)
    def mapSquare(_info: maptype.HOBJ) -> float:
        return mapSquare_t (_info)

    mapSquareEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSquareEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapSquareEx(_info: maptype.HOBJ, _square: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSquareEx_t (_info, _square)

    mapPrecisionSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPrecisionSquare', maptype.HOBJ)
    def mapPrecisionSquare(_info: maptype.HOBJ) -> float:
        return mapPrecisionSquare_t (_info)


# Вычисление площади объекта в проекции карты
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapSquareInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquareInMap', maptype.HOBJ)
    def mapSquareInMap(_info: maptype.HOBJ) -> float:
        return mapSquareInMap_t (_info)


# Вычисление площади объекта в проекции карты
# или на местности, в зависимости от текущего
# условия выполнения вычислений по карте -
# mapSetCalculationConventional
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapConventionalSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSquare', maptype.HOBJ)
    def mapConventionalSquare(_info: maptype.HOBJ) -> float:
        return mapConventionalSquare_t (_info)


# Вычисление площади отдельного подобъекта в проекции документа
# или на местности, в зависимости от текущего
# условия выполнения вычислений по карте -
# mapSetCalculationConventional
# mapPrecisionSubjectSquare выполняет деление полигона по участкам,
# занимающим по долготе не более 6 градусов для повышения точности
# вычислений (метрика не должна иметь самопересечений)
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта от 0 до mapPolyCount,
#           если равно нулю, то вычисляется площадь внешнего контура
#           без вычитания площади подобъектов
# При ошибке возвращает 0

    mapConventionalSubjectSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSubjectSquare', maptype.HOBJ, ctypes.c_int)
    def mapConventionalSubjectSquare(_info: maptype.HOBJ, _subject: int) -> float:
        return mapConventionalSubjectSquare_t (_info, _subject)

    mapPrecisionSubjectSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPrecisionSubjectSquare', maptype.HOBJ, ctypes.c_int)
    def mapPrecisionSubjectSquare(_info: maptype.HOBJ, _subject: int) -> float:
        return mapPrecisionSubjectSquare_t (_info, _subject)


# Вычисление площади подобъекта в проекции документа
# info  - идентификатор объекта карты в памяти
# subject - номер подобъекта от 0 до mapPolyCount,
#           если равно нулю, то вычисляется площадь внешнего контура
#           без вычитания площади подобъектов
# При ошибке возвращает 0

    mapSubjectSquareInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectSquareInMap', maptype.HOBJ, ctypes.c_int)
    def mapSubjectSquareInMap(_info: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectSquareInMap_t (_info, _subject)


# Установить условие для расчета расстояний и площадей
# по карте
# hmap   - идентификатор открытых данных
# flag   - условие выполнения расчетов:
#          0 - вычислять уточненное значение площадей и
#          расстояний по ближайшему осевому меридиану;
#          1 - вычислять площади и расстояния в проекции
#          карты, которой принадлежит объект
# Возвращает предыдущее значение условия

    mapSetCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCalculationConventional', maptype.HMAP, ctypes.c_int)
    def mapSetCalculationConventional(_hmap: maptype.HMAP, _flag: int) -> int:
        return mapSetCalculationConventional_t (_hmap, _flag)


# Запросить условие для расчета расстояний и площадей
# по карте
# hmap   - идентификатор открытых данных
# Возвращает условие выполнения расчетов:
#          0 - вычислять уточненное значение площадей и
#          расстояний по ближайшему осевому меридиану;
#          1 - вычислять площади и расстояния в проекции
#          карты, которой принадлежит объект

    mapGetCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCalculationConventional', maptype.HMAP)
    def mapGetCalculationConventional(_hmap: maptype.HMAP) -> int:
        return mapGetCalculationConventional_t (_hmap)


# Установить общее условие для расчета расстояний и площадей
# по карте для всех карт
# hmap   - идентификатор открытых данных
# flag   - условие выполнения расчетов:
#          0 - вычислять уточненное значение площадей и
#          расстояний по ближайшему осевому меридиану;
#          1 - вычислять площади и расстояния в проекции
#          карты, которой принадлежит объект
#         -1 - не учитывать общее условие в картах (будет учитываться условие,
#          которое установлено для каждого HMAP отдельно
# Возвращает предыдущее значение условия

    mapSetCommonCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCommonCalculationConventional', ctypes.c_int)
    def mapSetCommonCalculationConventional(_flag: int) -> int:
        return mapSetCommonCalculationConventional_t (_flag)


# Запросить общее условие для расчета расстояний и площадей
# по карте для всех карт
# hmap   - идентификатор открытых данных
# Возвращает условие выполнения расчетов:
#          0 - вычислять уточненное значение площадей и
#          расстояний по ближайшему осевому меридиану;
#          1 - вычислять площади и расстояния в проекции
#          карты, которой принадлежит объект
#         -1 - не учитывать общее условие в картах (будет учитываться условие,
#          которое установлено для каждого HMAP отдельно

    mapGetCommonCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCommonCalculationConventional')
    def mapGetCommonCalculationConventional() -> int:
        return mapGetCommonCalculationConventional_t ()


# Вычисление площади объекта c учетом рельефа
# При отсутствии рельефа(матрицы высот,слоев,Tin-матрицы) возвращает площадь объекта
# hmap   - идентификатор открытых данных
# info  - идентификатор объекта карты в памяти
# step - шаг инетрполяции в метрах, если 0 то вычисляется автоматически
# При ошибке возвращает 0

    mapSquareWithHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquareWithHeight', maptype.HMAP, maptype.HOBJ)
    def mapSquareWithHeight(_hmap: maptype.HMAP, _info: maptype.HOBJ) -> float:
        return mapSquareWithHeight_t (_hmap, _info)

    mapSquareWithHeightEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquareWithHeightEx', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapSquareWithHeightEx(_hmap: maptype.HMAP, _info: maptype.HOBJ, _step: float = 0.) -> float:
        return mapSquareWithHeightEx_t (_hmap, _info, _step)


# Вычисление периметра объекта
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает 0

    mapPerimeter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPerimeter', maptype.HOBJ)
    def mapPerimeter(_info: maptype.HOBJ) -> float:
        return mapPerimeter_t (_info)


# Вычисление длины объекта
# Для вычисления длины объекта его координаты пересчитываюся
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# info  - идентификатор объекта карты в памяти
# Для подобъектов считается суммарная длина
# При ошибке возвращает 0

    mapLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLength', maptype.HOBJ)
    def mapLength(_info: maptype.HOBJ) -> float:
        return mapLength_t (_info)

    mapLengthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLengthEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapLengthEx(_info: maptype.HOBJ, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapLengthEx_t (_info, _length)


# Вычисление длины объекта по карте
# Координаты объекта не пересчитываются, полученная длина
# может значительно отличаться от реальной длины объекта на местности
# info  - идентификатор объекта карты в памяти
# Для подобъектов считается суммарная длина
# При ошибке возвращает 0

    mapLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthInMap', maptype.HOBJ)
    def mapLengthInMap(_info: maptype.HOBJ) -> float:
        return mapLengthInMap_t (_info)


# Вычисление длины объекта от начала до заданной точки
# info  - идентификатор объекта карты в памяти
# point - координаты точки, расположенной вдоль(вблизи) объекта
# Если точка не на объекте - ищется ближайшая точка на контуре
# Координаты точки обновляются!
# При ошибке возвращает 0

    mapLengthToPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthToPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLengthToPoint(_info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapLengthToPoint_t (_info, _point)


# Вычисление длины подобъекта/объекта
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта:
#            0 или более - вычисляется длина подобъекта;
#           -1 - вычисляется суммарная длина всех подобъектов;
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов
# При ошибке возвращает 0

    mapSubjectLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectLength', maptype.HOBJ, ctypes.c_int)
    def mapSubjectLength(_info: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectLength_t (_info, _subject)


# Вычисление длины объекта\подобъекта в проекции документа
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта:
#            0 или более - вычисляется длина подобъекта;
#           -1 - вычисляется суммарная длина всех подобъектов;
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов
# При ошибке возвращает 0

    mapSubjectLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectLengthInMap', maptype.HOBJ, ctypes.c_int)
    def mapSubjectLengthInMap(_info: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectLengthInMap_t (_info, _subject)


# Вычисление длины объекта\подобъекта в проекции документа
# или на местности, в зависимости от текущего
# условия выполнения вычислений по карте -
# mapSetCalculationConventional
# info    - идентификатор объекта карты в памяти
# subject - номер подобъекта:
#            0 или более - вычисляется длина подобъекта;
#           -1 - вычисляется суммарная длина всех подобъектов;
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов
# При ошибке возвращает 0

    mapConventionalSubjectLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSubjectLength', maptype.HOBJ, ctypes.c_int)
    def mapConventionalSubjectLength(_info: maptype.HOBJ, _subject: int = -1) -> float:
        return mapConventionalSubjectLength_t (_info, _subject)


# Вычисление длины объекта c учетом рельефа
# При отсутствии рельефа(матрицы высот,слоев,Tin-матрицы) возвращает длину объекта
# При ошибке возвращает 0

    mapLengthWithHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthWithHeight', maptype.HMAP, maptype.HOBJ)
    def mapLengthWithHeight(_hmap: maptype.HMAP, _info: maptype.HOBJ) -> float:
        return mapLengthWithHeight_t (_hmap, _info)


# Определение замкнутости контура подобъекта
# info  - идентификатор объекта карты в памяти
# subject - номер текущего подобъекта (0 - объекта)
# Возвращает: 1 - объект замкнут, иначе 0

    mapCircuitousSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCircuitousSubject', maptype.HOBJ, ctypes.c_int)
    def mapCircuitousSubject(_info: maptype.HOBJ, _subject: int = 0) -> int:
        return mapCircuitousSubject_t (_info, _subject)


# Определение кратчайшего расстояния от точки до объекта
# hmap   - идентификатор открытых данных
# info  - идентификатор объекта карты в памяти
# subject - номер текущего подобъекта (0-объекта)
# координаты точки point заданы в прямоугольной
# системе координат , в метрах на местности
# Возвращает вычисленное расстояние в метрах
# или 0 в случае ошибки

    mapDistancePointSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistancePointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointSubject(_hmap: maptype.HMAP, _info: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistancePointSubject_t (_hmap, _info, _subject, _point)


# Определение кратчайшего расстояния от точки до объекта (включая
# подобъекты)
# hmap   - идентификатор открытых данных
# info  - идентификатор объекта карты в памяти
# координаты точки point заданы в прямоугольной
# системе координат , в метрах на местности
# Возвращает вычисленное расстояние  в метрах
# или 0 в случае ошибки

    mapDistancePointObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistancePointObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointObject(_hmap: maptype.HMAP, _info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistancePointObject_t (_hmap, _info, _point)


# Определение кратчайшего расстояния между объектами
# info1  - идентификатор 1-го объекта карты в памяти
# info2  - идентификатор 2-го объекта карты в памяти
# Возвращает вычисленное расстояние  в метрах
# или 0 в случае ошибки

    mapDistanceObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistanceObject', maptype.HOBJ, maptype.HOBJ)
    def mapDistanceObject(_info1: maptype.HOBJ, _info2: maptype.HOBJ) -> float:
        return mapDistanceObject_t (_info1, _info2)


# Определение кратчайшего расстояния между объектами и координат
# точек на контурах объектов
# hobj1  - идентификатор первого объекта карты в памяти
# hobj2  - идентификатор второго объекта карты в памяти
# point1 - координаты первой точки линии кратчайшего расстояния
#          между объектами (на объекте hobj1)
# point2 - координаты второй точки линии кратчайшего расстояния
#          между объектами (на объекте hobj2)
# Возвращает вычисленное расстояние  в метрах
# или большое значение (>= 100000000) в случае ошибки

    mapDistanceObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistanceObjectEx', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistanceObjectEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistanceObjectEx_t (_hobj1, _hobj2, _point1, _point2)


# Прямая геодезическая задача на эллипсоиде
# Для расстояния не более 250 км координаты определяются с ошибкой до 0,0001",
# а обратный азимут - до 0,001", что соответствует триангуляции 1 класса
# Способ вспомогательной точки по методу Красовского
# Метод предназначен для расстояний меньше радиуса Земли
# Вычисления выполняются на текущем эллипсоиде, установленном
# в документе - mapSetDocProjection
# Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
# hmap     - идентификатор открытых данных
# b1,l1    - геодезические координаты исходной точки
# angle1   - азимут на вторую точку
# distance - расстояние до второй точки
# b2,l2    - рассчитанные координаты второй точки
# angle2   - рассчитанный азимут со второй точки на первую
#            (если angle2 равен 0, то обратный азимут не вычисляется)
# При ошибке в параметрах возвращает 0

    mapDirectPositionComputation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDirectPositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapDirectPositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _angle1: float, _distance: float, _b2: ctypes.POINTER(ctypes.c_double), _l2: ctypes.POINTER(ctypes.c_double), _angle2: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapDirectPositionComputation_t (_hmap, _b1, _l1, _angle1, _distance, _b2, _l2, _angle2)


# Обратная геодезическая задача на эллипсоиде
# Для расстояния не более 180 градусов по широте
# Выполняется построение ортодромии функцией mapOrthodromeObject
# и запрос длины объекта и азимута первого отрезка
# Точность порядка точности триангуляции 1 класса
# Вычисления выполняются на текущем эллипсоиде, установленном
# в документе - mapSetDocProjection
# Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
# hmap     - идентификатор открытых данных
# b1,l1    - геодезические координаты первой точки
# b2,l2    - геодезические координаты второй точки
# angle    - рассчитанный азимут с первой точки на вторую
# Возвращает расстояние между заданными точками на текущем эллипсоиде
# При ошибке в параметрах возвращает 0

    mapInversePositionComputation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapInversePositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapInversePositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _b2: float, _l2: float, _angle: ctypes.POINTER(ctypes.c_double)) -> float:
        return mapInversePositionComputation_t (_hmap, _b1, _l1, _b2, _l2, _angle)


# Вычисление расстояния между двумя точками на плоскости
# point1, point2 - координаты точек в метрах
# При ошибке возвращает 0

    mapDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistance', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistance(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistance_t (_point1, _point2)


# Вычисление расстояния между двумя точками на местности
# hmap   - идентификатор открытых данных
# point1, point2 - координаты точек в метрах на местности
# Для вычисления расстояния координаты пересчитываются
# в проекцию топографической карты с установкой осевого
# меридиана в центре отрезка
# При ошибке возвращает 0

    mapRealDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRealDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRealDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapRealDistance_t (_hmap, _point1, _point2)


# Вычисление расстояния между двумя точками в проекции карты
# или на местности, в зависимости от текущего
# условия выполнения вычислений по карте -
# mapSetCalculationConventional
# hmap   - идентификатор открытых данных
# point1, point2 - координаты точек в метрах на местности
# При ошибке возвращает 0

    mapConventionalDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapConventionalDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapConventionalDistance_t (_hmap, _point1, _point2)


# Определение направления биссектрисы угла, заданного
# точками p1,p2,p3 с вершиной в точке p2
# p1,p2,p3 - координаты точек в метрах в системе документа
# Возвращаемый угол задан относительно оси X, его положительное
# направление соответствует положительному направлению оси Y

    mapBisectorAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapBisectorAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapBisectorAngle(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _p3: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapBisectorAngle_t (_p1, _p2, _p3)


# Определение положения проекции точки на векторе, заданном точкой и азимутом
# для расстояний менее 60 км
# base - координаты точки основания вектора в радианах системе WGS84 (широта, долгота)
# angle - азимут (угол от касательной к меридиану в базовой точке до направления вектора
#         по часовой стрелке)
# point - координаты точки, для которой строится проекция на вектор, в радианах системе WGS84
# target - координаты точки проекции на векторе в радианах системе WGS84
# При ошибке в параметрах возвращает ноль

    mapSeekPointOnVectorGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekPointOnVectorGeoWGS84', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointOnVectorGeoWGS84(_base: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekPointOnVectorGeoWGS84_t (_base, _angle, _point, _target)


# Определить положение точки относительно прямой (сторону линии)
# point - координаты точки
# first - координаты первой точки отрезка на линии
# last  - координаты второй точки отрезка на линии
# Возвращаемое значение: 1 - точка слева, 0 - точка справа или на линии

    mapGetLineSideForPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLineSideForPoint', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetLineSideForPoint(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _first: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetLineSideForPoint_t (_point, _first, _last)


# Вычисление дирекционного угла от точки 1 к точке 2 в радианах
# point1 - координаты точки 1
# point2 - координаты точки 2
# При ошибке возвращает ноль

    mapGetDirectionAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDirectionAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetDirectionAngle(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapGetDirectionAngle_t (_point1, _point2)


# Добавить врезку на карту
# hMap - идентификатор открытых данных
# name - имя карты (проекта, алиаса) для отображения врезки
# Возвращает текущий номер врезки в списке
# При ошибке возвращает ноль

    mapAppendInset_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendInset', maptype.HMAP, maptype.PWCHAR)
    def mapAppendInset(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapAppendInset_t (_hmap, _name.buffer())


# Добавить врезку на карту
# hMap - идентификатор открытых данных
# item - указатель на описание добавляемой врезки (карты, проекта, алиаса)
# Возвращает текущий номер врезки в списке
# При ошибке возвращает ноль

    mapAppendInsetItemEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendInsetItemEx', maptype.HMAP, ctypes.POINTER(maptype.INSETDESCEX))
    def mapAppendInsetItemEx(_hmap: maptype.HMAP, _item: ctypes.POINTER(maptype.INSETDESCEX)) -> int:
        return mapAppendInsetItemEx_t (_hmap, _item)


# Запросить число врезок на карте
# hMap - идентификатор открытых данных
# При ошибке возвращает ноль

    mapInsetCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapInsetCount', maptype.HMAP)
    def mapInsetCount(_hmap: maptype.HMAP) -> int:
        return mapInsetCount_t (_hmap)


# Запросить описание врезки по номеру с 1
# hMap   - идентификатор открытых данных
# number - порядковый номер врезки на карте с 1
# item   - указатель на описание врезки,
#          которое будет заполнено
# При ошибке возвращает ноль

    mapGetInsetEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInsetEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.INSETDESCEX))
    def mapGetInsetEx(_hmap: maptype.HMAP, _number: int, _item: ctypes.POINTER(maptype.INSETDESCEX)) -> int:
        return mapGetInsetEx_t (_hmap, _number, _item)


# Запросить название врезки по номеру с 1
# hMap   - идентификатор открытых данных
# number - порядковый номер врезки на карте
# name   - буфер для записи имени
# size   - длина буфера в байтах
# При ошибке возвращает ноль

    mapGetInsetName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInsetName', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetInsetName(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetInsetName_t (_hmap, _number, _name.buffer(), _size)


# Запросить идентификатор врезки по номеру с 1
# hMap   - идентификатор открытых данных
# number - порядковый номер врезки на карте
# При ошибке возвращает ноль

    mapGetInsetIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInsetIdent', maptype.HMAP, ctypes.c_int)
    def mapGetInsetIdent(_hmap: maptype.HMAP, _number: int) -> int:
        return mapGetInsetIdent_t (_hmap, _number)


# Запросить идентификатор открытых данных врезки по номеру с 1
# hMap   - идентификатор открытых данных
# number - порядковый номер врезки на карте
# Запрошенный идентификатор не должен закрываться (через вызов mapCloseData)
# При ошибке возвращает ноль

    mapGetInsetMapHandle_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapGetInsetMapHandle', maptype.HMAP, ctypes.c_int)
    def mapGetInsetMapHandle(_hmap: maptype.HMAP, _number: int) -> maptype.HMAP:
        return mapGetInsetMapHandle_t (_hmap, _number)


# Удалить описание врезки по номеру с 1
# hMap   - идентификатор открытых данных
# number - порядковый номер врезки на карте
# При ошибке возвращает ноль

    mapDeleteInset_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteInset', maptype.HMAP, ctypes.c_int)
    def mapDeleteInset(_hmap: maptype.HMAP, _number: int) -> int:
        return mapDeleteInset_t (_hmap, _number)


# Установить врезке признак схематичного отображения
# hMap   - идентификатор открытых данных
# number - номер врезки, для которой устанавливается флаг,
#          если равен -1, то устанавливается для всех врезок
# flag   - признак схематичного отображения (0 или 1)
# При ошибке возвращает ноль

    mapSetInsetSchemeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetInsetSchemeFlag', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetInsetSchemeFlag(_hmap: maptype.HMAP, _number: int, _flag: int) -> int:
        return mapSetInsetSchemeFlag_t (_hmap, _number, _flag)


# Запросить признак отображения врезки
# hMap   - идентификатор открытых данных
# number - номер врезки с 1, для которой запрашивается флаг
# При ошибке возвращает ноль

    mapGetInsetViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInsetViewFlag', maptype.HMAP, ctypes.c_int)
    def mapGetInsetViewFlag(_hmap: maptype.HMAP, _number: int) -> int:
        return mapGetInsetViewFlag_t (_hmap, _number)


# Установить врезке признак отображения
# hMap   - идентификатор открытых данных
# number - номер врезки, для которой устанавливается флаг,
#          если равен -1, то устанавливается для всех врезок
# flag   - признак отображения (0 или 1)
# При ошибке возвращает ноль

    mapSetInsetViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetInsetViewFlag', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetInsetViewFlag(_hmap: maptype.HMAP, _number: int, _flag: int) -> int:
        return mapSetInsetViewFlag_t (_hmap, _number, _flag)


# Запросить признак отображения фона врезки
# hMap   - идентификатор открытых данных
# number - номер врезки с 1, для которой запрашивается флаг
# При ошибке возвращает ноль

    mapGetInsetTransparenceFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetInsetTransparenceFlag', maptype.HMAP, ctypes.c_int)
    def mapGetInsetTransparenceFlag(_hmap: maptype.HMAP, _number: int) -> int:
        return mapGetInsetTransparenceFlag_t (_hmap, _number)


# Установить врезке признак отображения фона
# hMap   - идентификатор открытых данных
# number - номер врезки, для которой устанавливается флаг,
#          если равен -1, то устанавливается для всех врезок
# flag   - признак отображения (0 или 1)
# При ошибке возвращает ноль

    mapSetInsetTransparenceFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetInsetTransparenceFlag', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetInsetTransparenceFlag(_hmap: maptype.HMAP, _number: int, _flag: int) -> int:
        return mapSetInsetTransparenceFlag_t (_hmap, _number, _flag)


# Отобразить врезку в документе
# hMap     - идентификатор открытых данных
# number   - номер отображаемой врезки
#            если равен -1, то отображаются все врезки
# hdc      - идентификатор контекста устройства вывода,
# rect     - координаты отображаемого фрагмента карты (Draw) в изображении (Picture)
# position - положение верхнего левого угла отображаемой области в окне отображения
#            (если смещение предварительно задано через SetViewportOrgEx, то параметр равен 0)
# printscale - соответствие размера пиксела печатающего устройства и пиксела экрана
#            (для печати, для вывода на экран параметр равен 0)
# cliprect - область обрезки выводимого изображения (для применения в SelectClipRgn в сложных отчетах)
#            (если передается область обрезки, то внутренний расчет области обрезки отключается)
# hPaint   - идентификатор контекста отображения для многопоточного вызова функции отображения
# view     - группа отображаемых врезок (>=0 - врезки, которые на карте, <0 - врезки с признаком "под картой"),
#            если поле number равно -1
# При ошибке возвращает ноль

    mapPaintInsetProL_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintInsetProL', maptype.HMAP, ctypes.c_int, maptype.HDC, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(maptype.POINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.RECT), maptype.HPAINT, ctypes.c_int)
    def mapPaintInsetProL(_hMap: maptype.HMAP, _number: int, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.LRECT), _position: ctypes.POINTER(maptype.POINT), _printscale: ctypes.POINTER(ctypes.c_double), _cliprect: ctypes.POINTER(maptype.RECT), _hPaint: maptype.HPAINT, _view: int) -> int:
        return mapPaintInsetProL_t (_hMap, _number, _hdc, _rect, _position, _printscale, _cliprect, _hPaint, _view)

    mapPaintInsetPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintInsetPro', maptype.HMAP, ctypes.c_int, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.RECT), maptype.HPAINT, ctypes.c_int)
    def mapPaintInsetPro(_hMap: maptype.HMAP, _number: int, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _position: ctypes.POINTER(maptype.POINT), _printscale: ctypes.POINTER(ctypes.c_double), _cliprect: ctypes.POINTER(maptype.RECT), _hPaint: maptype.HPAINT, _view: int) -> int:
        return mapPaintInsetPro_t (_hMap, _number, _hdc, _rect, _position, _printscale, _cliprect, _hPaint, _view)

    mapPaintInsetToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintInsetToXImage', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT), ctypes.POINTER(ctypes.c_double))
    def mapPaintInsetToXImage(_hMap: maptype.HMAP, _number: int, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _position: ctypes.POINTER(maptype.POINT), _printscale: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPaintInsetToXImage_t (_hMap, _number, _imagedesc, _rect, _position, _printscale)

    mapPaintInsetToXImageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintInsetToXImageEx', maptype.HMAP, ctypes.c_int, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.LRECT), ctypes.POINTER(maptype.POINT), ctypes.POINTER(ctypes.c_double))
    def mapPaintInsetToXImageEx(_hMap: maptype.HMAP, _number: int, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.LRECT), _position: ctypes.POINTER(maptype.POINT), _printscale: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPaintInsetToXImageEx_t (_hMap, _number, _imagedesc, _rect, _position, _printscale)


# Определить тип файла
# hfile - идентификатор файла-хранилища, полученного в OpenTheFile
# name  - имя файла-хранилища
# sourcename  - имя тестируемого файла
# zposition - смещение на файл в хранилище от начала файла-хранилища или 0
# При ошибке возвращает ноль, иначе - идентификатор файла

    mapCheckFilePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckFilePro', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_int64)
    def mapCheckFilePro(_hfile: ctypes.c_void_p, _sourcename: mapsyst.WTEXT, _zposition: int) -> int:
        return mapCheckFilePro_t (_hfile, _sourcename.buffer(), _zposition)

    mapCheckFileNamePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckFileNamePro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int64)
    def mapCheckFileNamePro(_name: mapsyst.WTEXT, _sourcename: mapsyst.WTEXT, _zposition: int) -> int:
        return mapCheckFileNamePro_t (_name.buffer(), _sourcename.buffer(), _zposition)


# Определить тип файла по его имени
# name - имя тестируемого файла (полный путь)
# Анализируются первые 4 байта, содержащие идентификатор данных.
# При ошибке возвращает ноль, иначе - идентификатор файла
# (см. maptype.h : FILE_SXF, FILE_MAP, FILE_MTW,...)
# Дополнительно различает MAP (FILE_MAP) и SIT (FILE_MAPSIT)
# Имя может быть в виде ALIAS#XXXX для карт на ГИС Сервере

    mapCheckFileExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckFileExUn', maptype.PWCHAR)
    def mapCheckFileExUn(_name: mapsyst.WTEXT) -> int:
        return mapCheckFileExUn_t (_name.buffer())


# Запросить реальный путь к файлу по пути к файлу, который может быть ссылкой
# Если в файле строка ".ref путь или URL" - вернет реальный путь или URL
# Строка .ref в файле должна быть в кодировке UTF-8
# name - путь к файлу
# outname - буфер для записи пути к реальному файлу (совпадает с исходным или определен из записи ".ref")
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetFileNameForRefFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFileNameForRefFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetFileNameForRefFile(_name: mapsyst.WTEXT, _outname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetFileNameForRefFile_t (_name.buffer(), _outname.buffer(), _size)


# Освободить ресурсы ядра перед закрытием приложения и
# выгрузкой (FreeLibrary) библиотеки "gis64acces"

    mapCloseMapAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseMapAccess')
    def mapCloseMapAccess() -> int:
        return mapCloseMapAccess_t ()


# Запросить текущее время в формате "HH:MM:SS"
# buffer - адрес памяти для размещения результата запроса
# size   - размер выделенной памяти в байтах
# При ошибке возвращает ноль

    mapGetTheTimeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTheTimeUn', maptype.PWCHAR, ctypes.c_int)
    def mapGetTheTimeUn(_buff: mapsyst.WTEXT, _size: int) -> int:
        return mapGetTheTimeUn_t (_buff.buffer(), _size)

    mapGetTheTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTheTime', ctypes.c_char_p, ctypes.c_int)
    def mapGetTheTime(_buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetTheTime_t (_buffer, _size)


# Загрузить библиотеку DLL
# На каждый вызов mapLoadLibrary должен выполняться вызов mapFreeLibrary
# При поиске DLL проверяется и директория приложения
#  void (WINAPI # myfunction)(int param);
# (FARPROC)myfunction = mapLoadLibrary("ABC.DLL",&instance,"MyFunction");
#  if (myfunction)
#      { (#myfunction)(123); ::FreeLibrary(#instance); }
# При ошибке возвращает ноль и выдает сообщение на экран

    mapLoadLibrary_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapLoadLibrary', ctypes.c_char_p, ctypes.POINTER(maptype.HINSTANCE), ctypes.c_char_p)
    def mapLoadLibrary(_dllname: ctypes.c_char_p, _libinst: ctypes.POINTER(maptype.HINSTANCE), _funcname: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapLoadLibrary_t (_dllname, _libinst, _funcname)

    mapLoadLibraryEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapLoadLibraryEx', ctypes.c_char_p, ctypes.POINTER(maptype.HINSTANCE), ctypes.c_char_p, ctypes.c_int)
    def mapLoadLibraryEx(_dllname: ctypes.c_char_p, _libinst: ctypes.POINTER(maptype.HINSTANCE), _funcname: ctypes.c_char_p, _message: int) -> ctypes.c_void_p:
        return mapLoadLibraryEx_t (_dllname, _libinst, _funcname, _message)

    mapLoadLibraryUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapLoadLibraryUn', maptype.PWCHAR, ctypes.POINTER(maptype.HINSTANCE), maptype.PWCHAR)
    def mapLoadLibraryUn(_dllname: mapsyst.WTEXT, _libinst: ctypes.POINTER(maptype.HINSTANCE), _funcname: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapLoadLibraryUn_t (_dllname.buffer(), _libinst, _funcname.buffer())


# Выгрузить библиотеку DLL

    mapFreeLibrary_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFreeLibrary', maptype.HINSTANCE)
    def mapFreeLibrary(_libinst: maptype.HINSTANCE) -> int:
        return mapFreeLibrary_t (_libinst)


# Загрузить функцию библиотеки DLL

    mapGetProcAddress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetProcAddress', maptype.HINSTANCE, ctypes.c_char_p)
    def mapGetProcAddress(_libinst: maptype.HINSTANCE, _funcname: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapGetProcAddress_t (_libinst, _funcname)


# Подсчитать контрольную сумму файла по алгоритму CRC32
# При ошибке возвращает ноль

    mapGetFileCrc32_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFileCrc32', maptype.PWCHAR, ctypes.POINTER(ctypes.c_uint))
    def mapGetFileCrc32(_filename: mapsyst.WTEXT, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        return mapGetFileCrc32_t (_filename.buffer(), _value32)


# Подсчитать контрольную сумму записи по алгоритму CRC32
# value32 - текущее значение контрольной суммы и новый результат с учетом переданного буфера
# При первом обращении поле value32 нужно обнулить
# При ошибке возвращает ноль

    mapGetRecordCrc32_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRecordCrc32', ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint))
    def mapGetRecordCrc32(_buffer: ctypes.c_char_p, _size: int, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        return mapGetRecordCrc32_t (_buffer, _size, _value32)


# Сохранить в архиве список файлов
# Если файл один или все файлы в одной папке, то они сохраняются без пути
# Если файлы размещены в поддиректориях одной папки, то они сохраняются с относительными путями
# Если файлы не имеют общего пути, то они сохраняются без пути
# zipname - имя zip-архива
# filelist - массив указателей на пути к файлам
# count - число сохраняемых файлов (элементов массива указателей)
# flag - управляющие флажки (1 - записывать относительные пути в архив)
# error - поле для записи ошибки выполнения программы
# При ошибке возвращает ноль

    mapSaveFilesToZip_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveFilesToZip', maptype.PWCHAR, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR1)), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapSaveFilesToZip(_zipname: mapsyst.WTEXT, _filelist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR1)), _count: int, _flag: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapSaveFilesToZip_t (_zipname.buffer(), _filelist, _count, _flag, _error)


# Формирование имени файла с учетом языка интерфейса
# language - код языка или ноль (
# К имени файла добавляется окончание "_ru", "_en", "_es", ...
# При ошибке возвращает ноль

    mapFileNameWithLanguage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapFileNameWithLanguage', maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapFileNameWithLanguage(_filename: mapsyst.WTEXT, _size: int, _language: int) -> int:
        return mapFileNameWithLanguage_t (_filename.buffer(), _size, _language)


# Вызов окна справки системы с учётом установленного
# функцией mapSetMapAccessLanguage языка сообщений
# helpName - имя файла справки (полное или короткое)
# pageName - имя страницы справки, может быть равно 0
# Пример вызова функции: HelpExecLang("map3d", "Setup");

    HelpExecLangUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'HelpExecLangUn', maptype.PWCHAR, maptype.PWCHAR)
    def HelpExecLangUn(_helpName: mapsyst.WTEXT, _pageName: mapsyst.WTEXT) -> ctypes.c_void_p:
        return HelpExecLangUn_t (_helpName.buffer(), _pageName.buffer())

    HelpExecLang_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'HelpExecLang', ctypes.c_char_p, ctypes.c_char_p)
    def HelpExecLang(_helpName: ctypes.c_char_p, _pageName: ctypes.c_char_p) -> ctypes.c_void_p:
        return HelpExecLang_t (_helpName, _pageName)


# Формирование имени файла справки системы с учётом установленного
# функцией mapSetMapAccessLanguage языка сообщений
# helpName - исходное имя файла справки (без учёта языка сообщений)
# helpNameLang - адрес строки для формируемого имени файла справки
#                (с учётом языка сообщений)
# size - размер строки helpNameLang в байтах

    HelpNameLang_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'HelpNameLang', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def HelpNameLang(_helpName: ctypes.c_char_p, _helpNameLang: ctypes.c_char_p, _size: int) -> int:
        return HelpNameLang_t (_helpName, _helpNameLang, _size)

    HelpNameLangUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'HelpNameLangUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def HelpNameLangUn(_helpName: mapsyst.WTEXT, _helpNameLang: mapsyst.WTEXT, _size: int) -> int:
        return HelpNameLangUn_t (_helpName.buffer(), _helpNameLang.buffer(), _size)


# Сортировка отдельной карты документа
#  mapname - сортируемая карта
#  flags   - Флажки обработки карты :
#   0 - сортировать все листы,
#   1 - только несортированные,
#   2 - сохранять файлы отката,
#   4 - повысить точность хранения, формат - мкм
#  16 - повысить точность хранения, формат - см
#  32 - повысить точность хранения, формат - мм
#  64 - повысить точность хранения, формат - радианы
# 128 - формировать мультиконтура для объектов с флагом мультиконтурный
# hEvent - адрес функции обратного вызова для уведомлении о процессе
# eventparam - параметры функции обратного вызова
# outpath - адрес строки для записи нового пути к отсортированной карте,
#           если адрес строки не задан, то карта обновляется на месте
# size    - размер строки для записи пути
# Если карта отсортирована успешно - возвращает 1
# Если карта уже отсортирована - возвращает 2
# Если оператор прервал операцию - возвращает -1
# Если карта не доступна на редактирование - возвращает -2
# При ошибке возвращает ноль

#    MapSortingWithEvent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'MapSortingWithEvent', ctypes.c_char_p, ctypes.c_int, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.c_int)
#    def MapSortingWithEvent(_mapname: ctypes.c_char_p, _flags: int, _hEvent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _outpath: ctypes.c_char_p, _size: int) -> int:
#        return MapSortingWithEvent_t (_mapname, _flags, _hEvent, _eventparam, _outpath, _size)


# Сортировка отдельной карты документа
# mapname - сортируемая карта
# flags   - Флажки обработки карты :
#   0 - сортировать все листы,
#   1 - только несортированные,
#   2 - сохранять файлы отката,
#   4 - повысить точность хранения, формат - мкм
#  16 - повысить точность хранения, формат - см
#  32 - повысить точность хранения, формат - мм
#  64 - повысить точность хранения, формат - радианы
# 128 - формировать мультиконтура для объектов с флагом мультиконтурный
# handle     - идентификатор окна, которому посылаются сообщения WM_OBJECT и WM_ERROR,
#              если не задан параметр hEvent
# hEvent     - адрес функции обратного вызова для уведомления о проценте выполнения,
#              если параметр не задан, то посылаются сообщения WM_OBJECT и WM_ERROR
# eventparam - параметр, передаваемый функции обратного вызова
# outpath    - буфер для записи пути к папке, куда сохранили отсортированную карту,
#              если задан этот параметр, то исходная карта не обновляется,
#              папка создается автоматически в программе сортировки
# size       - длина буфера в байтах
# format - управление форматом карты :
#  0 - не менять,
#  1 - установить формат SITX (на входе может быть SIT или MAP с одним листом),
#  2 - упаковать карту в формат SITZ\MAPZ, точность - см,
# -1 - установить формат SIT (на входе может быть SITX или MAP с одним листом),
# code - управление шифрованием карты :
#  0 - не менять,
#  1 - шифровать данные с помощью пароля из параметра password (формат SITX),
# -1 - снять шифрование данных
# password - пароль для шифрования данных, когда code = 1, или 0
# Если карта отсортирована успешно - возвращает 1
# Если карта уже отсортирована - возвращает 2
# Если оператор прервал операцию - возвращает -1
# Если карта не доступна на редактирование - возвращает -2
# При ошибке возвращает ноль

#    MapSortingWithEventPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'MapSortingWithEventPro', maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
#    def MapSortingWithEventPro(_mapname: mapsyst.WTEXT, _flags: int, _handle: maptype.HMESSAGE, _hEvent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _outpath: mapsyst.WTEXT, _size: int, _format: int, _code: int, _password: mapsyst.WTEXT) -> int:
#        return MapSortingWithEventPro_t (_mapname, _flags, _handle, _hEvent, _eventparam, _outpath, _size, _format, _code, _password)

    MapSortingSitePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'MapSortingSitePro', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def MapSortingSitePro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flags: int, _handle: maptype.HMESSAGE, _format: int, _code: int, _password: mapsyst.WTEXT) -> int:
        return MapSortingSitePro_t (_hmap, _hsite, _flags, _handle, _format, _code, _password.buffer())

#    MapSortingWithEventUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'MapSortingWithEventUn', maptype.PWCHAR, ctypes.c_int, maptype.HMESSAGE, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, ctypes.c_int)
#    def MapSortingWithEventUn(_mapname: mapsyst.WTEXT, _flags: int, _handle: maptype.HMESSAGE, _hEvent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _outpath: mapsyst.WTEXT, _size: int) -> int:
#        return MapSortingWithEventUn_t (_mapname, _flags, _handle, _hEvent, _eventparam, _outpath, _size)


# Копирование cодержимого открытых файлов
# in     - имя входного файла
# out    - имя выходного файла
# mode   - флажки доступа к выходному файлу (GENERIC_READ, GENERIC_WRITE),
#          ноль соответствует GENERIC_READ,
# access - флажки открытия выходного файла (FILE_SHARE_READ,FILE_SHARE_WRITE)
#          ноль соответствует FILE_SHARE_READ|FILE_SHARE_WRITE
# При ошибке возвращает ноль

    mapCopyFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapCopyFileUn(_in: mapsyst.WTEXT, _out: mapsyst.WTEXT, _access: int = 0, _mode: int = 0) -> int:
        return mapCopyFileUn_t (_in.buffer(), _out.buffer(), _access, _mode)

    mapCopyFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyFile', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapCopyFile(_in: ctypes.c_char_p, _out: ctypes.c_char_p, _access: int = 0, _mode: int = 0) -> int:
        return mapCopyFile_t (_in, _out, _access, _mode)


# Запросить длину файла
# name - полный путь к файлу
# При ошибке возвращает ноль

    mapGetFileLengthUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetFileLengthUn', maptype.PWCHAR)
    def mapGetFileLengthUn(_name: mapsyst.WTEXT) -> float:
        return mapGetFileLengthUn_t (_name.buffer())


# Сравнить содержимое файлов
# Дата и время обновления файлов игнорируются
# При несовпадении возвращает ноль, иначе - ненулевое значение

    mapCompareFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareFiles', maptype.PWCHAR, maptype.PWCHAR)
    def mapCompareFiles(_first: mapsyst.WTEXT, _second: mapsyst.WTEXT) -> int:
        return mapCompareFiles_t (_first.buffer(), _second.buffer())


# Выделить имя крайней папки из пути
# При ошибке возвращает ноль

    mapGetFolderFromPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFolderFromPath', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetFolderFromPath(_spath: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        return mapGetFolderFromPath_t (_spath.buffer(), _folder.buffer(), _size)


# Разрешить/Запретить выдачу сообщений на экран
# (серверный режим работы)
# enable = 0  - запрет выдачи сообщений,
# Возвращает предыдущее значение флага

    mapMessageEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMessageEnable', ctypes.c_int)
    def mapMessageEnable(_enable: int) -> int:
        return mapMessageEnable_t (_enable)

    mapIsMessageEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMessageEnable')
    def mapIsMessageEnable() -> int:
        return mapIsMessageEnable_t ()



# Выдать сообщение об ошибке (на экран)
# hwnd - идентификатор родительского окна для выдачи сообщения или 0
# code - код ошибки (см. MAPERR.RH)
# filename - имя файла (объекта), для которого возникла ошибка
# message  - адрес строки для размещения текста сообщения (для записи
#            в протокол и т.п.), область памяти должна быть
#            не менее длины имени файла + 256 байт; значение может быть 0
# isshow   - признак вывода сообщения на экран

    mapErrorMessageLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessageLog', maptype.HWND, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapErrorMessageLog(_hwnd: maptype.HWND, _code: int, _filename: mapsyst.WTEXT, _message: mapsyst.WTEXT, _size: int, _isshow: int) -> ctypes.c_void_p:
        return mapErrorMessageLog_t (_hwnd, _code, _filename.buffer(), _message.buffer(), _size, _isshow)

    mapErrorMessagePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessagePro', maptype.HWND, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapErrorMessagePro(_hwnd: maptype.HWND, _code: int, _filename: mapsyst.WTEXT, _message: mapsyst.WTEXT, _isshow: int) -> ctypes.c_void_p:
        return mapErrorMessagePro_t (_hwnd, _code, _filename.buffer(), _message.buffer(), _isshow)

    mapErrorMessageExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessageExUn', maptype.HWND, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR)
    def mapErrorMessageExUn(_hwnd: maptype.HWND, _code: int, _filename: mapsyst.WTEXT, _message: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapErrorMessageExUn_t (_hwnd, _code, _filename.buffer(), _message.buffer())


# Выдать сообщение об ошибке (на экран)
# code - код ошибки (см. MAPERR.RH)

    mapErrorMessageUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessageUn', ctypes.c_int, maptype.PWCHAR)
    def mapErrorMessageUn(_code: int, _filename: mapsyst.WTEXT) -> ctypes.c_void_p:
        if (isinstance(_filename, str)):
            return mapErrorMessageUn_t (_code, (_filename + '\0').encode('utf-16LE'))
        return mapErrorMessageUn_t (_code, _filename.buffer())

    ErrorMessageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ErrorMessageEx', maptype.HMESSAGE, ctypes.c_int, ctypes.c_char_p)
    def ErrorMessageEx(_hwnd: maptype.HMESSAGE, _code: int, _filename: ctypes.c_char_p) -> ctypes.c_void_p:
        return ErrorMessageEx_t (_hwnd, _code, _filename)

    mapErrorMessage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessage', ctypes.c_int, ctypes.c_char_p)
    def mapErrorMessage(_code: int, _filename: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapErrorMessage_t (_code, _filename)


# Установить функцию обратного вызова для перехвата и замены
# сообщений об ошибках и вопросах, выдаваемых из ГИС-ядра
# через системную функцию MessageBox
# call - адрес функции обратного вызова (прототип в maptype.h)
# parm - значение первого параметра в функции обратного вызова (может быть 0)
# Остальные параметры в функции обратного вызова имеют то же назначение,
# что и параметры в функции MessageBox для UNICODE

#    mapSetMessageBoxCall_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMessageBoxCall', maptype.MESSAGEBOXCALL, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetMessageBoxCall(_call: maptype.MESSAGEBOXCALL, _parm: ctypes.POINTER(ctypes.c_void_p)) -> ctypes.c_void_p:
#        return mapSetMessageBoxCall_t (_call, _parm)


# Выдать сообщение на экран через системную функцию MessageBox
# Если mapIsMessageEnable() равно 0, то сообщение не выдается и функция возвращает ноль
# Если установлена функция обратного вызова mapSetMessageBoxCall, то выдача сообщения будет через эту функцию

    mapMessageBoxUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMessageBoxUn', maptype.HWND, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapMessageBoxUn(_message: mapsyst.WTEXT, _title: mapsyst.WTEXT, _flag=64) -> int:
        if (isinstance(_message, str)):
           if (isinstance(_title, str)):
              return mapMessageBoxUn_t (0, (_message + '\0').encode('utf-16LE'), (_title + '\0').encode('utf-16LE'), _flag)
           else:
              return mapMessageBoxUn_t (0, (_message + '\0').encode('utf-16LE'), _title.buffer(), _flag)
        else:
           if (isinstance(_title, str)):
              return mapMessageBoxUn_t (0, _message.buffer(), (_title + '\0').encode('utf-16LE'), _flag)
           else: 
              return mapMessageBoxUn_t (0, _message.buffer(), _title.buffer(), _flag)

    mapMessageBox_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapMessageBox', maptype.HWND, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapMessageBox(_hwnd: maptype.HWND, _message: ctypes.c_char_p, _title: ctypes.c_char_p, _flag: int) -> int:
        return mapMessageBox_t (_hwnd, _message, _title, _flag)


# Расчёт времени выполнения программы в виде строки "HH:MM:SS / HH:MM:SS",
# с указанием прошедшего времени и оставшегося до завершения
# begtime - временя старта программы,
# total   - общее число обрабатываемых элементов (например, 100 - в процентах),
# current - число обработанных элементов (например, выполненный процент работы программы)
# message - буфер для записи строки
# size    - размер буфера в байтах (не менее 64 байт)
# При ошибке в параметрах возвращает ноль

    mapSetTimeStringExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTimeStringExUn', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_int)
    def mapSetTimeStringExUn(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: float, _current: float, _message: mapsyst.WTEXT, _size: int) -> int:
        return mapSetTimeStringExUn_t (_begtime, _total, _current, _message.buffer(), _size)

    mapSetTimeStringEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTimeStringEx', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_int)
    def mapSetTimeStringEx(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: float, _current: float, _message: ctypes.c_char_p, _size: int) -> int:
        return mapSetTimeStringEx_t (_begtime, _total, _current, _message, _size)

    mapSetTimeStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTimeStringUn', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_int, ctypes.c_double, maptype.PWCHAR, ctypes.c_int)
    def mapSetTimeStringUn(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: int, _current: float, _message: mapsyst.WTEXT, _size: int) -> int:
        return mapSetTimeStringUn_t (_begtime, _total, _current, _message.buffer(), _size)

    mapSetTimeString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTimeString', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_int)
    def mapSetTimeString(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: int, _current: float, _message: ctypes.c_char_p, _size: int) -> int:
        return mapSetTimeString_t (_begtime, _total, _current, _message, _size)


# Выдать сообщение в протокол карты
# HMAP и HSITE определяют карту, в протокол которой
# записывается сообщение
# (для карты местности HSITE = HMAP, см. sitapi.h)
# code    - код ошибки (из maperr.rh) или 0
# message - текст сообщения
# type - тип сообщения (см. maptype.h : MT_INFO,MT_ERROR,...)

    mapMessageToLogEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageToLogEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapMessageToLogEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _code: int, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapMessageToLogEx_t (_hMap, _hSite, _code, _message.buffer(), _type)

    mapMessageToLogUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageToLogUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapMessageToLogUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapMessageToLogUn_t (_hMap, _hSite, _message.buffer(), _type)

    mapMessageToLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageToLog', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int)
    def mapMessageToLog(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _message: ctypes.c_char_p, _type: int) -> ctypes.c_void_p:
        return mapMessageToLog_t (_hMap, _hSite, _message, _type)


# Запросить версию модуля MapAccess.Dll
# Если полученная версия не равна значению MAPACCESSVERSION
# в работе программы может произойти сбой

    mapGetMapAccessVersion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapAccessVersion')
    def mapGetMapAccessVersion() -> int:
        return mapGetMapAccessVersion_t ()

    mapGetMapApiVersion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapApiVersion')
    def mapGetMapApiVersion() -> int:
        return mapGetMapApiVersion_t ()


# Установить/Запросить язык сообщений
# 1 - английский, 2 - русский, ... (см. Maptype.h)
# (по-умолчанию - английский)

    mapSetMapAccessLanguage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMapAccessLanguage', ctypes.c_int)
    def mapSetMapAccessLanguage(_code: int) -> ctypes.c_void_p:
        return mapSetMapAccessLanguage_t (_code)

    mapGetMapAccessLanguage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapAccessLanguage')
    def mapGetMapAccessLanguage() -> int:
        return mapGetMapAccessLanguage_t ()


# Установить идентификатор окна для приема сообщений
# от "затяжных" процессов (перекодировка при открытии
# карты, нарезка объектов по заданной границе,...)
# Код сообщения - WM_PROGRESSBARUN,
# wparm : -1 старт процесса,-2 завершение,0-100 процент выполнения
# lparm : текст сообщения в кодировке UTF-16
# Для отмены сообщений - установить идентификатор в ноль
# (Идентификатор закрытого окна может привести к сбою в системе)
# Для завершения процесса вернуть число WM_PROGRESSBARUN
# Возвращает предыдущее значение идентификатора

    mapSetHandleForMessage_t = mapsyst.GetProcAddress(acceslib,maptype.HMESSAGE,'mapSetHandleForMessage', maptype.HMESSAGE)
    def mapSetHandleForMessage(_hwnd: maptype.HMESSAGE) -> maptype.HMESSAGE:
        return mapSetHandleForMessage_t (_hwnd)

    mapGetHandleForMessage_t = mapsyst.GetProcAddress(acceslib,maptype.HMESSAGE,'mapGetHandleForMessage')
    def mapGetHandleForMessage() -> maptype.HMESSAGE:
        return mapGetHandleForMessage_t ()


# Установить идентификатор окна для приема сообщений о событиях карты
# hmap   - идентификатор открытых данных
# hwnd   - идентификатор окна
# event - флаг типов событий (1 - перерисовка карты)
# Код сообщения WM_MAPEVENT (0x591)
# wparm : идентификатор карты, в которой произошло событие (HMAP)
# lparm : описание события
# Для отмены сообщений - установить идентификатор в ноль
# (Идентификатор закрытого окна может привести к сбою в системе)
# При ошибке возвращает ноль
    if os.name == 'nt':
        mapSetHandleForEvent_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapSetHandleForEvent', maptype.HMAP, maptype.HWND, ctypes.c_int)
        def mapSetHandleForEvent(_hmap: maptype.HMAP, _hwnd: maptype.HWND, _event: int) -> int:
            return mapSetHandleForEvent_t(_hmap, _hwnd, _event)


# Запросить текущее значение идентификатора окна для приема сообщений

    if os.name == 'nt':
        mapGetHandleForEvent_t = mapsyst.GetProcAddress(acceslib,maptype.HWND,'mapGetHandleForEvent', maptype.HMAP)
        def mapGetHandleForEvent(_hmap: maptype.HMAP) -> maptype.HWND:
            return mapGetHandleForEvent_t (_hmap)


# Уточнение положения диалога относительно габаритов рабочего стола
# Входные параметры:
#   left, top, width, height -  адреса значений положения и размеров
#   проверямого окна диалога. Уточненные величины положения и размеров
#   присваиваются по этим же адресам.
#
# При ошибке и отсутсвии изменений положения и размеров окна
# возвращает ноль.
# При изменении положения и размеров окна возвращает единицу.
    if os.name == 'nt':
        mapAdjustFormBounds_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapAdjustFormBounds', ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        def mapAdjustFormBounds(_left: ctypes.POINTER(ctypes.c_int), _top: ctypes.POINTER(ctypes.c_int), _width: ctypes.POINTER(ctypes.c_int), _height: ctypes.POINTER(ctypes.c_int)) -> int:
            return mapAdjustFormBounds_t(_left, _top, _width, _height)


# Добавить строку UNICODE в буфер обмена
# При ошибке возвращает ноль
    if os.name == 'nt':
        mapSetTextToClipboardUn_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapSetTextToClipboardUn', maptype.PWCHAR)
        def mapSetTextToClipboardUn(_strW: mapsyst.WTEXT) -> int:
            return mapSetTextToClipboardUn_t(_strW.buffer())

        mapSetTextToClipboard_t = mapsyst.GetProcAddress(acceslib, ctypes.c_int, 'mapSetTextToClipboard', ctypes.c_char_p)
        def mapSetTextToClipboard(_str: ctypes.c_char_p) -> int:
            return mapSetTextToClipboard_t(_str)


# Сравнить две строки без учета регистра
# Возвращает : (1-CMLESS, 2-CMEQUAL, 3-CMMORE - см. Maptype.h)
# При ошибке возвращает ноль

    mapCompareStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareStringUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapCompareStringUn(_value: mapsyst.WTEXT, _temp: mapsyst.WTEXT) -> int:
        return mapCompareStringUn_t (_value.buffer(), _temp.buffer())

    mapCompareString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompareString', ctypes.c_char_p, ctypes.c_char_p)
    def mapCompareString(_string: ctypes.c_char_p, _filter: ctypes.c_char_p) -> int:
        return mapCompareString_t (_string, _filter)


# Преобразовать дату из строки date в число ГГГГММДД
# Строка может иметь вид ДД/ММ/ГГГГ или ДД.ММ.ГГГГ
# или ГГГГММДД или ГГГГ/ММ/ДД или ГГГГ-ММ-ДД
# При ошибке возвращает ноль, иначе - значение даты

    mapDateToLongUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDateToLongUn', maptype.PWCHAR)
    def mapDateToLongUn(_date: mapsyst.WTEXT) -> int:
        return mapDateToLongUn_t (_date.buffer())

    mapDateToLong_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDateToLong', ctypes.c_char_p)
    def mapDateToLong(_date: ctypes.c_char_p) -> int:
        return mapDateToLong_t (_date)


# Преобразовать время из строки time в число ЧЧММСС
# Строка может иметь вид ЧЧ:ММ:СС
# При ошибке возвращает ноль, иначе - значение даты

    mapTimeToLong_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTimeToLong', ctypes.c_char_p)
    def mapTimeToLong(_time: ctypes.c_char_p) -> int:
        return mapTimeToLong_t (_time)


# Преобразовать время из из числа ЧЧММСС в строку с системным и локальным временем
# ЧЧ:ММ:СС (ЧЧ:ММ:СС) - значение в скобках содержит локальное время
# number - числовое значение времени,
# time   - адрес строки для результата
# size   - размер строки для контроля
# При ошибке возвращает ноль, иначе - адрес входной строки

    mapTimeToLongUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTimeToLongUn', maptype.PWCHAR)
    def mapTimeToLongUn(_time: mapsyst.WTEXT) -> int:
        return mapTimeToLongUn_t (_time.buffer())


# Преобразовать угловую величину в градусах из строки
# в числовое значение в радианах
# Строка может иметь вид ГГГ°ММ'CC.CC" или ГГГ.ГГГГГГГГ°
# Для Linux вместо символа ° (\xB0) д.б. ^
# При ошибке возвращает ноль, иначе - значение в радианах

    mapAngleToRadianUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapAngleToRadianUn', maptype.PWCHAR)
    def mapAngleToRadianUn(_angle: mapsyst.WTEXT) -> float:
        return mapAngleToRadianUn_t (_angle.buffer())

    mapAngleToRadian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapAngleToRadian', ctypes.c_char_p)
    def mapAngleToRadian(_angle: ctypes.c_char_p) -> float:
        return mapAngleToRadian_t (_angle)


# Запись номера объекта в виде строки XXXXX/XXXXX или ХХХХХХХХХХХ
# (например, 16777339 соответствует строка 256/123)
# format - формат строки: 1 - XXXXX/XXXXX, 2 - XXXXXXXXXXX,
# 0 - взять значение по умолчанию (mapGetObjectKeyFormat).
# Минимальная длина выходной строки - 12 байт
# При ошибке возвращает ноль

    mapObjectKeyToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectKeyToStringUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapObjectKeyToStringUn(_key: int, _string: mapsyst.WTEXT, _size: int, _format: int) -> int:
        return mapObjectKeyToStringUn_t (_key, _string.buffer(), _size, _format)

    mapObjectKeyToString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapObjectKeyToString', ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapObjectKeyToString(_key: int, _string: ctypes.c_char_p, _size: int, _format: int) -> int:
        return mapObjectKeyToString_t (_key, _string, _size, _format)


# Преобразование номера объекта из строки XXXXX/XXXXX или ХХХХХХХХХХХ
# в число (например, 16777339 соответствует строка 256/123)
# string - входная строка
# long   - результат
# При ошибке возвращает ноль

    mapStringToObjectKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapStringToObjectKeyUn', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapStringToObjectKeyUn(_string: mapsyst.WTEXT, _key: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapStringToObjectKeyUn_t (_string.buffer(), _key)

    mapStringToObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapStringToObjectKey', ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
    def mapStringToObjectKey(_string: ctypes.c_char_p, _key: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapStringToObjectKey_t (_string, _key)


# Установить/Запросить формат номера объекта
# 1 - XXXXX/XXXXX, 2 - XXXXXXXXXXX

#   mapGetObjectKeyFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectKeyFormat', )
#   def mapGetObjectKeyFormat(_void) -> int:
#       return mapGetObjectKeyFormat_t (_void)

    mapSetObjectKeyFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectKeyFormat', ctypes.c_int)
    def mapSetObjectKeyFormat(_format: int) -> int:
        return mapSetObjectKeyFormat_t (_format)


# Сконвертировать значение строки, убрав спецсимволы XML ('\"', '?', '>', '<', '&', '\'' '\n')
# semval - входная строка в кодировке ANSI
# outval - выходная строка в кодировке ANSI (&quot; и т.д.)
# outsize - размер выходной строки в байтах
# При ошибке возвращает 0

    ConvertStringToXmlStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'ConvertStringToXmlStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def ConvertStringToXmlStringUn(_inval: mapsyst.WTEXT, _outval: mapsyst.WTEXT, _outsize: int) -> int:
        return ConvertStringToXmlStringUn_t (_inval.buffer(), _outval.buffer(), _outsize)

    ConvertStringToXmlString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'ConvertStringToXmlString', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def ConvertStringToXmlString(_semval: ctypes.c_char_p, _outval: ctypes.c_char_p, _outsize: int) -> int:
        return ConvertStringToXmlString_t (_semval, _outval, _outsize)


# Сконвертировать значение строки, заменив спецсимволы JSON ('\"', '\n', '\r', '\v', '\\', '\t')
# Заменяет '\"' на '\'', а остальные спецсимволы на пробелы
# inval  - обрабатываемая строка в кодировке UTF16, заканчивающаяся символом конца строки

    ConvertStringToJsonStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ConvertStringToJsonStringUn', maptype.PWCHAR)
    def ConvertStringToJsonStringUn(_inval: mapsyst.WTEXT) -> ctypes.c_void_p:
        return ConvertStringToJsonStringUn_t (_inval.buffer())

    ConvertStringToJsonString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ConvertStringToJsonString', ctypes.c_char_p)
    def ConvertStringToJsonString(_inval: ctypes.c_char_p) -> ctypes.c_void_p:
        return ConvertStringToJsonString_t (_inval)


# Экранировать спецсимволы строки JSON ('\"', '\n', '\r', '\v', '\\', '\t')
# inval  - обрабатываемая строка в кодировке UTF16, заканчивающаяся символом конца строки

    ShieldStringToJsonStringUnEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ShieldStringToJsonStringUnEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def ShieldStringToJsonStringUnEx(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outstring_size: int) -> ctypes.c_void_p:
        return ShieldStringToJsonStringUnEx_t (_instring.buffer(), _outstring.buffer(), _outstring_size)

    ShieldStringToJsonString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ShieldStringToJsonString', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def ShieldStringToJsonString(_instring: ctypes.c_char_p, _outstring: ctypes.c_char_p, _outstring_size: int) -> ctypes.c_void_p:
        return ShieldStringToJsonString_t (_instring, _outstring, _outstring_size)


# Сконвертировать значение строки, восстановив спецсимволы XML
# text - входная строка
# outtext - выходная строка
# size - размер выходной строки в байтах
# При ошибке возвращает 0

    ConvertFromXmlToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'ConvertFromXmlToStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def ConvertFromXmlToStringUn(_text: mapsyst.WTEXT, _outtext: mapsyst.WTEXT, _size: int) -> int:
        return ConvertFromXmlToStringUn_t (_text.buffer(), _outtext.buffer(), _size)

    ConvertFromXmlToString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'ConvertFromXmlToString', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def ConvertFromXmlToString(_text: ctypes.c_char_p, _outtext: ctypes.c_char_p, _size: int) -> int:
        return ConvertFromXmlToString_t (_text, _outtext, _size)


# Установить/Запросить путь к директории приложения, где
# располагаются вспомогательные файлы для функционирования
# ГИС-ядра (библиотеки ядра, библиотеки отрисовки программируемых знаков #.iml,
# файлы базы данных epsg.#, wmslist_xx.xml, xml-схемы и другие файлы)
# Рекомендуется устанавливать при запуске приложения

    mapSetPathShellUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetPathShellUn', maptype.PWCHAR)
    def mapSetPathShellUn(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetPathShellUn_t (_path.buffer())

    mapGetPathShellUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetPathShellUn', maptype.PWCHAR, ctypes.c_int)
    def mapGetPathShellUn(_path: mapsyst.WTEXT, _size: int) -> ctypes.c_void_p:
        return mapGetPathShellUn_t (_path.buffer(), _size)

    mapSetPathShell_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetPathShell', ctypes.c_char_p)
    def mapSetPathShell(_path: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapSetPathShell_t (_path)

    mapGetPathShellEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetPathShellEx', ctypes.c_char_p, ctypes.c_int)
    def mapGetPathShellEx(_path: ctypes.c_char_p, _size: int) -> ctypes.c_void_p:
        return mapGetPathShellEx_t (_path, _size)


# Установить новое имя INI-файла приложения

    mapSetIniPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetIniPathUn', maptype.PWCHAR)
    def mapSetIniPathUn(_inipath: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetIniPathUn_t (_inipath.buffer())

    mapSetIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetIniPath', ctypes.c_char_p)
    def mapSetIniPath(_inipath: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapSetIniPath_t (_inipath)


# Установить/Запросить путь к размещению данных
# path - адрес строки в кодировке UTF-16 c путем к папке для размещения данных
# size - длина строки (буфера) в байтах

    mapSetDataPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetDataPathUn', maptype.PWCHAR)
    def mapSetDataPathUn(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetDataPathUn_t (_path.buffer())

    mapGetDataPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetDataPathUn', maptype.PWCHAR, ctypes.c_int)
    def mapGetDataPathUn(_path: mapsyst.WTEXT, _size: int) -> ctypes.c_void_p:
        return mapGetDataPathUn_t (_path.buffer(), _size)


# Установить путь к общей папке файлов параметров задач системы (INI, XML)
# При ошибке возвращает ноль

    mapSetCommonIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCommonIniPath', maptype.PWCHAR)
    def mapSetCommonIniPath(_path: mapsyst.WTEXT) -> int:
        return mapSetCommonIniPath_t (_path.buffer())


# Запросить имя INI-файла документа в кодировке UNICODE
# name - адрес строки для размещения результата
# size - размер строки в байтах
# При ошибке возвращает 0

    mapGetMapIniNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapIniNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapIniNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapIniNameUn_t (_hMap, _name.buffer(), _size)


# Сформировать имя INI-файла по имени открываемых данных
# name - путь к открываемому файлу данных или алиас данных с ГИС-Сервера или
# URL геопортала
# mapininame - адрес строки для размещения результата
# size - размер строки, зарезервированный для размещения результата (не менее 260 байт)
# При ошибке возвращает ноль

    mapBuildIniNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildIniNameUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapBuildIniNameUn(_name: mapsyst.WTEXT, _mapininame: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildIniNameUn_t (_name.buffer(), _mapininame.buffer(), _size)

    mapBuildIniName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildIniName', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapBuildIniName(_name: ctypes.c_char_p, _mapininame: ctypes.c_char_p, _size: int) -> int:
        return mapBuildIniName_t (_name, _mapininame, _size)


# Установить путь к общим файлам классификаторам (RSC)
# При ошибке возвращает ноль

    mapSetCommonRscPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCommonRscPathUn', maptype.PWCHAR)
    def mapSetCommonRscPathUn(_rscpath: mapsyst.WTEXT) -> int:
        return mapSetCommonRscPathUn_t (_rscpath.buffer())


# Установить путь к папке для хранения кэшируемых данных с ГИС Сервер
# При ошибке возвращает ноль

    mapSetApplicationDataPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetApplicationDataPathUn', maptype.PWCHAR)
    def mapSetApplicationDataPathUn(_path: mapsyst.WTEXT) -> int:
        return mapSetApplicationDataPathUn_t (_path.buffer())


# Проверить, что имя файла не является алиасом сервера или геопортала
# При отсутствии спецсимволов возвращает ненулевое значение

    mapIsNormalPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsNormalPath', ctypes.c_char_p)
    def mapIsNormalPath(_name: ctypes.c_char_p) -> int:
        return mapIsNormalPath_t (_name)

    mapIsNormalPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsNormalPathUn', maptype.PWCHAR)
    def mapIsNormalPathUn(_name: mapsyst.WTEXT) -> int:
        return mapIsNormalPathUn_t (_name.buffer())


# Преобразовать имя алиаса или соединения с сервисом в имя файла (без пути)
# Длина имени c расширением усекается до 204 символов
# alias - имя алиаса или соединения с сервисом (WMS, WFS, WCS)
# name  - адрес строки для размещения результата
# size  - размер выделенной памяти в строке в байтах
# При ошибке возвращает ноль

    mapAliasToNormalNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAliasToNormalNameUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapAliasToNormalNameUn(_alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapAliasToNormalNameUn_t (_alias.buffer(), _name.buffer(), _size)

    mapAliasToNormalName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAliasToNormalName', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapAliasToNormalName(_alias: ctypes.c_char_p, _name: ctypes.c_char_p, _size: int) -> int:
        return mapAliasToNormalName_t (_alias, _name, _size)


# Формирование сокращенного имени файла из полного имени
# для отображения в различных диалогах
# source - исходный путь,
# target - полученная строка (c:\abc..\klm.ext),
# size   - предельный размер выходной строки в символах !!!
# При ошибке возвращает ноль

    mapPathToShortUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPathToShortUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapPathToShortUn(_source: mapsyst.WTEXT, _target: mapsyst.WTEXT, _size: int) -> int:
        return mapPathToShortUn_t (_source.buffer(), _target.buffer(), _size)

    mapPathToShort_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPathToShort', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapPathToShort(_source: ctypes.c_char_p, _target: ctypes.c_char_p, _size: int) -> int:
        return mapPathToShort_t (_source, _target, _size)


# Построить "длинное" имя файла (полный путь к файлу)
# templ - эталонный путь, относительно которого строится полный путь;
# templ - путь к библиотекам приложения (mapGetPathShellUnicode)
# name  - короткий путь к файлу; например, имя файла
# path  - "длинное" имя файла (указатель на массив для размещения результата)
# size  - размер массива для размещения результата в байтах
# При ошибке возвращает ноль

    mapBuildLongNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildLongNameEx', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapBuildLongNameEx(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildLongNameEx_t (_templ.buffer(), _name.buffer(), _path.buffer(), _size)

    mapBuildLongNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildLongNameUn', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def mapBuildLongNameUn(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT, _path: mapsyst.WTEXT) -> int:
        return mapBuildLongNameUn_t (_templ.buffer(), _name.buffer(), _path.buffer())


# Запомнить имя приложения

    mapSetApplicationNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetApplicationNameUn', maptype.PWCHAR)
    def mapSetApplicationNameUn(_name: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetApplicationNameUn_t (_name.buffer())


# Запросить глубину Dib
# Возвращает количество бит, выделяемое на одну точку изображения карты

    mapGetMapScreenDepth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapScreenDepth')
    def mapGetMapScreenDepth() -> int:
        return mapGetMapScreenDepth_t ()


# Выполнить скрипт на python и вернуть результат вычислений
# hmap - идентификатор открытого документа
# hobj - идентификатор выбранного объекта или ноль
# path - полный путь к файлу py, содержащему код скрипта на python
# function - имя выполняемой функции на python вида def Function(hmap:HMAP, hobj:HOBJ) -> float:
# error - возвращаемый код ошибки выполнения скрипта
# При ошибке возвращает ноль

#    mapCallPython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallPython', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double))
#    def mapCallPython(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int), _value: ctypes.POINTER(ctypes.c_double)) -> int:
#        return mapCallPython_t (_hmap, _hobj, _path.buffer(), _function.buffer(), _error, _value)


# Установить текущие координаты курсора для карты
# hmap     - идентификатор открытой карты (документа)
# position - координаты курсора в текущей системе координат документа
# Если position равно нулю, то координаты считаются не установленными

    mapSetMarkerPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMarkerPosition', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMarkerPosition(_hmap: maptype.HMAP, _position: ctypes.POINTER(maptype.DOUBLEPOINT)) -> ctypes.c_void_p:
        return mapSetMarkerPosition_t (_hmap, _position)


# Запросить текущие координаты курсора для карты
# hmap     - идентификатор открытой карты (документа)
# position - координаты курсора в текущей системе координат документа
# Если координаты не установлены, или параметры ошибочные, то возвращает ноль

    mapGetMarkerPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMarkerPosition', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMarkerPosition(_hmap: maptype.HMAP, _position: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetMarkerPosition_t (_hmap, _position)


# Установить адрес функции, которая будет периодически
# вызываться при смене координат курсора (вызове mapSetMarkerPosition)
# Для запроса координат необходимо вызвать mapGetMarkerPosition
# call - адрес вызываемой функции (см. maptype.h),
# parm - параметр, который будет передан вызываемой функции
# При завершении задачи, установившей адрес функции оповещения,
# необходимо еще раз вызвать функцию с нулевыми параметрами
# call и parm.

#    mapSetMarkerPositionCallAndParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMarkerPositionCallAndParm', maptype.HMAP, maptype.BREAKCALL, ctypes.POINTER(ctypes.c_void_p))
#    def mapSetMarkerPositionCallAndParm(_hmap: maptype.HMAP, _call: maptype.BREAKCALL, _parm: ctypes.POINTER(ctypes.c_void_p)) -> ctypes.c_void_p:
#        return mapSetMarkerPositionCallAndParm_t (_hmap, _call, _parm)


# Установить предельные размеры буфера изображения (не влияет на расчет разрешения экрана)
# Функция должна вызываться до открытия данных
# Чтобы оставить ширину или высоту без изменения соответствующий параметр
# должен быть равен 0
# Если экран компьютера, на котором выполняется программа, имеет большие
# размеры, то установленные значения будут автоматически увеличены до
# размеров экрана
# При ошибке возвращает ноль

    mapSetMaxScreenImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMaxScreenImageSize', ctypes.c_int, ctypes.c_int)
    def mapSetMaxScreenImageSize(_width: int, _height: int) -> int:
        return mapSetMaxScreenImageSize_t (_width, _height)


# Установить расчетные размеры буфера изображения (влияет на расчет разрешения экрана)
# Функция должна вызываться до открытия данных
# Чтобы оставить ширину или высоту без изменения соответствующий параметр
# должен быть равен 0
# Если экран компьютера, на котором выполняется программа, имеет большие
# размеры, то установленные значения будут автоматически увеличены до
# размеров экрана
# При ошибке возвращает ноль

    mapSetScreenImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScreenImageSize', ctypes.c_int, ctypes.c_int)
    def mapSetScreenImageSize(_width: int, _height: int) -> int:
        return mapSetScreenImageSize_t (_width, _height)

    SetScreenImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'SetScreenImageSize', ctypes.c_int, ctypes.c_int)
    def SetScreenImageSize(_width: int, _height: int) -> int:
        return SetScreenImageSize_t (_width, _height)


# Запросить максимальную ширину изображения карты в точках
# Установка нового значения - mapSetScreenImageSize

    mapGetMaxScreenWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMaxScreenWidth')
    def mapGetMaxScreenWidth() -> int:
        return mapGetMaxScreenWidth_t ()

    mapGetScreenWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScreenWidth')
    def mapGetScreenWidth() -> int:
        return mapGetScreenWidth_t ()


# Запросить максимальную высоту изображения карты в точках
# Установка нового значения - mapSetScreenImageSize

    mapGetMaxScreenHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMaxScreenHeight')
    def mapGetMaxScreenHeight() -> int:
        return mapGetMaxScreenHeight_t ()

    mapGetScreenHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScreenHeight')
    def mapGetScreenHeight() -> int:
        return mapGetScreenHeight_t ()


# Запросить/Установить размер диагонали видимого изображения
# экрана в миллиметрах (50 - 4000). При установке возвращает
# старое значение
# hdc - контекст главного окна для запроса текущих размеров
# экрана в пикселах
# При ошибке возвращает ноль

    mapGetScreenSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetScreenSizeEx')
    def mapGetScreenSizeEx() -> float:
        return mapGetScreenSizeEx_t ()

    mapSetScreenSizePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetScreenSizePro', ctypes.c_double)
    def mapSetScreenSizePro(_size: float) -> float:
        return mapSetScreenSizePro_t (_size)

    mapGetScreenSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScreenSize')
    def mapGetScreenSize() -> int:
        return mapGetScreenSize_t ()

    mapSetScreenSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScreenSize', ctypes.c_int)
    def mapSetScreenSize(_size: int) -> int:
        return mapSetScreenSize_t (_size)

    mapSetScreenSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScreenSizeEx', ctypes.c_int, maptype.HDC)
    def mapSetScreenSizeEx(_size: int, _hdc: maptype.HDC) -> int:
        return mapSetScreenSizeEx_t (_size, _hdc)


# Запросить/Установить коэффициент масштабирования изображения
# экрана в процентах (50 - 200). При установке возвращает
# старое значение и пересчитывает точность текущего режима экрана
# При ошибке возвращает ноль

    mapGetScreenScaleEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetScreenScaleEx')
    def mapGetScreenScaleEx() -> float:
        return mapGetScreenScaleEx_t ()

    mapSetScreenScaleEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetScreenScaleEx', ctypes.c_double)
    def mapSetScreenScaleEx(_scale: float) -> float:
        return mapSetScreenScaleEx_t (_scale)

    mapGetScreenScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScreenScale')
    def mapGetScreenScale() -> int:
        return mapGetScreenScale_t ()

    mapSetScreenScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScreenScale', ctypes.c_int)
    def mapSetScreenScale(_scale: int) -> int:
        return mapSetScreenScale_t (_scale)


# Запросить/Установить точность текущего режима экрана в точках
# на метр (1000 - 100000). При установке возвращает старое
# значение и пересчитывает коэффициент масштабирования экрана
# При ошибке возвращает ноль

    mapSetScreenPrecisionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetScreenPrecisionEx', ctypes.c_double, ctypes.c_double)
    def mapSetScreenPrecisionEx(_valueHor: float, _valueVer: float) -> ctypes.c_void_p:
        return mapSetScreenPrecisionEx_t (_valueHor, _valueVer)

    mapGetHorizontalScreenPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHorizontalScreenPrecision')
    def mapGetHorizontalScreenPrecision() -> float:
        return mapGetHorizontalScreenPrecision_t ()

    mapGetVerticalScreenPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetVerticalScreenPrecision')
    def mapGetVerticalScreenPrecision() -> float:
        return mapGetVerticalScreenPrecision_t ()

    mapGetScreenPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScreenPrecision')
    def mapGetScreenPrecision() -> int:
        return mapGetScreenPrecision_t ()

    mapSetScreenPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScreenPrecision', ctypes.c_int)
    def mapSetScreenPrecision(_value: int) -> int:
        return mapSetScreenPrecision_t (_value)


# Пересчет через текущие параметры экрана
# из метров экрана в пикселы и обратно

    mapScreenMeter2Pixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapScreenMeter2Pixel', ctypes.c_double)
    def mapScreenMeter2Pixel(_metric: float) -> int:
        return mapScreenMeter2Pixel_t (_metric)

    mapScreenPixel2Meter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapScreenPixel2Meter', ctypes.c_int)
    def mapScreenPixel2Meter(_pixel: int) -> float:
        return mapScreenPixel2Meter_t (_pixel)


# Пересчет через текущие параметры экрана из пикселов в мкм

    mapScreenToMkm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapScreenToMkm', maptype.HMAP, ctypes.c_int)
    def mapScreenToMkm(_hmap: maptype.HMAP, _pixels: int) -> int:
        return mapScreenToMkm_t (_hmap, _pixels)


# Компрессия данных по алгоритму типа LZW
#  in      - массив исходных данных
#  out     - массив выходных (сжатых) данных
#  sizein  - размер массива исходных данных
#  sizeout - размер массива выходных (сжатых) данных
# Возвращает размер сжатых данных в выходном буфере
# При ошибке или при сжатии менее чем на 20%
# выходной массив не заполняется и функция возвращает 0.

    mapCompressLZW_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompressLZW', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapCompressLZW(_in: ctypes.c_char_p, _sizein: int, _out: ctypes.c_char_p, _sizeout: int) -> int:
        return mapCompressLZW_t (_in, _sizein, _out, _sizeout)


# Декомпрессия данных по алгоритму типа LZW
#  in      - массив исходных (сжатых) данных
#  out     - массив выходных данных
#  sizein  - размер массива исходных (сжатых) данных
#  sizeout - размер массива выходных данных
# При ошибке возвращает 0

    mapDecompressLZW_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDecompressLZW', ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapDecompressLZW(_in: ctypes.c_char_p, _sizein: int, _out: ctypes.c_char_p, _sizeout: int) -> int:
        return mapDecompressLZW_t (_in, _sizein, _out, _sizeout)


# Компрессия изображения по алгоритму JPEG
# in       - массив исходных данных
# width    - ширина изображения (пикселей)
# height   - высота изображения (пикселей)
# bit      - количество бит на пиксель (выполняется сжатие изображения
#            с количеством бит на пиксель, равным 24)
# compressionValue - степень сжатия картинки (1-100, 1-максимальное сжатие,
# 100-сжатие без потери качества), рекомендуется значение 60.
#  out     - массив выходных данных
#  sizeout - размер массива выходных данных
# При ошибке возвращает 0

    mapCompressJPEG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCompressJPEG', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapCompressJPEG(_in: ctypes.c_char_p, _width: int, _height: int, _bit: int, _compressionValue: int, _out: ctypes.c_char_p, _sizeout: int) -> int:
        return mapCompressJPEG_t (_in, _width, _height, _bit, _compressionValue, _out, _sizeout)


# Декомпрессия изображения по алгоритму JPEG
# in       - массив исходных (сжатых) данных
# sizein   - размер массива исходных (сжатых) данных
# width    - ширина изображения (пикселей)
# height   - высота изображения (пикселей)
# bit      - количество бит на пиксель (выполняется сжатие изображения
#            с количеством бит на пиксель, равным 24)
#  out     - массив выходных данных
#  sizeout - размер массива выходных данных
# При ошибке возвращает 0

    mapDecompressJPEG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDecompressJPEG', ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapDecompressJPEG(_in: ctypes.c_char_p, _sizein: int, _width: int, _height: int, _bit: int, _out: ctypes.c_char_p, _sizeout: int) -> int:
        return mapDecompressJPEG_t (_in, _sizein, _width, _height, _bit, _out, _sizeout)


# Запросить является ли имя идентификатором данных на Сервере
# Если да, то возвращает ненулевое значение (1 - устаревший
# формат без имени сервера, 2 - содержит имя сервера)
# Если имя не указывает на данные с сервера, то возвращает ноль

    mapIsAliasNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsAliasNameUn', maptype.PWCHAR)
    def mapIsAliasNameUn(_name: mapsyst.WTEXT) -> int:
        return mapIsAliasNameUn_t (_name.buffer())


# Сформировать алиас данных на Сервере
# в формате "HOST#ХОСТ#ПОРТ#ALIAS#условное_имя_карты"
# host  - имя хоста
# port  - номер порта
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - имя ресурса (условное имя карты)
# name  - имя строки для размещения результата
# size  - максимальный размер строки в байтах
# При ошибке в параметрах возвращает ноль

    mapBuildAliasNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildAliasNameEx', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapBuildAliasNameEx(_number: int, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildAliasNameEx_t (_number, _alias.buffer(), _name.buffer(), _size)

    mapBuildAliasNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapBuildAliasNameUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapBuildAliasNameUn(_host: mapsyst.WTEXT, _port: int, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildAliasNameUn_t (_host.buffer(), _port, _alias.buffer(), _name.buffer(), _size)


# Запросить число подключений к ГИС Серверам
# При отсутствии подключений возвращает ноль

    mapActiveServerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapActiveServerCount')
    def mapActiveServerCount() -> int:
        return mapActiveServerCount_t ()


# Запросить состояние подключения к серверу
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При потоковом открытии\добавлении данных с ГИС Сервера рекомендуется
# после первой ошибки открытия данных проверить состояние подключения
# и при ошибке прервать потоковую обработку
# Если после ошибки открытия данных с именем "HOST#..." или "ALIAS#..."
# подключение не установлено, то нужно убедится, что Сервер запущен и
# введены правильные параметры соединения
# Если подключение к серверу установлено - возвращает ненулевое значение

    mapIsServerActiveEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsServerActiveEx', ctypes.c_int)
    def mapIsServerActiveEx(_number: int) -> int:
        return mapIsServerActiveEx_t (_number)


# Запросить доступ к средствам мониторинга состояния сервера
# Если мониторинг запрещен - возвращает нулевое значение

    mapIsServerMonitoringEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsServerMonitoringEnable', ctypes.c_int)
    def mapIsServerMonitoringEnable(_number: int) -> int:
        return mapIsServerMonitoringEnable_t (_number)


# Запросить доступ к средствам администрирования состояния сервера
# Если администрирование запрещено - возвращает нулевое значение

    mapIsServerAdministrationEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsServerAdministrationEnable', ctypes.c_int)
    def mapIsServerAdministrationEnable(_number: int) -> int:
        return mapIsServerAdministrationEnable_t (_number)


# Запросить версию ГИС Сервера по номеру подключения
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Возвращает шестнадцатеричный номер версии ГИС Сервер,
# например: 0x00040503 соответствует версии 4.5.3
# При ошибке возвращает ноль

    mapGetServerVersion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetServerVersion', ctypes.c_int)
    def mapGetServerVersion(_number: int) -> int:
        return mapGetServerVersion_t (_number)


# Освободить ресурсы после обработки данных мониторинга состояния сервера

    mapFreeServerState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeServerState', ctypes.POINTER(maptype.GSMONITOR))
    def mapFreeServerState(_buffer: ctypes.POINTER(maptype.GSMONITOR)) -> ctypes.c_void_p:
        return mapFreeServerState_t (_buffer)


# Освободить ресурсы после обработки данных журнала

    mapFreeServerLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeServerLog', ctypes.c_char_p)
    def mapFreeServerLog(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeServerLog_t (_buffer)


# Запросить выполнено ли подключение и регистрация пользователя
# для заданного имени алиаса данных и номера порта
# name - алиас в формате "HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты",
#        или "HOST#ХОСТ" или "HOST#ХОСТ:ПОРТ"
# port - номер порта для проверки или 0 (любой)
# (на одном сервере могут быть несколько экземпляров ГИС Сервера с разными портами)
# При успешной проверке возвращает номер подключения
# При ошибке возвращает ноль

    mapCheckConnectForAliasUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckConnectForAliasUn', maptype.PWCHAR)
    def mapCheckConnectForAliasUn(_name: mapsyst.WTEXT) -> int:
        return mapCheckConnectForAliasUn_t (_name.buffer())

    mapCheckConnectForAliasEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckConnectForAliasEx', ctypes.c_char_p, ctypes.c_int)
    def mapCheckConnectForAliasEx(_name: ctypes.c_char_p, _port: int) -> int:
        return mapCheckConnectForAliasEx_t (_name, _port)


# Открыть новое подключение к ГИС-серверу
# name - имя хоста (до 256 символов),
#        или строка адреса "XXX.XXX.XXX.XXX"
# Если параметр равен нулю - сервер ищется на локальном хосте "localhost".
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# В случае удачно выполненного подключения возвращает его порядковый номер
# При ошибке возвращает ноль

    mapOpenConnectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenConnectUn', maptype.PWCHAR, ctypes.c_int)
    def mapOpenConnectUn(_name: mapsyst.WTEXT, _port: int) -> int:
        return mapOpenConnectUn_t (_name.buffer(), _port)


# Открыть новое подключение к ГИС-серверу
# name - имя хоста (до 256 символов),
#        или строка адреса "XXX.XXX.XXX.XXX"
# Если параметр равен нулю - сервер ищется на локальном хосте "localhost".
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# cansleep - разрешение на открытие виртуального (спящего) соединения,
#        при отсутствии физического доступа к серверу
# Данные будут открываться из кэш, если он есть
# При появлении физического соединения оно автоматически (по мере вызова mapAdjustData)
# будет восстановлено вместо вирутального (кэш обновится по данным с сервера)
# В случае удачно выполненного подключения возвращает его порядковый номер
# При ошибке возвращает ноль

    mapOpenConnectExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenConnectExUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapOpenConnectExUn(_name: mapsyst.WTEXT, _port: int, _cansleep: int) -> int:
        return mapOpenConnectExUn_t (_name.buffer(), _port, _cansleep)


# Запросить - можно ли закрыть подключение
# При ошибке (подключение не найдено) возвращает ноль
# При занятости подключения возвращает "-1"
# Если соединение может быть закрыто, то возвращает положительное значение

    mapCanCloseConnect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCanCloseConnect', ctypes.c_int)
    def mapCanCloseConnect(_number: int) -> int:
        return mapCanCloseConnect_t (_number)


# Закрыть подключение к ГИС-серверу
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При ошибке (подключение не найдено) возвращает ноль
# При занятости подключения возвращает "-1"
# При успешном выполнении возвращает положительное значение
# Если счетчик ссылок на соединения равен 0 и все соединения закрыты возвращает 2

    mapCloseConnect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseConnect', ctypes.c_int)
    def mapCloseConnect(_number: int) -> int:
        return mapCloseConnect_t (_number)


# Изменить параметры подключения с ГИС-сервером
# Вызывается до открытия карт на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# name - имя хоста (до 256 символов),
#        или строка адреса "XXX.XXX.XXX.XXX"
# Если параметр равен нулю - сервер ищется на локальном хосте "localhost".
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# При ошибке возвращает ноль

    mapSetConnectParametersExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetConnectParametersExUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSetConnectParametersExUn(_number: int, _name: mapsyst.WTEXT, _port: int) -> int:
        return mapSetConnectParametersExUn_t (_number, _name.buffer(), _port)


# Запросить номер порта для связи с ГИС-сервером
# Номер порта от 1024 до 65536, по умолчанию - 2047
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()

    mapGetConnectPortEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetConnectPortEx', ctypes.c_int)
    def mapGetConnectPortEx(_number: int) -> int:
        return mapGetConnectPortEx_t (_number)


# Запросить имя\адрес хоста
# Если было установлен адрес хоста - возвращаемое значение 1,
# если имя хоста - возвращаемое значение 2.
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если установлено оба значения - возвращается адрес хоста
# name - адрес строки для размещения результата
# size - размер строки (для имени хоста не менее 256)
# При ошибке возвращает ноль

    mapGetConnectHostExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetConnectHostExUn', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetConnectHostExUn(_number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetConnectHostExUn_t (_number, _name.buffer(), _size)


# Зарегистрировать пользователя
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если соединение с сервером не было установлено -
# пытается соединиться с установленными ранее параметрами
# Пароль должен передаваться в зашифрованном виде по алгоритму MD5 (в виде хэша)
# Для получения хэша пароля следует использовать функцию svStringToHash
# (описана в gisdlgs.h)
# При ошибке возвращает ноль

    mapRegisterUserEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterUserEx', ctypes.c_int, ctypes.POINTER(maptype.TMCUSERPARM))
    def mapRegisterUserEx(_number: int, _parm: ctypes.POINTER(maptype.TMCUSERPARM)) -> int:
        return mapRegisterUserEx_t (_number, _parm)


# Зарегистрировать текущего пользователя ОС как пользователя ГИС Сервера в домене
# number - номер активного подключения (соединения) к ГИС Серверу от 1 до mapActiveServerCount()
# Если соединение с сервером не было установлено -
# пытается соединиться с установленными ранее параметрами
# При ошибке возвращает ноль

    mapRegisterSystemUserEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRegisterSystemUserEx', ctypes.c_int)
    def mapRegisterSystemUserEx(_number: int) -> int:
        return mapRegisterSystemUserEx_t (_number)


# Удалить в памяти параметры регистрации пользователя
# number - номер активного подключения (соединения) к ГИС Серверу от 1 до mapActiveServerCount()
# После закрытия последнего документа на Сервере соединение
# разрывается и для последующего открытия карты нужно повторно
# выполнить mapRegisterUser()

    mapUnRegisterUserEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnRegisterUserEx', ctypes.c_int)
    def mapUnRegisterUserEx(_number: int) -> ctypes.c_void_p:
        return mapUnRegisterUserEx_t (_number)


# Запросить тип регистрации пользователя
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если регистрация пользователя выполнялась через функцию mapRegisterSystemUserEx,
# то возвращается положительное значение

    mapGetRegisterUserType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRegisterUserType', ctypes.c_int)
    def mapGetRegisterUserType(_number: int) -> int:
        return mapGetRegisterUserType_t (_number)


# Запросить список доступных пользователю карт на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка карт,
#          структура TMCMAPLIST описана в maptype.h
# Если buffer равно нулю, возвращает размер необходимой области памяти
# length - длина выделенной области памяти
# Возвращает общий размер считанной записи или 0

    mapGetMapListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapListforUserUn', ctypes.c_int, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMapListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _length: int) -> int:
        return mapGetMapListforUserUn_t (_number, _buffer, _length)


# Запросить список доступных пользователю атласов на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка атласов,
#          структура TMCMAPLIST описана в maptype.h
# length - длина выделенной области памяти
# Возвращает общий размер считанной записи или 0

    mapGetAlsListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAlsListforUserUn', ctypes.c_int, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetAlsListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _length: int) -> int:
        return mapGetAlsListforUserUn_t (_number, _buffer, _length)


# Запросить список доступных пользователю матриц на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка матриц,
#          структура TMCMAPLIST описана в maptype.h
# Если buffer равно нулю, возвращает размер необходимой области памяти
# length - длина выделенной области памяти
# Возвращает общий размер считанной записи или 0

    mapGetMtwListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMtwListforUserUn', ctypes.c_int, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMtwListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _length: int) -> int:
        return mapGetMtwListforUserUn_t (_number, _buffer, _length)


# Запросить список доступных пользователю растров на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка растров,
#          структура TMCMAPLIST описана в maptype.h
# Если buffer равно нулю, возвращает размер необходимой области памяти
# length - длина выделенной области памяти
# Возвращает общий размер считанной записи или 0

    mapGetRswListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRswListforUserUn', ctypes.c_int, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetRswListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _length: int) -> int:
        return mapGetRswListforUserUn_t (_number, _buffer, _length)


# Установить текущий тип передаваемых данных
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# карты - 1, растры - 2, матрицы - 3, атласы  - 4
# При ошибке возвращает ноль

    mapSetActiveDataType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveDataType', ctypes.c_int, ctypes.c_int)
    def mapSetActiveDataType(_number: int, _type: int) -> int:
        return mapSetActiveDataType_t (_number, _type)


# Запросить текущий тип передаваемых данных
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# карты - 1, растры - 2, матрицы - 3, атласы  - 4
# При ошибке возвращает ноль

    mapGetActiveDataType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetActiveDataType', ctypes.c_int)
    def mapGetActiveDataType(_number: int) -> int:
        return mapGetActiveDataType_t (_number)


# Установить путь к папке для хранения кэшируемых данных с ГИС Сервера
# Если приложение не установило путь к папке для кэширования данных,
# то она автоматически будет размещена внутри системной папки Temp
# в папке Panorama.Cache.
# При ошибке возвращает ноль

    mapSetCachePathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCachePathUn', maptype.PWCHAR)
    def mapSetCachePathUn(_path: mapsyst.WTEXT) -> int:
        return mapSetCachePathUn_t (_path.buffer())


# Установить имя папки для хранения кэша векторных карт с ГИС Сервера
# Необходимо для организации устойчивой параллельной работы нескольких приложений
# на одном компьюере с картами на ГИС Сервере при редактировании карт
# Имя папки задается без косых и специальных символов, недопустимых в файловой системе
# При ошибке возвращает ноль

    mapSetMapCacheSubfolder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetMapCacheSubfolder', maptype.PWCHAR)
    def mapSetMapCacheSubfolder(_subfolder: mapsyst.WTEXT) -> int:
        return mapSetMapCacheSubfolder_t (_subfolder.buffer())


# Очистить папку с кэшем данных, открытых с ГИС Сервера или с геопорталов
# Имя папки определяется функцией mapGetCachePathUn
# Данные, открытые в момент вызова функции, могут не удалиться

    mapClearDataCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearDataCache')
    def mapClearDataCache() -> ctypes.c_void_p:
        return mapClearDataCache_t ()


# Очистить кэш данных для всех карт текущего документа,
# открытых с ГИС Сервера
# hMap  -  идентификатор открытых данных
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearDocCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearDocCache', maptype.HMAP)
    def mapClearDocCache(_hMap: maptype.HMAP) -> ctypes.c_void_p:
        return mapClearDocCache_t (_hMap)


# Очистить кэш данных для открытой пользовательской карты,
# открытой с ГИС Сервера
# hMap  -  идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearSiteCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearSiteCache', maptype.HMAP, maptype.HSITE)
    def mapClearSiteCache(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> ctypes.c_void_p:
        return mapClearSiteCache_t (_hMap, _hSite)


# Очистить кэш данных для всех карт текущего документа,
# открытых с ГИС Сервера и кэш базы данных на ГИС Сервере
# hMap  -  идентификатор открытых данных
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearServerCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearServerCache', maptype.HMAP)
    def mapClearServerCache(_hMap: maptype.HMAP) -> ctypes.c_void_p:
        return mapClearServerCache_t (_hMap)


# Запросить открыта ли карта на сервере или локально
# hmap -  идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Если карта открыта на сервере возвращает ненулевое значение

    mapIsMapFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsMapFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsMapFromServer(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsMapFromServer_t (_hMap, _hSite)


# Запросить список папок на сервере, доступных для записи файлов
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к виртуальной папке, в которой запрашивается список файлов и папок или 0
# Например, "Data\\Maps"
# Если folder равно 0, то запрашивается список алиасов всех доступных папок
# allfiles - признак запроса всех файлов в папке folder, если не установлен,
# то буден выдан список внутренних папок и файлов MAP,SIT,SITX,RSC,MTW,MTQ,RSW
# parm   - адрес буфера для размещения списка запрошенных данных или 0
# Если parm равно 0, то запрашивается размер буфера, требуемый для размещения списка
# length - размер буфера для размещения списка
# Список данных заполняется только для файлов и папок, непосредственно расположенных
# в заданной папке без вложений
# При успешном выполнении возвращает размер сформированного списка
# Если размер списка превышает размер буфера, то данные считаны не полностью.
# Тогда нужно выделить больший буфер и запросить данные повторно
# При ошибке возвращает ноль

    mapGetFolderList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetFolderList', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetFolderList(_number: int, _folder: mapsyst.WTEXT, _allfiles: int, _parm: ctypes.POINTER(maptype.TMCDATALIST), _size: int) -> int:
        return mapGetFolderList_t (_number, _folder.buffer(), _allfiles, _parm, _size)


# Запросить виртуальную папку по алиасу карты
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - алиас карты
# folder - адрес строки для записи алиаса виртуальной папки
# size   - длина строки в байтах
# При ошибке возвращает ноль

    mapGetMapFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapFolderOnServer', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapFolderOnServer(_number: int, _alias: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapFolderOnServer_t (_number, _alias.buffer(), _folder.buffer(), _size)


# Создать папку на сервере относительно алиаса доступной папки
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к создаваемой папке
# Например, "Data\\Maps" или "Data/Maps",
# где "Data" - виртуальная папка в настройках ГИС Сервера, "Maps" - создаваемая папка
# При ошибке возвращает ноль

    mapCreateFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateFolderOnServer', ctypes.c_int, maptype.PWCHAR)
    def mapCreateFolderOnServer(_number: int, _folder: mapsyst.WTEXT) -> int:
        return mapCreateFolderOnServer_t (_number, _folder.buffer())


# Удалить папку на сервере относительно алиаса доступной папки
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к удаляемой папке
# Например, для удаления папки "Maps": "Data\\Maps" или "Data/Maps",
# где "Data" - виртуальная папка в настройках ГИС Сервера, "Maps" - удаляемая папка
# deletefiles - удалить все файлы в папке (если задано ненулевое значение)
# deletefolders - удалить все подпапки с файлами в них (если задано ненулевое значение)
# При ошибке возвращает ноль

    mapDeleteFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteFolderOnServer', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapDeleteFolderOnServer(_number: int, _folder: mapsyst.WTEXT, _deletefiles: int, _deletefolders: int) -> int:
        return mapDeleteFolderOnServer_t (_number, _folder.buffer(), _deletefiles, _deletefolders)


# Удалить файл на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# file - путь к удаляемому файлу
# Например, "Data\\Maps\\image.rsw",
# где "Data" - виртуальная папка в настройках ГИС Сервера, "image.rsw" - удаляемый файл
# При ошибке возвращает ноль

    mapDeleteFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteFileOnServer', ctypes.c_int, maptype.PWCHAR)
    def mapDeleteFileOnServer(_number: int, _file: mapsyst.WTEXT) -> int:
        return mapDeleteFileOnServer_t (_number, _file.buffer())


# Скопировать файл на сервере
# source - путь к изменяемому файлу
# Например, "Data\\Maps\\image.sitx",
# где "Data" - виртуальная папка на ГИС Сервере, "image.sitx" - перемещаемый файл
# target - новый путь к файлу
# Например, "Storage\\Roads\\road_M4.sitx",
# При ошибке возвращает ноль

    mapCopyFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyFileOnServer', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR)
    def mapCopyFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        return mapCopyFileOnServer_t (_number, _source.buffer(), _target.buffer())


# Переименовать (переместить) файл или папку на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# source - путь к изменяемому файлу или папке
# Например, "Data\\Maps\\image.sitx",
# где "Data" - виртуальная папка на ГИС Сервере, "image.sitx" - перемещаемый файл
# target - новый путь к файлу или папке
# Например, "Storage\\Roads\\road_M4.sitx",
# При ошибке возвращает ноль

    mapRenameFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRenameFileOnServer', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR)
    def mapRenameFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        return mapRenameFileOnServer_t (_number, _source.buffer(), _target.buffer())


# Сохранить файл на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь для сохранения файла, путь может начинаться с имени алиаса папки,
#          доступной для записи данных
# Например: "Data\\Maps" или "Data/Maps/Images", где "Data" - виртуальная папка на ГИС Сервере, /Maps/Images - поддиректории
#          или содержать полный алиас виртуальной папки на сервере с поддиректориями
# Например: "HOST#123.345.0.12#ALIAS#Data/Maps/Images"
#          или содержать полный алиас карты, записанной в виртуальной папке на сервере (!), с поддиректориями относительно карты
# Например: "HOST#123.345.0.12#ALIAS#Mymap/Images"
# file   - путь к файлу, который будет записан в папку на сервере (файл должен
#          содержать данные, а не выполняемый код).
# Имя файла, расширение и атрибуты чтения/записи сохраняются.
# Отсутствующие директории создаются автоматически
# Символ косой может быть любого вида - "/" или "\\"
# Для доступа к файлу в дальнейшем нужно объединить путь к папке и имя файла,
# например: "HOST#123.345.0.12#ALIAS#Data/Maps/example.sitx"
# При ошибке возвращает ноль

    mapSaveFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveFileOnServer', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR)
    def mapSaveFileOnServer(_number: int, _folder: mapsyst.WTEXT, _file: mapsyst.WTEXT) -> int:
        return mapSaveFileOnServer_t (_number, _folder.buffer(), _file.buffer())


# Сохранить карту на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь для сохранения файла, путь должен начинаться с алиаса папки,
#          доступной для записи данных
# Например, "Data\\Maps" или "Data/Maps",
# где "Data" - виртуальная папка на ГИС Сервере
# hMap -  идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# rscsave - признак необходимости сохранения файла RSC на сервер
# При ошибке возвращает ноль

    mapSaveMapOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveMapOnServer', ctypes.c_int, maptype.PWCHAR, maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSaveMapOnServer(_number: int, _folder: mapsyst.WTEXT, _hMap: maptype.HMAP, _hSite: maptype.HSITE, _rscsave: int) -> int:
        return mapSaveMapOnServer_t (_number, _folder.buffer(), _hMap, _hSite, _rscsave)


# Прочитать файл на сервере (если есть доступ к виртуальной папке)
# alias   - алиас файла на сервере, начиная с имени виртуальной папки (кроме выполняемых файлов,
#           файлов карт, матриц и растров)
# path    - путь, по которому будет сохранен файл (после записи путь дополняется именем файла)
# size    - размер поля, содержащего путь
# error   - поле для записи кода ощибки, если функция вернет ноль
# При ошибке возвращает ноль

    mapReadFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadFileOnServer', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapReadFileOnServer(_number: int, _alias: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapReadFileOnServer_t (_number, _alias.buffer(), _path.buffer(), _size, _error)


# Запросить список пользователей, ролей и данных, размещенных на ГИС Сервере в виде xml
# path    - путь, по которому будет сохранен файл
# error   - поле для записи кода ощибки, если функция вернет ноль
# При ошибке возвращает ноль

    mapGetServerUsersListInXml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetServerUsersListInXml', ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapGetServerUsersListInXml(_number: int, _xmlname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetServerUsersListInXml_t (_number, _xmlname.buffer(), _error)


# Сохранить данные в Банк данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# handle  - иденетификатор окна, которому посылаются сообщения о ходе загрузки данных в Банк данных
#           (WM_PROGRESSBAR, WPARAM = -1 - старт, LPARAM - текст сообщения в кодировке приложения,
#                            0-100 - % выполнения, -2 - завершение процесса)
#           цикл сообщений посылается при передаче каждого набора данных (файла) на сервер и
#           при загрузке наборов в Банк данных на сервере
# dslist  - путь к файлу - списку загружаемых наборов данных (111, 222, 333 - имена файлов)
#           <?xml version="1.0" encoding="UTF-8"?> <dsl> 111, 222, 333 </dsl>
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# При ошибке возвращает ноль

    mapSaveToGeoDB_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveToGeoDB', ctypes.c_int, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapSaveToGeoDB(_number: int, _handle: maptype.HMESSAGE, _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
        return mapSaveToGeoDB_t (_number, _handle, _dslist.buffer(), _logname.buffer(), _size)


# Отправить команду на загрузку наборов данных, которые уже переданы на ГИС Сервер,
# в Банк данных ЦК и ДЗЗ
# Наборы данных могут быть загружены удаленно другим приложением на ГИС Сервер
# в специальную папку для Банка Данных
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# handle  - идентификатор окна, которому посылаются сообщения о ходе загрузки данных в Банк данных
# dslist  - имя файла - списка загружаемых наборов данных
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# error   - код ошибки выполнения запроса
# При ошибке возвращает ноль

#    mapCallGeoDBLoaderPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallGeoDBLoaderPro', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallGeoDBLoaderPro(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallGeoDBLoaderPro_t (_number, _callevent, _parm, _dslist, _logname, _size, _error)

#    mapCallGeoDBLoaderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallGeoDBLoaderEx', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
#    def mapCallGeoDBLoaderEx(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
#        return mapCallGeoDBLoaderEx_t (_number, _callevent, _parm, _dslist, _logname, _size)

    mapCallGeoDBLoader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallGeoDBLoader', ctypes.c_int, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCallGeoDBLoader(_number: int, _handle: maptype.HMESSAGE, _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
        return mapCallGeoDBLoader_t (_number, _handle, _dslist.buffer(), _logname.buffer(), _size)


# Отправить команду к Банку данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# dslist  - имя файла xml - списка обрабатываемых наборов данных (пути, идентификаторы записей базы и т.д.)
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# error   - поле для записи кода ощибки, если функция вернет ноль
# command - имя команды: "adjust" - выполнить сводку наборов данных, "control" - выполнить контроль качества векторных наборов данных,
#           "opencontrol" - выполнить контроль отсутствия закрытых сведений на карте, "export" - выполнить экспорт геопокрытий,
#           "expertise" - выполнить входной контроль наборов данных по шаблону требований, "upscheme" - обновить схему наличия наборов
# При ошибке возвращает ноль

#    mapCallDbCommand_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallDbCommand', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.PWCHAR)
#    def mapCallDbCommand(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int), _command: mapsyst.WTEXT) -> int:
#        return mapCallDbCommand_t (_number, _callevent, _parm, _dslist, _logname, _size, _error, _command)


# Отправить команду на формирование геопокрытия из наборов данных Банка данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# geolist - имя файла - списка наборов данных для формирования геопокрытий
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# При ошибке возвращает ноль

#    mapCallGeoLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallGeoLevel', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
#    def mapCallGeoLevel(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _geolist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
#        return mapCallGeoLevel_t (_number, _callevent, _parm, _geolist, _logname, _size)

#    mapCallGeoLevelEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallGeoLevelEx', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallGeoLevelEx(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _geolist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallGeoLevelEx_t (_number, _callevent, _parm, _geolist, _logname, _size, _error)


# Отправить команду на экспорт геопокрытия в Банке данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# exportlist - имя файла - списка экспортируемых геопокрытий (формат для экспорта задается в списке)
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# При ошибке возвращает ноль

#    mapCallExport_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallExport', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallExport(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _exportlist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallExport_t (_number, _callevent, _parm, _exportlist, _logname, _size, _error)


# Отправить команду на контроль наборов данных, которые уже переданы на ГИС Сервер в виртуальную папку или
# загружены в Банк данных
# mclist  - имя файла со списком наборов данных для контроля
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# При ошибке возвращает ноль

#    mapCallMapControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallMapControl', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallMapControl(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _mclist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallMapControl_t (_number, _callevent, _parm, _mclist, _logname, _size, _error)


# Выполнить контроль отсутствия закрытых сведения на картах открытого пользования
# mclist  - имя файла со списком наборов данных для контроля
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# При ошибке возвращает ноль

#    mapCallOpenMapControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallOpenMapControl', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallOpenMapControl(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _mclist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallOpenMapControl_t (_number, _callevent, _parm, _mclist, _logname, _size, _error)


# Отправить команду на обновление схемы наличия наборов данных для заданной таблицы метаданных Банка данных
# number  - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# table   - имя таблицы метаданных, для которой обновляется схема ("t_md_map", "t_md_image", "t_md_matrix")
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# flag    - флаг для выполнения дополнительного контроля наборов данных
#           (1 - признак контроля соответствия основного набора и резервных копий с
#            автоматическим восстановлением при наличии 2-ух совпадающих резервных копий)
# При ошибке возвращает ноль

#    mapCallUpSchemeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallUpSchemeEx', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
#    def mapCallUpSchemeEx(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _table: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int), _flag: int) -> int:
#        return mapCallUpSchemeEx_t (_number, _callevent, _parm, _table, _logname, _size, _error, _flag)

#    mapCallUpScheme_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCallUpScheme', ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
#    def mapCallUpScheme(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _table: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapCallUpScheme_t (_number, _callevent, _parm, _table, _logname, _size, _error)


# Запросить доступность функции сохранения наборов данных в Банк данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При ошибке возвращает ноль

    mapIsGeoDBEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsGeoDBEnable', ctypes.c_int)
    def mapIsGeoDBEnable(_number: int) -> int:
        return mapIsGeoDBEnable_t (_number)


# Запросить список обрабатываемых в Банке данных форматов
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес буфера для размещения результата запроса
# size   - размер буфера
# Список форматов состоит из трех текстовых строк, заканчивающихся символом '\n'
# В первой строке записывается список форматов векторых карт, во второй - растров (снимков),
# в третьей - матриц (моделей). Форматы данных разделяются запятыми.
# Кроме форматов основных файлов указываются форматы вспомогательных файлов
# (метаданных, уменьшенных изображений данных и других).
# Например:
# SXF,RSC,DIR,MIF,MID,KML,SITX,XML,SHP,DBF,PRJ,SHX,preview.png,
# RSW,TAB,INI,JPG,preview.png,TIF,IMG,TIFF,
# MTW,TIFF,TIF,preview.png,HGT,
# При ошибке возвращает ноль, иначе - размер считанных данных

    mapGetGeoDBFormats_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetGeoDBFormats', ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetGeoDBFormats(_number: int, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetGeoDBFormats_t (_number, _buffer, _size)

# Запросить список обрабатываемых в Банке данных групп
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес буфера для размещения результата запроса
# size   - размер буфера
# Список групп состоит из текстовых строк, заканчивающихся символом '\n'
# В начале строки указан идентификатор группы, а через запятую указано название группы в кодировке UTF-8
# Например: "7,Обзорно-географические карты\n"
# При ошибке возвращает ноль

    mapGetGeoDBGroups_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetGeoDBGroups', ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetGeoDBGroups(_number: int, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetGeoDBGroups_t (_number, _buffer, _size)


# Запросить разрешение на копирование файлов карты на клиент
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - алиас данных на сервере
# error - код ошибки доступа (см. maperr.rh)
# При ошибке возвращает ноль, иначе - тип данных (1 - карта, 2 - растр, 3 - матрица)

    mapIsCopyDataEnabled_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsCopyDataEnabled', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapIsCopyDataEnabled(_number: int, _alias: mapsyst.WTEXT, _type: int, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapIsCopyDataEnabled_t (_number, _alias.buffer(), _type, _error)


# Скопировать набор данных с ГИС Сервера на клиент
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias  - алиас данных на сервере
# type   - тип данных (1 - карта, 2 - растр, 3 - матрица или 0 - требуется определить)
# target - имя файла выходного набора данных (если задана только папка, то имя формируется
#          с учетом алиаса и типа данных
# error  - код ошибки доступа (см. maperr.rh)
# При ошибке возвращает ноль, иначе - тип данных (1 - карта, 2 - растр, 3 - матрица)

    mapCopyDataFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopyDataFromServer', ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapCopyDataFromServer(_number: int, _alias: mapsyst.WTEXT, _type: int, _target: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCopyDataFromServer_t (_number, _alias.buffer(), _type, _target.buffer(), _error)

    mapFreeRscList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeRscList', ctypes.c_char_p)
    def mapFreeRscList(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeRscList_t (_buffer)

# Открыть сервисные данные с ГИС Сервера
# alias    - имя ресурса (условное имя карты)
# connect - порядковый номер подключения,
# если connect > 0 вызвать mapCloseConnect(connect)
# error   - код ошибки
# Если идентификатор открытой векторной карты не нужен,
# необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

#    mapOpenServiceData_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenServiceData', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#    def mapOpenServiceData(_alias: mapsyst.WTEXT, _connect: ctypes.POINTER(ctypes.c_int), _error: ctypes.POINTER(ctypes.c_int)) -> maptype.HMAP:
#        return mapOpenServiceData_t (_alias, _connect, _error)

# Добавить сервисные данные с ГИС Сервера к открытой карте (карту, растр, матрицу)
# hmap     - идентификатор открытых данных
# alias    - имя ресурса (условное имя карты)
# connect - порядковый номер подключения,
# если connect > 0 вызвать mapCloseConnect(connect)
# error   - код ошибки
# Возвращает идентификатор типа данных (FILE_MAP - для векторной
# карты, FILE_RSW - для растра, FILE_MTW - для матрицы, FILE_MTL - для
# матрицы слоев, FILE_MTQ - для матрицы качеств), данные добавляются в
# список последними, если данные уже были открыты, число открытых данных (карт, растров, матриц) не меняется
# При ошибке возвращает ноль

#    mapAppendServiceData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendServiceData', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#    def mapAppendServiceData(_hmap: maptype.HMAP, _alias: mapsyst.WTEXT, _connect: ctypes.POINTER(ctypes.c_int), _error: ctypes.POINTER(ctypes.c_int)) -> int:
#        return mapAppendServiceData_t (_hmap, _alias, _connect, _error)


# Преобразовать входную строку (не более 1024 байта), заканчивающуюся 0, в строку в формате md5
# instring - входная строка
# outstring - выходная строка в формате md5
# length - размер выходной строки
# При ошибке возвращает ноль

    mapStringToMd5Hash_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapStringToMd5Hash',ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int)
    def mapStringToMd5Hash(_instring: ctypes.c_char_p, _outstring: ctypes.c_char_p, _length: int) -> int:
        return mapStringToMd5Hash_t(_instring, _outstring, _length)


# Открыть запись в диагностический протокол
# logname - путь к протоколу диагностической печати, если равен нулю,
# то запись идет в \ProgramData\mapdiagnostics.log

    mapOpenDiagnostics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapOpenDiagnostics', maptype.PWCHAR)
    def mapOpenDiagnostics(_logname: mapsyst.WTEXT) -> int:
        return mapOpenDiagnostics_t (_logname.buffer())


# Запросить - открыт ли диагностический протокол

    mapIsDiagnostics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsDiagnostics')
    def mapIsDiagnostics() -> int:
        return mapIsDiagnostics_t ()


# Закрыть запись в диагностический протокол

    mapCloseDiagnostics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseDiagnostics')
    def mapCloseDiagnostics() -> ctypes.c_void_p:
        return mapCloseDiagnostics_t ()


# Записать сообщение в диагностический протокол
# message - первая часть сообщения
# messageex - вторая часть сообщения
# type - тип сообщения (>>> MT_ERROR, --> MT_WARNING, MT_INFO, MT_CONTINUE - продолжение)
# error - код ошибки, запрошенный у системы (если равен 0, то будет запрошен при выводе сообщения)
# value - число, которое будет преобразовано в строку и добавлено к сообщению

    mapWriteToDiagnosticsLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToDiagnosticsLog', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapWriteToDiagnosticsLog(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapWriteToDiagnosticsLog_t (_message.buffer(), _messageex.buffer(), _type)

    mapWriteErrorToDiagnosticsLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteErrorToDiagnosticsLog', ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapWriteErrorToDiagnosticsLog(_code: int, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapWriteErrorToDiagnosticsLog_t (_code, _message.buffer(), _type)

    mapWriteToLogLastError_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToLogLastError', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapWriteToLogLastError(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int, _error: int) -> ctypes.c_void_p:
        return mapWriteToLogLastError_t (_message.buffer(), _messageex.buffer(), _type, _error)

    mapWriteToLogInt_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToLogInt', maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapWriteToLogInt(_message: mapsyst.WTEXT, _value: int, _type: int) -> ctypes.c_void_p:
        return mapWriteToLogInt_t (_message.buffer(), _value, _type)


# Получить идентификатор для системы кодирования
# key  - строка, содержащая двоичный ключ для кодирования данных
#        Ключ должен иметь случайное равномерное заполнение,
#        например, методом преобразования пароля пользователя и текущего
#        времени по алгоритму MD5
# size - длина строки (должна быть равна 32 байта)
# После завершения кодирования/раскодирования нужно освободить ресурсы
# функцией mapDeleteCoder
# При ошибке возвращает ноль

    mapCreateCoder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateCoder', ctypes.c_char_p, ctypes.c_int)
    def mapCreateCoder(_key: ctypes.c_char_p, _size: int) -> ctypes.c_void_p:
        return mapCreateCoder_t (_key, _size)


# Закодировать область данных заданным ключом (длина области кратна 16)
# hcoder - идентификатор для системы кодирования
# memory - адрес области памяти, которую нужно закодировать
# size   - размер области памяти для кодирования, кратный 16 байтам
# Для кодирования применяются операции XOR и циклического сдвига данных
# Состояние ключа меняется при кодировании под управлением кодируемых данных
# При ошибке возвращает ноль

    mapCoderOn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCoderOn', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int)
    def mapCoderOn(_coder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        return mapCoderOn_t (_coder, _memory, _size)


# Раскодировать область данных заданным ключом (длина области кратна 16)
# hcoder - идентификатор для системы кодирования
# memory - адрес области памяти, которую нужно закодировать
# size   - размер области памяти для кодирования, кратный 16 байтам
# Для кодирования применяются операции XOR и циклического сдвига данных
# Состояние ключа меняется при кодировании под управлением кодируемых данных
# При ошибке возвращает ноль

    mapCoderOff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCoderOff', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int)
    def mapCoderOff(_coder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        return mapCoderOff_t (_coder, _memory, _size)


# Освободить ресурсы после завершения кодирования/раскодирования

    mapDeleteCoder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteCoder', ctypes.c_void_p)
    def mapDeleteCoder(_coder: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapDeleteCoder_t (_coder)


# Открыть/Создать файл набора линеек знаков (макетов) EDTX в папке \log карты
# hmap -  идентификатор открытых данных
# hsite - идентификатор карты
# number - номер линейки, которая должна стать текущей
# Возвращает идентификатор набора в памяти
# При ошибке возвращает ноль

    mapOpenLayouts_t = mapsyst.GetProcAddress(acceslib,maptype.HEDTLINE,'mapOpenLayouts', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapOpenLayouts(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> maptype.HEDTLINE:
        return mapOpenLayouts_t (_hmap, _hsite, _number)


# Закрыть файл набора линеек знаков (макетов)
# hgroup - идентификатор набора линеек знаков (макетов) в памяти

    mapCloseLayouts_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseLayouts', maptype.HEDTLINE)
    def mapCloseLayouts(_hgroup: maptype.HEDTLINE) -> ctypes.c_void_p:
        return mapCloseLayouts_t (_hgroup)


# Считать в память заданную линейку в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# number - номер линейки знаков
# При ошибке возвращает ноль

    mapLoadLayoutsLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLoadLayoutsLine', maptype.HEDTLINE, ctypes.c_int)
    def mapLoadLayoutsLine(_hgroup: maptype.HEDTLINE, _number: int) -> int:
        return mapLoadLayoutsLine_t (_hgroup, _number)


# Добавить новую линейку в набор
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# При ошибке возвращает ноль

    mapAppendLayoutsLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendLayoutsLine', maptype.HEDTLINE)
    def mapAppendLayoutsLine(_hgroup: maptype.HEDTLINE) -> int:
        return mapAppendLayoutsLine_t (_hgroup)


# Удалить линейку в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# number - номер линейки знаков
# При ошибке возвращает ноль

    mapDeleteLayoutsLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteLayoutsLine', maptype.HEDTLINE, ctypes.c_int)
    def mapDeleteLayoutsLine(_hgroup: maptype.HEDTLINE, _number: int) -> int:
        return mapDeleteLayoutsLine_t (_hgroup, _number)


# Запросить номер текущей линейки в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# При ошибке возвращает ноль

    mapGetLayoutsLineNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineNumber', maptype.HEDTLINE)
    def mapGetLayoutsLineNumber(_hgroup: maptype.HEDTLINE) -> int:
        return mapGetLayoutsLineNumber_t (_hgroup)


# Запросить число линеек в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# При ошибке возвращает ноль

    mapGetLayoutsLineCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineCount', maptype.HEDTLINE)
    def mapGetLayoutsLineCount(_hgroup: maptype.HEDTLINE) -> int:
        return mapGetLayoutsLineCount_t (_hgroup)


# Запросить название линейки в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# number - номер линейки знаков
# name - буфер для записи названия
# size - длина буфера в байтах
# При ошибке возвращает ноль

    mapGetLayoutsLineNameForNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineNameForNumber', maptype.HEDTLINE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetLayoutsLineNameForNumber(_hgroup: maptype.HEDTLINE, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetLayoutsLineNameForNumber_t (_hgroup, _number, _name.buffer(), _size)


# Установить название текущей линейки в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# name - название линейки
# При ошибке возвращает ноль

    mapSetLayoutsLineName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetLayoutsLineName', maptype.HEDTLINE, maptype.PWCHAR)
    def mapSetLayoutsLineName(_hgroup: maptype.HEDTLINE, _name: mapsyst.WTEXT) -> int:
        return mapSetLayoutsLineName_t (_hgroup, _name.buffer())


# Запросить описание объекта в текущей линейке в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# item - номер элемента в текущей линейке
# При ошибке возвращает ноль

    mapGetLayoutsLineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineObject', maptype.HEDTLINE, ctypes.c_int, maptype.HOBJ)
    def mapGetLayoutsLineObject(_hgroup: maptype.HEDTLINE, _item: int, _hobj: maptype.HOBJ) -> int:
        return mapGetLayoutsLineObject_t (_hgroup, _item, _hobj)


# Установить описание объекта в текущей линейке в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# item - номер элемента в текущей линейке
# method - идентификатор способа нанесения объекта на карту (1 - Произвольная линия, 2 - Горизонтальный прямоугольник,
#          3 - Наклонный прямоугольник, 4 - Сложный прямоугольник, 5 - Окружность заданного задиуса, и т.д.)
# repeat - признак сохранения семантики при нанесении подряд нескольких объектов
# При ошибке возвращает ноль

    mapSetLayoutsLineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetLayoutsLineObject', maptype.HEDTLINE, ctypes.c_int, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapSetLayoutsLineObject(_hgroup: maptype.HEDTLINE, _item: int, _info: maptype.HOBJ, _method: int, _repeat: int) -> int:
        return mapSetLayoutsLineObject_t (_hgroup, _item, _info, _method, _repeat)


# Запросить идентификатор способа нанесения объекта на карту в текущей линейке в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# item - номер элемента в текущей линейке
# При ошибке возвращает ноль

    mapGetLayoutsLineMethod_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineMethod', maptype.HEDTLINE, ctypes.c_int)
    def mapGetLayoutsLineMethod(_hgroup: maptype.HEDTLINE, _item: int) -> int:
        return mapGetLayoutsLineMethod_t (_hgroup, _item)


# Запросить признак сохранения семантики в текущей линейке в наборе
# hgroup - идентификатор набора линеек знаков (макетов) в памяти
# item - номер элемента в текущей линейке
# При ошибке возвращает ноль

    mapGetLayoutsLineRepeat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLayoutsLineRepeat', maptype.HEDTLINE, ctypes.c_int)
    def mapGetLayoutsLineRepeat(_hgroup: maptype.HEDTLINE, _item: int) -> int:
        return mapGetLayoutsLineRepeat_t (_hgroup, _item)

# Открыть линейку progressbar в главном окне приложения
# Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически)
# Для создания линейки необходимо вызвать mapOpenProgressBar, для смены процента вызывается mapProgressBar,
# для скрытия линейки - mapCloseProgressBar
# В один момент времени в главной панели может быть только одна линейка
# При ошибке возвращает ноль, при успешном выполнении возвращает идентификатор линейки

    mapOpenProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenProgressBar')
    def mapOpenProgressBar() -> ctypes.c_void_p:
        return mapOpenProgressBar_t ()


# Отобразить линейку progressbar в главном окне приложения
# progressbar - идентификатор линейки, полученной в mapOpenProgressBar
# percent - процент заполнения линейки от 0 до 100
# message - комментарий к выполняемой операции, отображается на линейке после процентов
# Если оператор желает прервать процесс, функция вернет значение -1
# При ошибке возвращает ноль, при успешном выполнении возвращает 1

    mapProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapProgressBar', ctypes.c_void_p, ctypes.c_int, maptype.PWCHAR)
    def mapProgressBar(_progressbar: ctypes.c_void_p, _percent: int, _message: mapsyst.WTEXT) -> int:
        return mapProgressBar_t (_progressbar, _percent, _message.buffer())


# Закрыть линейку progressbar в главном окне приложения
# progressbar - идентификатор линейки, полученной в mapOpenProgressBar

    mapCloseProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseProgressBar', ctypes.c_void_p)
    def mapCloseProgressBar(_progressbar: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseProgressBar_t (_progressbar)


# Отправить команду главному окну (текущему окну карты)
# Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически) 
# command - идентификатор команды
# wparam  - первый параметр
# lparam  - второй параметр
# Например, перерисовать окно карты: mapSendMessage(MT_MAPWINPORT, MWP_INVALIDATE, 0);
# Например, выделить объекты на карте по общим условиям: mapSendMessage(CM_PAN_SEARCH, 1, 0);

    mapSendMessage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_longlong, 'mapSendMessage', ctypes.c_int,  ctypes.c_void_p, ctypes.c_void_p)
    def mapSendMessage(_command: ctypes.c_int, _wparam: ctypes.c_longlong, _lparam = 0) -> ctypes.c_longlong:
        return mapSendMessage_t(_command, ctypes.cast(_wparam, ctypes.c_void_p), ctypes.cast(_lparam, ctypes.c_void_p))

# Перерисовать окно карты
    def mapInvalidate():
        mapSendMessage(maptype.MT_MAPWINPORT, maptype.MWP_INVALIDATE, 0)

# Выделить объекты на карте по общим условиям 
    def mapSelectObjects(flag = 1):
        mapSendMessage(maptype.CM_PAN_SEARCH, flag)

# Показать всплывающее информационное сообщение
# text    - текст сообщения
# caption - заголовок сообщения
# Сообщение гаснет через 3 секунды или после нажатия клавиатуры\мышки
    def mapShowMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> int:
        return mapSendMessage_t(maptype.AW_MESSAGEBOX, _text.buffer(), _caption.buffer())

    def mapShowErrorMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> int:
        return mapSendMessage_t(maptype.AW_ERRORBOX, _text.buffer(), _caption.buffer())

# Число в строку
    def IntToStr(_number:int):
        text = mapsyst.WTEXT(64)
        mapLongToStringUn(_number, text, text.size())
        return text.string()

    def FloatToStr(_value:float, _precision = 3):
        text = mapsyst.WTEXT(64)
        mapDoubleToStringUn(_value, text, text.size(), _precision)
        return text.string()

# Запросить путь к папке для хранения кэшируемых данных с ГИС Сервера
    mapGetCachePathUn_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR, 'mapGetCachePathUn')
    def mapGetCachePathUn() -> maptype.PWCHAR:
        return mapGetCachePathUn_t()

# Запросить путь к общей папке файлов параметров задач приложения (INI, XML)
# Пример возращаемой строки: "c:\Users\Public\Documents\Panorama\",  "/var/Panorama/"
# При ошибке возвращает "" (пустую строку)
    mapGetCommonIniPath_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR, 'mapGetCommonIniPath')
    def mapGetCommonIniPath() -> maptype.PWCHAR:
        return mapGetCommonIniPath_t()   

# Запросить путь к пользовательской папке файлов параметров задач приложения (INI, XML)
# Пример возращаемой строки: "c:\Users\<User>\Application Data\Roaming\Panorama15\",  "/home/user/.panorama/"
# <User> - имя пользователя в системе
# При ошибке возвращает ноль
    mapGetUserIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int, 'mapGetUserIniPath', maptype.PWCHAR, ctypes.c_int)
    def mapGetUserIniPath(path:mapsyst.WTEXT) -> ctypes.c_int:
        return mapGetUserIniPath_t(path.buffer(),path.size())