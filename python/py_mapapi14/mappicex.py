#!/usr/bin/env python3

import os
import ctypes
import mapsyst
import maptype
import mapcreat

PACK_WIDTH = 1

#-----------------------------
class SAVEASPICTRPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("BitCount",ctypes.c_int),
                ("Scale",ctypes.c_double),
                ("ResolutionInch",ctypes.c_double),
                ("ResolutionMet",ctypes.c_double),
                ("MeterInElement",ctypes.c_double),
                ("Handle",maptype.HWND),
                ("PlaneFrame",maptype.DFRAME),
                ("Intensity",ctypes.c_int),
                ("ResolvColor",ctypes.c_int),
                ("IntergraphTIFF",ctypes.c_int),
                ("CompressTIFF",ctypes.c_int),
                ("CompressJPGValue",ctypes.c_int),
                ("OutputFileFormat",ctypes.c_int),
                ("Regime",ctypes.c_char),
                ("TypeView",ctypes.c_char),
                ("Black",ctypes.c_char),
                ("Border",ctypes.c_char),
                ("FileOfParam",ctypes.c_char),
                ("FormatCorel9",ctypes.c_char),
                ("ColorModel",ctypes.c_char),
                ("PolyMark",ctypes.c_char),
                ("Rezerv",ctypes.c_char*64),
                ("FileName",maptype.WCHAR1*(maptype.MAX_PATH_LONG*2))]
#-----------------------------


#TODO: LOCATIONPOINT struct
#-----------------------------
#class RASTERPARM(ctypes.Structure):
#    _pack_ = PACK_WIDTH
#    _fields_ = [("MapRegister",mapcreat.MAPREGISTEREX),
#                ("Ellipsoid",mapcreat.ELLIPSOIDPARAM),
#                ("Datum",mapcreat.DATUMPARAM),
#                ("FlagMapRegister",ctypes.c_int),
#                ("FlagLocation",ctypes.c_int),
#                ("LocationPoint",maptype.DOUBLEPOINT),
#                ("MeterInElementX",ctypes.c_double),
#                ("MeterInElementY",ctypes.c_double),
#                ("FlagMeterInElement",ctypes.c_int),
#                ("FlagRasterPoint",ctypes.c_int),
#                ("RasterPoint",maptype.DOUBLEPOINT*4),
#                ("RasterPointTr",LOCATIONPOINT*4),
#                ("FlagTransformation",ctypes.c_int),
#                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SAVEASPICTRPARMUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("Resolution",ctypes.c_int),
                ("BitCount",ctypes.c_int),
                ("Handle",maptype.HWND),
                ("PlaneFrame",maptype.DFRAME),
                ("Intensity",ctypes.c_char),
                ("ResolvColor",ctypes.c_char),
                ("IntergraphTIFF",ctypes.c_char),
                ("CompressTIFF",ctypes.c_char),
                ("OutputFileFormat",ctypes.c_int),
                ("Regime",ctypes.c_char),
                ("TypeView",ctypes.c_char),
                ("Black",ctypes.c_char),
                ("Border",ctypes.c_char),
                ("FileOfParam",ctypes.c_char),
                ("FormatCorel9",ctypes.c_char),
                ("ColorModel",ctypes.c_char),
                ("PolyMark",ctypes.c_char),
                ("FileName",maptype.WCHAR1*(maptype.MAX_PATH_LONG*2))]
#-----------------------------


#-----------------------------
class SAVEASPICTRPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_long),
                ("Reserve1",ctypes.c_long),
                ("Handle",maptype.HWND),
                ("Scale",ctypes.c_long),
                ("Resolution",ctypes.c_long),
                ("BitCount",ctypes.c_long),
                ("Reserve2",ctypes.c_long),
                ("Intensity",ctypes.c_char),
                ("ResolvColor",ctypes.c_char),
                ("IntergraphTIFF",ctypes.c_char),
                ("CompressTIFF",ctypes.c_char),
                ("Reserve3",ctypes.c_char*4),
                ("PlaneFrame",maptype.DFRAME),
                ("Regime",ctypes.c_char),
                ("TypeView",ctypes.c_char),
                ("Black",ctypes.c_char),
                ("Border",ctypes.c_char),
                ("FileOfParam",ctypes.c_char),
                ("FormatCorel9",ctypes.c_char),
                ("ColorModel",ctypes.c_char),
                ("PolyMark",ctypes.c_char),
                ("FileName",ctypes.c_char*260),
                ("Reserve4",ctypes.c_char*4)]
#-----------------------------


#-----------------------------
class SAVEASPICTRPARM_FOR_PRINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Reserve1",ctypes.c_int),
                ("Handle",maptype.HMESSAGE),
                ("HMap",maptype.HMAP),
                ("Regime",ctypes.c_int),
                ("Reserve2",ctypes.c_int),
                ("PlaneFrame",maptype.DFRAME),
                ("DPI",ctypes.c_double),
                ("LPI",ctypes.c_double),
                ("FactorVer",ctypes.c_double),
                ("FactorHor",ctypes.c_double),
                ("Rect",maptype.RECT),
                ("Scale",ctypes.c_int),
                ("BitCount",ctypes.c_int),
                ("Intensity",ctypes.c_int),
                ("ColorModel",ctypes.c_int),
                ("Method",ctypes.c_int),
                ("Shape",ctypes.c_int),
                ("AngleC",ctypes.c_double),
                ("AngleM",ctypes.c_double),
                ("AngleY",ctypes.c_double),
                ("AngleK",ctypes.c_double),
                ("Reserve",ctypes.c_char*96),
                ("Cross",ctypes.c_char),
                ("Negative",ctypes.c_char),
                ("Mirror",ctypes.c_char),
                ("Turn",ctypes.c_char),
                ("FileName",ctypes.c_char*260)]
#-----------------------------

#-----------------------------
class DATAINFORMATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [
        ("InputFileLength",ctypes.c_int),
        ("Width",ctypes.c_int),
        ("Height",ctypes.c_int),
        ("BitPerPixel",ctypes.c_int),
        ("Precision",ctypes.c_double),
        ("PaletteType",ctypes.c_char*4),
        ("BlockCount",ctypes.c_int),
        ("RswFileLength",ctypes.c_double),
        ("CompressImage",ctypes.c_char*16)
    ]
#-----------------------------

#-----------------------------
class GEOTIFFINFORMATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [
        ("StructSize",ctypes.c_int),
        ("TypeCS",ctypes.c_int),
        ("Spheroid",ctypes.c_int),
        ("Datum",ctypes.c_int),
        ("PrimeMeridian",ctypes.c_int),
        ("Projection",ctypes.c_int),
        ("Zone",ctypes.c_int),
        ("Units",ctypes.c_int),
        ("FrameImage",maptype.DFRAME),
        ("UnitsInElement_X",ctypes.c_double),
        ("UnitsInElement_Y",ctypes.c_double),
        ("UnitsInElement_Z",ctypes.c_double),
        ("Information",ctypes.c_char*256),
        ("PrecisionInch",ctypes.c_double),
        ("PrecisionMet",ctypes.c_double),
        ("UnitsAngular",ctypes.c_int),
        ("RswWidth",ctypes.c_int),
        ("RswHeight",ctypes.c_int),
        ("GeoTiffInformationZero",ctypes.c_int),
        ("Reserv",ctypes.c_char*236)
    ]
#-----------------------------

try:
    if os.environ['gispicexdll']:
        gispicexname = os.environ['gispicexdll']
except KeyError:
    gispicexname = 'gis64picex.dll'

try:
    picexlib = mapsyst.LoadLibrary(gispicexname)
except Exception as e:
    print(e)
    picexlib = 0  

if picexlib == 0:
    print(gispicexname)
else: 

#    Сохранить карту в формате TIFF
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    filename   - имя файла сохраняемого изображения RSW
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount   - количество бит на пиксель сохраняемого изображения
#    meterInElement - размер пикселя сохраняемого изображения в метрах
#    flagCompress   - При сохранении файла TIFF - Флаг сжатия изображения
#                     (0- не применять сжатие, 1 - сжатие PackBit)
#                     При сохранении файла JPG  - Коэффициент качества
#                     изображения при сжатии JPEG (0-100)
#    flagIntergraphTIFF - Флаг записи матрицы трансформирования для
#                     использования в программе Intergraph
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadDocumentImageToTiffFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToTiffFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def LoadDocumentImageToTiffFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitCount: int, _meterInElement: float, _flagCompress: int, _flagIntergraphTIFF: int) -> int:
        return LoadDocumentImageToTiffFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitCount, _meterInElement, _flagCompress, _flagIntergraphTIFF)

# Загрузка растровых данных из файла PCX в файл RSW
#    handle  - идентификатор диалога визуального сопровождения процесса обработки.
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг сжатия изображения
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    picexLoadPcxToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadPcxToRstAndCompressUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def picexLoadPcxToRstAndCompressUn(_handle: maptype.HMESSAGE, _pcxname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        return picexLoadPcxToRstAndCompressUn_t (_handle, _pcxname.buffer(), _rstname.buffer(), _meterInElementX, _meterInElementY, _point, _compression)


# Загрузка растровых данных из файла PCX в файл RSW
#    handle  - идентификатор диалога визуального сопровождения процесса обработки.
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг сжатия изображения
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 1 - 100
#              Рекомендуемое значение: 60
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    picexLoadPcxToRstAndCompressJPEG_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadPcxToRstAndCompressJPEG_Un', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def picexLoadPcxToRstAndCompressJPEG_Un(_handle: maptype.HMESSAGE, _pcxname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int) -> int:
        return picexLoadPcxToRstAndCompressJPEG_Un_t (_handle, _pcxname.buffer(), _rstname.buffer(), _meterInElementX, _meterInElementY, _point, _compression, _compressJpegQuality)


# Загрузка растровых данных из файла BMP в файл RSW
#    BmpName - имя BMP-файла;
#    RstName - имя RSW-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    handle - HWND диалога визуального сопровождения процесса обработки.
#    compression - флаг сжатия изображения
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    picexLoadBmpToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadBmpToRstAndCompressUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def picexLoadBmpToRstAndCompressUn(_handle: maptype.HMESSAGE, _BmpName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        return picexLoadBmpToRstAndCompressUn_t (_handle, _BmpName.buffer(), _RstName.buffer(), _meterInElementX, _meterInElementY, _point, _compression)


# Загрузка растровых данных из файла BMP в файл RSW
#    handle  - диалог визуального сопровождения процесса обработки.
#    BmpName - имя BMP-файла;
#    RstName - имя RSW-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг сжатия изображения
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 1 - 100
#              Рекомендуемое значение: 60
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    picexLoadBmpToRstAndCompressJPEG_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadBmpToRstAndCompressJPEG_Un', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def picexLoadBmpToRstAndCompressJPEG_Un(_handle: maptype.HMESSAGE, _BmpName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int) -> int:
        return picexLoadBmpToRstAndCompressJPEG_Un_t (_handle, _BmpName.buffer(), _RstName.buffer(), _meterInElementX, _meterInElementY, _point, _compression, _compressJpegQuality)


# Загрузка растровых данных из файла JPEG в файл RSW
#    hmap -  идентификатор открытых данных
#    inputname - имя JPEG-файла;
#    rstname   - имя RSW-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#              0 - сжатие к блокам изображения не применено
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 1 - 100
#              Рекомендуемое значение: 60
#    flagMessage - параметр не используется
#                  Управление диагностическими сообщениями осуществляется
#                  вызовом функции mapMessageEnable.
#                  Если mapIsMessageEnable() возвращает 0, то
#                  диагностические сообщения не выдаются.
#
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    picexLoadJpegToRswAndCompressJPEG_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadJpegToRswAndCompressJPEG_Un', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexLoadJpegToRswAndCompressJPEG_Un(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _flagMessage: int) -> int:
        return picexLoadJpegToRswAndCompressJPEG_Un_t (_hmap, _handle, _inputname.buffer(), _rstname.buffer(), _meterInElementX, _meterInElementY, _point, _compression, _compressJpegQuality, _flagMessage)


# Загрузка растровых данных из файла JPEG в файл RSW
#    hmap -  идентификатор открытых данных
#    handle - диалог визуального сопровождения процесса обработки.
#    inputname - имя JPEG-файла;
#    rstname   - имя RSW-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    flagMessage - параметр не используется
#                  Управление диагностическими сообщениями осуществляется
#                  вызовом функции mapMessageEnable.
#                  Если mapIsMessageEnable() возвращает 0, то
#                  диагностические сообщения не выдаются.
#
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    picexLoadJpegToRswAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadJpegToRswAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def picexLoadJpegToRswAndCompressUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagMessage: int) -> int:
        return picexLoadJpegToRswAndCompressUn_t (_hmap, _handle, _inputname.buffer(), _rstname.buffer(), _meterInElementX, _meterInElementY, _point, _compression, _flagMessage)


# Загрузка растровой карты без копирования изображения в формат RSW
# В качестве исходных данных в функцию могут передаваться имена файлов форматов:
# (TIFF, GeoTIFF, IMG, JPEG, PNG, GIF, BMP)
# При успешном выполнении функции создается файл RSW с именем outputName.
# В файл RSW записываются параметры загружаемого растра, при этом изображение в
# RSW не переносится. Исходный и выходной (#.RSW) файлы должны находиться в одной папке.
# Обзорное изображение растра записывается в файл #.TOF, который создается в этой же папке.
# Для доступа к изображению графического файла созданный файл outputName необходимо
# открыть вызовом функции mapOpenRstUn, или добавить в документ карты вызовом
# функции mapOpenRstForMapUn.
# Входные параметры функции:
#    handle          - диалог визуального сопровождения процесса обработки.
#    enableMessage   - флаг выдачи сообщений
#                             (при ==1, сообщение выдает MessageBox;
#                              при == 0, посылается сообщение диалогу WM_ERROR)
#    sourceName      - имя исходного файла (#.TIF, #.IMG, #.JPG, #.PNG, #.GIF, #.BMP);
#    outputName      - имя выходного файла (#.RSW);
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point           - привязка растра
#
#    Если в качестве исходного файла подается файл GeoTIFF, или файл IMG с
#    геопривязанным изображением, то входные параметры meterInElementX,
#    meterInElementY и point могут быть равны 0.
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexGetAccessToGraphicFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetAccessToGraphicFileUn', maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT))
    def picexGetAccessToGraphicFileUn(_handle: maptype.HMESSAGE, _enableMessage: int, _sourceName: mapsyst.WTEXT, _outputName: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return picexGetAccessToGraphicFileUn_t (_handle, _enableMessage, _sourceName.buffer(), _outputName.buffer(), _meterInPixelX, _meterInPixelY, _point)


# Загрузка растровой карты из Tiff(GeoTiff) в RSW
# Изображение в RSW не переносится, в RSW записываются заголовки, палитра, УК.
#    hmap -  идентификатор открытых данных
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point       - привязка растра
#    mapreg      - параметры проекции
#    handle      - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    flagMessage - параметр не используется
#                  Управление диагностическими сообщениями осуществляется
#                  вызовом функции mapMessageEnable.
#                  Если mapIsMessageEnable() возвращает 0, то
#                  диагностические сообщения не выдаются.
#
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    picexLoadTiffAccessToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadTiffAccessToRswUn', maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT))
    def picexLoadTiffAccessToRswUn(_handle: maptype.HMESSAGE, _enableMessage: int, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return picexLoadTiffAccessToRswUn_t (_handle, _enableMessage, _TiffName.buffer(), _RstName.buffer(), _meterInPixelX, _meterInPixelY, _point)

    
    LoadTiffAccessToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadTiffAccessToRswUn', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.c_int, ctypes.c_int)
    def LoadTiffAccessToRswUn(_Map: maptype.HMAP, _Handle: maptype.HMESSAGE, _enableMessage: int, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _res: int, _rez1: int) -> int:
        return LoadTiffAccessToRswUn_t (_Map, _Handle, _enableMessage, _TiffName.buffer(), _RstName.buffer(), _scale, _precision, _point, _mapreg, _res, _rez1)


# Импорт снимков Landsat, Kompsat и GeoEye, поставляемых в виде набора
# одноканальных TIF растров.  Одноканальные TIF растры интерпретируются
# как разные каналы одного изображения.
# Изображение в RSW не переносится, в RSW записывается служебная информация.
# Для ускорения отображения растровых данных применяется произвольная схема
# создаваемых обзорных изображений: 1:4, 1:16, 1:64 и т.д. Если исходный снимок
# содержит обзорные изображения, то они используются напрямую при создании
# производных обзорных изображений. Возможно применение сжатия обзорных изображений.
#
#    handle          - диалог визуального сопровождения процесса обработки.
#    enableMessage   - флаг выдачи сообщений
#                                       (при ==1, сообщение выдает MessageBox;
#                                        при == 0, посылается сообщение диалогу WM_ERROR)
#    tiffFileNames   - список имен одноканальных TIF растров.
#                      Имена отделены друг от друга ";".
#    sizeTiffFiles   - размер в байтах области памяти, выделенной для
#                      списка имен одноканальных TIF растров (включая завершающий ноль).
#    tafparm         - Параметры создания обзорного изображения графического файла.
#                      Указатель на структуру TAFPARM.
#    rstName         - имя выходного файла растровой карты RSW;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point           - привязка растра
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexMultyChannelsTiffAccessToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMultyChannelsTiffAccessToRswUn', maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.TAFPARM), maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT))
    def picexMultyChannelsTiffAccessToRswUn(_handle: maptype.HMESSAGE, _enableMessage: int, _tiffFileNames: mapsyst.WTEXT, _sizeTiffFiles: int, _tafparm: ctypes.POINTER(maptype.TAFPARM), _rstName: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return picexMultyChannelsTiffAccessToRswUn_t (_handle, _enableMessage, _tiffFileNames.buffer(), _sizeTiffFiles, _tafparm, _rstName.buffer(), _meterInPixelX, _meterInPixelY, _point)


# Загрузка растровой карты из Tiff(GeoTiff) в RSW
#    Handle - диалог визуального сопровождения процесса обработки.
#    TiffName - имя Tiff-файла;
#    RstName - имя Rst-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    flagIgnoreGeoTiff - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#              0 - привязка и СК считываются из тега
#                  исходного файла и устанавливаются в выходной растр
#              1 - привязка устанавливается в выходной растр из
#                  аргумента point, СК не устанавливается
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    picexLoadTiffToRstAndCompressExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadTiffToRstAndCompressExUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def picexLoadTiffToRstAndCompressExUn(_handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagIgnoreGeoTiff: int) -> int:
        return picexLoadTiffToRstAndCompressExUn_t (_handle, _TiffName.buffer(), _RstName.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _flagIgnoreGeoTiff)


# Загрузка растровой карты из Tiff(GeoTiff) в RSW
#    handle - диалог визуального сопровождения процесса обработки.
#    TiffName - имя Tiff-файла;
#    RstName - имя Rst-файла;
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#              0 - сжатие к блокам изображения применяться не будет
#              1 - блоки д.б. сжаты по методу LZW
#              2 - блоки д.б. сжаты по методу JPEG (справедливо для 24 битных растров)
#    compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 1 - 100
#              Рекомендуемое значение: 60
#    flagIgnoreGeoTiff - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#              0 - привязка и СК считываются из тега
#                  исходного файла и устанавливаются в выходной растр
#              1 - привязка устанавливается в выходной растр из
#                  аргумента point, СК не устанавливается
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    picexLoadTiffToRstAndCompressJPEG_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadTiffToRstAndCompressJPEG_Un', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexLoadTiffToRstAndCompressJPEG_Un(_handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _flagIgnoreGeoTiff: int) -> int:
        return picexLoadTiffToRstAndCompressJPEG_Un_t (_handle, _TiffName.buffer(), _RstName.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _compressJpegQuality, _flagIgnoreGeoTiff)


# Загрузка растровой карты из KMZ в RSW
#    handle - диалог визуального сопровождения процесса обработки.
#    inputFileName  - имя KMZ-файла
#    outputFileName - имя проекта MPT
#    compression - флаг сжатия выходного файла
#              0 - сжатие к блокам изображения применяться не будет
#              1 - сжатие изображения по методу LZW
#              2 - сжатие изображения по методу JPEG (справедливо для 24 битных растров)
#    compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 1 - 100
#              Рекомендуемое значение: 60
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexLoadKmzToRsw_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadKmzToRsw', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def picexLoadKmzToRsw(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _compression: int, _compressJpegQuality: int) -> int:
        return picexLoadKmzToRsw_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _compression, _compressJpegQuality)


# Загрузка матрицы высот рельефа из KMZ в MTW
#    handle - диалог визуального сопровождения процесса обработки.
#    inputFileName  - имя KMZ-файла
#    outputFileName - имя проекта MPT
#    compression    - флаг сжатия выходного файла
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexLoadKmzToMtw_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadKmzToMtw', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexLoadKmzToMtw(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _compression: int) -> int:
        return picexLoadKmzToMtw_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _compression)


#    Сохранить изображение растра в файл формата KMZ
#    Файл KMZ представляет собой ZIP-архив пирамиды растровых тайлов
#    в форматах JPEG или PNG
#    Входные параметры:
#    handle         - диалог сопровождения процесса обработки;
#    inputFileName  - имя исходного файла RSW
#    outputFileName - имя выходного файла KMZ
#    compress       - коэффициент качества (0-100)
#                     изображения при сжатии по методу JPEG
#    При ошибке функция возвращает ноль
#
#    Диалогу (handle) из процесса посылаются сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.

    picexSaveRswImageToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveRswImageToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveRswImageToKmz(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _compress: int) -> int:
        return picexSaveRswImageToKmz_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _compress)


#    Сохранить матрицу высот в файл формата KMZ
#    Файл KMZ представляет собой ZIP-архив пирамиды тайлов
#    в формате TIFF
#    Входные параметры:
#    handle         - диалог сопровождения процесса обработки;
#    inputFileName  - имя исходного файла RSW
#    outputFileName - имя выходного файла KMZ
#    compress       - флаг сжатия
#    При ошибке функция возвращает ноль
#
#    Диалогу (handle) из процесса посылаются сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.

    picexSaveMatrixToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveMatrixToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveMatrixToKmz(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _compress: int) -> int:
        return picexSaveMatrixToKmz_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _compress)


#    Конвертор PCX -> Rsw
#    hmap -  идентификатор открытых данных
#    handle - диалог визуального сопровождения процесса обработки.
#    pcxname - имя PCX-файла;
#    rstname - имя RST-файла(#.rsw);
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadPcxToRstConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadPcxToRstConverterUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double)
    def LoadPcxToRstConverterUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _PcxName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precisionMet: float) -> int:
        return LoadPcxToRstConverterUn_t (_hmap, _handle, _PcxName.buffer(), _RstName.buffer(), _scale, _precisionMet)


#    Конвертор PCX -> Rsw
#    hmap -  идентификатор открытых данных
#    handle - диалог визуального сопровождения процесса обработки.
#    pcxname - имя PCX-файла;
#    rstname - имя RST-файла(#.rsw);
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadPcxToRstConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadPcxToRstConverterExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def LoadPcxToRstConverterExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _pcxname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precisionMet: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return LoadPcxToRstConverterExUn_t (_hmap, _handle, _pcxname.buffer(), _rstname.buffer(), _scale, _precisionMet, _point)


#    hmap -  идентификатор открытых данных
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadPcxToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadPcxToRstAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def LoadPcxToRstAndCompressUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _pcxname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precisionMet: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        return LoadPcxToRstAndCompressUn_t (_hmap, _handle, _pcxname.buffer(), _rstname.buffer(), _scale, _precisionMet, _point, _compression)


#    Запросить параметры PCX-файла
#    pcxname     - имя PCX-файла;
#    information - указатель на структуру DATAINFORMATION для записи параметров PCX-файла
#    Структура DATAINFORMATION описана в picexprm.h
#
#    Функцию LoadPxcInformation рекомендуется вызывать перед началом
#    конвертации PCX-файла в Rsw для инициализации диалога сопровождения

#   LoadPcxInformation_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadPcxInformation', ctypes.c_char_p, ctypes.POINTER(DATAINFORMATION))
#   def LoadPcxInformation(_pcxname: ctypes.c_char_p, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadPcxInformation_t (_pcxname, _information)

#   LoadPcxInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadPcxInformationUn', maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION))
#   def LoadPcxInformationUn(_PcxName: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadPcxInformationUn_t (_PcxName.buffer(), _information)


#    Конвертор Bmp -> Rsw
#    hmap -  идентификатор открытых данных
#    handle    - диалог визуального сопровождения процесса обработки;
#    bmpname   - имя BMP-файла;
#    rstname   - имя RST-файла(#.rsw);
#    scale     - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadBmpToRstConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadBmpToRstConverterUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def LoadBmpToRstConverterUn(_hmap: maptype.HMAP, _Handle: maptype.HMESSAGE, _BmpName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precisionMet: float, _frame: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return LoadBmpToRstConverterUn_t (_hmap, _Handle, _BmpName.buffer(), _RstName.buffer(), _scale, _precisionMet, _frame)


#    Конвертор Bmp -> Rsw
#    hmap -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки;
#    bmpname - имя BMP-файла;
#    rstname - имя RST-файла;
#    scale   - масштаб создаваемого растра;
#    frame   - габариты растра(в метрах на местности)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    LoadBmpToRstByPlaceUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadBmpToRstByPlaceUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.POINTER(maptype.DFRAME))
    def LoadBmpToRstByPlaceUn(_Map: maptype.HMAP, _Handle: maptype.HMESSAGE, _BmpName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadBmpToRstByPlaceUn_t (_Map, _Handle, _BmpName.buffer(), _RstName.buffer(), _scale, _frame)


#    Конвертор Bmp -> Rsw
#    hmap -  идентификатор открытых данных
#    handle    - диалог визуального сопровождения процесса обработки;
#    bmpname   - имя BMP-файла;
#    rstname   - имя RST-файла(#.rsw);
#    scale     - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadBmpToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadBmpToRstAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def LoadBmpToRstAndCompressUn(_Map: maptype.HMAP, _Handle: maptype.HMESSAGE, _BmpName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precisionMet: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        return LoadBmpToRstAndCompressUn_t (_Map, _Handle, _BmpName.buffer(), _RstName.buffer(), _scale, _precisionMet, _point, _compression)


#    Запросить параметры BMP-файла
#    bmpname     - имя BMP-файла;
#    information - указатель на структуру DATAINFORMATION для записи параметров BMP-файла
#    Структура DATAINFORMATION описана в picexprm.h
#
#    Функцию LoadBmpInformation рекомендуется вызывать перед началом
#    конвертации BMP-файла в Rsw для инициализации диалога сопровождения

#   LoadBmpInformation_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadBmpInformation', ctypes.c_char_p, ctypes.POINTER(DATAINFORMATION))
#   def LoadBmpInformation(_bmpname: ctypes.c_char_p, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadBmpInformation_t (_bmpname, _information)

#   LoadBmpInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadBmpInformationUn', maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION))
#   def LoadBmpInformationUn(_bmpname: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadBmpInformationUn_t (_bmpname.buffer(), _information)


#    Конвертор Tiff -> Rsw
#    hmap      -  идентификатор открытых данных
#    handle    - диалог визуального сопровождения процесса обработки.
#    tifname   - имя TIF-файла;
#    rstname   - имя RST-файла;
#    scale     - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadTiffToRstConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadTiffToRstConverterUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double)
    def LoadTiffToRstConverterUn(_hmap: maptype.HMAP, _Handle: maptype.HMESSAGE, _tiffName: mapsyst.WTEXT, _rstName: mapsyst.WTEXT, _scale: float, _precision: float) -> int:
        return LoadTiffToRstConverterUn_t (_hmap, _Handle, _tiffName.buffer(), _rstName.buffer(), _scale, _precision)


#    Конвертор Tiff -> Rsw
#    hmap      -  идентификатор открытых данных
#    handle    - диалог визуального сопровождения процесса обработки.
#    tifname   - имя TIF-файла;
#    rstname   - имя RST-файла;
#    scale     - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

   
    LoadTiffToRstConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadTiffToRstConverterExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def LoadTiffToRstConverterExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _tifname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return LoadTiffToRstConverterExUn_t (_hmap, _handle, _tifname.buffer(), _rstname.buffer(), _scale, _precision, _point)


#    Конвертор Tiff -> Rsw
#    hmap    -  идентификатор открытых данных
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    Handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadTiffToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadTiffToRstAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def LoadTiffToRstAndCompressUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        return LoadTiffToRstAndCompressUn_t (_hmap, _handle, _TiffName.buffer(), _RstName.buffer(), _scale, _precision, _point, _compression)


#    Конвертор Tiff -> Rsw
#    hmap      -  идентификатор открытых данных
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    Handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    flagIgnoreGeoTiff - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#              0 - привязка и СК считываются из тега
#                  исходного файла и устанавливаются в выходной растр
#              1 - привязка устанавливается в выходной растр из
#                  аргумента point, СК не устанавливается
#    arg1,arg2 - параметры не используются
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadTiffToRstAndCompressExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadTiffToRstAndCompressExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadTiffToRstAndCompressExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _RstName: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagIgnoreGeoTiff: int, _arg1: int, _arg2: int) -> int:
        return LoadTiffToRstAndCompressExUn_t (_hmap, _handle, _TiffName.buffer(), _RstName.buffer(), _scale, _precision, _point, _compression, _flagIgnoreGeoTiff, _arg1, _arg2)


#    Запросить параметры TIFF-файла
#    tifname     - имя TIFF-файла;
#    information -  указатель на структуру DATAINFORMATION для записи параметров TIFF-файла
#    Структура DATAINFORMATION описана в picexprm.h
#
#    Функцию LoadTifInformation рекомендуется вызывать перед началом
#    конвертации TIFF-файла в Rsw для инициализации диалога сопровождения

#   LoadTifInformation_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadTifInformation', maptype.HMESSAGE, ctypes.c_char_p, ctypes.POINTER(DATAINFORMATION))
#   def LoadTifInformation(_handle: maptype.HMESSAGE, _TifName: ctypes.c_char_p, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadTifInformation_t (_handle, _TifName, _information)

#   LoadTifInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadTifInformationUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION))
#   def LoadTifInformationUn(_handle: maptype.HMESSAGE, _TifName: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadTifInformationUn_t (_handle, _TifName.buffer(), _information)


#    Запросить параметры GeoTIFF-файла
#    TifName - имя GeoTIF-файла;
#    DataInformation - структура, которую необходимо заполнить
#    geoTIFFinformation - структура, которую необходимо заполнить
#    Структуры DATAINFORMATION и GEOTIFFINFORMATION описаны в picexprm.h
#
#    Функцию LoadGeoTifInformation рекомендуется вызывать перед началом
#    конвертации TIFF-файла в Rsw для инициализации диалога сопровождения

    
    LoadGeoTifInformationUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadGeoTifInformationUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION), ctypes.POINTER(GEOTIFFINFORMATION))
    def LoadGeoTifInformationUn(_Handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION), _geoTIFFinformation: ctypes.POINTER(GEOTIFFINFORMATION)) -> int:
        return LoadGeoTifInformationUn_t (_Handle, _TiffName.buffer(), _information, _geoTIFFinformation)


#    Запросить параметры СК из файла GeoTiff
#    Handle              - диалог визуального сопровождения процесса обработки.
#    TifName             - имя TIF-файла;
#    geoTIFFparam        - указатель на структуру GEOTIFFPARAM для записи
#                                                                параметров СК

#   LoadGeoTiffParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadGeoTiffParameters', maptype.HMESSAGE, ctypes.c_char_p, ctypes.POINTER(GEOTIFFPARAM))
#   def LoadGeoTiffParameters(_Handle: maptype.HMESSAGE, _TiffName: ctypes.c_char_p, _geoTIFFparam: ctypes.POINTER(GEOTIFFPARAM)) -> int:
#       return LoadGeoTiffParameters_t (_Handle, _TiffName, _geoTIFFparam)

#   LoadGeoTiffParametersUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadGeoTiffParametersUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(GEOTIFFPARAM))
#   def LoadGeoTiffParametersUn(_Handle: maptype.HMESSAGE, _TiffName: mapsyst.WTEXT, _geoTIFFparam: ctypes.POINTER(GEOTIFFPARAM)) -> int:
#       return LoadGeoTiffParametersUn_t (_Handle, _TiffName.buffer(), _geoTIFFparam)


#    Запросить параметры JPEG-файла
#    inputname   - имя JPEG-файла;
#    information -  указатель на структуру DATAINFORMATION для записи параметров JPEG-файла
#    Структура DATAINFORMATION описана в picexprm.h
#
#    Функцию LoadJPEGInformation рекомендуется вызывать перед началом
#    преобразования JPEG-файла в Rsw для вывода информации о графическом файле

#   LoadJPEGInformation_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadJPEGInformation', ctypes.c_char_p, ctypes.POINTER(DATAINFORMATION))
#   def LoadJPEGInformation(_inputname: ctypes.c_char_p, _iformation: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadJPEGInformation_t (_inputname, _iformation)

#   LoadJPEGInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadJPEGInformationUn', maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION))
#   def LoadJPEGInformationUn(_inputname: mapsyst.WTEXT, _iformation: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return LoadJPEGInformationUn_t (_inputname.buffer(), _iformation)


#    hmap    -  идентификатор открытых данных
#    PcxName - имя PCX-файла;
#    RstName - имя RST-файла;
#    scale   - масштаб создаваемого растра
#    precision - разрешающая способность создаваемого растра(т/м)
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    Handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    flagMessage - параметр не используется
#                  Управление диагностическими сообщениями осуществляется
#                  вызовом функции mapMessageEnable.
#                  Если mapIsMessageEnable() возвращает 0, то
#                  диагностические сообщения не выдаются.
#
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadJpegToRswAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadJpegToRswAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int)
    def LoadJpegToRswAndCompressUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precisionMeters: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagMessage: int) -> int:
        return LoadJpegToRswAndCompressUn_t (_map, _handle, _inputname.buffer(), _rstname.buffer(), _scale, _precisionMeters, _point, _compression, _flagMessage)


# Сохранить изображение 24-х битного растра RSW в файл JPEG
# hmap                -  идентификатор открытых данных
# handle              - диалог визуального сопровождения процесса обработки
# rswName             - имя файла 24-х битного растра RSW
# jpegName            - имя файла JPEG
# compressJpegQuality - степень сжатия блока растра по алгоритму JPEG
#              Возможные значения: 10 - 100
#              Рекомендуемое значение: 60

    
    picexSaveRswToJpegUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveRswToJpegUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveRswToJpegUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rswName: mapsyst.WTEXT, _jpegName: mapsyst.WTEXT, _compressJpegQuality: int) -> int:
        return picexSaveRswToJpegUn_t (_hmap, _handle, _rswName.buffer(), _jpegName.buffer(), _compressJpegQuality)


#    Сохранить растровую карту в формате BMP
#    hmap    -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки.
#    rstname - имя RST-файла;
#    bmpname - имя BMP-файла;
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadRstToBmpConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToBmpConverterUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR)
    def LoadRstToBmpConverterUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstname: mapsyst.WTEXT, _bmpname: mapsyst.WTEXT) -> int:
        return LoadRstToBmpConverterUn_t (_hmap, _handle, _rstname.buffer(), _bmpname.buffer())


#    Сохранить растровую карту в формате BMP с возможной обрезкой изображения по рамке растра
#    hmap    -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки.
#    rstname - имя RST-файла;
#    bmpname - имя BMP-файла;
#    flagUseBorder - флаг "Вырезать изображение по рамке"(0/1)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadRstToBmpConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToBmpConverterExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def LoadRstToBmpConverterExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstname: mapsyst.WTEXT, _bmpname: mapsyst.WTEXT, _flagUseBorder: int) -> int:
        return LoadRstToBmpConverterExUn_t (_hmap, _handle, _rstname.buffer(), _bmpname.buffer(), _flagUseBorder)


#    Сохранить растровую карту в формате BMP
#    с предварительной очисткой области изображения цветом colorClear
#    Для растров с 1,4,8 бит на пиксель colorClear - индекс цвета палитры растра,
#    для растров с 16,24,32 бит на пиксель colorClear - цвет COLORREF,
#    hmap    -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки.
#    rstname - имя RST-файла;
#    bmpname - имя BMP-файла;
#    flagUseBorder - флаг "Вырезать изображение по рамке"
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadRstToBmpConverterClearUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToBmpConverterClearUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_long)
    def LoadRstToBmpConverterClearUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstname: mapsyst.WTEXT, _bmpname: mapsyst.WTEXT, _flagUseBorder: int, _colorClear: int) -> int:
        return LoadRstToBmpConverterClearUn_t (_hmap, _handle, _rstname.buffer(), _bmpname.buffer(), _flagUseBorder, _colorClear)

    LoadRstToBmpBackgroundClear_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToBmpBackgroundClear', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, maptype.COLORREF)
    def LoadRstToBmpBackgroundClear(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstNumber: int, _bmpname: mapsyst.WTEXT, _flagUseBorder: int, _colorClear: maptype.COLORREF) -> int:
        return LoadRstToBmpBackgroundClear_t (_hmap, _handle, _rstNumber, _bmpname.buffer(), _flagUseBorder, _colorClear)


#    Сохранить растровую карту в формате PCX
#    hmap    -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки.
#    rstname - имя RST-файла;
#    pcxname - имя PCX-файла;
#    flagUseBorder - флаг "Вырезать изображение по рамке"
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    SaveRstToPcxUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'SaveRstToPcxUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def SaveRstToPcxUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rstname: mapsyst.WTEXT, _pcxname: mapsyst.WTEXT, _flagUseBorder: int) -> int:
        return SaveRstToPcxUn_t (_map, _handle, _rstname.buffer(), _pcxname.buffer(), _flagUseBorder)


#    Сохранить растровую карту в формате PCX
#    с предварительной очисткой области изображения цветом colorClear
#    Для растров с 1,4,8 бит на пиксель colorClear - индекс цвета палитры растра,
#    для растров с 16,24,32 бит на пиксель colorClear - цвет COLORREF,
#    hmap    -  идентификатор открытых данных
#    handle  - диалог визуального сопровождения процесса обработки.
#    rstname - имя RST-файла;
#    pcxname - имя PCX-файла;
#    flagUseBorder - флаг "Вырезать изображение по рамке"
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    SaveRstToPcxClearUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'SaveRstToPcxClearUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_long)
    def SaveRstToPcxClearUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rstname: mapsyst.WTEXT, _pcxname: mapsyst.WTEXT, _flagUseBorder: int, _colorClear: int) -> int:
        return SaveRstToPcxClearUn_t (_map, _handle, _rstname.buffer(), _pcxname.buffer(), _flagUseBorder, _colorClear)

    LoadRstToPcxBackgroundClear_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToPcxBackgroundClear', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_long)
    def LoadRstToPcxBackgroundClear(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rstNumber: int, _pcxname: mapsyst.WTEXT, _flagUseBorder: int, _colorClear: int) -> int:
        return LoadRstToPcxBackgroundClear_t (_map, _handle, _rstNumber, _pcxname.buffer(), _flagUseBorder, _colorClear)


#    Сохранить растровую карту в формате TIFF
#    hmap    -  идентификатор открытых данных
#    RstName  - имя RST-файла;
#    TiffName - имя TIFF-файла;
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой (рекомендуемое значение - 0)
#    platform - Тип платформы (0 - INTEL, 1 - MOTOROLA)             (рекомендуемое значение - 0)
#    imageStructure - Структура изображения TIFF (0 - BLOCK, 1- STRIP, 2 - NONFRAG) (рекомендуемое значение - 1)
#    compressMethod - Флаг сжатия изображения (0- не применять сжатие, 1 - сжатие PackBit) (рекомендуемое значение - 0)
#    flagCMYK - выбор цветовой модели:
#                     0 - цветовая модель RGB 24 бит на пиксел
#                     1 - цветовая модель CMYK 32 бит на пиксел
#                     Режим поддерживается только для  растров 24,32 бит на пиксел.
#    handle - диалог визуального сопровождения процесса обработки.

    
    LoadRstToTiffConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToTiffConverterUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadRstToTiffConverterUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _RstName: mapsyst.WTEXT, _TiffName: mapsyst.WTEXT, _flagborder: int, _platform: int, _imageStructure: int, _compressMethod: int, _flagCMYK: int) -> int:
        return LoadRstToTiffConverterUn_t (_hmap, _handle, _RstName.buffer(), _TiffName.buffer(), _flagborder, _platform, _imageStructure, _compressMethod, _flagCMYK)


#    Сохранить растровую карту в формате TIFF
#    hmap           -  идентификатор открытых данных
#    handle         - диалог визуального сопровождения процесса обработки.
#    RstName        - имя RST-файла;
#    TiffName       - имя TIFF-файла;
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#                     (рекомендуемое значение - 0).
#    platform - Тип платформы (0 - INTEL, 1 - MOTOROLA)
#                     (рекомендуемое значение - 0).
#    imageStructure - Структура изображения TIFF (0 - BLOCK, 1- STRIP, 2 - NONFRAG)
#                     (рекомендуемое значение - 1).
#    compressMethod - Флаг сжатия изображения (0- не применять сжатие, 1 - сжатие PackBit)
#                     (рекомендуемое значение - 0).
#    flagCMYK - выбор цветовой модели:
#                     0 - цветовая модель RGB 24 бит на пиксел
#                     1 - цветовая модель CMYK 32 бит на пиксел
#                     Режим поддерживается только для  растров 24,32 бит на пиксел.
#    flagIntergraph - Флаг записи матрицы трансформирования,
#                        с помощью которой Intergraph определяет привязку растра
#    dframe         - Габариты изображения в районе в метрах.
#                     Параметр обязателен для записи матрицы трансформирования (если flagIntergraph == 1)
#    flag1 - flag6  - Не используются. Должны быть равны нулю.

    
    LoadRstToTiffConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstToTiffConverterExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadRstToTiffConverterExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _RstName: mapsyst.WTEXT, _tiffName: mapsyst.WTEXT, _flagborder: int, _platform: int, _imageStructure: int, _compressMethod: int, _flagCMYK: int, _flagIntergraph: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flag1: int, _flag2: int, _flag3: int, _flag4: int, _flag5: int, _flag6: int) -> int:
        return LoadRstToTiffConverterExUn_t (_hmap, _handle, _RstName.buffer(), _tiffName.buffer(), _flagborder, _platform, _imageStructure, _compressMethod, _flagCMYK, _flagIntergraph, _dframe, _flag1, _flag2, _flag3, _flag4, _flag5, _flag6)

    LoadRasterToTiffConverter_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRasterToTiffConverter', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def LoadRasterToTiffConverter(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstNumber: int, _tiffName: mapsyst.WTEXT, _flagborder: int, _compressMethod: int, _flagCMYK: int, _flagIntergraph: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadRasterToTiffConverter_t (_hmap, _handle, _rstNumber, _tiffName.buffer(), _flagborder, _compressMethod, _flagCMYK, _flagIntergraph, _dframe)


#    Вырезать изображение растровой карты по прямоугольной области, заданной в метрах
#    hmap          -  идентификатор открытых данных
#    handle        - диалог визуального сопровождения процесса обработки.
#    rstInputName  - имя файла растровой карты;
#    rstOutputName - имя файла формируемой растровой карты;
#    frame         - габариты вырезаемой прямоугольной области(в метрах)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadCutOfRstByFrameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutOfRstByFrameUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def LoadCutOfRstByFrameUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstInputName: mapsyst.WTEXT, _rstOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadCutOfRstByFrameUn_t (_hmap, _handle, _rstInputName.buffer(), _rstOutputName.buffer(), _frame)

    LoadCutRasterByFrame_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutRasterByFrame', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def LoadCutRasterByFrame(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstNumber: int, _rstOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadCutRasterByFrame_t (_hmap, _handle, _rstNumber, _rstOutputName.buffer(), _frame)


#    Вырезать изображение растровой карты по прямоугольной области, заданной в метрах
#    hmap          -  идентификатор открытых данных
#    handle        - диалог визуального сопровождения процесса обработки.
#    rstInputName  - имя файла растровой карты;
#    rstOutputName - имя файла формируемой растровой карты;
#    frame         - габариты вырезаемой прямоугольной области(в метрах)
#    flagUpdateRstDuplicates - флаг создания уменьшенной копии (0-нет, 1-да)
#
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadCutOfRstByFrameExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutOfRstByFrameExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int)
    def LoadCutOfRstByFrameExUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rstInputName: mapsyst.WTEXT, _rstOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME), _flagUpdateRstDuplicates: int) -> int:
        return LoadCutOfRstByFrameExUn_t (_map, _handle, _rstInputName.buffer(), _rstOutputName.buffer(), _frame, _flagUpdateRstDuplicates)


#    Вырезать изображение матрицы по прямоугольной области, заданной в метрах
#    hmap          -  идентификатор открытых данных
#    handle        - диалог визуального сопровождения процесса обработки.
#    rstInputName  - имя файла матрицы;
#    rstOutputName - имя файла формируемой матрицы;
#    frame         - габариты вырезаемой прямоугольной области(в метрах)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadCutOfMtrByFrameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutOfMtrByFrameUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def LoadCutOfMtrByFrameUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mtrInputName: mapsyst.WTEXT, _mtrOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadCutOfMtrByFrameUn_t (_hmap, _handle, _mtrInputName.buffer(), _mtrOutputName.buffer(), _frame)

    LoadCutMatrixByFrame_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutMatrixByFrame', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def LoadCutMatrixByFrame(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mtrNumber: int, _mtrOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadCutMatrixByFrame_t (_hmap, _handle, _mtrNumber, _mtrOutputName.buffer(), _frame)


# Вырезать изображение матрицы по прямоугольной области
# с учётом рамки исходной матрицы
#   hmap          -  идентификатор открытых данных
#   handle        - диалог визуального сопровождения процесса обработки
#   mtrInputName  - имя файла исходной матрицы
#   mtrOutputName - имя файла формируемой матрицы
#   frame         - габариты вырезаемой прямоугольной области(в метрах)
#   flag - флаг учёта рамки исходной матрицы, значения :
#     0 - рамка исходной матрицы не учитывается,
#     1 - элементы исходной матрицы, находящиеся вне рамки, не используются
#         (чистка формируемых элементов вне рамки)
#     2 - значения элементов исходной матрицы, находящихся вне рамки,
#         заменяются на fillValue (заливка значением fillValue
#         формируемых элементов вне рамки)
#   fillValue - значение для заливки формируемых элементов вне рамки,
#               используется при flag = 2, должно быть больше -111111
#               (если fillValue <= -111111, то выполняется чистка формируемых
#                элементов вне рамки как при flag = 1)
#   Диалогу визуального сопровождения процесса обработки посылаются
#   сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#      WPARAM - текущее состоние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#   -  (WM_ERROR) Извещение об ошибке
#      LPARAM - указатель на структуру ERRORINFORMATION
#      Структура ERRORINFORMATION описана в picexprm.h,
#      WM_PROGRESSBAR и WM_ERROR - в maptype.h
#
#   При ошибке возвращает ноль

    
    LoadCutOfMtrByFrameExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutOfMtrByFrameExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double)
    def LoadCutOfMtrByFrameExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mtrInputName: mapsyst.WTEXT, _mtrOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _fillValue: float) -> int:
        return LoadCutOfMtrByFrameExUn_t (_hmap, _handle, _mtrInputName.buffer(), _mtrOutputName.buffer(), _frame, _flag, _fillValue)


#    Трансформирование матрицы
# (вычисление коэффициентов пересчета координат методом наименьших квадратов)
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap       -  идентификатор открытых данных
#   parm      - параметры прикладной задачи;
#   namein    - имя исходного растра (maptype.MAX_PATH_LONG)
#   nameout   - имя выходного растра (размер выделенной памяти д.б. не менее maptype.MAX_PATH_LONG символов);
#               в случае незаданного или совпадающего с исходным выходного имени,
#               будет создана копия исходной матрицы - <имя_исходной_матрицы>~.mtw;
#               результат будет записан в исходный файл;
#   sizeNameOut - размер выделенной памяти для nameout в байтах
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек.
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль

    
    MtwTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'MtwTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def MtwTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _sizeNameOut: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return MtwTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _sizeNameOut, _count, _fact, _teor)


# Формирование матрицы высот с измененными параметрами из исходной
# handle   - диалог визуального сопровождения процесса обработки.
# sourceMtwName - имя исходной матрицы высот
# outputMtwName - имя выходной матрицы высот
# newParam      - указатель на структуру новых параметров
#                 выходной матрицы, тип структуры BUILDMTW
# flagSmoothing - флаг Сглаживание высот
#
# Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль

    picexMatrixParametersChange_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMatrixParametersChange', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.c_int)
    def picexMatrixParametersChange(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _sourceMtwName: mapsyst.WTEXT, _outputMtwName: mapsyst.WTEXT, _newParam: ctypes.POINTER(maptype.BUILDMTW), _flagSmoothing: int) -> int:
        return picexMatrixParametersChange_t (_hmap, _handle, _sourceMtwName.buffer(), _outputMtwName.buffer(), _newParam, _flagSmoothing)


#    Сохранить матрицу в файл формата TIFF
#    handle         - диалог визуального сопровождения процесса обработки.
#    mtwName        - имя файла матрицы
#    tiffName       - имя TIFF-файла;
#    flagborder     - флаг использования рамки
#                     0 - включать в формируемый файл все элементы матрицы
#                     1 - не включать в формируемый файл элементы матрицы
#                         невходящие в область, ограниченную рамкой
#    dframe         - прямоугольная область сохраняемых элементов матрицы
#                     указатель м.б. равен нулю
# При ошибке возвращает ноль

    
    LoadMtwToTiffConverterUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtwToTiffConverterUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def LoadMtwToTiffConverterUn(_handle: maptype.HMESSAGE, _mtwName: mapsyst.WTEXT, _tiffName: mapsyst.WTEXT, _flagborder: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadMtwToTiffConverterUn_t (_handle, _mtwName.buffer(), _tiffName.buffer(), _flagborder, _dframe)


#    Сохранить матрицу в формате TIFF
#    handle         - диалог визуального сопровождения процесса обработки.
#    mtwName        - имя файла матрицы
#    tiffName       - имя TIFF-файла;
#    fileName       - имя файла параметров (TFW, TAB);
#    flagborder     - флаг использования рамки
#                     0 - включать в формируемый файл все элементы матрицы
#                     1 - не включать в формируемый файл элементы матрицы
#                         невходящие в область, ограниченную рамкой
#    dframe         - прямоугольная область сохраняемых элементов матрицы
#                     указатель м.б. равен нулю
# При ошибке возвращает ноль

    LoadMtwToTiffConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtwToTiffConverterExUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def LoadMtwToTiffConverterExUn(_handle: maptype.HMESSAGE, _mtwName: mapsyst.WTEXT, _tiffName: mapsyst.WTEXT, _fileName: mapsyst.WTEXT, _flagborder: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadMtwToTiffConverterExUn_t (_handle, _mtwName.buffer(), _tiffName.buffer(), _fileName.buffer(), _flagborder, _dframe)


#    Сохранить матрицу в формате BigTIFF
#    handle         - диалог визуального сопровождения процесса обработки.
#    mtwName        - имя файла матрицы
#    tiffName       - имя TIFF-файла;
#    fileName       - имя файла параметров (TFW, TAB);
#    flagborder     - флаг использования рамки
#                     0 - включать в формируемый файл все элементы матрицы
#                     1 - не включать в формируемый файл элементы матрицы
#                         невходящие в область, ограниченную рамкой
#    dframe         - прямоугольная область сохраняемых элементов матрицы
#                     указатель м.б. равен нулю
# При ошибке возвращает ноль

    LoadMtwToBigTiffConverter_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtwToBigTiffConverter', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DFRAME))
    def LoadMtwToBigTiffConverter(_handle: maptype.HMESSAGE, _mtwName: mapsyst.WTEXT, _tiffName: mapsyst.WTEXT, _fileName: mapsyst.WTEXT, _flagborder: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadMtwToBigTiffConverter_t (_handle, _mtwName.buffer(), _tiffName.buffer(), _fileName.buffer(), _flagborder, _dframe)


# Загрузка матриц из формата SRTM (GeoTIFF)
# hmap     -  идентификатор открытых данных
# handle   - диалог визуального сопровождения процесса обработки.
# tiffname - имя исходного файла формата SRTM (GeoTIFF)
# mtwname  - имя файла формируемой матрицы
# scale    - масштаб формируемой матрицы
# flagCompress - параметр не используется, равен 0
# При ошибке возвращает ноль

    LoadGeoTiffToMtwPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadGeoTiffToMtwPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadGeoTiffToMtwPro(_handle: maptype.HMESSAGE, _nameTiff: mapsyst.WTEXT, _nameMtr: mapsyst.WTEXT, _scale: float, _flagCompress: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return LoadGeoTiffToMtwPro_t (_handle, _nameTiff.buffer(), _nameMtr.buffer(), _scale, _flagCompress, _callevent, _parm)

    LoadGeoTiffToMtrUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadGeoTiffToMtrUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_int)
    def LoadGeoTiffToMtrUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _tiffname: mapsyst.WTEXT, _mtwname: mapsyst.WTEXT, _scale: float = 100000, _flagCompress: int = 0) -> int:
        return LoadGeoTiffToMtrUn_t (_map, _handle, _tiffname.buffer(), _mtwname.buffer(), _scale, _flagCompress)

    

#    Сохранить карту в формате RSW
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    filename   - имя файла сохраняемого изображения RSW
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount   - количество бит на пиксель сохраняемого изображения
#    meterInElement - размер пикселя сохраняемого изображения в метрах
#    flagCompress   - Флаг сжатия изображения
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadDocumentImageToRswFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToRswFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def LoadDocumentImageToRswFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitCount: int, _meterInElement: float, _flagCompress: int) -> int:
        return LoadDocumentImageToRswFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitCount, _meterInElement, _flagCompress)


#    Сохранить карту в формате BMP, JPEG, PNG
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    filename   - имя файла сохраняемого изображения RSW
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount   - количество бит на пиксель сохраняемого изображения
#    meterInElement - размер пикселя сохраняемого изображения в метрах
#    resolutionMet  - разрешающая способность сохраняемого изображения (точек на метр)
#    flagCompress   - При сохранении файла TIFF - Флаг сжатия изображения
#                    (0- не применять сжатие, 1 - сжатие PackBit)
#                    При сохранении файла JPG  - Коэффициент качества
#                    изображения при сжатии JPEG (0-100)
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadDocumentImageToPictureFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToPictureFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def LoadDocumentImageToPictureFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitCount: int, _meterInElement: float, _flagCompress: int) -> int:
        return LoadDocumentImageToPictureFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitCount, _meterInElement, _flagCompress)

    LoadDocumentImageToPictureFileEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToPictureFileEx', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int)
    def LoadDocumentImageToPictureFileEx(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitCount: int, _scale: float, _resolutionMet: float, _flagCompress: int) -> int:
        return LoadDocumentImageToPictureFileEx_t (_hmap, _handle, _filename.buffer(), _dframe, _bitCount, _scale, _resolutionMet, _flagCompress)


#    Сохранить карту в формате TIFF GrayScale (8 бит на пиксель)
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    filename   - имя файла сохраняемого изображения RSW
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    meterInElement - размер пикселя сохраняемого изображения в метрах
#    resolutionMet  - разрешающая способность сохраняемого изображения (точек на метр)
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadDocumentImageToGrayScaleTiffFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToGrayScaleTiffFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double)
    def LoadDocumentImageToGrayScaleTiffFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _meterInElement: float) -> int:
        return LoadDocumentImageToGrayScaleTiffFile_t (_hmap, _handle, _filename.buffer(), _dframe, _meterInElement)

    LoadDocumentImageToGrayScaleTiffFileEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadDocumentImageToGrayScaleTiffFileEx', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_double)
    def LoadDocumentImageToGrayScaleTiffFileEx(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _scale: float, _resolutionMet: float) -> int:
        return LoadDocumentImageToGrayScaleTiffFileEx_t (_hmap, _handle, _filename.buffer(), _dframe, _scale, _resolutionMet)


#    Сохранить изображение растра в файл формата KMZ
#    Файл KMZ представляет собой ZIP-архив пирамиды растровых тайлов
#    в форматах JPEG или PNG
#    Входные параметры:
#    handle       - диалог сопровождения процесса обработки;
#    filename     - имя выходного файла
#    compress     - коэффициент качества (0-100)
#                   JPEG-изображения при сжатии по JPEG методу
#    При ошибке функция возвращает ноль

    picexSaveRswImageToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveRswImageToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveRswImageToKmz(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _compress: int) -> int:
        return picexSaveRswImageToKmz_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _compress)


#    Сохранить карту в формате BMP, Tiff, JPG, RSW
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount   - кол-во бит на пиксел сохраняемого изображения (16, 24-рекомендуемое значение, 32)
#    scale      - масштаб сохраняемого изображения
#    resolution - разрешающая способность сохраняемого изображения (точек на дюйм)
#    filename   - имя файла сохраняемого изображения (#.bmp, #.tif);
#    flagIntergraphTIFF - Флаг записи матрицы трансформирования для использования в программе Intergraph
#                 Аргумент flagIntergraphTIFF применим при сохранении файла TIFF
#    flagCompress  - При сохранении файла TIFF - Флаг сжатия изображения (0- не применять сжатие, 1 - сжатие PackBit)
#                    При сохранении файла JPG  - Коэффициент качества изображения при сжатии JPEG (0-100)
#    handleMainWin - должен быть равен нулю
#    flafAdjustMode- Флаг установки доступности для выполнения команды Adjust
#                    0 - adjustMode не устанавливался
#                    1 - adjustMode уже установлен до вызова функции
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadMapToPictureFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToPictureFileUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int)
    def LoadMapToPictureFileUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _dframe: ctypes.POINTER(maptype.DFRAME), _bitCount: int, _scale: int, _resolution: int, _filename: mapsyst.WTEXT, _flagIntergraphTIFF: int, _flagCompress: int, _handleMainWin: maptype.HMESSAGE, _flafAdjustMode: int) -> int:
        return LoadMapToPictureFileUn_t (_hmap, _handle, _dframe, _bitCount, _scale, _resolution, _filename.buffer(), _flagIntergraphTIFF, _flagCompress, _handleMainWin, _flafAdjustMode)


#    Сохранить карту в формате BMP, Tiff, RSW
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount   - кол-во бит на пиксел сохраняемого изображения (16, 24-рекомендуемое значение, 32)
#    scale      - масштаб сохраняемого изображения
#    resolution - разрешающая способность сохраняемого изображения (точек на дюйм)
#    filename   - имя файла сохраняемого изображения (#.bmp, #.tif);
#    handleMainWin - должен быть равен нулю
#    При ошибке функция возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMapToPictureUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToPictureUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.HMESSAGE)
    def LoadMapToPictureUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _scale: int, _resolution: int, _filename: mapsyst.WTEXT, _handleMainWin: maptype.HMESSAGE) -> int:
        return LoadMapToPictureUn_t (_map, _handle, _dframe, _bitcount, _scale, _resolution, _filename.buffer(), _handleMainWin)


#    Сохранить карту как TIFF GrayScale (8 бит на пиксель - 256 градаций серого)
#    hmap       -  идентификатор открытых данных
#    handle     - диалог сопровождения процесса обработки;
#    dframe     - фрагмент сохраняемой карты(в метрах на местности)
#    scale      - масштаб сохраняемого изображения
#    resolution - разрешающая способность сохраняемого изображения (точек на дюйм)
#    tiffName   - имя сохраняемого TIFF-файла;
#    handleMainWin - должен быть равен нулю
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMapToGrayScaleTiffUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToGrayScaleTiffUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.HMESSAGE)
    def LoadMapToGrayScaleTiffUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _dframe: ctypes.POINTER(maptype.DFRAME), _scale: int, _resolution: int, _tiffName: mapsyst.WTEXT, _handleMainWin: maptype.HMESSAGE) -> int:
        return LoadMapToGrayScaleTiffUn_t (_hmap, _handle, _dframe, _scale, _resolution, _tiffName.buffer(), _handleMainWin)


#    Сохранить карту в формате BMP
#    hmap         -  идентификатор открытых данных
#    handle       - диалог визуального сопровождения процесса обработки.
#    dframe       - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount     - кол-во бит на пиксел сохраняемого изображения(16,24,32)
#    scale        - масштаб сохраняемого изображения
#    resolution   - разрешающая способность сохраняемого изображения(точек на дюйм)
#    bmpname      - имя файла сохраняемого изображения (#.bmp);
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMapToBmpUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToBmpUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def LoadMapToBmpUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _scale: int, _resolution: int, _bmpname: mapsyst.WTEXT) -> int:
        return LoadMapToBmpUn_t (_hmap, _handle, _dframe, _bitcount, _scale, _resolution, _bmpname.buffer())


#    Сохранить карту в формате EMF
#    hmap         -  идентификатор открытых данных
#    handle       - диалог визуального сопровождения процесса обработки.
#    rectmetr     - фрагмент сохраняемой карты(в метрах на местности)
#    bitcount = 24 - кол-во бит на пиксел сохраняемого изображения
#    scale        - масштаб сохраняемого изображения
#    resolution   - разрешающая способность сохраняемого изображения (точек на дюйм)
#    emfname      - имя файла сохраняемого изображения (#.emf);
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h
    if os.name == 'nt':
    
        LoadMapToEmfUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToEmfUn', maptype.HMAP, maptype.HMESSAGE, maptype.RECT, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
        def LoadMapToEmfUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rectmetr: maptype.RECT, _bitcount: int, _scale: int, _resolution: int, _emfname: mapsyst.WTEXT) -> int:
            return LoadMapToEmfUn_t (_map, _handle, _rectmetr, _bitcount, _scale, _resolution, _emfname.buffer())


# Сохранить карту в растровом формате CMYK и RGB (BMP, ...)
# с целью подготовки карты к печати
#  parm   - параметры построения изображения
#  nameun - имя файла сохраняемого изображения
#  Диалогу визуального сопровождения процесса обработки посылаются
#  сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# (При работе программы используется около 60 Мб оперативной памяти)
    if os.name == 'nt':
        LoadMapToRasterForPrint_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToRasterForPrint', ctypes.POINTER(SAVEASPICTRPARM_FOR_PRINT))
        def LoadMapToRasterForPrint(_parm: ctypes.POINTER(SAVEASPICTRPARM_FOR_PRINT)) -> int:
            return LoadMapToRasterForPrint_t (_parm)

        LoadMapToRasterForPrintUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToRasterForPrintUn', ctypes.POINTER(SAVEASPICTRPARM_FOR_PRINT), maptype.PWCHAR)
        def LoadMapToRasterForPrintUn(_parm: ctypes.POINTER(SAVEASPICTRPARM_FOR_PRINT), _nameun: mapsyst.WTEXT) -> int:
            return LoadMapToRasterForPrintUn_t (_parm, _nameun.buffer())


# Сохранить карту в растровом формате CMYK (BMP, ...)
#  hmap   -  идентификатор открытых данных
#  handle - диалог визуального сопровождения процесса обработки
#  rect   - область сохраняемой карты (в пикселах)
#  parm   - дополнительные параметры отображения
#
#  Диалогу визуального сопровождения процесса обработки посылаются
#  сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.

    if os.name == 'nt':
        LoadMapToRasterCMYKEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToRasterCMYKEx', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.RECT), ctypes.POINTER(SAVEASPICTRPARMEX))
        def LoadMapToRasterCMYKEx(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rect: ctypes.POINTER(maptype.RECT), _parm: ctypes.POINTER(SAVEASPICTRPARMEX)) -> int:
            return LoadMapToRasterCMYKEx_t (_hmap, _handle, _rect, _parm)

        LoadMapToRasterCMYK_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToRasterCMYK', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.RECT), ctypes.POINTER(SAVEASPICTRPARM))
        def LoadMapToRasterCMYK(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rect: ctypes.POINTER(maptype.RECT), _parm: ctypes.POINTER(SAVEASPICTRPARM)) -> int:
            return LoadMapToRasterCMYK_t (_hmap, _handle, _rect, _parm)

        LoadMapToRasterCMYK_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMapToRasterCMYK_Un', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.RECT), ctypes.POINTER(SAVEASPICTRPARMUN))
        def LoadMapToRasterCMYK_Un(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rect: ctypes.POINTER(maptype.RECT), _parm: ctypes.POINTER(SAVEASPICTRPARMUN)) -> int:
            return LoadMapToRasterCMYK_Un_t (_hmap, _handle, _rect, _parm)


# Вывести изображение карты в метафайл с обрезкой объектов по рамке
# (Функция реализована только для платформы Windows)
#    handle  - диалог визуального сопровождения процесса обработки.
#    hmap    -  идентификатор открытых данных
#    name    - имя метафайла
#    Структура METAFILEBUILDPARMEX описана в maptype.h
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке в параметрах возвращает ноль

    if os.name == 'nt':
    
        PaintToEmfByFrameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'PaintToEmfByFrameUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.METAFILEBUILDPARMEX))
        def PaintToEmfByFrameUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.METAFILEBUILDPARMEX)) -> int:
            return PaintToEmfByFrameUn_t (_handle, _hmap, _name.buffer(), _parm)


#    Оптимизировать файл растровой карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    name           - имя файла растровой карты
#    newname        - имя файла оптимизированной растровой карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     1 - алгоритм сжатия LZW
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения,
#                         не входящие в область, ограниченную рамкой
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadRstOptimizationUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstOptimizationUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadRstOptimizationUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadRstOptimizationUn_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Оптимизировать файл растровой карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           -  идентификатор открытых данных
#    name           - имя файла растровой карты
#    newname        - имя файла оптимизированной растровой карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     1 - алгоритм сжатия LZW
#                     2 - алгоритм сжатия JPEG (для 24 битных растров)
#    jpegCompressValue - степень сжатия изображения растра по алгоритму JPEG
#                        имеет значение, если compressnumber присвоено значение 2
#                        (1-100, 1-максимальное сжатие, 100-сжатие без потери качества),
#                         рекомендуется значение 60.
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#     Добавлен пересчет габаритов растра при обрезке изображения по
#     рамке растра (когда flagborder == 1).
#    При ошибке возвращает ноль

    
    LoadRstOptimizationAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstOptimizationAndCompressUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadRstOptimizationAndCompressUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _jpegCompressValue: int, _flagborder: int) -> int:
        return LoadRstOptimizationAndCompressUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _jpegCompressValue, _flagborder)


#    Оптимизировать файл растровой карты с возможным сжатием изображения и
#    созданием уменьшенной копии растра
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           -  идентификатор открытых данных
#    name           - имя файла растровой карты
#    newname        - имя файла оптимизированной растровой карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     1 - алгоритм сжатия LZW
#                     2 - алгоритм сжатия JPEG (для 24 битных растров)
#    jpegCompressValue - степень сжатия изображения растра по алгоритму JPEG
#                        имеет значение, если compressnumber присвоено значение 2
#                        (1-100, 1-максимальное сжатие, 100-сжатие без потери качества),
#                         рекомендуется значение 60.
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         не входящие в область, ограниченную рамкой
#    flagSaveCopy   - флаг сохранения копии исходного файла с именем #.~rw
#                     0 - не создавать копию исходного файла
#                     1 - создать копию исходного файла
# flag_CreateDuplicate- флаг создания уменьшенной копии растра
#                     0 - не создавать уменьшенную копию растра
#                     1 - создавать уменьшенную копию растра
# flag              - не используется. Должен быть равен 0.
#
#     Добавлен пересчет габаритов растра при обрезке изображения по
#     рамке растра (когда flagborder == 1).
#    При ошибке возвращает ноль

    
    LoadRstOptimizationWithSurveyImageUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstOptimizationWithSurveyImageUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadRstOptimizationWithSurveyImageUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _jpegCompressValue: int, _flagborder: int, _flagSaveCopy: int, _flag_CreateDuplicate: int, _flag: int) -> int:
        return LoadRstOptimizationWithSurveyImageUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _jpegCompressValue, _flagborder, _flagSaveCopy, _flag_CreateDuplicate, _flag)

    LoadRstOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadRstOptimizationPro(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _jpegCompressValue: int, _flagborder: int, _flagSaveCopy: int, _flag_CreateDuplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return LoadRstOptimizationPro_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _jpegCompressValue, _flagborder, _flagSaveCopy, _flag_CreateDuplicate, _callevent, _parm)


#                       УСТАРЕВШАЯ ФУНКЦИЯ
#    Оптимизировать файл растровой карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           -  идентификатор открытых данных
#    name           - имя файла растровой карты
#    newname        - имя файла оптимизированной растровой карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     1 - алгоритм сжатия LZW
#                     2 - алгоритм сжатия JPEG (для 24 битных растров)
#    jpegCompressValue - степень сжатия изображения растра по алгоритму JPEG
#                        имеет значение, если compressnumber присвоено значение 2
#                        (1-100, 1-максимальное сжатие, 100-сжатие без потери качества),
#                         рекомендуется значение 60.
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#     Добавлен пересчет габаритов растра при обрезке изображения по
#     рамке растра (когда flagborder == 1).
#    При ошибке возвращает ноль

    

#    Оптимизировать файл растровой карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           -  идентификатор открытых данных
#    name           - имя файла растровой карты
#    newname        - имя файла оптимизированной растровой карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     1 - алгоритм сжатия LZW
#    flagborder     - флаг использования рамки растровой карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#     Добавлен пересчет габаритов растра при обрезке изображения по
#     рамке растра (когда flagborder == 1).
#    При ошибке возвращает ноль

    
    LoadRstOptimizationExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstOptimizationExUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadRstOptimizationExUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadRstOptimizationExUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Оптимизировать файл матричной карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    name           - имя файла матричной карты
#    newname        - имя файла оптимизированной матричной карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы
#    flagborder     - флаг использования рамки матричной карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMtrOptimizationUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtrOptimizationUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadMtrOptimizationUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadMtrOptimizationUn_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Оптимизировать файл матричной карты с возможным сжатием изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           -  идентификатор открытых данных
#    name           - имя файла матричной карты
#    newname        - имя файла оптимизированной матричной карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы
#    flagborder     - флаг использования рамки матричной карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#     Добавлен пересчет габаритов матричной карты при обрезке изображения по
#     рамке матричной карты (когда flagborder == 1).
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMtrOptimizationExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtrOptimizationExUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadMtrOptimizationExUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadMtrOptimizationExUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Оптимизировать файл матрицы высот с возможным сжатием изображения и
#    созданием уменьшенной копии изображения
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           - идентификатор открытых данных
#    name           - имя файла матрицы высот
#    newname        - имя файла оптимизированной матрицы высот
#    compressnumber - номер алгоритма сжатия блоков
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы
#    flagborder     - флаг использования рамки матрицы высот
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         не входящие в область, ограниченную рамкой
# flag_CreateDuplicate- флаг создания уменьшенной копии
#                     0 - не создавать уменьшенную копию
#                     1 - создавать уменьшенную копию
# flag              - не используется. Должен быть равен 0.
#
#     Добавлен пересчет габаритов матрицы высот при обрезке изображения по
#     рамке матрицы высот (когда flagborder == 1).
#    При ошибке возвращает ноль

    
    LoadMtrOptimizationWithSurveyImageUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtrOptimizationWithSurveyImageUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadMtrOptimizationWithSurveyImageUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flag_CreateDuplicate: int, _flag: int) -> int:
        return LoadMtrOptimizationWithSurveyImageUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flag_CreateDuplicate, _flag)

    LoadMtrOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtrOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadMtrOptimizationPro(_handle: maptype.HMESSAGE, _hMap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flagSaveCopy: int, _flag_CreateDuplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return LoadMtrOptimizationPro_t (_handle, _hMap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flagSaveCopy, _flag_CreateDuplicate, _callevent, _parm)


#    Оптимизировать файл матрицы качества MTQ с возможным сжатием изображения и
#    созданием уменьшенной копии изображения
#
#    ВНИМАНИЕ: сжатие может быть применено к матрицам с размером элемента в 4 байта
#
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           - идентификатор открытых данных
#    name           - имя файла матрицы качества MTQ
#    newname        - имя файла оптимизированной матрицы качества MTQ
#    compressnumber - номер алгоритма сжатия блоков
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы
#    flagborder     - флаг использования рамки матрицы качества MTQ
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         не входящие в область, ограниченную рамкой
# flag_CreateDuplicate- флаг создания уменьшенной копии
#                     0 - не создавать уменьшенную копию
#                     1 - создавать уменьшенную копию
# flag              - не используется. Должен быть равен 0.
#
#     Добавлен пересчет габаритов матрицы качества MTQ при обрезке изображения по
#     рамке матрицы качества MTQ (когда flagborder == 1).
#    При ошибке возвращает ноль

    
    LoadMtqOptimizationWithSurveyImageUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtqOptimizationWithSurveyImageUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def LoadMtqOptimizationWithSurveyImageUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flag_CreateDuplicate: int, _flag: int) -> int:
        return LoadMtqOptimizationWithSurveyImageUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flag_CreateDuplicate, _flag)

    picexMtqOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMtqOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexMtqOptimizationPro(_handle: maptype.HMESSAGE, _hMap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flagSaveCopy: int, _flag_CreateDuplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return picexMtqOptimizationPro_t (_handle, _hMap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flagSaveCopy, _flag_CreateDuplicate, _callevent, _parm)


#    Оптимизировать файл матрицы качества MTQ с возможным сжатием изображения
#    ВНИМАНИЕ: сжатие может быть применено к матрицам с размером элемента в 4 байта
#    hmap           - идентификатор открытых данных
#    handle         - диалог визуального сопровождения процесса обработки.
#    name           - имя файла матрицы качества
#    newname        - имя файла оптимизированной матрицы качества
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы качества
#    flagborder     - флаг использования рамки матрицы качества
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#     Добавлен пересчет габаритов матрицы качества при обрезке изображения по
#     рамке матрицы качества (когда flagborder == 1).
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMtqOptimizationExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtqOptimizationExUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadMtqOptimizationExUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadMtqOptimizationExUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Оптимизировать файл матрицы качества MTQ с возможным сжатием изображения
#    ВНИМАНИЕ: сжатие может быть применено к матрицам с размером элемента в 4 байта
#    handle         - диалог визуального сопровождения процесса обработки.
#    name           - имя файла матричной карты
#    newname        - имя файла оптимизированной матричной карты
#    compressnumber - номер алгоритма сжатия блоков изображения
#                     0 - не использовать сжатие
#                     32 - алгоритм сжатия матрицы
#    flagborder     - флаг использования рамки матричной карты
#                     0 - включать в формируемый файл все блоки изображения
#                     1 - не включать в формируемый файл блоки изображения
#                         невходящие в область, ограниченную рамкой
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadMtqOptimizationUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadMtqOptimizationUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def LoadMtqOptimizationUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int) -> int:
        return LoadMtqOptimizationUn_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder)


#    Вырезать изображение матрицы по прямоугольной области, заданной в метрах
#    map           - карта, содержащая векторные данные;
#    handle        - диалог визуального сопровождения процесса обработки.
#    rstInputName  - имя файла матрицы;
#    rstOutputName - имя файла формируемой матрицы;
#    frame         - габариты вырезаемой прямоугольной области(в метрах)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadCutOfMtqByFrameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadCutOfMtqByFrameUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def LoadCutOfMtqByFrameUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _mtqInputName: mapsyst.WTEXT, _mtqOutputName: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        return LoadCutOfMtqByFrameUn_t (_map, _handle, _mtqInputName.buffer(), _mtqOutputName.buffer(), _frame)


#    Трансформирование матрицы качеств
# (вычисление коэффициентов пересчета координат методом наименьших квадратов)
#
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap      - идентификатор открытых данных
#   parm      - параметры прикладной задачи;
#   namein    - имя исходноЙ матрицы качеств(maptype.MAX_PATH_LONG)
#   nameout   - имя выходной матрицы качеств(sizeNameOut);
#               в случае не заданного или совпадающего с исходным выходного имени,
#               будет создана копия исходной матрицы - <имя_исходной_матрицы>~.mtq;
#               результат будет записан в исходный файл;
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек.
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,

    MtqTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'MtqTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def MtqTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _sizeNameOut: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return MtqTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _sizeNameOut, _count, _fact, _teor)


#    Поворот растровой карты
#    handle         - диалог визуального сопровождения процесса обработки.
#    hmap           - идентификатор открытых данных
#    name           - имя файла растровой карты
#    newname        - имя файла растровой карты с зеркальным изображением
#    mirrortype     - тип обработки
#                     (0- Получение зеркального изображения растровой карты
#                           относитльно вертикальной оси )
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    
    LoadRstMirrorUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstMirrorUn', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def LoadRstMirrorUn(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _mirrortype: int) -> int:
        return LoadRstMirrorUn_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _mirrortype)


#    Сохранить изображение уменьшенной копии растровой карты как самостоятельный растр
#    hmap          - идентификатор открытых данных
#    handle        - диалог визуального сопровождения процесса обработки.
#    rstInputName  - имя файла растровой карты;
#    rstOutputName - имя файла формируемой растровой карты;
#    imageNumber   - номер обзорного изображения
#                    (0 - основное изображение,
#                     1,2,3 - производные изображения)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    LoadRstDuplicateUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadRstDuplicateUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def LoadRstDuplicateUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _rstInputName: mapsyst.WTEXT, _rstOutputName: mapsyst.WTEXT, _imageNumber: int) -> int:
        return LoadRstDuplicateUn_t (_map, _handle, _rstInputName.buffer(), _rstOutputName.buffer(), _imageNumber)

    

#    Сохранить уровень уменьшенной копии матрицы в самостоятельный файл
#    handle        - диалог визуального сопровождения процесса обработки.
#    inputName     - имя файла исходной матрицы
#    outputName    - имя файла выходной матрицы
#    levelNumber   - номер обзорного изображения
#                    (0 - основное изображение,
#                     1,2,3 - производные изображения)
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexSaveMtrDuplicateUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveMtrDuplicateUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveMtrDuplicateUn(_handle: maptype.HMESSAGE, _inputName: mapsyst.WTEXT, _outputName: mapsyst.WTEXT, _levelNumber: int) -> int:
        return picexSaveMtrDuplicateUn_t (_handle, _inputName.buffer(), _outputName.buffer(), _levelNumber)


#    Поворот растра вокруг точки NullPoint на угол Angle
#    hmap       - идентификатор открытых данных
#    RstNumber  - номер исходного растра в цепочке растров
#    NameRstIn  - имя исходного растра;
#    NameRstOut - имя выходного растра;
#    NullPoint  - координаты точки поворота в элементах растра;
#    Angle      - угол поворота (в радианах);
#    handle     - диалог визуального сопровождения процесса обработки.

    
    RstRotatingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RstRotatingUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, maptype.DOUBLEPOINT, ctypes.c_double, maptype.HMESSAGE)
    def RstRotatingUn(_hmap: maptype.HMAP, _RstNumber: int, _NameRstIn: mapsyst.WTEXT, _NameRstOut: mapsyst.WTEXT, _NullPoint: maptype.DOUBLEPOINT, _Angle: float, _Handle: maptype.HMESSAGE) -> int:
        return RstRotatingUn_t (_hmap, _RstNumber, _NameRstIn.buffer(), _NameRstOut.buffer(), _NullPoint, _Angle, _Handle)


#    Поворот растра вокруг точки NullPoint на угол Angle
#    hmap       - идентификатор открытых данных
#    RstNumber  - номер исходного растра в цепочке растров
#    NameRstIn  - имя исходного растра;
#    NameRstOut - имя выходного растра;
#    NullPoint  - координаты точки поворота в метрах на местности;
#    Angle      - угол поворота (в радианах);
#    handle     - диалог визуального сопровождения процесса обработки.

    
    RstPlaneRotatingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RstPlaneRotatingUn', maptype.HMAP, ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, maptype.DOUBLEPOINT, ctypes.c_double, maptype.HMESSAGE)
    def RstPlaneRotatingUn(_hmap: maptype.HMAP, _RstNumber: int, _NameRstIn: mapsyst.WTEXT, _NameRstOut: mapsyst.WTEXT, _NullPoint: maptype.DOUBLEPOINT, _Angle: float, _handle: maptype.HMESSAGE) -> int:
        return RstPlaneRotatingUn_t (_hmap, _RstNumber, _NameRstIn.buffer(), _NameRstOut.buffer(), _NullPoint, _Angle, _handle)


# Привязка растра с масштабированием по двум точкам
# Внимание: Возможна устанавка отличных друг от друга размеров пикселя по X и по Y
# ВАЖНО:
# Если размеры пикселя по X и по Y отличаются друг от друга, то в растр
# устанавливается версия  1.04 (0x0104).
# Растры версии 1.04 открываются в ПО начинаяя с 11-ой версии.
# hmap        - идентификатор открытых данных
# rswName     - имя файла растра
# pointMet1   - Координаты первой точки  в метрах
# pointMet1   - Координаты первой точки в метрах
# pointMet2   - Координаты второй точки  в метрах
# pointMet2   - Координаты второй точки в метрах
# message     - флаг на выдачу сообщений (0\1)
# При ошибке возвращает ноль

    
    AttachRswWithScalingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'AttachRswWithScalingUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def AttachRswWithScalingUn(_hmap: maptype.HMAP, _rswName: mapsyst.WTEXT, _pointMet1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMetNew1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMet2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMetNew2: ctypes.POINTER(maptype.DOUBLEPOINT), _message: int) -> int:
        return AttachRswWithScalingUn_t (_hmap, _rswName.buffer(), _pointMet1, _pointMetNew1, _pointMet2, _pointMetNew2, _message)


# Привязка растра с масштабированием по двум точкам
# Внимание: Устанавливается одинаковый размер пикселя по X и по Y
# hmap        - идентификатор открытых данных
# rswName     - имя файла растра
# pointMet1   - Координаты первой точки  в метрах
# pointMet1   - Координаты первой точки в метрах
# pointMet2   - Координаты второй точки  в метрах
# pointMet2   - Координаты второй точки в метрах
# message     - флаг на выдачу сообщений (0\1)
# При ошибке возвращает ноль

    
    AttachRswWithScalingExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'AttachRswWithScalingExUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def AttachRswWithScalingExUn(_hmap: maptype.HMAP, _rswName: mapsyst.WTEXT, _pointMet1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMetNew1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMet2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointMetNew2: ctypes.POINTER(maptype.DOUBLEPOINT), _message: int) -> int:
        return AttachRswWithScalingExUn_t (_hmap, _rswName.buffer(), _pointMet1, _pointMetNew1, _pointMet2, _pointMetNew2, _message)


# Привязка растра с масштабированием и поворотом по двум точкам
# hmap          - идентификатор открытых данных
# handle        - дескриптор окна диалога для обработки сообщений о ходе процесса
# rswname       - путь к файлу растра, который трансформируется
# pointmet1     - исходные координаты первой точки в метрах
# pointmetnew1  - желаемые координаты первой точки в метрах
# pointmet2     - исходные координаты второй точки в метрах
# pointmet2     - желаемые координаты второй точки в метрах
# message       - флаг на выдачу сообщений (0\1) в процессе трансформирования
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#       WPARAM - текущее состояние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль

    
    AttachRswWithScalingAndRotationUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'AttachRswWithScalingAndRotationUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def AttachRswWithScalingAndRotationUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rswname: mapsyst.WTEXT, _pointmet1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmet2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew2: ctypes.POINTER(maptype.DOUBLEPOINT), _message: int) -> int:
        return AttachRswWithScalingAndRotationUn_t (_hmap, _handle, _rswname.buffer(), _pointmet1, _pointmetnew1, _pointmet2, _pointmetnew2, _message)


# Привязка растра с масштабированием и поворотом по двум точкам
# hmap        - идентификатор открытых данных
# handle      - диалог визуального сопровождения процесса обработки.
# rswnamein   - имя исходного файла растра
# rswNameOut  - имя выходного файла растра (размер строки д.б. не менее maptype.MAX_PATH_LONG байт);
#               в случае не заданного или совпадающего с исходным выходного имени,
#               будет создана копия исходного растра с именем вида - <имя_исходного_растра>~.rsw;
#               результат будет записан вместо исходного файла;
# pointmet1   - Координаты первой точки  в метрах
# pointmet1   - Координаты первой точки в метрах
# pointmet2   - Координаты второй точки  в метрах
# pointmet2   - Координаты второй точки в метрах
# message     - флаг на выдачу сообщений (0\1)
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#       WPARAM - текущее состояние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль

    

# sizeNameIn  - размер строки rswName в байтах
# sizeNameOut - размер строки rswNameOut в байтах

    AttachRswWithScalingAndRotationExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'AttachRswWithScalingAndRotationExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def AttachRswWithScalingAndRotationExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rswName: mapsyst.WTEXT, _sizeNameIn: int, _rswNameOut: mapsyst.WTEXT, _sizeNameOut: int, _pointmet1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmet2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew2: ctypes.POINTER(maptype.DOUBLEPOINT), _message: int) -> int:
        return AttachRswWithScalingAndRotationExUn_t (_hmap, _handle, _rswName.buffer(), _sizeNameIn, _rswNameOut.buffer(), _sizeNameOut, _pointmet1, _pointmetnew1, _pointmet2, _pointmetnew2, _message)


#    Трансформирование растра
# (вычисление коэффициентов пересчета координат методом наименьших квадратов)
#
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap      - идентификатор открытых данных
#   map       - карта,содержащая векторные данные;
#   parm      - параметры прикладной задачи;
#   namein    - имя исходного растра (maptype.MAX_PATH_LONG)
#   nameout   - имя выходного растра (размер выделенной памяти д.б. не менее maptype.MAX_PATH_LONG символов);
#               в случае не заданного или совпадающего с исходным выходного имени,
#               будет создана копия исходного растра - <имя_исходного_растра>~.rsw;
#               результат будет записан в исходный файл;
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек (не меньше 4-х).
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,

    

#   sizeNameOut - размер выделенной памяти для nameout в байтах

    RswTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def RswTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _sizeNameOut: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return RswTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _sizeNameOut, _count, _fact, _teor)


#   Трансформирование растра по рамке листа карты
#
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap      - идентификатор открытых данных
#   parm      - параметры прикладной задачи;
#   namein    - имя исходного растра;
#   nameout   - имя выходного растра;
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек (не меньше 4-х).
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,

    
    RswTransformingByBorderMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswTransformingByBorderMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def RswTransformingByBorderMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        return RswTransformingByBorderMethodUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _count, _fact, _teor)


#   Трансформирование растра по рамке листа карты
#   (нелинейное трансформирование)
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap      - идентификатор открытых данных
#   parm      - параметры прикладной задачи;
#   namein    - имя исходного растра;
#   nameout   - имя выходного растра;
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек (не меньше 4-х).
#   flagBorder- 0 - Установить рамку растра по теоретическим координатам (например - по рамке номенклатурного листа)
#               1 - Установить рамку растра по пересчитанным габаритам исходного растра
#               Если исходный растр отображается по рамке, flagBorder игнорируется.
#               Рамка перессчитывается и устанавливается в выходной растр.
#   colorTransparent  - указатель на неотображаемый цвет
#               (если colorTransparent != 0, то в качестве цвета фона используется цвет из colorTransparent.
#                Отображение цвета colorTransparent отключается)
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,

    
    RswTransformingByBorderMethodExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswTransformingByBorderMethodExUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(maptype.COLORREF))
    def RswTransformingByBorderMethodExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT), _flagBorder: int, _colorTransparent: ctypes.POINTER(maptype.COLORREF)) -> int:
        return RswTransformingByBorderMethodExUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _count, _fact, _teor, _flagBorder, _colorTransparent)


#   Трансформирование растра по рамке листа карты
#   (нелинейное трансформирование)
#   handle    - диалог визуального сопровождения процесса обработки;
#   hmap      - идентификатор открытых данных
#   parm      - параметры прикладной задачи;
#   namein    - имя исходного растра;
#   nameout   - имя выходного растра;
#   fact      - исходные координаты опоры;
#   teor      - желаемые координаты опоры;
#   count     - количество опорных точек (не меньше 4-х).
#   colorTransparent  - указатель на неотображаемый цвет
#                       (если colorTransparent != 0, то в качестве цвета фона
#                        используется цвет из colorTransparent.
#                        Отображение цвета colorTransparent отключается)
#   flagCutting    - флаг обрезки изображения выходного растра по рамке растра.
#                    Значение флага принимается во внимание при установленной рамке в растр (см. flagBorder)
#   flagDuplicate  - флаг создания уменьшенной копии изображения выходного растра (0/1)
#   flagBorderNew  - 0 - Не устанавливать рамку выходного растра
#                    1 - Установить рамку выходного растра по теоретическим координатам
#                        (например - по объекту <Рамка номенклатурного листа карты>) /
#                    2 - Установить рамку выходного растра по рамке исходного раста.
#                        Если в исходном растре рамка не установлена, то будет установлена
#                        рамка растра по пересчитанным габаритам исходного растра
#                    3 - Установить рамку выходного растра по пересчитанным габаритам исходного растра
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,

    
    RswTransformingWithBorderSettingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswTransformingWithBorderSettingUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def RswTransformingWithBorderSettingUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT), _colorTransparent: ctypes.POINTER(maptype.COLORREF), _flagCutting: int, _flagDuplicate: int, _flagBorderNew: int) -> int:
        return RswTransformingWithBorderSettingUn_t (_hmap, _handle, _parm, _namein.buffer(), _nameout.buffer(), _count, _fact, _teor, _colorTransparent, _flagCutting, _flagDuplicate, _flagBorderNew)


# Преобразование растра к заданной проекции
#   handle  - диалог визуального сопровождения процесса обработки.
#   namein  - имя исходного растра;
#   nameout - имя выходного растра;
#   mapreg  - адрес структуры с данными о заданной проекции
#             (описание структуры MAPREGISTEREX см в mapcreate.h);
#
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения:
#   -  (WM_PROGRESSBAR) Извещение об изменении состояния процесса
#      WPARAM - текущее состояние процесса в процентах (0% - 100%)
#      Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
# При ошибке возвращает ноль,
# код ошибки возвращается функцией picexGetLastError() (коды ошибок см. maperr.rh)

    
    RswProjectionReformingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswProjectionReformingUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def RswProjectionReformingUn(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        return RswProjectionReformingUn_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg)


# Преобразование растра к заданной проекции
#   handle  - диалог визуального сопровождения процесса обработки.
#   namein  - имя исходного растра;
#   nameout - имя выходного растра;
#   mapreg  - адрес структуры с данными о заданной проекции
#             (описание структуры MAPREGISTEREX см в mapcreate.h);
#   datum   - параметры пересчета геодезических координат с заданного эллипсоида
#             на эллипсоид WGS-84 (может быть ноль),
#   ellparam - параметры пользовательского эллипсоида (может быть ноль).
#   ttype    - тип локального преобразования координат (см. TRANSFORMTYPE в mapcreat.h) или 0
#   tparm    - параметры локального преобразования координат (см. mapcreat.h)
#   Диалогу визуального сопровождения процесса обработки посылаются сообщения WM_PROGRESSBAR/WM_PROGRESSBARUN:
#   Извещение об изменении состояния процесса, WPARAM - текущее состояние процесса в процентах (0% - 100%)
#   Если функция-отклик возвращает WM_PROGRESSBAR/WM_PROGRESSBARUN, то процесс завершается.
#   hEvent - адрес функции обратного вызова для уведомлении о процессе
#   eventparam - параметры функции обратного вызова
# При ошибке возвращает ноль,
# код ошибки возвращается функцией picexGetLastError() (коды ошибок см. maperr.rh)

    RswProjectionReformingEvent_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswProjectionReformingEvent', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def RswProjectionReformingEvent(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _hEvent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return RswProjectionReformingEvent_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm, _hEvent, _eventparam)

    
    RswProjectionReformingExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswProjectionReformingExUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def RswProjectionReformingExUn(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        return RswProjectionReformingExUn_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam)

    RswProjectionReformingPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'RswProjectionReformingPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_int, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def RswProjectionReformingPro(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        return RswProjectionReformingPro_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm)


# Возвращает код последней ошибки (коды ошибок см. maperr.rh)
# В случае отсутствия ошибки возвращает ноль

    picexGetLastError_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetLastError')
    def picexGetLastError() -> int:
        return picexGetLastError_t ()


# Создать GIF-файл с размещением в памяти
#   palette    - указатель на палитру
#   colorcount - число цветов палитры (от 2 до 256)
#   width      - ширина изображения (от 1 до 65535)
#   height     - высота изображения (от 1 до 65535)
#   in         - указатель на входные данные
#   sizein     - размер входных данных (в байтах)
#   out        - указатель на выходной буфер
#   sizeout    - размер выходного буфера (в байтах)
#                (минимальный размер = sizein + 1000)
# Возвращает размер буфера, содержащего GIF-файл (в байтах)
# При ошибке возвращает 0
# Входные данные должны содержать 8-битное изображение с нормальным
# расположением строк (сверху-вниз) без байтов выравнивания в строке.
# В качестве входных данных может быть использовано изображение
# карты, полученное при помощи функции mapPaintToImage (mapapi.h)

    picexCreateGif_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCreateGif', ctypes.POINTER(maptype.RGBQUAD), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def picexCreateGif(_palette: ctypes.POINTER(maptype.RGBQUAD), _colorcount: int, _width: int, _height: int, _in: ctypes.POINTER(ctypes.c_byte), _sizein: int, _out: ctypes.POINTER(ctypes.c_byte), _sizeout: int) -> int:
        return picexCreateGif_t (_palette, _colorcount, _width, _height, _in, _sizein, _out, _sizeout)


# Создать GIF-файл с размещением на диске
#   name       - имя GIF-файла
#   palette    - указатель на палитру
#   colorcount - число цветов палитры (от 2 до 256)
#   width      - ширина изображения (от 1 до 65535)
#   height     - высота изображения (от 1 до 65535)
#   in         - указатель на входные данные
#   sizein     - размер входных данных (в байтах)
# Возвращает размер GIF-файла (в байтах)
# При ошибке возвращает 0
# Входные данные должны содержать 8-битное изображение с нормальным
# расположением строк (сверху-вниз) без байтов выравнивания в строке.
# В качестве входных данных может быть использовано изображение
# карты, полученное при помощи функции mapPaintToImage (mapapi.h)

    
    picexCreateGifFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCreateGifFileUn', maptype.PWCHAR, ctypes.POINTER(maptype.RGBQUAD), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte), ctypes.c_int)
    def picexCreateGifFileUn(_name: mapsyst.WTEXT, _palette: ctypes.POINTER(maptype.RGBQUAD), _colorcount: int, _width: int, _height: int, _in: ctypes.POINTER(ctypes.c_byte), _sizein: int) -> int:
        return picexCreateGifFileUn_t (_name.buffer(), _palette, _colorcount, _width, _height, _in, _sizein)


# Загрузка изображения в формате RGBA(для текстуры OpenGL) из BMP-файла
#          c обрезкой (высота и ширина не более 512 и кратны степени 2)
#    Вход: nameBmp - имя исходного Bmp-файла;
#            image - адрес области записи получаемого изображения;
#             size - размер этой области в байтах;
#      reth и retv - высота и ширина полученного изображения;
#        sizeimage - заполняемый данной функцией размер области, необходимой
#                    для записи получаемого изображения.
#    Возвращаемое значение:
#         0 - в случае ошибки (или при нехватке памяти для получаемого
#             изображения см. sizeimage);
#         1 - в случае успешного получения изображения.

    
    LoadBmpToImage32WithCutUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadBmpToImage32WithCutUn', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def LoadBmpToImage32WithCutUn(_bmpname: mapsyst.WTEXT, _image: ctypes.c_char_p, _size: int, _reth: ctypes.POINTER(ctypes.c_int), _retw: ctypes.POINTER(ctypes.c_int), _sizeimage: ctypes.POINTER(ctypes.c_int)) -> int:
        return LoadBmpToImage32WithCutUn_t (_bmpname.buffer(), _image, _size, _reth, _retw, _sizeimage)


# Загрузка изображения из памяти в BMP-файл
#    Вход: nameBmp - имя получаемого Bmp-файла;
#            image - адрес области с изображением для записи;
#   width и height - ширина и высота изображения;
#      elementsize - размер элемента изображения (в битах).
#    Возвращаемое значение:
#         0 - в случае ошибки;
#         1 - в случае успешного получения Bmp-файла изображения.

    
    LoadImageToBmpUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadImageToBmpUn', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def LoadImageToBmpUn(_bmpname: mapsyst.WTEXT, _image: ctypes.c_char_p, _width: int, _height: int, _elementsize: int) -> int:
        return LoadImageToBmpUn_t (_bmpname.buffer(), _image, _width, _height, _elementsize)


# Определить координаты точки фотографирования из файла JPEG
# Координаты
# hmap    - идентификатор открытых данных
# handle  - диалог визуального сопровождения процесса обработки.
# parm    - параметры прикладной задачи
# namein  - имя файла JPEG
# b,l     - координаты точки фотографирования (заполняется функцией)
# height  - высота точки фотографирования (заполняется функцией)
# mapreg  - адрес структуры с данными о заданной проекции (заполняется функцией)
#           (описание структуры MAPREGISTEREX см в mapcreate.h)
# ellipsoid - параметры эллипсоида (заполняется функцией)
# datum   - параметры пересчета геодезических координат с заданного эллипсоида
#           на эллипсоид WGS-84, для координат точки фотографирования (заполняется функцией)
# Возвращает: 1 - в случае успешного определения координат точки фотографирования
#            -1 - структура файла namein не соотвеотсут формату JPEG
#            -2 - в файле namein отсутствует маркер APP1, предназначенный для хранения метаданных
#            -3 - в файле namein найден маркер APP1, но координаты точки фотографирования не обнаружены
#
# При ошибке возвращает ноль

    
    LoadJpegGpsPointUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadJpegGpsPointUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.POINTER(maptype.SIGNDEGREE), ctypes.POINTER(maptype.SIGNDEGREE), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def LoadJpegGpsPointUn(_map: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _b: ctypes.POINTER(maptype.SIGNDEGREE), _l: ctypes.POINTER(maptype.SIGNDEGREE), _height: ctypes.POINTER(ctypes.c_double), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return LoadJpegGpsPointUn_t (_map, _handle, _parm, _namein.buffer(), _b, _l, _height, _mapreg, _ellipsoid, _datum)


# Определить параметры файла JPEG с тегами EXIF
# map     - карта,содержащая векторные данные
# handle  - диалог визуального сопровождения процесса обработки.
# parm    - параметры прикладной задачи
# namein  - имя файла JPEG
# exifParam-указатель на структуру EXIFPARAM (структура заполняется функцией)
# Возвращает: 1 - в случае успешного определения координат точки фотографирования
#            -1 - структура файла namein не соотвеотсут формату JPEG
#            -2 - в файле namein отсутствует маркер APP1, предназначенный для хранения метаданных
#            -3 - в файле namein найден маркер APP1, но координаты точки фотографирования не обнаружены
#
# При ошибке возвращает ноль

#   LoadJpegExifParameters_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadJpegExifParameters', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.POINTER(EXIFPARAM))
#   def LoadJpegExifParameters(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: ctypes.c_char_p, _exifParam: ctypes.POINTER(EXIFPARAM)) -> int:
#       return LoadJpegExifParameters_t (_hmap, _handle, _parm, _namein, _exifParam)

#   LoadJpegExifParametersUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'LoadJpegExifParametersUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.POINTER(EXIFPARAM))
#   def LoadJpegExifParametersUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namein: mapsyst.WTEXT, _exifParam: ctypes.POINTER(EXIFPARAM)) -> int:
#       return LoadJpegExifParametersUn_t (_hmap, _handle, _parm, _namein.buffer(), _exifParam)


# Запросить разрешение изображения из файлов форматов TIFF(GeoTIFF), BMP, PCX, JPEG
# name - имя файла (#.tif;#.bmp;#.pcx;#.jpg)
# precisionByWidth  - указатель на разрешение по горизонтали (заполняется функцией)
# precisionByHeight - указатель на разрешение по вертикали (заполняется функцией)
#                     значение разрешения заносится в выходные
#                     параметры precisionByWidth и precisionByHeight
#                     в точках на дюйм.
#    flagMessage    - параметр не используется
#                     Управление диагностическими сообщениями осуществляется
#                     вызовом функции mapMessageEnable.
#                     Если mapIsMessageEnable() возвращает 0, то
#                     диагностические сообщения не выдаются.
#
# Функция возвращает следующие значения:
#   1 - разрешение изображения определено и записано в выходные параметры precisionByWidth и precisionByHeight
#  -1 - разрешение изображения в файле обнаружить не удалось
# При ошибке возвращает 0

    
    picexGetPrecisionFromImageFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetPrecisionFromImageFileUn', maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)
    def picexGetPrecisionFromImageFileUn(_name: mapsyst.WTEXT, _precisionByWidth: ctypes.POINTER(ctypes.c_double), _precisionByHeight: ctypes.POINTER(ctypes.c_double), _flagMessage: int) -> int:
        return picexGetPrecisionFromImageFileUn_t (_name.buffer(), _precisionByWidth, _precisionByHeight, _flagMessage)


# Установить разрешение изображения в файл формата JPEG
# name - имя файла JPEG
# valueHorizontal   - разрешение по горизонтали
# valueVertical     - разрешение по вертикали
# precisionUnit     - единицы измерения разрешения
#                     0 - безразмерный (коэффициент),
#                     1 - точки на дюйм,
#                     2 - точки на сантиметр.
# Управление диагностическими сообщениями функции осуществляется
# предварительным вызовом функции mapMessageEnable.
# Если mapIsMessageEnable() возвращает 0, то диагностические сообщения
# в теле функции не выдаются.
#
# При ошибке функциz возвращает 0

    picexSetJPEGPrecisionUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetJPEGPrecisionUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexSetJPEGPrecisionUn(_name: mapsyst.WTEXT, _valueHorizontal: int, _valueVertical: int, _precisionUnit: int) -> int:
        return picexSetJPEGPrecisionUn_t (_name.buffer(), _valueHorizontal, _valueVertical, _precisionUnit)


# Запросить параметры растра (матрицы) - координаты габаритов изображения,
# размеры пикселя, код EPSG
# fileName        - имя файла (RSW, MTW, MTL, MTQ, BMP, TIFF, IMG, PNG, GIF)
# points          - указатель на массив из 4-х точек (заполняется функцией
#                   координатами габаритов изображения в радианах WGS-84)
# countPoint      - количество элементов массива, размещенного по адресу points
#                   (параметр должен быть равен 4)
# meterInElementX - указатель для записи значения размера элемента по X
#                   При обнаружении данных в исходном графическом файле, или в
#                   файле привязки растрового изображения функция заполняет поле
# meterInElementY - указатель для записи значения размера элемента по Y
#                   При обнаружении данных в исходном графическом файле, или в
#                   файле привязки растрового изображения функция заполняет поле
# codeEPSG        - указатель для записи значения кода EPSG
#
#    При ошибке возвращает ноль

    picexGetImageInfoByNameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetImageInfoByNameUn', maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def picexGetImageInfoByNameUn(_fileName: mapsyst.WTEXT, _points: ctypes.POINTER(maptype.DOUBLEPOINT), _countPoint: int, _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _codeEPSG: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexGetImageInfoByNameUn_t (_fileName.buffer(), _points, _countPoint, _meterInElementX, _meterInElementY, _codeEPSG)


# Запросить данные о проекции растра (матрицы)
# fileName        - имя файла (RSW, MTW, MTL, MTQ, BMP, TIFF, IMG, PNG, GIF)
# mapregister - адрес структуры MAPREGISTEREX.
# Структурa MAPREGISTEREX описанa в mapcreat.h
# ellipsoidparam - адрес структуры, в которой будут размещены
# параметры эллипсоида
# Структурa ELLIPSOIDPARAM описанa в mapcreat.h
# datumparam - адрес структуры, в которой будут размещены
# коэффициенты трансформирования геодезических координат
# Структурa DATUMPARAM описанa в mapcreat.h
# При ошибке возвращает ноль

    picexGetImageProjectionDataByNameUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetImageProjectionDataByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def picexGetImageProjectionDataByNameUn(_fileName: mapsyst.WTEXT, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        return picexGetImageProjectionDataByNameUn_t (_fileName.buffer(), _mapregister, _ellipsoidparam, _datumparam)


# Функция создает обзорное изображение растра(RSW, TIFF, JPEG, IMG, PNG, GIF, BMP, PCX)
# и матрицы(MTW, MTL, MTQ)  и записывает его в файл форматов (RSW, TIFF, JPEG, BMP, PNG).
# Глубина обзорного изображения - 24 бит на пиксель.
# handle - диалог визуального сопровождения процесса обработки
# inputFileName   - имя входного файла
# outputFileName  - имя выходного файла обзорного изображения
# width и height  - размеры обзорного изображения
# flagMessage     - параметр не используется
#                   Управление диагностическими сообщениями осуществляется
#                   вызовом функции mapMessageEnable.
#                   Если mapIsMessageEnable() возвращает 0, то
#                   диагностические сообщения не выдаются.
# При ошибке функция возвращает ноль

    
    picexPaintDataToFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexPaintDataToFileUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexPaintDataToFileUn(_handle: maptype.HMESSAGE, _inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _width: int, _height: int, _messageEnable: int) -> int:
        return picexPaintDataToFileUn_t (_handle, _inputFileName.buffer(), _outputFileName.buffer(), _width, _height, _messageEnable)


# Импорт растровых данных в файл RSW
# handle - диалог визуального сопровождения процесса обработки
# srcname        - имя входного файла (TIF, IMG, PNG, GIF, JPG, BMP, PCX)
# rstname        - имя выходного файла (#.rsw)
# retcode        - код возврата
# Приоритет изъятия параметров привязки:
#   1. Содержимое соответствующих тегов файлов TIF, IMG
#   2. Файл привязки world.file
#   3. Файл привязки TAB (MapInfo)
# Функция ищет файл привязки рядом с исходным файлом srcname,
# перебирая по приоритету типы файлов.
# При ошибке возвращает ноль

    picexLoadRasterToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadRasterToRswUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int))
    def picexLoadRasterToRswUn(_handle: maptype.HMESSAGE, _srcname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _retcode: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexLoadRasterToRswUn_t (_handle, _srcname.buffer(), _rstname.buffer(), _retcode)


# Подобрать имя файла привязки по содержимому папки графического файла
# Сформировать имя файла параметров в зависимости от формата графического файла
# и типа файла привязки
# type              - тип файла привязки
# Значения параметра type:
#        1 - файл привязки world file
#        2 - TAB (MapInfo)
#        3 - MAP (OziExplorer)
#        4 - INI            - устаревший формат
#        5 - tpf (FOTOPLAN) - устаревший формат
#        6 - pln (TALKA)    - устаревший формат
# graphicName       - имя графического файла
# locationFilesName - указатель для размещения сформированного имени файла привязки
# size              - размер памяти в байтах строки locationFilesName (не менее maptype.MAX_PATH_LONG)

    picexMakeLocationFileName_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMakeLocationFileName', ctypes.c_int, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexMakeLocationFileName(_type: int, _graphicName: mapsyst.WTEXT, _locationFilesName: mapsyst.WTEXT, _size: int) -> int:
        return picexMakeLocationFileName_t (_type, _graphicName.buffer(), _locationFilesName.buffer(), _size)


# Запросить информацию о графическом файле

#   picexGetFileInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexGetFileInformationUn', maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION))
#   def picexGetFileInformationUn(_inputName: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION)) -> int:
#       return picexGetFileInformationUn_t (_inputName.buffer(), _information)


# Чтение и Анализ файлов настройки
# #.tab (MapInfo), #.map (OziExplorer), World File
# inputName         - имя графического файла
# rstIniName        - имя файла привязки #.tab, #.map, World File
# fileType          - тип файла привязки rstIniName
# Возможные значения параметра fileType:
#                     1 - файл привязки world file
#                     2 - TAB (MapInfo)
#                     3 - MAP (OziExplorer)
# param             - указатель на заполняемую структуру RASTERPARM
# При ошибке функция возвращает 0
# retCode - код возрата ошибки

#   picexReadParamFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexReadParamFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(RASTERPARM), ctypes.POINTER(ctypes.c_int))
#   def picexReadParamFile(_inputName: mapsyst.WTEXT, _rstIniName: mapsyst.WTEXT, _fileType: int, _param: ctypes.POINTER(RASTERPARM), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
#       return picexReadParamFile_t (_inputName.buffer(), _rstIniName.buffer(), _fileType, _param, _retCode)


# Чтение и Анализ файла привязки World File
# inputName  - имя графического файла
# rstIniName - имя файла привязки World File
# locationPoint   - приаязка растра
# meterInElementX - размер элемента по X
# meterInElementY - размер элемента по Y
# rasterPoint - Левый Нижний, Левый Верхний, Правый Верхний, Правый Нижний
# countPoint  - 4
# rasterPointTr - LT,RT,RB,LB;  массив заполняется, если flagTransformation == 1
# countPointTr  - 4,
# flagTransformation - флаг трансформирования по координатам rasterPointTr
# flagWorldFile_CoordinateInGradus - флаг записи координат в градусах
# retCode - код возрата ошибки

#   picexReadWorldFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexReadWorldFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(LOCATIONPOINT), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#   def picexReadWorldFile(_inputName: mapsyst.WTEXT, _rstIniName: mapsyst.WTEXT, _locationPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _rasterPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _countPoint: int, _rasterPointTr: ctypes.POINTER(LOCATIONPOINT), _countPointTr: int, _flagTransformation: ctypes.POINTER(ctypes.c_int), _flagWorldFile_CoordinateInGradus: ctypes.POINTER(ctypes.c_int), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
#       return picexReadWorldFile_t (_inputName.buffer(), _rstIniName.buffer(), _locationPoint, _meterInElementX, _meterInElementY, _rasterPoint, _countPoint, _rasterPointTr, _countPointTr, _flagTransformation, _flagWorldFile_CoordinateInGradus, _retCode)


# Запись файла привязки World File
# fileName        - имя файла привязки World File
# locationPoint   - координата центра верхней левой точки
# elementSizeX    - размер элемента по X
# elementSizeY    - размер элемента по Y
# flagMessage     - параметр не используется
#                   Управление диагностическими сообщениями осуществляется
#                   вызовом функции mapMessageEnable.
#                   Если mapIsMessageEnable() возвращает 0, то
#                   диагностические сообщения не выдаются.
#
# Возможна запись координат и размеров элемента в градусах в СК EPSG 4326
# При ошибке возвращает ноль

    picexWriteWorldFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexWriteWorldFile', maptype.PWCHAR, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)
    def picexWriteWorldFile(_fileName: mapsyst.WTEXT, _locationPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _elementSizeX: ctypes.POINTER(ctypes.c_double), _elementSizeY: ctypes.POINTER(ctypes.c_double), _flagMessage: int) -> int:
        return picexWriteWorldFile_t (_fileName.buffer(), _locationPoint, _elementSizeX, _elementSizeY, _flagMessage)


# Чтение и Анализ файла настройки #.tab (MapInfo)
# inputName         - имя графического файла
# rstIniName        - имя файла привязки #.tab
# mapreg            - параметры системы координат и проекции
# datum             - параметры пересчета с эллипсоида рабочей системы координат
#                     к WGS-84
# ellipsoid         - параметры пользовательского эллипсоида для рабочей
#                     системы координат
# flagMapRegisterEx - флаг заполнения параметров проекции из файла TAB
# locationPoint     - привязка растра
# meterInElementX   - размер элемента по X
# meterInElementY   - размер элемента по Y
#
# rasterPoint - Левый Нижний, Левый Верхний, Правый Верхний, Правый Нижний
# countPoint  - 4
#
# rasterPointTr - LT,RT,RB,LB;  массив заполняется, если flagTransformation == 1
# countPointTr  - 4,
# flagTransformation - флаг трансформирования по координатам rasterPointTr
#
# При ошибке функция возвращает 0
# retCode - код возрата ошибки

#   picexReadTabFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexReadTabFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.POINTER(LOCATIONPOINT), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#   def picexReadTabFile(_inputName: mapsyst.WTEXT, _rstIniName: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _flagMapRegisterEx: ctypes.POINTER(ctypes.c_int), _locationPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _meterInElementX: ctypes.POINTER(ctypes.c_double), _meterInElementY: ctypes.POINTER(ctypes.c_double), _rasterPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _countPoint: int, _rasterPointTr: ctypes.POINTER(LOCATIONPOINT), _countPointTr: int, _flagTransformation: ctypes.POINTER(ctypes.c_int), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
#       return picexReadTabFile_t (_inputName.buffer(), _rstIniName.buffer(), _mapreg, _ellipsoid, _datum, _flagMapRegisterEx, _locationPoint, _meterInElementX, _meterInElementY, _rasterPoint, _countPoint, _rasterPointTr, _countPointTr, _flagTransformation, _retCode)


# В файле настройки #.tab (MapInfo) запросить прозрачный цвет
# tabFileName          - имя файла привязки #.tab
# flagTransparentColor - флаг наличия прозрачного цвета в файле #.tab
# transparentColor     - значение прозрачного цвета в формате RGB (от 0 до 0x00FFFFFF)
#
# При ошибке функция возвращает 0
# retCode - код возрата ошибки

    picexGetTransparentColorFromTab_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetTransparentColorFromTab', maptype.PWCHAR, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_int))
    def picexGetTransparentColorFromTab(_tabFileName: mapsyst.WTEXT, _flagTransparentColor: ctypes.POINTER(ctypes.c_int), _transparentColor: ctypes.POINTER(maptype.COLORREF), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexGetTransparentColorFromTab_t (_tabFileName.buffer(), _flagTransparentColor, _transparentColor, _retCode)


#  Определить координаты точки по коэффициентам мирового файла
#  double A_coeff = 0;   # масштаб растра по оси X; размер пиксела по оси X (например в 1 единице растра - 20 метров)
#  double B_coeff = 0;   # масштаб растра по оси Y; отрицательный размер пиксела по оси Y
#  double C_coeff = 0;   # параметры поворота (обычно равны нулю)
#  double D_coeff = 0;   # параметры поворота (обычно равны нулю)
#  double E_coeff = 0;   # параметры сдвига; X,Y координаты центра верхнего левого пиксела
#  double F_coeff = 0;   # параметры сдвига; X,Y координаты центра верхнего левого пиксела
# x1 = Ax + Сy + E
# y1 = Dx + By + F
# x,y - исходные файловые координаты растра (x - колонка, y - ряд).
# http:#gis-lab.info/qa/tfw.html

    picexGetWorldCoordinate_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetWorldCoordinate', ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def picexGetWorldCoordinate(_a_coeff: float, _b_coeff: float, _c_coeff: float, _d_coeff: float, _e_coeff: float, _f_coeff: float, _x: int, _y: int, _xMet: ctypes.POINTER(ctypes.c_double), _yMet: ctypes.POINTER(ctypes.c_double)) -> int:
        return picexGetWorldCoordinate_t (_a_coeff, _b_coeff, _c_coeff, _d_coeff, _e_coeff, _f_coeff, _x, _y, _xMet, _yMet)


# Определить СК по набору символов формата MapInfo из файла TAB
# stringIn      - строка c набором символов формата MapInfo из файла TAB (входной параметр )
#                 CoordSys Earth Projection 8, 104, "m", 21, 0, 0.9996, 500000, 0
#                 Вторая половина строки из файла TAB - 8, 104, 7, 21, 0, 0.9996, 500000, 0
# stringOut     - строка, для размещения описания проекции (выходной параметр )
# sizeStringOut - размер строки stringOut в байтах
# mapregOut     - структура для заполнения параметрами проекции (выходной параметр )
# ellipsoidOut  - структура для заполнения параметрами эллипсоида
# datumOut      - структура для заполнения коэффициентами трансформирования геодезических координат
# codeEPSG      - код EPSG
# retCode       - код возврата
#                           1 - выходные структуры заполнены
#                           0 - выходные структуры не заполнены
# При ошибке функция возвращает 0

    picexCheckMapInfoProjection_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCheckMapInfoProjection', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def picexCheckMapInfoProjection(_stringIn: ctypes.c_char_p, _stringOut: ctypes.c_char_p, _sizeStringOut: int, _mapregOut: ctypes.POINTER(mapcreat.MAPREGISTEREX), _numberProjOut: ctypes.POINTER(ctypes.c_int), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexCheckMapInfoProjection_t (_stringIn, _stringOut, _sizeStringOut, _mapregOut, _numberProjOut, _retCode)

    picexCheckMapInfoProjectionEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCheckMapInfoProjectionEx', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def picexCheckMapInfoProjectionEx(_stringIn: ctypes.c_char_p, _stringOut: ctypes.c_char_p, _sizeStringOut: int, _mapregOut: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoidOut: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumOut: ctypes.POINTER(mapcreat.DATUMPARAM), _codeEPSG: ctypes.POINTER(ctypes.c_int), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexCheckMapInfoProjectionEx_t (_stringIn, _stringOut, _sizeStringOut, _mapregOut, _ellipsoidOut, _datumOut, _codeEPSG, _retCode)


# Чтение и Анализ файла настройки #.map (OziExplorer)
# inputName         - имя графического файла
# rstIniName        - имя файла привязки #.map (OziExplorer)
# param             - указатель на заполняемую структуру RASTERPARM
# При ошибке функция возвращает 0
# retCode - код возрата ошибки

#   picexReadOziFile_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexReadOziFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(RASTERPARM), ctypes.POINTER(ctypes.c_int))
#   def picexReadOziFile(_inputName: mapsyst.WTEXT, _rstIniName: mapsyst.WTEXT, _param: ctypes.POINTER(RASTERPARM), _retCode: ctypes.POINTER(ctypes.c_int)) -> int:
#       return picexReadOziFile_t (_inputName.buffer(), _rstIniName.buffer(), _param, _retCode)


# Установка параметров проекции растра по файлу PRJ
# prjFileName - имя файла PRJ
# rswFileName - имя файла RSW
# При ошибке функция возвращает 0

    picexSetRstProjectionByPrj_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetRstProjectionByPrj', maptype.PWCHAR, maptype.PWCHAR)
    def picexSetRstProjectionByPrj(_prjFileName: mapsyst.WTEXT, _rswFileName: mapsyst.WTEXT) -> int:
        return picexSetRstProjectionByPrj_t (_prjFileName.buffer(), _rswFileName.buffer())


# Установка параметров проекции растра из PRJ-файла по имени графического файла
# graphicFileName - имя графического файла, рядом с которым находится PRJ-файл
#                   имена графического и PRJ- файлов соответствуют
# rswFileName     - имя файла RSW
# При ошибке функция возвращает 0

    picexSetRstProjectionFromPrj_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetRstProjectionFromPrj', maptype.PWCHAR, maptype.PWCHAR)
    def picexSetRstProjectionFromPrj(_graphicFileName: mapsyst.WTEXT, _rswFileName: mapsyst.WTEXT) -> int:
        return picexSetRstProjectionFromPrj_t (_graphicFileName.buffer(), _rswFileName.buffer())


# Корректировка масштаба выходного растра
# Установка масштаба растра, рассчитанного по размеру элемента растра и по
# разрешению исходного графического файла
# graphicFileName - имя импортируемого графического файла
# rswFileName     - имя сформированного выходного файла RSW
# При ошибке функция возвращает 0

    picexAdjustingRstScale_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexAdjustingRstScale', maptype.PWCHAR, maptype.PWCHAR)
    def picexAdjustingRstScale(_graphicFileName: mapsyst.WTEXT, _rswFileName: mapsyst.WTEXT) -> int:
        return picexAdjustingRstScale_t (_graphicFileName.buffer(), _rswFileName.buffer())


# Установить прозрачный цвет растра (для 4, 8, 16, 24, 32-битных растров)
# rswFileName      - имя файла RSW
# transparentColor - значение прозрачного цвета в формате RGB (от 0 до 0x00FFFFFF)
# При ошибке функция возвращает 0

    picexSetRstTransparentColor_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetRstTransparentColor', maptype.PWCHAR, maptype.COLORREF)
    def picexSetRstTransparentColor(_rswFileName: mapsyst.WTEXT, _color: maptype.COLORREF) -> int:
        return picexSetRstTransparentColor_t (_rswFileName.buffer(), _color)


# Запросить тип системы координат по коду EPSG
# epsgcode - код системы координат в базе данных EPSG
# typeProj - тип системы координат (выходной параметр)
#            0 - код EPSG отсутствует
#            1 - прямоугольная система координат (Projection Coordinate System)
#            2 - геодезическая система координат (Geographic latitude-longitude System)
# При ошибке возвращает ноль

    picexGetTypeSystemByEpsgCode_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetTypeSystemByEpsgCode', ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def picexGetTypeSystemByEpsgCode(_epsgcode: int, _typeProj: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexGetTypeSystemByEpsgCode_t (_epsgcode, _typeProj)


# Запросить название алгоритма сжатия по значению тэга TAG_COMPRESSION (259)
# compressValue     - значение тэга TAG_COMPRESSION (259) файла TIFF
# compressName      - указатель на строку для размещения названиz алгоритма сжатия (выходной параметр)
# sizeCompressName  - размер в байтах выделенной строки по указателю compressName
# При ошибке возвращает ноль

    

#========================================================================
###########/    GDAL             #############/
#========================================================================
# Начать работу с Gdal

    picexInitGdal_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexInitGdal')
    def picexInitGdal() -> int:
        return picexInitGdal_t ()


# Закончить работу с Gdal

    picexCloseGdal_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCloseGdal')
    def picexCloseGdal() -> int:
        return picexCloseGdal_t ()


#    Запросить параметры СК из файла средствами GDAL
#    name - имя файла (#.img;#.png;#.gif...)
#    geoTIFFparam - указатель заполняемой структуры

#   picexLoadGdalGeoParametersUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalGeoParametersUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(GEOTIFFPARAM))
#   def picexLoadGdalGeoParametersUn(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _geoTIFFparam: ctypes.POINTER(GEOTIFFPARAM)) -> int:
#       return picexLoadGdalGeoParametersUn_t (_handle, _name.buffer(), _geoTIFFparam)


# запросить параметры растрового изображения посредством библиотеки GDAL
# fileName     - имя файла графических форматов (IMG, PNG, GIF)
# information -  указатель на структуру DATAINFORMATION
#                для записи параметров графического файла
# Структура DATAINFORMATION описана в picexprm.h
# Функцию рекомендуется вызывать перед началом
# конвертации графического файла в Rsw для инициализации диалога сопровождения
# При ошибке возвращает 0

#   picexLoadGdalInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalInformationUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION), ctypes.POINTER(GEOTIFFINFORMATION))
#   def picexLoadGdalInformationUn(_handle: maptype.HMESSAGE, _fileName: mapsyst.WTEXT, _information: ctypes.POINTER(DATAINFORMATION), _geoInformation: ctypes.POINTER(GEOTIFFINFORMATION)) -> int:
#       return picexLoadGdalInformationUn_t (_handle, _fileName.buffer(), _information, _geoInformation)

#   picexGetGdalFileInformationUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexGetGdalFileInformationUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(DATAINFORMATION), ctypes.POINTER(GEOTIFFINFORMATION))
#   def picexGetGdalFileInformationUn(_handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _iformation: ctypes.POINTER(DATAINFORMATION), _geoInformation: ctypes.POINTER(GEOTIFFINFORMATION)) -> int:
#       return picexGetGdalFileInformationUn_t (_handle, _inputname.buffer(), _iformation, _geoInformation)


# Заполнить структуры MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM, GEOTIFFPARAM по данным
# гепространственной информации посредством библиотеки GDAL
# flagGeoSupported - результат работы функции TTranslate.SetProjection по проверке
#                    установленных параметров проекции
# flag_CoordInDegre- Координаты привязки в градусах ? (0-метры, 1-градусы)
# При ошибке возвращает 0

#   picexFillMapRegisterExByGdalExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexFillMapRegisterExByGdalExUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(GEOTIFFPARAM))
#   def picexFillMapRegisterExByGdalExUn(_handle: maptype.HMESSAGE, _fileName: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _flagGeoSupported: ctypes.POINTER(ctypes.c_int), _flag_CoordInDegre: ctypes.POINTER(ctypes.c_int), _geoTIFFparam: ctypes.POINTER(GEOTIFFPARAM)) -> int:
#       return picexFillMapRegisterExByGdalExUn_t (_handle, _fileName.buffer(), _mapreg, _ellipsoid, _datum, _flagGeoSupported, _flag_CoordInDegre, _geoTIFFparam)

    picexFillMapRegisterExByGdalUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexFillMapRegisterExByGdalUn', maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def picexFillMapRegisterExByGdalUn(_handle: maptype.HMESSAGE, _fileName: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _flagGeoSupported: ctypes.POINTER(ctypes.c_int), _flag_CoordInDegre: ctypes.POINTER(ctypes.c_int)) -> int:
        return picexFillMapRegisterExByGdalUn_t (_handle, _fileName.buffer(), _mapreg, _ellipsoid, _datum, _flagGeoSupported, _flag_CoordInDegre)


# Загрузка растровых данных посредством библиотеки GDAL
# обрабатываются файлы графических форматов (IMG, PNG, GIF)
#    Map - карта,содержащая векторные данные
#    inputname - имя загружаемого файла
#    rstname   - имя RST-файла
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point     - точка привязки растра (в метрах)
#                (положение юго-западного угла растра в районе)
#    Handle - диалог визуального сопровождения процесса обработки.
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#    flagMessage - параметр не используется
#                Управление диагностическими сообщениями осуществляется
#                вызовом функции mapMessageEnable.
#                Если mapIsMessageEnable() возвращает 0, то
#                диагностические сообщения не выдаются.
#    flagWorkLog - флаг ведения журнала
#                (при ==1, выполняется ведения журнала
#                при == 0, не выполняется ведения журнала)
#    flagIgnoreGeoTiff - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#    flagIgnoreGeoTag  - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#                 0 - привязка и СК считываются из тега
#                 исходного файла и устанавливаются в выходной растр
#                 1 - привязка устанавливается в выходной растр из
#                 аргумента point, СК не устанавливается
#    При ошибке возвращает ноль
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexLoadGdalFileToRswPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadGdalFileToRswPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexLoadGdalFileToRswPro(_inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _callevent: maptype.EVENTSTATE, _eventparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return picexLoadGdalFileToRswPro_t (_inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _compressJpegQuality, _callevent, _eventparm)

    picexLoadGdalFileToRswAndCompressPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadGdalFileToRswAndCompressPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexLoadGdalFileToRswAndCompressPro(_handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _flagIgnoreGeoTag: int, _callevent: maptype.EVENTSTATE, _eventparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return picexLoadGdalFileToRswAndCompressPro_t (_handle, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _compressJpegQuality, _flagIgnoreGeoTag, _callevent, _eventparm)

#   picexLoadGdalFileToRswAndCompressExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalFileToRswAndCompressExUn', maptype.HMESSAGE, ctypes.POINTER(TASKPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def picexLoadGdalFileToRswAndCompressExUn(_handle: maptype.HMESSAGE, _parm: ctypes.POINTER(TASKPARM), _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _flagMessage: int, _flagWorkLog: int, _flagIgnoreGeoTiff: int, _flagCreateDuplicate: int) -> int:
#       return picexLoadGdalFileToRswAndCompressExUn_t (_handle, _parm, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _compressJpegQuality, _flagMessage, _flagWorkLog, _flagIgnoreGeoTiff, _flagCreateDuplicate)

#   picexLoadGdalFileToRswUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalFileToRswUn', maptype.HMESSAGE, ctypes.POINTER(TASKPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def picexLoadGdalFileToRswUn(_handle: maptype.HMESSAGE, _parm: ctypes.POINTER(TASKPARM), _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagMessage: int, _flagWorkLog: int) -> int:
#       return picexLoadGdalFileToRswUn_t (_handle, _parm, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _flagMessage, _flagWorkLog)

#   picexLoadGdalFileToRswExUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalFileToRswExUn', maptype.HMESSAGE, ctypes.POINTER(TASKPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def picexLoadGdalFileToRswExUn(_handle: maptype.HMESSAGE, _parm: ctypes.POINTER(TASKPARM), _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _flagMessage: int, _flagWorkLog: int, _flagIgnoreGeoTiff: int) -> int:
#       return picexLoadGdalFileToRswExUn_t (_handle, _parm, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _flagMessage, _flagWorkLog, _flagIgnoreGeoTiff)

#   picexLoadGdalFileToRswAndCompressUn_t = mapsyst.GetProcAddress(curLib,ctypes.c_int,'picexLoadGdalFileToRswAndCompressUn', maptype.HMESSAGE, ctypes.POINTER(TASKPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
#   def picexLoadGdalFileToRswAndCompressUn(_handle: maptype.HMESSAGE, _parm: ctypes.POINTER(TASKPARM), _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressJpegQuality: int, _flagMessage: int, _flagWorkLog: int, _flagIgnoreGeoTiff: int) -> int:
#       return picexLoadGdalFileToRswAndCompressUn_t (_handle, _parm, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _compression, _compressJpegQuality, _flagMessage, _flagWorkLog, _flagIgnoreGeoTiff)


# Загрузка однобитных растровых данных посредством библиотеки GDAL в однобитный RSW
# обрабатываются файлы графических форматов (TIFF, IMG, PNG, GIF)
# GDAL описывает такие файлы как одноканальные, 8 бит на канал
#    handle      - дескриптор диалога визуального сопровождения процесса обработки.
#    parm        - указатель на структуру TASKPARM
#    inputname   - имя загружаемого однобитного файла
#    rstname     - имя однобитного файла RSW
#    meterInElementX - размер в метрах элемента по X
#    meterInElementY - размер в метрах элемента по Y
#    point       - точка привязки растра (в метрах)
#                  (положение юго-западного угла растра в районе)
#    palette     - палитра растра
#    paletteCount- количество цветов в палитре (для однобитного файла RSW д.б. 2)
#    compression - флаг использования сжатия при формировании RST-файла (0/1)
#                  0 - сжатие к блокам изображения применяться не будет
#                  1 - блоки д.б. сжаты по методу LZW
#                  метод JPEG недоступен
#    flagMessage - параметр не используется
#                  Управление диагностическими сообщениями осуществляется
#                  вызовом функции mapMessageEnable.
#                  Если mapIsMessageEnable() возвращает 0, то
#                  диагностические сообщения не выдаются.
#    flagWorkLog - флаг ведения журнала
#                  (при ==1, выполняется ведения журнала
#                   при == 0, не выполняется ведения журнала)
#    flagIgnoreGeoTiff - (0/1) флаг игнорирования тегов, содержащих привязку и СК
#                  0 - привязка и СК считываются из тега
#                  исходного файла и устанавливаются в выходной растр
#                  1 - привязка устанавливается в выходной растр из
#                  аргумента point, СК не устанавливается
#    При ошибке возвращает ноль
#
#    Диалогу визуального сопровождения процесса обработки посылаются
#    сообщения:
#    -  (WM_PROGRESSBAR) Извещение об изменении состония процесса
#       WPARAM - текущее состоние процесса в процентах (0% - 100%)
#       Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.
#
#    -  (WM_ERROR) Извещение об ошибке
#       LPARAM - указатель на структуру ERRORINFORMATION
#       Структура ERRORINFORMATION описана в picexprm.h,
#       WM_PROGRESSBAR и WM_ERROR - в maptype.h

    picexLoadGdalOneBitFileToOneBitRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadGdalOneBitFileToOneBitRswUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexLoadGdalOneBitFileToOneBitRswUn(_handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterInPixelX: ctypes.POINTER(ctypes.c_double), _meterInPixelY: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _palette: ctypes.POINTER(maptype.COLORREF), _paletteCount: int, _compression: int, _flagMessage: int, _flagWorkLog: int, _flagIgnoreGeoTiff: int) -> int:
        return picexLoadGdalOneBitFileToOneBitRswUn_t (_handle, _inputname.buffer(), _rstname.buffer(), _meterInPixelX, _meterInPixelY, _point, _palette, _paletteCount, _compression, _flagMessage, _flagWorkLog, _flagIgnoreGeoTiff)


# Загрузка изображения в формате RGBA(для текстуры OpenGL) из PNG-файла
#          c обрезкой (высота и ширина должны быть степенью 2)
#    Вход: namePng - имя исходного PNG-файла
#            image - адрес области записи получаемого изображения;
#             size - размер этой области в байтах;
#      reth и retv - высота и ширина полученного изображения;
#        sizeimage - заполняемый данной функцией размер области, необходимой
#                    для записи получаемого изображения;
#    Возвращаемое значение:
#         0 - в случае ошибки (или при нехватке памяти для получаемого
#             изображения см. sizeimage);
#         1 - в случае успешного получения изображения.

    
    LoadPngToImage32WithCutUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'LoadPngToImage32WithCutUn', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def LoadPngToImage32WithCutUn(_namePng: mapsyst.WTEXT, _image: ctypes.c_char_p, _size: int, _reth: ctypes.POINTER(ctypes.c_int), _retw: ctypes.POINTER(ctypes.c_int), _sizeimage: ctypes.POINTER(ctypes.c_int)) -> int:
        return LoadPngToImage32WithCutUn_t (_namePng.buffer(), _image, _size, _reth, _retw, _sizeimage)


# Функция создает файл RSW (всегда 24 б/п) по изображению
# входного графического файла
# Функция создана для обеспечения функционирования окна "PreView" программы "Банк данных ЦК"
# Привязка и параметры проекции переносятся в выходной растр.
# Размеры изображения выходного файла(ширина и высота) необходимо указать
# в параметрах width и height
# На вход функции могут подаваться файлы следующих форматов:
#    BMP (#.bmp), TIFF (#.tif), JPEG (#.jpg),
#    Imagine (#.img), PNG (#.png), GIF (#.gif)
# Описание работы функции:
# Функция пытается создать "внешнее" обзорное изображение средствами GDAL с
# установленными в аргументах (width, height) параметрами картинки.
# Если в исходном файле уже существует обзорное изображение, то GDAL может не
# позволить создать "внешнее" обзорное изображение. В таком случае, подбирается
# ближайшее обзорное изображение из исходного файла (критерий подбора -
# параметрамы width, height) и сохраняется в файл RSW.
# "Внешнее" обзорное изображение создается средствами GDAL в файл #.ovr.
# Описание входных параметров функции:
# handle - диалог визуального сопровождения процесса обработки
# inputFileName   - имя входного файла
# outputFileName  - имя выходного файла (#.rsw)
# width           - ширина в пикселях изображения выходного файла
# height          - высота в пикселях изображения выходного файла
# messageEnable   - флаг выдчи сообщений MessageBox
# Возвращает: 1 - в случае успешного создания выходного файла
# При ошибке возвращает ноль

    picexPaintImageDataToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexPaintImageDataToRswUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexPaintImageDataToRswUn(_handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _width: int, _height: int, _flagMessage: int) -> int:
        return picexPaintImageDataToRswUn_t (_handle, _inputname.buffer(), _rstname.buffer(), _width, _height, _flagMessage)


# Сохранение файла в JPEG
# Функция сохраняет содержимое файла filenameSource в JPEG-файл filenameOutput
# handle         - диалог визуального сопровождения процесса
# filenameSource - имя исходного файла (BMP, TIFF)
# filenameOutput - имя выходного файла JPEG
# quality        - коэффициент качества изображения, сжатого по методу JPEG

    picexCreateCopyJpegUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCreateCopyJpegUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexCreateCopyJpegUn(_handle: maptype.HMESSAGE, _filenameSource: mapsyst.WTEXT, _filenameOutput: mapsyst.WTEXT, _quality: int) -> int:
        return picexCreateCopyJpegUn_t (_handle, _filenameSource.buffer(), _filenameOutput.buffer(), _quality)


# Сохранение файла в PNG
# Функция сохраняет содержимое файла filenameSource в PNG-файл filenameOutput
# handle         - диалог визуального сопровождения процесса
# filenameSource - имя исходного файла (BMP, TIFF)
# filenameOutput - имя выходного файла PNG

    picexCreateCopyPngUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexCreateCopyPngUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR)
    def picexCreateCopyPngUn(_handle: maptype.HMESSAGE, _filenameSource: mapsyst.WTEXT, _filenameOutput: mapsyst.WTEXT) -> int:
        return picexCreateCopyPngUn_t (_handle, _filenameSource.buffer(), _filenameOutput.buffer())


# Сохранить изображение 24-х битного растра RSW в файл PNG
# Handle              - диалог визуального сопровождения процесса обработки.
# rswName             - имя файла 24-х битного растра RSW
# pngName             - имя файла PNG

    picexSaveRswToPngUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSaveRswToPngUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR)
    def picexSaveRswToPngUn(_handle: maptype.HMESSAGE, _rswName: mapsyst.WTEXT, _pngName: mapsyst.WTEXT) -> int:
        return picexSaveRswToPngUn_t (_handle, _rswName.buffer(), _pngName.buffer())


# Функция "Загрузка матриц из формата IMG"
# hmap         - дескриптор открытого документа
# handle       - диалог визуального сопровождения процесса
# inputnameW   - имя исходного файла IMG
# outputnameW  - имя выходного файла MTW
# scale        - знаменатель масштаба создаваемой матрицы
# flagCompress - флаг сжатия данных матрицы высот

    picexLoadIMGToMtwUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadIMGToMtwUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_int)
    def picexLoadIMGToMtwUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _inputnameW: mapsyst.WTEXT, _outputnameW: mapsyst.WTEXT, _scale: float, _flagCompress: int) -> int:
        return picexLoadIMGToMtwUn_t (_hmap, _handle, _inputnameW.buffer(), _outputnameW.buffer(), _scale, _flagCompress)

    picexLoadIMGToMtwPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexLoadIMGToMtwPro', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_int, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexLoadIMGToMtwPro(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _inputnameW: mapsyst.WTEXT, _outputnameW: mapsyst.WTEXT, _scale: float, _flagCompress: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        return picexLoadIMGToMtwPro_t (_hmap, _handle, _inputnameW.buffer(), _outputnameW.buffer(), _scale, _flagCompress, _callevent, _parm)


# Типы панхроматического слияния
# Панхроматическое слияние (pansharpening)
# Повышает разрешение цветного растра за счет использования панхроматического
# растра повышенного разрешения
# Исходные растры должны иметь одинаковую систему координат
# и их габариты должны пересекаться
# handle  - диалог визуального сопровождения процесса обработки
# hmap    - идентификатор открытых данных
# pannum  - номер панхроматического растра в цепочке
# rgbmap  - идентификатор открытых данных
# rgbnum  - номер RGB растра в цепочке
# outname - имя выходного tiff файла
# pantype - тип панхроматического слияния (PS_MEAN, PS_IHS, PS_BT)
#
# В случае ошибки возвращает 0
# Диалогу визуального сопровождения процесса обработки посылаeтся
# сообщениe WM_PROGRESSBAR об изменении состояния процесса
# WPARAM - текущее состоние процесса в процентах (0% - 100%)
# Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается.

    picexPanSharpening_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexPanSharpening', maptype.HWND, maptype.HMAP, ctypes.c_int, maptype.HMAP, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def picexPanSharpening(_handle: maptype.HWND, _hmap: maptype.HMAP, _pannum: int, _rgbmap: maptype.HMAP, _rgbnum: int, _outname: mapsyst.WTEXT, _pantype: int) -> int:
        return picexPanSharpening_t (_handle, _hmap, _pannum, _rgbmap, _rgbnum, _outname.buffer(), _pantype)


# Перемещение выходного файла на место исходного с созданием резервной копии
# и добавлением к карте
# hMap           - карта, содержащая векторные данные;
# fileNameIn     - имя входного файла;
# fileNameOut    - имя выходного файла;
# positionNumber - номер позиции файла в цепочке
# dataType       - тип обрабатываемых данных
#                          (FILE_RSW, FILE_MTW, FILE_MTL, FILE_MTQ)
# При ошибке возвращает ноль

    picexMoveFilesWithReserveCopyAndAppendToMap_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMoveFilesWithReserveCopyAndAppendToMap', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def picexMoveFilesWithReserveCopyAndAppendToMap(_hmap: maptype.HMAP, _fileNameIn: mapsyst.WTEXT, _fileNameOut: mapsyst.WTEXT, _positionNumber: int, _dataType: int) -> int:
        return picexMoveFilesWithReserveCopyAndAppendToMap_t (_hmap, _fileNameIn.buffer(), _fileNameOut.buffer(), _positionNumber, _dataType)


# Перемещение файла с созданием резервной копии выходного файла
# inputFileName   - имя входного файла;
# outputFileName  - имя выходного файла;
# dataType       - тип обрабатываемых данных
#                          (FILE_RSW, FILE_MTW, FILE_MTL, FILE_MTQ)
# При ошибке возвращает ноль

    picexMoveFileWithReserveCopy_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexMoveFileWithReserveCopy', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexMoveFileWithReserveCopy(_inputFileName: mapsyst.WTEXT, _outputFileName: mapsyst.WTEXT, _dataType: int) -> int:
        return picexMoveFileWithReserveCopy_t (_inputFileName.buffer(), _outputFileName.buffer(), _dataType)


# Добавить файл в документ с установкой позиции в цепочке
# hMap           - идентификатор документа
# fileName       - имя файла
# positionNumber - номер позиции файла в цепочке
# dataType       - тип обрабатываемых данных
#                          (FILE_RSW, FILE_MTW, FILE_MTL, FILE_MTQ)
# При ошибке возвращает ноль

    picexAppendFileToMapWithChainPosition_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexAppendFileToMapWithChainPosition', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def picexAppendFileToMapWithChainPosition(_hmap: maptype.HMAP, _fileName: mapsyst.WTEXT, _positionNumber: int, _dataType: int) -> int:
        return picexAppendFileToMapWithChainPosition_t (_hmap, _fileName.buffer(), _positionNumber, _dataType)


# Установить номер позиции файла в цепочке
# hMap           - идентификатор документа
# fileName       - имя файла
# positionNumber - номер позиции файла в цепочке
# dataType       - тип обрабатываемых данных
#                          (FILE_RSW, FILE_MTW, FILE_MTL, FILE_MTQ)
# При ошибке возвращает ноль

    picexSetCurrentFilePositionInChain_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetCurrentFilePositionInChain', maptype.HMAP, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def picexSetCurrentFilePositionInChain(_hmap: maptype.HMAP, _fileName: mapsyst.WTEXT, _positionNumber: int, _dataType: int) -> int:
        return picexSetCurrentFilePositionInChain_t (_hmap, _fileName.buffer(), _positionNumber, _dataType)


# Определить габариты сохраняемого изображения rectPixel в пикселях
# Применение контекста HPAINT отображения для многопоточного вызова
# dframe         - габариты сохраняемого изображения в метрах (входной параметр)
# meterInElement - размер пикселя выходного изображения в метрах
# rectPixel      - габариты сохраняемого изображения в пикселях (выходной параметр)
# В функции возможна корректировка габаритов сохраняемого изображения
# dframe в метрах на границу пикселя выходного изображения
# При ошибке возвращает ноль

    picexGetImageSize_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetImageSize', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.RECT))
    def picexGetImageSize(_hMap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _meterInElement: float, _rectPixel: ctypes.POINTER(maptype.RECT)) -> int:
        return picexGetImageSize_t (_hMap, _dframe, _meterInElement, _rectPixel)


# Изменить габариты сохраняемого изображения dframe кратно размеру блока aliquot.
# Например, ширина и высота изображения для KMZ должны быть кратны размеру блока aliquot.
# Применение контекста HPAINT отображения для многопоточного вызова
# dframe         - габариты сохраняемого изображения в метрах (входной параметр)
# meterInElement - размер пикселя выходного изображения в метрах
# rectPixel      - габариты сохраняемого изображения в пикселях (выходной параметр)
# aliquot        - размер блока выходного изображения
# В функции возможна корректировка габаритов сохраняемого изображения
# dframe в метрах на границу блока пикселя выходного изображения
# При ошибке возвращает ноль

    picexSetAliquotImageSize_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetAliquotImageSize', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.RECT), ctypes.c_int)
    def picexSetAliquotImageSize(_hMap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _meterInElement: float, _rectPixel: ctypes.POINTER(maptype.RECT), _aliquot: int) -> int:
        return picexSetAliquotImageSize_t (_hMap, _dframe, _meterInElement, _rectPixel, _aliquot)


# Определить габариты сохраняемого изображения rectPixel в пикселях
# dframe        - габариты сохраняемого изображения в метрах (входной параметр)
# scale         - знаменатель масштаба
# resolutionMet - разрешающая способность (точек на метр)
# rectPixel     - габариты сохраняемого изображения в пикселях (выходной параметр)
# В функции возможна корректировка габаритов сохраняемого изображения
# dframe в метрах на границу пикселя выходного изображения
# При ошибке возвращает ноль

    picexGetImageSizeEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexGetImageSizeEx', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.RECT))
    def picexGetImageSizeEx(_hMap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _scale: float, _resolutionMet: float, _rectPixel: ctypes.POINTER(maptype.RECT)) -> int:
        return picexGetImageSizeEx_t (_hMap, _dframe, _scale, _resolutionMet, _rectPixel)


# Изменить габариты сохраняемого изображения dframe кратно размеру блока aliquot.
# Например, ширина и высота изображения для KMZ должны быть кратны размеру блока aliquot.
# Применение контекста HPAINT отображения для многопоточного вызова
# dframe         - габариты сохраняемого изображения в метрах (входной параметр)
# scale         - знаменатель масштаба
# resolutionMet - разрешающая способность (точек на метр)
# rectPixel      - габариты сохраняемого изображения в пикселях (выходной параметр)
# aliquot        - размер блока выходного изображения
# В функции возможна корректировка габаритов сохраняемого изображения
# dframe в метрах на границу блока пикселя выходного изображения
# При ошибке возвращает ноль

    picexSetAliquotImageSizeEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_int,'picexSetAliquotImageSizeEx', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.RECT), ctypes.c_int)
    def picexSetAliquotImageSizeEx(_hMap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _scale: float, _resolutionMet: float, _rectPixel: ctypes.POINTER(maptype.RECT), _aliquot: int) -> int:
        return picexSetAliquotImageSizeEx_t (_hMap, _dframe, _scale, _resolutionMet, _rectPixel, _aliquot)
