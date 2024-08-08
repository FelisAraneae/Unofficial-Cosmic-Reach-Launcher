import sys
import random
import subprocess
import configparser
import darkdetect
import crl_import as crl
import qdarktheme
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *

def update_theme():
    crl.check_for_config()
    dark_setting = crl.check_in_config("App Settings", "dark_mode")
    if dark_setting == "Auto":
        if darkdetect.isDark():
            qdarktheme.setup_theme()
    elif dark_setting == "Dark":
        qdarktheme.setup_theme(dark_setting.lower())
    else:
        qdarktheme.setup_theme("light")

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ###Creating Tabs
        #Define Tabs
        self.tabs = QTabWidget(self)
        self.home_tab = QScrollArea()
        self.settings_tab = QScrollArea()
        #Add tabs to window
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.settings_tab, "Settings")
        
        #Modify & Defining tabs' layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        home_layout = QtWidgets.QVBoxLayout(self.home_tab)
        settings_layout = QtWidgets.QVBoxLayout(self.settings_tab)
        self.home_tab.setLayout(home_layout)
        self.settings_tab.setLayout(settings_layout)
        
        #Defining Setting's Widgets
        self.theme_label = QLabel(self.settings_tab)
        self.theme_label.setText("<div style ='font-size: 18px;'><b>Application Theme</b></div>")
        self.theme_dropdown = QComboBox()
        dropdown_fill = ["Dark", "Light", "Auto"]
        self.theme_dropdown.addItems(dropdown_fill)
        self.theme_dropdown.currentIndexChanged.connect(self.update_theme_combo_box)
        self.theme_dropdown.setCurrentIndex((dropdown_fill).index(crl.check_in_config("App Settings", "dark_mode")))
        
        # Adding Widgets to Settings
        settings_layout.addWidget(self.theme_label)
        settings_layout.addWidget(self.theme_dropdown)
        settings_layout.addStretch()
        
    @QtCore.Slot()
    def magic(self):
        print("working!")
    
    @QtCore.Slot()
    def update_theme_combo_box(self, value):
        crl.update_in_config("App Settings", "dark_mode", ["Dark", "Light", "Auto"][value])
        update_theme()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    update_theme()
    
    window = MyWidget()
    window.resize(800, 600)
    window.setMinimumSize(420, 260)
    if crl.check_os():
        window.setWindowTitle("Unofficial Cosmic Reach Launcher - macOS")
    else:
        window.setWindowTitle("Unofficial Cosmic Reach Launcher - Windows")
    window.setWindowIcon(QIcon("assets/ucrl_icon.png"))
    window.show()

    sys.exit(app.exec())