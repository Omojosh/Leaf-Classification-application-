# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'josh.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

# from tkinter import *
# from PIL import ImageTk, Image 
# from tkinter import filedialog
import base64
import requests
import webbrowser
import wikipedia
from time import sleep
from bs4 import BeautifulSoup as bs
import base64
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import sys

try:
    import os
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog


class Ui_Classifier(object):
    def setupUi(self, Classifier):
        Classifier.setObjectName("Classifier")
        Classifier.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Classifier)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(400, 10, 381, 41))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.classifyIt = QtWidgets.QPushButton(self.centralwidget)
        self.classifyIt.setGeometry(QtCore.QRect(560, 390, 121, 41))
        self.classifyIt.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 87 16pt \"Arial Black\";\n"
"background-color: rgb(0, 0, 0);\n"
"font: 75 16pt \"MS Shell Dlg 2\";")    
        self.classifyIt.setObjectName("classifyIt")
        self.learnMore = QtWidgets.QPushButton(self.centralwidget)
        self.learnMore.setGeometry(QtCore.QRect(300, 390, 121, 41))
        self.learnMore.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 87 16pt \"Arial Black\";\n"
"background-color: rgb(0, 0, 0);\n"
"font: 75 16pt \"MS Shell Dlg 2\";")
        self.learnMore.setObjectName("learnMore")
        self.report = QtWidgets.QTextEdit(self.centralwidget)
        self.report.setGeometry(QtCore.QRect(100, 500, 1000, 185))
        self.report.setStyleSheet("font: 75 26pt \"MS Shell Dlg 2\";")
        self.report.setReadOnly(True)
        self.report.setObjectName("report")
        self.pic = QtWidgets.QLabel(self.centralwidget)
        self.pic.setGeometry(QtCore.QRect(260, 60, 631, 321))
        # self.pic.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.pic.setText("")
        self.pic.setObjectName("pic")
        self.UploadPic = QtWidgets.QPushButton(self.centralwidget)
        self.UploadPic.setGeometry(QtCore.QRect(800, 390, 121, 41))
        self.UploadPic.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 87 16pt \"Arial Black\";\n"
"background-color: rgb(0, 0, 0);\n"
"font: 75 16pt \"MS Shell Dlg 2\";")
        self.UploadPic.setObjectName("UploadPic")
        Classifier.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Classifier)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Classifier.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Classifier)
        self.statusbar.setObjectName("statusbar")
        Classifier.setStatusBar(self.statusbar)

        self.retranslateUi(Classifier)
        QtCore.QMetaObject.connectSlotsByName(Classifier)
        ############################################################
        self.UploadPic.clicked.connect(self.uploadIt)
        self.classifyIt.clicked.connect(self.classIt)
        self.learnMore.clicked.connect(self.learnIt)
        

    def uploadIt(self):
            root = tk.Tk()
            style = ttk.Style(root)
            style.theme_use("clam")
            def c_open_file_old():
                    rep = filedialog.askopenfilenames(
    	            parent=root,
    	            initialdir='/',
    	            initialfile='tmp',
    	            filetypes=[
    		                ("PNG", "*.png"),
    		                ("JPEG", "*.jpg"),
    		                ("All files", "*")])
                    label = self.pic
                    def convertTuple(tup): 
                            str =  ''.join(tup) 
                            return str
                    tuple = rep
                    global thePic                        
                    thePic = convertTuple(tuple)
                    print(thePic)       
                    pixmap = QPixmap(thePic)
                    label.setScaledContents(True)
                    label.setPixmap(pixmap)
                #     label.resize(500,300)
                    try:
                            os.startfile(rep[0])
                    except IndexError:  
                            print("No file selected")
            ttk.Button(root, text="Open files", command=c_open_file_old).grid(row=1, column=0, padx=4, pady=4, sticky='ew')
            root.mainloop()
    

    def classIt(self):
        secret_access_key = "0oOPfd9YjmIpNRIyKAOE1saaPqfQr2WmTcH9Y1YHI01Qbh295h"
        class SendForIdentificationError(Exception):
            def __init__(self, m):
                self.message = m

            def __str__(self):
                return self.message
        def send_for_identification(file_names):
            files_encoded = []
            for file_name in file_names:
                with open(file_name, "rb") as file:
                    files_encoded.append(base64.b64encode(file.read()).decode("ascii"))

            params = {
                "latitude": 49.194161,
                "longitude": 16.603017,
                "week": 23,
                "images": files_encoded,
                "key": secret_access_key,
                "parameters": ["crops_fast"]
                }

            # see the docs for more optional attributes
            # for example "custom_id" allows you to work with your custom identifiers
            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post("https://plant.id/api/identify", json=params,
                                    headers=headers)

            if response.status_code != 200:
                raise SendForIdentificationError(response.text)

            # this reference allows you to gather the identification result
            # (once it is ready)
            return response.json().get("id")

        def get_suggestions(request_id):
            params = {
                "key": secret_access_key,
                "ids": [request_id]
            }
            headers = {
                "Content-Type": "application/json"
            }

            # To keep it simple, we are pooling the API waiting for the server
            # to finish the identification.
            # The better way would be to utilize "callback_url" parameter in /identify
            # call to tell our server to call your"s server endpoint once
            # the identification is done.
            while True:
                print("Waiting for suggestions...")
                sleep(5)
                resp = requests.post("https://plant.id/api/check_identifications",
                                    json=params, headers=headers).json()
                if resp[0]["suggestions"]:
                    return resp[0]["suggestions"]

        # more photos of the same plant increase the accuracy
        request_id = send_for_identification([thePic])

        # just listing the suggested plant names here (without the certainty values)
        for suggestion in get_suggestions(request_id):
            global name
            name = (suggestion["plant"]["name"]).replace(" ", "_")
            self.report.setText(name)
            name = self.report.toPlainText()

    def learnIt(self):
        print(name)
        URL = "https://en.wikipedia.org/wiki/"+name
        print(URL)
        html = requests.get(URL).text
        soup = bs(html, 'html.parser')
        # b= ta.find("td").renderContents().strip()
        # print(b)
        tb = soup.findAll("tr")
        print(tb)
        # print(tb)
        tag_a = tb[10].find('a')
        tag_b = tb[12].find('a')
        print(tag_a.text)
        # print(tag_a)
        # for tag in tb:
        # print (tag.contents[0])
        #print(tag[4])
        # print(tb[2])
        # print(tag_a.text)
        if not tag_a.text:
            webbrowser.open('https://en.wikipedia.org/wiki/'+name)
        else:
            print("Family:", tag_a.text)
            self.report.append("Family:"+ tag_a.text)
            self.report.append("Genus:"+ tag_b.text)
            self.report.append(wikipedia.summary(tag_a.text))


    def retranslateUi(self, Classifier):
        _translate = QtCore.QCoreApplication.translate
        Classifier.setWindowTitle(_translate("Classifier", "MainWindow"))
        self.textEdit.setHtml(_translate("Classifier", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">      Leaf Classification System </span></p></body></html>"))
        self.classifyIt.setText(_translate("Classifier", "  Classify "))
        self.learnMore.setText(_translate("Classifier", "  LearnMore "))
        self.UploadPic.setText(_translate("Classifier", "Upload Pic"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Classifier = QtWidgets.QMainWindow()
    ui = Ui_Classifier()
    ui.setupUi(Classifier)
    Classifier.show()
    sys.exit(app.exec_())
