"""
Модуль для операций со временем
"""
import time


def time_synch():
    return time.time()


def elapsed_sec(t: time):
    return (time_synch() - t) * 100


def time_elapsed(start: time, end: time = time_synch()):
    return end - start
