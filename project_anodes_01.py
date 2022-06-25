
# импортируем pickle для импорта/экспорта данных
# импортируем datetime для работы с датами
import pickle
from datetime import datetime
# импортируем классы Qt для работы с GUI
from PyQt6 import QtCore, QtWidgets#, QtGui
import sys

# класс cell - ванна
class cell:
    
# свойство "row" - ряд - отношение к ряду A,B,C,D (str)
# свойство "number" - номер - порядковый номер ванны в ряду (int)
# свойство "team" - подшефность бригаде с номером (int)
# свойство "clearing_info" - информация о чистке - даты и примечания \
#                 {дата1:'примечание 1', дата2:'примечание 2',...,датаn:'примечание n'} (dict)

    def __init__(self,row: str, number: int, team: int):
        self.__row = row
        self.__number = number
        self.__name = self.__row+str(self.__number)
        self.team = team
        self.clearing_info = {}

    # метод get_row возвращяет информацию об отношении ванны к ряду (str)
    def get_row(self):
        return self.__row
        
    # метод get_number возвращает информацию о номере ванны (int) в ряду        
    def get_number(self):
        return self.__number
        
    # метод get_name возвращает имя ванны (str)
    def get_name(self):
        return self.__name

    # метод get_team возвращяет номер бригады (int), в подшефность которой относится ванна
    def get_team(self):
        return self.team
        
    # метод set_team позволяет изменять номер бригады - подшефность ванны        
    def set_team(self, team):
        self.team = team
        
    # метод clearing вносит данные о чистке ванны (дату и комментарий) в словарь clearing_info
    def clearing(self,date,comment):        
        date = str_to_date(date)
        self.clearing_info[date] = comment        
            
    # метод get_clearing_info возвращает словарь с данными о чистке ванны
    def get_clearing_info(self):
        return self.clearing_info
    
    def delete_clear(self, date):
        date = str_to_date(date)
        if date not in self.clearing_info:
            return
        else:
            del self.clearing_info[date]

    # метод get_last_clear возвращает дату (datetime.date) последней чистки ванны
    def get_last_clear(self):
        if self.clearing_info == {}:
            return None
        else:
            return max(self.clearing_info.keys())
            
    # метод get_last_comment возвращает комментарий к последней чистке ванны
    def get_last_comment(self):
        if self.clearing_info == {}:
            return None
        else:
            date_target = self.get_last_clear()            
            return self.get_comment(date_target)
            
     # метод get_comment возвращает коментарий о чистке ванны
    def get_comment(self, date):
        if self.clearing_info == {}:
            return None
        else:
            return self.clearing_info[date]
    
    # метод get_cleaning_period возвращает количество дней (datetime.datedelta), прошедших с последней чистки ванны    
    def get_cleaning_period(self):
        if self.clearing_info == {}:
            return None
        else:
            period = datetime.today().date() - max(self.clearing_info.keys())
            return period.days
               
# класс team - для объектов бригада

class team:
    
    def __init__(self, team_number):
        self.team_number = team_number
    
    # метод get_cells_subjected выбирает из словаря cells и возвращает словарь (dict) со списком ванн, подшефных бригаде
    def get_cells_subjected(self, cells):
        cells_subjected = {}
        for cell in cells:            
            if cells[cell].get_team() == self.team_number:
                cells_subjected[cell]=cells[cell]
        return cells_subjected
        
    # метод get_cells_subjected выбирает из словаря takes и возвращает словарь (dict) подъёмов, подшефных бригаде
    def get_takes_subjected(self, takes):
        takes_subjected = {}
        for cell in takes:
            if takes[cell][1].get_team() == self.team_number:
                takes_subjected[cell] = {}
                takes_subjected[cell][1] = takes[cell][1]
                takes_subjected[cell][2] = takes[cell][2]
                takes_subjected[cell][3] = takes[cell][3]
                takes_subjected[cell][4] = takes[cell][4]
        return takes_subjected

# класс take - для объектов подъём анодов       
# свойство "__row" - ряд - отношение к ряду A,B,C,D (str) - копируется из соотвествующей cell
# свойство "__cell_number" - номер - порядковый номер ванны в ряду (int) - копируется из соотвествующей cell
# свойство "__cell_name" - имя соотвествующей ванны, копируется из cell
# свойство "take_number" - номер подъёма
# свойство "take_name" - имя подъёма формата 'A2(3)'
# свойство "team" - подшефность бригаде с номером (int) - копируется из соотвествующей cell
# свойство "anodes_apriori" - количество анодов в подъёме по умолчанию (20 или 21)
# свойство "clearing_info" - информация о чистке - даты, анодов почищенных на машине, вручную, \
#                  негодных анодов, замененых анодов и примечания \
#                 {дата1:w,h,b,c,'примечание 1',...,датаn:w(n),h(n),b(n),c(n),'примечание n'} (dict)

class take(cell):
    
    def __init__(self,cell,take_number):      
        self.__row = cell.get_row()
        self.__cell_number = cell.get_number()
        self.__cell_name = cell.get_name()
        self.take_number = take_number
        self.take_name = (cell.get_name()+'({0})'.format(int(take_number)))
        self.team = cell.get_team()
        self.anodes_apriori = 21 if take_number == 1 else 20
        self.clearing_info = {}        
    
#    @property                                  # не получилось создать свойство сходу, оставим навырост
#    def team(self):
#        self.team = cell.get_name()
        
    # метод get_row возвращяет информацию об отношении ванны к ряду
    def get_row(self):
        return self.__row
    
    # метод get_cell_number возвращает инфомацию о номере ванны, к которой относится подъём
    def get_cell_number(self):
        return self.__cell_number
        
    # метод get_cell_name возвращает имя ванны, к которой относится подъём
    def get_cell_name(self):
        return self.__cell_name
    
    # метод get_take_number возвращает номер подъёма
    def get_take_number(self):
        return self.take_number
    
    # метод get_take_name возвращает имя подъёма
    def get_take_name(self):
        return self.take_name
        
    # метод get_team возвращает номер бригды, к которой относится подъём
    def get_team(self):
        return self.team
        
    # метод clearing вносит данные о чистке подъёма
    # (дату, количество анодов почищенных на машине, вручную, негодных, замененных и комментарий) в словарь clearing_info
    def clearing(self, date, anodes_w703,  anodes_hand, anodes_bad, anodes_bad2, anodes_changed, comment):        
            date = str_to_date(date)
            self.clearing_info[date] = [anodes_w703,  anodes_hand, anodes_bad, anodes_bad2, anodes_changed, comment]
            
    # метод get_anodes_apriori возвращает количество анодов в подъёме
    def get_anodes_apriori(self):
        return self.anodes_apriori
        
    # метод get_clearing_info возвращает все данные о чистке подъёма
    def get_clearing_info(self):
        return self.clearing_info    
    
    # метод get_last_clear возвращает дату последней чистки подъёма
    def get_last_clear(self):
        if self.clearing_info == {}:
            return None
        else:
            return max(self.clearing_info.keys())
            
    # метод get_last_machined возвращает количество заменённых анодов в  последнюю чистку подъёма
    def get_last_machined(self):
        if self.clearing_info == {}:
            return None
        else:
            date_target = max(self.clearing_info.keys())
            return self.get_anodes_machined(date_target)
            
     # метод get_last_handed возвращает количество заменённых анодов в  последнюю чистку подъёма
    def get_last_handed(self):
        if self.clearing_info == {}:
            return None
        else:
            date_target = max(self.clearing_info.keys())
            return self.get_anodes_handed(date_target)       
            
    # метод get_last_changed возвращает количество заменённых анодов в  последнюю чистку подъёма
    def get_last_changed(self):
        if self.clearing_info == {}:
            return None
        else:
            date_target = max(self.clearing_info.keys())
            return self.get_anodes_changed(date_target)        
            
    # метод get_anodes_actual_bad возвращает количество плохих анодов в подъёме
    def get_anodes_actual_bad(self):
        if self.clearing_info == {}:
            return None
        else:
            last_date_cleaning = max(self.clearing_info.keys())
            bad_anodes = self.get_anodes_bad(last_date_cleaning)
            return bad_anodes
            
    # метод get_anodes_actual_bad2 возвращает количество плохих анодов второго типа (с прогаром >10%) в подъёме
    def get_anodes_actual_bad2(self):
        if self.clearing_info == {}:
            return None
        else:
            last_date_cleaning = max(self.clearing_info.keys())
            bad_anodes = self.get_anodes_bad2(last_date_cleaning)
            return bad_anodes            
            
    # метод get_anodes_machined возвращает количество анодов, почищанных на машине в заданную дату
    def get_anodes_machined(self, date):
        date = str_to_date(date)
        return self.clearing_info[date][0]
        
    # метод get_anodes_handed возвращает количество анодов, почищанных вручную в заданную дату
    def get_anodes_handed(self, date):
        date = str_to_date(date)
        return self.clearing_info[date][1]

    # метод get_anodes_changed возвращает количество анодов, почищанных вручную в заданную дату
    def get_anodes_changed(self, date):
        date = str_to_date(date)
        return self.clearing_info[date][-2]
        
     # метод get_anodes_bad возвращает количество анодов на замену, отмеченных в заданную дату
    def get_anodes_bad(self, date):
        date = str_to_date(date)
        return self.clearing_info[date][2]
        
    # метод get_anodes_bad2 возвращает количество анодов на замену второго типа (прогар > 10%), отмеченных в заданную дату
    def get_anodes_bad2(self, date):
        date = str_to_date(date)
        if len(self.clearing_info[date]) < 6:
            return None
        else:
            return self.clearing_info[date][3]
            
    # метод get_comment возвращает комментарий к чистке в заданную дату
    def get_comment(self, date):
        date = str_to_date(date)
        if self.clearing_info == {}:
            return None
        else:
            comment = self.clearing_info[date][-1]
            return comment
            
     # метод get_cleaning_period возвращает количество дней, прошедших с последней чистки подъёма
    def get_cleaning_period(self):
        if self.clearing_info == {}:
            return None
        else:
            period = datetime.today().date() - max(self.clearing_info.keys())
            return period.days

class CellButton(QtWidgets.QPushButton):
    def __init__(self, CellName, CellLastClearingDate):
        super().__init__()
#        self.setParent(parent)
        self.setCheckable(True)
        ButtonText = CellName + " " + CellLastClearingDate
        self.setText(ButtonText)
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        
        for tm, cls in cfw.items():
            # Вкладка для первой бригады
            self.Team1Tab = QtWidgets.QWidget()
            self.Team1Tab.setObjectName("Team1Tab")
            # Макет 
            self.layoutWidget = QtWidgets.QWidget(self.Team1Tab)
            # Размер вкладки первой бригады
            self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1758, 148))
            self.layoutWidget.setObjectName("layoutWidget")
            
            # Установка макета для вертикальной разметки и размещения ряда ванн
            self.verticalLayout_41 = QtWidgets.QVBoxLayout(self.layoutWidget)
            self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_41.setObjectName("verticalLayout_41")

            
            # Макеты для ряда ванн
            self.RowHorizontalLayout_1 = QtWidgets.QHBoxLayout()
            self.RowHorizontalLayout_1.setContentsMargins(1, 1, 1, 1)
            self.RowHorizontalLayout_1.setSpacing(1)
            self.RowHorizontalLayout_1.setObjectName("RowHorizontalLayout_1")
            self.verticalLayout_41.addLayout(self.RowHorizontalLayout_1)
            
            # Макеты для ряда ванн
            self.RowHorizontalLayout_2 = QtWidgets.QHBoxLayout()
            self.RowHorizontalLayout_2.setContentsMargins(1, 1, 1, 1)
            self.RowHorizontalLayout_2.setSpacing(1)
            self.RowHorizontalLayout_2.setObjectName("RowHorizontalLayout_2")
            self.verticalLayout_41.addLayout(self.RowHorizontalLayout_2)

            # Макеты для ряда ванн
            self.RowHorizontalLayout_3 = QtWidgets.QHBoxLayout()
            self.RowHorizontalLayout_3.setContentsMargins(1, 1, 1, 1)
            self.RowHorizontalLayout_3.setSpacing(1)
            self.RowHorizontalLayout_3.setObjectName("RowHorizontalLayout_3")
            self.verticalLayout_41.addLayout(self.RowHorizontalLayout_3)

            # Макеты для ряда ванн
            self.RowHorizontalLayout_4 = QtWidgets.QHBoxLayout()
            self.RowHorizontalLayout_4.setContentsMargins(1, 1, 1, 1)
            self.RowHorizontalLayout_4.setSpacing(1)
            self.RowHorizontalLayout_4.setObjectName("RowHorizontalLayout_4")
            self.verticalLayout_41.addLayout(self.RowHorizontalLayout_4)
            
            cells_in_layout = 0
            
            for cl, clinfo in cls.items():
                cl_name = cl
                cl_last_clear_date = clinfo['last_clearing_date'].strftime('%d.%m.%Y')
#                cl_last_comment = clinfo['last_clearing_comment']
#                cl_period = clinfo['clearing_period']

                # Начало формирования кнопок ванн и подъёмов
                # макет для кнопок ванны
                self.CellC11gridLayout = QtWidgets.QGridLayout()
                self.CellC11gridLayout.setContentsMargins(1, 1, 1, 1)
                self.CellC11gridLayout.setSpacing(1)
                self.CellC11gridLayout.setObjectName(f"Cell{cl_name}gridLayout")
                
                # Добавление кнопки чистки ванны C11CellClearing
                
                
                CellButton1 = CellButton(cl_name, cl_last_clear_date)
                CellButton1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
                CellButton1.setObjectName(f"{cl_name}CellClearing")
                CellButton1.setText(f"{cl} {cl_last_clear_date}")
                self.CellC11gridLayout.addWidget(CellButton1, 0, 0, 1, 2)
                CellButton1.clicked.connect(self.C11CellClearingClicked)
                
                for tk, tkinfo in clinfo['takes_info'].items():
                    tk_number = tk
                    tk_last_clear_date = tkinfo['last_take_clearing_date'].strftime('%d.%m.%Y')
                    tk_period = tkinfo['clearing_period']
                    tk_last_machined = tkinfo['anodes_last_machined']
                    tk_last_handed = tkinfo['anodes_last_handed']
                    tk_last_bad = tkinfo['anodes_last_bad']
                    tk_last_bad2 = tkinfo['anodes_last_bad2']
                    tk_last_changed = tkinfo['anodes_last_changed']
                    tk_last_comment = tkinfo['anodes_last_comment']

                    # Добавление кнопки чистки подъёма C11(1)
                    
                    self.C11_1_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
                    self.C11_1_TakeClearing.setObjectName(f"{cl}_{tk_number}_TakeClearing")
                    self.C11_1_TakeClearing.setText(f"{tk_number}\n{tk_last_clear_date}\nM  {tk_last_bad}/{tk_last_bad2}")
                    self.C11_1_TakeClearing.setCheckable(True)
                    self.CellC11gridLayout.addWidget(self.C11_1_TakeClearing, 1, 0, 1, 1)
                    self.C11_1_TakeClearing.clicked.connect(self.C11_1_TakeClearingClicked)

#                    # Добавление кнопки чистки подъёма C11(2)
#                    self.C11_2_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                    self.C11_2_TakeClearing.setObjectName("C11_2_TakeClearing")
#                    self.C11_2_TakeClearing.setText("2\n01.05.22\nM  10/10")
#                    self.C11_2_TakeClearing.setCheckable(True)
#                    self.CellC11gridLayout.addWidget(self.C11_2_TakeClearing, 1, 1, 1, 1)
#                    self.C11_2_TakeClearing.clicked.connect(self.C11_2_TakeClearingClicked)
#
#
#                    # Добавление кнопки чистки подъёма C11(3)
#                    self.C11_3_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                    self.C11_3_TakeClearing.setObjectName("C11_3_TakeClearing")
#                    self.C11_3_TakeClearing.setText("3\n01.05.22\nM  10/10")
#                    self.C11_3_TakeClearing.setCheckable(True)
#                    self.CellC11gridLayout.addWidget(self.C11_3_TakeClearing, 2, 0, 1, 1)
#
#                    # Добавление кнопки чистки подъёма C11(4)
#                    self.C11_4_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                    self.C11_4_TakeClearing.setObjectName("C11_4_TakeClearing")
#                    self.C11_4_TakeClearing.setText("4\n01.05.22\nM  10/10")
#                    self.C11_4_TakeClearing.setCheckable(True)
#                    self.CellC11gridLayout.addWidget(self.C11_4_TakeClearing, 2, 1, 1, 1)
                
                # Добавление макета ванны C11 в макет Ряда
                if cells_in_layout < 10:
                    self.RowHorizontalLayout_1.addLayout(self.CellC11gridLayout)
                    cells_in_layout += 1
                elif cells_in_layout < 20:
                    self.RowHorizontalLayout_2.addLayout(self.CellC11gridLayout)
                    cells_in_layout += 1
                elif cells_in_layout < 30:
                    self.RowHorizontalLayout_3.addLayout(self.CellC11gridLayout)
                    cells_in_layout += 1
                elif cells_in_layout < 40:
                    self.RowHorizontalLayout_4.addLayout(self.CellC11gridLayout)
                    cells_in_layout += 1
                
#                # макет для кнопок ванны
#                self.CellC12gridLayout = QtWidgets.QGridLayout()
#                self.CellC12gridLayout.setContentsMargins(1, 1, 1, 1)
#                self.CellC12gridLayout.setSpacing(1)
#                self.CellC12gridLayout.setObjectName("CellC12gridLayout")
#                
#                # Добавление чекбокса чистки ванны C12CellClearing
#                self.C12CellClearing = QtWidgets.QPushButton(self.layoutWidget)
#                self.C12CellClearing.setCheckable(True)
#                self.C12CellClearing.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
#                self.C12CellClearing.setObjectName("C12CellClearing")
#                self.C12CellClearing.setText("C12 01.05.22")
#                self.CellC12gridLayout.addWidget(self.C12CellClearing, 0, 0, 1, 2)
#                self.C12CellClearing.clicked.connect(self.C12CellClearingClicked)
#                
#                # Добавление кнопки чистки подъёма C11(1)
#                self.C12_1_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                self.C12_1_TakeClearing.setObjectName("C12_1_TakeClearing")
#                self.C12_1_TakeClearing.setText("1\n01.05.22\nM  10/10")
#                self.C12_1_TakeClearing.setCheckable(True)
#                self.CellC12gridLayout.addWidget(self.C12_1_TakeClearing, 1, 0, 1, 1)
#                
#                # Добавление кнопки чистки подъёма C11(2)
#                self.C12_2_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                self.C12_2_TakeClearing.setObjectName("C12_2_TakeClearing")
#                self.C12_2_TakeClearing.setText("2\n01.05.22\nM  10/10")
#                self.C12_2_TakeClearing.setCheckable(True)
#                self.CellC12gridLayout.addWidget(self.C12_2_TakeClearing, 1, 1, 1, 1)
#                
#                # Добавление кнопки чистки подъёма C11(3)
#                self.C12_3_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                self.C12_3_TakeClearing.setObjectName("C12_3_TakeClearing")
#                self.C12_3_TakeClearing.setText("3\n01.05.22\nM  10/10")
#                self.C12_3_TakeClearing.setCheckable(True)
#                self.CellC12gridLayout.addWidget(self.C12_3_TakeClearing, 2, 0, 1, 1)
#
#                # Добавление кнопки чистки подъёма C12(4)
#                self.C12_4_TakeClearing = QtWidgets.QPushButton(self.layoutWidget)
#                self.C12_4_TakeClearing.setObjectName("C12_4_TakeClearing")
#                self.C12_4_TakeClearing.setText("4\n01.05.22\nM  10/10")
#                self.C12_4_TakeClearing.setCheckable(True)
#                self.CellC12gridLayout.addWidget(self.C12_4_TakeClearing, 2, 1, 1, 1)

                # Добавление вкладки Бригада 1 в tabWidget
                self.TeamsTabWidget.addTab(self.Team1Tab, tm)
                
                # Добавление центрального виджета в главное окно
                MainWindow.setCentralWidget(self.centralWidget)

                # Добавление макета ванны C12 в макет Ряда
#                self.RowHorizontalLayout.addLayout(self.CellC12gridLayout)
        
    def C11CellClearingClicked(self, checked):
        print(checked)
        
    def C11_1_TakeClearingClicked(self, checked):
        print(checked)
        
    def C11_2_TakeClearingClicked(self, checked):
        print(checked)
        
    def C12CellClearingClicked(self, checked):
        print(checked)

        
# функция перевода строки дата в формат datetime
def str_to_date(date_str):
    if isinstance(date_str, str):
        valid_date = datetime.strptime(date_str, '%d.%m.%Y').date()
    else:
        valid_date = date_str
    return valid_date

# функкция проверки - находится ли искомая дата в промежутке между двумя остальными
def is_date_between(str_date_target,  str_date1, str_date2):
    date_target = str_to_date(str_date_target)
    date1 = str_to_date(str_date1)
    date2= str_to_date(str_date2)
    if date1 <= date_target <= date2:
        return True
    else:
        return False
        
# функция подсчёта количества чисток ванн в заданный период
# cells - список ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def count_cells_cleared(cells, str_date1, str_date2):
    count = 0
    for cell in cells:
        for date in cells[cell].get_clearing_info().keys():
            if is_date_between (date, str_date1,  str_date2):
                count += 1
    return count
    
# функция подсчёта количества почищенных на машине анодов в заданный период
# cells - список ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def count_anodes_machined(takes, str_date1, str_date2):
    count = 0
    for cell in takes:
        for take in takes[cell]:
            for date in takes[cell][take].get_clearing_info().keys():
                if is_date_between (date, str_date1,  str_date2):
                    count += takes[cell][take].get_anodes_machined(date)
    return count
    
# функция подсчёта количества почищенных вручную анодов в заданный период
# cells - список ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def count_anodes_handed(takes, str_date1, str_date2):
    count = 0
    for cell in takes:
        for take in takes[cell]:
            for date in takes[cell][take].get_clearing_info().keys():
                if is_date_between (date, str_date1,  str_date2):
                    count += takes[cell][take].get_anodes_handed(date)
    return count
    
# функция подсчёта количества почищенных вручную анодов в заданный период
# cells - список ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def count_anodes_changed(takes, str_date1, str_date2):
    count = 0
    for cell in takes:
        for take in takes[cell]:
            for date in takes[cell][take].get_clearing_info().keys():
                if is_date_between (date, str_date1,  str_date2):
                    count += takes[cell][take].get_anodes_changed(date)
    return count
    
# функция выбора имён ванн, почищенных в заданный период (list)
# cells - словарь ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def list_cells_cleared(cells, str_date1, str_date2):
    list = []
    for cell in cells:
        for date in cells[cell].get_clearing_info().keys():
            if is_date_between (date, str_date1,  str_date2):
                list.append(cell)
    return list
 
# функция выбора имён подъёмов, почищенных в заданный период (list)
# takes - словарь подъёмов, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def list_takes_machined(takes, str_date1, str_date2):
    list = []
    for cell in takes:
        for take in takes[cell]:
            for date in takes[cell][take].get_clearing_info().keys():
                if is_date_between (date, str_date1,  str_date2):
                    if takes[cell][take].get_anodes_machined(date) != 0:
                        list.append(takes[cell][take].get_take_name())
    return list
    
# функция выбора имён подъёмов, почищенных вручную в заданный период (list)
# takes - словарь подъёмов, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def list_takes_handed(takes, str_date1, str_date2):
    list = []
    for cell in takes:
        for take in takes[cell]:
            for date in takes[cell][take].get_clearing_info().keys():
                if is_date_between (date, str_date1,  str_date2):
                    if takes[cell][take].get_anodes_handed(date) != 0:
                        list.append(takes[cell][take].get_take_name())    
    return list

# функци импорта данных из файла
def import_from_file(file_name):
    file_for_import = open(file_name, 'rb')
    cells = pickle.load(file_for_import)
    takes = pickle.load(file_for_import)
    teams = pickle.load(file_for_import)
    return cells, takes, teams
    
# функция экспорта данных в файл
def export_to_file(file_name, cells, takes, teams):
    file_for_export=open(file_name, 'wb')
    pickle.dump(cells, file_for_export)
    pickle.dump(takes, file_for_export)
    pickle.dump(teams, file_for_export)
    file_for_export.close()

    

# функция формирования словаря для окна GUI
# получает словари teams, cells, takes
def dict_for_window(teams, cells, takes):
    # создаём пустой словарь
    cells_for_window = {}
    # перебираем номера бригад
    for team_number in range (1, 6):
        # создаём в словаре запись с ключом 'Бригада team_number' и значением - словарь подшефных ванн
        cells_team_subjected = teams[team_number].get_cells_subjected(cells)
        cells_for_window[f'Бригада {team_number}'] = {}
        # перебираем имена ванн в словаре подшефных ванн бригады
        for cell_name, cell_info in cells_team_subjected.items():
            cells_for_window[f'Бригада {team_number}'][cell_name] = {}
            # определяем дату последней чистки ванны
            last_clearing_date = cell_info.get_last_clear()
            cells_for_window[f'Бригада {team_number}'][cell_name]['last_clearing_date'] = last_clearing_date
            # определяем период чистки ванны
            clearing_periog = cell_info.get_cleaning_period()
            cells_for_window[f'Бригада {team_number}'][cell_name]['clearing_period'] = clearing_periog            
            # находим комментарий к последней чистке ванны
            last_clearing_comment = cell_info.get_last_comment()
            cells_for_window[f'Бригада {team_number}'][cell_name]['last_clearing_comment'] = last_clearing_comment
            cells_for_window[f'Бригада {team_number}'][cell_name]['takes_info'] = {}
            # перебираем имена подъёмов, относящихся к очередной ванне
            for take_number, take_info in takes[cell_name].items():
                cells_for_window[f'Бригада {team_number}'][cell_name]['takes_info'][take_number] = {}
                take_dict = cells_for_window[f'Бригада {team_number}'][cell_name]['takes_info'][take_number]
                # находим дату чистки первого подъёма
                last_take_clearing_date = take_info.get_last_clear()
                take_dict['last_take_clearing_date'] = last_take_clearing_date
                # находим период чистки первого подъёма
                clearing_period= take_info.get_cleaning_period()
                take_dict['clearing_period'] = clearing_period
                # находим количество почищенных на машине в последнюю чистку
                anodes_last_machined = take_info.get_last_machined()
                take_dict['anodes_last_machined'] = anodes_last_machined
                # находим количество почищенных вручную в последнюю чистку
                anodes_last_handed = take_info.get_last_handed()
                take_dict['anodes_last_handed'] = anodes_last_handed
                # находим количество обнаруженных негодных анодов в последнюю чистку
                anodes_last_bad = take_info.get_anodes_actual_bad()
                take_dict['anodes_last_bad'] = anodes_last_bad
                # находим количество обнаруженных негодных анодов второго типа в последнюю чистку
                anodes_last_bad2 = take_info.get_anodes_actual_bad2()
                take_dict['anodes_last_bad2'] = anodes_last_bad2
                # находим количество заменённых анодов в последнюю чистку
                anodes_last_changed = take_info.get_last_changed()
                take_dict['anodes_last_changed'] = anodes_last_changed
                # находим комментарий к последней чистке
                anodes_last_comment = take_info.get_last_comment()
                take_dict['anodes_last_comment'] = anodes_last_comment
    return cells_for_window
        
if __name__ == '__main__':
    # импорт данных из файла
    file_name='cells.data'
    cells, takes, teams = import_from_file(file_name)
    cfw = dict_for_window(teams, cells, takes)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


    # тело программы - внесение изменений в данные, анализ данных
    
    cfw = dict_for_window(teams, cells, takes)
    for tm, cls in cfw.items():
        print(tm)
        for cl, clinfo in cls.items():
            cl_name = cl
            cl_last_clear_date = clinfo['last_clearing_date'].strftime('%d.%m.%Y')
            cl_last_comment = clinfo['last_clearing_comment']
            cl_period = clinfo['clearing_period']
            print(f'Ванна {cl_name}, последняя чистка - {cl_last_clear_date} (период {cl_period}), комментарий')
            for tk, tkinfo in clinfo['takes_info'].items():
                tk_number = tk
                tk_last_clear_date = tkinfo['last_take_clearing_date'].strftime('%d.%m.%Y')
                tk_period = tkinfo['clearing_period']
                tk_last_machined = tkinfo['anodes_last_machined']
                tk_last_handed = tkinfo['anodes_last_handed']
                tk_last_bad = tkinfo['anodes_last_bad']
                tk_last_bad2 = tkinfo['anodes_last_bad2']
                tk_last_changed = tkinfo['anodes_last_changed']
                tk_last_comment = tkinfo['anodes_last_comment']
                print(f'Подъём {tk_number} почищен {tk_last_clear_date} (период {tk_period}), на машине - {tk_last_machined}, вручную - {tk_last_handed}')
                print(f'\tобнаружено {tk_last_bad}/{tk_last_bad2} прогаров,  заменили {tk_last_changed} анодов, комментарий: {tk_last_comment}')

#    print(cells['C11'].get_last_clear())
#    print(cells['C11'].get_clearing_info())
#    cells['C11'].clearing('24.04.2022', '')
#    print(cells['C11'].get_clearing_info())

    # экспорт данных в файл
    export_to_file(file_name, cells, takes, teams)

    del cells
    del takes
    del teams
