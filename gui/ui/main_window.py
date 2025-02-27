from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,QFileDialog, 
                            QFrame)
from .widgets import *
from .styles import WINDOW_STYLE
import sys
import os
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import QTimer


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.mode=None
        self.compressed_data = None

    def init_ui(self):
        self.setWindowTitle("Advanced File Compression Tool")
        self.setStyleSheet(WINDOW_STYLE)
        
        # Main horizontal layout
        self.main_layout = QHBoxLayout()
        self.setup_initial_view()
        self.setLayout(self.main_layout)
        self.setFixedSize(800, 600)

    def setup_initial_view(self):
        self.center_layout = QVBoxLayout()
        
        # Banner
        banner = create_banner()
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Create buttons
        self.compress_button = create_main_button("Compress", "#27ae60")
        self.decompress_button = create_main_button("Decompress", "#e74c3c")
        
        # Connect buttons
        self.compress_button.clicked.connect(
            lambda: self.switch_to_sidebar_layout("compress"))
        self.decompress_button.clicked.connect(
            lambda: self.switch_to_sidebar_layout("decompress"))
        
        # Add buttons to layout
        buttons_layout.addWidget(self.compress_button)
        buttons_layout.addWidget(self.decompress_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add everything to center layout
        self.center_layout.addWidget(banner)
        self.center_layout.addLayout(buttons_layout)
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.center_layout)
        self.main_layout.addWidget(self.central_widget)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sidebar_layout = QVBoxLayout()
        
        # Back button
        back_button = create_back_button()
        back_button.clicked.connect(self.return_to_initial_view)
        
        # Mode buttons
        compress_button = create_sidebar_button("Compress", "#27ae60")
        decompress_button = create_sidebar_button("Decompress", "#e74c3c")
        
        compress_button.clicked.connect(
            lambda: self.update_main_content("compress"))
        decompress_button.clicked.connect(
            lambda: self.update_main_content("decompress"))
        
        sidebar_layout.addWidget(back_button)
        sidebar_layout.addWidget(compress_button)
        sidebar_layout.addWidget(decompress_button)
        sidebar_layout.addStretch()
        
        sidebar.setLayout(sidebar_layout)
        return sidebar

    def create_main_content(self, mode):
        content = QWidget()
        layout = QVBoxLayout()
        
        title = create_title_label(f"{mode.title()} Mode" if mode else "Select Mode")
        description = create_description_label(self.get_mode_description(mode))
        select_file_button = create_selectfile_button("Select file", "#27ae60")
        select_file_button.clicked.connect(
            lambda: self.select_file_button_clicked(mode))
        
        self.file_label = create_file_label()
        # Save button
        self.save_button = create_selectfile_button("Save", "#f39c12")
        self.save_button.setVisible(False)
        self.save_button.clicked.connect(
            lambda: self.save_file_button_clicked(mode))
        #Visualize tree button
        self.visualize_tree_button = create_selectfile_button("Visualize tree", "#27ae60")
        self.visualize_tree_button.setVisible(False)
        self.visualize_tree_button.clicked.connect(self.visualize_tree_button_clicked)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(select_file_button)
        layout.addWidget(self.file_label)  # Show selected file
        layout.addWidget(self.save_button)  # Save button
        layout.addWidget(self.visualize_tree_button) # visualize tree button
        layout.addStretch()
        
        content.setLayout(layout)
        return content

    def get_mode_description(self, mode):
        if mode == "compress":
            return "Select files or folders to compress them into a single compressed file."
        elif mode == "decompress":
            return "Select a compressed file to extract its contents."
        return "Please select a mode from the sidebar."

    def switch_to_sidebar_layout(self, initial_mode):
        self.mode=initial_mode
        self.clear_layout(self.main_layout)
        self.main_layout.addWidget(self.create_sidebar())
        self.main_layout.addWidget(self.create_main_content(initial_mode))

    def update_main_content(self, mode):
        if self.main_layout.count() > 1:
            old_content = self.main_layout.takeAt(1)
            if old_content.widget():
                old_content.widget().deleteLater()
        self.main_layout.addWidget(self.create_main_content(mode))

    def return_to_initial_view(self):
        self.clear_layout(self.main_layout)
        self.setup_initial_view()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def select_file_button_clicked(self, mode):
        if mode == "compress":
            file_filter = "Text Files (*.txt)"
        elif mode == "decompress":
            file_filter = "Binary Files (*.bin)"
        else:
            file_filter = "All Files (*)"  # Fallback case    
        
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            f"Select a file for {mode}",
            "",
            file_filter  # Apply dynamic filter
        )

        if not file_name:
            return
        
        self.selected_file = file_name  # Store selected file path

        # Get file size in bytes
        file_size_bytes = os.path.getsize(file_name)
        
        # Convert file size to a human-readable format (KB, MB)
        if file_size_bytes < 1024:
            file_size = f"{file_size_bytes} bytes"
        elif file_size_bytes < 1048576:
            file_size = f"{file_size_bytes / 1024:.2f} KB"
        else:
            file_size = f"{file_size_bytes / 1048576:.2f} MB"


        # Handle long filenames with ellipsis
        font_metrics = QFontMetrics(self.file_label.font())
        elided_text = font_metrics.elidedText(file_name, Qt.TextElideMode.ElideMiddle, 300)

        # Update label with file name and size
        self.file_label.setText(f"Selected: {elided_text} ({file_size})")  # Update UI

        if mode in ["compress", "decompress"]:
            self.mode=mode
            command = [sys.executable, 'src/main.py', mode, file_name]
            subprocess.run(command)
            # After compression, open the Save As dialog
            self.save_button.setVisible(True)
            if self.mode == "compress":
                self.visualize_tree_button.setVisible(True)
                
    def save_file_button_clicked(self):
        if self.mode == "compress":
            file_filter = "Binary Files (*.bin)"
        elif self.mode == "decompress":
            file_filter = "Text Files (*.txt)"
        else:
            return  # Exit if the mode is not recognized

        save_file, _ = QFileDialog.getSaveFileName(self, "Save File As", "", file_filter)

        if save_file:
            self.save_path = save_file  # Store user-selected save path
    
    def visualize_tree_button_clicked(self, checked = "false"):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/core/tree_viz.py'))
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path], check=True)
        else:
            return