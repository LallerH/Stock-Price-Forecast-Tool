import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from utils import Ui_MainWindow, main_engine, get_collections_from_mongodb, Parameters, get_first_correct_date

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    parameters = Parameters()

    # --- manage TICKER SELECTION
    def on_ticker_selection_changed():
        selected_item = ui.list_of_tickersWidget.selectedItems()
        parameters.ticker = selected_item[0].text()
        setbutton()
        setdates()

    if get_collections_from_mongodb():
        list_of_tickers = sorted(get_collections_from_mongodb())
        ui.list_of_tickersWidget.addItems(list_of_tickers)
    else:
        ...
        # ... alapfeltöltést csinálni: ^GSPC

    ui.list_of_tickersWidget.itemSelectionChanged.connect(on_ticker_selection_changed)
    
    # --- manage SETUP SELECTION
    def on_setup_selection_changed():
        selected_item = ui.list_of_setupWidget.selectedItems()
        parameters.indicator_setup = selected_item[0].text()

    ui.list_of_setupWidget.addItem('Base setup')

    ui.list_of_setupWidget.itemSelectionChanged.connect(on_setup_selection_changed)
    ui.list_of_setupWidget.setCurrentRow(0)

    # --- manage DATE setup
    def setdates():
        if parameters.ticker:
            ui.dateEdit_start.setEnabled(True)
            ticker_first_date = get_first_correct_date(coll=parameters.ticker)[1]
            ui.dateEdit_start.setMinimumDate(QDate(int(ticker_first_date[0:4]), int(ticker_first_date[5:7]), int(ticker_first_date[8:10])))
            ui.dateEdit_start.setDate(QDate(int(ticker_first_date[0:4]), int(ticker_first_date[5:7]), int(ticker_first_date[8:10])))
            ui.dateEdit_end.setEnabled(True)
            ui.dateEdit_end.setMinimumDate(QDate(int(ticker_first_date[0:4]), int(ticker_first_date[5:7]), int(ticker_first_date[8:10])))
            ui.dateEdit_end.setDate(QDate.currentDate().addDays(1))
            ui.dateEdit_end.setMaximumDate(QDate.currentDate().addDays(1))
            ui.checkBox_today.setCheckable(True)
            ui.checkBox_today.setEnabled(True)
            ui.checkBox_today.setChecked(False)
            ui.checkBox_tomorrow.setCheckable(True)
            ui.checkBox_tomorrow.setEnabled(True)
            ui.checkBox_tomorrow.setChecked(True)
        else:
            ui.dateEdit_start.setEnabled(False)
            ui.dateEdit_end.setEnabled(False)
            ui.checkBox_today.setCheckable(False)
            ui.checkBox_today.setEnabled(False)
            ui.checkBox_today.setChecked(False)
            ui.checkBox_tomorrow.setCheckable(False)
            ui.checkBox_tomorrow.setEnabled(False)
            ui.checkBox_tomorrow.setChecked(False)

    def set_today():
        ui.checkBox_tomorrow.setChecked(False)
        ui.checkBox_today.setChecked(True)
        ui.dateEdit_end.setDate(QDate.currentDate())

    def set_tomorrow():
        ui.checkBox_today.setChecked(False)
        ui.checkBox_tomorrow.setChecked(True)
        ui.dateEdit_end.setDate(QDate.currentDate().addDays(1))

    def set_related_checkboxes(date):
        ui.checkBox_today.setChecked(False)
        ui.checkBox_tomorrow.setChecked(False)
        if date == QDate.currentDate():
            ui.checkBox_today.setChecked(True)
        elif date == QDate.currentDate().addDays(1):
            ui.checkBox_tomorrow.setChecked(True)

    ui.checkBox_today.clicked.connect(set_today)
    ui.checkBox_tomorrow.clicked.connect(set_tomorrow)
    ui.dateEdit_end.dateChanged.connect(set_related_checkboxes)

    # --- manage BUTTON
    def setbutton():
        if parameters.ticker:
            ui.pushButton.setEnabled(True)
        else:
            ui.pushButton.setEnabled(False)
    
    def start_main_engine():
        
        def show_message(text):
            message_box = QMessageBox()
            message_box.setWindowIcon(QIcon('ikon.ico'))
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setWindowTitle("Projection date info")
            message_box.setText(text)
            message_box.exec()           

        ticker = parameters.ticker
        projection_date = ui.dateEdit_end.date()

        if projection_date.dayOfWeek() == 6:
            show_message(f"{projection_date.toString('yyyy. MM. dd.')} is Saturday, projection will be made for next working day!")
            last_base_date = projection_date.addDays(-1)
        elif projection_date.dayOfWeek() == 7:
            show_message(f"{projection_date.toString('yyyy. MM. dd.')} is Sunday, projection will be made for next working day!")
            last_base_date = projection_date.addDays(-2)
        elif projection_date.dayOfWeek() == 1:
            last_base_date = projection_date.addDays(-3)
        else:
            last_base_date = projection_date.addDays(-1)

        last_base_date = last_base_date.toString('yyyy-MM-dd')
        main_engine(ticker=ticker, date=last_base_date)

    ui.pushButton.clicked.connect(start_main_engine)

    MainWindow.show()
    sys.exit(app.exec())
    