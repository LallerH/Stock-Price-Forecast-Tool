import sys
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class CandlestickChart(QWidget):
    def __init__(self, stock_data: dict, ticker: str, date: str, projection = None, chartwithfact = False, parent=None):
        """
        :Show candlestick chart
        
        :Parameters:
            stock_data : {dict}; returned by get_candle_from_df methods
            ticker: 'str'; stock name to be shown in title
            date: 'str'; date to be shown in title
            projection : {'Lowchg': int, 'Highchg': int};
            chartwithfact : bool; True -> sets a fact candle after projection candle
        """
        super().__init__(parent)
        
        self.fig = plt.figure()
        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        indexes = list(stock_data['Date'].keys())
        indexes.sort()
        if chartwithfact:
            factindex = indexes[-1]
            indexes = indexes[:-1]

        for idx in indexes:
            if stock_data['Close'][idx] >= stock_data['Open'][idx]:
                x_coordinate = stock_data['Date'][idx]
                height_top = stock_data['High'][idx] - stock_data['Close'][idx]
                height_body = stock_data['Close'][idx] - stock_data['Open'][idx]
                height_bottom = stock_data['Open'][idx] - stock_data['Low'][idx]
                color = 'green'
                bottom_top = stock_data['Close'][idx]
                bottom_body = stock_data['Open'][idx]
                bottom_bottom = stock_data['Low'][idx]
            else:
                x_coordinate = stock_data['Date'][idx]
                height_top = stock_data['High'][idx] - stock_data['Open'][idx]
                height_body = stock_data['Open'][idx] - stock_data['Close'][idx]
                height_bottom = stock_data['Close'][idx] - stock_data['Low'][idx]
                color = 'red'
                bottom_top = stock_data['Open'][idx]
                bottom_body = stock_data['Close'][idx]
                bottom_bottom = stock_data['Low'][idx]
            
            plt.bar(x_coordinate, height_top, 0.02, bottom_top, color='black')
            plt.bar(x_coordinate, height_body, 0.3, bottom_body, color=color)
            plt.bar(x_coordinate, height_bottom, 0.02, bottom_bottom, color='black')

        x_values = range(len(indexes))

        if projection:
            height = stock_data['High'][indexes[-1]] * projection['Highchg'] - stock_data['Low'][indexes[-1]] * projection['Lowchg']
            bottom = stock_data['Low'][indexes[-1]] * projection['Lowchg']
            self.fig.suptitle(f'{ticker} chart with LOW and HIGH price projection\n for the day after {date}')

            if height >= 0:
                plt.bar('Projection', height, 0.3, bottom, edgecolor='black', fill = False, hatch='\\')
                plt.text('Projection', bottom*0.9994, str(round(bottom)), ha='center', va='top')
                plt.text('Projection', (bottom+height)*1.0005, str(round(bottom+height)), ha='center')
            else:
                plt.bar('Projection', height_body, 0.3, bottom_body, edgecolor='white', fill = False)
                bottom, top = plt.ylim()
                plt.text('Projection', (bottom+top)/2, 'n.a.', ha='center')

        if chartwithfact:
            if stock_data['Close'][factindex] >= stock_data['Open'][factindex]:
                x_coordinate = (f'{date} fact')
                height_top = stock_data['High'][factindex] - stock_data['Close'][factindex]
                height_body = stock_data['Close'][factindex] - stock_data['Open'][factindex]
                height_bottom = stock_data['Open'][factindex] - stock_data['Low'][factindex]
                color = 'green'
                bottom_top = stock_data['Close'][factindex]
                bottom_body = stock_data['Open'][factindex]
                bottom_bottom = stock_data['Low'][factindex]
            else:
                x_coordinate = (f'{date} fact')
                height_top = stock_data['High'][factindex] - stock_data['Open'][factindex]
                height_body = stock_data['Open'][factindex] - stock_data['Close'][factindex]
                height_bottom = stock_data['Close'][factindex] - stock_data['Low'][factindex]
                color = 'red'
                bottom_top = stock_data['Open'][factindex]
                bottom_body = stock_data['Close'][factindex]
                bottom_bottom = stock_data['Low'][factindex]
            
            plt.bar(x_coordinate, height_top, 0.02, bottom_top, color='black')
            plt.bar(x_coordinate, height_body, 0.3, bottom_body, color=color)
            plt.bar(x_coordinate, height_bottom, 0.02, bottom_bottom, color='black')

        if projection and chartwithfact:
            x_values = range(len(indexes)+2)
        elif projection or chartwithfact:
            x_values = range(len(indexes)+1)

        plt.xlim(x_values[0] - 0.5, x_values[-1] + 0.5)
        bottom, top = plt.ylim()
        plt.ylim(bottom*0.997, top*1.002)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    candles_for_chart = {'Date': {24308: '2024-10-08', 24309: '2024-10-09', 24310: '2024-10-10', 24311: '2024-10-11'}, 'Open': {24308: 5719.14013671875, 24309: 5751.7998046875, 24310: 5778.35986328125, 24311: 5775.08984375}, 'High': {24308: 5757.60009765625, 24309: 5796.7998046875, 24310: 5795.02978515625, 24311: 5822.1298828125}, 'Low': {24308: 5714.56005859375, 24309: 5745.02001953125, 24310: 5764.759765625, 24311: 5775.08984375}, 'Close': {24308: 5751.1298828125, 24309: 5792.0400390625, 24310: 5780.0498046875, 24311: 5815.02978515625}, 'Volume': {24308: 3393400000, 24309: 3650340000, 24310: 3208790000, 24311: 3208720000}, 'RSI': {24308: 60.37452529959091, 24309: 63.81031751097014, 24310: 62.19211081518803, 24311: 65.12220261954819}, 'RSIavg': {24308: 61.44269895314572, 24309: 61.148276979436076, 24310: 60.92436451499597, 24311: 60.668950130783074}, 'MACD': {24308: 53.413354176355824, 24309: 55.95209999780673, 24310: 56.32073547858454, 24311: 58.683032380746226}, 'MACDhist': {24308: -6.627532334037525, 24309: -3.364760170965539, 24310: -2.4194047127406435, 24311: -0.04568624846316993}, 'MACDavg': {24308: 60.04088651039335, 24309: 59.316860168772266, 24310: 58.74014019132518, 24311: 58.728718629209396}, 'SMA20': {24308: 5690.708935546875, 24309: 5702.604443359375, 24310: 5711.8189453125, 24311: 5721.26943359375}, 'SMA50': {24308: 5564.42078125, 24309: 5571.532783203125, 24310: 5576.687783203125, 24311: 5584.054775390625}}
    median_highchg = 1.0015765079466905
    median_lowchg = 1.0029128343522764

    chart = CandlestickChart(candles_for_chart, 'S&P', '2024-10-14', projection={'Lowchg': median_lowchg, 'Highchg': median_highchg})
    chart.show()
    app.exec()

