from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                           QLabel, QLineEdit, QRadioButton, QVBoxLayout, 
                           QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
import sys
import os
from modify_data_report import data_report
from modify_wechat_template_info import WeChat_template

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据处理工具")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 加载背景图片
        try:
            bg_path = os.path.join(self.script_dir, "resource", "default_bg.jpg")
            pixmap = QPixmap(bg_path)
            
            # 设置窗口大小为图片大小的一半
            self.window_width = pixmap.width() // 2
            self.window_height = pixmap.height() // 2
            self.resize(self.window_width, self.window_height)
            
            # 缩放背景图片
            pixmap = pixmap.scaled(self.window_width, self.window_height, 
                                 Qt.AspectRatioMode.KeepAspectRatio)
            
            # 设置背景
            palette = self.palette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            self.setPalette(palette)
            
        except Exception as e:
            print(f"加载背景图片失败: {e}")
            self.window_width = 400
            self.window_height = 300
            self.resize(self.window_width, self.window_height)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: rgba(240, 240, 240, 200);
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px 15px;
                font-family: 微软雅黑;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(220, 220, 220, 200);
            }
        """
        
        # 创建按钮
        btn1 = QPushButton("数据报告生成")
        btn2 = QPushButton("微信模板生成")
        btn3 = QPushButton("选择背景图片")
        
        # 设置按钮样式
        for btn in [btn1, btn2, btn3]:
            btn.setStyleSheet(button_style)
            layout.addWidget(btn)
            layout.addSpacing(10)  # 添加间距
        
        # 连接按钮信号
        btn1.clicked.connect(self.open_data_report)
        btn2.clicked.connect(self.open_wechat_template)
        btn3.clicked.connect(self.change_background)
        
        # 居中显示窗口
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.window_width) // 2
        y = (screen.height() - self.window_height) // 2
        self.move(x, y)
    
    def open_data_report(self):
        """打开数据报告生成对话框"""
        self.dialog = DataReportDialog(self)
        # 设置为独立窗口
        self.dialog.setWindowFlags(Qt.WindowType.Window)
        self.dialog.show()
    
    def open_wechat_template(self):
        """打开微信模板生成对话框"""
        self.dialog = WeChatTemplateDialog(self)
        # 设置为独立窗口
        self.dialog.setWindowFlags(Qt.WindowType.Window)
        self.dialog.show()
    
    def change_background(self):
        """更改背景图片"""
        # TODO: 实现背景图片更改功能
        pass

class DataReportDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("数据报告生成")
        
        # 设置窗口大小为主窗口的90%
        self.window_width = int(parent.window_width * 0.9)
        self.window_height = int(parent.window_height * 0.9)
        self.resize(self.window_width, self.window_height)
        
        # 加载并设置背景
        try:
            bg_path = os.path.join(parent.script_dir, "resource", "default_bg.jpg")
            pixmap = QPixmap(bg_path)
            pixmap = pixmap.scaled(self.window_width, self.window_height, 
                                 Qt.AspectRatioMode.KeepAspectRatio)
            
            # 创建背景标签
            bg_label = QLabel(self)
            bg_label.setPixmap(pixmap)
            # 设置白色半透明遮罩
            bg_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 128);  /* 50%透明的白色 */
                }
            """)
            bg_label.resize(self.window_width, self.window_height)
        except Exception as e:
            print(f"加载背景图片失败: {e}")
        
        # 移除窗口整体透明度设置
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setWindowOpacity(0.5)
        
        # 创建主布局
        layout = QGridLayout(self)
        layout.setSpacing(10)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                font-family: 微软雅黑;
                font-size: 12px;
                color: black;
                background: transparent;
            }
            QLineEdit {
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background: rgba(255, 255, 255, 50%);
            }
            QRadioButton {
                font-family: 微软雅黑;
                font-size: 12px;
                color: black;
                background: transparent;
            }
            QPushButton {
                background-color: rgba(240, 240, 240, 50%);
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px 15px;
                font-family: 微软雅黑;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(220, 220, 220, 50%);
            }
        """)
        
        # 添加基本信息输入框
        fields = [
            ("项目地址：", 0),
            ("联系人：", 1),
            ("采样日期（MM-DD）：", 2),
            ("现场采样温度（℃）：", 3),
            ("现场采样湿度（%RH）：", 4)
        ]
        
        self.entries = {}
        for (label_text, row) in fields:
            label = QLabel(label_text)
            entry = QLineEdit()
            layout.addWidget(label, row, 0)
            layout.addWidget(entry, row, 1)
            self.entries[label_text] = entry
        
        # 添加检测类型选择
        type_label = QLabel("检测类型：")
        layout.addWidget(type_label, 5, 0)
        
        type_layout = QHBoxLayout()
        self.type_var = "1"
        self.radio1 = QRadioButton("初检")
        self.radio2 = QRadioButton("复检")
        self.radio1.setChecked(True)
        self.radio1.toggled.connect(lambda: self.set_type("1"))
        self.radio2.toggled.connect(lambda: self.set_type("2"))
        type_layout.addWidget(self.radio1)
        type_layout.addWidget(self.radio2)
        layout.addLayout(type_layout, 5, 1)
        
        # 添加点位输入
        point_label = QLabel("点位和值输入：")
        layout.addWidget(point_label, 6, 0, 1, 2)
        
        self.point_entries = []
        self.value_entries = []
        quick_texts = ["客厅", "主卧", "次卧", "儿童房"]
        
        for i in range(4):
            row = 7 + i
            point_layout = QHBoxLayout()
            
            # 点位输入
            point_label = QLabel(f"点位{i+1}：")
            point_entry = QLineEdit()
            point_layout.addWidget(point_label)
            point_layout.addWidget(point_entry)
            self.point_entries.append(point_entry)
            
            # 快捷按钮
            quick_btn = QPushButton(quick_texts[i])
            quick_btn.clicked.connect(lambda checked, e=point_entry, t=quick_texts[i]: 
                                   self.insert_quick_text(e, t))
            point_layout.addWidget(quick_btn)
            
            # 值输入
            value_label = QLabel(f"值{i+1}：")
            value_entry = QLineEdit()
            point_layout.addWidget(value_label)
            point_layout.addWidget(value_entry)
            self.value_entries.append(value_entry)
            
            layout.addLayout(point_layout, row, 0, 1, 2)
        
        # 添加生成报告按钮
        submit_btn = QPushButton("生成报告")
        submit_btn.clicked.connect(self.submit)
        layout.addWidget(submit_btn, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        
        # 居中显示窗口
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.window_width) // 2
        y = (screen.height() - self.window_height) // 2
        self.move(x, y)
    
    def set_type(self, value):
        """设置检测类型"""
        self.type_var = value
    
    def insert_quick_text(self, entry, text):
        """在指定输入框中插入文本"""
        entry.setText(text)
    
    def submit(self):
        """提交数据并生成报告"""
        try:
            # 收集所有输入值
            input_values = [
                self.entries["项目地址："].text(),
                self.entries["联系人："].text(),
                self.entries["采样日期（MM-DD）："].text(),
                self.entries["现场采样温度（℃）："].text(),
                self.entries["现场采样湿度（%RH）："].text(),
                self.type_var
            ]
            
            # 添加点位和值
            for point_entry, value_entry in zip(self.point_entries, self.value_entries):
                input_values.append(point_entry.text())
                input_values.append(value_entry.text())
            
            # 模拟用户输入
            input_generator = iter(input_values)
            def mock_input(*args):
                try:
                    return next(input_generator)
                except StopIteration:
                    return ""
            
            import builtins
            original_input = builtins.input
            try:
                builtins.input = mock_input
                # 修改工作目录到脚本所在目录
                original_cwd = os.getcwd()
                script_dir = os.path.dirname(os.path.abspath(__file__))
                os.chdir(script_dir)
                
                # 直接导入并运行模块
                import modify_data_report
                modify_data_report.data_report()
                
                os.chdir(original_cwd)
            finally:
                builtins.input = original_input
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "成功", "报告生成成功！")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "错误", f"生成报告时出错: {str(e)}")

class WeChatTemplateDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("微信模板生成")
        self.resize(400, 300)
        
        # 加载并设置背景
        try:
            bg_path = os.path.join(parent.script_dir, "resource", "default_bg.jpg")
            pixmap = QPixmap(bg_path)
            pixmap = pixmap.scaled(self.width(), self.height(), 
                                 Qt.AspectRatioMode.KeepAspectRatio)
            
            # 创建背景标签
            bg_label = QLabel(self)
            bg_label.setPixmap(pixmap)
            # 设置白色半透明遮罩
            bg_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 128);  /* 50%透明的白色 */
                }
            """)
            bg_label.resize(self.width(), self.height())
        except Exception as e:
            print(f"加载背景图片失败: {e}")
        
        # 移除窗口整体透明度设置
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setWindowOpacity(0.5)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 添加说明标签
        layout.addWidget(QLabel("请输入治理信息："))
        layout.addWidget(QLabel("格式：日期 时间 面积 地址"))
        layout.addWidget(QLabel("或：日期-时间-面积 地址"))
        
        # 添加输入框
        self.info_entry = QLineEdit()
        layout.addWidget(self.info_entry)
        
        # 添加生成按钮
        submit_btn = QPushButton("生成模板")
        submit_btn.clicked.connect(self.submit)
        layout.addWidget(submit_btn)
        
        # 居中显示窗口
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def submit(self):
        """提交数据并生成模板"""
        input_text = self.info_entry.text()
        
        import builtins
        original_input = builtins.input
        
        def mock_input(*args):
            return input_text
        
        try:
            builtins.input = mock_input
            # 直接导入并运行模块
            import modify_wechat_template_info
            modify_wechat_template_info.WeChat_template()
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "成功", "模板生成成功！")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "错误", f"生成模板时出错: {str(e)}")
        finally:
            builtins.input = original_input

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 