""" Точка входа для ГИС Панорама. Функция RosstatThematic. Основная реализация в модуле rosstat2map.py"""
from rosstat2map import run_rosstat_monitor


def RosstatThematic(hmap, hobj): #caption: Тематическое картографирование по данным Росстата
    """Данные Росстата и тематические карты по регионам РФ"""
    if hmap is None or (hasattr(hmap, '__int__') and int(hmap) == 0):
        return 0.0
    try:
        return run_rosstat_monitor(hmap)
    except Exception:
        return 0.0
