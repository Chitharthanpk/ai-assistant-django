from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Chat
    path('chat/', views.chat_page, name='chat_page'),
    path('chat/api/', views.chat_api, name='chat_api'),

    # Google OAuth (Single flow)
    path('oauth/google/start/', views.google_auth_start, name='google_auth_start'),
    path('oauth/google/callback/', views.google_auth_callback, name='google_auth_callback'),

    path('calendar/events/', views.get_calendar_events, name='get_calendar_events'),

]
