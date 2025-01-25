from utils import get_first_correct_date, get_stock_data_from_mongodb, Parameters, main_engine
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    def show_histogram(period: str, ticker: str, lowchg_data: list, highchg_data: list):
        all_data = lowchg_data + highchg_data

        bins = np.arange(round(min(all_data),3)-0.001, round(max(all_data),3)+0.002, 0.001)

        fig = plt.figure()
        fig.canvas.manager.set_window_title('Histogram and Box plot')
        fig.suptitle(f'Deviation of price forecast from fact data of {ticker} in the period {period}')

        fig.set_figheight(6)
        fig.set_figwidth(10)

        plt.subplot(2, 2, 1)
        hist_n = plt.hist(lowchg_data, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel('Deviation')
        plt.ylabel('Frequency')
        plt.title('Low change deviation - Distribution')
        plt.xticks(bins, rotation=90)
        plt.yticks(np.arange(1,max(hist_n[0])+1,1))

        plt.subplot(2, 2, 3)
        box = plt.boxplot(lowchg_data, 0, 'rs', 0, patch_artist=True)
        plt.setp(box['boxes'], facecolor='skyblue')
        plt.setp(box['medians'], color='red')  
        plt.xlabel('Deviation')
        plt.yticks([])
        plt.title('Low change deviation - Box plot')
        plt.xticks(bins, rotation=90)

        plt.subplot(2, 2, 2)
        hist_n = plt.hist(highchg_data, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel('Deviation')
        plt.ylabel('Frequency')
        plt.title('High change deviation - Distribution')
        plt.xticks(bins, rotation=90)
        plt.yticks(np.arange(1,max(hist_n[0])+1,1))

        plt.subplot(2, 2, 4)
        box = plt.boxplot(highchg_data, 0, 'rs', 0, patch_artist=True)
        plt.setp(box['boxes'], facecolor='skyblue')
        plt.setp(box['medians'], color='red')  
        plt.xlabel('Deviation')
        plt.yticks([])
        plt.title('High change deviation - Box plot')
        plt.xticks(bins, rotation=90)
        
        plt.tight_layout(pad=2)

        plt.show()

    parameters = Parameters()
    parameters.ticker = '^GDAXI'
    parameters.first_base_date = get_first_correct_date(coll=parameters.ticker)[1]
    parameters.indicator_setup = {
        'name' : 'Base setup',
        'days' : 2,
        'lowchg' : {'selected' : True, 'tolerance': 70},
        'openchg' : {'selected' : True, 'tolerance': 70},
        'highchg' : {'selected' : True, 'tolerance': 70},
        'body' : {'selected' : True, 'tolerance': 70},
        'color' : {'selected' : True, 'tolerance': False},
        'RSIavgchg' : {'selected' : False, 'tolerance': 100},
        'RSIstate' : {'selected' : True, 'tolerance': False},
        'MACDhistchg' : {'selected' : True, 'tolerance': 8},
        'MACDrange' : {'selected' : False, 'tolerance': False},
        'SMA20chg' : {'selected' : False, 'tolerance': 10},
        'SMA50chg' : {'selected' : False, 'tolerance': 4},
        'SMA20_50relation' : {'selected' : False, 'tolerance': False}
    }

    model_period_first_date = '2025-01-22' # first projection date of model period
    model_period_last_date = '2025-01-23' # last projection date of model period
    
    stock_df = get_stock_data_from_mongodb(coll=parameters.ticker)
    
    row_index_first = stock_df[stock_df['Date'] == model_period_first_date].index[0]
    row_index_last = stock_df[stock_df['Date'] == model_period_last_date].index[0]
    model_period_df_indexes = [index for index in range(row_index_first,row_index_last+1)]

    deviation = {
        'Date': [],
        'low_deviation': [],
        'high_deviation': []
    }

    for index in model_period_df_indexes:
        parameters.projection_date = stock_df.iloc[index]['Date']
        parameters.last_base_date = stock_df.iloc[index-1]['Date']

        print(f'\n----------------------------\nMaking projection for the date: {parameters.projection_date}!\n')

        success, candles_for_chart, median_highchg, median_lowchg, chartwithfact, next_day_chg_dict = main_engine(parameters)      

        low_price_fact = stock_df.iloc[index]['Low']
        low_price_forecast = stock_df.iloc[index-1]['Low'] * median_lowchg
        high_price_fact = stock_df.iloc[index]['High']
        high_price_forecast = stock_df.iloc[index-1]['High'] * median_highchg

        deviation['Date'].append(parameters.projection_date)

        if success[0]:
            print(f'\n---> Success for the date {parameters.projection_date}!\nLow price forecast: {low_price_forecast}'
                  f'\nHigh price forecast: {high_price_forecast}')
            deviation['low_deviation'].append(low_price_forecast / low_price_fact)
            deviation['high_deviation'].append(high_price_forecast / high_price_fact)
        elif success[1] == 'No hit with the chosen indicator setup!':
            print('No hit with the chosen indicator setup!')
            deviation['low_deviation'].append('no hit')
            deviation['high_deviation'].append('no hit')
        else:
            print('Projection failed!')
            deviation['low_deviation'].append(False)
            deviation['high_deviation'].append(False)
    
    print(f'\n----------------------------\nAnalysis has finished!\nDeviation: {deviation}')

    period = model_period_first_date + ' -> ' + model_period_last_date
    show_histogram(period, parameters.ticker, deviation['low_deviation'], deviation['high_deviation'])