# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from functools import partial
# import random
import pygame
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtGui
from PySide6.QtGui import *
from database import Database
from datetime import datetime


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()
        self.ui.btn_send.clicked.connect(self.addNewMessage)
        self.ui.btn_2.clicked.connect(self.delete_all)
        self.ui.btn_3.clicked.connect(self.theme)
        self.readMessages()
        self.thm = 2

        self.ui.setWindowTitle('Message Box')



    def theme(self):
        if self.thm == 1:
            self.ui.setStyleSheet('background-color: rgb(80, 80, 80)')
            self.thm = 2
        elif self.thm == 2:
            self.ui.setStyleSheet('background-color: rgb(230, 230, 230)')
            self.thm = 1
    def readMessages(self):
        messages = Database.select()
        for i, message in enumerate(messages):
            label = QLabel()
            label.setText(message[3] + ' - ' + message[1] + ':' + message[2])
            self.ui.gl_messages.addWidget(label, i, 1)
            btn = QPushButton()
            btn.setMinimumSize(35,35)
            btn.setMaximumSize(35,35)
            btn.setIcon(QIcon('images/recycle.png'))
            btn.clicked.connect(partial(self.delete, message[0], btn, label))
            self.ui.gl_messages.addWidget(btn, i, 0)


    def addNewMessage(self):
        name = self.ui.tb_name.text()
        text = self.ui.tb_text.text()
        time = datetime.now()
        time = time.strftime('%y/%m/%d - %H:%M')
        if name != "" and text != "":
            # add to backend
            response = Database.insert(name, text, time)
            if response:
                # add to frontend
                btn = QPushButton()
                btn.setMinimumSize(35, 35)
                btn.setMaximumSize(35, 35)
                btn.setIcon(QIcon('images/recycle.png'))
                self.ui.gl_messages.addWidget(btn)
                label = QLabel()
                label.setText(time + ' - ' + name + ':' + text)
                self.ui.gl_messages.addWidget(label)

                self.ui.tb_name.setText("")
                self.ui.tb_text.setText("")

                msg_box = QMessageBox()
                msg_box.setText("Your message sent successfully!")
                msg_box.exec_()

            else:
                msg_box = QMessageBox()
                msg_box.setText("Database Error!")
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Error:fields are empty!")
            msg_box.exec_()

    def delete(self, id, btn, label):
        response = Database.delete(id)
        if response:
            btn.hide()
            label.hide()

    def delete_all(self):
        num = self.ui.gl_messages.count()
        dl = Database.delete_all()
        if dl:
            for i in range(num):
                self.ui.gl_messages.itemAt(i).widget().deleteLater()
            msg_box = QMessageBox()
            msg_box.setText("All messages deleted successfully!")
            msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Database Error!")
            msg_box.exec_()

if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec_())
