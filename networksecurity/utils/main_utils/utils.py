import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import numpy as np
import pickle
import os,sys
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        return NetworkSecurityException(e,sys)    
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
            raise NetworkSecurityException(e,sys)                       
        
        
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
            raise NetworkSecurityException(e,sys)                                
        
        
def load_object(file_path:str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The File: {file_path} doesnot exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
            raise NetworkSecurityException(e,sys) from e          
        
def load_numpy_array_data(file_path:str)-> np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
            raise NetworkSecurityException(e,sys) from e       
        
def evaluate_model(x_train,y_train,x_test,y_test,models:dict,params:dict)->dict:
    try:
        report={}
        
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = models[model_name]
            para=params[list(models.keys())[i]]
            
            gs=GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)
            
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            
            report[model_name]=test_model_score
            
        return report                           
    except Exception as e:
            raise NetworkSecurityException(e,sys) from e          