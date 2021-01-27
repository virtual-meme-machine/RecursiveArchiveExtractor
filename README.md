## Recursive Archive Extractor
A simple utility for recursively extracting archive files to a single directory.

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

### TODO:
- Finish adding logging to all workflows
- Fix scanning / cancel button issues
- Window resizing
- Add sorting to file list
- Checkboxes to select archive files to be extracted from the file list
- Settings menu (toggle logging, language, etc.)
- Package application as OS specific binaries (exe, app, elf, etc.)