
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView,UpdateView,ListView
from django.contrib.auth import login,logout,authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View



from accounts.forms import LoginForm, OrderUpdateForm, RegisterForm, UserUpdateForm
from accounts.mixin import LoginMixin
from accounts.models import User
from core.models import Car
from orders.models import Order
# Create your views here.




class AdminDashboardView(LoginMixin,View):
    template_name = 'accounts/admin/dashboard.html'
    
    def get(self,request,*args, **kwargs):
        
        context = {
            'user':User.objects.all().count(),
            'order':Order.objects.all().count(),
            'car':Car.objects.all().count()
        }
        return render(request,self.template_name,context)



class AdminCarListdView(LoginMixin,ListView):
    model = Car
    template_name = 'accounts/admin/car_list.html'
    context_object_name=  'cars'
    paginate_by = 10


class AdminOrderUpdateView(LoginMixin,UpdateView):
    model = Order
    template_name = 'accounts/admin/edit_order.html'
    form_class = OrderUpdateForm
    success_url = reverse_lazy('admin_order')


class AdminOrderListdView(LoginMixin,ListView):
    model = Order
    template_name = 'accounts/admin/order_list.html'
    context_object_name=  'orders'
    paginate_by = 10

class UserProfileView(LoginMixin,UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    form_class = UserUpdateForm
    pk_url_kwarg = 'pk'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user'] = User.objects.get(id=self.kwargs.get('pk'))
        return context
    
    
    def form_valid(self, form):
        print('form data')
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print('form error')
        print(form.cleaned_data)
        return super().form_invalid(form)


class UserCreateView(SuccessMessageMixin,CreateView):
    model = User
    template_name = "accounts/registration.html"
    form_class = RegisterForm
    success_message = "User Create successfully now you can login"


class UserLoginView(View):
    tamplates_name = 'accounts/login.html'
    def get(self,request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated:
            if user.is_staff and user.is_superuser:
                return redirect(reverse_lazy('admin_dashboard', kwargs={'pk':user.id}))
            return redirect(reverse_lazy('home'))
        return render(request,self.tamplates_name,{'form':LoginForm(request=request)})
    
    def post(self,request, *args, **kwargs):
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if user.is_staff and user.is_superuser:
                    return redirect(reverse_lazy('admin_dashboard', kwargs={'pk':user.id}))
                return redirect(reverse_lazy('home'))
        
        return render(request,self.tamplates_name,{'form':form})

class LogoutView(LogoutView):
    def get_success_url(self,*args, **kwargs):
        return reverse_lazy('home')
    


class UserOrderListdView(LoginMixin,ListView):
    model = Order
    template_name = 'accounts/user/order_list.html'
    context_object_name=  'orders'
    paginate_by = 10


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

