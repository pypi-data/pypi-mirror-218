# -*- coding: utf-8 -*-
"""
Created Apr-2023

@author: Luis Alfonso Olivares Jimenez

GUI to load text data corresponding to dose profiles and PDD. 

The data should be in M ​​rows by 2 columns, corresponding to positions and
dose values, respectively.

The script has been tested with the following examples:

    * File in w2CAD format (format used by the TPS Eclipse 16.1, from the Varian(R) company).
      In the algorithm, the start of the data is identified by the words: '$STOM' or '$STOD'
      Physical unit assumed to be in mm.

    * File in mcc format (format used by Verisoft 7.1.0.199 software, from PTW(R) company).
      In the algorithm, the beginning of the data is identified by the word: 'BEGIN_DATA'
      Physical unit assumed to be in mm.

    * File in text format
      The data must be distributed in M ​​rows by 2 columns and separated
      for a blank space.
      The script ask for a word to identify the beginning of the data in the text file, 
      a number to add to the positions, and a factor for distance dimension conversion.

After two successful loaded data, normaliztion, gamma index comparison and dose difference are automatically calculated.

"""

import sys
from PyQt6.QtWidgets import QApplication

from relative_dose_1d.GUI_tool import GUI
      
app = QApplication(sys.argv)
window = GUI()
sys.exit(app.exec())

