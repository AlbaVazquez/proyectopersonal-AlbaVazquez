from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('artworks/', views.ArtworkList.as_view(), name='artwork_list'),
    path('artworks/create/', views.ArtworkCreate.as_view(), name='artwork_create'),
    path('artworks/<int:pk>/', views.ArtworkDetail.as_view(), name='artwork_detail'),
    path('artworks/<int:pk>/edit/', views.ArtworkUpdate.as_view(), name='artwork_update'),
    path('artworks/<int:pk>/delete', views.ArtworkDelete.as_view(), name='artwork_delete'),
    path('artworks/<int:pk>/comment/', views.add_private_comment, name='add_private_comment'),
    path('challenges/create/', views.ChallengeCreate.as_view(), name='challenge_create'),
    path('challenges/<int:pk>/complete/', views.challenge_complete, name='challenge_complete'),
    path('comments/<int:pk>/delete/', views.delete_private_comment, name='delete_private_comment'),
    path('stats/', views.GlobalStatsView.as_view(), name='global_stats'),
]