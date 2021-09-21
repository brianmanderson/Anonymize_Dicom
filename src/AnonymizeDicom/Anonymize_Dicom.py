import os
import pydicom
import time
from DicomRTTool.ReaderWriter import DicomReaderWriter
import typing


def anonymize_dicom_down_path(input_path: typing.Union[str, bytes, os.PathLike],
                              output_path: typing.Union[str, bytes, os.PathLike]) -> None:
    """
    :param input_path: a path to a set of DICOM files
    :param output_path: a path that anonymized DICOM files will be written
    :return: None
    """
    reader = DicomReaderWriter()
    reader.down_folder(input_path=input_path)
    xxx = 1


if __name__ == '__main__':
    pass
