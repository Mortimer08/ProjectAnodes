# экспорт и импорт данных
import pickle
file_name='cells.data'
#
# импорт данных из файла
def importing(cells, takes, teams):
    file_for_import = open(file_name, 'rb')
    cells = pickle.load(file_for_import)
    takes = pickle.load(file_for_import)
    teams = pickle.load(file_for_import)

# экспорт данных в файл
def exporting():
    file_for_export=open(file_name, 'wb')
    pickle.dump(cells, file_for_export)
    pickle.dump(takes, file_for_export)
    pickle.dump(teams, file_for_export)
    file_for_export.close()
    del cells
    del takes
    del teams
