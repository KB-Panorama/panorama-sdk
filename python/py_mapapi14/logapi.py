#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary( gisaccesname )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К ЖУРНАЛУ ТРАНЗАКЦИЙ +++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Запросить - ведется ли журнал транзакций
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# 0 - не ведется, иначе - ведется

    mapGetLogAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLogAccess', maptype.HMAP, maptype.HSITE)
    def mapGetLogAccess(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetLogAccess_t (_hMap, _hSite)


# Запретить/Разрешить ведение журнала транзакций (0/1)
# После открытия карты ведение журнала разрешено.
# Допускается использовать только при потоковой обработке
# объектов, когда быстродействие важнее возможности
# сохранить данные при сбое системы !
# Перед отключением журнала рекомендуется позаботиться о
# резервной копии данных !
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapLogAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogAccess', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapLogAccess(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mode: int) -> int:
        return mapLogAccess_t (_hMap, _hSite, _mode)


# Запросить число транзакций в журнале
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapLogCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCount', maptype.HMAP, maptype.HSITE)
    def mapLogCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogCount_t (_hMap, _hSite)


# Запросить дату создания журнала
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# date - дата в формате "YYYYMMDD"
# time - время в формате "число секунд от 00:00:00"
# на указанную дату
# При ошибке возвращает ноль

    mapLogDate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogDate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapLogDate(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _date: ctypes.POINTER(ctypes.c_int), _time: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapLogDate_t (_hMap, _hSite, _date, _time)


# Открыть запись транзакции
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# type - тип транзакции (от 0x= 4000 до 0х0FFFF - за Панорамой)
# При ошибке возвращает ноль

    mapLogCreateAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCreateAction', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapLogCreateAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _type: int) -> int:
        return mapLogCreateAction_t (_hMap, _hSite, _type)

    mapLogCreateActionObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCreateActionObject', maptype.HOBJ, ctypes.c_int)
    def mapLogCreateActionObject(_info: maptype.HOBJ, _type: int) -> int:
        return mapLogCreateActionObject_t (_info, _type)


# Внести в описание транзакции сведения об операции
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Структура ACTIONRECORD описана в maptype.h
# При ошибке возвращает ноль

    mapLogPutRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogPutRecord', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONRECORD))
    def mapLogPutRecord(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _record: ctypes.POINTER(maptype.ACTIONRECORD)) -> int:
        return mapLogPutRecord_t (_hMap, _hSite, _record)


# Закрыть запись транзакции
# hMap   - идентификатор открытой карты
# hSite  - идентификатор открытой пользовательской карты
# number - поле для записи номера выполненной транзакции в журнале транзакций
# Возвращает число выполненных операций в транзакции для карты
# Если число транзакций не может быть определено возвращает -1
# При ошибке возвращает ноль

    mapLogCommitActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCommitActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_int))
    def mapLogCommitActionEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapLogCommitActionEx_t (_hMap, _hSite, _number)

    mapLogCommitAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCommitAction', maptype.HMAP, maptype.HSITE)
    def mapLogCommitAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogCommitAction_t (_hMap, _hSite)

    mapLogCommitActionObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogCommitActionObject', maptype.HOBJ)
    def mapLogCommitActionObject(_info: maptype.HOBJ) -> int:
        return mapLogCommitActionObject_t (_info)


# Запросить номер первой транзакции,выполненной
# после указанных даты и времени
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# date - дата в формате "YYYYMMDD"
# time - время в формате "число секунд от 00:00:00"
# на указанную дату (по Гринвичу - GetSystemTime, in Coordinated Universal Time (UTC))
# При ошибке возвращает ноль

    mapLogGetActionNumberByTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetActionNumberByTime', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapLogGetActionNumberByTime(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _date: int, _time: int) -> int:
        return mapLogGetActionNumberByTime_t (_hMap, _hSite, _date, _time)


# Считать заголовок описания последней не отмененной транзакции
# задачи из журнала
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Структура ACTIONRECORD описана в maptype.h
# При ошибке возвращает ноль,
# иначе - номер транзакции

    mapReadLastAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadLastAction', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONHEAD))
    def mapReadLastAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _head: ctypes.POINTER(maptype.ACTIONHEAD)) -> int:
        return mapReadLastAction_t (_hMap, _hSite, _head)


# Считать заголовок описания последней не отмененной транзакции
# задачи из журнала
# flag - условия выбора последней транзакции:
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - считывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Структура ACTIONRECORD описана в maptype.h
# При ошибке возвращает ноль,
# иначе - номер транзакции

    mapReadLastActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadLastActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONHEAD), ctypes.c_int)
    def mapReadLastActionEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _head: ctypes.POINTER(maptype.ACTIONHEAD), _flag: int) -> int:
        return mapReadLastActionEx_t (_hMap, _hSite, _head, _flag)


# Считать заголовок описания последней транзакции "Шаг назад" и
# запросить номер отмененной транзакции (подготовка команды "Восстановить")
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# head  - адрес поля для записи заголовка транзакции "Шаг назад"
# Структура ACTIONRECORD описана в maptype.h
# actionnumber - адрес поля для записи номера отмененной транзакции,
# flag         - условия выбора последней транзакции "Шаг назад":
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - считывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# При ошибке возвращает ноль, иначе - номер транзакции

    mapReadLastUndoActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadLastUndoActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONHEAD), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapReadLastUndoActionEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _head: ctypes.POINTER(maptype.ACTIONHEAD), _actionnumber: ctypes.POINTER(ctypes.c_int), _flag: int) -> int:
        return mapReadLastUndoActionEx_t (_hMap, _hSite, _head, _actionnumber, _flag)


# Считать заголовок описания транзакции из журнала
# number - последовательный номер транзакции
# (от 1 до Count(...)).
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Структура ACTIONRECORD описана в maptype.h
# При ошибке возвращает ноль,
# иначе - число операций в транзакции

    mapLogReadAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogReadAction', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.ACTIONHEAD))
    def mapLogReadAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _head: ctypes.POINTER(maptype.ACTIONHEAD)) -> int:
        return mapLogReadAction_t (_hMap, _hSite, _number, _head)


# Запросить сведения об операции
# number - последовательный номер транзакции (от 1)
# recnumber - номер операции (от 1 до ReadAction(...))
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Структура ACTIONRECORD описана в maptype.h
# При ошибке возвращает ноль

    mapLogGetActionRecordEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetActionRecordEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.ACTIONRECORD))
    def mapLogGetActionRecordEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _recnumber: int, _record: ctypes.POINTER(maptype.ACTIONRECORD)) -> int:
        return mapLogGetActionRecordEx_t (_hMap, _hSite, _number, _recnumber, _record)

    mapLogGetActionRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetActionRecord', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.ACTIONRECORD))
    def mapLogGetActionRecord(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _recnumber: int, _record: ctypes.POINTER(maptype.ACTIONRECORD)) -> int:
        return mapLogGetActionRecord_t (_hMap, _hSite, _recnumber, _record)


# Запросить количество операций в транзакции
# hMap   - идентификатор открытой карты
# hSite  - идентификатор открытой пользовательской карты
# number - номер транзакции
# При ошибке возвращает ноль

    mapLogGetActionRecordCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetActionRecordCountEx', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapLogGetActionRecordCountEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int) -> int:
        return mapLogGetActionRecordCountEx_t (_hMap, _hSite, _number)

    mapLogGetActionRecordCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetActionRecordCount', maptype.HMAP, maptype.HSITE)
    def mapLogGetActionRecordCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogGetActionRecordCount_t (_hMap, _hSite)


# Запросить доступен ли журнал на запись
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapLogIsWrite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogIsWrite', maptype.HMAP, maptype.HSITE)
    def mapLogIsWrite(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogIsWrite_t (_hMap, _hSite)


# Отменить последнюю транзакцию
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# При ошибке возвращает ноль,
# иначе - количество восстановленных операций

    mapLogAbolitionLastAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogAbolitionLastAction', maptype.HMAP, maptype.HSITE)
    def mapLogAbolitionLastAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogAbolitionLastAction_t (_hMap, _hSite)


# Восстановить последнюю отмененную транзакцию
# flag - условия выбора последней транзакции:
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - считывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# Если после отмены транзакции выполнялись другие операции или
# выполнялась сортировка карты или журнал пуст - возвращает ноль
# При ошибке возвращает ноль,
# иначе - количество восстановленных операций

    mapLogRedoLastAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogRedoLastAction', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapLogRedoLastAction(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapLogRedoLastAction_t (_hMap, _hSite, _flag)


# Отменить последнюю транзакцию
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag - условия выбора последней транзакции:
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - обрабатывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# При ошибке возвращает ноль,
# иначе - количество восстановленных операций

    mapLogAbolitionLastActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogAbolitionLastActionEx', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapLogAbolitionLastActionEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapLogAbolitionLastActionEx_t (_hMap, _hSite, _flag)


# Отменить последнюю транзакцию в документе
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# hMap  - идентификатор открытой карты
# hSite - поле для записи идентификатора карты, на которой выполнена
#         отмена транзакции
# flag - условия выбора последней транзакции:
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - обрабатывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# При ошибке возвращает ноль,
# иначе - количество восстановленных операций

    mapLogUndoAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogUndoAction', maptype.HMAP, ctypes.POINTER(maptype.HSITE), ctypes.c_int)
    def mapLogUndoAction(_hMap: maptype.HMAP, _hSite: ctypes.POINTER(maptype.HSITE), _flag: int) -> int:
        return mapLogUndoAction_t (_hMap, _hSite, _flag)


# Прочитать последнюю транзакцию в документе,которую можно отменить
# Если после транзакции выполнялась сортировка карты
# или журнал пуст - возвращает ноль
# hMap  - идентификатор открытой карты
# hSite  - поле для записи идентификатора карты, на которой выполнена
#          отмена транзакции
# flag - условия выбора последней транзакции:
# LOG_ANYACTION(0) - нет условий, LOG_MYACTION(1) - обрабатывать последнюю
# свою транзакцию (пропускать транзакции других пользователей)
# При ошибке возвращает ноль, иначе - номер транзакции

    mapLogReadActionForUndo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogReadActionForUndo', maptype.HMAP, ctypes.POINTER(maptype.HSITE), ctypes.c_int)
    def mapLogReadActionForUndo(_hMap: maptype.HMAP, _hSite: ctypes.POINTER(maptype.HSITE), _flag: int) -> int:
        return mapLogReadActionForUndo_t (_hMap, _hSite, _flag)


# Сохранить журнал транзакций (и переоткрыть файл)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты

    mapLogFlush_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapLogFlush', maptype.HMAP, maptype.HSITE)
    def mapLogFlush(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> ctypes.c_void_p:
        return mapLogFlush_t (_hMap, _hSite)


# Запросить идентификатор текущего компьютера
# Записывается в поле Task структуры ACTIONHEAD
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapLogGetMyIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapLogGetMyIdent', maptype.HMAP, maptype.HSITE)
    def mapLogGetMyIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapLogGetMyIdent_t (_hMap, _hSite)


# Установить монопольный доступ ко всем открываемым векторным картам
# Ускоряет все операции редактирования карт за счет буферизации
# операций записи на диск при значении access не равном 0
# При монопольном доступе другие приложения не смогут
# редактировать карту
# Если какая-либо карта не может быть открыта в монопольном
# доступе - признак автоматически сбрасывается
# Возвращает новое значение признака монопольного доступа

    mapSetExclusiveAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetExclusiveAccess', ctypes.c_int)
    def mapSetExclusiveAccess(_access: int) -> int:
        return mapSetExclusiveAccess_t (_access)


# Запросить значение признака монопольного доступа к открываемым векторным картам

#   mapGetExclusiveAccess_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'mapGetExclusiveAccess', )
#   def mapGetExclusiveAccess(_void) -> int:
#       return mapGetExclusiveAccess_t (_void)


# Запросить список транзакций для заданной карты, начиная с указанного номера
# hMap   -  идентификатор открытых данных
# hSite  -  идентификатор открытой пользовательской карты
# number -  номер транзакции, с которой начинается выдача
# limit  -  предельное число выдаваемых записей или 0 (не ограничивать)
# error  -  поле для записи кода ошибки, возникшей при запросе списка операций
# outype -  формат вывода OST_GML/OST_JSON
# Возвращает идентификатор списка записей в памяти в формате XML
# <?xml version=\"1.0\" encoding=\"UTF-8\" ?>
# <actionlist fromnumber="37591" date="27/05/2019" time="12:45:08">
#  <action number="37591" kind="4009" user="user1">
#   <item type="edit" object="1234567" data="true" sheet="2"/>
#   <item type="edit" object="1237890" data="true" semn="true"/>
#  </action>
#  <action number="37594" kind="4001" user="user1">
#   <item type="create" object="2345678" data="true" semn="true"/>
#  </action>
#  <action number="37599" kind="4003" user="user2">
#   <item type="delete" object="2345678"/>
#  </action>
# </actionlist>
# Для чтения списка необходимо вызвать функцию mapGetActionListPoint, после чтения
# списка необходимо освободить память функцией mapFreeActionList
# При ошибке возвращает ноль

    mapGetActionList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetActionList', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mapGetActionList(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _limit: int, _error: ctypes.POINTER(ctypes.c_int)) -> ctypes.c_void_p:
        return mapGetActionList_t (_hMap, _hSite, _number, _limit, _error)

    mapGetActionListEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetActionListEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapGetActionListEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _limit: int, _error: ctypes.POINTER(ctypes.c_int), _outype: int) -> ctypes.c_void_p:
        return mapGetActionListEx_t (_hMap, _hSite, _number, _limit, _error, _outype)


# Удалить список транзакций в памяти

    mapFreeActionList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeActionList', ctypes.c_void_p)
    def mapFreeActionList(_actionlist: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeActionList_t (_actionlist)

except Exception as e:
    print(e)
    acceslib = 0

TAC_MED_CREATEOBJECT = 4001         #  Создание объекта
TAC_MED_UNDO         = 4002         #  Отмена
TAC_MED_DELETEOBJECT = 4003         #  Удаление объекта
TAC_MED_PASTE        = 4004         #  Сшивка объектов
TAC_MED_MOVEKNOT     = 4005         #  Перемещение узлов
TAC_MED_MOVEPART     = 4006         #  Перемещение участка объекта
TAC_MED_EDITPART     = 4007         #  Редактирование участка объекта
TAC_MED_LINECUT      = 4008         #  Рассечение линейного объекта
TAC_MED_ADJUST       = 4009         #  Согласование объектов
TAC_MED_SPLINE       = 4010         #  Сглаживание объектов
TAC_MED_FILTER       = 4011         #  Фильтрация объектов
TAC_MED_REVERT       = 4012         #  Изменение направления
TAC_MED_CUT          = 4013         #  Разрезание объекта
TAC_MED_POLYTITLE    = 4014         #  Сборка сложной подписи
TAC_MED_SEMAPPEND    = 4015         #  Добавление семантики
TAC_MED_SEMUPDATE    = 4016         #  Обновление семантики
TAC_MED_SEMDELETE    = 4017         #  Удаление семантики
TAC_MED_ROTATE       = 4018         #  Вращение объекта
TAC_MED_MOVE         = 4019         #  Перемещение объекта
TAC_MED_MODIFY       = 4020         #  Изменение кода объекта
TAC_MED_HIGHT        = 4021         #  Редактирование высоты
TAC_MED_TITLE        = 4022         #  Редактирование текста
TAC_MED_BOTTOP       = 4023         #  Изменение границ видимости
TAC_MED_MOVEROTATE   = 4024         #  Масштабирование и поворот объектов

TAC_MED_SCENARIO     = 4025         #  Создание сценария
TAC_MED_SCENEOBJECT  = 4026         #  Создание/обновление объекта по сценарию
TAC_MED_DRAWEDIT     = 4027         #  Редактирование графики объекта    
TAC_MED_COPYSEEK     = 4028         #  Копирование(перемещение) на другую карту 

TAC_MED_DELONESUB    = 4029         #  Удаление одного подобъекта              
TAC_MED_DELALLSUB    = 4030         #  Удаление всех подобъектов               
TAC_MED_SEEKDELALSUB = 4031         #  Удаление всех подобъектов у выделенных объектов
TAC_MED_DELSEEK      = 4032         #  Удаление выделенных объектов                   
TAC_MED_SMOVE        = 4033         #  Быстрое редактирование и удаление объектов     
TAC_MED_POINTGROUP   = 4034         #  Редактирование общих точек смежных объектов    
TAC_MED_DELETEPOINT  = 4035         #  Удаление точек                                 
TAC_MED_ADDPOINT     = 4036         #  Добавление точек                               
TAC_MED_LOCKOBJ      = 4037         #  Замыкание объекта                              

TAC_MED_RECTANGLE    = 4039         #  Приведение объектов к прямоугольному виду 
TAC_MED_SETBEGIN     = 4040         #  Установить первую точку метрики           
TAC_MED_CHANGESEMCODE = 4041        #  Изменение кода семантики                  
TAC_MED_LISTSEM      = 4042         #  Редактирование семантики списком          
TAC_MED_CALCVALUE    = 4043         #  Расчёты по семантике                      
TAC_MED_CALCSTRING   = 4044         #  Сборка символьной семантики               
TAC_MED_SET_COLOR    = 4045         #  Изменить цвет                             
TAC_MED_SET_SCALE    = 4046         #  Масштабирование объекта                   
TAC_MED_COPYHIGHT    = 4047         #  Копия значения абсолютной высоты          
TAC_MED_DELETEHIGHT  = 4048         #  Удаление высоты                           
TAC_MED_COPYPART     = 4049         #  Копия участка объекта                     
TAC_MED_COPYSUB      = 4050         #  Создание подобъекта                       
TAC_MED_SEEKSUBJECT  = 4051         #  Создание подобъектов  по выделенным объектам   
TAC_MED_CROSSPOINT   = 4052         #  Создание точек пересечения выбранных объектов  
TAC_MED_ADJUSPOINT   = 4053         #  Согласование двух точек двух объектов          
TAC_MED_ADJUSOBJECT  = 4054         #  Согласование концов (сводка) линейных объектов 
TAC_MED_ADJLINEFRAME = 4055         #  Сводка объектов по рамке                       
TAC_MED_KNOT         = 4056         #  Формирование узла                              
TAC_MED_ADJSHORTPOINT = 4057        #  Согласование точек                             
TAC_MED_CUTSET       = 4058         #  Вырезание списков                              
TAC_MED_ADJSET       = 4059         #  Согласование списков                           
TAC_MED_TOTALFILTR   = 4060         #  Согласованная фильтрация объекта               
TAC_MED_LINEPOINTCUT = 4061         #  Рассечение в точке                             
TAC_MED_SQUARECUT    = 4062         #  Рассечение площадного объекта объектом
TAC_MED_BUILDING     = 4063         #  Составление кварталов                          
TAC_MED_SEEKLINECUT  = 4064         #  Рассечение линейных объектов                   
TAC_MED_EXCAVAT      = 4065         #  Насыпь (пропорционально)                     
TAC_MED_EMBANKMENT   = 4066         #  Насыпь (перпендикулярно)                     
TAC_MED_PLATFORM     = 4067         #  Создание объекта типа ЭСТАКАДА               
TAC_MED_STAIRS       = 4068         #  Оформление объекта типа ЛЕСТНИЦА             
TAC_MED_ZIGZAG       = 4069         #  Создание зигзагообразного объекта            
TAC_MED_CREATECOPY   = 4070         #  Создание по типу                             
TAC_MED_CREATESUB    = 4071         #  Создание подобъекта                          
TAC_MED_COPY         = 4072         #  Копия объекта                                
TAC_MED_CHOICEMAP    = 4073         #  Копия на другую карту                        
TAC_MED_SAVEOBJECT   = 4074         #  Создание по условному                        
TAC_MED_SIT_LINE     = 4075         #  Нанесение линии                              
TAC_MED_SIT_SQUARE   = 4076         #  Нанесение полигона                           
TAC_MED_SIT_POINT    = 4077         #  Нанесение растрового знака                   
TAC_MED_SIT_TEXT     = 4078         #  Нанесение подписи            
TAC_MED_CRMODE0      = 4079         #  Комбинированный метод        
TAC_MED_LABELLINEFROMSEM = 4080     #  Подпись линии по семантике                     
TAC_MED_LABELFROMSEM1    = 4081     #  Подпись объекта по семантике(произвольный контур)
TAC_MED_LABELFROMSEM2    = 4082     #  Подпись объекта по семантике(сглаживающий сплайн)
TAC_MED_LINECONTINUE = 4083         #  Продолжение линии                                
TAC_MED_PARTMOVE     = 4084         #  Перемещение участка               
TAC_MED_TITLEMOVE    = 4085         #  Редактирование составной подписи  
TAC_MED_RESTORESEEK  = 4086         #  Восстановление удаленных          
TAC_MED_SEEKCODE     = 4087         #  Перекодировка выделенных          
TAC_MED_SEEKCROSS    = 4088         #  Пересечение выделенных            
TAC_MED_SEEKSPLINE   = 4089         #  Сглаживание выделенных            
TAC_MED_SEEKFILTER   = 4090         #  Фильтрация выделенных             

TAC_MED_SHAB         = 4092         #  Нанесение из макета                  
TAC_MED_SEEKHIGHTADD = 4093         #  Обновление высоты объекта из матрицы 
TAC_MED_HIGHTADD     = 4094         #  Добавление высот                     
TAC_MED_STAFFCREATE  = 4095         #  Нанесение КП                         
TAC_MED_BERGLINE     = 4096         #  Бергштрих в точке                    
TAC_MED_DOUBLEBERGLINE = 4097       #  Парные бергштрихи                    
TAC_MED_ADDOBJECTDRAW  = 4098       #  Копия графики                        
TAC_MED_POSUPDATE      = 4099       #  Изменить порядок отображения объекта в цепочке
TAC_MED_OUTBORDER      = 4100       #  Общая граница                       
TAC_MED_EDITLINE       = 4101       #  Редактирование линии
TAC_MED_GENSPLINE      = 4102       #  Согласованное сглаживание         
TAC_MED_ROTATESELECTED = 4199       #  Привязка выделенных объектов      
TAC_MED_UPDATEOBJECT   = 4200       #  Обновление объекта
TAC_MED_AZIMUTHCIRCLE  = 4201       #  Азимутальный круг
TAC_MED_EXPAND         = 4202       #  Расширяющаяся зона
TAC_MED_COPYMETRIC     = 4203       #  Копирование метрики
TAC_MED_DELETE4D       = 4204       #  Удаление 4D
