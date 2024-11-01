from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import SMBExercise, ExLog, ExInfo 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User  
from django.db.models import Avg, Count
from django.db.models import Q
from django.db.models import Avg, Case, When 
from django.db.models import IntegerField
from django.http import JsonResponse

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

def instructor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and (user.is_staff or user.is_superuser):
            auth_login(request, user)
            return redirect('instructor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions. This login is for instructors only.')
            return redirect('instructor_login')
    
    return render(request, 'scoreboard/instructor_login.html')

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

@login_required
def details(request):
    exLogID = request.GET.get('exLogID')
    if exLogID:
        exercise_log = get_object_or_404(ExLog.objects.select_related('exName'), exLogID=exLogID)
        context = {
            'exName': exercise_log.exName.exName,
            'exDateTime': exercise_log.exDateTime,
            'exScore': exercise_log.exScore,
            'exCriteria1': exercise_log.exCriteria1,
            'exCriteria2': exercise_log.exCriteria2,
            'exCriteria3': exercise_log.exCriteria3,
            'exCriteria4': exercise_log.exCriteria4,
            'exCriteria5': exercise_log.exCriteria5,
            'exCriteria6': exercise_log.exCriteria6,
            'exCriteriaDesc1': exercise_log.exName.exCriteriaDesc1,
            'exCriteriaDesc2': exercise_log.exName.exCriteriaDesc2,
            'exCriteriaDesc3': exercise_log.exName.exCriteriaDesc3,
            'exCriteriaDesc4': exercise_log.exName.exCriteriaDesc4,
            'exCriteriaDesc5': exercise_log.exName.exCriteriaDesc5,
            'exCriteriaDesc6': exercise_log.exName.exCriteriaDesc6,
            'exComment': exercise_log.exComment,
        }
        return render(request, 'scoreboard/details.html', context)
    else:
        messages.error(request, 'No exercise ID provided')
        return redirect('dashboard')

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
    # Get all exercise records
    exercise_records = ExLog.objects.all().select_related('exName')

    # Apply search filters if provided
    student_search = request.GET.get('student_search', '')
    exercise_search = request.GET.get('exercise_search', '')

    if student_search:
        exercise_records = exercise_records.filter(
            Q(exPlayerName__icontains=student_search) |
            Q(exPlayerName__in=User.objects.filter(
                Q(first_name__icontains=student_search) |
                Q(last_name__icontains=student_search)
            ).values('username'))
        )

    if exercise_search:
        exercise_records = exercise_records.filter(exName__exName__icontains=exercise_search)

    # Calculate statistics
    total_students = User.objects.count()
    total_exercises = exercise_records.count()

    def calculate_average_score(records):
        total_score = 0
        total_records = 0
        for record in records:
            criteria_sum = sum([
                record.exCriteria1, record.exCriteria2, record.exCriteria3,
                record.exCriteria4, record.exCriteria5, record.exCriteria6
            ])
            total_score += criteria_sum * (100 / 60)  # Convert to percentage
            total_records += 1
        return total_score / total_records if total_records > 0 else 0

    average_score = calculate_average_score(exercise_records)

    # Get top performing students
    # top_students = User.objects.annotate(
    #     average_score=Avg(
    #         Case(
    #             When(exlog__exCriteria1=True, then=10),
    #             When(exlog__exCriteria2=True, then=10),
    #             When(exlog__exCriteria3=True, then=10),
    #             When(exlog__exCriteria4=True, then=10),
    #             When(exlog__exCriteria5=True, then=10),
    #             When(exlog__exCriteria6=True, then=10),
    #             default=0,
    #             output_field=IntegerField()
    #         )
    #     ),
    #     exercises_completed=Count('exlog')
    # ).order_by('-average_score')[:10]

    context = {
        'exercise_records': exercise_records,
        'total_students': total_students,
        'total_exercises': total_exercises,
        'average_score': average_score,
        # 'top_students': top_students,
        'student_search': student_search,
        'exercise_search': exercise_search,
    }

    return render(request, 'scoreboard/instructor_dashboard.html', context)

def instructor_details(request):
    exLogID = request.GET.get('exLogID')
    if exLogID:
        exercise = get_object_or_404(ExLog, exLogID=exLogID)
        exerciseInfo = get_object_or_404(ExInfo, exName=exercise.exName.exName)
        context = {
            'exLogID': exLogID,
            'exName': exercise.exName.exName,
            'exDateTime': exercise.exDateTime,
            'exScore': exercise.exScore,
            'exPlayerName': exercise.exPlayerName,
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
            'exComment': exercise.exComment if hasattr(exercise, 'exComment') else '',
        }
    else:
        context = {}
    return render(request, 'scoreboard/instructor_details.html', context)

def exercise_list(request):
    exInfo = ExInfo.objects.all()
    context = {
        'exInfo': exInfo,
    }
    return render(request, 'scoreboard/exercise_list.html', context)

def exercise_question(request):
    return render(request, 'scoreboard/exercise_question.html')

def instructor_logout(request):
    logout(request)
    return redirect('instructor_login')

def update_comment(request, log_id):
    if request.method == 'POST':
        try:
            exercise_log = ExLog.objects.get(exLogID=log_id)
            exercise_log.exComment = request.POST.get('instructor_comment', '')
            exercise_log.save()
            messages.success(request, 'Comment updated successfully')
            return JsonResponse({'status': 'success', 'message': 'Comment updated successfully'})
        except ExLog.DoesNotExist:
            messages.error(request, 'Exercise log not found')
            return JsonResponse({'status': 'error', 'message': 'Exercise log not found'})
        except Exception as e:
            messages.error(request, f'Error updating comment: {str(e)}')
            return JsonResponse({'status': 'error', 'message': f'Error updating comment: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)