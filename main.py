import pydicom

from src.AnonymizeDicom.Anonymize_Dicom import anonymize_list_of_files, anonymize_datastructure
from DicomRTTool.ReaderWriter import DicomReaderWriter
import os
from glob import glob

path = r'O:\DICOM\Test2\Input'
output = r'O:\DICOM\Test2\Output'
reader = DicomReaderWriter()
reader.down_folder(input_path=path)
patient_index = 0
patient_ids_index = {}
for index in reader.series_instances_dictionary:
    pat_id = reader.series_instances_dictionary[index]['PatientID']
    if pat_id not in patient_ids_index:
        patient_ids_index[pat_id] = patient_index
        patient_index += 1
all_files = glob(os.path.join(path, '*.dcm'))
anonymized_files = []
for index in reader.series_instances_dictionary:
    files = reader.return_files_from_index(index)
    anonymized_files += files
    iteration = patient_ids_index[reader.series_instances_dictionary[index]['PatientID']]
    out_path = os.path.join(output, 'Anonymized_Patient_{}'.format(iteration))
    anonymize_list_of_files(files=files, out_path=out_path, anon_index=iteration)
for file in all_files:
    if file not in anonymized_files:
        ds = pydicom.read_file(file)
        pat_id = ds.PatientID
        if pat_id not in patient_ids_index:
            patient_ids_index[pat_id] = patient_index
            patient_index += 1
        anon_index = patient_ids_index[pat_id]
        output_path = os.path.join(output, 'Anonymized_Patient_{}'.format(anon_index))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        anonymize_datastructure(ds=ds, out_path=output_path, anon_index=anon_index)