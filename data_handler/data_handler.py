"""
All kinds of data input handlers will put in this file, all synced inside the pandas panel data
"""
from .base import AbstractDataHandler
import os
import pandas as pd
import warnings


class GenericCsvDataReader(AbstractDataHandler):
    """
    Generic csv data handler
    """
    def __init__(self, file_path, ticker_name, **pandas_kwargs):
        """
        :param file_path:  the file path + file name
        :param ticker_name: the ticker name
        :param pandas_kwargs: pandas read_csv
        """
        super().__init__()
        assert os.path.exists(file_path), "Cannot find the csv file path"
        self._file_path = file_path
        self._ticker_name = ticker_name
        self.data = self._read_csv_data(self._file_path, **pandas_kwargs)


    @property
    def ticker_name(self):
        return self._ticker_name

    def _read_csv_data(self, file_path, **kwargs):
        try:
            return pd.read_csv(file_path, **kwargs)
        except Exception:
            return -1


class GenericCsvDataReaderWithFormat(AbstractDataHandler):
    """
    This data reader provides a method to deal with data with "PATH/TICKER_NAME/files" storage style
    """
    def __init__(self, file_path, ticker_name, **kwargs):
        """
        :param file_path: the path where the all the equities data are stored
        :param ticker_name: ticker_name used as the folder (a list or a string)
        :param file_name_format: the format determines how the file is named, it contains three parts:
                %T ------ the ticker name
                %D ------ the date
                %* ------ the represents the extra part, e.g. %T-%D-**.csv
        :param kwargs: date ---- must be the date used to add into the file name, otherwise not need to set.
                                %D must be in the file_name_format
                       file_name ---- if specified, file_name_format cannot be used
        """
        self.file_path = None
        self.ticker_name = None
        self.file_name_format = None
        self.date = None
        self.file_name = None
        assert os.path.exists(file_path), "The specified path does not exist"
        self.file_path = file_path
        if 'file_name_format'in kwargs:
            assert isinstance(kwargs['file_name_format'], str), "the file name format must be a string"
            self.file_name_format = kwargs["file_name_format"]
        if 'date' in kwargs:
            self.date = kwargs["date"]
        if 'file_name' in kwargs:
            self.file_name = kwargs["file_name"]
        if isinstance(ticker_name, str):
            self.ticker_name = ticker_name
        if self.file_name is not None and self.file_name_format is not None:
            warnings.warn("notice that cannot use file name and file_name_format together, fall back to "
                          "file name")
        self.data = self._load_data()

    def _load_data(self):
        """
        :return: the data with specified or constructed path name
        """
        if self.file_name is not None and os.path.exists(os.path.join(self.file_path, self.file_name)):
            return pd.read_csv(os.path.join(self.file_path, self.file_name))
        if self.file_name_format is not None:
            file_name = self.file_name_format.replace("%T", self.ticker_name) if "%T" in self.file_name_format else \
                self.file_name_format
            file_name = file_name.replace("%D", self.date) if "%D" in file_name else file_name
            return pd.read_csv(os.path.join(self.file_path, file_name))


if __name__ == "__main__":
    handler = GenericCsvDataReaderWithFormat(file_path="/home/gausslee/programming/test_data/SP500",
                                             ticker_name="SP500", file_name="SP500.csv")
    print(handler.data)














