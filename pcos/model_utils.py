import pickle
import os
from pathlib import Path
import numpy as np

def load_pcos_model():
    """
    Load the PCOS prediction model from the PKL file
    """
    model_path = Path(__file__).resolve().parent.parent / 'model' / 'pcos_model.pkl'
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def create_engineered_features(features):
    """
    Create engineered features used during model training
    
    Args:
        features: Dictionary containing the base features
    Returns:
        dict: Dictionary containing base and engineered features
    """
    engineered = features.copy()
    
    # 1. Total Follicle Count
    engineered['Total_Follicle_Count'] = features.get('follicle_no_l', 0) + features.get('follicle_no_r', 0)
    
    # 2. Average Follicle Size
    engineered['Avg_Follicle_Size'] = (features.get('avg_f_size_l', 0) + features.get('avg_f_size_r', 0)) / 2
    
    # 3. BMI Category
    bmi = features.get('bmi', 0)
    if bmi < 18.5:
        bmi_category = 0  # Underweight
    elif bmi < 25:
        bmi_category = 1  # Normal
    elif bmi < 30:
        bmi_category = 2  # Overweight
    else:
        bmi_category = 3  # Obese
    engineered['BMI_Category'] = bmi_category
    
    # 4. LH/FSH Ratio
    fsh = features.get('fsh', 0.001)  # Avoid division by zero
    if fsh == 0:
        fsh = 0.001
    engineered['LH_FSH_Ratio'] = features.get('lh', 0) / fsh
    
    # 5. Symptom Count
    symptom_cols = ['weight_gain', 'hair_growth', 'skin_darkening', 'hair_loss', 'pimples']
    engineered['Symptom_Count'] = sum(features.get(col, 0) for col in symptom_cols)
    
    # 6. Lifestyle Score
    engineered['Lifestyle_Score'] = features.get('fast_food', 0) - features.get('reg_exercise', 0) + 1
    
    return engineered

def predict_pcos(features):
    """
    Make prediction using the loaded model
    
    Args:
        features: Dictionary containing the required features for prediction
    Returns:
        tuple: (prediction, probability)
            - prediction: 0 for no PCOS, 1 for PCOS
            - probability: Probability of the prediction
    """
    # Define the feature order based on the CSV columns and engineered features
    feature_order = [
        'Sl. No', 'Patient File No.', 'Age (yrs)', 'Weight (Kg)', 'Height(Cm)',
        'BMI', 'Blood Group', 'Pulse rate(bpm)', 'RR (breaths/min)', 'Hb(g/dl)',
        'Cycle(R/I)', 'Cycle length(days)', 'Marraige Status (Yrs)', 'Pregnant(Y/N)',
        'No. of abortions', 'I   beta-HCG(mIU/mL)', 'II    beta-HCG(mIU/mL)',
        'FSH(mIU/mL)', 'LH(mIU/mL)', 'FSH/LH', 'Hip(inch)', 'Waist(inch)',
        'Waist:Hip Ratio', 'TSH (mIU/L)', 'AMH(ng/mL)', 'PRL(ng/mL)',
        'Vit D3 (ng/mL)', 'PRG(ng/mL)', 'RBS(mg/dl)', 'Weight gain(Y/N)',
        'hair growth(Y/N)', 'Skin darkening (Y/N)', 'Hair loss(Y/N)',
        'Pimples(Y/N)', 'Fast food (Y/N)', 'Reg.Exercise(Y/N)',
        'BP _Systolic (mmHg)', 'BP _Diastolic (mmHg)', 'Follicle No. (L)',
        'Follicle No. (R)', 'Avg. F size (L) (mm)', 'Avg. F size (R) (mm)',
        'Endometrium (mm)',
        # Engineered features
        'Total_Follicle_Count', 'Avg_Follicle_Size', 'BMI_Category',
        'LH_FSH_Ratio', 'Symptom_Count', 'Lifestyle_Score'
    ]

    try:
        # Load the model
        model = load_pcos_model()
        if model is None:
            return None, None

        # Create engineered features
        engineered_features = create_engineered_features(features)

        # Map the input features to match CSV column names
        feature_mapping = {
            'age': 'Age (yrs)',
            'weight': 'Weight (Kg)',
            'height': 'Height(Cm)',
            'bmi': 'BMI',
            'blood_group': 'Blood Group',
            'pulse_rate': 'Pulse rate(bpm)',
            'rr': 'RR (breaths/min)',
            'hb': 'Hb(g/dl)',
            'cycle': 'Cycle(R/I)',
            'cycle_length': 'Cycle length(days)',
            'marriage_status': 'Marraige Status (Yrs)',
            'pregnant': 'Pregnant(Y/N)',
            'no_of_abortions': 'No. of abortions',
            'beta_hcg1': 'I   beta-HCG(mIU/mL)',
            'beta_hcg2': 'II    beta-HCG(mIU/mL)',
            'fsh': 'FSH(mIU/mL)',
            'lh': 'LH(mIU/mL)',
            'fsh_lh_ratio': 'FSH/LH',
            'hip': 'Hip(inch)',
            'waist': 'Waist(inch)',
            'waist_hip_ratio': 'Waist:Hip Ratio',
            'tsh': 'TSH (mIU/L)',
            'amh': 'AMH(ng/mL)',
            'prl': 'PRL(ng/mL)',
            'vit_d3': 'Vit D3 (ng/mL)',
            'prg': 'PRG(ng/mL)',
            'rbs': 'RBS(mg/dl)',
            'weight_gain': 'Weight gain(Y/N)',
            'hair_growth': 'hair growth(Y/N)',
            'skin_darkening': 'Skin darkening (Y/N)',
            'hair_loss': 'Hair loss(Y/N)',
            'pimples': 'Pimples(Y/N)',
            'fast_food': 'Fast food (Y/N)',
            'reg_exercise': 'Reg.Exercise(Y/N)',
            'bp_systolic': 'BP _Systolic (mmHg)',
            'bp_diastolic': 'BP _Diastolic (mmHg)',
            'follicle_no_l': 'Follicle No. (L)',
            'follicle_no_r': 'Follicle No. (R)',
            'avg_f_size_l': 'Avg. F size (L) (mm)',
            'avg_f_size_r': 'Avg. F size (R) (mm)',
            'endometrium': 'Endometrium (mm)',
            # Engineered features mapping
            'Total_Follicle_Count': 'Total_Follicle_Count',
            'Avg_Follicle_Size': 'Avg_Follicle_Size',
            'BMI_Category': 'BMI_Category',
            'LH_FSH_Ratio': 'LH_FSH_Ratio',
            'Symptom_Count': 'Symptom_Count',
            'Lifestyle_Score': 'Lifestyle_Score'
        }

        # Create a dictionary with CSV column names
        csv_features = {}
        for key, value in engineered_features.items():
            if key in feature_mapping:
                csv_features[feature_mapping[key]] = value

        # Add dummy values for Sl. No and Patient File No.
        csv_features['Sl. No'] = 0
        csv_features['Patient File No.'] = 0

        # Create feature array in the correct order
        X = np.array([[csv_features.get(feature, 0) for feature in feature_order]])
        
        # Make prediction
        prediction = model.predict(X)
        probability = model.predict_proba(X)[0]

        return int(prediction[0]), float(probability[1])  # Return probability of PCOS (class 1)
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
        return None, None 