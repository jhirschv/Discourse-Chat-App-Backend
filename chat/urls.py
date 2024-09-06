from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (UserViewSet)
from .views import (UserViewSet, UserRegistrationView, UserDeleteAPIView, UserChatSessionsView,ChatSessionViewSet)
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chat_sessions', ChatSessionViewSet, basename='chat_session')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/<int:other_user_id>/', views.ChatSessionMessageViewSet.as_view({'get': 'retrieve_or_create_session_get_messages'}), name='chat-session', ),
    path('user_chats/', UserChatSessionsView.as_view(), name='user_chats'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('delete-account/', UserDeleteAPIView.as_view(), name='delete-account'),
]
