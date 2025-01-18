from PyQt6 import QtCore, QtGui, QtWidgets

class IndicatorSetup_Form(object):
    def setupUi(self, Form):
        Form.resize(851, 513)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 281, 22))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        # Fixed items
        self.label_numberofdays = QtWidgets.QLabel(parent=Form)
        self.label_numberofdays.setText("Please define the number of candles (days) of comparison!")
        self.label_numberofdays.setGeometry(QtCore.QRect(10, 10, 411, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_numberofdays.setFont(font)       
    
        self.line = QtWidgets.QFrame(parent=Form)
        self.line.setGeometry(QtCore.QRect(10, 50, 581, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.label_indicators = QtWidgets.QLabel(parent=Form)
        self.label_indicators.setText("Please choose the indicators to be considered as well as the tolerance (basepoint) of them!")
        self.label_indicators.setGeometry(QtCore.QRect(10, 70, 591, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_indicators.setFont(font)

        self.line_2 = QtWidgets.QFrame(parent=Form)
        self.line_2.setGeometry(QtCore.QRect(10, 440, 581, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        # Layouts
        self.formLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 100, 581, 335))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.formLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayoutWidget.setStyleSheet("""
            QSpinBox:disabled {
                color: lightgrey;
            }
            QSpinSlider:disabled {
                color: lightgrey;
            }
        """)

        # DAYS / INTERVALL
        self.label_days = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.label_days.setText("Number of candles to be compared")
        self.horizontalLayout.addWidget(self.label_days)

        self.spinbox_days = QtWidgets.QSpinBox(parent=self.horizontalLayoutWidget)
        self.spinbox_days.setMouseTracking(False)
        self.spinbox_days.setFrame(False)
        self.spinbox_days.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinbox_days.setMinimum(1)
        self.spinbox_days.setMaximum(5)
        self.spinbox_days.setProperty("value", 3)
        self.horizontalLayout.addWidget(self.spinbox_days)

        # LOW
        self.checkBox_low = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_low.setText("Change of LOW price")
        self.gridLayout.addWidget(self.checkBox_low, 0, 0, 1, 1)    
        
        self.spinBox_low = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_low.setFrame(False)
        self.spinBox_low.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_low.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_low.setMaximum(100)
        self.spinBox_low.setSingleStep(5)
        self.spinBox_low.setProperty("value", 50)
        self.gridLayout.addWidget(self.spinBox_low, 0, 1, 1, 1)

        self.Slider_low = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_low.setMaximum(100)
        self.Slider_low.setSingleStep(5)
        self.Slider_low.setPageStep(5)
        self.Slider_low.setSliderPosition(50)
        self.Slider_low.setTracking(True)
        self.Slider_low.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_low.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_low.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_low, 0, 2, 1, 1)

        # OPEN
        self.checkBox_open = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_open.setText("Change of OPEN price")        
        self.gridLayout.addWidget(self.checkBox_open, 1, 0, 1, 1)

        self.spinBox_open = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_open.setFrame(False)
        self.spinBox_open.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_open.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_open.setMaximum(100)
        self.spinBox_open.setSingleStep(5)
        self.spinBox_open.setProperty("value", 50)
        self.gridLayout.addWidget(self.spinBox_open, 1, 1, 1, 1)

        self.Slider_open = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_open.setMaximum(100)
        self.Slider_open.setSingleStep(5)
        self.Slider_open.setPageStep(5)
        self.Slider_open.setSliderPosition(50)
        self.Slider_open.setTracking(True)
        self.Slider_open.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_open.setInvertedAppearance(False)
        self.Slider_open.setInvertedControls(False)
        self.Slider_open.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_open.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_open, 1, 2, 1, 1)

        # HIGH
        self.checkBox_high = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_high.setText("Change of HIGH price")
        self.gridLayout.addWidget(self.checkBox_high, 2, 0, 1, 1)
        
        self.spinBox_high = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_high.setFrame(False)
        self.spinBox_high.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_high.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_high.setMaximum(100)
        self.spinBox_high.setSingleStep(5)
        self.spinBox_high.setProperty("value", 50)
        self.gridLayout.addWidget(self.spinBox_high, 2, 1, 1, 1)

        self.Slider_high = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_high.setMaximum(100)
        self.Slider_high.setSingleStep(5)
        self.Slider_high.setPageStep(5)
        self.Slider_high.setSliderPosition(50)
        self.Slider_high.setTracking(True)
        self.Slider_high.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_high.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_high.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_high, 2, 2, 1, 1)
        
        # BODY
        self.checkBox_body = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_body.setText("Change of HEIGHT of candles")
        self.gridLayout.addWidget(self.checkBox_body, 3, 0, 1, 1)
        
        self.spinBox_body = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_body.setFrame(False)
        self.spinBox_body.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_body.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_body.setMaximum(100)
        self.spinBox_body.setSingleStep(5)
        self.spinBox_body.setProperty("value", 50)
        self.gridLayout.addWidget(self.spinBox_body, 3, 1, 1, 1)

        self.Slider_body = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_body.setMaximum(100)
        self.Slider_body.setSingleStep(5)
        self.Slider_body.setPageStep(5)
        self.Slider_body.setSliderPosition(50)
        self.Slider_body.setTracking(True)
        self.Slider_body.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_body.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_body.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_body, 3, 2, 1, 1)
        
        # COLOR
        self.checkBox_color = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_color.setText("COLOR of candles")
        self.gridLayout.addWidget(self.checkBox_color, 4, 0, 1, 1)

        # RSI AVG CHG
        self.checkBox_RSIavgchg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_RSIavgchg.setText("Change of RSI AVERAGE")
        self.gridLayout.addWidget(self.checkBox_RSIavgchg, 5, 0, 1, 1)
        
        self.spinBox_RSIavgchg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_RSIavgchg.setFrame(False)
        self.spinBox_RSIavgchg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_RSIavgchg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_RSIavgchg.setMaximum(200)
        self.spinBox_RSIavgchg.setSingleStep(5)
        self.spinBox_RSIavgchg.setProperty("value", 100)
        self.gridLayout.addWidget(self.spinBox_RSIavgchg, 5, 1, 1, 1)

        self.Slider_RSIavgchg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_RSIavgchg.setMaximum(200)
        self.Slider_RSIavgchg.setSingleStep(5)
        self.Slider_RSIavgchg.setPageStep(5)
        self.Slider_RSIavgchg.setSliderPosition(100)
        self.Slider_RSIavgchg.setTracking(True)
        self.Slider_RSIavgchg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_RSIavgchg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_RSIavgchg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_RSIavgchg, 5, 2, 1, 1)

        # RSI STATE
        self.checkBox_RSIstate = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_RSIstate.setText("RSI STATE (overb./overs.) of last candle")
        self.gridLayout.addWidget(self.checkBox_RSIstate, 6, 0, 1, 1)

        # MACD HIST CHG
        self.checkBox_MACDhistchg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_MACDhistchg.setText("Change of MACD HISTOGRAM")
        self.gridLayout.addWidget(self.checkBox_MACDhistchg, 7, 0, 1, 1)

        self.spinBox_MACDhistchg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_MACDhistchg.setFrame(False)
        self.spinBox_MACDhistchg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_MACDhistchg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_MACDhistchg.setMaximum(200)
        self.spinBox_MACDhistchg.setSingleStep(5)
        self.spinBox_MACDhistchg.setProperty("value", 100)
        self.gridLayout.addWidget(self.spinBox_MACDhistchg, 7, 1, 1, 1)

        self.Slider_MACDhistchg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_MACDhistchg.setMaximum(200)
        self.Slider_MACDhistchg.setSingleStep(5)
        self.Slider_MACDhistchg.setPageStep(5)
        self.Slider_MACDhistchg.setSliderPosition(100)
        self.Slider_MACDhistchg.setTracking(True)
        self.Slider_MACDhistchg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_MACDhistchg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_MACDhistchg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_MACDhistchg, 7, 2, 1, 1)

        # MACD RANGE
        self.checkBox_MACDrange = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_MACDrange.setText("RANGE (+/-) of MACD of last candle")
        self.gridLayout.addWidget(self.checkBox_MACDrange, 8, 0, 1, 1)

        # SMA20 CHG
        self.checkBox_SMA20chg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_SMA20chg.setText("Change of SMA20")
        self.gridLayout.addWidget(self.checkBox_SMA20chg, 9, 0, 1, 1)

        self.spinBox_SMA20chg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_SMA20chg.setFrame(False)
        self.spinBox_SMA20chg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_SMA20chg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_SMA20chg.setMaximum(200)
        self.spinBox_SMA20chg.setSingleStep(5)
        self.spinBox_SMA20chg.setProperty("value", 100)
        self.gridLayout.addWidget(self.spinBox_SMA20chg, 9, 1, 1, 1)

        self.Slider_SMA20chg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_SMA20chg.setMaximum(200)
        self.Slider_SMA20chg.setSingleStep(5)
        self.Slider_SMA20chg.setPageStep(5)
        self.Slider_SMA20chg.setSliderPosition(100)
        self.Slider_SMA20chg.setTracking(True)
        self.Slider_SMA20chg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_SMA20chg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_SMA20chg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_SMA20chg, 9, 2, 1, 1)

        # SMA50 CHG
        self.checkBox_SMA50chg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_SMA50chg.setText("Change of SMA50")
        self.gridLayout.addWidget(self.checkBox_SMA50chg, 10, 0, 1, 1)

        self.spinBox_SMA50chg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_SMA50chg.setFrame(False)
        self.spinBox_SMA50chg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_SMA50chg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_SMA50chg.setMaximum(200)
        self.spinBox_SMA50chg.setSingleStep(5)
        self.spinBox_SMA50chg.setProperty("value", 100)
        self.spinBox_SMA50chg.setMinimumWidth(42)
        self.gridLayout.addWidget(self.spinBox_SMA50chg, 10, 1, 1, 1)
       
        self.Slider_SMA50chg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_SMA50chg.setMaximum(200)
        self.Slider_SMA50chg.setSingleStep(5)
        self.Slider_SMA50chg.setPageStep(5)
        self.Slider_SMA50chg.setSliderPosition(100)
        self.Slider_SMA50chg.setTracking(True)
        self.Slider_SMA50chg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_SMA50chg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_SMA50chg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_SMA50chg, 10, 2, 1, 1)
        
        # SMA 20/50 RELATION
        self.checkBox_SMA20_50relation = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_SMA20_50relation.setText("Relation of SMA20 and SMA50 (last candle)")
        self.gridLayout.addWidget(self.checkBox_SMA20_50relation, 11, 0, 1, 1)

        self.harmonize_indicator_widgets()

        # BUTTONS
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 450, 331, 41))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutWidget_2.setStyleSheet("""
            QPushButton {
                background-color: rgb(76, 172, 207);
                border: 1px solid #4c7a9b;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(56, 152, 187);
            }
        """)

        self.pushButton_indicator_save = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_indicator_save.setText("Save")
        self.horizontalLayout_2.addWidget(self.pushButton_indicator_save)
        self.pushButton_indicator_save.setEnabled(False)

        self.pushButton_indicator_saveas = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_indicator_saveas.setText("Save as ...")
        self.horizontalLayout_2.addWidget(self.pushButton_indicator_saveas)
        self.pushButton_indicator_saveas.setEnabled(False)
        
        self.pushButton_indicator_reset = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_indicator_reset.setText("Reset")
        self.horizontalLayout_2.addWidget(self.pushButton_indicator_reset)
        self.pushButton_indicator_reset.setEnabled(False)

        self.pushButton_indicator_delete = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_indicator_delete.setText("Delete")
        self.horizontalLayout_2.addWidget(self.pushButton_indicator_delete)
        self.pushButton_indicator_delete.setEnabled(False)

        self.indicator_widgets = [
            {'checkbox' : self.checkBox_low, 'spinbox' : self.spinBox_low, 'name' : 'lowchg'},
            {'checkbox' : self.checkBox_open, 'spinbox' : self.spinBox_open, 'name' : 'openchg'},
            {'checkbox' : self.checkBox_high, 'spinbox' : self.spinBox_high, 'name' : 'highchg'},
            {'checkbox' : self.checkBox_body, 'spinbox' : self.spinBox_body, 'name' : 'body'},
            {'checkbox' : self.checkBox_color, 'spinbox' : False, 'name' : 'color'},
            {'checkbox' : self.checkBox_RSIavgchg, 'spinbox' : self.spinBox_RSIavgchg, 'name' : 'RSIavgchg'},
            {'checkbox' : self.checkBox_RSIstate, 'spinbox' : False, 'name' : 'RSIstate'},
            {'checkbox' : self.checkBox_MACDhistchg, 'spinbox' : self.spinBox_MACDhistchg, 'name' : 'MACDhistchg'},
            {'checkbox' : self.checkBox_MACDrange, 'spinbox' : False, 'name' : 'MACDrange'},
            {'checkbox' : self.checkBox_SMA20chg, 'spinbox' : self.spinBox_SMA20chg, 'name' : 'SMA20chg'},
            {'checkbox' : self.checkBox_SMA50chg, 'spinbox' : self.spinBox_SMA50chg, 'name' : 'SMA50chg'},
            {'checkbox' : self.checkBox_SMA20_50relation, 'spinbox' : False, 'name' : 'SMA20_50relation'}
        ]

        for checkbox in self.indicator_widgets:
            checkbox['checkbox'].stateChanged.connect(self.manage_buttons)
    
    def manage_buttons(self):
        one_is_checked = False
        for checkbox in self.indicator_widgets:
            if checkbox['checkbox'].isChecked():
                self.pushButton_indicator_save.setEnabled(True)
                self.pushButton_indicator_saveas.setEnabled(True)
                self.pushButton_indicator_reset.setEnabled(True)
                self.pushButton_indicator_delete.setEnabled(True)
                one_is_checked = True
                break
        
        if one_is_checked == False:
                self.pushButton_indicator_save.setEnabled(False)
                self.pushButton_indicator_saveas.setEnabled(False)
                self.pushButton_indicator_reset.setEnabled(False)
                self.pushButton_indicator_delete.setEnabled(False)

    def reset_indicator_widgets(self):
        for widget in self.indicator_widgets:
            widget['checkbox'].setChecked(False)
            if widget['spinbox'] != False:
                widget['spinbox'].setValue(widget['spinbox'].maximum()//2)
        
        self.spinbox_days.setValue(3)

    def harmonize_indicator_widgets(self):
        
        def set_status_of_sliders(checkbox, slider, spinbox):
            status = checkbox.isChecked()
            slider.setEnabled(status)
            spinbox.setEnabled(status)

        def harmonize_sliders(checkbox, slider, spinbox):
            value = spinbox.value()
            slider.setValue(value)
        
        def harmonize_spinboxes(checkbox, slider, spinbox):
            value = slider.value()
            spinbox.setValue(value)

        sliders = [
            self.Slider_low, self.Slider_open, self.Slider_high,
            self.Slider_body, self.Slider_RSIavgchg, self.Slider_MACDhistchg,
            self.Slider_SMA20chg, self.Slider_SMA50chg
        ]
        
        spinboxes = [
            self.spinBox_low, self.spinBox_open, self.spinBox_high,
            self.spinBox_body, self.spinBox_RSIavgchg, self.spinBox_MACDhistchg,
            self.spinBox_SMA20chg, self.spinBox_SMA50chg
        ]
        
        for slider, spinbox in zip(sliders, spinboxes):
            slider.setEnabled(False)
            spinbox.setEnabled(False)
        
        checkboxes_with_sliders = [
            self.checkBox_low, self.checkBox_open, self.checkBox_high,
            self.checkBox_body, self.checkBox_RSIavgchg, self.checkBox_MACDhistchg,
            self.checkBox_SMA20chg, self.checkBox_SMA50chg
        ]
        
        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):
            checkbox.stateChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: set_status_of_sliders(cb, sl, sp))

        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):        
            spinbox.valueChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: harmonize_sliders(cb, sl, sp))

        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):
            slider.valueChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: harmonize_spinboxes(cb, sl, sp))

    def get_indicator_setup(self):
        result = {
            'name' : '',
            'days' : '',
            'lowchg' : {'selected' : False, 'tolerance': 100},
            'openchg' : {'selected' : False, 'tolerance': 100},
            'highchg' : {'selected' : False, 'tolerance': 100},
            'body' : {'selected' : False, 'tolerance': 100},
            'color' : {'selected' : False, 'tolerance': False},
            'RSIavgchg' : {'selected' : False, 'tolerance': 100},
            'RSIstate' : {'selected' : False, 'tolerance': False},
            'MACDhistchg' : {'selected' : False, 'tolerance': 100},
            'MACDrange' : {'selected' : False, 'tolerance': False},
            'SMA20chg' : {'selected' : False, 'tolerance': 100},
            'SMA50chg' : {'selected' : False, 'tolerance': 100},
            'SMA20_50relation' : {'selected' : False, 'tolerance': False}
        }
        
        result['days'] = self.spinbox_days.value()

        for widget in self.indicator_widgets:
            if widget['checkbox'].isChecked():
                result[widget['name']]['selected'] = True
                if widget['spinbox'] != False:
                    result[widget['name']]['tolerance'] = widget['spinbox'].value()
        return result

    def set_indicator_setup_on_screen(self, setup: dict):
        self.reset_indicator_widgets()
        self.spinbox_days.setValue(setup['days'])
        for widget in self.indicator_widgets:
            if setup[widget['name']]['selected']:
                widget['checkbox'].setEnabled(True)
                widget['checkbox'].setChecked(True)
                if widget['spinbox']:
                    widget['spinbox'].setEnabled(True)
                    widget['spinbox'].setValue(setup[widget['name']]['tolerance'])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = IndicatorSetup_Form()
    ui.setupUi(Form)
    Form.show()
    ui.harmonize_indicator_widgets()
    sys.exit(app.exec())
