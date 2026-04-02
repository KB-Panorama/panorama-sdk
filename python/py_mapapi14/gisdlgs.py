#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst

PACK_WIDTH = 1

#-----------------------------
class MEDRSCPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Regime",ctypes.c_int),
                ("Repeat",ctypes.c_int),
                ("FlagKey",ctypes.c_int),
                ("AllowReadOnly",ctypes.c_int),
                ("NameDlg",ctypes.c_char*128),
                ("Key",ctypes.c_char*32)]
#-----------------------------


#-----------------------------
class CHOICEOBJECTPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hSelect",maptype.HSELECT),
                ("MapSelect",ctypes.c_int),
                ("MapEditSelect",ctypes.c_int)]
#-----------------------------


#-----------------------------
class OBJFROMRSC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hSelect",maptype.HSELECT),
                ("MapSelect",ctypes.c_int),
                ("Regime",ctypes.c_int),
                ("Repeat",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BUILDZONEPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("FlagDial",ctypes.c_int),
                ("Check",ctypes.c_int),
                ("Size",ctypes.c_int),
                ("TypeZone",ctypes.c_int),
                ("EnableType",ctypes.c_int),
                ("FormZone",ctypes.c_int)]
#-----------------------------


#-----------------------------
class COPY_OPTIONS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MapNumber",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("DeleteSourceObject",ctypes.c_int),
                ("DeleteWrongSemantic",ctypes.c_int),
                ("CutByObject",ctypes.c_int),
                ("LocationPoint",ctypes.c_int),
                ("SimplifyScale",ctypes.c_int),
                ("Reserve",ctypes.c_int*9)]
#-----------------------------


try:
    if os.environ['gisdlgsdll']:
        gisdlgsname = os.environ['gisdlgsdll']
except KeyError:
    gisdlgsname = 'gis64dlgs.dll'

try:
    dlgslib = mapsyst.LoadLibrary( gisdlgsname )


# Диалог "Редактирование метрики объекта"
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# info    - идентификатор редактируемого объекта
# rect    - местоположение открываемого диалога или 0
# Вызов файла справки из Mapscena.chm ("ENPOINT")
# При ошибке возвращает ноль

    tedInsertPoints_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedInsertPoints', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(maptype.RECT))
    def tedInsertPoints(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        return tedInsertPoints_t (_hmap, _parm, _info, _rect)


# Диалог "Редактирование семантики объекта"
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать идентификатор главного окна)
# info    - идентификатор редактируемого объекта
# Вызов файла справки из Mapscena.chm ("SOKOL")
# При ошибке возвращает ноль

    tedEditSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedEditSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ)
    def tedEditSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ) -> int:
        return tedEditSemantic_t (_hmap, _parm, _info)


# Диалог "Обновление семантики объектов"
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# Вызов файла справки из Mapscena.chm ("ZAMSEM")
# При ошибке возвращает ноль

    tedUpdateSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedUpdateSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def tedUpdateSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return tedUpdateSemantic_t (_hmap, _parm)


# Диалог "Редактирование семантики типа "Дата"
# value   - адрес строки, содержащей дату в виде ДД/ММ/ГГГГ
#           (строка исходная и в неё же записывается результат)
# size    - размер строки
# parm    - структура параметров для диалога (см. maptype.h)
# point - координаты верхнего левого угла диалога
# При ошибке возвращает ноль

#    semGetDateSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'semGetDateSemantic', ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.POINT))
#    def semGetDateSemantic(_value: ctypes.c_char_p, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _point: ctypes.POINTER(maptype.POINT)) -> int:
#        return semGetDateSemantic_t (_value, _size, _parm, _point)


# Установка/Изменение текста многострочной подписи
# parm    - параметры задачи (поле Handle должно содержать идентификатор главного окна)
# hobj    - идентификатор объекта типа ПОДПИСЬ
# subject - номер продобъекта
# font    - описание шрифта
# При вызове диалога Выбор объекта для редактирования семантики возвращает -1
# При отказе возвращает 0, иначе 1

    tedSetPolyText_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedSetPolyText', ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_int, ctypes.POINTER(maptype.LOGFONT))
    def tedSetPolyText(_taskparm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _subject: int, _font: ctypes.POINTER(maptype.LOGFONT)) -> int:
        return tedSetPolyText_t (_taskparm, _hobj, _subject, _font)


# Ввод произвольного текста
# При ошибке возвращает ноль

    tedSetTextUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedSetTextUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.RECT))
    def tedSetTextUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _caption: mapsyst.WTEXT, _ctext: mapsyst.WTEXT, _maxsize: int, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        return tedSetTextUn_t (_parm, _caption.buffer(), _ctext.buffer(), _maxsize, _rect)


# Диалог "Отмена транзакций"
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# Вызов файла справки из Mapscena.chm ("KON1")
# При ошибке возвращает ноль

    tedUndoOperation_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedUndoOperation', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def tedUndoOperation(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return tedUndoOperation_t (_hmap, _parm)


# Диалог "Перейти в заданную точку по координатам"
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# place   - формат отображаемых в диалоге координат:
# PLANEPOINT      = 1,  В метрах на местности
# MAPPOINT        = 2,  В условных единицах карты (дискретах)
# PICTUREPOINT    = 3,  В пикселах текущего полного изображения
#                       эллипсоид Красовского 1942г.
# GEORAD          = 4,  В радианах в соответствии с проекцией
# GEOGRAD         = 5,  В градусах ...
# GEOGRADMIN      = 6,  В градусах, минутах, секундах ...
#                       общеземной эллипсоид WGS84
# GEORADWGS84     = 7,  В радианах в соответствии с проекцией
# GEOGRADWGS84    = 8,  В градусах ...
# GEOGRADMINWGS84 = 9,  В градусах, минутах, секундах ...
# PLANE42POINT    = 10, В метрах на местности по ближайшей зоне
# GEORADPZ90      = 11, В радианах в соответствии с проекцией
# GEOGRADPZ90     = 12, В градусах ...
# GEOGRADMINPZ90  = 13, В градусах, минутах, секундах ...
# point  - координаты текущей точки в метрах на карте
# При успешном выполнении возвращает координаты выбранной точки в метрах
# на карте
# Вызов файла справки из Mapscena.chm ("MOVEMENT")
# При ошибке возвращает ноль

    tedGoPoint_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedGoPoint', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT))
    def tedGoPoint(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _place: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return tedGoPoint_t (_hmap, _parm, _place, _point)


# Диалог "Добавление в документ данных из каталога"
# Могут быть добавлены ПК, Mtw, Rsw, Mtl, Mtq, Tin
# hmap    - идентификатор открытой карты
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# title   - указатель на текст заголовка диалога или 0
# flagSit - флаг запрета добавления ПК  (0-запрещено/1-разрешено)
# flagMtw - флаг запрета добавления Mtw (0-запрещено/1-разрешено)
# flagRsw - флаг запрета добавления Rsw (0-запрещено/1-разрешено)
# flagMtl - флаг запрета добавления Mtl (0-запрещено/1-разрешено)
# flagMtq - флаг запрета добавления Mtq (0-запрещено/1-разрешено)
# flagTin - флаг запрета добавления Tin (0-запрещено/1-разрешено)
# Вызов файла справки из Mapscena.chm ("IDN7081")
# При ошибке возвращает ноль

    tedAddDataFormDirEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedAddDataFormDirEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def tedAddDataFormDirEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: ctypes.c_char_p, _flagSit: int, _flagMtw: int, _flagRsw: int, _flagMtl: int, _flagMtq: int, _flagTin: int) -> int:
        return tedAddDataFormDirEx_t (_hmap, _parm, _title, _flagSit, _flagMtw, _flagRsw, _flagMtl, _flagMtq, _flagTin)


# Создание нового объекта  (устаревшая функция)
# hmap - идентификатор открытой векторной карты
# parm    - параметры задачи
# hobj - идентификатор объекта
# medparm - параметры создания
# choiceparm - параметры для диалога выбора вида объекта
# hselect - фильтр (если hselect == 0 - фильтр не используется)
# title  - заголовок диалога или 0
# Возвращает внутренний код объекта
# Вызов файла справки из Mapscena.chm ("SelecOb")
# При ошибке или отмене выбора возвращает 0

    scnChoiceNewObjectUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnChoiceNewObjectUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(MEDRSCPARM), ctypes.POINTER(CHOICEOBJECTPARM), maptype.HSELECT, maptype.PWCHAR)
    def scnChoiceNewObjectUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _medparm: ctypes.POINTER(MEDRSCPARM), _choiceparm: ctypes.POINTER(CHOICEOBJECTPARM), _select: maptype.HSELECT, _title: mapsyst.WTEXT) -> int:
        return scnChoiceNewObjectUn_t (_hmap, _parm, _hobj, _medparm, _choiceparm, _select, _title.buffer())

    scnChoiceNewObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnChoiceNewObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(MEDRSCPARM), ctypes.POINTER(CHOICEOBJECTPARM), maptype.HSELECT)
    def scnChoiceNewObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _medparm: ctypes.POINTER(MEDRSCPARM), _choiceparm: ctypes.POINTER(CHOICEOBJECTPARM), _select: maptype.HSELECT) -> int:
        return scnChoiceNewObject_t (_hmap, _parm, _hobj, _medparm, _choiceparm, _select)


# Создание (выбора вида) объекта
# hmap - идентификатор открытой векторной карты
# parm - параметры задачи (описание в maptype.h)
# hobj - идентификатор объекта
# objparm - параметры для диалога выбора вида объекта
# name - заголовок диалога
# checkedit - флаг обязательного наличия карт, доступных для редактирования
# если checkedit=1 и нет карт доступных для редактирования при вызове диалога
# будет сгенерирована ошибка
# Возвращает внутренний код объекта
# При ошибке или отмене выбора возвращает 0

    scnGetObjectFromRsc_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetObjectFromRsc', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(OBJFROMRSC), ctypes.c_char_p)
    def scnGetObjectFromRsc(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _objparm: ctypes.POINTER(OBJFROMRSC), _title: ctypes.c_char_p) -> int:
        return scnGetObjectFromRsc_t (_hmap, _parm, _hobj, _objparm, _title)

    scnGetObjectFromRscUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetObjectFromRscUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(OBJFROMRSC), maptype.PWCHAR)
    def scnGetObjectFromRscUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _objparm: ctypes.POINTER(OBJFROMRSC), _title: mapsyst.WTEXT) -> int:
        return scnGetObjectFromRscUn_t (_hmap, _parm, _hobj, _objparm, _title.buffer())

    scnGetObjectFromRscUnEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetObjectFromRscUnEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(OBJFROMRSC), maptype.PWCHAR, ctypes.c_int)
    def scnGetObjectFromRscUnEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _objparm: ctypes.POINTER(OBJFROMRSC), _title: mapsyst.WTEXT, _checkedit: int = 1) -> int:
        return scnGetObjectFromRscUnEx_t (_hmap, _parm, _hobj, _objparm, _title.buffer(), _checkedit)


# Диалог настройки графического описания линии и полигона
# На момент вызова функции info должен быть зарегистрирован (mapRegisterDrawObject)
# как линейный или площадной объект (в зависимости от локализации появляются разные диалоги)
# hmap   - идентификатор открытой векторной карты
# parm   - параметры приложения
# info   - идентификатор редактируемого объекта
# regime - указатель на переменную, в которую будет записан выбранный способ нанесения
#          объекта (MC_POLYLINE,MC_RECT,...)
# isnew  - признак нового или редактируемого объекта:
#          1 - объект создается (есть кнопки способа нанесения)
#          0 - редактируется графика объекта, нет кнопок способа нанесения
# При ошибке возвращает 0

    scnSetLineDraw_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetLineDraw', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def scnSetLineDraw(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _regime: ctypes.POINTER(ctypes.c_int), _isnew: int) -> int:
        return scnSetLineDraw_t (_hmap, _parm, _info, _regime, _isnew)


# Диалог настройки графического описания подписи
# На момент вызова функции info должен быть зарегистрирован (mapRegisterDrawObject)
# как подпись
# hmap   - идентификатор открытой векторной карты
# parm   - параметры приложения
# info   - идентификатор редактируемого объекта
# regime - указатель на переменную, в которую будет записан выбранный способ
#          нанесения объекта (MC_POLYLINE,...)
# isnew  - признак нового или редактируемого объекта:
#            1 - объект создается (есть кнопки способа нанесения)
#            0 - редактируется графика объекта, нет кнопок способа нанесения
# При ошибке возвращает 0

    scnSetLabelDraw_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetLabelDraw', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def scnSetLabelDraw(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _regime: ctypes.POINTER(ctypes.c_int), _isnew: int) -> int:
        return scnSetLabelDraw_t (_hmap, _parm, _info, _regime, _isnew)


# Диалог "Настройка вида лицензии"
# param  - параметры задачи (поле IniName должно содержать
#          имя ini файла, поле PathShell - каталог приложения)
# Вызов файла справки из Mapscena.chm (тема "IDN_LICENSE")
# При ошибке или отказе возвращает 0

    mapExecuteGNClient_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mapExecuteGNClient', ctypes.POINTER(maptype.TASKPARMEX))
    def mapExecuteGNClient(_param: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return mapExecuteGNClient_t (_param)


# Выбор номера карты (векторной, растровой, матричной) из списка
# hmap    - идентификатор открытой векторной карты
# parm    - параметры задачи
# maptype - тип данных: FILE_MAP, FILE_RSW, FILE_MTW
# accesstype - тип доступа к данным:
#              0 - все, 1-только для копирования, 2-только с полным доступом
# title      - название вызывающей задачи
# Возвращает: -1 при отказе от выбора или отсутствии карт, иначе - номер карты
# в списке (с 0 для FILE_MAP и с 1 для FILE_RSW, FILE_MTW)

    scnGetMapNumberWithTitleEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetMapNumberWithTitleEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def scnGetMapNumberWithTitleEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _maptype: ctypes.POINTER(ctypes.c_int), _accesstype: int, _current: int, _addflag: int, _title: mapsyst.WTEXT) -> int:
        return scnGetMapNumberWithTitleEx_t (_hmap, _parm, _maptype, _accesstype, _current, _addflag, _title.buffer())

    scnGetMapNumberWithTitle_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetMapNumberWithTitle', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
    def scnGetMapNumberWithTitle(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _maptype: int, _accesstype: int, _current: int, _title: ctypes.c_char_p) -> int:
        return scnGetMapNumberWithTitle_t (_hmap, _parm, _maptype, _accesstype, _current, _title)


# Функция создания диалога обработки сообщения
# hWnd     -  идентификатор окна
# message  -  строка, содержащая текст сообщения для размещения в окне диалога
# title    -  заголовок диалога
# flag     -  тип сообщения (MB_OK, MB_YESNO, MB_YESNOCANCEL)
# percent  -  значение процента выполнения
# second   -  значение оставшегося времени обработки в сек.
# Возвращает идентификатор окна диалога
# Для закрытия диалога нужно вызвать функцию scnCloseMessageBoxProcess
# При ошибке возвращает 0

#   scnOpenMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,,'scnOpenMessageBoxProcess', maptype.HWND, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def scnOpenMessageBoxProcess(_hWnd: maptype.HWND, _message: ctypes.c_char_p, _title: ctypes.c_char_p, _flag: int, _percent: int, _second: int) -> :
#       return scnOpenMessageBoxProcess_t (_hWnd, _message, _title, _flag, _percent, _second)


# Функция обновления содержимого диалога
# hmsgproc - идентификатор окна диалога обработки сообщения
#            (получен как результат выполнения функции CallMessageBoxProcess)
# Если диалог закрыт пользователем, то возвращает 0
# В этом случае нужно вызвать scnCloseMessageBoxProcess

    scnUpdateMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnUpdateMessageBoxProcess', ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
    def scnUpdateMessageBoxProcess(_hmsgproc: ctypes.c_void_p, _percent: int, _second: int) -> int:
        return scnUpdateMessageBoxProcess_t (_hmsgproc, _percent, _second)


# Функция закрытия диалога
# hmsgproc - идентификатор окна диалога обработки сообщения
#            (получен как результат выполнения функции CallMessageBoxProcess)
# Возвращает код нажатой кнопки - IDYES, IDNO, IDCANCEL.

    scnCloseMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnCloseMessageBoxProcess', ctypes.c_void_p)
    def scnCloseMessageBoxProcess(_hmsgproc: ctypes.c_void_p) -> int:
        return scnCloseMessageBoxProcess_t (_hmsgproc)


# Функция выбора кода семантики из классификатора для просмотра
# hmap       - идентификатор открытой векторной карты
# parm       - параметры задачи
# sitenumber - номер пользовательской карты в цепочке от 1 до числа карт
# code       - код семантики для просмотра
# Возвращает код назначенной семантики и номер пользовательской карты (sitenumber).

#    scnChangeCodeSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnChangeCodeSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
#    def scnChangeCodeSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sitenumber: ctypes.POINTER(ctypes.c_int), _code: int) -> int:
#        return scnChangeCodeSemantic_t (_hmap, _parm, _sitenumber, _code)


# Функция редактирования семантики
# hmap       - идентификатор открытой векторной карты
# parm       - параметры задачи
# info       - идентификатор редактируемого объекта
# ident      - для режима Редактора "Создание объекта" ident = 0,
# иначе ident = 1
# При ошибке возвращает ноль

    semMakeSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'semMakeSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_int)
    def semMakeSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _ident: int) -> int:
        return semMakeSemantic_t (_hmap, _parm, _info, _ident)


# Нанесение объектов по координатам из файла KML
# hmap        - идентификатор главного документа
# parm        - текущие системные параметры
# kmlfile     - полное имя загружаемого файла
# При ошибке возвращает ноль

    tedLoadObjectsFromKML_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedLoadObjectsFromKML', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_char_p)
    def tedLoadObjectsFromKML(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _kmlfile: ctypes.c_char_p) -> int:
        return tedLoadObjectsFromKML_t (_hmap, _parm, _info, _kmlfile)


# Диалог запроса режима объединения наборов объектов
# type   - признак группового объекта, принадлежащего группе groupname
#        - GROUPLEADER -  главный объект набора
#        - GROUPSLAVE  -  подчиненный объект набора
#        - GROUPPARTNER - равноправный объект набора
# isreply     - признак повторяемости семантики GROUPSLAVE (подчинённый объект)
# groupname   - название группы, которой принадлежит выбранный объект
# groupleader - название группы, в которую добавляется объект
# objectname  - имя добавляемого объекта
# Возвращает значения
#        - SET_ONE        - включить отдельный объект с исключением из группы
#        - SET_GROUP      - включить всю группу
#        - SET_HIERARCHY  - сделать иерархию
#        - SET_SUBJECT    - включить отдельный объект
# При ошибке или отказе возвращает 0

    medMessageSetEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'medMessageSetEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def medMessageSetEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _type: int, _isreply: int, _groupname: mapsyst.WTEXT, _groupleader: mapsyst.WTEXT, _objectname: mapsyst.WTEXT) -> int:
        return medMessageSetEx_t (_parm, _type, _isreply, _groupname.buffer(), _groupleader.buffer(), _objectname.buffer())


# Диалог выбора режима преобразования метрики объекта к точечному знаку
# Возвращает 0 - выполнить преобразование по координатам первой точки метрики (по умолчанию)
#            1 - выполнить преобразование по координатам центра объекта
#            2 - cформировать мультиточечный объект
#            3 - вычислить средние координаты точек объекта
#            4 - cформировать ряд точечных объектов

#    scnModeForConverting_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnModeForConverting')
#    def scnModeForConverting() -> int:
#        return scnModeForConverting_t ()


# Диалог выбора режима сшивки объектов
# message - текст сообщения
# local   - локализация объекта
# Возвращает 0 - выполнить сшивку
#            1 - формировать мультиполигон или мультилинию

    scnSetMerge_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetMerge', maptype.PWCHAR)
    def scnSetMerge(_message: mapsyst.WTEXT) -> int:
        return scnSetMerge_t (_message.buffer())

    scnSetMergeEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetMergeEx', maptype.PWCHAR, ctypes.c_int)
    def scnSetMergeEx(_message: mapsyst.WTEXT, _local: int) -> int:
        return scnSetMergeEx_t (_message.buffer(), _local)


# Выбрать открываемый файл DBM и открыть таблицу из базы пространственных данных
# parm       - параметры задачи
# Возвращает ненулевое значение, если карта открыта или добавлена
# При ошибке возвращает ноль

    scnDbmOpen_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnDbmOpen', ctypes.POINTER(maptype.TASKPARMEX))
    def scnDbmOpen(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return scnDbmOpen_t (_parm)


# Настройка параметров подключения к базе пространственных данных, открываемой через файл DBM
# parm - параметры задачи
# dbparams - параметры подключения
# title    - условное имя базы данных в заголовок диалога или 0
# При ошибке возвращает 0

    scnSetDbmConnectDbParam_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetDbmConnectDbParam', ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.TSQLMap_DBConnectParmEx), maptype.PWCHAR)
    def scnSetDbmConnectDbParam(_parm: ctypes.POINTER(maptype.TASKPARMEX), _dbparams: ctypes.POINTER(maptype.TSQLMap_DBConnectParmEx), _title: mapsyst.WTEXT = None) -> int:
        return scnSetDbmConnectDbParam_t (_parm, _dbparams, _title.buffer())


# Диалог просмотра и редактирования параметров представления пространственной БД
# parm - параметры задачи
# dbmname - полное имя файла DBM
# При вызове режима "Сохранить как" в dbmname запишется новое имя файла
# При ошибке возвращает 0

    scnDbmParam_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnDbmParam', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int)
    def scnDbmParam(_parm: ctypes.POINTER(maptype.TASKPARMEX), _dbmname: mapsyst.WTEXT, _size: int) -> int:
        return scnDbmParam_t (_parm, _dbmname.buffer(), _size)


# Вызвать диалог регистрации пользователя на ГИС Сервере
# (ввод имени пользователя и пароля и подключение к ГИС Серверу)
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# При ошибке возвращает ноль

    svGetUserData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svGetUserData', ctypes.POINTER(maptype.TASKPARMEX))
    def svGetUserData(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return svGetUserData_t (_parm)


# Вызвать диалог регистрации пользователя на ГИС Сервере при открытии данных
# (ввод имени пользователя и пароля и подключение к ГИС Серверу)
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# aliasName алиас данных вида "HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты"
# При ошибке возвращает ноль

    svGetUserDataEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svGetUserDataEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p)
    def svGetUserDataEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _aliasName: ctypes.c_char_p) -> int:
        return svGetUserDataEx_t (_parm, _aliasName)


# Вызвать диалог ввода параметров соединения с ГИС Сервером
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# Пользователь выбирает имя хоста (или IP) и номер порта
# При ошибке возвращает ноль

    svGetConnectParameters_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svGetConnectParameters', ctypes.POINTER(maptype.TASKPARMEX))
    def svGetConnectParameters(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return svGetConnectParameters_t (_parm)


# Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# name    - буфер для размещения выбранного алиаса данных
#          (выделять не менее MAXPATH)
# size    - размер выделенного буфера
# Имя выбранного алиаса карты помещается в name
# При ошибке возвращает ноль

    svOpenDataEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svOpenDataEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int)
    def svOpenDataEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int) -> int:
        return svOpenDataEx_t (_parm, _name, _size)


# Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
# для атласа
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# name    - буфер для размещения выбранного алиаса данных
#          (выделять не менее MAXPATH)
# size    - размер выделенного буфера
# Имя выбранного алиаса карты помещается в name
# При ошибке возвращает ноль

    svOpenDataAtlas_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svOpenDataAtlas', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int)
    def svOpenDataAtlas(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int) -> int:
        return svOpenDataAtlas_t (_parm, _name, _size)


# Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
# для атласа
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# hwnd - идентификатор окна атласа для передачи сообщений о открытии данных
# При ошибке возвращает ноль

    svOpenDataAtlasEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svOpenDataAtlasEx', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND)
    def svOpenDataAtlasEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hwnd: maptype.HWND) -> int:
        return svOpenDataAtlasEx_t (_parm, _hwnd)


# Вызвать диалог выбора для уже зарегистрированных пользователей
# доступных данных на ГИС Сервере
# Возможен множественный выбор данных
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# hwnd - идентификатор окна для передачи сообщений
# При выборе данных окну посылается сообщение MT_CHANGEDATAUN
# (0x65D, WPARAM - type : FILE_MAP, FILE_RSW, FILE_MTW...
#         LPARAM - имя выбранного алиаса данных (указатель на двухбайтовую
# строку в кодировке UTF-16)
# При ошибке возвращает ноль

    svGetServerData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svGetServerData', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND)
    def svGetServerData(_parm: ctypes.POINTER(maptype.TASKPARMEX), _handle: maptype.HWND) -> int:
        return svGetServerData_t (_parm, _handle)


# Вызвать диалог выбора для уже зарегистрированных пользователей
# доступных данных определенного типа на ГИС Сервере
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# hwnd - идентификатор окна для передачи сообщений
# При выборе данных окну посылается сообщение MT_CHANGEDATAUN
# (0x65D, WPARAM - type : FILE_MAP, FILE_RSW, FILE_MTW...
#         LPARAM - имя выбранного алиаса данных (указатель на двухбайтовую
# строку в кодировке UTF-16)
# filetype - тип открываемых данных: (1 - карты, 2 - матрицы, 3 - растры,
#                                    -1 - данные всех типов)
# Возможен множественный выбор данных
# При ошибке возвращает ноль

    svGetServerTypeData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svGetServerTypeData', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND, ctypes.c_int)
    def svGetServerTypeData(_parm: ctypes.POINTER(maptype.TASKPARMEX), _handle: maptype.HWND, _filetype: int) -> int:
        return svGetServerTypeData_t (_parm, _handle, _filetype)


# Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# При выборе открываемых данных главному окну посылается сообщение
# AW_OPENDOC (0x655) c именем выбранного алиаса карты (может быть передан
# в mapOpenData).
# При ошибке возвращает ноль

    svOpenData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svOpenData', ctypes.POINTER(maptype.TASKPARMEX))
    def svOpenData(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return svOpenData_t (_parm)


# Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
# для добавления к текущей открытой карте
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# При выборе добавляемых данных вызывается функция mapAppendData(hmap, ...),
# и окну карты посылается уведомление - сообщение MT_CHANGEDATA или MT_CHANGEDATAUN
# (0x65D, WPARAM - type : FILE_MAP, FILE_RSW, FILE_MTW...)
# Идентификатор окна карты запрашивается через посылку главному окну сообщения
# AW_GETCURRENTDOC (0x673, WPARAM - HWND #, LPARAM - HMAP #).
# При ошибке возвращает ноль

    svAppendData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svAppendData', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def svAppendData(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return svAppendData_t (_hmap, _parm)


# Преобразовать строку в хэш по алгоритму MD5
# source - исходная строка ANSI
# target - строка результата (32 символа и замыкающий ноль)
# size   - число байт, зарезервированных в строке (не менее 33)
# При ошибке параметров возвращает ноль

    svStringToHash_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'svStringToHash', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def svStringToHash(_source: ctypes.c_char_p, _target: ctypes.c_char_p, _size: int) -> int:
        return svStringToHash_t (_source, _target, _size)


# Диалог "Открыть атлас карт"
# parm - параметры задачи (поле Handle должно содержать идентификатор главного окна)
# name - буфер для записи имени файла атласа карт, который открывается или создается
# size - размер буфера в байтах
# mode - доступ к режимам диалога
#        0 - полный доступ
#        ALS_NO_CHOICE_ATLAS - режим редактирования выбранного атласа
#                                            (выбор атласа в диалоге отменен)
#        ALS_NO_SEND_MESSAGE - сообщение AW_OPENDOCUN главному окну не посылается
# Если mode = ALS_NO_SEND_MESSAGE, то отсутствует режим Открыть данные.
# Допустимо совместное использование флагов (ALS_NO_CHOICE_ATLAS | ALS_NO_SEND_MESSAGE).
# Название файла справки Arealist.chm (TOPIC: AREALIST).
# При выборе открываемых данных главному окну посылается сообщение
# AW_OPENDOCUN (0x623) c именем выбранной карты (может быть передано в mapOpenDataUn).
# При ошибке возвращает ноль

    scnOpenAtlasUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnOpenAtlasUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def scnOpenAtlasUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: mapsyst.WTEXT, _size: int, _mode: int) -> int:
        return scnOpenAtlasUn_t (_parm, _name.buffer(), _size, _mode)

    tedOpenAtlasUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedOpenAtlasUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def tedOpenAtlasUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: mapsyst.WTEXT, _size: int, _mode: int) -> int:
        return tedOpenAtlasUn_t (_parm, _name.buffer(), _size, _mode)

    tedOpenAtlas_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedOpenAtlas', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int)
    def tedOpenAtlas(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int) -> int:
        return tedOpenAtlas_t (_parm, _name, _size)

    tedOpenAtlasEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedOpenAtlasEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def tedOpenAtlasEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int, _mode: int) -> int:
        return tedOpenAtlasEx_t (_parm, _name, _size, _mode)


# Диалог "Создать атлас карт"
# parm - параметры задачи (поле Handle должно содержать
#        идентификатор главного окна)
# name - буфер для записи имени файла атласа карт
# size - размер буфера в байтах
# mode - доступ к режимам диалога
#        0 - полный доступ
#        ALS_NO_CHOICE_ATLAS - режим редактирования выбранного атласа
#                                            (выбор атласа в диалоге отменен)
#        ALS_NO_SEND_MESSAGE - сообщение AW_OPENDOCUN главному окну не посылается
# Если mode = ALS_NO_SEND_MESSAGE, то отсутствует режим Открыть данные.
# Допустимо совместное использование флагов (ALS_NO_CHOICE_ATLAS | ALS_NO_SEND_MESSAGE).
# Название файла справки Arealist.chm (TOPIC: AREALIST).
# При ошибке возвращает ноль

    scnCreateAtlasUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnCreateAtlasUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def scnCreateAtlasUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: mapsyst.WTEXT, _size: int, _mode: int) -> int:
        return scnCreateAtlasUn_t (_parm, _name.buffer(), _size, _mode)

    scnCreateAtlas_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnCreateAtlas', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def scnCreateAtlas(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int, _mode: int) -> int:
        return scnCreateAtlas_t (_parm, _name, _size, _mode)

    tedCreateAtlas_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedCreateAtlas', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def tedCreateAtlas(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int, _mode: int) -> int:
        return tedCreateAtlas_t (_parm, _name, _size, _mode)


# Диалог "Выбрать карту из списка"
# parm    - параметры задачи (поле Handle должно содержать
#           идентификатор главного окна)
# hmap    - идентификатор открытой карты
# item    - указатель на список элементов атласа, выбранных в текущей точке
# count   - число элементов в списке
# hals    - идентификатор открытого атласа
# Возвращает номер выбранного пользователем элемента
# Если функция возвращает -1, то необходимо вызвать диалог "Открыть атлас карт"
# Название файла справки Mapscena.chm (TOPIC: AREALIST1).
# При ошибке возвращает ноль

    scnAtlasListPro_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnAtlasListPro', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.ALSITEM), ctypes.c_int, maptype.HALS)
    def scnAtlasListPro(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _item: ctypes.POINTER(maptype.ALSITEM), _count: int, _hals: maptype.HALS) -> int:
        return scnAtlasListPro_t (_hmap, _parm, _item, _count, _hals)

    tedAtlasList_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedAtlasList', ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.ALSITEM), ctypes.c_int)
    def tedAtlasList(_parm: ctypes.POINTER(maptype.TASKPARMEX), _item: ctypes.POINTER(maptype.ALSITEM), _count: int) -> int:
        return tedAtlasList_t (_parm, _item, _count)

    tedAtlasListEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'tedAtlasListEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.ALSITEM), ctypes.c_int)
    def tedAtlasListEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _item: ctypes.POINTER(maptype.ALSITEM), _count: int) -> int:
        return tedAtlasListEx_t (_hmap, _parm, _item, _count)


# Открыть диалог построения профиля
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (см.maptype.h)
# profparm - описание параметров построения профиля (см.maptype.h)
# Если шаг по горизонтали в profparm равен нулю, отображается весь профиль
# Указанные шаг по горизонтали и по вертикали могут быть скорректированы
# согласно масштабу и высоте
# В процессе работы диалога в profparm записываются текущие параметры
# При закрытии диалога главному окну посылается сообщение
# AW_CLOSEDIALOGNOTIFY (0x610 - см.maptype.h)
# Возвращает указатель на диалог построения профиля (HBuildProfil)
# Вызов файла справки из Mapscena.chm ("Proflin")
# При ошибке возвращает ноль
# Пример вызова функций построения диалога
# HBUILDPROFIL Hbuildprofil;
# HINSTANCE LibInst;
# HBUILDPROFIL (WINAPI # Openprof)(HMAP hmap, const TASKPARMEX# parm, PROFBUILDPARM # profparm);
# long int (WINAPI # Closeprof)(long int Hbuildprofil);
# long int (WINAPI # SetCurrentValue)(long int HBuildProfil, DOUBLEPOINT # point);
# (FARPROC)Openprof = mapLoadLibrary("gisdlgs.dll",&LibInst,"mclOpenBuildProf");
# (FARPROC)Closeprof = mapGetProcAddress(LibInst,"mclCloseBuildProf");
# (FARPROC)SetCurrentValue = mapGetProcAddress(LibInst,"mclSetCurrentValue");
# Hbuildprofil = (#(Openprof))(hmap,parm,&profparm);
# ....
# (#(SetCurrentValue))(Hbuildprofil,&(profparm.Point));
# ....
# if (Hbuildprofil)  (#(Closeprof))(Hbuildprofil);

    mclOpenBuildProf_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'mclOpenBuildProf', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.PROFBUILDPARM))
    def mclOpenBuildProf(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _profparm: ctypes.POINTER(maptype.PROFBUILDPARM)) -> ctypes.c_void_p:
        return mclOpenBuildProf_t (_hmap, _parm, _profparm)

    mclOpenBuildProfEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'mclOpenBuildProfEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.PROFBUILDPARMEX))
    def mclOpenBuildProfEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _profparm: ctypes.POINTER(maptype.PROFBUILDPARMEX)) -> ctypes.c_void_p:
        return mclOpenBuildProfEx_t (_hmap, _parm, _profparm)


# Закрыть диалог построения профиля
# HBuildProfil - указатель открытого диалога построения профиля

    mclCloseBuildProf_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclCloseBuildProf', ctypes.c_void_p)
    def mclCloseBuildProf(_HBuildProfil: ctypes.c_void_p) -> int:
        return mclCloseBuildProf_t (_HBuildProfil)


# Отобразить профиль в текущей точке
# HBuildProfil - указатель открытого диалога построения профиля
# point - координаты точки в метрах на контуре объекта,
#         по которому построен профиль
# Функция отображает участок профиля, на котором находится данная точка и
# устанавливает в окна диалога вычисленные значения по данной точке.

    mclSetCurrentValue_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclSetCurrentValue', ctypes.c_void_p, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mclSetCurrentValue(_HBuildProfil: ctypes.c_void_p, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mclSetCurrentValue_t (_HBuildProfil, _point)


# Построение зоны видимости по матрице высот в виде растрового изображения
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (см.maptype.h)
# namersw - полное имя растра
# zonevisibility - параметры построения зоны (см.maptype.h)
# Построение производится при наличии открытой матрицы высот
# Результат записывается в файл namersw
# Возвращает номер растра в цепочке
# Вызов файла справки из Mapscena.chm ("ZONVIEW")
# При ошибке возвращает ноль

    mclBuildZoneVisibility_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclBuildZoneVisibility', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY))
    def mclBuildZoneVisibility(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namersw: ctypes.c_char_p, _zonevisibility: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY)) -> int:
        return mclBuildZoneVisibility_t (_hmap, _parm, _namersw, _zonevisibility)

    mclBuildZoneVisibilityUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclBuildZoneVisibilityUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY))
    def mclBuildZoneVisibilityUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namersw: mapsyst.WTEXT, _zonevisibility: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY)) -> int:
        return mclBuildZoneVisibilityUn_t (_hmap, _parm, _namersw.buffer(), _zonevisibility)


# Диалог отображения высоты в точке для всех открытых матриц
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (см.maptype.h)
# point - координаты точки в метрах
# Вызов файла справки из Mapscena.chm ("CAN")
# При ошибке возвращает ноль

    mclShowHeight_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclShowHeight', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mclShowHeight(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mclShowHeight_t (_hmap, _parm, _point)


# Диалог настройки парапметров масштабирования, перемещения и поворота
# #center - указатель на точку привязки, после обработки содержимое может измениться
# #dx,#dy - указатели на значения смещений (м)
# #angle  - указатель на значение угла поворота (град., против часовой стрелки +)
# #scale  - указатель на значение коэффициента масштабирования
# При отказе возвращает 0, 1 - нормальное завершение

    scnSetRotateOptions_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetRotateOptions', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def scnSetRotateOptions(_map: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _center: ctypes.POINTER(maptype.DOUBLEPOINT), _dx: ctypes.POINTER(ctypes.c_double), _dy: ctypes.POINTER(ctypes.c_double), _angle: ctypes.POINTER(ctypes.c_double), _scale: ctypes.POINTER(ctypes.c_double)) -> int:
        return scnSetRotateOptions_t (_map, _parm, _center, _dx, _dy, _angle, _scale)


# currentScale - значение текущего масштаба
# Функция возвращает значение установленного масштаба
# При ошибке возвращает ноль

#    scnChooseScaleEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_double,'scnChooseScaleEx', ctypes.c_double)
#    def scnChooseScaleEx(_currentScale: float) -> float:
#        return scnChooseScaleEx_t (_currentScale)

#    scnChooseScale_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnChooseScale', ctypes.c_int)
#    def scnChooseScale(_currentScale: int) -> int:
#        return scnChooseScale_t (_currentScale)


# mapname  - имя карты
# password - буфер для размещения пароля
# size     - размер буфера в байтах для пароля
# При отказе возвращает 0, 1 - нормальное завершение

    scnGetMapPassword_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetMapPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def scnGetMapPassword(_mapname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        return scnGetMapPassword_t (_mapname.buffer(), _password.buffer(), _size)


# Диалог ввода пароля для распаковки архива
# zipname  - имя файла zip
# password - буфер для размещения пароля
# size     - размер буфера в байтах для пароля
# Возвращает   0 - отказ от ввода
#              1 - формируется пароль

    scnGetUnzipPassword_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnGetUnzipPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def scnGetUnzipPassword(_zipname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        return scnGetUnzipPassword_t (_zipname.buffer(), _password.buffer(), _size)


# Построение зоны
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (см.maptype.h)
# zoneparm - параметры построения зоны
# При ошибке возвращает ноль

#    mclPutRadiusZoneObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclPutRadiusZoneObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(BUILDZONEPARMEX))
#    def mclPutRadiusZoneObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _zoneparm: ctypes.POINTER(BUILDZONEPARMEX)) -> int:
#        return mclPutRadiusZoneObject_t (_hmap, _parm, _zoneparm)


# Справка об объекте местности
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (см.maptype.h)
# info - выбранный объект
# При ошибке возвращает ноль
# Открыть диалог "Справка об объекте"

#    mclCreateStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'mclCreateStatisticObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ)
#    def mclCreateStatisticObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ) -> ctypes.c_void_p:
#        return mclCreateStatisticObject_t (_hmap, _parm, _info)


# Закрыть диалог "Справка об объекте"

#    mclCloseStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclCloseStatisticObject', ctypes.c_void_p)
#    def mclCloseStatisticObject(_hstat: ctypes.c_void_p) -> int:
#        return mclCloseStatisticObject_t (_hstat)


# Обновление диалога "Справка об объекте"

#    mclChangeStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'mclChangeStatisticObject', ctypes.c_void_p, maptype.HOBJ)
#    def mclChangeStatisticObject(_hstat: ctypes.c_void_p, _info: maptype.HOBJ) -> int:
#        return mclChangeStatisticObject_t (_hstat, _info)


# Диалог Вопрос-Ответ
# Диалог имеет заголовок, в центре сам вопрос, под ним название документа и кнопки до 6 шт.
# title     - строка, содержащая заголовок
# question  - содержимое вопроса
# docname   - название документа
# button1   - название 1-ой кнопки
# button2   - название 2-ой кнопки
# button3   - название 3-ой кнопки
# button4   - название 4-ой кнопки
# button5   - название 5-ой кнопки
# button6   - название 6-ой кнопки
# Если в качестве указателя на название кнопки передается NULL, то
# кнопка на форме не отображается
#
# При ошибке возвращает ноль
# Возвращает   1 - нажата 1-я кнопка
#              2 - нажата 2-я кнопка
#              3 - нажата 3-я кнопка
#              4 - нажата 4-я кнопка
#              5 - нажата 5-я кнопка
#              6 - нажата 6-я кнопка

    scnQuestion_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnQuestion', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def scnQuestion(_title: mapsyst.WTEXT, _question: mapsyst.WTEXT, _docname: mapsyst.WTEXT, _button1: mapsyst.WTEXT, _button2: mapsyst.WTEXT, _button3: mapsyst.WTEXT, _button4: mapsyst.WTEXT, _button5: mapsyst.WTEXT, _button6: mapsyst.WTEXT) -> int:
        return scnQuestion_t (_title.buffer(), _question.buffer(), _docname.buffer(), _button1.buffer(), _button2.buffer(), _button3.buffer(), _button4.buffer(), _button5.buffer(), _button6.buffer())


# Настройка параметров копирования объектов на другую карту
# handle  - идентификатор окна родителя
# map     - объект доступа к карте
# options - параметры копирования
# При ошибке возвращает ноль

    scnSetCopyOptionsEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnSetCopyOptionsEx', maptype.HWND, maptype.HMAP, ctypes.POINTER(COPY_OPTIONS))
    def scnSetCopyOptionsEx(_handle: maptype.HWND, _hmap: maptype.HMAP, _options: ctypes.POINTER(COPY_OPTIONS)) -> int:
        return scnSetCopyOptionsEx_t (_handle, _hmap, _options)


# Открыть диалог просмотра журнала сообщений
# Журнал сообщений формируют задачи: Контроль качества векторной карты,
# Контроль согласования объектов смежных листов, Контроль абсолютных высот,
# Объединение данных и другие. Запись информации в журнал сообщений
# выполняет функция vecWriteDocErrorUn (vecexapi.h)
# hmap - идентификатор открытой векторной карты
# parm - описание параметров задачи (maptype.h)
# Возвращает идентификатор диалога просмотра журнала сообщений
# При ошибке возвращает ноль

#    scnCreateViewMessageLog_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'scnCreateViewMessageLog', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
#    def scnCreateViewMessageLog(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> ctypes.c_void_p:
#        return scnCreateViewMessageLog_t (_hmap, _parm)


# Закрыть диалог просмотра журнала сообщений
# hviewmes - идентификатор открытого диалога просмотра журнала сообщений
# При ошибке возвращает ноль

#    scnCloseViewMessageLog_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnCloseViewMessageLog', ctypes.c_void_p)
#    def scnCloseViewMessageLog(_hviewmes: ctypes.c_void_p) -> int:
#        return scnCloseViewMessageLog_t (_hviewmes)


# Обновить диалог просмотра журнала сообщений
# hviewmes - идентификатор открытого диалога просмотра журнала сообщений
# При ошибке возвращает ноль

#    scnUpdateViewMessageLog_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnUpdateViewMessageLog', ctypes.c_void_p)
#    def scnUpdateViewMessageLog(_hviewmes: ctypes.c_void_p) -> int:
#        return scnUpdateViewMessageLog_t (_hviewmes)


# Открыть журнал всплывающих сообщений приложения
# При ошибке возвращает ноль

#    scnLogTextDialog_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnLogTextDialog', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.RECT), ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
#    def scnLogTextDialog(_hMap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _position: ctypes.POINTER(maptype.RECT), _log_list: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _type_message: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
#        return scnLogTextDialog_t (_hMap, _parm, _position, _log_list, _type_message, _count)


# Открыть диалог запуска приложений
# parm - описание параметров задачи (maptype.h)
# path - буфер для записи строки, содержащей полный путь к запускаемой задаче
# pathsize - размер строки в байтах
# comment  - буфер для записи строки, содержащей комментарий к задаче
# commentsize - размер строки в байтах
# При выборе задачи (библиотеки) возвращает 1, при ошибке возвращает ноль

    scnRunningApplication_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_int,'scnRunningApplication', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def scnRunningApplication(_parm: ctypes.POINTER(maptype.TASKPARMEX), _taskpath: mapsyst.WTEXT, _pathsize: int, _comment: mapsyst.WTEXT, _commentsize: int) -> int:
        return scnRunningApplication_t (_parm, _taskpath.buffer(), _pathsize, _comment.buffer(), _commentsize)

except Exception as e:
    print(e)
    dlgslib = 0