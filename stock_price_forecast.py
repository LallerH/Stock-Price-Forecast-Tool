import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from utils import Ui_MainWindow, main_engine, get_collections_from_mongodb, Parameters, get_first_correct_date

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    parameters = Parameters()

    # --- manage TICKER SELECTION
    def on_item_selection_changed():
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

    ui.list_of_tickersWidget.itemSelectionChanged.connect(on_item_selection_changed)

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
            ui.checkBox_today.setCheckable(True)
            ui.checkBox_today.setChecked(False)
            ui.checkBox_tomorrow.setCheckable(True)
            ui.checkBox_tomorrow.setChecked(True)
        else:
            ui.dateEdit_start.setEnabled(False)
            ui.dateEdit_end.setEnabled(False)
            ui.checkBox_today.setCheckable(False)
            ui.checkBox_today.setChecked(False)
            ui.checkBox_tomorrow.setCheckable(False)
            ui.checkBox_tomorrow.setChecked(False)

    def set_today():
        ui.checkBox_tomorrow.setChecked(False)
        ui.checkBox_today.setChecked(True)
        ui.dateEdit_end.setDate(QDate.currentDate())

    def set_tomorrow():
        ui.checkBox_today.setChecked(False)
        ui.checkBox_tomorrow.setChecked(True)
        ui.dateEdit_end.setDate(QDate.currentDate().addDays(1))

    ui.checkBox_today.clicked.connect(set_today)
    ui.checkBox_tomorrow.clicked.connect(set_tomorrow)

    # --- manage BUTTON
    def setbutton():
        if parameters.ticker:
            ui.pushButton.setEnabled(True)
        else:
            ui.pushButton.setEnabled(False)
    
    ui.pushButton.clicked.connect(main_engine)

    MainWindow.show()
    sys.exit(app.exec())
    