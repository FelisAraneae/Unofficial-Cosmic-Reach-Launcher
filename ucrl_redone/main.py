import sys
import random as ran
import subprocess
import configparser
import darkdetect
import crl_import as crl
import qdarktheme
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, QRect, QPoint
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

#Defining FlowLayout              
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
    
    def addItem(self, item):
        self.itemList.append(item)
    
    def count(self):
        return len(self.itemList)
    
    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None
    
    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None
    
    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height
    
    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)
    
    def sizeHint(self):
        return self.minimumSize()
    
    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size
    
    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        
        for item in self.itemList:
            widget = item.widget()
            spaceX = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y += lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
            
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        
        return y + lineHeight - rect.y()

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
            button_widget = QWidget()
            button_layout = FlowLayout(button_widget)
            list = []
            for i in range(ran.randint(1,30)):
                list.append("Instance " + str(i))
            for instance in list:
                button = QToolButton()
                button.setText(instance)
                icon = QIcon("assets/app_icons/ucrl_icon.png")
                button.setIcon(icon)
                button.setFixedSize(QSize(100, 100))
                button.setIconSize(QSize(48, 48))
                button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                button_layout.addWidget(button)
            home_layout.addWidget(button_widget)
            add_instance = QPushButton("Add Instance")
            add_instance.clicked.connect(self.add_instance)
            home_layout.addWidget(add_instance)
            edit_instances = QPushButton("Edit Instances")
            edit_instances.clicked.connect(self.edit_instances)
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
        home_layout = QtWidgets.QHBoxLayout(self.home_tab)
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

    @QtCore.Slot(int)
    def update_theme_combo_box(self, value):
        crl.update_in_config("App Settings", "dark_mode", ["Dark", "Light", "Auto"][value])
        update_theme()

    @QtCore.Slot()
    def edit_instances(self):
        self.edit_instance = QMainWindow()
        self.edit_instance.setWindowTitle("New Window")
        self.edit_instance.resize(300, 200)
        layout = QVBoxLayout()
        label = QLabel("This is a new window", self.edit_instance)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        layout.addWidget(label)
        self.edit_instance.setCentralWidget(central_widget)
        self.edit_instance.show()

    @QtCore.Slot()
    def add_instance(self):
        #Defining Window
        self.new_instance = QMainWindow()
        self.new_instance.setWindowTitle("New Instance")
        self.new_instance.setMinimumSize(500, 300)
        layout = FlowLayout()

        #Defining Icon
        self.icon_label = QLabel(self.new_instance)
        pixmap = QPixmap("assets/app_icons/ucrl_icon.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        #Defining LineEdits
        self.instance_name = QLineEdit(self.new_instance)
        self.instance_name.setText("New Instance")
        self.instance_name.setMinimumWidth(360)
        layout.addWidget(self.instance_name)
        
        
        self.icon_path_edit = QLineEdit(self.new_instance)
        self.icon_path_edit.setText("assets/app_icons/ucrl_icon.png")
        self.icon_path_edit.setMinimumWidth(266)
        layout.addWidget(self.icon_path_edit)

        #Defining PushButton
        self.select_icon_button = QPushButton("Select Icon", self.new_instance)
        self.select_icon_button.clicked.connect(self.select_icon)
        layout.addWidget(self.select_icon_button)

        #Setting Layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.new_instance.setCentralWidget(central_widget)
        central_widget.setContentsMargins(10, 10, 10, 10)
        self.new_instance.show()

        
    @QtCore.Slot()
    def select_icon(self):
        file_path, _ = crl.open_dialog("Select Icon", "Images (*.png *.xpm *.jpg)", self)
        if file_path:
            self.icon_path_edit.setText(file_path)
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(scaled_pixmap)

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