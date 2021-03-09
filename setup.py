""" setup the app """
from setuptools import setup

APP = ['bar_osc.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'sounddevice'],
}

setup(
    app=APP,
    name='Bar Osc',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps', 'sounddevice']
)
