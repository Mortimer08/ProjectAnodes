from PyQt6 import QtCore, QtGui, QtWidgets
from project_anodes_01 import dict_for_window
print(dict_for_window[0])
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        super().__init__()
        tks = {}
        # Установка главного окна
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Чистка анодов и ванн")
        # Установка размера главного окна
        MainWindow.resize(2228, 891)
        # Локализация - Россия, язык - русский
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.Russian, QtCore.QLocale.Country.Russia))
        # Установка центрального виджета
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        # Виджет для вкладок бригад
        self.TeamsTabWidget = QtWidgets.QTabWidget(self.centralWidget)
        # Установка размера виджета вкладок
        self.TeamsTabWidget.setGeometry(QtCore.QRect(0, 30, 2051, 781))
        self.TeamsTabWidget.setObjectName("TeamsTabWidget")
        # Вкладка для первой бригады
        self.Team1Tab = QtWidgets.QWidget()
        self.Team1Tab.setObjectName("Team1Tab")
        # Макет 
        self.layoutWidget = QtWidgets.QWidget(self.Team1Tab)
        # Размер вкладки первой бригады
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1758, 148))
        self.layoutWidget.setObjectName("layoutWidget")
        # Макет для ряда ванн
        self.RowHorizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.RowHorizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.RowHorizontalLayout.setSpacing(1)
        self.RowHorizontalLayout.setObjectName("RowHorizontalLayout")
        
        # Начало формирования кнопок ванн и подъёмов
        # макет для кнопок ванны
        self.CellC11gridLayout = QtWidgets.QGridLayout()
        self.CellC11gridLayout.setContentsMargins(1, 1, 1, 1)
        self.CellC11gridLayout.setSpacing(1)
        self.CellC11gridLayout.setObjectName("CellC11gridLayout")
        
        # Добавление чекбокса чистки ванны C11CellClearing
        self.C11CellClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C11CellClearing.setCheckable(True)
        self.C11CellClearing.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.C11CellClearing.setObjectName("C11CellClearing")
        self.C11CellClearing.setText("C11 01.05.22")
        self.CellC11gridLayout.addWidget(self.C11CellClearing, 0, 0, 1, 2)
        self.C11CellClearing.clicked.connect(self.C11CellClearingClicked)
        
        # Добавление кнопки чистки подъёма C11(1)
        self.C11_1_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        tks["C11_1"] = self.C11_1_TakeClearing
        tks["C11_1"].setObjectName("C11_1_TakeClearing")
        tks["C11_1"].setText("1\n01.05.22\nM  10/10")
        tks["C11_1"].setCheckable(True)
        self.CellC11gridLayout.addWidget(tks["C11_1"], 1, 0, 1, 1)
        tks["C11_1"].clicked.connect(self.C11_1_TakeClearingClicked)

        # Добавление кнопки чистки подъёма C11(2)
        self.C11_2_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C11_2_TakeClearing.setObjectName("C11_2_TakeClearing")
        self.C11_2_TakeClearing.setText("2\n01.05.22\nM  10/10")
        self.C11_2_TakeClearing.setCheckable(True)
        self.CellC11gridLayout.addWidget(self.C11_2_TakeClearing, 1, 1, 1, 1)
        self.C11_2_TakeClearing.clicked.connect(self.C11_2_TakeClearingClicked)


        # Добавление кнопки чистки подъёма C11(3)
        self.C11_3_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C11_3_TakeClearing.setObjectName("C11_3_TakeClearing")
        self.C11_3_TakeClearing.setText("3\n01.05.22\nM  10/10")
        self.C11_3_TakeClearing.setCheckable(True)
        self.CellC11gridLayout.addWidget(self.C11_3_TakeClearing, 2, 0, 1, 1)

        # Добавление кнопки чистки подъёма C11(4)
        self.C11_4_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C11_4_TakeClearing.setObjectName("C11_4_TakeClearing")
        self.C11_4_TakeClearing.setText("4\n01.05.22\nM  10/10")
        self.C11_4_TakeClearing.setCheckable(True)
        self.CellC11gridLayout.addWidget(self.C11_4_TakeClearing, 2, 1, 1, 1)
        
        # Добавление макета ванны C11 в макет Ряда
        self.RowHorizontalLayout.addLayout(self.CellC11gridLayout)
        
        # макет для кнопок ванны
        self.CellC12gridLayout = QtWidgets.QGridLayout()
        self.CellC12gridLayout.setContentsMargins(1, 1, 1, 1)
        self.CellC12gridLayout.setSpacing(1)
        self.CellC12gridLayout.setObjectName("CellC12gridLayout")
        
        # Добавление чекбокса чистки ванны C12CellClearing
        self.C12CellClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C12CellClearing.setCheckable(True)
        self.C12CellClearing.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.C12CellClearing.setObjectName("C12CellClearing")
        self.C12CellClearing.setText("C12 01.05.22")
        self.CellC12gridLayout.addWidget(self.C12CellClearing, 0, 0, 1, 2)
        self.C12CellClearing.clicked.connect(self.C12CellClearingClicked)
        
        # Добавление кнопки чистки подъёма C11(1)
        self.C12_1_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C12_1_TakeClearing.setObjectName("C12_1_TakeClearing")
        self.C12_1_TakeClearing.setText("1\n01.05.22\nM  10/10")
        self.C12_1_TakeClearing.setCheckable(True)
        self.CellC12gridLayout.addWidget(self.C12_1_TakeClearing, 1, 0, 1, 1)
        
        # Добавление кнопки чистки подъёма C11(2)
        self.C12_2_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C12_2_TakeClearing.setObjectName("C12_2_TakeClearing")
        self.C12_2_TakeClearing.setText("2\n01.05.22\nM  10/10")
        self.C12_2_TakeClearing.setCheckable(True)
        self.CellC12gridLayout.addWidget(self.C12_2_TakeClearing, 1, 1, 1, 1)
        
        # Добавление кнопки чистки подъёма C11(3)
        self.C12_3_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C12_3_TakeClearing.setObjectName("C12_3_TakeClearing")
        self.C12_3_TakeClearing.setText("3\n01.05.22\nM  10/10")
        self.C12_3_TakeClearing.setCheckable(True)
        self.CellC12gridLayout.addWidget(self.C12_3_TakeClearing, 2, 0, 1, 1)

        # Добавление кнопки чистки подъёма C12(4)
        self.C12_4_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
        self.C12_4_TakeClearing.setObjectName("C12_4_TakeClearing")
        self.C12_4_TakeClearing.setText("4\n01.05.22\nM  10/10")
        self.C12_4_TakeClearing.setCheckable(True)
        self.CellC12gridLayout.addWidget(self.C12_4_TakeClearing, 2, 1, 1, 1)

        # Добавление вкладки Бригада 1 в tabWidget
        self.TeamsTabWidget.addTab(self.Team1Tab, "Бригада 1")
        
        # Добавление центрального виджета в главное окно
        MainWindow.setCentralWidget(self.centralWidget)

        # Добавление макета ванны C12 в макет Ряда
        self.RowHorizontalLayout.addLayout(self.CellC12gridLayout)
        
    def C11CellClearingClicked(self, checked):
        print(checked)
        
    def C11_1_TakeClearingClicked(self, checked):
        print(checked)
        
    def C11_2_TakeClearingClicked(self, checked):
        print(checked)

        
    def C12CellClearingClicked(self, checked):
        print(checked)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
