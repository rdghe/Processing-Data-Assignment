from django.urls import path

from . import views

urlpatterns = [
    path('grading_queue/', views.grading_queue, name='grading queue'),
    path('dedup_queue/', views.dedup_queue, name='de-duplication queue'),
    path('poison_queue/', views.poison_queue, name='poison queue'),
]
