# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 23:01:12 2022

@author: Karan Gupta
"""
import os
import pickle
import numpy as np
from dotenv import load_dotenv
from os.path import join, dirname
from stop_words import get_stop_words


def predict(data, ui_flag_param=False, top_n_results_param=5):
    output = []
    try:
        """Read the parameters from the method call"""
        input_data = data
        ui_flag = ui_flag_param
        top_n_results = int(top_n_results_param)

        """use the stop words to ignore them in the search match"""
        stop_words = get_stop_words('english')

        """Setup to read env file for various parameters"""
        dotenv_path = join(dirname(__file__), 'var.env')
        load_dotenv(dotenv_path)

        """Read Parameters from env file"""
        output_no_match = os.getenv('output_no_match')
        pickle_files_path = os.getenv('pickle_files_path')
        input_column = os.getenv('input_column')
        output_column = os.getenv('output_columns')
        delimiter = os.getenv('delimiter')

        """Load the Countvectorizer which was saved as pickle for later use as part of training"""
        with open(pickle_files_path + 'cv.pkl', 'rb') as tm:
            cv = pickle.load(tm)

        """Load the model which was saved as pickle for later use as part of training"""
        with open(pickle_files_path + 'model.pkl', 'rb') as tm:
            model = pickle.load(tm)

        """Prediction for user input"""
        input_data_cv = cv.transform([input_data])
        predicted = model.predict_proba(input_data_cv)

        """Read the labels index and probabilities in sorted order"""
        top_n_labels_idx = np.argsort(-predicted, axis=1)  # [:, :topNResults]
        top_n_probs = np.round(-np.sort(-predicted), 3)  # [:, :topNResults]

        """Convert user input into lowercase for better matching"""
        input_data_lowercase = str(input_data).lower().split()

        """Split the output Data based on env file column names"""
        op_col = output_column.split(",")

        """Position of input column name in the list of output column names"""
        position_of_ip_in_op = op_col.index(input_column)

        """calculate length of input column name to find substring which is to be used to match against the user 
        input"""
        len_of_ip = len(input_column)
        counter = 0
        results_predicted_count = 0

        while counter < len(model.classes_):
            for i, x in zip(top_n_labels_idx, top_n_probs):
                if results_predicted_count < top_n_results:
                    temp_label = str(model.classes_[i[counter]]).lower()
                    """use split at the end to match exact words"""
                    # temp_label_substring = (temp_label[temp_label.index(op_col[position_of_ip_in_op].lower()) +
                    # len_of_ip +4:temp_label.index(op_col[position_of_ip_in_op+1].lower()) - len(delimiter) ]).split()
                    temp_label_substring = (temp_label[temp_label.index(
                        op_col[position_of_ip_in_op].lower()) + len_of_ip + 4:temp_label.index(
                        op_col[position_of_ip_in_op + 1].lower()) - len(delimiter)])

                    """Match any word in user input in the model class label substring excluding stop words. If 
                    matches, add label to output array"""
                    res = any(element in temp_label_substring for element in input_data_lowercase if
                              (element not in stop_words))
                    if res:
                        output.append(model.classes_[i[counter]])
                        results_predicted_count += 1
                else:
                    break
            counter += 1

        """if the output is blank, append no match found in output or check if user supplied top_n_results parameter 
        > 0 or not and modify output accorindingly"""
        if len(output) == 0:
            if top_n_results > 0:
                output.append(output_no_match)
            else:
                output.append("The top n results parameter should be greater than 0")

        """Based on whether call is from UI or Commandline, format the output"""
        if ui_flag:
            return output
        else:
            if len(output) >= 1 and results_predicted_count > 0:
                for o in output:
                    print("Record No. " + str(output.index(o) + 1) + '\n')
                    o = o.replace(delimiter, "\n\n")
                    print(o)
                    print(
                        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            elif len(output) == 1:
                print(output[0])
    except Exception as e:
        output.clear()
        output.append("There is an error in the processing. Please contact the site owner")
        if ui_flag:
            return output
        else:
            print(output[0])

# predict("CPU",False,3)
