import ctypes

import mapsyst
import maptype
import mapapi
import seekapi
import maperr
import doforeach


class SquareSum:
    __square = 0.0

    def __init__(self, square = 0.0):
        self.__square = square

    def add(self, value):
        self.__square += value

    def value(self):
        return self.__square

def ObjectArea(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm:SquareSum) -> int:
    _parm.add(mapapi.mapSquare(_hobj))
    return 1 

# Calculation of the area of selected objects or a choosed object
def GetObjectsArea(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Вычислить площадь выделенных объектов
    if _hmap == 0:
        return 0

    if _hobj == 0:
        if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0

    square = SquareSum()
    dofunction = doforeach.DoForEach('Подсчет площади объектов:', 0)
    result = dofunction.run(ObjectArea, _hmap, _hobj, square)

    mapapi.mapShowMessage(mapsyst.WTEXT('Площадь объектов (' + mapapi.IntToStr(result) + ') ' + mapapi.FloatToStr(square.value()) + ' м'), mapsyst.WTEXT('Подсчет площади'))
    return square.value()
