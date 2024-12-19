from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('processed/', views.processed_feedback_view, name='processed_feedback'),
    path('success/', views.success_view, name='success'),
]
