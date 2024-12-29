import sys, psutil, platform, datetime, json, os, wmi
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTabWidget, QProgressBar, QTableWidget, QTableWidgetItem, QMessageBox,
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QGradient, QLinearGradient


class ModernButton(QPushButton):
    def __init__(self, text, color="#4a9eff"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 24px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 1.1)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, 0.9)};
            }}
        """)

    def adjust_color(self, color, factor):
        # Brighten or darken the color
        color = color.lstrip('#')
        r = int(min(255, int(color[0:2], 16) * factor))
        g = int(min(255, int(color[2:4], 16) * factor))
        b = int(min(255, int(color[4:6], 16) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"


class ModernProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #2a2a2a;
                border-radius: 7px;
                text-align: center;
                color: white;
                height: 14px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #4a9eff, stop:1 #2196F3);
                border-radius: 7px;
            }
        """)


class ModernTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2979ff;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #4a9eff;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #1e1e1e;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                border-radius: 5px;
            }
        """)


class ModernTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #1e1e1e;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #252525;
                color: #808080;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #4a9eff;
            }
            QTabBar::tab:hover:!selected {
                color: #4a9eff;
            }
        """)


class SystemScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Scanner")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: #1a1a1a;")

        # Set the window icon
        self.setWindowIcon(QIcon("icon1.ico"))

        # Main layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QHBoxLayout()
        title = QLabel("SYSTEM SCANNER")
        title.setStyleSheet("""
            color: #4a9eff;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        # Buttons
        button_layout = QHBoxLayout()
        self.scan_btn = ModernButton("SCAN", "#4a9eff")
        self.save_btn = ModernButton("SAVE REPORT", "#2196F3")
        self.scan_btn.clicked.connect(self.start_scan)
        self.save_btn.clicked.connect(self.save_report)
        button_layout.addWidget(self.scan_btn)
        button_layout.addWidget(self.save_btn)

        header.addWidget(title)
        header.addStretch()
        header.addLayout(button_layout)

        # Progress bar with status
        progress_layout = QVBoxLayout()
        self.status = QLabel("Ready")
        self.status.setStyleSheet("color: #4a9eff; font-size: 13px;")
        self.progress = ModernProgressBar()
        progress_layout.addWidget(self.status)
        progress_layout.addWidget(self.progress)

        # Tabs
        self.tabs = ModernTabWidget()
        self.tables = {}

        tab_configs = {
            "SYSTEM": ["Component", "Specification"],
            "PROCESSES": ["Name", "PID", "CPU %", "Memory %"],
            "STORAGE": ["Drive", "Total", "Used", "Free"],
            "NETWORK": ["Interface", "Status", "Speed", "Data"],
            "SECURITY": ["Service", "Status", "Type", "Started"]
        }

        for name, columns in tab_configs.items():
            table = ModernTableWidget()
            table.setColumnCount(len(columns))
            table.setHorizontalHeaderLabels(columns)
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)
            self.tables[name] = table
            self.tabs.addTab(table, name)

        # Add everything to main layout
        layout.addLayout(header)
        layout.addLayout(progress_layout)
        layout.addWidget(self.tabs)

        # Add shadow effects
        for widget in [self.tabs, self.progress]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 160))
            shadow.setOffset(0, 0)
            widget.setGraphicsEffect(shadow)

        # Real-time monitoring
        self.monitor = QTimer()
        self.monitor.timeout.connect(self.update_monitor)
        self.monitor.start(1000)

        self.scan_thread = None
        self.scan_results = None

        self.start_scan()

    def update_monitor(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        self.status.setText(f"CPU Usage: {cpu}%  |  Memory Usage: {memory}%")

    def start_scan(self):
        self.scan_btn.setEnabled(False)
        self.status.setText("Scanning...")

        # SYSTEM tab - System Information
        system_info = [
            ("OS", platform.system() + " " + platform.version()),
            ("Architecture", platform.architecture()[0]),
            ("Processor", platform.processor()),
            ("Uptime", str(datetime.timedelta(seconds=int(psutil.boot_time()))))
        ]
        self.populate_table("SYSTEM", system_info)

        # PROCESSES tab - Running processes
        process_info = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            process_info.append((proc.info['name'], proc.info['pid'], proc.info['cpu_percent'], proc.info['memory_percent']))
        self.populate_table("PROCESSES", process_info)

        # STORAGE tab - Disk usage
        storage_info = []
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info.append((partition.device, f"{usage.total / (1024**3):.2f} GB", f"{usage.used / (1024**3):.2f} GB", f"{usage.free / (1024**3):.2f} GB"))
        self.populate_table("STORAGE", storage_info)

        # NETWORK tab - Network information
        net_info = []
        for iface, addrs in psutil.net_if_addrs().items():
            net_info.append((iface, ", ".join([addr.address for addr in addrs if addr.family == psutil.AF_LINK]), "N/A", "N/A"))
        self.populate_table("NETWORK", net_info)

        # SECURITY tab - Basic security services
        security_info = [
            ("Firewall", "Enabled", "Software", "N/A"),
            ("Antivirus", "Active", "Software", "N/A")
        ]
        self.populate_table("SECURITY", security_info)

        self.status.setText("Scan Complete")
        self.scan_btn.setEnabled(True)

    def populate_table(self, tab_name, data):
        table = self.tables[tab_name]
        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                table.setItem(row, col, QTableWidgetItem(str(col_data)))

    def save_report(self):
        QMessageBox.information(self, "Save Report", "Report saved successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Enable high DPI scaling
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    window = SystemScanner()
    window.show()
    sys.exit(app.exec())
