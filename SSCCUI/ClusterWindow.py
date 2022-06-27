#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 2021

@author: Vahana Dorcis (dor6vahana@gmail.com)
"""
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow


class ClusterWindow(QMainWindow):

    def __init__(self, window_size: QtCore.QRect):
        super().__init__()
        self.resize(window_size.size())
        # Add menu bar
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(window_size.x(), window_size.y(), window_size.width(), 30))
        self.menu_options = QtWidgets.QMenu(self.menu_bar)
        self.menu_options.setTitle("Options")

        self.action_display_graph = QAction(self)
        self.action_display_graph.setText("Show graph")

        self.action_display_graph_full = QAction(self)
        self.action_display_graph_full.setText("Show graph without loop (WL)")

        self.action_view_graph_full = QAction(self)
        self.action_view_graph_full.setText("Save graph WL content (digraph)")

        self.action_view_graph = QAction(self)
        self.action_view_graph.setText("Save graph content (digraph)")

        self.action_save_result = QAction(self)
        self.action_save_result.setText("Save result to Excel")

        self.menu_options.addAction(self.action_display_graph)
        self.menu_options.addAction(self.action_view_graph)
        self.menu_options.addAction(self.action_display_graph_full)
        self.menu_options.addAction(self.action_view_graph_full)
        self.menu_options.addAction(self.action_save_result)

        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.addAction(self.menu_options.menuAction())
        self.setMenuBar(self.menu_bar)

        self.margin_bottom = 20
        widget_size = QtCore.QRect(0, self.menu_bar.geometry().bottom(), window_size.width(),
                                   window_size.height() - self.menu_bar.geometry().bottom() - self.margin_bottom)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setGeometry(widget_size)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #5d6d7e;
                font-size: 10em;
            }
            QTreeView {
                alternate-background-color: #f6fafb;
                background: #e8f4fc;
            }
            QTreeView::item:open {
                background-color: #c5ebfb;
                color: blue;
            }
            QHeaderView {
                color: #fff;
                background-color: #000;
                font-size: 12em;
                font-weight: bold;
            }
            """
        )

        self.tree = QtWidgets.QTreeWidget(self.centralWidget)
        self.tree.resize(self.centralWidget.size())
    # end __init__

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        widget_size = QtCore.QSize(a0.size().width(), a0.size().height() - self.menu_bar.geometry().bottom()
                                   - self.margin_bottom)
        self.centralWidget.resize(widget_size)
        self.tree.resize(self.centralWidget.size())
    # end resizeEvent
# end ClusterWindow
