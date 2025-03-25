from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogPostListView.as_view(), name='blogs'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blog/create/', views.BlogPostCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/create/', views.add_comment, name='comment-create'),
] 