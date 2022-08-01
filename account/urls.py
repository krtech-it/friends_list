from django.urls import path
from . import views
from django.contrib.auth.views import logout_then_login


urlpatterns = [
    path('', views.HomeCaseListView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path('profiles/list/', views.ProfileListView.as_view(), name='profile_list'),
    path('my_friends/', views.FriendsListView.as_view(), name='my_friends'),
    path('me_to_requests/', views.AcceptFriendsListView.as_view(), name='me_to_requests'),
    path('accept_friend_request/<int:requestID>/', views.AcceptFriendsListView.as_view(), name='accept_friend_request'),
    path('send_friend_request/<int:userID>/', views.ProfileListView.as_view(), name='send_friend_request'),
    path('delete_friend/<int:userID>/', views.FriendsListView.as_view(), name='delete_friend'),
    path('view_profile/<int:userID>/', views.ProfileDetailView.as_view(), name='detail_friend'),
    path('create_case/', views.CreateCaseView.as_view(), name='create_case'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete_case'),
    path('update_case/<int:pk>/', views.CaseUpdateView.as_view(), name='update_case'),
]
