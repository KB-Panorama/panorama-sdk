#!/usr/bin/env python3

import os
import ctypes
import maptype
import mapsyst

try:
    if os.environ['gisvectrdll']:
        gisvectrname = os.environ['gisvectrdll']
except KeyError:
    gisvectrname = 'gis64vectr.dll'


try:
    vectrlib = mapsyst.LoadLibrary(gisvectrname)

# Вызвать диалог сортировки векторных карт
# hmap - идентификатор открытых данных
# parm - параметры задачи, описание структуры TASKPARM в maptype.h
#        (поле Handle должно содержать идентификатор главного окна)
# Вызов файла справки из Mapvectr.chm ("MAPSORTS")
# При ошибке возвращает ноль

#   MapSort_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'MapSort', maptype.HMAP, ctypes.POINTER(TASKPARM))
#   def MapSort(_hmap: maptype.HMAP, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return MapSort_t (_hmap, _parm)


# Выполнить преобразование системы координат (трансформирование) векторной карты
# hmap - идентификатор открытых данных
# parm - параметры задачи, описание структуры TASKPARMEX в maptype.h
#        (поле Handle должно содержать идентификатор главного окна)
# При успешном выполнении посылается сообщение AW_OPENDOCUN окну,
# заданному в поле TASKPARMEX::Handle.
# При ошибке возвращает ноль

    Modify_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'Modify', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def Modify(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return Modify_t (_hmap, _parm)


# Вызвать диалог импорта векторных карт из формата SXF или TXF
# lpszsource - адрес строки с именем импортируемого файла
# lpsztarget - адрес строки для размещения имени создаваемой карты, строка может иметь начальное значение
# size       - длина строки в байтах
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h
#              (поле Handle должно содержать идентификатор главного окна)
# Вызов справки из раздела "IMPORTSXF"
# При ошибке возвращает ноль

#   LoadSxf2MapUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadSxf2MapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(TASKPARM))
#   def LoadSxf2MapUn(_lsource: mapsyst.WTEXT, _ltarget: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return LoadSxf2MapUn_t (_lsource.buffer(), _ltarget.buffer(), _size, _parm)


# Вызвать диалог импорта векторных карт из формата DIR (списка SXF или TXF)
# lpszsource - адрес строки с именем импортируемого файла DIR
# lpsztarget - адрес строки для размещения имени создаваемой карты, строка может иметь начальное значение
# size       - длина строки в байтах
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h
#              (поле Handle должно содержать идентификатор главного окна)
# Вызов справки из раздела "IMPORTSXF"
# При ошибке возвращает ноль

#   vctLoadDir2MapUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'vctLoadDir2MapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(TASKPARM))
#   def vctLoadDir2MapUn(_lpszsource: mapsyst.WTEXT, _lpsztarget: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return vctLoadDir2MapUn_t (_lpszsource.buffer(), _lpsztarget.buffer(), _size, _parm)


# Вызвать диалог обновления векторных карт из формата SXF, TXF или DIR (списка SXF или TXF)
# lpszsource - адрес строки с именем импортируемого файла, используемого
#              для обновления векторной карты
# size - длина строки lpszsource для записи имени файла SXF, если в диалоге выбрано другое имя SXF
# hmap - идентификатор открытых данных
# parm - параметры задачи, описание структуры TASKPARM в maptype.h
#        (поле Handle должно содержать идентификатор главного окна).
# Вызов справки из раздела "UPDATESXF"
# При ошибке возвращает ноль

#   UpdateMapFromSxfUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'UpdateMapFromSxfUn', maptype.PWCHAR, ctypes.c_int, maptype.HMAP, ctypes.POINTER(TASKPARM))
#   def UpdateMapFromSxfUn(_lpszsource: mapsyst.WTEXT, _size: int, _hmap: maptype.HMAP, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return UpdateMapFromSxfUn_t (_lpszsource.buffer(), _size, _hmap, _parm)


# Сохранить векторную карту (экспорт) в формат SXF
# hmap       - идентификатор открытых данных
# lpsztarget - имя выходного файла
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h
#              (поле Handle должно содержать идентификатор главного окна)
# Вызов справки из раздела "EXPORTSXF"
# При ошибке возвращает ноль

#   SaveMap2SxfUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'SaveMap2SxfUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def SaveMap2SxfUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return SaveMap2SxfUn_t (_hmap, _lpsztarget.buffer(), _parm)


# Сохранить векторную карту (экспорт) в формат TXF (текстовый SXF)
# hmap       - идентификатор открытых данных
# lpsztarget - имя выходного файла
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h
#              (поле Handle должно содержать идентификатор главного окна).
# Вызов справки из раздела "EXPORTSXF"
# При ошибке возвращает ноль

#   SaveMap2TxtUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'SaveMap2TxtUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def SaveMap2TxtUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return SaveMap2TxtUn_t (_hmap, _lpsztarget.buffer(), _parm)


# Сохранить одну или все векторные карты (экспорт) в формат DIR (список SXF или TXF)
# hmap       - идентификатор открытых данных
# lpsztarget - имя файла сохраняемой карты
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h
#              (поле Handle должно содержать идентификатор главного окна)
# Вызов справки из раздела "EXPORTSXF"
# При ошибке возвращает ноль

#   SaveMap2DirUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'SaveMap2DirUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(TASKPARM))
#   def SaveMap2DirUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return SaveMap2DirUn_t (_hmap, _lpsztarget.buffer(), _parm)


# Импорт данных Shape (исходные данные выбираются из диалогового окна открытия файла)
# hmap       - идентификатор открытых данных
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h.
# При ошибке возвращает ноль

    CallImportShp_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'CallImportShp', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def CallImportShp(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return CallImportShp_t (_hmap, _parm)


# Импорт набора данных Shape (исходные данные выбираются из диалогового окна выбора директории)
# hmap       - идентификатор открытых данных
# parm       - параметры задачи, описание структуры TASKPARM в maptype.h.
# При ошибке возвращает ноль

    ImportShpSet_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'ImportShpSet', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def ImportShpSet(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        return ImportShpSet_t (_hmap, _parm)


# Импорт из ShapeFile набора данных с дополнительным параметром "onlyconfig"
# handle  - окно визуального сопровождения процесса обработки
# mapname - имя файла (полный путь) создаваемой карты
#           Если имя не указано - сформируется по имени первого SHP в списке
#           Если карта с указанным (или сформированным) именем не существует
#               - будет создана
#           Если карта уже существует и clear = 1 - выполняется перезапись
#           (предварительное удаление старых объектов)
# clear   - 0/1 предварительно чистить существующую карту?
# rscname - имя файла (полный путь) классификатора (может = 0, если карта
#           уже существует), обязан быть, если карты еще нет
# shiname - имя файла настроек(полный путь) 0 - для набора данных,
#           сформированных средствами "Панорама"
# scale   - знаменатель масштаба создаваемой карты (может = 0, если карта
#           уже существует)
# shppath - путь к папке с набором данных
# charset - таблица кодировки таблицы DBF (0 - ANSI,1 - UTF-8, 2-OEM,
#                                   -1 - неизвестно, опр. автоматически)
# sort    - выполнить итоговую сортировку карты (0,1)
# clear   - выполнить предварительную очистку карты (0,1)
# onlyconfig - загружать только настроенные слои (0,1)
#
# Возврат:  1 - нормальное завершение, 0 - загрузка не выполнена, -1 - выполнено с ошибками
# Ошибки, выявленные после создания (или открытия карты) пишутся в LOG карты

    ShpLoadFolderEx_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'ShpLoadFolderEx', maptype.HMESSAGE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def ShpLoadFolderEx(_handle: maptype.HMESSAGE, _mapname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _shiname: ctypes.c_char_p, _scale: int, _shppath: ctypes.c_char_p, _charset: int, _sort: int, _clear: int, _onlyconfig: int) -> int:
        return ShpLoadFolderEx_t (_handle, _mapname, _rscname, _shiname, _scale, _shppath, _charset, _sort, _clear, _onlyconfig)

    ShpLoadFolder_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'ShpLoadFolder', maptype.HMESSAGE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def ShpLoadFolder(_handle: maptype.HMESSAGE, _mapname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _shiname: ctypes.c_char_p, _scale: int, _shppath: ctypes.c_char_p, _charset: int, _sort: int, _clear: int = 0) -> int:
        return ShpLoadFolder_t (_handle, _mapname, _rscname, _shiname, _scale, _shppath, _charset, _sort, _clear)

    ShpLoadFolderUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'ShpLoadFolderUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def ShpLoadFolderUn(_handle: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _shiname: mapsyst.WTEXT, _scale: int, _shppath: mapsyst.WTEXT, _charset: int, _sort: int, _clear: int, _onlyconfig: int) -> int:
        return ShpLoadFolderUn_t (_handle, _mapname.buffer(), _rscname.buffer(), _shiname.buffer(), _scale, _shppath.buffer(), _charset, _sort, _clear, _onlyconfig)


# Импорт из OSM ShapeFile набора данных на восточное полушарие
# handle  - окно визуального сопровождения процесса обработки
# mapname - имя файла (полный путь) создаваемой карты
#           Если имя не указано - сформируется по имени первого SHP в списке
#           Если карта с указанным (или сформированным) именем не существует
#               - будет создана
#           Если карта уже существует и clear = 1 - выполняется перезапись
#           (предварительное удаление старых объектов)
# rscname - имя файла (полный путь) классификатора (может = 0, если карта
#           уже существует), обязан быть, если карты еще нет
# shiname - имя файла настроек(полный путь) 0 - для набора данных,
#           сформированных средствами "Панорама"
# scale   - знаменатель масштаба создаваемой карты (может = 0, если карта
#           уже существует)
# shppath - путь к папке с набором данных
# charset - таблица кодировки таблицы DBF (0 - ANSI,1 - UTF-8, 2-OEM,
#                                   -1 - неизвестно, опр. автоматически)
# sort    - выполнить итоговую сортировку карты (0,1)
# Возврат:  1 - нормальное завершение, 0 - загрузка не выполнена, -1 - выполнено с ошибками
# Ошибки, выявленные после создания (или открытия карты) пишутся в LOG карты

    OSMShpLoadFolderEx_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_int,'OSMShpLoadFolderEx', maptype.HMESSAGE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def OSMShpLoadFolderEx(_handle: maptype.HMESSAGE, _mapname: ctypes.c_char_p, _rscname: ctypes.c_char_p, _shiname: ctypes.c_char_p, _scale: int, _shppath: ctypes.c_char_p, _charset: int, _sort: int, _source: int) -> int:
        return OSMShpLoadFolderEx_t (_handle, _mapname, _rscname, _shiname, _scale, _shppath, _charset, _sort, _source)


#========================================================================
#   Функции импорта и экспорта формата S57
#========================================================================
# Для работы программы требуется классификатор s57navy.rsc
# Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
# Импорт морской карты из формата S57 в формат MAP
# s57name - полное имя файла формата S57
# mapname - полное имя создаваемой карты
# mapnamesize - размер буфера с именем создаваемой карты в байтах
# parm    - параметры задачи, описание структуры TASKPARM в maptype.h.
# При ошибке в параметрах возвращает ноль

#   LoadS57ToMapUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadS57ToMapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(TASKPARM))
#   def LoadS57ToMapUn(_s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _mapnamesize: int, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return LoadS57ToMapUn_t (_s57name.buffer(), _mapname.buffer(), _mapnamesize, _parm)


# Импорт морской карты из формата S57 в формат MAP
# s57name - полное имя (путь) файла формата S57
# mapname - полное имя файла создаваемой карты
# mapnamesize - размер буфера с именем создаваемой карты в байтах
# rscname - полное имя файла классификатора (путь к файлу s57navy.rsc)
# rscnamesize - размер буфера с именем файла RSC в байтах
# parm    - параметры задачи, описание структуры TASKPARM в maptype.h.
# При ошибке в параметрах возвращает ноль

#   LoadS57ToMapForRscUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadS57ToMapForRscUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(TASKPARM))
#   def LoadS57ToMapForRscUn(_s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _mapnamesize: int, _rscname: mapsyst.WTEXT, _rscnamesize: int, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return LoadS57ToMapForRscUn_t (_s57name.buffer(), _mapname.buffer(), _mapnamesize, _rscname.buffer(), _rscnamesize, _parm)


# Экспорт морской карты из формата MAP/SIT в формат S57
# hmap - идентификатор открытых данных
# parm    - параметры задачи, описание структуры TASKPARM в maptype.h.
# При ошибке в параметрах возвращает ноль

#   SaveMap2S57_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'SaveMap2S57', maptype.HMAP, ctypes.POINTER(TASKPARM))
#   def SaveMap2S57(_hmap: maptype.HMAP, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return SaveMap2S57_t (_hmap, _parm)


#========================================================================
#   Функции импорта из формата MIF\MID
#========================================================================
# Функция для вызова диалога импорта данных из формата MIF/MID
# mifname - имя загружаемого файла формата MIF
# mapname - имя создаваемой карты
# size    - длина буфера для размещения имени файла выходной карты
# parm    - параметры задачи
# При ошибке возвращает ноль

#   LoadMifToMapUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadMifToMapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(TASKPARM))
#   def LoadMifToMapUn(_mifname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(TASKPARM)) -> int:
#       return LoadMifToMapUn_t (_mifname.buffer(), _mapname.buffer(), _size, _parm)

except Exception as e:
    print(e)
    vectrlib = 0