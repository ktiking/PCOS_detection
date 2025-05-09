import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings

# Load the model
model_path = os.path.join(settings.BASE_DIR, 'model', 'pcos_model.pkl')
model = joblib.load(model_path)

def predict_pcos(data):
    """
    this function takes in some data and tells us if someone might have PCOS
    it's pretty straightforward - just feed it the right numbers and it'll give you a prediction
    
    Args:
        data (dict): all the info we need about the person:
            - age: how old they are
            - weight: their weight in kg
            - bmi: their body mass index
            - cycle: if their cycle is regular (R) or irregular (I)
            - cycle_length: how long their cycle is in days
            - lh_fsh_ratio: the ratio of LH to FSH hormones
            - weight_gain: if they've gained weight (Y/N)
            - hair_growth: if they have excess hair growth (Y/N)
            - follicle_no_l: how many follicles on the left ovary
            - follicle_no_r: how many follicles on the right ovary
            - hip: hip measurement in inches
            - skin_darkening: if they have skin darkening (Y/N)
            - lifestyle_score: their lifestyle score (-1 to 1)
            - symptom_count: how many symptoms they have
            - total_follicle_count: total number of follicles
        
    Returns:
        dict: tells us if they might have PCOS and how likely it is
    """
    try:
        # convert yes/no and regular/irregular to numbers
        cycle_map = {'R': 2, 'I': 4}  # based on what we saw in the training data
        yn_map = {'Y': 1, 'N': 0}
        
        # put all the data in the right format for our model
        features = pd.DataFrame([{
            'Weight (Kg)': float(data['weight']),
            'Lifestyle_Score': float(data['lifestyle_score']),
            'Cycle(R/I)': cycle_map[data['cycle']],
            'BMI': float(data['bmi']),
            'LH_FSH_Ratio': float(data['lh_fsh_ratio']),
            'Weight gain(Y/N)': yn_map[data['weight_gain']],
            'hair growth(Y/N)': yn_map[data['hair_growth']],
            'Follicle No. (L)': float(data['follicle_no_l']),
            'Age (yrs)': float(data['age']),
            'Follicle No. (R)': float(data['follicle_no_r']),
            'Symptom_Count': float(data['symptom_count']),
            'Hip(inch)': float(data['hip']),
            'Skin darkening (Y/N)': yn_map[data['skin_darkening']],
            'Total_Follicle_Count': float(data['total_follicle_count']),
            'Cycle length(days)': float(data['cycle_length'])
        }])
        
        # make the prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1] * 100
        
        return {
            'prediction': int(prediction),
            'probability': float(probability)
        }
        
    except Exception as e:
        raise Exception(f"oops, something went wrong: {str(e)}")

def get_feature_importance():
    """
    this function tells us which things are most important for predicting PCOS
    like, is weight more important than age? that kind of thing
    
    Returns:
        dict: shows how important each feature is
    """
    try:
        # list of all the things we look at
        feature_names = [
            'Weight (Kg)', 'Lifestyle_Score', 'Cycle(R/I)', 'BMI', 'LH_FSH_Ratio',
            'Weight gain(Y/N)', 'hair growth(Y/N)', 'Follicle No. (L)', 'Age (yrs)',
            'Follicle No. (R)', 'Symptom_Count', 'Hip(inch)', 'Skin darkening (Y/N)',
            'Total_Follicle_Count', 'Cycle length(days)'
        ]
        
        # get how important each thing is
        importance_scores = model.feature_importances_
        
        # put it all together in a nice dictionary
        feature_importance = dict(zip(feature_names, importance_scores))
        
        # sort it so the most important things are first
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
    except Exception as e:
        raise Exception(f"oops, couldn't get feature importance: {str(e)}") 