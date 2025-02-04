import sys
import pandas as pd
import numpy as np
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
            self.fig.suptitle(f'{ticker} chart with LOW and HIGH price projection\n for the day {date}')

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
                x_coordinate = ('Fact')
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

class HistogramChart(QWidget):
    def __init__(self, date: str, ticker: str, **kwargs):
        """
        :Show histogram and box plot for projected changes of LOW and HIGH value data
        
        :Parameters:
            date : 'str'; date to be shown in title
            ticker: 'str'; stock name to be shown in title
            Lowchg and/or Highchg : [list]; kwargs; which data array to be shown
        """
        parent=None
        super().__init__(parent)

        if kwargs.get('Lowchg') and kwargs.get('Highchg'):
            Lowchg_data = kwargs['Lowchg']
            Highchg_data = kwargs['Highchg']
            all_data = kwargs['Lowchg'] + kwargs['Highchg']
        elif kwargs.get('Lowchg'):
            data = kwargs['Lowchg']
            all_data = kwargs['Lowchg']
            title1 = 'Low change - Distribution'
            title2 = 'Low change - Box plot'
        elif kwargs.get('Highchg'):
            data = kwargs['Highchg']
            all_data = kwargs['Highchg']
            title1 = 'High change - Distribution'
            title2 = 'High change - Box plot'
        else:
            raise Exception('No arguments were given! Lowchg and/or Highchg list are waited as key world arguments!')

        self.fig = plt.figure()
        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.fig.suptitle(f'Possible changes of {ticker} LOW and HIGH price for the day {date}')

        bins = np.arange(round(min(all_data),3)-0.001, round(max(all_data),3)+0.002, 0.001)
        num_bins = len(bins)
        n = max(1, num_bins // 30)

        if len(kwargs) == 2:
            self.fig.set_figheight(6)
            self.fig.set_figwidth(10)

            plt.subplot(2, 2, 1)
            hist_n1 = plt.hist(Lowchg_data, bins=bins, color='skyblue', edgecolor='black')
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.title('Low change - Distribution')
            plt.xticks(bins[::n], rotation=90, fontsize=8)
            plt.yticks(np.arange(1,max(hist_n1[0])+1,1))

            plt.subplot(2, 2, 3)
            box = plt.boxplot(Lowchg_data, 0, 'rs', 0, patch_artist=True)
            plt.setp(box['boxes'], facecolor='skyblue')
            plt.setp(box['medians'], color='red')  
            plt.xlabel('Values')
            plt.yticks([])
            plt.title('Low change - Box plot')
            plt.xticks(bins[::n], rotation=90, fontsize=8)

            plt.subplot(2, 2, 2)
            hist_n2 = plt.hist(Highchg_data, bins=bins, color='skyblue', edgecolor='black')
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.title('High change - Distribution')
            plt.xticks(bins[::n], rotation=90, fontsize=8)
            plt.yticks(np.arange(1,max(hist_n2[0])+1,1))

            plt.subplot(2, 2, 4)
            box = plt.boxplot(Highchg_data, 0, 'rs', 0, patch_artist=True)
            plt.setp(box['boxes'], facecolor='skyblue')
            plt.setp(box['medians'], color='red')  
            plt.xlabel('Values')
            plt.yticks([])
            plt.title('High change - Box plot')
            plt.xticks(bins[::n], rotation=90, fontsize=8)
            
            plt.tight_layout(pad=2)
        else:
            self.fig.set_figheight(6)
            self.fig.set_figwidth(6)
            
            plt.subplot(2, 1, 1)
            hist_n = plt.hist(data, bins=bins, color='skyblue', edgecolor='black')
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.title(title1)
            plt.xticks(bins[::n], rotation=90, fontsize=8)
            plt.yticks(np.arange(1,max(hist_n[0])+1,1))

            plt.subplot(2, 1, 2)
            box = plt.boxplot(data, 0, 'rs', 0, patch_artist=True)
            plt.setp(box['boxes'], facecolor='skyblue')
            plt.setp(box['medians'], color='red')  
            plt.xlabel('Values')
            plt.yticks([])
            plt.title(title2)
            plt.xticks(bins[::n], rotation=90, fontsize=8)

            plt.tight_layout(pad=2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    candles_for_chart = {'Date': {24308: '2024-10-08', 24309: '2024-10-09', 24310: '2024-10-10', 24311: '2024-10-11'}, 'Open': {24308: 5719.14013671875, 24309: 5751.7998046875, 24310: 5778.35986328125, 24311: 5775.08984375}, 'High': {24308: 5757.60009765625, 24309: 5796.7998046875, 24310: 5795.02978515625, 24311: 5822.1298828125}, 'Low': {24308: 5714.56005859375, 24309: 5745.02001953125, 24310: 5764.759765625, 24311: 5775.08984375}, 'Close': {24308: 5751.1298828125, 24309: 5792.0400390625, 24310: 5780.0498046875, 24311: 5815.02978515625}, 'Volume': {24308: 3393400000, 24309: 3650340000, 24310: 3208790000, 24311: 3208720000}, 'RSI': {24308: 60.37452529959091, 24309: 63.81031751097014, 24310: 62.19211081518803, 24311: 65.12220261954819}, 'RSIavg': {24308: 61.44269895314572, 24309: 61.148276979436076, 24310: 60.92436451499597, 24311: 60.668950130783074}, 'MACD': {24308: 53.413354176355824, 24309: 55.95209999780673, 24310: 56.32073547858454, 24311: 58.683032380746226}, 'MACDhist': {24308: -6.627532334037525, 24309: -3.364760170965539, 24310: -2.4194047127406435, 24311: -0.04568624846316993}, 'MACDavg': {24308: 60.04088651039335, 24309: 59.316860168772266, 24310: 58.74014019132518, 24311: 58.728718629209396}, 'SMA20': {24308: 5690.708935546875, 24309: 5702.604443359375, 24310: 5711.8189453125, 24311: 5721.26943359375}, 'SMA50': {24308: 5564.42078125, 24309: 5571.532783203125, 24310: 5576.687783203125, 24311: 5584.054775390625}}
    median_highchg = 1.0015765079466905
    median_lowchg = 1.0029128343522764
    lowchg = [0.9910824993110049, 1.0032765247597832, 1.0049642272763502, 0.9990066182535793, 0.994204266536603, 1.0080124509316308, 1.00176443389618, 0.9989678935058213, 1.0078936223080412, 0.9993946049567247, 0.9987408545421277, 1.0059357866192433, 1.0148133518407494, 1.0134568234515353, 0.996713637655329, 1.037652370057351, 1.0116830843041766, 1.0312715135078752, 1.0094276336088106, 1.0107838889059195, 1.0118638322567628, 0.991884511619201, 1.000879450241674, 0.9976485355095779, 1.013422115278686, 0.9827764824824333, 1.035322819118646, 0.9892460739401969, 1.0118344149340652, 1.0136099187401555, 1.0118543009467729, 1.0101011469935999, 1.0075330346890068, 1.0069027078533657, 1.0038698358815608, 1.0024686660260105, 0.992854988738274, 1.0090854235527842, 1.0028643234041201, 0.9990329770820658, 1.0082725423540853, 1.002546437632575, 0.9962034374448335, 1.001408506588344, 1.0008159893883481, 0.9923535481916569, 1.0237449574135764, 0.994584720664965, 1.0098552013644204, 1.002447381302007, 1.0106014268900645, 1.0120640747047167, 1.0105651675300116, 1.0049756631357472, 0.9975297323822852, 1.015729199709386, 1.0066754745308244, 1.0336762860680198, 1.0239115801992758, 0.9969283999909773, 1.0045811578545496, 1.00255999314175, 1.0042783298808056, 0.9985362468708403, 0.993396338354464, 1.0002575817135697, 0.9946414663853756, 1.0106683441765614, 1.0058417573852083, 1.0079335772025557]
    highchg = [1.003230419754443, 0.9970479927257101, 1.0038075694517978, 1.0013208689169961, 0.9962148490670927, 1.0040818192272694, 1.0016451303754277, 1.0098101356912121, 1.0057141874056852, 0.9937978193529686, 0.9994180954458753, 0.9968462036563072, 0.9963628721208869, 1.0054444177793842, 1.0169765401195954, 1.0057555883681086, 1.0167559563362492, 1.0119890494421802, 1.0064676070148482, 1.0064875793550419, 1.0046319569073934, 0.9972162916813766, 0.9925166772058889, 0.9983289050425604, 1.003273706298257, 0.9817081515722615, 1.0107149983294974, 1.0022614667144065, 1.0022645026546673, 1.017485931877231, 1.0131357791675986, 1.011298038529696, 0.9981902099810025, 1.0016070987149508, 1.008443760637977, 0.9997790741189814, 1.000981870094182, 0.9964715692346751, 1.0035164845582993, 0.9967735947598222, 1.0143650994273161, 1.001245337283162, 0.9970982461349749, 1.0008994284689097, 1.003962790670816, 0.9951646069039042, 1.012150486984083, 0.9903648025504186, 1.0048232806373603, 1.001105857371515, 1.0061097700928197, 1.007216322871054, 1.0020611609885646, 0.9957289052578511, 0.9946622639194476, 1.0114333811924534, 1.0003096780066603, 1.0159984264654571, 1.0374797568292147, 0.9942869419648879, 1.0025209821842553, 1.0002638604275278, 0.996985580955088, 0.9977571348135124, 1.0, 1.003899907931769, 0.9923828645394354, 1.0039444513044316, 1.007060268149581, 1.0124063004561366]

    # chart = CandlestickChart(candles_for_chart, 'S&P', '2024-10-14', projection={'Lowchg': median_lowchg, 'Highchg': median_highchg})
    chart = HistogramChart('2024-10-14', 'S&P', Lowchg=lowchg, Highchg=highchg)
    
    chart.show()
    app.exec()

