def show_histogram(date: str, **kwargs):
    '''
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image, ImageTk

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
    thismanager = plt.get_current_fig_manager()
    img = ImageTk.PhotoImage(Image.open('ikon.ico'))
    thismanager.window.tk.call('wm', 'iconphoto', thismanager.window._w, img)
    fig.suptitle('Possible changes of OPEN and CLOSE value for the day after '+date)

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

if __name__ == '__main__':
    data = [1.0054416223478437, 1.0062501301052167, 1.004196494194109, 1.0019394383285984, 1.002018908808809, 1.0131752979178803, 0.9943834768730091, 1.0052478733295327, 1.00843362005185, 1.0080694438216675, 1.0060730392084474, 1.0088350821074197, 0.9997055203088745, 0.9951873024819768, 0.9948919023617266, 1.0034391916713643, 1.0007148168578732, 1.0006939596482074, 1.0036526343423815, 1.0031769365588643, 1.0080399857053313, 1.0059640641347218]
    show_histogram('2024-05-09', Lowchg=data, Highchg=data)
