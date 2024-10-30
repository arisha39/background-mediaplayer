# Background Media Player

An application for playing media files in a window with a green chromakey background, ideal for capturing in OBS. It allows you to create custom button bindings to trigger playback in the background while using other applications.

## Features
- **Chromakey Background**: A green background for easy capture and keying in OBS.
- **Custom Key Bindings**: Set key combinations to trigger media playback.
- **Easy File Management**: Store and manage key bindings in `media_files.json`.

## Getting Started

### 1. Launching the Application
When you start the app, a window with a green chromakey background opens. 

### 2. Configuring Key Bindings
1. Open the **Settings** window by pressing the `Tab` key.
2. In the settings window:
   - Enter your preferred key combination for playback.
   - Specify the path to the media file, or use the **Browse** button to locate it.
3. Save the key binding by clicking **Save Binding**.
4. To delete a binding, select it in the list of all bindings and press **Delete Bindings**.

### 3. Managing Bindings
- When new bindings are created, a file called `media_files.json` is generated in the application’s root directory. This file stores all your bindings.
- **Persistence**: Your bindings will be ready to use each time you start the app if the `media_files.json` file is present.

## Installation Requirements

Make sure to install the necessary libraries:

```bash
pip install python-vlc
pip install pyqt5
pip install keyboard
```

### Additional Requirements
- **VLC Player**: [Download and install the VLC media player](https://www.videolan.org/vlc/).
- **Microsoft C++ Build Tools**: [Install Visual Studio](https://visualstudio.microsoft.com/ru/visual-cpp-build-tools/) with the **Desktop Development with C++** workload enabled.
