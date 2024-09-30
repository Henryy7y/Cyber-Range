from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import SMBExercise, ExLog, ExInfo  # Add this import
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User  # Add this import

def scoreboard_home(request):
    return render(request, 'scoreboard/home.html')

@login_required
def dummy_score(request):
    exercises = SMBExercise.objects.filter(exPlayer=request.user.username)
    return render(request, 'scoreboard/dummy_score.html', {'exercises': exercises, 'user': request.user})

@login_required
def dashboard_view(request):
    ex_logs = ExLog.objects.filter(exPlayerName=request.user.username)
    total_score = sum(ex_log.exScore for ex_log in ex_logs)
    return render(request, 'scoreboard/dashboard.html', {'user': request.user, 'exercises': ex_logs, 'total_score': total_score})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to redirect2 view after successful login, return redirect('dummy_score')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'scoreboard/login2.html')

def redirect_view(request):
    exercise_name = request.GET.get('exercise', '')
    return render(request, 'scoreboard/redirect.html', {'exercise_name': exercise_name})

def redirect2_view(request):
    context = {
        'exName': request.GET.get('exName', ''),
        'exDate': request.GET.get('exDate', ''),
        'exScore': request.GET.get('exScore', ''),
        'exCriteria1': request.GET.get('exCriteria1', ''),
        'exCriteria2': request.GET.get('exCriteria2', ''),
        'exCriteria3': request.GET.get('exCriteria3', ''),
        'exCriteria4': request.GET.get('exCriteria4', ''),
        'exCriteria5': request.GET.get('exCriteria5', ''),
        'exCriteria6': request.GET.get('exCriteria6', ''),
    }
    return render(request, 'scoreboard/redirect2.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def profile(request):
    return render(request, 'scoreboard/profile.html', {'user': request.user})

@login_required
def profile_view(request):
    return render(request, 'scoreboard/profile.html')

def details(request):
    exLogID = request.GET.get('exLogID')
    if exLogID:
        exercise = get_object_or_404(ExLog, exLogID=exLogID)
        exerciseInfo = get_object_or_404(ExInfo, exName=exercise.exName)
        context = {
            'exName': exercise.exName,
            'exDateTime': exercise.exDateTime.strftime("%Y-%m-%d %H:%M:%S"),
            'exScore': exercise.exScore,
            'exCriteria1': exercise.exCriteria1,
            'exCriteria2': exercise.exCriteria2,
            'exCriteria3': exercise.exCriteria3,
            'exCriteria4': exercise.exCriteria4,
            'exCriteria5': exercise.exCriteria5,
            'exCriteria6': exercise.exCriteria6,
            'exCriteriaDesc1': exerciseInfo.exCriteriaDesc1,
            'exCriteriaDesc2': exerciseInfo.exCriteriaDesc2,
            'exCriteriaDesc3': exerciseInfo.exCriteriaDesc3,
            'exCriteriaDesc4': exerciseInfo.exCriteriaDesc4,
            'exCriteriaDesc5': exerciseInfo.exCriteriaDesc5,
            'exCriteriaDesc6': exerciseInfo.exCriteriaDesc6,
        }
    else:
        context = {}
    return render(request, 'scoreboard/details.html', context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        
        # Create a new User instance
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)  # Set the password
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')  # Redirect to the login page after signup

    return render(request, 'scoreboard/signup.html')

def instructor_dashboard(request):
    return render(request, 'scoreboard/instructor_dashboard.html')

def instructor_details(request):
    return render(request, 'scoreboard/instructor_details.html')

def exercise_list(request):
    return render(request, 'scoreboard/exercise_list.html')

def exercise_question(request):
    return render(request, 'scoreboard/exercise_question.html')

