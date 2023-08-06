"""
QVSED - Qt-Based Volatile Small Editor
A cross-platform simple and volatile text editor by Arsalan Kazmi
See README.md or "Get Help" inside QVSED for more info
"""

# pylint: disable=no-name-in-module
# pylint: disable=attribute-defined-outside-init
# pylint: disable=broad-exception-caught

import os
import sys
import shutil
import importlib.util
import pkg_resources
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QFileDialog, QPlainTextEdit, QLineEdit,
    QAction, QShortcut
)
from PyQt5.QtGui import (
    QKeySequence, QFont, QDragEnterEvent, QDropEvent
)
from PyQt5.QtCore import QTextCodec
from PyQt5.uic import loadUi


class QVSEDApp:
    """
    The main application class for QVSED.
    """

    def __init__(self):
        """
        Initialize the QVSED application.
        """
        self.app = QApplication([])
        self.window = QVSEDWindow()

    def run(self):
        """
        Run the QVSED application.
        """
        self.window.show()
        self.app.exec()


class QVSEDWindow(QMainWindow):
    """
    The main window class for QVSED.
    """

    def __init__(self):
        """
        Initialize the QVSED window.
        """
        super().__init__()
        self.load_ui_file()
        self.focus_text_area()
        self.set_text_area_encoding("UTF-8")
        self.set_up_text_area_handlers()
        self.set_up_action_deck()
        self.echo_area_update(f"Welcome to QVSED v{self.get_qvsed_version()}!")
        self.load_config()
        self.set_up_fonts()
        if self.check_if_file_parameter():
            self.load_from_file(sys.argv[1])

    def apply_style_sheet(self, text_color, background_color, button_color, button_focus_color):
        """
        Generate and apply a style sheet based on the config.py file.
        """

        stylesheet = f"""
QMainWindow {{
    color: {text_color};
    background: {background_color};
}}

QPlainTextEdit, QLineEdit {{
    color: {text_color};
    background: {button_focus_color};
    padding: 8px;
    border: none;
}}

QPushButton {{
    color: {text_color};
    border: 2px solid {button_focus_color};
    background: {button_color};
    padding: 2px;
}}

QPushButton:hover {{
    color: {text_color};
    background: {button_focus_color};
}}

QPushButton:pressed {{
    color: {text_color};
    background: {background_color};
}}

QScrollBar:vertical {{
    background-color: {button_focus_color};
    width: 16px;
    margin: 16px 0 16px 0;
}}

QScrollBar::handle:vertical {{
    background-color: {button_color};
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {button_color};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
        """

        # Apply the stylesheet to the app
        self.setStyleSheet(stylesheet)

    def check_if_file_parameter(self):
        """
        Check if a file path was specified at the parameter.
        """
        if len(sys.argv) < 2:
            return False

        file_path = sys.argv[1]
        return os.path.isfile(file_path)

    def clear_text_area(self):
        """
        Clear the Text Area.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is already blank.")
            return

        text_area.clear()

        self.echo_area_update("Text Area has been cleared.")

    def connect_command_buttons(self):
        """
        Connect the Action Deck command buttons to their respective functions.
        """
        self.findChild(QPushButton, "clearButton").clicked.connect(self.clear_text_area)
        self.findChild(QPushButton, "saveButton").clicked.connect(self.save_text_contents)
        self.findChild(QPushButton, "openButton").clicked.connect(self.load_from_file)
        self.findChild(QPushButton, "helpButton").clicked.connect(self.show_help)
        self.findChild(QPushButton, "quitButton").clicked.connect(self.quit_app)
        self.findChild(QPushButton, "fullscreenButton").clicked.connect(self.toggle_fullscreen)

    def connect_key_bindings(self):
        """
        Connect the Action Deck keybindings to their respective functions.
        """
        self.clear_shortcut.activated.connect(self.clear_text_area)
        self.save_shortcut.activated.connect(self.save_text_contents)
        self.open_shortcut.activated.connect(self.load_from_file)
        self.help_shortcut.activated.connect(self.show_help)
        self.quit_shortcut.activated.connect(self.quit_app)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

    def drag_enter_event(self, event: QDragEnterEvent):
        """
        Handle the drag enter event for the Text Area.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        """
        Handle the drop event for the Text Area.
        """
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.load_from_file(file_path)
        text_area = self.findChild(QPlainTextEdit, "textArea")
        text_area.repaint()

    def echo_area_update(self, message):
        """
        Update the Echo Area with the given message.

        Args:
            message (str): The message to display in the Echo Area.
        """
        echo_area = self.findChild(QLineEdit, "echoArea")
        echo_area.setText(message)
        echo_area.setCursorPosition(0)

    def focus_text_area(self):
        """
        Set the Text Area to have focus.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")
        text_area.setFocus()

    def generate_config(self):
        """
        Generate the config file for QVSED.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_default = os.path.join(current_dir, "config_default.py")

        if os.name == "nt":  # Windows
            user_config_dir = os.path.join(os.environ["APPDATA"], "QVSED")
        else:  # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"

        if not os.path.exists(user_config_dir):
            os.makedirs(user_config_dir)
        user_config_file = os.path.join(user_config_dir, "config.py")

        shutil.copyfile(config_default, user_config_file)

        # Update the first line of config.py
        with open(user_config_file, "r+", encoding="utf-8") as config_file:
            lines = config_file.readlines()
            if lines:
                lines[0] = "# This is QVSED's config file, you can change its options here.\n"
                config_file.seek(0)
                config_file.writelines(lines)
                config_file.truncate()

        self.echo_area_update(f"Config generated at {user_config_file}.")

    def get_qvsed_version(self):
        """
        Return the QVSED version specified in setup.py.
        """
        try:
            return pkg_resources.get_distribution('qvsed').version
        except pkg_resources.DistributionNotFound:
            return "?.?.?"

    def load_config(self):
        """
        Load the configuration for QVSED.
        """
        if os.name == "nt":  # Windows
            user_config_dir = os.path.join(os.environ["APPDATA"], "QVSED")
        else:  # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"

        user_config_file = os.path.join(user_config_dir, "config.py")

        if not os.path.isfile(user_config_file):
            self.generate_config()

        spec = importlib.util.spec_from_file_location("qvsed_config", user_config_file)
        qvsed_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qvsed_config)

        self.font_family = qvsed_config.font_family
        self.font_size = qvsed_config.font_size

        # Load the colour scheme settings from the config file
        # We use the shorter American spellings because it's standard, I guess
        try:
            text_color = qvsed_config.text_color
            background_color = qvsed_config.background_color
            button_color = qvsed_config.button_color
            button_focus_color = qvsed_config.button_focus_color
            self.apply_style_sheet(text_color, background_color, button_color, button_focus_color)
        except AttributeError as error:
            self.echo_area_update(f"Check config.py: {str(error)}")

    def load_from_file(self, file_path = None):
        """
        Open a file dialog, and load the contents of a file into the Text Area.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")

        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File")

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text_area.setPlainText(file.read())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"Opened file {file_name}.")
            except Exception as error:
                self.echo_area_update(f"Error opening file: {str(error)}")

    def load_ui_file(self):
        """
        Load the UI file for the QVSED window.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, "qvsed.ui")
        loadUi(ui_file, self)

    def quit_app(self):
        """
        Quit QVSED.
        """
        QApplication.quit()

    def save_text_contents(self):
        """
        Open a file dialog, and save the contents of the Text Area to a file.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is blank, will not save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File")

        if file_path:
            try:
                with open(file_path, "w", encoding="UTF-8") as file:
                    file.write(text_area.toPlainText())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"Saved file {file_name}.")
            except Exception as error:
                self.echo_area_update(f"Error saving file: {str(error)}")

    def set_text_area_encoding(self, encoding):
        """
        Set the Text Area encoding.

        Args:
            encoding (str): The encoding to set for the Text Area.
        """
        QTextCodec.setCodecForLocale(QTextCodec.codecForName(encoding))

    def set_up_action_deck(self):
        """
        Set up the Action Deck for the QVSED window.

        This module does nothing by itself, but it's used to run the
        below three modules, which are all components of the Action Deck.
        """
        self.set_up_actions()
        self.set_up_shortcuts()
        self.set_up_action_deck_handlers()

    def set_up_actions(self):
        """
        Set up the Action Deck commands for the QVSED window.
        """
        self.clear_action = QAction("Clear Text", self)
        self.save_action = QAction("Save File", self)
        self.open_action = QAction("Open File", self)
        self.help_action = QAction("Get Help", self)
        self.quit_action = QAction("Quit QVSED", self)

    def set_up_action_deck_handlers(self):
        """
        Set up the event handlers for the Action Deck.
        """
        self.connect_command_buttons()
        self.connect_key_bindings()

    def set_up_text_area_handlers(self):
        """
        Set up the event handlers for the Text Area.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")

        text_area.dragEnterEvent = self.drag_enter_event
        text_area.dragMoveEvent = self.drag_enter_event
        text_area.dropEvent = self.drop_event

    def set_up_fonts(self):
        """
        Set up the fonts for the QVSED window.
        """
        font = QFont()
        font.setFamilies(self.font_family)
        font.setPointSize(self.font_size)
        QApplication.instance().setFont(font)
        self.update_widget_fonts(self)

    def set_up_shortcuts(self):
        """
        Set up the key bindings for the Action Deck commands.
        """
        self.clear_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.help_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        self.quit_shortcut = QShortcut(QKeySequence("Alt+Q"), self)
        self.fullscreen_shortcut = QShortcut(QKeySequence("Alt+F"), self)

    def show_help(self):
        """
        Display the help message in the Text Area.
        """
        text_area = self.findChild(QPlainTextEdit, "textArea")

        help_message = """QVSED - Qt-based Volatile Small Editor
========================================
QVSED is a stateless, volatile text editor with a minimalist approach, focusing solely on text editing without file metadata or prompts for potentially destructive actions.

This is the Text Area, where the actual editing takes place. Type anything you want into here, and edit as you please.
Down there, at the bottom of the window, is the Echo Area, where messages and errors will be displayed.
On the left of the QVSED window is the Action Deck, containing commands to clear the Text Area, open or save a file, display this help text, toggle in and out of full screen mode or quit QVSED.

I hope you enjoy using QVSED! I enjoyed writing it, and it's a nice little venture into my first Qt project.

- Arsalan Kazmi <sonicspeed848@gmail.com>, That1M8Head on GitHub"""

        self.echo_area_update("Help message shown in Text Area.")

        text_area.setPlainText(help_message)

    def toggle_fullscreen(self):
        """
        Toggle the QVSED window between fullscreen and normal mode.
        """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def update_widget_fonts(self, widget):
        """
        Iteratively update the fonts of the given widget and its children.

        Used to update QVSED's font face.

        Args:
            widget (QWidget): The widget to update the fonts for.
        """
        if widget is None:
            return

        widget.setFont(QApplication.instance().font())

        for child_widget in widget.findChildren(QWidget):
            self.update_widget_fonts(child_widget)


def main():
    """
    The entry point for the QVSED application.
    """
    app = QVSEDApp()
    app.run()


if __name__ == "__main__":
    main()
