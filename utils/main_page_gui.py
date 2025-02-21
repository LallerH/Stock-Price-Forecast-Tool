from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Stock price forecast tool")
        MainWindow.resize(1024, 610)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        MainWindow.setWindowIcon(QIcon('ikon.ico'))
        self.centralwidget.setObjectName("centralwidget")
        
        # verticalLayout --- setup area
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 9, 191, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # verticalLayout_workplace --- workplace area
        self.workplaceLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.workplaceLayoutWidget.setGeometry(QtCore.QRect(229, 9, 775, 541))
        self.workplaceLayoutWidget.setObjectName("workplaceLayoutWidget")
        self.verticalLayout_workplace = QtWidgets.QVBoxLayout(self.workplaceLayoutWidget)
        self.verticalLayout_workplace.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_workplace.setObjectName("workplaceLayoutWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # --- set WIDGETS of setup area
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setText("Choose ticker:")
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("""
            QLabel {
                background-color: lightblue;
                border: 1px solid #4c7a9b;
                border-radius: 5px;
            }
        """)
        self.label.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
     
        self.list_of_tickersWidget = QtWidgets.QListWidget(parent=self.verticalLayoutWidget)
        self.list_of_tickersWidget.setEnabled(True)
        self.list_of_tickersWidget.setObjectName("list_of_tickersWidget")
        self.list_of_tickersWidget.setStyleSheet("""
            QListWidget::item:selected {
                background-color: rgb(76, 172, 207);
                color: white;
            }
            QListWidget::item:hover {
                background-color: #D3D3D3;
                color: black;
            }
        """)
        self.verticalLayout.addWidget(self.list_of_tickersWidget)
        
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_3.setText("Choose indicator setup:")
        self.label_3.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("""
            QLabel {
                background-color: lightblue;
                border: 1px solid #4c7a9b;
                border-radius: 5px;
            }
        """)
        self.label_3.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        
        self.list_of_setupWidget = QtWidgets.QListWidget(parent=self.verticalLayoutWidget)
        self.list_of_setupWidget.setEnabled(True)
        self.list_of_setupWidget.setObjectName("list_of_setupWidget")
        self.list_of_setupWidget.setStyleSheet("""
            QListWidget::item:selected {
                background-color: rgb(76, 172, 207);
                color: white;
            }
            QListWidget::item:hover {
                background-color: #D3D3D3;
                color: black;
            }
        """)
        self.verticalLayout.addWidget(self.list_of_setupWidget)
        
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_4.setText("Choose range and forecast day:")
        self.label_4.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("""
            QLabel {
                background-color: lightblue;
                border: 1px solid #4c7a9b;
                border-radius: 5px;
            }
        """)
        self.label_4.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
               
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setText("First day of base period:")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        
        self.dateEdit_start = QtWidgets.QDateEdit(parent=self.verticalLayoutWidget)
        self.dateEdit_start.setAutoFillBackground(False)
        self.dateEdit_start.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.dateEdit_start.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 2), QtCore.QTime(0, 0, 0)))
        self.dateEdit_start.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1900, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_start.setCalendarPopup(True)
        self.dateEdit_start.setEnabled(False)
        self.dateEdit_start.setStyleSheet("""
            QDateEdit:disabled {
                background-color: #e0e0e0;
                color: darkgray;
                border: 1px solid gray;
            }
            QDateEdit:enabled {
                background-color: white;
                color: black;
                border: 1px solid gray;
            }
        """)
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.verticalLayout.addWidget(self.dateEdit_start)
        
        self.label_5 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_5.setText("Day to make projection:")
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)

        self.dateEdit_end = QtWidgets.QDateEdit(parent=self.verticalLayoutWidget)
        self.dateEdit_end.setAutoFillBackground(False)
        self.dateEdit_end.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.dateEdit_end.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 2), QtCore.QTime(0, 0, 0)))
        self.dateEdit_end.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1900, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_end.setCalendarPopup(True)
        self.dateEdit_end.setEnabled(False)
        self.dateEdit_end.setStyleSheet("""
            QDateEdit:disabled {
                background-color: #e0e0e0;
                color: darkgray;
                border: 1px solid gray;
            }
            QDateEdit:enabled {
                background-color: white;
                color: black;
                border: 1px solid gray;
            }
        """)
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.verticalLayout.addWidget(self.dateEdit_end)

        self.checkBox_today = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_today.setText("Today")
        self.checkBox_today.setCheckable(False)
        self.checkBox_today.setEnabled(False)
        self.checkBox_today.setStyleSheet("""
            QCheckBox:disabled {
                color: darkgrey;
            }
        """)
        self.checkBox_today.setObjectName("checkBox_today")
        self.verticalLayout.addWidget(self.checkBox_today)
        
        self.checkBox_tomorrow = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_tomorrow.setText("Tomorrow")
        self.checkBox_tomorrow.setCheckable(False)
        self.checkBox_tomorrow.setEnabled(False)
        self.checkBox_tomorrow.setStyleSheet("""
            QCheckBox:disabled {
                color: darkgrey;
            }
        """)
        self.checkBox_tomorrow.setObjectName("checkBox_tomorrow")
        self.verticalLayout.addWidget(self.checkBox_tomorrow)
        
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem)

        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setText("Calculate")
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(76, 172, 207);
                border: 1px solid #4c7a9b;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(56, 152, 187);
            }
        """)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        
        # --- MENU
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 26))
        self.menubar.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.menubar.setObjectName("menubar")
        
        # --- File menu
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")

        self.actionLoad_projection = QtGui.QAction(parent=MainWindow)
        self.actionLoad_projection.setText("Load projection")
        self.actionLoad_projection.setObjectName("actionLoad_projection")
        self.menuFile.addAction(self.actionLoad_projection)
        self.actionLoad_projection.setEnabled(False)

        self.actionSave_projection = QtGui.QAction(parent=MainWindow)
        self.actionSave_projection.setText("Save projection")
        self.actionSave_projection.setObjectName("actionSave_projection")
        self.menuFile.addAction(self.actionSave_projection)
        self.actionSave_projection.setEnabled(False)

        self.actionSave_projection_as = QtGui.QAction(parent=MainWindow)
        self.actionSave_projection_as.setText("Save projection as ...")
        self.actionSave_projection_as.setObjectName("actionSave_projection_as")
        self.menuFile.addAction(self.actionSave_projection_as)
        self.menuFile.addSeparator()
        self.actionSave_projection_as.setEnabled(False)

        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setText("Exit")
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)

        # --- User menu
        self.menuUser = QtWidgets.QMenu(parent=self.menubar)
        self.menuUser.setTitle("User")
        self.menuUser.setObjectName("menuUser")
        self.menuUser.setEnabled(False)

        self.actionUser_details = QtGui.QAction(parent=MainWindow)
        self.actionUser_details.setText("User details")
        self.actionUser_details.setObjectName("actionUser_details")
        self.menuUser.addAction(self.actionUser_details)
        self.menuUser.addSeparator()

        self.actionLogout = QtGui.QAction(parent=MainWindow)
        self.actionLogout.setText("Logout")
        self.actionLogout.setObjectName("actionLogout")
        self.menuUser.addAction(self.actionLogout)

        # --- Database menu
        self.menuDatabase = QtWidgets.QMenu(parent=self.menubar)
        self.menuDatabase.setTitle("Database")
        self.menuDatabase.setObjectName("menuDatabase")        
        
        self.actionAvailable_data = QtGui.QAction(parent=MainWindow)
        self.actionAvailable_data.setText("Available stock data")
        self.actionAvailable_data.setObjectName("actionAvailable_data")
        self.menuDatabase.addAction(self.actionAvailable_data)
        self.actionAvailable_data.setEnabled(False)

        self.actionDownload_new_stock = QtGui.QAction(parent=MainWindow)
        self.actionDownload_new_stock.setText("Download new stock")
        self.actionDownload_new_stock.setObjectName("actionDownload_new_stock")
        self.menuDatabase.addAction(self.actionDownload_new_stock)

        self.actionUpdate_stock_data = QtGui.QAction(parent=MainWindow)
        self.actionUpdate_stock_data.setText("Update stock data")
        self.actionUpdate_stock_data.setObjectName("actionUpdate_stock_data")
        self.menuDatabase.addAction(self.actionUpdate_stock_data)
        self.actionUpdate_stock_data.setEnabled(False)

        # --- Setup indicators menu
        # self.menuSetup_indicators = QtWidgets.QMenu(parent=self.menubar)
        # self.menuSetup_indicators.setTitle("Setup indicators")
        # self.menuSetup_indicators.setObjectName("menuSetup_indicators")

        # self.actionLoad_setup = QtGui.QAction(parent=MainWindow)
        # self.actionLoad_setup.setText("Load setup")
        # self.actionLoad_setup.setObjectName("actionLoad_setup")
        # self.menuSetup_indicators.addAction(self.actionLoad_setup)

        # self.actionSave_setup = QtGui.QAction(parent=MainWindow)
        # self.actionSave_setup.setText("Save setup")
        # self.actionSave_setup.setObjectName("actionSave_setup")
        # self.menuSetup_indicators.addAction(self.actionSave_setup)

        # self.actionSave_setup_as = QtGui.QAction(parent=MainWindow)
        # self.actionSave_setup_as.setText("Save setup as ...")
        # self.actionSave_setup_as.setObjectName("actionSave_setup_as")
        # self.menuSetup_indicators.addAction(self.actionSave_setup_as)

        # self.actionNew_setup = QtGui.QAction(parent=MainWindow)
        # self.actionNew_setup.setText("New setup")
        # self.actionNew_setup.setObjectName("actionNew_setup")
        # self.menuSetup_indicators.addAction(self.actionNew_setup)

        # --- Help menu
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setTitle("Help")
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setEnabled(False)

        self.actionIndicators = QtGui.QAction(parent=MainWindow)
        self.actionIndicators.setText("Indicators")
        self.actionIndicators.setObjectName("actionIndicators")
        self.menuHelp.addAction(self.actionIndicators)
        
        self.actionList_of_tickers = QtGui.QAction(parent=MainWindow)
        self.actionList_of_tickers.setText("List of tickers")
        self.actionList_of_tickers.setObjectName("actionList_of_tickers")
        self.menuHelp.addAction(self.actionList_of_tickers)

        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setText("About")
        self.actionAbout.setObjectName("actionAbout")       
        self.menuHelp.addAction(self.actionAbout)

        # --- setMenuBar ---
        self.menubar.setStyleSheet("""
            QMenuBar {
                border: 1px solid #809fa8;
                border-radius: 1px;
                background-color: #bcdee8;
            }            
            QMenu::item {
                padding-left: 12px;
                padding-right: 12px;
                padding-top: 3px;
                padding-bottom: 3px;
            }
            QMenu::item:selected { 
                background-color: lightblue;
                border-radius: 8px;
                margin: 1px;
            }
        """)
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuUser.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        # self.menubar.addAction(self.menuSetup_indicators.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # TabWidgets on WORKPLACE
        self.tabs = QtWidgets.QTabWidget()

        self.tab_indicator = QtWidgets.QWidget()
        self.tab_histogram = QtWidgets.QWidget()
        self.tab_candlestick = QtWidgets.QWidget()

        self.tabs.addTab(self.tab_indicator, "Indicator settings")
        self.tabs.addTab(self.tab_histogram, "Histogram")
        self.tabs.addTab(self.tab_candlestick, "Candlestick chart")

        self.verticalLayout_workplace.addWidget(self.tabs)

        self.indicator_layout = QtWidgets.QVBoxLayout(self.tab_indicator)
        self.histogram_layout = QtWidgets.QVBoxLayout(self.tab_histogram)
        self.candlestick_layout = QtWidgets.QVBoxLayout(self.tab_candlestick)

        # Set STATUSBAR
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: transparent;
                border: none;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        MainWindow.setStatusBar(self.statusbar)
        
        # Set PROGRESSBAR
        self.label_progress = QtWidgets.QLabel()
        self.label_progress.setText("Processing data:")
        self.label_progress.setObjectName("label_progress")
        
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                background-color: #E0E0E0;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: rgb(76, 172, 207);
                margin: 1px;
            }
        """)
        self.progress_bar.setFormat('%p%')
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setFixedWidth(200)
        self.spacer = QtWidgets.QWidget()
        self.spacer.setStyleSheet("background-color: transparent; border: none;")
        self.statusbar.addWidget(self.spacer, 1)

def show_message(text):
    message_box = QtWidgets.QMessageBox()
    message_box.setWindowIcon(QIcon('ikon.ico'))
    message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
    message_box.setWindowTitle("Information")
    message_box.setText(text)
    message_box.exec()

def input_text():
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle('Save')
    dialog.setLabelText('Input setup name:')    
    dialog.setWindowIcon(QIcon('ikon.ico'))
    dialog.setStyleSheet("""
        QLineEdit {
            border: 1px solid grey;
            border-radius: 1px;
            padding: 2px;
        }
        QDialogButtonBox QPushButton {
            background-color: rgb(76, 172, 207);
            border: 1px solid #4c7a9b;
            border-radius: 5px;
            padding: 5px;
            min-width: 75px;
            height: 10px;
            color: black;
        }
        QDialogButtonBox QPushButton:hover {
            background-color: rgb(56, 152, 187);
            color: black;
        }
    """)
    ok = dialog.exec()
    if ok:
        return ok, dialog.textValue()
    return ok, False

def input_text_stock():
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle('New stock')
    dialog.setLabelText('Input ticker name:')    
    dialog.setWindowIcon(QIcon('ikon.ico'))
    dialog.setStyleSheet("""
        QLineEdit {
            border: 1px solid grey;
            border-radius: 1px;
            padding: 2px;
        }
        QDialogButtonBox QPushButton {
            background-color: rgb(76, 172, 207);
            border: 1px solid #4c7a9b;
            border-radius: 5px;
            padding: 5px;
            min-width: 75px;
            height: 10px;
            color: black;
        }
        QDialogButtonBox QPushButton:hover {
            background-color: rgb(56, 152, 187);
            color: black;
        }
    """)
    ok = dialog.exec()
    if ok:
        return ok, dialog.textValue()
    return ok, False

def hide_widgets(layout):
    for i in range(layout.count() - 1, -1, -1):
        item = layout.itemAt(i)
        if item:
            widget = item.widget()
            if widget:
                widget.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    input_text()
    sys.exit(app.exec())
