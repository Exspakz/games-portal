from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('user_posts/', views.UserPostList.as_view(), name='user_posts'),
    path('user_posts_comments/', views.UserPostCommentList.as_view(), name='user_posts_comments'),
    path('accept_comment/<int:pk>/', views.accept_comment, name='accept_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='comment_delete'),
]