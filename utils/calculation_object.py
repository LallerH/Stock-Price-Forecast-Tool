class Parameters:
    
    def __init__(self):
        self.ticker = '^GDAXI'
        self.indicator_setup = {
            'name' : 'Base setup',
            'days' : 3,
            'lowchg' : {'selected' : True, 'tolerance': 50},
            'openchg' : {'selected' : False, 'tolerance': 50},
            'highchg' : {'selected' : True, 'tolerance': 50},
            'body' : {'selected' : False, 'tolerance': 50},
            'color' : {'selected' : False, 'tolerance': False},
            'RSIavgchg' : {'selected' : True, 'tolerance': 100},
            'RSIstate' : {'selected' : True, 'tolerance': False},
            'MACDhistchg' : {'selected' : False, 'tolerance': 100},
            'MACDrange' : {'selected' : True, 'tolerance': False},
            'SMA20chg' : {'selected' : False, 'tolerance': 100},
            'SMA50chg' : {'selected' : False, 'tolerance': 100},
            'SMA20_50relation' : {'selected' : False, 'tolerance': False}
        }
        self.first_base_date = '2000-01-01'
        self.last_base_date = '2024-10-18'
        self.projection_date = False