import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu

from rena.config import app_logo_path
from rena.configs.configs import AppConfigs
from rena.ui.SplashScreen import SplashScreen

AppConfigs(_reset=False)  # create the singleton app configs object
from MainWindow import MainWindow
from rena.startup import load_settings

app = None

if __name__ == '__main__':

    # load the qt application
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    tray_icon = QSystemTrayIcon(QIcon(app_logo_path), parent=app)
    tray_icon.setToolTip('RenaLabApp')
    tray_icon.show()

    # create the splash screen
    splash = SplashScreen()
    splash.show()

    # load default settings
    load_settings(revert_to_default=False, reload_presets=False)

    # main window init
    window = MainWindow(app=app)

    window.setWindowIcon(QIcon(app_logo_path))
    # make tray menu
    menu = QMenu()
    exit_action = menu.addAction('Exit')
    exit_action.triggered.connect(window.close)

    # splash screen destroy
    splash.close()
    window.show()

    try:
        app.exec()
        sys.exit()
    except KeyboardInterrupt:
        print('App terminate by KeyboardInterrupt')
        sys.exit()
