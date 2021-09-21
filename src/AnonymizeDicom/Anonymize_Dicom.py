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

    def change_dicom_image_files(self, series_instances_dictionary, out_path_base, iteration):
        out_path = os.path.join(out_path_base, 'Anonymized_Patient_{}'.format(iteration))
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        series_instance = series_instances_dictionary[iteration]
        series_id = series_instance['SeriesInstanceUID']
        dicom_path = series_instance['Image_Path']
        dicom_names = self.reader.GetGDCMSeriesFileNames(dicom_path, series_id)
        PatientID = "Patient_{}".format(iteration)
        today = datetime.datetime.today()
        AcquistionDate = ContentDate = StudyDate = PatientsBirthDate = "{}{}{}".format(today.year, today.month, today.day)
        PatientName = "Anonymized_{}".format(iteration)
        file_index = 0
        for dicom_name in dicom_names:
            ds = pydicom.read_file(dicom_name)
            ds.PatientID = PatientID
            ds.OtherPatientIDs = PatientID
            ds.AcquistionDate = AcquistionDate
            ds.ContentDate = ContentDate
            ds.StudyDate = StudyDate
            ds.PatientsBirthDate = PatientsBirthDate
            ds.PatientName = PatientName
            pydicom.write_file(os.path.join(out_path, "dicom_{}.dcm".format(file_index)), ds)
            file_index += 1
        rt_index = 0
        for RT in series_instance['RTs']:
            ds = pydicom.read_file(series_instance['RTs'][RT]['Path'])
            ds.PatientID = PatientID
            ds.OtherPatientIDs = PatientID
            ds.AcquistionDate = AcquistionDate
            ds.ContentDate = ContentDate
            ds.StudyDate = StudyDate
            ds.PatientsBirthDate = PatientsBirthDate
            ds.PatientName = PatientName
            pydicom.write_file(os.path.join(out_path, "RT_{}.dcm".format(rt_index)), ds)
            rt_index += 1

        rd_index = 0
        for RD in series_instance['RDs']:
            ds = pydicom.read_file(series_instance['RDs'][RD]['Path'])
            ds.PatientID = PatientID
            ds.OtherPatientIDs = PatientID
            ds.AcquistionDate = AcquistionDate
            ds.ContentDate = ContentDate
            ds.StudyDate = StudyDate
            ds.PatientsBirthDate = PatientsBirthDate
            ds.PatientName = PatientName
            pydicom.write_file(os.path.join(out_path, "RD_{}.dcm".format(rd_index)), ds)
            rt_index += 1

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
    for key in reader.series_instances_dictionary.keys():
        anonymizer.change_dicom_image_files(series_instances_dictionary=reader.series_instances_dictionary,
                                            out_path_base=output_path, iteration=key)
    xxx = 1


if __name__ == '__main__':
    pass
