from django.contrib.auth import views as auth_views
from django.urls import include, path
from .views import RegisterView, profile, CustomLoginView
from .forms import LoginForm


# app_name = "account"

urlpatterns = [
    # path("home/", home, name="home"),
    # path(
    #     "login/",
    #     CustomLoginView.as_view(
    #         redirect_authenticated_user=True,
    #         template_name="registration/login.html",
    #         authentication_form=LoginForm,
    #     ),
    #     name="login",
    # ),
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
]
