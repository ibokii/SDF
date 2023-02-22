from django.urls import path
from . import views


urlpatterns = [
	path('create-account/', views.CreateAccountView.as_view(), name='create_account'),
	path('login/', views.MyLoginView.as_view(template_name='registration/login.html'), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	# path('add-new-user-info/', views.AddUserInfoView.as_view(), name='add_new_user_info')
]
