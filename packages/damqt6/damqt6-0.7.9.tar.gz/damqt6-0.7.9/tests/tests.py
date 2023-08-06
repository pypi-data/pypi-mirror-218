#!/usr/bin/env python3

__appname__ = 'Tests'

import sys
from time import sleep

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QWidgetItem, QLayout

from src.damqt6 import QApplication, QTopMainWindow, QBaseTable

app = QApplication([])

app.setApplicationName(__appname__)

# mainwindow = QTopMainWindow()
# mainwindow.show()

class QTestWidget(QWidget):
    def __init__(self, name:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __del__(self):
        print(f'deleted {self.name}')


l1 = QVBoxLayout()
l2 = QVBoxLayout()

w1 = QTestWidget('w1')
w2 = QTestWidget('w2')

# w1.setLayout(l1)
l2.addWidget(w1)
l2.addWidget(w2)
l1.addLayout(l2)

# print(w2.parent() is w1)
w2 = None
l2 = None
# l1 = None
# w1 = None
# l3 = None

print(l1.count())


def clear():
    while l1.count():
        item = l1.takeAt(0)
        print(item is w1)
        print(item is w2)
        # if hasattr(item, 'widget'):
        #     l1.removeWidget(item.widget())
        # if hasattr(item, 'layout'):
        #     l1.removeItem(item.layout())


clear()


print(l1.count())

pass
pass

# l2 = None
l1 = None
l1 = None
l1 = None
l1 = None

# w1 = QTestWidget('w1')
# w2 = QTestWidget('w2')
# w2.setParent(w1)
# print(len(w1.children()))
# del w1.children()[0]
# w2.setParent(None)
# w2.deleteLater()
# print(w2.name)
# print(len(w1.children()))
# while len(w1.children()) > 0:
#     sleep(0.1)
# sleep(2)
