import os
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % 'spareparts',
    '--onefile',
    '--windowed',
#    '--add-data=%s' % os.path.join('resource', 'T:\TEMPO\RECS', 'levels.csv'),
    '--icon=%s' % os.path.join('resource', '.', 'icon.ico'),
    os.path.join('spareparts', '__main__.py'),
])