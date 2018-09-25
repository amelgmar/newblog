from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListPost.as_view(), name='post_list'),
    path('post/<int:pk>/', views.DetailPost.as_view(), name='post_detail'),
    path('post/new/', views.NewPost.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.EditPost.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', views.DeletePost.as_view(), name='post_delete'),
]
