from django.urls import path  # type: ignore
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('my-projects/', views.MyProjectsView.as_view(), name='projects'),
    path('my-projects/<int:project_id>/board/', views.BoarsView.as_view(), name='board'),
    path('create-project/', views.CreateProjectView.as_view(), name='create_project'),
]
