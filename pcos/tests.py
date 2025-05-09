from django.test import TestCase
from pcos_detection.model_utils import predict_pcos, calculate_derived_features, get_feature_importance

class PCOSModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.sample_data = {
            'weight': 65.0,  # Weight in Kg
            'lifestyle_score': 7.5,  # Lifestyle score
            'cycle': 'I',  # Irregular cycle
            'bmi': 24.5,  # Normal BMI
            'lh_fsh_ratio': 2.1,  # LH/FSH ratio
            'weight_gain': 'Y',  # Yes to weight gain
            'hair_growth': 'Y',  # Yes to hair growth
            'follicle_no_l': 12,  # Follicle number left
            'age': 28,  # Age in years
            'follicle_no_r': 10,  # Follicle number right
            'symptom_count': 4,  # Number of symptoms
            'hip': 36.0,  # Hip measurement in inches
            'skin_darkening': 'Y',  # Yes to skin darkening
            'total_follicle_count': 22,  # Total follicle count
            'cycle_length': 45  # Cycle length in days
        }

    def test_derived_features(self):
        """Test if derived features are calculated correctly"""
        features = calculate_derived_features(self.sample_data)
        
        # Test BMI category
        self.assertEqual(features['bmi_category'], 1)  # Normal BMI (18.5-25)
        
        # Test age category
        self.assertEqual(features['age_category'], 1)  # Young adult (20-30)
        
        # Test weight category
        self.assertEqual(features['weight_category'], 1)  # Normal weight (50-70)
        
        # Test cycle category
        self.assertEqual(features['cycle_category'], 2)  # Long cycle (>35 days)

    def test_prediction(self):
        """Test if the prediction function works with sample data"""
        try:
            prediction = predict_pcos(self.sample_data)
            
            # Test prediction structure
            self.assertIsNotNone(prediction, "Prediction should not be None")
            self.assertIn('prediction', prediction, "Prediction should have 'prediction' key")
            self.assertIn('probability', prediction, "Prediction should have 'probability' key")
            
            # Test prediction values
            self.assertIn(prediction['prediction'], [0, 1], "Prediction should be 0 or 1")
            self.assertGreaterEqual(prediction['probability'], 0, "Probability should be >= 0")
            self.assertLessEqual(prediction['probability'], 1, "Probability should be <= 1")
            
        except Exception as e:
            self.fail(f"Prediction failed with error: {str(e)}")

    def test_categorical_conversion(self):
        """Test if categorical features are converted correctly"""
        # Test regular cycle
        data_regular = self.sample_data.copy()
        data_regular['cycle'] = 'R'
        prediction_regular = predict_pcos(data_regular)
        self.assertIsNotNone(prediction_regular)
        
        # Test irregular cycle
        data_irregular = self.sample_data.copy()
        data_irregular['cycle'] = 'I'
        prediction_irregular = predict_pcos(data_irregular)
        self.assertIsNotNone(prediction_irregular)
        
        # Test Y/N features
        data_yn = self.sample_data.copy()
        data_yn['weight_gain'] = 'N'
        data_yn['hair_growth'] = 'N'
        data_yn['skin_darkening'] = 'N'
        prediction_yn = predict_pcos(data_yn)
        self.assertIsNotNone(prediction_yn)

    def test_edge_cases(self):
        """Test edge cases for feature values"""
        # Test minimum values
        data_min = self.sample_data.copy()
        data_min['age'] = 15
        data_min['weight'] = 40
        data_min['bmi'] = 16
        data_min['cycle_length'] = 15
        prediction_min = predict_pcos(data_min)
        self.assertIsNotNone(prediction_min)
        
        # Test maximum values
        data_max = self.sample_data.copy()
        data_max['age'] = 45
        data_max['weight'] = 100
        data_max['bmi'] = 35
        data_max['cycle_length'] = 60
        prediction_max = predict_pcos(data_max)
        self.assertIsNotNone(prediction_max)

    def test_missing_features(self):
        """Test handling of missing features"""
        # Test with missing required feature
        data_missing = self.sample_data.copy()
        del data_missing['age']
        with self.assertRaises(ValueError):
            predict_pcos(data_missing)

    def test_invalid_values(self):
        """Test handling of invalid feature values"""
        # Test with invalid numeric value
        data_invalid = self.sample_data.copy()
        data_invalid['age'] = 'invalid'
        with self.assertRaises(ValueError):
            predict_pcos(data_invalid)
        
        # Test with invalid categorical value
        data_invalid = self.sample_data.copy()
        data_invalid['cycle'] = 'invalid'
        with self.assertRaises(ValueError):
            predict_pcos(data_invalid)

    def test_feature_importance(self):
        """Test if feature importance can be retrieved"""
        importance = get_feature_importance()
        self.assertIsNotNone(importance)
        self.assertIsInstance(importance, dict)
        self.assertTrue(len(importance) > 0)
