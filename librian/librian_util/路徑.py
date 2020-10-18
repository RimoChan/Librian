import os
from pathlib import Path


此處 = Path(__file__).parent

librian = (此處 / '..').resolve()

librian面板 = librian / 'librian面板'
librian本體 = librian / 'librian本體'



def 虛擬相對前端路徑(x):
    源 = librian本體 / 'v' / x
    前端 = librian本體 / '前端'
    return os.path.relpath(源, start=前端)
