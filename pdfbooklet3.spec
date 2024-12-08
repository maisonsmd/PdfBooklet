# -*- mode: python3 -*-

import os
import site

gnome_path = 'C:\msys64\mingw64'
typelib_path = os.path.join(gnome_path, 'lib', 'girepository-1.0')
missing_files = []

for tl in ["GIRepository-2.0.typelib", "GdkPixbuf-2.0.typelib", "GModule-2.0.typelib", "Poppler-0.18.typelib"] :
    typelib_full_path = os.path.join(typelib_path, tl)
    if os.path.exists(typelib_full_path):
        missing_files.append((typelib_full_path, "./gi_typelibs"))
    else:
        print(f"Warning: {typelib_full_path} not found")

for dll in ["libpoppler-143.dll", "libpoppler-cpp-1.dll", "libpoppler-glib-8.dll", "libstdc++-6.dll", "libopenjp2-7.dll", "liblcms2-2.dll", "libgirepository-2.0-0.dll"] :
    dll_full_path = os.path.join(gnome_path, 'bin', dll)
    if os.path.exists(dll_full_path):
        missing_files.append((dll_full_path, "./"))
    else:
        print(f"Warning: {dll_full_path} not found")

datafiles = [("pdfbooklet/data", "pdfbooklet/data")]

excluded = [("./share/*.*"), ("./share/etc/*.*")]

block_cipher = None

print("Missing files:")
for f in missing_files:
    print(f)

a = Analysis(['pdfbooklet/pdfbooklet3.py'],
             pathex=[
                'd:\\repos\\PdfBooklet\\pdfbooklet',
                'C:\\msys64\\mingw64\\bin',
                'C:\\msys64\\mingw64\\lib',
                'C:\\msys64\\mingw64\\lib\\girepository-1.0',
                'C:\\msys64\\mingw64\\lib\\python3.12\\site-packages'
             ],
             binaries=missing_files,            
             datas=datafiles,
             hiddenimports=[
                'gi',
                'gi.repository',
                'gi.repository.Poppler',
                'backports',
             ],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

"""
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pdfbooklet',
          debug=False,
          strip=False,
          upx=True,
          console=False )
"""
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pdfbooklet',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='pdfbooklet/data/pdfbooklet.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pdfbooklet')
