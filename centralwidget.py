#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QPushButton, QLayout
from PyQt5.QtGui import QFont
from painttree import PaintTree
from sender import Sender


file2pro = "data/data.txt"


class CentralWidget(QWidget):

    def __init__(self):
        super(CentralWidget, self).__init__()

        self.initUI()

    def initUI(self):

        self.textArea = QTextEdit()
        self.textArea.setFont(QFont("consolas"))
        self.huffArea = QTextEdit()
        self.huffArea.setFont(QFont("consolas"))
        self.decodeArea = QTextEdit()
        self.decodeArea.setFont(QFont("consolas"))

        self.eButton = QPushButton()
        self.eButton.setText('Encode')
        self.eButton.clicked.connect(self.encodeAct)

        self.dButton = QPushButton()
        self.dButton.setText('Decode')
        self.dButton.clicked.connect(self.decodeAct)

        self.bButton = QPushButton()
        self.bButton.setText("BuildTree")
        self.bButton.clicked.connect(self.buildAct)

        self.sendBtn = QPushButton("Send")
        self.sendBtn.clicked.connect(self.sendAct)

        grid = QGridLayout()
        grid.addWidget(self.textArea, 1, 1, 1, 1)
        grid.addWidget(self.eButton, 2, 1)
        grid.addWidget(self.huffArea, 3, 1, 1, 1)
        grid.addWidget(self.dButton, 4, 1)
        grid.addWidget(self.bButton, 5, 1)
        grid.addWidget(self.sendBtn, 5, 2)
        self.setLayout(grid)
        grid.addWidget(self.decodeArea, 1, 2, 4, 1)

    def encodeAct(self):
        str = 'python hc.py -c %s ' % file2pro
        os.system(str)
        name = os.path.splitext(file2pro)
        if name[0]:
            str = name[0] + "-map.txt"
            with open(str, 'r') as f:
                codes = f.read()
                self.huffArea.setText(codes)

    def decodeAct(self):
        name = os.path.splitext(file2pro)
        str = "python hc.py -x %s" % (name[0]+".bin")
        if name[0]:
            os.system(str)
            str = name[0]+"-extract.txt"
            with open(str, 'r') as f:
                data2Decode = f.read()
                self.decodeArea.setText(data2Decode)

    def buildAct(self):
        self.win = PaintTree()


    def sendAct(self):
        self.win = Sender()

#