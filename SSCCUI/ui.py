#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 2021

@author: Vahana Dorcis (dor6vahana@gmail.com)
"""
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        text_box_width, widget_width = 350, 400
        left = top = 10
        default_size = QtCore.QRect(0, 0, text_box_width + widget_width + (left * 3), 400)

        self.resize(default_size.size())

        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setGeometry(default_size)

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setText("Enter one sequence per line")
        self.label.move(left, top)
        text_box_height = 300  # default_size.height() - self.label.geometry().bottom() - (top * 2)

        self.txtSequences = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.txtSequences.setPlaceholderText("Sample: [\'a\', \'a\', \'b\', \'c\', \'d\']")
        self.txtSequences.setGeometry(left, self.label.geometry().bottom(), text_box_width, text_box_height)

        self.widget = QtWidgets.QWidget(self.centralWidget)
        widget_size = QtCore.QRect(text_box_width + (left * 2), self.txtSequences.geometry().top(), widget_width, 100)
        self.widget.setGeometry(widget_size)

        # Holds the buttons and combobox block
        self.lblCos = QtWidgets.QLabel(self.widget)
        self.lblCos.setText("Consider Order of Sequence")
        self.cbCos = QtWidgets.QComboBox(self.widget)

        self.lblCdv = QtWidgets.QLabel(self.widget)
        self.lblCdv.setText("Consider Duplicate Values")
        self.cbCdv = QtWidgets.QComboBox(self.widget)

        self.lblCio = QtWidgets.QLabel(self.widget)
        self.lblCio.setText("Consider Immediate Occurrence")
        self.cbCio = QtWidgets.QComboBox(self.widget)

        self.lblMaxCio = QtWidgets.QLabel(self.widget)
        self.lblMaxCio.setText("Max Immediate Occurrence")
        self.txtMaxCio = QtWidgets.QTextEdit(self.widget)
        self.txtMaxCio.setText("2")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.lblCos, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.cbCos, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.lblCdv, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.cbCdv, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.lblCio, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.cbCio, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.lblMaxCio, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.txtMaxCio, 3, 1, 1, 1)
        self.gridLayout.setSpacing(5)

        # self.widget.resize(self.gridLayout.)
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #2c3e50;
                color: #FFF; font-size: 12em;
            }
        """)
        self.splitter.setGeometry(QtCore.QRect(
            widget_size.left(), self.widget.geometry().bottom() + top, widget_size.width(), 100))
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self.btnGenCluster = QtWidgets.QPushButton(self.splitter)
        # self.btnGenPattern = QtWidgets.QPushButton(self.splitter)
        self.btnGenGraph = QtWidgets.QPushButton(self.splitter)
        self.btnGenCluster.setText("Generate Clusters")
        # self.btnGenPattern.setText("Generate Patterns")
        self.btnGenGraph.setText("Generate Graph")
        self.setCentralWidget(self.centralWidget)
        # self.btnGenGraph.clicked.connect(lambda x: print("HERE"))

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, default_size.width(), 30))
        self.menu_help = QtWidgets.QMenu(self.menu_bar)
        self.menu_help.setTitle("Help")
        self.menu_upload_sequences = QtWidgets.QMenu(self.menu_bar)
        self.menu_upload_sequences.setTitle("Upload sequences")
        self.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.action_help_about = QAction(self)
        self.action_help_about.setText("About")
        self.action_help_parameters = QAction(self)
        self.action_help_parameters.setText("Parameters")
        self.action_help_enter_sequence = QAction(self)
        self.action_help_enter_sequence.setText("Enter sequences")
        self.action_help_upload_sequences = QAction(self)
        self.action_help_upload_sequences.setText("Upload sequences")
        self.action_help_graph = QAction(self)
        self.action_help_graph.setText("Show graph")

        self.action_display_in_ui = QAction(self)
        self.action_display_in_ui.setText("Display in UI")
        self.action_generate_clusters = QAction(self)
        self.action_generate_clusters.setText("Generate Clusters")
        self.action_generate_graph = QAction(self)
        self.action_generate_graph.setText("Generate Graph")

        self.menu_help.addAction(self.action_help_about)
        self.menu_help.addAction(self.action_help_parameters)
        self.menu_help.addAction(self.action_help_enter_sequence)
        self.menu_help.addAction(self.action_help_upload_sequences)
        self.menu_help.addAction(self.action_help_graph)

        self.menu_upload_sequences.addAction(self.action_display_in_ui)
        self.menu_upload_sequences.addAction(self.action_generate_clusters)
        self.menu_upload_sequences.addAction(self.action_generate_graph)

        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_bar.addAction(self.menu_upload_sequences.menuAction())
        combo_items = ["Yes", "No"]
        self.cbCos.addItems(combo_items)
        self.cbCdv.addItems(combo_items)
        self.cbCio.addItems(combo_items)
        self.cbCdv.setCurrentIndex(1)
        box_size = QtCore.QSize(90, 30)
        self.cbCos.setMaximumSize(box_size)
        self.cbCio.setMaximumSize(box_size)
        self.cbCdv.setMaximumSize(box_size)
        self.txtMaxCio.setMaximumSize(box_size)
        self.cbCio.currentTextChanged.connect(self.toggle_max_cio)
    # end __init__

    @property
    def get_cos(self) -> bool:
        return "Y" in self.cbCos.currentText()
    # end get_cos

    @property
    def get_cdv(self) -> bool:
        return "Y" in self.cbCdv.currentText()
    # end get_cdv

    @property
    def get_cio(self) -> bool:
        return "Y" in self.cbCio.currentText()
    # end get_cio

    @property
    def get_max_cio(self) -> int:
        try:
            n = int(self.txtMaxCio.toPlainText())
            if n < 2:
                return 2
            # end if
            return n
        except TypeError as ex:
            return 2
        except Exception as ex:
            return 2
        # end try
    # end get_max_cio

    def toggle_max_cio(self, value: str):
        is_visible = self.get_cio  # not self.txtMaxCio.isVisible()
        self.txtMaxCio.setVisible(is_visible)
        self.lblMaxCio.setVisible(is_visible)
    # end toggle_max_cio

# end UI

