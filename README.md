# PCOS Detection System
A Django-based system for PCOS (Polycystic Ovary Syndrome) detection.
This project aims to benefit in clinical environments by providing quick, data-driven assessments that support early diagnosis. By analyzing patient health metrics, the system assists healthcare professionals in identifying potential PCOS cases more efficiently, reducing diagnostic delays, and enabling timely interventions—ultimately improving patient outcomes and streamlining clinical workflows.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL database in XAMPP:
- Start XAMPP and ensure MySQL service is running
- Create a new database named 'pcos_detection'

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Features
- User authentication
- PCOS detection system
- Patient management
- Medical history tracking
- Results analysis 
