"""
Class to compare zipped, zipped files for equality.

Suggested by CoPilot after long discussion.
"""


from zipfile import ZipFile
from io import BytesIO
from pathlib import Path


class InnerZip:
    """Represents a single inner ZIP inside an outer ZIP."""
    def __init__(self, outer_zip_path, inner_zip_name):
        self.outer_zip_path = Path(outer_zip_path)
        self.inner_zip_name = inner_zip_name

    def _open(self):
        """Open the inner ZIP as an in-memory ZipFile."""
        with ZipFile(self.outer_zip_path) as outer:
            inner_bytes = outer.read(self.inner_zip_name)
        return ZipFile(BytesIO(inner_bytes))

    def list_files(self):
        """Return all file names inside this inner ZIP."""
        with self._open() as inner:
            return inner.namelist()

    def iter_csvs(self, *, decode=False):
        """Yield (csv_name, csv_bytes_or_text) for each CSV inside this inner ZIP."""
        with self._open() as inner:
            for name in inner.namelist():
                if name.lower().endswith(".csv"):
                    data = inner.read(name)
                    yield name, (data.decode() if decode else data)

    def __repr__(self):
        return f"InnerZip({self.inner_zip_name!r})"


class NestedZipArchive:
    """Represents an outer ZIP containing multiple inner ZIPs."""
    def __init__(self, outer_zip_path):
        self.outer_zip_path = Path(outer_zip_path)

    def iter_inner_zips(self):
        """Yield InnerZip objects for each ZIP stored inside the outer ZIP."""
        with ZipFile(self.outer_zip_path) as outer:
            for name in outer.namelist():
                if name.lower().endswith(".zip"):
                    yield InnerZip(self.outer_zip_path, name)

    def iter_all_csvs(self, *, decode=False):
        """
        Yield (inner_zip_name, csv_name, csv_bytes_or_text)
        for every CSV inside every inner ZIP.
        """
        for inner in self.iter_inner_zips():
            for csv_name, data in inner.iter_csvs(decode=decode):
                yield inner.inner_zip_name, csv_name, data

    def __repr__(self):
        return f"NestedZipArchive({self.outer_zip_path!r})"


def nested_csv_dict(archive):
    """Return dict of all CSV file data in zip file."""
    return {
        (inner_zip, csv_name): data
        for inner_zip, csv_name, data in archive.iter_all_csvs()
    }
