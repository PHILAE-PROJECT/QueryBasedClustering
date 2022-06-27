#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 2021

@author: Vahana Dorcis (dor6vahana@gmail.com)
"""
import ast
import graphviz
import json
import pandas
import tempfile
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog
from ClusterWindow import ClusterWindow
from HelpWindow import HelpWindow
from PrefixSuffixFactorizedModel import PrefixSuffixFactorizedModel
from SequencesStringComparisonClustering import SequencesStringComparisonClustering
from ui import UI


class Analysis(UI):

    def __init__(self):
        super().__init__()
        self.window_help = HelpWindow()
        self.setWindowTitle("Sequences String Comparison Clustering (SSCC)")
        # -fx-base: #2c3e50;
        self.action_help_about.triggered.connect(lambda: self.window_help.about())
        self.action_help_enter_sequence.triggered.connect(lambda: self.window_help.enter_sequences())
        self.action_help_parameters.triggered.connect(lambda: self.window_help.clustering_parameters())
        self.action_help_upload_sequences.triggered.connect(lambda: self.window_help.upload_sequences())
        self.action_help_graph.triggered.connect(lambda: self.window_help.display_graph())

        self.action_display_in_ui.triggered.connect(lambda: self.upload_and_display())
        self.action_generate_clusters.triggered.connect(lambda: self.upload_and_generate_clusters())
        self.action_generate_graph.triggered.connect(lambda: self.upload_and_generate_graph())

        self.btnGenCluster.clicked.connect(lambda: self.generate_clusters())
        self.btnGenGraph.clicked.connect(lambda: self.generate_graph())
        self.sequences, self.clusters = list(), list()
        self.graph = str()
        self.graph_original = str()
        self._data_columns, self._data_rows = list(), list()
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #5d6d7e;
            }
            QLabel {
                font-size: 13px;
            }
            QTreeView {
                alternate-background-color: yellow;
            }
            """)
        self.window_cluster = ClusterWindow(QtCore.QRect(0, 0, 500, 500))
        self.window_cluster.action_display_graph.triggered.connect(lambda: self.display_graph())
        self.window_cluster.action_display_graph_full.triggered.connect(
            lambda: self.display_graph_without_reflexive_arcs())
        self.window_cluster.action_save_result.triggered.connect(lambda: self.save_to_excel())
        self.window_cluster.action_view_graph_full.triggered.connect(lambda: self.save_graph(False))
        self.window_cluster.action_view_graph.triggered.connect(lambda: self.save_graph(True))
        self.window_alert = QtWidgets.QMainWindow()
    # end __init__

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # print(self.status_bar.geometry().bottom() - self.txtSequences.geometry().bottom() - self.status_bar.height())
        margin = 20
        width = a0.size().width() - self.widget.geometry().width() - (margin * 2)
        height = a0.size().height() - self.txtSequences.geometry().top() * 2
        height -= (self.status_bar.height() * 2) - (margin * 2)
        self.txtSequences.setFixedSize(width, height)
        self.widget.move(width + margin, self.widget.geometry().top())
        self.splitter.move(width + margin, self.splitter.geometry().top())
    # end resizeEvent

    def get_selected_file_content(self):
        """
        Set the sequences to the content of the selected file if the file content is valid.
        """
        filepath = QFileDialog.getOpenFileName(self, "Select file", filter="JSON files (*.json)")
        if not filepath or not filepath[0]:
            return None
        # end if
        with open(filepath[0], "r") as f:
            try:
                return json.load(f)
            except Exception as ex:
                QtWidgets.QMessageBox.critical(self, "File upload error", str(ex),
                                               QtWidgets.QMessageBox.StandardButton.Ok)
        # end with
    # end get_selected_file_content

    def _set_sequences_from_file(self) -> bool:
        """
        Update the values of the sequences using the content of the uploaded files.
        """
        content = self.get_selected_file_content()
        if content is None:
            return False
            # end if
        self.sequences = list()
        if isinstance(content, list) is True:
            self.sequences = content
        # end if
        if not self.sequences:
            self.display_alert(title="File upload", message="No sequence was read from the file.")
            return False
        # end if
        return True
    # end _set_sequences_from_file

    def _set_sequences_from_input(self) -> bool:
        """
        Update the values of the sequences using the user's input.
        """
        self.sequences = self._get_textbox_content()
        if not self.sequences:
            self.display_alert(title="Enter sequences", message="Sequence not found")
            return False
        # end if
        return True
    # end _set_sequences_from_input

    def upload_and_display(self):
        """
        Display the content of the file in the textbox
        """
        content = self.get_selected_file_content()
        if content is not None:
            cleaned = str()
            for c in content:
                if c:
                    if cleaned:
                        cleaned += "\n"
                    # end if
                    cleaned += str(c)
                # end if
            # end for
            self.txtSequences.setPlainText(cleaned)
        # end if
    # end upload_and_display

    def upload_and_generate_clusters(self):
        """
        Use the content of the file to create the clusters.
        """
        if self._set_sequences_from_file() is False:
            return
        # end if
        self._create_clusters()
        self.display_clusters()
    # end upload_and_generate_clusters

    def upload_and_generate_graph(self):
        """
        Use the content of the file to generate a graph.
        """
        if self._set_sequences_from_file() is False:
            return
        # end if
        self._create_graph_content()
        self.display_graph()
        # end if
    # end upload_and_generate_graph

    def generate_clusters(self):
        """
        Use the content of the textbox to generate the clusters.
        """
        if self._set_sequences_from_input() is False:
            return
        # end if
        self._create_clusters()
        self.display_clusters()
    # end generate_clusters

    def generate_graph(self):
        """
        Use the content of the textbox to generate the graph.
        """
        if self._set_sequences_from_input() is False:
            return
            # end if
        self._create_clusters()
        self.display_graph()
    # end generate_graph

    def _create_clusters(self):
        """
        Generate the clusters using the parameters.
        """
        if not self.sequences:
            return list()
        # end if
        _, _, _, dict_patterns = SequencesStringComparisonClustering.create_clusters(
            self.sequences, consider_order_of_sequence=self.get_cos, consider_immediate_occurrence=self.get_cio,
            consider_duplicate_values=self.get_cdv, immediate_occurrence_max=self.get_max_cio)

        self.clusters = list()
        self._data_rows = list()
        self._data_columns = ["Cluster #", "Cluster Size", "Pattern", "Sequence Count", "Sequence"]
        for cn, values in dict_patterns.items():
            dic_count = dict()
            for cluster_item in values[1]:
                key = str(cluster_item)
                if key in dic_count.keys():
                    dic_count[key] += 1
                else:
                    dic_count[key] = 1
            # end for

            cluster_size = str(len(values[1]))
            pattern = str(values[0])
            item = QtWidgets.QTreeWidgetItem([str(cn), cluster_size, pattern])
            for sequence, items_count in dic_count.items():
                item.addChild(QtWidgets.QTreeWidgetItem([str(), str(items_count), sequence]))
                self._data_rows.append([cn, cluster_size, pattern, items_count, sequence])
            # end for
            self.clusters.append(item)
        # end for
        self._create_graph_content()
    # end _create_clusters

    def _create_graph_content(self):
        if not self.sequences:
            self.graph = self.graph_original = str()
            return
        # end if
        model = PrefixSuffixFactorizedModel(build_with_loop=True)
        model.build_prefix_tree_acceptor(list_of_sequences=self.sequences)
        self.graph = model.get_pta_content()

        model = PrefixSuffixFactorizedModel(build_with_loop=False)
        model.build_prefix_tree_acceptor(list_of_sequences=self.sequences)
        self.graph_original = model.get_pta_content()
    # end _create_graph_content

    def _get_textbox_content(self) -> list:
        content = self.txtSequences.toPlainText()
        if not content:
            return list()
        # end if
        try:
            # Convert to list
            converted = list()
            for c in content.split("\n"):
                converted.append(ast.literal_eval(c))
            # end for
            return converted
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Enter sequences error", str(ex),
                                           QtWidgets.QMessageBox.StandardButton.Ok)
            return list()
        # end try
    # end _get_textbox_content

    def save_to_excel(self):
        """
        Save the clustering result to Excel (.xlsx)
        """
        if not self._data_rows or not self._data_columns:
            box = QtWidgets.QMessageBox.warning(self, "", "There is no data to save",
                                                QtWidgets.QMessageBox.StandardButton.Ok)
            box.show()
            return
        # end if
        filepath = QFileDialog.getSaveFileName(self, "Save result", filter="Excel files (*.xlsx)")
        if not filepath or not filepath[0]:
            return
        # end if
        file_name = filepath[0]
        df = pandas.DataFrame(data=self._data_rows, columns=self._data_columns)
        df.to_excel(file_name)
    # end save_to_excel

    def save_graph(self, with_reflexive_arc: bool):
        if not self.graph or not self.graph_original:
            box = QtWidgets.QMessageBox.warning(self, "", "There is no data to save",
                                                QtWidgets.QMessageBox.StandardButton.Ok)
            box.show()
            return
        # end if
        filepath = QFileDialog.getSaveFileName(self, "Save graph", filter="Text file (*.txt)")
        if not filepath or not filepath[0]:
            return
        # end if
        file_name = filepath[0]
        with open(file_name, "w") as f:
            f.write(self.graph if with_reflexive_arc is True else self.graph_original)
        # end with
    # end save_graph

    def display_clusters(self):
        self.window_cluster.setWindowTitle("Cluster Results")
        self.window_cluster.tree.clear()
        self.window_cluster.tree.setColumnCount(3)
        self.window_cluster.tree.setHeaderLabels(["Cluster #", "Cluster size", "Patterns / Sequences"])
        self.window_cluster.tree.insertTopLevelItems(0, self.clusters)
        self.window_cluster.show()
    # end display_clusters

    def display_graph(self):
        if not self.graph:
            return
        # end if
        graph = graphviz.Source(self.graph)
        name = tempfile.NamedTemporaryFile()
        graph.render(view=True, filename=name.name, format="png")
    # end display_graph

    def display_graph_without_reflexive_arcs(self):
        if not self.graph_original:
            return
        # end if
        graph = graphviz.Source(self.graph_original)
        name = tempfile.NamedTemporaryFile()
        graph.render(view=True, filename=name.name, format="png")
    # end display_graph

    def display_alert(self, title: str, message: str):
        QtWidgets.QMessageBox.warning(self, title, message, QtWidgets.QMessageBox.StandardButton.Ok)
    # end display_alert

# end Analysis


