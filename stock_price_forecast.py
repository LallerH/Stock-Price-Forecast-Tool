import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from utils import Ui_MainWindow, IndicatorSetup_Form, main_engine, get_stock_collections_from_mongodb,\
                  Parameters, get_first_correct_date, CandlestickChart, HistogramChart, show_message, hide_widgets,\
                  check_stock_database_in_mongodb, initial_upload_of_stock_database, write_indicator_setup,\
                  initialize_indicator_setup_database, check_indicator_setup_database, input_text, get_indicator_setups_from_mongodb,\
                  load_indicator_setup, delete_indicator_setup

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

    if not check_stock_database_in_mongodb(database = 'Stock_data'):
        show_message('Click to start the initial setup of database!')
        print('Downloading...')
        try:
            initial_upload_of_stock_database(database = 'Stock_data')
            show_message('Initial setup of database succeded!\nInitial download of S&P, DAX and NASDAQ indexes succeeded!')
        except:
            show_message('Initial setup of database was not succeeded!\nRequired:\n- database manager MongoDB (mongodb://localhost:27017)\n- internet connection')
            sys.exit(app.exec())

    if get_stock_collections_from_mongodb():
        list_of_tickers = sorted(get_stock_collections_from_mongodb(), key=str.casefold)
        ui.list_of_tickersWidget.addItems(list_of_tickers)
    else:
        print('Downloading...')
        try:
            initial_upload_of_stock_database(database = 'Stock_data')
            show_message('Initial setup of database succeded!\nInitial download of S&P, DAX and NASDAQ indexes succeeded!')
        except:
            show_message('Initial setup of database was not succeeded!\nRequired:\n- database manager MongoDB (mongodb://localhost:27017)\n- internet connection')
            sys.exit(app.exec())

    ui.list_of_tickersWidget.itemSelectionChanged.connect(on_ticker_selection_changed)
    
    # --- manage INDICATOR SETUP SELECTION
    def on_setup_selection_changed():
        selected_item = ui.list_of_setupWidget.selectedItems()
        if selected_item:
            parameters.indicator_setup = load_indicator_setup(selected_item[0].text())
            indicator_form.set_indicator_setup_on_screen(parameters.indicator_setup)

    def clear_selection():
        ui.list_of_setupWidget.itemSelectionChanged.disconnect()
        ui.list_of_setupWidget.clearSelection()
        ui.list_of_setupWidget.setCurrentRow(-1)
        ui.list_of_setupWidget.itemSelectionChanged.connect(on_setup_selection_changed)

    def saveas_to_mongodb():
        status, text = input_text()
        list_of_indicator_setups = sorted(get_indicator_setups_from_mongodb(), key=str.casefold)
        if status == 1 and text != '' and (text not in list_of_indicator_setups):
            setup = indicator_form.get_indicator_setup()
            setup['name'] = text
            write_indicator_setup(setup)
            list_of_indicator_setups = sorted(get_indicator_setups_from_mongodb(), key=str.casefold)
            ui.list_of_setupWidget.clear()
            ui.list_of_setupWidget.addItems(list_of_indicator_setups)
            item = ui.list_of_setupWidget.findItems(text, Qt.MatchFlag.MatchExactly)
            ui.list_of_setupWidget.setCurrentItem(item[0])
            show_message(f'{text} indicator setup has been saved!')
        elif status == 1 and text == '' and (text not in list_of_indicator_setups):
            show_message('No SETUP NAME was given, setup was not saved!')
        elif (text in list_of_indicator_setups):
            show_message('SETUP NAME already exists, setup was not saved!')
        
    def overwrite_in_mongodb():
        setup = indicator_form.get_indicator_setup()
        selected_item = ui.list_of_setupWidget.currentItem()
        if selected_item:
            setup['name'] = selected_item.text()
            
            delete_indicator_setup(selected_item.text())
            ui.list_of_setupWidget.takeItem(ui.list_of_setupWidget.row(selected_item))

            write_indicator_setup(setup)
            list_of_indicator_setups = sorted(get_indicator_setups_from_mongodb(), key=str.casefold)
            ui.list_of_setupWidget.clear()
            ui.list_of_setupWidget.addItems(list_of_indicator_setups)
            items = ui.list_of_setupWidget.findItems(selected_item.text(), Qt.MatchFlag.MatchExactly)
            ui.list_of_setupWidget.setCurrentItem(items[0])

            show_message(f'{selected_item.text()} indicator setup has been updated!')
        
        else:
            saveas_to_mongodb()

    def delete_in_mongodb():
        selected_item = ui.list_of_setupWidget.currentItem()
        delete_indicator_setup(selected_item.text())
        ui.list_of_setupWidget.takeItem(ui.list_of_setupWidget.row(selected_item))

    if check_indicator_setup_database() == False:
        initialize_indicator_setup_database()

    list_of_indicator_setups = sorted(get_indicator_setups_from_mongodb(), key=str.casefold)
    ui.list_of_setupWidget.addItems(list_of_indicator_setups)

    indicators = QtWidgets.QWidget()
    indicator_form = IndicatorSetup_Form()
    indicator_form.setupUi(indicators)
    ui.indicator_layout.addWidget(indicators)
    
    ui.list_of_setupWidget.setCurrentRow(0)
    selected_item = ui.list_of_setupWidget.selectedItems()
    parameters.indicator_setup = load_indicator_setup(selected_item[0].text())
    indicator_form.set_indicator_setup_on_screen(parameters.indicator_setup)
    ui.list_of_setupWidget.itemSelectionChanged.connect(on_setup_selection_changed)

    indicator_form.pushButton_indicator_reset.clicked.connect(indicator_form.reset_indicator_widgets)
    indicator_form.pushButton_indicator_reset.clicked.connect(clear_selection)
    indicator_form.pushButton_indicator_saveas.clicked.connect(saveas_to_mongodb)
    indicator_form.pushButton_indicator_save.clicked.connect(overwrite_in_mongodb)
    indicator_form.pushButton_indicator_delete.clicked.connect(delete_in_mongodb)

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
        parameters.first_base_date = ui.dateEdit_start.date()

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
        first_base_date = parameters.first_base_date.toString('yyyy-MM-dd')

        ui.statusbar.addWidget(ui.label_progress)
        ui.label_progress.show()
        ui.statusbar.addWidget(ui.progress_bar)
        ui.progress_bar.setValue(0)
        ui.progress_bar.show()
        QtWidgets.QApplication.processEvents()

        success, candles_for_chart, median_highchg, median_lowchg, chartwithfact, next_day_chg_dict =\
        main_engine(ui.progress_bar, ticker=parameters.ticker, first_base_date=first_base_date, last_base_date=last_base_date, chartwithfact=True)      

        if success[0]:
            candlestick_chart = CandlestickChart(candles_for_chart, parameters.ticker, parameters.projection_date.toString('yyyy-MM-dd'), projection={'Lowchg': median_lowchg, 'Highchg': median_highchg},
                                                chartwithfact=chartwithfact)          
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
    