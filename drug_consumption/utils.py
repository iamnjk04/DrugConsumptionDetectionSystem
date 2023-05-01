import pandas as pd
import os
import pickle
from django.conf import settings
import joblib
import sys

class Model:
    ohe_pipeline = None
    ohe_features  = None
    numerical_pipeline = None
    model_pipeline = None
    numeric_features =['Nscore', 'Escore', 'Oscore', 'AScore', 'Cscore', 'Impulsive'] 
    categorical_features = ['Age', 'Ethnicity']
    binary_features = ['Gender']
    
    def __init__(self,name):
        self.ohe_pipeline, self.ohe_features = self.load_file("frozen_files/ohe_pipeline.pkl")
        self.numerical_pipeline = self.load_file("frozen_files/numeric_pipeline.pkl")
        if name=="coke":
            self.model_pipeline =self.open_models("frozen_files/coke_grid_dtree.pkl")
        elif name=="heroin":
            self.model_pipeline =self.open_models("frozen_files/Heroin_dtree.pkl")
        elif name=="lsd":
            self.model_pipeline =self.open_models("frozen_files/LSD_dtree.pkl")
        elif name=="mushroom":
            self.model_pipeline =self.open_models("frozen_files/mushroom_grid_dtree.pkl")            
        # pass
    
    def open_models(self,file_name):
        file_path = os.path.join(settings.BASE_DIR, "drug_consumption/"+file_name)
        with open(file_path,"rb") as file:
            obj = pickle.load(file)
        return obj

    def load_file(self,file_name):
        file_path = os.path.join(settings.BASE_DIR, "drug_consumption/"+file_name)
        with open(file_path,"rb") as file:
            obj = joblib.load(file)
        return obj
    
    def set_values(self,nscore,escore,oscore,ascore,cscore,impulsive,gender,age,ethnicity):
        self.nscore = nscore
        self.escore = escore
        self.oscore = oscore
        self.ascore = ascore
        self.cscore = cscore
        self.impulsive = impulsive
        self.age = self.set_age(age)
        self.gender = gender
        self.ethnicity = ethnicity
    
    def set_age(self,age):
        if age>=25 and age<=34:
            age = '25-34'
        elif age>=35 and age<=44:
            age = '35-44'
        elif age>=18 and age<=24:
            age = '18-24'
        elif age>=45 and age<=54:
            age = '45-54'
        elif age>=55 and age<=64:
            age = '55-64'
        elif age>=65 :
            age = '65+'
        return age
    
    def create_dataframe(self):
        dict_ = {'Age': {0: self.age},
    'Gender': {0: self.gender},
    'Ethnicity': {0: self.ethnicity},
    'Nscore': {0: self.nscore},
    'Escore': {0: self.escore},
    'Oscore': {0: self.oscore},
    'AScore': {0: self.ascore},
    'Cscore': {0: self.cscore},
    'Impulsive': {0: self.impulsive}}
        self.df = pd.DataFrame(dict_)
        
    def preprocess_data(self,dataframe):
        X = dataframe.copy(deep = True)
        new_X = self.numerical_pipeline.transform(X)
        scaled_X = pd.DataFrame(new_X, columns = self.numeric_features+self.binary_features+self.categorical_features)
        transformed = self.ohe_pipeline.transform(scaled_X)
        transformed_df = pd.DataFrame(transformed, columns=self.ohe_features)
        arr_X = transformed_df.to_numpy()
        return arr_X
    
    def predict_data(self):
        self.create_dataframe()
        X = self.preprocess_data(self.df)
        prediction = self.model_pipeline.predict(X)
        print(prediction)
        return prediction
        # return prediction