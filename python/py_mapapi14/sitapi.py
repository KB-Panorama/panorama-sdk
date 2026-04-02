#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype
import mapcreat
import mapgdi

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++ ОПИСАНИЕ ФУНКЦИЙ ДОСТУПА К ПОЛЬЗОВАТЕЛЬСКОЙ КАРТЕ +++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Открыть пользовательскую карту в заданном районе работ
# (добавить в цепочку пользовательских карт (в обстановку))
# Возвращает идентификатор открытой пользовательской карты
# hMap     - идентификатор открытой карты
# sitename - имя открываемого файла пользовательской карты
# mode     - режим чтения/записи (GENERIC_READ, GENERIC_WRITE
#            или 0) GENERIC_READ - все данные только на чтение
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
# При ошибке возвращает ноль

    mapOpenSiteForMapPro_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapOpenSiteForMapPro(_hMap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int, _transform: int, _password: mapsyst.WTEXT, _size: int) -> maptype.HSITE:
        return mapOpenSiteForMapPro_t (_hMap, _sitename.buffer(), _mode, _transform, _password.buffer(), _size)

    mapOpenSiteForMapExUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapExUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapOpenSiteForMapExUn(_hMap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int, _transform: int) -> maptype.HSITE:
        return mapOpenSiteForMapExUn_t (_hMap, _sitename.buffer(), _mode, _transform)

    mapOpenSiteForMapUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenSiteForMapUn(_hMap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int) -> maptype.HSITE:
        return mapOpenSiteForMapUn_t (_hMap, _sitename.buffer(), _mode)

    mapOpenSiteForMap_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMap', maptype.HMAP, ctypes.c_char_p, ctypes.c_int)
    def mapOpenSiteForMap(_hMap: maptype.HMAP, _sitename: ctypes.c_char_p, _mode: int) -> maptype.HSITE:
        return mapOpenSiteForMap_t (_hMap, _sitename, _mode)

    mapOpenSiteForMapEx_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapEx', maptype.HMAP, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
    def mapOpenSiteForMapEx(_hMap: maptype.HMAP, _sitename: ctypes.c_char_p, _mode: int, _transform: int) -> maptype.HSITE:
        return mapOpenSiteForMapEx_t (_hMap, _sitename, _mode, _transform)


# Закрыть пользовательскую карту в заданном районе работ
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если hSite == 0, закрываются все данные обстановки
# При ошибке возвращает ноль

    mapCloseSiteForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseSiteForMap', maptype.HMAP, maptype.HSITE)
    def mapCloseSiteForMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapCloseSiteForMap_t (_hMap, _hSite)


# Закрыть пользовательскую карту в заданном районе работ
# hMap - идентификатор открытой карты
# name - имя паспорта пользовательской карты
# При ошибке возвращает ноль

    mapCloseSiteForMapByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseSiteForMapByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapCloseSiteForMapByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        return mapCloseSiteForMapByNameUn_t (_hMap, _name.buffer())

    mapCloseSiteForMapByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCloseSiteForMapByName', maptype.HMAP, ctypes.c_char_p)
    def mapCloseSiteForMapByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> int:
        return mapCloseSiteForMapByName_t (_hMap, _name)


# Удалить пользовательскую карту (все файлы данных)
# hMap - идентификатор открытой карты
# number - номер пользовательской карты в цепочке от 1 до числа карт
# При ошибке возвращает ноль

    mapDeleteSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSite', maptype.HMAP, ctypes.c_int)
    def mapDeleteSite(_hMap: maptype.HMAP, _number: int) -> int:
        return mapDeleteSite_t (_hMap, _number)


# Удалить пользовательскую карту (все файлы данных)
# name - полное имя файла паспорта карты
# При ошибке возвращает ноль

    mapDeleteSiteByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteByName', ctypes.c_char_p)
    def mapDeleteSiteByName(_name: ctypes.c_char_p) -> int:
        return mapDeleteSiteByName_t (_name)

    mapDeleteSiteByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteByNameUn', maptype.PWCHAR)
    def mapDeleteSiteByNameUn(_name: mapsyst.WTEXT) -> int:
        return mapDeleteSiteByNameUn_t (_name.buffer())


# Удалить все объекты пользовательской карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapClearSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearSite', maptype.HMAP, maptype.HSITE)
    def mapClearSite(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapClearSite_t (_hMap, _hSite)


# Скопировать пользовательскую карту с изменением имен файлов
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# newname - новое полное имя паспорта карты
# Имена файлов данных будут иметь такое же имя, как у карты,
# но свое расширение
# Если классификатор расположен с картой, он тоже копируется
# в новую директорию
# Для удаления старой копии вызовите mapDeleteSite()
# При ошибке (новое имя не создано) возвращает ноль

    mapCopySiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopySiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapCopySiteUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _newname: mapsyst.WTEXT) -> int:
        return mapCopySiteUn_t (_hMap, _hSite, _newname.buffer())

    mapCopySite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCopySite', maptype.HMAP, maptype.HSITE, ctypes.c_char_p)
    def mapCopySite(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _newname: ctypes.c_char_p) -> int:
        return mapCopySite_t (_hMap, _hSite, _newname)


# Сохранить текущее состояние карты на диск
# hMap - идентификатор основной векторной карты
# hSite - идентификатор открытой пользовательской карты
# force - сохранять всегда, если не 0, или только при редактировании
# При выполнении редактирования карты с отключенным
# журналом транзакций состояние карты в памяти и
# на диске может отличаться, в этом случае можно
# вызвать mapSaveSite

    mapSaveSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSaveSite', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSaveSite(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _force: int) -> ctypes.c_void_p:
        return mapSaveSite_t (_hMap, _hSite, _force)


# Сортировка отдельной карты документа
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# handle  - идентификатор окна (HWND) для получения сообщений или 0
# flags   - Флажки обработки карты :
# 0 - сортировать все листы,
# 1 - только несортированные,
# 2 - сохранять файлы отката (устанавливается автоматически),
# 4 - повысить точность хранения,
# 16 - повысить точность хранения, формат - см
# 32 - повысить точность хранения, формат - мм
# 64 - повысить точность хранения, формат - радианы
# При ошибке возвращает ноль

    gsMapSorting_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gsMapSorting', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.c_int)
    def gsMapSorting(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _flags: int) -> int:
        return gsMapSorting_t (_hmap, _hsite, _handle, _flags)


# Запросить является ли пользовательская карта временной,
# то есть созданной через mapCreateTempSite или mapCreateAndAppendTempSite
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Для временной карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsTempSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsTempSite', maptype.HMAP, maptype.HSITE)
    def mapIsTempSite(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsTempSite_t (_hMap, _hSite)


# Запросить является ли пользовательская карта ограниченной
# по территории (по рамке номенклатурного листа)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если карта содержит номенклатурный лист, то функция возвращает
# ненулевое значение
# Если территория карты не ограничена (меняется при добавлении
# или удалении объектов) - возвращает ноль
# При ошибке возвращает ноль

    mapIsSiteLimited_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteLimited', maptype.HMAP, maptype.HSITE)
    def mapIsSiteLimited(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteLimited_t (_hMap, _hSite)


# Запросить содержит ли пользовательская карта координаты
# в геодезической системе (радианы)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если карта хранит координаты в геодезической системе,
# то функция возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteRealGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteRealGeo', maptype.HMAP, maptype.HSITE)
    def mapIsSiteRealGeo(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteRealGeo_t (_hMap, _hSite)


# Запросить содержит ли карта объекта координаты
# в геодезической системе (радианы)
# info - идентификатор объекта
# Если карта хранит координаты в геодезической системе,
# то функция возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsObjectMapRealGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsObjectMapRealGeo', maptype.HOBJ)
    def mapIsObjectMapRealGeo(_info: maptype.HOBJ) -> int:
        return mapIsObjectMapRealGeo_t (_info)


# Запрос - поддерживается ли пересчет к геодезическим
# координатам из плоских прямоугольных и обратно
# hMap     - идентификатор открытой основной карты
# hSite    - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapIsSiteGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteGeoSupported', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGeoSupported(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteGeoSupported_t (_hMap, _hSite)


# Запросить является ли пользовательская карта морской
# (карта создана по классификатору с именем s57navy.rsc)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Для морской карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteMarine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteMarine', maptype.HMAP, maptype.HSITE)
    def mapIsSiteMarine(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteMarine_t (_hMap, _hSite)

    mapIsSiteSeanutic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteSeanutic', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSeanutic(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteSeanutic_t (_hMap, _hSite)


# Запросить - это карта обстановки?
# (если карта создана по классификатору с именем operator.rsc)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Для карты обстановки возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteArmy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteArmy', maptype.HMAP, maptype.HSITE)
    def mapIsSiteArmy(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteArmy_t (_hMap, _hSite)


# Запросить - это аэронавигационная карта?
# (если карта создана по классификатору с именем dfc.rsc)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Для аэронавигационной карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteAero_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteAero', maptype.HMAP, maptype.HSITE)
    def mapIsSiteAero(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteAero_t (_hMap, _hSite)


# Запросить является ли пользовательская карта графом дорог?
# (карта создана по классификатору с именем service.rsc или road25.rsc и содержит дуги графа)
# Для карты графа возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteGraph_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteGraph', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGraph(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteGraph_t (_hMap, _hSite)


# Запросить открыта ли карта на сервере или локально
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Если карта открыта на сервере возвращает ненулевое значение

    mapIsSiteFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsSiteFromServer(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteFromServer_t (_hMap, _hSite)


# Запросить состояние данных для карты, открытой на сервере
# Если представление карты формируется на лету из базы данных,
# то при открытии карты устанавливается признак "состояние загрузки", равное 1.
# Признак сбрасывается при вызове функций mapAdjustData или mapAdjustSiteData,
# если загрузка карты завершена
# При ошибке возвращает ноль

    mapGetMapStateFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapStateFlag', maptype.HMAP, maptype.HSITE)
    def mapGetMapStateFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetMapStateFlag_t (_hMap, _hSite)


# Выполнить согласование данных карты в памяти и на диске
# (при многопользовательском доступе к данным)
# hmap -  идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Если состояние данных в памяти изменилось (по данным
# с диска) - возвращает ненулевое значение (1), иначе 0
# Если карта должна быть закрыта - возвращает 2
# (доступ на ГИС Сервер прекращен!)
# Если состояние изменилось - необходимо перерисовать
# изображение карты
# Опрос состояния целесообразно выполнять периодически
# в процессе работы приложения

    mapAdjustSiteData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAdjustSiteData', maptype.HMAP, maptype.HSITE)
    def mapAdjustSiteData(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapAdjustSiteData_t (_hMap, _hSite)


# Запросить - есть ли карты в состоянии загрузки на сервере
# Проверка выполняется для всех карт в составе "документа" (hMap)
# Если представление карты формируется на лету из базы данных,
# то при открытии карты устанавливается признак "состояние загрузки", равное 1.
# Признак сбрасывается при вызове функции mapAdjustData,
# если загрузка карты завершена
# Если есть карты в состоянии загрузки, то возвращает 1
# При ошибке возвращает ноль

    mapCheckMapStateFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckMapStateFlag', maptype.HMAP)
    def mapCheckMapStateFlag(_hMap: maptype.HMAP) -> int:
        return mapCheckMapStateFlag_t (_hMap)


# Запросить хранится ли карта в одном файле (формат SITX)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Если карта в одном файле возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteSitX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteSitX', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSitX(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteSitX_t (_hMap, _hSite)


# Запросить хранится ли карта в одном упакованном файле (формат SITZ/MAPZ)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Если карта в одном упакованном файле возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSitePackaged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSitePackaged', maptype.HMAP, maptype.HSITE)
    def mapIsSitePackaged(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSitePackaged_t (_hMap, _hSite)


# Запросить/Установить признак применения альтернативных шрифтов
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# flag - признак применения альтернативных шрифтов, заданных в файле altfonts.xml
# При ошибке возвращает ноль

    mapGetAlternativeFontsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE)
    def mapGetAlternativeFontsFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetAlternativeFontsFlag_t (_hMap, _hSite)

    mapSetAlternativeFontsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetAlternativeFontsFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetAlternativeFontsFlag_t (_hMap, _hSite, _flag)


# Установить признак ведения даты и времени обновления для каждого объекта
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак ведения даты и времени обновления
# Признак устанавливается после создания карты до записи объектов
# Если открытых данных нет возвращает ноль

    mapSetObjectTimeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectTimeFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetObjectTimeFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetObjectTimeFlag_t (_hMap, _hSite, _flag)


# Запросить признак ведения даты и времени обновления для каждого объекта
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если открытых данных нет или признак не установлен - возвращает ноль

    mapGetObjectTimeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectTimeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTimeFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetObjectTimeFlag_t (_hMap, _hSite)


# Установить признак ведения уникального идентификатора GUID для объектов карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак ведения GUID для объектов карты
# Признак устанавливается после создания карты до записи объектов
# Если признак установлен, то каждому объекту карты при создании автоматически
# присваивается семантика с кодом 32799, содержащая уникальную комбинацию
# из 32 шестнадцатеричных символов от 0 до F (GUID)
# Если открытых данных нет возвращает ноль

    mapSetAutoObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetAutoObjectGUID', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetAutoObjectGUID(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetAutoObjectGUID_t (_hMap, _hSite, _flag)


# Запросить признак ведения уникального идентификатора GUID для объектов карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если открытых данных нет или признак не установлен - возвращает ноль

    mapGetAutoObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetAutoObjectGUID', maptype.HMAP, maptype.HSITE)
    def mapGetAutoObjectGUID(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetAutoObjectGUID_t (_hMap, _hSite)


# Запросить количество открытых пользовательских карт
# hMap - идентификатор открытой карты
# При ошибке возвращает ноль

    mapGetSiteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteCount', maptype.HMAP)
    def mapGetSiteCount(_hMap: maptype.HMAP) -> int:
        return mapGetSiteCount_t (_hMap)


# Определить номер пользовательской карты в цепочке
# по ее идентификатору
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSiteNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteNumber_t (_hMap, _hSite)


# Определить имя файла паспорта пользовательской карты
# по ее идентификатору
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает пустую строку
# size - размер строки в байтах
# При ошибке возвращает 0

    mapGetSiteFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteFileNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteFileNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteFileNameUn_t (_hMap, _hSite, _name.buffer(), _size)

    mapGetSiteFileNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteFileNameEx', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int)
    def mapGetSiteFileNameEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetSiteFileNameEx_t (_hMap, _hSite, _name, _size)


# Запросить имена файлов данных листа карты для контроля
# целостности данных
# hMap  - идентификатор открытой карты (документа)
# hSite - идентификатор открытой пользовательской карты
# list   - номер листа карты с 1 до числа листов
# type   - тип листа карты (1 - файл заголовков, 2 - файл метрики,
#                           3 - файл семантики, 4 - файл графики)
# Кроме указанных файлов карта имеет паспорт карты и цифровой классификатор RSC
# Файл SITX содержит все данные (кроме RSC) в одном файле
# name   - адрес буфера для записи имени файла
# size   - размер буфера для записи имени файла
# Если запрошенный тип файла должен входить в состав карты (в паспорте карты
# отмечено, что такие данные есть в листе), то возвращает 1,
# если таких данных нет, то возвращает -1
# Файлы заголовков и метрики присутствуют всегда
# При ошибке возвращает 0

    mapGetMapFilesName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapFilesName', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetMapFilesName(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _type: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapFilesName_t (_hMap, _hSite, _list, _type, _name.buffer(), _size)


# Запросить длину файлов листа карты в байтах
# hMap  - идентификатор открытой карты (документа)
# hSite - идентификатор открытой пользовательской карты
# list  - номер листа карты с 1 до числа листов
# head  - указатель на поле для записи размера индексного файла (может равняться нулю)
# data  - указатель на поле для записи размера файла метрики (может равняться нулю)
# semn  - указатель на поле для записи размера файла семантики (может равняться нулю)
# draw  - указатель на поле для записи размера файла графических
#         параметров графических объектов (может равняться нулю)
# При экспорте в SXF размер файла SXF примерно будет равен сумме размеров всех файлов листа карты
# При ошибке возвращает ноль

    mapGetSheetFilesLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSheetFilesLength', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
    def mapGetSheetFilesLength(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _head: ctypes.POINTER(ctypes.c_ulong), _data: ctypes.POINTER(ctypes.c_ulong), _semn: ctypes.POINTER(ctypes.c_ulong), _draw: ctypes.POINTER(ctypes.c_ulong)) -> int:
        return mapGetSheetFilesLength_t (_hMap, _hSite, _list, _head, _data, _semn, _draw)


# Запросить общую длину данных всех файлов карты в байтах
# hMap  - идентификатор открытой карты (документа)
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteTotalDataSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapGetSiteTotalDataSize', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTotalDataSize(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteTotalDataSize_t (_hMap, _hSite)


# Определить путь к папке пользовательской карты
# по ее идентификатору
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает пустую строку

    mapGetSitePathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetSitePathUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSitePathUn_t (_hMap, _hSite, _name.buffer(), _size)

    mapGetLogPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetLogPathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetLogPathUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _path: mapsyst.WTEXT, _pathsize: int) -> int:
        return mapGetLogPathUn_t (_hMap, _hSite, _path.buffer(), _pathsize)


# Запросить имя файла vclx для карты
# При ошибке возвращает ноль

    mapGetVclxName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetVclxName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetVclxName(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _vclname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetVclxName_t (_hMap, _hSite, _vclname.buffer(), _size)


# Определить идентификатор открытой пользовательской карты
# по ее номеру в цепочке
# hMap   - идентификатор открытой карты
# number - номер пользовательской карты в цепочке
# Если number == 0, возвращается идентификатор фоновой
# (базовой) карты, равный hMap (он может применяться вместо HSITE)!
# При ошибке возвращает ноль

    mapGetSiteIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdent', maptype.HMAP, ctypes.c_int)
    def mapGetSiteIdent(_hMap: maptype.HMAP, _number: int) -> maptype.HSITE:
        return mapGetSiteIdent_t (_hMap, _number)


# Определить идентификатор открытой пользовательской карты
# по имени файла паспорта
# hMap - идентификатор открытой карты
# name - имя файла паспорта пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteIdentByName_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByName', maptype.HMAP, ctypes.c_char_p)
    def mapGetSiteIdentByName(_hMap: maptype.HMAP, _name: ctypes.c_char_p) -> maptype.HSITE:
        return mapGetSiteIdentByName_t (_hMap, _name)

    mapGetSiteIdentByNameUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetSiteIdentByNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT) -> maptype.HSITE:
        return mapGetSiteIdentByNameUn_t (_hMap, _name.buffer())


# Запросить имя листа по его номеру (number)
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# list  - номер листа карты
# name  - адрес буфера для результата запроса
# size  - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetSiteSheetNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteSheetNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteSheetNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteSheetNameUn_t (_hMap, _hSite, _list, _name.buffer(), _size)

    mapGetSiteSheetName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteSheetName', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetSiteSheetName(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetSiteSheetName_t (_hMap, _hSite, _list, _name, _size)


# Запросить номенклатуру листа по его номеру
# Номенклатура листа применяется для поиска в функции mapSeekObject
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# list  - номер листа карты
# name  - адрес буфера для результата запроса
# size  - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetSiteNomenclature_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteNomenclature', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetSiteNomenclature(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetSiteNomenclature_t (_hMap, _hSite, _list, _name, _size)

    mapGetSiteListNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListNameEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetSiteListNameEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: ctypes.c_char_p, _size: int) -> int:
        return mapGetSiteListNameEx_t (_hMap, _hSite, _list, _name, _size)

    mapGetSiteNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteNomenclatureUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteNomenclatureUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteNomenclatureUn_t (_hMap, _hSite, _list, _name.buffer(), _size)

    mapGetSiteListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteListNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteListNameUn_t (_hMap, _hSite, _list, _name.buffer(), _size)


# Определить идентификатор открытой пользовательской карты
# по имени листа карты (номенклатуре листа !)
# hMap - идентификатор открытой карты
# name - номенклатура листа карты
# list - поле для размещения номера листа (если лист найден в многолистовой карте)
# При ошибке возвращает ноль

    mapGetSiteIdentByNomenclature_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByNomenclature', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
    def mapGetSiteIdentByNomenclature(_hMap: maptype.HMAP, _name: ctypes.c_char_p, _list: ctypes.POINTER(ctypes.c_int)) -> maptype.HSITE:
        return mapGetSiteIdentByNomenclature_t (_hMap, _name, _list)

    mapGetSiteIdentBySheetName_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentBySheetName', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
    def mapGetSiteIdentBySheetName(_hMap: maptype.HMAP, _name: ctypes.c_char_p, _list: ctypes.POINTER(ctypes.c_int)) -> maptype.HSITE:
        return mapGetSiteIdentBySheetName_t (_hMap, _name, _list)

    mapGetSiteIdentByNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByNomenclatureUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapGetSiteIdentByNomenclatureUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_int)) -> maptype.HSITE:
        return mapGetSiteIdentByNomenclatureUn_t (_hMap, _name.buffer(), _list)


# Определить идентификатор открытой пользовательской карты
# по имени листа карты (которое получено в mapGetSiteSheetNameUn)
# hMap - идентификатор открытой карты
# name - имя листа карты
# list - поле для размещения номера листа
# При ошибке возвращает ноль

    mapGetSiteIdentBySheetNameUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentBySheetNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def mapGetSiteIdentBySheetNameUn(_hMap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_int)) -> maptype.HSITE:
        return mapGetSiteIdentBySheetNameUn_t (_hMap, _name.buffer(), _list)


# Запросить активную пользовательскую карту
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# При ошибке возвращает ноль

    mapGetActiveSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetActiveSite', maptype.HMAP)
    def mapGetActiveSite(_hMap: maptype.HMAP) -> maptype.HSITE:
        return mapGetActiveSite_t (_hMap)


# Установить активную пользовательскую карту
# (устанавливается приложением по своему усмотрению)
# hMap - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSetActiveSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetActiveSite', maptype.HMAP, maptype.HSITE)
    def mapSetActiveSite(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapSetActiveSite_t (_hMap, _hSite)


# Запросить идентификатор текущей отображаемой карты
# (при запросе в момент отображения из вспомогательной библиотеки -
# считаем, что один HMAP применяется в одном потоке отображения)
# При ошибке возвращает ноль

    mapGetCurrentViewSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetCurrentViewSite', maptype.HMAP)
    def mapGetCurrentViewSite(_hMap: maptype.HMAP) -> maptype.HSITE:
        return mapGetCurrentViewSite_t (_hMap)


# Запросить номер состояния пользовательской карты
# по ее идентификатору
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# Номер состояния меняется при любой операции редактирования
# карты (увеличивается на 1)
# При ошибке возвращает ноль

    mapGetSiteMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteMode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteMode(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteMode_t (_hMap, _hSite)


# Запросить - является ли открытая карта картой с данными c сервиса WFS
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapIsSiteWFS_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteWFS', maptype.HMAP, maptype.HSITE)
    def mapIsSiteWFS(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteWFS_t (_hMap, _hSite)


# Запросить - HWFS
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetHWFS_t = mapsyst.GetProcAddress(acceslib,maptype.HWFS,'mapGetHWFS', maptype.HMAP, maptype.HSITE)
    def mapGetHWFS(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> maptype.HWFS:
        return mapGetHWFS_t (_hMap, _hSite)


# Запросить - установлено ли шифрование данных
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)

    mapGetSiteCodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteCodeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCodeFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteCodeFlag_t (_hMap, _hSite)


# Запросить - зашифрована ли карта (формат SITX)
# name - имя карты (путь к файлу)
# Если нет - возвращает ноль

    mapGetSiteCodeFlagByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteCodeFlagByName', maptype.PWCHAR)
    def mapGetSiteCodeFlagByName(_name: mapsyst.WTEXT) -> int:
        return mapGetSiteCodeFlagByName_t (_name.buffer())


# Запросить - могут ли объекты карты копироваться на другие карты или экспортироваться
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteCopyFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCopyFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteCopyFlag_t (_hMap, _hSite)


# Запретить копирование объектов с карты (свойство нельзя отменить)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSetSiteHideCopy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteHideCopy', maptype.HMAP, maptype.HSITE)
    def mapSetSiteHideCopy(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapSetSiteHideCopy_t (_hMap, _hSite)


# Запросить - запрещено ли показывать параметры паспорта
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteHidePassportFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteHidePassportFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteHidePassportFlag_t (_hMap, _hSite)


# Запросить - может ли карта выводиться на печать
# Для карт, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения карты на печать
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetPrintFlag', maptype.HMAP, maptype.HSITE)
    def mapGetPrintFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetPrintFlag_t (_hMap, _hSite)


# Запросить - отражает ли карта содержимое таблицы базы данных,
# открытой на ГИС Сервере или с клиентского компьютера (через файл DBM)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если карта не отражает данные из базы данных - возвращает ноль

    mapGetDBMapFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetDBMapFlag', maptype.HMAP, maptype.HSITE)
    def mapGetDBMapFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetDBMapFlag_t (_hMap, _hSite)


# Запросить идентификатор группы карт с ограничением типа записываемых объектов
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если карта не входит в группу карт с ограничением типа
# создаваемых объектов - возвращает ноль,
# иначе - идентификатор группы карт с одним классификатором

    mapGetObjectTypeLimitIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetObjectTypeLimitIdent', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTypeLimitIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetObjectTypeLimitIdent_t (_hMap, _hSite)


# Подобрать карту для записи объекта в таблицу базы данных (DBM)
# Отображение базы данных формируется из набора таблиц (представленных
# в интерфейсе программы пользовательскими картами), каждая таблица
# может содержать определенные виды объектов
# Не зависимо от текущей пользовательской карты, на которой создается объект,
# сохранять его нужно именно в ту таблицу, которой соответствует его тип
# info  - идентификатор объекта в памяти,
#         предварительно созданного функцией mapCreateObject()
#         или mapCreateSiteObject()
# При ошибке возвращает ноль

    mapGetSiteForObjectIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteForObjectIdent', maptype.HOBJ)
    def mapGetSiteForObjectIdent(_info: maptype.HOBJ) -> maptype.HSITE:
        return mapGetSiteForObjectIdent_t (_info)


# Подобрать карту для записи объекта в таблицу базы данных (DBM)
# Отображение базы данных формируется из набора таблиц (представленных
# в интерфейсе программы пользовательскими картами), каждая таблица
# может содержать определенные виды объектов
# hMap   - идентификатор открытой карты
# hSite  - идентификатор открытой пользовательской карты
# incode - внутренний код создаваемого объекта
# При ошибке возвращает ноль

    mapGetSiteForObjectCode_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteForObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteForObjectCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _incode: int) -> maptype.HSITE:
        return mapGetSiteForObjectCode_t (_hMap, _hSite, _incode)


# Запросить - может ли карта редактироваться
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteEditFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteEditFlag_t (_hMap, _hSite)


# Установить флаг редактирования карты (0 - не редактировать)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак возможности редактирования
# Возвращает новое значение флага

    mapSetSiteEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteEditFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteEditFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteEditFlag_t (_hMap, _hSite, _flag)


# Запросить - можно ли изменить признак редактирования карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteChangeEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteChangeEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteChangeEditFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteChangeEditFlag_t (_hMap, _hSite)


# Запросить флаг масштабируемости объектов карты относительно заданного масштаба
# Если признак не установлен, то масштабирование выполняется относительно
# базового масштаба карты, установленного в паспорте
# Заданный масштаб устанавливается программно (например, в библиотеках IMLAPI)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetScalingToLevelFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetScalingToLevelFlag', maptype.HMAP, maptype.HSITE)
    def mapGetScalingToLevelFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetScalingToLevelFlag_t (_hMap, _hSite)


# Установить флаг масштабируемости объектов карты относительно заданного масштаба
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак возможности редактирования
# Возвращает новое значение флага

    mapSetScalingToLevelFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetScalingToLevelFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetScalingToLevelFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetScalingToLevelFlag_t (_hMap, _hSite, _flag)


# Запросить степень прозрачности карты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Возвращает значение от 0 (карта не видна) до 100 (карта не прозрачная)

    mapGetSiteTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteTransparent', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTransparent(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteTransparent_t (_hMap, _hSite)


# Установить степень прозрачности карты (от 0 до 100)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# transparent - степень прозрачности карты от 0 (карта не видна)
# до 100 (карта не прозрачная)
# Возвращает новое значение флага

    mapSetSiteTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteTransparent', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteTransparent(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _transparent: int) -> int:
        return mapSetSiteTransparent_t (_hMap, _hSite, _transparent)


# Запросить флаг подсветки подписей
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Возвращает значение флага

    mapGetSiteBackLightText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteBackLightText', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBackLightText(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteBackLightText_t (_hMap, _hSite)


# Установить флаг подсветки подписей
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак подсветки:
#         0 - подсветка отключена (подписи отображаются в соответствии с параметрами);
#         1 - подсветка включена (все подписи отображаются с белым контуром),
#             использовать при отображении карты поверх растров
# Возвращает новое значение флага

    mapSetSiteBackLightText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteBackLightText', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteBackLightText(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteBackLightText_t (_hMap, _hSite, _flag)


# Запросить - могут ли на карте выбираться объекты
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteInquiryFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteInquiryFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteInquiryFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteInquiryFlag_t (_hMap, _hSite)


# Установить флаг разрешения выбора объектов на карте (0 - не выбирать)
# Влияет на работу функции mapWhatObject
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# flag  - признак возможности выбора объектов в функциях типа mapWhatObject
# Возвращает новое значение флага

    mapSetSiteInquiryFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteInquiryFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteInquiryFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteInquiryFlag_t (_hMap, _hSite, _flag)


# Запросить - отображается ли карта
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# Если нет - возвращает ноль

    mapGetSiteViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteViewFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteViewFlag_t (_hMap, _hSite)


# Установить флаг отображения карты (0 - не отображать)
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты (для основной карты равен hMap)
# flag  - флаг отображения карты
# Возвращает новое значение флага

    mapSetSiteViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteViewFlag', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteViewFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteViewFlag_t (_hMap, _hSite, _flag)


# Установить номер объекта, который временно (до переоткрытия карты
# или до восстановления отображения) не будет виден на карте
# Функция применяется при редактировании отдельного (единственного) объекта
# в интерактивном режиме
# info - идентификатор скрываемого объекта

    mapHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapHideSiteObject', maptype.HOBJ)
    def mapHideSiteObject(_info: maptype.HOBJ) -> int:
        return mapHideSiteObject_t (_info)


# Восстановить отображение объекта (после mapHideSiteObject)
# Функция обнуляет номер скрываемого объекта и номер листа
# info - идентификатор восстанавливаемого объекта

    mapUnhideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnhideSiteObject', maptype.HOBJ)
    def mapUnhideSiteObject(_info: maptype.HOBJ) -> ctypes.c_void_p:
        return mapUnhideSiteObject_t (_info)


# Восстановить отображение объекта (после mapHideSiteObject)
# Функция обнуляет номер скрываемого объекта и номер листа
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты (для основной карты равен hMap)

    mapClearHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearHideSiteObject', maptype.HMAP, maptype.HSITE)
    def mapClearHideSiteObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> ctypes.c_void_p:
        return mapClearHideSiteObject_t (_hMap, _hSite)


# Запросить номер скрываемого объекта и номер листа на карте
# hMap   - идентификатор открытой карты
# hSite  - идентификатор открытой пользовательской карты (для основной карты равен hMap)
# number - указатель на поле для записи номера объекта
# list   - указатель на поле для записи номера листа
# При ошибке возвращает 0

    mapGetHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetHideSiteObject', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetHideSiteObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: ctypes.POINTER(ctypes.c_int), _list: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetHideSiteObject_t (_hMap, _hSite, _number, _list)


# Установить порядок отображения карты
# hMap  - идентификатор открытой карты
# number - номер пользовательской карты в цепочке
# order  - флаг(0 - под основной картой, 1 - над основной картой)
# При ошибке возвращает 0

    mapSetSiteViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteViewOrder', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapSetSiteViewOrder(_hMap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetSiteViewOrder_t (_hMap, _number, _order)


# Запросить порядок отображения карты
# hMap  - идентификатор открытой карты
# number - номер пользовательской карты в цепочке
# Dозвращает флаг(0 - под основной картой, 1 - над основной картой)
# При ошибке возвращает 0

    mapGetSiteViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteViewOrder', maptype.HMAP, ctypes.c_int)
    def mapGetSiteViewOrder(_hMap: maptype.HMAP, _number: int) -> int:
        return mapGetSiteViewOrder_t (_hMap, _number)


# Поменять очередность отображения карт (sit) в цепочке
# oldNumber - текущий номер файла в цепочке
# newNumber - устанавливаемый номер файла в цепочке
# При ошибке возвращает 0

    mapChangeOrderSiteShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeOrderSiteShow', maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def mapChangeOrderSiteShow(_hMap: maptype.HMAP, _oldNumber: int, _newNumber: int) -> int:
        return mapChangeOrderSiteShow_t (_hMap, _oldNumber, _newNumber)


# Запросить значения масштаба нижней и верхней границ видимости карты
# hMap  - идентификатор открытой карты
# number - номер пользовательской карты в цепочке(если number == 0, базовая карта)
# По адресу bottomScale записывается знаменатель масштаба нижней границы видимости карты
# По адресу topScale записывается знаменатель масштаба верхней границы видимости карты
# При ошибке возвращает 0

    mapGetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetSiteRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: ctypes.POINTER(ctypes.c_int), _topScale: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetSiteRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Установить значения масштаба нижней и верхней границ видимости карты
# hMap  - идентификатор открытой карты
# number - номер пользовательской карты в цепочке(если number == 0, базовая карта)
# bottomScale   - знаменатель масштаба нижней границы видимости карты
# topScale   - знаменатель масштаба верхней границы видимости карты
#              bottomScale <= topScale, иначе возвращает 0
# При ошибке возвращает 0

    mapSetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapSetSiteRangeScaleVisible(_hMap: maptype.HMAP, _number: int, _bottomScale: int, _topScale: int) -> int:
        return mapSetSiteRangeScaleVisible_t (_hMap, _number, _bottomScale, _topScale)


# Запросить длину описания паспорта карты в виде записи
# hMap  - идентификатор открытой основной карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetMapPassportRecordLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapPassportRecordLength', maptype.HMAP, maptype.HSITE)
    def mapGetMapPassportRecordLength(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetMapPassportRecordLength_t (_hMap, _hSite)


# Запросить описание паспорта карты в виде записи
# (для передачи в другой процесс,на другой компьютер ...)
# Передается описание только первого листа карты
# (у пользовательской карты он всегда один)
# Размер буфера должен быть не менее, чем указано
# в mapGetMapPassportRecordLength()
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# buffer - указатель на запись для описания паспорта карты
# size   - размер записи
# При ошибке возвращает ноль

    mapGetMapPassportRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapPassportRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int)
    def mapGetMapPassportRecord(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetMapPassportRecord_t (_hMap, _hSite, _buffer, _size)


# Создать карту по записи паспорта карты
# Запись создается при вызове mapGetMapPassportRecord()
# hMap  - идентификатор открытой основной карты
# mapname - имя файла паспорта (#.map или #.sit)
# rscname - имя файла классификатора (#.rsc) !
# Если hMap = 0, возвращает идентификатор
# открытой карты HMAP (см. mapCreateMap() в mapapi.h)
# При ошибке возвращает ноль

    mapPutMapPassportRecord_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapPutMapPassportRecord', maptype.HMAP, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapPutMapPassportRecord(_hMap: maptype.HMAP, _mapname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _buffer: ctypes.c_char_p, _size: int) -> maptype.HSITE:
        return mapPutMapPassportRecord_t (_hMap, _mapname, _rscname, _buffer, _size)

    mapPutMapPassportRecordUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapPutMapPassportRecordUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int)
    def mapPutMapPassportRecordUn(_hMap: maptype.HMAP, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _buffer: ctypes.c_char_p, _size: int) -> maptype.HSITE:
        return mapPutMapPassportRecordUn_t (_hMap, _mapname.buffer(), _rscname.buffer(), _buffer, _size)


# Запросить объект "Рамка листа"
# hmap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# list  - номер листа (c 1)
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetSiteListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListFrameObject', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HOBJ)
    def mapGetSiteListFrameObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _info: maptype.HOBJ) -> int:
        return mapGetSiteListFrameObject_t (_hmap, _hsite, _list, _info)


# Запросить габариты объекта "Рамка листа" (если рамки нет -
# заполняются по габаритам из паспорта)
# hmap  - идентификатор открытых данных
# hSite -  идентификатор открытой пользовательской карты
# list  - номер листа
# frame - указатель на габариты листа в метрах
# При ошибке возвращает ноль

    mapGetSiteListFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListFrame', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteListFrame(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetSiteListFrame_t (_hMap, _hSite, _list, _frame)


# Cоздать пустой объект пользовательской карты
# hMap  - идентификатор открытой основной карты
# hSite - идентификатор открытой пользовательской карты, в которой будет расположен
#         создаваемый объект (для первой карты равен hMap)
# kind  - формат метрики
# text  - признак метрики с текстом (для объектов типа "подпись")
# pointcount - зарезервировать память под число точек (ускоряет первичное заполнение метрики из массива)
# После вызова функций типа What...() и Seek...() все параметры
# полученного объекта могут измениться (text,kind и т.п.)
# Для каждого полученного и больше не используемого
# идентификатора HOBJ необходим вызов функции mapFreeObject()
# При ошибке возвращает ноль

    mapCreateSiteObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateSiteObjectEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapCreateSiteObjectEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _kind: int = maptype.IDDOUBLE2, _text: int = 0, _pointcount: int = 0) -> maptype.HOBJ:
        return mapCreateSiteObjectEx_t (_hMap, _hSite, _kind, _text, _pointcount)

    mapCreateSiteObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateSiteObject', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapCreateSiteObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _kind: int = maptype.IDDOUBLE2, _text: int = 0) -> maptype.HOBJ:
        return mapCreateSiteObject_t (_hMap, _hSite, _kind, _text)


# Определить идентификатор открытого документа
# для заданного объекта
# При ошибке возвращает ноль

    mapGetObjectDocIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapGetObjectDocIdent', maptype.HOBJ)
    def mapGetObjectDocIdent(_hObj: maptype.HOBJ) -> maptype.HMAP:
        return mapGetObjectDocIdent_t (_hObj)


# Определить идентификатор открытой пользовательской карты
# для заданного объекта
# hMap  - идентификатор открытой основной карты
# hObj  - идентификатор объекта пользовательской карты
# При ошибке возвращает ноль

    mapGetObjectSiteIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetObjectSiteIdent', maptype.HMAP, maptype.HOBJ)
    def mapGetObjectSiteIdent(_hMap: maptype.HMAP, _hObj: maptype.HOBJ) -> maptype.HSITE:
        return mapGetObjectSiteIdent_t (_hMap, _hObj)


# Перенести объект на другую карту (пересчитать координаты и
# заменить ссылку в объекте на карту)
# При переносе объекта выполняется перекодировка объекта
# для нового классификатора, если код не найден -
# он устанавливается в ноль, прежнее значение
# сохраняется в семантике (код 32800).
# (для замены вызывается mapRegisterObject())
# Метрика преобразуется в соответствии с типом карты
# hSite - идентификатор открытой пользовательской карты
# hObj  - идентификатор объекта пользовательской карты
# hMap  - идентификатор открытой основной карты
# Объект на исходной карте при этом не удаляется,
# для записи объекта в новой карте необходимо вызвать mapCommitObject
# При ошибке возвращает ноль

    mapSetObjectMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetObjectMap', maptype.HOBJ, maptype.HSITE)
    def mapSetObjectMap(_info: maptype.HOBJ, _hSite: maptype.HSITE) -> int:
        return mapSetObjectMap_t (_info, _hSite)

    mapChangeObjectMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeObjectMap', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapChangeObjectMap(_hObj: maptype.HOBJ, _hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapChangeObjectMap_t (_hObj, _hMap, _hSite)


# Очистить содержание объекта и разместить его на заданной карте
# hObj  - идентификатор объекта пользовательской карты
# hMap  - идентификатор открытой основной карты
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapClearSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapClearSiteObject', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapClearSiteObject(_info: maptype.HOBJ, _hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapClearSiteObject_t (_info, _hMap, _hSite)


# Обновить размеры пользовательской карты и габариты района
# Данная функция может применяться при создании карты, когда объектов еще
# нет и необходимо задать пустую область для окна карты
# При создании или обновлении объектов габариты пользовательской карты
# будут автоматически пересчитаны
# После вызова этой функции необходимо согласовать параметры
# скроллинга подобно масштабированию карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# dframe - координаты прямоугольной области района
# place  - система координат (PP_PLANE, PP_GEO, PP_PICTURE)
# При ошибке возвращает ноль

    mapSetSiteBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapSetSiteBorder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapSetSiteBorder_t (_hMap, _hSite, _dframe, _place)


# Запросить габариты пользовательской карты в системе координат документа
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# list   - номер листа для многолистовой карты или 0
# dframe - координаты прямоугольной области района
# place  - система координат (PP_PLANE, PP_GEO, PP_PICTURE)
# При ошибке возвращает ноль

    mapGetSiteBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteBorderEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetSiteBorderEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetSiteBorderEx_t (_hMap, _hSite, _list, _dframe, _place)

    mapGetSiteBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def mapGetSiteBorder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetSiteBorder_t (_hMap, _hSite, _dframe, _place)


# Запросить габариты пользовательской карты в системе координат карты в метрах
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# dframe - координаты прямоугольной области района
# При ошибке возвращает ноль

    mapGetSiteMapBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteMapBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteMapBorder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetSiteMapBorder_t (_hMap, _hSite, _dframe)


# Запросить объект "Рамка листа"
# hmap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# list  - номер листа (c 1)
# info  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetSiteListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListFrameObject', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.HOBJ)
    def mapGetSiteListFrameObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _info: maptype.HOBJ) -> int:
        return mapGetSiteListFrameObject_t (_hmap, _hsite, _list, _info)


# Запросить габариты объекта "Рамка листа" (если рамки нет -
# заполняются по габаритам из паспорта)
# hmap  - идентификатор открытых данных
# hSite  - идентификатор открытой пользовательской карты
# list  - номер листа
# frame - указатель на габариты листа в метрах
# При ошибке возвращает ноль

    mapGetSiteListFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListFrame', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteListFrame(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetSiteListFrame_t (_hMap, _hSite, _list, _frame)


# Запросить высоту сечения в метрах для листа из паспорта
# hmap  - идентификатор открытых данных
# hSite  - идентификатор открытой пользовательской карты
# list  - номер листа
# При ошибке возвращает ноль

    mapGetSiteListReliefHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteListReliefHeight', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteListReliefHeight(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int) -> float:
        return mapGetSiteListReliefHeight_t (_hMap, _hSite, _list)


# Заменить файл классификатора и перекодировать карту
# Поддерживается только для карт, размещенных локально и
# доступных на запись
# hMap    - идентификатор открытой основной карты
# hSite   - идентификатор открытой пользовательской карты
# rscname - имя нового классификатора
# При ошибке возвращает ноль

    mapChangeSiteRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapChangeSiteRsc', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapChangeSiteRsc(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _rscname: mapsyst.WTEXT) -> int:
        return mapChangeSiteRsc_t (_hMap, _hSite, _rscname.buffer())


# Запросить имя классификатора из паспорта карты
# hMap    - идентификатор открытой основной карты
# hSite   - идентификатор открытой пользовательской карты
# rscname - строка для записи имени классификатора без пути
# size    - размер строки для записи имени
# При ошибке возвращает ноль

    mapGetSiteRscName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteRscName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteRscName(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteRscName_t (_hMap, _hSite, _rscname.buffer(), _size)


# Запросить состояние (стиль) классификатора из паспорта карты
# При смене стиля могут быть изменены внутренние коды объектов
# Для проверки соответствия открытых данных классификатору можно сравнить этот
# показатель со значением в самом классификаторе (см. mapGetRscStyle)
# hMap    - идентификатор открытой основной карты
# hSite   - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteRscStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteRscStyle', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRscStyle(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteRscStyle_t (_hMap, _hSite)


# Установить порядок записи объектов на карту в цепочку отображения в порядке
# их поступления (например, карта содержит один вид объектов)
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# flag  - признак последовательной записи и отображения объектов (0/1)
# При ошибке возвращает ноль

    mapSetSiteDirectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteDirectOrder', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteDirectOrder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteDirectOrder_t (_hMap, _hSite, _flag)


# Запросить флаг записи объектов на карту в цепочку отображения в порядке
# их поступления (например, карта содержит один вид объектов)
# hMap  - идентификатор открытых данных
# hSite  - идентификатор открытой пользовательской карты
# При ошибке и выключенном режиме "прямой" записи возвращает ноль

    mapGetSiteDirectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteDirectOrder', maptype.HMAP, maptype.HSITE)
    def mapGetSiteDirectOrder(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteDirectOrder_t (_hMap, _hSite)


# Запросить список изменившихся на ГИС Сервере объектов и
# обновить описание объектов в памяти
# Возвращает идентификатор списка объектов
# После обработки списка объектов он должен быть удален функцией
# mapFreeChangedObjectList
# hMap        - идентификатор открытой основной карты
# hSite       - идентификатор открытой пользовательской карты
# maxcount    - максимальное число измененных объектов, которое может быть в списке,
#               если изменилось больше объектов, то список не формируется,
#               а карта обновляется с ГИС Сервера полностью (обычно равен 1000)
#               mapGetChangedObjectCount в этом случае возвращает "-1"
# skipaction  - код транзакции, который не должен обрабатываться на ГИС Сервере
#               при заполнении списка изменившихся объектов
# checkaction - номер транзакции, с которой должен формироваться список изменившихся
#               объектов. Это может быть значение, которое вернула функция
#               mapGetChangedObjectAction или 0. Ноль означает формирование
#               списка для текущего состояния (крайней транзакции, запомненной
#               в предыдущем вызове обновления). Но вызов mapAdjust тоже обновляет
#               состояние карты и номер последней транзакции в памяти карты.
# При ошибке возвращает ноль

    mapGetChangedObjectListAndUpdate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetChangedObjectListAndUpdate', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetChangedObjectListAndUpdate(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _maxcount: int, _skipaction: int, _checkaction = 0) -> ctypes.c_void_p:
        return mapGetChangedObjectListAndUpdate_t (_hMap, _hSite, _maxcount, _skipaction, _checkaction)


# Запросить число объектов в списке
# Число изменившихся объектов может быть нулевым
# Если число изменившихся объектов больше предельного значения maxcount,
# заданого в функции mapGetChangedObjectListAndUpdate, то возвращается
# значение -1 и карта в памяти обновляется полностью
# Дополнительную информацию можно получить из журнала транзакций
# функциями из logapi.h

    mapGetChangedObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectCount', ctypes.c_void_p)
    def mapGetChangedObjectCount(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectCount_t (_hObjlist)


# Запросить номер последней транзакции, по которой заполнен список объектов
# При ошибке возвращает ноль

    mapGetChangedObjectAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectAction', ctypes.c_void_p)
    def mapGetChangedObjectAction(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectAction_t (_hObjlist)


# Запросить номер последней транзакции в журнале, в момент формирования списка
# Номер последней транзакции может быть больше номера обработанной транзакции,
# если список слишком большой
# В этом случае нужно запросить следующую порцию обновлений
# При ошибке возвращает ноль

    mapGetChangedObjectTotalAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectTotalAction', ctypes.c_void_p)
    def mapGetChangedObjectTotalAction(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectTotalAction_t (_hObjlist)


# Запросить описание изменившегося объекта
# При ошибке возвращает ноль

    mapGetChangedObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObject', ctypes.c_void_p, ctypes.c_int, maptype.HMAP, maptype.HSITE, maptype.HOBJ)
    def mapGetChangedObject(_hObjlist: ctypes.c_void_p, _number: int, _hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ) -> int:
        return mapGetChangedObject_t (_hObjlist, _number, _hMap, _hSite, _info)


# Запросить описание изменений объекта
# Возвращает признак изменений объекта:
# 1 - обновлена семантика, 2 - обновлена метрика
# 3 - обновлена метрика и семантика,
# 4 - объект создан, 8 - объект удален, 16 - объект восстановлен после удаления
# Нулевое значение может означать изменение кода объекта,
# границ видимости, масштабируемости

    mapGetChangedObjectState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectState', ctypes.c_void_p, ctypes.c_int)
    def mapGetChangedObjectState(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectState_t (_hObjlist, _number)


# Запросить код вида объекта, который был до обновления
# Возвращает внутренний код объекта в классификаторе
# У графических объектов код равен нулю

    mapGetChangedObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectCode', ctypes.c_void_p, ctypes.c_int)
    def mapGetChangedObjectCode(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectCode_t (_hObjlist, _number)


# Запросить уникальный номер объекта в листе, который был до обновления
# В штатных ситуациях номер объекта не меняется при редактировании карты
# Возвращает идентификационный номер объекта (mapObjectKey)

    mapGetChangedObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetChangedObjectKey', ctypes.c_void_p, ctypes.c_int)
    def mapGetChangedObjectKey(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectKey_t (_hObjlist, _number)


# Освободить ресурсы, занятые списком объектов, созданным
# функцией mapGetChangedObjectListAndUpdate

    mapFreeChangedObjectList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeChangedObjectList', ctypes.c_void_p)
    def mapFreeChangedObjectList(_hObjlist: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeChangedObjectList_t (_hObjlist)


# Запросить дату и время по Гринвичу обновления карты
# Если возвращаются нулевые значения, то карта после создания не редактировалась
# hMap    - идентификатор открытой основной карты
# hSite   - идентификатор открытой пользовательской карты
# list    - номер листа карты
# date    - поле для записи даты в виде числа формата YYYYMMDD по Гринвичу
# time    - поле для записи числа секунд с 0 часов
# При ошибке возвращает ноль

    mapGetSiteDateAndTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteDateAndTime', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def mapGetSiteDateAndTime(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _date: ctypes.POINTER(ctypes.c_int), _time: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapGetSiteDateAndTime_t (_hMap, _hSite, _list, _date, _time)


# Удалить документ (произвольный файл) на сервере
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# При ошибке возвращает ноль

    mapDeleteSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapDeleteSiteDocumentUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _alias: mapsyst.WTEXT) -> int:
        return mapDeleteSiteDocumentUn_t (_hMap, _hSite, _alias.buffer())


# Считать документ на сервере
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# name   - полный путь к считанному документу, строка заполняется
#          автоматически при считывании документа, имя документа и
#          дата редактирования устанавливаются такими, какими они были
#          при записи в mapSaveSiteDocument.
# Например: HOST#WorkServer#ALIAS#Моя_Карта#DOC#MyFolder#schema.png
# size   - размер буфера в байтах для записи пути (не менее 520 байт)
# При успешном выполнении возвращает имя считанного файла документа в поле name
# При ошибке возвращает ноль

    mapReadSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapReadSiteDocumentUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapReadSiteDocumentUn_t (_hMap, _hSite, _alias.buffer(), _name.buffer(), _size)


# Считать информацию о документе на сервере
# alias - алиас документа на сервере
# time  - время обновления файла в хранилище
# size  - размер файла документа
# При успешном выполнении возвращает размер исходного файла и время его обновления
# в хранилище
# При ошибке возвращает ноль

    mapReadSiteDocumentInfoUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapReadSiteDocumentInfoUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.SYSTEMTIME), ctypes.POINTER(ctypes.c_int64))
    def mapReadSiteDocumentInfoUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _alias: mapsyst.WTEXT, _time: ctypes.POINTER(maptype.SYSTEMTIME), _size: ctypes.POINTER(ctypes.c_int64)) -> int:
        return mapReadSiteDocumentInfoUn_t (_hMap, _hSite, _alias.buffer(), _time, _size)


# Сохранить документ на сервере
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# name   - полный путь к сохраняемому документу (один файл любого размера)
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#"),
#          строка формируется сервером и заполняется при сохранении документа
# size   - размер буфера для записи алиаса (не менее 260 символов)
# При успешном выполнении возвращает алиас документа на сервере
# При ошибке возвращает ноль

    mapSaveSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSaveSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapSaveSiteDocumentUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: mapsyst.WTEXT, _alias: mapsyst.WTEXT, _size: int) -> int:
        return mapSaveSiteDocumentUn_t (_hMap, _hSite, _name.buffer(), _alias.buffer(), _size)


# Запросить путь к кэшу документа на клиенте
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# name   - полный путь к документу
# size   - размер буфера для записи пути (не менее 260 символов)
# При успешном выполнении возвращает имя кэша файла документа в поле name
# Операция чтения не выполняется, файл может отсутствовать
# При успешном выполнении возвращает ненулевое значение,
# если файл имеется в кэш - возвращает положительное значение, иначе - отрицательное
# При ошибке возвращает ноль

    mapGetSiteDocumentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteDocumentNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteDocumentNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteDocumentNameUn_t (_hMap, _hSite, _alias.buffer(), _name.buffer(), _size)


# Запросить - можно ли сохранить документ с картой
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# Если карта размещена на сервере и может редактироваться,
# то в ней есть хранилище документов
# При ошибке возвращает ноль

    mapIsSiteDocumentStorage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteDocumentStorage', maptype.HMAP, maptype.HSITE)
    def mapIsSiteDocumentStorage(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteDocumentStorage_t (_hMap, _hSite)


# Освободить память с прочитанным документом
# memory - адрес памяти, полученной при вызове mapGetDocumentFromSitz/mapGetDocumentFromSitzEx

    mapFreeDocumentFromSitz_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeDocumentFromSitz', ctypes.c_char_p)
    def mapFreeDocumentFromSitz(_memory: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeDocumentFromSitz_t (_memory)


# Отобразить образец вида объекта по номеру записи
# в классификаторе объектов (incode)
# Используется в диалогах выбора вида объекта
# hdc   - идентификатор контекста устройства вывода,
# rect  - координаты фрагмента карты (Draw)
# в изображении (Picture).
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hDC    - идентификатор контекста устройства вывода
# rect   - область прорисовки
# incode - внутренний код объекта
# text   - текст подписи или ноль
# factor - коэффициент масштабируемости изображения 50, 100, 200...
# semvalue - запись семантики
# При ошибке возвращает ноль

    mapPaintExampleSiteObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleSiteObjectPro', maptype.HMAP, maptype.HSITE, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.SEMANTIC))
    def mapPaintExampleSiteObjectPro(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _text: mapsyst.WTEXT, _factor: int, _semvalue: ctypes.POINTER(maptype.SEMANTIC)) -> int:
        return mapPaintExampleSiteObjectPro_t (_hMap, _hSite, _hdc, _rect, _incode, _text.buffer(), _factor, _semvalue)

    mapPaintExampleSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleSiteObject', maptype.HMAP, maptype.HSITE, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_int)
    def mapPaintExampleSiteObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int) -> int:
        return mapPaintExampleSiteObject_t (_hMap, _hSite, _hdc, _rect, _incode)

    mapPaintExampleSiteObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPaintExampleSiteObjectEx', maptype.HMAP, maptype.HSITE, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_int, ctypes.c_int)
    def mapPaintExampleSiteObjectEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _factor: int) -> int:
        return mapPaintExampleSiteObjectEx_t (_hMap, _hSite, _hdc, _rect, _incode, _factor)


# Запросить состав отображаемых объектов пользовательской карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)
# select - идентификатор контекста поиска/отображения
# в который будут помещены текущие условия отображения
# см. mapCreateMapSelectContext(...)
# При ошибке возвращает ноль

    mapGetSiteViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteViewSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _select: maptype.HSELECT) -> int:
        return mapGetSiteViewSelect_t (_hMap, _hSite, _select)


# Установить состав отображаемых объектов
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)
# select - идентификатор контекста поиска/отображения

    mapSetSiteViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteViewSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _select: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSetSiteViewSelect_t (_hMap, _hSite, _select)


# Запросить номер состояния услвоий отображения карты
# При обновлении условий номер состояния меняется
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)
# При ошибке возвращает ноль

    mapGetSiteViewSelectState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteViewSelectState', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewSelectState(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteViewSelectState_t (_hMap, _hSite)


# Запросить яркость карты (от -16 до +16)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)

    mapGetSiteBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteBright', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBright(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteBright_t (_hMap, _hSite)


# Установить яркость карты (от -16 до +16)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)

    mapSetSiteBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteBright', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteBright(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _bright: int) -> int:
        return mapSetSiteBright_t (_hMap, _hSite, _bright)


# Запросить контрастность  (от -16 до +16)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)

    mapGetSiteContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteContrast', maptype.HMAP, maptype.HSITE)
    def mapGetSiteContrast(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteContrast_t (_hMap, _hSite)


# Установить контрастность (от -16 до +16)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой карты hSite = hMap)

    mapSetSiteContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteContrast', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteContrast(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _contrast: int) -> int:
        return mapSetSiteContrast_t (_hMap, _hSite, _contrast)


# Запросить параболическую яркость
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteGamma', maptype.HMAP, maptype.HSITE)
    def mapGetSiteGamma(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteGamma_t (_hMap, _hSite)


# Установить параболическую яркость
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# gamma  - параболическая яркость
# При ошибке возвращает ноль

    mapSetSiteGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteGamma', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteGamma(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _gamma: int) -> int:
        return mapSetSiteGamma_t (_hMap, _hSite, _gamma)


# Запросить число цветов в текущей палитре карты
# Обычно 16 или 32
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteColorsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteColorsCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteColorsCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteColorsCount_t (_hMap, _hSite)


# Запросить текущую палитру карты (с учетом яркости/контрастности)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# При ошибке возвращает ноль

    mapGetSitePalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePalette', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapGetSitePalette(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetSitePalette_t (_hMap, _hSite, _colors, _count)


# Запросить текущую палитру карты (без учета яркости/контрастности)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# При ошибке возвращает ноль

    mapGetSiteColors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteColors', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapGetSiteColors(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetSiteColors_t (_hMap, _hSite, _colors, _count)


# Установить текущую палитру карты
# Если colors равно 0, устанавливается палитра из классификатора
# (палитра классификатора не меняется, изменения будут временными)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# При ошибке возвращает ноль

    mapSetSiteColors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteColors', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapSetSiteColors(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapSetSiteColors_t (_hMap, _hSite, _colors, _count)


# Установить текущую палитру в карте из классификатора
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# number - номер палитры в класификаторе
# При ошибке возвращает ноль

    mapSetSitePaletteByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSitePaletteByNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int) -> int:
        return mapSetSitePaletteByNumber_t (_hMap, _hSite, _number)


# Запросить палитру из классификатора по номеру
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# number - номер палитры в класификаторе
# При ошибке возвращает ноль

    mapGetSitePaletteByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int)
    def mapGetSitePaletteByNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetSitePaletteByNumber_t (_hMap, _hSite, _colors, _count, _number)


# Запросить номер текущей палитры в карте
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSitePaletteNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePaletteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSitePaletteNumber_t (_hMap, _hSite)


# Запросить число палитр в классификаторе карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSitePaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePaletteCount', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSitePaletteCount_t (_hMap, _hSite)


# Запросить название палитры по номеру
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSitePaletteName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePaletteName', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSitePaletteName(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSitePaletteName_t (_hMap, _hSite, _number, _name.buffer(), _size)


# Запросить условия поиска активных объектов по пользовательской карте
# (для фоновой hSite = hMap)
# Активные объекты - доступны для интерактивного выбора (оператором)
# Выбор выполняется функцией mapWhatActiveObject()
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - идентификатор контекста поиска/отображения
#          в который будут помещены текущие условия поиска
#          см. mapCreateMapSelectContext(...)
# При ошибке возвращает ноль

    mapGetSiteActiveSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteActiveSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapGetSiteActiveSelect_t (_hMap, _hSite, _hSelect)


# Установить условия поиска активных объектов для пользовательской карты
# (для фоновой hSite = hMap)
# Активные объекты - доступны для интерактивного выбора (оператором)
# Выбор выполняется функцией mapWhatActiveObject()
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - идентификатор контекста поиска,
#          который содержит устанавливаемые условия поиска
# При ошибке возвращает ноль

    mapSetSiteActiveSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteActiveSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapSetSiteActiveSelect_t (_hMap, _hSite, _hSelect)


# Запросить условия поиска объектов по пользовательской карте
# (для фоновой hSite = hMap)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - идентификатор контекста поиска/отображения
#          в который будут помещены текущие условия поиска
#          см. mapCreateMapSelectContext(...)
# При ошибке возвращает ноль

    mapGetSiteSeekSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteSeekSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteSeekSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapGetSiteSeekSelect_t (_hMap, _hSite, _hSelect)


# Установить условия поиска объектов для пользовательской карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# (для фоновой (основной) карты hSite = hMap)
# hSelect - идентификатор контекста поиска,
#          который содержит устанавливаемые условия поиска
# При ошибке возвращает ноль

    mapSetSiteSeekSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteSeekSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteSeekSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapSetSiteSeekSelect_t (_hMap, _hSite, _hSelect)


# Поиск объекта по уникальному номеру на карте
# info     - идентификатор существующего объекта,
# созданного функцией CreateObject() или CreateSiteObject(),
# в котором будет размещен результат поиска.
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# key   - идентификатор объекта на карте
# При ошибке возвращает ноль

    mapSeekSiteObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int)
    def mapSeekSiteObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _key: int) -> maptype.HOBJ:
        return mapSeekSiteObject_t (_hMap, _hSite, _info, _key)


# Поиск объектов по заданным условиям среди всех объектов
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# info     - идентификатор существующего объекта,
# созданного функцией mapCreateObject() или mapCreateSiteObject(),
# в котором будет размещен результат поиска,
# hSelect - условия поиска объекта,
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# skip - число найденных объектов, которые нужно пропустить перед выдачей результата
# Если объект не найден - возвращает ноль

    mapSeekSiteSelectObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_int, ctypes.c_int)
    def mapSeekSiteSelectObjectEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _select: maptype.HSELECT, _flag: int, _skip: int) -> maptype.HOBJ:
        return mapSeekSiteSelectObjectEx_t (_hMap, _hSite, _info, _select, _flag, _skip)

    mapSeekSiteSelectObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteSelectObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _hSelect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        return mapSeekSiteSelectObject_t (_hMap, _hSite, _info, _hSelect, _flag)


# Поиск ближайшего объекта по заданным условиям среди всех объектов
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты в которой ищется объект,
# info   - идентификатор существующего объекта,
# созданного функцией mapCreateObject() или mapCreateSiteObject(),
# в котором будет размещен результат поиска,
# point  - координаты точки в метрах в системе карты; среди всех
# подходящих объектов ищется ближайший к заданной точке.
# target   - координаты ближайшей виртуальной точки на контуре объекта
#            в метрах документа;
# hSelect - условия поиска объекта,
# flag     - дополнительные условия поиска объектов: WO_CANCEL,
#            WO_VISUAL; флажки типа WO_FIRST, WO_NEXT не учитываются
# Если объект не найден - возвращает ноль

    mapSeekSiteSelectNearestObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectNearestObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteSelectNearestObjectEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT), _hSelect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        return mapSeekSiteSelectNearestObjectEx_t (_hMap, _hSite, _info, _point, _target, _hSelect, _flag)

    mapSeekSiteSelectNearestObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectNearestObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekSiteSelectNearestObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _hSelect: maptype.HSELECT, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> maptype.HOBJ:
        return mapSeekSiteSelectNearestObject_t (_hMap, _hSite, _info, _hSelect, _point)


# Запросить число объектов, удовлетворяющих условиям поиска
# для функции mapSeekSiteSelectObject (выполняет внутренний перебор объектов)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - условия поиска объекта
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteSelectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSiteSelectCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteSelectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapSeekSiteSelectCount_t (_hMap, _hSite, _hSelect)


# Запросить число объектов, удовлетворяющих условиям поиска в заданном листе
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - условия поиска объекта
# list    - номер листа для многолистовой карты, с 1
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteSelectCountForList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSiteSelectCountForList', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteSelectCountForList(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT, _list: int) -> int:
        return mapSeekSiteSelectCountForList_t (_hMap, _hSite, _hSelect, _list)


# Поиск объектов по заданным условиям среди отображаемых объектов
# (пересечение заданных условий с условиями отображения)
# hMap     - идентификатор открытой основной карты
# hSite    - идентификатор открытой пользовательской карты
# info     - идентификатор существующего объекта,
# созданного функцией mapCreateObject() или mapCreateSiteObject(),
# в котором будет размещен результат поиска,
# hSelect - условия поиска объекта,
# flag - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# Если объект не найден - возвращает ноль

    mapSeekSiteViewObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteViewObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteViewObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _hSelect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        return mapSeekSiteViewObject_t (_hMap, _hSite, _info, _hSelect, _flag)


# Запросить число объектов, удовлетворяющих условиям поиска
# для функции mapSeekSiteViewObject (выполняет внутренний перебор объектов)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# hSelect - условия поиска объекта
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteViewCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSeekSiteViewCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteViewCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hSelect: maptype.HSELECT) -> int:
        return mapSeekSiteViewCount_t (_hMap, _hSite, _hSelect)


# Проверить наличие кода семантики на карте
# hMap, hSite - идентификатор карты
# code - код семантики
# В случае отсутствия возвращает ноль

    mapCheckExistSemanticInSheetByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCheckExistSemanticInSheetByCode', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapCheckExistSemanticInSheetByCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _code: int) -> int:
        return mapCheckExistSemanticInSheetByCode_t (_hMap, _hSite, _list, _code)


# Проверить что хэш семантик готов
# hMap, hSite - идентификатор карты
# Если не готов - возвращает "-1"
# При ошибке возвращает ноль

    mapIsSemanticHashReady_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSemanticHashReady', maptype.HMAP, maptype.HSITE)
    def mapIsSemanticHashReady(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSemanticHashReady_t (_hMap, _hSite)


# Запросить идентификатор карты, для которой созданы/заполнены условия поиска
# hMap   - идентификатор открытой основной карты
# hSelect - условия поиска объекта
# При ошибке возвращает ноль

    mapGetSiteIdentForSelect_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentForSelect', maptype.HMAP, maptype.HSELECT)
    def mapGetSiteIdentForSelect(_hMap: maptype.HMAP, _hSelect: maptype.HSELECT) -> maptype.HSITE:
        return mapGetSiteIdentForSelect_t (_hMap, _hSelect)


# Запросить число отображаемых объектов на карте
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке или отсутствии объектов возвращает ноль

    mapGetViewObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetViewObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetViewObjectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetViewObjectCount_t (_hMap, _hSite)


# Запросить число отображаемых объектов в документе
# hMap   - идентификатор открытой основной карты
# При ошибке или отсутствии объектов возвращает ноль

    mapGetTotalViewObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetTotalViewObjectCount', maptype.HMAP)
    def mapGetTotalViewObjectCount(_hMap: maptype.HMAP) -> int:
        return mapGetTotalViewObjectCount_t (_hMap)


# Опросить наличие списка объектов в контексте условий поиска/отображения карты
# Список объектов содержит номер листа и номер объекта
# в листе
# Если список объектов не установлен,возвращает ноль

    mapIsSiteSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsSiteSeekSample', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSeekSample(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsSiteSeekSample_t (_hMap, _hSite)


# Запросить базовый масштаб карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteScale', maptype.HMAP, maptype.HSITE)
    def mapGetSiteScale(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteScale_t (_hMap, _hSite)


# Изменить базовый масштаб пользовательской карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При отображении в базовом масштабе пользовательской карты
# размер условных знаков на карте будет соответствовать их размеру
# в классификаторе RSC
# При ошибке возвращает ноль

    mapSetSiteScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteScale', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteScale(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _scale: int) -> int:
        return mapSetSiteScale_t (_hMap, _hSite, _scale)

    mapSetSiteNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteNameEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetSiteNameEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: mapsyst.WTEXT) -> int:
        return mapSetSiteNameEx_t (_hMap, _hSite, _name.buffer())


# Запросить главное название карты (листа)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# size   - размер строки для размещения результата в байтах
# При ошибке возвращает 0

    mapGetSiteNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteNameUn_t (_hMap, _hSite, _name.buffer(), _size)


# Запросить тип карты (см. maptype.h)
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteType(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteType_t (_hMap, _hSite)


# Запросить прямоугольные координаты габаритов карты
# в метрах (система координат PLANE)
# X - снизу вверх, Y - слева направо
# т.1 - нижний левый угол,
# т.2 - верхний правый
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты

    mapGetSiteX1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteX1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX1(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> float:
        return mapGetSiteX1_t (_hMap, _hSite)

    mapGetSiteY1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteY1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY1(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> float:
        return mapGetSiteY1_t (_hMap, _hSite)

    mapGetSiteX2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteX2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX2(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> float:
        return mapGetSiteX2_t (_hMap, _hSite)

    mapGetSiteY2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteY2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY2(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> float:
        return mapGetSiteY2_t (_hMap, _hSite)


# Запросить количество объектов в пользовательской карте
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteObjectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteObjectCount_t (_hMap, _hSite)


# Запросить количество объектов в пользовательской карте, исключая удаленные
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteRealObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteRealObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRealObjectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteRealObjectCount_t (_hMap, _hSite)


# Запросить количество удаленных объектов в листе карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# list   - номер листа (для совместимости с многолистовыми картами)
# При ошибке возвращает ноль

    mapGetSiteDeleteObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteDeleteObjectCount', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteDeleteObjectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int) -> int:
        return mapGetSiteDeleteObjectCount_t (_hMap, _hSite, _list)


# Запросить идентификатор нового объекта, который будет создан на карте следующим
# Идентификатор созданного объекта может быть запрошен функцией mapObjectKey
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# list   - номер листа (для совместимости с многолистовыми картами)
# При ошибке возвращает ноль

    mapGetSiteNewObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteNewObjectKey', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteNewObjectKey(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list = 1) -> int:
        return mapGetSiteNewObjectKey_t (_hMap, _hSite, _list)


# Запросить общее число листов на карте
# hMap   - идентификатор открытой основной карты (данных)
# hSite  - идентификатор открытой пользовательской карты (может быть равен hMap
#          для доступа к основной карте)
# При ошибке возвращает ноль

    mapGetSiteListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteListCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteListCount(_hmap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteListCount_t (_hmap, _hSite)


# Удалить указанный лист карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# list - номер листа (с 1)
# При ошибке возвращает ноль

    mapDeleteSiteList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteList', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapDeleteSiteList(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int) -> int:
        return mapDeleteSiteList_t (_hMap, _hSite, _list)


# Изменить порядковый номер листа карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# oldnumber - номер листа карты
# newnumber - новое положение листа карты в паспорте
# При ошибке возвращает ноль

    mapSetSiteListOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteListOrder', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSetSiteListOrder(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _oldnumber: int, _newnumber: int) -> int:
        return mapSetSiteListOrder_t (_hMap, _hSite, _oldnumber, _newnumber)


# Запросить количество объектов в листе
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты (может быть равен hMap
#          для доступа к основной карте)
# number - номер листа карты (для пользовательской карты обычно равен 1)
# При ошибке возвращает ноль

    mapGetSiteObjectCountInList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteObjectCountInList', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteObjectCountInList(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number = 1) -> int:
        return mapGetSiteObjectCountInList_t (_hMap, _hSite, _number)


# Запросить паспортные данные векторной карты
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# Структуры MAPREGISTEREX, LISTREGISTER, SHEETNAMES описаны в mapcreat.h
# sheetnumber - номер листа карты (c 1)
# При ошибке возвращает ноль

    mapGetSiteInfoEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteInfoEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_int)
    def mapGetSiteInfoEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnumber: int) -> int:
        return mapGetSiteInfoEx_t (_hMap, _hSite, _mapreg, _listreg, _sheetnumber)

    mapGetSiteInfoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteInfoPro', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), ctypes.c_int)
    def mapGetSiteInfoPro(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _sheetnumber: int) -> int:
        return mapGetSiteInfoPro_t (_hMap, _hSite, _mapreg, _listreg, _sheetnames, _sheetnumber)


# Обновить паспортные данные векторной карты
# При смене параметров проекции карта
# будет трансформирована в соответствии
# с новыми параметрами проекции из MAPREGISTEREX,
# если параметр transform не равен нулю
# Для листа карты можно изменить название, номенклатуру и метаданные
# (LISTREGISTEREX), координаты рамки (если территория карты
# ограничена рамкой) пересчитываются автоматически.
# Время выполнения функции соответствует времени выполнения
# трансформировании карты (при смене параметров проекции)
# При выполнении трансформирования посылается сообщение
# WM_PROGRESSBAR (maptype.h) окну (mapSetHandleForMessage)
# Структуры MAPREGISTER и LISTREGISTER описаны в mapcreat.h
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# sheetnumber - номер листа карты (c 1)
# type - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# parm - параметры локального преобразования координат или 0
# transform   - признак пересчета координат при смене параметров
#               0 - не пересчитывать, 1 - пересчитать координаты объектов
# Если при обновлении параметров проекции выполнялось
# трансформирование карты - возвращает отрицательное значение,
# иначе - положительное.
# При ошибке возвращает ноль

    mapUpdateSiteInfo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateSiteInfo', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_int)
    def mapUpdateSiteInfo(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _list: int, _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _transform: int) -> int:
        return mapUpdateSiteInfo_t (_hMap, _hSite, _mapreg, _listreg, _sheetnames, _mainname.buffer(), _list, _datum, _ellparm, _type, _parm, _transform)

    mapUpdateSiteInfoEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateSiteInfoEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int)
    def mapUpdateSiteInfoEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _map: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnumber: int, _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _transform: int) -> int:
        return mapUpdateSiteInfoEx_t (_hMap, _hSite, _map, _sheet, _sheetnumber, _datum, _ellparm, _transform)

    mapUpdateSiteInfoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapUpdateSiteInfoPro', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int)
    def mapUpdateSiteInfoPro(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _map: ctypes.POINTER(mapcreat.MAPREGISTEREX), _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _sheetnumber: int, _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _transform: int) -> int:
        return mapUpdateSiteInfoPro_t (_hMap, _hSite, _map, _sheet, _sheetnames, _mainname.buffer(), _sheetnumber, _datum, _ellparm, _transform)


# Установить параметры Datum для карты
# Может выполняться или до записи объектов на карту или
# в другой момент - для карты хранящей геодезические координаты объектов
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSetSiteDatum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetSiteDatum(_hmap: maptype.HMAP, _hSite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetSiteDatum_t (_hmap, _hSite, _parm)


# Запросить параметры Datum для карты
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteDatum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetSiteDatum(_hmap: maptype.HMAP, _hSite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetSiteDatum_t (_hmap, _hSite, _parm)


# Установить параметры эллипсоида для карты
# Может выполняться или до записи объектов на карту или
# в другой момент - для карты хранящей геодезические координаты объектов
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetSiteEllipsoidParameters(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetSiteEllipsoidParameters_t (_hMap, _hSite, _parm)


# Запросить параметры эллипсоида для карты
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetSiteEllipsoidParameters(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetSiteEllipsoidParameters_t (_hMap, _hSite, _parm)


# Запросить тип локального преобразования системы координат
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# При ошибке или отсутствии преобразования возвращает ноль

    mapGetSiteLocalTransformationType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteLocalTransformationType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLocalTransformationType(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteLocalTransformationType_t (_hMap, _hSite)


# Запросить адрес параметров локального преобразования системы координат
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# parm - параметры локального преобразования координат (см. mapcreat.h)
# Возвращает тип локального преобразования системы координат
# При ошибке или отсутствии преобразования возвращает ноль

    mapGetSiteLocalTransformationParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteLocalTransformationParm', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetSiteLocalTransformationParm(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetSiteLocalTransformationParm_t (_hMap, _hSite, _parm)


# Установить параметры локального преобразования системы координат
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# type  - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# parm - параметры локального преобразования координат (см. mapcreat.h)
# При ошибке или отсутствии преобразования возвращает ноль

    mapSetLocalTransformation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetLocalTransformation', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetLocalTransformation(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetLocalTransformation_t (_hMap, _hSite, _type, _parm)


# Запрос и установка кода EPSG системы координат
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# При ошибке возвращает ноль

    mapGetEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetEPSGCode', maptype.HMAP, maptype.HSITE)
    def mapGetEPSGCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetEPSGCode_t (_hMap, _hSite)

    mapSetEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetEPSGCode', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetEPSGCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _code: int) -> int:
        return mapSetEPSGCode_t (_hMap, _hSite, _code)


# Запрос идентификатора системы координат
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# ident - строка длиной не менее 64 символов для размещения идентификатора
# size  - длина строки
# При ошибке возвращает ноль

    mapGetCRSIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCRSIdent', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_int)
    def mapGetCRSIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _ident: ctypes.c_char_p, _size: int) -> int:
        return mapGetCRSIdent_t (_hMap, _hSite, _ident, _size)

    mapGetCRSIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_int)
    def mapGetCRSIdentUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _ident: mapsyst.WTEXT, _size: int) -> int:
        return mapGetCRSIdentUn_t (_hMap, _hSite, _ident.buffer(), _size)


# Установка идентификатора системы координат
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# ident - строка со значением идентификатора не более 64 символов
# При ошибке возвращает ноль

    mapSetCRSIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCRSIdent', maptype.HMAP, maptype.HSITE, ctypes.c_char_p)
    def mapSetCRSIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _ident: ctypes.c_char_p) -> int:
        return mapSetCRSIdent_t (_hMap, _hSite, _ident)

    mapSetCRSIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetCRSIdentUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _ident: mapsyst.WTEXT) -> int:
        return mapSetCRSIdentUn_t (_hMap, _hSite, _ident.buffer())


# Запрос и установка идентификатора набора данных листа карты
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# list   - номер листа карты с 1 или 0 (запрос/установка идентикатора набора листов)
# Для пользовательской (однолистовой карты) list равен 1
# ident - строка со значением идентификатора не более 32 символов,
#         обычно 32 шестнадцатеричных символа GUID и замыкающий ноль
# При ошибке возвращает ноль

    mapGetDataIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetDataIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p, _size: int) -> int:
        return mapGetDataIdent_t (_hMap, _hSite, _list, _ident, _size)

    mapSetDataIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p)
    def mapSetDataIdent(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p) -> int:
        return mapSetDataIdent_t (_hMap, _hSite, _list, _ident)


# Запросить/Установить гриф секретности карты
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# code  - код степени секретности данных:
# 1 - открытая информация (unclassified), 2 - информация с ограниченным доступом (restricted),
# 3 - информация для служебного пользования (confidential),
# 4 - секретная информация (secret), 5 - совершенно секретная информация (topsecret)
# При ошибке или отсутствии значения возвращает ноль

    mapGetSiteSecurityCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteSecurityCode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteSecurityCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteSecurityCode_t (_hMap, _hSite)

    mapSetSiteSecurityCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSiteSecurityCode', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSiteSecurityCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _code: int) -> int:
        return mapSetSiteSecurityCode_t (_hMap, _hSite, _code)


# Запросить/Установить формат рамки листа для плана
# hMap  - идентификатор открытых данных
# hSite - идентификатор открытой пользовательской карты
# size  - формат рамки листа:
# 0 -  не установлен,
# 1 - установлен пользователем, 2 - A0(841x1189 мм),
# 3 - A1(594x841 мм),           4 - A2(420x594 мм),
# 5 - A3(297x420 мм),           6 - A4(210x297 мм)
# При ошибке или отсутствии значения возвращает ноль

    mapGetSitePaperSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSitePaperSize', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaperSize(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSitePaperSize_t (_hMap, _hSite)

    mapSetSitePaperSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSitePaperSize', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSetSitePaperSize(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _size: int) -> int:
        return mapSetSitePaperSize_t (_hMap, _hSite, _size)


# Запросить сведения о реально имеющихся объектах на карте
# (для фоновой hSite = hMap)
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# select - идентификатор контекста поиска
# в который будут помещены условия, соответствующие имеющимся объектам
# (слои, объекты, локализации - доступ см. в seekapi.h)
# см. mapCreateMapSelectContext(...)
# force - признак принудительного обновления состава условий поиска по реально
#         имеющимся на карте объектам (для больших карт длительное выполнение)
# При ошибке возвращает ноль

    mapGetSiteUsedSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteUsedSelectEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_int)
    def mapGetSiteUsedSelectEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _select: maptype.HSELECT, _force: int) -> int:
        return mapGetSiteUsedSelectEx_t (_hMap, _hSite, _select, _force)

    mapGetSiteUsedSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteUsedSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteUsedSelect(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _select: maptype.HSELECT) -> int:
        return mapGetSiteUsedSelect_t (_hMap, _hSite, _select)


# Запросить установлены ли сведения об имеющихся объектах
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# Если по условиям поиска все объекты выбираются без исключений -
# возвращает ноль, иначе - ненулевое значение

    mapIsUsedSelectActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapIsUsedSelectActive', maptype.HMAP, maptype.HSITE)
    def mapIsUsedSelectActive(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapIsUsedSelectActive_t (_hMap, _hSite)


# Трансформировать векторную карту в заданную систему координат
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# mapname  - имя создаваемой карты
# mapreg - адрес структуры, описанной в mapcreat.h
# ellparam - параметры эллипсоида (необязательный параметр)
# datum - параметры DATUM для карты (необязательный параметр)
# ttype - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
# tparm - параметры локального преобразования координат или 0
# issavecopy - признак создания копии исходной карты в поддиректории ИМЯКАРТЫ.YYYYMMDD.HHMMSS
# error - код ошибки при выполнении трансформирвоания
# callevent - адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
# parm    - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#           вторым параметром в вызываемой функции передается процент от 0 до 100
# При ошибке возвращает ноль

    mapTransformationMapEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTransformationMapEx', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_int, ctypes.POINTER(ctypes.c_int), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapTransformationMapEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _hmessage: maptype.HMESSAGE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _issavecopy: int, _error: ctypes.POINTER(ctypes.c_int), _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mapTransformationMapEx_t (_hMap, _hSite, _hmessage, _mapreg, _datum, _ellparam, _ttype, _tparm, _issavecopy, _error, _callevent, _callparm)


# Трансформировать векторную карту в заданную систему координат по заданному пути
# hMap   - идентификатор открытого документа
# hSite  - идентификатор открытой пользовательской карты в документе
# mapname  - имя создаваемой карты в заданной системе координат
# mapreg - адрес структуры, описанной в mapcreat.h
# ellparam - параметры эллипсоида (необязательный параметр)
# datum - параметры DATUM для карты (необязательный параметр)
# При ошибке возвращает ноль

    mapTransformationMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapTransformationMap', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapTransformationMap(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mapname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapTransformationMap_t (_hMap, _hSite, _mapname.buffer(), _mapreg, _datum, _ellparam)


# Запросить число слоев на карте
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteLayerCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLayerCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteLayerCount_t (_hMap, _hSite)


# namesize - размер буфера для возвращаемой строки в байтах
# При ошибке возвращает ноль

    mapGetSiteLayerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteLayerNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteLayerNameUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetSiteLayerNameUn_t (_hMap, _hSite, _number, _name.buffer(), _namesize)


# Запросить число объектов описанных в классификаторе
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSiteRscObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectCount', maptype.HMAP, maptype.HSITE)
    def mapSiteRscObjectCount(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapSiteRscObjectCount_t (_hMap, _hSite)


# Запросить число объектов описанных в классификаторе
# в заданном слое
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# layer  - номер слоя
# При ошибке возвращает ноль

    mapSiteRscObjectCountInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectCountInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapSiteRscObjectCountInLayer(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _layer: int) -> int:
        return mapSiteRscObjectCountInLayer_t (_hMap, _hSite, _layer)


# namesize - размер буфера для возвращаемой строки в байтах
# При ошибке возвращает ноль

    mapSiteRscObjectNameInLayerUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectNameInLayerUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def mapSiteRscObjectNameInLayerUn(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _layer: int, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        return mapSiteRscObjectNameInLayerUn_t (_hMap, _hSite, _layer, _number, _name.buffer(), _namesize)


# Запросить классификационный код объекта
# по порядковому номеру в заданном слое
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapSiteRscObjectExcodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectExcodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSiteRscObjectExcodeInLayer(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectExcodeInLayer_t (_hMap, _hSite, _layer, _number)


# Запросить код локализации объекта
# по порядковому номеру в заданном слое
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль (ноль допустим)

    mapSiteRscObjectLocalInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectLocalInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSiteRscObjectLocalInLayer(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectLocalInLayer_t (_hMap, _hSite, _layer, _number)


# Запросить внутренний код (индекс) объекта
# по порядковому номеру в заданном слое
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapSiteRscObjectCodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectCodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSiteRscObjectCodeInLayer(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectCodeInLayer_t (_hMap, _hSite, _layer, _number)


# Запросить внутренний код (индекс) объекта
# по внешнему коду и локализации
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# excode - внешний код объекта
# local  - локализация объекта
# При ошибке возвращает ноль

    mapSiteRscObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSiteRscObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapSiteRscObjectCode(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _excode: int, _local: int) -> int:
        return mapSiteRscObjectCode_t (_hMap, _hSite, _excode, _local)


# ############################################################
#                                                            #
#         РЕДАКТИРОВАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО ОБ'ЕКТА           #
# (доступны все функции редактирования объекта базовой карты)#
#                                                            #
# ############################################################
# Запросить (найти) последовательный номер объекта
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# key    - уникальный идентификатор объекта
# При ошибке возвращает ноль

    mapGetSiteObjectNumberByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteObjectNumberByKey', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteObjectNumberByKey(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _key: int) -> int:
        return mapGetSiteObjectNumberByKey_t (_hMap, _hSite, _key)


# Запросить уникальный идентификатор объекта по последовательному номеру объекта
# hMap     - идентификатор открытой основной карты
# hSite    - идентификатор открытой пользовательской карты
# number   - последовательный номер объекта
# list     - номер листа (для пользовательской карты равен 1)
# isdelete - признак учета удаленных объектов
# При ошибке возвращает ноль

    mapGetSiteObjectKeyByNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteObjectKeyByNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapGetSiteObjectKeyByNumberEx(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _list: int = 1, _isdelete: int = 0) -> int:
        return mapGetSiteObjectKeyByNumberEx_t (_hMap, _hSite, _number, _list, _isdelete)

    mapGetSiteObjectKeyByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetSiteObjectKeyByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapGetSiteObjectKeyByNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _number: int, _list: int = 1) -> int:
        return mapGetSiteObjectKeyByNumber_t (_hMap, _hSite, _number, _list)


# Удалить объект карты по его последовательному номеру
# Для отмены удаления применяются mapUndeleteObjectByNumber и
# mapUndeleteObject
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# object - последовательный номер объекта
# При ошибке возвращает ноль

    mapDeleteSiteObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteObjectNumber', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapDeleteSiteObjectNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _object: int) -> int:
        return mapDeleteSiteObjectNumber_t (_hMap, _hSite, _object)

    mapDeleteSiteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapDeleteSiteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapDeleteSiteObjectByNumber(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _object: int) -> int:
        return mapDeleteSiteObjectByNumber_t (_hMap, _hSite, _object)


# Восстановить копию объекта по дате и времени
# выполнения транзакции
# hMap  - идентификатор открытой карты
# hSite - идентификатор открытой пользовательской карты
# info -  идентификатор существующего объекта,
#         созданного функцией CreateObject() или CreateSiteObject() и
#         прочитанного функцией mapReadObjectByNumber или mapReadObjectByKey,
#         в котором будет размещен результат восстановления
# date - дата в формате "YYYYMMDD"
# time - время в формате "число секунд от 00:00:00"
#        (по Гринвичу - GetSystemTime, in Coordinated Universal Time (UTC))
# При ошибке возвращает ноль

    mapRestoreBackObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapRestoreBackObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapRestoreBackObject(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _info: maptype.HOBJ, _date: int, _time: int) -> int:
        return mapRestoreBackObject_t (_hMap, _hSite, _info, _date, _time)


# Создать контекст (описание условий) поиска/отображения
# объектов карты
# В состав условий отбора объектов входят : слой,
# локализация, диапазон номеров объектов, характеристики
# (семантика) объекта, область расположения (метрика) объекта
# В созданном контексте доступны все объекты карты без исключений
# Запрашивается минимум 10 Кб памти,
# если заданы условия поиска по метрике и семантике - до 300 Кб
# Каждый созданный контекст должен быть удален, когда
# он больше не используется
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapCreateSiteSelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateSiteSelectContext', maptype.HMAP, maptype.HSITE)
    def mapCreateSiteSelectContext(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> maptype.HSELECT:
        return mapCreateSiteSelectContext_t (_hMap, _hSite)


# Связать контекст условий поиска с другой картой
# Все условия поиска автоматически сбрасываются
# hMap   - идентификатор открытой основной карты
# hSite  - идентификатор открытой пользовательской карты
# При ошибке возвращает ноль

    mapSetSelectContextSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetSelectContextSite', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSetSelectContextSite(_hSelect: maptype.HSELECT, _hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapSetSelectContextSite_t (_hSelect, _hMap, _hSite)


# Добавить зарамочное оформление в пользовательскую карту
# hmap - идентификатор основной векторной карты
# hsite - идентификатор пользовательской карты
# frmname - полное имя файла шаблона зарамочного оформления (#.frm)
# frame - габариты внутреннего контура зарамочного оформления в метрах
# При ошибке возвращает ноль

    mapAddMarginalRepresentationSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAddMarginalRepresentationSite', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.POINTER(maptype.DFRAME))
    def mapAddMarginalRepresentationSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: ctypes.c_char_p, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapAddMarginalRepresentationSite_t (_hmap, _hsite, _frmname, _frame)


# Добавить зарамочное оформление в пользовательскую карту
# hmap - идентификатор основной векторной карты
# hsite - идентификатор пользовательской карты
# frmname - полное имя файла шаблона зарамочного оформления (#.frm)
# frame - габариты внутреннего контура зарамочного оформления в метрах
# angle - угол поворота (если есть)
# center - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapAddMarginalRepresentationSiteEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAddMarginalRepresentationSiteEx', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapAddMarginalRepresentationSiteEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: ctypes.c_char_p, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapAddMarginalRepresentationSiteEx_t (_hmap, _hsite, _frmname, _frame, _angle, _center)

    mapAddMarginalRepresentationSiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAddMarginalRepresentationSiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapAddMarginalRepresentationSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapAddMarginalRepresentationSiteUn_t (_hmap, _hsite, _frmname.buffer(), _frame, _angle, _center)


# Нанести линию заданного кода на пользовательскую карту
# hmap - идентификатор открытой векторной карты
# hsite - идентификатор пользовательской карты
# excode - код линии
# x1,y1,x2,y2 - координаты первой и второй точек в метрах
# angle - угол поворота (если есть)
# center - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateLineSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateLineSite', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateLineSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _x1: float, _y1: float, _x2: float, _y2: float, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateLineSite_t (_hmap, _hsite, _excode, _x1, _y1, _x2, _y2, _angle, _center)


# Создать рамку для зарамочного оформления на пользовательской карте
# hmap - идентификатор открытой векторной карты
# hsite - идентификатор пользовательской карты
# framecode - код внутренней рамки
# fillcode - код заполнения
# linecode - код внешней рамки
# delta - расстояние от внутренней до внешней рамки а м
# frame - габариты внутренней рамки в м
# angle - угол поворота (если есть)
# center - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateFrameFillSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateFrameFillSite', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateFrameFillSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _framecode: int, _fillcode: int, _linecode: int, _delta: float, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateFrameFillSite_t (_hmap, _hsite, _framecode, _fillcode, _linecode, _delta, _frame, _angle, _center)


# Нанести текст заданного кода на пользовательскую карту
# hmap - идентификатор открытой векторной карты
# hsite - идентификатор пользовательской карты
# excode - код текста подписи
# text - текст подписи
# x1,x2,y1,y2 - координаты первой и второй точек в метрах
# wide - выравнивание по горизонтали
#      - UNIA_LEFT  - по левому краю
#      - UNIA_CENTER - по центру
#      - UNIA_RIGHT - по правому краю
# vert - наличие выравнивания по вертикали (0 или 1)
# angle - угол поворота (если есть)
# center - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateTitleSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateTitleSite', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateTitleSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _text: ctypes.c_char_p, _x1: float, _y1: float, _x2: float, _y2: float, _wide: int, _vert: int, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateTitleSite_t (_hmap, _hsite, _excode, _text, _x1, _y1, _x2, _y2, _wide, _vert, _angle, _center)

    mapCreateTitleSiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateTitleSiteUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateTitleSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _text: mapsyst.WTEXT, _x1: float, _y1: float, _x2: float, _y2: float, _wide: int, _vert: int, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateTitleSiteUn_t (_hmap, _hsite, _excode, _text.buffer(), _x1, _y1, _x2, _y2, _wide, _vert, _angle, _center)


# Замена буквы 'я' на спецсимвол перед тем как разобрать строку
# функцией sscanf
# string - строка
# len - длина строки
# simbol - спецсимвол (если == 0 - то заменяет 'я' на '^')
# При ошибке возвращает ноль

    mapPreSscanf_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPreSscanf', ctypes.c_char_p, ctypes.c_int, ctypes.c_char)
    def mapPreSscanf(_string: ctypes.c_char_p, _len: int, _simbol: int) -> int:
        return mapPreSscanf_t (_string, _len, _simbol)

    mapPreSscanfUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPreSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPreSscanfUn(_string: mapsyst.WTEXT, _len: int, _simbol: int) -> int:
        return mapPreSscanfUn_t (_string.buffer(), _len, _simbol)


# Замена спецсимвола на 'я' после разбора строки функцией sscanf
# string - строка
# len - длина строки
# simbol - спецсимвол (если == 0 - то заменяет '^' на 'я')
# При ошибке возвращает ноль

    mapPostSscanf_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPostSscanf', ctypes.c_char_p, ctypes.c_int, ctypes.c_char)
    def mapPostSscanf(_string: ctypes.c_char_p, _len: int, _simbol: int) -> int:
        return mapPostSscanf_t (_string, _len, _simbol)

    mapPostSscanfUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapPostSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPostSscanfUn(_string: mapsyst.WTEXT, _len: int, _simbol: int) -> int:
        return mapPostSscanfUn_t (_string.buffer(), _len, _simbol)


# Функция создания легенды карты
# hmap      - идентификатор открытого документа
# hsite     - идентификатор открытой пользовательской карты
# outname   - полное имя файла выходной карты-легенды
# desc      - параметры легенды (фон, подпись, контур; описана в mapgdi.h)
# hselect   - контекст отбора слоев\объектов карты для формирования легенды (необязательный параметр, может быть равен нулю)
# error     - код ошибки при построении легенды (необязательный параметр, может быть равен нулю, коды в maperr.rh)
# При ошибке возвращает ноль

    mapCreateLegend_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateLegend', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(mapgdi.LEGENDESC), maptype.HSELECT, ctypes.POINTER(ctypes.c_int))
    def mapCreateLegend(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _desc: ctypes.POINTER(mapgdi.LEGENDESC), _hselect: maptype.HSELECT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCreateLegend_t (_hmap, _hsite, _outname.buffer(), _desc, _hselect, _error)


# Функция подготовки легенды карты
# При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32)
# необходимо указать размер в параметре imgsize
# hmap      - идентификатор открытой векторной карты
# hsite     - идентификатор открытой пользовательской карты
# hselect   - контекст отбора слоев карты для формирования легенды (необязательный параметр)
# xmlname   - имя выходного xml-файла
# imgpath   - путь к изображениям формата png
# frsc      - флаг отбора объектов (1 - по всему классификатору; 0 - по hselect)
# imgsize   - нестандартный размер изображения (сторона квадрата)
# transparentColor - цвет прозрачного фона, если параметр не задан то фон непрозрачный белый
# Если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32)
# Максимальный размер изображения 1024x1024
# При ошибке возвращает 0

    mapCreateLegendFromXMLEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateLegendFromXMLEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def mapCreateLegendFromXMLEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _frsc: int, _imgsize: int, _transparentColor: int) -> int:
        return mapCreateLegendFromXMLEx_t (_hmap, _hsite, _hselect, _xmlname.buffer(), _imgpath.buffer(), _frsc, _imgsize, _transparentColor)

    mapCreateLegendFromXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCreateLegendFromXML', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapCreateLegendFromXML(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _frsc: int, _imgsize: int) -> int:
        return mapCreateLegendFromXML_t (_hmap, _hsite, _hselect, _xmlname.buffer(), _imgpath.buffer(), _frsc, _imgsize)


except Exception as e:
    print(e)
    acceslib = 0
