from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from article.models import Article, Comment
from authapp.forms import UserRegisterForm, UserAuthenticationForm, UserEditForm, UserProfileEditForm
from authapp.models import User, UserProfile
from django.db import transaction

from notification.models import Notification


class UserLogin(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'authapp/login.html'


class UserLogout(LogoutView):
    next_page = '/'


class RegisterUserView(CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    success_msg = 'Пользователь успешно создан'


class ProfileView(UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserEditForm

    success_msg = 'Профиль успешно изменен'

    def get_user_profile(request, username):
        user = User.objects.get(username=username)
        return render(request, 'authapp/user_profile.html', {"user": user})

    def get_success_url(self):
        return reverse_lazy('authapp:profile', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.get_user_articles(self.request.user)
        context['notices'] = Notification.get_all(self.request.user)
        if self.request.POST:
            context['profile_form'] = UserProfileEditForm(self.request.POST, instance=self.request.user.userprofile)
        else:
            context['profile_form'] = UserProfileEditForm(instance=self.request.user.userprofile)
        print('get_context_data', context)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = UserEditForm(request.POST, request.FILES, instance=request.user)

        profile_form = UserProfileEditForm(self.request.POST, instance=self.request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            print(form.errors)
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        """
        Called if all forms are valid. Creates a Author instance along
        with associated books and then redirects to a success page.
        """
        self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_form):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )


class UserInfoView(DetailView):
    model = User
    template_name = 'authapp/user_profile.html'

    # def get_queryset(self):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_info'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user_profile'] = get_object_or_404(UserProfile, user=self.kwargs['pk'])
        context['comments_count'] = Comment.objects.filter(user=self.kwargs['pk']).count()
        context['article_count'] = Article.objects.filter(user=self.kwargs['pk']).count()
        return context


@login_required
def moderation(request):
    context = {
        'articles': Article.get_moderated_articles()
    }
    return render(request, 'authapp/moderation.html', context)

# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('authapp:profile'))
#     else:
#         form = UserEditForm(instance=request.user)
#
#     context = {
#         'form': form,
#         'articles': Article.get_user_articles(request.user)
#     }
#     return render(request, 'authapp/profile.html', context)


# @transaction.atomic
# def edit(request):
#     title = 'редактирование'
#     if request.method == 'POST':
#         edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
#         profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
#         if edit_form.is_valid() and profile_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('authapp:edit'))
#     else:
#         edit_form = UserEditForm(instance=request.user)
#         profile_form = UserProfileEditForm(instance=request.user.userprofile)
#     content = {
#         'title': title,
#         'edit_form': edit_form,
#         'profile_form': profile_form
#     }
#     return render(request, 'authapp/edit.html', content)
