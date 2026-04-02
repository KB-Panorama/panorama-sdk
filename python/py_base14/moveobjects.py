import ctypes

import mapsyst
import maptype
import mapapi
import seekapi
import logapi
import maperr
import doforeach

import tkinter
from tkinter import filedialog

def MoveObject(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm:ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
    if _hobj == 0:
        return 0
    iret = mapapi.mapRelocateObjectPlane(_hobj, _parm)
    if iret != 0:
      return mapapi.mapCommitObject(_hobj)
    return 0

# Move selected objects or one object 
def MoveObjectsByDxDy(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, dx, dy) -> int:
    if _hmap == 0:
        return 0

    dpoint = maptype.DOUBLEPOINT(dx, dy)
    dofunction = doforeach.DoForEach('Перемещение объектов:', logapi.TAC_MED_MOVE)
    result = dofunction.run(MoveObject, _hmap, _hobj, ctypes.byref(dpoint))

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработано объектов - ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Перемещение объектов'))
    mapapi.mapInvalidate()
    return result


# Move selected objects or one object
def MoveObjects(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Сдвинуть объекты на заданные смещения dx,dy
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    root = tkinter.Tk()
    root.title("Сдвиг объектов")
 
    dx_label = tkinter.Label(text="Смещение по X (вверх): ")
    dy_label = tkinter.Label(text="Смещение по Y (влево): ")
    dx_label.grid(row=0, column=0, sticky="w")
    dy_label.grid(row=1, column=0, sticky="w")

    dx_value = tkinter.IntVar()
    dy_value = tkinter.IntVar()

    dx_entry = tkinter.Entry(textvariable=dx_value)
    dy_entry = tkinter.Entry(textvariable=dy_value)
    dx_entry.grid(row=0,column=1, padx=5, pady=5)
    dy_entry.grid(row=1,column=1, padx=5, pady=5)

    ret_value = tkinter.IntVar()
    ret_value.set(0)

    def Run():
        ret = MoveObjectsByDxDy(_hmap, _hobj, dx_value.get(), dy_value.get())
        ret_value.set(ret)
        root.destroy()

    def Close():
        root.destroy()

    message_button = tkinter.Button(text="Выполнить", command=Run)
    message_button.grid(row=2,column=0, padx=5, pady=5, sticky="e")
    message_button = tkinter.Button(text="Отменить", command=Close)
    message_button.grid(row=2,column=1, padx=5, pady=5, sticky="w")

    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
    return float(ret_value.get())
