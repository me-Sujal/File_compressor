import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Window title
        self.setWindowTitle("PyQt6 Window with Banner and Side-by-Side Buttons")
        
        # Create a vertical layout
        main_layout = QVBoxLayout()
        
        # Create a banner (label)
        banner = QLabel("Welcome to My App", self)
        banner.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px; text-align: center;")
        main_layout.addWidget(banner)
        
        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Create two buttons
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)
        
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        
        # Add the button layout to the main vertical layout
        main_layout.addLayout(button_layout)
        
        # Set the layout to the window
        self.setLayout(main_layout)
        
        # Set window size
        self.resize(300, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec())
