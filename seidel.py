import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import interface
import sys

def testProblem(x, y):
    value = 1 - x * x - y * y
    return value

def boundary1(x, y):
    value = -y * y
    return value

def boundary2(x, y):
    value = -x * x
    return value

def countEpsN(oldSol, newSol):
        vec1 = []
        vec1.append(oldSol[1][1])
        vec1.append(oldSol[1][2])
        vec1.append(oldSol[2][1])
        vec1.append(oldSol[2][2])

        vec2 = []
        vec2.append(newSol[1][1])
        vec2.append(newSol[1][2])
        vec2.append(newSol[2][1])
        vec2.append(newSol[2][2])

        value = 0
        for i in range(4):
            vec2[i] = np.abs(vec2[i] - vec1[i])
            if (vec2[i] > value):
                value = vec2[i]

        return value
        

class Example(QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Консольное приложение по модулю 8-9. Петров Павел, гр. 381803-1, команда 1.")
        self.setWindowIcon(QIcon('boat.jpg'))
        self.buildSolution.clicked.connect(self.solutionClicked)
        self.iterate.clicked.connect(self.iterateClicked)

        self.oldSol = np.zeros((4, 4))
        self.newSol = np.zeros((4, 4))

        self.x = np.linspace(-1, 1, 4)
        self.y = np.linspace(-1, 1, 4)

        self.nMax = 0
        self.iter = 0
        self.eps = 0.0
        self.epsN = 0.0

        for j in range(0, 4):
            for i in range(0, 4):
                if (j == 0):
                    self.oldSol[j][i] = boundary2(self.x[i], self.y[j])

                if (j == 3):
                    self.oldSol[j][i] = boundary2(self.x[i], self.y[j])

                if ((j == 1) or (j == 2)) and ((i == 0) or (i == 3)):
                    self.oldSol[j][i] = boundary1(self.x[i], self.y[j])

        for j in range(0, 4):
            for i in range(0, 4):
                if (j == 0):
                    self.newSol[j][i] = boundary2(self.x[i], self.y[j])

                if (j == 3):
                    self.newSol[j][i] = boundary2(self.x[i], self.y[j])

                if ((j == 1) or (j == 2)) and ((i == 0) or (i == 3)):
                    self.newSol[j][i] = boundary1(self.x[i], self.y[j])


        # создание таблицы
        self.tableForSolution.setRowCount(4)
        self.tableForSolution.setColumnCount(4)

        head = []
        for i in range(0, 4):
            temp = "x" + str(i) + " = " + str(self.x[i])
            head.append(temp)

        self.tableForSolution.setVerticalHeaderLabels(head)

        head.clear()
        for i in range(0, 4):
            temp = "y" + str(i) + " = " + str(self.y[i])
            head.append(temp)

        self.tableForSolution.setHorizontalHeaderLabels(head)

        # заполним таблицу исходя из начальных условий
        for j in range(4):
            for i in range(4):
                temp = str(self.oldSol[j][i])
                newItem = QTableWidgetItem(temp)
                self.tableForSolution.setItem(j, i, newItem)

        self.tableForSolution.resizeColumnsToContents()

    def solutionClicked(self):
        if (self.lineEditForNMAX.text() == ""):
            QMessageBox.question(self, 'Ошибка!', "Не введено максимальное число итераций!", QMessageBox.Ok, QMessageBox.Ok)
            return
            
        if (self.lineEditForEps.text() == ""):
            QMessageBox.question(self, 'Ошибка!', "Не введена требуемая точность!", QMessageBox.Ok, QMessageBox.Ok)
            return

        # считываю максимальное число итераций
        temp = self.lineEditForNMAX.text()
        self.nMax = int(temp)

        # считываю точность
        temp = self.lineEditForEps.text()
        self.eps = float(temp)

        for i in range(self.iter, self.nMax):
            self.iterateClicked()
            if (i > 0) and (self.epsN < self.eps):
                return


    def iterateClicked(self):
        if (self.lineEditForNMAX.text() == ""):
            QMessageBox.question(self, 'Ошибка!', "Не введено максимальное число итераций!", QMessageBox.Ok, QMessageBox.Ok)
            return
            
        if (self.lineEditForEps.text() == ""):
            QMessageBox.question(self, 'Ошибка!', "Не введена требуемая точность!", QMessageBox.Ok, QMessageBox.Ok)
            return

        # считываю максимальное число итераций
        temp = self.lineEditForNMAX.text()
        self.nMax = int(temp)

        # считываю точность
        temp = self.lineEditForEps.text()
        self.eps = float(temp)

        if (self.iter >= self.nMax):
            QMessageBox.question(self, 'Предупреждение!', "Превышено допустимое число итераций!", QMessageBox.Ok, QMessageBox.Ok)
            return

        if (self.iter > 0):
            self.epsN = countEpsN(self.oldSol, self.newSol)
            temp = "Достигнутая точность: " + str(self.epsN)
            self.labelForEpsN.setText(temp)

            if (self.epsN < self.eps):
                QMessageBox.question(self, 'Предупреждение!', "Достигнута заданная точность!", QMessageBox.Ok, QMessageBox.Ok)
                return

        A = -9
        hk = 9 / 4
        f = -7/2

        vec = []
        vec.append(self.newSol[1][1])
        vec.append(self.newSol[1][2])
        vec.append(self.newSol[2][1])
        vec.append(self.newSol[2][2])

        self.newSol[1][1] = 1/A * (f - hk * vec[1] - hk * vec[2])
        self.newSol[1][2] = 1/A * (f - hk * vec[0] - hk * vec[3])
        self.newSol[2][1] = 1/A * (f - hk * vec[0] - hk * vec[3])
        self.newSol[2][2] = 1/A * (f - hk * vec[1] - hk * vec[2])

        if (self.iter > 0):
            vec2 = []
            vec2.append(self.oldSol[1][1])
            vec2.append(self.oldSol[1][2])
            vec2.append(self.oldSol[2][1])
            vec2.append(self.oldSol[2][2])

            self.oldSol[1][1] = 1/A * (f - hk * vec2[1] - hk * vec2[2])
            self.oldSol[1][2] = 1/A * (f - hk * vec2[0] - hk * vec2[3])
            self.oldSol[2][1] = 1/A * (f - hk * vec2[0] - hk * vec2[3])
            self.oldSol[2][2] = 1/A * (f - hk * vec2[1] - hk * vec2[2])

        for j in range(4):
            for i in range(4):
                temp = str(self.newSol[j][i])
                newItem = QTableWidgetItem(temp)
                self.tableForSolution.setItem(j, i, newItem)

        self.iter += 1
        temp = "Проведено итераций: " + str(self.iter)
        self.labelForIt.setText(temp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    app.exec()