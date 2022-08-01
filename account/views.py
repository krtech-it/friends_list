from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .forms import CreateUserForm
from .models import Profile, Friend_Request, Case
from .utils import FriendRequiredMixin, CheckUserCaseMixin


class RegisterView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')


class AccountLoginView(LoginView):
    model = User
    template_name = 'account/login.html'


class AccountLogoutView(LogoutView):
    pass


# # @login_required
# def home_page(request):
#     return render(request, 'account/home.html')

class HomeCaseListView(ListView):
    template_name = 'account/home.html'
    context_object_name = 'cases'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.request.user.profile.cases.all()
            return queryset


def delete_case(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.user.profile.id == case.profile.id:
        case.delete()
    return redirect('home')


class CaseUpdateView(CheckUserCaseMixin, UpdateView):
    model = Case
    fields = ('title', 'description', 'deadline')
    template_name = 'account/update_case.html'
    success_url = reverse_lazy('home')
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        if self.check_user_case(request):
            return super().get(request, *args, **kwargs)
        return redirect('login')



class CreateCaseView(CreateView):
    template_name = 'account/create_case.html'
    model = Case
    fields = ('title', 'description', 'deadline')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object = form.save()
        return super().form_valid(form)




class ProfileDetailView(LoginRequiredMixin, FriendRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile_detail.html'
    pk_url_kwarg = 'userID'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'userID' in self.kwargs.keys():
            is_friend = self.get_user_context(self.request, userID=self.kwargs['userID'])
            context['is_friend'] = is_friend
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    template_name = 'account/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profile.objects.exclude(user=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        my_friends = list(self.request.user.profile.friends.all())
        profile = self.request.user.profile
        my_orders = list(Friend_Request.objects.filter(from_user=profile).values_list('to_user', flat=True))
        context['my_friends'] = my_friends
        context['my_orders'] = my_orders
        return context

    def get(self, request, *args, **kwargs):
        if 'userID' in kwargs.keys():
            from_user = request.user.profile
            to_user = Profile.objects.get(id=kwargs['userID'])
            friend_request, created = Friend_Request.objects.get_or_create(
                from_user=from_user, to_user=to_user)
            # if created:
            #     return redirect('profile_list')
            # else:
            #     return redirect('my_friends')
        return super().get(self, request, *args, **kwargs)


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'account/friends_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        queryset = self.request.user.profile.friends.all()
        return queryset

    def get(self, request, *args, **kwargs):
        if 'userID' in kwargs.keys():
            friends_list = self.request.user.profile.friends.values_list('id', flat=True)
            if kwargs['userID'] in friends_list:
                self.request.user.profile.friends.remove(kwargs['userID'])
                Profile.objects.get(id=kwargs['userID']).friends.remove(self.request.user.profile.id)
        return super().get(self, request, *args, **kwargs)



class AcceptFriendsListView(LoginRequiredMixin, ListView):
    template_name = 'account/accept_friends_list.html'
    context_object_name = 'requests_list'

    def get_queryset(self):
        queryset = Friend_Request.objects.filter(to_user=self.request.user.profile)
        return queryset

    def get(self, request, *args, **kwargs):
        if "requestID" in kwargs.keys():
            friend_request = Friend_Request.objects.get(id=kwargs['requestID'])
            if friend_request.to_user == request.user.profile:
                friend_request.to_user.friends.add(friend_request.from_user)
                friend_request.from_user.friends.add(friend_request.to_user)
                to_user, from_user = friend_request.to_user, friend_request.from_user
                friend_request.delete()
                try:
                    friend_request_1 = Friend_Request.objects.get(from_user=from_user, to_user=to_user)
                except ObjectDoesNotExist:
                    friend_request_1 = None
                try:
                    friend_request_2 = Friend_Request.objects.get(from_user=to_user, to_user=from_user)
                except ObjectDoesNotExist:
                    friend_request_2 = None
                if friend_request_1 or friend_request_2:
                    try:
                        friend_request_1.delete()
                    except ValueError:
                        friend_request_2.delete()
        return super().get(self, request, *args, **kwargs)
