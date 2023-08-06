# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout,
                             QPushButton, QMessageBox, QFileDialog, QVBoxLayout,
                             QFormLayout, QInputDialog, QMainWindow)
from PyQt6.QtCore import Qt
import numpy as np
from relative_dose_1d.tools import identify_format, get_data, gamma_1D, build_from_array_and_step
import sys
import os
import copy

class GUI(QWidget):

    def __init__(self, D_ref = None, D_eval = None):
        """Constructor for a graphical user interface (GUI). Data has to be in 2 columns, 
        corresponding to positions and dose values, respectively.

        Parameters
        ----------

        D_ref : ndarray,
            Reference dose profile represented by a (M, 2) numpy array.  

        D_eva : ndarray,
            Dose profile to be evaluated, represented by a (N, 2) numpy array.

        Returns
        -------

        A PyQt widget to showing dose profiles, gamma analysis and dose difference.

        """
        super().__init__()

        self.D_ref = D_ref
        self.D_eval = D_eval

        self.initializeUI()

    def initializeUI(self):
        """Set up the apllication"""
        "x, y, width, height"
        self.setGeometry(200,100,1000,400)
        self.setWindowTitle("Relative dose 1D")

        self.set_up_window()
        self.set_up_data()
        self.show()

    def set_up_window(self):

        "Layouts definition"
        self.main_box_layout = QHBoxLayout()
   
        self.v_box_layout = QVBoxLayout()
        self.settings_layout_v = QVBoxLayout()
        
        self.Q_grafica = Q_Base_Figure() 

        self.main_box_layout.addLayout(self.settings_layout_v)
        self.main_box_layout.addLayout(self.v_box_layout)

        self.setLayout(self.main_box_layout)

        self.open_file_button = QPushButton("Load a text file", self)
        self.open_file_button.clicked.connect(self.open_file_button_clicked)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_data_and_plots)
        
        self.button_factor = QPushButton("Scale factor", self)
        self.button_factor.clicked.connect(self.factor_button_clicked)
        self.button_factor.setFixedSize(80, 40)
        self.button_factor.setEnabled(False)

        self.button_origin = QPushButton("Move origin", self)
        self.button_origin.clicked.connect(self.move_button_clicked)
        self.button_origin.setFixedSize(80, 40)
        self.button_origin.setEnabled(False)

        axis_label = QLabel("Axis position")
        #axis_label.setFont(QFont(Arial, 15))
        self.settings_layout_v.addWidget(axis_label, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.settings_layout_v.addWidget(self.button_factor)
        self.settings_layout_v.addWidget(self.button_origin)
        self.settings_layout_v.addWidget(QLabel("Gamma", alignment = Qt.AlignmentFlag.AlignHCenter))

        gammaLayout = QFormLayout()
        self.dose_t_QLine = QLineEdit()
        self.dose_t_QLine.setFixedWidth(40)
        self.dose_t_QLine.setText("3.0")
        self.DTA_t_QLine = QLineEdit()
        self.DTA_t_QLine.setFixedWidth(40)
        self.DTA_t_QLine.setText("2.0")
        self.thres_QLine = QLineEdit()
        self.thres_QLine.setFixedWidth(40)
        self.thres_QLine.setText("0.0")
        self.interp_QLine = QLineEdit()
        self.interp_QLine.setFixedWidth(40)
        self.interp_QLine.setText("1")
        gammaLayout.addRow("Dose [%]:", self.dose_t_QLine)
        gammaLayout.addRow("DTA [mm]:", self.DTA_t_QLine)
        gammaLayout.addRow("Threshold [%]:", self.thres_QLine)
        gammaLayout.addRow("Interp.:", self.interp_QLine)

        self.gamma_button = QPushButton("Apply")
        self.gamma_button.clicked.connect(self.calc_difference_and_gamma)
        self.gamma_button.setFixedSize(120, 40)
        #self.button_origin.setEnabled(False)

        results_label = QLabel("Results", alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gamma_rate_label = QLabel("Pass rate: ")
        self.total_points_label = QLabel("Total points: ")
        self.evaluated_points_label = QLabel("Evaluated ponits: ")

        self.settings_layout_v.addLayout(gammaLayout)
        self.settings_layout_v.addWidget(self.gamma_button)
        self.settings_layout_v.addWidget(results_label)
        self.settings_layout_v.addWidget(self.gamma_rate_label)
        self.settings_layout_v.addWidget(self.total_points_label)
        self.settings_layout_v.addWidget(self.evaluated_points_label)

        self.settings_layout_v.addStretch()
         
        self.v_box_layout.addWidget(self.open_file_button)
        self.v_box_layout.addWidget(self.clear_button)
        self.v_box_layout.addWidget(self.Q_grafica.Qt_fig)
        
    def set_up_data(self):
        if self.D_ref is None:
            self.loaded_data = []
        else:          
            self.loaded_data = [self.D_ref, self.D_eval]
            self.Q_grafica.plot_data(self.D_ref)
            self.Q_grafica.plot_data(self.D_eval)
            self.calc_difference_and_gamma()

    # Button's functions

    def open_file_button_clicked(self):
        self.last_file_name, _ = QFileDialog.getOpenFileName()
        _ , extension = os.path.splitext(self.last_file_name)

        if self.last_file_name:
            with open(self.last_file_name, encoding='UTF-8', mode = 'r') as file:
                all_list = [line.strip() for line in file]

            format = identify_format(all_list)

            if format == 'text_file':
                self.show_new_window()  #New window for input user parameters.

            else:
                data = get_data(self.last_file_name)
                self.load_data(data)

    def clear_data_and_plots(self):
        self.Q_grafica.ax_perfil.clear()
        self.Q_grafica.ax_perfil_resta.clear()
        self.Q_grafica.ax_gamma.clear()
        self.Q_grafica.fig.canvas.draw()
        self.open_file_button.setEnabled(True)
        self.loaded_data = []

    def clear_gamma(self):
        self.Q_grafica.ax_perfil_resta.clear()
        self.Q_grafica.ax_gamma.clear()

    def factor_button_clicked(self):
        scale_factor, ok = QInputDialog.getText(self, 'Scale factor', 'Scale factor:')
        try:
            scale_factor = float(scale_factor)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] * scale_factor
                cache_data = copy.deepcopy(self.loaded_data)
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')

    def move_button_clicked(self):
        delta, ok = QInputDialog.getText(self, 'Scale factor', 'Origin displacement:')
        try:
            delta = float(delta)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] + delta
                cache_data = copy.deepcopy(self.loaded_data)
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')        

    def show_new_window(self):
        start_word, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Start word:')
        if ok:
            data = get_data(self.last_file_name, start_word)
        else:
            data = get_data(self.last_file_name)
                
        self.load_data(data)
    
    #   Additional functions

    def load_data(self, data):
        
        self.loaded_data.append(data)       
        self.Q_grafica.plot_data(data)
        self.button_factor.setEnabled(True)
        self.button_origin.setEnabled(True)
        if len(self.loaded_data) == 2:
            self.calc_difference_and_gamma()

    def calc_difference_and_gamma(self):

        data_A = self.loaded_data[0]
        data_B = self.loaded_data[1]

        # Using interpolation, new values ​​of B are computed at positions given by A.
        data_B_from_A_positions = np.interp(data_A[:,0], data_B[:,0], data_B[:,1], left = np.nan)
    
        difference = data_A[:,1] - data_B_from_A_positions

        added_positions = np.array((data_A[:,0], difference))
        values = np.transpose(added_positions)
       
        g, g_percent, evaluated_points = gamma_1D(
            data_A, 
            data_B,
            dose_t = float(self.dose_t_QLine.text()),
            dist_t = float(self.DTA_t_QLine.text()),
            dose_threshold = float(self.thres_QLine.text()),
            interpol = int(self.interp_QLine.text()),
            )

        self.Q_grafica.plot_resta(values)
        self.Q_grafica.ax_gamma.clear()
        #self.Q_grafica.ax_gamma = self.Q_grafica.ax_perfil_resta.twinx()
        self.Q_grafica.plot_gamma(g)
        #self.Q_grafica.ax_gamma.set_ylabel('gamma')
        self.gamma_rate_label.setText(f"Pass rate: {g_percent:0.1f}%")
        self.total_points_label.setText(f"Total points: {data_A.shape[0]:0.1f}")
        self.evaluated_points_label.setText(f"Evaluated ponits: {evaluated_points:0.1f}")

class Q_Base_Figure:
        
    def __init__(self):
        self.fig = Figure(figsize=(40,4), tight_layout = True, facecolor = 'whitesmoke')
        self.Qt_fig = FigureCanvas(self.fig)

        #   Axes para la imagen
        self.ax_perfil = self.fig.add_subplot(1, 2, 1)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance [mm]')
        self.ax_perfil.grid(alpha = 0.3)

        self.ax_perfil_resta =  self.fig.add_subplot(1, 2, 2)
        self.ax_perfil_resta.set_ylabel('Percentage [%]')
        self.ax_perfil_resta.set_xlabel('Distance [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)

        self.ax_gamma = self.ax_perfil_resta.twinx()
        self.ax_gamma.set_ylabel('gamma')
        #self.ax_gamma.set_ylim((0, 2))
        
    def plot_data(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil.plot(x, y)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance [mm]')
        self.ax_perfil.grid(alpha = 0.3)
        #self.ax_perfil.legend()
        self.fig.canvas.draw()
        
    def plot_resta(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil_resta.plot(x, y, color='r', label = 'Difference', alpha = 0.7)
        self.ax_perfil_resta.set_ylabel('Difference')
        self.ax_perfil_resta.set_xlabel('Distance [mm]')
        self.ax_perfil_resta.grid(alpha = 0.4)
        self.ax_perfil_resta.legend(loc = 'upper left')

        self.fig.canvas.draw()

    def plot_gamma(self, data):
        x = data[:,0]
        y = data[:,1]

        self.ax_gamma.plot(x, y, color='g', label = 'gamma', marker = '.')
        self.ax_gamma.plot(x, np.ones(x.shape[0]), 'g--', alpha = 0.5, linewidth=2)
        self.ax_gamma.set_ylabel('gamma')
        self.ax_gamma.yaxis.set_label_position("right")
        self.ax_gamma.legend(loc = 'upper right')

        self.fig.canvas.draw()

def plot(D_ref, D_eval):
    """
    A function to show a graphical user interface (GUI) to showing 1D dose profiles, 
    gamma analysis and dose difference. Data has to be in 2 columns, 
    corresponding to positions and dose values, respectively.

    Parameters
    ----------

    D_ref : ndarray,
        Reference dose profile represented by a (M, 2) numpy array.  

    D_eva : ndarray,
        Dose profile to be evaluated, represented by a (N, 2) numpy array.

    Returns
    -------

    A GUI showing dose profiles, gamma analysis and dose difference.

    Examples
    --------

    >>> import relative_dose_1d.GUI_tool as rd

    >>> a = np.array([0,1,2,3,4,5,6,7,8,9,10])
    >>> b = a + np.random.random_sample((11,))

    >>> A = build_from_array_and_step(a, 1)
    >>> B = build_from_array_and_step(b, 1)
    
    >>> rd.plot(A,B)

    """

    app = QApplication(sys.argv)    
    window = GUI(D_ref, D_eval)
    sys.exit(app.exec())

def run_demo():

    a = np.array([0,1,2,3,4,5,6,7,8,9,10])
    b = a + np.random.random_sample((11,))

    A = build_from_array_and_step(a, 1)
    B = build_from_array_and_step(b, 1)
    
    plot(A,B)

if __name__ == '__main__':
    
    a = np.array([0,1,2,3,4,5,6,7,8,9,10])
    b = a + np.random.random_sample((11,))
    A = build_from_array_and_step(a, 1)
    B = build_from_array_and_step(b, 1)
    
    app = QApplication(sys.argv)
    window = GUI(A, B)
    sys.exit(app.exec())