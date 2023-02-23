from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.http import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# Create your views here.
class TripsList(DataMixin, ListView):
    model = Trip
    template_name = 'main/trips.html'
    context_object_name = 'trips'
    #form = SearchTripForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Поездки")
        return dict(list(context.items()) + list(c_def.items()))

    #def get_queryset(self):
    #    return Trip.objects.filter(from_city=f, to_city=t, date=d)


def index(request):
    return render(request, 'main/index.html')


class AddInfo(LoginRequiredMixin, DataMixin, CreateView):
    form_class = RedInfoForm
    template_name = 'main/red_info.html'
    login_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Редактирование профиля")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        inf = UserInfo.objects.get(user=self.request.user)
        inf.info = form.cleaned_data.get('info')
        inf.photo = self.request.FILES['photo']
        #print(self.request.FILES['photo'])
        inf.save()
        print(inf.user, inf.info, inf.photo)
        return redirect('home')


class ShowTrip(DataMixin, DetailView):
    model = Trip
    template_name = 'main/show_trip.html'
    pk_url_kwarg = 'trip_id'
    context_object_name = 'trip'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Поездка")
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, pk=trip_id)
        form = BookForm()
        action = self.request.POST.get("book")
        if action == 'book':
            trip.passangers.add(self.request.user)
            trip.capacity-=1
            trip.save()
        if action == 'unbook':
            trip.passangers.remove(self.request.user)
            trip.capacity+=1
            trip.save()
        return redirect(trip.get_absolute_url())


class ShowProfile(DataMixin, DetailView):
    model = UserInfo
    template_name = 'main/show_profile.html'
    pk_url_kwarg = 'profile_id'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Профиль")
        return dict(list(context.items()) + list(c_def.items()))


class AddTrip(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTripForm
    template_name = 'main/add_trip.html'
    login_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Создание поездки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        #trip = Trip(driver=self.request.user)
        trip = form.save(commit=False)
        trip.driver = self.request.user
        trip.save()
        return redirect(trip.get_absolute_url())


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        UserInfo.objects.create(user=user)
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contex(title="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
