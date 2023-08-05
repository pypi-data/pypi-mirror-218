# QVSED - Qt-based Volatile Small Editor

QVSED is a volatile text editor, meaning that there are no restrictions against unsaved work or bad files.

QVSED is a PyQt5 rewrite of my older project, [ASMED (Another SMol EDitor)](https://github.com/That1M8Head/ASMED), which was written using Windows Forms, and was quite obviously only for Windows.

QVSED seeks to replace ASMED by being cross-platform, and it will bring over the benefits of such a lightweight editor without the overhead of .NET.

QVSED is licensed under the GNU General Public License version 3 or later.

## The window

QVSED is broken up into three parts - the Action Deck, the Text Area and the Echo Area.

![QVSED screenshot, editing its own source code](qsved_screenie.png)

The Action Deck includes the commands Clear Text, Open File, Save File, Get Help and Quit QVSED. These can be activated by clicking on them or entering their keyboard shortcut.

The Text Area is where the actual text editing takes place. This is straightforward so I won't say anything more.

The Echo Area is a small bar at the bottom of the QSMED window that prints information, for example, when a file is opened, it prints its path.

## Action Deck commands

**Clear Text** - Clicking this command or entering the shortcut <C-n> will clear the Text Area. Think of it like New File.

**Open File** - Clicking this command or entering the shortcut <C-f> will launch a file picker and load the chosen file's contents into the Text Area.

**Save File** - Clicking this command or entering the shortcut <C-s> will launch a save dialog and save the contents of the Text Area to the chosen file name.

**Get Help** - Clicking this command or entering the shortcut <C-h> will populate the Text Area with this README.

**Quit QVSED** - Clicking this command or entering the shortcut <A-q> will quit QVSED on the spot with no confirmation dialog.
