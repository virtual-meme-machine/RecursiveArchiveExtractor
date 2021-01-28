## Recursive Archive Extractor
A simple utility for recursively extracting archive files to a single directory.

![screen_shot](https://user-images.githubusercontent.com/46010615/106102154-d0b87100-60f3-11eb-9be6-6ebe30283ab6.png)

Designed to handle annoying situations like this:
```
Downloads
└── Root Folder
    ├── Sub Folder 1
    │   ├── Sub Sub Folder 1
    │   │   ├── archive_file_1.zip
    │   │   ├── archive_file_2.zip
    │   │   └── archive_file_3.zip
    │   ├── Sub Sub Folder 2
    │   │   ├── archive_file_4.zip
    │   │   └── archive_file_5.zip
    │   └── Sub Sub Folder 3
    │       ├── archive_file_6.zip
    │       ├── archive_file_7.zip
    │       ├── archive_file_8.zip
    │       └── archive_file_9.zip
    └── Sub Folder 2
        ├── Sub Sub Folder 4
        │   └── archive_file_10.rar
        ├── Sub Sub Folder 5
        │   ├── archive_file_11.rar
        │   ├── archive_file_12.rar
        │   └── archive_file_13.rar
        └── Sub Sub Folder 6
            ├── archive_file_14.rar
            └── archive_file_15.rar
```

### Python library dependencies:
- rarfile
- wxPython

### (Janky) Installation:
```
pip install wxpython
pip install rarfile
git clone https://github.com/virtual-meme-machine/RecursiveArchiveExtractor.git
cd RecursiveArchiveExtractor
python main.py
```

### Known issues:
- Cancelling an in progress scan will sometimes not fully clear the file list in the gui
- Cancel buttons don't kill spawned process threads immediately, this seems to be a limitation of Python

### Upcoming features:
- Support for additional archive formats, currently supports RAR and ZIP format archive files
- Window resizing
- Add sorting to file list
- Better installation method
- Checkboxes to select archive files to be extracted from the file list
- Settings menu (toggle logging, language, etc.)
- Package application as OS specific binaries (exe, app, elf, etc.)