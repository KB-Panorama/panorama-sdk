#!/usr/bin/env python3

import ctypes
import maptype

PACK_WIDTH = 1

LISTSNAME = ctypes.c_char*256

#-----------------------------
class INFOLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
#-----------------------------


#-----------------------------
class INFOSXF(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SheetName",ctypes.c_char*32),
                ("Nomenclature",ctypes.c_char*32),
                ("RealCoordinate",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("RecordCount",ctypes.c_int),
                ("MapType",ctypes.c_int)]
#-----------------------------


#-----------------------------
class INFODIR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SheetName",ctypes.c_char*32),
                ("NameRsc",ctypes.c_char*maptype.MAX_PATH),
                ("CountList",ctypes.c_int)]
#-----------------------------


#-----------------------------
class INFOCOORD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("CoordPsp",ctypes.c_double),
                ("CoordCalc",ctypes.c_double),
                ("Delta",ctypes.c_double),
                ("Number",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ARRAYNAME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code",ctypes.c_int),
                ("Title",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Name",ctypes.c_char*16)]
#-----------------------------


#-----------------------------
class NAMESARRAY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Size",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Record",LISTSNAME*1)]
#-----------------------------


#-----------------------------
class RESTOREMODE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Note",ctypes.c_int),
                ("VisualSeek",ctypes.c_int),
                ("MapSeek",ctypes.c_int),
                ("RestoreSelect",ctypes.c_int)]
#-----------------------------


#-----------------------------
class AREASEEKPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Size",ctypes.c_int),
                ("RestoreSelect",ctypes.c_int),
                ("ToSelectArea",ctypes.c_int),
                ("VisualSeek",ctypes.c_int),
                ("MapSeek",ctypes.c_int),
                ("AreaType",ctypes.c_int),
                ("InsideFlag",ctypes.c_int),
                ("FilterFlag",ctypes.c_int),
                ("AreaAction",ctypes.c_int),
                ("InversionFlag",ctypes.c_int),
                ("Distance",ctypes.c_double)]
#-----------------------------


#-----------------------------
class BUILDZONESELECTEDPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ZNameSit",ctypes.c_char*256),
                ("ZRadius",ctypes.c_double),
                ("ArcDist",ctypes.c_double),
                ("CornerFactor",ctypes.c_double),
                ("Precision",ctypes.c_double),
                ("ZRegim",ctypes.c_int),
                ("ZCodeSemantic",ctypes.c_int),
                ("ZIndexLocal",ctypes.c_int),
                ("ZForm",ctypes.c_int),
                ("FlagTransaction",ctypes.c_int),
                ("ZCodeObject",ctypes.c_int),
                ("FlagFilter",ctypes.c_int),
                ("TypeZone",ctypes.c_int),
                ("Reserve",ctypes.c_char*16)]
#-----------------------------


