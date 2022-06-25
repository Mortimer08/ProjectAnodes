# Import pandas, use for import data from excel
#import pandas as pd

import pickle
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

    # метод get_row возвращяет информацию об отношении ванны к ряду
    def get_row(self):
        return self.__row
        
    # метод get_number возвращает информацию о номере ванны в ряду        
    def get_number(self):
        return self.__number
        
    # метод get_name возвращает имя ванны
    def get_name(self):
        return self.__name

    # метод get_team возвращяет номер бригады, в подшефность которой относится ванна
    def get_team(self):
        return self.team
        
    # метод set_team позволяет изменять номер бригады - подшефность ванны        
    def set_team(self, team):
        self.team = team
        
    # метод clearing вносит данные о чистке ванны (дату и комменттарий) в словарь clearing_info
    def clearing(self,date,comment):        
            #date = str_to_date(date)
            self.clearing_info[date] = comment        
            
    # метод get_clearing_info возвращает все данные о чистке ванны
    def get_clearing_info(self):
        return self.clearing_info

    # метод get_last_clear возвращает дату последней чистки ванны
    def get_last_clear(self):
        if self.clearing_info == {}:
            return None
        else:
            return max(self.clearing_info.keys())
               
# класс team - для объектов бригада

class team:
    
    def __init__(self, team_number):
        self.team_number = team_number
    
    # метод get_cells_subjected выбирает из списка cells и возвращает список ванн, подшефных бригаде
    def get_cells_subjected(self, cells):
        cells_subjected = []
        for cell in cells:            
            if cells[cell].get_team() == self.team_number:
                cells_subjected.append(cells[cell])
        return cells_subjected
        
    

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
        
    # метод clearing вносит данные о чистке подъёма (дату, количество анодов почищенных на машине, вручную, негодных, замененных и комментарий) в словарь clearing_info
    def clearing(self, date, anodes_w703,  anodes_hand, anodes_bad, anodes_changed, comment):        
            #date = str_to_date(date)
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
            
# функция перевода строки дата в формат datetime
def str_to_date(date_str):
    if type(date_str) is str:
        valid_date = datetime.strptime(date_str, '%d.%m.%Y').date()
    else:
        valid_date = date_str
    return  valid_date

# функкция проверки - находится ли искомая дата в промежутке между двумя остальными
def is_date_between(str_date_target,  str_date1, str_date2):
    date_target = str_to_date(str_date_target)
    date1= str_to_date(str_date1)
    date2= str_to_date(str_date2)
    if date1 <= date_target <= date2:
        return True
    else:
        return False
        
# функция подсчёта количества чисток ванн в заданный период
# cells - список ванн, str_date1 - начальная дата (формат %d.%m.%Y), str_date2 - конечная дата (формат %d.%m.%Y)
def get_cells_cleared(cells, str_date1, str_date2):
    count = 0
    for cell in cells:
        for date in cells[cell].get_clearing_info().keys():
            if is_date_between (date, str_date1,  str_date2):
                count += 1
            
## формирование словаря с объектами класса cell
#cells={}
#
#for i in range (1, 52):
#    cell_name_for_filling = 'A'+str(i)
#    cells[cell_name_for_filling]=cell('A', i, 5 if i<11 else 3)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'B'+str(i)
#    cells[cell_name_for_filling]=cell('B', i, 5 if i<11 else 4)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'C'+str(i)
#    cells[cell_name_for_filling]=cell('C', i, 5 if i<11 else 1)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'D'+str(i)
#    cells[cell_name_for_filling]=cell('D', i, 5 if i<11 else 2)
#
#teams = {}
#teams[1] = team(1)
#teams[2] = team(2)
#teams[3] = team(3)
#teams[4] = team(4)
#teams[5] = team(5)
#
## редактирование свойства team
#
#for i in range (11, 52):
#    cell_name_for_filling = 'B'+str(i)
#    cells[cell_name_for_filling].set_team(4)
#    
#for i in range (11, 52):
#    cell_name_for_filling = 'C'+str(i)
#    cells[cell_name_for_filling].set_team(1)
#    
#for i in range (11, 52):
#    cell_name_for_filling = 'D'+str(i)
#    cells[cell_name_for_filling].set_team(2)
#
## формирование словаря с объектами класса take
#takes={}
#
#for i in range (1, 52):
#    cell_name_for_filling = 'A'+str(i)
#    takes[cell_name_for_filling] = {}    
#    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
#    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
#    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
#    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'B'+str(i)
#    takes[cell_name_for_filling] = {}    
#    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
#    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
#    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
#    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'C'+str(i)
#    takes[cell_name_for_filling] = {}    
#    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
#    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
#    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
#    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
#    
#for i in range (1, 52):
#    cell_name_for_filling = 'D'+str(i)
#    takes[cell_name_for_filling] = {}    
#    takes[cell_name_for_filling][1] = take(cells[cell_name_for_filling], 1)
#    takes[cell_name_for_filling][2] = take(cells[cell_name_for_filling], 2)
#    takes[cell_name_for_filling][3] = take(cells[cell_name_for_filling], 3)
#    takes[cell_name_for_filling][4] = take(cells[cell_name_for_filling], 4)
    


# экспорт и импорт данных
file_name='cells.data'
#
# импорт данных из файла
file_for_import = open(file_name, 'rb')
cells = pickle.load(file_for_import)
takes = pickle.load(file_for_import)
teams = pickle.load(file_for_import)

# тело программы - внесение изменений в данные, анализ данных

#takes['C11'][1].clearing('2.1.2022', 20, 0, 3, 0, 'Примечание')
#
# Импорт данных из файла Excel
# Assign spreadsheet filename to `file`
#file = 'xls_data_ready_to_import.xls'
#
## Load spreadsheet
#xl = pd.ExcelFile(file)
#
## Print the sheet names
##print(xl.sheet_names)
#
## Load a sheet into a DataFrame by name: df1
## список имён листов исходного файла Excel
#sheets_letters = ['Бригада 1', 'Бригада 2','Бригада 3','Бригада 4','Бригада 5']
## список имён ванн и подъёмов
#cell_index = []
## список вспомогательных строк, подлежащих удалению перед анализом основной информации
#rows_to_delete = []
#
## перебираем листы исходного файла Excel
#for s_l in sheets_letters:
#    # в df1 сохраняем результат парсинга листа
#    df1 = xl.parse(s_l)
#    # буква для ряда ванн
#    letter = ''
#    # номер ванны
#    number = ''
#    # номер подъёма
#    tk_nr = ''
#    # наименование строки вида 'A11_1t', где A - буква ряда ванн, 11 - номер ванны (вместе - cell_name), 1 - номер подъёма
#    #  (0, если строка содержит инфомацию о чистке ванны), 
#    # t - дополнительная литера:
#    # e - пустая - для строки с информацией о ванне, t - для строки с информацией о датах чистки подъёмов
#    # b - для строки с информацией о количестве анодов с прогарами в подъёме, c - для строки с информацией о количестве замененных анодов
#    # w - для строки с информацией о количестве анодов, почищенных на машине
#    # h - для строки с информацией о количестве анодов, почищенных вручную
#    str_index = ''
#    # дополнительная литера по умолчанию
#    add_letter = 'e'
#    # перебираем строки DataFrame с результатом парсинга страницы
#    for row in df1.index:
#        # если в столбце 'Unnamed: 2' (третьем по счёту) содержится текст 'Ванна' формирруем наименование строки
#        #  с нулевым номером подъёма и дополнительной литерой e 
#        if df1['Unnamed: 2'].loc[row] == 'Ванна':
#            letter = df1['Unnamed: 0'].loc[row]
#            number = str(int(df1['Unnamed: 1'].loc[row]))
#            tk_nr = '_0'
#            str_index = f'{letter}{number}{tk_nr}{add_letter}'
#        
#        # в противном случае проверяем содержимое столбца 'Unnamed: 0' (первого по счёту)
#        # если там содержится текст 'Подъём' - это служебная строка, после которой начинаются строки
#        # с информацией о датах чистки подъёмов. Дополнительная литера t
#        # строка вносится в список подлежащих удалению перед анализом основной информации
#        elif df1['Unnamed: 0'].loc[row] == 'Подъём':
#            add_letter = 't'
#            rows_to_delete.append(row)
#            # остальные строки в цикле пропускаются
#            continue
#        # аналогично
#        elif df1['Unnamed: 0'].loc[row] == 'Прогары':
#            add_letter = 'b'
#            rows_to_delete.append(row)
#            continue            
#        elif df1['Unnamed: 0'].loc[row] == 'Замена':
#            add_letter = 'c'
#            rows_to_delete.append(row)
#            continue    
#        elif df1['Unnamed: 0'].loc[row] == 'Машина':
#            add_letter = 'w'
#            rows_to_delete.append(row)
#            continue
#        elif df1['Unnamed: 0'].loc[row] == 'Вручную':
#            add_letter = 'h'
#            rows_to_delete.append(row)
#            continue
#        # если в строке 'Unnamed: 2' содержится 1, 2, 3 или 4
#        elif df1['Unnamed: 2'].loc[row] == 1 or df1['Unnamed: 2'].loc[row] == 2 or df1['Unnamed: 2'].loc[row] == 3 or df1['Unnamed: 2'].loc[row] == 4:
#            # формируется наименование строки, содержащее информацию о чистке подъёма анодов, 
#            # с соотвествующим номером подъёма и дополнительной литерой
#            letter = df1['Unnamed: 0'].loc[row]
#            number = str(int(df1['Unnamed: 1'].loc[row]))
#            tk_nr = '_'+str(int(df1['Unnamed: 2'].loc[row]))
#            str_index = f'{letter}{number}{tk_nr}{add_letter}'
#        # в список наименований строк вносится сформированное наименование
#        cell_index.append(str_index)
#    # удаляем вспомогательные строки
#    df1.drop(labels = rows_to_delete, inplace = True)
#    # изменяем список индексов, в соответствии с новыми наименованиями строк
#    df1.index = cell_index
#    # удаляем вспомогательные столбцы (Series). В DataFrame остаётся только основная информация
#    df1.drop(columns = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2'], inplace = True)
#    # очищаем списки с индексами строк и удаляемыми строками
#    cell_index.clear()
#    rows_to_delete.clear()
#    # очищаем содержимое переменных    
#    letter = ''
#    number = ''
#    tk_nr = ''
#    str_index = ''
#    add_letter = ''
#    # переменные для наименований строк с данными о
#    # количестве анодов с прогарами
#    anodes_bad_index = ''
#    # количестве замененных анодов
#    anodes_changed_index = ''
#    # количестве анодов, почищенных на машине
#    anodes_machine_index = ''
#    # количестве анодов, почищенных вручную
#    anodes_hand_index = ''
#    # дата чистки (ванны или подъёма анодов)
#    date_clearing = None
#    # переменные для
#    # количестве анодов с прогарами
#    anodes_bad = None
#    # количестве замененных анодов
#    anodes_changed = None
#    # количестве анодов, почищенных на машине
#    anodes_machine = None
#    # количестве анодов, почищенных вручную
#    anodes_hand = None
#    # перебираем строки DataFrame с основной информацией
#    # cell_name_temp содержит имя очередной строки вида 'A11_1t'
#    for cell_name_temp in df1.index:
#        # имя ванны - для работы с классом cell
#        cell_name = cell_name_temp[0:-3]
#        # номер подъёма - для работы с классом cell
#        tk_nr = int(cell_name_temp[-2])
#        # дополнительная литера
#        add_letter = cell_name_temp[-1]
#        # если нулевой подъём, значит в строке - информация о чистке ванны
#        if tk_nr == 0:
#            # перебираем данные в строке
#            # target - данные очередной ячейки
#            for target in df1.loc[cell_name_temp]:
#                # если в ячейке не нулевое значение, значит - информация о дате чистки ванны
#                if not pd.isnull(target):
#
#                    date_clearing = pd.to_datetime(target).date()
#                    print(cell_name, date_clearing)
#                    
#                    cells[cell_name].clearing(date_clearing, '')
#
#        # если дополнительная литера - t, значит в строке информация о дате чистки подъёмов
#        elif add_letter == 't':
#            # перебираем столбцы в строке
#            for col in df1.columns:
#                # занечение в ячейке
#                target = df1[col].loc[cell_name_temp]
#                # если значение не нулевое
#                if not pd.isnull(target):
#                    # формируем индексы строк с информацией о прогарах
#                    anodes_bad_index = f'{cell_name}_{tk_nr}b'
#                    # замененных анодах
#                    anodes_changed_index = f'{cell_name}_{tk_nr}c'
#                    # количестве анодов, почищенных на машине
#                    anodes_machine_index = f'{cell_name}_{tk_nr}w'
#                    # количестве анодов, почищенных вручную
#                    anodes_hand_index = f'{cell_name}_{tk_nr}h'   
#                    # дата чистки
#                    date_clearing = pd.to_datetime(target).date()
#                    # данные о чистке подъёма
#                    anodes_bad = 0 if pd.isnull(df1[col].loc[anodes_bad_index]) else int(df1[col].loc[anodes_bad_index])
#                    anodes_changed = 0 if pd.isnull(df1[col].loc[anodes_changed_index]) else int(df1[col].loc[anodes_changed_index])
#                    anodes_machine = 0 if pd.isnull(df1[col].loc[anodes_machine_index]) else int(df1[col].loc[anodes_machine_index])
#                    anodes_hand = 0 if pd.isnull(df1[col].loc[anodes_hand_index]) else int(df1[col].loc[anodes_hand_index])
#                    takes[cell_name][tk_nr].clearing(date_clearing, anodes_machine, anodes_hand, anodes_bad, anodes_changed, '')
##                    print(f'Ванна {cell_name}, подъём {tk_nr}, прогаров {anodes_bad}, заменено {anodes_changed}, \
##                    на машине {anodes_machine}, вручную {anodes_hand}, дата {date_clearing}')  



#
r0 = takes['C11'][1].get_row()
r1 = takes['C11'][1].get_cell_number()
r2 = takes['C11'][1].get_cell_name()
r3 = takes['C11'][1].get_take_number()
r4 = takes['C11'][1].get_take_name()
r5 = takes['C11'][1].get_team()
r6 = takes['C11'][1].get_anodes_apriori()
r7 = takes['C11'][1].get_clearing_info()
r8 = takes['C11'][1].get_last_clear()
#

#
print('Ряд {0}, Номер ванны {1}, Имя ванны {2}, номер подъёма {3}, имя подъёма {4}'. format(r0, r1, r2, r3, r4))
print('бригада {0}, анодов в подъёме {1}, данные о чистке {2}, последняя чистка {3}'. format(r5, r6, r7, r8))

r0 = cells['B2'].get_row()
r1 = cells['B2'].get_number()
r2 = cells['B2'].get_name()
r5 = cells['B2'].get_team()
r7 = cells['B2'].get_clearing_info()
r8 = cells['B2'].get_last_clear()
#

#
print('Ряд {0}, Номер ванны {1}, Имя ванны {2}'. format(r0, r1, r2))
print('бригада {0}, данные о чистке {1}, последняя чистка {2}'. format(r5, r7, r8))

#print(get_cells_cleared(cells, '1.1.2022','30.07.2022'))



# экспорт данных в файл
file_for_export=open(file_name, 'wb')
pickle.dump(cells, file_for_export)
pickle.dump(takes, file_for_export)
pickle.dump(teams, file_for_export)
file_for_export.close()
del cells
del takes
del teams
