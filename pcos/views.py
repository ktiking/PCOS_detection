from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Prediction
from django.db.models import Count, Avg
from django.db.models.functions import Round
import numpy as np

def login_view(request):
    # if they're already logged in, send them home
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # try to find the user and check their password
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home')
        except User.DoesNotExist:
            pass
            
        messages.error(request, 'Invalid email or password.')
    
    return render(request, 'pcos/login.html')

def signup_view(request):
    # if they're already logged in, send them home
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # make sure the password is long enough
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'pcos/signup.html')
        
        # check if someone's already using this email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'pcos/signup.html')
        
        # make a username from their email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # create their account
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # split their name into first and last
        name_parts = name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.save()
        
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    
    return render(request, 'pcos/signup.html')

@login_required
def home_view(request):
    return render(request, 'pcos/home.html')

@login_required
def prediction_form_view(request):
    if request.method == 'POST':
        try:
            # grab all the info they entered
            data = {
                'age': float(request.POST.get('age')),
                'weight': float(request.POST.get('weight')),
                'bmi': float(request.POST.get('bmi')),
                'cycle': request.POST.get('cycle'),
                'cycle_length': float(request.POST.get('cycle_length')),
                'lh_fsh_ratio': float(request.POST.get('lh_fsh_ratio')),
                'weight_gain': request.POST.get('weight_gain'),
                'hair_growth': request.POST.get('hair_growth'),
                'follicle_no_l': float(request.POST.get('follicle_no_l')),
                'follicle_no_r': float(request.POST.get('follicle_no_r')),
                'hip': float(request.POST.get('hip')),
                'skin_darkening': request.POST.get('skin_darkening'),
                'lifestyle_score': float(request.POST.get('lifestyle_score'))
            }
            
            # count up their symptoms and total follicles
            data['symptom_count'] = sum(1 for x in [data['weight_gain'], data['hair_growth'], data['skin_darkening']] if x == 'Y')
            data['total_follicle_count'] = data['follicle_no_l'] + data['follicle_no_r']
            
            # use our model to make a prediction
            from pcos_detection.model_utils import predict_pcos
            prediction_result = predict_pcos(data)
            
            # save everything to the database
            prediction = Prediction.objects.create(
                user=request.user,
                age=data['age'],
                weight=data['weight'],
                bmi=data['bmi'],
                cycle=data['cycle'],
                cycle_length=data['cycle_length'],
                lh_fsh_ratio=data['lh_fsh_ratio'],
                weight_gain=data['weight_gain'],
                hair_growth=data['hair_growth'],
                follicle_no_l=data['follicle_no_l'],
                follicle_no_r=data['follicle_no_r'],
                hip=data['hip'],
                skin_darkening=data['skin_darkening'],
                lifestyle_score=data['lifestyle_score'],
                prediction=prediction_result['prediction'],
                probability=prediction_result['probability']
            )
            
            return render(request, 'pcos/prediction_result.html', {'prediction': prediction})
            
        except Exception as e:
            messages.error(request, f'Error making prediction: {str(e)}')
    
    return render(request, 'pcos/prediction_form.html')

@login_required
def statistics_view(request):
    # get some basic numbers
    total_predictions = Prediction.objects.count()
    high_risk_count = Prediction.objects.filter(prediction=1).count()
    low_risk_count = Prediction.objects.filter(prediction=0).count()
    high_risk_percentage = round((high_risk_count / total_predictions * 100) if total_predictions > 0 else 0, 2)
    avg_probability = round(Prediction.objects.aggregate(Avg('probability'))['probability__avg'] or 0, 2)
    
    # figure out how many people are in each age group
    age_ranges = [(0, 20), (21, 30), (31, 40), (41, 50), (51, 100)]
    age_labels = ['0-20', '21-30', '31-40', '41-50', '51+']
    age_data = []
    
    for min_age, max_age in age_ranges:
        count = Prediction.objects.filter(age__gte=min_age, age__lte=max_age).count()
        age_data.append(count)
    
    # same thing for BMI groups
    bmi_ranges = [(0, 18.5), (18.5, 25), (25, 30), (30, 100)]
    bmi_data = []
    
    for min_bmi, max_bmi in bmi_ranges:
        count = Prediction.objects.filter(bmi__gte=min_bmi, bmi__lt=max_bmi).count()
        bmi_data.append(count)
    
    # check how common each symptom is
    total = Prediction.objects.count()
    symptoms_data = [
        round(Prediction.objects.filter(weight_gain='Y').count() / total * 100 if total > 0 else 0, 2),
        round(Prediction.objects.filter(hair_growth='Y').count() / total * 100 if total > 0 else 0, 2),
        round(Prediction.objects.filter(skin_darkening='Y').count() / total * 100 if total > 0 else 0, 2)
    ]
    
    # put all the numbers together for the template
    context = {
        'total_predictions': total_predictions,
        'high_risk_count': high_risk_count,
        'low_risk_count': low_risk_count,
        'high_risk_percentage': high_risk_percentage,
        'avg_probability': avg_probability,
        'age_labels': age_labels,
        'age_data': age_data,
        'bmi_data': bmi_data,
        'symptoms_data': symptoms_data
    }
    
    return render(request, 'pcos/statistics.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')
