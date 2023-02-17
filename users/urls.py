from django.urls import path
from . import views

app_user = 'users'
urlpatterns = [
    path('create/',views.CreateUserApiView.as_view(),name='create'),
    path('token/',views.CreateTokenView.as_view(),name='token'),
    path('<int:id>/',views.EditUserApiView.as_view(),name='edit'),
    path('get/<int:id>/',views.GetUserApiView.as_view(),name='detail')
]