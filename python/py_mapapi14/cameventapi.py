#!/usr/bin/env python3

#********************************************************************
#*                                                                  *
#*              Copyright (c) PANORAMA Group 1991-2022              *
#*                      All Rights Reserved                         *
#*                                                                  *
#********************************************************************
#*                                                                  *
#*              API-функции для работы с информацией                *
#*                 о событиях, принятых от камеры                   *
#*                                                                  *
#********************************************************************

import os
import mapsyst
import maptype
import ctypes
import camtype

HCAMEVENT = ctypes.c_void_p        

try:
    if os.environ['gisvideodll']:
        gisvideoname = os.environ['gisvideodll']
except KeyError:
    gisvideoname = 'mapvideo64.dll'

try:
    videolib = mapsyst.LoadLibrary(gisvideoname)

# Создать объект для передачи информации о возникшем событии во внешний скрипт
# hCam - идентификатор объекта для управления IP-камерой
# hObj - идентификатор объекта карты, к которому привязана IP-камера
# message - адрес структуры с описанием события
# В случае успеха возвращает идентификатор созданного объекта
# При ошибке возвращает 0

    camCreateEventDescriptor_t = mapsyst.GetProcAddress(videolib,HCAMEVENT,'camCreateEventDescriptor', camtype.HCAM, maptype.HOBJ, ctypes.POINTER(camtype.CAMERAEVENT))
    def camCreateEventDescriptor(_hCam: camtype.HCAM, _hObj: maptype.HOBJ, _message: ctypes.POINTER(camtype.CAMERAEVENT)) -> HCAMEVENT:
       return camCreateEventDescriptor_t (_hCam, _hObj, _message)


# Удалить объект для передачи информации о возникшем событии
# hEvent - идентификатор объекта с описанием события

    camDeleteEventDescriptor_t = mapsyst.GetProcAddress(videolib,ctypes.c_void_p,'camDeleteEventDescriptor', HCAMEVENT)
    def camDeleteEventDescriptor(_hEvent: HCAMEVENT) -> ctypes.c_void_p:
       return camDeleteEventDescriptor_t (_hEvent)


# Запросить скриншот с камеры
# hEvent - идентификатор объекта с описанием события
# buffer - указатель на буфер WCHAR для записи
# numbytes - размер буфера в байтах
# При повторном вызове обновляет изображение в файле
# При ошибке возвращает 0

    camGetSnapshotByEvent_t = mapsyst.GetProcAddress(videolib, ctypes.c_int,'camGetSnapshotByEvent', HCAMEVENT, maptype.PWCHAR, ctypes.c_int)
    def camGetSnapshotByEvent(_hEvent: HCAMEVENT, _buffer: mapsyst.WTEXT, _numbytes: int) -> int:
        return camGetSnapshotByEvent_t (_hEvent,_buffer.buffer(),_numbytes)


# Запросить текстовое описание события в формате:
# "ЧЧ:ММ:СС ДД/ММ/ГГГГ, Тема уведомления, Данные"
# hEvent      - идентификатор объекта с описанием события
# message     - адрес строки для возврата описания события
# messageSize - размер выделенного для строки буфера (в байтах)
# В случае успеха возвращает текстовое описание события.
# Время возникновения события указывается во временной зоне камеры
# При ошибке возвращает 0

    camGetEventMessageUn_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetEventMessageUn', HCAMEVENT, maptype.PWCHAR, ctypes.c_int)
    def camGetEventMessageUn(_hEvent: HCAMEVENT, _message: mapsyst.WTEXT, _messageSize: int) -> int:
        return camGetEventMessageUn_t (_hEvent, _message.buffer(), _messageSize)


# Запросить текстовую строку с параметрами запуска скрипта
# (например, email для отправки сообщения или полный путь к файлу БД)
# hEvent - идентификатор объекта с описанием события
# strparam     - адрес строки для возврата параметров
# strparamSize - размер выделенного для строки буфера (в байтах)
# В случае успеха возвращает строку с параметром (параметрами)
# При ошибке возвращает 0

    # camGetParamTextByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetParamTextByEvent', HCAMEVENT, maptype.PWCHAR, ctypes.c_int)
    # def camGetParamTextByEvent(_hEvent: HCAMEVENT, _strparam: mapsyst.WTEXT, _strparamSize: int) -> int:
        # return camGetParamTextByEvent_t (_hEvent, _strparam.buffer(), _strparamSize)


# Заполнить структуру с описанием события
# hEvent  - идентификатор объекта с описанием события
# message - адрес структуры для записи информации о событии
# При ошибке возвращает 0

    camGetEventStucture_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetEventStucture', HCAMEVENT, ctypes.POINTER(camtype.CAMERAEVENT))
    def camGetEventStucture(_hEvent: HCAMEVENT, _message: ctypes.POINTER(camtype.CAMERAEVENT)) -> int:
        return camGetEventStucture_t (_hEvent, _message)
 

# Запросить идентификатор камеры, от которой было принято событие
# hEvent  - идентификатор объекта с описанием события
# В случае успеха возвращает идентификатор камеры, от которой было
# принято уведомление о событии
# При ошибке возвращает 0

    camGetCameraByEvent_t = mapsyst.GetProcAddress(videolib,camtype.HCAM,'camGetCameraByEvent', HCAMEVENT)
    def camGetCameraByEvent(_hEvent: HCAMEVENT) -> camtype.HCAM:
        return camGetCameraByEvent_t (_hEvent)


# Запросить название камеры, от которой было принято событие
# hEvent   - идентификатор объекта с описанием события
# name     - адрес строки для записи названия камеры
# nameSize - размер выделенного буфера (в байтах)
# При ошибке возвращает 0

    camGetCameraNameByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetCameraNameByEvent', HCAMEVENT, maptype.PWCHAR, ctypes.c_int)
    def camGetCameraNameByEvent(_hEvent: HCAMEVENT, _name: mapsyst.WTEXT, _nameSize: int) -> int:
        return camGetCameraNameByEvent_t (_hEvent, _name.buffer(), _nameSize)


# Запросить сетевой адрес камеры, от которой было принято событие
# hEvent   - идентификатор объекта с описанием события
# addr     - адрес строки для записи сетевого адреса
# addrSize - размер выделенного буфера (в байтах)
# При ошибке возвращает 0

    camGetCameraAddrByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetCameraAddrByEvent', HCAMEVENT, maptype.PWCHAR, ctypes.c_int)
    def camGetCameraAddrByEvent(_hEvent: HCAMEVENT, _addr: mapsyst.WTEXT, _addrSize: int) -> int:
        return camGetCameraAddrByEvent_t (_hEvent, _addr.buffer(), _addrSize)


# Запросить идентификатор объекта-камеры на карте
# hEvent  - идентификатор объекта с описанием события
# В случае успеха возвращает идентификатор объекта-камеры, от которого было
# принято уведомление о событие
# При ошибке возвращает 0

    camGetObjectByEvent_t = mapsyst.GetProcAddress(videolib,maptype.HOBJ,'camGetObjectByEvent', HCAMEVENT)
    def camGetObjectByEvent(_hEvent: HCAMEVENT) -> maptype.HOBJ:
        return camGetObjectByEvent_t (_hEvent)


# Запросить номер активного медиапрофиля камеры
# hEvent  - идентификатор объекта с описанием события
# В случае успеха возвращает номер медиапрофиля (начиная с 0), который был
# активным во время возникновения события
# При ошибке возвращает -1

    camGetProfileNumByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_int,'camGetProfileNumByEvent', HCAMEVENT)
    def camGetProfileNumByEvent(_hEvent: HCAMEVENT) -> int:
        return camGetProfileNumByEvent_t (_hEvent)

except Exception as e:
    print(e)
    videolib = 0