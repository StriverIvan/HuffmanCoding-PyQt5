#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint
import centralwidget
import os
import time


class Node:
    def __init__(self, character, freq):
        self.left = None
        self.right = None
        self.character = character
        self.freq = freq
        self.absx = 0
        self.absy = 0
        self.xp = 0
        self.yp = 0
        self.d = 0
        self.zt = 0
        self.yt = 0

    def __gt__(self, other):
        if other is None:
            return -1
        if not isinstance(other, Node):
            return -1
        return self.freq > other.freq


class PaintTree(QWidget):
    repaintSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.repaintSignal.connect(self.repaint)
        self.fre = {}
        self.node = []
        self.initUI()
        self.dataPro()
        # self.build_tree()

    def initUI(self):
        self.move(300, 200)
        self.resize(1200, 750)
        self.setMinimumSize(1200, 750)
        self.setMaximumSize(1200, 750)
        self.setWindowTitle("PaintTree")
        self.show()

    def dataPro(self):
        name = os.path.splitext(centralwidget.file2pro)
        path = name[0] + "-freq.txt"
        with open(path, 'r') as f:
            while True:
                str = f.readline()
                if str == "":
                    break
                x = str.split(" ")
                x[0].strip()
                x[1].strip()
                self.fre[x[0]] = x[1]
                self.node.append(Node(x[0], int(x[1])))
        # 冒泡排序
        for x in range(len(self.node)):
            for y in range(len(self.node)):
                if self.node[x] < self.node[y]:
                    temp = self.node[x]
                    self.node[x] = self.node[y]
                    self.node[y] = temp

        n = len(self.node) + 4
        # 坐标计算
        width = self.width()
        height = self.height()
        self.space = int(width / n)
        self.leftspace = self.rightspace = 2 * self.space


        for x in range(len(self.node)):
            self.node[x].absx = int(self.leftspace + (2*x+1)*(self.space/2))
            self.node[x].absy = int(height / 3)
            self.node[x].d = int(self.space / 4)
            self.node[x].zt = int(self.space / 2)
            self.node[x].yt = int(self.space / 2)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawUI(qp)
        qp.end()

    def drawUI(self, qp):
        for node in self.node:
            self.drawUI_helper(qp, node)

    def drawUI_helper(self, qp, root):
        if root is None:
            return

        qp.setPen(QColor(250, 0, 0))
        qp.drawEllipse(QPoint(root.absx, root.absy), root.d, root.d)
        qp.setPen(QColor(0, 0, 0))
        if root.character is not None:
            qp.drawText(QPoint(root.absx, root.absy), root.character)
        qp.drawText(QPoint(int(root.absx+root.d), int(root.absy+root.d)), str(root.freq))
        if root.left is not None:
            root.left.absy = root.absy + 60
            root.left.absx = (root.absx - root.left.xp)
            qp.drawLine(root.absx, root.absy, root.left.absx, root.left.absy)
        if root.right is not None:
            root.right.absy = root.absy + 60
            root.right.absx = (root.absx + root.right.xp)
            qp.drawLine(root.absx, root.absy, root.right.absx, root.right.absy)
        self.drawUI_helper(qp, root.left)
        self.drawUI_helper(qp, root.right)

    def build_tree(self):
        while len(self.node) > 1:
            node1 = self.node[0]
            node2 = self.node[1]
            node3 = Node(None, node1.freq+node2.freq)
            node3.absx = int((node1.absx + node2.absx) / 2)
            node3.zt = node1.zt + node1.yt
            node3.yt = node2.zt + node2.yt
            node1.xp = node3.absx - node1.absx
            node2.xp = node2.absx - node3.absx
            node3.absy = node1.absy - 60
            node3.d = node1.d
            node3.left = node1
            node3.right = node2
            self.node.pop(0)
            self.node.pop(0)
            self.node.insert(0,node3)
            self.repaintSignal.emit()
            time.sleep(3)
            height = self.height()
            while node3.absy != int(height/3):
                node3.absy += 1
                self.repaintSignal.emit()
                time.sleep(0.03)
            leng = len(self.node)
            for i in range(leng-1):
                if self.node[i] > self.node[i+1]:
                    j = i + 1
                    newix = self.node[i].absx + self.node[j].zt + self.node[j].yt
                    newjx = self.node[j].absx - self.node[i].zt - self.node[i].yt
                    temp = self.node[i]
                    self.node[i] = self.node[j]
                    self.node[j] = temp
                    self.node[i].absx = newjx
                    self.node[j].absx = newix
                    self.repaintSignal.emit()
                    time.sleep(2)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_S:
            self.build_tree()
