import ctypes

import mapsyst
import maptype
import mapapi
import maperr
import gisdlgs

# Edit points for one object
def EditPoints(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Редактирование списка координат в табличном виде
    if _hmap == 0:
        return 0

    if _hobj == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_OBJECTNOTSETTED, __name__)
        return 0

    _parm = maptype.TASKPARMEX()
    _parm.Handle = mapapi.mapGetHandleForMessage()

    gisdlgs.tedInsertPoints(_hmap, ctypes.byref(_parm), _hobj, None);

    return 0
