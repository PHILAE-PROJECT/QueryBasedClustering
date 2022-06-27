#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 2021

@author: Vahana Dorcis (dor6vahana@gmail.com)
"""
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow


class HelpWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        width = 500
        height = 400
        self.resize(QtCore.QSize(width, height))
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setGeometry(QtCore.QRect(0, 0, width, height))
        self.container = QtWidgets.QTextEdit(self.centralWidget)
        self.container.setGeometry(0, 0, self.centralWidget.width(), self.centralWidget.height())
        self.container.setReadOnly(True)
    # end __init__

    def about(self):
        self.centralWidget.children().clear()
        self.setWindowTitle("HELP - About")
        content = "Developed by <strong>Vahana Dorcis</strong><br/><br/>"
        content += "This application uses the Sequences String Comparison Clustering (SSCC) algorithm to create the "
        content += "clusters. SSCC was inspired by gene sequencing comparison and Needleman–Wunsch algorithm. It is a "
        content += "pattern based algorithm. It uses the parameters (Consider Order of Sequence, "
        content += "Consider Duplicate Values, Consider Immediate Occurrence) to create the patterns used for "
        content += "clustering."
        self.container.setText(content)
        self.show()
    # end about

    def enter_sequences(self):
        self.setWindowTitle("HELP - Enter sequences")
        content = "The sequence should be provided as a list, meaning it begins with "
        content += "<strong>[</strong> and ends with <strong>]</strong>. Below are some examples: "
        content += "['a', 'a', 'b', 'c', 'd']<br/>[['u', 0], ['s', 0], ['s', 0], ['a', 0], ['s', -2], ['p', 0]]"
        self.container.setText(content)
        self.show()
    # end enter_sequences

    def clustering_parameters(self):
        self.setWindowTitle("HELP - Parameters")
        content = "<strong>Consider Order of Sequence (COS)</strong> sorts the sequence when set to No otherwise the "
        content += "sequence remains the same. <br/>Example: Given S = ['d', 'a', 'b', 'c'], the sequence becomes "
        content += "['a', 'b', 'c', 'd'] if COS = No.<br/>"
        content += "<strong>Consider Immediate Occurrence (CIO)</strong> deals with repeated back-to-back values. "
        content += "When No, only one value is kept if it is repeated back-to-back otherwise the values are kept up "
        content += "to <strong>Max Immediate Occurrence</strong>. "
        content += "<br/>Example: Given S = ['d', 'b', 'd', 'd', 'a', 'd', 'd', 'd', 'd'], "
        content += "S = ['d', 'b', 'd', 'a', 'd'] for CIO = No and S = ['d', 'b', 'd', 'd', 'a', 'd', 'd'] "
        content += "for CIO = Yes. <br/>"
        content += "<strong>Consider Duplicate Values (CDV)</strong> strips duplicate values from the sequence when "
        content += "set to No. When combined with CIO, only the first set of duplicate is kept in accordance with CIO. "
        content += "<br/>Example: Given S = ['a', 'a', 'a', 'b', 'a'], for CDV = CIO = No, S = ['a', 'b']; "
        content += "S = ['a', 'a', 'b'] for CDV = No and CIO = Yes. When CDV = Yes, S remains the same unless "
        content += "CIO = No, in which case S = ['a', 'b', 'a']."
        self.container.setText(content)
        self.show()
    # end clustering_parameters

    def upload_sequences(self):
        self.setWindowTitle("HELP - Upload sequences")
        content = "The file to upload should be a json file. The content of the file should be a list. "
        content += "<br/>Example: [['i', 't', 'e', 'm', '1'], ['i', 't', 'e', 'm', '2']]"
        self.container.setText(content)
        self.show()
    # end upload_sequences

    def display_graph(self):
        self.setWindowTitle("HELP - Graph display")
        content = "The model is a factorization of the prefixes and suffixes in the sequences displayed in a "
        content += "tree manner.<br/>"
        content += "<strong>Graph without self-loop</strong> displays the model without self-loop. If there is "
        content += "stuttering in the sequences, the value appears as many times as present in the sequences. "
        content += "This could take a while to render.<br/>"
        content += "<strong>Graph with self-loop</strong> displays the model with self-loop. When there is stuttering, "
        content += "the value appears once."
        self.container.setText(content)
        self.show()
    # end display_graph

# end HelpWindow
