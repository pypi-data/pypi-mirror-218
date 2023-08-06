# QVSED - Qt-based Volatile Small Editor

QVSED is a volatile text editor, meaning that there are no restrictions against unsaved work or bad files.

QVSED is a PyQt5 rewrite of my older project, [ASMED (Another SMol EDitor)](https://github.com/That1M8Head/ASMED), which was written using Windows Forms, and was quite obviously only for Windows.

QVSED aims to replace ASMED by offering cross-platform support and the advantages of a lightweight editor without the overhead of .NET.

## Installing

QVSED [is available on PyPI](https://pypi.org/project/QVSED/). You can install it using the following command:

```bash
pip install --upgrade qvsed
```

To run QVSED, use the `qvsed` command. If you find it convenient to have a clickable icon to launch QVSED with, scroll down to find out how to make a shortcut/alias/symlink/whatever.

## License

QVSED is free software, licensed under the GNU General Public License version 3 or later.

## Usage

QVSED is broken up into three parts - the Action Deck, the Text Area and the Echo Area.

![QVSED screenshot, showing the help message](qsved_screenie.png)

## Action Deck

### Key

+ `C` - `Ctrl` (Windows, Linux), `⌘` (macOS)
+ `A` - `Alt` (Windows, Linux), `⌥` (macOS)

### Commands

**Clear Text** - `C-n` - Clear the Text Area. Think of it like New File.

**Open File** - `C-f` - Launch a file picker and load the chosen file's contents into the Text Area.

**Save File** - `C-s` - Launch a file picker and save the contents of the Text Area to the chosen file name.

**Full Screen** - `A-f` - Toggle full screen mode.

**Get Help** - `C-h` - Show a help message in the Text Area. This will overwrite your current work.

**Quit QVSED**  - `A-q` - Quit QVSED on the spot with no confirmation dialog.

## Text Area

The Text Area is where the actual text editing takes place.

You can enter and delete text, scroll down and up, cut, copy, paste, all that standard Notepad stuff.

QVSED is intentionally simplistic, and so there's not much to the Text Area.

## Echo Area

The Echo Area is the small bar at the bottom of the QVSED window that prints information.

For example, when a file is opened, it prints its file name. If a config file was not found, it'll generate one and give you the path.

QVSED inherited the name from Emacs. Well, less "inherited" and more "stolen from."

## Configuration

When QVSED is started, it looks for a configuration file. If it can't find one, it creates one and populates it with defaults.

On Windows, the configuration file will be stored at `C:\Users\<username>\AppData\Roaming\QVSED\config.py`, where `<username>` is your Windows username.

On *nix systems, the configuration file will be stored at `~/.config/QVSED/config.py`, where `~` is your home directory (`/home/<username>`).

The configuration file currently only supports two options to configure: `font_family` and `font_size`.

```python
# The default QVSED config.
font_family = ["JetBrains Mono", "Cascadia Code", "Consolas", "Menlo", "monospace"]
font_size = 11
```

Keep in mind that `font_family` *must* be a list. If you want only one font, specify:

```python
# Obviously replace "My Font" with the name of the font you want.
font_family = ["My Font"]
```

## Making Shortcuts

### Windows

1. Locate the QVSED executable file, usually located at `C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Scripts\qvsed.exe`. Substitute `<username>` with your Windows username and `xx` with whatever Python version you use, for example `Python311`.
2. Right-click on the executable file and select "Create Shortcut."
3. Move the shortcut to your desired location, such as the desktop or the Start Menu folder.
4. Double-click on the shortcut to launch QVSED directly.
5. If you want, supply your own icon, because QVSED doesn't have its own icon yet.

There aren't instructions for macOS or Linux because I didn't have access to either system at the time to check, but I'll update it in the future sometime maybe.
