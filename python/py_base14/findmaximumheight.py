import mapsyst
import maptype
import mapapi
import seekapi
import doforeach
import maperr

def CheckMaximumHeight(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, MaxHeights) -> int:
    if _hobj == 0:
        return 0
    ObjectNumber = mapapi.mapGetObjectNumber(_hobj)
    ObjectHeight = mapapi.mapSemanticCodeDoubleValue(_hobj, 4,1)
    if ObjectHeight > MaxHeights[-1][0]:
        MaxHeights[-1][0],MaxHeights[-1][1]=ObjectHeight,ObjectNumber
    return MaxHeights[-1][0]
    
def SearchHeightObject(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> int:
    MaxHeights=[[-10**5,0]]
    dofunction = doforeach.DoForEach('Поиск максимума высоты')
    result = dofunction.run(CheckMaximumHeight, _hmap, _hobj, MaxHeights)
    mapapi.mapShowMessage(mapsyst.WTEXT('Найдена максимальная высота в семантике 4 - ' + str(MaxHeights[-1][0])), mapsyst.WTEXT('Номер объекта - ' + str(MaxHeights[-1][1])))
    return MaxHeights[-1][0]

# Determine the maximum height of the selected objects
def SearchForTheMaximum(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Определить максимумальную высоту среди выделенных объектов
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    return SearchHeightObject(_hmap, _hobj)
