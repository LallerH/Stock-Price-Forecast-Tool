import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from multiprocessing import Process

def set_window_icon(fig, icon_path):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    icon = ImageTk.PhotoImage(Image.open(icon_path))
    fig.canvas.get_tk_widget().winfo_toplevel().iconphoto(False, icon)
    root.destroy()

def show_histogram(date: str, **kwargs):
    """
    :Show histogram and box plot for projected changes of LOW and HIGH value data
    
    :Parameters:
        date : 'str'; date to be shown in title
        Lowchg and/or Highchg : [list]; kwargs; which data array to be shown
    """
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

    bins = np.arange(round(min(all_data),3)-0.001, round(max(all_data),3)+0.002, 0.001)

    fig = plt.figure()
    fig.canvas.toolbar.pack_forget()
    fig.canvas.manager.set_window_title('Histogram and Box plot')
    set_window_icon(fig, 'ikon.ico')
    fig.suptitle('Possible changes of S&P 500 LOW and HIGH price for the day after '+date)

    if len(kwargs) == 2:
        fig.set_figheight(6)
        fig.set_figwidth(10)

        plt.subplot(2, 2, 1)
        hist_n = plt.hist(Lowchg_data, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.title('Low change - Distribution')
        plt.xticks(bins, rotation=90)
        plt.yticks(np.arange(1,max(hist_n[0])+1,1))

        plt.subplot(2, 2, 3)
        box = plt.boxplot(Lowchg_data, 0, 'rs', 0, patch_artist=True)
        plt.setp(box['boxes'], facecolor='skyblue')
        plt.setp(box['medians'], color='red')  
        plt.xlabel('Values')
        plt.yticks([])
        plt.title('Low change - Box plot')
        plt.xticks(bins, rotation=90)

        plt.subplot(2, 2, 2)
        hist_n = plt.hist(Highchg_data, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.title('High change - Distribution')
        plt.xticks(bins, rotation=90)
        plt.yticks(np.arange(1,max(hist_n[0])+1,1))

        plt.subplot(2, 2, 4)
        box = plt.boxplot(Highchg_data, 0, 'rs', 0, patch_artist=True)
        plt.setp(box['boxes'], facecolor='skyblue')
        plt.setp(box['medians'], color='red')  
        plt.xlabel('Values')
        plt.yticks([])
        plt.title('High change - Box plot')
        plt.xticks(bins, rotation=90)
        
        plt.tight_layout(pad=2)
    else:
        fig.set_figheight(6)
        fig.set_figwidth(6)
        
        plt.subplot(2, 1, 1)
        hist_n = plt.hist(data, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.title(title1)
        plt.xticks(bins, rotation=90)
        plt.yticks(np.arange(1,max(hist_n[0])+1,1))

        plt.subplot(2, 1, 2)
        box = plt.boxplot(data, 0, 'rs', 0, patch_artist=True)
        plt.setp(box['boxes'], facecolor='skyblue')
        plt.setp(box['medians'], color='red')  
        plt.xlabel('Values')
        plt.yticks([])
        plt.title(title2)
        plt.xticks(bins, rotation=90)

        plt.tight_layout(pad=2)

    plt.show()

def show_candle_chart(stock_data: dict, projection = None):
    """
    :Show candle chart
    
    :Parameters:
        stock_data : {dict}; returned by get_candle_from_df methods
        projection : {'Lowchg': int, 'Highchg': int}; 
    """
    fig = plt.figure()
    fig.canvas.toolbar.pack_forget()
    fig.canvas.manager.set_window_title('Japanese candle chart')
    set_window_icon(fig, 'ikon.ico')
    fig.suptitle('S&P 500 chart')

    indexes = list(stock_data['Date'].keys())
    indexes.sort()

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
        fig.suptitle('S&P 500 chart with LOW and HIGH price projection')

        if height >= 0:
            plt.bar('Next period', height, 0.3, bottom, edgecolor='black', fill = False, hatch='\\')
            plt.text('Next period', bottom-5, str(round(bottom)), ha='center')
            plt.text('Next period', bottom+height+2, str(round(bottom+height)), ha='center')
            x_values = range(len(indexes)+1)
        else:
            plt.bar('Next period', height_body, 0.3, bottom_body, edgecolor='white', fill = False)
            bottom, top = plt.ylim()
            plt.text('Next period', (bottom+top)/2, 'n.a.', ha='center')
            x_values = range(len(indexes)+1)

    plt.xlim(x_values[0] - 0.5, x_values[-1] + 0.5)
    bottom, top = plt.ylim()
    plt.ylim(bottom*0.998, top*1.002)
    plt.show()

def show_all_charts(stock_data: dict, date: str, Lowchg: list, Highchg: list, projection=None):
    """
    :Show histogram/box plot and candle chart for projected changes of LOW and HIGH value data in two separated windows
    
    :Parameters:
        stock_data : {dict}; returned by get_candle_from_df methods
        date : 'str'; date to be shown in title of histogram/box plot
        Lowchg and/or Highchg : [list]; kwargs; which data array to be shown
        projection : {'Lowchg': int, 'Highchg': int}; 
    """

    histogram_process = Process(target=show_histogram, args=(date,), kwargs={'Lowchg': Lowchg, 'Highchg': Highchg})
    candle_chart_process = Process(target=show_candle_chart, args=(stock_data,), kwargs={'projection': projection})
    
    histogram_process.start()
    candle_chart_process.start()
    histogram_process.join()
    candle_chart_process.join()


if __name__ == '__main__':
    from database_manager import get_candles_from_df, get_data_from_mongodb

    Lowchg = [0.9996554912124962, 0.9958912528506714, 1.00448931540741, 0.9982181758349802, 1.0029118277535642, 1.0012103609429495, 1.0003555293541195, 1.00986476231454, 0.9955466190771032, 1.004226864695291, 1.002761470327116, 1.000041061493693, 1.0372261654256407, 0.9932368456496866, 0.9935887890282025]
    Highchg = [0.9960764321660329, 1.0020689851767919, 1.0012057667356538, 0.9928610438680883, 1.0002006310175175, 0.9949739542058338, 0.9973874497383509, 1.009752270884467, 0.9964499496773966, 1.0055059913757989, 1.0020899694486982, 0.9929869651965559, 1.0239271700303225, 0.9910996187996407, 0.9951449353133529]
    stock_df = get_data_from_mongodb()
    candles_for_chart = get_candles_from_df(stock_df, date='2024-05-30', period=4)
    
    show_all_charts(candles_for_chart, '2024-05-30', Lowchg=Lowchg, Highchg=Highchg, projection={'Lowchg': 1.05, 'Highchg': 0.99})
   
