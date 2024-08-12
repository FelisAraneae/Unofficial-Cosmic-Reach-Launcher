import sys
import random as ran
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
        else:
            qdarktheme.setup_theme("light")
    elif dark_setting == "Dark":
        qdarktheme.setup_theme(dark_setting.lower())
    else:
        qdarktheme.setup_theme("light")

def developer_mode_widgets(visibility, self):
            if not visibility or visibility == "False":
                self.relinst_button.hide()
            else:
                self.relinst_button.show()

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        def reload_instances(self, home_layout):
            if home_layout is not None:
                while home_layout.count() > 0:
                    item = home_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
            print("Loading instances")
            for instance in ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5"]:
                button = QPushButton(instance)
                home_layout.addWidget(button)
            edit_instances = QPushButton("Edit Instances")
            home_layout.addWidget(edit_instances)
            home_layout.addStretch()

        
        ###Creating Tabs
        #Define Tabs
        self.tabs = QTabWidget(self)
        self.home_tab = QScrollArea()
        self.settings_tab = QScrollArea()
        # Set QScrollArea to be resizable
        self.home_tab.setWidgetResizable(True)
        self.settings_tab.setWidgetResizable(True)
        #Add tabs to window
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.settings_tab, "Settings")
        
        ###Modify & Defining tabs' layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        home_layout = QtWidgets.QVBoxLayout(self.home_tab)
        settings_layout = QtWidgets.QVBoxLayout(self.settings_tab)
        self.home_tab.setLayout(home_layout)
        self.settings_tab.setLayout(settings_layout)
        #Create content widgets
        home_content = QWidget()
        settings_content = QWidget()
        #Set layout for content widgets
        home_layout = QtWidgets.QVBoxLayout(home_content)
        settings_layout = QtWidgets.QVBoxLayout(settings_content)
        #Add content widgets to scroll areas
        self.home_tab.setWidget(home_content)
        self.settings_tab.setWidget(settings_content)
        
        ###Defining Setting's Widgets
        #Labels
        self.theme_label = QLabel(self.settings_tab)
        self.theme_label.setText("<div style ='font-size: 18px;'><b>Application Theme</b></div>")
        self.update_label = QLabel(self.settings_tab)
        self.update_label.setText("<div style ='font-size: 18px;'><b>Update</b></div>")
        self.info_label = QLabel(self.settings_tab)
        self.info_label.setText("<div style ='font-size: 18px;'><b>Info</b></div>")
        self.version_label = QLabel(self.settings_tab)
        self.version_label.setText("<div style ='font-size: 13px;'>UCRL 0.0.6</div>")
        self.authors_label = QLabel(self.settings_tab)
        self.authors_label.setText("<div style ='font-size: 13px;'>By <a href='https://github.com/ieatsoulsmeow'>IEatSoulsMeow</a> and <a href='https://github.com/felisaraneae'>FelisAraneae</a>")
        self.authors_label.setOpenExternalLinks(True)
        self.github_label = QLabel(self.settings_tab)
        self.github_label.setText("<div style ='font-size: 13px;'>Source can be found on <a href='https://github.com/FelisAraneae/Unofficial-Cosmic-Reach-Launcher'>Github</a>")
        self.github_label.setOpenExternalLinks(True)
        self.discord_label = QLabel(self.settings_tab)
        self.discord_label.setText("<div style ='font-size: 13px;'>Join the unofficial <a href='https://discord.gg/jRs9q7FMSu'>Discord</a> for other Cosmic Reach launchers")
        self.discord_label.setOpenExternalLinks(True)
        self.developer_label = QLabel(self.settings_tab)
        self.developer_label.setText("<div style ='font-size: 18px;'><b>Developer Settings</b></div>")
        #QComboBox
        self.theme_dropdown = QComboBox()
        dropdown_fill = ["Dark", "Light", "Auto"]
        self.theme_dropdown.addItems(dropdown_fill)
        self.theme_dropdown.currentIndexChanged.connect(self.update_theme_combo_box)
        self.theme_dropdown.setCurrentIndex((dropdown_fill).index(crl.check_in_config("App Settings", "dark_mode")))
        #Buttons
        self.update_button = QPushButton("Update Application")
        self.update_button.setIcon(QIcon("assets/button_icons/update_darkmode.svg"))
        self.update_button.clicked.connect(self.magic)
        #Buttons
        self.relinst_button = QPushButton("Reload Instances")
        self.relinst_button.clicked.connect(lambda: reload_instances(self, home_layout))
        #Toggle
        self.developer_toggle = QPushButton("Developer Mode: ", self)
        self.developer_toggle.setCheckable(True)
        self.developer_toggle.setChecked(True)
        self.developer_toggle.clicked.connect(self.toggle)
        if crl.check_in_config("App Settings", "dev_mode") == "True":
            self.developer_toggle.setText("Developer Mode: Enabled")
            self.developer_toggle.setStyleSheet("QPushButton {background-color:#43904b; color:#dfdfdf}")
        else:
            self.developer_toggle.setChecked(False)
            self.developer_toggle.setText("Developer Mode: False")
            self.developer_toggle.setStyleSheet("QPushButton {background-color:#904343; color:#dfdfdf}")
        
        # Adding Widgets to Settings
        settings_layout.addWidget(self.theme_label)
        settings_layout.addWidget(self.theme_dropdown)
        settings_layout.addSpacing(35)
        settings_layout.addWidget(self.update_label)
        settings_layout.addWidget(self.update_button)
        settings_layout.addSpacing(35)
        settings_layout.addWidget(self.info_label)
        settings_layout.addWidget(self.version_label)
        settings_layout.addWidget(self.authors_label)
        settings_layout.addWidget(self.github_label)
        settings_layout.addWidget(self.discord_label)
        settings_layout.addSpacing(70)
        settings_layout.addWidget(self.developer_label)
        settings_layout.addWidget(self.developer_toggle)
        settings_layout.addWidget(self.relinst_button)
        settings_layout.addStretch()
        
        ### Afterwards
        developer_mode_widgets(crl.check_in_config("App Settings", "dev_mode"), self)
        reload_instances(self, home_layout)
        
    @QtCore.Slot()
    def magic(self):
        print("working!")
        
    @QtCore.Slot()
    def toggle(self):
        if self.developer_toggle.isChecked():
            self.developer_toggle.setStyleSheet("QPushButton {background-color:#43904b; color:#dfdfdf}")
            self.developer_toggle.setText("Developer Mode: Enabled")
        else:
            self.developer_toggle.setStyleSheet("QPushButton {background-color:#904343; color:#dfdfdf}")
            self.developer_toggle.setText("Developer Mode: Disabled")
        crl.update_in_config("App Settings", "dev_mode", str(self.developer_toggle.isChecked()))
        developer_mode_widgets(self.developer_toggle.isChecked(), self)
    
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
        window.setWindowIcon(QIcon("assets/ucrl_icon.png"))
    else:
        window.setWindowTitle("Unofficial Cosmic Reach Launcher - Windows")
        window.setWindowIcon(QIcon("assets/ucrl_icon.icns"))
    window.show()

    sys.exit(app.exec())