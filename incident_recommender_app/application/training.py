# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 23:01:12 2022

@author: Karan Gupta
"""
import os
import glob
import shutil
import pickle
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

"""
Below library to be used when data splitting is required into training and testing data
#from sklearn.model_selection import train_test_split
"""


def train(excel_files=None):
    try:
        """Setup to read env file for various parameters"""
        dotenv_path = join(dirname(__file__), 'var.env')
        load_dotenv(dotenv_path)

        """Read Parameters from env file"""
        sheets_names = os.getenv('sheets_to_read')
        input_column = os.getenv('input_column')
        output_column = os.getenv('output_columns')
        training_data_path = os.getenv('training_data_path')
        pickle_files_path = os.getenv('pickle_files_path')
        delimiter = os.getenv('delimiter')

        """Read all sheet names for all the data which is to be used for data training"""
        sheets_to_read = sheets_names.split(",")

        """Read all excel sheets from Training Data Path which is to be used for data training"""
        filenames = glob.glob(training_data_path + "*.xlsx")

        if excel_files is not None:
            newfolder = datetime.now().strftime('%Y%m%d-%H%M%S')
            os.mkdir(training_data_path + newfolder)
            for i in filenames:
                shutil.move(i, training_data_path + newfolder)
            for i in excel_files:
                with open(training_data_path + i.name, 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
            filenames = glob.glob(training_data_path + "*.xlsx")

        if len(filenames) == 0:
            raise FileNotFoundError()

        """Read all the data into a single dataset "orig_data" for all the worksheets mentioned in env file"""
        orig_data = pd.DataFrame()
        dataframe = []
        for filename in filenames:
            # orig_data = orig_data.append(pd.concat(pd.read_excel(filename, sheet_name=sheets_to_read).values(
            # )).dropna(how='all'),ignore_index=True)
            xls = pd.ExcelFile(filename)
            for sheet_name in sheets_to_read:
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(filename, sheet_name=sheet_name)
                    dataframe.append(df)
            xls.close()
        orig_data = pd.concat(dataframe, ignore_index=True)

        """Split the input Data based on env file input column name"""
        x = np.array(orig_data[input_column].str.replace("\n", " "))

        """Split the output Data based on env file column names"""
        op_col = output_column.split(",")
        temp_count = 0
        y = ''
        while temp_count < len(op_col):
            if y is None:
                y = op_col[temp_count] + "\" - " + np.array(
                    orig_data[op_col[temp_count]].str.replace('\n', " ")) + delimiter
            elif temp_count == len(op_col) - 1:
                y = y + '"' + op_col[temp_count] + "\" - " + np.array(
                    orig_data[op_col[temp_count]].str.replace('\n', " "))
            else:
                y = y + '"' + op_col[temp_count] + "\" - " + np.array(
                    orig_data[op_col[temp_count]].str.replace('\n', " ")) + delimiter
            temp_count += 1

        """Machines cannot understand characters and words. So when dealing with text data we need to represent it in 
        numbers to be understood by the machine.Countvectorizer is a method to convert text to numerical data."""
        cv = CountVectorizer(max_df=0.5)
        X = cv.fit_transform(x)
        with open(pickle_files_path + 'cv.pkl', 'wb') as picklefile:
            pickle.dump(cv, picklefile)

        """Naive Bayes classifier for multinomial models. suitable for classification with discrete features (e.g., 
        word counts for text classification)"""
        model = MultinomialNB()
        model.fit(X, y)

        """Save the model for prediction later on"""
        with open(pickle_files_path + 'model.pkl', 'wb') as picklefile:
            pickle.dump(model, picklefile)
        print("Model Training successfully completed")
        return "Model Training successfully completed"
    except FileNotFoundError:
        error_msg = "There is an error processing the excel files. Please contact the site owner"
        print(error_msg)
        return error_msg
    except Exception as ex:
        error_msg = "There is an error in the model training process. Please contact the site owner"
        print(error_msg)
        return error_msg

# train()
