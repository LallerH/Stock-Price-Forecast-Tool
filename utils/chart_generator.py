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

def show_histogram(date: str, ticker: str, **kwargs):
    """
    :Show histogram and box plot for projected changes of LOW and HIGH value data
    
    :Parameters:
        date : 'str'; date to be shown in title
        ticker: 'str'; stock name to be shown in title
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
    fig.suptitle(f'Possible changes of {ticker} LOW and HIGH price for the day after {date}')

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

def show_candle_chart(stock_data: dict, ticker: str, date: str, projection = None, chartwithfact = False):
    """
    :Show candle chart
    
    :Parameters:
        stock_data : {dict}; returned by get_candle_from_df methods
        ticker: 'str'; stock name to be shown in title
        date: 'str'; date to be shown in title
        projection : {'Lowchg': int, 'Highchg': int};
        chartwithfact : bool; True -> sets a fact candle after projection candle
    """
    fig = plt.figure()
    fig.canvas.toolbar.pack_forget()
    fig.canvas.manager.set_window_title('Japanese candle chart')
    set_window_icon(fig, 'ikon.ico')
    fig.suptitle(ticker)

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
        fig.suptitle(f'{ticker} chart with LOW and HIGH price projection\n for the day after {date}')

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
    plt.show()

def show_all_charts(stock_data: dict, date: str, ticker: str, Lowchg: list, Highchg: list, projection=None, chartwithfact=False):
    """
    :Show histogram/box plot and candle chart for projected changes of LOW and HIGH value data in two separated windows
    
    :Parameters:
        stock_data : {dict}; returned by get_candle_from_df methods
        date : 'str'; date to be shown in title of histogram/box plot
        ticker: 'str'; stock name to be shown in title
        Lowchg and/or Highchg : [list]; kwargs; which data array to be shown
        projection : {'Lowchg': int, 'Highchg': int}; 
    """

    histogram_process = Process(target=show_histogram, args=(date,ticker,), kwargs={'Lowchg': Lowchg, 'Highchg': Highchg})
    candle_chart_process = Process(target=show_candle_chart, args=(stock_data,ticker,date), kwargs={'projection': projection, 'chartwithfact': chartwithfact})
    
    histogram_process.start()
    candle_chart_process.start()
    histogram_process.join()
    candle_chart_process.join()


if __name__ == '__main__':
    from utils.stock_database_manager import get_candles_from_df, get_data_from_mongodb

    Lowchg = [0.9996554912124962, 0.9958912528506714, 1.00448931540741, 0.9982181758349802, 1.0029118277535642, 1.0012103609429495, 1.0003555293541195, 1.00986476231454, 0.9955466190771032, 1.004226864695291, 1.002761470327116, 1.000041061493693, 1.0372261654256407, 0.9932368456496866, 0.9935887890282025] 
    Highchg = [0.9862913541847809, 1.0149977200623694, 1.008387816797034, 1.0054172464910773, 1.0043957108167876, 0.9972588554807796, 0.9988511160007469, 0.9963072788828856, 0.9942447656225549, 0.9949120623898702, 1.0008423042175159, 1.0020689851767919, 0.9957899875988884, 0.9954114168249036, 1.0080286072667715, 0.9981945552193169, 0.990014469254289, 0.9977382778564082, 1.0009723710674077, 0.9941799067100272, 1.012377348422996, 1.0037891042591203, 0.995796199850876, 0.9967335903187154, 0.99728162408626, 0.9853711801223551, 0.9985118321106567, 0.9909577996907095, 0.994492715104553, 0.9961163504389984, 1.0011860805342816, 1.0099168060527426, 0.986664870731078, 0.9961071623938865, 0.9930308991764328, 0.9959267177290837, 1.0111228706516597, 0.9981542116820552, 0.9899007287069127, 0.9923725370622776, 1.0018690878573413, 0.9899562979829027, 0.9935844058014726, 0.9889504016831717, 0.9875377761635439, 1.0118623521189531, 1.0001074141401745, 0.9898231693374995, 0.9998951450979733, 0.9954111676465003, 1.0047856637669383, 0.9762445783465862, 0.9992471379371538, 0.9994192354482484, 1.0041555243169913, 0.9999139360566565, 0.9982651201391398, 0.9965530708563501, 1.0012057667356538, 1.0091612641153633, 0.9943055872931783, 1.0019883887887882, 0.9928610438680883, 1.0002006310175175, 1.0057945030271793, 1.014215172840748, 0.9949739542058338, 0.9865139776439243, 0.9960772726526114, 1.0010532297960153, 0.9995098471252304, 1.004826711826536, 0.9892047271917538, 0.9885459826840668, 0.9877957991708214, 0.9975046558848187, 1.0014401984067995, 0.9968880158733481, 0.9912322649519134, 0.9861813855550438, 0.9883722676532266, 0.9913868696602149, 0.995531893841686, 0.9876330119538343, 1.0023064674752962, 0.9740886097284261, 0.9925775945123526, 1.008041020228928, 1.012915215720466, 0.978049689815565, 0.9790866372607935, 1.0300653893989593, 0.9869360267215883, 1.0045111319560878, 0.9954965796660206, 1.0170259050124064, 0.991335963618455, 0.993716197303626, 0.9973874497383509, 0.9946047126484148, 0.9998815242488979, 0.9935940779498015, 0.9922696778497451, 1.0004115595203584, 0.98393070595571, 1.009752270884467, 1.006346522000461, 0.9861720599500248, 0.9964499496773966, 0.9920195910926125, 1.0073514818693954, 1.034606270912789, 1.0034281751951353, 1.0038499670077052, 0.9864295493477641, 0.9952663005438935, 0.983352638643703, 0.9972603896428551, 0.9973253392164735, 0.9940206765590699, 0.9998147242530679, 1.0015506473481977, 1.0023709626509982, 0.9978836364479355, 0.9936732379404922, 0.9805282050543924, 1.0112155135146126, 0.9861183175928899, 0.981908954534412, 1.0037999109632614, 1.0110682169439582, 0.9769553252826401, 1.0033575477834904, 0.999390463331722, 1.0073994026431758, 1.0085686489734054, 0.9929861327892318, 0.9903423368878215, 0.9968928990877538, 1.0058273245372096, 0.9864441294765232, 0.981947132579616, 0.9875198348327419, 0.9935612818246622, 1.0039135043957004, 0.9896669348378875, 0.9939985619991777, 0.9976505180550508, 1.0134601894731965, 1.0009403612967087, 1.0031596892372951, 0.9998432902052773, 1.0055059913757989, 0.9914598321639713, 1.018099627915624, 0.9988390589400951, 0.9853767718894462, 0.9930024187553997, 0.9983825622182898, 0.999108368887716, 0.9999305789371653, 0.9882255300246489, 0.9973694399897244, 1.0083775577501926, 0.9874479063580759, 1.006059969685016, 0.992048692594687, 0.999965991186859, 0.9919832672011543, 1.0020899694486982, 0.9929869651965559, 0.9930610171183897, 0.9871198166779654, 1.014529238370684, 0.9948266690669809, 1.0239271700303225, 1.0020865526161877, 1.0051038223914865, 0.9981648490746949, 1.008797279512912, 0.9955333858693338, 0.9979529785416923, 0.9766216263960962, 0.9952751526760366, 1.0210979185404714, 0.9956885290972036, 0.9913679766985135, 1.002720668328234, 1.0048115323840872, 1.011876340493937, 1.015776650332659, 1.0046132657210805, 0.9910996187996407, 1.005871985042958, 0.9951449353133529, 1.005871338618562, 1.000831807397005, 0.9935701544803912, 0.9994692112588748, 0.9828593346493534, 1.003948943048966]
    stock_df = get_data_from_mongodb(coll='^GSPC')
    candles_for_chart = get_candles_from_df(stock_df, date='2024-05-31', period=4)
    
    show_all_charts(candles_for_chart, '2024-05-30', 'S&P 500', Lowchg=Lowchg, Highchg=Highchg, projection={'Lowchg': 1.0001458162636458, 'Highchg': 0.9973694399897244}, chartwithfact=True)
   
    # Lowchg = [0.9920902162797264, 1.0169317865625667, 1.0068844847744827, 0.9901810490308226, 0.9902830679227229, 0.9959169466341237, 0.9741846280107039, 0.9796332484530766, 1.0088599574680956, 0.9952986621801193, 0.974214141784294, 0.986355835772398, 0.9997276195015199, 0.983501257881302, 0.9852302866095208, 1.0135509123551094, 0.988885808724376, 1.0037997555202527, 1.0164067381236, 0.9904439400089752, 0.9890843779959467, 0.9896849212476974, 0.992135770752653, 0.9788602171812101, 1.0233441175317142, 0.9887346584535085, 0.9800767127378608, 1.0033809976785, 1.000033387459019, 1.005741719028462, 1.0008217088036366, 1.0192829444648575, 1.0079001185068575, 0.991306912333409, 0.9930714244502004, 0.9776189898507845, 1.006079519017122, 1.014422177227651, 0.9814135551580582, 1.004463904581928, 0.9910890917203888, 0.9813158546927936, 0.9789720550965516, 0.9834317133350803, 1.0010201288142333, 1.013803970795913, 0.9901765522707588, 1.0025238368939264, 0.9782234606856018, 1.0006741702123265, 1.0037342463448877, 0.9948286862554742, 0.9885137876965925, 0.9987745253521004, 0.991407483149825, 1.0164089797690272, 0.9948354200729488, 0.9718937080851822, 0.9890227650658932, 1.0056934464843055, 0.9977035344521739, 1.00760501660792, 1.0100787274929575, 1.00281152326265, 1.0105110291552086, 1.007929211718254, 1.004844320040996, 1.0066019346114239, 0.9994013987680991, 0.9945851436978161, 0.9963624168992121, 1.001492623349337, 0.9985241459969885, 1.0067125572799704, 0.9968069708098874, 0.9991614416022777]
    # Highchg = [1.004564289267662, 1.0237026574896326, 1.009098721863629, 0.9982336456722032, 0.9933710182731514, 1.0018586463173935, 0.9855439614168755, 0.9836052450388729, 1.011189735264538, 1.0037360220868392, 0.9885931982488777, 1.006590361773857, 1.0005210618768046, 1.0051154736320926, 0.9984849829397939, 1.005640425221451, 1.010176053951878, 1.0052615793651993, 1.0134682609625836, 0.9996001914340917, 0.9892805959456356, 0.9939071143173823, 0.9823827580502925, 0.9930279795580693, 1.012180417121135, 0.9962821546633206, 1.014002605098054, 1.0028143574809627, 1.000048242640889, 1.0030641527993802, 0.9989826781496398, 1.0197352663069403, 1.00954384983519, 0.9957079368950584, 0.9931653000451697, 0.9904454513983113, 1.0184079137386135, 1.0272821928094473, 0.9952090136128048, 1.0059369941269174, 0.9968562797867254, 0.9921363594090175, 0.9868873845254671, 0.9903650006790947, 0.9961405864201519, 1.0233005256636116, 0.9879152661588012, 1.0089969826669924, 0.9977776549660762, 1.0025718961889174, 1.0026449918651985, 1.0006081576357977, 0.9814408556612957, 0.9998416314230062, 0.9944502955634636, 1.0192675942557679, 0.9946891551978856, 0.9860808222933124, 0.9884372711779807, 1.005379300547268, 1.005240033290309, 1.0076733852414639, 1.0033150213333053, 1.0046651135640696, 1.0077340110878792, 0.9992638321698739, 0.999769351582169, 1.0021075725882038, 1.0030792254106882, 0.9955144947448922, 1.003686756306624, 1.0060676898843128, 1.0033692568607042, 0.998884342640925, 1.001145784853227, 0.9975284340244797]
    # stock_df = get_data_from_mongodb(coll='^GDAXI')
    # candles_for_chart = get_candles_from_df(stock_df, date='2024-05-31', period=4)
    
    # show_all_charts(candles_for_chart, '2024-05-30', 'DAX', Lowchg=Lowchg, Highchg=Highchg, projection={'Lowchg': 0.9972552526310307, 'Highchg': 1.0008769712445122}, chartwithfact=True)
