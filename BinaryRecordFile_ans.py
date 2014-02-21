import os
import struct
import tempfile


class BinaryRecordFile:

    def __init__(self, filename, record_size, auto_flush=True):
        """A random access binary file that behaves rather like a list
        with each item a bytes or bytesarray object of record_size
        """
        self.__record_size = record_size
        mode = "w+b" if not os.path.exists(filename) else "r+b"
        self.__fh = open(filename, mode)
        self.auto_flush = auto_flush

    @property
    def record_size(self):
        "The size of each item"
        return self.__record_size

    @property
    def name(self):
        "The name of filename"
        return self.__fh.name

    def flush(self):
        """Flush writes to disk
        Done automatically if auto_flush if True
        """
        self.__fh.flush()

    def close(self):
        self.__fh.close()

    def append(self, record):
        """Add a new record"""
        assert isinstance(record, (bytes, bytearray), \
                "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(self.record_size))
        self.__fh.seek(0, os.SEEK_END)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()

    def __setitem__(self, index, record):
        """Sets the item at postion index to be the given record
        The index position can be beyond the current end of the file.
        """
        assert isinstance(record, (bytes, bytearray)), \
                "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(self.record_size))
        self.__seek_to_index(index)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()

    def __getitem__(self, index):
        """Return the item at the given index position
        If there is no item at the given position, raises an
        IndexError exception.
        If the item at the given position has been deleted returns
        None.
        """
        self.__seek_to_index(index)
        return self.__fh.read(self.record_size)

    def __seek_to_index(self, index):
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        offset = index * self.record_size
        if offset >= end:
            raise IndexError("no record at index position {0}".format(index)
        self.__fh.seek(offset)

    def __delitem__(self, index):
        """Delete the item at the given index position and moves the
        following records up.
        """
        length = len(self)
        for following in range(index+1, length):
            self[index] = self[following]
            index += 1
        self.__fh.truncate((length-1) * self.record_size)
        self.__fh.flush()

    def __len__(self):
        """The number of records"""
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        return end // self.record_size

if __name__ == "__main__":
    import doctest
    doctest.testmod()
