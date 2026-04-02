#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst
import mmstruct

try:
    if os.environ['gisselecdll']:
        gisselecname = os.environ['gisselecdll']
except KeyError:
    gisselecname = 'gis64selec.dll'


try:
    seleclib = mapsyst.LoadLibrary(gisselecname)


# Выбор из классификатора карты семантической
# характеристики c предустановленным кодом семантики
# hrsc - идентификатор классификатора ресурсов карты
# parm - параметры задачи (см. maptype.h)
# code - предустановленное значение кода характеристики
#       (при открытии формы данный код характеристики будет выбран)
# При успешном выполнении возвращает код выбранной семантики
# При ошибке возвращает ноль

    selSemanticSelectInit_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSemanticSelectInit', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def selSemanticSelectInit(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int) -> int:
        return selSemanticSelectInit_t (_hrsc, _parm, _code)


# Выбор из классификатора карты семантической
# характеристики по фильтру семантик c предустановленным кодом семантики.
# hrsc   - идентификатор классификатора ресурсов карты;
# parm   - параметры задачи (см. maptype.h);
# code   - предустановленное значение кода характеристики
#          (при открытии формы данный код характеристики будет выбран);
# filter - массив кодов семантик для выбора (фильтр);
# count  - количество элементов в массиве filter.
# При успешном выполнении возвращает код выбранной семантики,
# иначе возвращает ноль.

    selSemanticSelectFilterInit_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSemanticSelectFilterInit', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def selSemanticSelectFilterInit(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int, _filter: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
        return selSemanticSelectFilterInit_t (_hrsc, _parm, _code, _filter, _count)


# Выбор из классификатора карты семантической
# характеристики по фильтру семантик.
# hrsc   - идентификатор классификатора ресурсов карты;
# parm   - параметры задачи (см. maptype.h);
# filter - массив кодов семантик для выбора (фильтр);
# count  - количество элементов в массиве filter.
# При успешном выполнении возвращает код выбранной семантики,
# иначе возвращает ноль.

    selSemanticSelectFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSemanticSelectFilter', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def selSemanticSelectFilter(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _filter: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
        return selSemanticSelectFilter_t (_hrsc, _parm, _filter, _count)


# Выбор из классификатора карты кода символьной семантической характеристики
# (при открытии формы будут доступны для выбора только семантики типа
# TSTRING - Символьная строка)
# hrsc - идентификатор классификатора ресурсов карты
# parm - параметры задачи (см. maptype.h)
# code - предустановленное значение кода характеристики
#       (при открытии формы данный код характеристики будет выбран,
#        при code = 0 первоначально будет выбран первый по порядку код)
# При успешном выполнении возвращает код выбранной семантики,
# при ошибке возвращает ноль.

#   selStringSemanticSelect_t = mapsyst.GetProcAddress(seleclib,long int _export,'selStringSemanticSelect', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
#   def selStringSemanticSelect(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int) -> long int _export:
#       return selStringSemanticSelect_t (_hrsc, _parm, _code)


# Установить фильтр отображения объектов карты
# hmap    - идентификатор открытой векторной карты
# parm    - параметры задачи (см. maptype.h)
# note    - адрес переменной,определяющей вид окна и содержащей
#           индекс активной закладки при старте программы фильтра
#           (допустимо note = 0).
# Если фильтр изменился, возвращает ненулевое значение
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetViewStaff_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetViewStaff', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int))
    def selSetViewStaff(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _note: ctypes.POINTER(ctypes.c_int)) -> int:
        return selSetViewStaff_t (_hmap, _parm, _note)


# Установить фильтр отображаемых объектов карты
# hmap    - идентификатор открытой векторной карты
# parm    - параметры задачи (см. maptype.h)
# note    - адрес переменной,определяющей вид окна и содержащей
#           индекс активной закладки при старте программы фильтра (допустимо note = 0).
# restoremode - флаг восстановления контекста отображения карты :
#           "-1" - стандартно восстановить контекст отображения;
#           "0"  - использовать текущее состояние контекста отображения.
# Если фильтр изменился, возвращает ненулевое значение
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetViewStaffEx_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetViewStaffEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def selSetViewStaffEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _note: ctypes.POINTER(ctypes.c_int), _restoremode: int) -> int:
        return selSetViewStaffEx_t (_hmap, _parm, _note, _restoremode)


# Установить фильтр отображаемых объектов карты
# hmap    - идентификатор открытой векторной карты
# hsite   - идентификатор идентификатор пользовательской карты
# parm    - параметры задачи (см. maptype.h)
# note    - адрес переменной, содержащей индекс активной закладки
# Если фильтр изменился, возвращает ненулевое значение

#   selSetSiteViewStaff_t = mapsyst.GetProcAddress(seleclib,long int _export,'selSetSiteViewStaff', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int))
#   def selSetSiteViewStaff(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _note: ctypes.POINTER(ctypes.c_int)) -> long int _export:
#       return selSetSiteViewStaff_t (_hmap, _hsite, _parm, _note)


# Восстановить параметры поиска
# hmap    - идентификатор открытой векторной карты

    selRestoreSeekSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selRestoreSeekSelect', maptype.HMAP)
    def selRestoreSeekSelect(_hmap: maptype.HMAP) -> int:
        return selRestoreSeekSelect_t (_hmap)


# Сформировать модель и записать ее в файл моделей
# hmap  - идентификатор открытой векторной карты
# hsite - идентификатор пользовательской карты, для которой формируется модель
# parm - параметры задачи (см. maptype.h);
# modelname - имя модели
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок
# Help вызывается из mapselec.chm, топик ?? IDN_SETMODELS    6710

    selSetSiteModelFilterTitleUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSiteModelFilterTitleUn', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def selSetSiteModelFilterTitleUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _modelname: mapsyst.WTEXT, _namesize: int, _title: mapsyst.WTEXT) -> int:
        return selSetSiteModelFilterTitleUn_t (_hmap, _hsite, _parm, _modelname.buffer(), _namesize, _title.buffer())


# Сформировать модель и записать ее в файл моделей
# hmap  - идентификатор открытой векторной карты
# parm - параметры задачи (см. maptype.h);
# modelnames - массив имен моделей 2D
# modelnames3D - массив имен моделей 3D
# namesize - максимальная длина имени модели
# modelcount - число моделей в каждом массиве
# modifyflag - массив флагов изменений моделей
# размерность массивов modelnames и modifyflag равна количеству сайтов + 1
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок
# Help вызывается из mapselec.chm, топик ?? IDN_SETMODELS   6710

    selSetModelsFilterTitleUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetModelsFilterTitleUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR)
    def selSetModelsFilterTitleUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _modelnames: mapsyst.WTEXT, _modelnames3D: mapsyst.WTEXT, _namesize: int, _modelcount: int, _modifyflag: ctypes.POINTER(ctypes.c_long), _title: mapsyst.WTEXT) -> int:
        return selSetModelsFilterTitleUn_t (_hmap, _parm, _modelnames.buffer(), _modelnames3D.buffer(), _namesize, _modelcount, _modifyflag, _title.buffer())


# Установить фильтр поиска объектов карты
# Фильтр поиска объектов карты автоматически восстанавливается/запоминается в
# служебном файле при старте/завершении программы.
# hmap - идентификатор открытой векторной карты
# parm - параметры задачи (см. maptype.h);
# note - адрес переменной,определяющей вид окна фильтра.
#        Служит для запоминания/восстановления индекса активной закладки
#        при старте программы фильтра.(Допустимо note = 0).
# Возвращает: "1" - выбран режим поиска объектов;
#             "2" - выбран режим выделения объектов карты;
#             "0" - ошибка или отказ.
# Help вызывается из mapselec.chm, топик "POISK"

#   selSetObjectsSearch_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetObjectsSearch', maptype.HMAP, ctypes.POINTER(TASKPARM), ctypes.POINTER(ctypes.c_int))
#   def selSetObjectsSearch(_hmap: maptype.HMAP, _parm: ctypes.POINTER(TASKPARM), _note: ctypes.POINTER(ctypes.c_int)) -> int:
#       return selSetObjectsSearch_t (_hmap, _parm, _note)


# Расширенная установка фильтра поиска объектов карты
# Фильтр поиска объектов карты автоматически восстанавливается/запоминается в
# служебном файле при старте/завершении программы.
# Для изменения стандартных операций  восстановления используется
# структура RESTOREMODE.
# hmap - идентификатор открытой векторной карты;
# parm - параметры задачи (см. maptype.h);
# mode - параметры восстановления фильтра;
# Возвращает: "1" - выбран режим поиска объектов;
#             "2" - выбран режим выделения объектов карты;
#             "0" - ошибка или отказ.
# Help вызывается из mapselec.chm, топик "POISK"

#   selSetObjectsSearchEx_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetObjectsSearchEx', maptype.HMAP, ctypes.POINTER(TASKPARM), ctypes.POINTER(mmstruct.RESTOREMODE))
#   def selSetObjectsSearchEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(TASKPARM), _mode: ctypes.POINTER(mmstruct.RESTOREMODE)) -> int:
#       return selSetObjectsSearchEx_t (_hmap, _parm, _mode)


# Расширенная установка фильтра поиска объектов карты
# Фильтр поиска объектов карты автоматически восстанавливается/запоминается в
# служебном файле при старте/завершении программы.
# Для изменения стандартных операций  восстановления используется
# структура RESTOREMODE.
# При старте отображается полный состав в соответствии с
# классификатором карты.
# hmap - идентификатор открытой векторной карты;
# parm - параметры задачи (см. maptype.h);
# mode - параметры восстановления фильтра;
# Возвращает: "1" - выбран режим поиска объектов;
#             "2" - выбран режим выделения объектов карты;
#             "0" - ошибка или отказ.
# Help вызывается из mapselec.chm, топик "POISK"

    selSetObjectsSearchRsc_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetObjectsSearchRsc', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(mmstruct.RESTOREMODE))
    def selSetObjectsSearchRsc(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _mode: ctypes.POINTER(mmstruct.RESTOREMODE)) -> int:
        return selSetObjectsSearchRsc_t (_hmap, _parm, _mode)


# Установить фильтр слоев карты
# hwnd      - идентификатор родительского окна;
# hrsc      - идентификатор классификатора ресурсов карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# title     - заголовок окна фильтра слоев карты;
# rc        - записать 0

    selSetLayersFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetLayersFilter', maptype.HWND, maptype.HRSC, maptype.HSELECT, ctypes.c_char_p, maptype.HINSTANCE)
    def selSetLayersFilter(_hwnd: maptype.HWND, _hrsc: maptype.HRSC, _hselect: maptype.HSELECT, _title: ctypes.c_char_p, _rc: maptype.HINSTANCE) -> int:
        return selSetLayersFilter_t (_hwnd, _hrsc, _hselect, _title, _rc)


# Восстановить параметры отображения карты
# hmap - идентификатор открытой векторной карты
# При ошибке возвращает ноль

    selRestoreSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selRestoreSelect', maptype.HMAP)
    def selRestoreSelect(_hmap: maptype.HMAP) -> int:
        return selRestoreSelect_t (_hmap)


# Сохранить параметры отображения объектов &
# Установить доступ ко всем видам данных контекста поиска для всех карт
# hmap - идентификатор открытой векторной карты
# При ошибке возвращает ноль

    selSaveSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSaveSelect', maptype.HMAP)
    def selSaveSelect(_hmap: maptype.HMAP) -> int:
        return selSaveSelect_t (_hmap)


# Сохранить параметры поиска объектов
# hmap - идентификатор открытой векторной карты;
# При ошибке возвращает ноль

    selSaveSeekSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSaveSeekSelect', maptype.HMAP)
    def selSaveSeekSelect(_hmap: maptype.HMAP) -> int:
        return selSaveSeekSelect_t (_hmap)


# Установить фильтр объектов карты
# hmap      - идентификатор открытой векторной карты;
# parm      - параметры задачи (см. maptype.h);
# hselect   - идентификатор контекста поиска карты (фильтр);
# В контексте фильтра HSELECT должна быть установлена карта.
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# При hmap != 0 список слоев, локализаций и объектов в диалоге фильтра
# формируется в соответствии с фактическим составом объектов карты
# (список м. б. меньше, чем в RSC !),
# иначе - по классификатору объектов карты (полный список)
# Если фильтр изменился, возвращает ненулевое значение
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetFilterTitleUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetFilterTitleUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HMAP, maptype.PWCHAR)
    def selSetFilterTitleUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hmap: maptype.HMAP, _title: mapsyst.WTEXT) -> int:
        return selSetFilterTitleUn_t (_parm, _hselect, _hmap, _title.buffer())

    selSetFilterTitle_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetFilterTitle', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HMAP, ctypes.c_char_p)
    def selSetFilterTitle(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hmap: maptype.HMAP, _title: ctypes.c_char_p) -> int:
        return selSetFilterTitle_t (_parm, _hselect, _hmap, _title)


# Установить фильтр объектов карты
# hmap      - идентификатор открытой векторной карты;
# hsite     - идентификатор идентификатор пользовательской карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# parm      - параметры задачи (см. maptype.h);
# В контексте фильтра HSELECT должна быть установлена карта.
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# mode - режим установки списка слоев, локализаций и объектов в диалоге фильтра
# При mode = 1 список слоев, локализаций и объектов в диалоге фильтра
# формируется по классификатору объектов карты (полный список)
# иначе - список слоев, локализаций и объектов
# формируется в соответствии с фактическим составом объектов карты
# (список м. б. меньше, чем в RSC !),
# Если фильтр изменился, возвращает ненулевое значение
# Help вызывается из mapselec.chm, топик "USTANOVKA"

#   selSetFilterMode_t = mapsyst.GetProcAddress(seleclib,long int _export,'selSetFilterMode', maptype.HSELECT, maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
#   def selSetFilterMode(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _mode: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> long int _export:
#       return selSetFilterMode_t (_hselect, _hmap, _hsite, _mode, _parm, _title.buffer())


# Установить фильтр объектов для заданной пользовательской карты
# hmap - идентификатор открытой векторной карты;
# hsite - идентификатор пользовательской карты
# hselect   - идентификатор контекста поиска пользовательской карты (фильтр);
# В контексте фильтра HSELECT должна быть установлена карта.
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# Если фильтр изменился, возвращает ненулевое значение
# При hmap != 0 список слоев, локализаций и объектов в диалоге фильтра
# формируется в соответствии с фактическим составом объектов карты
# (список м. б. меньше, чем в RSC !),
# иначе - по классификатору объектов карты (полный список)
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetSiteFilterTitleUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSiteFilterTitleUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def selSetSiteFilterTitleUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _title: mapsyst.WTEXT) -> int:
        return selSetSiteFilterTitleUn_t (_parm, _hselect, _hmap, _hsite, _title.buffer())

    selSetSiteFilterTitle_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSiteFilterTitle', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HMAP, maptype.HSITE, ctypes.c_char_p)
    def selSetSiteFilterTitle(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _title: ctypes.c_char_p) -> int:
        return selSetSiteFilterTitle_t (_parm, _hselect, _hmap, _hsite, _title)


# Установить условия поиска объектов карты по названию семантики
# hmap - идентификатор открытой векторной карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# arrayname - условия поиска по названию (см. mmstruct.h)
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "MARPOISK"

    selSearchNameUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSearchNameUn', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(maptype.TASKPARMEX))
    def selSearchNameUn(_hmap: maptype.HMAP, _select: maptype.HSELECT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return selSearchNameUn_t (_hmap, _select, _parm)

    selSearchName_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSearchName', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(mmstruct.ARRAYNAME), ctypes.POINTER(maptype.TASKPARMEX))
    def selSearchName(_hmap: maptype.HMAP, _select: maptype.HSELECT, _arrayname: ctypes.POINTER(mmstruct.ARRAYNAME), _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return selSearchName_t (_hmap, _select, _arrayname, _parm)


# Установить параметры поиска объектов карты по области
# hmap      - идентификатор открытой векторной карты;
# parm      - параметры задачи (см. maptype.h);
# hobj      - данные области поиска;
#             метрика области должна быть в метрах !
# seekparm - параметры поиска по области;
# hwnd      - идентификатор окна назначения сообщений WM_PROGRESSBAR
# Возвращает: "1" - выбран режим поиска объектов;
#             "2" - выбран режим выделения объектов карты;
#             "3" - выбран режим выбора области;
#             "0" - ошибка или отказ.
# Help вызывается из mapselec.chm, топик "POISKOBL"

    selSearchObjectByArea_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSearchObjectByArea', ctypes.POINTER(maptype.TASKPARMEX), maptype.HMAP, maptype.HOBJ, maptype.HWND, ctypes.POINTER(mmstruct.AREASEEKPARM))
    def selSearchObjectByArea(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hwnd: maptype.HWND, _seekparm: ctypes.POINTER(mmstruct.AREASEEKPARM)) -> int:
        return selSearchObjectByArea_t (_parm, _hmap, _hobj, _hwnd, _seekparm)


# Установить фильтр объектов карты
# hmap - идентификатор открытой векторной карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# В контексте фильтра HSELECT должна быть установлена карта.
# Если фильтр изменился, возвращает ненулевое значение
# При hmap != 0 список слоев, локализаций и объектов в диалоге фильтра
# формируется в соответствии с фактическим составом объектов карты
# (список м. б. меньше, чем в RSC !),
# иначе - по классификатору объектов карты (полный список)
# Если фильтр изменился, возвращает ненулевое значение
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetFilter', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HMAP)
    def selSetFilter(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hmap: maptype.HMAP) -> int:
        return selSetFilter_t (_parm, _hselect, _hmap)


# Установить фильтр объектов карты
# hrsc - идентификатор классификатора открытой карты
# hselect   - идентификатор контекста поиска карты (фильтр);
# Структура NAMESARRAY должна содержать список имен листов карты
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# Если фильтр изменился, возвращает ненулевое значение
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "USTANOVKA"

    selSetFilterByNameUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetFilterByNameUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HRSC, ctypes.POINTER(mmstruct.NAMESARRAY), maptype.PWCHAR)
    def selSetFilterByNameUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hrsc: maptype.HRSC, _namesarray: ctypes.POINTER(mmstruct.NAMESARRAY), _title: mapsyst.WTEXT) -> int:
        return selSetFilterByNameUn_t (_parm, _hselect, _hrsc, _namesarray, _title.buffer())

    selSetFilterByName_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetFilterByName', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HRSC, ctypes.POINTER(mmstruct.NAMESARRAY), ctypes.c_char_p)
    def selSetFilterByName(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hrsc: maptype.HRSC, _namesarray: ctypes.POINTER(mmstruct.NAMESARRAY), _title: ctypes.c_char_p) -> int:
        return selSetFilterByName_t (_parm, _hselect, _hrsc, _namesarray, _title)


# Установить условия поиска объектов карты
# hmap - идентификатор открытой векторной карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# Если фильтр изменился, возвращает ненулевое значение
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "FORMPOISK"

    selFindStaff_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selFindStaff', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(maptype.TASKPARMEX))
    def selFindStaff(_hmap: maptype.HMAP, _select: maptype.HSELECT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return selFindStaff_t (_hmap, _select, _parm)


# Установить фильтр объектов карты для выделения по рамке
# hmap - идентификатор открытой векторной карты;
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "POISK"

    selSetMarkFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetMarkFilter', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def selSetMarkFilter(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return selSetMarkFilter_t (_hmap, _parm)


# Установить фильтр поиска объектов карты
# hmap - идентификатор открытой векторной карты;
# activepage - номер активной закладки(страницы)
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# При ошибке возвращает ноль
# Help вызывается из mapselec.chm, топик "POISK"

    selSetSearchFilterUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSearchFilterUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), maptype.PWCHAR)
    def selSetSearchFilterUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _activepage: ctypes.POINTER(ctypes.c_int), _title: mapsyst.WTEXT) -> int:
        return selSetSearchFilterUn_t (_hmap, _parm, _activepage, _title.buffer())

    selSetSearchFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSearchFilter', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_char_p)
    def selSetSearchFilter(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _activepage: ctypes.POINTER(ctypes.c_int), _title: ctypes.c_char_p) -> int:
        return selSetSearchFilter_t (_hmap, _parm, _activepage, _title)


# Установить фильтр объектов классификатора
# hmap      - идентификатор открытой векторной карты;
# hsite     - идентификатор идентификатор пользовательской карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# parm      - параметры задачи (см. maptype.h);
# В контексте фильтра HSELECT должна быть установлена карта.
# title - заголовок окна фильтра объектов карты,
# если == 0, устанавливается стандартный заголовок.
# mode - режим установки списка слоев, локализаций и объектов в диалоге фильтра
# При mode = 1 список слоев, локализаций и объектов в диалоге фильтра
# формируется по классификатору объектов карты (полный список)
# иначе - список слоев, локализаций и объектов
# формируется в соответствии с фактическим составом объектов карты
# (список м. б. меньше, чем в RSC !),
# Если фильтр изменился, возвращает ненулевое значение

    selSetObjectFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetObjectFilter', maptype.HSELECT, maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def selSetObjectFilter(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _mode: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        return selSetObjectFilter_t (_hselect, _hmap, _hsite, _mode, _parm, _title.buffer())


#++++++++++++++++++++++++++++++++++++++++++++++++++
#  Интерфейс с файлами моделей поиска/отображения +
#++++++++++++++++++++++++++++++++++++++++++++++++++
# Boccтановить параметры поиска объектов по имени модели
# hmap - идентификатор открытой векторной карты;
# При ошибке возвращает "0", иначе "1"

    selRestoreParmsUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selRestoreParmsUn', maptype.HMAP, maptype.PWCHAR)
    def selRestoreParmsUn(_hmap: maptype.HMAP, _modelname: mapsyst.WTEXT) -> int:
        return selRestoreParmsUn_t (_hmap, _modelname.buffer())

    selRestoreParms_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selRestoreParms', maptype.HMAP, ctypes.c_char_p)
    def selRestoreParms(_hmap: maptype.HMAP, _modelname: ctypes.c_char_p) -> int:
        return selRestoreParms_t (_hmap, _modelname)


# Установить контекст по модели с номером "nmodel"
# hmap - идентификатор открытой векторной карты;
# hselect   - идентификатор контекста поиска карты (фильтр);
# nmap - номер карты в цепочке
# При ошибке возвращает "0", иначе "1"

    selSetSelectByModel_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSelectByModel', maptype.HSELECT, maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def selSetSelectByModel(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _nmap: int, _nmodel: int) -> int:
        return selSetSelectByModel_t (_hselect, _hmap, _nmap, _nmodel)


# Установить условия поиска объектов карты по адресу
# hmap      - идентификатор открытой векторной карты;
# parm      - параметры задачи (см. maptype.h);
# Help вызывается из mapselec.chm, топик "IDN_SEARCH_ADDR"

    selSearchAddress_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSearchAddress', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def selSearchAddress(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return selSearchAddress_t (_hmap, _parm)


# Открыть диалог выбора карт и установить параметры поиска объектов
# по выбранным картам
#   hmap    - идентификатор открытой векторной карты
#   parm    - параметры задачи (см. maptype.h)
#   flag    - флаг выделения карт в списке
#             0 - не выделять
#             1 - выделить все
#             2 - выделить карты, доступные для редактирования
# Для выделения объектов в окне карты после функции selSetSelectByMap вызвать:
#   ::PostMessage(parm->DocHandle, CM_PAN_SEARCH, 1, 0);
# При ошибке возвращает 0

    selSetSelectByMap_t = mapsyst.GetProcAddress(seleclib,ctypes.c_int,'selSetSelectByMap', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_int)
    def selSetSelectByMap(_map: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _flag: int) -> int:
        return selSetSelectByMap_t (_map, _parm, _flag)

except Exception as e:
    print(e)
    seleclib = 0