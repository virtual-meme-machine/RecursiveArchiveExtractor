class ArchiveObject(object):
    """Object that stores data for a single archive file"""

    def __init__(self, file_path, file_name, archive_format, archive_size):
        """Initialize object variables"""
        self.file_name = file_name
        self.file_path = file_path
        self.archive_format = archive_format
        self.archive_size = archive_size
