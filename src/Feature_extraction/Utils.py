import os
import csv
import random
from Features_extraction import head_nods, head_rotation, overall_motion

dataset_path = "C://Users//ghamm//OneDrive//Bureau//UQAC//Hiver//Séminaire//dataset"

csv_file = "extracted_features.csv"

def featurestoCSV(dataset_path ,csv_file): 

    es_path = dataset_path + '//'+ "ES"
    ne_path = dataset_path + '//'+ "NE"

    # Create or open the CSV file in write mode
    with open(csv_file, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(["File", "Head_nods", "Head_rotations", "Magnitude", "Temporal_dynamic", "Target"])


        # Iterate over files in the 'es' directory
        for es_file in os.listdir(es_path):
            print(es_file)
            if es_file.endswith(".mp4"):
                # Construct the full file path
                es_file_path = es_path+'//'+es_file
                print(es_file_path)

                feature1 = head_nods(es_file_path)
                feature2 = head_rotation(es_file_path)
                feature3,feature4 = overall_motion(es_file_path)

                # Write the extracted features to the CSV file with target label 'ES'
                csv_writer.writerow([es_file, feature1, feature2, feature3, feature4, 'ES'])

        # Iterate over files in the 'neurotic' directory
        for neurotic_file in os.listdir(ne_path):
            print(neurotic_file)
            if neurotic_file.endswith(".mp4"):
                # Construct the full file path
                ne_file_path = ne_path+'//'+neurotic_file

                feature1 = head_nods(ne_file_path)
                feature2 = head_rotation(ne_file_path)
                feature3,feature4 = overall_motion(ne_file_path)

                # Write the extracted features to the CSV file with target label 'neurotic'
                csv_writer.writerow([neurotic_file, feature1, feature2, feature3, feature4, 'NE'])        

        

# Call the function to extract features and shuffle the CSV file
featurestoCSV(dataset_path, csv_file) 




