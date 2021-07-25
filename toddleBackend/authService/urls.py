from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    # path('login/',views.Login.as_view()),
    path('signup/',views.Signup.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]