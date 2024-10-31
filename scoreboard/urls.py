from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.scoreboard_home, name='scoreboard_home'),
    path('dummyscore/', views.dummy_score, name='dummy_score'),
    path('redirect/', views.redirect_view, name='redirect'),
    path('redirect2/', views.redirect2_view, name='redirect2'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('details/', views.details, name='details'),
    path('signup/', views.signup, name='signup'), 
    path('instructor-login/', views.instructor_login, name='instructor_login'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor-details/', views.instructor_details, name='instructor_details'),
    path('exercise-list/', views.exercise_list, name='exercise_list'),
    path('exercise-question/', views.exercise_question, name='exercise_question'),
    path('instructor/logout/', views.instructor_logout, name='instructor_logout'),
]