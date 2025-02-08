# Base styles
WINDOW_STYLE = """
    QWidget {
        background-color: #f5f6fa;
        
    }
"""
#font-family: 'Segoe UI', Arial;

BANNER_STYLE = """
    QLabel {
        color: #2c3e50;
        padding: 5px;
        letter-spacing: -0.5px;
        line-height: 1;
        white-space: pre;
    }"""

# Button styles
def create_main_button_style(color):
    return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            padding: 15px 32px;
            border-radius: 8px;
            font-size: 18px;
            min-width: 200px;
            margin: 10px;
        }}
        QPushButton:hover {{
            background-color: {color}dd;
        }}
        QPushButton:pressed {{
            background-color: {color}aa;
        }}
    """

BACK_BUTTON_STYLE = """
    QPushButton {
        background-color: #34495e;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 14px;
        margin: 10px;
        max-width: 100px;
    }
    QPushButton:hover {
        background-color: #2c3e50;
    }
"""

def create_sidebar_button_style(color):
    return f"""
        QPushButton {{
            background-color: transparent;
            color: white;
            border: 2px solid {color};
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
            text-align: left;
            margin: 5px 10px;
        }}
        QPushButton:hover {{
            background-color: {color}55;
        }}
    """

SIDEBAR_STYLE = """
    QFrame {
        background-color: #2c3e50;
        border-radius: 0px;
        max-width: 250px;
        min-width: 250px;
    }
"""

TITLE_STYLE = """
    font-size: 28px;
    color: #2c3e50;
    padding: 20px;
    font-weight: bold;
"""

DESCRIPTION_STYLE = """
    font-size: 16px;
    color: #34495e;
    padding: 20px;
"""
