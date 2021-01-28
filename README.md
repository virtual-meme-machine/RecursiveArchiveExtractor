## Recursive Archive Extractor
A simple utility for recursively extracting archive files to a single directory.

![image](https://user-images.githubusercontent.com/46010615/106102840-dbbfd100-60f4-11eb-86ed-404b16252bed.png)

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
        │   ├── archive_file_10.part1.rar
        │   ├── archive_file_10.part2.rar
        │   ├── archive_file_10.part3.rar
        │   ├── archive_file_10.part4.rar
        │   └── archive_file_10.part5.rar
        ├── Sub Sub Folder 5
        │   ├── archive_file_11.rar
        │   ├── archive_file_12.rar
        │   └── archive_file_13.rar
        └── Sub Sub Folder 6
            ├── archive_file_14.rar
            └── archive_file_15.rar
```

### Features:
- Easy to use GUI
- Supports RAR and ZIP archive formats
- Intelligently handles split archives to avoid extracting the same file multiple times

### Upcoming Features:
- Support for additional archive formats
- Window resizing
- Add sorting to file list
- Better installation method
- Checkboxes to select archive files to be extracted from the file list
- Settings menu (toggle logging, language, etc.)
- Prebuilt applications for macOS, Linux, BSD, etc.
- Safety check to prevent attempting to extract files to a location that does not have enough space for them

### Known Issues:
- Cancelling an in progress scan will sometimes not fully clear the file list in the gui
- Cancel buttons don't kill spawned process threads immediately, this seems to be a limitation of Python