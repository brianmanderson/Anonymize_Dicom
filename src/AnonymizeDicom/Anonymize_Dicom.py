import os
import pydicom
import time
import datetime
import SimpleITK as sitk
from DicomRTTool.ReaderWriter import DicomReaderWriter
import typing


class DicomAnonymizerClass(object):
    def __init__(self):
        self.image_reader = sitk.ImageFileReader()
        self.image_reader.LoadPrivateTagsOn()
        self.reader = sitk.ImageSeriesReader()
        self.reader.GlobalWarningDisplayOff()

    def change_dicom_image_files(self, files, out_path_base, iteration):
        out_path = os.path.join(out_path_base, 'Anonymized_Patient_{}'.format(iteration))
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        PatientID = "Patient_{}".format(iteration)
        today = datetime.datetime.today()
        AcquistionDate = ContentDate = StudyDate = PatientsBirthDate = "{}{}{}".format(today.year, today.month, today.day)
        PatientName = "Anonymized_{}".format(iteration)
        modality_names = {}
        for file in files:
            ds = pydicom.read_file(file)
            modality = ds.Modality
            if modality not in modality_names:
                modality_names[modality] = 1
            ds.PatientID = PatientID
            ds.OtherPatientIDs = PatientID
            ds.AcquistionDate = AcquistionDate
            ds.ContentDate = ContentDate
            ds.StudyDate = StudyDate
            ds.PatientsBirthDate = PatientsBirthDate
            ds.PatientName = PatientName
            pydicom.write_file(os.path.join(out_path, "{}_{}.dcm".format(modality, modality_names[modality])), ds)
            modality_names[modality] += 1

def anonymize_dicom_down_path(input_path: typing.Union[str, bytes, os.PathLike],
                              output_path: typing.Union[str, bytes, os.PathLike]) -> None:
    """
    :param input_path: a path to a set of DICOM files
    :param output_path: a path that anonymized DICOM files will be written
    :return: None
    """
    anonymizer = DicomAnonymizerClass()
    """
    Go down the input path and find all of the patients
    """
    reader = DicomReaderWriter()
    reader.down_folder(input_path=input_path)
    """
    For each patient, we will need to anonymize the images, structures, plans, and dose files while ensuring
    we still maintain a consistent identifier
    """
    for index in reader.series_instances_dictionary:
        files = reader.return_files_from_index(index)
        anonymizer.change_dicom_image_files(files=files, out_path_base=output_path, iteration=index)
    xxx = 1


if __name__ == '__main__':
    pass
