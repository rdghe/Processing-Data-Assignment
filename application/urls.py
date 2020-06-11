from django.urls import path

from . import views

urlpatterns = [
    path('', views.grading_queue, name='grading queue'),
    path('', views.dedup_queue, name='de-duplication queue'),
]