#!/usr/bin/env python3

# **********************************************************************
# *                                                                    *
# *              Copyright (c) PANORAMA Group 1991-2026                *
# *                      All Rights Reserved                           *
# *                                                                    *
# **********************************************************************
# *                                                                    *
# *      Описание интерфейса доступа к векторной карте                 *
# *                                                                    *
# *   Под векторными картами понимаются: локально расположенные файлы  *
# *   форматов SITX, SIT, SITZ, MAP, MAPZ или файлы на ГИС Сервере,    *
# *   таблицы пространственных баз данных, открываемые через файлы     *
# *   параметров доступа DBM, данные с сервисов WFS и WFS-T.           *
# *   Карта обстановки (пользовательская) может состоять из одного     *
# *   листа произвольных размеров или набора листов, имеет свой        *
# *   классификатор и  может открываться поверх другой базовой         *
# *   (фоновой) карты местности любого масштаба. Над одной картой      *
# *   местности может отображаться произвольное число других карт      *
# *                                                                    *
# **********************************************************************

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
    curLib = mapsyst.LoadLibrary(gisaccesname)

# Открыть векторную карту в наборе данных (документе)
# hmap      - идентификатор открытых данных (документа)
# sitename  - имя открываемого файла векторной карты
# mode      - режим чтения/записи (GENERIC_READ, GENERIC_WRITE или 0)
# transform - признак трансформирования карты к ранее открытым данным:
#             0 - не трансформировать данные (преобразовывать "на лету"),
#             1 - трансформировать данные при открытии и сохранить карту в новой проекции,
#            -1 - задать вопрос пользователю
#             В серверной версии -1 обрабатывается, как 0
# password  - пароль доступа к данным из которого формируется 256-битный код
#             для шифрования данных (при утрате данные не восстанавливаются) или ноль
# size      - длина пароля в байтах или ноль
# Передача пароля необходима, если при создании карты он был указан
# Если пароль не передан, а он был указан при создании,
# то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
# Если выдача сообщений запрещена (mapIsMessageEnable), то диалог
# не вызывается, а при отсутствии пароля происходит отказ открытия данных
# Возвращает идентификатор открытой векторной карты
# При ошибке возвращает ноль

    mapOpenSiteForMapPro_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapOpenSiteForMapPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapOpenSiteForMapPro(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int, _transform: int, _password: mapsyst.WTEXT, _size: int) -> maptype.HSITE:
        return mapOpenSiteForMapPro_t (_hmap, _sitename.buffer(), _mode, _transform, _password.buffer(), _size)

    mapOpenSiteForMapUn_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapOpenSiteForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapOpenSiteForMapUn(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int) -> maptype.HSITE:
        return mapOpenSiteForMapUn_t (_hmap, _sitename.buffer(), _mode)
    

# Закрыть по идентификатору векторную карту в наборе данных (документе)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если hsite == 0, закрываются все данные обстановки
# При ошибке возвращает ноль

    mapCloseSiteForMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCloseSiteForMap', maptype.HMAP, maptype.HSITE)
    def mapCloseSiteForMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapCloseSiteForMap_t (_hmap, _hsite)


# Закрыть по названию векторную карту в наборе данных (документе)
# hmap - идентификатор открытых данных (документа)
# sitename - полный путь к файлу паспорта карты
# При ошибке возвращает ноль

    mapCloseSiteForMapByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCloseSiteForMapByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapCloseSiteForMapByNameUn(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT) -> int:
        return mapCloseSiteForMapByNameUn_t (_hmap, _sitename.buffer())


# Удалить векторную карту (все файлы данных)
# hmap  - идентификатор открытых данных (документа)
# number - номер векторную карту по номеру от 1 до mapGetSiteCount()
# При ошибке возвращает ноль

    mapDeleteSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSite', maptype.HMAP, ctypes.c_long)
    def mapDeleteSite(_hmap: maptype.HMAP, _number: int) -> int:
        return mapDeleteSite_t (_hmap, _number)


# Удалить векторную карту (все файлы данных)
# sitename - полное имя файла паспорта карты
# При ошибке возвращает ноль

    mapDeleteSiteByNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSiteByNameUn', maptype.PWCHAR)
    def mapDeleteSiteByNameUn(_sitename: mapsyst.WTEXT) -> int:
        return mapDeleteSiteByNameUn_t (_sitename.buffer())


# Удалить все объекты векторной карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapClearSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearSite', maptype.HMAP, maptype.HSITE)
    def mapClearSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapClearSite_t (_hmap, _hsite)


# Скопировать векторную карту с изменением имен файлов
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# newname - полный путь к имени паспорта новой карты
# Имена файлов данных будут иметь такое же имя, как у карты, но свое расширение
# Если классификатор расположен с картой, он тоже копируется в новую директорию
# Для удаления старой копии необходимо вызвать mapDeleteSite
# При ошибке (новое имя не создано) возвращает ноль

    mapCopySiteUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCopySiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapCopySiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _newname: mapsyst.WTEXT) -> int:
        return mapCopySiteUn_t (_hmap, _hsite, _newname.buffer())


# Сохранить текущее состояние карты на диск
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# force - сохранять всегда, если не 0, или только при редактировании
# При выполнении редактирования карты с отключенным журналом транзакций состояние карты в памяти и
# на диске может отличаться, в этом случае можно вызвать mapSaveSite

    mapSaveSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSaveSite', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSaveSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _force: int) -> ctypes.c_void_p:
        return mapSaveSite_t (_hmap, _hsite, _force)


# Сохранить фрагмент карты в виде векторной карты SITX в см
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# handle - идентификатор окна (HWND/функция обратного вызова в Linux) для получения сообщений WM_PROGRESSBARUN или 0
# frame - сохраняемая область в метрах в системе координат документа
# newname - полный путь к имени паспорта новой карты
# sheetframe - признак формирования новой карты с рамкой
# error - результат выполнения: код ошибки или ноль
# При ошибке возвращает ноль

    mapSaveMapFrameAs_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveMapFrameAs', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSaveMapFrameAs(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _frame: ctypes.POINTER(maptype.DFRAME), _newname: mapsyst.WTEXT, _sheetframe: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapSaveMapFrameAs_t (_hmap, _hsite, _handle, _frame, _newname.buffer(), _sheetframe, _error)


# Сортировка отдельной карты документа
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# handle - идентификатор окна, которому посылаются сообщения WM_OBJECT и WM_ERROR
# flags  - флажки обработки карты:
#          0 - сортировать все листы,
#          1 - только несортированные,
#          2 - сохранять файлы отката (устанавливается автоматически),
#          4 - повысить точность хранения,
#          16 - повысить точность хранения, формат - см
#          32 - повысить точность хранения, формат - мм
#          64 - повысить точность хранения, формат - радианы
# При ошибке возвращает ноль

    gsMapSorting_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'gsMapSorting', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.c_long)
    def gsMapSorting(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _flags: int) -> int:
        return gsMapSorting_t (_hmap, _hsite, _handle, _flags)


# Запросить количество открытых векторных карт поверх фоновой карты (снимка, геопортала или других данных)
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetSiteCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteCount', maptype.HMAP)
    def mapGetSiteCount(_hmap: maptype.HMAP) -> int:
        return mapGetSiteCount_t (_hmap)


# Определить номер векторной карты в цепочке по ее идентификатору
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSiteNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteNumber_t (_hmap, _hsite)


# Определить имя файла паспорта векторной карты по ее идентификатору
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# name  - адрес буфера для записи имени файла
# size  - размер строки в байтах
# При ошибке возвращает 0

    mapGetSiteFileNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteFileNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteFileNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteFileNameUn_t (_hmap, _hsite, _name.buffer(), _size)


# Запросить является ли карта временной, созданной через mapCreateTempSite или mapCreateAndAppendTempSite
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Для временной карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsTempSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsTempSite', maptype.HMAP, maptype.HSITE)
    def mapIsTempSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsTempSite_t (_hmap, _hsite)


# Запросить является ли карта ограниченной по территории (по рамке номенклатурного листа)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта содержит номенклатурный лист, то функция возвращает ненулевое значение
# Если территория карты не ограничена (меняется при добавлении
# или удалении объектов) - возвращает ноль
# При ошибке возвращает ноль

    mapIsSiteLimited_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteLimited', maptype.HMAP, maptype.HSITE)
    def mapIsSiteLimited(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteLimited_t (_hmap, _hsite)


# Запросить содержит ли карта координаты в геодезической системе (радианы)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта хранит координаты в геодезической системе,
# функция возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteRealGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteRealGeo', maptype.HMAP, maptype.HSITE)
    def mapIsSiteRealGeo(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteRealGeo_t (_hmap, _hsite)


# Запросить признак повышенной точности хранения координат
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает значения:
#     1 - максимальная точность хранения (метры или радианы),
#     2 - с точностью 2 знака (сантиметры),
#     3 - с точностью 3 знака (миллиметры)
# При ошибке или нормальной точности хранения координат возвращает ноль

    mapGetSitePrecision_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePrecision', maptype.HMAP, maptype.HSITE)
    def mapGetSitePrecision(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePrecision_t (_hmap, _hsite)


# Запросить содержит ли карта объекта координаты в геодезической системе (радианы)
# hobj - идентификатор объекта
# Если карта хранит координаты в геодезической системе,
# функция возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsObjectMapRealGeo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsObjectMapRealGeo', maptype.HOBJ)
    def mapIsObjectMapRealGeo(_hobj: maptype.HOBJ) -> int:
        return mapIsObjectMapRealGeo_t (_hobj)


# Запросить поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта поддерживает пересчет к геодезическим координатам, функция возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteGeoSupported_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteGeoSupported', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGeoSupported(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteGeoSupported_t (_hmap, _hsite)


# Запросить является ли карта морской (создана по классификатору s57navy.rsc)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Для морской карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteMarine_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteMarine', maptype.HMAP, maptype.HSITE)
    def mapIsSiteMarine(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteMarine_t (_hmap, _hsite)


# Запросить является ли карта морской по стандарту S63
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Карта должна быть создана по классификатору s57navy.rsc в формате SITX и закодирована hw_id6
# Для морской карты по стандарту S63 возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteS63_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteS63', maptype.HMAP, maptype.HSITE)
    def mapIsSiteS63(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteS63_t (_hmap, _hsite)


# Запросить дату завершения срока действия лицензии на карту S63 (полученную из PERMIT.TXT)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа с 1
# Карта должна быть создана по классификатору s57navy.rsc в формате SITX и закодирована hw_id6
# Возвращается значение, которое было указано в файле PERMIT.TXT при создании карты
# При ошибке возвращает ноль

    mapGetS63LicenseTerm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetS63LicenseTerm', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetS63LicenseTerm(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        return mapGetS63LicenseTerm_t (_hmap, _hsite, _list)


# Запросить является ли карта оперативной обстановкой (создана по классификатору operator.rsc)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Для карты обстановки возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteArmy_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteArmy', maptype.HMAP, maptype.HSITE)
    def mapIsSiteArmy(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteArmy_t (_hmap, _hsite)


# Запросить является ли карта аэронавигационной (создана по классификатору dfc.rsc)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных,
# Для аэронавигационной карты возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteAero_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteAero', maptype.HMAP, maptype.HSITE)
    def mapIsSiteAero(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteAero_t (_hmap, _hsite)


# Запросить является ли карта графом дорог
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Карта должна быть создана по классификатору service.rsc или road25.rsc и содержать дуги графа
# Для карты графа возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteGraph_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteGraph', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGraph(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteGraph_t (_hmap, _hsite)


# Запросить открыта ли карта на сервере или локально
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта открыта на сервере возвращает ненулевое значение

    mapIsSiteFromServer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsSiteFromServer(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteFromServer_t (_hmap, _hsite)


# Запросить состояние данных для карты, открытой на сервере
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если представление карты формируется на лету из базы данных,
# то при открытии карты устанавливается признак "состояние загрузки", равное 1
# Признак сбрасывается при вызове функций mapAdjustData или mapAdjustSiteData,
# если загрузка карты завершена
# При ошибке возвращает ноль

    mapGetMapStateFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapStateFlag', maptype.HMAP, maptype.HSITE)
    def mapGetMapStateFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetMapStateFlag_t (_hmap, _hsite)


# Выполнить согласование данных карты в памяти и на диске (при многопользовательском доступе к данным)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных,
# Если состояние данных в памяти изменилось (по данным с диска)
# возвращает ненулевое значение 1, иначе - 0
# Если карта должна быть закрыта - возвращает 2 (доступ на ГИС Сервер прекращен)
# Если карта, открыта с ГИС Сервера, а связи с ним нет, то возвращает -1
# Если состояние изменилось - необходимо перерисовать изображение карты
# Опрос состояния целесообразно выполнять периодически
# в процессе работы приложения

    mapAdjustSiteData_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAdjustSiteData', maptype.HMAP, maptype.HSITE)
    def mapAdjustSiteData(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapAdjustSiteData_t (_hmap, _hsite)


# Проверить и при необходимости обновить общие файлы XML
# Обновляются файлы XML, размещенные в общей папке
# классификаторов по эталонам, размещенным на ГИС Сервере
# Если хост ГИС Сервера не установлен или не доступен - возвращает ноль
# При успешном обновлении возвращает число обновленных файлов

    mapAdjustCommonXml_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAdjustCommonXml')
    def mapAdjustCommonXml() -> int:
        return mapAdjustCommonXml_t ()


# Запросить, есть ли карты в состоянии загрузки на сервере
# hmap - идентификатор открытых данных (документа)
# Проверка выполняется для всех карт в составе "документа" (hmap)
# Если представление карты формируется на лету из базы данных,
# то при открытии карты устанавливается признак "состояние загрузки", равное 1
# Признак сбрасывается при вызове функции mapAdjustData,
# если загрузка карты завершена
# Если есть карты в состоянии загрузки, то возвращает 1
# При ошибке возвращает ноль

    mapCheckMapStateFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckMapStateFlag', maptype.HMAP)
    def mapCheckMapStateFlag(_hmap: maptype.HMAP) -> int:
        return mapCheckMapStateFlag_t (_hmap)


# Запросить, хранится ли карта в одном файле (формат SITX)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта в одном файле возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSiteSitX_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteSitX', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSitX(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteSitX_t (_hmap, _hsite)


# Запросить, хранится ли карта в одном упакованном файле (формат SITZ/MAPZ)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта в одном упакованном файле возвращает ненулевое значение
# При ошибке возвращает ноль

    mapIsSitePackaged_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSitePackaged', maptype.HMAP, maptype.HSITE)
    def mapIsSitePackaged(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSitePackaged_t (_hmap, _hsite)


# Установить признак применения альтернативных шрифтов
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак применения альтернативных шрифтов, заданных в файле altfonts.xml
# При ошибке возвращает ноль

    mapSetAlternativeFontsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetAlternativeFontsFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetAlternativeFontsFlag_t (_hmap, _hsite, _flag)


# Запросить признак применения альтернативных шрифтов
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает ранее установленное значение

    mapGetAlternativeFontsFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE)
    def mapGetAlternativeFontsFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetAlternativeFontsFlag_t (_hmap, _hsite)


# Установить признак использования координаты M, как линейной координаты маршрута
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак использования координаты M, как линейной координаты маршрута
# Используется при загрузке в карту готовых маршрутов без калибровочных точек
# При ошибке возвращает ноль

    mapSetRouteMap4DFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetRouteMap4DFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetRouteMap4DFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetRouteMap4DFlag_t (_hmap, _hsite, _flag)


# Запросить признак использования координаты M, как линейной координаты маршрута
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Используется при загрузке в карту готовых маршрутов без калибровочных точек
# Возвращает ранее установленное значение

    mapGetRouteMap4DFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetRouteMap4DFlag', maptype.HMAP, maptype.HSITE)
    def mapGetRouteMap4DFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetRouteMap4DFlag_t (_hmap, _hsite)


# Установить признак ведения даты и времени обновления для каждого объекта
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак ведения даты и времени обновления
# Признак устанавливается после создания карты до записи объектов
# Если открытых данных нет возвращает ноль

    mapSetObjectTimeFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetObjectTimeFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetObjectTimeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetObjectTimeFlag_t (_hmap, _hsite, _flag)


# Запросить признак ведения даты и времени обновления для каждого объекта
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если открытых данных нет или признак не установлен - возвращает ноль

    mapGetObjectTimeFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectTimeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTimeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetObjectTimeFlag_t (_hmap, _hsite)


# Установить флаг сводки объектов по рамке листа карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 до числа листов
# flag  - флаг сводки объектов по рамке листа карты
# Если открытых данных нет возвращает ноль

    mapSetMatchingFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetMatchingFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSetMatchingFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _flag: int) -> int:
        return mapSetMatchingFlag_t (_hmap, _hsite, _list, _flag)


# Запросить флаг сводки объектов по рамке листа карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 до числа листов
# Если открытых данных нет или флаг не установлен - возвращает ноль

    mapGetMatchingFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMatchingFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetMatchingFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        return mapGetMatchingFlag_t (_hmap, _hsite, _list)


# Установить признак ведения уникального идентификатора GUID для объектов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных,
# flag  - признак ведения GUID для объектов карты
# Признак устанавливается после создания карты до записи объектов
# Если признак установлен, то каждому объекту карты при создании автоматически
# присваивается семантика с кодом 32799, содержащая уникальную комбинацию
# из 32 шестнадцатеричных символов от 0 до F (GUID)
# Если открытых данных нет возвращает ноль

    mapSetAutoObjectGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetAutoObjectGUID', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetAutoObjectGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetAutoObjectGUID_t (_hmap, _hsite, _flag)


# Запросить признак ведения уникального идентификатора GUID для объектов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если открытых данных нет или признак не установлен возвращает ноль

    mapGetAutoObjectGUID_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetAutoObjectGUID', maptype.HMAP, maptype.HSITE)
    def mapGetAutoObjectGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetAutoObjectGUID_t (_hmap, _hsite)


# Запросить имена файлов данных листа карты для контроля целостности данных
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 до числа листов
# type  - тип листа карты:
#         1 - файл заголовков,
#         2 - файл метрики,
#         3 - файл семантики,
#         4 - файл графики
# name   - адрес буфера для записи имени файла
# size   - размер буфера для записи имени файла
# Кроме указанных файлов карта имеет паспорт карты и цифровой классификатор RSC
# Файл SITX содержит все данные (кроме RSC) в одном файле
# Если запрошенный тип файла должен входить в состав карты (в паспорте карты
# отмечено, что такие данные есть в листе), то возвращает 1,
# если таких данных нет, то возвращает -1
# Файлы заголовков и метрики присутствуют всегда
# При ошибке возвращает 0

    mapGetMapFilesName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapFilesName', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapFilesName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _type: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetMapFilesName_t (_hmap, _hsite, _list, _type, _name.buffer(), _size)


# Запросить длину файлов листа карты в байтах
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 до числа листов
# head  - указатель на поле для записи размера индексного файла (может равняться нулю)
# data  - указатель на поле для записи размера файла метрики (может равняться нулю)
# semn  - указатель на поле для записи размера файла семантики (может равняться нулю)
# draw  - указатель на поле для записи размера файла графических
#         параметров графических объектов (может равняться нулю)
# При экспорте в SXF размер файла SXF примерно будет равен сумме размеров всех файлов листа карты
# При ошибке возвращает ноль

    mapGetSheetFilesLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSheetFilesLength', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
    def mapGetSheetFilesLength(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _head: ctypes.POINTER(ctypes.c_ulong), _data: ctypes.POINTER(ctypes.c_ulong), _semn: ctypes.POINTER(ctypes.c_ulong), _draw: ctypes.POINTER(ctypes.c_ulong)) -> int:
        return mapGetSheetFilesLength_t (_hmap, _hsite, _list, _head, _data, _semn, _draw)


# Запросить общую длину данных всех файлов карты в байтах
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteTotalDataSize_t = mapsyst.GetProcAddress(curLib,ctypes.c_int64,'mapGetSiteTotalDataSize', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTotalDataSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteTotalDataSize_t (_hmap, _hsite)


# Определить путь к папке векторной карты по ее идентификатору
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# name  - адрес буфера для записи пути к папке
# size  - размер буфера для записи пути
# При ошибке возвращает пустую строку

    mapGetSitePathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSitePathUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSitePathUn_t (_hmap, _hsite, _name.buffer(), _size)


# Определить путь к папке LOG векторной карты по ее идентификатору
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# path  - адрес буфера для записи пути к папке
# size  - размер буфера в байтах
# При ошибке возвращает 0

    mapGetLogPathUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetLogPathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetLogPathUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _path: mapsyst.WTEXT, _size: int) -> int:
        return mapGetLogPathUn_t (_hmap, _hsite, _path.buffer(), _size)


# Запросить имя файла vclx для карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# vclname - адрес буфера для записи имени файла vclx
# size    - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetVclxName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetVclxName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetVclxName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _vclname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetVclxName_t (_hmap, _hsite, _vclname.buffer(), _size)


# Определить идентификатор векторной карты в открытых данных по ее номеру в цепочке
# hmap   - идентификатор открытых данных (документа)
# number - номер пользовательской карты в цепочке
# Если number == 0, возвращается идентификатор фоновой
# (базовой) карты, равный hmap (он может применяться вместо HSITE)
# При ошибке возвращает ноль

    mapGetSiteIdent_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteIdent', maptype.HMAP, ctypes.c_long)
    def mapGetSiteIdent(_hmap: maptype.HMAP, _number: int) -> maptype.HSITE:
        return mapGetSiteIdent_t (_hmap, _number)


# Определить идентификатор векторной карты в открытых данных по имени файла паспорта
# hmap - идентификатор открытых данных (документа)
# name - имя файла паспорта пользовательской карты
# При ошибке возвращает ноль

    mapGetSiteIdentByNameUn_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteIdentByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetSiteIdentByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> maptype.HSITE:
        return mapGetSiteIdentByNameUn_t (_hmap, _name.buffer())


# Запросить имя листа по его номеру
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты
# name  - адрес буфера для результата запроса
# size  - размер буфера в байтах
# При ошибке возвращает ноль

    mapGetSiteSheetNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteSheetNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteSheetNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteSheetNameUn_t (_hmap, _hsite, _list, _name.buffer(), _size)


# Запросить номенклатуру листа по его номеру
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты
# name  - адрес буфера для результата запроса
# size  - размер буфера в байтах
# Номенклатура листа применяется для поиска в функции mapSeekObject
# При ошибке возвращает ноль

    mapGetSiteNomenclatureUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteNomenclatureUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteNomenclatureUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteNomenclatureUn_t (_hmap, _hsite, _list, _name.buffer(), _size)


# Запросить номенклатуру листа по его номеру
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты
# При ошибке возвращает пустую строку

    mapGetSiteListName_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetSiteListName', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteListName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int = 1) -> ctypes.POINTER(ctypes.c_char):
        return mapGetSiteListName_t (_hmap, _hsite, _list)


# Определить идентификатор открытой карты по номенклатуре листа
# hmap - идентификатор открытых данных (документа)
# name - номенклатура листа карты
# list - поле для размещения номера листа (если лист найден в многолистовой карте)
# При ошибке возвращает ноль

    mapGetSiteIdentByNomenclatureUn_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteIdentByNomenclatureUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetSiteIdentByNomenclatureUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_long)) -> maptype.HSITE:
        return mapGetSiteIdentByNomenclatureUn_t (_hmap, _name.buffer(), _list)


# Определить идентификатор открытой векторной карты по имени листа карты
# hmap - идентификатор открытых данных (документа)
# name - имя листа карты
# list - поле для размещения номера листа
# Имя листа карты запрашивается в функции mapGetSiteSheetNameUn
# При ошибке возвращает ноль

    mapGetSiteIdentBySheetNameUn_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteIdentBySheetNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetSiteIdentBySheetNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_long)) -> maptype.HSITE:
        return mapGetSiteIdentBySheetNameUn_t (_hmap, _name.buffer(), _list)


# Запросить активную векторной карту (устанавливается приложением по своему усмотрению)
# hmap - идентификатор открытых данных (документа)
# При ошибке возвращает ноль

    mapGetActiveSite_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetActiveSite', maptype.HMAP)
    def mapGetActiveSite(_hmap: maptype.HMAP) -> maptype.HSITE:
        return mapGetActiveSite_t (_hmap)


# Установить активную пользовательскую карту (устанавливается приложением по своему усмотрению)
# hmap - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapSetActiveSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetActiveSite', maptype.HMAP, maptype.HSITE)
    def mapSetActiveSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapSetActiveSite_t (_hmap, _hsite)


# Запросить идентификатор текущей отображаемой карты
# hmap - идентификатор открытых данных (документа)
# При запросе в момент отображения из вспомогательной библиотеки
# считаем, что один HMAP применяется в одном потоке отображения
# При ошибке возвращает ноль

    mapGetCurrentViewSite_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetCurrentViewSite', maptype.HMAP)
    def mapGetCurrentViewSite(_hmap: maptype.HMAP) -> maptype.HSITE:
        return mapGetCurrentViewSite_t (_hmap)


# Запросить номер состояния пользовательской карты по ее идентификатору
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Номер состояния меняется при любой операции редактирования карты (увеличивается на 1)
# При ошибке возвращает ноль

    mapGetSiteMode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteMode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteMode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteMode_t (_hmap, _hsite)


# Запросить является ли открытая карта картой с данными c сервиса WFS
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapIsSiteWFS_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteWFS', maptype.HMAP, maptype.HSITE)
    def mapIsSiteWFS(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteWFS_t (_hmap, _hsite)


# Запросить HWFS
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetHWFS_t = mapsyst.GetProcAddress(curLib,maptype.HWFS,'mapGetHWFS', maptype.HMAP, maptype.HSITE)
    def mapGetHWFS(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HWFS:
        return mapGetHWFS_t (_hmap, _hsite)


# Запросить установлено ли шифрование данных
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteCodeFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteCodeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCodeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteCodeFlag_t (_hmap, _hsite)


# Запросить, зашифрована ли карта (формат SITX)
# name - имя карты (путь к файлу)
# Если нет - возвращает ноль

    mapGetSiteCodeFlagByName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteCodeFlagByName', maptype.PWCHAR)
    def mapGetSiteCodeFlagByName(_name: mapsyst.WTEXT) -> int:
        return mapGetSiteCodeFlagByName_t (_name.buffer())


# Запросить, могут ли объекты карты копироваться на другие карты или экспортироваться
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteCopyFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteCopyFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCopyFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteCopyFlag_t (_hmap, _hsite)


# Запросить, можно ли записывать файлы картинок и документов в папке с картой на ГИС Сервере
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если запись разрешена, то можно применить функции mapSaveFileOnServer(), mapReadFileOnServer()
# Если нет - возвращает ноль

    mapGetSiteFolderEditFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteFolderEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteFolderEditFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        return mapGetSiteFolderEditFlag_t (_hMap, _hSite)


# Запретить копирование объектов с карты (свойство нельзя отменить)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapSetSiteHideCopy_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteHideCopy', maptype.HMAP, maptype.HSITE)
    def mapSetSiteHideCopy(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapSetSiteHideCopy_t (_hmap, _hsite)


# Запросить запрещено ли показывать параметры паспорта
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteHidePassportFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteHidePassportFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteHidePassportFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteHidePassportFlag_t (_hmap, _hsite)


# Запросить может ли карта выводиться на печать
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Для карт, открытых на ГИС Сервере, может устанавливаться
# запрет вывода изображения карты на печать
# Если нет - возвращает ноль

    mapGetPrintFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetPrintFlag', maptype.HMAP, maptype.HSITE)
    def mapGetPrintFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetPrintFlag_t (_hmap, _hsite)


# Запросить отражает ли карта содержимое таблицы базы данных
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Таблица базы данных открыта на ГИС Сервере или с клиентского компьютера (через файл DBM)
# Если карта не отражает данные из базы данных - возвращает ноль (DBMFLAG_NOTDBM)
# Для карты, открытой на ГИС Сервере, возвращает DBMFLAG_GISSERVER (1)
# Для локально открытой карты DBM возвращает DBMFLAG_LOCAL (2)

    mapGetDBMapFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDBMapFlag', maptype.HMAP, maptype.HSITE)
    def mapGetDBMapFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetDBMapFlag_t (_hmap, _hsite)


# Запросить полный путь к локальному DBM-файлу
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetDBFileName_t = mapsyst.GetProcAddress(curLib,maptype.PWCHAR,'mapGetDBFileName', maptype.HMAP, maptype.HSITE)
    def mapGetDBFileName(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> mapsyst.WTEXT:
        return mapGetDBFileName_t (_hmap, _hsite)


# Запросить полный путь к карте (map/sit/sitx) для локального DBM-файла
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetDBMapName_t = mapsyst.GetProcAddress(curLib,maptype.PWCHAR,'mapGetDBMapName', maptype.HMAP, maptype.HSITE)
    def mapGetDBMapName(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> mapsyst.WTEXT:
        return mapGetDBMapName_t (_hmap, _hsite)


# Запросить идентификатор группы карт с ограничением типа записываемых объектов
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта не входит в группу карт с ограничением типа
# создаваемых объектов - возвращает ноль,
# иначе - идентификатор группы карт с одним классификатором

    mapGetObjectTypeLimitIdent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetObjectTypeLimitIdent', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTypeLimitIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetObjectTypeLimitIdent_t (_hmap, _hsite)


# Подобрать карту для записи объекта в таблицу базы данных (DBM)
# hobj - идентификатор объекта в памяти, предварительно созданного функцией
#        mapCreateObject() или mapCreateSiteObject()
# Отображение базы данных формируется из набора таблиц (представленных
# в интерфейсе программы пользовательскими картами), каждая таблица
# может содержать определенные виды объектов
# Не зависимо от текущей пользовательской карты, на которой создается объект,
# сохранять его нужно именно в ту таблицу, которой соответствует его тип
# При ошибке возвращает ноль

    mapGetSiteForObjectIdent_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteForObjectIdent', maptype.HOBJ)
    def mapGetSiteForObjectIdent(_hobj: maptype.HOBJ) -> maptype.HSITE:
        return mapGetSiteForObjectIdent_t (_hobj)


# Подобрать карту для записи объекта в таблицу базы данных (DBM)
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# incode - внутренний код создаваемого объекта
# Отображение базы данных формируется из набора таблиц (представленных
# в интерфейсе программы пользовательскими картами), каждая таблица
# может содержать определенные виды объектов
# При ошибке возвращает ноль

    mapGetSiteForObjectCode_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteForObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteForObjectCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _incode: int) -> maptype.HSITE:
        return mapGetSiteForObjectCode_t (_hmap, _hsite, _incode)


# Запросить - может ли карта редактироваться (включая метрику)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteEditFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteEditFlag_t (_hmap, _hsite)


# Установить флаг редактирования карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак возможности редактирования (0 - не редактировать)
# Возвращает новое значение флага (запрет редактирования может сохраниться)

    mapSetSiteEditFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteEditFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteEditFlag_t (_hmap, _hsite, _flag)


# Запросить может ли карта редактироваться (семантика и графика объекта)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При общем запрете редактирования векторной карты может быть разрешено редактирование
# семантики и графики объекта (кроме координат)
# Если нет - возвращает ноль

    mapGetSiteEditFlagWithoutMetric_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteEditFlagWithoutMetric', maptype.HMAP, maptype.HSITE)
    def mapGetSiteEditFlagWithoutMetric(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteEditFlagWithoutMetric_t (_hmap, _hsite)


# Запросить можно ли изменить признак редактирования карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteChangeEditFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteChangeEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteChangeEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteChangeEditFlag_t (_hmap, _hsite)


# Запросить признак редактируемости паспорта карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Для карт с ГИС Сервера разрешено редактирование паспорта для
# администраторов и при отсутствии запрета показывать параметры системы координат
# Если нет - возвращает ноль

    mapGetSitePaspEditFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaspEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaspEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePaspEditFlag_t (_hmap, _hsite)


# Запросить флаг масштабируемости объектов карты относительно заданного масштаба
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если признак не установлен, то масштабирование выполняется относительно
# базового масштаба карты, установленного в паспорте
# Заданный масштаб устанавливается программно (например, в библиотеках IMLAPI)
# Если нет - возвращает ноль

    mapGetScalingToLevelFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetScalingToLevelFlag', maptype.HMAP, maptype.HSITE)
    def mapGetScalingToLevelFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetScalingToLevelFlag_t (_hmap, _hsite)


# Установить флаг масштабируемости объектов карты относительно заданного масштаба
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак возможности редактирования
# Возвращает новое значение флага

    mapSetScalingToLevelFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetScalingToLevelFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetScalingToLevelFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetScalingToLevelFlag_t (_hmap, _hsite, _flag)


# Запросить степень прозрачности карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает значение от 0 (карта не видна) до 100 (карта не прозрачная)

    mapGetSiteTransparent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteTransparent', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTransparent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteTransparent_t (_hmap, _hsite)


# Установить степень прозрачности карты (от 0 до 100)
# hmap        - идентификатор открытых данных (документа)
# hsite       - идентификатор векторной карты в открытых данных
# transparent - степень прозрачности карты от 0 (карта не видна) до 100 (карта не прозрачная)
# Возвращает новое значение флага

    mapSetSiteTransparent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteTransparent', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteTransparent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _transparent: int) -> int:
        return mapSetSiteTransparent_t (_hmap, _hsite, _transparent)


# Запросить флаг подсветки подписей
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает значение флага

    mapGetSiteBackLightText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteBackLightText', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBackLightText(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteBackLightText_t (_hmap, _hsite)


# Установить флаг подсветки подписей
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак подсветки:
#         0 - подсветка отключена (подписи отображаются в соответствии с параметрами);
#         1 - подсветка включена (все подписи отображаются с белым контуром),
#             использовать при отображении карты поверх растров
# Возвращает новое значение флага

    mapSetSiteBackLightText_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteBackLightText', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteBackLightText(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteBackLightText_t (_hmap, _hsite, _flag)


# Запросить могут ли на карте выбираться объекты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если нет - возвращает ноль

    mapGetSiteInquiryFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteInquiryFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteInquiryFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteInquiryFlag_t (_hmap, _hsite)


# Установить флаг разрешения выбора объектов на карте (0 - не выбирать)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак возможности выбора объектов в функциях типа mapWhatObject
# Влияет на работу функции mapWhatObject
# Возвращает новое значение флага

    mapSetSiteInquiryFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteInquiryFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteInquiryFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteInquiryFlag_t (_hmap, _hsite, _flag)


# Запросить отображается ли карта
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта не отображается возвращает ноль

    mapGetSiteViewFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteViewFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteViewFlag_t (_hmap, _hsite)


# Установить флаг отображения карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# flag  - флаг отображения карты:
#         0 - не отображать,
#         1 - отображать
# Возвращает новое значение флага

    mapSetSiteViewFlag_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteViewFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteViewFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteViewFlag_t (_hmap, _hsite, _flag)


# Установить объект, который временно не будет виден на карте
# hobj - идентификатор скрываемого объекта
# Установка сохраняется до переоткрытия карты или до восстановления отображения
# Функция применяется при редактировании отдельного (единственного) объекта в интерактивном режиме
# При ошибке возвращает ноль

    mapHideSiteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapHideSiteObject', maptype.HOBJ)
    def mapHideSiteObject(_hobj: maptype.HOBJ) -> int:
        return mapHideSiteObject_t (_hobj)


# Установить объект, который временно не будет виден на карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# key - идентификатор объекта на карте (уникальный номер объекта на листе карты)
# list - номер листа карты
# Установка выполняется до переоткрытия карты или до восстановления отображения
# Функция применяется при редактировании отдельного (единственного) объекта в интерактивном режиме
# При ошибке возвращает ноль

    mapHideSiteObjectByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapHideSiteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapHideSiteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _key: int, _list: int) -> int:
        return mapHideSiteObjectByNumber_t (_hmap, _hsite, _key, _list)


# Восстановить отображение объекта (после mapHideSiteObject)
# hobj - идентификатор восстанавливаемого объекта
# Функция обнуляет номер скрываемого объекта и номер листа

    mapUnhideSiteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapUnhideSiteObject', maptype.HOBJ)
    def mapUnhideSiteObject(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        return mapUnhideSiteObject_t (_hobj)


# Восстановить отображение объекта (после mapHideSiteObject)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Функция обнуляет номер скрываемого объекта и номер листа

    mapClearHideSiteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearHideSiteObject', maptype.HMAP, maptype.HSITE)
    def mapClearHideSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        return mapClearHideSiteObject_t (_hmap, _hsite)


# Запросить номер скрываемого объекта и номер листа на карте
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# number - указатель на поле для записи номера объекта
# list   - указатель на поле для записи номера листа
# При ошибке возвращает 0

    mapGetHideSiteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetHideSiteObject', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetHideSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: ctypes.POINTER(ctypes.c_long), _list: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetHideSiteObject_t (_hmap, _hsite, _number, _list)


# Установить порядок отображения карты
# hmap  - идентификатор открытых данных (документа)
# number - номер пользовательской карты в цепочке
# order  - флаг: 0 - под основной картой, 1 - над основной картой
# При ошибке возвращает 0

    mapSetSiteViewOrder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetSiteViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        return mapSetSiteViewOrder_t (_hmap, _number, _order)


# Запросить порядок отображения карты
# hmap   - идентификатор открытых данных (документа)
# number - номер пользовательской карты в цепочке
# Возвращает флаг: 0 - под основной картой, 1 - над основной картой
# При ошибке возвращает 0

    mapGetSiteViewOrder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetSiteViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        return mapGetSiteViewOrder_t (_hmap, _number)


# Поменять очередность отображения карт (sit) в цепочке
# hmap      - идентификатор открытых данных (документа)
# oldnumber - текущий номер файла в цепочке
# newnumber - устанавливаемый номер файла в цепочке
# При ошибке возвращает 0

    mapChangeOrderSiteShow_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeOrderSiteShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderSiteShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        return mapChangeOrderSiteShow_t (_hmap, _oldnumber, _newnumber)


# Очистить дерево объектов для отображения при больших изменениях листа карты для последующего перестроения
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты

    mapClearShowObjectList_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapClearShowObjectList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapClearShowObjectList(_hMmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> ctypes.c_void_p:
        return mapClearShowObjectList_t (_hMmap, _hsite, _list)


# Запросить значения масштаба нижней и верхней границ видимости карты
# hmap        - идентификатор открытых данных (документа)
# number      - номер пользовательской карты в цепочке (если number == 0, базовая карта)
# bottomscale - адрес для записи знаменателя масштаба нижней границы видимости карты
# topscale    - адрес для записи знаменателя масштаба верхней границы видимости карты
# При ошибке возвращает 0

    mapGetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetSiteRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetSiteRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)


# Установить значения масштаба нижней и верхней границ видимости карты
# hmap        - идентификатор открытых данных (документа)
# number      - номер пользовательской карты в цепочке (если number == 0, базовая карта)
# bottomscale - знаменатель масштаба нижней границы видимости карты
# topscale    - знаменатель масштаба верхней границы видимости карты
#              bottomscale <= topscale, иначе возвращает 0
# При ошибке возвращает 0

    mapSetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetSiteRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        return mapSetSiteRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)


# Запросить длину описания паспорта карты в виде записи
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetMapPassportRecordLength_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapPassportRecordLength', maptype.HMAP, maptype.HSITE)
    def mapGetMapPassportRecordLength(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetMapPassportRecordLength_t (_hmap, _hsite)


# Запросить описание паспорта карты в виде записи
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# buffer - указатель на запись для описания паспорта карты
# size   - размер записи
# Описание используется для передачи в другой процесс,на другой компьютер
# Передается описание только первого листа карты
# Размер буфера должен быть не менее, чем указано в mapGetMapPassportRecordLength
# При ошибке возвращает ноль

    mapGetMapPassportRecord_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetMapPassportRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long)
    def mapGetMapPassportRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int) -> int:
        return mapGetMapPassportRecord_t (_hmap, _hsite, _buffer, _size)


# Создать карту по записи паспорта карты
# hmap    - идентификатор открытых данных (документа)
# mapname - имя файла паспорта (#.map или #.sit)
# rscname - имя файла классификатора (#.rsc)
# buffer  - запись описания паспорта карты
# size    - размер записи
# Запись создается при вызове mapGetMapPassportRecord
# Если hmap = 0, возвращает идентификатор открытых данных (документа) HMAP (mapCreateMap в mapapi.h)
# При ошибке возвращает ноль

    mapPutMapPassportRecordUn_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapPutMapPassportRecordUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_char_p, ctypes.c_long)
    def mapPutMapPassportRecordUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _buffer: ctypes.c_char_p, _size: int) -> maptype.HSITE:
        return mapPutMapPassportRecordUn_t (_hmap, _mapname.buffer(), _rscname.buffer(), _buffer, _size)


# Запросить объект "Рамка листа"
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа c 1
# hobj  - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetSiteListFrameObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteListFrameObject', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HOBJ)
    def mapGetSiteListFrameObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hobj: maptype.HOBJ) -> int:
        return mapGetSiteListFrameObject_t (_hmap, _hsite, _list, _hobj)


# Запросить габариты объекта "Рамка листа"
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа
# frame - указатель на габариты листа в метрах
# Eсли рамки нет, габариты объекта "Рамка листа" заполняются по габаритам из паспорта
# При ошибке возвращает ноль

    mapGetSiteListFrame_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteListFrame', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteListFrame(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetSiteListFrame_t (_hmap, _hsite, _list, _frame)


# Cоздать пустой объект пользовательской карты
# hmap       - идентификатор открытых данных (документа)
# hsite      - идентификатор векторной карты в открытых данных, в которой будет расположен
#              создаваемый объект (для первой карты равен hmap)
# kind       - формат метрики
# text       - признак метрики с текстом (для объектов типа "подпись")
# pointcount - зарезервировать память под число точек (ускоряет первичное заполнение метрики из массива)
# После вызова функций типа What... и Seek... все параметры
# полученного объекта могут измениться (text, kind и т.п.)
# Для каждого полученного и больше не используемого идентификатора HOBJ необходим вызов функции mapFreeObject
# При ошибке возвращает ноль

    mapCreateSiteObjectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapCreateSiteObjectEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCreateSiteObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _kind: int = maptype.IDDOUBLE2, _text: int = 0, _pointcount: int = 0) -> maptype.HOBJ:
        return mapCreateSiteObjectEx_t (_hmap, _hsite, _kind, _text, _pointcount)

    mapCreateSiteObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapCreateSiteObject', maptype.HMAP, maptype.HSITE, ctypes.c_int, ctypes.c_int)
    def mapCreateSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _kind: int = maptype.IDDOUBLE2, _text: int = 0) -> maptype.HOBJ:
        return mapCreateSiteObject_t (_hmap, _hsite, _kind, _text)


# Определить идентификатор открытого документа для заданного объекта
# hobj - идентификатор объекта пользовательской карты
# При ошибке возвращает ноль

    mapGetObjectDocIdent_t = mapsyst.GetProcAddress(curLib,maptype.HMAP,'mapGetObjectDocIdent', maptype.HOBJ)
    def mapGetObjectDocIdent(_hobj: maptype.HOBJ) -> maptype.HMAP:
        return mapGetObjectDocIdent_t (_hobj)


# Определить идентификатор открытой векторной карты для заданного объекта
# hmap - идентификатор открытых данных (документа)
# hobj - идентификатор объекта пользовательской карты
# При ошибке возвращает ноль

    mapGetObjectSiteIdent_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetObjectSiteIdent', maptype.HMAP, maptype.HOBJ)
    def mapGetObjectSiteIdent(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HSITE:
        return mapGetObjectSiteIdent_t (_hmap, _hobj)


# Перенести объект на другую карту (пересчитать координаты и заменить ссылку в объекте на карту)
# hobj  - идентификатор объекта пользовательской карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При переносе объекта выполняется перекодировка объекта
# для нового классификатора, если код не найден - он устанавливается в ноль,
# прежнее значение сохраняется в семантике (код 32800)
# Для замены вызывается mapRegisterObject
# Метрика преобразуется в соответствии с типом карты
# Объект на исходной карте при этом не удаляется,
# для записи объекта в новой карте необходимо вызвать mapCommitObject
# При ошибке возвращает ноль

    mapChangeObjectMap_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeObjectMap', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapChangeObjectMap(_hobj: maptype.HOBJ, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapChangeObjectMap_t (_hobj, _hmap, _hsite)


# Сравнить параметры системы координат двух карт
# hmap1  - идентификатор открытых данных
# hsite1 - идентификатор векторной карты в открытых данных
# hmap2  - идентификатор открытых данных
# hsite2 - идентификатор векторной карты в открытых данных
# При несовпадении каких-либо значений параметров возвращает ненулевое значение
# Некоторые несовпадающие параметры могут считаться идентичными
# (например, топографическая карта UTM и обзорно-географическая карта UTM)
# При ошибке возвращает ноль

    mapCompareSiteSystemParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCompareSiteSystemParameters', maptype.HMAP, maptype.HSITE, maptype.HMAP, maptype.HSITE)
    def mapCompareSiteSystemParameters(_hmap1: maptype.HMAP, _hsite1: maptype.HSITE, _hmap2: maptype.HMAP, _hsite2: maptype.HSITE) -> int:
        return mapCompareSiteSystemParameters_t (_hmap1, _hsite1, _hmap2, _hsite2)


# Очистить содержание объекта и разместить его на заданной карте
# hobj  - идентификатор объекта пользовательской карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapClearSiteObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapClearSiteObject', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapClearSiteObject(_hobj: maptype.HOBJ, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapClearSiteObject_t (_hobj, _hmap, _hsite)


# Запросить габариты пользовательской карты в системе координат документа
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# list   - номер листа для многолистовой карты или 0
# dframe - координаты прямоугольной области района
# place  - система координат (PP_PLANE, PP_GEO, PP_PICTURE)
# При ошибке возвращает ноль

    mapGetSiteBorderEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteBorderEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetSiteBorderEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapGetSiteBorderEx_t (_hmap, _hsite, _list, _dframe, _place)


# Обновить размеры пользовательской карты и габариты района
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# dframe - координаты прямоугольной области района
# place  - система координат (PP_PLANE, PP_GEO, PP_PICTURE)
# Данная функция может применяться при создании карты, когда объектов еще
# нет и необходимо задать пустую область для окна карты
# При создании или обновлении объектов габариты пользовательской карты
# будут автоматически пересчитаны
# После вызова этой функции необходимо согласовать параметры
# скроллинга подобно масштабированию карты
# При ошибке возвращает ноль

    mapSetSiteBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapSetSiteBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        return mapSetSiteBorder_t (_hmap, _hsite, _dframe, _place)


# Запросить габариты пользовательской карты в системе координат карты в метрах
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# dframe - координаты прямоугольной области района
# При ошибке возвращает ноль

    mapGetSiteMapBorder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteMapBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteMapBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapGetSiteMapBorder_t (_hmap, _hsite, _dframe)


# Запросить приращение в метрах на местности, добавляемое при расчете габаритов объектов
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Пример: 1 мм на карте -> 1.00 # BaseScale / 1000.
# При ошибке возвращает ноль

    mapGetSiteObjectBorderReserve_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteObjectBorderReserve', maptype.HMAP, maptype.HSITE)
    def mapGetSiteObjectBorderReserve(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteObjectBorderReserve_t (_hmap, _hsite)


# Запросить высоту сечения в метрах для листа из паспорта
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа
# При ошибке возвращает ноль

    mapGetSiteListReliefHeight_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetSiteListReliefHeight', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteListReliefHeight(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> float:
        return mapGetSiteListReliefHeight_t (_hmap, _hsite, _list)


# Заменить файл классификатора и перекодировать карту
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# rscname - имя нового классификатора
# Поддерживается только для карт, размещенных локально и доступных на запись
# При ошибке возвращает ноль

    mapChangeSiteRsc_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeSiteRsc', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapChangeSiteRsc(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscname: mapsyst.WTEXT) -> int:
        return mapChangeSiteRsc_t (_hmap, _hsite, _rscname.buffer())


# Запросить имя классификатора из паспорта карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# rscname - строка для записи имени классификатора без пути
# size    - размер строки для записи имени
# При ошибке возвращает ноль

    mapGetSiteRscName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteRscName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteRscName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscname: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteRscName_t (_hmap, _hsite, _rscname.buffer(), _size)


# Запросить состояние (стиль) классификатора из паспорта карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При смене стиля могут быть изменены внутренние коды объектов
# Для проверки соответствия открытых данных классификатору можно сравнить этот
# показатель со значением в самом классификаторе (mapGetRscStyle)
# При ошибке возвращает ноль

    mapGetSiteRscStyle_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteRscStyle', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRscStyle(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteRscStyle_t (_hmap, _hsite)


# Установить порядок записи объектов на карту в цепочку отображения в порядке их поступления
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# flag  - признак последовательной записи и отображения объектов (0/1)
# Например, карта содержит один вид объектов
# При ошибке возвращает ноль

    mapSetSiteDirectOrder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteDirectOrder', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteDirectOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        return mapSetSiteDirectOrder_t (_hmap, _hsite, _flag)


# Запросить флаг записи объектов на карту в цепочку отображения в порядке их поступления
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Например, карта содержит один вид объектов
# При ошибке и выключенном режиме "прямой" записи возвращает ноль

    mapGetSiteDirectOrder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteDirectOrder', maptype.HMAP, maptype.HSITE)
    def mapGetSiteDirectOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteDirectOrder_t (_hmap, _hsite)


# Проверить параметры системы координат карты на соответствие цилиндрической проекции
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Если параметры соответствуют цилиндрической проекции (Меркатора, Миллера ...) возвращает ненулевое значение

    mapCheckCylindrical_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckCylindrical', maptype.HMAP, maptype.HSITE)
    def mapCheckCylindrical(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapCheckCylindrical_t (_hmap, _hsite)


# Запросить список изменившихся на ГИС Сервере объектов и обновить описание объектов в памяти
# hmap        - идентификатор открытых данных (документа)
# hsite       - идентификатор векторной карты в открытых данных
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
# Возвращает идентификатор списка объектов
# После обработки списка объектов он должен быть удален функцией mapFreeChangedObjectList
# При ошибке возвращает ноль

    mapGetChangedObjectListAndUpdate_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapGetChangedObjectListAndUpdate', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetChangedObjectListAndUpdate(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _maxcount: int = 1000, _skipaction: int = 0, _checkaction: int = 0) -> ctypes.c_void_p:
        return mapGetChangedObjectListAndUpdate_t (_hmap, _hsite, _maxcount, _skipaction, _checkaction)


# Запросить число объектов в списке
# hObjlist - идентификатор списка объектов
# Число изменившихся объектов может быть нулевым
# Если число изменившихся объектов больше предельного значения maxcount,
# заданого в функции mapGetChangedObjectListAndUpdate, то возвращается
# значение -1 и карта в памяти обновляется полностью
# Дополнительную информацию можно получить из журнала транзакций
# функциями из logapi.h

    mapGetChangedObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectCount', ctypes.c_void_p)
    def mapGetChangedObjectCount(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectCount_t (_hObjlist)


# Запросить номер последней транзакции, по которой заполнен список объектов
# hObjlist - идентификатор списка объектов
# При ошибке возвращает ноль

    mapGetChangedObjectAction_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectAction', ctypes.c_void_p)
    def mapGetChangedObjectAction(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectAction_t (_hObjlist)


# Запросить номер последней транзакции в журнале в момент формирования списка
# hObjlist - идентификатор списка объектов
# Номер последней транзакции может быть больше номера обработанной транзакции,
# если список слишком большой
# В этом случае нужно запросить следующую порцию обновлений
# При ошибке возвращает ноль

    mapGetChangedObjectTotalAction_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectTotalAction', ctypes.c_void_p)
    def mapGetChangedObjectTotalAction(_hObjlist: ctypes.c_void_p) -> int:
        return mapGetChangedObjectTotalAction_t (_hObjlist)


# Запросить описание изменившегося объекта
# hObjlist - идентификатор списка объектов
# number   - номер объекта в списке
# hmap     - идентификатор открытых данных (документа)
# hsite    - идентификатор векторной карты в открытых данных
# hobj     - идентификатор объекта карты в памяти
# При ошибке возвращает ноль

    mapGetChangedObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObject', ctypes.c_void_p, ctypes.c_long, maptype.HMAP, maptype.HSITE, maptype.HOBJ)
    def mapGetChangedObject(_hObjlist: ctypes.c_void_p, _number: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ) -> int:
        return mapGetChangedObject_t (_hObjlist, _number, _hmap, _hsite, _hobj)


# Запросить описание изменений объекта
# hObjlist - идентификатор списка объектов
# number   - номер объекта в списке
# Возвращает признак изменений объекта:
#     1 - обновлена семантика,
#     2 - обновлена метрика,
#     3 - обновлена метрика и семантика,
#     4 - объект создан,
#     8 - объект удален,
#     16 - объект восстановлен после удаления
# Нулевое значение может означать изменение кода объекта, границ видимости, масштабируемости

    mapGetChangedObjectState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectState', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectState(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectState_t (_hObjlist, _number)


# Запросить последовательный номер обновлённого объекта
# hObjlist - идентификатор списка объектов
# number   - номер объекта в списке
# При ошибке возвращает ноль

    mapGetChangedObjectNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectNumber', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectNumber(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectNumber_t (_hObjlist, _number)


# Запросить код вида объекта, который был до обновления
# hObjlist - идентификатор списка объектов
# number   - номер объекта в списке
# Возвращает внутренний код объекта в классификаторе
# У графических объектов код равен нулю

    mapGetChangedObjectCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectCode', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectCode(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectCode_t (_hObjlist, _number)


# Запросить уникальный номер объекта в листе, который был до обновления
# hObjlist - идентификатор списка объектов
# number   - номер объекта в списке
# В штатных ситуациях номер объекта не меняется при редактировании карты
# Возвращает идентификационный номер объекта (mapObjectKey)

    mapGetChangedObjectKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetChangedObjectKey', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectKey(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        return mapGetChangedObjectKey_t (_hObjlist, _number)


# Освободить ресурсы, занятые списком объектов, созданным функцией mapGetChangedObjectListAndUpdate
# hObjlist - идентификатор списка объектов

    mapFreeChangedObjectList_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeChangedObjectList', ctypes.c_void_p)
    def mapFreeChangedObjectList(_hObjlist: ctypes.c_void_p) -> ctypes.c_void_p:
        return mapFreeChangedObjectList_t (_hObjlist)


# Запросить дату и время по Гринвичу обновления карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# list    - номер листа карты
# date    - поле для записи даты в виде числа формата YYYYMMDD по Гринвичу
# time    - поле для записи числа секунд с 0 часов
# Если возвращаются нулевые значения, то карта после создания не редактировалась
# При ошибке возвращает ноль

    mapGetSiteDateAndTime_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteDateAndTime', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetSiteDateAndTime(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _date: ctypes.POINTER(ctypes.c_long), _time: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetSiteDateAndTime_t (_hmap, _hsite, _list, _date, _time)


# Запросить дату и время по Гринвичу создания карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# list    - номер листа карты
# date    - поле для записи даты в виде числа формата YYYYMMDD по Гринвичу
# time    - поле для записи числа секунд с 0 часов
# При ошибке возвращает ноль

    mapGetCreateSiteDateAndTime_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCreateSiteDateAndTime', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetCreateSiteDateAndTime(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _date: ctypes.POINTER(ctypes.c_long), _time: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapGetCreateSiteDateAndTime_t (_hmap, _hsite, _list, _date, _time)


# Удалить документ (произвольный файл) на сервере
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# При ошибке возвращает ноль

    mapDeleteSiteDocumentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapDeleteSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT) -> int:
        return mapDeleteSiteDocumentUn_t (_hmap, _hsite, _alias.buffer())


# Считать документ на сервере
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# name   - полный путь к считанному документу, строка заполняется
#          автоматически при считывании документа, имя документа и
#          дата редактирования устанавливаются такими, какими они были
#          при записи в mapSaveSiteDocument.
# size   - размер буфера в байтах для записи пути (не менее 520 байт)
# Например: HOST#WorkServer#ALIAS#Моя_Карта#DOC#MyFolder#schema.png
# При успешном выполнении возвращает имя считанного файла документа в поле name
# При ошибке возвращает ноль

    mapReadSiteDocumentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapReadSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapReadSiteDocumentUn_t (_hmap, _hsite, _alias.buffer(), _name.buffer(), _size)


# Считать информацию о документе на сервере
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# alias - алиас документа на сервере
# time  - время обновления файла в хранилище
# size  - размер файла документа
# При успешном выполнении возвращает размер исходного файла и время его обновления в хранилище
# При ошибке возвращает ноль

    mapReadSiteDocumentInfoUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapReadSiteDocumentInfoUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.SYSTEMTIME), ctypes.POINTER(ctypes.c_int64))
    def mapReadSiteDocumentInfoUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _time: ctypes.POINTER(maptype.SYSTEMTIME), _size: ctypes.POINTER(ctypes.c_int64)) -> int:
        return mapReadSiteDocumentInfoUn_t (_hmap, _hsite, _alias.buffer(), _time, _size)


# Сохранить документ на сервере
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# name   - полный путь к сохраняемому документу (один файл любого размера)
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#"),
#          строка формируется сервером и заполняется при сохранении документа
# size   - размер буфера для записи алиаса (не менее 260 символов)
# При успешном выполнении возвращает алиас документа на сервере
# При ошибке возвращает ноль

    mapSaveSiteDocumentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSaveSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapSaveSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _alias: mapsyst.WTEXT, _size: int) -> int:
        return mapSaveSiteDocumentUn_t (_hmap, _hsite, _name.buffer(), _alias.buffer(), _size)


# Запросить путь к кэшу документа на клиенте
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# alias  - алиас документа на сервере (может храниться в семантике
#          объекта карты, начинается со строки "HOST#")
# name   - полный путь к документу
# size   - размер буфера для записи пути (не менее 260 символов)
# При успешном выполнении возвращает имя кэша файла документа в поле name
# Операция чтения не выполняется, файл может отсутствовать
# При успешном выполнении возвращает ненулевое значение,
# если файл имеется в кэш - возвращает положительное значение, иначе - отрицательное
# При ошибке возвращает ноль

    mapGetSiteDocumentNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteDocumentNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteDocumentNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteDocumentNameUn_t (_hmap, _hsite, _alias.buffer(), _name.buffer(), _size)


# Запросить - можно ли сохранить документ с картой
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если карта размещена на сервере и может редактироваться,
# то в ней есть хранилище документов
# При ошибке возвращает ноль

    mapIsSiteDocumentStorage_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteDocumentStorage', maptype.HMAP, maptype.HSITE)
    def mapIsSiteDocumentStorage(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteDocumentStorage_t (_hmap, _hsite)


# Считать документ из SITZ/MAPZ архива в память
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа, в котором записан документ
# name  - имя документа
# size  - указатель на размер считанного документа и выделенной памяти
# error - код ошибки при неудаче (IDS_PARM, IDS_MEMORY, IDS_READ, IDS_FILE_NOT_FOUND)
# Возвращает адрес документа в памяти
# При ошибке возвращает ноль

    mapGetDocumentFromSitz_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetDocumentFromSitz', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetDocumentFromSitz(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetDocumentFromSitz_t (_hmap, _hsite, _list, _name.buffer(), _size, _error)


# Считать документ из SITZ/MAPZ архива в память
# hmap   - идентификатор открытых данных (документа)
# hPaint - идентификатор контекста отображения для многопоточного вызова
# name   - имя документа
# size   - указатель на размер считанного документа и выделенной памяти
# error  - код ошибки при неудаче (IDS_PARM, IDS_MEMORY, IDS_READ, IDS_FILE_NOT_FOUND)
# Возвращает адрес документа в памяти
# При ошибке возвращает ноль

    mapGetDocumentFromSitzEx_t = mapsyst.GetProcAddress(curLib,ctypes.POINTER(ctypes.c_char),'mapGetDocumentFromSitzEx', maptype.HPAINT, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetDocumentFromSitzEx(_hPaint: maptype.HPAINT, _name: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        return mapGetDocumentFromSitzEx_t (_hPaint, _name.buffer(), _size, _error)


# Освободить память с прочитанным документом
# memory - адрес памяти, полученной при вызове mapGetDocumentFromSitz/mapGetDocumentFromSitzEx

    mapFreeDocumentFromSitz_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapFreeDocumentFromSitz', ctypes.c_char_p)
    def mapFreeDocumentFromSitz(_memory: ctypes.c_char_p) -> ctypes.c_void_p:
        return mapFreeDocumentFromSitz_t (_memory)


# Отобразить образец вида объекта по номеру записи в классификаторе объектов (incode)
# hmap     - идентификатор открытых данных (документа)
# hsite    - идентификатор векторной карты в открытых данных
# hdc      - идентификатор контекста устройства вывода,
# rect     - координаты фрагмента карты (Draw) в изображении (Picture)
# incode   - внутренний код объекта
# text     - текст подписи или ноль
# factor   - коэффициент масштабируемости изображения 50, 100, 200...
# semvalue - запись семантики
# Используется в диалогах выбора вида объекта
# При ошибке возвращает ноль

    mapPaintExampleSiteObjectPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPaintExampleSiteObjectPro', maptype.HMAP, maptype.HSITE, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.SEMANTIC))
    def mapPaintExampleSiteObjectPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _text: mapsyst.WTEXT, _factor: int, _semvalue: ctypes.POINTER(maptype.SEMANTIC)) -> int:
        return mapPaintExampleSiteObjectPro_t (_hmap, _hsite, _hdc, _rect, _incode, _text.buffer(), _factor, _semvalue)


# Запросить состав отображаемых объектов пользовательской карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска/отображения, в который будут помещены
#           текущие условия отображения, создание в mapCreateMapSelectContext
# При ошибке возвращает ноль

    mapGetSiteViewSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteViewSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapGetSiteViewSelect_t (_hmap, _hsite, _hselect)


# Установить состав отображаемых объектов
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска/отображения

    mapSetSiteViewSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'mapSetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteViewSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> ctypes.c_void_p:
        return mapSetSiteViewSelect_t (_hmap, _hsite, _hselect)


# Запросить номер состояния условий отображения карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При обновлении условий номер состояния меняется
# При ошибке возвращает ноль

    mapGetSiteViewSelectState_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteViewSelectState', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewSelectState(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteViewSelectState_t (_hmap, _hsite)


# Запросить яркость карты (от -16 до +16)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteBright_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteBright', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBright(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteBright_t (_hmap, _hsite)


# Установить яркость карты (от -16 до +16)
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# bright - яркость карты
# При ошибке возвращает ноль

    mapSetSiteBright_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteBright', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteBright(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _bright: int) -> int:
        return mapSetSiteBright_t (_hmap, _hsite, _bright)


# Запросить контрастность  (от -16 до +16)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteContrast_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteContrast', maptype.HMAP, maptype.HSITE)
    def mapGetSiteContrast(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteContrast_t (_hmap, _hsite)


# Установить контрастность (от -16 до +16)
# hmap     - идентификатор открытых данных (документа)
# hsite    - идентификатор векторной карты в открытых данных
# contrast - контрастность
# При ошибке возвращает ноль

    mapSetSiteContrast_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteContrast', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteContrast(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _contrast: int) -> int:
        return mapSetSiteContrast_t (_hmap, _hsite, _contrast)


# Запросить параболическую яркость
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteGamma_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteGamma', maptype.HMAP, maptype.HSITE)
    def mapGetSiteGamma(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteGamma_t (_hmap, _hsite)


# Установить параболическую яркость
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# gamma - параболическая яркость
# При ошибке возвращает ноль

    mapSetSiteGamma_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteGamma', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteGamma(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _gamma: int) -> int:
        return mapSetSiteGamma_t (_hmap, _hsite, _gamma)


# Запросить число цветов в текущей палитре карты (обычно 16 или 32)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteColorsCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteColorsCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteColorsCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteColorsCount_t (_hmap, _hsite)


# Запросить текущую палитру карты (с учетом яркости/контрастности)
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# При ошибке возвращает ноль

    mapGetSitePalette_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePalette', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetSitePalette(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetSitePalette_t (_hmap, _hsite, _colors, _count)


# Запросить текущую палитру карты (без учета яркости/контрастности)
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# При ошибке возвращает ноль

    mapGetSiteColors_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteColors', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetSiteColors(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        return mapGetSiteColors_t (_hmap, _hsite, _colors, _count)


# Установить текущую палитру карты
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# number - номер эталонной палитры в классификаторе
# Если colors равно 0, устанавливается палитра из классификатора
# (палитра классификатора не меняется, изменения будут временными)
# При ошибке возвращает ноль

    mapSetSiteColorsEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteColorsEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapSetSiteColorsEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapSetSiteColorsEx_t (_hmap, _hsite, _colors, _count, _number)


# Установить текущую палитру в карте из классификатора
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# number - номер палитры в класификаторе
# При ошибке возвращает ноль

    mapSetSitePaletteByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSitePaletteByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        return mapSetSitePaletteByNumber_t (_hmap, _hsite, _number)


# Запросить палитру из классификатора по номеру
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# colors - указатель на структуру COLORREF первого цвета в палитре
# count  - количество цветов (не более 256)
# number - номер палитры в класификаторе
# При ошибке возвращает ноль

    mapGetSitePaletteByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetSitePaletteByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        return mapGetSitePaletteByNumber_t (_hmap, _hsite, _colors, _count, _number)


# Запросить номер текущей палитры в карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSitePaletteNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaletteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePaletteNumber_t (_hmap, _hsite)


# Запросить число палитр в классификаторе карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSitePaletteCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaletteCount', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePaletteCount_t (_hmap, _hsite)


# Запросить название палитры по номеру
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# name  - адрес буфера для записи названия палитры
# size  - размер буфера для записи названия палитры
# При ошибке возвращает ноль

    mapGetSitePaletteName_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaletteName', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSitePaletteName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSitePaletteName_t (_hmap, _hsite, _number, _name.buffer(), _size)


# Запросить условия поиска активных объектов по карте
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска/отображения, в который будут помещены
#           текущие условия поиска, создание в mapCreateMapSelectContext
# Активные объекты доступны для интерактивного выбора (оператором)
# Выбор выполняется функцией mapWhatActiveObject
# При ошибке возвращает ноль

    mapGetSiteActiveSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteActiveSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapGetSiteActiveSelect_t (_hmap, _hsite, _hselect)


# Установить условия поиска активных объектов для карты
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска, который содержит устанавливаемые условия поиска
# Активные объекты - доступны для интерактивного выбора (оператором)
# Выбор выполняется функцией mapWhatActiveObject
# При ошибке возвращает ноль

    mapSetSiteActiveSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteActiveSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapSetSiteActiveSelect_t (_hmap, _hsite, _hselect)


# Запросить условия поиска объектов по карте
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска/отображения, в который будут помещены
#           текущие условия поиска, создание в mapCreateMapSelectContext
# При ошибке возвращает ноль

    mapGetSiteSeekSelect_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteSeekSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteSeekSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapGetSiteSeekSelect_t (_hmap, _hsite, _hselect)


# Установить условия поиска объектов для карты
# hmap       - идентификатор открытых данных (документа)
# hsite      - идентификатор векторной карты в открытых данных
# hselect    - идентификатор контекста поиска, который содержит устанавливаемые условия поиска
# keepsample - признак сохранения в условиях поиска списка объектов (Sample)
# При ошибке возвращает ноль

    mapSetSiteSeekSelectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteSeekSelectEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapSetSiteSeekSelectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _keepsample: int) -> int:
        return mapSetSiteSeekSelectEx_t (_hmap, _hsite, _hselect, _keepsample)


# Поиск объекта по уникальному номеру на карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj  - идентификатор существующего объекта, созданного функцией CreateObject
#         или CreateSiteObject, в котором будет размещен результат поиска
# key   - уникальный номер объекта на карте
# При ошибке возвращает ноль

    mapSeekSiteObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekSiteObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long)
    def mapSeekSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _key: int) -> maptype.HOBJ:
        return mapSeekSiteObject_t (_hmap, _hsite, _hobj, _key)


# Поиск объектов по заданным условиям среди всех объектов
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hobj    - идентификатор существующего объекта, созданного функцией mapCreateObject
#           или mapCreateSiteObject, в котором будет размещен результат поиска
# hselect - условия поиска объекта
# flag    - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# skip    - число найденных объектов, которые нужно пропустить перед выдачей результата
# Если объект не найден - возвращает ноль

    mapSeekSiteSelectObjectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekSiteSelectObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSeekSiteSelectObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int, _skip: int) -> maptype.HOBJ:
        return mapSeekSiteSelectObjectEx_t (_hmap, _hsite, _hobj, _hselect, _flag, _skip)


# Поиск ближайшего объекта по заданным условиям среди всех объектов
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных в которой ищется объект
# hobj    - идентификатор существующего объекта созданного функцией mapCreateObject() или
#           mapCreateSiteObject(), в котором будет размещен результат поиска
# point   - координаты точки в метрах в системе карты, среди всех подходящих объектов
#           ищется ближайший к заданной точке
# target  - координаты ближайшей виртуальной точки на контуре объекта в метрах документа
# hselect - условия поиска объекта
# flag    - дополнительные условия поиска объектов: WO_CANCEL, WO_VISUAL; флажки типа WO_FIRST, WO_NEXT не учитываются
# Если объект не найден - возвращает ноль

    mapSeekSiteSelectNearestObjectEx_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekSiteSelectNearestObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteSelectNearestObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT), _hselect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        return mapSeekSiteSelectNearestObjectEx_t (_hmap, _hsite, _hobj, _point, _target, _hselect, _flag)


# Запросить число объектов, удовлетворяющих условиям поиска
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# hselect - условия поиска объекта
# Для функции mapSeekSiteSelectObject (выполняет внутренний перебор объектов)
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteSelectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSiteSelectCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteSelectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapSeekSiteSelectCount_t (_hmap, _hsite, _hselect)


# Запросить число объектов, удовлетворяющих условиям поиска в заданном листе
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - условия поиска объекта
# list    - номер листа для многолистовой карты, с 1
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteSelectCountForList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSiteSelectCountForList', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapSeekSiteSelectCountForList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _list: int) -> int:
        return mapSeekSiteSelectCountForList_t (_hmap, _hsite, _hselect, _list)


# Поиск объектов по заданным условиям среди отображаемых объектов
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hobj    - идентификатор существующего объекта, созданного функцией mapCreateObject
#           или mapCreateSiteObject, в котором будет размещен результат поиска
# hselect - условия поиска объекта
# flag    - порядок поиска объектов (WO_FIRST, WO_NEXT...)
# Если объект не найден - возвращает ноль

    mapSeekSiteViewObject_t = mapsyst.GetProcAddress(curLib,maptype.HOBJ,'mapSeekSiteViewObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekSiteViewObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        return mapSeekSiteViewObject_t (_hmap, _hsite, _hobj, _hselect, _flag)


# Запросить число объектов, удовлетворяющих условиям поиска
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - условия поиска объекта
# Для функции mapSeekSiteSelectObject (выполняет внутренний перебор объектов)
# При ошибке или отсутствии объектов возвращает ноль

    mapSeekSiteViewCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSeekSiteViewCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteViewCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        return mapSeekSiteViewCount_t (_hmap, _hsite, _hselect)


# Проверить наличие кода семантики на карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1
# code  - код семантики
# В случае отсутствия возвращает ноль

    mapCheckExistSemanticInSheetByCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCheckExistSemanticInSheetByCode', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapCheckExistSemanticInSheetByCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _code: int) -> int:
        return mapCheckExistSemanticInSheetByCode_t (_hmap, _hsite, _list, _code)


# Проверить что хэш семантик готов
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Если не готов - возвращает "-1"
# При ошибке возвращает ноль

    mapIsSemanticHashReady_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSemanticHashReady', maptype.HMAP, maptype.HSITE)
    def mapIsSemanticHashReady(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSemanticHashReady_t (_hmap, _hsite)


# Запросить идентификатор карты, для которой созданы/заполнены условия поиска
# hmap    - идентификатор открытых данных (документа)
# hselect - условия поиска объектов
# При ошибке возвращает ноль

    mapGetSiteIdentForSelect_t = mapsyst.GetProcAddress(curLib,maptype.HSITE,'mapGetSiteIdentForSelect', maptype.HMAP, maptype.HSELECT)
    def mapGetSiteIdentForSelect(_hmap: maptype.HMAP, _hselect: maptype.HSELECT) -> maptype.HSITE:
        return mapGetSiteIdentForSelect_t (_hmap, _hselect)


# Запросить число отображаемых объектов на карте
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# При ошибке или отсутствии объектов возвращает ноль

    mapGetViewObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetViewObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetViewObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetViewObjectCount_t (_hmap, _hsite)


# Запросить число отображаемых объектов в документе
# hmap   - идентификатор открытых данных (документа)
# При ошибке или отсутствии объектов возвращает ноль

    mapGetTotalViewObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetTotalViewObjectCount', maptype.HMAP)
    def mapGetTotalViewObjectCount(_hmap: maptype.HMAP) -> int:
        return mapGetTotalViewObjectCount_t (_hmap)


# Опросить наличие списка объектов в контексте условий поиска/отображения карты
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# Список объектов содержит номер листа и номер объекта в листе
# Если список объектов не установлен,возвращает ноль

    mapIsSiteSeekSample_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsSiteSeekSample', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSeekSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsSiteSeekSample_t (_hmap, _hsite)


# Запросить последовательный номер объекта по его уникальному идентификатору
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# key    - уникальный идентификатор объекта
# При ошибке возвращает ноль

    mapGetSiteObjectNumberByKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteObjectNumberByKey', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteObjectNumberByKey(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _key: int) -> int:
        return mapGetSiteObjectNumberByKey_t (_hmap, _hsite, _key)


# Запросить уникальный идентификатор объекта по последовательному номеру объекта
# hmap     - идентификатор открытых данных (документа)
# hsite    - идентификатор векторной карты в открытых данных
# number   - последовательный номер объекта
# list     - номер листа карты с 1
# isdelete - признак учета удаленных объектов
# При ошибке возвращает ноль

    mapGetSiteObjectKeyByNumberEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteObjectKeyByNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetSiteObjectKeyByNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _list: int = 1, _isdelete: int = 0) -> int:
        return mapGetSiteObjectKeyByNumberEx_t (_hmap, _hsite, _number, _list, _isdelete)


# Запросить базовый масштаб карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteScale', maptype.HMAP, maptype.HSITE)
    def mapGetSiteScale(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteScale_t (_hmap, _hsite)


# Изменить базовый масштаб пользовательской карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# scale - базовый масштаб
# При отображении в базовом масштабе пользовательской карты размер условных
# знаков на карте будет соответствовать их размеру в классификаторе RSC
# При ошибке возвращает ноль

    mapSetSiteScale_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteScale', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteScale(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _scale: int) -> int:
        return mapSetSiteScale_t (_hmap, _hsite, _scale)


# Запросить главное название карты (листа)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# name  - адрес строки для размещения результата
# size  - размер строки для размещения результата в байтах
# При ошибке возвращает пустую строку

    mapGetSiteNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        return mapGetSiteNameUn_t (_hmap, _hsite, _name.buffer(), _size)


# Установить главное название карты (листа)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# name  - главное название карты
# При ошибке возвращает пустую строку

    mapSetSiteNameEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteNameEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetSiteNameEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT) -> int:
        return mapSetSiteNameEx_t (_hmap, _hsite, _name.buffer())


# Запросить тип карты (описание типов в maptype.h)
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteType(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteType_t (_hmap, _hsite)


# Запросить координату X юго-западного угла габаритов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает координату в метрах на север в системе координат документа

    mapGetSiteX1_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetSiteX1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX1(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        return mapGetSiteX1_t (_hmap, _hsite)


# Запросить координату Y юго-западного угла габаритов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает координату в метрах на восток в системе координат документа

    mapGetSiteY1_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetSiteY1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY1(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        return mapGetSiteY1_t (_hmap, _hsite)


# Запросить координату X северо-восточного угла габаритов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает координату в метрах на север в системе координат документа

    mapGetSiteX2_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetSiteX2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX2(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        return mapGetSiteX2_t (_hmap, _hsite)


# Запросить координату Y северо-восточного угла габаритов карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Возвращает координату в метрах на восток в системе координат документа

    mapGetSiteY2_t = mapsyst.GetProcAddress(curLib,ctypes.c_double,'mapGetSiteY2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY2(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        return mapGetSiteY2_t (_hmap, _hsite)


# Запросить количество объектов в пользовательской карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteObjectCount_t (_hmap, _hsite)


# Запросить количество объектов в пользовательской карте, исключая удаленные
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteRealObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteRealObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRealObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteRealObjectCount_t (_hmap, _hsite)


# Запросить количество удаленных объектов в листе карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа (для совместимости с многолистовыми картами)
# При ошибке возвращает ноль

    mapGetSiteDeleteObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteDeleteObjectCount', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteDeleteObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        return mapGetSiteDeleteObjectCount_t (_hmap, _hsite, _list)


# Запросить идентификатор нового объекта, который будет создан на карте следующим
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа (для совместимости с многолистовыми картами)
# Идентификатор созданного объекта может быть запрошен функцией mapObjectKey
# При ошибке возвращает ноль

    mapGetSiteNewObjectKey_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteNewObjectKey', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteNewObjectKey(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int = 1) -> int:
        return mapGetSiteNewObjectKey_t (_hmap, _hsite, _list)


# Запросить общее число листов на карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных (может быть равен hmap
#         для доступа к основной карте)
# При ошибке возвращает ноль

    mapGetSiteListCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteListCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteListCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteListCount_t (_hmap, _hsite)


# Удалить указанный лист карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа с 1
# При ошибке возвращает ноль

    mapDeleteSiteList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSiteList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapDeleteSiteList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        return mapDeleteSiteList_t (_hmap, _hsite, _list)


# Изменить порядковый номер листа карты
# hmap      - идентификатор открытых данных (документа)
# hsite     - идентификатор векторной карты в открытых данных
# oldnumber - номер листа карты
# newnumber - новое положение листа карты в паспорте
# При ошибке возвращает ноль

    mapSetSiteListOrder_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteListOrder', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSetSiteListOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _oldnumber: int, _newnumber: int) -> int:
        return mapSetSiteListOrder_t (_hmap, _hsite, _oldnumber, _newnumber)


# Запросить количество объектов в листе
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных (может быть равен hmap
#          для доступа к основной карте)
# number - номер листа карты (для пользовательской карты обычно равен 1)
# При ошибке возвращает ноль

    mapGetSiteObjectCountInList_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteObjectCountInList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteObjectCountInList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int = 1) -> int:
        return mapGetSiteObjectCountInList_t (_hmap, _hsite, _number)


# Запросить паспортные данные векторной карты
# hmap        - идентификатор открытых данных (документа)
# hsite       - идентификатор векторной карты в открытых данных
# sheetnumber - номер листа карты c 1
# Структуры MAPREGISTEREX, LISTREGISTER, SHEETNAMES описаны в mapcreat.h
# При ошибке возвращает ноль

    mapGetSiteInfoPro_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteInfoPro', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), ctypes.c_long)
    def mapGetSiteInfoPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _sheetnumber: int) -> int:
        return mapGetSiteInfoPro_t (_hmap, _hsite, _mapreg, _listreg, _sheetnames, _sheetnumber)


# Обновить паспортные данные векторной карты
# hmap        - идентификатор открытых данных
# hsite       - идентификатор векторной карты в открытых данных
# mainname    - главное название многолистовой карты (MAP),
#               для пользовательской карты совпадает с названием листа карты
# sheetnumber - номер листа карты c 1
# type        - тип локального преобразования координат (описан в TRANSFORMTYPE в mapcreat.h) или 0
# parm        - параметры локального преобразования координат или 0
# transform   - признак пересчета координат при смене параметров:
#               0 - не пересчитывать;
#               1 - пересчитать координаты объектов
# Структуры MAPREGISTEREX, LISTREGISTER, SHEETNAMES, DATUMPARAM, ELLIPSOIDPARAM,
# LOCALTRANSFORM описаны в mapcreat.h
# При смене параметров проекции карта будет трансформирована в соответствии
# с новыми параметрами проекции из MAPREGISTEREX, если параметр transform не равен нулю
# Для листа карты можно изменить название, номенклатуру и метаданные
# (LISTREGISTER), координаты рамки (если территория карты
# ограничена рамкой) пересчитываются автоматически
# Время выполнения функции соответствует времени выполнения
# трансформировании карты (при смене параметров проекции)
# При выполнении трансформирования посылается сообщение
# WM_PROGRESSBAR (maptype.h) окну (mapSetHandleForMessage)
# Если при обновлении параметров проекции выполнялось
# трансформирование карты - возвращает отрицательное значение, иначе - положительное
# При ошибке возвращает ноль

    mapUpdateSiteInfo_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapUpdateSiteInfo', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_long)
    def mapUpdateSiteInfo(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _sheetnumber: int, _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _transform: int) -> int:
        return mapUpdateSiteInfo_t (_hmap, _hsite, _mapreg, _listreg, _sheetnames, _mainname.buffer(), _sheetnumber, _datum, _ellparm, _type, _parm, _transform)


# Установить параметры Datum для карты
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# datum - параметры датума
# Структура DATUMPARAM описана в mapcreat.h
# Может выполняться или до записи объектов на карту или
# в другой момент - для карты хранящей геодезические координаты объектов
# При ошибке возвращает ноль

    mapSetSiteDatum_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetSiteDatum(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapSetSiteDatum_t (_hmap, _hsite, _parm)


# Запросить параметры Datum для карты
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# datum - параметры датума
# Структура DATUMPARAM описана в mapcreat.h
# При ошибке возвращает ноль

    mapGetSiteDatum_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetSiteDatum(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return mapGetSiteDatum_t (_hmap, _hsite, _parm)


# Установить параметры эллипсоида для карты
# hmap      - идентификатор открытых данных
# hsite     - идентификатор векторной карты в открытых данных
# ellipsoid - параметры эллипсоида
# Структура ELLIPSOIDPARAM описана в mapcreat.h
# Может выполняться или до записи объектов на карту или
# в другой момент - для карты хранящей геодезические координаты объектов
# При ошибке возвращает ноль

    mapSetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetSiteEllipsoidParameters(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapSetSiteEllipsoidParameters_t (_hmap, _hsite, _ellipsoid)


# Запросить параметры эллипсоида для карты
# hmap      - идентификатор открытых данных
# hsite     - идентификатор векторной карты в открытых данных
# ellipsoid - параметры эллипсоида
# Структура ELLIPSOIDPARAM описана в mapcreat.h
# При ошибке возвращает ноль

    mapGetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetSiteEllipsoidParameters(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return mapGetSiteEllipsoidParameters_t (_hmap, _hsite, _ellipsoid)


# Запросить тип локального преобразования системы координат
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# При ошибке или отсутствии преобразования возвращает ноль

    mapGetSiteLocalTransformationType_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteLocalTransformationType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLocalTransformationType(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteLocalTransformationType_t (_hmap, _hsite)


# Запросить адрес параметров локального преобразования системы координат
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# parm  - параметры локального преобразования координат
# Структура LOCALTRANSFORM описана в mapcreat.h
# Возвращает тип локального преобразования системы координат
# При ошибке или отсутствии преобразования возвращает ноль

    mapGetSiteLocalTransformationParm_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteLocalTransformationParm', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetSiteLocalTransformationParm(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapGetSiteLocalTransformationParm_t (_hmap, _hsite, _parm)


# Установить параметры локального преобразования системы координат
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# type  - тип локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# parm  - параметры локального преобразования координат
# Структура LOCALTRANSFORM описана в mapcreat.h
# При ошибке или отсутствии преобразования возвращает ноль

    mapSetLocalTransformation_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetLocalTransformation', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetLocalTransformation(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return mapSetLocalTransformation_t (_hmap, _hsite, _type, _parm)


# Запросить код EPSG системы координат
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetEPSGCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetEPSGCode', maptype.HMAP, maptype.HSITE)
    def mapGetEPSGCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetEPSGCode_t (_hmap, _hsite)


# Установить код EPSG системы координат
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# code  -  код EPSG
# При ошибке возвращает ноль

    mapSetEPSGCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetEPSGCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetEPSGCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int) -> int:
        return mapSetEPSGCode_t (_hmap, _hsite, _code)


# Запросить идентификатор системы координат
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# ident - строка длиной не менее 64 символов для размещения идентификатора
# size  - длина строки
# При ошибке возвращает ноль

    mapGetCRSIdentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetCRSIdentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ident: mapsyst.WTEXT, _size: int) -> int:
        return mapGetCRSIdentUn_t (_hmap, _hsite, _ident.buffer(), _size)


# Установить идентификатор системы координат
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# ident - строка со значением идентификатора не более 64 символов
# При ошибке возвращает ноль

    mapSetCRSIdentUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetCRSIdentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ident: mapsyst.WTEXT) -> int:
        return mapSetCRSIdentUn_t (_hmap, _hsite, _ident.buffer())


# Запросить идентификатор набора данных листа карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 или 0 (запрос или установка идентификатора набора листов)
#         для пользовательской карты list равен 1
# ident - строка длиной не менее 33 символов для размещения идентификатора
# size  - длина строки
# Для чтения значения необходимо подать буфер не менее 33 символов (32 + 1 для замыкающего нуля)
# При ошибке возвращает ноль

    mapGetDataIdent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapGetDataIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p, _size: int) -> int:
        return mapGetDataIdent_t (_hmap, _hsite, _list, _ident, _size)


# Установить идентификатор набора данных листа карты
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# list  - номер листа карты с 1 или 0 (запрос или установка идентификатора набора листов)
#         для пользовательской карты list равен 1
# ident - строка со значением идентификатора (обычно 32 шестнадцатеричных символа GUID и замыкающий ноль)
# При записи будут записаны не более 32 символов
# При ошибке возвращает ноль

    mapSetDataIdent_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_char_p)
    def mapSetDataIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p) -> int:
        return mapSetDataIdent_t (_hmap, _hsite, _list, _ident)


# Запросить гриф секретности карты
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# code  - код степени секретности данных:
#         1 - открытая информация (unclassified),
#         2 - информация с ограниченным доступом (restricted),
#         3 - информация для служебного пользования (confidential),
#         4 - секретная информация (secret),
#         5 - совершенно секретная информация (topsecret)
# При ошибке или отсутствии значения возвращает ноль

    mapGetSiteSecurityCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteSecurityCode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteSecurityCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteSecurityCode_t (_hmap, _hsite)


# Установить гриф секретности карты
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# code  - код степени секретности данных:
#         1 - открытая информация (unclassified),
#         2 - информация с ограниченным доступом (restricted),
#         3 - информация для служебного пользования (confidential),
#         4 - секретная информация (secret),
#         5 - совершенно секретная информация (topsecret)
# При ошибке или отсутствии значения возвращает ноль

    mapSetSiteSecurityCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSiteSecurityCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteSecurityCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int) -> int:
        return mapSetSiteSecurityCode_t (_hmap, _hsite, _code)


# Запросить формат рамки листа для плана
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# Возвращает:
#    0 -  не установлен,
#    1 - установлен пользователем, 2 - A0(841x1189 мм),
#    3 - A1(594x841 мм),           4 - A2(420x594 мм),
#    5 - A3(297x420 мм),           6 - A4(210x297 мм)
# При ошибке или отсутствии значения возвращает ноль

    mapGetSitePaperSize_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSitePaperSize', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaperSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSitePaperSize_t (_hmap, _hsite)


# Установить формат рамки листа для плана
# hmap  - идентификатор открытых данных
# hsite - идентификатор векторной карты в открытых данных
# size  - формат рамки листа:
#         0 -  не установлен,
#         1 - установлен пользователем,  2 - A0 (841x1189 мм),
#         3 - A1 (594x841 мм),           4 - A2 (420x594 мм),
#         5 - A3 (297x420 мм),           6 - A4 (210x297 мм)
# При ошибке или отсутствии значения возвращает ноль

    mapSetSitePaperSize_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSitePaperSize', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSitePaperSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _size: int) -> int:
        return mapSetSitePaperSize_t (_hmap, _hsite, _size)


# Запросить сведения о реально имеющихся объектах на карте
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска, в который будут помещены условия, соответствующие имеющимся объектам
#           (слои, объекты, локализации - доступ в seekapi.h)
# force   - признак принудительного обновления состава условий поиска по реально
#           имеющимся на карте объектам (для больших карт длительное выполнение)
# При ошибке возвращает ноль

    mapGetSiteUsedSelectEx_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteUsedSelectEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapGetSiteUsedSelectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _force: int) -> int:
        return mapGetSiteUsedSelectEx_t (_hmap, _hsite, _hselect, _force)


# Запросить установлены ли сведения об имеющихся объектах
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# Если по условиям поиска все объекты выбираются без исключений -
# возвращает ноль, иначе - ненулевое значение

    mapIsUsedSelectActive_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapIsUsedSelectActive', maptype.HMAP, maptype.HSITE)
    def mapIsUsedSelectActive(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapIsUsedSelectActive_t (_hmap, _hsite)


# Трансформировать векторную карту в заданную систему координат
# hmap       - идентификатор открытых данных (документа)
# hsite      - идентификатор векторной карты в открытых данных
# hmessage   - идентификатор окна (HWND/функция обратного вызова в Linux) для получения сообщений WM_PROGRESSBARUN или 0
# mapname    - имя создаваемой карты в заданной системе координат
# mapreg     - структура параметров системы координат карты
# ellparam   - параметры эллипсоида (необязательный параметр)
# datum      - параметры DATUM для карты (необязательный параметр)
# ttype      - тип локального преобразования координат (TRANSFORMTYPE в mapcreat.h) или 0
# tparm      - параметры локального преобразования координат или 0
# issavecopy - признак создания копии исходной карты в поддиректории ИМЯКАРТЫ.YYYYMMDD.HHMMSS
# error      - код ошибки при выполнении трансформирвоания
# callevent  - адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
# parm       - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы),
#              вторым параметром в вызываемой функции передается процент от 0 до 100
# Структуры MAPREGISTEREX, DATUMPARAM, ELLIPSOIDPARAM, LOCALTRANSFORM описаны в mapcreat.h
# При ошибке возвращает ноль

    mapTransformationSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapTransformationSite', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapTransformationSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hmessage: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _issavecopy: int, _error: ctypes.POINTER(ctypes.c_long), _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return mapTransformationSite_t (_hmap, _hsite, _hmessage, _mapname.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm, _issavecopy, _error, _callevent, _callparm)


# Сменить координатные оси между собой
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# Не может быть выполнено для карты, ограниченной рамкой
# При ошибке возвращает ноль

    mapChangeXY_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapChangeXY', maptype.HMAP, maptype.HSITE)
    def mapChangeXY(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapChangeXY_t (_hmap, _hsite)


# Запросить число слоев на карте
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapGetSiteLayerCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteLayerCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLayerCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapGetSiteLayerCount_t (_hmap, _hsite)


# Запросить название слоя по его номеру
# hmap      - идентификатор открытых данных (документа)
# hsite     - идентификатор векторной карты в открытых данных
# layer     - номер слоя
# layername - адрес буфера для записи названия слоя
# namesize  - размер буфера для возвращаемой строки в байтах
# Номер первого слоя 0
# При ошибке возвращает ноль

    mapGetSiteLayerNameUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapGetSiteLayerNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteLayerNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _layername: mapsyst.WTEXT, _namesize: int) -> int:
        return mapGetSiteLayerNameUn_t (_hmap, _hsite, _layer, _layername.buffer(), _namesize)


# Запросить число объектов описанных в классификаторе
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# При ошибке возвращает ноль

    mapSiteRscObjectCount_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectCount', maptype.HMAP, maptype.HSITE)
    def mapSiteRscObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapSiteRscObjectCount_t (_hmap, _hsite)


# Запросить число объектов описанных в классификаторе в заданном слое
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# layer - номер слоя
# При ошибке возвращает ноль

    mapSiteRscObjectCountInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectCountInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSiteRscObjectCountInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int) -> int:
        return mapSiteRscObjectCountInLayer_t (_hmap, _hsite, _layer)


# Запросить название объекта по порядковому номеру в заданном слое
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# layer  - номер слоя
# number - номер объекта в слое
# objectname - адрес буфера для записи названия объекта
# namesize  - размер буфера для возвращаемой строки в байтах
# При ошибке возвращает ноль

    mapSiteRscObjectNameInLayerUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectNameInLayerUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSiteRscObjectNameInLayerUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int, _objectname: mapsyst.WTEXT, _namesize: int) -> int:
        return mapSiteRscObjectNameInLayerUn_t (_hmap, _hsite, _layer, _number, _objectname.buffer(), _namesize)


# Запросить классификационный код объекта по порядковому номеру в заданном слое
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapSiteRscObjectExcodeInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectExcodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectExcodeInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectExcodeInLayer_t (_hmap, _hsite, _layer, _number)


# Запросить код локализации объекта по порядковому номеру в заданном слое
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль (ноль допустим)

    mapSiteRscObjectLocalInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectLocalInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectLocalInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectLocalInLayer_t (_hmap, _hsite, _layer, _number)


# Запросить внутренний код (индекс) объекта по порядковому номеру в заданном слое
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# layer  - номер слоя
# number - номер объекта в слое
# При ошибке возвращает ноль

    mapSiteRscObjectCodeInLayer_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectCodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectCodeInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        return mapSiteRscObjectCodeInLayer_t (_hmap, _hsite, _layer, _number)


# Запросить внутренний код (индекс) объекта по внешнему коду и локализации
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# excode - внешний код объекта
# local  - локализация объекта
# При ошибке возвращает ноль

    mapSiteRscObjectCode_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSiteRscObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _local: int) -> int:
        return mapSiteRscObjectCode_t (_hmap, _hsite, _excode, _local)


# Удалить объект карты по его последовательному номеру
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# number - последовательный номер объекта
# Для отмены удаления применяются mapUndeleteObjectByNumber и mapUndeleteObject
# При ошибке возвращает ноль

    mapDeleteSiteObjectByNumber_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapDeleteSiteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapDeleteSiteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        return mapDeleteSiteObjectByNumber_t (_hmap, _hsite, _number)


# Восстановить копию объекта по дате и времени выполнения транзакции
# hmap  - идентификатор открытых данных (документа)
# hsite - идентификатор векторной карты в открытых данных
# hobj  - идентификатор существующего объекта, созданного функцией CreateObject или
#         CreateSiteObject и прочитанного функцией mapReadObjectByNumber
#         или mapReadObjectByKey, в котором будет размещен результат восстановления
# date  - дата в формате "YYYYMMDD"
# time  - время в формате "число секунд от 00:00:00"
#         (по Гринвичу - GetSystemTime, in Coordinated Universal Time (UTC))
# При ошибке возвращает ноль

    mapRestoreBackObject_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapRestoreBackObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRestoreBackObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _date: int, _time: int) -> int:
        return mapRestoreBackObject_t (_hmap, _hsite, _hobj, _date, _time)


# Создать контекст (описание условий) поиска или отображения объектов карты
# hmap   - идентификатор открытых данных (документа)
# hsite  - идентификатор векторной карты в открытых данных
# В состав условий отбора объектов входят : слой,
# локализация, диапазон номеров объектов, характеристики
# (семантика) объекта, область расположения (метрика) объекта
# В созданном контексте доступны все объекты карты без исключений
# Запрашивается минимум 10 Кб памяти,
# если заданы условия поиска по метрике и семантике - до 300 Кб
# Каждый созданный контекст должен быть удален функцией mapDeleteSelectContext, когда
# он больше не используется
# При ошибке возвращает ноль

    mapCreateSiteSelectContext_t = mapsyst.GetProcAddress(curLib,maptype.HSELECT,'mapCreateSiteSelectContext', maptype.HMAP, maptype.HSITE)
    def mapCreateSiteSelectContext(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HSELECT:
        return mapCreateSiteSelectContext_t (_hmap, _hsite)


# Связать контекст условий поиска с другой картой
# hmap    - идентификатор открытых данных (документа)
# hsite   - идентификатор векторной карты в открытых данных
# hselect - идентификатор контекста поиска/отображения
# Все условия поиска автоматически сбрасываются
# При ошибке возвращает ноль

    mapSetSelectContextSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapSetSelectContextSite', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSetSelectContextSite(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        return mapSetSelectContextSite_t (_hselect, _hmap, _hsite)


# Добавить зарамочное оформление в пользовательскую карту
# hmap    - идентификатор основной векторной карты
# hsite   - идентификатор пользовательской карты
# frmname - полное имя файла шаблона зарамочного оформления (#.frm)
# frame   - габариты внутреннего контура зарамочного оформления в метрах
# При ошибке возвращает ноль

    mapAddMarginalRepresentationSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAddMarginalRepresentationSite', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.POINTER(maptype.DFRAME))
    def mapAddMarginalRepresentationSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: ctypes.c_char_p, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return mapAddMarginalRepresentationSite_t (_hmap, _hsite, _frmname, _frame)


# Добавить зарамочное оформление в пользовательскую карту
# hmap    - идентификатор основной векторной карты
# hsite   - идентификатор пользовательской карты
# frmname - полное имя файла шаблона зарамочного оформления (#.frm)
# frame   - габариты внутреннего контура зарамочного оформления в метрах
# angle   - угол поворота (если есть)
# center  - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapAddMarginalRepresentationSiteUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapAddMarginalRepresentationSiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapAddMarginalRepresentationSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapAddMarginalRepresentationSiteUn_t (_hmap, _hsite, _frmname.buffer(), _frame, _angle, _center)


# Нанести линию заданного кода на пользовательскую карту
# hmap        - идентификатор открытой векторной карты
# hsite       - идентификатор пользовательской карты
# excode      - код линии
# x1,y1,x2,y2 - координаты первой и второй точек в метрах
# angle       - угол поворота (если есть)
# center      - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateLineSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateLineSite', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateLineSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _x1: float, _y1: float, _x2: float, _y2: float, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateLineSite_t (_hmap, _hsite, _excode, _x1, _y1, _x2, _y2, _angle, _center)


# Создать рамку для зарамочного оформления на пользовательской карте
# hmap      - идентификатор открытой векторной карты
# hsite     - идентификатор пользовательской карты
# framecode - код внутренней рамки
# fillcode  - код заполнения
# linecode  - код внешней рамки
# delta     - расстояние от внутренней до внешней рамки в метрах
# frame     - габариты внутренней рамки в м
# angle     - угол поворота (если есть)
# center    - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateFrameFillSite_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateFrameFillSite', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateFrameFillSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _framecode: int, _fillcode: int, _linecode: int, _delta: float, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateFrameFillSite_t (_hmap, _hsite, _framecode, _fillcode, _linecode, _delta, _frame, _angle, _center)


# Нанести текст заданного кода на пользовательскую карту
# hmap        - идентификатор открытой векторной карты
# hsite       - идентификатор пользовательской карты
# excode      - код текста подписи
# text        - текст подписи
# x1,x2,y1,y2 - координаты первой и второй точек в метрах
# wide        - выравнивание по горизонтали:
#               UNIA_LEFT  - по левому краю,
#               UNIA_CENTER - по центру,
#               UNIA_RIGHT - по правому краю
# vert        - наличие выравнивания по вертикали (0 или 1)
# angle       - угол поворота (если есть)
# center      - центр поворота (если есть угол)
# При ошибке возвращает ноль

    mapCreateTitleSiteUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateTitleSiteUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateTitleSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _text: mapsyst.WTEXT, _x1: float, _y1: float, _x2: float, _y2: float, _wide: int, _vert: int, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return mapCreateTitleSiteUn_t (_hmap, _hsite, _excode, _text.buffer(), _x1, _y1, _x2, _y2, _wide, _vert, _angle, _center)


# Замена буквы 'я' на спецсимвол перед тем как разобрать строку функцией sscanf
# string - строка
# length - длина строки
# simbol - спецсимвол (если == 0 - то заменяет 'я' на '^')
# При ошибке возвращает ноль

    mapPreSscanfUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPreSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPreSscanfUn(_string: mapsyst.WTEXT, _length: int, _simbol: int) -> int:
        return mapPreSscanfUn_t (_string.buffer(), _length, _simbol)


# Замена спецсимвола на 'я' после разбора строки функцией sscanf
# string - строка
# length - длина строки
# simbol - спецсимвол (если == 0 - то заменяет '^' на 'я')
# При ошибке возвращает ноль

    mapPostSscanfUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapPostSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPostSscanfUn(_string: mapsyst.WTEXT, _length: int, _simbol: int) -> int:
        return mapPostSscanfUn_t (_string.buffer(), _length, _simbol)


# Функция создания легенды карты
# hmap      - идентификатор открытых данных (документа)
# hsite     - идентификатор векторной карты в открытых данных
# outname   - полное имя файла выходной карты-легенды
# desc      - параметры легенды (фон, подпись, контур; описана в mapgdi.h)
# hselect   - контекст отбора слоев\объектов карты для формирования легенды (необязательный параметр, может быть равен нулю)
# error     - код ошибки при построении легенды (необязательный параметр, может быть равен нулю, коды в maperr.rh)
# При ошибке возвращает ноль

    mapCreateLegend_t = mapsyst.GetProcAddress(curLib,ctypes.c_long,'mapCreateLegend', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(mapgdi.LEGENDESC), maptype.HSELECT, ctypes.POINTER(ctypes.c_int))
    def mapCreateLegend(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _desc: ctypes.POINTER(mapgdi.LEGENDESC), _hselect: maptype.HSELECT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        return mapCreateLegend_t (_hmap, _hsite, _outname.buffer(), _desc, _hselect, _error)

except Exception as e:
    print(e)
    curLib = 0

def sitapi_healthcheck(): 
    return 1