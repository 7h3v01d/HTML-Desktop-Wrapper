import sys
import os
import argparse
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QMenu
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

class FramelessWindow(QWidget):
    def __init__(self, content):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setStyleSheet("background-color: #2c3e50; border-radius: 10px;")
        self.setMinimumSize(800, 650)  # Allow resizing

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create control bar layout
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(5)

        # Add window control buttons
        self.minimize_btn = QPushButton("🗕", self)
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setStyleSheet("background-color: #34495e; color: white; border: none;")
        self.minimize_btn.clicked.connect(self.showMinimized)
        control_layout.addWidget(self.minimize_btn)

        self.max_restore_btn = QPushButton("🗖", self)
        self.max_restore_btn.setFixedSize(30, 30)
        self.max_restore_btn.setStyleSheet("background-color: #34495e; color: white; border: none;")
        self.max_restore_btn.clicked.connect(self.toggle_max_restore)
        control_layout.addWidget(self.max_restore_btn)

        self.close_btn = QPushButton("🗙", self)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("background-color: #e74c3c; color: white; border: none;")
        self.close_btn.clicked.connect(self.close)
        control_layout.addWidget(self.close_btn)

        control_layout.addStretch()  # Push buttons to the left
        main_layout.addLayout(control_layout)

        # Create the web view widget
        self.web_view = QWebEngineView(self)
        main_layout.addWidget(self.web_view)

        # Enable custom context menu for developer tools
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.web_view.customContextMenuRequested.connect(self.show_context_menu)

        # Load the content (file or URL)
        base_path = os.path.dirname(os.path.abspath(__file__))
        if content.startswith(('http://', 'https://')):
            # Load as a URL
            self.web_view.setUrl(QUrl(content))
        else:
            # Load as a local file
            html_file_path = os.path.join(base_path, content)
            if not os.path.exists(html_file_path):
                QMessageBox.critical(self, "Error", f"HTML file '{content}' not found in {base_path}")
                self.close()
                return
            self.web_view.setUrl(QUrl.fromLocalFile(html_file_path))

        # Enable dragging
        self.old_pos = None
        # Initialize resize debounce timer
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.refresh_web_view)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        inspect_action = menu.addAction("Inspect")
        inspect_action.triggered.connect(self.open_dev_tools)
        menu.exec(self.web_view.mapToGlobal(pos))

    def open_dev_tools(self):
        # Trigger Chromium DevTools
        self.web_view.page().triggerAction(QWebEnginePage.WebAction.InspectElement)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() < 40:  # Only drag from top
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        # Toggle maximize/restore on F11
        if event.key() == Qt.Key.Key_F11:
            self.toggle_max_restore()
        
        # Toggle fullscreen on Ctrl+F
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_F:
            if self.isFullScreen():
                self.showNormal()
                self.max_restore_btn.setText("🗖")
            else:
                self.showFullScreen()
                self.max_restore_btn.setText("🗗")
        
        # Close the window on Esc
        elif event.key() == Qt.Key.Key_Escape:
            self.close()

    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.max_restore_btn.setText("🗖")
        else:
            self.showMaximized()
            self.max_restore_btn.setText("🗗")
        # Force web view repaint after state change
        QTimer.singleShot(100, self.refresh_web_view)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Throttle resize events to prevent flickering
        self.web_view.resize(self.size())  # Use window size directly
        if not self.isFullScreen():  # Skip during fullscreen to avoid flicker
            self.resize_timer.start(150)  # 150ms for stability

    def refresh_web_view(self):
        # Lightweight repaint to prevent blank screen
        self.web_view.setZoomFactor(self.web_view.zoomFactor())  # Trigger redraw
        self.web_view.update()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Frameless HTML Window Application")
    parser.add_argument("--html", default="index.html", help="Path to a local HTML file or a web URL (e.g., https://example.com)")
    parser.add_argument("--gpu", choices=["enable", "disable"], default="enable", help="Control GPU acceleration (enable/disable)")
    args, unknown_args = parser.parse_known_args()

    # Pass --disable-gpu to QApplication if specified
    app_args = sys.argv[:]
    if args.gpu == "disable":
        app_args.append("--disable-gpu")
    app = QApplication(app_args)
    window = FramelessWindow(args.html)
    window.show()
    sys.exit(app.exec())
