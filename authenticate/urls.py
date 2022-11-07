from django.urls import path, include
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/user/', RegisterView.as_view(), name='update'),
    path('api/user/currentUserData', RegisterView.as_view(), name='current user'),
    # path('api/user-group/', UserGroupView.as_view(), name='user_group'),

    # path('api/buyer/', BuyerAggView.as_view(), name='buyer'),

]