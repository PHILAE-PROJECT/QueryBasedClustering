#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 2021

@author: Vahana Dorcis (dor6vahana@gmail.com)
"""
import sys
from PyQt6.QtWidgets import QApplication
from Analysis import Analysis

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Analysis()
    window.show()
    app.exec()
