from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tips/<int:tip_id>/upvote/', views.upvote, name='upvote'),
    path('tips/<int:tip_id>/downvote/', views.downvote, name='downvote'),
    path('tips/<int:tip_id>/delete/', views.delete_tip, name='delete_tip'),
]
