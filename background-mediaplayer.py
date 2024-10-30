import sys
import vlc
import json
import keyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: green;")
        self.setFixedSize(640, 480)

        self.media_player = None
        self.key_bindings = self.load_bindings()
        
        self.registered_hotkeys = []

        self.video_frame = QtWidgets.QFrame(self)
        self.video_frame.setStyleSheet("background-color: transparent;")
        self.video_widget = QtWidgets.QVBoxLayout(self)
        self.video_widget.addWidget(self.video_frame)
        self.setLayout(self.video_widget)

        self.show()

        self.start_keyboard_listener()

    def load_bindings(self):
        try:
            with open('media_files.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_bindings(self):
        with open('media_files.json', 'w') as file:
            json.dump(self.key_bindings, file)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Tab:
            self.open_settings()

    def start_keyboard_listener(self):
        for hotkey in self.registered_hotkeys:
            keyboard.remove_hotkey(hotkey)
        self.registered_hotkeys.clear()

        for key_combination, file_path in self.key_bindings.items():
            hotkey = keyboard.add_hotkey(key_combination, self.play_media_from_hotkey, args=[key_combination])
            self.registered_hotkeys.append(hotkey)

    def play_media_from_hotkey(self, key_combination):
        file_path = self.key_bindings.get(key_combination)
        if file_path:
            self.play_media(file_path)

    def play_media(self, file_path):
        if self.media_player:
            self.media_player.stop()
            self.media_player.release()
            self.media_player = None

        # Отображаем видео окно перед началом воспроизведения
        self.video_frame.show()

        # Запускаем воспроизведение в основном потоке
        QtCore.QMetaObject.invokeMethod(self, "start_playback", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, file_path))

    @QtCore.pyqtSlot(str)
    def start_playback(self, file_path):
        self.media_player = vlc.MediaPlayer(file_path)
        self.media_player.set_hwnd(int(self.video_frame.winId()))
        self.media_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_video_end)
        self.media_player.play()
        QtCore.QTimer.singleShot(100, self.set_video_size)

    def set_video_size(self):
        if self.media_player:
            video_width = self.media_player.video_get_width()
            video_height = self.media_player.video_get_height()

            new_height = 480 - 40
            new_width = int(video_width * (new_height / video_height))
            self.video_frame.setFixedSize(new_width, new_height)
            self.video_frame.setContentsMargins(0, 20, 0, 20)
            horizontal_margin = (640 - new_width) // 2
            self.video_widget.setContentsMargins(horizontal_margin, 0, horizontal_margin, 0)

    def on_video_end(self, event):
        self.video_frame.hide()

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 250)  # Увеличиваем высоту для новой кнопки

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.key_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.key_input)

        self.file_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.file_input)

        # Добавляем кнопку для выбора файла
        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)  # Привязываем кнопку к функции
        self.layout.addWidget(self.browse_button)

        self.save_button = QtWidgets.QPushButton("Save Binding", self)
        self.save_button.clicked.connect(self.save_binding)
        self.layout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton("Delete Binding", self)
        self.delete_button.clicked.connect(self.delete_binding)  # Привязываем кнопку к функции удаления
        self.layout.addWidget(self.delete_button)

        self.key_input.setPlaceholderText("Enter key combination (e.g., 'shift+t')")
        self.file_input.setPlaceholderText("Enter media file path")

        self.existing_bindings = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.existing_bindings)
        self.update_existing_bindings()

    def browse_file(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Media File")
        if file_path:  # Если файл был выбран, устанавливаем его путь в file_input
            self.file_input.setText(file_path)

    def save_binding(self):
        key_text = self.key_input.text()
        file_path = self.file_input.text()
        
        if key_text and file_path:
            self.main_window.key_bindings[key_text] = file_path
            self.main_window.save_bindings()
            self.main_window.start_keyboard_listener()
            self.update_existing_bindings()
            #self.close()

    def delete_binding(self):
        selected_item = self.existing_bindings.currentItem()  # Получаем текущий выбранный элемент
        if selected_item:
            key_text = selected_item.text().split(":")[0]  # Извлекаем ключ из текста
            del self.main_window.key_bindings[key_text]  # Удаляем биндинг
            self.main_window.save_bindings()  # Сохраняем изменения
            self.update_existing_bindings()  # Обновляем список

    def update_existing_bindings(self):
        self.existing_bindings.clear()
        for key, file_path in self.main_window.key_bindings.items():
            self.existing_bindings.addItem(f"{key}: {file_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    app.exec_()
