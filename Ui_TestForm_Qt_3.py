from PyQt6 import QtCore, QtWidgets

class CellButton(QtWidgets.QPushButton):
    def __init__(self, parent, CellName, CellLastClearingDate, CellLastClearingComment):
        super().__init__()
        self = QtWidgets.QPushButton(parent)
        self.CellName = CellName
        self.CellLastClearingDate = CellLastClearingDate
        self.CellLastClearingComment = CellLastClearingComment
        
        self.setText(CellName)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = QtWidgets.QWidget()
    CellGrid = QtWidgets.QGridLayout(MyWindow)
    
    FirstCellButton = CellButton(MyWindow,'C11', '20.05.2022', 'No Comment')
    SecondCellButton = CellButton(MyWindow,'C12', '20.05.2022', 'No Comment')
    CellGrid.addWidget(FirstCellButton)
    CellGrid.addWidget(SecondCellButton)
    MyWindow.show()
    sys.exit(app.exec())
