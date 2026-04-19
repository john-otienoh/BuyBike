from django.contrib.auth import views as auth_views
from django.urls import include, path
from .views import RegisterView, profile, CustomLoginView
from .forms import LoginForm


app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('account/', views.AccountView.as_view(), name='account'),
    path('account/profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('account/addresses/', views.AddressListView.as_view(), name='address_list'),
    path('account/addresses/add/', views.AddressCreateView.as_view(), name='address_create'),
    path('account/addresses/<int:pk>/edit/', views.AddressUpdateView.as_view(), name='address_update'),
    path('account/addresses/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
    path('account/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
