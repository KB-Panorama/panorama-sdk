#!/usr/bin/env python3

import mapsyst
import maptype
import mapapi
import seekapi

#################################################################
# Вспомогательные функции для запуска отладки скрипта
#################################################################
def open(debug_syspath, debug_docname, sheet_name = None, obj_number = 0):
    mapapi.mapSetPathShellUn(mapsyst.WTEXT(debug_syspath))
    mapapi.mapSetMapAccessLanguage(maptype.ML_RUSSIAN)
    debug_hmap = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(debug_docname))
    if debug_hmap == 0:
        return 0, 0
    seekapi.mapRestoreTotalSeekSelectModel(debug_hmap, mapsyst.WTEXT("PySeekParameters"));
    seekapi.mapSetTotalSeekAccess(debug_hmap, 1)
    seekapi.mapSetTotalSelectFlag(debug_hmap, 1)
    if sheet_name is None:
        debug_hobj = 0
    else:
        debug_hobj = mapapi.mapCreateObject(debug_hmap, 1, maptype.IDDOUBLE2, 0)
        seekapi.mapSeekObjectUn(debug_hmap, debug_hobj, mapsyst.WTEXT(sheet_name), obj_number)
    return debug_hmap, debug_hobj

def close(debug_hmap, debug_hobj):
    mapapi.mapFreeObject(debug_hobj)
    mapapi.mapCloseData(debug_hmap)


#################################################################
# Примерный вид вставок в скрипт для эмуляции запуска из ГИС
#################################################################

#debug.begin1
#import sys
#sys.path.append('c:/Users/Public/Documents/Panorama/py_mapapi14')
#import mapsyst
#debug_syspath = 'c:/Program Files/Panorama/Panorama15'
#mapsyst.setuppanlib(debug_syspath)
#import mapdebug
#debug_docname = 'c:/Users/Public/Documents/Panorama/Panorama15/data/noginsk/debug_moveobjects.mpt'
#debug_hmap, debug_hobj = mapdebug.open(debug_syspath, debug_docname)
#if debug_hmap == 0:
#    sys.exit()
#debug.end1

# Move selected objects or one object
#def MoveObjects(hmap:maptype.HMAP, hobj:maptype.HOBJ) -> float: #caption:Сдвинуть объекты на заданные смещения dx,dy
#     ...

#debug.begin2
#MoveObjects(debug_hmap, debug_hobj)
#mapdebug.close(debug_hmap, debug_hobj)
#debug.end2