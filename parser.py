# Read in the filenames and 
with open('./Experimental_setup/Knot_Tying/Balanced/GestureClassification/OneTrialOut/10_Out/itr_1/Train.txt') as f:
     file_names = f.readlines()
file_data = np.loadtxt('./Knot_Tying/kinematics/AllGestures/Knot_Tying_B001.txt')


import numpy as np

# Read in the filenames and 
with open('./Experimental_setup/Knot_Tying/Balanced/GestureClassification/OneTrialOut/10_Out/itr_1/Train.txt') as f:
     file_names = f.readlines()
file_data = np.loadtxt('./Knot_Tying/kinematics/AllGestures/Knot_Tying_B001.txt')

import numpy as np
import os 
# Read in the filenames and 
with open('./Experimental_setup/Knot_Tying/Balanced/GestureClassification/OneTrialOut/10_Out/itr_1/Train.txt') as f:
     file_names = f.readlines()
file_data = np.loadtxt('./Knot_Tying/kinematics/AllGestures/Knot_Tying_B001.txt')

class PreProcess(): 
    def __init__(self, directory):
        self.directory = directory
        
    def get_from_labelType(self, directory, data_type, labels, leave_out):
        '''
        Helper function for parse_experiment setup
        data_type: "Knot_Tying", "Suturing", "Needle_Passing"
        Labels: "GestureClassification", "GestureRecognition", "SkillDetection"
        Leave_out: "OneTrialOut", "SuperTrialOut", "UserOut"
        '''
        rootdir = os.path.join(directory, "Experimental_setup", data_type, "unBalanced", labels, leave_out)
        output = None
        if (labels == "SkillDetection"):
            form = 'i4'
        else:
            form = 'U64'
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                f = os.path.join(subdir, file)           
                if output is None:
                    output = np.loadtxt(f, dtype={'names': ('fileName', 'gesture'), 
                                             'formats': ('U64',  form)})
                else:
                    a = np.loadtxt(f, dtype={'names': ('fileName', 'gesture'), 
                                             'formats': ('U64', form)})
                    output = np.append(output, a)
        return output
    def parse_experimental_setup(self, data_type):
        '''
        Will iterate throught the experimental setup txt files
        @param data_type: will be either knot_tying, suturing, or needle_passing 
        @return: will return a list of three numpy objects:
            1). Gesture classification 
            2). Gesture Recognition
            3). Skill detection
        '''  
        leave_out="OneTrialOut"
        gClass = self.get_from_labelType(self.directory, data_type, "GestureClassification", leave_out)
        gRec = self.get_from_labelType(self.directory, data_type, "GestureRecognition", leave_out)

        if (data_type == "Suturing"):
            skillDet = self.get_from_labelType(self.directory, data_type, "SkillDetection", leave_out)
            return gClass, gRec, skillDet
        return gClass, gRec
    
    
    def get_start_and_end(txt_file):
        # Gets rid of '.txt' for the end of the row
        txt_file[4] = txt_file[4][0:-4]
        return txt_file[3], txt_file[4]

    def get_file_name(txt_file):
        return txt_file[0] + '_' + txt_file[1] + '_' + txt_file[2] + '.txt'
    
    def read_data(data, data_type):
        """
        Will read the data by it's appropriate line number
        @param data: a numpy array of size two containing a txt file name & 
        class value
        @param data_type: string that is either Knot_Tying, Suturing, or Needle_Passing
        @return output_data: the correct time series data
        """
        output_data = []
        for i in range(len(data)):
            row_data = []
            txt_file = data[i][0].split('_')
            file_name = get_file_name(txt_file)
            row_start, row_end = get_start_and_end(txt_file)
            with open('./' + data_type + '/kinematics/AllGestures/' + file_name) as f:
                rows = f.readlines()
            for j in range(row_start, row_end):
                current_row = rows[j].split()
                row_data.append(current_row)
            output_data.append(row_data)
        return output_data

    def parse(self):
        """
        Provides the entire functionality to parse our data

        @param: 
        @return: 
        """
        knot_tying_data = self.parse_experimental_setup('Knot_tying')
        suturing_data = self.parse_experimental_setup('Suturing')
        needle_passing = self.parse_experimental_setup('Needle_passing')
        
        # Iterate through the knot_tying data
        kt_gest_class_data = read_data(knot_tying_data[0], 'Knot_Tying')
        kt_gest_rec_data = read_data(knot_tying_data[1], 'Knot_Tying')
        print(kt_gest_class_data)
        # Iterate through the suturing data
        sut_gest_class_data = read_data(suturing_data[0], 'Suturing')
        sut_gest_rec_data = read_data(suturing_data[1], 'Suturing')
        sut_skill_data = read_data(suturing_data[2], 'Suturing')
        
        # Iterate through the needle passing data
        np_gest_class_data = read_data(needle_passing[0], 'Needle_Passing')
        np_gest_rec_data = read_data(suturing_data[1], 'Needle_Passing')
        