#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, QMenu, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir
from centralwidget import CentralWidget
import centralwidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.initMenuBar()
        self.initStatusBar()
        self.initToolBar()
        self.initCentralWidget()

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Huffman')
        self.show()

    def initMenuBar(self):
        self.createActions()
        self.fileMenu = QMenu('&File(F)', self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addMenu(self.fileMenu)

    def initToolBar(self):
        pass

    def initStatusBar(self):
        pass

    def initCentralWidget(self):
        self.cenwid = CentralWidget()
        self.setCentralWidget(self.cenwid)

    def createActions(self):
        self.openAct = QAction(QIcon('res/file.svg'), '&Open ...', shortcut='Ctrl+O',
                               triggered=self.open)
        self.exitAct = QAction(QIcon('res/exit.svg'), '&Exit', shortcut='Ctrl+Q',
                               triggered=self.close)

    def open(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open File', QDir.currentPath())
        if fileName[0]:
            centralwidget.file2pro = fileName[0]
            file2pro = fileName[0]
            with open(fileName[0], 'r') as f:
                data2Decode = f.read()
                self.cenwid.textArea.setText(data2Decode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    huff = MainWindow()
    sys.exit(app.exec_())
