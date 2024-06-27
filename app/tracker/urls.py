from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('trackers/', views.TrackerList.as_view(), name='list_trackers'),
    path('create/', views.TrackerCreateView.as_view(), name='create_tracker'),
    path('update/<int:pk>/', views.TrackerUpdateView.as_view(), name='update_tracker'),
    path('delete_creature/<int:pk>/', views.delete_creature, name='delete_creature'),
    path('run/<int:pk>/', views.RunView.as_view(), name='run')
]
