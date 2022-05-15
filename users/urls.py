from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('enable-two-factor-auth/', views.EnableTwoFactorAuthenticationAPIView.as_view(), name='enable-two-factor-auth'),
    path('verify-two-factor-auth/', views.TwoFactorAuthTokenView.as_view(), name='verify-two-factor-auth'),
    path("login/", views.ObtainAuthTokenView.as_view(), name="login"),

]
