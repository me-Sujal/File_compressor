from PyQt6.QtWidgets import QPushButton, QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont 
from .styles import *

def create_banner():

    BANNER_ASCII = """
       ██╗  ██╗██╗   ██╗███████╗███████╗███╗   ███╗ █████╗ ███╗   ██╗    ██████╗  █████╗ ███████╗███████╗██████╗ 
        ██║  ██║██║   ██║██╔════╝██╔════╝████╗ ████║██╔══██╗████╗  ██║    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
        ███████║██║   ██║█████╗  █████╗  ██╔████╔██║███████║██╔██╗ ██║    ██████╔╝███████║███████╗█████╗  ██║  ██║
        ██╔══██║██║   ██║██╔══╝  ██╔══╝  ██║╚██╔╝██║██╔══██║██║╚██╗██║    ██╔══██╗██╔══██║╚════██║██╔══╝  ██║  ██║
        ██║  ██║╚██████╔╝██║     ██║     ██║ ╚═╝ ██║██║  ██║██║ ╚████║    ██████╔╝██║  ██║███████║███████╗██████╔╝
       ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝ 

        ██████╗ ██████╗ ███╗   ███╗██████╗ ██████╗ ███████╗███████╗███████╗ ██████╗ ██████╗                      
        ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗                     
        ██║     ██║   ██║██╔████╔██║██████╔╝██████╔╝█████╗  ███████╗███████╗██║   ██║██████╔╝                     
        ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██╗██╔══╝  ╚════██║╚════██║██║   ██║██╔══██╗                     
        ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║███████╗███████║███████║╚██████╔╝██║  ██║                     
         ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝                     
    """

    label = QLabel(BANNER_ASCII)
    label.setFont(QFont('Monospace', 8))  # Using Monospace font with smaller size
    label.setStyleSheet(BANNER_STYLE)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)    
    return label
# end of create_banner

def create_main_button(text, color):
    button = QPushButton(text)
    button.setStyleSheet(create_main_button_style(color))
    return button
# end of create_main_button

def create_back_button():
    button = QPushButton("← Back")
    button.setStyleSheet(BACK_BUTTON_STYLE)
    return button
# end of create_back_button

def create_sidebar_button(text, color):
    button = QPushButton(text)
    button.setStyleSheet(create_sidebar_button_style(color))
    return button
# end of create_sidebar_button

def create_selectfile_button(text, color):
    button = QPushButton(text)
    button.setStyleSheet(create_selectfile_button_style(color))
    return button
# end of create_selectfile_button

def create_title_label(text):
    label = QLabel(text)
    label.setStyleSheet(TITLE_STYLE)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label
# end of create_title_label

def create_description_label(text):
    label = QLabel(text)
    label.setStyleSheet(DESCRIPTION_STYLE)
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label
# end of create_descrition_label

def create_file_name_label(text):
    label = QLabel(text)
    label.setStyleSheet(DESCRIPTION_STYLE)
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label
# end of create_file_name_label

def create_file_label():
    label = QLabel("No file selected")
    label.setStyleSheet("color: #34495e; font-size: 14px; padding: 5px;")
    label.setMinimumWidth(400)  # Adjust as needed
    label.setWordWrap(False)  # Prevent wrapping
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # Allow text selection
    return label
# end of create_file_label

def create_action_button(text, color):
    button = QPushButton(text)
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 14px;
            max-width: 150px;
        }}
        QPushButton:hover {{
            background-color: {color}dd;
        }}
        QPushButton:pressed {{
            background-color: {color}aa;
        }}
    """)
    return button
# end of create_action_button