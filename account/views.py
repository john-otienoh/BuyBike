from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Address
from .forms import AddressForm, RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from orders.models import Order
from wishlist.models import Wishlist

class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, self.template_name, {'form': RegisterForm()})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to BuyBike, {user.username}! Your account is ready ")
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, self.template_name, {'form': LoginForm()})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = authenticate(
                request, username=identifier, password=password
            )

            if user is None:
                try:
                    uname = User.objects.get(email__iexact=identifier).username
                    user = authenticate(request, username=uname, password=password)
                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                messages.success(request, f'Welcome Back, {user.username}')
                next_url = request.GET.get('next', 'home:home')

                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid Username or password')

        return render(request, self.template_name, {'form': form})
    
class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You've been logged out.")
        return redirect('home:home')

class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        recent_orders = Order.objects.filter(user=request.user).order_by('-created_by')[:5]
        wishlist_count = 0
        try:
            wishlist_count = Wishlist.objects.get(user=request.user).products.count()
        except Wishlist.DoesNotExist:
            pass
        return render(request, 'account/dashboard.html', {
            'recent_orders': recent_orders,
            'wishlist_count': wishlist_count,
        })

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {
            'user_form': UserUpdateForm(instance=request.user),
            'profile_form': ProfileUpdateForm(instance=profile),
        })
    
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user.request.user)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=profile)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated Successfully')
            return redirect('account:profile')

        return render(request, self.template_name,{
            'user_form': user_form,
            'profile_form': profile_form,
        })

class AddressListView(LoginRequiredMixin, View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'account/addresses.html', {'addresses': addresses})
    
class AddressCreateView(LoginRequiredMixin, View):
    template_name = 'account/address_form.html'
    def get(self, request):
        return render(request, self.template_name, {'form': AddressForm(), 'action': 'Add'})
    
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            messages.success(request, "Address saved.")
            return redirect('account:address_list')
        return render(request, self.template_name, {'form': form, 'action': 'Add'})

class AddressUpdateView(LoginRequiredMixin, View):
    template_name = 'account/address_form.html'

    def get(self, request, pk):
        addr = get_object_or_404(Address, pk=pk, user=request.user)
        return render(request, self.template_name, {'form': AddressForm(instance=addr), 'action': 'Edit'})
    def post(self, request, pk):
        addr = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated.")
            return redirect('account:address_list')
        return render(request, self.template_name, {'form': form, 'action': 'Edit'})

class AddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        addr = get_object_or_404(Address, pk=pk, user=request.user)
        addr.delete()
        messages.success(request, "Address deleted.")
        return redirect('account:address_list')

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'account/change_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': PasswordChangeForm(request.user)})
    
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, "Password changed successfully.")
            return redirect('account:account')
        return render(request, self.template_name, {'form': form})
    