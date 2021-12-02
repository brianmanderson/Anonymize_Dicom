import os
import pydicom
import time
import datetime
import SimpleITK as sitk
from DicomRTTool.ReaderWriter import DicomReaderWriter
import typing


def anonymize_datastructure(ds, out_path, anon_index):
    PatientID = "Patient_{}".format(anon_index)
    today = datetime.datetime.today()
    PatientsBirthDate = "{}{}{}".format(today.year, today.month, today.day)
    PatientName = "Anonymized_{}".format(anon_index)
    modality = ds.Modality
    ds.__setattr__("PatientID", PatientID)
    ds.__setattr__("OtherPatientIDs", PatientID)
    ds.__setattr__("PatientName", PatientName)
    ds.__setattr__("PatientBirthDate", PatientsBirthDate)
    for key in ["PhysiciansOfRecord", "ReferringPhysicianName", "StationName", "StudyDescription", "OperatorsName",
                "InstitutionName", "InstitutionAddress", "ReviewerName"]:
        if key in ds:
            ds.__setattr__(key, "Null")
    pydicom.write_file(os.path.join(out_path, "{}_{}.dcm".format(ds.Modality, ds.SOPInstanceUID)), ds)
    return None


def anonymize_list_of_files(files, out_path, anon_index):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for file in files:
        ds = pydicom.read_file(file)
        anonymize_datastructure(ds=ds, out_path=out_path, anon_index=anon_index)
    return None


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
    patient_index = 0
    patient_ids_index = {}
    for index in reader.series_instances_dictionary:
        pat_id = reader.series_instances_dictionary[index]['PatientID']
        if pat_id not in patient_ids_index:
            patient_ids_index[pat_id] = patient_index
            patient_index += 1
    for index in reader.series_instances_dictionary:
        files = reader.return_files_from_index(index)
        iteration = patient_ids_index[reader.series_instances_dictionary[index]['PatientID']]
        anonymizer.change_dicom_image_files(files=files, out_path_base=output_path, iteration=iteration)
    xxx = 1


if __name__ == '__main__':
    pass
