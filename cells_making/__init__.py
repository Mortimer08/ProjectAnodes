from datetime import datetime

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

    # метод get_last_clear возвращает дату (datetime.date) последней чистки ванны
    def get_last_clear(self):
        if self.clearing_info == {}:
            return None
        else:
            return max(self.clearing_info.keys())
    
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
    def clearing(self, date, anodes_w703,  anodes_hand, anodes_bad, anodes_changed, comment):        
            date = str_to_date(date)
            self.clearing_info[date] = [anodes_w703,  anodes_hand, anodes_bad, anodes_changed, comment]
            
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
            
    # метод get_anodes_actual_bad возвращает количество плохих анодов в подъёме
    def get_anodes_actual_bad(self):
        if self.clearing_info == {}:
            return None
        else:
            last_date_cleaning = max(self.clearing_info.keys())
            bad_anodes = self.get_anodes_bad(last_date_cleaning)
            return bad_anodes
            
    # метод get_anodes_actual_bad возвращает количество плохих анодов второго вида (прогар >10%) в подъёме
    def get_anodes_actual_bad2(self):
        if self.clearing_info == {}:
            return None
        else:
            last_date_cleaning = max(self.clearing_info.keys())
            bad_anodes2 = self.get_anodes_bad2(last_date_cleaning)
            return bad_anodes2
            
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
        return self.clearing_info[date][3]
        
     # метод get_anodes_bad возвращает количество анодов на замену, отмеченных в заданную дату
    def get_anodes_bad(self, date):
        date = str_to_date(date)
        return self.clearing_info[date][2]
        
    # метод get_anodes_bad возвращает количество анодов на замену, отмеченных в заданную дату
    def get_anodes_bad2(self, date):
        date = str_to_date(date)
        if len(self.clearing_info[date]) < 6:
            return None
        else:
            return self.clearing_info[date][3]   
     
     # метод get_cleaning_period возвращает количество дней, прошедших с последней чистки подъёма
    def get_cleaning_period(self):
        if self.clearing_info == {}:
            return None
        else:
            period = datetime.today().date() - max(self.clearing_info.keys())
            return period.days
        
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
    
# функция выбора имён подъёмов, почищенных в заданный период (list)
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
 
# формирование словаря с объектами класса cell
cells={}

for i in range (1, 52):
    cell_name_for_filling = 'A'+str(i)
    cells[cell_name_for_filling]=cell('A', i, 5 if i<11 else 3)
    
for i in range (1, 52):
    cell_name_for_filling = 'B'+str(i)
    cells[cell_name_for_filling]=cell('B', i, 5 if i<11 else 4)
    
for i in range (1, 52):
    cell_name_for_filling = 'C'+str(i)
    cells[cell_name_for_filling]=cell('C', i, 5 if i<11 else 1)
    
for i in range (1, 52):
    cell_name_for_filling = 'D'+str(i)
    cells[cell_name_for_filling]=cell('D', i, 5 if i<11 else 2)

teams = {}
teams[1] = team(1)
teams[2] = team(2)
teams[3] = team(3)
teams[4] = team(4)
teams[5] = team(5)

# редактирование свойства team

for i in range (11, 52):
    cell_name_for_filling = 'B'+str(i)
    cells[cell_name_for_filling].set_team(4)
    
for i in range (11, 52):
    cell_name_for_filling = 'C'+str(i)
    cells[cell_name_for_filling].set_team(1)
    
for i in range (11, 52):
    cell_name_for_filling = 'D'+str(i)
    cells[cell_name_for_filling].set_team(2)

# формирование словаря с объектами класса take
takes={}

for i in range (1, 52):
    cell_name_for_filling = 'A'+str(i)
    takes[cell_name_for_filling] = {}    
    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
    
for i in range (1, 52):
    cell_name_for_filling = 'B'+str(i)
    takes[cell_name_for_filling] = {}    
    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
    
for i in range (1, 52):
    cell_name_for_filling = 'C'+str(i)
    takes[cell_name_for_filling] = {}    
    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
    
for i in range (1, 52):
    cell_name_for_filling = 'D'+str(i)
    takes[cell_name_for_filling] = {}    
    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
