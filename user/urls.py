from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('sinup/', views.SinupView.as_view(), name="sinup"),
    path('sinup/active/<str:email>/<str:code>', views.ActiveAccountView.as_view(), name="active account"),
    path('forgetPassword/', views.ForegetPasswordView.as_view(), name="forget password"),
    path('forgetPassword/confirm/<str:email>/<str:code>', views.ConfirmForgetPasswordView.as_view(), name="confirm forget password"),
    path('logout', views.logout_view, name='logout'),
    path('user/profile/', views.ProfileView.as_view(),name="profile"),
    path('user/changePassword/', views.ChangePasswordView.as_view(),name="change password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)