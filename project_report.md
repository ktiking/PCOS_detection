# PCOS Detection System - Project Report

## Project Overview

The PCOS (Polycystic Ovary Syndrome) Detection System is a web application that uses machine learning to predict the likelihood of PCOS in patients based on various medical and demographic parameters. The system provides a user-friendly interface for healthcare professionals to input patient data and receive predictions along with relevant medical insights.

## Technical Architecture

The project consists of two main components:

1. **Data Science Pipeline**: A machine learning pipeline that processes the PCOS dataset, trains models, and selects the best performing one for deployment. This includes data preprocessing, feature engineering, model training, and evaluation.
2. **Web Application**: A Django-based web application that provides an interface for healthcare professionals to input patient data and view predictions.

## Data Science Pipeline

### Dataset

The project uses the PCOS dataset which contains various medical and demographic parameters including:

- Age
- BMI (Body Mass Index)
- Blood pressure
- Hormonal levels
- Menstrual cycle information
- Ultrasound results
- Other relevant medical parameters

### Data Preprocessing

The data preprocessing steps include:

1. Handling missing values
2. Feature scaling and normalization
3. Feature selection to identify the most relevant parameters
4. Data cleaning and validation

### Model Training

The system uses scikit-learn for model development, with the following components:

1. Feature selection using the saved `pcos_selected_features.pkl`
2. Model training and serialization using `pcos_model.pkl`
3. Model evaluation using standard metrics (accuracy, precision, recall, F1-score)

## Web Application

### Technology Stack

- **Backend**: Django 5.0.2
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL (using mysqlclient)
- **Machine Learning**: scikit-learn 1.3.0
- **Image Processing**: Pillow
- **Environment Management**: python-dotenv

### Key Features

1. **User Authentication**: Secure login system for healthcare professionals
2. **Patient Data Input**: Form for entering patient medical parameters
3. **Prediction Results**: Display of PCOS prediction with confidence level
4. **Medical Insights**: Additional medical information and recommendations
5. **Patient History**: Tracking of previous predictions and results
6. **Responsive Design**: Mobile-friendly interface

### Application Structure

The Django application follows the MVT (Model-View-Template) architecture:

- **Models**: Define database schema for patient data and predictions
- **Views**: Handle HTTP requests, process form data, and interact with the ML model
- **Templates**: HTML files for the user interface
- **Model Utils**: Custom utilities for ML model integration (`model_utils.py`)

## Implementation Details

### Models

The application uses several models to store:
1. Patient information
2. Medical parameters
3. Prediction results
4. User authentication data

### Prediction Process

When a healthcare professional submits patient data:

1. The form data is validated and processed
2. The ML model is loaded and used to make predictions
3. Results are saved to the database
4. The user is presented with the prediction and relevant medical insights

## Deployment Instructions

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables
5. Configure MySQL database
6. Run migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`


## Conclusion

The PCOS Detection System demonstrates the practical application of machine learning in healthcare. By combining medical expertise with advanced data science techniques, the system provides valuable insights to healthcare professionals in diagnosing PCOS. The project showcases the successful integration of machine learning with web development, creating a tool that can potentially improve healthcare outcomes.
