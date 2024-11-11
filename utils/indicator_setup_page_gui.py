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
        self.label_indicators.setText("Please choose the indicators to be considered as well as the tolerance (%) level of them!")
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
        self.gridLayout.setObjectName("gridLayout")

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
        self.spinBox_low.setMaximum(200)
        self.spinBox_low.setSingleStep(5)
        self.spinBox_low.setProperty("value", 100)
        self.spinBox_low.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_low, 0, 1, 1, 1)

        self.Slider_low = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_low.setMaximum(200)
        self.Slider_low.setSingleStep(5)
        self.Slider_low.setPageStep(5)
        self.Slider_low.setSliderPosition(100)
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
        self.spinBox_open.setMaximum(200)
        self.spinBox_open.setSingleStep(5)
        self.spinBox_open.setProperty("value", 100)
        self.spinBox_open.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_open, 1, 1, 1, 1)

        self.Slider_open = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_open.setMaximum(200)
        self.Slider_open.setSingleStep(5)
        self.Slider_open.setPageStep(5)
        self.Slider_open.setSliderPosition(100)
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
        self.spinBox_high.setMaximum(200)
        self.spinBox_high.setSingleStep(5)
        self.spinBox_high.setProperty("value", 100)
        self.spinBox_high.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_high, 2, 1, 1, 1)

        self.Slider_high = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_high.setMaximum(200)
        self.Slider_high.setSingleStep(5)
        self.Slider_high.setPageStep(5)
        self.Slider_high.setSliderPosition(100)
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
        self.spinBox_body.setMaximum(200)
        self.spinBox_body.setSingleStep(5)
        self.spinBox_body.setProperty("value", 100)
        self.spinBox_body.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_body, 3, 1, 1, 1)

        self.Slider_body = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_body.setMaximum(200)
        self.Slider_body.setSingleStep(5)
        self.Slider_body.setPageStep(5)
        self.Slider_body.setSliderPosition(100)
        self.Slider_body.setTracking(True)
        self.Slider_body.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_body.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_body.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_body, 3, 2, 1, 1)
        
        # COLOR
        self.checkBox_color = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_color.setText("COLOR of last candle")
        self.gridLayout.addWidget(self.checkBox_color, 4, 0, 1, 1)

        # RSI AVG CHG
        self.checkBox_rsiavgchg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_rsiavgchg.setText("Change of RSI AVERAGE")
        self.gridLayout.addWidget(self.checkBox_rsiavgchg, 5, 0, 1, 1)
        
        self.spinBox_rsiavgchg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_rsiavgchg.setFrame(False)
        self.spinBox_rsiavgchg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_rsiavgchg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_rsiavgchg.setMaximum(200)
        self.spinBox_rsiavgchg.setSingleStep(5)
        self.spinBox_rsiavgchg.setProperty("value", 100)
        self.spinBox_rsiavgchg.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_rsiavgchg, 5, 1, 1, 1)

        self.Slider_rsiavgchg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_rsiavgchg.setMaximum(200)
        self.Slider_rsiavgchg.setSingleStep(5)
        self.Slider_rsiavgchg.setPageStep(5)
        self.Slider_rsiavgchg.setSliderPosition(100)
        self.Slider_rsiavgchg.setTracking(True)
        self.Slider_rsiavgchg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_rsiavgchg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_rsiavgchg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_rsiavgchg, 5, 2, 1, 1)

        # RSI STATE
        self.checkBox_rsistate = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_rsistate.setText("RSI STATE (overb./overs.) of last candle")
        self.gridLayout.addWidget(self.checkBox_rsistate, 6, 0, 1, 1)

        # MACD HIST CHG
        self.checkBox_macdhistchg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_macdhistchg.setText("Change of MACD HISTOGRAM")
        self.gridLayout.addWidget(self.checkBox_macdhistchg, 7, 0, 1, 1)

        self.spinBox_macdhistchg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_macdhistchg.setFrame(False)
        self.spinBox_macdhistchg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_macdhistchg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_macdhistchg.setMaximum(200)
        self.spinBox_macdhistchg.setSingleStep(5)
        self.spinBox_macdhistchg.setProperty("value", 100)
        self.spinBox_macdhistchg.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_macdhistchg, 7, 1, 1, 1)

        self.Slider_macdhistchg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_macdhistchg.setMaximum(200)
        self.Slider_macdhistchg.setSingleStep(5)
        self.Slider_macdhistchg.setPageStep(5)
        self.Slider_macdhistchg.setSliderPosition(100)
        self.Slider_macdhistchg.setTracking(True)
        self.Slider_macdhistchg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_macdhistchg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_macdhistchg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_macdhistchg, 7, 2, 1, 1)

        # MACD RANGE
        self.checkBox_macdrange = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_macdrange.setText("RANGE (+/-) of MACD of last candle")
        self.gridLayout.addWidget(self.checkBox_macdrange, 8, 0, 1, 1)

        # SMA20 CHG
        self.checkBox_sma20chg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_sma20chg.setText("Change of SMA20")
        self.gridLayout.addWidget(self.checkBox_sma20chg, 9, 0, 1, 1)

        self.spinBox_sma20chg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_sma20chg.setFrame(False)
        self.spinBox_sma20chg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_sma20chg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_sma20chg.setMaximum(200)
        self.spinBox_sma20chg.setSingleStep(5)
        self.spinBox_sma20chg.setProperty("value", 100)
        self.spinBox_sma20chg.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.gridLayout.addWidget(self.spinBox_sma20chg, 9, 1, 1, 1)

        self.Slider_sma20chg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_sma20chg.setMaximum(200)
        self.Slider_sma20chg.setSingleStep(5)
        self.Slider_sma20chg.setPageStep(5)
        self.Slider_sma20chg.setSliderPosition(100)
        self.Slider_sma20chg.setTracking(True)
        self.Slider_sma20chg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_sma20chg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_sma20chg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_sma20chg, 9, 2, 1, 1)

        # SMA50 CHG
        self.checkBox_sma50chg = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_sma50chg.setText("Change of SMA50")
        self.gridLayout.addWidget(self.checkBox_sma50chg, 10, 0, 1, 1)

        self.spinBox_sma50chg = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_sma50chg.setFrame(False)
        self.spinBox_sma50chg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_sma50chg.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_sma50chg.setMaximum(200)
        self.spinBox_sma50chg.setSingleStep(5)
        self.spinBox_sma50chg.setProperty("value", 100)
        self.spinBox_sma50chg.setStyleSheet("""QSpinBox:disabled {color: lightgrey;}""")
        self.spinBox_sma50chg.setMinimumWidth(42)
        self.gridLayout.addWidget(self.spinBox_sma50chg, 10, 1, 1, 1)
       
        self.Slider_sma50chg = QtWidgets.QSlider(parent=self.formLayoutWidget)
        self.Slider_sma50chg.setMaximum(200)
        self.Slider_sma50chg.setSingleStep(5)
        self.Slider_sma50chg.setPageStep(5)
        self.Slider_sma50chg.setSliderPosition(100)
        self.Slider_sma50chg.setTracking(True)
        self.Slider_sma50chg.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider_sma50chg.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.Slider_sma50chg.setTickInterval(5)
        self.gridLayout.addWidget(self.Slider_sma50chg, 10, 2, 1, 1)
        
        # SMA 20/50 RELATION
        self.checkBox_sma20_50relation = QtWidgets.QCheckBox(parent=self.formLayoutWidget)
        self.checkBox_sma20_50relation.setText("Relation of SMA20 and SMA50 (last candle)")
        self.gridLayout.addWidget(self.checkBox_sma20_50relation, 11, 0, 1, 1)

    def reset_indicators(self):
        
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
            self.Slider_body, self.Slider_rsiavgchg, self.Slider_macdhistchg,
            self.Slider_sma20chg, self.Slider_sma50chg
        ]
        
        spinboxes = [
            self.spinBox_low, self.spinBox_open, self.spinBox_high,
            self.spinBox_body, self.spinBox_rsiavgchg, self.spinBox_macdhistchg,
            self.spinBox_sma20chg, self.spinBox_sma50chg
        ]
        
        for slider, spinbox in zip(sliders, spinboxes):
            slider.setEnabled(False)
            spinbox.setEnabled(False)
        
        checkboxes_with_sliders = [
            self.checkBox_low, self.checkBox_open, self.checkBox_high,
            self.checkBox_body, self.checkBox_rsiavgchg, self.checkBox_macdhistchg,
            self.checkBox_sma20chg, self.checkBox_sma50chg
        ]
        
        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):
            checkbox.stateChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: set_status_of_sliders(cb, sl, sp))

        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):        
            spinbox.valueChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: harmonize_sliders(cb, sl, sp))

        for checkbox, slider, spinbox in zip(checkboxes_with_sliders, sliders, spinboxes):
            slider.valueChanged.connect(lambda _, cb=checkbox, sl=slider, sp=spinbox: harmonize_spinboxes(cb, sl, sp))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = IndicatorSetup_Form()
    ui.setupUi(Form)
    Form.show()

    ui.reset_indicators()


    sys.exit(app.exec())
