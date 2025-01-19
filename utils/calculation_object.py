class Parameters:
    
    def __init__(self):
        self.ticker = '^GDAXI'
        self.indicator_setup = {
            'name' : 'Base setup',
            'days' : 2,
            'lowchg' : {'selected' : True, 'tolerance': 80},
            'openchg' : {'selected' : True, 'tolerance': 80},
            'highchg' : {'selected' : True, 'tolerance': 80},
            'body' : {'selected' : True, 'tolerance': 80},
            'color' : {'selected' : True, 'tolerance': False},
            'RSIavgchg' : {'selected' : False, 'tolerance': 100},
            'RSIstate' : {'selected' : False, 'tolerance': False},
            'MACDhistchg' : {'selected' : True, 'tolerance': 9},
            'MACDrange' : {'selected' : False, 'tolerance': False},
            'SMA20chg' : {'selected' : False, 'tolerance': 5},
            'SMA50chg' : {'selected' : False, 'tolerance': 4},
            'SMA20_50relation' : {'selected' : False, 'tolerance': False}
        }
        self.first_base_date = '2000-01-01'
        self.last_base_date = '2024-10-18'
        self.projection_date = False