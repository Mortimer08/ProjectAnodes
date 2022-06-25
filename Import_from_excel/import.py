# Import pandas
import pandas as pd

# Импорт данных из файла Excel используются классы cells и takes из основного модуля
# Assign spreadsheet filename to `file`
file = 'xls_data_ready_to_import.xls'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Print the sheet names
#print(xl.sheet_names)

# Load a sheet into a DataFrame by name: df1
# список имён листов исходного файла Excel
sheets_letters = ['Бригада 1', 'Бригада 2','Бригада 3','Бригада 4','Бригада 5']
# список имён ванн и подъёмов
cell_index = []
# список вспомогательных строк, подлежащих удалению перед анализом основной информации
rows_to_delete = []

# перебираем листы исходного файла Excel
for s_l in sheets_letters:
    # в df1 сохраняем результат парсинга листа
    df1 = xl.parse(s_l)
    # буква для ряда ванн
    letter = ''
    # номер ванны
    number = ''
    # номер подъёма
    tk_nr = ''
    # наименование строки вида 'A11_1t', где A - буква ряда ванн, 11 - номер ванны (вместе - cell_name), 1 - номер подъёма
    #  (0, если строка содержит инфомацию о чистке ванны), 
    # t - дополнительная литера:
    # e - пустая - для строки с информацией о ванне, t - для строки с информацией о датах чистки подъёмов
    # b - для строки с информацией о количестве анодов с прогарами в подъёме, c - для строки с информацией о количестве замененных анодов
    # w - для строки с информацией о количестве анодов, почищенных на машине
    # h - для строки с информацией о количестве анодов, почищенных вручную
    str_index = ''
    # дополнительная литера по умолчанию
    add_letter = 'e'
    # перебираем строки DataFrame с результатом парсинга страницы
    for row in df1.index:
        # если в столбце 'Unnamed: 2' (третьем по счёту) содержится текст 'Ванна' формирруем наименование строки
        #  с нулевым номером подъёма и дополнительной литерой e 
        if df1['Unnamed: 2'].loc[row] == 'Ванна':
            letter = df1['Unnamed: 0'].loc[row]
            number = str(int(df1['Unnamed: 1'].loc[row]))
            tk_nr = '_0'
            str_index = f'{letter}{number}{tk_nr}{add_letter}'
        
        # в противном случае проверяем содержимое столбца 'Unnamed: 0' (первого по счёту)
        # если там содержится текст 'Подъём' - это служебная строка, после которой начинаются строки
        # с информацией о датах чистки подъёмов. Дополнительная литера t
        # строка вносится в список подлежащих удалению перед анализом основной информации
        elif df1['Unnamed: 0'].loc[row] == 'Подъём':
            add_letter = 't'
            rows_to_delete.append(row)
            # остальные строки в цикле пропускаются
            continue
        # аналогично
        elif df1['Unnamed: 0'].loc[row] == 'Прогары':
            add_letter = 'b'
            rows_to_delete.append(row)
            continue            
        elif df1['Unnamed: 0'].loc[row] == 'Замена':
            add_letter = 'c'
            rows_to_delete.append(row)
            continue    
        elif df1['Unnamed: 0'].loc[row] == 'Машина':
            add_letter = 'w'
            rows_to_delete.append(row)
            continue
        elif df1['Unnamed: 0'].loc[row] == 'Вручную':
            add_letter = 'h'
            rows_to_delete.append(row)
            continue
        # если в строке 'Unnamed: 2' содержится 1, 2, 3 или 4
        elif df1['Unnamed: 2'].loc[row] == 1 or df1['Unnamed: 2'].loc[row] == 2 or df1['Unnamed: 2'].loc[row] == 3 or df1['Unnamed: 2'].loc[row] == 4:
            # формируется наименование строки, содержащее информацию о чистке подъёма анодов, 
            # с соотвествующим номером подъёма и дополнительной литерой
            letter = df1['Unnamed: 0'].loc[row]
            number = str(int(df1['Unnamed: 1'].loc[row]))
            tk_nr = '_'+str(int(df1['Unnamed: 2'].loc[row]))
            str_index = f'{letter}{number}{tk_nr}{add_letter}'
        # в список наименований строк вносится сформированное наименование
        cell_index.append(str_index)
    # удаляем вспомогательные строки
    df1.drop(labels = rows_to_delete, inplace = True)
    # изменяем список индексов, в соответствии с новыми наименованиями строк
    df1.index = cell_index
    # удаляем вспомогательные столбцы (Series). В DataFrame остаётся только основная информация
    df1.drop(columns = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2'], inplace = True)
    # очищаем списки с индексами строк и удаляемыми строками
    cell_index.clear()
    rows_to_delete.clear()
    # очищаем содержимое переменных    
    letter = ''
    number = ''
    tk_nr = ''
    str_index = ''
    add_letter = ''
    # переменные для наименований строк с данными о
    # количестве анодов с прогарами
    anodes_bad_index = ''
    # количестве замененных анодов
    anodes_changed_index = ''
    # количестве анодов, почищенных на машине
    anodes_machine_index = ''
    # количестве анодов, почищенных вручную
    anodes_hand_index = ''
    # дата чистки (ванны или подъёма анодов)
    date_clearing = None
    # переменные для
    # количестве анодов с прогарами
    anodes_bad = None
    # количестве замененных анодов
    anodes_changed = None
    # количестве анодов, почищенных на машине
    anodes_machine = None
    # количестве анодов, почищенных вручную
    anodes_hand = None
    # перебираем строки DataFrame с основной информацией
    # cell_name_temp содержит имя очередной строки вида 'A11_1t'
    for cell_name_temp in df1.index:
        # имя ванны - для работы с классом cell
        cell_name = cell_name_temp[0:-3]
        # номер подъёма - для работы с классом cell
        tk_nr = int(cell_name_temp[-2])
        # дополнительная литера
        add_letter = cell_name_temp[-1]
        # если нулевой подъём, значит в строке - информация о чистке ванны
        if tk_nr == 0:
            # перебираем данные в строке
            # target - данные очередной ячейки
            for target in df1.loc[cell_name_temp]:
                # если в ячейке не нулевое значение, значит - информация о дате чистки ванны
                if not pd.isnull(target):

                    date_clearing = pd.to_datetime(target).date()
                    print(cell_name, date_clearing)
                    
                    cells[cell_name].clearing(date_clearing, '')

        # если дополнительная литера - t, значит в строке информация о дате чистки подъёмов
        elif add_letter == 't':
            # перебираем столбцы в строке
            for col in df1.columns:
                # занечение в ячейке
                target = df1[col].loc[cell_name_temp]
                # если значение не нулевое
                if not pd.isnull(target):
                    # формируем индексы строк с информацией о прогарах
                    anodes_bad_index = f'{cell_name}_{tk_nr}b'
                    # замененных анодах
                    anodes_changed_index = f'{cell_name}_{tk_nr}c'
                    # количестве анодов, почищенных на машине
                    anodes_machine_index = f'{cell_name}_{tk_nr}w'
                    # количестве анодов, почищенных вручную
                    anodes_hand_index = f'{cell_name}_{tk_nr}h'   
                    # дата чистки
                    date_clearing = pd.to_datetime(target).date()
                    # данные о чистке подъёма
                    anodes_bad = 0 if pd.isnull(df1[col].loc[anodes_bad_index]) else int(df1[col].loc[anodes_bad_index])
                    anodes_changed = 0 if pd.isnull(df1[col].loc[anodes_changed_index]) else int(df1[col].loc[anodes_changed_index])
                    anodes_machine = 0 if pd.isnull(df1[col].loc[anodes_machine_index]) else int(df1[col].loc[anodes_machine_index])
                    anodes_hand = 0 if pd.isnull(df1[col].loc[anodes_hand_index]) else int(df1[col].loc[anodes_hand_index])
                    takes[cell_name][tk_nr].clearing(date_clearing, anodes_machine, anodes_hand, anodes_bad, anodes_changed, '')
#                    print(f'Ванна {cell_name}, подъём {tk_nr}, прогаров {anodes_bad}, заменено {anodes_changed}, \
#                    на машине {anodes_machine}, вручную {anodes_hand}, дата {date_clearing}')  
