#!/usr/bin/env python3

import os
import mapsyst
import ctypes
import maptype
import mapgdi


try:
    if os.environ['gisrsctoolsdll']:
        gisrsctoolsname = os.environ['gisrsctoolsdll']
except KeyError:
    gisrsctoolsname = 'gis64rsctools.dll'

try:
    rsctoolslib = mapsyst.LoadLibrary( gisrsctoolsname )


# Ввод значения
# Открыть диалог "Выбор объекта"
#  hmap  - идентификатор открытых данных
#  parm  - параметры задачи
#  info  - идентификатор объекта карты
#  flag  - флаг режима работы диалога:
#          0 - ввод семантики при создании или редактировании объекта включена
#              опция "Вся семантика", активны только кнопки "Сохранить" и "Помощь".
#              Сохранение объекта mapCommitObject(...) не выполняется
#              в данном режиме;
#          1 - просмотр, редактирование и выбор объекта карты,
#              заполняется список объектов в данной точке;
#         -1 - режим поиска и выделения объекта
#
# Основные закладки "Семантика", "Метрика", "Масштаб". Для объекта:
# - вид которого определен в классификаторе, добавляется закладка "Вид";
# - имеющего 3D-вид, добавляется закладка "3D";
# - входящего в группу объектов, добавляется закладка "Набор объектов";
# - имеющего графический вид, добавляется закладка "Графика".
# Активность и действия при нажатии кнопки "Сохранить" на всех закладках
# диалога синхронизированы. Кнопка "Сохранить" становится активной
# при изменении любого параметра, либо при создании объекта.
# При закрытии диалога:
# - форма освобождается вне зависимости от возвращаемого значения;
# - единицы измерения площади и длины записываются в INI-файл документа.
#
# Возвращаемые значения в выбранном режиме работы диалога:
# 1) создание объекта (flag = 0):
#          1 - при нажатии кнопки "Сохранить";
#          0 - закрытие диалога (отказ от сохранения);
# 2) выбор объекта (flag = 1):
#         -1 - при нажатии кнопки "Выбор объекта на карте";
#          1 - при нажатии кнопки "Сохранить";
#          0 - закрытие диалога (отказ от сохранения и выбора);
# 3) поиск объекта (flag = -1):
#         -1 - при выборе режима "Выбор объекта на карте"
#          0 - закрытие диалога (отказ от выбора)
# При ошибке возвращает 0

    rscShowStatisticObject_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscShowStatisticObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_int)
    def rscShowStatisticObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _flag: int) -> int:
        return rscShowStatisticObject_t (_hmap, _parm, _info, _flag)


# Открыть диалог "Выбор объекта"
#  hmap  - идентификатор открытых данных
#  parm  - параметры задачи
#  info  - идентификатор объекта карты
#  flag  - флаг режима работы диалога:
#          0 - ввод семантики при создании объекта,
#              включена опция "Вся семантика",
#              активны только кнопки "Сохранить" и "Помощь";
#          1 - просмотр, редактирование и выбор объекта карты,
#              заполняется список объектов в данной точке;
#         -1 - режим поиска и выделения объекта
#  active_page - флаг установки активной закладки:
#          0 - семантика; 1 - метрика; 2 - набор; 3 - масштаб;
#          4 - вид; 5 - графика; 6 - 3D;
#         -1 - устанавливается из ini-файла приложения.
#          При создании объекта (flag = 0) устанавливаетсяв закладка "Семантика";
#          при отсутствии точек метрики - "Метрика".
#
# Основные закладки "Семантика", "Метрика", "Масштаб". Для объекта:
# - вид которого определен в классификаторе, добавляется закладка "Вид";
# - имеющего 3D-вид, добавляется закладка "3D";
# - входящего в группу объектов, добавляется закладка "Набор объектов";
# - имеющего графический вид, добавляется закладка "Графика".
# Активность и действия при нажатии кнопки "Сохранить" на всех закладках
# диалога синхронизированы. Кнопка "Сохранить" становится активной
# при изменении любого параметра, либо при создании объекта.
# При закрытии диалога:
# - форма освобождается вне зависимости от возвращаемого значения;
# - единицы измерения площади и длины записываются в INI-файл документа.
#
# Возвращаемые значения в выбранном режиме работы диалога:
# 1) создание объекта (flag = 0):
#          1 - при нажатии кнопки "Сохранить";
#          0 - закрытие диалога (отказ от сохранения);
# 2) выбор объекта (flag = 1):
#         -1 - при нажатии кнопки "Выбор объекта на карте";
#          1 - при нажатии кнопки "Сохранить";
#          0 - закрытие диалога (отказ от сохранения и выбора);
# 3) поиск объекта (flag = -1):
#         -1 - при выборе режима "Выбор объекта на карте"
#          0 - закрытие диалога (отказ от выбора)
# При ошибке возвращает 0

    rscShowStatisticObjectEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscShowStatisticObjectEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def rscShowStatisticObjectEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _flag: int, _active_page: int) -> int:
        return rscShowStatisticObjectEx_t (_hmap, _parm, _info, _flag, _active_page)


# Создать диалог "Выбор объекта"
#  hmap  - идентификатор открытых данных
#  parm  - параметры задачи
#  info  - идентификатор объекта карты
#  point - точка курсора на карте (в метрах на местности). Используется для размещения
#          изображения выбранного объекта в диалоге (соответствует центру окна с объектом).
#          Если point = 0, то выбирается первая точка метрики объекта,
#          (исключение - для линейного объекта выбирается центральная точка).
#  flag  - флаг режима работы диалога:
#          0 - ввод семантики при создании объекта,
#              включена опция "Вся семантика",
#              активны только кнопки "Сохранить" и "Помощь";
#          1 - просмотр, редактирование и выбор объекта карты,
#              заполняется список объектов в данной точке;
#         -1 - режим поиска и выделения объекта
#
# Основные закладки "Семантика", "Метрика", "Масштаб". Для объекта:
# - вид которого определен в классификаторе, добавляется закладка "Вид";
# - имеющего 3D-вид, добавляется закладка "3D";
# - входящего в группу объектов, добавляется закладка "Набор объектов";
# - имеющего графический вид, добавляется закладка "Графика".
# Активность и действия при нажатии кнопки "Сохранить" на всех закладках
# диалога синхронизированы. Кнопка "Сохранить" становится активной
# при изменении любого параметра, либо при создании объекта.
#
# Возвращает идентификатор открытого диалога (HSTATISTIC).
# Для освобождения объекта диалога вызывать rscCloseStatisticObject.
# Для смены объекта (без переоткрытия диалога) вызывать rscChangeStatisticObject.
# При ошибке возвращает 0

#   rscCreateStatisticObject_t = mapsyst.GetProcAddress(curLib,HSTATISTIC,'rscCreateStatisticObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
#   def rscCreateStatisticObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _flag: int) -> HSTATISTIC:
#       return rscCreateStatisticObject_t (_hmap, _parm, _info, _point, _flag)


# Изменить выбранный объект в диалоге "Выбор объекта",
# открытый с помощью функции rscCreateStatisticObject
#  hstat - идентификатор открытого диалога
#  info  - идентификатор объекта карты
#  point - точка курсора на карте (в метрах на местности). Используется для размещения
#          изображения выбранного объекта в диалоге (соответствует центру окна с объектом).
#          Если point = 0, то выбирается первая точка метрики объекта,
#          (исключение - для линейного объекта выбирается центральная точка).
# При ошибке возвращает 0

#   rscChangeStatisticObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'rscChangeStatisticObject', HSTATISTIC, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
#   def rscChangeStatisticObject(_hstat: HSTATISTIC, _info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
#       return rscChangeStatisticObject_t (_hstat, _info, _point)


# Закрыть диалог "Выбор объекта", открытый с помощью функции rscCreateStatisticObject
#  hstat - идентификатор открытого диалога
# При ошибке возвращает 0

#   rscCloseStatisticObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'rscCloseStatisticObject', HSTATISTIC)
#   def rscCloseStatisticObject(_hstat: HSTATISTIC) -> int:
#       return rscCloseStatisticObject_t (_hstat)


# Диалог редактирования параметров текста
# hmap           - идентификатор открытых данных
# hrsc           - идентификатор классификатора открытой карты
# text           - параметры шрифта
# function       - номер функции шрифта
# textflag       - режим диалога:
#                  0 - чистый диалог текст
#                  1 - вызван из TRUETYPE
#                  2 - вызван из TRIETYPE в шаблоне
#                  3 - вызван из шаблона
#                  4 - вызван из векторного объекта
# typedia        - тип диалога редактирования параметров (DI_SCR, DI_PRN, DI_IMG)
# currentPalette - номер текущей палитры
# parm           - параметры задачи
# При успешном завершении возвращает 1 и новые параметры, иначе возвращает 0

    rscEditTextParameters_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditTextParameters', maptype.HMAP, maptype.HRSC, ctypes.POINTER(mapgdi.IMGTEXT), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditTextParameters(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _text: ctypes.POINTER(mapgdi.IMGTEXT), _function: int, _textflag: int, _typedia: int, _currentPalette: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return rscEditTextParameters_t (_hmap, _hrsc, _text, _function, _textflag, _typedia, _currentPalette, _parm)


# Диалог редактирования цвета
# hrsc           - идентификатор классификатора открытой карты
# color          - цвет из классификатора
# currentPalette - номер текущей палитры
# diaType        - тип параметров - DI_SCR, DI_PRN, DI_IMG
# parm           - параметры задачи
# При успешном завершении возвращает 1 и новый цвет, иначе возвращает 0

    rscEditColorByType_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditColorByType', maptype.HRSC, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditColorByType(_hrsc: maptype.HRSC, _color: ctypes.POINTER(maptype.COLORREF), _currentPalette: int, _diaType: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return rscEditColorByType_t (_hrsc, _color, _currentPalette, _diaType, _parm)


# Диалог редактирования параметров объекта типа Таблица (IMG_TABLE)
# hmap           - идентификатор открытых данных
# hrsc           - идентификатор классификатора
# parm           - параметры задачи
# diaType        - тип параметров - DI_SCR, DI_PRN, DI_IMG
# currentPalette - номер текущей палитры в классификаторе
# buff           - параметры IMGTABLE
# buffsize       - размер выделенного буфера (1024)
# При сохранении редактирования возвращает 1
# При ошибке или отказе редактирования возвращает 0

    rscEditTableParameters_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditTableParameters', maptype.HMAP, maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def rscEditTableParameters(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diaType: int, _currentPalette: int, _buff: ctypes.c_char_p, _buffsize: int) -> int:
        return rscEditTableParameters_t (_hmap, _hrsc, _parm, _diaType, _currentPalette, _buff, _buffsize)


# Диалог создания объекта типа Таблица (IMG_TABLE)
#  hmap    - идентификатор открытых данных
#  hobj    - идентификатор создаваемого объекта
#  parm    - параметры задачи
#  diaType - тип параметров - DI_SCR, DI_PRN, DI_IMG
#  currentPalette - номер текущей палитры в классификаторе
#  buff    - параметры IMGTABLE
#  buffsize- размер выделенного буфера
#  При сохранении редактирования возвращает 1
#  При ошибке или отказе редактирования возвращает 0

    rscCreateObjectTable_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscCreateObjectTable', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def rscCreateObjectTable(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diaType: int, _currentPalette: int, _buff: ctypes.c_char_p, _buffsize: int) -> int:
        return rscCreateObjectTable_t (_hmap, _hobj, _parm, _diaType, _currentPalette, _buff, _buffsize)


# Создать диалог "Ввод данных"
# value        - значение для установки в редактируемое поле
# parm         - параметры задачи
# callbackfunc - указатель на функцию обратного вызова
# callparam    - параметр, который будет передан вызываемой функции
# Возвращает идентификатор открытого диалога (HEDITVALUE)
# При ошибке возвращает 0

#   rscCreateEditValueDialog_t = mapsyst.GetProcAddress(curLib,HEDITVALUE,'rscCreateEditValueDialog', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX), CallbackEditValue, ctypes.c_void_p)
#   def rscCreateEditValueDialog(_value: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX), _callbackfunc: CallbackEditValue, _callparam: ctypes.c_void_p) -> HEDITVALUE:
#       return rscCreateEditValueDialog_t (_value, _parm, _callbackfunc, _callparam)


# Обновить положение и текста диалога "Ввод данных"
# hdial     - идентификатор открытого диалога
# value     - значение для установки в редактируемое поле
# left, top - положение диалога относительно курсора (справа)
# isFocus   - установка фокуса в диалог для ввода значения
# clRect    - габариты окна (клиентская область), в пределах которого
# отображается диалог в пикселях экрана
# Положение диалога изменяется в пределах габаритов окна
# (например, в крайней правой точке диалог будет расположен слева от курсора)
#           - 0 - положение диалога относительно значений left, top без
#              корректировки положения
# key - код клавиши, с помощью которой установился фокус на диалог
# Обрабатываемые символы: "," (код: 188), "." (код: 190) и цифры
# Добавляется первым символом в поле ввода, курсор ставится на следующую позицию
#           - 0 - не добавляется в поле ввода
# При ошибке возвращает 0

#   rscChangeEditValueDialogPos_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'rscChangeEditValueDialogPos', HEDITVALUE, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.RECT), ctypes.c_uint)
#   def rscChangeEditValueDialogPos(_hdial: HEDITVALUE, _value: mapsyst.WTEXT, _left: int, _top: int, _isFocus: int, _clRect: ctypes.POINTER(maptype.RECT), _key: int) -> int:
#       return rscChangeEditValueDialogPos_t (_hdial, _value, _left, _top, _isFocus, _clRect, _key)


# Установить видимость диалога "Ввод данных"
# hdial - идентификатор открытого диалога
# view  - видимость диалога
#       - 0 - скрыть диалог
#       - 1 - отобразить диалог

#   rscSetEditValueVisible_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'rscSetEditValueVisible', HEDITVALUE, ctypes.c_int)
#   def rscSetEditValueVisible(_hdial: HEDITVALUE, _view: int) -> ctypes.c_void_p:
#       return rscSetEditValueVisible_t (_hdial, _view)


# Закрыть диалог "Ввод данных"
# hdial - идентификатор открытого диалога

#   rscCloseEditValueDialog_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'rscCloseEditValueDialog', HEDITVALUE)
#   def rscCloseEditValueDialog(_hdial: HEDITVALUE) -> ctypes.c_void_p:
#       return rscCloseEditValueDialog_t (_hdial)


# Редактирование параметров графического файла
# hmap           - идентификатор открытых данных
# hrsc           - идентификатор классификатора открытой карты
# parm           - параметры задачи
# diaType        - тип диалога редактирования параметров (DI_SCR, DI_PRN, DI_IMG)
# currentPalette - номер текущей палитры
# function       - номер функции визуализации графических объектов
# buff           - параметры IMGGRAPHICMARKEX
# buffsize       - размер выделенного буфера (1024)
# mapnumber      - номер пользовательской карты в цепочке
# layernumber    - номер слоя
# regime         - режим вызова диалога (1 - режим нанесения на карту графического файла, иначе - 0)
# При сохранении редактирования возвращает 1
# При ошибке или отказе редактирования возвращает 0

    rscEditGraphicMarkParametersEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditGraphicMarkParametersEx', maptype.HMAP, maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def rscEditGraphicMarkParametersEx(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diaType: int, _currentPalette: int, _function: ctypes.POINTER(ctypes.c_int), _buff: ctypes.c_char_p, _buffsize: int, _mapnumber: ctypes.POINTER(ctypes.c_int), _layernumber: ctypes.POINTER(ctypes.c_int), _regime: int) -> int:
        return rscEditGraphicMarkParametersEx_t (_hmap, _hrsc, _parm, _diaType, _currentPalette, _function, _buff, _buffsize, _mapnumber, _layernumber, _regime)

    rscEditGraphicMarkParameters_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditGraphicMarkParameters', maptype.HMAP, maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int)
    def rscEditGraphicMarkParameters(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diaType: int, _currentPalette: int, _function: ctypes.POINTER(ctypes.c_int), _buff: ctypes.c_char_p, _buffsize: int) -> int:
        return rscEditGraphicMarkParameters_t (_hmap, _hrsc, _parm, _diaType, _currentPalette, _function, _buff, _buffsize)


# Нанесение графического точечного объекта
# hmap   - идентификатор открытой векторной карты
# parm   - параметры приложения
# buff   - адрес области для размещения параметров точечного знака
# buffsize - размер области параметров (не менее 8#1024)
# mapnumber - номер пользовательской карты в цепочке
# layernumber - номер слоя
# type        - тип диалога редактирования параметров (DI_SCR, DI_PRN, DI_IMG)
# currentPalette - номер текущей палитры
# При ошибке возвращает 0

    rscEditPointImage_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditPointImage', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def rscEditPointImage(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _buff: ctypes.c_char_p, _buffsize: int, _mapnumber: ctypes.POINTER(ctypes.c_int), _layernumber: ctypes.POINTER(ctypes.c_int)) -> int:
        return rscEditPointImage_t (_hmap, _parm, _buff, _buffsize, _mapnumber, _layernumber)

    rscEditPointImageEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_int,'rscEditPointImageEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
    def rscEditPointImageEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _buff: ctypes.c_char_p, _buffsize: int, _mapnumber: ctypes.POINTER(ctypes.c_int), _layernumber: ctypes.POINTER(ctypes.c_int), _type: int, _currentpalette: int) -> int:
        return rscEditPointImageEx_t (_hmap, _parm, _buff, _buffsize, _mapnumber, _layernumber, _type, _currentpalette)

except Exception as e:
    print(e)
    rsctoolslib = 0