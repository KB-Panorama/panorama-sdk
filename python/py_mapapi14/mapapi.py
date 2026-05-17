#!/usr/bin/env python3

#********************************************************************
#*                                                                  *
#*              Copyright (c) PANORAMA Group 1991-2026              *
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
    _fields_ = [("hMap",maptype.HMAP)]
    def __init__(self, value: maptype.HMAP = 0):
        super().__init__()
        self.hMap = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hMap != 0:
            mapCloseData(self.hMap)
        self.hMap = 0
    def HMAP(self):
        return self.hMap
    def __eq__(self, other):
        return self.hMap == other.hMap
    def __ne__(self, other):
        return self.hMap != other.hMap
#-----------------------------


#-----------------------------
class TEMPHOBJ(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hInfo",maptype.HOBJ)]
    def __init__(self, value: maptype.HOBJ = 0):
        super().__init__()
        self.hInfo = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hInfo != 0:
            mapFreeObject(self.hInfo)
        self.hInfo = 0
    def HOBJ(self):
        return self.hInfo
    def __eq__(self, other):
        return self.hInfo == other.hInfo
    def __ne__(self, other):
        return self.hInfo != other.hInfo
#-----------------------------


#-----------------------------
class TEMPHUSER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hUser",ctypes.c_void_p)]
    def __init__(self, value: ctypes.c_void_p = 0):
        super().__init__()
        self.hUser = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hUser != 0:
            mapDeleteUserSystemParameters(self.hUser)
        self.hUser = 0
    def HUSER(self):
        return self.hUser
    def __eq__(self, other):
        return self.hUser == other.hUser
    def __ne__(self, other):
        return self.hUser != other.hUser
#-----------------------------


#-----------------------------
class TEMPCONNECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Connect",ctypes.c_long)]
    def __init__(self, value: ctypes.c_long = 0):
        super().__init__()
        self.Connect = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.Connect != 0:
            mapCloseConnect(self.Connect)
        self.Connect = 0
    def CONNECT(self):
        return self.Connect
    def __eq__(self, other):
        return self.Connect == other.Connect
    def __ne__(self, other):
        return self.Connect != other.Connect
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'


try:
    curLib = mapsyst.LoadLibrary(gisaccesname)
except Exception as e:
    print(e)
    curLib = 0 

if curLib == 0:
    print(gisaccesname)
else:

#   Программное обеспечение, применяющее интерфейс "MAPAPI",
# может выполняться в различных операционных системах
# (Windows, Linux, QNX, Android и других)
#   Все строковые параметры API - функций имеют кодировку
# ANSI для Windows и KOI-8 для Linux-подобных систем
# Параметры типа HWND и HDC в Windows являются идентификаторами
# окна и графического контекста соответственно.
# В Linux параметр HDC содержит указатель на структуру DEVICECONTEXT
# Версия интерфейса MAPAPI
# #define MAPAPIVERSION ... см. maptype.h
#enum PPLACE             # ПРИМЕНЯЕМАЯ СИСТЕМА КООРДИНАТ
#    {
#      PP_MAP     = 1,    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ КАРТЫ В ДИСКРЕТАХ
#      PP_PICTURE = 2,    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ ИЗОБРАЖЕНИЯ В ПИКСЕЛАХ
#      PP_PLANE   = 3,    # КООРДИНАТЫ ТОЧЕК В ПЛОСКОЙ ПРЯМОУГОЛЬНОЙ СИСТЕМЕ
#                         # НА МЕСТНОСТИ В МЕТРАХ
#      PP_GEO     = 4,    # КООРДИНАТЫ ТОЧЕК В ГЕОДЕЗИЧЕСКИХ КООРДИНАТАХ В РАДИАНАХ
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
# Открыть данные с автоматическим определением их типа: векторные, растровые, матричные, проект, ...
# name - полный путь к открываемому файлу (MAP, SITX, MTW, RSW, MPT и так далее) в кодировке UNICODE
# mode - режим чтения/записи: GENERIC_READ, GENERIC_WRITE или 0
#      GENERIC_READ - все данные только на чтение, при этом не открываются
#      файлы \Log\name.log и \Log\name.tac - протокол работы и журнал транзакций
# error - после выполнения функции переменная содержит код ошибки, когда HMAP равен 0, или 0;
#      коды ошибок приведены в maperr.rh
# password - пароль доступа к данным из которого формируется 256-битный код
#      для шифрования данных (при утрате пароля данные не восстанавливаются) или ноль
# size - длина пароля в байтах или ноль
# Передача пароля необходима, если при создании карты он был указан
# Если пароль не передан, а он был указан при создании,
# то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
# Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
# не вызывается, а при отсутствии пароля происходит отказ открытия данных
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

    mapOpenAnyDataPro_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapOpenAnyDataPro', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapOpenAnyDataPro(_name: mapsyst.WTEXT, _mode: int, _error: ctypes.POINTER(ctypes.c_long), _password: mapsyst.WTEXT, _size: int) -> maptype.HMAP:
        if _error == 0:
            etemp = ctypes.c_int(0)
            return mapOpenAnyDataPro_t (_name.buffer(), _mode, ctypes.byref(etemp), _password.buffer(), _size)
        return mapOpenAnyDataPro_t (_name.buffer(), _mode, _error, _password.buffer(), _size)


# Проверить идентификатор данных на корректность
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapIsMapHandleCorrect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMapHandleCorrect', maptype.HMAP)
    def mapIsMapHandleCorrect(_hmap: maptype.HMAP) -> int:
        return mapIsMapHandleCorrect_t (_hmap)


# Установить разрешение выполнять структурный контроль карты после сбоев программы
# flag - нулевое значение запрещает выполнение контроля структуры
#     при открытии карты, ненулевое значение - разрешает
# Возвращает старое значение флага

    mapSetStructureControlFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetStructureControlFlag', ctypes.c_long)
    def mapSetStructureControlFlag(_flag: int) -> int:
        return mapSetStructureControlFlag_t (_flag)


# Установить ограничение на число разрешенных к использованию ядер (процессоров) в системе
# state - флаг ограничения числа ядер (процессоров) в системе:
#     = 0 - не использовать многопоточность
#     > 1 - максимальное число потоков в выполняемых задачах
#     < -1 - доля ядер (процессоров) разрешенных для выполнения потоков
#     Например, -2 - использовать не более 1/2 ядер (процессоров) в системе
# Изначально потоки разрешены, но для серверного применения библиотеки,
# работающей в многопоточных приложениях, внутренние потоки понижают
# общую производительность. Например, внутренняя реализация функции
# отображения растра запускает до 8 потоков. Если функция отображения
# вызвана параллельно 10 потоками, одномоментно будет работать 90 потоков.
# Внутреннее число потоков не превышает число ядер процессора, включая виртуальные ядра
# Возвращает старое значение состояния разрешения внутренних потоков

    mapUseInsideThread_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUseInsideThread', ctypes.c_long)
    def mapUseInsideThread(_state: int) -> int:
        return mapUseInsideThread_t (_state)


# Запросить число ядер (процессоров) в системе, доступных для приложения с учетом установленных ограничений
# Минимальное возвращаемое значение равно 1 (не использовать многопоточность)

    mapGetProcessorNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProcessorNumber')
    def mapGetProcessorNumber() -> int:
        return mapGetProcessorNumber_t ()


# Установить режим добавления данных к карте
# hmap - идентификатор открытых данных (документа)
# mode - режим добавления данных: 1 - ускоренный, 0 - стандартный
# При ускоренном режиме не пересчитываются габариты документа по
# всем открытым данным и не обновляется палитра, что существенно
# ускоряет процесс добавления данных потоком
# По окончанию добавления данных рекомендуется вернуть режим добавления
# к стандартному для обновления габаритов и палитры
# Габариты обновляются автоматически и при масштабировании документа,
# а палитра нужна при формировании изображений с ограниченным диапазоном цветов
# После вызова mapOpenProject или mapAppendProject автоматически устанавливает
# стандартный режим обновления данных
# Возвращает текущее значение режима

    mapSetAppendDataMode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAppendDataMode', maptype.HMAP, ctypes.c_long)
    def mapSetAppendDataMode(_hmap: maptype.HMAP, _mode: int) -> int:
        return mapSetAppendDataMode_t (_hmap, _mode)


# Установить для карты режим потоковой загрузки данных
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# state - режим потоковой загрузки данных: 1 - включен, 0 - выключен
# Применяется для ускорения загрузки данных из обменных форматов при создании карты
# В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
# В режиме потоковой загрузки данных отключается журналирование операций
# При ошибке возвращает ноль

    mapSetLoadState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetLoadState', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetLoadState(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _state: int) -> int:
        return mapSetLoadState_t (_hmap, _hsite, _state)


# Запросить для карты режим потоковой загрузки данных
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# Применяется для ускорения загрузки данных из обменных форматов при создании карты
# В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
# В режиме потоковой загрузки данных отключается журналирование операций
# При ошибке возвращает ноль

    mapGetLoadState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLoadState', maptype.HMAP, maptype.HSITE)
    def mapGetLoadState(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetLoadState_t (_hmap, _hsite)


# Запросить наличие в составе открытых данных карт в состоянии потоковой загрузки данных
# hmap - идентификатор открытых данных (документа)
# В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
# Возвращает ненулевое значение, если хотя бы одна из карт находится в режиме потоковой загрузки
# При ошибке возвращает ноль

    mapCheckLoadState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckLoadState', maptype.HMAP)
    def mapCheckLoadState(_hmap: maptype.HMAP) -> int:
        return mapCheckLoadState_t (_hmap)


# Запросить процент загрузки данных
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# Для локальных данных показывает процесс загрузки в оперативную память,
# для данных с ГИС Сервера - процесс загрузки в кэш, для баз данных - процесс формирования кэша
# Возвращает процент загрузки данных

    mapGetSitePercentLoad_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePercentLoad', maptype.HMAP, maptype.HSITE)
    def mapGetSitePercentLoad(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePercentLoad_t (_hmap, _hsite)


# Запросить процент загрузки и объём загруженных данных в Мб
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# loadsize - поле для записи размера загруженных данных в Мб
# Для локальных данных показывает процесс загрузки в оперативную память,
# для данных с ГИС Сервера - процесс загрузки в кэш,
# для баз данных - процесс формирования кэша
# Возвращает процент загрузки данных

    mapGetSitePercentAndSizeLoad_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePercentAndSizeLoad', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapGetSitePercentAndSizeLoad(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _loadsize: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetSitePercentAndSizeLoad_t (_hmap, _hsite, _loadsize)


# Добавить данные (карту, растр, матрицу) к открытой карте и выполнить трансформирование при необходимости
# hmap - идентификатор открытых данных (документа)
# name - полный путь к открываемому файлу (MAP, SITX, SIT, MTW, MTQ, RSW, MPT) в кодировке UNICODE
# mode - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# transform - признак трансформирования векторной карты к ранее открытым данным:
#     0 - не трансформировать данные (преобразовывать "на лету"),
#     1 - трансформировать данные при открытии и сохранить карту в новой проекции,
#     -1 - задать вопрос пользователю.
#     В серверной версии -1 обрабатывается, как 0
# password - пароль доступа к данным из которого формируется 256-битный код
#     для шифрования данных (при утрате данные не восстанавливаются) или ноль
# size - длина пароля в байтах или ноль
# Передача пароля необходима, если при создании карты он был указан
# Если пароль не передан, а он был указан при создании,
# то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
# Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
# не вызывается, а при отсутствии пароля происходит отказ открытия данных
# Возвращает идентификатор типа данных (FILE_MAP - для векторной
# карты, FILE_RSW - для растра, FILE_MTW - для матрицы, FILE_MTL - для
# матрицы слоев, FILE_MTQ - для матрицы качеств), данные добавляются в
# список последними, если данные уже были открыты, число открытых данных (карт, растров, матриц) не меняется
# При ошибке возвращает ноль

    mapAppendAnyDataPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendAnyDataPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapAppendAnyDataPro(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int = 0, _transform: int = -1, _password: mapsyst.WTEXT = None, _size: int = 0) -> int:
        return mapAppendAnyDataPro_t (_hmap, _name.buffer(), _mode, _transform, _password.buffer(), _size)

    mapAppendAnyDataEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendAnyDataEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapAppendAnyDataEx(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int = 0, _transform: int = -1, _password: mapsyst.WTEXT = None, _size: int = 0, _error: ctypes.POINTER(ctypes.c_long) = None) -> int:
        return mapAppendAnyDataEx_t (_hmap, _name.buffer(), _mode, _transform, _password.buffer(), _size, _error)


# Обновить в документе общие габариты района работ
# hmap - идентификатор открытых данных (документа)
# После смены ограничения на область отображения или создания объекта на векторной карте
# за пределами текущих габаритов документа необходимо обновить габариты района и затем обновить
# позицию изображения карты в окне
# При ошибке возвращает ноль

    mapSetRegion_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetRegion', maptype.HMAP)
    def mapSetRegion(_hmap: maptype.HMAP) -> int:
        return mapSetRegion_t (_hmap)


# Проверить, что карты, растры и матрицы из одного документа, входят в состав открытых данных другого документа
# hmap - идентификатор открытых данных (документа)
# hcheckhmap - идентификатор открытых данных (документа), в котором ищутся карты из hmap
# Если все данные входят, то возвращает положительное значение
# При ошибке возвращает ноль

    mapCheckDocIncludeDoc_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckDocIncludeDoc', maptype.HMAP, maptype.HMAP)
    def mapCheckDocIncludeDoc(_hmap: maptype.HMAP, _hcheckhmap: maptype.HMAP) -> int:
        return mapCheckDocIncludeDoc_t (_hmap, _hcheckhmap)


# Запросить соответствие систем координат добавляемой в документ карты и документа
# hmap - идентификатор открытых данных (документа)
# fileName - имя файла добавляемых данных (карты, растра, матрицы)
# Если система координат карты не соответствует открытому району, функция возвращает 1
# При ошибке возвращает ноль

    mapIsNeedTranslate_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsNeedTranslate', maptype.HMAP, maptype.PWCHAR)
    def mapIsNeedTranslate(_hmap: maptype.HMAP, _fileName: mapsyst.WTEXT) -> int:
        return mapIsNeedTranslate_t (_hmap, _fileName.buffer())


# Запросить размер данных по имени файла
# name - полный путь к файлу
# При ошибке возвращает ноль

    mapGetDataSizeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetDataSizeUn', maptype.PWCHAR)
    def mapGetDataSizeUn(_name: mapsyst.WTEXT) -> float:
        return mapGetDataSizeUn_t (_name.buffer())


# Запросить имя главной карты в документе или имя проекта (mpt, mptz), если открыт проект
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает пустую строку

    mapGetMainNameEx_t = mapsyst.GetProcAddress(curLib,maptype.PWCHAR,'mapGetMainNameEx', maptype.HMAP)
    def mapGetMainNameEx(_hmap: maptype.HMAP) -> mapsyst.WTEXT:
        return mapGetMainNameEx_t (_hmap)


# Запросить в кодировке UNICODE имя главной карты в документе или имя проекта (mpt, mptz), если открыт проект
# hmap - идентификатор открытых данных (документа)
# name - адрес буфера для записи полного пути к файлу
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetMainNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMainNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMainNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMainNameUn_t (_hmap, _name.buffer(), _size)


# Запросить имя (полный путь к файлу) главной карты в документе или в проекте (MPT)
# hmap - идентификатор открытых данных (документа)
# name - буфер для возвращаемой строки
# namesize - размер буфера в байтах
# При ошибке возвращает 0

    mapGetMainMapNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMainMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMainMapNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetMainMapNameUn_t (_hmap, _name.buffer(), _namesize)


# Заполнение справочных данных в зависимости от типа карты
# maptype - тип карты, описание в MAPTYPE в файле mapcreat.h
# mapreg - заполняемая структура параметров системы координат карты
# Структуры MAPREGISTEREX, LISTREGISTER описаны в mapcreat.h
# При ошибке возвращает ноль

    mapRegisterFromMapType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterFromMapType', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapRegisterFromMapType(_maptype: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return mapRegisterFromMapType_t (_maptype, _mapreg)


# Запросить допустимые параметры для проекции
# code - номер проекции из MAPPROJECTION в файле mapcreat.h
# Возвращает комбинацию флагов PROJECTIONPARAMETERS в файле mapcreat.h
# Например: значение 49 = EPP_AXISMERIDIAN|EPP_FALSEEASTING|EPP_FALSENORTHING
# При ошибке возвращает ноль

    mapGetProjectionParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProjectionParameters', ctypes.c_long)
    def mapGetProjectionParameters(_code: int) -> int:
        return mapGetProjectionParameters_t (_code)


# Создать новую векторную карту
# mapname - полное имя файла карты (MAP, SIT, SITX)
# rscname - полное имя файла ресурсов (RSC)
# mapreg - структура параметров системы координат карты
# listreg - параметры листа многолистовой карты или 0
# sheetnames - название (UTF-16) листа карты, номенклатуры и файлов даных (для многолистовой карты),
#     для векторной карты не ограниченной рамкой название листа и номенклатуры совпадает,
#     а название файлов данных совпадает с названием паспорта карты
# mainname - главное название (UTF-16) многолистовой карты (MAP),
#     для пользовательской карты совпадает с названием листа карты
#     Запросить главное название карты можно функцией mapGetSiteNameUn
# password  - пароль доступа к данным из которого формируется 256-битный код
#     для шифрования данных или 0. При утрате пароля данные не восстанавливаются.
#     Поддерживается для карт с расширением SITX - хранилище в одном файле
# size - длина пароля в байтах или 0
# hmap - идентификатор документа с открытыми картами
# hsite - идентификатор карты в документе, из которой будет скопирован пароль доступа к данным
# error - поле для получения кода ошибки или 0; коды ошибок приведены в maperr.rh
# Возвращает идентификатор открытой векторной карты
# Структуры MAPREGISTEREX, LISTREGISTER и SHEETNAMES описаны в mapcreat.h
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

    mapCreateMapExp_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapCreateMapExp', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.HMAP, maptype.HSITE)
    def mapCreateMapExp(_mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long), _hmap: maptype.HMAP = 0, _hsite: maptype.HSITE = 0) -> maptype.HMAP:
        return mapCreateMapExp_t (_mapname.buffer(), _rscname.buffer(), _mapreg, _listreg, _sheetnames, _mainname.buffer(), _password.buffer(), _size, _error, _hmap, _hsite)


# Создать новую векторную карту по образцу
# mapname - полный путь к файлу новой карты (расширение MAP, SIT, SITX):
#     MAP - может быть задано только, если исходная карта имеет тип MAP
# mainname - название карты или 0; eсли mainname = 0, то используется имя файла (без расширения)
# rscname - имя файла классификатора; eсли rscname = 0, используется классификатор исходной карты
# saveborder  - сохранить объект-рамку (учитывается только при наличии у исходной карты объекта-рамки):
#     1 - сохранить рамку, название листа и номенклатуру;
#     0 - не сохранять рамку; в название листа и номенклатуру записывается название карты
# hmap - идентификатор документа с открытыми картами
# hsite - идентификатор карты в документе, из которой будут скопированы параметры системы координат
# error - поле для получения кода ошибки или 0; коды ошибок приведены в maperr.rh
# Возвращает идентификатор новой векторной карты
# При ошибке возвращает ноль

    mapCreateSiteForMapEx_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapCreateSiteForMapEx', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapCreateSiteForMapEx(_mapname: mapsyst.WTEXT, _mainname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _saveborder: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _error: ctypes.POINTER(ctypes.c_long)) -> maptype.HMAP:
        return mapCreateSiteForMapEx_t (_mapname.buffer(), _mainname.buffer(), _rscname.buffer(), _saveborder, _hmap, _hsite, _error)

    mapCreateSiteForMap_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapCreateSiteForMap', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapCreateSiteForMap(_mapname: mapsyst.WTEXT, _mainname: mapsyst.WTEXT, _saveborder: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _error: ctypes.POINTER(ctypes.c_long)) -> maptype.HMAP:
        return mapCreateSiteForMap_t (_mapname.buffer(), _mainname.buffer(), _saveborder, _hmap, _hsite, _error)


# Создать временную пользовательскую карту
# rscname - полный путь к файлу ресурсов (RSC)
# mapreg - параметры проекции создаваемой временной карты или 0
#     Если mapreg не задан, то создается Цилиндрическая прямая равноугольная Меркатора на шаре EPSG:3857
# datum - параметры датума или 0
# ellipsoid - параметры эллипсоида или 0
# inmemory - признак создания карты в оперативной памяти или 0
# Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
# и освобождаются при закрытии карты
# Файлы карты размещаются в рабочей директории системы и имеют уникальные имена, генерируемые автоматически
# При закрытии карты все файлы данных удаляются
# После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
# При ошибке возвращает ноль

    mapCreateTempSitePro_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapCreateTempSitePro', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long)
    def mapCreateTempSitePro(_rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _inmemory: int) -> maptype.HMAP:
        return mapCreateTempSitePro_t (_rscname.buffer(), _mapreg, _datum, _ellipsoid, _inmemory)


# Создать временную пользовательскую карту с системой координат и классификатором, как у эталонной карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# inmemory - признак создания карты в оперативной памяти или 0
# При ошибке возвращает ноль

    mapCreateTempSiteForMap_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapCreateTempSiteForMap', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapCreateTempSiteForMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _inmemory: int) -> maptype.HMAP:
        return mapCreateTempSiteForMap_t (_hmap, _hsite, _inmemory)


# Создать временную пользовательскую карту с текущими параметрами документа и добавить ее в документ
# hmap - идентификатор открытого документа
# rscname - полное имя файла ресурсов, если равно 0 - выбирается из открытой карты
# inmemory - признак создания карты в оперативной памяти или 0
# Файлы карты размещаются в рабочей директории системы и имеют уникальные имена, генерируемые автоматически
# При закрытии векторной карты все файлы данных автоматически удаляются
# Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
# и освобождаются при закрытии карты
# Возвращает идентификатор открытой векторной карты
# При ошибке возвращает ноль

    mapCreateAndAppendTempSitePro_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapCreateAndAppendTempSitePro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapCreateAndAppendTempSitePro(_hmap: maptype.HMAP, _rscname: mapsyst.WTEXT, _inmemory: int) -> maptype.HSITE:
        return mapCreateAndAppendTempSitePro_t (_hmap, _rscname.buffer(), _inmemory)


# Закрыть все данные электронной карты
# hmap - идентификатор открытых данных (документа)
# Идентификатор HMAP становится недействительным

    mapCloseData_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseData', maptype.HMAP)
    def mapCloseData(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapCloseData_t (_hmap)


# Копирование или перемещение векторной карты
# sourcename - полный путь к файлу к файлу существующей карты
# newname - полный путь к новому файлу карты
# ismove - признак необходимости удаления старой копии карты (перемещения)
# error - поле для получения кода ошибки при выполнении команды (описаны в maperr.rh)
# total - копировать (перемещать) вместе со служебными файлами в папке \LOG (например, для резервного копирования)
# При ошибке возвращает ноль

    mapCopyMapEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyMapEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapCopyMapEx(_sourcename: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _ismove: int, _error: ctypes.POINTER(ctypes.c_long), _total: int) -> int:
        return mapCopyMapEx_t (_sourcename.buffer(), _newname.buffer(), _ismove, _error, _total)


# Закрыть и удалить векторную карту (все файлы данных)
# hmap - идентификатор открытых данных (документа)
# После удаления идентификатор hmap не должен использоваться, как после mapCloseData()
# При ошибке возвращает ноль

    mapDeleteMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteMap', maptype.HMAP)
    def mapDeleteMap(_hmap: maptype.HMAP) -> int:
        return mapDeleteMap_t (_hmap)


# Удаление района работ
# name - полный путь к файлу удаляемой карты
# rscdelete - признак удаления файла классификатора вместе с картой
# При ошибке возвращает ноль

    mapDeleteMapByNameEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteMapByNameEx', maptype.PWCHAR, ctypes.c_long)
    def mapDeleteMapByNameEx(_name: mapsyst.WTEXT, _rscdelete: int) -> int:
        return mapDeleteMapByNameEx_t (_name.buffer(), _rscdelete)


# Открыть проект данных (может содержать карты, растры, матрицы, геопорталы ...)
# name - полный путь к файлу проекта MPT
# При ошибке возвращает ноль

    mapOpenProjectUn_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapOpenProjectUn', maptype.PWCHAR)
    def mapOpenProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        return mapOpenProjectUn_t (_name.buffer())


# Добавить проект данных
# hmap - идентификатор открытых данных (документа)
# name - полный путь к файлу проекта MPT
# При ошибке возвращает ноль

    mapAppendProjectUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapAppendProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapAppendProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapAppendProjectUn_t (_hmap, _name.buffer())


# Открыть упакованный проект данных
# name - полный путь к файлу проекта MPTZ со сжатыми данными
# При ошибке возвращает ноль

    mapOpenZipProjectUn_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapOpenZipProjectUn', maptype.PWCHAR)
    def mapOpenZipProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        return mapOpenZipProjectUn_t (_name.buffer())


# Запросить имя открытого проекта
# hmap - идентификатор открытых данных (документа)
# name - буфер для размещения возвращаемой строки
# namesize - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetProjectNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProjectNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetProjectNameUn_t (_hmap, _name.buffer(), _namesize)


# Сохранить список открытых наборов данных и их свойства в проекте данных MPT
# hmap - идентификатор открытых данных (документа)
# name - полный путь к файлу проекта MPT
# При ошибке возвращает ноль

    mapSaveProjectUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapSaveProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapSaveProjectUn_t (_hmap, _name.buffer())


# Сохранить список открытых наборов данных, их свойства и упакованные наборы данных в проекте данных MPTZ
# hmap - идентификатор открытых данных (документа)
# name - полный путь к файлу проекта MPTZ
# savefromserver - признак копирования в MPTZ наборов данных с ГИС Сервера,
#     если есть права на их копирование
# В проект сохраняются упакованные векторные карты (SITZ\MAPZ), сжатые растры RSW и
# сжатые матрицы MTW, MTQ
# При ошибке возвращает ноль

    mapSaveZipProjectUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveZipProjectUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSaveZipProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _savefromserver: int) -> int:
        return mapSaveZipProjectUn_t (_hmap, _name.buffer(), _savefromserver)


# Запросить, является ли документ проектом MPT или MPTZ
# hmap - идентификатор открытых данных (документа)
# Если это проект, то возвращает ненулевое значение,
# если это упакованный проект MPTZ - возвращает значение FILE_MPTZ

    mapIsDocProject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDocProject', maptype.HMAP)
    def mapIsDocProject(_hmap: maptype.HMAP) -> int:
        return mapIsDocProject_t (_hmap)


# Проверить изменение состояния файла проекта на ГИС Сервере
# hmap - идентификатор открытых данных (документа)
# Если состояние проекта изменилось - возвращает ненулевое значение

    mapCheckProjectState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckProjectState', maptype.HMAP)
    def mapCheckProjectState(_hmap: maptype.HMAP) -> int:
        return mapCheckProjectState_t (_hmap)


# Сохранить текущие параметры открытого документа в INI-файл карты
# hmap - идентификатор открытых данных (документа)
# point - координаты центра окна в метрах или 0
# Вызывается перед закрытием окна карты
# Сохраняет описание открытых данных, масштаб, палитру, признаки видимости,
# редактируемости, состав отображаемых объектов...
# При ошибке возвращает ноль

    mapSaveMapState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSaveMapState(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSaveMapState_t (_hmap, _point)


# Восстановить параметры окна карты из INI-файла карты
# hmap - идентификатор открытых данных (документа)
# point - поле для записи сохраненных координат центра окна в метрах или 0
# Имя INI-файла можно запросить через mapGetMapIniName()
# Вызывается после открытия карты
# Восстанавливает описание списка данных, масштаб, палитру, признаки видимости,
# редактируемости, состав отображаемых объектов
# При ошибке возвращает ноль

    mapRestoreMapState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRestoreMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRestoreMapState(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapRestoreMapState_t (_hmap, _point)


# Запросить, есть ли какие-либо открытые карты, растры, матрицы, геопорталы или другие данные
# hmap - идентификатор открытых данных (документа)
# Если открытых данных нет, то возвращает ноль

    mapIsActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsActive', maptype.HMAP)
    def mapIsActive(_hmap: maptype.HMAP) -> int:
        return mapIsActive_t (_hmap)


# Запросить, есть ли какие-либо открытые векторные карты
# hmap - идентификатор открытых данных (документа)
# Если открытых векторных карт нет, то возвращает ноль

    mapIsVectorMapActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsVectorMapActive', maptype.HMAP)
    def mapIsVectorMapActive(_hmap: maptype.HMAP) -> int:
        return mapIsVectorMapActive_t (_hmap)


# Запросить, есть ли какие-либо открытые векторные карты, доступные для редактирования
# hmap - идентификатор открытых данных (документа)
# Если доступных для редактирования векторных карт нет, то возвращает ноль

    mapIsVectorMapEdit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsVectorMapEdit', maptype.HMAP)
    def mapIsVectorMapEdit(_hmap: maptype.HMAP) -> int:
        return mapIsVectorMapEdit_t (_hmap)


# Запросить, есть ли какие-либо открытые векторные карты c доступом на редактирование семантики или графики
# hmap - идентификатор открытых данных (документа)
# Если доступных для редактирования векторных карт нет, то возвращает ноль

    mapIsVectorMapEditWithoutMetric_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsVectorMapEditWithoutMetric', maptype.HMAP)
    def mapIsVectorMapEditWithoutMetric(_hmap: maptype.HMAP) -> int:
        return mapIsVectorMapEditWithoutMetric_t (_hmap)


# Запросить, есть ли в документе какие-либо открытые данные помимо указанного типа
# hmap - идентификатор открытых данных (документа)
# dataType - идентификатор типа данныхб который не нужно учитывать при подсчете
#     Примеры типов данных: FILE_MAP - для векторной карты, FILE_SITE - для пользовательских карт,
#     FILE_RSW - для растров, FILE_MTW - для матриц, FILE_MTL - для матриц слоев,
#     FILE_MTQ - для матрицы качеств, FILE_MTD - для модели "Облако точек",
#     FILE_TIN - для TIN-модели ", FILE_WMS - для геопортала).
# Если dataType равно 0, то выполняется подсчет всех видов данных документа
# Возвращает количество открытых данных в документе помимо указанного типа

    mapGetActiveDataCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetActiveDataCount', maptype.HMAP, ctypes.c_long)
    def mapGetActiveDataCount(_hmap: maptype.HMAP, _dataType: int) -> int:
        return mapGetActiveDataCount_t (_hmap, _dataType)


# Выполнить согласование данных электронной карты в памяти и на диске
# hmap - идентификатор открытых данных (документа)
# Если состояние данных в памяти изменилось (по данным с диска) - возвращает ненулевое значение (1), иначе - 0
# Если карта должна быть закрыта - возвращает 2 (доступ на ГИС Сервер прекращен)
# Если состояние изменилось - необходимо перерисовать изображение карты
# Опрос состояния целесообразно выполнять периодически в процессе работы приложения

    mapAdjustData_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAdjustData', maptype.HMAP)
    def mapAdjustData(_hmap: maptype.HMAP) -> int:
        return mapAdjustData_t (_hmap)


# Установить доступность для выполнения команды Adjust
# hmap - идентификатор открытых данных (документа)
# mode - признак доступности обработки команды Adjust,
#     если равен 0, то команда не обрабатывается
# При выполнении длительных процедур (отмена длинных транзакций, трансформирование данных и других) целесообразно
# отключать команду Adjust, если она может быть вызвана из других потоков приложения
# Команда Adjust может вызывать переоткрытие карт и перераспределение памяти
# Возвращает прежнее значение

    mapSetAdjustMode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAdjustMode', maptype.HMAP, ctypes.c_long)
    def mapSetAdjustMode(_hmap: maptype.HMAP, _mode: int) -> int:
        return mapSetAdjustMode_t (_hmap, _mode)


# Создать (добавить) новый лист в многолистовой карте типа MAP
# hmap - идентификатор открытых данных (документа)
# sheet - описание создаваемого листа в многолистововй карте
# sheetnames - имена файлов листа в многолистовой карте
# Структуры LISTREGISTER и SHEETNAMES описаны в mapcreat.h
# При ошибке возвращает ноль, иначе - номер созданного листа c 1

    mapCreateListPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateListPro', maptype.HMAP, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapCreateListPro(_hmap: maptype.HMAP, _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        return mapCreateListPro_t (_hmap, _sheet, _sheetnames)


# Удалить указанный лист карты в многолистовой карте типа MAP
# hmap - идентификатор открытых данных (документа)
# list - номер листа с 1
# При ошибке возвращает ноль

    mapDeleteList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteList', maptype.HMAP, ctypes.c_long)
    def mapDeleteList(_hmap: maptype.HMAP, _list: int) -> int:
        return mapDeleteList_t (_hmap, _list)


# Добавить листы из одной многолистовой карт в другую
# hmap - идентификатор открытых данных (документа)
# name - полный путь к файлу добавляемой карты
# handle - идентификатор окна, которое будет извещаться о ходе процесса (0x585 - 0x588)
# При ошибке возвращает ноль

    mapAppendMapToMapUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendMapToMapUn', maptype.HMAP, maptype.PWCHAR, maptype.HWND)
    def mapAppendMapToMapUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        return mapAppendMapToMapUn_t (_hmap, _name.buffer(), _handle)


# Сортировка отдельной карты документа
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор сортируемой векторной карты
# flags - флажки обработки карты:
#     0 - сортировать все листы,
#     1 - только несортированные,
#     2 - сохранять файлы отката,
#     4 - повысить точность хранения, формат - мкм
#     16 - повысить точность хранения, формат - см
#     32 - повысить точность хранения, формат - мм
#     64 - повысить точность хранения, формат - радианы
#     128 - формировать мультиконтура для объектов с флагом мультиконтурный
#     256 - упаковать карту вместе с локальными документами, на которые есть ссылка из семантики
#     512 - не упаковывать RSC
#     1024 - перекодировать семантику в кодировку ANSI (возможна потеря некоторых символов из кодировки UTF16)
# handle - идентификатор окна, которому посылаются сообщения WM_OBJECT и WM_ERROR,
#          если не задан параметр hEvent. Может быть равен 0
# format - управление форматом карты:
#     0 - не менять,
#     1 - установить формат SITX (на входе может быть SIT или MAP с одним листом),
#     2 - упаковать карту в формат SITZ\MAPZ, точность - см,
#     -1 - установить формат SIT (на входе может быть SITX или MAP с одним листом),
# code - управление шифрованием карты:
#     0 - не менять,
#     1 - шифровать данные с помощью пароля из параметра password (формат SITX),
#     -1 - снять шифрование данных
# password - пароль для шифрования данных, когда code = 1, или 0
# Если карта отсортирована успешно, то возвращает 1
# Если карта уже отсортирована - возвращает 2
# Если оператор прервал операцию - возвращает -1
# Если карта не доступна на редактирование - возвращает -2
# При ошибке возвращает ноль

    MapSortingSitePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'MapSortingSitePro', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HMESSAGE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def MapSortingSitePro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flags: int, _handle: maptype.HMESSAGE, _format: int, _code: int, _password: mapsyst.WTEXT) -> int:
        return MapSortingSitePro_t (_hmap, _hsite, _flags, _handle, _format, _code, _password.buffer())


# Cоздать пустой объект векторной карты
# hmap - идентификатор открытых данных (документа)
# sheetnumber - номер листа в котором будет расположен объект
# kind - тип создаваемой метрики, описан в maptype.h
# text - признак метрики с текстом для создания объектов типа "подпись"
# После вызова функций поиска и чтения объектов все параметры
# полученного объекта могут быть другими
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции mapFreeObject()
# При ошибке возвращает ноль

    mapCreateObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapCreateObject', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCreateObject(_hmap: maptype.HMAP, _sheetnumber: int = 1, _kind: int = maptype.IDDOUBLE2, _text: int = 0) -> maptype.HOBJ:
        return mapCreateObject_t (_hmap, _sheetnumber, _kind, _text)


# Очистить содержимое объекта
# hobj - идентификатор объекта карты в памяти
# sheetnumber - номер листа в котором будет расположен
# kind - тип создаваемой метрики, описан в maptype.h
# При ошибке возвращает ноль

    mapClearObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapClearObject(_hobj: maptype.HOBJ, _sheetnumber: int = 1, _kind: int = maptype.IDDOUBLE2) -> int:
        return mapClearObject_t (_hobj, _sheetnumber, _kind)


# Запросить корректность содержания объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsObjectCorrect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectCorrect', maptype.HOBJ)
    def mapIsObjectCorrect(_hobj: maptype.HOBJ) -> int:
        return mapIsObjectCorrect_t (_hobj)


# Запросить признак удаленного объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsObjectDeleted_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectDeleted', maptype.HOBJ)
    def mapIsObjectDeleted(_hobj: maptype.HOBJ) -> int:
        return mapIsObjectDeleted_t (_hobj)


# Cоздать копию объекта векторной карты
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции mapFreeObject()
# При ошибке возвращает ноль

    mapCreateCopyObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapCreateCopyObject', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        return mapCreateCopyObject_t (_hmap, _hobj)


# Считать полную копию объекта векторной карты в другой объект
# hdest - идентификатор заполняемого объекта карты в памяти
# hsrc - идентификатор считываемого объекта карты в памяти
# При ошибке возвращает ноль

    mapReadCopyObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadCopyObject', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        return mapReadCopyObject_t (_hdest, _hsrc)


# Считать копию подобъекта векторной карты в другой объект
# hdest - идентификатор заполняемого объекта карты в памяти
# hsrc - идентификатор считываемого объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Копирует все данные объекта с сохранением в качестве одного главного контура указанный подобъект
# При ошибке возвращает ноль

    mapReadCopySubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadCopySubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapReadCopySubject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ, _subject: int) -> int:
        return mapReadCopySubject_t (_hdest, _hsrc, _subject)


# Считать копию внешнего контура мультиполигона вместе с его подобъектами в другой объект
# hdest - идентификатор заполняемого объекта карты в памяти
# hsrc - идентификатор считываемого объекта карты в памяти
# number - порядковый номер внешнего контура, начиная с 1
# Копирует все данные объекта с сохранением одного внешнего контура и его подобъектов
# При ошибке возвращает ноль

    mapReadCopyMultiSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadCopyMultiSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapReadCopyMultiSubject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ, _number: int) -> int:
        return mapReadCopyMultiSubject_t (_hdest, _hsrc, _number)


# Считать копию метрики объекта векторной карты в другой объект
# hdest - идентификатор заполняемого объекта карты в памяти
# hsrc - идентификатор считываемого объекта карты в памяти
# При ошибке возвращает ноль

    mapReadCopyObjectData_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadCopyObjectData', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObjectData(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        return mapReadCopyObjectData_t (_hdest, _hsrc)


# Копировать метрику подобъекта одного объекта в подобъект другого объекта
# hdest - объект-приемник, в который добавляется подобъект
# destsub - номер подобъекта приемника с 0. Если указать -1 или несуществующий номер подобъекта,
#           то добавляется новый подобъект
# hsource - объект-источник (source и dest должны принадлежать одной карте)
# sourcesub - номер подобъекта источника с 0, если указать -1, то копируются все подобъекты, а destSub игнорируется
# Функция выполняет:
#   - добавление подобъекта;
#   - замену подобъекта;
#   - замену всех подобъектов.
# Пример (назначение последнего подобъекта главным):
#   int sub = mapPolyCount(obj)-1;           # Номер последнего контура
#   mapCopySubjectOneMap(obj, -1, obj, 0);   # Копировать главный контур в дополнительный
#   mapCopySubjectOneMap(obj, 0, obj, sub);  # Копировать контур в главный
#   mapDeleteSubject(obj, subject);          # Удалить старую копию контура
# При ошибке возвращает ноль

    mapCopySubjectOneMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopySubjectOneMap', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCopySubjectOneMap(_hdest: maptype.HOBJ, _destsub: int, _hsource: maptype.HOBJ, _sourcesub: int) -> int:
        return mapCopySubjectOneMap_t (_hdest, _destsub, _hsource, _sourcesub)


# Cоздать копию объекта векторной карты, как нового объекта
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# В созданной копии объекта обнуляются порядковый номер и уникальный идентификатор на карте
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции mapFreeObject()
# При ошибке возвращает ноль

    mapCreateCopyObjectAsNew_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapCreateCopyObjectAsNew', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObjectAsNew(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        return mapCreateCopyObjectAsNew_t (_hmap, _hobj)


# Считать копию объекта векторной карты, как нового объекта
# hsrc - исходный объект
# hdest - копия объекта
# В прочитанной копии объекта обнуляются порядковый номер и уникальный идентификатор на карте
# Для сохранения объекта на карте необходимо выполнить функцию
# mapCommitObject()
# При ошибке возвращает ноль

    mapCopyObjectAsNew_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyObjectAsNew', maptype.HOBJ, maptype.HOBJ)
    def mapCopyObjectAsNew(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        return mapCopyObjectAsNew_t (_hdest, _hsrc)


# Удалить описание объекта векторной карты из памяти
# hobj - идентификатор объекта карты в памяти
# Для сохранения объекта на карте необходимо
# до вызова mapFreeObject(...) выполнить функцию
# mapCommitObject(...)
# При ошибке возвращает ноль

    mapFreeObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeObject', maptype.HOBJ)
    def mapFreeObject(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapFreeObject_t (_hobj)


# Проверить, что карта объекта еще открыта
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# Если карта уже закрыта, то возвращает ноль
# При ошибке возвращает ноль

    mapIsObjectMapActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectMapActive', maptype.HMAP, maptype.HOBJ)
    def mapIsObjectMapActive(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        return mapIsObjectMapActive_t (_hmap, _hobj)


# Считать объект, который отображался последним перед возникновением сбоя отображения карт
# Применяется при аварийном завершении функций отображения векторных карт для вывода диагностической информации
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в котором будет размещен результат поиска
# Если такой объект не установлен - возвращает ноль

    mapReadLastViewObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadLastViewObject', maptype.HMAP, maptype.HOBJ)
    def mapReadLastViewObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        return mapReadLastViewObject_t (_hmap, _hobj)


# Запросить признак растягивания объекта по метрике
# Данный признак может быть установлен у подписей и векторных объектов
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsObjectStretch_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectStretch', maptype.HOBJ)
    def mapIsObjectStretch(_hobj: maptype.HOBJ) -> int:
        return mapIsObjectStretch_t (_hobj)


# Установить общие параметры системы координат документа для отображения, печати и расчета координат
# hmap  - идентификатор открытых данных (документа)
# mapreg - параметры проекции или 0
# datum - параметры датума или 0
# ellipsoid - параметры эллипсоида или 0
# type - тип локального преобразования координат (описан в TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# Структуры MAPREGISTER, DATUMPARAM и ELLIPSOIDPARAM описаны в mapcreat.h
# Устанавливать общие параметры проекции можно для документа
# поддерживающего пересчет геодезических координат (mapIsGeoSupported() != 0)
# После установки общих параметров проекции изображение карты формируется
# в заданной проекции. Векторные карты, матрицы и растры, имеющие другие параметры
# трансформируются в процессе отображения без изменения исходных данных
# Все операции с координатами (mapPlaneToGeo, mapGeoToPlane,
# mapPlaneToGeoWGS84, mapAppendPointPlane, mapInsertPointPlane,
# mapUpdatePointPlane, mapAppendPointGeo и другие) выполняются
# в системе координат документа, определяемой общими параметрами проекции
# При чтении\записи координат в конкретной карте выполняется пересчет из системы координат документа
# Например, при записи координат из WGS84 на карту в СК-42 можно
# установить общие параметры документа, как "Широта/Долгота на WGS84"
# и выполнить запись координат функцией mapAppendPointGeo, не заботясь
# о дополнительном пересчете координат, или считать координаты функцией
# mapGetGeoPoint (или функцией mapGetGeoPointWGS84, игнорирующей параметры
# документа)
# Чтобы установить текущие параметры проекции и системы координат, как у первой
# карты в документе, можно передать в качестве параметров нули (кроме hmap),
# или вызвать mapClearDocProjection
# При ошибке возвращает ноль

    mapSetDocProjectionPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetDocProjectionPro(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetDocProjectionPro_t (_hmap, _mapreg, _datum, _ellipsoid, _ttype, _tparm)


# Установить общие параметры системы координат открытых данных
# hmap - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат, создается в mapCreateUserSystemParametersPro()
# Общие параметры системы координат открытых данных применяются для отображения,
# печати и расчета координат из пользовательской системы координат
# При ошибке возвращает ноль

    mapSetDocProjectionFromUserSystem_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetDocProjectionFromUserSystem', maptype.HMAP, ctypes.c_void_p)
    def mapSetDocProjectionFromUserSystem(_hmap: maptype.HMAP, _huser: ctypes.c_void_p) -> int:
        return mapSetDocProjectionFromUserSystem_t (_hmap, _huser)

    mapClearDocProjection_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearDocProjection', maptype.HMAP)
    def mapClearDocProjection(_hmap: maptype.HMAP) -> int:
        return mapClearDocProjection_t (_hmap)


# Запросить общие параметры системы координат открытых данных
# hmap  - идентификатор открытых данных (документа)
# mapreg - параметры проекции или 0
# datum - параметры датума или 0
# ellipsoid - параметры эллипсоида или 0
# ttype  - тип локального преобразования координат (описан в TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# Структуры MAPREGISTER, DATUMPARAM и ELLIPSOIDPARAM описаны в mapcreat.h
# Если параметры не устанавливались функцией mapSetMapInfoEx,
# то они соответсвуют параметрам карты, открытой в документе первой
# При ошибке возвращает ноль

    mapGetDocProjectionPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetDocProjectionPro(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetDocProjectionPro_t (_hmap, _mapreg, _datum, _ellipsoid, _ttype, _tparm)


# Запросить, устанавливались ли общие параметры системы координат открытых данных
# hmap  - идентификатор открытых данных (документа)
# Если параметры системы координат открытых данных были изменены, то возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsDocProjection_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDocProjection', maptype.HMAP)
    def mapIsDocProjection(_hmap: maptype.HMAP) -> int:
        return mapIsDocProjection_t (_hmap)


# Установить ограничения области отображения для документа
# hmap - идентификатор открытых данных (документа)
# frame - указатель на габариты области ограничения или ноль (отменить ограничение)
# После смены ограничения на область отображения необходимо вызвать функцию mapSetRegion
# для обновления габаритов района и обновить позицию изображения карты в окне
# При ошибке возвращает ноль

    mapSetDocShowLimit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetDocShowLimit', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapSetDocShowLimit(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapSetDocShowLimit_t (_hmap, _frame)


# Запросить ограничения области отображения для документа
# hmap - идентификатор открытой основной карты
# frame - указатель на запись для получения габаритов области ограничения
# Если ограничение области отображения не установлено, то возвращает -1 и заполняет габариты документа
# При ошибке возвращает ноль

    mapGetDocShowLimit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDocShowLimit', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapGetDocShowLimit(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetDocShowLimit_t (_hmap, _frame)


# Запросить высоту общего изображения карты в пикселах для текущего масштаба
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetPictureHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPictureHeight', maptype.HMAP)
    def mapGetPictureHeight(_hmap: maptype.HMAP) -> int:
        return mapGetPictureHeight_t (_hmap)


# Запросить ширину общего изображения карты в пикселах для текущего масштаба
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetPictureWidth_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPictureWidth', maptype.HMAP)
    def mapGetPictureWidth(_hmap: maptype.HMAP) -> int:
        return mapGetPictureWidth_t (_hmap)


# Запросить размеры общего изображения карты в пикселах для текущего масштаба
# width - поле для записи ширины изображения в пикселах
# height - поле для записи высоты изображения в пикселах
# hpaint - идентификатор контекста отображения для многопоточного вызова, создается функцией mapCreatePaintControl()

    mapGetPictureSizeEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapGetPictureSizeEx', ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), maptype.HPAINT)
    def mapGetPictureSizeEx(_width: ctypes.POINTER(ctypes.c_long), _height: ctypes.POINTER(ctypes.c_long), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapGetPictureSizeEx_t (_width, _height, _hpaint)


# Запросить ширину пиксела изображения карты в метрах на местности для текущего масштаба изображения
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetPixelWidth_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetPixelWidth', maptype.HMAP)
    def mapGetPixelWidth(_hmap: maptype.HMAP) -> float:
        return mapGetPixelWidth_t (_hmap)


# Запросить высоту пиксела изображения карты в метрах на местности для текущего масштаба изображения
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetPixelHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetPixelHeight', maptype.HMAP)
    def mapGetPixelHeight(_hmap: maptype.HMAP) -> float:
        return mapGetPixelHeight_t (_hmap)


# Запросить текущее число пикселов на метр изображения - разрешение по вертикали
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetVerticalPixel_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetVerticalPixel', maptype.HMAP)
    def mapGetVerticalPixel(_hmap: maptype.HMAP) -> float:
        return mapGetVerticalPixel_t (_hmap)


# Запросить текущее число пикселов на метр изображения - разрешение по горизонтали
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetHorizontalPixel_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetHorizontalPixel', maptype.HMAP)
    def mapGetHorizontalPixel(_hmap: maptype.HMAP) -> float:
        return mapGetHorizontalPixel_t (_hmap)


# Запросить текущее число пикселов на метр изображения - разрешение по вертикали
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке возвращает ноль

    mapGetVerticalPixelEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetVerticalPixelEx', maptype.HPAINT)
    def mapGetVerticalPixelEx(_hpaint: maptype.HPAINT) -> float:
        return mapGetVerticalPixelEx_t (_hpaint)


# Запросить текущее число пикселов на метр изображения - разрешение по горизонтали
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке возвращает ноль

    mapGetHorizontalPixelEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetHorizontalPixelEx', maptype.HPAINT)
    def mapGetHorizontalPixelEx(_hpaint: maptype.HPAINT) -> float:
        return mapGetHorizontalPixelEx_t (_hpaint)


# Запретить или разрешить построение дерева объектов для отображения всех карт
# flag - признак применения дерева объектов: 0 или 1
# Построение дерева замедляет (от долей секунды до нескольких секунд) открытие
# неотсортированных карт с большим числом объектов (от нескольких сот тысяч и более),
# но ускоряет (в 1,5 - 3 раза) отображение больших карт в крупных масштабах
# Возвращает ранее установленное значение

    mapSetFrameTree_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetFrameTree', ctypes.c_long)
    def mapSetFrameTree(_flag: int) -> int:
        return mapSetFrameTree_t (_flag)


# Создать контекст потока отображения для многопоточного вызова
# hmap - идентификатор открытых данных
# Для каждого потока приложения создается свой контекст и передается в качестве параметров функций отображения или поиска
# Например: mapPaintByFramePro или mapPaintByFrameToXImagePro
# В каждом контексте создается свой буфер отображения и выделяется память под служебные области
# Размер резервируемой памяти помимо буфера отображения может занимать 1-2 Мбайта,
# внутренний буфер отображения для размера 1920x1080 занимает 8 Мбайт
# Размер может ограничиваться программно в функции mapSetMaxScreenImageSize
# После завершения использования контекст потока отображения его необходимо освободить функцией mapFreePaintControl
# При ошибке возвращает ноль

    mapCreatePaintControl_t = mapsyst.GetProcAddress(curLib,maptype.HPAINT,'mapCreatePaintControl', maptype.HMAP)
    def mapCreatePaintControl(_hmap: maptype.HMAP) -> maptype.HPAINT:
        return mapCreatePaintControl_t (_hmap)


# Создать контекст потока отображения для многопоточного вызова
# hmap - идентификатор открытых данных (документа)
# hpaint - контекст потока отображения для копирования параметров отображения и поиска или 0
# Для каждого потока приложения создается свой контекст и передается в качестве параметров функций отображения или поиска
# После завершения использования контекст потока отображения его необходимо освободить функцией mapFreePaintControl
# При ошибке возвращает ноль

    mapCreatePaintControlEx_t = mapsyst.GetProcAddress(curLib,maptype.HPAINT,'mapCreatePaintControlEx', maptype.HMAP, maptype.HPAINT)
    def mapCreatePaintControlEx(_hmap: maptype.HMAP, _hpaint: maptype.HPAINT) -> maptype.HPAINT:
        return mapCreatePaintControlEx_t (_hmap, _hpaint)


# Удалить контекст потока отображения
# hpaint - контекст потока отображения, созданный функциями mapCreatePaintControl или mapCreatePaintControlEx

    mapFreePaintControl_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreePaintControl', maptype.HPAINT)
    def mapFreePaintControl(_hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapFreePaintControl_t (_hpaint)


# Сменить идентификатор открытых данных в контексте отображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# hmap - идентификатор открытых данных (документа)
# Применяется для последовательной отрисовки в многопоточном варианте
# в буфер изображения одного контекста из нескольких HMAP для наложения слоев
# При ошибке возвращает ноль

    mapSetPaintControlMapHandle_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPaintControlMapHandle', maptype.HPAINT, maptype.HMAP)
    def mapSetPaintControlMapHandle(_hpaint: maptype.HPAINT, _hmap: maptype.HMAP) -> int:
        return mapSetPaintControlMapHandle_t (_hpaint, _hmap)


# Установить параметры системы координат документа в контексте отображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# epsgcode - код EPSG для требуемой системы координат (например, 3395, 3857, 4326)
# Применяется для установки системы координат формируемого изображения по коду EPSG
# Для геодезических систем координат возвращает 2,
# для плоских прямоугольных возвращает 1
# При ошибке возвращает ноль

    mapSetPaintControlProjection_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPaintControlProjection', maptype.HPAINT, ctypes.c_long)
    def mapSetPaintControlProjection(_hpaint: maptype.HPAINT, _epsgcode: int) -> int:
        return mapSetPaintControlProjection_t (_hpaint, _epsgcode)


# Установить параметры системы координат документа в контексте отображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения или поиска
# mapreg - параметры проекции или 0
# datum - параметры датума или 0
# ellipsoid - параметры эллипсоида или 0
# Применяется для установки системы координат формируемого изображения
# При ошибке возвращает ноль

    mapSetPaintControlProjectionEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPaintControlProjectionEx', maptype.HPAINT, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetPaintControlProjectionEx(_hpaint: maptype.HPAINT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetPaintControlProjectionEx_t (_hpaint, _mapreg, _datum, _ellipsoid)


# Установить параметры рисования объектов новыми примитивами
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# drawList - список примитивов (DRAWOBJECT) и условий их отбора для рисования объектов на карте
# Создать drawList можно с помощью функции mapCreatePaintDrawList (maprscex.h).
# Объекты, не вошедшие в список, рисуются согласно условным знакам классификатора
# Добавить объекты в список можно с помощью функции mapAppendDrawToDrawList или в автоматическом режиме
# функцией gmlCreatePaintDrawListByOgcSld (gmlapi.h)
# Параметры устанавливаются для текущего контекста рисования
# Для отключения рисования объектов новыми примитивами необходим вызов mapSetPaintControlDrawList(hPaint, 0)
# При ошибке возвращает ноль

    mapSetPaintControlDrawList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPaintControlDrawList', maptype.HPAINT, ctypes.c_void_p)
    def mapSetPaintControlDrawList(_hpaint: maptype.HPAINT, _drawList: ctypes.c_void_p) -> int:
        return mapSetPaintControlDrawList_t (_hpaint, _drawList)


# Запросить идентификатор открытых данных, для которых создан контекст отображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке возвращает ноль

    mapGetPaintControlMapHandle_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapGetPaintControlMapHandle', maptype.HPAINT)
    def mapGetPaintControlMapHandle(_hpaint: maptype.HPAINT) -> maptype.HMAP:
        return mapGetPaintControlMapHandle_t (_hpaint)


# Скопировать содержимое внутреннего буфера в заданную область
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# imagedesc - описание выходного буфера изображения
# При ошибке возвращает ноль

    mapCopyPaintControlToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyPaintControlToXImage', maptype.HPAINT, ctypes.POINTER(maptype.XIMAGEDESC))
    def mapCopyPaintControlToXImage(_hpaint: maptype.HPAINT, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC)) -> int:
        return mapCopyPaintControlToXImage_t (_hpaint, _imagedesc)


# Получить описание внутреннего буфера в виде структуры XIMAGEDESC
# hmap - идентификатор открытых данных (документа)
# imagedesc - поле для записи описания внутреннего буфера изображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или 0
# Формат хранения изображения остается: для Linux нисходящий DIB, для Windows - восходящий
# Описание буфера может измениться (увеличение размера) в процессе выполнения функций отрисовки
# В буфер будет выполнено отображение документа при вызове функций отрисовки
# с идентификатором контекста устройства (HDC) равным 0
# При ошибке возвращает ноль

    mapGetXImageDescForMapDibPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetXImageDescForMapDibPro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), maptype.HPAINT)
    def mapGetXImageDescForMapDibPro(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _hpaint: maptype.HPAINT) -> int:
        return mapGetXImageDescForMapDibPro_t (_hmap, _imagedesc, _hpaint)


# Запросить код ошибки, возникшей при рисовании
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# В случае успеха возвращает ноль, иначе код ошибки

    mapGetPaintErrorCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPaintErrorCode', maptype.HPAINT)
    def mapGetPaintErrorCode(_hpaint: maptype.HPAINT) -> int:
        return mapGetPaintErrorCode_t (_hpaint)


# Отобразить фрагмент карты и сохранить в файл png
# hmap - идентификатор открытых данных (документа)
# filename  - полное имя создаваемого файла формата png или 0
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2
# frame  - координаты фрагмента карты в системе координат документа в метрах, изменяется в mapSetDocProjection()
# width  - ширина изображения в пикселах
# height - высота изображения в пикселах
# alpha - флаг использования альфа канала: 0 - не использовать 1 - использовать
# viewselect - условия отбора отображаемых объектов, если равно 0, то применяются
#           условия обобщенного поиска\выделения (внутренние)
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Данная функция может изменять текущий масштаб отображения документа (если hPaint равен 0),
# для сохранения текущего масштаба можно применить функции mapGetRealShowScale/mapSetRealShowScale
# При ошибке возвращает ноль

    mapPaintByFrameToFilePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintByFrameToFilePro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFrameToFilePro(_hmap: maptype.HMAP, _filename: mapsyst.WTEXT, _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hpaint: maptype.HPAINT) -> int:
        return mapPaintByFrameToFilePro_t (_hmap, _filename.buffer(), _erase, _frame, _width, _height, _alpha, _viewselect, _hpaint)


# Отобразить фрагмент карты и врезки (Inset)в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2 (минус 2)
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# alpha - флаг использования альфа канала: 0 - не использовать 1 - использовать (фон прозрачный согласно значению альфа в BackColor/BackPrintColor)
# При ошибке возвращает ноль

    mapPaintDocToXImageEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintDocToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), ctypes.c_long)
    def mapPaintDocToXImageEx(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _alpha: int) -> int:
        return mapPaintDocToXImageEx_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _alpha)


# Отобразить объект в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# erase - признак предварительной очистки фона изображения: 0 - фон не стирать, 1 - очистить фрагмент цветом фона,
#         -2 - выполнить отображение поверх существующего изображения
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# image - описание вида объекта (см. MAPGDI.H), если объект должен рисоваться своим условным знаком,
#         то значение параметра можно установить в ноль
# hobj - идентификатор объекта карты в памяти
# При ошибке в параметрах возвращает ноль

    mapPaintMapObjectToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintMapObjectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapPaintMapObjectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        return mapPaintMapObjectToXImage_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _image, _hobj)


# Отобразить фрагмент карты в буфер изображения, смасштабировав до заданной ширины и высоты
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#                для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2 (минус 2))
# frame  - координаты фрагмента карты в системе координат документа в метрах
# width  - ширина изображения в пикселах
# height - высота изображения в пикселах
# alpha - флаг использования альфа канала: 0 - не использовать 1 - использовать
# viewselect - условия отбора объектов, если равны 0, то применяются условия обобщенного поиска\выделения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке в параметрах возвращает ноль

    mapPaintByFrameToXImagePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintByFrameToXImagePro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFrameToXImagePro(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hpaint: maptype.HPAINT) -> int:
        return mapPaintByFrameToXImagePro_t (_hmap, _imagedesc, _erase, _frame, _width, _height, _alpha, _viewselect, _hpaint)


# Отобразить динамические подписи карты в буфер изображения, смасштабировав до заданной ширины и высоты
# hmap  - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом: 0 - фон не стирать, !=0 - очистить фрагмент цветом фона,
#          всегда стирает цветом фона, кроме значения -2 (минус 2)
# frame - координаты фрагмента карты в системе координат документа в метрах
# width - ширина изображения в пикселах
# height - высота изображения в пикселах
# alpha - флаг использования альфа канала: 0 - не использовать (для WinGDI), 1 - использовать
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке в параметрах возвращает ноль

    mapPaintLabelsByFrameToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintLabelsByFrameToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapPaintLabelsByFrameToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _hpaint: maptype.HPAINT) -> int:
        return mapPaintLabelsByFrameToXImage_t (_hmap, _imagedesc, _erase, _frame, _width, _height, _alpha, _hpaint)


# Отобразить фрагмент карты в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2 (минус 2)
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# При ошибке в параметрах возвращает ноль

    mapPaintToXImageProL_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintToXImageProL', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), maptype.HPAINT)
    def mapPaintToXImageProL(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _hpaint: maptype.HPAINT) -> int:
        return mapPaintToXImageProL_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _hpaint)


# Отобразить объект заданным видом в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# image - описание вида объекта (структуры описаны в mapgdi.h),
# data  - координаты объекта,
# place - вид системы координат: PP_PICTURE - в точках экрана, PP_PLANE - в метрах в системе координат документа,
#         PP_GEO - в радианах на эллипсоиде документа
# При ошибке в параметрах возвращает ноль

    mapPaintUserObjectToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintUserObjectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapPaintUserObjectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapPaintUserObjectToXImage_t (_hmap, _imagedesc, _w, _h, _rect, _image, _data, _place)


# Отобразить выделенные объекты в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# hselect - условие отбора выделенных объектов
# color - цвет выделения объектов
# alpha  - флаг использования альфа канала: 0 - не использовать (для WinGDI), 1 - использовать
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2 (минус 2)
# При ошибке в параметрах возвращает ноль

    mapPaintSelectToXImageEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintSelectToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF, ctypes.c_long, maptype.HPAINT, ctypes.c_long)
    def mapPaintSelectToXImageEx(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _hselect: maptype.HSELECT, _color: maptype.COLORREF, _alpha: int, _hpaint: maptype.HPAINT, _erase: int) -> int:
        return mapPaintSelectToXImageEx_t (_hmap, _imagedesc, _w, _h, _rect, _hselect, _color, _alpha, _hpaint, _erase)


# Отобразить карту и выделенные объекты в буфер изображения, смасштабировав до заданной ширины и высоты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# imagedesc - описание выходного буфера изображения
# erase - признак стирания фона перед выводом: 0 - фон не стирать, != 0 - очистить фрагмент цветом фона,
#         для экранного способа вывода (VT_SCREEN) всегда стирает цветом фона, кроме значения -2 (минус 2)
# frame - координаты фрагмента карты в системе координат документа в метрах
# width - ширина изображения в пикселах
# height - высота изображения в пикселах
# alpha - флаг использования альфа канала: 0 - не использовать (для WinGDI), 1 - использовать
# hselect - условие отбора для выделенных объектов
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# color - цвет выделения объектов
# При ошибке в параметрах возвращает ноль

    mapPaintSelectByFrameToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintSelectByFrameToXImage', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT, maptype.COLORREF)
    def mapPaintSelectByFrameToXImage(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _hselect: maptype.HSELECT, _hpaint: maptype.HPAINT, _color: maptype.COLORREF) -> int:
        return mapPaintSelectByFrameToXImage_t (_hmap, _hsite, _imagedesc, _erase, _frame, _width, _height, _alpha, _hselect, _hpaint, _color)


# Отобразить фрагмент карты и выделенные объекты в буфер изображения в области памяти
# hmap - идентификатор открытых данных (документа)
# imagedesc - описание выходного буфера изображения
# w - положение левой верхней точки заполняемой области в буфере по ширине или 0
# h - положение левой верхней точки заполняемой области в буфере по высоте или 0
# rect - координаты фрагмента карты в изображении в пикселах
# hselect - условие отбора выделенных объектов, если равно нулю и установлено mapSetTotalSelectFlag(),
#           то применяются условия обобщенного поиска\выделения
# color - цвет, которым будут выделяться объекты на карте
# При ошибке в параметрах возвращает ноль

    mapPaintAndSelectToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintAndSelectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF)
    def mapPaintAndSelectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _hselect: maptype.HSELECT, _color: maptype.COLORREF) -> int:
        return mapPaintAndSelectToXImage_t (_hmap, _imagedesc, _w, _h, _rect, _hselect, _color)


# Вывести изображение графического объекта в файл
# hobj - идентификатор объекта карты в памяти
# width - ширина изображения в пикселах кратная 16
# height - высота изображения в пикселах
# filename - имя файла для сохранения
# transparentColor - цвет прозрачного фона
# При ошибке возвращает ноль

    mapPaintDrawObjectToFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintDrawObjectToFile', maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapPaintDrawObjectToFile(_hobj: maptype.HOBJ, _width: int, _height: int, _filename: mapsyst.WTEXT, _transparentColor: int) -> int:
        return mapPaintDrawObjectToFile_t (_hobj, _width, _height, _filename.buffer(), _transparentColor)


# Установить уровень качественного отображения подписей при печати
# mode - уровень рисования подписей:
#        0 - рисование подписи без уточнения длины (быстрое рисование)
#        1 - рисование подписи с уточнением длины (пропорционально масштабу)
#        2 - рисование подписи с уточнением длины и короткими пробелами после
#            знаков препинания и цифровых символов
# При старте программы установлен режим 1
# Возвращает предыдущее значение

    mapSetTextQuality_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetTextQuality', ctypes.c_long)
    def mapSetTextQuality(_mode: int) -> int:
        return mapSetTextQuality_t (_mode)


# Запросить значение уровня качественного отображения подписей

    mapGetTextQuality_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextQuality')
    def mapGetTextQuality() -> int:
        return mapGetTextQuality_t ()


# Запросить число элементов в списке наборов данных
# hmap - идентификатор открытых данных (документа)
# Если возвращается нулевое значение, то список отображения не активен
# При ошибке возвращает ноль

    mapGetViewListCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListCount', maptype.HMAP)
    def mapGetViewListCount(_hmap: maptype.HMAP) -> int:
        return mapGetViewListCount_t (_hmap)


# Запросить название элемента (путь к набору данных) и тип в списке наборов данных
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# itemname - указатель на буфер для записи пути к набору данных или алиаса данных
# size - размер буфера в байтах
# Возвращает один из следующих типов данных:
# FILE_MAP, FILE_RSW, FILE_MTW, FILE_MTQ, FILE_MTL, FILE_MTD, FILE_TIN, FILE_WMS
# При ошибке возвращает ноль

    mapGetViewListItemName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetViewListItemName(_hmap: maptype.HMAP, _index: int, _itemname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetViewListItemName_t (_hmap, _index, _itemname.buffer(), _size)


# Запросить тип набора данных и его порядковый номер с 1 в списке данных этого типа
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# number - поле для записи порядкового номера с 1 (применение: для FILE_RSW - mapGetRstView(hmap, #number))
# Возвращает один из следующих типов данных:
# FILE_MAP, FILE_RSW, FILE_MTW, FILE_MTQ, FILE_MTL, FILE_MTD, FILE_TIN, FILE_WMS
# При ошибке возвращает ноль

    mapGetViewListItemNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemNumber', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetViewListItemNumber(_hmap: maptype.HMAP, _index: int, _number: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetViewListItemNumber_t (_hmap, _index, _number)


# Переместить элемент в списке наборов данных в позицию перед элементом с заданным номером
# hmap - идентификатор открытых данных (документа)
# index - номер перемещаемого элемента с 1 до mapGetViewListCount()
# position - номер опорного элемента в списке с 1 до mapGetViewListCount() + 1, перед которым
#            будет размещен перемещаемый элемент
# Если position равен mapGetViewListCount() + 1, то элемент переместится в конец списка
# Если элемент перемещается к началу списка (position < index), то его новый номер
# будет равен указанному (position)
# Если элемент перемещается к концу списка (position > index + 1), то его новый номер
# будет на 1 меньше указанного, чтобы элемент встал перед опорным элементом
# Если номер опорного элемента на 1 больше номера перемещаемого элемента (position = index + 1),
# то перемещаемый элемент будет размещен за опорным элементом
# При ошибке возвращает ноль

    mapSetViewListItemPosition_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetViewListItemPosition', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemPosition(_hmap: maptype.HMAP, _index: int, _position: int) -> int:
        return mapSetViewListItemPosition_t (_hmap, _index, _position)


# Запросить идентификатор элемента в списке наборов данных
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# При ошибке возвращает ноль

    mapGetViewListItemIdent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemIdent', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemIdent(_hmap: maptype.HMAP, _index: int) -> int:
        return mapGetViewListItemIdent_t (_hmap, _index)


# Запросить номер элемента в списке наборов данных
# hmap - идентификатор открытых данных (документа)
# ident - идентификатор элемента
# Возвращает значение от 1 до mapGetViewListCount()
# При ошибке возвращает ноль

    mapGetViewListItemIndex_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemIndex', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemIndex(_hmap: maptype.HMAP, _ident: int) -> int:
        return mapGetViewListItemIndex_t (_hmap, _ident)


# Запросить GUID элемента в списке наборов данных
# hmap - идентификатор открытых данных (документа)
# ident - идентификатор элемента
# При ошибке возвращает ноль

    mapGetViewListItemGuid_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.INTQUAD),'mapGetViewListItemGuid', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemGuid(_hmap: maptype.HMAP, _ident: int) -> ctypes.POINTER(maptype.INTQUAD):
        return mapGetViewListItemGuid_t (_hmap, _ident)


# Запросить флаг отображения для элемента списка отображения
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# Если элемент не отображается возвращает ноль

    mapGetViewListItemViewFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemViewFlag', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemViewFlag(_hmap: maptype.HMAP, _index: int) -> int:
        return mapGetViewListItemViewFlag_t (_hmap, _index)


# Установить флаг отображения для элемента списка отображения
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# view - флаг отображения элемента: 0 или 1

    mapSetViewListItemViewFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetViewListItemViewFlag', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemViewFlag(_hmap: maptype.HMAP, _index: int, _view: int) -> int:
        return mapSetViewListItemViewFlag_t (_hmap, _index, _view)


# Запросить границы видимости отображения для элемента списка отображения
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# bottom - поле для записи масштаба нижней границы отображения (от 1:1)
# top - поле для записи масштаба верхней границы отображения (до 1: 250 000 000)
# При ошибке возвращает ноль

    mapGetViewListItemRangeScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListItemRangeScale', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetViewListItemRangeScale(_hmap: maptype.HMAP, _index: int, _bottom: ctypes.POINTER(ctypes.c_long), _top: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetViewListItemRangeScale_t (_hmap, _index, _bottom, _top)


# Установить границы видимости отображения для элемента списка отображения
# hmap - идентификатор открытых данных (документа)
# index - номер элемента с 1 до mapGetViewListCount()
# bottom - масштаб нижней границы отображения (от 1:1)
# top - масштаб верхней границы отображения (до 1: 250 000 000)

    mapSetViewListItemRangeScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetViewListItemRangeScale', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemRangeScale(_hmap: maptype.HMAP, _index: int, _bottom: int, _top: int) -> int:
        return mapSetViewListItemRangeScale_t (_hmap, _index, _bottom, _top)


# Запросить номер состояния списка наборов данных
# hmap - идентификатор открытых данных (документа)
# После изменения состава данных или порядка отображения номер состояния данных увеличивается
# При ошибке возвращает ноль

    mapGetViewListState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewListState', maptype.HMAP)
    def mapGetViewListState(_hmap: maptype.HMAP) -> int:
        return mapGetViewListState_t (_hmap)


# Перезаполнить список по стандартному расположению по типам наборов данных (матрицы, снимки, векторные карты)
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapResetViewList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapResetViewList', maptype.HMAP)
    def mapResetViewList(_hmap: maptype.HMAP) -> int:
        return mapResetViewList_t (_hmap)


# Включить или отключить отображение документа по общему списку данных
# hmap - идентификатор открытых данных (документа)
# viewlistaccess - признак отображения документа по общему списку данных: 0 или 1

    mapSetViewListAccess_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetViewListAccess', maptype.HMAP, ctypes.c_long)
    def mapSetViewListAccess(_hmap: maptype.HMAP, _viewlistaccess: int) -> ctypes.c_void_p:
        return mapSetViewListAccess_t (_hmap, _viewlistaccess)


# Функция настройки отображения карты с поворотом
# hmap - идентификатор открытых данных (документа)
# angle - угол поворота карты в плане с вершиной в юго-западном углу карты (от -Pi до Pi)
# fixation - угол сектора фиксации поворота отображения карты
#             относительно предыдущего положения (от 0 до Pi/6)
# Угол fixation используется для минимизации дрожания изображения
# при движении по повернутой карте по прямой (или почти по прямой),
# когда при последовательном вызове функции подаются близкие
# значения угла поворота (angle). В случае, если разность между
# текущим углом поворота и требуемым будет меньше fixation,
# то новый угол поворота не устанавливается
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Автоматически вызывает функцию mapSetRegion для обновления габаритов документа
# Возвращает значение установленного угла поворота
# При ошибке возвращает 0

    mapSetupTurn_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSetupTurn', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapSetupTurn(_hmap: maptype.HMAP, _angle: float, _fixation: float) -> float:
        return mapSetupTurn_t (_hmap, _angle, _fixation)

    mapSetupTurnEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSetupTurnEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapSetupTurnEx(_hmap: maptype.HMAP, _angle: float, _fixation: float, _hPaint: maptype.HPAINT) -> float:
        return mapSetupTurnEx_t (_hmap, _angle, _fixation, _hPaint)


# Запросить, установлен ли поворот
# hmap - идентификатор открытых данных (документа)
# Возвращает: 1 - активен, 0 - нет

    mapTurnIsActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTurnIsActive', maptype.HMAP)
    def mapTurnIsActive(_hmap: maptype.HMAP) -> int:
        return mapTurnIsActive_t (_hmap)


# Запросить угол поворота
# hmap - идентификатор открытых данных (документа)
# Возвращает значение от -Pi до Pi

    mapGetTurnAngle_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetTurnAngle', maptype.HMAP)
    def mapGetTurnAngle(_hmap: maptype.HMAP) -> float:
        return mapGetTurnAngle_t (_hmap)


# Установить масштаб отображения
# hmap - идентификатор открытых данных (документа)
# wx - координата x в пикселах по горизонтали любой точки привязки в текущем масштабе или 0
# hy - координата y в пикселах по вертикали любой точки привязки в текущем масштабе или 0
# scale - реальный масштаб отображения, который желают получить
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Возвращает: 0 - масштаб не изменился, 1 - масштаб изменился
# Координаты в пикселах обновляются с учетом изменения маштаба
# При изменении масштаба отображения меняются общие габариты изображения в пикселах
# При ошибке возвращает ноль

    mapSetRealScalePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetRealScalePro', maptype.HMAP, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_double, maptype.HPAINT)
    def mapSetRealScalePro(_hmap: maptype.HMAP, _wx: ctypes.POINTER(ctypes.c_long), _hy: ctypes.POINTER(ctypes.c_long), _scale: float, _hpaint: maptype.HPAINT) -> int:
        return mapSetRealScalePro_t (_hmap, _wx, _hy, _scale, _hpaint)


# Запросить масштаб отображения контекста отображения
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Возвращает значение знаменателя масштаба
# При ошибке возвращает 1

    mapGetRealScalePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetRealScalePro', maptype.HPAINT)
    def mapGetRealScalePro(_hpaint: maptype.HPAINT) -> float:
        return mapGetRealScalePro_t (_hpaint)


# Установить масштаб отображения (знаменатель масштаба)
# hmap - идентификатор открытых данных (документа)
# scale - реальный масштаб отображения, который желают получить
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# horpix - число пикселов в метре по горизонтали или 0
# verpix - число пикселов в метре по вертикали или 0
# wmsscaleflag - признак выполнения согласования масштаба с масштабом геопортала (уровнями отображения)
# Возвращает: 0 - масштаб не изменился, 1 - масштаб изменился

    mapSetRealScalePrint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetRealScalePrint', maptype.HMAP, ctypes.c_double, maptype.HPAINT, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapSetRealScalePrint(_hmap: maptype.HMAP, _scale: float, _hpaint: maptype.HPAINT, _horpix: ctypes.POINTER(ctypes.c_double), _verpix: ctypes.POINTER(ctypes.c_double), _wmsscaleflag: int) -> int:
        return mapSetRealScalePrint_t (_hmap, _scale, _hpaint, _horpix, _verpix, _wmsscaleflag)


# Запросить масштаб отображения карты
# hmap - идентификатор открытых данных (документа)
# Возвращает значение знаменателя масштаба

    mapGetRealShowScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetRealShowScale', maptype.HMAP)
    def mapGetRealShowScale(_hmap: maptype.HMAP) -> float:
        return mapGetRealShowScale_t (_hmap)


# Установить масштаб отображения карты
# hmap - идентификатор открытых данных (документа)
# scale - реальный масштаб отображения, который желают получить
# Возвращает значение знаменателя масштаба

    mapSetRealShowScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSetRealShowScale', maptype.HMAP, ctypes.c_double)
    def mapSetRealShowScale(_hmap: maptype.HMAP, _scale: float) -> float:
        return mapSetRealShowScale_t (_hmap, _scale)


# Запросить текущий коэффициент масштабирования карты
# hmap - идентификатор открытых данных (документа)
# Например: 5 - растянута в 5 раз относительно базового масштаба,
#         0.1 - сжата в 10 раз.

    mapGetDrawScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetDrawScale', maptype.HMAP)
    def mapGetDrawScale(_hmap: maptype.HMAP) -> float:
        return mapGetDrawScale_t (_hmap)


# Подобрать "стандартный" реальный масштаб, ближайший к заданному (scale)
# hmap - идентификатор открытых данных (документа)
# scale - масштаб отображения, который желают получить
# Масштаб подбираетсмя с учетом состава открытых данных, например WMTS могут быть
# другие стандартные масштабы
# Возвращает новое реальное (неокругленное) значение знаменателя масштаба

    mapScaleToRoundScaleReal_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapScaleToRoundScaleReal', maptype.HMAP, ctypes.c_double)
    def mapScaleToRoundScaleReal(_hmap: maptype.HMAP, _scale: float) -> float:
        return mapScaleToRoundScaleReal_t (_hmap, _scale)


# Установить способ масштабирования объектов карты при отображении
# method - способ масштабирования: 0 - картографический "с запаздыванием увеличения", 1 - чертежный
# Возвращает ранее установленное значение

    mapSetScaleMethod_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetScaleMethod', ctypes.c_long)
    def mapSetScaleMethod(_method: int) -> int:
        return mapSetScaleMethod_t (_method)


# Запросить способ масштабирования объектов карты при отображении
# Возвращает ранее установленное значение

    mapGetScaleMethod_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetScaleMethod')
    def mapGetScaleMethod() -> int:
        return mapGetScaleMethod_t ()


# Установить отображение объектов карт без учета границ видимости и состава
# flag - признак установки флага: 1 - установить, 0 - сбросить
# Доступно только в составе ГИС
# Возвращает ранее установленное значение

    mapShowAllObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapShowAllObjects', ctypes.c_long)
    def mapShowAllObjects(_flag: int) -> int:
        return mapShowAllObjects_t (_flag)


# Запросить флаг отображение объектов карт без учета границ видимости и состава
# Доступно только в составе ГИС
# Возвращает ранее установленное значение в mapShowAllObjects()

    mapIsShowAllObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsShowAllObjects')
    def mapIsShowAllObjects() -> int:
        return mapIsShowAllObjects_t ()


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

    mapCreateImageEx_t = mapsyst.GetProcAddress(curLib,maptype.HIMAGE,'mapCreateImageEx', ctypes.c_long, ctypes.c_long)
    def mapCreateImageEx(_width: int, _height: int) -> maptype.HIMAGE:
        return mapCreateImageEx_t (_width, _height)


# Удалить буфер образа окна карты
# himage - идентификатор буфера окна

    mapCloseImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseImage', maptype.HIMAGE)
    def mapCloseImage(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseImage_t (_himage)


# Удалить буфер выделенных объектов в буфере образа окна карты
# himage - идентификатор буфера образа окна карты
# После удаления буфера выделенных объектов необходимо перерисовать буфер
# объектов, если он был открыт

    mapCloseTotalSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseTotalSelect', maptype.HIMAGE)
    def mapCloseTotalSelect(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseTotalSelect_t (_himage)


# Удалить буфер объектов в буфере образа окна карты для ускорения отображения
# himage - идентификатор буфера образа окна карты

    mapCloseObjectsImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseObjectsImage', maptype.HIMAGE)
    def mapCloseObjectsImage(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        return mapCloseObjectsImage_t (_himage)


# Запросить - открыт ли буфер объектов
# himage - идентификатор буфера образа окна карты

    mapIsObjectsImageActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectsImageActive', maptype.HIMAGE)
    def mapIsObjectsImageActive(_himage: maptype.HIMAGE) -> int:
        return mapIsObjectsImageActive_t (_himage)


# Обновить размеры буфера образа окна карты
# himage - идентификатор буфера образа окна карты
# erase  - признак очистки окна, если равен 0 - содержимое сохраняется
# width  - новая ширина буфера
# height - новая высота буфера
# При ошибке возвращает ноль

    mapChangeImageSizeEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeImageSizeEx', maptype.HIMAGE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapChangeImageSizeEx(_himage: maptype.HIMAGE, _erase: int, _width: int, _height: int) -> int:
        return mapChangeImageSizeEx_t (_himage, _erase, _width, _height)


# Очистить буфер образа окна карты
# himage - идентификатор буфера образа окна карты
# При ошибке во входных параметрах возвращает ноль

    mapClearMapImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearMapImage', maptype.HIMAGE)
    def mapClearMapImage(_himage: maptype.HIMAGE) -> int:
        return mapClearMapImage_t (_himage)


# Очистить буфер объектов в буфере образа окна карты
# himage - идентификатор буфера образа окна карты
# rect - область очистки или ноль (очистить весь буфер)

    mapClearObjectsImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearObjectsImage', maptype.HIMAGE, ctypes.POINTER(maptype.RECT))
    def mapClearObjectsImage(_himage: maptype.HIMAGE, _rect: ctypes.POINTER(maptype.RECT)) -> ctypes.c_void_p:
        return mapClearObjectsImage_t (_himage, _rect)


# Запросить ширину буфера образа окна карты
# himage - идентификатор буфера образа окна карты
# При ошибке во входные параметрах возвращает ноль

    mapGetImageWidth_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetImageWidth', maptype.HIMAGE)
    def mapGetImageWidth(_himage: maptype.HIMAGE) -> int:
        return mapGetImageWidth_t (_himage)


# Запросить высоту буфера образа окна карты
# himage - идентификатор буфера образа окна карты
# При ошибке во входные параметрах возвращает ноль

    mapGetImageHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetImageHeight', maptype.HIMAGE)
    def mapGetImageHeight(_himage: maptype.HIMAGE) -> int:
        return mapGetImageHeight_t (_himage)


# Отобразить содержимое буфера образа окна карты в заданный контекст
# himage - идентификатор буфера образа окна карты
# hdc - контекст области отображения (окна),
# rect - координаты область отображения в буфере и контексте
# При ошибке возвращает ноль

    mapViewImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapViewImage', maptype.HIMAGE, maptype.HDC, ctypes.POINTER(maptype.RECT))
    def mapViewImage(_himage: maptype.HIMAGE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        return mapViewImage_t (_himage, _hdc, _rect)


# Отобразить содержимое буфера в заданный внешний XImage
# himage - идентификатор буфера образа окна карты
# imagedesc - описание выходного буфера изображения
# rect - прямоугольник исходного изображения для копирования, если = 0 - используется размер всего буфера
# offset - верхняя левая точка области отображения в буфере, если = 0 - копируется с координатами 0, 0
# При ошибке возвращает ноль

    mapViewImageToXImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapViewImageToXImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapViewImageToXImage(_himage: maptype.HIMAGE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        return mapViewImageToXImage_t (_himage, _imagedesc, _rect, _offset)


# Отобразить в буфер объектов содержимое внешнего XImage
# himage - идентификатор буфера образа окна карты
# imagedesc - описание входного буфера изображения
# rect - прямоугольник исходного изображения для копирования, если = 0 - используется размер всего буфера
# offset - точка для размещения прямоугольника в буфере объектов, если = 0 - копируется с координатами {0, 0}
# При ошибке возвращает ноль

    mapCopyXImageToImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyXImageToImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapCopyXImageToImage(_himage: maptype.HIMAGE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        return mapCopyXImageToImage_t (_himage, _imagedesc, _rect, _offset)


# Скроллинг буфера образа окна карты
# himage - идентификатор буфера образа окна карты
# dx     - величина смещения окна по горизонтали (> 0 - слева направо, < 0 - справа налево)
# dy     - величина смещения окна по вертикали   (> 0 - сверху вниз, < 0 - снизу вверх)
# При ошибке возвращает ноль

    mapScrollImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapScrollImage', maptype.HIMAGE, ctypes.c_long, ctypes.c_long)
    def mapScrollImage(_himage: maptype.HIMAGE, _dx: int, _dy: int) -> int:
        return mapScrollImage_t (_himage, _dx, _dy)


# Очистка буфера образа окна карты заданным цветом
# himage - идентификатор буфера образа окна карты
# rect - прямоугольник изображения для очистки
# color- цвет, которым будет выполнена очистка
# При ошибке возвращает ноль

    mapClearScreenRect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearScreenRect', maptype.HIMAGE, ctypes.POINTER(maptype.RECT), maptype.COLORREF)
    def mapClearScreenRect(_himage: maptype.HIMAGE, _rect: ctypes.POINTER(maptype.RECT), _color: maptype.COLORREF) -> int:
        return mapClearScreenRect_t (_himage, _rect, _color)


# Обновить изображение заданного фрагмента карты в буфере образа окна карты
# himage - идентификатор буфера образа окна карты
# hmap - идентификатор открытых данных (документа)
# rect - обновляемый фрагмент карты, задается в пикселах в системе координат полного изображения карты (PICTURE)
# position - положение верхнего левого угла фрагмента в клиентской области окна карты (и образа экрана) или 0
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# После обновления карты изображение перемещаемых объектов стирается
# в пределах заданного фрагмента (для стирания объектов текущим видом карты достаточно вызвать mapClearObjectsImage)
# При ошибке возвращает ноль

    mapDrawImageMapPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageMapPro', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(maptype.POINT), maptype.HPAINT)
    def mapDrawImageMapPro(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _rect: ctypes.POINTER(maptype.LRECT), _position: ctypes.POINTER(maptype.POINT), _hpaint: maptype.HPAINT) -> int:
        return mapDrawImageMapPro_t (_himage, _hmap, _rect, _position, _hpaint)


# Отобразить объект поверх карты местности в буфере объектов образа окна карты
# himage - идентификатор буфера образа окна карты
# hmap - идентификатор открытых данных (документа)
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# hobj - идентификатор описания объекта в памяти
# При ошибке возвращает ноль

    mapDrawImageMapObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageMapObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        return mapDrawImageMapObject_t (_himage, _hmap, _parm, _hobj)


# Отобразить объект поверх карты местности в буфере объектов образа окна карты c учетом сдвига
# himage - идентификатор буфера образа окна карты
# hmap - идентификатор открытых данных (документа)
# offset - величина смещения изображения объекта в буфере от его реальных
#          координат в метрах в текущей системе координат документа
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# hobj - идентификатор описания объекта в памяти
# При ошибке возвращает ноль

    mapDrawImageOffsetMapObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageOffsetMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageOffsetMapObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        return mapDrawImageOffsetMapObject_t (_himage, _hmap, _offset, _parm, _hobj)


# Отобразить объект поверх карты местности в буфере образа окна карты
# himage - идентификатор буфера образа окна карты
# hmap - идентификатор открытых данных (документа)
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# data - список координат объекта в системе координат, заданной параметром place
# place - вид системы координат: PP_PICTURE - в точках экрана, PP_PLANE - в метрах в
#         системе координат документа, PP_GEO - в радианах на эллипсоиде документа
# При ошибке возвращает ноль

    mapDrawImageUserObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapDrawImageUserObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapDrawImageUserObject_t (_himage, _hmap, _parm, _data, _place)


# Отобразить объект поверх карты местности в буфере образа окна карты c учетом сдвига
# himage - идентификатор буфера образа окна карты
# hmap - идентификатор открытых данных (документа)
# offset - величина смещения изображения объекта в буфере от его реальных
#          координат в системе координат, заданной параметром place
# parm - параметры отображения объекта карты в буфере экрана (второй буфер)
# data - список координат объекта в системе координат, заданной параметром place
# place - вид системы координат (в точках экрана - PP_PICTURE, в метрах в
#         системе координат документа - PP_PLANE, в радианах на эллипсоиде документа - PP_GEO)
# При ошибке возвращает ноль

    mapDrawImageOffsetUserObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageOffsetUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapDrawImageOffsetUserObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        return mapDrawImageOffsetUserObject_t (_himage, _hmap, _offset, _parm, _data, _place)


# Отобразить графические данные в буфере образа окна карты
# himage - идентификатор буфера образа окна карты
# hScreen - идентификатор образа экрана
# points - координаты в пикселах
# count - число координат
# type - тип графического примитива (см. mapgdi.h)
# parm - параметры графического примитива
# При ошибке возвращает ноль

    mapDrawImageGraphics_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageGraphics', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapDrawImageGraphics(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _type: int, _parm: ctypes.c_char_p) -> int:
        return mapDrawImageGraphics_t (_himage, _hmap, _points, _count, _type, _parm)


# Отобразить текстовую строку
# himage - идентификатор буфера образа окна карты
# points - координаты в пикселах
# count - число координат
# text - текст подписи
# height - высота подписи в мкм
# color - цвет подписи RGB
# align - флажки выравнивания текста (для -1 - FA_BASELINE|FA_LEFT)
# При ошибке возвращает ноль

    mapDrawImageTextUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageTextUn', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDrawImageTextUn(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _text: mapsyst.WTEXT, _height: int, _color: int, _align: int) -> int:
        return mapDrawImageTextUn_t (_himage, _hmap, _points, _count, _text.buffer(), _height, _color, _align)


# Отобразить BMP в образ экрана
# himage - идентификатор буфера образа окна карты
# point     - координаты в пикселах
# bmpmemory - адрес массива байт, содержащего образ BMP-файла
# transparent - цвет RGB, который не должен отображаться
# При ошибке возвращает ноль

    mapDrawImageBitMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImageBitMap', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_char_p, ctypes.c_long)
    def mapDrawImageBitMap(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DRAWPOINT), _bmpmemory: ctypes.c_char_p, _transparent: int) -> int:
        return mapDrawImageBitMap_t (_himage, _hmap, _point, _bmpmemory, _transparent)


# Включить отображение выделенных объектов и обновить буфер выделенных объектов
# himage - идентификатор буфера образа окна карты
# image     - идентификатор образа экрана
# selectcolor - цвет выделения объектов на фоне карты (RGB)
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или 0
# При дальнешем обновлении буфера карты (Map) буфер выделенных объектов будет тоже обновляться
# Если выделение объектов не установлено (mapGetTotalSelectFlag() возвращает ноль) -
# буфер выделенных объектов автоматически закроется, а функия отображения вернет ноль
# При ошибке возвращает ноль

    mapDrawTotalSelectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawTotalSelectEx', maptype.HIMAGE, maptype.HMAP, ctypes.c_long, maptype.HPAINT)
    def mapDrawTotalSelectEx(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _selectcolor: int, _hpaint: maptype.HPAINT) -> int:
        return mapDrawTotalSelectEx_t (_himage, _hmap, _selectcolor, _hpaint)


# Включить отображение динамических подписей и обновить буфер выделенных объектов
# himage - идентификатор буфера образа окна карты
# image - идентификатор образа экрана
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или 0
# При дальнешем обновлении буфера карты (Map) буфер выделенных объектов будет тоже обновляться
# Если отображение подписей не установлено (mapGetLabelingState) возвращает ноль) -
# буфер выделенных объектов автоматически закроется, а функия отображения вернет ноль
# При ошибке возвращает ноль

    mapDrawLabels_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawLabels', maptype.HIMAGE, maptype.HMAP, maptype.HPAINT)
    def mapDrawLabels(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _hpaint: maptype.HPAINT) -> int:
        return mapDrawLabels_t (_himage, _hmap, _hpaint)


# Запросить базовый масштаб документа
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetMapScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapScale', maptype.HMAP)
    def mapGetMapScale(_hmap: maptype.HMAP) -> int:
        return mapGetMapScale_t (_hmap)


# Запросить название карты
# hmap - идентификатор открытых данных (документа)
# name - указатель на буфер для записи названия
# size - размер буфера в байтах
# При ошибке возвращает пустую строку

    mapGetMapNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapNameUn_t (_hmap, _name.buffer(), _size)


# Запросить полный путь к паспорту главной карты
# hmap - идентификатор открытых данных (документа)
# name - указатель на буфер для записи пути
# size - размер буфера в байтах
# При ошибке возвращает 0

    mapGetMapPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapPathUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapPathUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapPathUn_t (_hmap, _name.buffer(), _size)


# Запросить паспортные данные векторной карты
# hmap - идентификатор открытых данных (документа)
# sheetnumber - номер листа карты, для которого запрашиваются паспортные данные
# mapreg - заполняемая структура параметров системы координат карты
# listreg - параметры листа многолистовой карты или 0
# sheetnames - название листа карты, номенклатуры и файлов даных (для многолистовой карты) или 0
# Структуры MAPREGISTER, LISTREGISTER и SHEETNAMES описаны в mapcreat.h
# При ошибке возвращает ноль

    mapGetMapInfoPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapInfoPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapGetMapInfoPro(_hmap: maptype.HMAP, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        return mapGetMapInfoPro_t (_hmap, _sheetnumber, _mapreg, _listreg, _sheetnames)


# Запросить паспортные данные векторной карты по имени файла - паспорта карты
# name - имя файла паспорта карты (MAP,SIT,SITX)
# sheetnumber - номер листа карты, для которого запрашиваются паспортные данные
# mapreg - заполняемая структура параметров системы координат карты
# listreg - параметры листа многолистовой карты или 0
# metainfo - указатель на структуру для записи метаданных листа карты
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# При ошибке возвращает ноль, иначе - число объектов на листе карты (если нет объектов, то возвращает -1)

    mapGetMapInfoByNameMeta_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapInfoByNameMeta', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.METAINFO))
    def mapGetMapInfoByNameMeta(_name: mapsyst.WTEXT, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _metainfo: ctypes.POINTER(mapcreat.METAINFO)) -> int:
        return mapGetMapInfoByNameMeta_t (_name.buffer(), _sheetnumber, _mapreg, _listreg, _metainfo)


# Контроль номенклатуры карты
# nomenclature - строка с номенклатурой
# length - длина строки
# type - тип карты (из MAPTYPE)
# scale - знаменатель масштаба, соответствующий типу карты
# Возвращает масштаб карты
# При ошибке возвращает ноль

    mapCheckNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckNomenclatureUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapCheckNomenclatureUn(_nomenclature: mapsyst.WTEXT, _type: int, _scale: int) -> int:
        return mapCheckNomenclatureUn_t (_nomenclature.buffer(), _type, _scale)


# Формирование имени файла по номенклатуре (удаляет точки, пробелы, -)
# filename - буфер для имени файла
# namesize - размер буфера в байтах
# nomenclature - номенклатура листа
# Формирование имени удаляет точки, пробелы, тире
# При ошибке возвращает ноль

    mapSetFileNameFromNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetFileNameFromNomenclatureUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def mapSetFileNameFromNomenclatureUn(_filename: mapsyst.WTEXT, _namesize: int, _nomenclature: mapsyst.WTEXT) -> int:
        return mapSetFileNameFromNomenclatureUn_t (_filename.buffer(), _namesize, _nomenclature.buffer())


# Расчет данных на лист топографической карты
# hmap - идентификатор открытых данных (документа) или ноль
# mapreg - заполняемая структура параметров системы координат карты
# listreg - параметры листа многолистовой карты или 0
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# Входные данные заполняются в mapreg: тип карты, масштаб, в listreg - номенклатура
# Выходные данные заполняются в mapreg: осевой меридиан,
# в listreg: геодезические координаты, прямоугольные координаты, сближение меридианов
# Если mapreg и listreg заполняются для создания карты (самый первый лист), то hmap равно 0
# Если mapreg заполняется для добавления листа в карту, то hmap не равно 0
# При ошибке возвращает ноль

    mapCalcTopographicSheetEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCalcTopographicSheetEx', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapCalcTopographicSheetEx(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        return mapCalcTopographicSheetEx_t (_hmap, _mapreg, _listreg)


# Рассчитать осевой меридиан (от 0 до 360) по номенклатуре топокарты
# type - тип карты: CK_42, CK_95, GCK_2011, Pulkovo2017 ...
# nomenclature - номенклатура листа
# При ошибке возвращает ноль

    mapGetAxisMeridianFromNomenclatureEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetAxisMeridianFromNomenclatureEx', ctypes.c_long, ctypes.c_char_p)
    def mapGetAxisMeridianFromNomenclatureEx(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        return mapGetAxisMeridianFromNomenclatureEx_t (_type, _nomenclature)


# Рассчитать масштаб топокарты по номенклатуре (от 1 : 10 000 до 1 : 1 000 000)
# type - тип карты: CK_42, CK_95, GCK_2011, Pulkovo2017 или 0
# nomenclature - номенклатура листа
# При ошибке возвращает ноль

    mapGetTopoScaleByNomenclature_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetTopoScaleByNomenclature', ctypes.c_long, ctypes.c_char_p)
    def mapGetTopoScaleByNomenclature(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        return mapGetTopoScaleByNomenclature_t (_type, _nomenclature)


# Рассчитать осевой меридиан топокарты по долготе

    mapGetAxisMeridian_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetAxisMeridian', ctypes.c_double)
    def mapGetAxisMeridian(_longitude: float) -> float:
        return mapGetAxisMeridian_t (_longitude)


# Запросить признак повышенной точности хранения координат
# hmap - идентификатор открытых данных (документа)
# Возвращает значения:
#     1 - максимальная точность хранения (метры или радианы),
#     2 - с точностью 2 знака (сантиметры),
#     3 - с точностью 3 знака (миллиметры)
# При ошибке или нормальной точности хранения координат возвращает ноль

    mapGetMapPrecision_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapPrecision', maptype.HMAP)
    def mapGetMapPrecision(_hmap: maptype.HMAP) -> int:
        return mapGetMapPrecision_t (_hmap)


# Запросить количество эллипсоидов в списке

    mapGetEllipsoidCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidCount')
    def mapGetEllipsoidCount() -> int:
        return mapGetEllipsoidCount_t ()


# Запросить название эллипсоида по коду
# code - код эллипсоида
# name - адрес строки для размещения названия эллипсоида
# size - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает ноль, name содержит значение "Не установлено"

    mapGetEllipsoidNameByCodeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetEllipsoidNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetEllipsoidNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия эллипсоида по номеру в таблице
# number - номер строки таблицы эллипсоидов с 1
# code - код эллипсоида
# name - адрес строки для размещения названия эллипсоида
# size - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает ноль

    mapGetEllipsoidByNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetEllipsoidByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetEllipsoidByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запросить по коду EPSG номер эллипсоида
# code - код EPSG
# При ошибке возвращает ноль

    mapGetEllipsoidByEPSGCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidByEPSGCode', ctypes.c_long)
    def mapGetEllipsoidByEPSGCode(_code: int) -> int:
        return mapGetEllipsoidByEPSGCode_t (_code)


# Запросить код EPSG эллипсоида по его коду
# ellipsoid - номер эллипсоида с 1 (ELLIPSOIDKIND)
# При ошибке возвращает ноль

    mapGetEllipsoidEPSGCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidEPSGCode', ctypes.c_long)
    def mapGetEllipsoidEPSGCode(_code: int) -> int:
        return mapGetEllipsoidEPSGCode_t (_code)


# Запрос количества типов карт в списке

    mapGetMapTypeCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapTypeCount')
    def mapGetMapTypeCount() -> int:
        return mapGetMapTypeCount_t ()


# Запрос названия типа карты по коду
# code - код типа карты
# name - адрес строки для размещения названия типа карты
# size - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает ноль

    mapGetMapTypeByCodeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapTypeByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapTypeByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapTypeByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия типа карты по номеру в таблице
# number - номер строки таблицы типа карты с 1
# code - код типа карты
# name - адрес строки для размещения названия типа карты
# size - длина выделенной области под строку в байтах
# При ошибке возвращает ноль

    mapGetMapTypeByNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapTypeByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetMapTypeByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapTypeByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запрос количества проекций в списке
# При ошибке возвращает ноль

    mapGetProjectionCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProjectionCount')
    def mapGetProjectionCount() -> int:
        return mapGetProjectionCount_t ()


# Запрос названия проекции по коду
# code - код проекции
# name - адрес строки для размещения названия проекции
# size - длина выделенной области под строку в байтах
# При ошибке возвращает ноль, name содержит значение "Не установлено"

    mapGetProjectionNameByCodeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProjectionNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectionNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetProjectionNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия проекции по номеру в таблице
# number - номер строки таблицы проекций с 1
# code - код проекции
# name - адрес строки для размещения названия проекции
# size - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает ноль

    mapGetProjectionByNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetProjectionByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectionByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetProjectionByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запрос количества систем высот в списке

    mapGetHeightSystemCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetHeightSystemCount')
    def mapGetHeightSystemCount() -> int:
        return mapGetHeightSystemCount_t ()


# Запрос названия системы высот по коду
# code - код системы высот
# name - адрес строки для размещения названия системы высот
# size - длина выделенной области под строку в байтах
# При ошибке возвращает ноль, name содержит значение "Не установлено"

    mapGetHeightSystemNameByCodeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetHeightSystemNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetHeightSystemNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetHeightSystemNameByCodeUn_t (_code, _name.buffer(), _size)


# Запрос кода и названия системы высот по номеру в таблице
# number - номер строки таблицы систем высот с 1
# code - код системы высот
# name - адрес строки для размещения названия проекции
# size - длина выделенной области под строку в БАЙТАХ
# При ошибке возвращает ноль

    mapGetHeightSystemByNumberUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetHeightSystemByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetHeightSystemByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetHeightSystemByNumberUn_t (_number, _code, _name.buffer(), _size)


# Запросить число слоев на карте
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetLayerCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLayerCount', maptype.HMAP)
    def mapGetLayerCount(_hmap: maptype.HMAP) -> int:
        return mapGetLayerCount_t (_hmap)


# Запросить название слоя по его номеру
# hmap - идентификатор открытых данных (документа)
# number - номер слоя с 0
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# Номер первого слоя равен 0
# При ошибке возвращает ноль

    mapGetLayerNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLayerNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetLayerNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetLayerNameUn_t (_hmap, _number, _name.buffer(), _size)


# Определить номер листа в точке по координатам
# hmap - идентификатор открытых данных (документа)
# number - порядковый номер листа в перекрытии (начина с 1).
# place - вид системы координат: PP_PICTURE - в точках экрана, PP_PLANE - в метрах в системе координат документа,
#         PP_GEO - в радианах на эллипсоиде документа
# Если в одной точке несколько листов, то для их перебора значение параметра number увеличивается на 1
# Поиск всегда дает одинаковый порядок листов
# Если лист не найден - возвращает ноль
# При ошибке возвращает ноль

    mapWhatListNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWhatListNumber', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapWhatListNumber(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int) -> int:
        return mapWhatListNumber_t (_hmap, _x, _y, _number, _place)


# Запросить номенклатуру листа по заданным координатам
# hmap - идентификатор открытых данных (документа)
# x, y - координаты точки в метрах в системе документа
# number - номер листа в списке найденных, который нужно вернуть (если точка в габаритах нескольких листов)
# place - cистема координат (пикселы, метры, радианы)
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# Если лист не найден - возвращает ноль

    mapWhatListNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWhatListNameUn', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapWhatListNameUn(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapWhatListNameUn_t (_hmap, _x, _y, _number, _place, _name.buffer(), _size)


# Запросить имя листа по его номеру (number)
# hmap - идентификатор открытых данных (документа)
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetSheetNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSheetNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSheetNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetSheetNameUn_t (_hmap, _number, _name.buffer(), _namesize)


# Запросить номенклатуру листа по его номеру (number)
# Для топокарт номенклатура листа не совпадает с названием листа
# hmap - идентификатор открытых данных (документа)
# name - адрес буфера для результата запроса
# size - размер буфера
# При ошибке возвращает ноль

    mapGetNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetNomenclatureUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetNomenclatureUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetNomenclatureUn_t (_hmap, _number, _name.buffer(), _size)


# Запросить общее число листов в районе
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetListCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetListCount', maptype.HMAP)
    def mapGetListCount(_hmap: maptype.HMAP) -> int:
        return mapGetListCount_t (_hmap)


# Запросить общее число объектов в листе
# hmap - идентификатор открытых данных (документа)
# list - номер листа
# При ошибке возвращает ноль

    mapGetObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectCount', maptype.HMAP, ctypes.c_long)
    def mapGetObjectCount(_hmap: maptype.HMAP, _list: int) -> int:
        return mapGetObjectCount_t (_hmap, _list)


# Запросить общее число объектов в листе, исключая удаленные
# hmap - идентификатор открытых данных (документа)
# number - номер листа
# При ошибке возвращает ноль

    mapGetRealObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetRealObjectCount', maptype.HMAP, ctypes.c_long)
    def mapGetRealObjectCount(_hmap: maptype.HMAP, _number: int) -> int:
        return mapGetRealObjectCount_t (_hmap, _number)


# Запросить номер листа по его номенклатуре
# hmap - идентификатор открытых данных (документа)
# name - имя листа
# При ошибке возвращает ноль

    mapGetListNumberByNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetListNumberByNomenclatureUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetListNumberByNomenclatureUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetListNumberByNomenclatureUn_t (_hmap, _name.buffer())


# Определить по номенклатуре листа его принадлежность карте
# hmap - идентификатор открытых данных (документа)
# listname - имя листа (номенклатура)
# Возвращает номер карты в цепочке карт, которой принадлежит лист по имени listname:
#      0 - фоновая карта, 1 - первая пользовательская карта и так далее
# При ошибке возвращает "-1"

    mapWhatListLayoutIsUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWhatListLayoutIsUn', maptype.HMAP, maptype.PWCHAR)
    def mapWhatListLayoutIsUn(_hmap: maptype.HMAP, _listname: mapsyst.WTEXT) -> int:
        return mapWhatListLayoutIsUn_t (_hmap, _listname.buffer())


# Запросить объект "Рамка листа"
# hmap - идентификатор открытых данных (документа)
# list - номер листа c 1
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetListFrameObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetListFrameObject', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetListFrameObject(_hmap: maptype.HMAP, _list: int, _hobj: maptype.HOBJ) -> int:
        return mapGetListFrameObject_t (_hmap, _list, _hobj)


# Запросить габариты объекта "Рамка листа"
# hmap  - идентификатор открытых данных (документа)
# list  - номер листа с 1
# frame - указатель на габариты листа в метрах
# Если рамки нет габариты заполняются по метаданным из паспорта
# При ошибке возвращает ноль

    mapGetListFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetListFrame', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapGetListFrame(_hmap: maptype.HMAP, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetListFrame_t (_hmap, _list, _frame)


# Создать объект "Рамка листа"
# hmap - идентификатор открытых данных (документа)
# list - последовательный номер листа карты c 1
# hobj - идентификатор объекта карты в памяти
# HOBJ должен быть создан вызовом mapCreateObject
# При успешном выполнении HOBJ будет содержать созданную
# или существующую рамку листа
# Для пользовательской карты (SIT, SITX) рамка создается, но не записывается
# Для многолистовой карты (MAP) созданная рамка сохраняется на карте
# При ошибке возвращает ноль

    mapCreateListFrameObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateListFrameObject', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapCreateListFrameObject(_hmap: maptype.HMAP, _list: int, _hobj: maptype.HOBJ) -> int:
        return mapCreateListFrameObject_t (_hmap, _list, _hobj)


# Установить ограничение на число листов, открытых одновременно
# hmap - идентификатор открытых данных (документа)
# islimited - признак установки ограничения числа открытых листов,
# обычно от 8 до 32, но не менее числа потоков, обрабатывающих листы параллельно
# Применяется при работе с многолистовыми картами местности в
# ограниченной области памяти
# При ошибке возвращает ноль

    mapSetActiveListCountLimit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetActiveListCountLimit', maptype.HMAP, ctypes.c_long)
    def mapSetActiveListCountLimit(_hmap: maptype.HMAP, _islimited: int = 32) -> int:
        return mapSetActiveListCountLimit_t (_hmap, _islimited)


# Установить ограничение на размер используемой памяти
# hmap - идентификатор открытых данных (документа)
# limit - размер разрешенной к использованию памяти
# Применяется при работе с большими многолистовыми картами
# Если лимит больше доступной приложению памяти, устанавливается доступный объем физической памяти
# Если лимит меньше 32 Мб, то устанавливается 32 Мб
# При ошибке возвращает 0

    mapSetMemoryLimit_t = mapsyst.GetProcAddress(curLib,ctypes.c_ulong,'mapSetMemoryLimit', maptype.HMAP, ctypes.c_ulong)
    def mapSetMemoryLimit(_hmap: maptype.HMAP, _limit: int) -> int:
        return mapSetMemoryLimit_t (_hmap, _limit)


# Запросить габариты открытых данных
# hmap - идентификатор открытых данных (документа)
# dframe - указатель на заполняемую структуру
# place - вид системы координат: PP_PICTURE - в точках экрана, PP_PLANE - в метрах в системе координат документа,
#         PP_GEO - в радианах на эллипсоиде документа
# Запрашиваются координаты углов района в метрах или радианах на местности
# в картографической системе или в пикселах относительно верхнего левого угла района
# При ошибке возвращает ноль

    mapGetTotalBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetTotalBorder(_hmap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetTotalBorder_t (_hmap, _dframe, _place)


# Запросить габариты открытых данных в системе координат, заданной кодом EPSG
# hmap - идентификатор открытых данных (документа)
# dframeplane - указатель на заполняемую структуру в метрах
# dframegeo - указатель на заполняемую структуру в радианах
# epsgcode - код системы координат (3395, 3857, 4326 и другие)
# Порядок осей - всегда широта\долгота, север\восток
# При ошибке возвращает ноль

    mapGetTotalBorderByEPSG_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalBorderByEPSG', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetTotalBorderByEPSG(_hmap: maptype.HMAP, _dframeplane: ctypes.POINTER(maptype.DFRAME), _dframegeo: ctypes.POINTER(maptype.DFRAME), _epsgcode: int) -> int:
        return mapGetTotalBorderByEPSG_t (_hmap, _dframeplane, _dframegeo, _epsgcode)


# Установить левый отступ изображения карты от начала буфера изображения
# hmap - идентификатор открытых данных (документа)
# leftmm - примерная величина отступа левой границы изображения от края окна в мм
# Ширина полосы в метрах, на которую расширяются габариты изображения в текущем масштабе, вычисляется так:
# double delta = mapGetRealShowScale(hmap) # mapGetLeftIndent(hmap) / 1000.0;

    mapSetLeftIndent_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetLeftIndent', maptype.HMAP, ctypes.c_long)
    def mapSetLeftIndent(_hmap: maptype.HMAP, _leftmm: int) -> ctypes.c_void_p:
        return mapSetLeftIndent_t (_hmap, _leftmm)


# Запросить левый отступ изображения карты от начала буфера изображения
# hmap - идентификатор открытых данных (документа)
# Возвращает сдвиг в окне (буфере) левой границы изображения в мм от края окна (буфера)

    mapGetLeftIndent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLeftIndent', maptype.HMAP)
    def mapGetLeftIndent(_hmap: maptype.HMAP) -> int:
        return mapGetLeftIndent_t (_hmap)


# Преобразование из пикселов в изображении в координаты на местности в метрах
# hmap - идентификатор открытых данных (документа)
# x - координата в пикселах по горизонтали
# y - координата в пикселах по вертикали
# Полученные координаты будут в метрах: x - на сервер, y - на восток

    mapPictureToPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapPictureToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPictureToPlane(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapPictureToPlane_t (_hmap, _x, _y)


# Преобразование из пикселов в изображении в координаты на местности в метрах
# x - координата в пикселах по горизонтали
# y - координата в пикселах по вертикали
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Полученные координаты будут в метрах: x - на сервер, y - на восток

    mapPictureToPlanePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapPictureToPlanePro', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapPictureToPlanePro(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapPictureToPlanePro_t (_x, _y, _hpaint)


# Преобразование из метров на местности в пикселы на изображении
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе координат документа
# y - координата в метрах на восток в системе координат документа
# Полученные координаты будут в пикселах: x - по горизонтали, y - по вертикали

    mapPlaneToPicture_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapPlaneToPicture', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPicture(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapPlaneToPicture_t (_hmap, _x, _y)


# Преобразование из метров на местности в пикселы на изображении
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе координат документа
# y - координата в метрах на восток в системе координат документа
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
# Полученные координаты будут в пикселах: x - по горизонтали, y - по вертикали

    mapPlaneToPicturePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapPlaneToPicturePro', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapPlaneToPicturePro(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        return mapPlaneToPicturePro_t (_x, _y, _hpaint)


# Преобразование из метров на местности в геодезические координаты
# hmap - идентификатор открытых данных (документа)
# bx - координата в метрах на север в системе координат документа
# ly - координата в метрах на восток в системе координат документа
# Полученные координаты будут в радианах: bx - широта, ly - долгота
# Пересчет выполняется в соответствии с проекцией карты и поддерживается не для всех карт (mapIsGeoSupported() != 0)
# При ошибке возвращает ноль

    mapPlaneToGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToGeo_t (_hmap, _bx, _ly)


# Преобразование из геодезических координат открытых данных в плоские прямоугольные координаты
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах
# ly - долгота в радианах
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток
# Пересчет выполняется в соответствии с проекцией карты и поддерживается не для всех карт (mapIsGeoSupported() != 0)
# При ошибке возвращает ноль

    mapGeoToPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToPlane(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToPlane_t (_hmap, _bx, _ly)


# Запрос, поддерживается ли пересчет для геодезических координат
# hmap - идентификатор открытых данных (документа)
# Если нет - возвращает ноль

    mapIsGeoSupported_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsGeoSupported', maptype.HMAP)
    def mapIsGeoSupported(_hmap: maptype.HMAP) -> int:
        return mapIsGeoSupported_t (_hmap)


# Преобразование из метров на местности в геодезические координаты WGS84
# hmap - идентификатор открытых данных (документа)
# bx - координата в метрах на север в системе координат документа
# ly - координата в метрах на восток в системе координат документа
# Полученные координаты будут в радианах: bx - широта в системе WGS84, ly - долгота в системе WGS84
# При ошибке возвращает ноль

    mapPlaneToGeoWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToGeoWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeoWGS84(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToGeoWGS84_t (_hmap, _bx, _ly)


# Преобразование ортометрической высоты (MSL) к геодезической (WGS84)
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - ортометрическая высота в метрах
# hegm - идентификатор модели геоида, открытой mapOpenEgmPro()
# При ошибке возвращает ноль

    mapNormalHeightToGeoHeightWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapNormalHeightToGeoHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapNormalHeightToGeoHeightWGS84(_bx: float, _ly: float, _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapNormalHeightToGeoHeightWGS84_t (_bx, _ly, _h, _hegm)


# Преобразование геодезической (WGS84) высоты к ортометрической (MSL)
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - геодезическая высота на эллипсоиде WGS84 в метрах
# hegm - идентификатор модели геоида, открытой mapOpenEgmPro
# При ошибке возвращает ноль

    mapGeoHeightToNormalHeightWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoHeightToNormalHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoHeightToNormalHeightWGS84(_bx: float, _ly: float, _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapGeoHeightToNormalHeightWGS84_t (_bx, _ly, _h, _hegm)


# Преобразование геодезических координат документа к геоцентрическим для эллипсоида WGS84
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах в системе открытых данных (документа)
# ly - долгота в радианах в системе открытых данных (документа)
# h - геодезическая высота на эллипсоиде карты в метрах
# Преобразование ортометрической высоты к геодезической выполняет mapNormalHeightToGeoHeightWGS84
# или mapUserPlaneToGeoWGS84Pro
# Полученные координаты будут в геоцентрической системе WGS84 в метрах
# При ошибке возвращает ноль

    mapGeoToXYZWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToXYZWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZWGS84(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToXYZWGS84_t (_hmap, _bx, _ly, _h)


# Преобразование геодезических координат к геоцентрическим в системе открытых данных (документа)
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах в системе открытых данных (документа)
# ly - долгота в радианах в системе открытых данных (документа)
# h - геодезическая высота в метрах в системе открытых данных (документа)
# Полученные координаты будут в геоцентрической системе в метрах на эллипсоиде документа
# При ошибке возвращает ноль

    mapGeoToXYZ_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToXYZ', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZ(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToXYZ_t (_hmap, _bx, _ly, _h)


# Преобразование геоцентрических координат WGS84 к геодезическим координатам карты
# hmap - идентификатор открытых данных (документа)
# bx - геоцентрическая координата WGS84 в метрах
# ly - геоцентрическая координата WGS84 в метрах
# h - геоцентрическая координата WGS84 в метрах
# Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
#     h - геодезическая высота на эллипсоиде карты
# При ошибке возвращает ноль

    mapXYZWGS84ToGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapXYZWGS84ToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZWGS84ToGeo_t (_hmap, _bx, _ly, _h)


# Преобразование геоцентрических координат на эллипсоиде карты к геодезическим
# hmap - идентификатор открытых данных (документа)
# bx - геоцентрическая координата в метрах на эллипсоиде карты
# ly - геоцентрическая координата в метрах на эллипсоиде карты
# h - геоцентрическая координата в метрах на эллипсоиде карты
# Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
#     h - геодезическая высота на эллипсоиде карты
# При ошибке возвращает ноль

    mapXYZToGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapXYZToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZToGeo_t (_hmap, _bx, _ly, _h)


# Пересчет геоцентрических координат по заданным параметрам преобразования
# X - геоцентрическая координата в метрах
# Y - геоцентрическая координата в метрах
# Z - геоцентрическая координата в метрах
# datum - параметры преобразования геоцентрических координат
# Пересчет выполняется по формуле Обратное преобразование Гельмерта, или Coordinate Frame Rotation, EPSG:1032
# Знаки числовых значений должны быть заданы с учетом направления преобразования
# При ошибке возвращает ноль

    mapTransformXYZ_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTransformXYZ', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM))
    def mapTransformXYZ(_X: ctypes.POINTER(ctypes.c_double), _Y: ctypes.POINTER(ctypes.c_double), _Z: ctypes.POINTER(ctypes.c_double), _datum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM)) -> int:
        return mapTransformXYZ_t (_X, _Y, _Z, _datum)


# Преобразование геодезических координат карты в геодезические координаты WGS84
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах в системе карты
# ly - долгота в радианах в системе карты
# h - геодезическая высота на эллипсоиде карты в метрах
# Полученные координаты будут в радианах: bx - широта WGS84, ly - долгота WGS84,
#     h - геодезическая высота на эллипсоиде WGS84
# При ошибке возвращает ноль

    mapGeoToGeoWGS843D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToGeoWGS843D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToGeoWGS843D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToGeoWGS843D_t (_hmap, _bx, _ly, _h)


# Преобразование геодезических координат WGS84 в геодезические координаты карты
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - геодезическая высота на эллипсоиде WGS84 в метрах
# Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
#     h - геодезическая высота на эллипсоиде карты
# При ошибке возвращает ноль

    mapGeoWGS84ToGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToGeo3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToGeo3D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToGeo3D_t (_hmap, _bx, _ly, _h)


# Преобразование геодезических координат WGS84 в метры в системе карты
# hmap - идентификатор открытых данных (документа)
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - высота в метрах или 0 (не пересчитывается)
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - высота в метрах
# При ошибке возвращает ноль

    mapGeoWGS84ToPlane3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToPlane3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToPlane3D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToPlane3D_t (_hmap, _bx, _ly, _h)


# Преобразование набора точек из одной системы координат в другую
# hmap - идентификатор открытых данных (документа)
# srcpoints - указатель на список исходных точек
# tagpoints - указательн на список пересчитанных точек (может быть равен srcpoints)
# srctype - тип входной системы координат: PP_PLANE, PP_GEO, PP_GEOWGS84, PP_PICTURE
# targettype - тип выходной системы координат: PP_PLANE, PP_GEO, PP_GEOWGS84, PP_PICTURE
# count - число преобразуемых точек в списках
# При ошибке возвращает ноль

    mapTransformPoints_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapTransformPoints', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapTransformPoints(_hmap: maptype.HMAP, _srcpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _srctype: int, _tagpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _targettype: int, _count: int) -> ctypes.c_void_p:
        return mapTransformPoints_t (_hmap, _srcpoints, _srctype, _tagpoints, _targettype, _count)


# Преобразование координат из градусов в радианы с учетом знака
# degree - структура, содержащая координаты в градусах, минутах, секундах. Описана в maptype.h
# radian - значение в радианах

    mapSignDegreeToRadian_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSignDegreeToRadian', ctypes.POINTER(maptype.SIGNDEGREE), ctypes.POINTER(ctypes.c_double))
    def mapSignDegreeToRadian(_degree: ctypes.POINTER(maptype.SIGNDEGREE), _radian: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        return mapSignDegreeToRadian_t (_degree, _radian)


# Преобразование координат из радиан в градусы со знаком
# radian - значение в радианах
# degree - структура, содержащая координаты в градусах, минутах, секундах. Описана в maptype.h

    mapRadianToSignDegree_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapRadianToSignDegree', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.SIGNDEGREE))
    def mapRadianToSignDegree(_radian: ctypes.POINTER(ctypes.c_double), _degree: ctypes.POINTER(maptype.SIGNDEGREE)) -> ctypes.c_void_p:
        return mapRadianToSignDegree_t (_radian, _degree)


# Вычисление осевого маридиана по номеру зоны для топокарт СК-42, 95, ГСК-2011
# zone - номер зоны
# При ошибке возвращает ноль

    mapGetAxisMeridianByZone_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetAxisMeridianByZone', ctypes.c_long)
    def mapGetAxisMeridianByZone(_zone: int) -> float:
        return mapGetAxisMeridianByZone_t (_zone)


# Вычисление осевого маридиана по номеру зоны для топокарт UTM
# zone - номер зоны UTM
# При ошибке возвращает ноль

    mapGetAxisMeridianByUTMZone_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetAxisMeridianByUTMZone', ctypes.c_long)
    def mapGetAxisMeridianByUTMZone(_zone: int) -> float:
        return mapGetAxisMeridianByUTMZone_t (_zone)


# Вычисление осевого маридиана топокарты по номеру зоны с учетом типа карты
# zone - номер зоны от 1 до 60 с учетом типа карты
# type - тип топокарты (CK_42, CK_95, GCK_2011, UTMWGS84, UTMTYPE)
# Для UTM зоны идут от -180 до +180, для СК-42, 95, ГСК-2011 - от 0 до 360
# При ошибке возвращает ноль

    mapGetAxisMeridianByZoneAndType_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetAxisMeridianByZoneAndType', ctypes.c_long, ctypes.c_long)
    def mapGetAxisMeridianByZoneAndType(_zone: int, _maptype: int) -> float:
        return mapGetAxisMeridianByZoneAndType_t (_zone, _maptype)


# Вычисление номера зоны по геодезической долготе в радианах (меридиану) для топокарт СК-42, 95, ГСК-2011
# meridian - значение меридиана в радианах
# При ошибке возвращает ноль

    mapGetZoneByMeridian_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetZoneByMeridian', ctypes.c_double)
    def mapGetZoneByMeridian(_meridian: float) -> int:
        return mapGetZoneByMeridian_t (_meridian)


# Вычисление номера зоны UTM по геодезической долготе в радианах
# meridian - значение меридиана в радианах
# При ошибке возвращает ноль

    mapGetUTMZoneByMeridian_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetUTMZoneByMeridian', ctypes.c_double)
    def mapGetUTMZoneByMeridian(_meridian: float) -> int:
        return mapGetUTMZoneByMeridian_t (_meridian)


# Заполнение осевого меридиана по геодезической долготе в радианах для топографических карт СК-42, 95, ГСК-2011, UTM
# hmap - идентификатор открытых данных (документа)
# meridian - значение меридиана в радианах
# Не рекомендуется применять для карт уже содержащих объекты
# При ошибке возвращает ноль

    mapSetAxisMeridianByMeridian_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAxisMeridianByMeridian', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByMeridian(_hmap: maptype.HMAP, _meridian: float) -> int:
        return mapSetAxisMeridianByMeridian_t (_hmap, _meridian)


# Заполнение осевого меридиана по старшей цифре координаты Y для топографических карт СК-42, 95, ГСК-2011
# hmap - идентификатор открытых данных (документа)
# y - координата по горизонтали в метрах произвольной точки, попадающей на заданный лист
# Не рекомендуется применять для карт уже содержащих объекты
# При ошибке возвращает ноль

    mapSetAxisMeridianByPlaneY_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAxisMeridianByPlaneY', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByPlaneY(_hmap: maptype.HMAP, _y: float) -> int:
        return mapSetAxisMeridianByPlaneY_t (_hmap, _y)


# Запросить параметры эллипсоида по его номеру
# ellipsoid - номер эллипсоида, описан в ELLIPSOIDKIND
# parm - параметры заданного эллипсоида
# При ошибке возвращает ноль

    mapGetEllipsoidParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEllipsoidParameters', ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetEllipsoidParameters(_ellipsoid: int, _parm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetEllipsoidParameters_t (_ellipsoid, _parm)


# Установить текущие параметры пользовательской системы координат
# mapreg - структура параметров системы координат карты
# datum - параметры пересчета с эллипсоида рабочей системы координат к WGS84 или 0
# ellipsoid - параметры пользовательского эллипсоида, когда поле EllipsoidKind в
#             MAPREGISTEREX равно USERELLIPSOID или 0
# ttype - тип локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# Возвращает идентификатор пользовательской системы координат
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# Для Широта\Долгота на WGS84 код равен 4326, для СК-42 зоны 1-60: 28401-28460, для СК-95 зоны 1-60: 20001-20060
# для UTM на WGS84 зоны 1-60: 32601-32660
# При ошибке возвращает ноль

    mapCreateUserSystemParametersPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateUserSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCreateUserSystemParametersPro(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersPro_t (_mapreg, _datum, _ellipsoid, _ttype, _tparm)


# Установить текущие параметры пользовательской системы координат по коду EPSG
# epsgcode - код EPSG
# Возвращает идентификатор пользовательской системы координат
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateUserSystemParametersByEpsg', ctypes.c_long)
    def mapCreateUserSystemParametersByEpsg(_epsgcode: int) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByEpsg_t (_epsgcode)


# Установить текущие параметры пользовательской системы координат из открытых данных
# hmap - идентификатор открытых данных (документа)
# Возвращает идентификатор пользовательской системы координат
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersByDoc_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateUserSystemParametersByDoc', maptype.HMAP)
    def mapCreateUserSystemParametersByDoc(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByDoc_t (_hmap)


# Установить текущие параметры пользовательской системы координат из записи XML
# point - указатель на строку, завершающуся нулем и содержащую запись параметров системы координат из XML
# Запись параметров из XML можно запросить через mapGetUserSystemXmlNode()
# Возвращает идентификатор пользовательской системы координат
# По завершении использования необходимо вызвать mapDeleteUserSystemParameters
# При ошибке возвращает ноль

    mapCreateUserSystemParametersByXmlNode_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateUserSystemParametersByXmlNode', ctypes.c_char_p)
    def mapCreateUserSystemParametersByXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapCreateUserSystemParametersByXmlNode_t (_point)


# Освободить ресурсы пользовательской системы координат
# huser - идентификатор пользовательской системы координат

    mapDeleteUserSystemParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapDeleteUserSystemParameters', ctypes.c_void_p)
    def mapDeleteUserSystemParameters(_huser: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapDeleteUserSystemParameters_t (_huser)


# Запросить текущие параметры пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# mapreg - структура параметров системы координат карты
# datum - параметры пересчета с эллипсоида рабочей системы координат к WGS84 или 0
# ellipsoid - параметры пользовательского эллипсоида, когда поле EllipsoidKind в
#             MAPREGISTEREX равно USERELLIPSOID или 0
# ttype - тип локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# При ошибке возвращает ноль

    mapGetUserSystemParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetUserSystemParameters', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetUserSystemParameters(_huser: ctypes.c_void_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetUserSystemParameters_t (_huser, _mapreg, _datum, _ellipsoid, _ttype, _tparm)


# Изменить текущие параметры пользовательской системы координат по коду EPSG
# huser - идентификатор пользовательской системы координат
# epsgcode - код EPSG
# При ошибке возвращает ноль

    mapChangeUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeUserSystemParametersByEpsg', ctypes.c_void_p, ctypes.c_long)
    def mapChangeUserSystemParametersByEpsg(_huser: ctypes.c_void_p, _epsgcode: int) -> int:
        return mapChangeUserSystemParametersByEpsg_t (_huser, _epsgcode)


# Установить тип пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# type - тип пользовательской системы координат: 1 - плоская прямоугольная, 2 - геодезическая
# При отсутствии данных возвращает ноль

    mapSetUserSystemType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetUserSystemType', ctypes.c_void_p, ctypes.c_long)
    def mapSetUserSystemType(_huser: ctypes.c_void_p, _type: int) -> int:
        return mapSetUserSystemType_t (_huser, _type)


# Запросить тип пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# Возвращает тип пользовательской системы координат: 1 - плоская прямоугольная, 2 - геодезическая
# При отсутствии данных возвращает ноль

    mapGetUserSystemType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetUserSystemType', ctypes.c_void_p)
    def mapGetUserSystemType(_huser: ctypes.c_void_p) -> int:
        return mapGetUserSystemType_t (_huser)


# Запросить значение осевого меридиана для пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# При ошибке возвращает ноль

    mapGetUserSystemAxisMeridian_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetUserSystemAxisMeridian', ctypes.c_void_p)
    def mapGetUserSystemAxisMeridian(_huser: ctypes.c_void_p) -> float:
        return mapGetUserSystemAxisMeridian_t (_huser)


# Установить номер зоны для пользовательской системы координат и обновить осевой меридиан
# huser - идентификатор пользовательской системы координат
# zone - номер зоны от 1 до 60
# isupdateaxis - признак необходимости пересчета осевого меридиана для заданного номера зоны
# При ошибке возвращает ноль

    mapSetUserSystemZone_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetUserSystemZone', ctypes.c_void_p, ctypes.c_long, ctypes.c_long)
    def mapSetUserSystemZone(_huser: ctypes.c_void_p, _zone: int, _isupdateaxis: int) -> int:
        return mapSetUserSystemZone_t (_huser, _zone, _isupdateaxis)


# Запросить номер зоны для пользовательской системы координат
# huser - идентификатор пользовательской системы координат
# При ошибке возвращает ноль

    mapGetUserSystemZone_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetUserSystemZone', ctypes.c_void_p)
    def mapGetUserSystemZone(_huser: ctypes.c_void_p) -> int:
        return mapGetUserSystemZone_t (_huser)


# Преобразование пользовательских геодезических координат в геодезические координаты WGS84
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах или 0
# Полученные координаты будут в радианах: bx - широта WGS84, ly - долгота WGS84,
#     h - геодезическая высота на эллипсоиде WGS84
# При ошибке возвращает 0

    mapUserGeoToGeoWGS843D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToGeoWGS843D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeoWGS843D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeoWGS843D_t (_huser, _bx, _ly, _h)


# Преобразование пользовательских геодезических координат в геодезические координаты на заданном эллипсоиде
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах или 0
# ldatum - параметры перехода от пользовательской системы координат к геодезической системе на заданном эллипсоиде
#          (обратное преобразование Гельмерта, или Coordinate Frame Rotation; EPSG dataset coordinate operation method code 1032)
# ellipsoid - параметры эллипсоида, на котором определяют геодезические координаты
# Полученные координаты будут в радианах: bx - широта на заданном эллипсоиде, ly - долгота WGS84 на заданном эллипсоиде,
#     h - геодезическая высота на заданном эллипсоиде
# При ошибке возвращает 0

    mapUserGeoToLocalGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToLocalGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapUserGeoToLocalGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _ldatum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapUserGeoToLocalGeo3D_t (_huser, _bx, _ly, _h, _ldatum, _ellipsoid)


# Преобразование пользовательских геодезических координат в геоцентрические координаты WGS84
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах
# Полученные координаты будут в геоцентрической системе WGS84 в метрах
# При ошибке возвращает ноль

    mapUserGeoToXYZWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToXYZWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToXYZWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToXYZWGS84_t (_huser, _bx, _ly, _h)


# Преобразование геоцентрических координат WGS84 в пользовательские геодезические координаты
# huser - идентификатор пользовательской системы координат
# bx - геоцентрическая координата WGS84 в метрах
# ly - геоцентрическая координата WGS84 в метрах
# h - геоцентрическая координата WGS84 в метрах
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе,
#     h - геодезическая высота на пользовательском эллипсоиде
# При ошибке возвращает ноль

    mapXYZWGS84ToUserGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapXYZWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapXYZWGS84ToUserGeo_t (_huser, _bx, _ly, _h)


# Преобразование геодезических координат к геоцентрическим для пользовательской системы
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах
# Полученные координаты будут в геоцентрической системе в метрах на пользователськом эллипсоиде
# При ошибке возвращает ноль

    mapUserGeoToUserXYZ_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToUserXYZ', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserXYZ(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToUserXYZ_t (_huser, _bx, _ly, _h)


# Преобразование геоцентрических координат в геодезические координаты для пользовательской системы
# bx - геоцентрическая координата в метрах на пользовательском эллипсоиде
# ly - геоцентрическая координата в метрах  на пользовательском эллипсоиде
# h - геоцентрическая координата в метрах на пользовательском эллипсоиде
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе,
#     h - геодезическая высота на пользовательском эллипсоиде
# При ошибке возвращает ноль

    mapUserXYZToUserGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserXYZToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserXYZToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserXYZToUserGeo_t (_huser, _bx, _ly, _h)


# Преобразование геодезических координат в плоские прямоугольные в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах или 0
# hegm - идентификатор модели геоида для пересчета геодезической высоты в ортометрическую (геоид MSL) или 0
# Для получения hegm применяется функция mapOpenEgmPro
# Высота пересчитывается сначала из геодезической в геодезическую WGS84, затем в ортометрическую
# Если параметр hegm равен нулю, то пересчет высоты не выполняется
# Балтийская система высот (относительно квазигеоида, нормальная) отличается от ортометрической в среднем
# в пределах 1-2 метров
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - ортометрическая высота в метрах (MSL),
# если был задан hegm, или без изменений
# При ошибке возвращает ноль

    mapUserGeoToUserPlanePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserGeoToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserGeoToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)


# Преобразование геодезических координат в плоские прямоугольные в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток
# При ошибке возвращает ноль

    mapUserGeoToUserPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToUserPlane_t (_huser, _bx, _ly)


# Преобразование из метров на местности в пользовательской системе в геодезические координаты WGS84
# huser - идентификатор пользовательской системы координат
# bx - координата в метрах на север
# ly - координата в метрах на восток
# h - ортометрическая высота в точке (метры) или 0
# hegm - идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или 0
# Для получения hegm применяется функция mapOpenEgmPro
# Полученные координаты будут в радианах: bx - широта WGS84, ly - долгота WGS84,
#     h - геодезическая высота на эллипсоиде WGS84, если задан параметр hegm, или не изменится
# При ошибке возвращает ноль

    mapUserPlaneToGeoWGS84Pro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserPlaneToGeoWGS84Pro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToGeoWGS84Pro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserPlaneToGeoWGS84Pro_t (_huser, _bx, _ly, _h, _hegm)


# Преобразование из метров на местности в пользовательской проекции в геодезические координаты WGS84
# huser - идентификатор пользовательской системы координат
# bx - координата в метрах на север
# ly - координата в метрах на восток
# Полученные координаты будут в радианах: bx - широта WGS84, ly - долгота WGS84
# При ошибке возвращает ноль

    mapUserPlaneToGeoWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserPlaneToGeoWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToGeoWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToGeoWGS84_t (_huser, _bx, _ly)


# Преобразование из метров на местности в геодезические координаты в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - координата в метрах на север
# ly - координата в метрах на восток
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
# При ошибке возвращает ноль

    mapUserPlaneToUserGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserPlaneToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserPlaneToUserGeo_t (_huser, _bx, _ly)


# Преобразование из метров на местности в геодезические координаты в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - координата в метрах на север
# ly - координата в метрах на восток
# h - ортометрическая высота в метрах или 0
# hegm - идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или 0
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
#     h - геодезическая высота на пользовательском эллипсоиде, если задан параметр hegm, или не изменится
# При ошибке возвращает ноль

    mapUserPlaneToUserGeoPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserPlaneToUserGeoPro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToUserGeoPro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapUserPlaneToUserGeoPro_t (_huser, _bx, _ly, _h, _hegm)


# Преобразование геодезических координат WGS84 в геодезические в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
# При ошибке возвращает ноль

    mapGeoWGS84ToUserGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserGeo_t (_huser, _bx, _ly)


# Преобразование геодезических координат WGS84 в геодезические в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - геодезическая высота на эллипсоиде WGS84 в метрах или 0
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
#     h - геодезическая высота на пользовательском эллипсоиде
# При ошибке возвращает ноль

    mapGeoWGS84ToUserGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToUserGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserGeo3D_t (_huser, _bx, _ly, _h)


# Преобразование геодезических координат WGS84 в плоские прямоугольные в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# h - геодезическая высота на эллипсоиде WGS84 в метрах или 0
# hegm - идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или 0
# Для получения hegm применяется функция mapOpenEgmPro
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - ортометрическая высота в метрах (MSL),
# если был задан hegm, или без изменений
# При ошибке возвращает ноль

    mapGeoWGS84ToUserPlanePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoWGS84ToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        return mapGeoWGS84ToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)


# Преобразование геодезических координат WGS84 в плоские прямоугольные в пользовательской системе
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах WGS84
# ly - долгота в радианах WGS84
# Полученные координаты будут в метрах: bx - на сервер, ly - на восток
# При ошибке возвращает ноль

    mapGeoWGS84ToUserPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoWGS84ToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoWGS84ToUserPlane_t (_huser, _bx, _ly)


# Преобразование геодезических координат документа в геодезические пользовательские координаты
# hmap  - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в системе открытых данных (документа)
# ly - долгота в радианах в системе открытых данных (документа)
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
# При ошибке возвращает ноль

    mapGeoToUserGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToUserGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToUserGeo_t (_hmap, _huser, _bx, _ly)


# Преобразование геодезических координат документа в геодезические пользовательские координаты
# hmap - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в системе открытых данных (документа)
# ly - долгота в радианах в системе открытых данных (документа)
# h - геодезическая высота в метрах на эллипсоиде открытых данных (документа)
# Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
#     h - геодезическая высота на пользовательском эллипсоиде
# При ошибке возвращает ноль

    mapGeoToUserGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeoToUserGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGeoToUserGeo3D_t (_hmap, _huser, _bx, _ly, _h)


# Преобразование геодезических пользовательских координат в геодезические координаты документа
# hmap  - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# h - геодезическая высота на эллипсоиде пользовательской системы в метрах или 0
# Полученные координаты будут в радианах: bx - широта в системе документа, ly - долгота в системе документа
#     h - геодезическая высота на эллипсоиде документа
# При ошибке возвращает ноль

    mapUserGeoToGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeo3D_t (_hmap, _huser, _bx, _ly, _h)


# Преобразование геодезических пользовательских координат в геодезические координаты документа
# hmap  - идентификатор открытых данных (документа)
# huser - идентификатор пользовательской системы координат
# bx - широта в радианах в пользовательской системе
# ly - долгота в радианах в пользовательской системе
# Полученные координаты будут в радианах: bx - широта в системе документа, ly - долгота в системе документа
# При ошибке возвращает ноль

    mapUserGeoToGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUserGeoToGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapUserGeoToGeo_t (_hmap, _huser, _bx, _ly)


# Сравнить параметры двух систем координат
# mapreg1 - параметры первой системы координат
# datum1 - параметры пересчета с эллипсоида первой системы координат к WGS84, или 0
# ellipsoid1 - параметры пользовательского эллипсоида для первой системы координат,
#              только когда поле EllipsoidKind в MAPREGISTEREX равно USERELLIPSOID, или 0
# type1 - тип локального преобразования первой системы координат, описан в TRANSFORMTYPE в mapcreat.h, или 0
# tparm1 - параметры локального преобразования координат для первой системы координат, или 0
# mapreg2 - параметры второй системы координат
# datum2 - параметры пересчета с эллипсоида второй системы координат к WGS84, или 0
# ellipsoid2 - параметры пользовательского эллипсоида для второй системы координат, или 0
# type2 - тип локального преобразования второй системы координат, описан в TRANSFORMTYPE в mapcreat.h, или 0
# tparm2 - параметры локального преобразования координат второй системы координат, или 0
# При несовпадении каких-либо значений параметров возвращает ненулевое значение
# Некоторые несовпадающие параметры могут считаться идентичными
# Например, топографическая карта UTM и обзорно-географическая карта UTM - обозначают одно и тоже

    mapCompareSystemParametersPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCompareSystemParametersPro(_mapreg1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype1: int, _tparm1: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _mapreg2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype2: int, _tparm2: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapCompareSystemParametersPro_t (_mapreg1, _datum1, _ellipsoid1, _ttype1, _tparm1, _mapreg2, _datum2, _ellipsoid2, _ttype2, _tparm2)


# Сравнить параметры двух систем координат
# mapreg1 - параметры первой системы координат
# datum1 - параметры пересчета с эллипсоида первой системы координат к WGS84, или 0
# ellipsoid1 - параметры пользовательского эллипсоида для первой системы координат,
#              только когда поле EllipsoidKind в MAPREGISTEREX равно USERELLIPSOID, или 0
# mapreg2 - параметры второй системы координат
# datum2 - параметры пересчета с эллипсоида второй системы координат к WGS84, или 0
# ellipsoid2 - параметры пользовательского эллипсоида для второй системы координат, или 0
# При несовпадении каких-либо значений параметров возвращает ненулевое значение

    mapCompareSystemParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareSystemParameters', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCompareSystemParameters(_mapreg1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _mapreg2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapCompareSystemParameters_t (_mapreg1, _datum1, _ellipsoid1, _mapreg2, _datum2, _ellipsoid2)


# Сравнить параметры двух пользовательских систем координат
# huser1 - идентификатор первой пользовательской системы координат
# huser2 - идентификатор второй пользовательской системы координат
# При несовпадении каких-либо значений параметров возвращает ненулевое значение

    mapCompareUserSystemParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareUserSystemParameters', ctypes.c_void_p, ctypes.c_void_p)
    def mapCompareUserSystemParameters(_huser1: ctypes.c_void_p, _huser2: ctypes.c_void_p) -> int:
        return mapCompareUserSystemParameters_t (_huser1, _huser2)


# Запросить описание пользовательской системы координат в виде XML-строки, заканчивающейся нулем
# huser - идентификатор пользовательской системы координат
# name - условное имя системы координат (атрибут Name), указывается обязательно
# Строка содержит узел с названием Project (смотри mapOpenMapRegisterListUn())
# <Project Name="Nicaragua NAD-27"><Projection Type="Transverse Mercator" CentralMeridian="-87.0" ...
# ScaleFactor="0.9996" Angle="0.0"/><Spheroid Type="Clarke 1866" Parm="6378206.400, 294.97869821"/>
# <Datum DX="2.478" ... M="0.000000685000"/></Project>
# После чтения строки необходимо освободить память через mapFreeUserSystemXmlNode
# При ошибке возвращает ноль

    mapGetUserSystemXmlNode_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetUserSystemXmlNode', ctypes.c_void_p, maptype.PWCHAR)
    def mapGetUserSystemXmlNode(_huser: ctypes.c_void_p, _name: mapsyst.WTEXT) -> ctypes.POINTER(ctypes.c_char):
        return mapGetUserSystemXmlNode_t (_huser, _name.buffer())


# Освободить память строки с описанием параметров системы координат
# point - адрес строки, полученной из mapGetUserSystemXmlNode

    mapFreeUserSystemXmlNode_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeUserSystemXmlNode', ctypes.c_char_p)
    def mapFreeUserSystemXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeUserSystemXmlNode_t (_point)


# Установить формат отображения текущих координат курсора
# hmap - идентификатор открытых данных (документа)
# format - номер формата отображения координат (CURRENTPOINTFORMAT, например: PLANEPOINT, PLANE42POINT, GEORADWGS84)
# При ошибке возвращает ноль, иначе - установленное значение

    mapSetCurrentPointFormat_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCurrentPointFormat', maptype.HMAP, ctypes.c_long)
    def mapSetCurrentPointFormat(_hmap: maptype.HMAP, _format: int) -> int:
        return mapSetCurrentPointFormat_t (_hmap, _format)


# Запросить формат отображения текущих координат курсора
# hmap - идентификатор открытых данных (документа)
# Возвращает номер формата отображения координат (CURRENTPOINTFORMAT)
# При ошибке возвращает ноль

    mapGetCurrentPointFormat_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCurrentPointFormat', maptype.HMAP)
    def mapGetCurrentPointFormat(_hmap: maptype.HMAP) -> int:
        return mapGetCurrentPointFormat_t (_hmap)


# Установить число цифр после точки (запятой) в формате отображения координат на плоскости
# hmap - идентификатор открытых данных (документа)
# decimal - число цифр после точки в формате отображения текущих координат курсора на плоскости
# При ошибке возвращает ноль, иначе - установленное значение

    mapSetCurrentPointPlaneDecimal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCurrentPointPlaneDecimal', maptype.HMAP, ctypes.c_long)
    def mapSetCurrentPointPlaneDecimal(_hmap: maptype.HMAP, _decimal: int) -> int:
        return mapSetCurrentPointPlaneDecimal_t (_hmap, _decimal)


# Запросить число цифр после точки (запятой) в формате отображения координат на плоскости
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль, иначе - установленное значение

    mapGetCurrentPointPlaneDecimal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCurrentPointPlaneDecimal', maptype.HMAP)
    def mapGetCurrentPointPlaneDecimal(_hmap: maptype.HMAP) -> int:
        return mapGetCurrentPointPlaneDecimal_t (_hmap)


# Пересчитать плоские прямоугольные координаты документа в заданный формат отображения
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе открытых данных (документа)
# y - координата в метрах на восток в системе открытых данных (документа)
# h - высота в метрах в системе открытых данных (документа) или 0
# Формат отображения устанавливается вызовом mapSetCurrentPointFormat
# При ошибке возвращает ноль

    mapPlaneToPointFormat_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToPointFormat', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPointFormat(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlaneToPointFormat_t (_hmap, _x, _y, _h)


# Пересчитать плоские прямоугольные координаты документа в заданный формат в виде комментария
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе открытых данных (документа)
# y - координата в метрах на восток в системе открытых данных (документа)
# h - высота в метрах в системе открытых данных (документа) или 0
# hegm - идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или 0
#        Для получения hegm применяется функция mapOpenEgmPro
# place - адрес строки для записи результата
# size - размер выделеной строки (не менее 256 байт)
# Пример строки:
# B= -73° 27' 04.53"  L= 175° 51' 21.07"  H= 109.51 m (WGS84)
# X= 6 309 212.12 м   Y= 7 412 249.25 м (СК42)
# При ошибке возвращает ноль

    mapPlaneToPointFormatStringPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToPointFormatStringPro', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long)
    def mapPlaneToPointFormatStringPro(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapPlaneToPointFormatStringPro_t (_hmap, _x, _y, _h, _hegm, _place.buffer(), _size)


# Пересчитать плоские прямоугольные координаты документа в заданный формат в виде комментария
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе открытых данных (документа)
# y - координата в метрах на восток в системе открытых данных (документа)
# h - высота в метрах в системе открытых данных (документа) или 0
# place - адрес строки для записи результата
# size - размер выделеной строки (не менее 256 байт)
# Пример строки:
# B= -73° 27' 04.53"  L= 175° 51' 21.07"  H= 109.51 m (WGS84)
# X= 6 309 212.12 м   Y= 7 412 249.25 м (СК42)
# При ошибке возвращает ноль

    mapPlaneToPointFormatStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToPointFormatStringUn', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_long)
    def mapPlaneToPointFormatStringUn(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int) -> int:
        return mapPlaneToPointFormatStringUn_t (_hmap, _x, _y, _h, _place.buffer(), _size)


# Пересчитать плоские прямоугольные координаты документа в заданный формат в виде строки
# hmap - идентификатор открытых данных (документа)
# x - координата в метрах на север в системе открытых данных (документа)
# y - координата в метрах на восток в системе открытых данных (документа)
# h - высота в метрах в системе открытых данных (документа) или 0
# hegm - идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или 0
#        Для получения hegm применяется функция mapOpenEgmPro
# place - адрес строки для записи результата
# size - размер выделеной строки (не менее 256 байт)
# Пример строки:
# -73.45093678 175.83160324 109.51
# 6309212.123 7412249.257
# При ошибке возвращает ноль

    mapPlaneToPointFormatText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlaneToPointFormatText', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapPlaneToPointFormatText(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p, _place: ctypes.c_char_p, _size: int) -> int:
        return mapPlaneToPointFormatText_t (_hmap, _x, _y, _h, _hegm, _place, _size)


# Вывод плоских прямоугольных координат точки в строку
# x - координата в метрах на север в системе открытых данных (документа)
# y - координата в метрах на восток в системе открытых данных (документа)
# h - высота в метрах в системе открытых данных (документа) или 0
# place - адрес строки для размещения результата
# size  - размер строки в байтах (не менее 80 байт)
# maptype - тип карты (MAPTYPE), если не равен нулю, то добавляется строка
#           с обозначением системы координат: "   (СК42)", "   (CК95)",...
# decimal - число знаков после запятой (точки)
# Пример результата:
# "X=  438 145.27 m  Y= 6 230 513.03 m  H=  54.12 m"

    mapPlaneToStringUnEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapPlaneToStringUnEx', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPlaneToStringUnEx(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int, _maptype: int, _decimal: int = 2) -> ctypes.c_void_p:
        return mapPlaneToStringUnEx_t (_x, _y, _h, _place.buffer(), _size, _maptype, _decimal)


# Вывод геоцентрических координат точки в строку
# x - геоцентрическая координата в метрах
# y - геоцентрическая координата в метрах
# h - геоцентрическая координата в метрах
# place - адрес строки для размещения результата
# size  - размер строки в байтах (не менее 80 байт)
# Пример результата:
# "X= -4 438 145.271 Y= 3 230 513.034 H= 6 632 054.125 m"

    mapXYZToString_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapXYZToString', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapXYZToString(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _z: ctypes.POINTER(ctypes.c_double), _place: ctypes.c_char_p, _size: int, _maptype: int) -> ctypes.c_void_p:
        return mapXYZToString_t (_x, _y, _z, _place, _size, _maptype)


# Запись вещественного числа в символьном виде с фиксированной точкой
# value  - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 32)
# precision - число знаков после точки (запятой), если равно 0, то округление до целого числа,
#             если меньше 0, то округление в большую сторону
# separator - разделитель целой и дробной части:
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#                 '.' или ',' - заменить десятичную точку на separator: '.' или ','
# При ошибке возвращает ноль

    mapDoubleFormatPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDoubleFormatPro', ctypes.c_double, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDoubleFormatPro(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int, _separator: int) -> int:
        return mapDoubleFormatPro_t (_value, _string.buffer(), _size, _precision, _separator)


# Запись вещественного числа в символьном виде с фиксированной точкой
# value  - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 16)
# precision - число знаков после точки (запятой)
# При ошибке возвращает ноль

    mapDoubleFormat_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDoubleFormat', ctypes.c_double, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapDoubleFormat(_value: float, _string: ctypes.c_char_p, _size: int, _precision: int) -> int:
        return mapDoubleFormat_t (_value, _string, _size, _precision)


# Запись вещественного числа в символьном виде с фиксированной точкой со вставкой разделяющих пробелов
# value - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size   - длина строки в байтах (не менее 16)
# precision - число знаков после точки (запятой)
# При записи числа в строку выполняется разделение на тройки символов от конца строки к началу
# Например: 7 390 621.458
# При ошибке возвращает ноль

    mapDoubleToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDoubleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapDoubleToStringUn(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int) -> int:
        return mapDoubleToStringUn_t (_value, _string.buffer(), _size, _precision)


# Запись целого числа в символьном виде со вставкой разделяющих пробелов
# value - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size - длина строки в байтах (не менее 16)
# При записи числа в строку выполняется разделение на тройки символов от конца строки к началу
# Например: 7 390 621
# При ошибке возвращает ноль

    mapLongToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLongToStringUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToStringUn(_value: int, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapLongToStringUn_t (_value, _string.buffer(), _size)


# Запись целого числа типа __int64 в символьном виде со вставкой разделяющих пробелов
# value - значение числа, записываемого в строку
# string - адрес строки для размещения результата
# size - длина строки в байтах (не менее 32)
# При записи числа в строку выполняется разделение на тройки символов от конца строки к началу
# При ошибке возвращает ноль

    mapInt64ToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInt64ToStringUn', ctypes.c_int64, maptype.PWCHAR, ctypes.c_long)
    def mapInt64ToStringUn(_value: int, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapInt64ToStringUn_t (_value, _string.buffer(), _size)


# Округлить дробную часть числа до заданного числа знаков
# value - исходное значение числа, которое нужно округлить
# count - число знаков после запятой (от 0 до 9)
# Целая часть числа остается без изменения

    mapRoundDouble_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapRoundDouble', ctypes.c_double, ctypes.c_int)
    def mapRoundDouble(_value: float, _count: int) -> float:
        return mapRoundDouble_t (_value, _count)


# Запись масштаба в символьном виде со вставкой разделяющих пробелов
# scale - значение знаменателя масштаба, записываемого в строку
# string - адрес строки для размещения результата
# size - длина строки в байтах (не менее 20)
# При записи числа в строку выполняется разделение на тройки символов от конца строки к началу
# Например: "1 : 50 000", "2 : 1" - если scale < 1
# При ошибке возвращает ноль

    mapScaleToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapScaleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_long)
    def mapScaleToStringUn(_scale: float, _string: mapsyst.WTEXT, _size: int) -> int:
        return mapScaleToStringUn_t (_scale, _string.buffer(), _size)


# Запросить параметры проекции и системы координат по коду EPSG
# epsgcode - код EPSG, для СК-42 зоны 2-32 : 28402-28432, для СК-95 зоны 4-32: 20004-20032
# mapreg - параметры системы координат и проекции
# datum - параметры пересчета с эллипсоида рабочей системы координат к WGS84
# ellipsoid - параметры пользовательского эллипсоида для рабочей системы координат
# Если код EPSG задает геодезическую или геоцентрическую систему координат,
# то устанавливается проекция Широта\Долгота и соответствующие
# параметры эллипсоида и датум
# Если код EPSG задает плоскую прямоугольную систему координат,
# то все параметры устанавливаются из базы EPSG
# Для геодезических систем координат возвращает 2, для геоцентрических - 3,
# для плоских прямоугольных - 1
# При ошибке возвращает ноль

    mapGetParametersForEPSG_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetParametersForEPSG', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetParametersForEPSG(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetParametersForEPSG_t (_epsgcode, _mapreg, _datum, _ellipsoid)


# Зарегистрировать пользовательский код параметров Epsg
# epsg - регистрируемый код системы координат
# mapreg - параметры системы координат и проекции
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# ellipsoid - параметры эллипсоида
# Заданный код и его параметры запоминаются на сеанс работы приложения и будут выдаваться по запросу из mapGetParametersForEPSG()
# При ошибке возвращает ноль

    mapRegisterUserEpsgParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterUserEpsgParameters', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapRegisterUserEpsgParameters(_epsg: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellips: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapRegisterUserEpsgParameters_t (_epsg, _mapregister, _datum, _ellips)


# Открыть базу данных EPSG
# При успешном выполнении возвращает идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapOpenEPSGDatabase_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapOpenEPSGDatabase')
    def mapOpenEPSGDatabase() -> ctypes.c_void_p:
        return mapOpenEPSGDatabase_t ()


# Закрыть базу данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG

    mapCloseEPSGDatabase_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseEPSGDatabase', ctypes.c_void_p)
    def mapCloseEPSGDatabase(_epsgdata: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseEPSGDatabase_t (_epsgdata)


# Запросить количество прямоугольных систем координат в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapGetEPSGProjectedSystemCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGProjectedSystemCount', ctypes.c_void_p)
    def mapGetEPSGProjectedSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        return mapGetEPSGProjectedSystemCount_t (_epsgdata)


# Запросить количество геодезических систем координат в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystemCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGGeodeticSystemCount', ctypes.c_void_p)
    def mapGetEPSGGeodeticSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        return mapGetEPSGGeodeticSystemCount_t (_epsgdata)


# Считать данные на прямоугольную систему координат по номеру записи в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# number - номер записи в списке прямоугольных систем координат c 1
# mapreg - параметры системы координат и проекции
# ellipsoid - параметры эллипсоида
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# rectsys - параметры прямоугольной системы координат
# geodsys - параметры базовой геодезической системы координат
# unit - единицы измерения
# При ошибке или при выходе за границы набора данных возвращает ноль

    mapReadEPSGProjectedSystemByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadEPSGProjectedSystemByNumber', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadEPSGProjectedSystemByNumber(_epsgdata: ctypes.c_void_p, _number: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapReadEPSGProjectedSystemByNumber_t (_epsgdata, _number, _mapreg, _ellipsoid, _datum, _rectsys, _geodsys, _unit)


# Считать параметры геодезической системы координат по порядковому номеру в базе данных EPSG
# epsgdata - идентификатор открытой базы данных EPSG
# number - порядковый номер геодезической системы координат в базе данных EPSG c 1
# ellipsoid - параметры эллипсоида или 0
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# geodsys - параметры геодезической системы координат или 0
# При ошибке возвращает ноль

    mapReadEPSGGeodeticSystemByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadEPSGGeodeticSystemByNumber', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapReadEPSGGeodeticSystemByNumber(_epsgdata: ctypes.c_void_p, _number: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapReadEPSGGeodeticSystemByNumber_t (_epsgdata, _number, _ellipsoid, _datum, _geodsys)


# Запросить параметры геодезической системы координат по коду
# epsgcode - код геодезической системы координат в базе данных EPSG
# ellipsoid - параметры эллипсоида
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# geodsys - параметры геодезической системы координат
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystem_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGGeodeticSystem', ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystem(_epsgcode: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapGetEPSGGeodeticSystem_t (_epsgcode, _ellipsoid, _datum, _geodsys)


# Запросить параметры геодезической системы координат по имени в базе данных EPSG
# name - имя геодезической системы координат
# ellipsoid - параметры эллипсоида
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# geodsys - параметры геодезической системы координат
# При ошибке возвращает ноль

    mapGetEPSGGeodeticSystemByName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGGeodeticSystemByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystemByName(_name: ctypes.c_char_p, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        return mapGetEPSGGeodeticSystemByName_t (_name, _ellipsoid, _datum, _geodsys)


# Запросить параметры прямоугольной системы координат по коду в базе данных EPSG
# epsgcode - код прямоугольной системы координат в базе данных EPSG
# mapreg - параметры системы координат и проекции
# rectsys - параметры прямоугольной системы координат
# При ошибке возвращает ноль

    mapGetEPSGProjectedSystem_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGProjectedSystem', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.EPSGRECTSYS))
    def mapGetEPSGProjectedSystem(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS)) -> int:
        return mapGetEPSGProjectedSystem_t (_epsgcode, _mapreg, _rectsys)


# Запросить параметры единицы измерения по коду в базе данных EPSG
# epsgcode - код единицы измерения в базе данных EPSG
# unit - параметры единицы измерения
# При ошибке возвращает ноль

    mapGetEPSGUnit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGUnit', ctypes.c_long, ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapGetEPSGUnit(_epsgcode: int, _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapGetEPSGUnit_t (_epsgcode, _unit)


# Заполнить WKT строку из MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM
# mapreg - параметры системы координат и проекции
# ellipsoid - параметры эллипсоида
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# wktstr - заполняемая строка с описанием системы координат
# wktstrsize - зарезервированный размер строки (4 Кбайта достаточно)
# flag3D - флаг добавления вертикальной системы координат, соответствующей значению поля MAPREGISTEREX::HeightSystem
# При ошибке возвращает ноль

    mapSetWKTStringEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetWKTStringEx', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.c_char_p, ctypes.c_long, ctypes.c_int)
    def mapSetWKTStringEx(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _wktstr: ctypes.c_char_p, _wktstrsize: int, _flag3D: int) -> int:
        return mapSetWKTStringEx_t (_mapreg, _ellipsoid, _datum, _wktstr, _wktstrsize, _flag3D)


# Заполнить MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM из WKT строки
# wktstr - строка с описанием системы координат
# mapreg - параметры системы координат и проекции
# ellipsoid - заполняемые параметры эллипсоида
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84
# При ошибке возвращает ноль

    mapReadWKTString_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadWKTString', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapReadWKTString(_wktstr: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapReadWKTString_t (_wktstr, _mapreg, _ellipsoid, _datum)


# Прочитать описание системы координат из строки WKT (стандарт OGC 12-063r5)
# wktstr - WKT-строка с описанием системы координат
# isprojection - возвращает признак прямоугольной системы координат (1)
# mapreg - параметры системы координат и проекции или 0
# ellipsoid - параметры эллипсоида или 0
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84 или 0
# sysrect - параметры прямоугольной системы координат (при isprojection = 1) или 0
# sysgeo - параметры геодзической системы координат (при isprojection = 0) или 0
# unit - заполняемые параметры единицы измерения или 0
# При ошибке возвращает ноль

    mapReadWKTStringEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadWKTStringEx', ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadWKTStringEx(_wktstr: ctypes.c_char_p, _isprojection: ctypes.POINTER(ctypes.c_int), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _sysrect: ctypes.POINTER(mapcreat.EPSGRECTSYS), _sysgeo: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        return mapReadWKTStringEx_t (_wktstr, _isprojection, _mapreg, _ellipsoid, _datum, _sysrect, _sysgeo, _unit)


# Определить EPSG код для известных систем координат
# mapreg - параметры системы координат и проекции или 0
# ellipsoid - параметры эллипсоида или 0
# datum - параметры пересчета от заданного эллипсоида к эллипсоиду WGS84 или 0
# Возвращает код EPSG или ноль

    mapFindEPSGCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFindEPSGCode', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapFindEPSGCode(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapFindEPSGCode_t (_mapreg, _ellipsoid, _datum)


# Открыть список параметров систем координат
# name - имя файла списка параметров
# При успешном выполнении возвращает идентификатор списка в памяти
# При ошибке возвращает ноль

    mapOpenMapRegisterListUn_t = mapsyst.GetProcAddress(curLib,maptype.HMAPREG,'mapOpenMapRegisterListUn', maptype.PWCHAR)
    def mapOpenMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        return mapOpenMapRegisterListUn_t (_name.buffer())


# Создать список параметров систем координат
# name - имя файла списка параметров
# При успешном выполнении возвращает идентификатор списка в памяти
# При ошибке возвращает ноль

    mapCreateMapRegisterListUn_t = mapsyst.GetProcAddress(curLib,maptype.HMAPREG,'mapCreateMapRegisterListUn', maptype.PWCHAR)
    def mapCreateMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        return mapCreateMapRegisterListUn_t (_name.buffer())


# Закрыть список параметров систем координат
# hmapreg - идентификатор списка параметров систем координат

    mapCloseMapRegisterList_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseMapRegisterList', maptype.HMAPREG)
    def mapCloseMapRegisterList(_hmapreg: maptype.HMAPREG) -> ctypes.c_void_p:
        return mapCloseMapRegisterList_t (_hmapreg)


# Запросить число систем координат в списке
# hmapreg - идентификатор списка параметров систем координат
# При успешном выполнении возвращает число записей параметров
# Одной системе соответствует один узел "Project" в списке
# <ProjectList Version="1.0">
# При ошибке возвращает ноль

    mapMapRegisterListCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListCount', maptype.HMAPREG)
    def mapMapRegisterListCount(_hmapreg: maptype.HMAPREG) -> int:
        return mapMapRegisterListCount_t (_hmapreg)


# Запросить название системы координат по заданному порядковому номеру в списке
# hmapreg - идентификатор списка параметров систем координат
# number  - порядковый номер записи параметров с 1
# name - адрес строки для размещения результата
# size - размер выделенной строки в байтах
# При ошибке возвращает ноль

    mapMapRegisterListNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _size)


# Запросить комментарий для системы координат по порядковому номеру
# hmapreg - идентификатор списка параметров систем координат
# number - порядковый номер записи параметров с 1
# name - адрес строки для размещения результата
# size - длина выделенной строки для размещения результата
# При ошибке возвращает ноль

    mapMapRegisterListCommentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListCommentUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListCommentUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListCommentUn_t (_hmapreg, _number, _name.buffer(), _size)


# Запросить порядковый номер записи в списке по коду EPSG
# hmapreg - идентификатор списка параметров систем координат
# epsg - код EPSG для системы координат
# При ошибке возвращает ноль

    mapSeekMapRegisterListByEPSG_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekMapRegisterListByEPSG', maptype.HMAPREG, ctypes.c_long)
    def mapSeekMapRegisterListByEPSG(_hmapreg: maptype.HMAPREG, _epsg: int) -> int:
        return mapSeekMapRegisterListByEPSG_t (_hmapreg, _epsg)


# Запросить код EPSG для системы координат по порядковому номеру
# hmapreg - идентификатор списка параметров систем координат
# number  - порядковый номер записи параметров с 1
# Если код не задан - возвращает "-1"
# При ошибке возвращает ноль

    mapMapRegisterListEPSG_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListEPSG', maptype.HMAPREG, ctypes.c_long)
    def mapMapRegisterListEPSG(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        return mapMapRegisterListEPSG_t (_hmapreg, _number)


# Запросить идентификатор для системы координат по порядковому номеру
# hmapreg - идентификатор списка параметров систем координат
# number - порядковый номер записи параметров с 1
# ident - адрес строки для размещения идентификатора
# size - длина выделенной строки для размещения идентификатора
# При ошибке возвращает ноль

    mapMapRegisterListCrsIdentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListCrsIdentUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListCrsIdentUn(_hmapreg: maptype.HMAPREG, _number: int, _ident: mapsyst.WTEXT, _size: int) -> int:
        return mapMapRegisterListCrsIdentUn_t (_hmapreg, _number, _ident.buffer(), _size)


# Запросить параметры системы координат по заданному порядковому номеру
# hmapreg - идентификатор списка параметров систем координат
# number - порядковый номер записи параметров с 1
# mapreg - параметры проекции <Projection ...>
# datum  - параметры датума <Datum ...>
# ellparm - параметры эллипсоида <Spheroid ...>
# ttype - адрес поля для записи типа локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# При ошибке возвращает ноль

    mapMapRegisterListParametersPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMapRegisterListParametersPro', maptype.HMAPREG, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _number: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapMapRegisterListParametersPro_t (_hmapreg, _number, _mapreg, _datum, _ellparm, _ttype, _tparm)


# Добавить запись параметров системы координат
# hmapreg - идентификатор списка параметров систем координат
# name - уникальное название системы отсчета
# comment - комментарий для системы отсчета или ноль
# epsgcode - код EPSG или ноль
# ident - идентификатор системы отсчета или ноль
# mapreg - описание параметров системы отсчета
# datum - описание параметров датума или ноль
# ellparam - описание параметров эллипсоида или ноль
# ttype - тип локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат
# При ошибке возвращает ноль

    mapAppendMapRegisterListParametersPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendMapRegisterListParametersPro', maptype.HMAPREG, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapAppendMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _epsgcode: int, _ident: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapAppendMapRegisterListParametersPro_t (_hmapreg, _name.buffer(), _comment.buffer(), _epsgcode, _ident.buffer(), _mapreg, _datum, _ellparm, _ttype, _tparm)


# Удалить запись параметров систем отсчета по порядковому номеру в списке
# hmapreg - идентификатор списка параметров систем координат
# number  - порядковый номер записи параметров c 1
# Для немедленного изменения данных в файле нужно вызвать функцию mapCommitMapRegisterList
# При ошибке возвращает ноль

    mapDeleteMapRegisterListParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteMapRegisterListParameters', maptype.HMAPREG, ctypes.c_long)
    def mapDeleteMapRegisterListParameters(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        return mapDeleteMapRegisterListParameters_t (_hmapreg, _number)


# Обновить название, комментарий и код системы отсчета по заданному порядковому номеру
# hmapreg - идентификатор списка параметров систем координат
# number - порядковый номер записи параметров c 1
# name - название системы отсчета или 0 (не менять)
# comment - комментарий к системе отсчета или 0 (не менять)
# code - код EPSG или 0 (не менять)
# ident - идентификатор системы отсчета или 0 (не менять)
# При ошибке возвращает ноль

    mapUpdateMapRegisterListNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR)
    def mapUpdateMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _code: int, _ident: mapsyst.WTEXT) -> int:
        return mapUpdateMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _comment.buffer(), _code, _ident.buffer())


# Сохранить изменения списка параметров систем отсчета в файле
# hmapreg - идентификатор списка параметров систем координат
# При ошибке возвращает ноль

    mapCommitMapRegisterList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitMapRegisterList', maptype.HMAPREG)
    def mapCommitMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        return mapCommitMapRegisterList_t (_hmapreg)


# Отменить изменения списка параметров систем отсчета в памяти
# hmapreg - идентификатор списка параметров систем координат
# Отмена изменений может быть выполнена до вызова mapCommitMapRegisterList
# При ошибке возвращает ноль

    mapUndoMapRegisterList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUndoMapRegisterList', maptype.HMAPREG)
    def mapUndoMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        return mapUndoMapRegisterList_t (_hmapreg)


# Запросить название листа на котором расположен объект
# hobj - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapListNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapListNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapListNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapListNameUn_t (_hobj, _name.buffer(), _size)


# Запросить номенклатуру листа на котором расположен объект
# hobj - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapNomenclatureUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapNomenclatureUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapNomenclatureUn_t (_hobj, _name.buffer(), _size)


# Запросить базовый масштаб карты
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapObjectMapScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectMapScale', maptype.HOBJ)
    def mapObjectMapScale(_hobj: maptype.HOBJ) -> int:
        return mapObjectMapScale_t (_hobj)


# Запросить идентификатор классификатора карты, содержащей объект
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetRscIdentByObject_t = mapsyst.GetProcAddress(curLib,maptype.HRSC,'mapGetRscIdentByObject', maptype.HOBJ)
    def mapGetRscIdentByObject(_hobj: maptype.HOBJ) -> maptype.HRSC:
        return mapGetRscIdentByObject_t (_hobj)


# Запросить уникальный номер объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapObjectKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectKey', maptype.HOBJ)
    def mapObjectKey(_hobj: maptype.HOBJ) -> int:
        return mapObjectKey_t (_hobj)


# Установить уникальный номер объекта
# hobj - идентификатор объекта карты в памяти
# number - уникальный номер объекта в листе
# Программа, вызывающая данную функцию, должна обеспечить уникальность номеров в листе
# Для резервирования уникального номера объекта в листе до вызова mapCommitObject можно
# вызвать функцию mapGetSiteNewObjectKey()
# При ошибке возвращает ноль

    mapSetObjectKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectKey', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectKey(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapSetObjectKey_t (_hobj, _number)


# Запросить классификационный код объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль, ноль допустим для нового объекта до вызова mapCommitObject()

    mapObjectExcode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectExcode', maptype.HOBJ)
    def mapObjectExcode(_hobj: maptype.HOBJ) -> int:
        return mapObjectExcode_t (_hobj)


# Запросить характер локализации объекта
# hobj - идентификатор объекта карты в памяти

    mapObjectLocal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectLocal', maptype.HOBJ)
    def mapObjectLocal(_hobj: maptype.HOBJ) -> int:
        return mapObjectLocal_t (_hobj)


# Запросить условное название объекта
# hobj - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapObjectNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectNameUn_t (_hobj, _name.buffer(), _size)


# Сформировать строку с описанием объекта
# hobj - идентификатор объекта карты в памяти
# comment - адрес буфера для результата запроса
# size - размер буфера в байтах
# Cтрока с описанием объекта имеет вид:
#     "номер_объекта - имя_объекта - имя_слоя - имя_листа_карты"
# При ошибке возвращает ноль

    mapObjectComment_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectComment', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectComment(_hobj: maptype.HOBJ, _comment: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectComment_t (_hobj, _comment.buffer(), _size)


# Запросить текущее направление цифрования контура объекта
# hobj - идентификатор объекта карты в памяти
# Возвращает:
#    OD_UNDEFINED (1) - не определено (незамкнутый контур или контур,
#                       вырожденный в точку или контур, имеющий "петли")
#    0D_RIGHT     (2) - объект справа (основной контур замкнутого объекта
#                       по часовой стрелке)
#    0D_LEFT      (4) - объект слева (основной контур замкнутого объекта
#                       против часовой стрелки)
# При ошибке возвращает ноль

    mapObjectDirect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectDirect', maptype.HOBJ)
    def mapObjectDirect(_hobj: maptype.HOBJ) -> int:
        return mapObjectDirect_t (_hobj)


# Запросить текущее направление цифрования контура подобъекта
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта (для объекта - равен нулю)
# Возвращает:
#    OD_UNDEFINED (1) - не определено (незамкнутый контур или контур,
#                       вырожденный в точку или контур, имеющий "петли")
#    0D_RIGHT     (2) - объект справа (замкнутый контур объекта
#                       по часовой стрелке)
#    0D_LEFT      (4) - объект слева (замкнутый контур объекта
#                       против часовой стрелки)
# При ошибке возвращает ноль

    mapSubjectDirect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSubjectDirect', maptype.HOBJ, ctypes.c_long)
    def mapSubjectDirect(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapSubjectDirect_t (_hobj, _subject)


# Запросить номер слоя объекта
# hobj - идентификатор объекта карты в памяти
# Номера слоев начинаются с ноля
# При ошибке возвращает ноль

    mapSegmentNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSegmentNumber', maptype.HOBJ)
    def mapSegmentNumber(_hobj: maptype.HOBJ) -> int:
        return mapSegmentNumber_t (_hobj)


# Запросить название слоя объекта
# hobj - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapSegmentNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSegmentNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapSegmentNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSegmentNameUn_t (_hobj, _name.buffer(), _size)


# Запросить класс объекта в дереве слоев и классов
# hobj - идентификатор объекта карты в памяти
# Если объект не включен в дерево слоев - возвращает ноль
# При ошибке возвращает ноль

    mapObjectClassNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectClassNumber', maptype.HOBJ)
    def mapObjectClassNumber(_hobj: maptype.HOBJ) -> int:
        return mapObjectClassNumber_t (_hobj)


# Запросить название класса объекта (название подслоя в дереве слоев)
# hobj - идентификатор объекта карты в памяти
# name - адрес буфера для результата запроса
# size - размер буфера в байтах
# Если объект не включен в дерево слоев - возвращает ноль
# При ошибке возвращает ноль

    mapObjectClassName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectClassName', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapObjectClassName(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectClassName_t (_hobj, _name.buffer(), _size)


# Запросить внутренний код объекта в классификаторе
# hobj - идентификатор объекта карты в памяти
# При удалении объектов классификатора внутренние коды объектов
# могут изменяться. Внутренний код может использоваться для
# идентификации объекта классификатора только в течение одного
# сеанса работы с картой при неизменном классификаторе
# При ошибке возвращает ноль, ноль допустим для нового объекта и для графического объекта

    mapObjectCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectCode', maptype.HOBJ)
    def mapObjectCode(_hobj: maptype.HOBJ) -> int:
        return mapObjectCode_t (_hobj)


# Запросить уникальный идентификатор объекта GUID
# hobj - идентификатор объекта карты в памяти
# ident - поле для записи идентификатора (32 шестнадцатеричных символов от 0 до F)
# size - размер поля в байтах
# Идентификатор GUID может автоматически присваиваться объектам карты,
# если установлен признак ведения GUID (например, mapSetAutoObjectGUID())
# Идентификатор хранится в семантике объекта с кодом 32799
# При ошибке возвращает 0

    mapObjectGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectGUID', maptype.HOBJ, ctypes.c_char_p, ctypes.c_long)
    def mapObjectGUID(_hobj: maptype.HOBJ, _ident: ctypes.c_char_p, _size: int) -> int:
        return mapObjectGUID_t (_hobj, _ident, _size)


# Проверить наличие GUID и создать при необходимости
# hobj - идентификатор объекта карты в памяти
# force - признак принудительного заполнения или замены GUID в семантике 32799
# Если значение семантики не соответствует формату GUID - выполняется принудительное обновление семантики
# Если изменений семантики нет - возвращает ноль

    mapCheckObjectGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckObjectGUID', maptype.HOBJ, ctypes.c_long)
    def mapCheckObjectGUID(_hobj: maptype.HOBJ, _force: int) -> int:
        return mapCheckObjectGUID_t (_hobj, _force)


# Установить значение границ видимости по классификатору объектов
# hobj - идентификатор объекта карты в памяти

    mapClearBotTop_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearBotTop', maptype.HOBJ)
    def mapClearBotTop(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapClearBotTop_t (_hobj)


# Установить масштаб нижней границы видимости на карте
# hobj - идентификатор объекта карты в памяти
# scale - знаменатель масштаба отображения от 1:1 до 1:40 000 000

    mapSetObjectBotScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectBotScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectBotScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectBotScale_t (_hobj, _scale)


# Запросить масштаб нижней границы видимости на карте
# hobj - идентификатор объекта карты в памяти

    mapObjectTopScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectTopScale', maptype.HOBJ)
    def mapObjectTopScale(_hobj: maptype.HOBJ) -> int:
        return mapObjectTopScale_t (_hobj)


# Установить масштаб верхней границы видимости на карте
# hobj - идентификатор объекта карты в памяти
# scale - знаменатель масштаба отображения от 1:1 до 1:40 000 000

    mapSetObjectTopScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectTopScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectTopScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectTopScale_t (_hobj, _scale)


# Запросить масштаб верхней границы видимости на карте
# hobj - идентификатор объекта карты в памяти

    mapObjectBotScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectBotScale', maptype.HOBJ)
    def mapObjectBotScale(_hobj: maptype.HOBJ) -> int:
        return mapObjectBotScale_t (_hobj)


# Запросить, являются ли границы видимости объекта уникальными
# hobj - идентификатор объекта карты в памяти
# Уникальные границы устанавливаются при вызове mapSetObjectTopScale() и mapSetObjectBotScale()
# Если границы видимости беруться из классификатора - возвращает ноль

    mapObjectBotTopUniqueness_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectBotTopUniqueness', maptype.HOBJ)
    def mapObjectBotTopUniqueness(_hobj: maptype.HOBJ) -> int:
        return mapObjectBotTopUniqueness_t (_hobj)


# Зарегистрировать объекта в классификаторе по внешнему коду и локализации
# hobj - идентификатор объекта карты в памяти
# excode - внешний код объекта,
# local - локализация метрики объекта:
#         LOCAL_LINE (линейны), LOCAL_SQUARE (площадной, или полигон), LOCAL_POINT (точечный) ...
# Обычно вызывается после mapCreateObject(...)
# При ошибке возвращает ноль

    mapRegisterObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRegisterObject(_hobj: maptype.HOBJ, _excode: int, _local: int) -> int:
        return mapRegisterObject_t (_hobj, _excode, _local)


# Сформировать описание нового объекта по короткому имени объекта
# hobj - идентификатор объекта карты в памяти
# name - символьный код объекта в классификаторе (до 31 символа)
# Обычно вызывается после mapCreateObject(...)
# При ошибке возвращает ноль

    mapRegisterObjectByKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterObjectByKey', maptype.HOBJ, ctypes.c_char_p)
    def mapRegisterObjectByKey(_hobj: maptype.HOBJ, _name: ctypes.c_char_p) -> int:
        return mapRegisterObjectByKey_t (_hobj, _name)


# Сформировать описание нового объекта по внутреннему коду объекта
# hobj - идентификатор объекта карты в памяти
# code - внутренний код объекта
# При ошибке возвращает ноль

    mapDescribeObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDescribeObject', maptype.HOBJ, ctypes.c_long)
    def mapDescribeObject(_hobj: maptype.HOBJ, _code: int) -> int:
        return mapDescribeObject_t (_hobj, _code)


# Сформировать описание нового графического объекта по номеру слоя и локализации
# hobj - идентификатор объекта карты в памяти
# layer - порядковый номер слоя в классификаторе с 0
# local - локализация метрики объекта: LOCAL_LINE, LOCAL_SQUARE, LOCAL_POINT...
# Вызывается после mapCreateObject(...)
# Для формирования условного знака необходимо использовать функцию mapAppendDraw(...)
# При ошибке возвращает ноль

    mapRegisterDrawObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterDrawObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRegisterDrawObject(_hobj: maptype.HOBJ, _layer: int, _local: int) -> int:
        return mapRegisterDrawObject_t (_hobj, _layer, _local)


# Установить номер листа для нового объекта
# hobj - идентификатор объекта карты в памяти
# list - последовательный номер листа с 1
# Обнуляет последовательный и уникальный номера объекта
# При ошибке возвращает ноль

    mapSetObjectListNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectListNumber', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectListNumber(_hobj: maptype.HOBJ, _list: int) -> int:
        return mapSetObjectListNumber_t (_hobj, _list)


# Запросить номер листа для объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetListNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetListNumber', maptype.HOBJ)
    def mapGetListNumber(_hobj: maptype.HOBJ) -> int:
        return mapGetListNumber_t (_hobj)


# Запросить формат хранения метрики
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль, иначе - тип формата хранения метрики (IDLONG2, IDLONG3, IDDOUBLE2, IDDOUBLE3 ...)

    mapGetObjectKind_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectKind', maptype.HOBJ)
    def mapGetObjectKind(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectKind_t (_hobj)


# Установить тип и размерность метрики объекта
# hobj - идентификатор объекта карты в памяти
# kind - тип метрики: IDLONG2, IDLONG3, IDDOUBLE2, IDDOUBLE3, IDDOUBLE4, IDDOUBLE4F
# Преобразование метрики из типа IDDOUBLE4 и IDDOUBLE4F не выполняется, если число точек больше нуля
# Для удаления 4-го измерения применяется функция mapDeletePointMeasurement4D
# Пересчет выполняется с сохранением существующих координат
# При ошибке возвращает ноль

    mapSetObjectKind_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectKind', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectKind(_hobj: maptype.HOBJ, _kind: int) -> int:
        return mapSetObjectKind_t (_hobj, _kind)


# Удалить из метрики измерение 4D
# Метрика приводится к типу IDDOUBLE3
# При ошибке возвращает ноль

    mapDeletePointMeasurement4D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeletePointMeasurement4D', maptype.HOBJ)
    def mapDeletePointMeasurement4D(_hobj: maptype.HOBJ) -> int:
        return mapDeletePointMeasurement4D_t (_hobj)


# Запросить описание объекта в виде двоичной записи для передачи по сети
# hobj - идентификатор объекта карты в памяти
# buffer - адрес памяти для размещения результата
# size - размер выделенной памяти для контроля
# Может применяться для переноса объекта на другую карту той же проекции (ограничение данной версии)
# Передача объекта может выполняться между различными потоками, процессами, компьютерами
# по соответствующим протоколам
# При ошибке возвращает ноль

    mapGetObjectRecord_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectRecord', maptype.HOBJ, ctypes.c_char_p, ctypes.c_long)
    def mapGetObjectRecord(_hobj: maptype.HOBJ, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetObjectRecord_t (_hobj, _buffer, _size)


# Запросить длину описания объекта в виде записи
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectRecordLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectRecordLength', maptype.HOBJ)
    def mapGetObjectRecordLength(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectRecordLength_t (_hobj)


# Создать объект на указанной карте из записи объекта
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# buffer - адрес области памяти с записью объекта, созданной в mapGetObjectRecord
# mode  - режим создания:
#     0 - записать,как новый;
#     1 - заменить объект при совпадении Key();
#     4 - создать в памяти,как новый,
#     5 - заменить объект при совпадении Key() в памяти;
# Для режимов 4 и 5 требуется последующий вызов mapCommitObject()
# После завершения использования объекта необходимо освободить ресурсы функцией mapFreeObject()
# При ошибке возвращает ноль, иначе - идентификатор созданного объекта

    mapPutObjectRecord_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapPutObjectRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapPutObjectRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int, _mode: int) -> maptype.HOBJ:
        return mapPutObjectRecord_t (_hmap, _hsite, _buffer, _size, _mode)


# Сформировать дамп объекта
# hobj - идентификатор объекта карты в памяти
# filename - имя файла дампа или ноль (в этом случае имя будет - \LOG\имя_карты.номер_объекта.dump)
# Если имя не задано, то дамп обновляется не чаще 1 раз в 5 минут
# При ошибке возвращает ноль

    mapSaveObjectDump_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveObjectDump', maptype.HOBJ, maptype.PWCHAR)
    def mapSaveObjectDump(_hobj: maptype.HOBJ, _filename: mapsyst.WTEXT) -> int:
        return mapSaveObjectDump_t (_hobj, _filename.buffer())


# Запросить порядковый номер объекта в карте
# hobj - идентификатор объекта карты в памяти
# Если объект только создан и метод mapCommitObject() не вызывался - возвращает ноль
# При ошибке возвращает ноль

    mapGetObjectNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectNumber', maptype.HOBJ)
    def mapGetObjectNumber(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectNumber_t (_hobj)


# Очистить порядковый номер объекта в карте
# hobj - идентификатор объекта карты в памяти
# Очистка номера приводит к тому, что в mapCommitObject объект записывается как новый, но без изменения
# уникального номера объекта, который в этом случае должен устанавливаться через mapSetObjectKey
# При вызове mapCopyObjectAsNew уникальный номер объекта устанавливается автоматически
# как автоинкрементное поле от предыдущего максимального значения
# При ошибке возвращает ноль

    mapClearObjectNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearObjectNumber', maptype.HOBJ)
    def mapClearObjectNumber(_hobj: maptype.HOBJ) -> int:
        return mapClearObjectNumber_t (_hobj)


# Запросить положение объекта в документе
# hobj - идентификатор объекта карты в памяти
# desc - положение объекта в документе (номер листа, номер объекта, идентификатор карты)
# При ошибке возвращает ноль

    mapObjectDescribe_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectDescribe', maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapObjectDescribe(_hobj: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        return mapObjectDescribe_t (_hobj, _desc)


# Прочитать объект по заданному положению в документе
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# desc - положение объекта в документе
# При ошибке возвращает ноль

    mapReadObjectByDescribe_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadObjectByDescribe', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapReadObjectByDescribe(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        return mapReadObjectByDescribe_t (_hmap, _hobj, _desc)


# Запросить уникальный идентификатор вида объекта в классификаторе
# hobj - идентификатор объекта карты в памяти
# key - адрес буфера для записи результата
# size - длина строки
# При ошибке возвращает ноль

    mapObjectRscKeyUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectRscKeyUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectRscKeyUn(_hobj: maptype.HOBJ, _key: mapsyst.WTEXT, _size: int) -> int:
        return mapObjectRscKeyUn_t (_hobj, _key.buffer(), _size)


# Установить признак общей метрики объекта из объекта источника
# hobj - идентификатор объекта карты в памяти
# hsource - идентификатор объекта c исходной эталонной метрикой или 0
# Если после установки общей метрики будет отредактирована метрика
# клона, то изменится и метрика эталонного объекта
# При удалении эталонного объекта будет удаляться и клон
# При переносе объектов на другой лист (другую карту) признак клонирования сбрасывается
# и должен отслеживаться и устанавливаться программой, выполняющей перенос - mapSetObjectMetricDuplication()
# После установки общей метрики нужно сохранить (в mapCommitObject()) оба объекта - hobj и hsource
# При ошибке возвращает ноль

    mapSetObjectMetricDuplicationForObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectMetricDuplicationForObject', maptype.HOBJ, maptype.HOBJ)
    def mapSetObjectMetricDuplicationForObject(_hobj: maptype.HOBJ, _hsource: maptype.HOBJ) -> int:
        return mapSetObjectMetricDuplicationForObject_t (_hobj, _hsource)


# Cбросить признак общей метрики в объекте - эталоне и перевести клон на свою метрику
# hobj - идентификатор объекта карты в памяти - эталон метрики
# Если объект не ссылаются на общую метрику - возвращает -2
# Если объект был клоном - возвращает -1
# Если объект был эталоном для клонов - возвращает 1, клон пересохраняется со своей метрикой
# Если функция вернула ненулевое значение, то после завершения других операций редактирования
# нужно вызвать mapCommitObject
# При ошибке возвращает ноль

    mapClearMetricDuplicationForClone_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearMetricDuplicationForClone', maptype.HOBJ)
    def mapClearMetricDuplicationForClone(_hobj: maptype.HOBJ) -> int:
        return mapClearMetricDuplicationForClone_t (_hobj)


# Запросить идентификатор дубликата метрики, если метрика объекта дублируется в другом объекте
# hobj  - идентификатор объекта карты в памяти
# ismainclone - признак объекта - эталона метрики
# Применяется при восстановлении признака клонирования метрики в различных процедурах обработки объектов
# При ошибке возвращает ноль

    mapGetObjectMetricDuplication_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectMetricDuplication', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapGetObjectMetricDuplication(_hobj: maptype.HOBJ, _ismainclone: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetObjectMetricDuplication_t (_hobj, _ismainclone)


# Запросить признак размещения записи метрики по смещению более 4 Гб от начала файла
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectBigMetric_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectBigMetric', maptype.HOBJ)
    def mapGetObjectBigMetric(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectBigMetric_t (_hobj)


# Установить признак увеличения графического объекта при приближении карты на экране
# hobj - идентификатор объекта карты в памяти
# scale - признак увеличения объекта на масштабах, крупнее базового масштаба карты: 0 или 1
# Применяется только для графических объектов, имеющих внутренний код равный нулю
# Для объектов из классификатора значение игнорируется
# При ошибке возвращает ноль

    mapSetObjectScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        return mapSetObjectScale_t (_hobj, _scale)


# Запросить признак увеличения графического объекта при приближении карты на экране
# hobj - идентификатор объекта карты в памяти

    mapGetObjectScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectScale', maptype.HOBJ)
    def mapGetObjectScale(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectScale_t (_hobj)


# Установить графическому объекту признак "Не сжимать"
# hobj - идентификатор объекта карты в памяти
# dontpress - значение признака: 1 - для установки признака "Не сжимать", 0 - для сброса признака
# Применяется только для графических объектов, имеющих внутренний код равный нулю
# Разрешает уменьшение объекта при сжатии карты мельче базового масштаба
# Для объектов из классификатора значение игнорируется
# При ошибке возвращает ноль

    mapSetObjectPress_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectPress', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectPress(_hobj: maptype.HOBJ, _dontpress: int) -> int:
        return mapSetObjectPress_t (_hobj, _dontpress)


# Запросить признак "Не сжимать"
# hobj - идентификатор объекта карты в памяти
# Применяется только для графических объектов, имеющих внутренний код равный нулю
# Разрешает уменьшение объекта при сжатии карты мельче базового масштаба
# При ошибке возвращает ноль

    mapGetObjectPress_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectPress', maptype.HOBJ)
    def mapGetObjectPress(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectPress_t (_hobj)


# Установить способ отображения метрики объекта в виде динамического сплайна
# hobj - идентификатор объекта карты в памяти
# type - тип сплайна: SPLINETYPE_SMOOTH - сглаживает углы, SPLINETYPE_POINTS - дуги по точкам
# При ошибке или отмене рисования сплайна возвращает ноль

    mapSetObjectSpline_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectSpline', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectSpline(_hobj: maptype.HOBJ, _type: int) -> int:
        return mapSetObjectSpline_t (_hobj, _type)


# Запросить способ отображения метрики объекта в виде динамического сплайна
# hobj - идентификатор объекта карты в памяти
# При ошибке или отмене рисования сплайна возвращает ноль

    mapGetObjectSpline_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectSpline', maptype.HOBJ)
    def mapGetObjectSpline(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectSpline_t (_hobj)


# Установить признак выравнивания подобъекта векторного знака или подписи по вертикали
# hobj - идентификатор объекта карты в памяти
# flag - выравнивания первой точки подобъекта по первой точке объекта по вертикали: 0 или 1
# При отображении первая точка метрики подобъекта выравнивается по вертикали
# по первой точке метрики объекта для векторных знаков и подписей
# При ошибке возвращает ноль

    mapSetObjectVerticalAlignment_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectVerticalAlignment', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectVerticalAlignment(_hobj: maptype.HOBJ, _flag: int) -> int:
        return mapSetObjectVerticalAlignment_t (_hobj, _flag)


# Запросить признак выравнивания подобъекта векторного знака или подписи по вертикали
# hobj - идентификатор объекта карты в памяти
# При отображении первая точка метрики подобъекта выравнивается по вертикали
# по первой точке метрики объекта для векторных знаков и подписей
# При ошибке возвращает ноль

    mapGetObjectVerticalAlignment_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectVerticalAlignment', maptype.HOBJ)
    def mapGetObjectVerticalAlignment(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectVerticalAlignment_t (_hobj)


# Запросить признак отображать объект Выше всех
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectShowUp_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectShowUp', maptype.HOBJ)
    def mapGetObjectShowUp(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectShowUp_t (_hobj)


# Установить признак отображать объект Выше всех
# hobj - идентификатор объекта карты в памяти
# flag - признак Выше всех: 0 или 1
# Объекты любой локализации с признаком Выше всех всегда отображаются после
# всех других объектов одной с ними карты
# При ошибке возвращает ноль

    mapSetObjectShowUp_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectShowUp', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectShowUp(_hobj: maptype.HOBJ, _flag: int) -> int:
        return mapSetObjectShowUp_t (_hobj, _flag)


# Запросить признак отображать объект Ниже всех
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetObjectShowDown_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectShowDown', maptype.HOBJ)
    def mapGetObjectShowDown(_hobj: maptype.HOBJ) -> int:
        return mapGetObjectShowDown_t (_hobj)


# Установить признак отображать объект Ниже всех
# hobj - идентификатор объекта карты в памяти
# flag - признак Ниже всех: 0 или 1
# Объекты любой локализации с признаком Ниже всех всегда отображаются до
# всех других объектов одной с ними карты
# При ошибке возвращает ноль

    mapSetObjectShowDown_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectShowDown', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectShowDown(_hobj: maptype.HOBJ, _flag: int) -> int:
        return mapSetObjectShowDown_t (_hobj, _flag)


# Запросить число семантических характеристик (семантик) у объекта
# hobj - идентификатор объекта карты в памяти
# Одна семантическая характеристика записывается в виде последовательности: числовой код
# семантики и значение семантики
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# По числовому коду из классификатора RSC можно запросить описание семантики, аналогичное описанию
# поля в таблице базы данных: ключ (имя поля), название, формат, точность, описание справочника
# и другие свойства
# При ошибке возвращает ноль

    mapSemanticAmount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticAmount', maptype.HOBJ)
    def mapSemanticAmount(_hobj: maptype.HOBJ) -> int:
        return mapSemanticAmount_t (_hobj)


# Запросить по номеру название семантической характеристики объекта
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер семантики c 1
# name - адрес буфера для записи названия семантики
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapSemanticFullName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticFullName', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticFullName(_hobj: maptype.HOBJ, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticFullName_t (_hobj, _number, _name.buffer(), _size)


# Найти номер семантики для экземпляра объекта по ее коду
# hobj - идентификатор объекта карты в памяти
# code - код семантики
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# При ошибке возвращает ноль

    mapSemanticNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticNumber', maptype.HOBJ, ctypes.c_long)
    def mapSemanticNumber(_hobj: maptype.HOBJ, _code: int) -> int:
        return mapSemanticNumber_t (_hobj, _code)


# Запросить код семантики по ее номеру для экземпляра объекта с проверкой сервисных семантик
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер семантики c 1
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# Для сервисной семантики (код от TEMPSEMANTICFIRST до TEMPSEMANTICFIRST),
# выполняется подбор кода по ключу из классификатора (классификатор могли дополнить после формирования карты)
# Сервисные семантики могут формироваться, например, при импорте данных из обменных форматов,
# когда по имени поля не найден подходящий код семантики в классификаторе RSC
# Сервисная семантика хранится в формате "имя_поля:значение"
# При ошибке возвращает ноль

    mapSemanticCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCode', maptype.HOBJ, ctypes.c_long)
    def mapSemanticCode(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapSemanticCode_t (_hobj, _number)


# Запросить код семантики по ее номеру для экземпляра объекта
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер семантики c 1
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# При ошибке возвращает ноль

    mapRealSemanticCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRealSemanticCode', maptype.HOBJ, ctypes.c_long)
    def mapRealSemanticCode(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapRealSemanticCode_t (_hobj, _number)


# Запросить, является ли семантика строкой UTF16
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# Если семантика в кодировке UTF16 - возвращает ненулевое значение

    mapIsSemanticUnicode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSemanticUnicode', maptype.HOBJ, ctypes.c_long)
    def mapIsSemanticUnicode(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapIsSemanticUnicode_t (_hobj, _number)


# Запросить по номеру значение семантики в виде строки
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# place - адрес буфера для записи семантики
# size - длина буфера в байтах
# separator - разделитель целой и дробной части для числового значения:
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# Значение преобразуется в символьный вид без раскодирования семантик типа справочник
# Значение семантики типа справочник будет прочитано в виде числового кода справочника
# При ошибке возвращает ноль

    mapSemanticValuePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticValuePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticValuePro(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int, _separator: int) -> int:
        return mapSemanticValuePro_t (_hobj, _number, _place.buffer(), _size, _separator)


# Запросить по номеру значение семантики в символьном раскодированном виде
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# place - адрес буфера для записи семантики
# size - длина буфера в байтах
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# error - поле для записи ошибки после анализа значения или 0
# Коды ошибок: IDS_STRUCT - значение поля не соответствует формату (нечисловые символы вместо числа и т.п.),
#              IDS_VALUEOUTSIDE - нарушение ожидаемого диапазона значений
# Например: для семантики типа справочник "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# При ошибке возвращает ноль, иначе - код семантики

    mapSemanticValueNamePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticValueNamePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSemanticValueNamePro(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int, _separator: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapSemanticValueNamePro_t (_hobj, _number, _place.buffer(), _size, _separator, _error)


# Запросить по номеру значение семантики в виде числа с плавающей точкой
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticDoubleValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSemanticDoubleValue', maptype.HOBJ, ctypes.c_long)
    def mapSemanticDoubleValue(_hobj: maptype.HOBJ, _number: int) -> float:
        return mapSemanticDoubleValue_t (_hobj, _number)


# Запросить по номеру значение семантики в виде целого числа
# hobj - идентификатор объекта карты в памяти
# number  - последовательный номер характеристики
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticLongIntValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSemanticLongIntValue', maptype.HOBJ, ctypes.c_int)
    def mapSemanticLongIntValue(_info: maptype.HOBJ, _number: int) -> int:
        return mapSemanticLongIntValue_t (_info, _number)

    mapSemanticLongValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSemanticLongValue', maptype.HOBJ, ctypes.c_long)
    def mapSemanticLongValue(_hobj: maptype.HOBJ, _number: int) -> float:
        return mapSemanticLongValue_t (_hobj, _number)


# Запросить по номеру значение семантики в символьном раскодированном виде
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# place - адрес буфера для записи значения семантики
# size - длина буфера в байтах
# Например: для семантики типа справочник "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# При ошибке возвращает ноль, иначе - код семантики

    mapSemanticValueNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticValueNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticValueNameUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticValueNameUn_t (_hobj, _number, _place.buffer(), _size)


# Запросить по номеру значение семантики в раскодированном виде с единицей измерения
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# place - адрес буфера для записи значения семантики
# size - длина буфера в байтах
# Например: для семантики типа справочник "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# Для числовой семантики "ВЫСОТА" значение "205,5" заменется на "205,5 м"
# При ошибке возвращает ноль

    mapSemanticValueFullNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticValueFullNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticValueFullNameUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticValueFullNameUn_t (_hobj, _number, _place.buffer(), _size)


# Запросить по коду семантики значение в виде строки
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи значения семантики или 0
# size - длина буфера в байтах или 0
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Значение семантики преобразуется в символьный вид без раскодирования справочников
# Например: код "code" имеют 3-я и 6-я характеристики, соответственно для
# number = 1 вернется значение семантики 3, для number = 2 - семаники 6, для number = 3 вернется ноль
# Семантика с одним кодом может иметь несколько значений, если в классификаторе RSC для нее
# установлено свойство Разрешается повторение
# Чтобы найти семантику с нужным кодом без запроса значения - необходимо передать параметры
# place и size равными нулю
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeValueUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeValueUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValueUn(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int) -> int:
        return mapSemanticCodeValueUn_t (_hobj, _code, _place.buffer(), _size, _number)


# Запросить по коду семантики значение в виде строки с разделителем для числа
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи значения семантики или 0
# size - длина буфера в байтах или 0
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# Например: код "code" имеют 3-я и 6-я характеристики, соответственно для
# number = 1 вернется значение семантики 3, для number = 2 - семаники 6, для number = 3 вернется ноль
# Семантика с одним кодом может иметь несколько значений, если в классификаторе RSC для нее
# установлено свойство Разрешается повторение
# Чтобы найти семантику с нужным кодом без запроса значения - необходимо передать параметры
# place и size равными нулю
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeValuePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeValuePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValuePro(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int, _separator: int) -> int:
        if _place is None:
           return mapSemanticCodeValuePro_t (_hobj, _code, 0, 0, _number, 0) # Поиск номера семантики с заданным кодом
        else:
           return mapSemanticCodeValuePro_t (_hobj, _code, _place.buffer(), _size, _number, _separator)

# Запросить по коду значение семантики в символьном раскодированном виде
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи значения семантики
# size - длина буфера в байтах
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Например: для семантики типа справочник "СОСТОЯНИЕ" значение "5" заменется на "жилой"
# Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeValueNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeValueNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValueNameUn(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int) -> int:
        return mapSemanticCodeValueNameUn_t (_hobj, _code, _place.buffer(), _size, _number)


# Сформировать по коду значение семантики для подписывания
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи обработанного значения семантики или 0
# size - длина буфера в байтах или 0
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#             не равен последовательному номеру характеристики
# separator - разделитель целой и дробной части
#             0 - десятичную точку не изменять
#             1 - заменить десятичную точку на символ, установленный в системе
#             '.' или ',' - заменить десятичную точку на separator: '.' или ','
# Заполняет строку для подписи (place) в формате: "[префикс] <значение> [постфикс]"
# Если значение пусто, то префикс и постфикс не добавляются
# Например: - для названия озера может быть задан префикс "оз.":    "оз. Южное"
#           - для площади участка может быть задан постфикс "(га)": "1.2 (га)"
# Настройки текста подписи хранятся в классификаторе RSC
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeLabel_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeLabel', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeLabel(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int, _issystemdot: int) -> int:
        return mapSemanticCodeLabel_t (_hobj, _code, _place.buffer(), _size, _number, _issystemdot)


# Запросить по коду семантики значение в виде числа с плавающей точкой
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# value - поле для размещения результата запроса
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticCodeDoubleValueEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeDoubleValueEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapSemanticCodeDoubleValueEx(_hobj: maptype.HOBJ, _code: int, _value: ctypes.POINTER(ctypes.c_double), _number: int) -> int:
        return mapSemanticCodeDoubleValueEx_t (_hobj, _code, _value, _number)


# Запросить по коду семантики значение в виде числа с плавающей точкой
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticCodeDoubleValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSemanticCodeDoubleValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeDoubleValue(_hobj: maptype.HOBJ, _code: int, _number: int) -> float:
        return mapSemanticCodeDoubleValue_t (_hobj, _code, _number)


# Запросить по коду семантики значение в виде целого числа
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# value - поле для размещения результата запроса
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticCodeLongValueEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeLongValueEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapSemanticCodeLongValueEx(_hobj: maptype.HOBJ, _code: int, _value: ctypes.POINTER(ctypes.c_long), _number: int) -> int:
        return mapSemanticCodeLongValueEx_t (_hobj, _code, _value, _number)


# Запросить по коду семантики значение в виде целого числа
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Если значение семантики не может быть преобразовано к числовому виду
# или не найдено - возвращает ноль

    mapSemanticCodeLongValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeLongValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeLongValue(_hobj: maptype.HOBJ, _code: int, _number: int) -> int:
        return mapSemanticCodeLongValue_t (_hobj, _code, _number)


# Запросить по коду значение семантики типа справочник в виде ключа значения
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи значения семантики
# size - длина буфера в байтах
# Семантика типа справочник для каждого значения имеет числовой код, ключ, короткое обозначение и название
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Ключ и короткое обозначение имеют одинаковое назначение и позволяют использовать фактически 2 разных ключа
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeKeyValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeKeyValue', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeKeyValue(_hobj: maptype.HOBJ, _code: int, _place: ctypes.c_char_p, _size: int, _number: int) -> int:
        return mapSemanticCodeKeyValue_t (_hobj, _code, _place, _size, _number)


# Запросить по коду значение семантики типа справочник в виде короткое обозначения
# hobj - идентификатор объекта карты в памяти
# code - код семантики, для которой ищется значение
# place - адрес буфера для записи значения семантики
# size - длина буфера в байтах
# Семантика типа справочник для каждого значения имеет числовой код, ключ, короткое обозначение и название
# number - последовательный номер с 1 запрашиваемого значения среди семантик с тем же кодом,
#          не равен последовательному номеру характеристики
# Ключ и короткое обозначение имеют одинаковое назначение и позволяют использовать фактически 2 разных ключа
# При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики

    mapSemanticCodeShortName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticCodeShortName', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeShortName(_hobj: maptype.HOBJ, _code: int, _place: ctypes.c_char_p, _size: int, _number: int) -> int:
        return mapSemanticCodeShortName_t (_hobj, _code, _place, _size, _number)


# Запросить из RSC количество записей в семантике типа справочник по коду семантики
# hobj - идентификатор объекта карты в памяти
# code - код семантики типа справочник (TCODE)
# Описание семантики типа справочник запрашивается из классификатора формата RSC
# При ошибке возвращает ноль

    mapSemanticClassificatorCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticClassificatorCount', maptype.HOBJ, ctypes.c_long)
    def mapSemanticClassificatorCount(_hobj: maptype.HOBJ, _code: int) -> int:
        return mapSemanticClassificatorCount_t (_hobj, _code)


# Запросить название значения семантики типа справочник
# hobj - идентификатор объекта карты в памяти
# code - код семантики типа справочник (TCODE)
# number - последовательный номер в справочнике с 1
# place - адрес буфера для записи названия
# size - длина буфера в байтах
# При ошибке возвращает ноль

    mapSemanticClassificatorNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticClassificatorNameUn', maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticClassificatorNameUn(_hobj: maptype.HOBJ, _code: int, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        return mapSemanticClassificatorNameUn_t (_hobj, _code, _number, _place.buffer(), _size)


# Запросить код значения семантики типа справочник
# hobj - идентификатор объекта карты в памяти
# code - код семантики типа справочник (TCODE)
# number - последовательный номер значения в справочнике с 1
# При ошибке возвращает ноль

    mapSemanticClassificatorCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSemanticClassificatorCode', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticClassificatorCode(_hobj: maptype.HOBJ, _code: int, _number: int) -> int:
        return mapSemanticClassificatorCode_t (_hobj, _code, _number)


# Найти номер объекта в семантике для кодов SEMOBJECTTOTEXT, SEMOBJECTFROMTEXT
# hobj - идентификатор объекта карты в памяти
# code - поле для записи кода найденной семантики: SEMOBJECTTOTEXT или SEMOBJECTFROMTEXT
# number - поле для записи номера найденной семантики
# Возвращает значение найденной семантики - номер объекта или подписи
# При создании на карте подписи некоторой характеристики исходный объект и его подписи
# связываются через служебные семантики SEMOBJECTTOTEXT, SEMOBJECTFROMTEXT
# Значением этих семантик являютсяуникальные номера подписи и объекта соответственно
# Служебные семантики позволяют автоматически обновить текст пописи при обновлении семантики объекта
# При ошибке возвращает ноль

    mapFindTextGroup_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFindTextGroup', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapFindTextGroup(_hobj: maptype.HOBJ, _code: ctypes.POINTER(ctypes.c_long), _number: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapFindTextGroup_t (_hobj, _code, _number)


# Запросить количество видов семантик, которые еще могут быть добавлены для данного объекта
# hobj - идентификатор объекта карты в памяти
# Объекту могут быть добавлены те семантики, которые ему назначены в классификаторе RSC
# Если для семантики не установлено свойство Разрешается повторение, то она может быть
# у объекта только в одном экземпляре
# Результат запроса изменяется в процессе добавления семантик объекту
# При ошибке возвращает ноль

    mapAvailableSemanticCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAvailableSemanticCount', maptype.HOBJ)
    def mapAvailableSemanticCount(_hobj: maptype.HOBJ) -> int:
        return mapAvailableSemanticCount_t (_hobj)


# Запросить список кодов семантик, которые могут быть добавлены объекту
# hobj - идентификатор объекта карты в памяти
# list - указатель на область памяти для списка кодов семантик или 0
# count - максимальное число элементов в списке (размер буфера деленный на размер long int)
# Если count меньше требуемого числа семантик, то заполняться первые count семантик
# Возвращает число кодов доступных семантик на объект, которые могут быть записаны
# Если параметр list равен нулю, то функция только считает число доступных семантик
# При ошибке возвращает ноль

    mapAvailableSemanticList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAvailableSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapAvailableSemanticList(_hobj: maptype.HOBJ, _list: ctypes.POINTER(ctypes.c_long), _count: int) -> int:
        return mapAvailableSemanticList_t (_hobj, _list, _count)


# Запросить список кодов доступных обязательных семантик на объект
# hobj - идентификатор объекта карты в памяти
# list - указатель на область памяти для размещения списка кодов семантик
# count - максимальное число элементов в списке (размер буфера деленный на sizeof(long int))
# Семантики, которые назначены объекту в классификаторе RSC, могут быть обязательными и
# дополнительными. Все обязательные семантики необходимо заполнить при создании объекта
# При ошибке возвращает ноль

    mapAvailableMustSemanticList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAvailableMustSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapAvailableMustSemanticList(_hobj: maptype.HOBJ, _list: ctypes.POINTER(ctypes.c_long), _count: int) -> int:
        return mapAvailableMustSemanticList_t (_hobj, _list, _count)


# Добавить семантику объекту
# hobj - идентификатор объекта карты в памяти
# code - код семантической характеристики
# value - адрес строки, содержащей значение семантики в символьном виде
# size - длина добавляемой строки в байтах (если необходимо взять часть строки) или ноль
# Для семантики числового типа значения будут преобразовываться в двоичный вид
# Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
# Если такая семантика была и она не повторяемая - значение заменяется
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemantic_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSemantic', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapAppendSemantic(_hobj: maptype.HOBJ, _code: int, _value: ctypes.c_char_p, _size: int) -> int:
        return mapAppendSemantic_t (_hobj, _code, _value, _size)


# Добавить семантику объекту в кодировке UTF-16
# hobj - идентификатор объекта карты в памяти
# code - код семантической характеристики
# value - значение характеристики в кодировке UTF-16
# size - длина добавляемой строки в байтах, если нужно добавить подстроку, или 0
# Для семантики числового типа значения будут преобразовываться в двоичный вид
# Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
# Если такая семантика была и она не повторяемая - значение заменяется
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSemanticUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapAppendSemanticUn(_hobj: maptype.HOBJ, _code: int, _value: mapsyst.WTEXT, _size: int) -> int:
        return mapAppendSemanticUn_t (_hobj, _code, _value.buffer(), _size)


# Добавить произвольную характеристику в семантику объекта
# hobj - идентификатор объекта карты в памяти
# name - условное имя характеристики в кодировке UTF-16
# value - значение характеристики в кодировке UTF-16
# Применяется для записи произвольного атрибута в формате "имя_поля:значение" ("name:value")
# в кодировке UTF-16 с кодом 32862 (SEMSERVICECODE) или временным сервисным кодом в диапазоне
# от TEMPSEMANTICFIRST до TEMPSEMANTICFIRST
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendServiceSemantic_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendServiceSemantic', maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendServiceSemantic(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _value: mapsyst.WTEXT) -> int:
        return mapAppendServiceSemantic_t (_hobj, _name.buffer(), _value.buffer())


# Добавить семантику типа число
# hobj - идентификатор объекта карты в памяти
# code - код семантической характеристики
# value - значение в виде числа двойной точности
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticDouble_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSemanticDouble', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapAppendSemanticDouble(_hobj: maptype.HOBJ, _code: int, _value: float) -> int:
        return mapAppendSemanticDouble_t (_hobj, _code, _value)


# Добавить семантику типа целое число
# hobj - идентификатор объекта карты в памяти
# code - код семантической характеристики
# value - значение в виде целого числа
# При успешном выполнении возвращает последовательный номер созданной характеристики
# При ошибке возвращает ноль

    mapAppendSemanticLong_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSemanticLong', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapAppendSemanticLong(_hobj: maptype.HOBJ, _code: int, _value: int) -> int:
        return mapAppendSemanticLong_t (_hobj, _code, _value)


# Удалить по номеру семантику объекта
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики с 1,
#          если номер равен "-1", удаляются все характеристики
# При ошибке возвращает ноль

    mapDeleteSemantic_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSemantic', maptype.HOBJ, ctypes.c_long)
    def mapDeleteSemantic(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapDeleteSemantic_t (_hobj, _number)


# Изменить по номеру код семантики объекта
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики с 1
# code - новый код семантики
# При ошибке возвращает ноль, иначе - код семантики

    mapSetSemanticCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSemanticCode', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticCode(_hobj: maptype.HOBJ, _number: int, _code: int) -> int:
        return mapSetSemanticCode_t (_hobj, _number, _code)


# Изменить значение семантики типа число
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики с 1
# value - новое значение семантики
# При ошибке возвращает ноль

    mapSetSemanticDoubleValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSemanticDoubleValue', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapSetSemanticDoubleValue(_hobj: maptype.HOBJ, _number: int, _value: float) -> int:
        return mapSetSemanticDoubleValue_t (_hobj, _number, _value)


# Изменить значение семантики типа целое число
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики с 1
# value - новое значение семантики
# При ошибке возвращает ноль

    mapSetSemanticLongValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSemanticLongValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticLongValue(_hobj: maptype.HOBJ, _number: int, _value: int) -> int:
        return mapSetSemanticLongValue_t (_hobj, _number, _value)


# Изменить значение семантики объекта
# hobj - идентификатор объекта карты в памяти
# number - последовательный номер характеристики c 1
# place - адрес строки, содержащей новое значение в виде строки UTF16
# size - длина добавляемой строки в байтах, если нужно добавить подстроку,
#           или ноль - размер будет определен автоматически до замыкающего нуля
# Семантика числового типа будет автоматически преобразовываться в двоичный вид
# Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
# При ошибке возвращает ноль

    mapSetSemanticValueUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSemanticValueUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSetSemanticValueUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _maxsize: int) -> int:
        return mapSetSemanticValueUn_t (_hobj, _number, _place.buffer(), _maxsize)


# Обновить условный знак объекта при изменении семантических характеристик
# hobj - идентификатор объекта карты в памяти
# Данная функция выполняется автоматически при сохранении объекта функцией mapCommitObject()
# Если для кода объекта назначена серия объектов по семантике, то будет выполнен подбор
# подходящего условного знака
# Если вид объекта не изменился возвращает ноль

    mapRedefineObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRedefineObject', maptype.HOBJ)
    def mapRedefineObject(_hobj: maptype.HOBJ) -> int:
        return mapRedefineObject_t (_hobj)


# Обновить значения семантик типа формула при обновлении семантики или метрики объекта
# hobj - идентификатор объекта карты в памяти
# Применяется для обновления значений семантик типа формула, зависящих от других семантик и
# координат объекта
# Данная функция автоматически вызывается при сохранении объекта функцией mapCommitObject()
# При ошибке возвращает ноль

    mapUpdateSemanticByFormula_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateSemanticByFormula', maptype.HOBJ, ctypes.c_long)
    def mapUpdateSemanticByFormula(_hobj: maptype.HOBJ, _int: int) -> int:
        return mapUpdateSemanticByFormula_t (_hobj, _int)


# Запросить замкнутость объекта или подобъекта
# hobj - идентификатор объекта карты в памяти
# subject - номер объекта (0) или подобъекта (больше 0)
# Внешний контур полигона или первый контур мультилинии - это контур объекта,
# внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
# Возвращает:  0 - не замкнут, не 0 - замкнут

    mapGetExclusiveSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetExclusiveSubject', maptype.HOBJ, ctypes.c_long)
    def mapGetExclusiveSubject(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapGetExclusiveSubject_t (_hobj, _number)


# Запрос габаритов объекта в метрах в системе открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# dframe - поле для записи габаритов метрики объекта в метрах в системе документа
# Габариты перевычисляются по координатам объекта при каждом запросе
# Для полигона учитываются только внешние контура, для остальных локализаций - все контура
# При ошибке возвращает ноль

    mapObjectFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectFrame', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrame(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectFrame_t (_hobj, _dframe)


# Запрос габаритов объекта в радианах в системе WGS84
# hobj - идентификатор объекта карты в памяти
# dframe - поле для записи габаритов в радианах WGS84
# Габариты перевычисляются по координатам объекта при каждом запросе
# Для полигона учитываются только внешние контура, для остальных локализаций - все контура
# При ошибке возвращает ноль

    mapObjectFrameGeoWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectFrameGeoWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrameGeoWGS84(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapObjectFrameGeoWGS84_t (_hobj, _dframe)


# Запросить габариты подобъекта в метрах
# hobj - идентификатор объекта карты в памяти
# dframe - поле для записи габаритов подобъекта в метрах в системе документа
# subject - номер объекта (0) или подобъекта (больше 0)
# Внешний контур полигона или первый контур мультилинии - это контур объекта,
# внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
# Габариты перевычисляются при каждом запросе
# При ошибке возвращает ноль

    mapSubjectFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSubjectFrame', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapSubjectFrame(_hobj: maptype.HOBJ, _subject: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapSubjectFrame_t (_hobj, _subject, _dframe)


# Запрос габаритов изображения знака объекта в метрах
# hobj - идентификатор объекта карты в памяти
# dframe - поле для записи габаритов изображения объекта в метрах
# force  - признак принудительного пересчета габаритов, необходимо установить,
#          если объект редактировался, но не записан на карту
# Габариты считываются из заголовка объекта или перевычисляются по координатам объекта
# с учетом вида условного знака, если параметр force не равен нулю
# При ошибке возвращает ноль

    mapObjectViewFrameEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectViewFrameEx', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapObjectViewFrameEx(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME), _force: int) -> int:
        return mapObjectViewFrameEx_t (_hobj, _dframe, _force)


# Определить габаритную рамку изображения объекта в текущих условиях отображения
# hobj - идентификатор объекта карты в памяти
# hcontour - идентификатор объекта, в метрику которого заносятся габариты исходного объекта
# hpaint - идентификатор контекста отображения или 0
# Определяет габариты объектов (точечных, векторных и подписей) с учетом текущих
# условий отображения (масштаб, разрешение устройства вывода)
# Для каждого подобъекта подписи создается прямоугольный подобъект,
# ограничивающий текст подписи
# При ошибке возвращает 0

    mapGetObjectContour_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectContour', maptype.HOBJ, maptype.HOBJ, maptype.HPAINT)
    def mapGetObjectContour(_hobj: maptype.HOBJ, _hcontour: maptype.HOBJ, _hpaint: maptype.HPAINT) -> int:
        return mapGetObjectContour_t (_hobj, _hcontour, _hpaint)


# Запрос числа частей метрики (объект и подобъекты)
# hobj - идентификатор объекта карты в памяти
# Если подобъектов нет - возвращает 1 (только объект)
# При ошибке возвращает ноль

    mapPolyCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPolyCount', maptype.HOBJ)
    def mapPolyCount(_hobj: maptype.HOBJ) -> int:
        return mapPolyCount_t (_hobj)


# Запрос числа точек метрики объекта или подобъекта
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Внешний контур полигона или первый контур мультилинии - это контур объекта,
# внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
# При ошибке возвращает ноль

    mapPointCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPointCount', maptype.HOBJ, ctypes.c_long)
    def mapPointCount(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapPointCount_t (_hobj, _subject)


# Запросить геодезические координаты точки в радианах в системе документа
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - широта в радианах
#         DOUBLEPOINT::Y - долгота в радианах
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetGeoPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetGeoPoint_t (_hobj, _point, _number, _subject)


# Запросить геодезические координаты точки в радианах в системе координат карты
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - широта в радианах
#         DOUBLEPOINT::Y - долгота в радианах
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetMapGeoPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetMapGeoPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetMapGeoPoint_t (_hobj, _point, _number, _subject)


# Запросить геодезические координаты 2D точки в радианах на эллипсоиде WGS84
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - широта в радианах WGS84
#         DOUBLEPOINT::Y - долгота в радианах WGS84
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetGeoPointWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetGeoPointWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPointWGS84(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetGeoPointWGS84_t (_hobj, _point, _number, _subject)


# Запросить геодезические координаты 3D точки в радианах на эллипсоиде WGS84
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - широта в радианах WGS84
#         DOUBLEPOINT::Y - долгота в радианах WGS84
# heigth - поле для записи нормальной или ортометрической высоты (например, MSL) или 0
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetGeoPointWGS843D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetGeoPointWGS843D', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPointWGS843D(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _heigth: ctypes.POINTER(ctypes.c_double), _number: int, _subject: int) -> int:
        return mapGetGeoPointWGS843D_t (_hobj, _point, _heigth, _number, _subject)


# Запрос координат точки в метрах в системе координат карты
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - координата в метрах на север,
#         DOUBLEPOINT::Y - координата в метрах на восток
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetMapPlanePoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetMapPlanePoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetMapPlanePoint_t (_hobj, _point, _number, _subject)


# Запросить координаты точки в системе координат документа в метрах
# hobj - идентификатор объекта карты в памяти
# point - поле для записи координат точки
#         DOUBLEPOINT::X - координата в метрах на север,
#         DOUBLEPOINT::Y - координата в метрах на восток
# number - номер точки (начинается с 1)
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetPlanePoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetPlanePoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        return mapGetPlanePoint_t (_hobj, _point, _number, _subject)


# Запрос высоты точки объекта в метрах на местности
# hobj - идентификатор объекта карты в памяти
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для получения значения высоты объект должен иметь тип метрики IDDOUBLE3, IDDOUBLE4,
# IDDOUBLE4F или IDLONG3
# Если значение высоты для точки не устанавливалось, то возвращаемое значение может
# быть равно псевдокоду высоты: -111111 (ERRORHEIGHT)
# Возвращает значение координаты высота или ноль

    mapHPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapHPlane', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapHPlane(_hobj: maptype.HOBJ, _number: int, _subject: int = 0) -> float:
        return mapHPlane_t (_hobj, _number, _subject)


# Запрос высоты точки объекта в метрах на местности с контролем наличия высоты
# hobj - идентификатор объекта карты в памяти
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# h - поле для записи значения высоты точки
# Для получения значения высоты объект должен иметь тип метрики IDDOUBLE3, IDDOUBLE4,
# IDDOUBLE4F или IDLONG3
# Если значение высоты для точки не устанавливалось, то возвращаемое значение может
# быть равно псевдокоду высоты: -111111 (ERRORHEIGHT)
# При ошибке возвращает ноль

    mapHPlaneEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapHPlaneEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapHPlaneEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapHPlaneEx_t (_hobj, _number, _subject, _h)


# Запросить, имеет ли объект 3D метрику
# hobj - идентификатор объекта карты в памяти
# Если да, возвращает ненулевое значение

    mapIsObject3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObject3D', maptype.HOBJ)
    def mapIsObject3D(_hobj: maptype.HOBJ) -> int:
        return mapIsObject3D_t (_hobj)


# Запросить тип высоты в третьей координате
# hobj - идентификатор объекта карты в памяти
# Реально высота может быть и не задана
# Возвращает: 0 - если в метрике хранитя абсолютная высота,
# ненулевое значение - относительная высота
# При ошибке возвращает ноль

    mapGetHeightType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetHeightType', maptype.HOBJ)
    def mapGetHeightType(_hobj: maptype.HOBJ) -> int:
        return mapGetHeightType_t (_hobj)


# Установить тип высоты в третьей координате
# hobj - идентификатор объекта карты в памяти
# type - тип высоты: 0 - абсолютная, иначе - относительная
# Значение высоты может быть установлено позднее
# Объекты с относительной высотой не влияют на построение матрицы высот

    mapSetHeightType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetHeightType', maptype.HOBJ, ctypes.c_long)
    def mapSetHeightType(_hobj: maptype.HOBJ, _type: int) -> int:
        return mapSetHeightType_t (_hobj, _type)


# Проверить, что третья координата метрики содержит допустимые значения абсолютной высоты
# hobj - идентификатор объекта карты в памяти
# Выполняется проверка, что хотя бы одна точка содержит высоту, не равную псевдокоду: -111111
# При отсутствии допустимых значений возвращает ноль

    mapCheckHeightCorrect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckHeightCorrect', maptype.HOBJ)
    def mapCheckHeightCorrect(_hobj: maptype.HOBJ) -> int:
        return mapCheckHeightCorrect_t (_hobj)


# Запросить значение 4-го измерения точки метрики
# hobj - идентификатор объекта карты в памяти
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для получения значения измерения объект должен иметь тип метрики IDDOUBLE4
# При ошибке возвращает ноль

    mapMValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapMValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapMValue(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapMValue_t (_hobj, _number, _subject)


# Запросить значение 4-го измерения точки метрики в виде большого целого числа
# hobj - идентификатор объекта карты в памяти
# number - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для получения значения измерения объект должен иметь тип метрики IDDOUBLE4F
# При ошибке возвращает ноль

    mapFValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_int64,'mapFValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapFValue(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapFValue_t (_hobj, _number, _subject)


# Запросить является ли объект мультиполигоном
# hobj - идентификатор объекта карты в памяти
# Мультиполигон - это площадной объект, у которого некоторые подобъекты
# могут быть вне границ объекта
# При подсчете площади мультиполигона площадь внешних подобъектов
# будет добавляться к площади основного объекта, а площади
# внутренних подобъектов - вычитаться
# Если объект является мультиполигоном, то возвращается ненулевое значение

    mapIsMultiPolygon_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMultiPolygon', maptype.HOBJ)
    def mapIsMultiPolygon(_hobj: maptype.HOBJ) -> int:
        return mapIsMultiPolygon_t (_hobj)


# Установить или сбросить признак мультиполигона
# hobj - идентификатор объекта карты в памяти
# multi - признак мультиполигона: 0 или 1
# isautoset - признак необходимости подтверждения наличия внешних контуров: 0 или 1
#         Если при подтверждении наличия внешних контуров они не будут найдены, то
#         признак мультиполигона не будет установлен. Для большого числа точек и подобъектов
#         для подтверждения запускается набор потоков для определения входимости подобъектов
# ischeckobject - контроль главного контура объекта - проверить, что объект не входит в
#         какой-либо подобъект и перенести этот подобъект перед объектом
#         при необходимости (сделать главным),
#         если в главном (нулевом) контуре меньше 4 точек, то он удаляется
# При ошибке возвращает ноль

    mapSetMultiPolygonAndCheckObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetMultiPolygonAndCheckObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMultiPolygonAndCheckObject(_hobj: maptype.HOBJ, _multi: int, _isautoset: int, _ischeckobject: int) -> int:
        return mapSetMultiPolygonAndCheckObject_t (_hobj, _multi, _isautoset, _ischeckobject)


# Запросить флаг размещения подобъекта вне площадного объекта (полигона)
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для внешних подобъектов возвращает отрицательное значение (-1),
# для внутренних подобъектов возвращает номер внешнего подобъекта (c 0), в который
# входит данный подобъект
# При отсутствии описания возвращает ноль

    mapGetSubjectMultiFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSubjectMultiFlag', maptype.HOBJ, ctypes.c_long)
    def mapGetSubjectMultiFlag(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapGetSubjectMultiFlag_t (_hobj, _subject)


# Установить флаг размещения подобъекта вне площадного объекта (полигона)
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# flag - признак размещения (входимости) подобъекта
# Для внешних подобъектов устанавливается отрицательное значение (-1),
# для внутренних подобъектов устанавливается номер внешнего подобъекта (c 0), в который
# входит данный подобъект
# При отсутствии описания возвращает ноль

    mapSetSubjectMultiFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSubjectMultiFlag', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSubjectMultiFlag(_hobj: maptype.HOBJ, _subject: int, _flag: int) -> int:
        return mapSetSubjectMultiFlag_t (_hobj, _subject, _flag)


# Запросить число внешних контуров в площадном объекте (полигоне)
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetMultiSubjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMultiSubjectCount', maptype.HOBJ)
    def mapGetMultiSubjectCount(_hobj: maptype.HOBJ) -> int:
        return mapGetMultiSubjectCount_t (_hobj)


# Запросить номер подобъекта внешнего контура в площадном объекте (полигоне)
# hobj - идентификатор объекта карты в памяти
# number - порядковый номер внешнего контура от 1 до mapGetMultiSubjectCount
# При отсутствии описания возвращает -1

    mapGetMultiSubjectNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMultiSubjectNumber', maptype.HOBJ, ctypes.c_long)
    def mapGetMultiSubjectNumber(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapGetMultiSubjectNumber_t (_hobj, _number)


# Запросить, является ли объект мультимасштабным
# hobj - идентификатор объекта карты в памяти
# Мультимасштабный объект имеет несколько контуров для разных масштабов
# Мультимасштабные объекты могут формироваться при сортировке карты,
# если задана соответствующая опция, и в классификаторе карты объект
# имеет свойство "мультимасштабный"
# Если объект мультимасштабный, то возвращается ненулевое значение

    mapIsMultiContour_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMultiContour', maptype.HOBJ)
    def mapIsMultiContour(_hobj: maptype.HOBJ) -> int:
        return mapIsMultiContour_t (_hobj)


# Удалить признак мультимасштабного объекта
# hobj - идентификатор объекта карты в памяти

    mapClearMultiContour_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearMultiContour', maptype.HOBJ)
    def mapClearMultiContour(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapClearMultiContour_t (_hobj)


# Запросить, является ли объект полигоном с центральной точкой
# hobj - идентификатор объекта карты в памяти
# Центральная точка - это подобъект с одной точкой, которая вычисляется
# в центре полигона, но может быть смещена оператором
# В этой точке отображается точечный знак, заданный в классификаторе
# Если да, возвращает ненулевое значение

    mapIsPolygonWithPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsPolygonWithPoint', maptype.HOBJ)
    def mapIsPolygonWithPoint(_hobj: maptype.HOBJ) -> int:
        return mapIsPolygonWithPoint_t (_hobj)


# Запросить, является ли объект объектом оформления
# hobj - идентификатор объекта карты в памяти
# Свойство "объект оформления" устанавливается в классификаторе RSC
# Если это объект оформления, то возвращается ненулевое значение

    mapIsDesignObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDesignObject', maptype.HOBJ)
    def mapIsDesignObject(_hobj: maptype.HOBJ) -> int:
        return mapIsDesignObject_t (_hobj)


# Определить центр объекта
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# x - поле для записи координаты x центра (на север) в метрах в системе документа
# y - поле для записи координаты y центра (на восток) в метрах в системе документа
# type - тип алгоритма определения центра контура:
#        0 - для полигона строится линия сечения по центру вертикальных габаритов объекта
#            с поиском середины отрезка сечения; для линии ищется примерная середина контура по всей длине
#        1 - для полигона вычисляется геометрическое среднее значение контура объекта,
#            для остальных объектов вычисляется геометрическое среднее значение координат всех точек
# При ошибке возвращает ноль

    mapGetObjectCenterEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectCenterEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapGetObjectCenterEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _type: int = 0) -> int:
        return mapGetObjectCenterEx_t (_hmap, _hobj, _x, _y, _type)


# Запросить габариты объекта (векторного, точечного, подписи) в текущем масштабе
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта
# frame - поле для записи габаритов объекта
# viewtype - тип отображения карты:
#            VT_SCREEN - экранный вид
#            VT_PRINT - принтерный вид
#            0 - тип отображения карты определяется автоматически (текущий вид карты hmap)
# flag - признак системы координат габаритов объекта:
#         0 - в метрах на местности (относительно точки привязки знака)
#         1 - в абсолютных метрах на местности
#         2 - не расширять габариты знака (допустимо совместное использование флагов - 1|2)
# При ошибке возвращает ноль

    mapGetDrawedObjectFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDrawedObjectFrame', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long)
    def mapGetDrawedObjectFrame(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _viewtype: int, _flag: int) -> int:
        return mapGetDrawedObjectFrame_t (_hmap, _hobj, _frame, _viewtype, _flag)


# Запросить, совпадают ли координаты объектов с точностью DELTANULL
# hobj  - идентификатор исходного объекта карты в памяти
# hanother - идентификатор объекта карты в памяти для сравнения метрики
# При совпадении возвращает ненулевое значение

    mapIsObjectDataEquivalent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectDataEquivalent', maptype.HOBJ, maptype.HOBJ)
    def mapIsObjectDataEquivalent(_hobj: maptype.HOBJ, _hanother: maptype.HOBJ) -> int:
        return mapIsObjectDataEquivalent_t (_hobj, _hanother)


# Запросить, совпадают ли координаты подобъекта с заданной точностью
# hobj - идентификатор исходного объекта карты в памяти
# hanother - идентификатор объекта карты в памяти для сравнения метрики
# subject - номер подобъекта или -1 (все подобъекты)
# precision - точность сравнения координат на плоскости
# hprecision - точность сравнения высот или ноль (не проверять)
# При совпадении возвращает ненулевое значение

    mapIsObjectDataEquivalentEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectDataEquivalentEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapIsObjectDataEquivalentEx(_hobj: maptype.HOBJ, _hanother: maptype.HOBJ, _subject: int = -1, _precision: float = maptype.DELTANULL, _hprecision: ctypes.POINTER(ctypes.c_double) = None) -> int:
        return mapIsObjectDataEquivalentEx_t (_hobj, _hanother, _subject, _precision, _hprecision)


# Включить или отключить доступ к общему буферу векторных карт для работы с большими объемами данных
# hide - признак отключения общего буфера памяти для векторных карт (1 или 0)
# Общий буфер не рекомендуется применять для многопоточных приложений
# Если буфер отключен, то при нехватке памяти будет формироватся ошибка при чтении данных карт
# Возвращает значение флага доступа, который был до вызова функции

    mapHideCommonBuffer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapHideCommonBuffer', ctypes.c_int)
    def mapHideCommonBuffer(_hide: int) -> int:
        return mapHideCommonBuffer_t (_hide)


# Запросить, используется ли общий буфер векторных карт
# В этом случае многопоточный режим использования MAPAPI-функций не применим
# Если буфер используется, то возвращает ненулевое значение

    mapIsCommonBufferActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsCommonBufferActive')
    def mapIsCommonBufferActive() -> int:
        return mapIsCommonBufferActive_t ()


# Установить ограничение объема открытых векторных карт в Кб
# maxsize - предельное значение объема памяти в Кб для размещения векторных карт
# При достижении 75% от заданного объема открытых данных будет включаться механизм прокачки
# векторных карт через буфер обмена

    mapSetTotalMapMemoryLimitKb_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetTotalMapMemoryLimitKb', ctypes.c_int64)
    def mapSetTotalMapMemoryLimitKb(_maxsize: int) -> ctypes.c_void_p:
        return mapSetTotalMapMemoryLimitKb_t (_maxsize)


# Запросить ограничение объема открытых векторных карт в Кб

    mapGetTotalMapMemoryLimitKb_t = mapsyst.GetProcAddress(curLib,ctypes.c_int64,'mapGetTotalMapMemoryLimitKb')
    def mapGetTotalMapMemoryLimitKb() -> int:
        return mapGetTotalMapMemoryLimitKb_t ()


# Установить максимальное время работы функций в милисекундах
# Пример функций на которые влияет установленное время: поиск объектов, рисование области
# и другие функции, обращающиеся к данным
# Функция используется для работы с большими объёмами данных, время первой загрузки
# или обновления которых может занимать минуты
# Если установлено время и данные не готовы для работы за заданный промежуток времени,
# то выполнение функции, обращающейся к данным, завершится с ошибкой
# Возвращает старое значение в милисекундах

    mapSetTimeForWaitingDataReady_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSetTimeForWaitingDataReady', ctypes.c_int)
    def mapSetTimeForWaitingDataReady(_waitTime: int) -> int:
        return mapSetTimeForWaitingDataReady_t (_waitTime)


# Запросить количество калибровочных точек линейных координат для объекта
# hobj - идентификатор объекта карты в памяти
# Любому линейному объекту могут быть присвоены калибровочные точки для определения
# линейных координат
# Например: участок дороги может иметь километровые столбы по которым определяется
# (интерполируется) линейная координата любой точки дороги
# Если калибровочные точки не заданы, то вычисления линейных координат идут
# по длине объекта от его начала
# При ошибке возвращает ноль

    mapGetLinearPointCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLinearPointCount', maptype.HOBJ)
    def mapGetLinearPointCount(_hobj: maptype.HOBJ) -> int:
        return mapGetLinearPointCount_t (_hobj)


# Запросить описание калибровочной точки линейных координат по номеру
# hobj - идентификатор объекта карты в памяти
# number - номер калибровочной точки от 1 до mapGetLinearPointCount
# point - поле для записи координаты калибровочной точки линейных координат в метрах в системе координат документа
# linear - поле для записи калибровочного расстояния от первой точки объекта до калибровочной точки
# При ошибке возвращает ноль

    mapGetLinearPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLinearPoint', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapGetLinearPoint(_hobj: maptype.HOBJ, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapGetLinearPoint_t (_hobj, _number, _point, _linear)


# Добавить калибровочную точку линейных координат для объекта
# hobj  - идентификатор объекта карты в памяти
# point - координаты калибровочной точки линейных координат в метрах в системе координат документа
# linear - калибровочное расстояние от первой точки объекта до калибровочной точки
# При ошибке возвращает ноль

    mapAppendLinearPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendLinearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapAppendLinearPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: float) -> int:
        return mapAppendLinearPoint_t (_hobj, _point, _linear)


# Удалить калибровочную точку линейных координат для объекта
# hobj - идентификатор объекта карты в памяти
# number - номер удалаяемой калибровочной точки от 1 до GetLinearPointCount()
# Если number равен -1, удаляются все калибровочные точки
# При ошибке возвращает ноль

    mapDeleteLinearPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteLinearPoint', maptype.HOBJ, ctypes.c_long)
    def mapDeleteLinearPoint(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapDeleteLinearPoint_t (_hobj, _number)


# Рассчитать линейную координату для заданной точки по ее плоским прямоугольным координатам
# hobj - идентификатор объекта карты в памяти
# point - координаты точки в системе документа, для которой определяется линейная координата
# linear - поле для записи линейной координаты в метрах
# При наличии калибровочных точек линейных координат выполняется интерполяция положения
# заданной точки, иначе - поиск положения точки в SeekNearVirtualPoint()
# При ошибке возвращает ноль

    mapPlanePointToLinearPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPlanePointToLinearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapPlanePointToLinearPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapPlanePointToLinearPoint_t (_hobj, _point, _linear)


# Определить координаты в системе документа для заданной линейной координаты
# hobj - идентификатор объекта карты в памяти
# linear - линейные координаты точки на контуре объекта в метрах
# point - поле для записи координат точки в системе документа, для которой вычисляется линейная координата
# intermediate - флаг определения положения точки между крайними точками подобъектов:
#     0 - выбирать результирующую точку на контуре объекта или подобъектов
#     1 - выбирать точку между последней точкой одного подобъекта и первой точкой другого подобъекта,
#         если в этих точках есть калибровочные точки или 4-е измерение с линейной координатой
#         и входное значение линейной координаты попадает между ними
# При ошибке возвращает ноль

    mapLinearPointToPlanePointEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLinearPointToPlanePointEx', maptype.HOBJ, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapLinearPointToPlanePointEx(_hobj: maptype.HOBJ, _linear: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _intermediate: int) -> int:
        return mapLinearPointToPlanePointEx_t (_hobj, _linear, _point, _intermediate)


# Определить координаты в системе документа для заданных линейных координат
# hobj  - идентификатор объекта карты в памяти
# linear - линейные координаты точки на контуре объекта в метрах
# point - поле для записи координат точки в системе документа, для которой вычисляется линейная координата
# Найденная точка притягивается к контуру объекта в системе координат карты (искажается)
# Не применять для заполнения баз данных - результат зависим от системы координат карты
# При ошибке возвращает ноль

    mapLinearPointToPlanePointForObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLinearPointToPlanePointForObject', maptype.HOBJ, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLinearPointToPlanePointForObject(_hobj: maptype.HOBJ, _linear: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapLinearPointToPlanePointForObject_t (_hobj, _linear, _point)


# Связать калибровочные точки с маршрутами по двум группам выделенных объектов
# hmap - идентификатор открытых данных (документа), в состав которых входит карта маршрутов и карта
#        с калибровочными точками (могут быть на одной карте)
# hrouteselect - условия отбора объектов - маршрутов
# hpointsselect - условия отбора объектов - калибровочных точек
# deviation - значение допустимого отклонения координат калибровочной точки от осевой линии маршрута в метрах
# linearsemanticcode - код семантики калибровочной точки, содержащий калибровочное значение линейной координаты
# Для каждой найденной пары маршрут и калибровочная точка вызывается mapAppendLinearPoint
# Если все найденные точки уже есть в маршруте - возвращает отрицательное число найденных точек
# При ошибке или отсутствии добавленных и дублирующихся точек возвращает ноль

    mapLoadSelectedLinearPoints_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLoadSelectedLinearPoints', maptype.HMAP, maptype.HSELECT, maptype.HSELECT, ctypes.c_double, ctypes.c_long)
    def mapLoadSelectedLinearPoints(_hmap: maptype.HMAP, _hrouteselect: maptype.HSELECT, _hpointsselect: maptype.HSELECT, _deviation: float, _linearsemanticcode: int) -> int:
        return mapLoadSelectedLinearPoints_t (_hmap, _hrouteselect, _hpointsselect, _deviation, _linearsemanticcode)


# Установить предельное искажение линейных измерений для линейных координат
# factor - предельное искажение линейных измерений от 1 до 10, определяется как
#          предел соотношения разницы линейных координат между смежными калибровочными точками и
#          расчетной длины этих участков на эллипсоиде
# Возвращает установленное значение

    mapSetMaxLengthDistortionFactor_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetMaxLengthDistortionFactor', ctypes.c_long)
    def mapSetMaxLengthDistortionFactor(_factor: int) -> int:
        return mapSetMaxLengthDistortionFactor_t (_factor)


# Запросить предельное искажение линейных измерений для линейных координат

    mapGetMaxLengthDistortionFactor_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMaxLengthDistortionFactor')
    def mapGetMaxLengthDistortionFactor() -> int:
        return mapGetMaxLengthDistortionFactor_t ()


# Установить в четвертое измерение каждой точки значение линейной координаты в этой точке (калибровка маршрута)
# hobj  - идентификатор объекта карты в памяти
# Если объект не содержит калибровочных точек, то в четвертое измерение будет записана длина от начала объекта на эллипсоиде WGS84
# Применяется перед записью объекта в таблицу маршрутов базы пространственных данных
# При ошибке возвращает ноль

    mapSetLinearPointAsMValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetLinearPointAsMValue', maptype.HOBJ)
    def mapSetLinearPointAsMValue(_hobj: maptype.HOBJ) -> int:
        return mapSetLinearPointAsMValue_t (_hobj)


# Добавить в конец метрики объекта точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для изменения координаты Н необходимо далее выполнить функцию SetHPlane()
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _subject: int = 0) -> int:
        return mapAppendPointPlane_t (_hobj, _x, _y, _subject)


# Добавить в конец метрики объекта точку в прямоугольной системе в метрах на местности в проекции карты
# hobj    - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат карты
# y - координата y (на восток) точки в метрах в системе координат карты
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для изменения координаты Н необходимо далее выполнить функцию SetHPlane()
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendMapPointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _subject: int = 0) -> int:
        return mapAppendMapPointPlane_t (_hobj, _x, _y, _subject)


# Добавить в конец метрики объекта точку
# hobj    - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - высота (абсолютная или относительная) в метрах
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane3D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _subject: int = 0) -> int:
        return mapAppendPointPlane3D_t (_hobj, _x, _y, _h, _subject)


# Добавить в конец метрики объекта точку и измерение (свойство) в точке
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# m - измерение в формате double (для типа метрики IDDOUBLE4)
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane4D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointPlane4D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane4D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _m: float, _subject: int) -> int:
        return mapAppendPointPlane4D_t (_hobj, _x, _y, _h, _m, _subject)


# Добавить в конец метрики объекта точку и целочисленное измерение (свойство) в точке
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# f - измерение в формате __int64 (для типа метрики IDDOUBLE4F)
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает номер добавленной точки в подобъекте (с 1)
# При ошибке возвращает ноль

    mapAppendPointPlane4F_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointPlane4F', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int64, ctypes.c_long)
    def mapAppendPointPlane4F(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _f: int, _subject: int) -> int:
        return mapAppendPointPlane4F_t (_hobj, _x, _y, _h, _f, _subject)


# Удалить заданную точку метрики
# hobj - идентификатор объекта карты в памяти
# number  - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapDeletePointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeletePointPlane', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapDeletePointPlane(_hobj: maptype.HOBJ, _number: int, _subject: int = 0) -> int:
        return mapDeletePointPlane_t (_hobj, _number, _subject)


# Удаление из метрики одинаковых точек
# hobj - идентификатор объекта карты в памяти
# precision - величина расхождения значений координат в метрах на местности
# height - признак учета трехмерной метрики (в этом случае две одинаковые
#          точки с разной высотой считаются разными)
# При ошибке возвращает ноль

    mapDeleteEqualPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteEqualPoint', maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapDeleteEqualPoint(_hobj: maptype.HOBJ, _precision: float, _height: int) -> int:
        return mapDeleteEqualPoint_t (_hobj, _precision, _height)


# Удалить из подобъекта участок по номерам точек
# hobj - идентификатор объекта карты в памяти
# number1 - номер с 1 первой удаляемой точки в диапазоне
# number2 - номер с 1 последней удаляемой точки в диапазоне
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При удалении всех точек подобъекта удаляется только метрика,
# подобъект не удаляется и будет содержать 0 точек
# При ошибке возвращает ноль

    mapDeletePartObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeletePartObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDeletePartObject(_hobj: maptype.HOBJ, _number1: int, _number2: int, _subject: int = 0) -> int:
        return mapDeletePartObject_t (_hobj, _number1, _number2, _subject)


# Вставить в метрику объекта точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# number  - номер точки с 0, за которой будет добавлена новая точка
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для изменени координаты Н необходимо далее выполнить функцию mapSetHPlane()
# При ошибке возвращает ноль

    mapInsertPointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInsertPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapInsertPointPlane_t (_hobj, _x, _y, _number, _subject)


# Вставить в метрику объекта точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат карты
# y - координата y (на восток) точки в метрах в системе координат карты
# number - номер точки c 0, за которой будет добавлена новая точка
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для изменени координаты Н необходимо далее выполнить функцию mapSetHPlane()
# При ошибке возвращает ноль

    mapInsertMapPointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInsertMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapInsertMapPointPlane_t (_hobj, _x, _y, _number, _subject)


# Изменить координаты точки метрики
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapUpdatePointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane_t (_hobj, _x, _y, _number, _subject)


# Изменить координаты точки метрики
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
#     Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# number  - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapUpdatePointPlane3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3D_t (_hobj, _x, _y, _h, _number, _subject)


# Изменить координаты точки метрики
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат карты
# y - координата y (на восток) точки в метрах в системе координат карты
# number  - номер точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapUpdateMapPointPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdateMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        return mapUpdateMapPointPlane_t (_hobj, _x, _y, _number, _subject)


# Добавить в конец метрики объекта точку
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе координат документа
# l - долгота точки в радианах в геодезической системе координат документа
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает номер добавленной точки в подобъекте с 1
# При ошибке возвращает ноль

    mapAppendPointGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int = 0) -> int:
        return mapAppendPointGeo_t (_hobj, _b, _l, _subject)


# Добавить в конец метрики объекта точку в геодезической системе карты
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе координат карты
# l - долгота точки в радианах в геодезической системе координат карты
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Значение координат задано в радианах
# При ошибке возвращает ноль

    mapAppendMapPointGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendMapPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendMapPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int = 0) -> int:
        return mapAppendMapPointGeo_t (_hobj, _b, _l, _subject)


# Добавить в конец метрики объекта точку
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе WGS84
# l - долгота точки в радианах в геодезической системе WGS84
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает номер добавленной точки в подобъекте с 1
# При ошибке возвращает ноль

    mapAppendPointGeoWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointGeoWGS84', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeoWGS84(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int) -> int:
        return mapAppendPointGeoWGS84_t (_hobj, _b, _l, _subject)


# Добавить в конец метрики объекта точку
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе WGS84
# l - долгота точки в радианах в геодезической системе WGS84
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# Возвращает номер добавленной точки в подобъекте с 1
# При ошибке возвращает ноль

    mapAppendPointGeoWGS843D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendPointGeoWGS843D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeoWGS843D(_hobj: maptype.HOBJ, _b: float, _l: float, _h: float, _subject: int) -> int:
        return mapAppendPointGeoWGS843D_t (_hobj, _b, _l, _h, _subject)


# Вставить в метрику объекта точку
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе координат документа
# l - долгота точки в радианах в геодезической системе координат документа
# number - номер точки c 0, за которой будет добавлена новая точка
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для изменения координаты Н необходимо далее выполнить функцию HPlane()
# При ошибке возвращает ноль

    mapInsertPointGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInsertPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int = 0) -> int:
        return mapInsertPointGeo_t (_hobj, _b, _l, _number, _subject)


# Изменить координаты точки метрики
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе координат документа
# l - долгота точки в радианах в геодезической системе координат документа
# number - номер обновляемой точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapUpdatePointGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointGeo_t (_hobj, _b, _l, _number, _subject)


# Изменить координаты точки метрики
# hobj - идентификатор объекта карты в памяти
# b - широта точки в радианах в геодезической системе координат документа
# l - долгота точки в радианах в геодезической системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
#     Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# number - номер обновляемой точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapUpdatePointGeo3D_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointGeo3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointGeo3D(_hobj: maptype.HOBJ, _b: float, _l: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointGeo3D_t (_hobj, _b, _l, _h, _number, _subject)


# Изменить координаты общей точки метрики у объекта и у всех объектов карты, имеющих такую точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
# При ошибке возвращает ноль

    mapUpdatePointPlaneInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlaneInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlaneInMap(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlaneInMap_t (_hobj, _x, _y, _number, _subject)


# Изменить координаты общей точки метрики у объекта и у всех объектов карты, имеющих такую точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
#     Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
# При ошибке возвращает ноль

    mapUpdatePointPlane3DInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlane3DInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3DInMap(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3DInMap_t (_hobj, _x, _y, _h, _number, _subject)


# Изменить координаты общей точки у объекта и у всех объектов общего слоя, имеющих такую точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
# При ошибке возвращает ноль

    mapUpdatePointPlaneInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlaneInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlaneInLayer(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlaneInLayer_t (_hobj, _x, _y, _number, _subject)


# Изменить координаты общей точки у объекта и у всех объектов общего слоя, имеющих такую точку
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# y - координата y (на восток) точки в метрах в системе координат документа
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
#     Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
# При ошибке возвращает ноль

    mapUpdatePointPlane3DInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdatePointPlane3DInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3DInLayer(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int = 0) -> int:
        return mapUpdatePointPlane3DInLayer_t (_hobj, _x, _y, _h, _number, _subject)


# Редактирование координаты точки объекта/подобъекта в прямоугольной системе в метрах на местности
# hobj - идентификатор объекта карты в памяти
# x - координата x (на север) точки в метрах в системе координат документа
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapSetXPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetXPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetXPlane(_hobj: maptype.HOBJ, _x: float, _number: int, _subject: int = 0) -> int:
        return mapSetXPlane_t (_hobj, _x, _number, _subject)


# Редактирование координаты точки объекта/подобъекта в прямоугольной системе в метрах на местности
# hobj - идентификатор объекта карты в памяти
# y - координата y (на восток) точки в метрах в системе координат документа
# number - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapSetYPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetYPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetYPlane(_hobj: maptype.HOBJ, _y: float, _number: int, _subject: int = 0) -> int:
        return mapSetYPlane_t (_hobj, _y, _number, _subject)


# Редактирование высоты точки объекта/подобъекта в метрах
# hobj - идентификатор объекта карты в памяти
# h - нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
#     Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
# number  - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Тип высоты может быть запрошен функцией mapGetHeightType
# Система высот устанавливается в паспорте карты (HEIGHTSYSTEM)
# Если объект имел двухмерную метрику (mapIsObject3D() == 0), то будет изменен формат записи с установкой значения высоты ERRORHEIGHT
# При ошибке возвращает ноль

    mapSetHPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetHPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetHPlane(_hobj: maptype.HOBJ, _h: float, _number: int, _subject: int = 0) -> int:
        return mapSetHPlane_t (_hobj, _h, _number, _subject)


# Изменить измерение (свойство) точки метрики
# hobj - идентификатор объекта карты в памяти
# m - измерение в формате double (для типа метрики IDDOUBLE4)
# number  - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapSetMValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetMValue', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetMValue(_hobj: maptype.HOBJ, _m: float, _number: int, _subject: int) -> int:
        return mapSetMValue_t (_hobj, _m, _number, _subject)


# Изменить измерение (свойство) точки метрики
# hobj - идентификатор объекта карты в памяти
# f - измерение в формате __int64 (для типа метрики IDDOUBLE4F)
# number  - номер точки c 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapSetFValue_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetFValue', maptype.HOBJ, ctypes.c_int64, ctypes.c_long, ctypes.c_long)
    def mapSetFValue(_hobj: maptype.HOBJ, _f: int, _number: int, _subject: int) -> int:
        return mapSetFValue_t (_hobj, _f, _number, _subject)


# Создать пустой подобъект в конце записи метрики
# hobj - идентификатор объекта карты в памяти
# В конец записи добавляется дескриптор подобъекта с нулевым числом точек
# Если предыдущий подобъект не содержит ни одной точки, то новый подобъект не будет создан
# Возвращает номер созданного подобъекта
# При ошибке возвращает ноль

    mapCreateSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateSubject', maptype.HOBJ)
    def mapCreateSubject(_hobj: maptype.HOBJ) -> int:
        return mapCreateSubject_t (_hobj)


# Удалить подобъект в записи метрики
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки,
#           если равен (-1), то удаляется вся метрика объекта вместе с подобъектами
# Текущей становится первая точка объекта
# При ошибке возвращает ноль

    mapDeleteSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSubject', maptype.HOBJ, ctypes.c_long)
    def mapDeleteSubject(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapDeleteSubject_t (_hobj, _subject)


# Удалить подобъект - главный контур из указанной записи и его подобъекты
# hobj - идентификатор объекта карты в памяти
# number - номер подобъекта, который является внешним контуром (запросить число внешних конутров - mapGetMultiSubjectNumber())
# При ошибке возвращает ноль

    mapDeleteMultiSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteMultiSubject', maptype.HOBJ, ctypes.c_long)
    def mapDeleteMultiSubject(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapDeleteMultiSubject_t (_hobj, _subject)


# Добавить подобъект из указанной записи в конец метрики
# hobj - идентификатор объекта карты в памяти
# hsource - идентификатор объекта карты в памяти, из которого добавляют подобъет
# subject - номер добавляемого подобъекта или -1 (добавить все подобъекты)
# При ошибке возвращает 0

    mapAppendSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapAppendSubject(_hobj: maptype.HOBJ, _hsource: maptype.HOBJ, _subject: int) -> int:
        return mapAppendSubject_t (_hobj, _hsource, _subject)


# Сместить все координаты метрики объекта на заданную величину
# hobj - идентификатор объекта карты в памяти
# delta - смещение в метрах в системе координат карты на север (delta->X) и на восток (delta->Y)
# При ошибке возвращает 0

    mapRelocateObjectPlane_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRelocateObjectPlane', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRelocateObjectPlane(_hobj: maptype.HOBJ, _delta: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapRelocateObjectPlane_t (_hobj, _delta)


# Изменить направление цифрования подобъекта
# hobj  - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Порядок точек заданного контура от первой до последней меняется на обратный
# Для полигона направление цифрование внутренних контуров обычно противоположно направлению внешнего контура
# При ошибке возвращает ноль

    mapChangeSubjectDirect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeSubjectDirect', maptype.HOBJ, ctypes.c_long)
    def mapChangeSubjectDirect(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapChangeSubjectDirect_t (_hobj, _subject)


# Изменить направление цифрования объекта
# hobj  - идентификатор объекта карты в памяти
# Порядок точек всех контуров объекта от первой до последней меняется на обратный в пределах каждого контура
# Для полигона направление цифрование внутренних контуров обычно противоположно направлению внешнего контура
# При ошибке возвращает ноль

    mapChangeObjectDirect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeObjectDirect', maptype.HOBJ)
    def mapChangeObjectDirect(_hobj: maptype.HOBJ) -> int:
        return mapChangeObjectDirect_t (_hobj)


# Проверить и исправить направление цифрования контуров площадного объекта (полигона)
# hobj - идентификатор объекта карты в памяти
# Направление цифрования внешних контуров полигона сравнивается со значением,
# заданным в классификаторе RSC: OD_LEFT, OD_RIGHT
# При иных значениях (OD_NONE, ...) и для графических объектов
# устанавливается OD_LEFT (объект слева - против часовой стрелки)
# Если выбрано значение OD_LEFT, то направление внешних контуров
# устанавливается равным OD_LEFT, а внутренних - OD_RIGHT
# Возвращает установленное направление цифрования для внешних контуров
# При ошибке возвращает ноль

    mapCorrectPolygonDirect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCorrectPolygonDirect', maptype.HOBJ)
    def mapCorrectPolygonDirect(_hobj: maptype.HOBJ) -> int:
        return mapCorrectPolygonDirect_t (_hobj)


# Установить в метрике объекта или подобъекта полигона первой заданную точку
# hobj  - идентификатор объекта карты в памяти
# number - номер точки c 1, которая будет первой
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Выполняется циклический сдвиг точек, не меняя их последовательности в контуре
# При ошибке возвращает ноль

    mapSetFirstPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetFirstPoint', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetFirstPoint(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapSetFirstPoint_t (_hobj, _number, _subject)


# Выполнить линейную фильтрацию точек метрики
# hobj - идентификатор объекта карты в памяти
# precision - минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
# При линейной фильтрации метрики удаляются:
#     - двойные точки метрики,
#     - незамкнутые подобъекты < 2 точек,
#     - замкнутые подобъекты < 4 точек,
#     - точки метрики, лежащие в середине отрезка прямой на расстоянии precision от прямой.
# Объект не удаляется никогда
# Возвращает общее число точек метрики
# При ошибках возвращает:
#      0 - ошибка структуры
#     -1 - объект состоит из одной точки
#     -2 - объект состоит из двух одинаковых точек
#     -3 - число точек замкнутого контура объекта равно 3
#    -10 - число точек метрики превышает длину записи метрики

    mapLinearFilter_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLinearFilter', maptype.HOBJ, ctypes.c_double)
    def mapLinearFilter(_hobj: maptype.HOBJ, _precision: float) -> int:
        return mapLinearFilter_t (_hobj, _precision)


# Выполнить фильтрацию точек объекта с учетом топологических связей с соседними объектами
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# precision - точность в метрах на местности (минимальное расстояние от точки до прямой,
#             соединяющей предыдущую и следующую точки)
# При фильтрации объекта будут фильтроваться на той же карте и соседние объекты, имеющие общие точки,
# для сохранения общих точек контуров
# Концевые общие точки не фильтруются
# При ошибке возвращает ноль

    mapGeneralFilter_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeneralFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralFilter(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        return mapGeneralFilter_t (_hmap, _hobj, _precision)


# Выполнить фильтрацию точек всех объектов на заданной карте с учетом топологических связей с соседними объектами
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# list - номер листа для многолистовой карты или 1
# precision - минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
# hwnd - идентификатор обработчика, которое будут отправляться сообщения, или 0
# Процесс отправляет сообщение WM_PROGRESSBARUN: wparm - процент обработки,
# Для прерывания процесса из обработчика сообщения нужно вернуть WM_PROGRESSBARUN
# При ошибке возвращает ноль

    mapGeneralFilterInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeneralFilterInMap', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_double, maptype.HMESSAGE)
    def mapGeneralFilterInMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _precision: float, _hwnd: maptype.HMESSAGE) -> int:
        return mapGeneralFilterInMap_t (_hmap, _hsite, _list, _precision, _hwnd)


# Выполнить фильтрацию двойных точек с учетом топологических связей с соседними объектами
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# precision - минимальное расстояние между точками в метрах для определения двойных точек
# При ошибке возвращает ноль

    mapGeneralDuplicatePointFilter_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeneralDuplicatePointFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralDuplicatePointFilter(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        return mapGeneralDuplicatePointFilter_t (_hmap, _hobj, _precision)


# Выполнить генерализацию метрики линейного или площадного объекта для выбранного масштаба
# hobj - идентификатор объекта карты в памяти
# scale - масштаб генерализации метрики (1: 100 000 соответствует сетке с шагом 100 м на местности и 1 мм на изображении)
# force - признак формирования минимальной метрики при вырождении
# Выполняет фильтрацию метрики объекта с подбором точности для заданного масштаба изображения
# При сжатии изображения точки на изображении будут совмещаться и выстраиваться на одной линии, что
# позволяет их исключить без нарушения вида контура на данном масштабе
# Возвращает: 1 - метрика генерализирована успешно
#             2 - метрика не изменилась (исходные точки достаточно разряжены для заданного масштаба)
#             -1 - метрика не изменилась (объект вырождается или максимальное число точек подобъектов меньше 64)
# При ошибке возвращает ноль

    mapObjectGeneralization_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectGeneralization', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapObjectGeneralization(_hobj: maptype.HOBJ, _scale: int, _force: int) -> int:
        return mapObjectGeneralization_t (_hobj, _scale, _force)


# Установить шаг сетки в мм для генерализации контуров объектов в масштабе карты
# step - точность генерализации в мм - минимальное расстояние на изображении от точки до прямой, соединяющей предыдущую и следующую точки
# Применяется для управления степенью генерализации метрики объектов
# Возвращает установленное значение

    mapSetGeneralizationGridStep_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSetGeneralizationGridStep', ctypes.c_double)
    def mapSetGeneralizationGridStep(_step: float) -> float:
        return mapSetGeneralizationGridStep_t (_step)


# Запросить шаг сетки в мм для генерализации контуров объектов в масштабе карты
# Возвращает установленное значение

    mapGetGeneralizationGridStep_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetGeneralizationGridStep')
    def mapGetGeneralizationGridStep() -> float:
        return mapGetGeneralizationGridStep_t ()


# Построить сглаживающий сплайн по координатам объекта и всех его подобъектов
# hobj - исходная метрика объекта, по которому строится сплайн
# cashion - условный процент спиливания углов ломаной линии объекта (1<= cashion <= 50)
#           (метрика исходного объекта/подобъекта)
#           Чем больше cashion, тем больше спиливается угол
# smooth - плавность кривой сплайна (число точек между узлами объекта smooth >= 3)
#          Чем больше smooth, тем более гладкой смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического определения точности установить значение "-1"
# Это сплайн, который проходит только через первую и последнюю точки объекта (подобъекта) и как бы
# сглаживает (спиливает) углы ломаной, соединяющей точки объекта (метрику исходного объекта/подобъекта)
# Если исходный объект имел 3-ю координату (высоту), то у сплайна также есть высота (интерполяция для новых точек)
# При ошибке возвращает ноль

    mapCashionSpline_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCashionSpline', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCashionSpline(_hobj: maptype.HOBJ, _cashion: int, _smooth: int, _precision: float) -> int:
        return mapCashionSpline_t (_hobj, _cashion, _smooth, _precision)


# Построить сглаживающий сплайн по координатам заданного подобъекта
# hobj  - исходная метрика объекта, по подобъекту которого строится сплайн
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# cashion - условный процент спиливания углов ломаной линии объекта (1<= cashion <= 50)
#           Чем больше cashion, тем больше спиливается угол
# smooth - плавность кривой сплайна (число точек между узлами подобъекта smooth >= 3)
#           Чем больше smooth, тем более гладкой смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического определения точности установить значение "-1"
# Это сплайн, который проходит только через первую и последнюю точки подобъекта и как бы
# сглаживает (спиливает) углы ломаной, соединяющей точки объекта (метрику исходного подобъекта)
# Если исходный подобъект имел 3-ю координату (высоту), то у сплайна также есть высота
# При ошибке возвращает ноль

    mapCashionSplineSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCashionSplineSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCashionSplineSubject(_hobj: maptype.HOBJ, _subject: int, _cashion: int, _smooth: int, _precision: float) -> int:
        return mapCashionSplineSubject_t (_hobj, _subject, _cashion, _smooth, _precision)


# Построить огибающий сплайн для объекта и всех его подобъектов
# hobj - исходная метрика объекта, по которому строится сплайн
# press - максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка ( >= 5 )
#         Чем больше press, тем более сплайн может удаляться от отрезка ломаной (метрики исходного объекта/подобъекта).
# smooth - плавность кривой сплайна (число точек между узлами объекта smooth >= 3)
#          Чем больше smooth, тем более гладкой смотрится линия
# precision - порог (точность) при фильтрации точек, для автоматического определения точности установить значение "-1"
# Это сплайн, который проходит через все точки исходного объекта по гладкой кривой заданной амплитуды
# Если исходный объект имел 3-ю координату (высоту), то у сплайна также есть высота (интерполяция для новых точек)
# При ошибке возвращает ноль

    mapBendSpline_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBendSpline', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapBendSpline(_hobj: maptype.HOBJ, _press: int, _smooth: int, _precision: float) -> int:
        return mapBendSpline_t (_hobj, _press, _smooth, _precision)


# Построить огибающий сплайн для заданного подобъекта
# hobj  - исходная метрика объекта, по которому строится сплайн
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# press - максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка ( >= 5 )
#         Чем больше press, тем более сплайн может удаляться от отрезка ломаной (метрики исходного объекта/подобъекта)
# smooth - плавность кривой сплайна (число точек между узлами объекта smooth >= 3)
#         Чем больше smooth, тем более гладкой смотрится линия
# precision - порог (точность) при фильтрации точек
# Это сплайн, который проходит через все точки исходного объекта по гладкой кривой заданной амплитуды
# Если исходный подобъект имел 3-ю координату (высоту), то у сплайна также есть высота
# При ошибке возвращает ноль

    mapBendSplineSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBendSplineSubject', maptype.HOBJ, ctypes.c_int, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapBendSplineSubject(_hobj: maptype.HOBJ, _subject: int, _press: int, _smooth: int, _precision: float) -> int:
        return mapBendSplineSubject_t (_hobj, _subject, _press, _smooth, _precision)


# Построить огибающий сплайн для объекта и подобъектов с учетом топологических связей с соседними объектами
# hmap - идентификатор открытых данных (документа)
# hobj - фильтруемый объект
# press - максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка (>= 5), чем больше press,
#        тем больше сплайн может оклоняться от исходного контура
# smooth - плавность кривой сплайна (>= 3) число точек между узлами объекта,
#          чем больше smooth, тем более гладким будет сплайн
# adjustdist - допуск согласования - максимальное расстояние, при котором две соседние
#              точки считаются расположенными на одном месте
# filterprec - уровень фильтрации (минимальное расстояние от точки до прямой, соединяющей предыдущую и следующую точки)
# При ошибке возвращает ноль

    mapGeneralBendSpline_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGeneralBendSpline', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapGeneralBendSpline(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _press: int, _smooth: int, _adjustdist: float, _filterprec: float) -> int:
        return mapGeneralBendSpline_t (_hmap, _hobj, _press, _smooth, _adjustdist, _filterprec)


# Построить одномерный сглаживающий сплайн
# points - массив точек, содержащих одну координату
# count - количество точек
# smooth - уровень сглаживания от 0.0 до 1.0, где: 0 - прямая линия, 1 - кубический сплайн
# При ошибке возвращает ноль

    mapSmoothingSpline1_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSmoothingSpline1', ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline1(_points: ctypes.POINTER(ctypes.c_double), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline1_t (_points, _count, _smooth)


# Построить двухмерный сглаживающий сплайн
# points - массив точек (x, y)
# count - количество точек
# smooth - уровень сглаживания от 0.0 до 1.0, где: 0 - прямая линия, 1 - кубический сплайн
# При ошибке возвращает ноль

    mapSmoothingSpline2_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSmoothingSpline2', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline2(_points: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline2_t (_points, _count, _smooth)


# Построить трёхмерный сглаживающий сплайн
# points - массив точек (x, y, h)
# count - количество точек
# smooth - уровень сглаживания от 0.0 до 1.0, где: 0 - прямая линия, 1 - кубический сплайн
# При ошибке возвращает ноль

    mapSmoothingSpline3_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSmoothingSpline3', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline3(_points: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _smooth: float) -> int:
        return mapSmoothingSpline3_t (_points, _count, _smooth)


# Построить сглаживающий сплайн подобъекта (2-х или 3-х мерный в зависимости от наличия высоты)
# hobj - сглаживаемый объект
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# smooth - уровень сглаживания от 0.0 до 1.0, где: 0 - прямая линия, 1 - кубический сплайн
# При ошибке возвращает ноль

    mapSmoothingSplineSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSmoothingSplineSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapSmoothingSplineSubject(_hobj: maptype.HOBJ, _subject: int, _smooth: float) -> int:
        return mapSmoothingSplineSubject_t (_hobj, _subject, _smooth)


# Построить сглаживающий сплайн всего объекта (2-х или 3-х мерный в зависимости от наличия высоты)
# hobj - сглаживаемый объект
# smooth - уровень сглаживания от 0.0 до 1.0, где: 0 - прямая линия, 1 - кубический сплайн
# При ошибке возвращает ноль

    mapSmoothingSplineObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSmoothingSplineObject', maptype.HOBJ, ctypes.c_double)
    def mapSmoothingSplineObject(_hobj: maptype.HOBJ, _smooth: float) -> int:
        return mapSmoothingSplineObject_t (_hobj, _smooth)


# Построить дугу по часовой стрелке заданного радиуса с заданным центром
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти, в который запишется дуга
# first - координаты первой точки дуги в метрах
# center - координаты центра дуги в метрах
# last - координаты последней точки дуги в метрах
# radius - радиус дуги в метрах
# Координаты дуги заполняются в метрах в системе исходного документа
# Применяется для коротких радиусов в пределах километров
# При ошибке возвращает ноль

    mapCreateArc_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateArc', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCreateArc(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float) -> int:
        return mapCreateArc_t (_hmap, _hobj, _first, _center, _last, _radius)


# Построить геодезическую дугу по часовой стрелке заданного радиуса с заданным центром
# hobj - идентификатор объекта карты в памяти, в который запишется дуга
# first - координаты первой точки дуги в радианах WGS84
# center - координаты центра дуги в радианах WGS84
# last - координаты последней точки дуги в радианах WGS84
# step - шаг дуги в градусах (угловой интервал между точками)
# Применяется для больших радиусов порядка десятков километров и более
# Радиус определяется по расстоянию до первой точки
# При ошибке возвращает ноль

    mapCreateGeoArc_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateGeoArc', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCreateGeoArc(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _step: float) -> int:
        return mapCreateGeoArc_t (_hobj, _first, _center, _last, _step)


# Построить геодезическую дугу по часовой стрелке заданного радиуса с заданным центром
# hobj - идентификатор объекта карты в памяти, в который запишется дуга
# center - координаты центра дуги в радианах WGS84
# startangle - истинный азимут на первую точку дуги в радианах
# endangle - истинный азимут на последнюю точку дуги в радианах
# radius - радиус дуги в метрах
# step - шаг дуги в градусах (угловой интервал между точками)
# Применяется для больших радиусов порядка десятков километров и более
# При ошибке возвращает ноль

    mapCreateGeoArcByAngle_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateGeoArcByAngle', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapCreateGeoArcByAngle(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _startangle: float, _endangle: float, _radius: float, _step: float) -> int:
        return mapCreateGeoArcByAngle_t (_hobj, _center, _startangle, _endangle, _radius, _step)


# Построить дугу заданного радиуса по трем точкам дуги в метрах
# hobj - идентификатор объекта карты в памяти, в который запишется дуга
# first - координаты первой точки дуги в метрах
# middle - координаты промежуточной точки дуги в метрах
# last - координаты последней точки дуги в метрах
# Координаты дуги заполняются в метрах в системе исходного документа
# Применяется для коротких радиусов в пределах километров
# При ошибке возвращает ноль-

    mapCreateArcByPoints_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateArcByPoints', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateArcByPoints(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _middle: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateArcByPoints_t (_hobj, _first, _middle, _last)


# Построить зону вокруг подобъекта с фильтрацией
# radius - радиус создаваемой зоны в метрах на местности
# hobj - идентификатор копии объекта, по метрике которого строится зона
#        В этот объект будет записана метрика построенной зоны
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - построить зону вокруг всех контуров
# form - тип угла: 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности), рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла, рекомендуется 3
# side - направление построения зоны: 1-справа, 2-слева, 3-с обеих сторон, 4-внешняя для полигонов,
#        5-внутренняя для полигонов
# filterprec - уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой,
#              соединяющей предыдущую и следующую точки
# Если задан прямой тип угла, то внешний угол обрезается по расстоянию от узла по
# допуску radius # cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapZoneObjectWithFilter_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapZoneObjectWithFilter', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_double)
    def mapZoneObjectWithFilter(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int, _filterprec: float) -> int:
        return mapZoneObjectWithFilter_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side, _filterprec)


# Построить зону вокруг подобъекта
# radius - радиус создаваемой зоны в метрах на местности
# hobj - идентификатор копии объекта, по метрике которого строится зона
#           В этот объект будет записана метрика построенной зоны
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - построить зону вокруг всех контуров
# form - тип угла: 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности), рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла, рекомендуется 3
# side - направление построения зоны: 1-справа, 2-слева, 3-с обеих сторон, 4-внешняя для полигонов,
#        5-внутренняя для полигонов
# Если задан прямой тип угла, то внешний угол обрезается по расстоянию от узла по
# допуску radius # cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapZoneObjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapZoneObjectEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapZoneObjectEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int) -> int:
        return mapZoneObjectEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side)


# Построить зону снаружи подобъекта
# radius - радиус создаваемой зоны в метрах на местности
# hobj - идентификатор копии объекта, по метрике которого строится зона.
#           В этот объект будет записана метрика построенной зоны.
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - построить зону вокруг всех контуров
# form - тип угла: 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности), рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла, рекомендуется 3
# side - направление построения зоны: 1-справа, 2-слева, 3-с обеих сторон, 4-внешняя для полигонов,
#           5-внутренняя для полигонов
# filterprec - уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой,
#              соединяющей предыдущую и следующую точки
# calcinmap - признак выполнения расчетов в системе карты (0/1)
# Если тип угла прямой, то внешний угол обрезается по расстоянию от узла по
# допуску radius#cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapZoneObjectWithFilterEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapZoneObjectWithFilterEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_double, ctypes.c_long)
    def mapZoneObjectWithFilterEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int, _filterprec: float, _calcinmap: int) -> int:
        return mapZoneObjectWithFilterEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side, _filterprec, _calcinmap)


# Построить зону внутри подобъекта
# radius - радиус создаваемой зоны в метрах на местности
# hobj - идентификатор копии объекта, по метрике которого строится зона.
#           В этот объект будет записана метрика построенной зоны.
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - построить зону вокруг всех контуров
# form - тип угла: 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге (в метрах на местности), рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла, рекомендуется 3
# side    - направление построения зоны: 1-справа, 2-слева, 3-с обеих сторон, 4-внешняя для полигонов,
#           5-внутренняя для полигонов
# filterprec - уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой,
#              соединяющей предыдущую и следующую точки
# calcinmap - признак выполнения расчетов в системе карты (0/1)
# Если тип угла прямой, то внешний угол обрезается по расстоянию от узла по
# допуску radius#cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapInsideZoneObjectWithFilterEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapInsideZoneObjectWithFilterEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapInsideZoneObjectWithFilterEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _filterprec: float, _calcinmap: int) -> int:
        return mapInsideZoneObjectWithFilterEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _filterprec, _calcinmap)


# Построить половину зоны вокруг заданного подобъекта
# radius - радиус создаваемой зоны (в метрах на местности)
# hobj - метрика объекта, по которому строится зона
# subject - номер подобъекта с 0, вокруг которого строим зону
# Зона строится справа от объекта по направлению цифрования
# При ошибке возвращает ноль

    mapHalfZoneObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapHalfZoneObject', ctypes.c_double, maptype.HOBJ, ctypes.c_long)
    def mapHalfZoneObject(_radius: float, _hobj: maptype.HOBJ, _subject: int) -> int:
        return mapHalfZoneObject_t (_radius, _hobj, _subject)


# Построить линейный объект, смещенный относительно заданного линейного подобъекта
# hobj - идентификатор линейного объекта, относительно которого строится смещенная линия
#        В этот же объект будет записана метрика смещенной линии вместо всей исходной метрики
# subject - номер подобъекта, относительно которого строится смещенная линия
# radius - смещение создаваемой зоны в метрах на местности
#          > 0 - смещение вправо, < 0 - смещение влево
# form - тип угла: 0 - прямой, 1 - закругленный
# arcdist - расстояние между точками по дуге для закругленного угла в метрах на местности, рекомендуется radius / 15
# cornerfactor - коэффициент для расчета максимальной длины угла для прямого угла, рекомендуется 3
# calcinmap    - признак выполнения вычислений в системе карты
# Если тип угла прямой, то внешний угол обрезается по расстоянию от узла
# по допуску radius#cornerfactor для устранения длинных углов
# При ошибке возвращает ноль

    mapOffsetLineEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOffsetLineEx', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapOffsetLineEx(_hobj: maptype.HOBJ, _subject: int, _radius: float, _form: int, _arcdist: float, _cornerfactor: float, _calcinmap: int) -> int:
        return mapOffsetLineEx_t (_hobj, _subject, _radius, _form, _arcdist, _cornerfactor, _calcinmap)


# Построить осевую линию по площадному объекту
# hmap - идентификатор открытых данных (документа)
# hobj - исходный площадной объект (простой или мультиполигон)
# haxis - линейный объект для записи результата
# width  - минимальная ширина исходного объекта в метрах или 0
# length - минимальная длина осевой линии или 0
# mode - метод построения:
#        1 - построить по объекту произвольной формы
#        2 - построить по объекту в форме ленты
#        0 - использовать оба метода
# При ошибке возвращает ноль

    mapBuildAxisLine_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildAxisLine', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapBuildAxisLine(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _haxis: maptype.HOBJ, _width: float, _length: float, _mode: int) -> int:
        return mapBuildAxisLine_t (_hmap, _hobj, _haxis, _width, _length, _mode)


# Построить фарватер (средней линии) для полигона
# hmap - идентификатор открытых данных (документа)
# hobj - исходный площадной объект, например - река, для которой строим фарватер
# haxis - объект, в метрику которого запишется результат - линейный объект c подобъектами
# width - минимальная ширина исходного объекта в метрах или 0
# length - минимальная длина участка фарватера или 0
# mode - метод построения, равен 0
# Для подобъектов hobj средняя линия не строится
# В объект haxis и его подобъекты записываются отрезки средней линии,
# построенные для участков реки шире width и длиной более length
# При width = 0 и length = 0 средняя линия строится по всему исходному объекту
# При ошибке возвращает ноль

    mapWaterwayCreate_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWaterwayCreate', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapWaterwayCreate(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _axis: maptype.HOBJ, _width: float, _length: float, _mode: int) -> int:
        return mapWaterwayCreate_t (_hmap, _hobj, _axis, _width, _length, _mode)


# Установить первую точку контура по вытянутости площадного объекта (полигона)
# hobj - идентификатор объекта карты в памяти
# Выполняется сдвиг метрики на найденную по вытянутости первую точку полигона
# Возвращает номер "последней" точки в метрике объекта, выходящей на условную осевую линию
# При ошибке возвращает ноль

    mapGetEndPointSetBeginPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEndPointSetBeginPoint', maptype.HOBJ)
    def mapGetEndPointSetBeginPoint(_hobj: maptype.HOBJ) -> int:
        return mapGetEndPointSetBeginPoint_t (_hobj)


# Замкнуть метрику объекта и всех его подобъектов для площадного или линейного объекта
# hobj - идентификатор объекта карты в памяти
# delta - порог замыкания в мм на карте в базовом масштабе или 0
# Если расстояние между первой и последней точкой меньше delta, то вместо последней точки пишем первую
# Если расстояние между первой и последней точкой больше delta, то после последней точки добавляем первую
# При ошибке возвращает ноль

    mapAbridge_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAbridge', maptype.HOBJ, ctypes.c_double)
    def mapAbridge(_hobj: maptype.HOBJ, _delta: float) -> int:
        return mapAbridge_t (_hobj, _delta)


# Замкнуть метрику подобъекта для площадного или линейного объекта
# hobj - идентификатор объекта карты в памяти
# delta - порог замыкания в мм на карте в базовом масштабе или 0
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Если расстояние между первой и последней точкой меньше delta, то вместо последней точки пишем первую
# Если расстояние между первой и последней точкой больше delta, то после последней точки добавляем первую
# При ошибке возвращает ноль

    mapAbridgeSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAbridgeSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapAbridgeSubject(_hobj: maptype.HOBJ, _subject: int, _delta: float) -> int:
        return mapAbridgeSubject_t (_hobj, _subject, _delta)


# Округлить метрику объекта по установленной точности карты (мм, см)
# hobj - идентификатор объекта карты в памяти
# Точность карты запрашивается функцией mapGetSitePrecision()
# При ошибке возвращает ноль

    mapRoundObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRoundObject', maptype.HOBJ)
    def mapRoundObject(_hobj: maptype.HOBJ) -> int:
        return mapRoundObject_t (_hobj)


# Построить ортодромию в виде массива точек
# first - геодезические координаты первой точки в радианах на эллипсоиде документа
# second - геодезические координаты второй точки в радианах на эллипсоиде документа
# array - адрес массива для записи координат построенной ортодромии, размер массива в параметре count
# count - количество точек для построения ортодромии (если точки размещены ближе 0.000001 радиан, заполняет только 2 точки)
# Ортодромия - это дуга между двумя точками на поверхности Земли по кратчайшему расстоянию
# При больших расстояниях точки дуги формируются с шагом не более 0,5 градуса,
# при малых растояниях - не чаще 10 километров, что обеспечивает определение
# длин и углов с точностью триангуляции 1 класса
# Возвращает заполненное число точек в массиве
# При ошибке возвращает ноль

    mapOrthodrome_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOrthodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapOrthodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        return mapOrthodrome_t (_first, _second, _array, _count)


# Построить ортодромию в метрику объекта
# hobj - идентификатор объекта карты в памяти, в метрику которого будет записан построенный контур
# first - геодезические координаты первой точки в радианах на эллипсоиде документа
# second - геодезические координаты второй точки в радианах на эллипсоиде документа
# Ортодромия - это дуга между двумя точками на поверхности Земли по кратчайшему расстоянию
# При больших расстояниях точки дуги формируются с шагом не более 0,5 градуса,
# при малых растояниях - не чаще 10 километров, что обеспечивает определение
# длин и углов с точностью триангуляции 1 класса
# При ошибке возвращает ноль

    mapOrthodromeObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOrthodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapOrthodromeObject(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapOrthodromeObject_t (_hobj, _first, _second)


# Построить локсодромию в виде массива точек
# first - геодезические координаты первой точки в радианах на эллипсоиде документа
# second - геодезические координаты второй точки в радианах на эллипсоиде документа
# array - адрес массива для записи координат построенной локсодромии, размер массива в параметре count
# count - количество точек для построения локсодромии
# Локсодромия - это кривая между двумя точками на поверхности Земли, пересекающая все меридианы под постоянным углом
# При ошибке возвращает ноль

    mapLoxodrome_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLoxodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapLoxodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        return mapLoxodrome_t (_first, _second, _array, _count)


# Построить локсодромию в метрику объекта
# hobj - идентификатор объекта карты в памяти
# first - геодезические координаты первой точки в радианах на эллипсоиде документа
# second - геодезические координаты второй точки в радианах на эллипсоиде документа
# Локсодромия - это кривая между двумя точками на поверхности Земли, пересекающая все меридианы под постоянным углом
# При ошибке возвращает ноль

    mapLoxodromeObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLoxodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLoxodromeObject(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapLoxodromeObject_t (_hobj, _first, _second)


# Построить географическую линию (ортодромию или локсодромию)
# sourceInfo - объект, содержащий точки исходных контуров
# destInfo - объект для записи точех кривых, построенных по каждому отрезку объекта sourceInfo
# step - шаг между точками в угловых секундах от 0.001 до 3600 (1 градус)
# method - метод построения:
#          0 - ортодромия (дуговые контуры на поверхности Земли, проходящие по кратчайшему расстоянию)
#          1 - локсодромия (дуговые контуры на поверхности Земли, пересекающие меридианы под постоянным углом)
# При ошибке возвращает ноль

    mapBuildGeoPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildGeoPath', maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapBuildGeoPath(_sourceInfo: maptype.HOBJ, _destInfo: maptype.HOBJ, _step: float, _method: int) -> int:
        return mapBuildGeoPath_t (_sourceInfo, _destInfo, _step, _method)


# Построить эллипс по двум точкам и параметрам полуосей
# hobj - идентификатор объекта карты в памяти
# centre - координаты центра эллипса в метрах на местности в системе документа
# bigaxis - большая полуось в метрах на местности
# littleaxis - малая полуось в метрах на местности
# angle - угол поворота большой полуоси в радианах против часовой стрелки от направления на восток
# count - число точек создаваемой метрики эллипса: от 16 до 256
# Создаваемый объект отображается сплайном, что позволяет минимизировать число точек метрики
# При ошибке возвращает ноль

    mapBuildEllipse_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildEllipse', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapBuildEllipse(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _bigaxis: float, _littleaxis: float, _angle: float, _count: int) -> int:
        return mapBuildEllipse_t (_hobj, _center, _bigaxis, _littleaxis, _angle, _count)


# Построить зону видимости по матрице высот в виде растрового изображения
# hmap - идентификатор открытой векторной карты
# rstname - полное имя растра
# zoneparm - параметры построения зоны (maptype.h)
# hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или 0
# flags - управляющие флаги: 1 - запретить нанесение границы зоны на растр
# Построение производится при наличии открытой матрицы высот
# Результат записывается в файл rstname
# Возвращает номер растра в цепочке
# При ошибке возвращает ноль

    mapVisibilityZonePro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapVisibilityZonePro', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), maptype.HPAINT, ctypes.c_long)
    def mapVisibilityZonePro(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _zoneparm: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), _hpaint: maptype.HPAINT, _flags: int) -> int:
        return mapVisibilityZonePro_t (_hmap, _rstname.buffer(), _zoneparm, _hpaint, _flags)


# Определить видимость точки point2 из точки point1 (координаты в метрах на местности)
# hmap - идентификатор открытой векторной карты
# point1 - координаты точки наблюдателя в метрах на местности в системе документа
# point2 - координаты наблюдаемой точки в метрах на местности в системе документа
# deltaheight1 - высота наблюдения (в метрах), добавляется к высоте в точке point1
# deltaheight2 - высота наблюдения (в метрах), добавляется к высоте в точке point2
# Вычисление производится при наличии открытой матрицы высот
# Возвращает: 0 - point2 не видна из point1
#             1 - point2 видна из point1
# При ошибке в параметрах или отсутствии матрицы возвращает "-1"

    mapVisibilityFromPointEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapVisibilityFromPointEx', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double)
    def mapVisibilityFromPointEx(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _deltaheight1: float, _deltaheight2: float) -> int:
        return mapVisibilityFromPointEx_t (_hmap, _point1, _point2, _deltaheight1, _deltaheight2)


# Создать объекты - пустоты по выделенным объектам
# hmap - идентификатор открытой векторной карты с выделенными объектами
# hsite - идентификатор векторной карты для записи объектов - пустот
# hobj - идентификатор объекта карты в памяти, граница области для создания объектов - пустот
# incode - внутренний код объекта для выбора условного знака объектов - пустот
# Возвращает количество созданных объектов - пустот
# При ошибке возвращает ноль

    mapCreateObjectVoid_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateObjectVoid', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long)
    def mapCreateObjectVoid(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _incode: int) -> int:
        return mapCreateObjectVoid_t (_hmap, _hsite, _hobj, _incode)


# Удалить петли у объекта
# hobj - идентификатор объекта карты в памяти
# precision - точность (величина расхождения координат) при проверке совпадения точек
# minsquare - минимальная площадь петли полигона, при которой петля сохраняется как подобъект
# При сохранении петель в виде подобъектов будет сформирован мультиполигон
# Если петли удалялись - возвращает -1
# При ошибке возвращает ноль

    mapDeleteLoopEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteLoopEx', maptype.HOBJ, ctypes.c_double, ctypes.c_double)
    def mapDeleteLoopEx(_hobj: maptype.HOBJ, _precision: float, _minsquare: float) -> int:
        return mapDeleteLoopEx_t (_hobj, _precision, _minsquare)


# Повернуть объект вокруг заданной точки на заданный угол
# hobj - идентификатор объекта карты в памяти
# center - координаты точки, вокруг которой поворачивается объект, в метрах в системе координат документа
# angle - угол поворота против часовой стрелки в радианах от -PI до +PI
# При ошибке возвращает ноль

    mapRotateObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRotateObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapRotateObject(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapRotateObject_t (_hobj, _center, _angle)


# Построить внешнюю границу для объектов, выделенных по условиям обобщенного поиска
# hmap - идентификатор главной карты
# hobj - объект в который записывается определенный контур
# precision - допуск согласования объектов (должен быть >= DELTANULL)
# Объекты могут быть выделены на разных картах
# Условия поиска задаются функциями mapSetTotalSeekMapRule(), mapSetSiteSeekSelectEx() и другими
# При ошибке возвращает ноль

    mapContourTotalSeekObjects_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapContourTotalSeekObjects', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapContourTotalSeekObjects(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        return mapContourTotalSeekObjects_t (_hmap, _hobj, _precision)


# Установить указанную точку замкнутого контура объекта первой
# hobj - идентификатор объекта карты в памяти
# number - номер выбранной точки с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapSetFirstPointOfLockedContour_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetFirstPointOfLockedContour', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetFirstPointOfLockedContour(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        return mapSetFirstPointOfLockedContour_t (_hobj, _number, _subject)


# Запросить содержание текста подписи
# hobj - идентификатор объекта карты в памяти
# text - адрес для размещения строки
# size - длина выделенной области под строку в байтах
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetTextUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetTextUn(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        return mapGetTextUn_t (_hobj, _text.buffer(), _size, _subject)


# Запросить длину в байтах строки, возвращаемой функцией mapGetTextUn
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapGetTextUnSize_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextUnSize', maptype.HOBJ, ctypes.c_long)
    def mapGetTextUnSize(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextUnSize_t (_hobj, _subject)


# Запросить текст подписи, который будет реально отображаться на карте
# hobj - идентификатор объекта карты в памяти
# text - адрес для размещения строки
# size - длина выделенной области под строку
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Текст подписи может содержать ссылки на семантики, которые на карте будут отображаться содержимым
# этих подписей с учетом заданного форматирования - добавления единиц измерения, округления числовых значений
# и других операций
# Например: строка #27(1)-этажный - заменится на "9-этажный", #46(#11)#55 - "7,5(9)АСФАЛЬТ" и так далее
# При ошибке возвращает ноль

    mapGetShowText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetShowText', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetShowText(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        return mapGetShowText_t (_hobj, _text.buffer(), _size, _subject)


# Установить новое содержание текстовой строки
# hobj - идентификатор объекта карты в памяти
# text - новый текст подписи в кодировке UTF-16
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# При ошибке возвращает ноль

    mapPutTextUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapPutTextUn(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _subject: int) -> int:
        return mapPutTextUn_t (_hobj, _text.buffer(), _subject)


# Установить новое содержание текста подобъекта в виде многострочного текста
# hobj - идентификатор объекта карты в памяти
# text - адрес новой строки, если text = 0, то обрабатывается ранее записанный текст подобъекта
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Если вид подписи не установлен (для графического объекта), у объекта менее двух точек
# либо расстояние между точками слишком мало - разбиение на строки не выполняется
# Разбиение на строки выполняется с учетом параметров вида подписи и расстояния между
# двумя точками подобъекта. В ходе разбиения текста записываются коды переноса строки '\n'
# При ошибке возвращает ноль

    mapPutMultilineText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutMultilineText', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapPutMultilineText(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _subject: int) -> int:
        return mapPutMultilineText_t (_hobj, _text.buffer(), _subject)


# Сформировать текст подписи и заполнить семантику по семантике подписываемого объекта
# hobj - подписываемый объект
# semcode - текст семантики для подписывания или ноль
# precision - число знаков после запятой для числовой семантики или "-1"
# prefix - текст, который вставляется перед выводимым значением семантики или 0
# postfix - текст, который вставляется после выводимого значения семантики или 0
# text - текст подписи (может включать номера семантик #XXXX) для подписывания при отсутствии семантики
# Если код семантики не задан, то значения полей precision, prefix и postfix игнорируются
# Добавляет семантики - ссылки на подпись у объекта и на объект у подписи, если у объекту
# уже присвоен уникальный номер
# При ошибке возвращает ноль

    mapBuildText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildText', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def mapBuildText(_htitle: maptype.HOBJ, _hobj: maptype.HOBJ, _semcode: int, _precision: int, _prefix: mapsyst.WTEXT, _postfix: mapsyst.WTEXT, _text: mapsyst.WTEXT) -> int:
        return mapBuildText_t (_htitle, _hobj, _semcode, _precision, _prefix.buffer(), _postfix.buffer(), _text.buffer())


# Подогнать текст по размерам прямоугольной области
# source - исходный текст
# text - буфер для размещения подогнанного текста
# textsize - размер буфера text в байтах (рекомендуется в 2 раза больше размера исходного текста)
# param - параметры обработки
# Возвращает:
#     - в исходном тексте символы переноса строки '\n' заменяются на пробелы;
#     - многострочный текст в буфере text;
#     - рекомендуемую высоту текста (FITTEXT::TextHeight);
#     - рекомендуемую высоту ячейки (FITTEXT::RectHeight);
# При ошибке возвращает 0 и код ошибки (FITTEXT::Error)

    mapFitTextForRect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFitTextForRect', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.FITTEXT))
    def mapFitTextForRect(_source: mapsyst.WTEXT, _text: mapsyst.WTEXT, _textsize: int, _param: ctypes.POINTER(maptype.FITTEXT)) -> int:
        return mapFitTextForRect_t (_source.buffer(), _text.buffer(), _textsize, _param)


# Запросить, хранится ли текст подписи в кодировке UTF16
# hobj - идентификатор объекта карты в памяти
# Если текст в UTF16 - возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsTextUnicode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTextUnicode', maptype.HOBJ)
    def mapIsTextUnicode(_hobj: maptype.HOBJ) -> int:
        return mapIsTextUnicode_t (_hobj)


# Запросить длину текста в микронах на карте
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для подписи, растягиваемой по метрике от точки до точки, возвращает 0
# При ошибке возвращает ноль

    mapGetTextLengthMkm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextLengthMkm', maptype.HOBJ, ctypes.c_long)
    def mapGetTextLengthMkm(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextLengthMkm_t (_hobj, _subject)


# Запросить высоту строки текста для объектов типа подпись в микронах
# hobj - идентификатор объекта карты в памяти
# Для подписи, растягиваемой по метрике от точки до точки, возвращает 0
# При ошибке возвращает ноль

    mapGetTextHeightMkm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextHeightMkm', maptype.HOBJ)
    def mapGetTextHeightMkm(_hobj: maptype.HOBJ) -> int:
        return mapGetTextHeightMkm_t (_hobj)


# Запросить рамку подписи в пикселах для текущих условий отображения
# hmap - идентификатор документа
# hdc - идентификатор контекста, на котором рассчитывается размер рамки, или 0
# rect - положение области отображения, относительно которой считается рамка,
#        в пикселах на документе или 0
# hobj - идентификатор объекта типа подпись, параметры отображения должны быть типа IMG_TEXT
# box - поле для записи координат 4-ех точек наклонной рамки относительно верхнего левого
#       угла области rect
# Подобъекты подписи не учитываются при расчете рамки
# При ошибке возвращает ноль

    mapGetPaintTextBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPaintTextBorder', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.HOBJ, ctypes.POINTER(maptype.DRAWBOX))
    def mapGetPaintTextBorder(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _hobj: maptype.HOBJ, _box: ctypes.POINTER(maptype.DRAWBOX)) -> int:
        return mapGetPaintTextBorder_t (_hmap, _hdc, _rect, _hobj, _box)


# Запросить способ выравнивания текста по горизонтали
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает значение: FA_LEFT, FA_RIGHT или FA_CENTER
# При ошибке возвращает ноль

    mapGetTextHorizontalAlign_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextHorizontalAlign', maptype.HOBJ, ctypes.c_long)
    def mapGetTextHorizontalAlign(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextHorizontalAlign_t (_hobj, _subject)


# Запросить способ выравнивания текста по вертикали
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает значение: FA_BOTTOM, FA_TOP, FA_BASELINE, FA_MIDDLE
# При ошибке возвращает ноль

    mapGetTextVerticalAlign_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTextVerticalAlign', maptype.HOBJ, ctypes.c_long)
    def mapGetTextVerticalAlign(_hobj: maptype.HOBJ, _subject: int) -> int:
        return mapGetTextVerticalAlign_t (_hobj, _subject)


# Установить способ выравнивания текста по горизонтали
# hobj - идентификатор объекта карты в памяти
# align - код выравнивания по горизонтали: FA_LEFT, FA_RIGHT, FA_CENTER
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - установить всем подобъектам
# По умолчанию выравнивание установлено как FA_LEFT (текст прижат к первой точке координат)
# При успешном выполнении возвращает установленное значение

    mapPutTextHorizontalAlign_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutTextHorizontalAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextHorizontalAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        return mapPutTextHorizontalAlign_t (_hobj, _align, _subject)


# Установить способ выравнивания текста по вертикали
# hobj - идентификатор объекта карты в памяти
# align - код выравнивания по вертикали: FA_BOTTOM, FA_TOP, FA_BASELINE, FA_MIDDLE
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - установить всем подобъектам
# По умолчанию выравнивание установлено как FA_BASELINE
# При успешном выполнении возвращает установленное значение

    mapPutTextVerticalAlign_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutTextVerticalAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextVerticalAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        return mapPutTextVerticalAlign_t (_hobj, _align, _subject)


# Установить способ выравнивания текста по горизонтали и вертикали
# hobj - идентификатор объекта карты в памяти
# align - код выравнивания содержит сумму кодов по горизонтали и вертикали
#           [FA_LEFT,FA_RIGHT,FA_CENTER] | [FA_BOTTOM,FA_TOP,FA_BASELINE,FA_MIDDLE]
# subject - номер объекта (0) или подобъекта (больше 0) или -1 - установить всем подобъектам
# По умолчанию выравнивание установлено как FA_LEFT | FA_BASELINE
# При успешном выполнении возвращает установленное значение

    mapPutTextAlign_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPutTextAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        return mapPutTextAlign_t (_hobj, _align, _subject)


# Запросить, имеет ли объект графическое описание
# hobj - идентификатор объекта карты в памяти
# Графическое описание имеется, как правило, у объектов векторной карты,
# не связанных с классификатором - функция mapObjectCode() возвращает ноль
# При ошибке возвращает ноль

    mapIsDrawObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDrawObject', maptype.HOBJ)
    def mapIsDrawObject(_hobj: maptype.HOBJ) -> int:
        return mapIsDrawObject_t (_hobj)


# Запросить количество элементов графического описания
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapDrawCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawCount', maptype.HOBJ)
    def mapDrawCount(_hobj: maptype.HOBJ) -> int:
        return mapDrawCount_t (_hobj)


# Запросить вид элемента графического описания по его номеру
# hobj - идентификатор объекта карты в памяти
# number - порядковый номер элемента от 1 до mapDrawCount()
# Возвращает номер функции типа IMG_XXXXXXX (описаны в mapgdi.h)
# При ошибке возвращает ноль

    mapDrawImage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawImage', maptype.HOBJ, ctypes.c_long)
    def mapDrawImage(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapDrawImage_t (_hobj, _number)


# Запросить адрес параметров элемента графического описания по его номеру
# hobj - идентификатор объекта карты в памяти
# number - порядковый номер элемента от 1 до mapDrawCount() или 0
# Возвращает адрес структуры типа IMGXXXXXX, в соответствии с видом элемента (описаны в mapgdi.h)
# Для запроса с 0 номером возвращает адрес параметров
# графического описания объекта в виде структуры IMGDRAW
# При ошибке возвращает ноль

    mapDrawParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_char_p,'mapDrawParameters', maptype.HOBJ, ctypes.c_long)
    def mapDrawParameters(_hobj: maptype.HOBJ, _number: int) -> ctypes.c_char_p:
        return mapDrawParameters_t (_hobj, _number)


# Запросить длину параметров элемента графического описания по его номеру
# hobj - идентификатор объекта карты в памяти
# number - порядковый номер элемента от 1 до mapDrawCount() или 0
# Для запроса с 0 номером возвращает длину параметров
# графического описания всех элементов
# При ошибке возвращает ноль

    mapDrawLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDrawLength', maptype.HOBJ, ctypes.c_long)
    def mapDrawLength(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapDrawLength_t (_hobj, _number)


# Загрузить внешний вид объекта типа IMGGRAPHICFILE в память RSC (освобождается при закрытии карты)
# hobj - идентификатор объекта
# number - порядковый номер элемента от 1 до mapDrawCount(), тип элемента должен быть IMGGRAPHICFILE
# size - поле для записи длины считанного графического файла
# Выделенная для файла память освобождается при закрытии карты и классификатора
# При ошибке возвращает ноль, иначе - адрес файла в памяти

    mapLoadDrawObjectViewToMemory_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapLoadDrawObjectViewToMemory', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapLoadDrawObjectViewToMemory(_hobj: maptype.HOBJ, _number: int, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapLoadDrawObjectViewToMemory_t (_hobj, _number, _size)


# Добавить элемент графического описания объектов
# hobj - идентификатор объекта карты в памяти
# image - номер функции типа IMG_XXXXXXX (описаны в mapgdi.h)
# parm - адрес структуры типа IMGXXXXXX
# При ошибке возвращает ноль, иначе - число элементов в записи

    mapAppendDraw_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAppendDraw', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p)
    def mapAppendDraw(_hobj: maptype.HOBJ, _image: int, _parm: ctypes.c_char_p) -> int:
        return mapAppendDraw_t (_hobj, _image, _parm)


# Удалить все элементы графического описания объекта
# hobj - идентификатор объекта карты в памяти

    mapClearDraw_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearDraw', maptype.HOBJ)
    def mapClearDraw(_hobj: maptype.HOBJ) -> int:
        return mapClearDraw_t (_hobj)


# Удалить элемент графического описания объекта
# hobj - идентификатор объекта карты в памяти
# number - порядковый номер элемента от 1 до mapDrawCount()
# При ошибке возвращает ноль

    mapDeleteDraw_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteDraw', maptype.HOBJ, ctypes.c_int)
    def mapDeleteDraw(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapDeleteDraw_t (_hobj, _number)


# Считать графические параметры объекта
# hobj - идентификатор объекта карты в памяти
# hdrw - идентификатор набора примитивов в памяти (создается функцией mapCreateDraw())
# При ошибке возвращает ноль

    mapReadObjectDraw_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapReadObjectDraw(_hobj: maptype.HOBJ, _hdrw: maptype.HDRAW) -> int:
        return mapReadObjectDraw_t (_hobj, _hdrw)


# Записать графические параметры в объект
# hobj - идентификатор объекта карты в памяти
# hdrw - идентификатор записываемого набора примитивов в памяти
# При ошибке возвращает ноль

    mapWriteObjectDraw_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapWriteObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapWriteObjectDraw(_hobj: maptype.HOBJ, _hdrw: maptype.HDRAW) -> int:
        return mapWriteObjectDraw_t (_hobj, _hdrw)


# Запросить обобщенные графические параметры для полигона или линейного объекта
# hobj - идентификатор объекта карты в памяти
# square - цвет полигона (на входе рекомендуется установить цвет в IMGC_TRANSPARENT для контроля изменения
# line - цвет линии и толщина в пикселах
# isalpha - признак добавления alpha-канала
# При ошибке возвращает ноль

    mapGetPolyStyleEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPolyStyleEx', maptype.HOBJ, ctypes.POINTER(mapgdi.IMGSQUARE), ctypes.POINTER(mapgdi.IMGLINE), ctypes.c_long)
    def mapGetPolyStyleEx(_hobj: maptype.HOBJ, _square: ctypes.POINTER(mapgdi.IMGSQUARE), _line: ctypes.POINTER(mapgdi.IMGLINE), _isalpha: int) -> int:
        return mapGetPolyStyleEx_t (_hobj, _square, _line, _isalpha)


# Запросить обобщенные графические параметры для полигона или линейного объекта
# hobj - идентификатор объекта карты в памяти
# square - цвет полигона (на входе рекомендуется установить цвет в IMGC_TRANSPARENT для контроля изменения
# line - цвет линии и толщина в пикселах
# При ошибке возвращает ноль

    mapGetPolyStyle_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPolyStyle', maptype.HOBJ, ctypes.POINTER(mapgdi.IMGSQUARE), ctypes.POINTER(mapgdi.IMGLINE))
    def mapGetPolyStyle(_hobj: maptype.HOBJ, _square: ctypes.POINTER(mapgdi.IMGSQUARE), _line: ctypes.POINTER(mapgdi.IMGLINE)) -> int:
        return mapGetPolyStyle_t (_hobj, _square, _line)


# Запросить, является ли карта объекта редактируемой (включая редактирование координат)
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsEdit_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsEdit', maptype.HOBJ)
    def mapIsEdit(_hobj: maptype.HOBJ) -> int:
        return mapIsEdit_t (_hobj)


# Запросить, может ли на карте объекта редактироваться семантика и графика объекта
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapIsEditWithoutMetric_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsEditWithoutMetric', maptype.HOBJ)
    def mapIsEditWithoutMetric(_hobj: maptype.HOBJ) -> int:
        return mapIsEditWithoutMetric_t (_hobj)


# Запросить, изменились ли какие-либо данные объекта в памяти: метрика, семантика, графика
# hobj - идентификатор объекта карты в памяти
# Если данные были изменены, но еще не были сохранены функцией типа mapCommitObject,
# то возвращает ненулевое значение
# Изменение кода объекта, границ видимости и других свойств эта функция не проверяет
# При наличии изменений возвращает флаг изменения: 2 - метрика, 4 - семантика, 8 - графика
# При ошибке возвращает ноль

    mapIsDirtyObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDirtyObject', maptype.HOBJ)
    def mapIsDirtyObject(_hobj: maptype.HOBJ) -> int:
        return mapIsDirtyObject_t (_hobj)


# Добавить новый объект или обновить существующий объект на карте
# hobj - идентификатор объекта карты в памяти
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# Если объект был создан в памяти и отредактирован, то он добавляется на карту
# Если объект был считан с карты и отредактирован, то он обновляется на карте
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitObject', maptype.HOBJ)
    def mapCommitObject(_hobj: maptype.HOBJ) -> int:
        return mapCommitObject_t (_hobj)


# Сохранить данные объекта в карту
# hobj - идентификатор объекта карты в памяти
# isnewobject - признак записи нового объекта (аналог mapCommitObjectAsNew)
# isload - признак записи объекта без пересчета семантики-формула (аналог mapCommitObjectForLoad)
# isorder - признак записи объектов в порядке поступления (аналог mapCommitObjectByOrder)
# error - поле для записи кода ошибки (описаны в maperr.rh)
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObjectPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitObjectPro', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectPro(_hobj: maptype.HOBJ, _isnewobject: int, _isload: int, _isorder: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCommitObjectPro_t (_hobj, _isnewobject, _isload, _isorder, _error)


# Сохранить данные объекта в карту без пересчета семантики типа формула
# Это бывает необходимо при чтении данных из базы данных или наборов данных
# hobj - идентификатор объекта карты в памяти
# error - поле для записи кода ошибки (описаны в maperr.rh)
# Номер листа в районе должен быть установлен
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitObjectForLoadEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitObjectForLoadEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectForLoadEx(_hobj: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCommitObjectForLoadEx_t (_hobj, _error)


# Добавить новый объект в карту
# hobj - идентификатор объекта карты в памяти
# error - поле для записи кода ошибки (описаны в maperr.rh)
# Объект сохраняется с новым уникальным номером и порядковым номером
# Может применяться при чтении существующего объекта, как образца, изменении координат
# и семантики и сохранении как нового объекта
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# При ошибке возвращает ноль

    mapCommitObjectAsNewEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitObjectAsNewEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectAsNewEx(_hobj: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCommitObjectAsNewEx_t (_hobj, _error)

    mapCommitObjectAsNew_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapCommitObjectAsNew', maptype.HOBJ)
    def mapCommitObjectAsNew(_info: maptype.HOBJ) -> int:
        return mapCommitObjectAsNew_t (_info)

# Сохранить данные об объекте в многолистовой карте MAP с автоматическим делением контура по листам
# hobj  - идентификатор объекта карты в памяти
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# Если объект не попал в габариты какого-либо листа - возвращает -2
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# При ошибке возвращает ноль

    mapCommitWithPlace_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitWithPlace', maptype.HOBJ)
    def mapCommitWithPlace(_hobj: maptype.HOBJ) -> int:
        return mapCommitWithPlace_t (_hobj)


# Добавить объект в многолистовой карте MAP с автоматическим делением контура по листам
# Объект будет сохранен, как новый, с присвоением нового уникального номера
# hobj  - идентификатор объекта карты в памяти
# Для объектов пользовательских карт (обстановки) достаточно mapCommitObject() - там один лист и нет границ
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# При ошибке возвращает ноль

    mapCommitWithPlaceAsNew_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitWithPlaceAsNew', maptype.HOBJ)
    def mapCommitWithPlaceAsNew(_hobj: maptype.HOBJ) -> int:
        return mapCommitWithPlaceAsNew_t (_hobj)


# Сохранить данные об объекте в многолистовой карте с обрезанием объекта по границам листа
# hobj - идентификатор объекта карты в памяти
# list - номер листа с 1, по рамке которого будет обрезан контур объекта
# При ошибке возвращает ноль

    mapCommitWithPlaceForList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitWithPlaceForList', maptype.HOBJ, ctypes.c_long)
    def mapCommitWithPlaceForList(_hobj: maptype.HOBJ, _list: int) -> int:
        return mapCommitWithPlaceForList_t (_hobj, _list)


# Запрость параметры обработки метрики линейных и площадных объектов
# hmap - идентификатор открытых данных (документа)
# parm - параметры, используемые при разрезания объектов по рамкам листов карты
# Параметры обработки метрики линейных и площадных объектов используются при сохранении объектов
# для автоматического удаления малых отрезков, малых линейных и вырожденных площадных объектов,
# которые получаются при разрезания объектов по рамкам листов карты
# Параметры применяются в функциях типа: mapCommitWithPlace, mapCommitWithPlaceAsNew, mapCommitWithPlaceForList
# При ошибке возвращает ноль

    mapGetCommitObjectParm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapGetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        return mapGetCommitObjectParm_t (_hmap, _parm)


# Установить параметры обработки метрики линейных и площадных объектов
# hmap - идентификатор открытых данных (документа)
# parm - параметры, используемые при разрезания объектов по рамкам листов карты
# Параметры обработки метрики линейных и площадных объектов используются при сохранении объектов
# для автоматического удаления малых отрезков, малых линейных и вырожденных площадных объектов,
# которые получаются при разрезания объектов по рамкам листов карты
# Параметры применяются в функциях типа: mapCommitWithPlace, mapCommitWithPlaceAsNew, mapCommitWithPlaceForList
# При ошибке возвращает ноль

    mapSetCommitObjectParm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapSetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        return mapSetCommitObjectParm_t (_hmap, _parm)


# Сохранить объект в файле с разбиением мультигеометрии на простые объекты
# hobj - идентификатор объекта карты в памяти
# forload - флаг режима загрузки: при сохранении объекта не пересчитываются семантики-формулы;
# makeset - флаг необходимости объединить полученные объекты в набор
# asnew - флаг сохранения объекта как нового, если ноль, то объект в hobj будет заменен, иначе
#           все объекты, включая основной контур, будут сохранены новыми объектами, объект переданный
#           в hobj на карте останется без изменений;
# error - буфер для возврата кода ошибки
# Если объект не содержит мультигеометрии, то он сохраняется одним объектом
# При успешном завершении в hobj останется основной контур объекта, а все его
# внешние подобъекты станут самостоятельными объектами, при необходимости объединенными
# в набор (параметр makeset)
# При ошибке возвращает ноль

    mapCommitObjectAsSimple_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCommitObjectAsSimple', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectAsSimple(_hobj: maptype.HOBJ, _forload: int, _makeset: int, _asnew: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCommitObjectAsSimple_t (_hobj, _forload, _makeset, _asnew, _error)


# Запросить, выполняется ли загрузка объекта из базы данных или набора данных
# hobj - идентификатор объекта карты в памяти
# Применяется в функциях обратного вызова для определения того, что
# выполняется функция mapCommitObjectForLoad()
# При ошибке возвращает ноль

    mapIsObjectLoading_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectLoading', maptype.HOBJ)
    def mapIsObjectLoading(_hobj: maptype.HOBJ) -> int:
        return mapIsObjectLoading_t (_hobj)


# Удалить объект карты
# hobj - идентификатор объекта карты в памяти
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# Признак удаления сразу записывается в памяти и в карте
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# При ошибке возвращает ноль

    mapDeleteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteObject', maptype.HOBJ)
    def mapDeleteObject(_hobj: maptype.HOBJ) -> int:
        return mapDeleteObject_t (_hobj)


# Удалить объект карты по его номеру
# hmap - идентификатор открытых данных (документа)
# list - последовательный номер листа с 1
# number - последовательный ноиер объекта в листе с 1
# Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
# Признак удаления сразу записывается в карте
# Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных,
# отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных
# При ошибке возвращает ноль

    mapDeleteObjectByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteObjectByNumber', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapDeleteObjectByNumber(_hmap: maptype.HMAP, _list: int, _number: int) -> int:
        return mapDeleteObjectByNumber_t (_hmap, _list, _number)


# Отменить удаление объекта карты
# hobj - идентификатор объекта карты в памяти
# Признак удаления убирается в памяти и в карте
# При ошибке возвращает ноль

    mapUndeleteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUndeleteObject', maptype.HOBJ)
    def mapUndeleteObject(_hobj: maptype.HOBJ) -> int:
        return mapUndeleteObject_t (_hobj)


# Переместить объект в цепочке объектов в конец для отображения над всеми
# hobj - идентификатор объекта карты в памяти
# Объекту присваивается признак "выше всех"
# Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber()
# При ошибке возвращает ноль

    mapUpdateObjectUp_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateObjectUp', maptype.HOBJ)
    def mapUpdateObjectUp(_hobj: maptype.HOBJ) -> int:
        return mapUpdateObjectUp_t (_hobj)


# Переместить объект в цепочке объектов в начало для отображения под всеми
# hobj - идентификатор объекта карты в памяти
# Объекту присваивается признак "ниже всех"
# Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber()
# При ошибке возвращает ноль

    mapUpdateObjectDown_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateObjectDown', maptype.HOBJ)
    def mapUpdateObjectDown(_hobj: maptype.HOBJ) -> int:
        return mapUpdateObjectDown_t (_hobj)


# Сбросить признаки "выше всех" и "ниже всех" в объекте
# hobj - идентификатор объекта карты в памяти
# Положение объекта в соответствии с его слоем и локализацией изменится только после сортировки карты
# При ошибке возвращает ноль

    mapUpdateObjectNormal_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateObjectNormal', maptype.HOBJ)
    def mapUpdateObjectNormal(_hobj: maptype.HOBJ) -> int:
        return mapUpdateObjectNormal_t (_hobj)


# Запросить признаки размещения объекта "выше всех" и "ниже всех"
# hobj - идентификатор объекта карты в памяти
# Возвращает код размещения объекта: 2 - над всеми, 3 - под всеми, 1 - не задано
# При ошибке возвращает ноль

    mapObjectUpDownState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapObjectUpDownState', maptype.HOBJ)
    def mapObjectUpDownState(_hobj: maptype.HOBJ) -> int:
        return mapObjectUpDownState_t (_hobj)


# Отменить удаление объекта карты по его номеру
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# list - последовательный номер листа с 1
# number - последовательный ноиер объекта в листе c 1
# Признак удаления объекта убирается в карте
# При ошибке возвращает ноль

    mapUndeleteObjectByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUndeleteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapUndeleteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _number: int) -> int:
        return mapUndeleteObjectByNumber_t (_hmap, _hsite, _list, _number)


# Восстановить в памяти данные об объекте из карты
# hobj - идентификатор объекта карты в памяти
# Номер листа в районе и номер объекта должны быть установлены
# При ошибке возвращает ноль

    mapRevertObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRevertObject', maptype.HOBJ)
    def mapRevertObject(_hobj: maptype.HOBJ) -> int:
        return mapRevertObject_t (_hobj)


# Восстановить копию объекта, по состоянию до выполнения заданной транзакции
# hobj - идентификатор объекта карты в памяти
# number - номер транзакции
# При ошибке возвращает ноль

    mapRestoreBackObjectByAction_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRestoreBackObjectByAction', maptype.HOBJ, ctypes.c_long)
    def mapRestoreBackObjectByAction(_hobj: maptype.HOBJ, _number: int) -> int:
        return mapRestoreBackObjectByAction_t (_hobj, _number)


# Восстановить копию объекта, по состоянию до выполнения транзакции, ближайшей к заданному времени
# hobj - идентификатор объекта карты в памяти
# number - номер транзакции
# При ошибке возвращает ноль

    mapRestoreBackObjectByTime_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRestoreBackObjectByTime', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRestoreBackObjectByTime(_hobj: maptype.HOBJ, _date: int, _time: int) -> int:
        return mapRestoreBackObjectByTime_t (_hobj, _date, _time)


# Считать в объект метрику мультимасштабного объекта заданного уровня
# hobj - идентификатор объекта карты в памяти
# level - уровень генерализации контура от 1 до 4
# Если для заданного уровня контура нет, то считывается соседний более сжатый
# контур, если его нет, то менее сжатый
# Если у объекта нет дополнительных контуров - возвращает ноль
# Возвращает номер считанного уровня
# При ошибке возвращает ноль

    mapLoadMulticontourLevel_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLoadMulticontourLevel', maptype.HOBJ, ctypes.c_long)
    def mapLoadMulticontourLevel(_hobj: maptype.HOBJ, _level: int) -> int:
        return mapLoadMulticontourLevel_t (_hobj, _level)


# Записать в объект дату, время создания или редактирования объекта и имя оператора
# hobj - идентификатор объекта карты в памяти
# Для вновь создаваемого объекта пишется дата и время создания SEMOBJECTDATE
# и SEMOBJECTTIME, имя оператора пишется в семантику SEMOBJECTAUTHOR
# Для редактируемого объекта пишется (при отсутствии) или изменяется (при наличии)
# время последнего редактирования SEMOBJECTREDATE и SEMOBJECTRETIME,
# имя оператора пишется в семантику SEMOBJECTREAUTHOR (SEMOBJECTREAUTHOR)
# При ошибке возвращает 0

    mapSetObjectEditDateTime_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectEditDateTime', maptype.HOBJ)
    def mapSetObjectEditDateTime(_hobj: maptype.HOBJ) -> int:
        return mapSetObjectEditDateTime_t (_hobj)


# Вычисление длины участка объекта на эллипсоиде (местности), начиная с указанной точки
# hobj - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для последней точки вычисляет расстояние до первой точки
# У замкнутых объектов первая и последняя точки совпадают
# Расчет выполняется на основе геодезических вычислений на эллипсоиде
# Для точек, удаленных по долготе более чем на 5 градусов, расчет выполняется по ортодромии
# При ошибке возвращает ноль (при совпадении точек также вернет ноль)

    mapSideLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSideLength', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideLength(_hobj: maptype.HOBJ, _number: int, _subject: int = 0) -> float:
        return mapSideLength_t (_hobj, _number, _subject)


# Вычисление длины участка объекта на эллипсоиде (местности), начиная с указанной точки
# hobj - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# length - поле для записи результата вычисления
# Для последней точки вычисляет расстояние до первой точки
# У замкнутых объектов первая и последняя точки совпадают
# Расчет выполняется на основе геодезических вычислений на эллипсоиде
# Для точек, удаленных по долготе более чем на 5 градусов, расчет выполняется по ортодромии
# При ошибке возвращает ноль

    mapSideLengthEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSideLengthEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSideLengthEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSideLengthEx_t (_hobj, _number, _subject, _length)


# Вычисление длины участка объекта на карте, начиная с указанной точки
# hobj  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Для последней точки вычисляет расстояние до первой точки
# Вычисляет корень квадратный из суммы квадратов приращений координат
# При ошибке возвращает ноль

    mapSideLengthInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSideLengthInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideLengthInMap(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideLengthInMap_t (_hobj, _number, _subject)


# Установить метод для расчета расстояний и площадей
# hmap - идентификатор открытых данных (документа)
# method - метод выполнения расчетов: 0 - выполнять геодезические вычисления на эллипсоиде,
#          1 - выполнять геометрические вычисления в текущей проекции документа
# Если текущая проекция документа топографическая (UTM, Гаусса-Крюгера), то результаты
# вычислений двумя методами будут совпадать по мере приближения точек к осевому меридиану
# Возвращает предыдущее значение условия

    mapSetCalculationConventional_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCalculationConventional', maptype.HMAP, ctypes.c_long)
    def mapSetCalculationConventional(_hmap: maptype.HMAP, _flag: int) -> int:
        return mapSetCalculationConventional_t (_hmap, _flag)


# Запросить текущий метод для расчета расстояний и площадей по карте
# hmap - идентификатор открытых данных (документа)
# Возвращает метод выполнения расчетов : 0 - выполнять геодезические вычисления на эллипсоиде,
#          1 - выполнять геометрические вычисления в текущей проекции документа
# Если текущая проекция документа топографическая (UTM, Гаусса-Крюгера), то результаты
# вычислений двумя методами будут совпадать по мере приближения точек к осевому меридиану

    mapGetCalculationConventional_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCalculationConventional', maptype.HMAP)
    def mapGetCalculationConventional(_hmap: maptype.HMAP) -> int:
        return mapGetCalculationConventional_t (_hmap)


# Вычисление длины участка объекта заданным методом
# hobj - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Вычисление выполняется на карте или на эллипсоиде, в зависимости от текущего метода вычислений,
# установленного в mapSetCalculationConventional()
# При ошибке возвращает ноль

    mapConventionalSideLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapConventionalSideLength', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapConventionalSideLength(_hobj: maptype.HOBJ, _number: int, _subject: int = 0) -> float:
        return mapConventionalSideLength_t (_hobj, _number, _subject)


# Вычисление азимута участка объекта (стороны)
# hobj  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает величину угла в радианах между направлением меридиана, проходящего через первую точку на север,
# и стороной объекта
# Если в документе геодезия не поддерживается (крупномасштабный план), то вычисляется дирекционный угол
# между направлением на север (вертикаль) и стороной объекта
# Для цилиндрических проекций азимут и дирекционный угол совпадают
# Для последней точки вычисляет направление на первую точку
# У замкнутых объектов первая и последняя точки совпадают
# При ошибке возвращает ноль

    mapSideAzimuth_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSideAzimuth', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideAzimuth(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideAzimuth_t (_hobj, _number, _subject)


# Вычисление азимута участка объекта (стороны)
# hobj  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# azimuth - поле для записи вычисленного угла
# Возвращает величину угла в радианах между направлением касательной меридиана,
# проходящего через первую точку на север, и направлениемна вторую точку
# Для последней точки вычисляет направление на первую точку
# При ошибке возвращает ноль

    mapSideAzimuthEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSideAzimuthEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSideAzimuthEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _azimuth: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSideAzimuthEx_t (_hobj, _number, _subject, _azimuth)


# Вычисление дирекционного угла участка объекта (стороны) в системе координат документа
# hobj  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер подобъекта (если = 0, обрабатывается объект)
# Возвращает величину угла в радианах между направлением на север (вертикаль) и стороной объекта
# Дирекционный угол зависит от текущей системы координат документа
# Для последней точки вычисляет направление на первую точку
# У замкнутых объектов первая и последняя точки совпадают
# При ошибке возвращает ноль

    mapSideDirection_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSideDirection', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideDirection(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideDirection_t (_hobj, _number, _subject)


# Вычисление дирекционного угла участка объекта (стороны) по координатам в системе карты
# hobj  - идентификатор объекта карты в памяти
# number - номер точки, начиная с 1
# subject - номер контура объекта (0) или контура подобъекта (больше 0), контура содержат не менее 1 точки
# Возвращает величину угла в радианах между направлением на север (вертикаль) и стороной объекта
# При ошибке возвращает ноль

    mapSideDirectionInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSideDirectionInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideDirectionInMap(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        return mapSideDirectionInMap_t (_hobj, _number, _subject)


# Вычисление площади объекта на местности
# hobj - идентификатор объекта карты в памяти
# Для вычисления площади объекта его координаты пересчитываются
# в проекцию топографической карты ближайшей зоны
# При ошибке возвращает ноль

    mapSquare_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSquare', maptype.HOBJ)
    def mapSquare(_hobj: maptype.HOBJ) -> float:
        return mapSquare_t (_hobj)


# Вычисление площади объекта на местности
# hobj - идентификатор объекта карты в памяти
# square - поле для записи значения площади
# Для вычисления площади объекта его координаты пересчитываются
# в проекцию топографической карты ближайшей зоны
# При ошибке возвращает ноль

    mapSquareEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSquareEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapSquareEx(_hobj: maptype.HOBJ, _square: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapSquareEx_t (_hobj, _square)


# Вычисление уточненной площади объекта на местности
# hobj - идентификатор объекта карты в памяти
# Для вычисления площади объекта его контур делится на участки,
# занимающие по долготе не более 6 градусов для повышения точности
# Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны
# Для корректных вычислений контура не должны иметь самопересечений
# При ошибке возвращает ноль

    mapPrecisionSquare_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapPrecisionSquare', maptype.HOBJ)
    def mapPrecisionSquare(_hobj: maptype.HOBJ) -> float:
        return mapPrecisionSquare_t (_hobj)


# Вычисление площади объекта в системе координат карты
# hobj - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapSquareInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSquareInMap', maptype.HOBJ)
    def mapSquareInMap(_hobj: maptype.HOBJ) -> float:
        return mapSquareInMap_t (_hobj)


# Вычисление площади объекта заданным методом
# hobj - идентификатор объекта карты в памяти
# Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости от текущего метода вычислений,
# установленного в mapSetCalculationConventional()
# При ошибке возвращает ноль

    mapConventionalSquare_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapConventionalSquare', maptype.HOBJ)
    def mapConventionalSquare(_hobj: maptype.HOBJ) -> float:
        return mapConventionalSquare_t (_hobj)


# Вычисление площади контура отдельного подобъекта заданным методом
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0)
# Вычисление выполняется на карте или на эллипсоиде, в зависимости от текущего метода вычислений,
# установленного в mapSetCalculationConventional()
# При ошибке возвращает ноль

    mapConventionalSubjectSquare_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapConventionalSubjectSquare', maptype.HOBJ, ctypes.c_long)
    def mapConventionalSubjectSquare(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapConventionalSubjectSquare_t (_hobj, _subject)


# Вычисление уточненной площади контура отдельного подобъекта
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0)
# Для вычисления площади контур делится на участки,
# занимающие по долготе не более 6 градусов для повышения точности
# Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны
# Для корректных вычислений контура не должны иметь самопересечений
# При ошибке возвращает ноль

    mapPrecisionSubjectSquare_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapPrecisionSubjectSquare', maptype.HOBJ, ctypes.c_long)
    def mapPrecisionSubjectSquare(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapPrecisionSubjectSquare_t (_hobj, _subject)


# Вычисление площади подобъекта в системе координат карты
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0)
# При ошибке возвращает ноль

    mapSubjectSquareInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSubjectSquareInMap', maptype.HOBJ, ctypes.c_long)
    def mapSubjectSquareInMap(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectSquareInMap_t (_hobj, _subject)


# Вычисление площади объекта c учетом рельефа
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# step - шаг интерполяции в метрах (размер ячейки, на которой высота принимается одинаковой),
# если 0 - то вычисляется автоматически
# При отсутствии рельефа (матрицы высот, слоев, TIN-модели) вычисляет без учета рельефа
# Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны
# При ошибке возвращает ноль

    mapSquareWithHeightEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSquareWithHeightEx', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapSquareWithHeightEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _step: float) -> float:
        return mapSquareWithHeightEx_t (_hmap, _hobj, _step)


# Вычисление длины объекта на местности
# hobj - идентификатор объекта карты в памяти
# length - поле для записи вычисленной длины объекта
# Для подобъектов считается суммарная длина
# При вычислении длины объекта его координаты пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapLengthEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapLengthEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapLengthEx(_hobj: maptype.HOBJ, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapLengthEx_t (_hobj, _length)


# Вычисление длины объекта на местности
# hobj - идентификатор объекта карты в памяти
# Для подобъектов считается суммарная длина
# При вычислении длины объекта его координаты пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapLength', maptype.HOBJ)
    def mapLength(_hobj: maptype.HOBJ) -> float:
        return mapLength_t (_hobj)


# Вычисление длины объекта в системе координат карты
# hobj - идентификатор объекта карты в памяти
# Координаты объекта не пересчитываются к топокарте, длины отрезков вычисляются геометрическим методом
# Полученная длина для некоторых популярных проекций может в разы отличаться от реальной длины объекта на местности
# Для подобъектов считается суммарная длина
# При ошибке возвращает ноль

    mapLengthInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapLengthInMap', maptype.HOBJ)
    def mapLengthInMap(_hobj: maptype.HOBJ) -> float:
        return mapLengthInMap_t (_hobj)


# Вычисление длины объекта от начала до заданной точки рядом с контуром
# hobj - идентификатор объекта карты в памяти
# point - координаты точки, расположенной вблизи объекта
# Если точка не на объекте - ищется ближайшая точка на контуре
# Координаты точки обновляются найденной точкой на контуре
# При вычислении длины объекта его координаты пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapLengthToPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapLengthToPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLengthToPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapLengthToPoint_t (_hobj, _point)


# Вычисление длины подобъекта или всего объекта на местности
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта: 0 или более - вычисляется длина подобъекта
#           -1 - вычисляется суммарная длина всех подобъектов
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов мультиполигона
# При вычислении длины объекта его координаты пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapSubjectLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSubjectLength', maptype.HOBJ, ctypes.c_long)
    def mapSubjectLength(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectLength_t (_hobj, _subject)


# Вычисление длины объекта или подобъекта в проекции карты
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта: 0 или более - вычисляется длина подобъекта
#           -1 - вычисляется суммарная длина всех подобъектов;
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов
# Координаты объекта не пересчитываются к топокарте, длины отрезков вычисляются геометрическим методом
# При ошибке возвращает ноль

    mapSubjectLengthInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapSubjectLengthInMap', maptype.HOBJ, ctypes.c_long)
    def mapSubjectLengthInMap(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapSubjectLengthInMap_t (_hobj, _subject)


# Вычисление длины объекта или подобъекта заданным методом
# hobj - идентификатор объекта карты в памяти
# subject - номер подобъекта: 0 или более - вычисляется длина подобъекта;
#           -1 - вычисляется суммарная длина всех подобъектов;
#           -2 - вычисляется суммарная длина всех главных (внешних) подобъектов
# Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости от текущего метода вычислений,
# установленного в mapSetCalculationConventional()
# При ошибке возвращает ноль

    mapConventionalSubjectLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapConventionalSubjectLength', maptype.HOBJ, ctypes.c_long)
    def mapConventionalSubjectLength(_hobj: maptype.HOBJ, _subject: int) -> float:
        return mapConventionalSubjectLength_t (_hobj, _subject)


# Вычисление длины объекта c учетом рельефа
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# При отсутствии данных о рельефе (матрицы высот, слоев, TIN-модели) возвращает длину объекта
# При вычислении длины объекта его координаты пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapLengthWithHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapLengthWithHeight', maptype.HMAP, maptype.HOBJ)
    def mapLengthWithHeight(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> float:
        return mapLengthWithHeight_t (_hmap, _hobj)


# Вычисление периметра объекта
# hobj - идентификатор объекта карты в памяти
# При вычислении координаты объекта пересчитываются
# в проекцию топографической карты по каждому отрезку отдельно
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapPerimeter_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapPerimeter', maptype.HOBJ)
    def mapPerimeter(_hobj: maptype.HOBJ) -> float:
        return mapPerimeter_t (_hobj)


# Определение замкнутости контура подобъекта
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0)
# Возвращает: 1 - объект замкнут, иначе - 0

    mapCircuitousSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCircuitousSubject', maptype.HOBJ, ctypes.c_long)
    def mapCircuitousSubject(_hobj: maptype.HOBJ, _subject: int = 0) -> int:
        return mapCircuitousSubject_t (_hobj, _subject)


# Определение кратчайшего расстояния от точки до объекта
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# subject - номер контура объекта (0) или контура подобъекта (больше 0)
# Координаты точки point заданы в плоской прямоугольной системе координат документа в метрах на местности
# При вычислении координаты пересчитываются в проекцию топографической карты
# с установкой осевого меридиана в центре отрезка
# Возвращает вычисленное расстояние в метрах
# При ошибке возвращает ноль

    mapDistancePointSubject_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapDistancePointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointSubject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistancePointSubject_t (_hmap, _hobj, _subject, _point)


# Определение кратчайшего расстояния от точки до объекта, включая подобъекты
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта карты в памяти
# point - координаты точки в системе координат документа
# При вычислении координаты пересчитываются в проекцию топографической карты
# с установкой осевого меридиана в центре отрезка
# Возвращает вычисленное расстояние в метрах
# При ошибке возвращает ноль

    mapDistancePointObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapDistancePointObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistancePointObject_t (_hmap, _hobj, _point)


# Определение кратчайшего расстояния между объектами
# hobj1 - идентификатор 1-го объекта карты в памяти
# hobj2 - идентификатор 2-го объекта карты в памяти
# При вычислении координаты найденных ближайших точек пересчитываются в проекцию топографической карты
# с установкой осевого меридиана в центре отрезка
# Возвращает вычисленное расстояние в метрах
# При ошибке возвращает ноль

    mapDistanceObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapDistanceObject', maptype.HOBJ, maptype.HOBJ)
    def mapDistanceObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> float:
        return mapDistanceObject_t (_hobj1, _hobj2)


# Определение кратчайшего расстояния между объектами и координат точек на контурах объектов
# hobj1 - идентификатор первого объекта карты в памяти
# hobj2 - идентификатор второго объекта карты в памяти
# point1 - координаты первой точки линии кратчайшего расстояния
#          между объектами (на объекте hobj1)
# point2 - координаты второй точки линии кратчайшего расстояния
#          между объектами (на объекте hobj2)
# При вычислении координаты найденных ближайших точек пересчитываются в проекцию топографической карты
# с установкой осевого меридиана в центре отрезка
# Возвращает вычисленное расстояние  в метрах
# или большое значение (100000001) в случае ошибки

    mapDistanceObjectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapDistanceObjectEx', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistanceObjectEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistanceObjectEx_t (_hobj1, _hobj2, _point1, _point2)


# Прямая геодезическая задача на эллипсоиде
# hmap - идентификатор открытых данных (документа) или 0 (координаты на WGS84)
# b - широта исходной точки в радианах в геодезической системе координат документа или WGS84
# l - долгота исходной точки в радианах в геодезической системе координат документа или WGS84
# angle1 - азимут на вторую точку в радианах
# distance - расстояние до второй точки в метрах на местности
# b2 - широта найденной точки в радианах в геодезической системе координат документа или WGS84
# l2 - долгота найденной точки в радианах в геодезической системе координат документа или WGS84
# angle2 - рассчитанный азимут со второй точки на первую в радианах
#          (если angle2 равен 0, то обратный азимут не вычисляется)
# Для расстояния не более 250 км координаты определяются с ошибкой до 0,0001",
# а обратный азимут - до 0,001", что соответствует триангуляции 1 класса
# Способ вспомогательной точки по методу Красовского
# Метод предназначен для расстояний меньше радиуса Земли
# Вычисления выполняются на текущем эллипсоиде, установленном в документе - mapSetDocProjection
# Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
# При ошибке возвращает ноль

    mapDirectPositionComputation_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDirectPositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapDirectPositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _angle1: float, _distance: float, _b2: ctypes.POINTER(ctypes.c_double), _l2: ctypes.POINTER(ctypes.c_double), _angle2: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapDirectPositionComputation_t (_hmap, _b1, _l1, _angle1, _distance, _b2, _l2, _angle2)


# Обратная геодезическая задача на эллипсоиде
# hmap - идентификатор открытых данных (документа) или 0 (координаты на WGS84)
# b - широта исходной точки в радианах в геодезической системе координат документа или WGS84
# l - долгота исходной точки в радианах в геодезической системе координат документа или WGS84
# b2 - широта найденной точки в радианах в геодезической системе координат документа или WGS84
# l2 - долгота найденной точки в радианах в геодезической системе координат документа или WGS84
# angle - рассчитанный азимут с первой точки на вторую в радианах
# Для расстояния не более 180 градусов по широте
# Выполняется построение ортодромии функцией mapOrthodromeObject и запрос длины объекта и азимута первого отрезка
# Точность порядка точности триангуляции 1 класса
# Вычисления выполняются на текущем эллипсоиде, установленном в документе - mapSetDocProjection
# Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
# Возвращает расстояние между заданными точками на текущем эллипсоиде в метрах на местности
# При ошибке возвращает ноль

    mapInversePositionComputation_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapInversePositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapInversePositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _b2: float, _l2: float, _angle: ctypes.POINTER(ctypes.c_double)) -> float:
        return mapInversePositionComputation_t (_hmap, _b1, _l1, _b2, _l2, _angle)


# Определить центр и радиус окружности, проходящей через три точки
# first - координаты первой точки на эллипсоиде WGS84 в радианах
# middle - координаты второй точки на эллипсоиде WGS84 в радианах
# last - координаты третьей точки в радианах
# center - рассчитанные координаты центра окружности в радианах
# Рекомендуется применять для расчетов окружностей с радиусом в пределах 500 000 метров
# Возвращает длину радиуса окружности в метрах на местности
# При ошибке в параметрах или расположении точек на одной линии возвращает ноль

    mapGetGeoCircleRadius_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetGeoCircleRadius', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetGeoCircleRadius(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _middle: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapGetGeoCircleRadius_t (_first, _middle, _last, _center)


# Вычисление расстояния между двумя точками на плоскости
# point1 - координаты первой точки в метрах
# point2 - координаты второй точки в метрах
# Расстояние вычисляется геометрическим методом
# При ошибке возвращает ноль

    mapDistance_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapDistance', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistance(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapDistance_t (_point1, _point2)


# Вычисление расстояния между двумя точками на местности
# hmap - идентификатор открытых данных (документа)
# point1 - координаты первой точки в метрах в системе координат документа
# point2 - координаты второй точки в метрах в системе координат документа
# Для вычисления расстояния координаты пересчитываются в проекцию топографической карты
# с установкой осевого меридиана в центре отрезка
# При ошибке возвращает ноль

    mapRealDistance_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapRealDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRealDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapRealDistance_t (_hmap, _point1, _point2)


# Вычисление расстояния между двумя точками заданным методом
# hmap - идентификатор открытых данных (документа)
# point1 - координаты первой точки в метрах в системе координат документа
# point2 - координаты второй точки в метрах в системе координат документа
# Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости
# от текущего метода вычислений, установленного в mapSetCalculationConventional()
# При ошибке возвращает ноль

    mapConventionalDistance_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapConventionalDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapConventionalDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapConventionalDistance_t (_hmap, _point1, _point2)


# Определение направления биссектрисы угла, заданного тремя точками
# point1 - координаты первой точки угла в метрах в системе координат документа
# point2 - координаты центра угла в метрах в системе координат документа
# point3 - координаты последней точки угла в метрах в системе координат документа
# Возвращаемый дирекционный угол в радианах задан относительно вертикальной оси X, его положительное
# направление соответствует положительному направлению горизонтальной оси Y
# При ошибке возвращает ноль

    mapBisectorAngle_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapBisectorAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapBisectorAngle(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _p3: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapBisectorAngle_t (_p1, _p2, _p3)


# Определение положения проекции точки на векторе, заданном точкой и азимутом
# base - координаты точки основания вектора в радианах в системе WGS84 (широта, долгота)
# angle - азимут (угол от касательной к меридиану в базовой точке до направления вектора
#         по часовой стрелке)
# point - координаты точки, для которой строится проекция на вектор, в радианах системе WGS84
# target - координаты точки проекции на векторе в радианах в системе WGS84
# Рекомендуется применять для расстояний менее 3 градусов по долготе
# При ошибке возвращает ноль

    mapSeekPointOnVectorGeoWGS84_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekPointOnVectorGeoWGS84', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointOnVectorGeoWGS84(_base: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapSeekPointOnVectorGeoWGS84_t (_base, _angle, _point, _target)


# Определить положение точки относительно прямой
# point - координаты точки в метрах в системе координат документа
# first - координаты первой точки отрезка на линии в метрах в системе координат документа
# last  - координаты второй точки отрезка на линии в метрах в системе координат документа
# Возвращаемое значение: 1 - точка слева, 0 - точка справа или на линии

    mapGetLineSideForPoint_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLineSideForPoint', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetLineSideForPoint(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _first: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapGetLineSideForPoint_t (_point, _first, _last)


# Вычисление дирекционного угла по двум точкам
# point1 - координаты точки 1 в метрах в заданной плоской прямоугольной системе координат
# point2 - координаты точки 2 в метрах в заданной плоской прямоугольной системе координат
# Возвращает величину угла в радианах между направлением на север (вертикаль) и
# направлением от первой точки до второй
# Дирекционный угол зависит от текущей системы координат документа
# При ошибке возвращает ноль

    mapGetDirectionAngle_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetDirectionAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetDirectionAngle(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        return mapGetDirectionAngle_t (_point1, _point2)


# Установить заданную длину отрезка между точками с исходными координатами x1,y1 и x2,y2
# x1 - координата первой точки в метрах на север в системе координат документа
# y1 - координата первой точки в метрах на восток в системе координат документа
# x2 - координата второй точки в метрах на север в системе координат документа
# y2 - координата второй точки в метрах на восток в системе координат документа
# delta - новое расстояние в соответствии с котором по вектору сдвигается 1-я или 2-я точка
# number - номер редактируемой точки: 1 или 2
# Для определения координат выполняются геометрические вычисления
# Для выполнения геодезических вычислений применяется функция mapDirectPositionComputation()
# При ошибке возвращает ноль

    mapSetLineLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetLineLength', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_long)
    def mapSetLineLength(_x1: ctypes.POINTER(ctypes.c_double), _y1: ctypes.POINTER(ctypes.c_double), _x2: ctypes.POINTER(ctypes.c_double), _y2: ctypes.POINTER(ctypes.c_double), _delta: float, _number: int) -> int:
        return mapSetLineLength_t (_x1, _y1, _x2, _y2, _delta, _number)


# Построить перпендикуляры к отрезку, заданному двумя точками (p1 и p2)
# p1 - координаты первой точки отрезка в метрах
# p2 - координаты второй точки отрезка в метрах
# forwleft - поле для записи координат левого перпендикуляра от второй точки или 0
# forwright - поле для записи координат правого перпендикуляра от второй точки или 0
# backleft - поле для записи координат левого перпендикуляра от первой точки или 0
# backright - поле для записи координат правого перпендикуляра от первой точки или 0
# size - длина перпендикуляров в метрах
# Построения производятся в координатах карты, без пересчета длины с учетом проекции
# При ошибке возвращает ноль

    mapSeekNormalInMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekNormalInMap', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapSeekNormalInMap(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _forwleft: ctypes.POINTER(maptype.DOUBLEPOINT), _forwright: ctypes.POINTER(maptype.DOUBLEPOINT), _backleft: ctypes.POINTER(maptype.DOUBLEPOINT), _backright: ctypes.POINTER(maptype.DOUBLEPOINT), _size: float) -> int:
        return mapSeekNormalInMap_t (_p1, _p2, _forwleft, _forwright, _backleft, _backright, _size)


# Освободить ресурсы ядра перед закрытием приложения и
# освобождением библиотеки "gis64acces.dll"

    mapCloseMapAccess_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCloseMapAccess')
    def mapCloseMapAccess() -> int:
        return mapCloseMapAccess_t ()


# Запросить текущее время в формате "HH:MM:SS" в кодировке UTF16
# buffer - адрес памяти для размещения результата запроса
# size - размер выделенной памяти в байтах
# При ошибке возвращает ноль

    mapGetTheTimeUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTheTimeUn', maptype.PWCHAR, ctypes.c_long)
    def mapGetTheTimeUn(_buffer: mapsyst.WTEXT, _size: int) -> int:
        return mapGetTheTimeUn_t (_buffer.buffer(), _size)


# Запросить текущее время в формате "HH:MM:SS"
# buffer - адрес памяти для размещения результата запроса
# size - размер выделенной памяти в байтах
# При ошибке возвращает ноль

    mapGetTheTime_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTheTime', ctypes.c_char_p, ctypes.c_long)
    def mapGetTheTime(_buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetTheTime_t (_buffer, _size)


# Определить тип файла по его имени
# name - полный путь к файлу
# Анализируются первые 4 байта, содержащие идентификатор данных
# При ошибке возвращает ноль, иначе - идентификатор файла: FILE_SXF, FILE_MAP, FILE_MTW, ...
# Дополнительно различает MAP (FILE_MAP) и SIT (FILE_MAPSIT)
# Имя может быть в виде ALIAS#XXXX для карт на ГИС Сервере

    mapCheckFileExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckFileExUn', maptype.PWCHAR)
    def mapCheckFileExUn(_name: mapsyst.WTEXT) -> int:
        return mapCheckFileExUn_t (_name.buffer())


# Запросить реальный путь к файлу по пути к файлу, который может быть ссылкой
# name - полный путь к файлу
# outname - буфер для записи пути к реальному файлу (совпадает с исходным или определен из записи ".ref")
# size - размер буфера в байтах
# Если в файле строка ".ref путь или URL" - вернет реальный путь или URL
# Строка .ref в файле должна быть в кодировке UTF-8
# При ошибке возвращает ноль

    mapGetFileNameForRefFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetFileNameForRefFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetFileNameForRefFile(_name: mapsyst.WTEXT, _outname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetFileNameForRefFile_t (_name.buffer(), _outname.buffer(), _size)


# Сравнить содержимое файлов
# first - полный путь к первому файлу
# second - полный путь ко второму файлу
# Дата и время обновления файлов игнорируются
# При несовпадении возвращает ноль, иначе - ненулевое значение

    mapCompareFiles_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareFiles', maptype.PWCHAR, maptype.PWCHAR)
    def mapCompareFiles(_first: mapsyst.WTEXT, _second: mapsyst.WTEXT) -> int:
        return mapCompareFiles_t (_first.buffer(), _second.buffer())


# Выделить имя крайней папки из пути
# path - путь к папке, который завершается символом прямой '\\' или обратный слэш '/'
# При ошибке возвращает ноль

    mapGetFolderFromPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetFolderFromPath', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapGetFolderFromPath(_path: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        return mapGetFolderFromPath_t (_path.buffer(), _folder.buffer(), _size)


# Установить путь к директории приложения
# path - путь к директории (папке) приложения
# В директории приложения располагаются вспомогательные файлы
# для функционирования ГИС-ядра: библиотеки ядра, библиотеки отрисовки программируемых знаков #.iml,
# файлы базы данных epsg.# и другие файлы
# Рекомендуется устанавливать путь при запуске приложения

    mapSetPathShellUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetPathShellUn', maptype.PWCHAR)
    def mapSetPathShellUn(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetPathShellUn_t (_path.buffer())


# Запросить путь к директории приложения
# path - буфер для записи пути к директории (папке) приложения
# size - длина буфера в байтах

    mapGetPathShellUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapGetPathShellUn', maptype.PWCHAR, ctypes.c_long)
    def mapGetPathShellUn(_path: mapsyst.WTEXT, _size: int) -> ctypes.c_void_p:
        return mapGetPathShellUn_t (_path.buffer(), _size)


# Установить новое имя INI-файла приложения
# inipath - полнй путь к ini-файлу приложения, в котором будут запоминаться параметры сеанса работы

    mapSetIniPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetIniPathUn', maptype.PWCHAR)
    def mapSetIniPathUn(_inipath: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapSetIniPathUn_t (_inipath.buffer())


# Запросить имя INI-файла приложения
# При ошибке возвращает ноль

    mapGetIniPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetIniPathUn')
    def mapGetIniPathUn() -> ctypes.POINTER(maptype.WCHAR):
        return mapGetIniPathUn_t ()


# Запросить путь к общей папке файлов параметров задач приложения (INI, XML)
# Пример возращаемой строки: "c:\Users\Public\Documents\Panorama\",  "/var/Panorama/"
# При ошибке возвращает "" (пустую строку)

    mapGetCommonIniPath_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetCommonIniPath')
    def mapGetCommonIniPath() -> ctypes.POINTER(maptype.WCHAR):
        return mapGetCommonIniPath_t ()


# Установить путь к общей папке файлов параметров задач системы (INI, XML)
# При ошибке возвращает ноль

    mapSetCommonIniPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSetCommonIniPath', maptype.PWCHAR)
    def mapSetCommonIniPath(_path: mapsyst.WTEXT) -> int:
        return mapSetCommonIniPath_t (_path.buffer())


# Запросить путь к общей папке файлов параметров задач приложения с учетом версии (INI, XML)
# path - адрес буфера для записи пути
# size - размер буфера в байтах
# Добавляет к пути mapGetCommonIniPath имя папки приложения mapGetAppFolderName и старшие цифры номера версии
# Пример возращаемой строки: "c:\Users\Public\Documents\Panorama\Panorama15\",  "/var/Panorama/Panorama15/"
# При ошибке возвращает ноль

    mapGetApplicationCommonIniPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetApplicationCommonIniPath', maptype.PWCHAR, ctypes.c_long)
    def mapGetApplicationCommonIniPath(_path: mapsyst.WTEXT, _size: int) -> int:
        return mapGetApplicationCommonIniPath_t (_path.buffer(), _size)


# Запросить путь к пользовательской папке файлов параметров задач приложения (INI, XML)
# path - адрес буфера для записи пути
# size - размер буфера в байтах
# Пример возращаемой строки: "c:\Users\<User>\Application Data\Roaming\Panorama15\",  "/home/user/.panorama/"
# <User> - имя пользователя в системе
# При ошибке возвращает ноль

    mapGetUserIniPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetUserIniPath', maptype.PWCHAR, ctypes.c_long)
    def mapGetUserIniPath(_path: mapsyst.WTEXT, _size: int) -> int:
        return mapGetUserIniPath_t (_path.buffer(), _size)


# Запросить полный путь к файлу соединений с БД
# Пример возращаемой строки: "c:\Users\User\Application Data\Panorama15\dbmlist.xml",  "/home/user/.panorama15/dbmlist.xml"
# При ошибке возвращает "" (пустую строку)

    mapGetDBConnectionListFileName_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetDBConnectionListFileName')
    def mapGetDBConnectionListFileName() -> ctypes.POINTER(maptype.WCHAR):
        return mapGetDBConnectionListFileName_t ()


# Установить полный путь до файла соединений с БД
# path - полный путь к файлу
# При ошибке возвращает ноль

    mapSetDBConnectionListFileName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetDBConnectionListFileName', maptype.PWCHAR)
    def mapSetDBConnectionListFileName(_path: mapsyst.WTEXT) -> int:
        return mapSetDBConnectionListFileName_t (_path.buffer())


# Запросить имя INI-файла документа
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает пустую строку

    mapGetMapIniNameEx_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetMapIniNameEx', maptype.HMAP)
    def mapGetMapIniNameEx(_hmap: maptype.HMAP) -> ctypes.POINTER(maptype.WCHAR):
        return mapGetMapIniNameEx_t (_hmap)


# Запросить имя INI-файла документа
# hmap - идентификатор открытых данных (документа)
# name - адрес строки для размещения результата
# size - размер строки в байтах
# При ошибке возвращает 0

    mapGetMapIniNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapIniNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapIniNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapIniNameUn_t (_hmap, _name.buffer(), _size)


# Установить путь к общим файлам классификаторам (RSC)
# rscpath - путь к общим файлам классификаторам (RSC)
# При ошибке возвращает ноль

    mapSetCommonRscPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCommonRscPathUn', maptype.PWCHAR)
    def mapSetCommonRscPathUn(_rscpath: mapsyst.WTEXT) -> int:
        return mapSetCommonRscPathUn_t (_rscpath.buffer())


# Запросить путь к общим файлам классификаторам (RSC)
# При ошибке возвращает пустую строку

    mapGetCommonRscPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetCommonRscPathUn')
    def mapGetCommonRscPathUn() -> ctypes.POINTER(maptype.WCHAR):
        return mapGetCommonRscPathUn_t ()


# Установить имя хоста для согласования общей папки классификаторов на ГИС Сервере
# rschost - имя хоста или IP-адрес

    mapSetCommonRscHost_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapSetCommonRscHost', ctypes.c_char_p)
    def mapSetCommonRscHost(_rschost: ctypes.c_char_p) -> ctypes.POINTER(ctypes.c_char):
        return mapSetCommonRscHost_t (_rschost)


# Запросить имя хоста для согласования общей папки классификаторов на ГИС Сервере

    mapGetCommonRscHost_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetCommonRscHost')
    def mapGetCommonRscHost() -> ctypes.POINTER(ctypes.c_char):
        return mapGetCommonRscHost_t ()


# Проверить, что имя файла не является алиасом сервера или геопортала
# При отсутствии спецсимволов возвращает ненулевое значение

    mapIsNormalPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsNormalPathUn', maptype.PWCHAR)
    def mapIsNormalPathUn(_name: mapsyst.WTEXT) -> int:
        return mapIsNormalPathUn_t (_name.buffer())


# Преобразовать имя алиаса или соединения с сервисом в имя файла (без пути)
# alias - имя алиаса или соединения с сервисом (WMS, WFS, WCS)
# name - адрес строки для размещения результата
# size - размер выделенной памяти в строке в байтах
# Длина имени c расширением усекается до 204 символов
# При ошибке возвращает ноль

    mapAliasToNormalNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAliasToNormalNameUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapAliasToNormalNameUn(_alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapAliasToNormalNameUn_t (_alias.buffer(), _name.buffer(), _size)


# Построить "короткое" имя файла
# templ - эталонный путь, относительно которого строится короткий путь
#         например, путь к библиотекам приложения - mapGetPathShellUn()
# name - исходное полное имя файла
# Возвращает указатель на "короткое" имя файла
# При ошибке возвращает ноль

    mapBuildShortNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapBuildShortNameUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapBuildShortNameUn(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        return mapBuildShortNameUn_t (_templ.buffer(), _name.buffer())


# Построить "короткое" имя файла
# name - полное имя файла
# В качестве эталонного пути применяется путь к библиотекам приложения - mapGetPathShellUn()
# Возвращает указатель на "короткое" имя файла
# При ошибке возвращает ноль

    mapBuildShellShortNameUnicode_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapBuildShellShortNameUnicode', maptype.PWCHAR)
    def mapBuildShellShortNameUnicode(_name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        return mapBuildShellShortNameUnicode_t (_name.buffer())


# Построить "длинное" имя файла (полный путь к файлу)
# templ - эталонный путь, относительно которого строится полный путь,
#         например, путь к библиотекам приложения - mapGetPathShellUn()
# name - исходный короткий путь к файлу; например, имя_папки/имя_файла или ../имя_папки/имя_файла и тому подобное
# path - указатель на буфер для размещения полного пути к файлу
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapBuildLongNameEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildLongNameEx', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapBuildLongNameEx(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildLongNameEx_t (_templ.buffer(), _name.buffer(), _path.buffer(), _size)


# Подсчитать контрольную сумму файла по алгоритму CRC32
# filename - полный путь к файлу
# value32 - поле для записи результата подсчета
# При ошибке возвращает ноль

    mapGetFileCrc32_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetFileCrc32', maptype.PWCHAR, ctypes.POINTER(ctypes.c_uint))
    def mapGetFileCrc32(_filename: mapsyst.WTEXT, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        return mapGetFileCrc32_t (_filename.buffer(), _value32)


# Подсчитать контрольную сумму записи по алгоритму CRC32
# buffer - адрес записи
# size - длина записи в байтах
# value32 - текущее значение контрольной суммы и новый результат с учетом переданного буфера
# При первом обращении поле value32 нужно обнулить
# При ошибке возвращает ноль

    mapGetRecordCrc32_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetRecordCrc32', ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint))
    def mapGetRecordCrc32(_buffer: ctypes.c_char_p, _size: int, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        return mapGetRecordCrc32_t (_buffer, _size, _value32)


# Сохранить в архиве список файлов
# zipname - имя zip-архива
# filelist - массив указателей на пути к файлам
# count - число сохраняемых файлов (элементов массива указателей)
# flag - управляющие флажки: 1 - записывать относительные пути в архив или 0
# error - поле для записи ошибки выполнения программы
# Если файл один или все файлы в одной папке, то они сохраняются без пути
# Если файлы размещены в поддиректориях одной папки, то они сохраняются с относительными путями
# Если файлы не имеют общего пути, то они сохраняются без пути
# При ошибке возвращает ноль

    mapSaveFilesToZip_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveFilesToZip', maptype.PWCHAR, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSaveFilesToZip(_zipname: mapsyst.WTEXT, _filelist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _count: int, _flag: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapSaveFilesToZip_t (_zipname.buffer(), _filelist, _count, _flag, _error)


# Распаковать файл из ZIP-архива в памяти
# source - адрес упакованного ZIP-архива в памяти
# sourcesize - размер упакованного архива в байтах
# zipfile - номер распаковываемого файла в Zip-архиве с 1
# error - поле для записи ошибки распаковки
# Возвращает идентификатор распакованного файла в памяти
# Для чтения данных необходимо вызвать mapGetUnzipFilePoint и mapFreeUnzipFile
# При ошибке возвращает ноль

    mapUnzipFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUnzipFile', ctypes.c_char_p, ctypes.c_ulong, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapUnzipFile(_source: ctypes.c_char_p, _sourcesize: int, _zipfile: int, _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_void_p:
        return mapUnzipFile_t (_source, _sourcesize, _zipfile, _error)


# Чтение распакованного файла из ZIP-архива после распаковки mapUnzipFile
# hunzipfile - идентификатор распакованного файла в памяти
# size - поле, в которое запишется длина файла в памяти
# Возвращает указатель на начало записи файла в памяти
# При ошибке возвращает ноль

    mapGetUnzipFilePoint_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetUnzipFilePoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetUnzipFilePoint(_hunzipfile: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetUnzipFilePoint_t (_hunzipfile, _size)


# Освободить ресурсы распакованного файла в mapUnzipFile
# hunzipfile - идентификатор распакованного файла в памяти

    mapFreeUnzipFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeUnzipFile', ctypes.c_void_p)
    def mapFreeUnzipFile(_hunzipfile: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeUnzipFile_t (_hunzipfile)


# Запретить выдачу сообщений на экран (серверный режим работы)
# enable - флаг разрешения (1) или запрета (0) выдачи сообщений
# При выполнении автоматических процедур без диалогов с оператором
# выдача сообщений должна быть запрещена
# Возвращает предыдущее значение флага

    mapMessageEnable_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapMessageEnable', ctypes.c_long)
    def mapMessageEnable(_enable: int) -> int:
        return mapMessageEnable_t (_enable)


# Запросить, разрешена ли выдача сообщений

    mapIsMessageEnable_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMessageEnable')
    def mapIsMessageEnable() -> int:
        return mapIsMessageEnable_t ()


# enable - флаг разрешения (1) или запрета (0) выдачи сообщений
# При выполнении автоматических процедур без диалогов с оператором
# выдача сообщений должна быть запрещена

    mapMessageEnableForThread_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapMessageEnableForThread', ctypes.c_long)
    def mapMessageEnableForThread(_enable: int) -> ctypes.c_void_p:
        return mapMessageEnableForThread_t (_enable)


# Запросить признак разрешения выдачи сообщений на экран для текущего потока

    mapIsMessageEnableForThread_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMessageEnableForThread')
    def mapIsMessageEnableForThread() -> int:
        return mapIsMessageEnableForThread_t ()


# Выдать сообщение об ошибке (на экран)
# hwnd - идентификатор родительского окна для выдачи сообщения или 0
# code - код ошибки (maperr.rh)
# filename - имя файла (объекта), для которого возникла ошибка
# message - адрес буфера для размещения текста сообщения (для записи в протокол и т.п.), область памяти должна быть
#            не менее длины имени файла + 256 байт; значение может быть 0
# size - длина буфера в байтах
# isshow   - признак вывода сообщения на экран

    mapErrorMessageLog_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapErrorMessageLog', maptype.HWND, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapErrorMessageLog(_hwnd: maptype.HWND, _code: int, _filename: mapsyst.WTEXT, _message: mapsyst.WTEXT, _size: int, _isshow: int) -> ctypes.c_void_p:
        return mapErrorMessageLog_t (_hwnd, _code, _filename.buffer(), _message.buffer(), _size, _isshow)


# Выдать сообщение об ошибке (на экран)
# code - код ошибки (maperr.rh)
# filename - имя файла (объекта), для которого возникла ошибка

    mapErrorMessageUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapErrorMessageUn', ctypes.c_long, maptype.PWCHAR)
    def mapErrorMessageUn(_code: int, _filename: mapsyst.WTEXT) -> ctypes.c_void_p:
        if (isinstance(_filename, str)):
            return mapErrorMessageUn_t (_code, (_filename + '\0').encode('utf-16LE'))
        return mapErrorMessageUn_t (_code, _filename.buffer())


# Расчёт времени выполнения процесса в виде строки "HH:MM:SS / HH:MM:SS",
# begtime - временя старта программы,
# total   - общее число обрабатываемых элементов (например, 100 - в процентах),
# current - число обработанных элементов (например, выполненный процент работы программы)
# message - буфер для записи строки
# size - размер буфера в байтах (не менее 64 байт)
# В строке указано прошедшее время и оставшееся до завершения процесса обработки
# При ошибке в параметрах возвращает ноль

    mapSetTimeStringExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetTimeStringExUn', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_long)
    def mapSetTimeStringExUn(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: float, _current: float, _message: mapsyst.WTEXT, _size: int) -> int:
        return mapSetTimeStringExUn_t (_begtime, _total, _current, _message.buffer(), _size)


# Записать сообщение в протокол карты по коду ошибки
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# code - код ошибки (из maperr.rh) или 0
# message - текст сообщения
# type - тип сообщения: MT_INFO, MT_ERROR, MT_WARNING

    mapMessageToLogEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapMessageToLogEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMessageToLogEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapMessageToLogEx_t (_hmap, _hsite, _code, _message.buffer(), _type)


# Записать сообщение в протокол карты
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в документе, для фоновой карты равен hmap
# message - текст сообщения
# messageex - продолжение сообщения или 0
# type - тип сообщения: MT_INFO, MT_ERROR, MT_WARNING

    mapMessageToLogPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapMessageToLogPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapMessageToLogPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapMessageToLogPro_t (_hmap, _hsite, _message.buffer(), _messageex.buffer(), _type)


# Открыть линейку progressbar в главном окне приложения
# Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически)
# Для создания линейки необходимо вызвать mapOpenProgressBar, для смены процента вызывается mapProgressBar,
# для скрытия линейки - mapCloseProgressBar
# В один момент времени в главной панели может быть только одна линейка
# При ошибке возвращает ноль, при успешном выполнении возвращает идентификатор линейки

    mapOpenProgressBar_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapOpenProgressBar')
    def mapOpenProgressBar() -> ctypes.c_void_p:
        return mapOpenProgressBar_t ()


# Отобразить линейку progressbar в главном окне приложения
# progressbar - идентификатор линейки, полученной в mapOpenProgressBar
# percent - процент заполнения линейки от 0 до 100
# message - комментарий к выполняемой операции, отображается на линейке после процентов
# Если оператор желает прервать процесс, функция вернет значение -1
# При ошибке возвращает ноль, при успешном выполнении возвращает 1

    mapProgressBar_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapProgressBar', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR)
    def mapProgressBar(_progressbar: ctypes.c_void_p, _percent: int, _message: mapsyst.WTEXT) -> int:
        return mapProgressBar_t (_progressbar, _percent, _message.buffer())


# Закрыть линейку progressbar в главном окне приложения
# progressbar - идентификатор линейки, полученной в mapOpenProgressBar

    mapCloseProgressBar_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseProgressBar', ctypes.c_void_p)
    def mapCloseProgressBar(_progressbar: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapCloseProgressBar_t (_progressbar)


# Показать всплывающее информационное сообщение
# text - текст сообщения
# caption - заголовок сообщения
# Посылает главному окну приложения сообщение AW_MESSAGEBOX через mapSendMessage
# Сообщение гаснет через 3 секунды или после нажатия клавиатуры\мышки

    mapShowMessage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapShowMessage', maptype.PWCHAR, maptype.PWCHAR)
    def mapShowMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapShowMessage_t (_text.buffer(), _caption.buffer())


# Показать всплывающее сообщение об ошибке
# text - текст сообщения
# caption - заголовок сообщения
# Посылает главному окну приложения сообщение AW_ERRORBOX через mapSendMessage
# Сообщение гаснет через 3 секунды или после нажатия клавиатуры\мышки

    mapShowErrorMessage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapShowErrorMessage', maptype.PWCHAR, maptype.PWCHAR)
    def mapShowErrorMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> ctypes.c_void_p:
        return mapShowErrorMessage_t (_text.buffer(), _caption.buffer())


# Преобразовать дату из строки в число ГГГГММДД
# date - исходная строка с датой
# Строка может иметь вид ДД/ММ/ГГГГ или ДД.ММ.ГГГГ
# или ГГГГММДД или ГГГГ/ММ/ДД или ГГГГ-ММ-ДД
# При ошибке возвращает ноль, иначе - значение даты в виде числа

    mapDateToLongUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDateToLongUn', maptype.PWCHAR)
    def mapDateToLongUn(_date: mapsyst.WTEXT) -> int:
        return mapDateToLongUn_t (_date.buffer())


# Преобразовать дату из из числа ГГГГММДД в строку ДД/ММ/ГГГГ
# number - числовое значение даты
# date - адрес буфера для записи строки с датой
# size - размер буфера в байтах
# При ошибке возвращает ноль, иначе - адрес входной строки

    mapLongToDateUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapLongToDateUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToDateUn(_number: int, _date: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        return mapLongToDateUn_t (_number, _date.buffer(), _size)


# Преобразовать время из строки в число ЧЧММСС
# time - исходная строка со временем
# Строка может иметь вид ЧЧ:ММ:СС
# При ошибке возвращает ноль, иначе - значение времени в виде числа

    mapTimeToLongUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTimeToLongUn', maptype.PWCHAR)
    def mapTimeToLongUn(_time: mapsyst.WTEXT) -> int:
        return mapTimeToLongUn_t (_time.buffer())


# Преобразовать время из числа ЧЧММСС в строку с системным и локальным временем
# number - числовое значение времени
# time - адрес буфера для записи результата
# size - размер буфера в байтах
# Строка будет иметь вид ЧЧ:ММ:СС (ЧЧ:ММ:СС) - значение в скобках содержит локальное время
# При ошибке возвращает ноль, иначе - адрес входной строки

    mapLongToDoubleTime_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapLongToDoubleTime', ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapLongToDoubleTime(_number: int, _time: ctypes.c_char_p, _size: int) -> ctypes.POINTER(ctypes.c_char):
        return mapLongToDoubleTime_t (_number, _time, _size)


# Преобразовать время из числа ЧЧММСС в строку ЧЧ:ММ:СС
# number - числовое значение времени
# time - адрес буфера для записи результата
# size - размер буфера в байтах
# При ошибке возвращает ноль, иначе - адрес входной строки

    mapLongToTimeUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapLongToTimeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToTimeUn(_number: int, _time: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        return mapLongToTimeUn_t (_number, _time.buffer(), _size)


# Преобразовать угловую величину в градусах из строки в числовое значение в радианах
# angle - исходная строка с угловой величиной
# Строка может иметь вид ГГГ°ММ'CC.CC" или ГГГ.ГГГГГГГГ°
# Для Linux вместо символа ° (\xB0) д.б. ^
# При ошибке возвращает ноль, иначе - значение в радианах

    mapAngleToRadianUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapAngleToRadianUn', maptype.PWCHAR)
    def mapAngleToRadianUn(_angle: mapsyst.WTEXT) -> float:
        return mapAngleToRadianUn_t (_angle.buffer())


# Преобразовать числовое значение из радиан в строку вида ГГГ°ММ'CC.CC"
# radian - исходное значение в радианах
# angle - адрес буфера для записи результата
# size - размер буфера в байтах
# Для Linux вместо символа ° (\xB0) д.б. ^
# При ошибке возвращает ноль, иначе - адрес входной строки

    mapRadianToAngleUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapRadianToAngleUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_int)
    def mapRadianToAngleUn(_radian: float, _angle: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        return mapRadianToAngleUn_t (_radian, _angle.buffer(), _size)


# Сконвертировать значение строки, убрав спецсимволы XML ('\"', '?', '>', '<', '&', '\'' '\n')
# instring - входная строка
# outstring - выходная строка (&quot; и т.д.)
# outsize - размер выходной строки в байтах
# При ошибке возвращает ноль

    ConvertStringToXmlStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ConvertStringToXmlStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertStringToXmlStringUn(_instring: mapsyst.WTEXT, _outval: mapsyst.WTEXT, _outsize: int) -> int:
        return ConvertStringToXmlStringUn_t (_instring.buffer(), _outval.buffer(), _outsize)


# Сконвертировать значение строки, заменив спецсимволы JSON ('\"', '\n', '\r', '\v', '\\', '\t')
# inval  - обрабатываемая строка в кодировке UTF16, заканчивающаяся символом конца строки
# Заменяет '\"' на '\'', а остальные спецсимволы на пробелы

    ConvertStringToJsonStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'ConvertStringToJsonStringUn', maptype.PWCHAR)
    def ConvertStringToJsonStringUn(_inval: mapsyst.WTEXT) -> ctypes.c_void_p:
        return ConvertStringToJsonStringUn_t (_inval.buffer())


# Экранировать спецсимволы строки JSON ('\"', '\n', '\r', '\v', '\\', '\t')
# instring - обрабатываемая строка в кодировке UTF16, заканчивающаяся символом конца строки
# outstring - выходная строка
# outsize - размер выходной строки в байтах

    ShieldStringToJsonStringUnEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'ShieldStringToJsonStringUnEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ShieldStringToJsonStringUnEx(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> ctypes.c_void_p:
        return ShieldStringToJsonStringUnEx_t (_instring.buffer(), _outstring.buffer(), _outsize)


# Убрать экранирующие слеши
# instring  - обрабатываемая строка
# outstring - выходная строка
# outsize - размер выходной строки в байтах
# Возвращает количество убранных символов

    ConvertJsonStringToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'ConvertJsonStringToStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertJsonStringToStringUn(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> ctypes.c_void_p:
        return ConvertJsonStringToStringUn_t (_instring.buffer(), _outstring.buffer(), _outsize)


# Сконвертировать значение строки, восстановив спецсимволы XML
# instring - входная строка
# outtext - выходная строка
# outsize - размер выходной строки в байтах
# При ошибке возвращает 0

    ConvertFromXmlToStringUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'ConvertFromXmlToStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertFromXmlToStringUn(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> int:
        return ConvertFromXmlToStringUn_t (_instring.buffer(), _outstring.buffer(), _outsize)


# Закодировать данные в base64
# srcdata - указатель на буфер с исходными данными для кодирования
# srclength - размер исходных данных в байтах
# result - указатель на выходной буфер в кодировке base64
# resultlength - размер выделенной памяти в выходном буфере в байтах
# Возвращает длину выходного буфера вместе с замыкающим нулем
# Если буфер не задан или его длина меньше требуемой, то вернется требуемая длина выходного буфера
# При ошибке возвращает ноль

    mapBase64Encode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBase64Encode', ctypes.POINTER(ctypes.c_void_p), ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapBase64Encode(_srcdata: ctypes.POINTER(ctypes.c_void_p), _srclength: int, _result: ctypes.c_char_p, _resultlength: int) -> int:
        return mapBase64Encode_t (_srcdata, _srclength, _result, _resultlength)


# Раскодировать данные из base64
# srcdata - указатель на буфер с исходными данными для раскодирования
# srclength - размер исходных данных в байтах
# result - указатель на выходной буфер в кодировке base64
# resultSize - размер выделенной памяти в выходном буфере в байтах
# Возвращает длину выходного буфера вместе с замыкающим нулем
# Если буфер не задан или его длина меньше требуемой, то вернется требуемая длина выходного буфера
# При ошибке возвращает ноль

    mapBase64Decode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBase64Decode', ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapBase64Decode(_srcdata: ctypes.c_char_p, _srclength: int, _result: ctypes.POINTER(ctypes.c_byte), _resultlength: int) -> int:
        return mapBase64Decode_t (_srcdata, _srclength, _result, _resultlength)


# Установить до начала работы с python путь к папке с библиотеками Python
# pythondirectory - путь к каталогу, который содержит библиотеку Python и установленные пакеты расширений
# Если эта функция не была вызвана, то интерпретатор запускается из директории, заданой в ОС по умолчанию
# При ошибке возвращает ноль

    mapSetPythonLibraryPath_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPythonLibraryPath', maptype.PWCHAR)
    def mapSetPythonLibraryPath(_pythondirectory: mapsyst.WTEXT) -> int:
        return mapSetPythonLibraryPath_t (_pythondirectory.buffer())


# Установить до начала работы с python путь к исполняемому файлу интерпретатора Python
# pythoninterpreter - полный путь к исполняемому файлу интерпретатора Python
# Если функции mapSetPythonInterpreter или не были mapSetPythonLibraryPath вызваны,
# то интерпретатор запускается из директории, заданой в ОС по умолчанию
# Для выбора другого интерпретатора Python необходимо завершить приложение
# Функция является альтернативной для функции mapSetPythonLibraryPath
# При ошибке возвращает ноль

    mapSetPythonInterpreter_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetPythonInterpreter', maptype.PWCHAR)
    def mapSetPythonInterpreter(_pythoninterpreter: mapsyst.WTEXT) -> int:
        return mapSetPythonInterpreter_t (_pythoninterpreter.buffer())


# Выполнить на python скрипт из строкового буфера
# buffer   - адрес строки со скриптом
# function - имя выполняемой функции на python вида def Function(args) -> float:
# args     - идентификатор объекта, передаваемого в функцию в качестве аргумента
# error    - возвращаемый код ошибки выполнения скрипта
# value    - адрес переменной для записи результата
# При ошибке возвращает ноль

    mapRunPythonFromBuf_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRunPythonFromBuf', ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapRunPythonFromBuf(_buffer: ctypes.c_char_p, _function: ctypes.c_char_p, _args: ctypes.POINTER(ctypes.c_void_p), _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapRunPythonFromBuf_t (_buffer, _function, _args, _error, _value)


# Выполнить скрипт на python и вернуть результат вычислений
# hmap - идентификатор открытого документа
# hobj - идентификатор выбранного объекта или ноль
# path - полный путь к файлу py, содержащему код скрипта на python
# function - имя выполняемой функции на python вида def Function(hmap:HMAP, hobj:HOBJ) -> float:
# error - возвращаемый код ошибки выполнения скрипта
# При ошибке возвращает ноль

    mapCallPython_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallPython', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapCallPython(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapCallPython_t (_hmap, _hobj, _path.buffer(), _function.buffer(), _error, _value)


# Выполнить скрипт на python из прикладной задачи и вернуть результат вычислений
# hident - идентификатор объекта прикладной задачи или ноль
# parm - указатель на параметры скрипта или ноль
# path - полный путь к файлу py, содержащему код скрипта на python
# function - имя выполняемой функции на python вида def Function(hmap:HMAP, hobj:HOBJ) -> float:
# error - возвращаемый код ошибки выполнения скрипта
# При ошибке возвращает ноль

    mapCallTaskPython_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallTaskPython', ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapCallTaskPython(_hident: ctypes.POINTER(ctypes.c_void_p), _parm: ctypes.POINTER(ctypes.c_void_p), _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        return mapCallTaskPython_t (_hident, _parm, _path.buffer(), _function.buffer(), _error, _value)


# Получить строку версии активного интерпретатора Python
# versionString - адрес строки для записи версии
# size - размер строки в байтах
# При ошибке возвращает ноль

    mapGetPythonVersion_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPythonVersion', maptype.PWCHAR, ctypes.c_int)
    def mapGetPythonVersion(_versionString: mapsyst.WTEXT, _size: int) -> int:
        return mapGetPythonVersion_t (_versionString.buffer(), _size)


# Закрыть текущую сессию интерпретатора Python
# Применяется при необходимости отредактировать скрипты, которые запускались в сеансе работы

    mapClosePython_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClosePython')
    def mapClosePython() -> ctypes.c_void_p:
        return mapClosePython_t ()


# Выполнить скрипт из указанного файла с заданным именем функции и параметром HMAP в режиме отладки
# hmap - идентификатор открытого документа
# hobj - идентификатор выбранного объекта или ноль
# path - полный путь к файлу py, содержащему код скрипта на python
# function - имя выполняемой функции на python вида def Function(hmap:HMAP, hobj:HOBJ) -> float:
# error - возвращаемый код ошибки выполнения скрипта
# Вызывает команду: pythonw.exe idle.pyw debug_имя_скрипта.py
# При ошибке возвращает ноль

    mapDebugPython_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDebugPython', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapDebugPython(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapDebugPython_t (_hmap, _hobj, _path.buffer(), _function.buffer(), _error)


# Найти путь к программе запуска скрипта pythonw.exe
# pathexe - возвращаемый полный путь к pythonw.exe
# size - размер строки pathexe в байтах
# error - возвращаемый код ошибки выполнения скрипта
# При ошибке возвращает ноль

    mapFindPathExePython_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapFindPathExePython', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapFindPathExePython(_pathexe: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapFindPathExePython_t (_pathexe.buffer(), _size, _error)


# Запросить число подключений к ГИС Серверам
# При отсутствии подключений возвращает ноль

    mapActiveServerCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapActiveServerCount')
    def mapActiveServerCount() -> int:
        return mapActiveServerCount_t ()


# Сформировать алиас данных на Сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - имя ресурса (условное имя карты)
# name - имя строки для размещения результата
# size - размер строки в байтах
# Алиас создается в формате "HOST#ХОСТ#ПОРТ#ALIAS#условное_имя_карты"
# При ошибке в параметрах возвращает ноль

    mapBuildAliasNameEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapBuildAliasNameEx', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapBuildAliasNameEx(_number: int, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapBuildAliasNameEx_t (_number, _alias.buffer(), _name.buffer(), _size)


# Запросить является ли имя идентификатором данных на Сервере
# name - строка с именем файла
# Если да, то возвращает ненулевое значение (1 - устаревший
# формат без имени сервера, 2 - содержит имя сервера)
# Если имя не указывает на данные с сервера, то возвращает ноль

    mapIsAliasNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsAliasNameUn', maptype.PWCHAR)
    def mapIsAliasNameUn(_name: mapsyst.WTEXT) -> int:
        return mapIsAliasNameUn_t (_name.buffer())


# Запросить имя алиаса данных из полной строки имени, включающей имя хоста
# name - строка с именем файла на ГИС Сервере
# Возвращает указатель на имя алиаса (первый символ после ALIAS#) или 0

    mapGetDataNameFromAliasUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetDataNameFromAliasUn', maptype.PWCHAR)
    def mapGetDataNameFromAliasUn(_name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        return mapGetDataNameFromAliasUn_t (_name.buffer())


# Запросить состояние подключения к серверу
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При потоковом открытии\добавлении данных с ГИС Сервера рекомендуется
# после первой ошибки открытия данных проверить состояние подключения
# и при ошибке прервать потоковую обработку
# Если после ошибки открытия данных с именем "HOST#..." или "ALIAS#..."
# подключение не установлено, то нужно убедится, что Сервер запущен и
# введены правильные параметры соединения
# Если подключение к серверу установлено - возвращает ненулевое значение

    mapIsServerActiveEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsServerActiveEx', ctypes.c_long)
    def mapIsServerActiveEx(_number: int) -> int:
        return mapIsServerActiveEx_t (_number)


# Запросить доступ к средствам мониторинга состояния сервера
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если мониторинг запрещен - возвращает нулевое значение

    mapIsServerMonitoringEnable_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsServerMonitoringEnable', ctypes.c_long)
    def mapIsServerMonitoringEnable(_number: int) -> int:
        return mapIsServerMonitoringEnable_t (_number)


# Запросить доступ к средствам администрирования состояния сервера
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если администрирование запрещено - возвращает нулевое значение

    mapIsServerAdministrationEnable_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsServerAdministrationEnable', ctypes.c_long)
    def mapIsServerAdministrationEnable(_number: int) -> int:
        return mapIsServerAdministrationEnable_t (_number)


# Запросить версию ГИС Сервера по номеру подключения
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Возвращает шестнадцатеричный номер версии ГИС Сервер,
# например: 0x00040503 соответствует версии 4.5.3
# При ошибке возвращает ноль

    mapGetServerVersion_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetServerVersion', ctypes.c_long)
    def mapGetServerVersion(_number: int) -> int:
        return mapGetServerVersion_t (_number)


# Считать информацию о состоянии открытых подключений (мониторинг)
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# versin - буфер для размещения строки с именем и версией ГИС Сервера
# size - размер буфера (не менее 80 байт)
# state - состояние ГИС Сервера, полученное в предыдущем запросе,
#         если состояние не изменилось, то возвращается сокращенный отчет
# После завершения обработки данных необходимо освободить ресурсы путем
# вызова mapFreeServerState с указателем, полученным в mapGetServerState
# При ошибке возвращает ноль

    mapGetServerState_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.GSMONITOR),'mapGetServerState', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetServerState(_number: int, _version: mapsyst.WTEXT, _size: int, _state: int) -> ctypes.POINTER(maptype.GSMONITOR):
        return mapGetServerState_t (_number, _version.buffer(), _size, _state)


# Освободить ресурсы после обработки данных мониторинга состояния сервера
# buffer - информация о состоянии, полученная в функции mapGetServerState

    mapFreeServerState_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeServerState', ctypes.POINTER(maptype.GSMONITOR))
    def mapFreeServerState(_buffer: ctypes.POINTER(maptype.GSMONITOR)) -> ctypes.c_void_p:
        return mapFreeServerState_t (_buffer)


# Прочитать журнал на сервере (если есть права администратора)
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# size - поле для записи размера считанного журнала
# error - поле для записи кода ощибки, если функция вернет ноль
# Содержимое журнала не должно сохраняться на диск в целях безопасности
# Возвращает указатель на буфер с журналом в кодировке UTF-8
# Если размер журнала больше 2 Мб, то считывает последние 2 Мб
# После чтения записи необходимо освободить память функцией mapFreeServerLog
# При ошибке возвращает ноль

    mapReadLogOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_char_p,'mapReadLogOnServer', ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapReadLogOnServer(_number: int, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_char_p:
        return mapReadLogOnServer_t (_number, _size, _error)


# Освободить ресурсы после обработки данных журнала
# buffer - адрес записи журнала в памяти, созданный функцией mapReadLogOnServer

    mapFreeServerLog_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeServerLog', ctypes.c_char_p)
    def mapFreeServerLog(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeServerLog_t (_buffer)


# Запросить, выполнено ли подключение и регистрация пользователя для алиаса
# name - алиас в формате "HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты",
#        или "HOST#ХОСТ" или "HOST#ХОСТ:ПОРТ"
# При успешной проверке возвращает номер подключения
# При ошибке возвращает ноль

    mapCheckConnectForAliasUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckConnectForAliasUn', maptype.PWCHAR)
    def mapCheckConnectForAliasUn(_name: mapsyst.WTEXT) -> int:
        return mapCheckConnectForAliasUn_t (_name.buffer())


# Запросить, выполнено ли подключение и регистрация пользователя для алиаса и порта
# name - алиас в формате "HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты",
#        или "HOST#ХОСТ" или "HOST#ХОСТ:ПОРТ"
# port - номер порта для проверки или 0 (любой)
# На одном сервере могут быть несколько экземпляров ГИС Сервера с разными портами
# При успешной проверке возвращает номер подключения
# При ошибке возвращает ноль

    mapCheckConnectForAliasEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckConnectForAliasEx', ctypes.c_char_p, ctypes.c_long)
    def mapCheckConnectForAliasEx(_name: ctypes.c_char_p, _port: int) -> int:
        return mapCheckConnectForAliasEx_t (_name, _port)


# Открыть новое подключение к ГИС-серверу
# name - имя хоста (до 256 символов) или адрес "XXX.XXX.XXX.XXX"
#        Если параметр равен нулю - сервер ищется на локальном хосте "localhost"
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# В случае удачно выполненного подключения возвращает его порядковый номер
# При ошибке возвращает ноль

    mapOpenConnectUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOpenConnectUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenConnectUn(_name: mapsyst.WTEXT, _port: int) -> int:
        return mapOpenConnectUn_t (_name.buffer(), _port)


# Открыть новое подключение к ГИС-серверу
# name - имя хоста (до 256 символов) или адрес "XXX.XXX.XXX.XXX"
#        Если параметр равен нулю - сервер ищется на локальном хосте "localhost".
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# cansleep - разрешение на открытие виртуального (спящего) соединения,
#        при отсутствии физического доступа к серверу
# Данные будут открываться из кэш, если он есть
# При появлении физического соединения оно автоматически (по мере вызова mapAdjustData)
# будет восстановлено вместо вирутального (кэш обновится по данным с сервера)
# В случае удачно выполненного подключения возвращает его порядковый номер
# При ошибке возвращает ноль

    mapOpenConnectExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOpenConnectExUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapOpenConnectExUn(_name: mapsyst.WTEXT, _port: int, _cansleep: int) -> int:
        return mapOpenConnectExUn_t (_name.buffer(), _port, _cansleep)


# Запросить, можно ли закрыть подключение
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При ошибке (подключение не найдено) возвращает ноль
# При занятости подключения возвращает "-1"
# Если соединение может быть закрыто, то возвращает положительное значение

    mapCanCloseConnect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCanCloseConnect', ctypes.c_long)
    def mapCanCloseConnect(_number: int) -> int:
        return mapCanCloseConnect_t (_number)


# Закрыть подключение к ГИС-серверу
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При ошибке (подключение не найдено) возвращает ноль
# При занятости подключения возвращает "-1"
# При успешном выполнении возвращает положительное значение
# Если счетчик ссылок на соединения равен 0 и все соединения закрыты возвращает 2

    mapCloseConnect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCloseConnect', ctypes.c_long)
    def mapCloseConnect(_number: int) -> int:
        return mapCloseConnect_t (_number)


# Изменить параметры подключения с ГИС-сервером
# Вызывается до открытия карт на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# name - имя хоста (до 256 символов) или адрес "XXX.XXX.XXX.XXX"
#        Если параметр равен нулю - сервер ищется на локальном хосте "localhost".
# port - номер порта от 1024 до 65536, по умолчанию - 2047 (если port = 0)
# При ошибке возвращает ноль

    mapSetConnectParametersExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetConnectParametersExUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSetConnectParametersExUn(_number: int, _name: mapsyst.WTEXT, _port: int) -> int:
        return mapSetConnectParametersExUn_t (_number, _name.buffer(), _port)


# Запросить номер порта для связи с ГИС-сервером
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Номер порта от 1024 до 65536, по умолчанию - 2047
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()

    mapGetConnectPortEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetConnectPortEx', ctypes.c_long)
    def mapGetConnectPortEx(_number: int) -> int:
        return mapGetConnectPortEx_t (_number)


# Запросить имя или адрес хоста
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# name - адрес строки для размещения результата
# size - размер строки (для имени хоста не менее 256)
# Если было установлен адрес хоста - возвращаемое значение 1,
# если имя хоста - возвращаемое значение 2
# При ошибке возвращает ноль

    mapGetConnectHostExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetConnectHostExUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetConnectHostExUn(_number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetConnectHostExUn_t (_number, _name.buffer(), _size)


# Зарегистрировать пользователя
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# parm - логин и пароль для подключения
# Если соединение с сервером не было установлено -
# пытается соединиться с установленными ранее параметрами
# Пароль должен передаваться в зашифрованном виде по алгоритму MD5 (в виде хэша)
# Для получения хэша пароля следует использовать функцию mapStringToMd5Hash
# или svStringToHash (описана в gisdlgs.h)
# выделив выходной буфер для размещения не менее 33 символов (32 символа и замыкающий ноль)
# При ошибке возвращает ноль

    mapRegisterUserUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCUSERPARMUN))
    def mapRegisterUserUn(_number: int, _parm: ctypes.POINTER(maptype.TMCUSERPARMUN)) -> int:
        return mapRegisterUserUn_t (_number, _parm)


# Зарегистрировать текущего пользователя ОС как пользователя ГИС Сервера в домене
# number - номер активного подключения (соединения) к ГИС Серверу от 1 до mapActiveServerCount()
# Если соединение с сервером не было установлено -
# пытается соединиться с установленными ранее параметрами
# При ошибке возвращает ноль

    mapRegisterSystemUserEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRegisterSystemUserEx', ctypes.c_long)
    def mapRegisterSystemUserEx(_number: int) -> int:
        return mapRegisterSystemUserEx_t (_number)


# Удалить в памяти параметры регистрации пользователя
# number - номер активного подключения (соединения) к ГИС Серверу от 1 до mapActiveServerCount()
# После закрытия последнего документа на Сервере соединение
# разрывается и для последующего открытия карты нужно повторно
# выполнить mapRegisterUser()

    mapUnRegisterUserEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUnRegisterUserEx', ctypes.c_long)
    def mapUnRegisterUserEx(_number: int) -> ctypes.c_void_p:
        return mapUnRegisterUserEx_t (_number)


# Запросить тип регистрации пользователя
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# Если регистрация пользователя выполнялась через функцию mapRegisterSystemUserEx,
# то возвращается положительное значение

    mapGetRegisterUserType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetRegisterUserType', ctypes.c_long)
    def mapGetRegisterUserType(_number: int) -> int:
        return mapGetRegisterUserType_t (_number)


# Запросить список доступных пользователю карт на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка карт, структура TMCMAPLIST описана в maptype.h
# buffersize - длина выделенной области памяти
# Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0
# Если общий размер считанной записи больше чем значение buffersize,
# то необходимо увеличить размер буфера и повторить запрос

    mapGetMapListforUserUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMapListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        return mapGetMapListforUserUn_t (_number, _buffer, _buffersize)


# Запросить список доступных пользователю атласов на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка атласов, структура TMCMAPLIST описана в maptype.h
# buffersize - длина выделенной области памяти
# Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0
# Если общий размер считанной записи больше чем значение buffersize,
# то необходимо увеличить размер буфера и повторить запрос

    mapGetAlsListforUserUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetAlsListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetAlsListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        return mapGetAlsListforUserUn_t (_number, _buffer, _buffersize)


# Запросить список доступных пользователю матриц на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка матриц, структура TMCMAPLIST описана в maptype.h
# buffersize - длина выделенной области памяти
# Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0
# Если общий размер считанной записи больше чем значение buffersize,
# то необходимо увеличить размер буфера и повторить запрос

    mapGetMtwListforUserUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMtwListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMtwListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        return mapGetMtwListforUserUn_t (_number, _buffer, _buffersize)


# Запросить список доступных пользователю растров на ГИС-сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# buffer - адрес памяти для размещения списка растров, структура TMCMAPLIST описана в maptype.h
# buffersize - длина выделенной области памяти
# Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0
# Если общий размер считанной записи больше чем значение buffersize,
# то необходимо увеличить размер буфера и повторить запрос

    mapGetRswListforUserUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetRswListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetRswListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        return mapGetRswListforUserUn_t (_number, _buffer, _buffersize)


# Запросить имя пользователя, подключившегося к ГИС-серверу
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# При ошибке возвращает пустую строку

    mapGetCurrentUserNameUn_t = mapsyst.GetProcAddress(curLib,maptype.PWCHAR,'mapGetCurrentUserNameUn', ctypes.c_long)
    def mapGetCurrentUserNameUn(_number: int) -> mapsyst.WTEXT:
        return mapGetCurrentUserNameUn_t (_number)


# Запросить путь к папке для хранения кэшируемых данных с ГИС Сервера

    mapGetCachePathUn_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(maptype.WCHAR),'mapGetCachePathUn')
    def mapGetCachePathUn() -> ctypes.POINTER(maptype.WCHAR):
        return mapGetCachePathUn_t ()


# Установить путь к папке для хранения кэшируемых данных с ГИС Сервера
# path - путь к папке для хранения кэшируемых данных с ГИС Сервера
# Если приложение не установило путь к папке для кэширования данных,
# то она автоматически будет размещена внутри системной папки Temp
# в папке Panorama.Cache
# При ошибке возвращает ноль

    mapSetCachePathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCachePathUn', maptype.PWCHAR)
    def mapSetCachePathUn(_path: mapsyst.WTEXT) -> int:
        return mapSetCachePathUn_t (_path.buffer())


# Установить имя папки для хранения кэша векторных карт с ГИС Сервера
# subfolder - имя папки для хранения кэша векторных карт с ГИС Сервера
# Необходимо для организации устойчивой параллельной работы нескольких приложений
# на одном компьюере с картами на ГИС Сервере при редактировании карт
# Имя папки задается без косых и специальных символов, недопустимых в файловой системе
# При ошибке возвращает ноль

    mapSetMapCacheSubfolder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetMapCacheSubfolder', maptype.PWCHAR)
    def mapSetMapCacheSubfolder(_subfolder: mapsyst.WTEXT) -> int:
        return mapSetMapCacheSubfolder_t (_subfolder.buffer())


# Очистить папку с кэшем данных, открытых с ГИС Сервера или с геопорталов
# Имя папки определяется функцией mapGetCachePathUn
# Данные, открытые в момент вызова функции, могут не удалиться

    mapClearDataCache_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearDataCache')
    def mapClearDataCache() -> ctypes.c_void_p:
        return mapClearDataCache_t ()


# Очистить кэш данных для всех карт текущего документа, открытых с ГИС Сервера
# hmap - идентификатор открытых данных
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearDocCache_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearDocCache', maptype.HMAP)
    def mapClearDocCache(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapClearDocCache_t (_hmap)


# Очистить кэш данных для векторной карты, открытой с ГИС Сервера
# hmap - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearSiteCache_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearSiteCache', maptype.HMAP, maptype.HSITE)
    def mapClearSiteCache(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return mapClearSiteCache_t (_hmap, _hsite)


# Очистить кэш карты из пространственной базы открытой без ГИС Сервера
# hmap - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Запускает процесс полного переформирования картографического представления
# на основе данных из пространственной базы данных

    mapClearLocalDbmCache_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearLocalDbmCache', maptype.HMAP, maptype.HSITE)
    def mapClearLocalDbmCache(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return mapClearLocalDbmCache_t (_hmap, _hsite)


# Очистить кэш данных для всех карт текущего документа с ГИС Сервера
# hmap - идентификатор открытых данных
# Кэш автоматически очищается при сортировке карты на ГИС Сервере
# или обнаружении большого числа выполненных транзакций,
# с момента предыдущего обращения к данным
# Иначе кэш обновляется (реплицируется) в соответствии
# с журналом транзакций на ГИС Сервере

    mapClearServerCache_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearServerCache', maptype.HMAP)
    def mapClearServerCache(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        return mapClearServerCache_t (_hmap)


# Запросить открыта ли карта на сервере или локально
# hmap - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Если карта открыта на сервере возвращает ненулевое значение

    mapIsMapFromServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsMapFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsMapFromServer(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsMapFromServer_t (_hmap, _hsite)


# Запросить список папок на сервере, доступных для записи файлов
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к виртуальной папке, в которой запрашивается список файлов и папок или 0
#          Например, "Data\\Maps"
#          Если folder равно 0, то запрашивается список алиасов всех доступных папок
# allfiles - признак запроса всех файлов в папке folder, если не установлен,
#           то буден выдан список внутренних папок и файлов MAP,SIT,SITX,RSC,MTW,MTQ,RSW
# parm   - адрес буфера для размещения списка запрошенных данных или 0
#          Если parm равно 0, то запрашивается размер буфера, требуемый для размещения списка
# size - размер буфера для размещения списка
# Список данных заполняется только для файлов и папок, непосредственно расположенных
# в заданной папке без вложений
# При успешном выполнении возвращает размер сформированного списка
# Если размер списка превышает размер буфера, то данные считаны не полностью
# Тогда нужно выделить больший буфер и запросить данные повторно
# При ошибке возвращает ноль

    mapGetFolderList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetFolderList', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_long)
    def mapGetFolderList(_number: int, _folder: mapsyst.WTEXT, _allfiles: int, _parm: ctypes.POINTER(maptype.TMCDATALIST), _size: int) -> int:
        return mapGetFolderList_t (_number, _folder.buffer(), _allfiles, _parm, _size)


# Запросить виртуальную папку по алиасу карты
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - алиас карты
# folder - адрес строки для записи алиаса виртуальной папки
# size   - длина строки в байтах
# При ошибке возвращает ноль

    mapGetMapFolderOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapFolderOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapFolderOnServer(_number: int, _alias: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapFolderOnServer_t (_number, _alias.buffer(), _folder.buffer(), _size)


# Создать папку на сервере относительно алиаса доступной папки
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к создаваемой папке
#          Например, "Data\\Maps" или "Data/Maps",
#          где "Data" - виртуальная папка в настройках ГИС Сервера, "Maps" - создаваемая папка
# При ошибке возвращает ноль

    mapCreateFolderOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateFolderOnServer', ctypes.c_long, maptype.PWCHAR)
    def mapCreateFolderOnServer(_number: int, _folder: mapsyst.WTEXT) -> int:
        return mapCreateFolderOnServer_t (_number, _folder.buffer())


# Удалить папку на сервере относительно алиаса доступной папки
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь к удаляемой папке
#          Например, для удаления папки "Maps": "Data\\Maps" или "Data/Maps",
#          где "Data" - виртуальная папка в настройках ГИС Сервера, "Maps" - удаляемая папка
# deletefiles - удалить все файлы в папке (если задано ненулевое значение)
# deletefolders - удалить все подпапки с файлами в них (если задано ненулевое значение)
# При ошибке возвращает ноль

    mapDeleteFolderOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteFolderOnServer', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapDeleteFolderOnServer(_number: int, _folder: mapsyst.WTEXT, _deletefiles: int, _deletefolders: int) -> int:
        return mapDeleteFolderOnServer_t (_number, _folder.buffer(), _deletefiles, _deletefolders)


# Удалить файл на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# file - путь к удаляемому файлу
#        Например, "Data\\Maps\\image.rsw",
#        где "Data" - виртуальная папка в настройках ГИС Сервера, "image.rsw" - удаляемый файл
# При ошибке возвращает ноль

    mapDeleteFileOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteFileOnServer', ctypes.c_long, maptype.PWCHAR)
    def mapDeleteFileOnServer(_number: int, _file: mapsyst.WTEXT) -> int:
        return mapDeleteFileOnServer_t (_number, _file.buffer())


# Скопировать файл на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# source - путь к изменяемому файлу
#          Например, "Data\\Maps\\image.sitx",
#          где "Data" - виртуальная папка на ГИС Сервере, "image.sitx" - перемещаемый файл
# target - новый путь к файлу
#          Например, "Storage\\Roads\\road_M4.sitx",
# При ошибке возвращает ноль

    mapCopyFileOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapCopyFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        return mapCopyFileOnServer_t (_number, _source.buffer(), _target.buffer())


# Переименовать (переместить) файл или папку на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# source - путь к изменяемому файлу или папке
#          Например, "Data\\Maps\\image.sitx",
#          где "Data" - виртуальная папка на ГИС Сервере, "image.sitx" - перемещаемый файл
# target - новый путь к файлу или папке
#          Например, "Storage\\Roads\\road_M4.sitx",
# При ошибке возвращает ноль

    mapRenameFileOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRenameFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapRenameFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        return mapRenameFileOnServer_t (_number, _source.buffer(), _target.buffer())


# Сохранить файл на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь для сохранения файла, путь может начинаться с имени алиаса папки, доступной для записи данных
#          Например: "Data\\Maps" или "Data/Maps/Images", где "Data" - виртуальная папка на ГИС Сервере, /Maps/Images - поддиректории
#          или содержать полный алиас виртуальной папки на сервере с поддиректориями
#          Например: "HOST#123.345.0.12#ALIAS#Data/Maps/Images"
#          или содержать полный алиас карты, записанной в виртуальной папке на сервере, с поддиректориями относительно карты
#          Например: "HOST#123.345.0.12#ALIAS#Mymap/Images"
# file   - путь к файлу, который будет записан в папку на сервере (файл должен содержать данные, а не выполняемый код).
# Имя файла, расширение и атрибуты чтения/записи сохраняются
# Отсутствующие директории создаются автоматически
# Символ косой может быть любого вида - "/" или "\\"
# Для доступа к файлу в дальнейшем нужно объединить путь к папке и имя файла,
# например: "HOST#123.345.0.12#ALIAS#Data/Maps/example.sitx"
# При ошибке возвращает ноль

    mapSaveFileOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapSaveFileOnServer(_number: int, _folder: mapsyst.WTEXT, _file: mapsyst.WTEXT) -> int:
        return mapSaveFileOnServer_t (_number, _folder.buffer(), _file.buffer())


# Сохранить карту на сервере
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# folder - путь для сохранения файла, путь должен начинаться с алиаса папки,
#          доступной для записи данных
#          Например, "Data\\Maps" или "Data/Maps",
#          где "Data" - виртуальная папка на ГИС Сервере
# hmap -  идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# rscsave - признак необходимости сохранения файла RSC на сервер
# При ошибке возвращает ноль

    mapSaveMapOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveMapOnServer', ctypes.c_long, maptype.PWCHAR, maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSaveMapOnServer(_number: int, _folder: mapsyst.WTEXT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscsave: int) -> int:
        return mapSaveMapOnServer_t (_number, _folder.buffer(), _hmap, _hsite, _rscsave)


# Прочитать файл на сервере (если есть доступ к виртуальной папке)
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias   - алиас файла на сервере, начиная с имени виртуальной папки (кроме выполняемых файлов,
#           файлов карт, матриц и растров)
# path    - путь, по которому будет сохранен файл (после записи путь дополняется именем файла)
# size    - размер поля, содержащего путь
# error   - поле для записи кода ощибки, если функция вернет ноль
# При ошибке возвращает ноль

    mapReadFileOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapReadFileOnServer(_number: int, _alias: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapReadFileOnServer_t (_number, _alias.buffer(), _path.buffer(), _size, _error)


# Запросить список пользователей, ролей и данных, размещенных на ГИС Сервере в виде xml
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# path    - путь, по которому будет сохранен файл
# error   - поле для записи кода ощибки, если функция вернет ноль
# При ошибке возвращает ноль

    mapGetServerUsersListInXml_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetServerUsersListInXml', ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetServerUsersListInXml(_number: int, _xmlname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
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

    mapSaveToGeoDB_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveToGeoDB', ctypes.c_long, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapSaveToGeoDB(_number: int, _handle: maptype.HMESSAGE, _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
        return mapSaveToGeoDB_t (_number, _handle, _dslist.buffer(), _logname.buffer(), _size)


# Отправить команду на загрузку наборов данных c ГИС Сервера в Банк данных
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# handle  - идентификатор окна, которому посылаются сообщения о ходе загрузки данных в Банк данных
# dslist  - имя файла - списка загружаемых наборов данных
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# error   - код ошибки выполнения запроса
# Наборы данных могут быть загружены удаленно другим приложением на ГИС Сервер
# в специальную папку для Банка Данных
# При ошибке возвращает ноль

    mapCallGeoDBLoaderPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallGeoDBLoaderPro', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCallGeoDBLoaderPro(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCallGeoDBLoaderPro_t (_number, _callevent, _parm, _dslist.buffer(), _logname.buffer(), _size, _error)


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

    mapCallDbCommand_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallDbCommand', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR)
    def mapCallDbCommand(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long), _command: mapsyst.WTEXT) -> int:
        return mapCallDbCommand_t (_number, _callevent, _parm, _dslist.buffer(), _logname.buffer(), _size, _error, _command.buffer())


# Отправить команду на формирование геопокрытия из наборов данных Банка данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# geolist - имя файла - списка наборов данных для формирования геопокрытий
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size - размера буфера для записи имени файла протокола
# error - поле для записи кода ошибки (maperr.rh)
# При ошибке возвращает ноль

    mapCallGeoLevelEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallGeoLevelEx', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCallGeoLevelEx(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _geolist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCallGeoLevelEx_t (_number, _callevent, _parm, _geolist.buffer(), _logname.buffer(), _size, _error)


# Отправить команду на экспорт геопокрытия в Банке данных ЦК и ДЗЗ
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# exportlist - имя файла - списка экспортируемых геопокрытий (формат для экспорта задается в списке)
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# logname - буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
# size    - размера буфера для записи имени файла протокола
# error - поле для записи кода ошибки (maperr.rh)
# При ошибке возвращает ноль

    mapCallExport_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCallExport', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_long))
    def mapCallExport(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _exportlist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCallExport_t (_number, _callevent, _parm, _exportlist.buffer(), _logname.buffer(), _size, _error)


# Запросить разрешение на копирование файлов карты на клиент
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - алиас данных на сервере
# error - код ошибки доступа (см. maperr.rh)
# При ошибке возвращает ноль, иначе - тип данных (1 - карта, 2 - растр, 3 - матрица)

    mapIsCopyDataEnabled_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsCopyDataEnabled', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapIsCopyDataEnabled(_number: int, _alias: mapsyst.WTEXT, _type: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapIsCopyDataEnabled_t (_number, _alias.buffer(), _type, _error)


# Скопировать набор данных с ГИС Сервера на клиент
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias  - алиас данных на сервере
# type   - тип данных (1 - карта, 2 - растр, 3 - матрица или 0 - требуется определить)
# target - имя файла выходного набора данных (если задана только папка, то имя формируется
#          с учетом алиаса и типа данных
# targetsize - длина буфера target в байтах (для обновления выходного имени)
# error  - код ошибки доступа (см. maperr.rh)
# При ошибке возвращает ноль, иначе - тип данных (1 - карта, 2 - растр, 3 - матрица)

    mapCopyDataFromServerEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopyDataFromServerEx', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCopyDataFromServerEx(_number: int, _alias: mapsyst.WTEXT, _type: int, _target: mapsyst.WTEXT, _targetsize: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapCopyDataFromServerEx_t (_number, _alias.buffer(), _type, _target.buffer(), _targetsize, _error)


# Запросить список классификаторов, доступных для операций импорта данных
#<?xml version="1.0" encoding="UTF-8"?>
#<rsclist><rsc name="Топокарты масштаба 1:25 000" alias="25t17g.rsc"/></rsclist>
# После завершения обработки ответа необходимо освободить память - mapFreeRscList
# При ошибке возвращает ноль

    mapGetRscListOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetRscListOnServer', ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRscListOnServer(_number: int, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetRscListOnServer_t (_number, _size)


# Освободить память, выделенную функцией mapGetRscListOnServer
# buffer - адрес памяти, выделенной функцией mapGetRscListOnServer

    mapFreeRscList_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeRscList', ctypes.c_char_p)
    def mapFreeRscList(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeRscList_t (_buffer)


# Прочитать состояние файла (дату и время обновления, размер) на сервере (если есть доступ к виртуальной папке)
# number - номер активного подключения к ГИС Серверу от 1 до mapActiveServerCount()
# alias - алиас файла на сервере, начиная с имени виртуальной папки (кроме выполняемых файлов,
#         файлов карт, матриц и растров)
# size  - поле для записи размера файла
# time  - поле для записи даты и времени обновления файла
# error - поле для записи кода ощибки, если функция вернет ноль
# При ошибке возвращает ноль

    mapReadFileStateOnServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadFileStateOnServer', ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(maptype.SYSTEMTIME), ctypes.POINTER(ctypes.c_long))
    def mapReadFileStateOnServer(_number: int, _alias: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_int64), _time: ctypes.POINTER(maptype.SYSTEMTIME), _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapReadFileStateOnServer_t (_number, _alias.buffer(), _size, _time, _error)


# Преобразовать входную строку (не более 1024 байта), заканчивающуюся 0, в строку в формате md5
# instring - входная строка
# outstring - выходная строка в формате md5
# length - размер выходной строки
# При ошибке возвращает ноль

    mapStringToMd5Hash_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapStringToMd5Hash', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapStringToMd5Hash(_instring: ctypes.c_char_p, _outstring: ctypes.c_char_p, _length: int) -> int:
        return mapStringToMd5Hash_t (_instring, _outstring, _length)


# Открыть запись в диагностический протокол
# logname - путь к протоколу диагностической печати, если равен нулю,
#           то запись идет в \ProgramData\mapdiagnostics.log или /var/Panorama/
# hideinfo - признак отключения выдачи информационных сообщений (MT_INFO)
# При ошибке возвращает ноль

    mapOpenDiagnosticsEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapOpenDiagnosticsEx', maptype.PWCHAR, ctypes.c_long)
    def mapOpenDiagnosticsEx(_logname: mapsyst.WTEXT, _hideinfo: int) -> int:
        return mapOpenDiagnosticsEx_t (_logname.buffer(), _hideinfo)


# Запросить, открыт ли диагностический протокол

    mapIsDiagnostics_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsDiagnostics')
    def mapIsDiagnostics() -> int:
        return mapIsDiagnostics_t ()


# Закрыть запись в диагностический протокол

    mapCloseDiagnostics_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCloseDiagnostics')
    def mapCloseDiagnostics() -> ctypes.c_void_p:
        return mapCloseDiagnostics_t ()


# Записать сообщение в диагностический протокол
# message - первая часть сообщения
# messageex - вторая часть сообщения
# type - тип сообщения (>>> MT_ERROR, --> MT_WARNING, MT_INFO, MT_CONTINUE - продолжение)
# error - код ошибки, запрошенный у системы (если равен 0, то будет запрошен при выводе сообщения)
# value - число, которое будет преобразовано в строку и добавлено к сообщению

    mapWriteToLogLastError_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapWriteToLogLastError', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapWriteToLogLastError(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int = maptype.MT_ERROR, _error: int = 0) -> ctypes.c_void_p:
        return mapWriteToLogLastError_t (_message.buffer(), _messageex.buffer(), _type, _error)


# Записать сообщение по коду ошибки в диагностический протокол
# code - код ошибки для формирования сообщения (maperr.rh)
# message - сообщение, добавляемое к описанию ошибки
# type - тип сообщения (>>> MT_ERROR, --> MT_WARNING, MT_INFO, MT_CONTINUE - продолжение)
# error - код ошибки, запрошенный у системы (если равен 0, то будет запрошен при выводе сообщения)

    mapWriteErrorToDiagnosticsLog_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapWriteErrorToDiagnosticsLog', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapWriteErrorToDiagnosticsLog(_code: int, _message: mapsyst.WTEXT, _type: int = maptype.MT_ERROR) -> ctypes.c_void_p:
        return mapWriteErrorToDiagnosticsLog_t (_code, _message.buffer(), _type)


# Записать сообщение с числом в диагностический протокол
# message - текст сообщения
# value - число, которое будет преобразовано в строку и добавлено к сообщению
# type - тип сообщения (>>> MT_ERROR, --> MT_WARNING, MT_INFO, MT_CONTINUE - продолжение)

    mapWriteToLogInt_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapWriteToLogInt', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapWriteToLogInt(_message: mapsyst.WTEXT, _value: int, _type: int = maptype.MT_INFO) -> ctypes.c_void_p:
        return mapWriteToLogInt_t (_message.buffer(), _value, _type)


# Включить или отключить вывод диагностического протокола в консоль
# flag - флаг включения вывода на консоль: 1 или 0
# std::cout << "Diagnostics" << ": " << message << std::endl;

    SetConsoleOutput_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'SetConsoleOutput', ctypes.c_long)
    def SetConsoleOutput(_flag: int) -> ctypes.c_void_p:
        return SetConsoleOutput_t (_flag)


# Запросить полный путь к диагностическому протоколу
# mapdiagnostic - буфер для записи пути к файлу протокола
# size - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetDiagnosticFileName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDiagnosticFileName', maptype.PWCHAR, ctypes.c_long)
    def mapGetDiagnosticFileName(_mapdiagnostic: mapsyst.WTEXT, _size: int) -> int:
        return mapGetDiagnosticFileName_t (_mapdiagnostic.buffer(), _size)


# Получить идентификатор системы кодирования
# key  - строка, содержащая двоичный ключ для кодирования данных
#        Ключ должен иметь случайное равномерное заполнение,
#        например, методом преобразования пароля пользователя и текущего
#        времени по алгоритму MD5
# size - длина строки (должна быть равна 32 байта)
# После завершения кодирования/раскодирования нужно освободить ресурсы
# функцией mapDeleteCoder
# При ошибке возвращает ноль

    mapCreateCoder_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapCreateCoder', ctypes.c_char_p, ctypes.c_int)
    def mapCreateCoder(_key: ctypes.c_char_p, _size: int) -> ctypes.c_void_p:
        return mapCreateCoder_t (_key, _size)


# Закодировать область данных заданным ключом (длина области кратна 16)
# hcoder - идентификатор системы кодирования
# memory - адрес области памяти, которую нужно закодировать
# size   - размер области памяти для кодирования, кратный 16 байтам
# Для кодирования применяются операции XOR и циклического сдвига данных
# Состояние ключа меняется при кодировании под управлением кодируемых данных
# При ошибке возвращает ноль

    mapCoderOn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCoderOn', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapCoderOn(_hcoder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        return mapCoderOn_t (_hcoder, _memory, _size)


# Раскодировать область данных заданным ключом (длина области кратна 16)
# hcoder - идентификатор системы кодирования
# memory - адрес области памяти, которую нужно декодировать
# size   - размер области памяти для декодирования, кратный 16 байтам
# Для кодирования применяются операции XOR и циклического сдвига данных
# Состояние ключа меняется при кодировании под управлением кодируемых данных
# При ошибке возвращает ноль

    mapCoderOff_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCoderOff', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapCoderOff(_hcoder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        return mapCoderOff_t (_hcoder, _memory, _size)


# Освободить ресурсы после завершения кодирования/раскодирования
# hcoder - идентификатор системы кодирования

    mapDeleteCoder_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapDeleteCoder', ctypes.c_void_p)
    def mapDeleteCoder(_hcoder: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapDeleteCoder_t (_hcoder)


# Запросить/Установить признак использования семантики при отображении объекта
# info   - идентификатор объекта карты в памяти
# isview - признак использования семантики при отображении объекта
# При отображении объектов классификатора и присвоении служебных семантик,
# влияющих на вид объекта, использование семантики происходит автоматически
# При ошибке возвращает ноль

    mapSetObjectViewSemantic_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapSetObjectViewSemantic', maptype.HOBJ, ctypes.c_int)
    def mapSetObjectViewSemantic(_info: maptype.HOBJ, _isview: int) -> int:
        return mapSetObjectViewSemantic_t (_info, _isview)


# Запросить номер листа по его номенклатуре
# hmap - идентификатор открытых данных
# name - имя листа
# При ошибке возвращает ноль

    mapGetListNumberByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetListNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetListNumberByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapGetListNumberByNameUn_t (_hmap, _name.buffer())


# Установить/Запросить язык сообщений
# 1 - английский, 2 - русский, ... (см. Maptype.h)
# (по-умолчанию - английский)

    mapSetMapAccessLanguage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetMapAccessLanguage', ctypes.c_int)
    def mapSetMapAccessLanguage(_code: int) -> ctypes.c_void_p:
        return mapSetMapAccessLanguage_t (_code)

    mapGetMapAccessLanguage_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetMapAccessLanguage')
    def mapGetMapAccessLanguage() -> int:
        return mapGetMapAccessLanguage_t ()


# Записать сообщение в диагностический протокол
# message - первая часть сообщения
# messageex - вторая часть сообщения
# type - тип сообщения (>>> MT_ERROR, --> MT_WARNING, MT_INFO, MT_CONTINUE - продолжение)
# error - код ошибки, запрошенный у системы (если равен 0, то будет запрошен при выводе сообщения)
# value - число, которое будет преобразовано в строку и добавлено к сообщению

    mapWriteToDiagnosticsLog_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapWriteToDiagnosticsLog', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapWriteToDiagnosticsLog(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        return mapWriteToDiagnosticsLog_t (_message.buffer(), _messageex.buffer(), _type)


# Выдать сообщение на экран через системную функцию MessageBox
# Если mapIsMessageEnable() равно 0, то сообщение не выдается и функция возвращает ноль
# Если установлена функция обратного вызова mapSetMessageBoxCall, то выдача сообщения будет через эту функцию

    mapMessageBoxUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapMessageBoxUn', maptype.HWND, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
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

    mapSetHandleForMessage_t = mapsyst.GetProcAddress(curLib,maptype.HMESSAGE,'mapSetHandleForMessage', maptype.HMESSAGE)
    def mapSetHandleForMessage(_hwnd: maptype.HMESSAGE) -> maptype.HMESSAGE:
        return mapSetHandleForMessage_t (_hwnd)

    mapGetHandleForMessage_t = mapsyst.GetProcAddress(curLib,maptype.HMESSAGE,'mapGetHandleForMessage')
    def mapGetHandleForMessage() -> maptype.HMESSAGE:
        return mapGetHandleForMessage_t ()


# Отправить команду главному окну (текущему окну карты)
# Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически) 
# command - идентификатор команды
# wparam  - первый параметр
# lparam  - второй параметр
# Например, перерисовать окно карты: mapSendMessage(MT_MAPWINPORT, MWP_INVALIDATE, 0);
# Например, выделить объекты на карте по общим условиям: mapSendMessage(CM_PAN_SEARCH, 1, 0);

    mapSendMessage_t = mapsyst.GetProcAddress(curLib,ctypes.c_longlong, 'mapSendMessage', ctypes.c_int,  ctypes.c_void_p, ctypes.c_void_p)
    def mapSendMessage(_command: ctypes.c_int, _wparam: ctypes.c_longlong, _lparam = 0) -> ctypes.c_longlong:
        return mapSendMessage_t(_command, ctypes.cast(_wparam, ctypes.c_void_p), ctypes.cast(_lparam, ctypes.c_void_p))


# Перерисовать окно карты
    def mapInvalidate():
        mapSendMessage(maptype.MT_MAPWINPORT, maptype.MWP_INVALIDATE, 0)

# Выделить объекты на карте по общим условиям 
    def mapSelectObjects(flag = 1):
        mapSendMessage(maptype.CM_PAN_SEARCH, flag)

# Число в строку
    def IntToStr(_number:int):
        text = mapsyst.WTEXT(64)
        mapLongToStringUn(_number, text, text.size())
        return text.string()

    def FloatToStr(_value:float, _precision = 3):
        text = mapsyst.WTEXT(64)
        mapDoubleToStringUn(_value, text, text.size(), _precision)
        return text.string()

def mapapi_healthcheck(): 
    return 1