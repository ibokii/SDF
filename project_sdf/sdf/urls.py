from django.urls import path  # type: ignore
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('my-projects/', views.MyProjectsView.as_view(), name='projects'),
    path('my-projects/<int:project_id>/board/', views.BoarsView.as_view(), name='board'),
    path('my-projects/edit/<int:project_id>', views.EditProjectView.as_view(), name='edit_project'),
    path('my-projects/edit/delete-project/<int:project_id>', views.delete_project, name='delete_project'),
]
