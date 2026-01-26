"""
Classes to describe source file formats
"""


class Source():
    """
    Read multiple line records from text file
    """
    def __init__(self, filename, pad_cols, split_csz):
        self.file_hndl = open(filename, encoding='utf8')
        self.pad_cols = pad_cols
        self.split_csz = split_csz

    # context manager methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_hndl.close()

    # iterator methods
    def __iter__(self):
        return self

    def __next__(self):
        record = []
        line = self.file_hndl.readline()
        while line != '\n':
            record.append(line.strip())
            line = self.file_hndl.readline()
            if line == '':
                raise StopIteration
        if self.pad_cols:
            count = len(record)
            while count < 4:
                record.insert(-1, '')
                count += 1
        if self.split_csz:
            csz = record[-1].split()
            if len(csz) > 3 and len(csz[-2]) == 2:
                # handle multi word city names
                csz = [' '.join(csz[:-2])] + csz[-2:]
            record = record[:-1]
            record.extend(csz)
        return record
