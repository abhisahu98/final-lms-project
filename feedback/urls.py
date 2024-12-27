from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),  # Root URL renders the feedback form
    path('success/', views.success_view, name='success'),
    path('chatgpt/<int:feedback_id>/', views.chatgpt_interaction, name='chatgpt_interaction'),
]
