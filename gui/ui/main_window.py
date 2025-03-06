from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, 
                            QFrame, QLabel)
from .widgets import *
from .styles import WINDOW_STYLE
import sys
import os
import subprocess
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import QTimer, Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.mode = None
        self.compressed_data = None
        self.selected_file = None

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
        
        # Select file button
        self.select_file_button = create_selectfile_button("Select file", "#27ae60")
        self.select_file_button.clicked.connect(
            lambda: self.select_file_button_clicked(mode))
        
        # Create file info section
        self.file_info_widget = QWidget()
        self.file_info_layout = QHBoxLayout(self.file_info_widget)
        
        # Original file column
        self.original_file_column = QWidget()
        original_layout = QVBoxLayout(self.original_file_column)
        
        original_title = QLabel("Original File")
        original_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        original_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.original_icon = QLabel("📄")  # Using emoji as icon
        self.original_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_icon.setStyleSheet("font-size: 36px; margin: 10px;")
        
        self.original_file_name = QLabel("No file selected")
        self.original_file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_file_name.setStyleSheet("color: #34495e; font-size: 14px;")
        self.original_file_name.setWordWrap(True)
        
        self.original_file_size = QLabel("")
        self.original_file_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_file_size.setStyleSheet("color: #0c0d0d; font-size: 12px;")
        
        original_layout.addWidget(original_title)
        original_layout.addWidget(self.original_icon)
        original_layout.addWidget(self.original_file_name)
        original_layout.addWidget(self.original_file_size)
        original_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Compressed file column
        self.compressed_file_column = QWidget()
        compressed_layout = QVBoxLayout(self.compressed_file_column)
        
        compressed_title = QLabel("Compressed File" if mode == "compress" else "Decompressed File")
        compressed_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        compressed_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.compressed_icon = QLabel("🗜️" if mode == "compress" else "📄")
        self.compressed_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.compressed_icon.setStyleSheet("font-size: 36px; margin: 10px;")
        
        self.compressed_file_name = QLabel("Not processed yet")
        self.compressed_file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.compressed_file_name.setStyleSheet("color: #34495e; font-size: 14px;")
        self.compressed_file_name.setWordWrap(True)
        
        self.compressed_file_size = QLabel("")
        self.compressed_file_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.compressed_file_size.setStyleSheet("color: #0c0d0d; font-size: 12px;")
        
        compressed_layout.addWidget(compressed_title)
        compressed_layout.addWidget(self.compressed_icon)
        compressed_layout.addWidget(self.compressed_file_name)
        compressed_layout.addWidget(self.compressed_file_size)
        compressed_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add both columns to file info layout
        self.file_info_layout.addWidget(self.original_file_column)
        self.file_info_layout.addWidget(self.compressed_file_column)
        
        # Set initial visibility of file info
        self.file_info_widget.setVisible(False)
        
        # Bottom buttons container (right-aligned)
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Create smaller action buttons
        self.save_button = create_action_button("Save", "#f39c12")
        self.save_button.setVisible(False)
        self.save_button.clicked.connect(self.save_file_button_clicked)
        
        self.visualize_tree_button = create_action_button("Visualize tree", "#27ae60")
        self.visualize_tree_button.setVisible(False)
        self.visualize_tree_button.clicked.connect(self.visualize_tree_button_clicked)
        
        bottom_layout.addWidget(self.visualize_tree_button)
        bottom_layout.addWidget(self.save_button)
        
        # Add all elements to main layout
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.file_info_widget)
        layout.addStretch()
        layout.addWidget(bottom_buttons)
        
        content.setLayout(layout)
        return content

    def get_mode_description(self, mode):
        if mode == "compress":
            return "Select files or folders to compress them into a single compressed file."
        elif mode == "decompress":
            return "Select a compressed file to extract its contents."
        return "Please select a mode from the sidebar."

    def switch_to_sidebar_layout(self, initial_mode):
        self.mode = initial_mode
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
            file_filter
        )

        if not file_name:
            return
        
        self.selected_file = file_name  # Store selected file path

        # Get file size in bytes
        file_size_bytes = os.path.getsize(file_name)
        
        # Convert file size to a human-readable format
        file_size = self.format_file_size(file_size_bytes)
        
        # Update original file info
        file_basename = os.path.basename(file_name)
        self.original_file_name.setText(file_basename)
        self.original_file_size.setText(file_size)
        
        # Change button text to "Compress another" or "Decompress another"
        self.select_file_button.setText(f"{mode.title()} another")
        
        # Make file info visible
        self.file_info_widget.setVisible(True)

        if mode in ["compress", "decompress"]:
            self.mode = mode
            command = [sys.executable, 'src/main.py', mode, file_name]
            subprocess.run(command)     
            
            # After compression/decompression, update compressed file info
            if mode == "compress":
                # Update compressed file information (assuming output is filename.bin)
                compressed_filename = os.path.splitext(file_basename)[0] + ".bin"
                self.compressed_file_name.setText(compressed_filename)
                
                # Estimate compressed file size (this is a placeholder - replace with actual calculation)
                # In a real implementation, you would get the actual size of the compressed file
                compressed_size_bytes = file_size_bytes // 2  # Just an example compression ratio
                self.compressed_file_size.setText(self.format_file_size(compressed_size_bytes))
                
                self.visualize_tree_button.setVisible(True)
            elif mode == "decompress":
                # Update decompressed file information
                decompressed_filename = os.path.splitext(file_basename)[0] + ".txt"
                self.compressed_file_name.setText(decompressed_filename)
                
                # Placeholder for decompressed size
                decompressed_size_bytes = file_size_bytes * 2  # Example ratio
                self.compressed_file_size.setText(self.format_file_size(decompressed_size_bytes))
            
            # Show save button
            self.save_button.setVisible(True)

    def format_file_size(self, size_bytes):
        """Convert file size to human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1048576:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / 1048576:.2f} MB"
        
    def save_file_button_clicked(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        if project_root not in sys.path:
            sys.path.append(project_root)
        
        print(sys.path)

        try:
            from src.main import Save
            save = Save()
            save.save_file()
        except Exception as e:
            print(f"error!{e}")
    
    def visualize_tree_button_clicked(self):
        if self.mode == "compress" and self.selected_file:            
            # Get the project root directory
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            
            # Add to path if not already there
            if project_root not in sys.path:
                sys.path.append(project_root)
            
            print(project_root)
                
            try:
                # Now import the necessary modules with proper paths
                from src.core.huffman_codec import HuffmanCodec
                from src.utils.file_handler import FileHandler
                
                # Initialize codec
                codec = HuffmanCodec()
                
                # Read and encode the data to generate the tree
                data = FileHandler.read_text(self.selected_file)
                codec.encode(data)
                
                # Visualize the tree
                codec.visualize_tree()
            except ImportError as e:
                print(f"Import error: {str(e)}")
                print(f"Current path: {sys.path}")
            except Exception as e:
                print(f"Error visualizing tree: {str(e)}")