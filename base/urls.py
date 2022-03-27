from django.urls import path, include
from .views import CustomLoginView, TaskList, TaskLists, ShareList, TaskDetail, ShareDetail, TaskCreate, ShareCreate, TaskUpdate, SuperTaskUpdate, OwnerTaskUpdate, ShareUpdate, SharingUpdate, TaskDeleteView, ShareDeleteView, CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view() ,name = 'login'),
    path('logout/', LogoutView.as_view(next_page = 'login') ,name = 'logout'),
    path('register/', RegisterPage.as_view() ,name = 'register'),
    path('', TaskList.as_view() ,name = 'tasks'),
    path('share/', TaskLists.as_view() ,name = 'taskss'),
    path('shares/', ShareList.as_view() ,name = 'shares'),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
    path('share/<int:pk>/', ShareDetail.as_view(), name = 'share'),
    path('task-create/', TaskCreate.as_view(), name = 'task-create'),
    path('share-create/', ShareCreate.as_view(), name = 'share-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name = 'task-update'),
    path('super-task-update/<int:pk>/', SuperTaskUpdate.as_view(), name = 'super-task-update'),
    path('owner-task-update/<int:pk>/', OwnerTaskUpdate.as_view(), name = 'owner-task-update'),
    path('share-update/<int:pk>/', ShareUpdate.as_view(), name = 'share-update'),
    path('sharing-update/<int:pk>/', SharingUpdate.as_view(), name = 'sharing-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name = 'task-delete'),
    path('share-delete/<int:pk>/', ShareDeleteView.as_view(), name = 'share-delete'),
    path('accounts/',include('allauth.urls')),
]