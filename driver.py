# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:31:21 2022

@author: hcaslan
"""
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction
from qt import Ui_MainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
    #closing alert
    def closeEvent(self, event):
        close = QMessageBox()
        close.setWindowTitle("Window Close")
        close.setIcon(QMessageBox.Critical)
        close.setText("Are you sure you want to close the window?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close.setDefaultButton(QMessageBox.Cancel)
        
        #If there is no output or if the output has already been saved in a way, do not ask if it is desired to save when closing.
        if(self.ui.pB_clearOutput.isEnabled() == False or self.ui.pB_exportAsOutput.isEnabled() == False or self.ui.pB_saveAsOutput.isEnabled() == False or self.ui.pB_saveOutput.isEnabled() == False):
            close = close.exec()
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        #else ask the user for if it is desired to save when closing.
        else:
            close.setStandardButtons(QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel)
            close = close.exec()
            if close == QMessageBox.Yes:
                print("Yes")
                event.accept()
            elif close == QMessageBox.Save:
                print("Save")
                self.op.saveAsOutputImage(self.ui)
            else:
                print("Ignore")
                event.ignore()
            

app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.show()
sys.exit(app.exec_())