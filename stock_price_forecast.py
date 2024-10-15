import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from utils import Ui_MainWindow, main_engine, get_collections_from_mongodb, Parameters, get_first_correct_date, CandlestickChart

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
        
        def show_message(text):
            message_box = QMessageBox()
            message_box.setWindowIcon(QIcon('ikon.ico'))
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setWindowTitle("Projection date info")
            message_box.setText(text)
            message_box.exec()           

        parameters.projection_date = ui.dateEdit_end.date()

        if parameters.projection_date.dayOfWeek() == 6:
            show_message(f"{parameters.projection_date.toString('yyyy. MM. dd.')} is Saturday, projection will be made for next working day!")
            last_base_date = parameters.projection_date.addDays(-1)
        elif parameters.projection_date.dayOfWeek() == 7:
            show_message(f"{parameters.projection_date.toString('yyyy. MM. dd.')} is Sunday, projection will be made for next working day!")
            last_base_date = parameters.projection_date.addDays(-2)
        elif parameters.projection_date.dayOfWeek() == 1:
            last_base_date = parameters.projection_date.addDays(-3)
        else:
            last_base_date = parameters.projection_date.addDays(-1)

        last_base_date = last_base_date.toString('yyyy-MM-dd')
        candles_for_chart, median_highchg, median_lowchg = main_engine(ticker=parameters.ticker, date=last_base_date)      
        # candles_for_chart = {'Date': {24308: '2024-10-08', 24309: '2024-10-09', 24310: '2024-10-10', 24311: '2024-10-11'}, 'Open': {24308: 5719.14013671875, 24309: 5751.7998046875, 24310: 5778.35986328125, 24311: 5775.08984375}, 'High': {24308: 5757.60009765625, 24309: 5796.7998046875, 24310: 5795.02978515625, 24311: 5822.1298828125}, 'Low': {24308: 5714.56005859375, 24309: 5745.02001953125, 24310: 5764.759765625, 24311: 5775.08984375}, 'Close': {24308: 5751.1298828125, 24309: 5792.0400390625, 24310: 5780.0498046875, 24311: 5815.02978515625}, 'Volume': {24308: 3393400000, 24309: 3650340000, 24310: 3208790000, 24311: 3208720000}, 'RSI': {24308: 60.37452529959091, 24309: 63.81031751097014, 24310: 62.19211081518803, 24311: 65.12220261954819}, 'RSIavg': {24308: 61.44269895314572, 24309: 61.148276979436076, 24310: 60.92436451499597, 24311: 60.668950130783074}, 'MACD': {24308: 53.413354176355824, 24309: 55.95209999780673, 24310: 56.32073547858454, 24311: 58.683032380746226}, 'MACDhist': {24308: -6.627532334037525, 24309: -3.364760170965539, 24310: -2.4194047127406435, 24311: -0.04568624846316993}, 'MACDavg': {24308: 60.04088651039335, 24309: 59.316860168772266, 24310: 58.74014019132518, 24311: 58.728718629209396}, 'SMA20': {24308: 5690.708935546875, 24309: 5702.604443359375, 24310: 5711.8189453125, 24311: 5721.26943359375}, 'SMA50': {24308: 5564.42078125, 24309: 5571.532783203125, 24310: 5576.687783203125, 24311: 5584.054775390625}}
        # median_highchg = 1.0015765079466905
        # median_lowchg = 1.0029128343522764
        candlestick_chart = CandlestickChart(candles_for_chart, parameters.ticker, parameters.projection_date.toString('yyyy. MM. dd.'), projection={'Lowchg': median_lowchg, 'Highchg': median_highchg},
                                            chartwithfact=True, parent=ui.workplaceLayoutWidget)

        ui.candlestick_layout.addWidget(candlestick_chart)
        candlestick_chart.show()
        ui.tabs.setCurrentIndex(2)


    ui.pushButton.clicked.connect(start_main_engine)

    MainWindow.show()
    sys.exit(app.exec())
    