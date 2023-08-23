# -------- INFOS -------- #
VERSION = "1.0.0"
CREATOR = "Bugpig"

# -------- LIBRARIES -------- #
import sys
import os
import yaml
import win32gui
import win32con
import win32api
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer

# -------- VARIABLES -------- #
#YAML
# Obtention du chemin absolu du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construction du chemin absolu du fichier YAML
yaml_file = os.path.join(script_dir, "config.yaml")

# Lecture du fichier de configuration YAML
with open(yaml_file, "r") as config_file:
    config_data = yaml.safe_load(config_file)


# QT DESIGNER
# Obtention du chemin absolu du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construction du chemin absolu du fichier UI
ui_file = os.path.join(script_dir, "mcmdmanager_ui.ui")

app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi(ui_file)


# initialisation de la configuration via le fichier YAML
# Global Parameters

window.setWindowTitle(config_data.get("app_name"))

tab_widget = window.findChild(QtWidgets.QTabWidget, "main_tab")
tab_widget.setTabText(0, config_data.get("tab0_name"))
tab_widget.setTabText(1, config_data.get("tab1_name"))

# Internal Parameters

# label_version
label_main_title = window.findChild(QtWidgets.QLabel, "label_version") #pointe sur id label
label_main_title.setText("version " + f"{VERSION}") # pointe sur la variable app_version

# label_creator
label_main_title = window.findChild(QtWidgets.QLabel, "label_creator") #pointe sur id label
label_main_title.setText("made by : " + f"{CREATOR}") # pointe sur la variable app_version

# label_main_title
label_main_title = window.findChild(QtWidgets.QLabel, "label_main_title") #pointe sur id label
label_main_title.setText(config_data.get("pa_main_title")) # pointe sur parametre du fichier YAML

# label_description
label_description = window.findChild(QtWidgets.QLabel, "label_description") #pointe sur id label
label_description.setText(config_data.get("pa_description")) # pointe sur parametre du fichier YAML

# label_title_zbreath_tab
label_title_zbreath_tab = window.findChild(QtWidgets.QLabel, "label_title_zbreath_tab") #pointe sur id label
label_title_zbreath_tab.setText(config_data.get("pa_title_zbreath_tab")) # pointe sur parametre du fichier YAML

# label states servers
label_state_server0 = window.findChild(QtWidgets.QLabel, "label_state_server0") #pointe sur id label
label_state_server1 = window.findChild(QtWidgets.QLabel, "label_state_server1") #pointe sur id label
label_state_server2 = window.findChild(QtWidgets.QLabel, "label_state_server2") #pointe sur id label
label_state_server3 = window.findChild(QtWidgets.QLabel, "label_state_server3") #pointe sur id label
label_state_server4 = window.findChild(QtWidgets.QLabel, "label_state_server4") #pointe sur id label
label_state_server5 = window.findChild(QtWidgets.QLabel, "label_state_server5") #pointe sur id label
label_state_server6 = window.findChild(QtWidgets.QLabel, "label_state_server6") #pointe sur id label

# Affichage de la fenêtre
window.show()

# -------- FUNCTIONS -------- #

def is_cmd_running(server_name):
    hwnd = win32gui.FindWindow(None, server_name)
    if hwnd == 0:
        hwnd = win32gui.FindWindow(None, "Sélection server_" + server_name)
        if hwnd == 0:
            return False
        else:
            return True
    else:
        return True
    
def f_launch_server(server_name, server_index):
    if is_cmd_running("server_"+server_name):
        print("The CMD console is running.")
    else:
        if config_data.get(f"path_server{server_index}"):
            if os.path.exists(config_data.get(f"path_server{server_index}")):
                os.chdir(config_data.get(f"path_server{server_index}"))
                os.startfile(config_data.get("server_bat_name"))
                print("The CMD console is not running. The server will start...")    
            else:
                print(f"The path does not found for server : {server_name}")
        else:
            print(f"The path does not exist for server : {server_name}")

def f_stop_bungee_server(server_name, server_index):
    # Trouver la fenêtre de commande avec le titre spécifié
    hwnd = win32gui.FindWindow(None, "server_" + server_name)
    if hwnd == 0:
        hwnd = win32gui.FindWindow(None, "Sélection server_" + server_name)
    if hwnd:
        # Envoyer le message WM_CLOSE pour fermer la fenêtre
        win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print("The bungee server has just been stopped.")
    else:
        print("The bungee server is not running.")

#Lance un serveur avec la commande stop via son nom
def f_stop_server(server_name, server_index):
    if is_cmd_running("server_"+server_name):
        hwnd = win32gui.FindWindow("ConsoleWindowClass", "server_" +server_name)
        if hwnd == 0:
            hwnd = win32gui.FindWindow(None, "Sélection server_" + server_name)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(0x53, 0, 0, 0) # "s"
        win32api.keybd_event(0x54, 0, 0, 0) # "t"
        win32api.keybd_event(0x4F, 0, 0, 0) # "o"
        win32api.keybd_event(0x50, 0, 0, 0) # "p"
        win32api.keybd_event(0x0D, 0, 0, 0) # enfoncer la touche Enter
        win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0) # relache la touche Enter
        print(f"The server {server_name} has just been stopped.")
    else:
        print(f"The server {server_name} is not running.")

def refresh_server_states():
    for i in range(13):
        if config_data.get(f"server_name{i}"):
            temp_label_state_reference = window.findChild(QtWidgets.QLabel, f"label_state_server{i}")
            if is_cmd_running("server_" + config_data.get(f"server_name{i}")):
                temp_label_state_reference.setText("ON")
                temp_label_state_reference.setStyleSheet("color: green;")
            else:
                temp_label_state_reference.setText("OFF")
                temp_label_state_reference.setStyleSheet("color: red;")

    QTimer.singleShot(1000, refresh_server_states)

def sort_server_list(): #Name and set visibility of list for server tab
    for i in range(13):
        temp_button_launch = window.findChild(QtWidgets.QPushButton, f"bp_launch_server{i}")
        temp_button_stop = window.findChild(QtWidgets.QPushButton, f"bp_stop_server{i}")
        temp_label_state = window.findChild(QtWidgets.QLabel, f"label_state_server{i}")
        if not config_data.get(f"server_name{i}"):
            temp_button_launch.hide()
            temp_button_stop.hide()
            temp_label_state.hide()
        else:
            temp_button_launch.setText("Launch " + config_data.get(f"server_name{i}"))
            temp_button_stop.setText("Stop " + config_data.get(f"server_name{i}"))

#Link Button
# server0
if config_data.get("server_name0"):
    bp_launch_server0 = window.findChild(QtWidgets.QPushButton, "bp_launch_server0")
    bp_launch_server0.clicked.connect(lambda: f_launch_server(config_data.get("server_name0"),0))
    bp_stop_server0 = window.findChild(QtWidgets.QPushButton, "bp_stop_server0")
    bp_stop_server0.clicked.connect(lambda: f_stop_bungee_server(config_data.get("server_name0"),0))

# server1
if config_data.get("server_name1"):
    bp_launch_server1 = window.findChild(QtWidgets.QPushButton, "bp_launch_server1")
    bp_launch_server1.clicked.connect(lambda: f_launch_server(config_data.get("server_name1"),1))
    bp_stop_server1 = window.findChild(QtWidgets.QPushButton, "bp_stop_server1")
    bp_stop_server1.clicked.connect(lambda: f_stop_server(config_data.get("server_name1"),1))

# server2
if config_data.get("server_name2"):
    bp_launch_server2 = window.findChild(QtWidgets.QPushButton, "bp_launch_server2")
    bp_launch_server2.clicked.connect(lambda: f_launch_server(config_data.get("server_name2"),2))
    bp_stop_server2 = window.findChild(QtWidgets.QPushButton, "bp_stop_server2")
    bp_stop_server2.clicked.connect(lambda: f_stop_server(config_data.get("server_name2"),2))

# server3
if config_data.get("server_name3"):
    bp_launch_server3 = window.findChild(QtWidgets.QPushButton, "bp_launch_server3")
    bp_launch_server3.clicked.connect(lambda: f_launch_server(config_data.get("server_name3"),3))
    bp_stop_server3 = window.findChild(QtWidgets.QPushButton, "bp_stop_server3")
    bp_stop_server3.clicked.connect(lambda: f_stop_server(config_data.get("server_name3"),3))

# server4
if config_data.get("server_name4"):
    bp_launch_server4 = window.findChild(QtWidgets.QPushButton, "bp_launch_server4")
    bp_launch_server4.clicked.connect(lambda: f_launch_server(config_data.get("server_name4"),4))
    bp_stop_server4 = window.findChild(QtWidgets.QPushButton, "bp_stop_server4")
    bp_stop_server4.clicked.connect(lambda: f_stop_server(config_data.get("server_name4"),4))

# server5
if config_data.get("server_name5"):
    bp_launch_server5 = window.findChild(QtWidgets.QPushButton, "bp_launch_server5")
    bp_launch_server5.clicked.connect(lambda: f_launch_server(config_data.get("server_name5"),5))
    bp_stop_server5 = window.findChild(QtWidgets.QPushButton, "bp_stop_server5")
    bp_stop_server5.clicked.connect(lambda: f_stop_server(config_data.get("server_name5"),5))

# server6
if config_data.get("server_name6"):
    bp_launch_server6 = window.findChild(QtWidgets.QPushButton, "bp_launch_server6")
    bp_launch_server6.clicked.connect(lambda: f_launch_server(config_data.get("server_name6"),6))
    bp_stop_server6 = window.findChild(QtWidgets.QPushButton, "bp_stop_server6")
    bp_stop_server6.clicked.connect(lambda: f_stop_server(config_data.get("server_name6"),6))

# server7
if config_data.get("server_name7"):
    bp_launch_server7 = window.findChild(QtWidgets.QPushButton, "bp_launch_server7")
    bp_launch_server7.clicked.connect(lambda: f_launch_server(config_data.get("server_name7"),7))
    bp_stop_server7 = window.findChild(QtWidgets.QPushButton, "bp_stop_server7")
    bp_stop_server7.clicked.connect(lambda: f_stop_server(config_data.get("server_name7"),7))

# server8
if config_data.get("server_name8"):
    bp_launch_server8 = window.findChild(QtWidgets.QPushButton, "bp_launch_server8")
    bp_launch_server8.clicked.connect(lambda: f_launch_server(config_data.get("server_name8"),8))
    bp_stop_server8 = window.findChild(QtWidgets.QPushButton, "bp_stop_server8")
    bp_stop_server8.clicked.connect(lambda: f_stop_server(config_data.get("server_name8"),8))

# server9
if config_data.get("server_name9"):
    bp_launch_server9 = window.findChild(QtWidgets.QPushButton, "bp_launch_server9")
    bp_launch_server9.clicked.connect(lambda: f_launch_server(config_data.get("server_name9"),9))
    bp_stop_server9 = window.findChild(QtWidgets.QPushButton, "bp_stop_server9")
    bp_stop_server9.clicked.connect(lambda: f_stop_server(config_data.get("server_name9"),9))

# server10
if config_data.get("server_name10"):
    bp_launch_server10 = window.findChild(QtWidgets.QPushButton, "bp_launch_server10")
    bp_launch_server10.clicked.connect(lambda: f_launch_server(config_data.get("server_name10"),10))
    bp_stop_server10 = window.findChild(QtWidgets.QPushButton, "bp_stop_server10")
    bp_stop_server10.clicked.connect(lambda: f_stop_server(config_data.get("server_name10"),10))

# server11
if config_data.get("server_name11"):
    bp_launch_server11 = window.findChild(QtWidgets.QPushButton, "bp_launch_server11")
    bp_launch_server11.clicked.connect(lambda: f_launch_server(config_data.get("server_name11"),11))
    bp_stop_server11 = window.findChild(QtWidgets.QPushButton, "bp_stop_server11")
    bp_stop_server11.clicked.connect(lambda: f_stop_server(config_data.get("server_name11"),11))

# server12
if config_data.get("server_name12"):
    bp_launch_server12 = window.findChild(QtWidgets.QPushButton, "bp_launch_server12")
    bp_launch_server12.clicked.connect(lambda: f_launch_server(config_data.get("server_name12"),12))
    bp_stop_server12 = window.findChild(QtWidgets.QPushButton, "bp_stop_server12")
    bp_stop_server12.clicked.connect(lambda: f_stop_server(config_data.get("server_name12"),12))

sort_server_list()
refresh_server_states()

# Exécution de la boucle d'événements de l'application
sys.exit(app.exec_())

