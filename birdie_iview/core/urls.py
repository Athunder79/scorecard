from django.urls import path, include
from .views import ScoreListView, find_golf_courses, start_round, scorecard, hole_details
from . import views


urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/<int:hole_id>/', scorecard,  name='scorecard'),
    path('find-golf-courses/', find_golf_courses, name='find-golf-courses'),
    path('start-round/', start_round, name='start-round'),
    path('hole-details/<int:course_id>/<int:round_id>/', hole_details, name='hole-details'),
    path('hole-details/<int:course_id>/<int:round_id>/<int:hole_id>/next/', views.next_hole, name='next-hole'),
    path('map-shots',views.mapshots, name='map-shots'),
    path('rounds/', ScoreListView.as_view(), name='rounds'),
    path('finish-round/<int:round_id>/', views.finish_round, name='finish-round'),
    path('end-of-shot/<int:course_id>/<int:round_id>/<int:hole_id>/', views.end_of_shot, name='end-of-shot'),


    
]

