from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('sinup/', views.SinupView.as_view(), name="sinup"),
    path('sinup/active/<str:email>/<str:code>', views.ActiveAccountView.as_view(), name="active account"),
    path('forgetPassword/', views.ForegetPasswordView.as_view(), name="forget password"),
    path('forgetPassword/confirm/<str:email>/<str:code>', views.ConfirmForgetPasswordView.as_view(), name="confirm forget password"),
    path('logout', views.logout_view, name='logout'),
    path('user/profile/', views.ProfileView.as_view(),name="profile"),
    path('user/changePassword/', views.ChangePasswordView.as_view(),name="change password"),
    path('user/cart/', views.CartView.as_view(), name="cart view"),
    path('user/history', views.HistoryBuyView.as_view(), name="history buy"),
    path('about', TemplateView.as_view(template_name="ecommerce/about.html"), name="about")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)