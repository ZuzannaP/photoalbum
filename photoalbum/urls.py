"""photoalbum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from album_photo.views import homepage, AddPhoto, ViewPhotos, LikePhoto, UnlikePhoto, MyPhotos, LoginView, LogoutView
from photoalbum.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("photo/add", AddPhoto.as_view(), name="add_photo"),
    path('photo/like/<int:pk>', LikePhoto.as_view(), name='like'),
    path('photo/unlike/<int:pk>', UnlikePhoto.as_view(), name='unlike'),
    path("photos/", ViewPhotos.as_view(), name="view_photos"),
    path("photos/my_photos", MyPhotos.as_view(), name="my_photos"),
    path("", homepage, name="homepage")
]+ static(MEDIA_URL, document_root=MEDIA_ROOT)
