import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from utils import Ui_MainWindow, main_engine, get_collections_from_mongodb,\
                  Parameters, get_first_correct_date, CandlestickChart, HistogramChart, show_message, hide_widgets,\
                  check_database_in_mongodb, initial_upload_of_database

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

    if not check_database_in_mongodb(database = 'Stock_data'):
        show_message('Click to start the initial setup of database!')
        print('Downloading...')
        try:
            initial_upload_of_database(database = 'Stock_data')
            show_message('Initial setup of database succeded!\nInitial download of S&P, DAX and NASDAQ indexes succeeded!')
        except:
            show_message('Initial setup of database was not succeeded!\nRequired:\n- database manager MongoDB (mongodb://localhost:27017)\n- internet connection')
            sys.exit(app.exec())

    if get_collections_from_mongodb():
        list_of_tickers = sorted(get_collections_from_mongodb())
        ui.list_of_tickersWidget.addItems(list_of_tickers)
    else:
        print('Downloading...')
        try:
            initial_upload_of_database(database = 'Stock_data')
            show_message('Initial setup of database succeded!\nInitial download of S&P, DAX and NASDAQ indexes succeeded!')
        except:
            show_message('Initial setup of database was not succeeded!\nRequired:\n- database manager MongoDB (mongodb://localhost:27017)\n- internet connection')
            sys.exit(app.exec())

    ui.list_of_tickersWidget.itemSelectionChanged.connect(on_ticker_selection_changed)
    
    # --- manage SETUP SELECTION
    def on_setup_selection_changed():
        selected_item = ui.list_of_setupWidget.selectedItems()
        parameters.indicator_setup = selected_item[0].text()

    ui.list_of_setupWidget.addItem('Base setup')

    ui.list_of_setupWidget.itemSelectionChanged.connect(on_setup_selection_changed)
    ui.list_of_setupWidget.setCurrentRow(0)

    # --- manage DATE SELECTION
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

        hide_widgets(ui.candlestick_layout)
        hide_widgets(ui.histogram_layout)

        parameters.projection_date = ui.dateEdit_end.date()

        if parameters.projection_date.dayOfWeek() == 6:
            show_message(f"{parameters.projection_date.toString('yyyy. MM. dd.')} is Saturday, projection will be made for next working day!")
            last_base_date = parameters.projection_date.addDays(-1)
            parameters.projection_date = parameters.projection_date.addDays(2)
        elif parameters.projection_date.dayOfWeek() == 7:
            show_message(f"{parameters.projection_date.toString('yyyy. MM. dd.')} is Sunday, projection will be made for next working day!")
            last_base_date = parameters.projection_date.addDays(-2)
            parameters.projection_date = parameters.projection_date.addDays(1)
        elif parameters.projection_date.dayOfWeek() == 1:
            last_base_date = parameters.projection_date.addDays(-3)
        else:
            last_base_date = parameters.projection_date.addDays(-1)

        last_base_date = last_base_date.toString('yyyy-MM-dd')
        
        ui.statusbar.addWidget(ui.label_progress)
        ui.label_progress.show()
        ui.statusbar.addWidget(ui.progress_bar)
        ui.progress_bar.setValue(0)
        ui.progress_bar.show()
        QtWidgets.QApplication.processEvents()

        success, candles_for_chart, median_highchg, median_lowchg, chartwithfact, next_day_chg_dict = main_engine(ui.progress_bar, ticker=parameters.ticker, date=last_base_date, chartwithfact=True)      
        # print(success)
        # print(candles_for_chart)
        # print(median_highchg)
        # print(median_lowchg)
        # print(chartwithfact)
        # print(next_day_chg_dict)

        if success[0]:
            candlestick_chart = CandlestickChart(candles_for_chart, parameters.ticker, parameters.projection_date.toString('yyyy-MM-dd'), projection={'Lowchg': median_lowchg, 'Highchg': median_highchg},
                                                chartwithfact=chartwithfact, parent=ui.workplaceLayoutWidget)          
            histogram_chart = HistogramChart(parameters.projection_date.toString('yyyy-MM-dd'), parameters.ticker, Lowchg=next_day_chg_dict['Lowchg'], Highchg=next_day_chg_dict['Highchg'])
            ui.candlestick_layout.addWidget(candlestick_chart)
            candlestick_chart.show()
            ui.histogram_layout.addWidget(histogram_chart)
            histogram_chart.show()
            ui.tabs.setCurrentIndex(2)
            ui.progress_bar.hide()
            ui.label_progress.hide()
        else:
            show_message(success[1])
            ui.progress_bar.hide()
            ui.label_progress.hide()

    ui.pushButton.clicked.connect(start_main_engine)

    MainWindow.show()
    sys.exit(app.exec())
    