import os
from pathlib import Path

此處 = Path(__file__).parent

librian = (此處 / '..').resolve()
librian外層 = (此處 / '../..').resolve()

librian面板 = librian / 'librian面板'
librian本體 = librian / 'librian本體'

adv網頁 = librian本體 / '前端/adv.html'


相對adv網頁處 = lambda x: os.path.relpath(x, start=adv網頁/'..')
