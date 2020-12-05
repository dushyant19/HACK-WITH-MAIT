from django.urls import path

from . import views
app_name="parents"
urlpatterns = [
    path('',views.parent_index,name="parent_index"),
    path('gradecard/<pk>',views.grade_card,name="grade_card")
]
