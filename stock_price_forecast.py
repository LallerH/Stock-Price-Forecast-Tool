import sys
from PyQt6 import QtWidgets
from utils import Ui_MainWindow, main_engine, get_collections_from_mongodb

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    ui.pushButton.clicked.connect(main_engine)
    if get_collections_from_mongodb():
        ui.list_of_tickersWidget.addItems(sorted(get_collections_from_mongodb()))
        
    MainWindow.show()
    sys.exit(app.exec())
    