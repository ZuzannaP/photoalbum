from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView
from django.views.generic.base import View

from album_photo.forms import AddPhotoForm, EditPhotoForm,  LoginForm, CustomUserChangeForm, CommentCreationForm
from album_photo.models import Photo, Comment


# user functionality

class LoginView(FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = "login.html"

    def form_valid(self, form: LoginForm):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)

        if user is None:
            form.add_error(None, "Incorrect login or password")
            return super().form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        ctx = {}
        logout(request)
        if request.user.is_authenticated:
            ctx["my_verdict"] = "Ups. Something went wrong."
        else:
            ctx["my_verdict"] = "You have been logged out"
        return render(request, "logout.html", ctx)


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created. Welcome on board!'
    template_name = 'signup.html'


def account_settings(request):
    return render(request, "account_settings_tmp.html")


class EditPersonalInfoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('view_photos')
    success_message = "Your personal data has been succesfully changed!"
    template_name = 'account_edit_personal_info.html'

    def get_object(self):
        return self.request.user


class DeleteAccountView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'account_confirm_delete.html'
    model = User
    success_url = reverse_lazy("view_photos")
    success_message = "Your account has been deleted"

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'password_change_done.html'


# photos functionality

class AddPhoto(LoginRequiredMixin, View):

    def get(self, request):
        form = AddPhotoForm()
        ctx = {"form": form}
        return render(request, "add_photo_tmp.html", ctx)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            path = form.cleaned_data["path"]
            description = form.cleaned_data["description"]
            photo = Photo.objects.create(path=path, owner=request.user, description=description)
            messages.success(request, 'Photo successfully uploaded')
            return redirect(f"/photo/{photo.pk}/")
        ctx = {"form": form}
        return render(request, "add_photo_tmp.html", ctx)


class EditPhoto(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        if photo.owner != request.user:
            raise PermissionDenied
        else:
            form = EditPhotoForm()
            ctx = {"form": form, "photo": photo}
            return render(request, "edit_photo_tmp.html", ctx)

    def post(self, request, photo_id):
        form = EditPhotoForm(request.POST)
        photo = Photo.objects.get(pk=photo_id)
        if form.is_valid():
            new_description = form.cleaned_data["description"]
            photo.description = new_description
            photo.save()
            messages.success(request, 'Description changed')
            return redirect(f"/photo/{photo_id}")
        ctx = {"form": form}
        return render(request, "edit_photo_tmp.html", ctx)


class DeletePhoto(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Photo
    template_name = "delete_photo_tmp.html"
    success_url = '/photos/my_photos'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return render(request, "delete_photo_tmp.html")


class LikePhoto(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        photo.likes.add(request.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UnlikePhoto(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        photo.likes.remove(request.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ViewPhotos(ListView):
    template_name = "view_photos_tmp.html"
    model = Photo
    context_object_name = 'photos'
    paginate_by = 21
    ordering = "-creation_date"


class MyPhotos(LoginRequiredMixin, View):

    def get(self, request):
        photos = Photo.objects.filter(owner=request.user).order_by("-creation_date")
        ctx = {"photos": photos}
        return render(request, "my_photos_tmp.html", ctx)


# this view displays photo details and a form to add comments
class OnePhoto(LoginRequiredMixin, View):

    def get(self, request, photo_id):
        form = CommentCreationForm()
        photo = Photo.objects.get(pk=photo_id)
        ctx = {"photo": photo, "form": form}
        return render(request, "view_one_photo_tmp.html", ctx)

    def post(self, request, photo_id):
        form = CommentCreationForm(request.POST)
        photo = Photo.objects.get(pk=photo_id)
        if form.is_valid():
            content = form.cleaned_data["content"]
            comment = Comment.objects.create(content=content, photo=photo, author=request.user)
            messages.success(request, 'Your comment has been saved!')
            return redirect(f'/photo/{photo_id}/')
        ctx = {"form": form}
        return render(request, "view_photos_tmp.html", ctx)




