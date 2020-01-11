from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, FormView
from django.views.generic.base import View

from album_photo.forms import AddPhotoForm, LoginForm
from album_photo.models import Photo


def homepage(request):
    return render(request, "homepage.html")


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


class AddPhoto(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPhotoForm()
        ctx = {"form": form}
        return render(request, "add_photo_tmp.html", ctx)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            path = form.cleaned_data["path"]
            photo = Photo.objects.create(path=path, owner=request.user)
            return redirect("view_photos")
        ctx = {"form": form}
        return render(request, "add_photo_tmp.html", ctx)


class LikePhoto(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        photo.likes.add(request.user)
        return redirect('view_photos')


class UnlikePhoto(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        photo.likes.remove(request.user)
        return redirect('view_photos')


class ViewPhotos(LoginRequiredMixin, ListView):
    template_name = "view_photos_tmp.html"
    model = Photo
    context_object_name = 'photos'


class MyPhotos(LoginRequiredMixin, View):
    def get(self, request):
        photos = Photo.objects.filter(owner = request.user)
        ctx = {"photos": photos}
        return render(request, "my_photos_tmp.html", ctx)





