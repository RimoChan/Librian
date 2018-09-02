import os
import tempfile

f=tempfile.NamedTemporaryFile(delete=False)
f.write(b'import os;os.system(\'\""./python36/python.exe\"" -m Librian.py\')')
f.close()

os.system(f'pyinstaller {f.name} --name Librian.exe --distpath ./ -F -i 資源/librian.ico')
