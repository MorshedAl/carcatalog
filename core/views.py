
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    TemplateView,UpdateView, DetailView, 
    CreateView,ListView,DeleteView
)
from accounts.mixin import LoginMixin

from core.forms import CarCreateForm

from core.models import Car

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['recent_list'] = Car.objects.all()[:3]

        return context


class CarListView(ListView):
    model = Car
    template_name = "core/car_list.html"
    context_object_name = 'cars'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['brand'] = self.model.objects.values('brand')
        
        
        context.update({
            'brand_list':set([b.get('brand') for b in self.model.objects.values('brand')]),
            'model_list' : set([b.get('modal') for b in self.model.objects.values('modal')])
        })
        return context

    


class CarDetailView(DetailView):
    model = Car
    template_name = "core/car_detail.html"
    context_object_name = 'car'
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'
    slug_field = 'slug'


class CarCreateView(LoginMixin,CreateView):
    model = Car
    template_name = "core/create_car.html"
    form_class = CarCreateForm
    success_url = reverse_lazy('car_list')


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title)
        car = form.save()
        # messages.success(self.request,'car added successfully')
        return super().form_valid(form)


class CarUpdateView(LoginMixin,UpdateView):
    model = Car
    template_name = "core/create_car.html"
    form_class = CarCreateForm
    success_url = reverse_lazy('admin_car')


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title)
        car = form.save()
        # messages.success(self.request,'car added successfully')
        return super().form_valid(form)


class CarDeleteView(LoginMixin,DeleteView):
    model = Car
    template_name = "core/delete_car.html"
    success_url = reverse_lazy('admin_car')
