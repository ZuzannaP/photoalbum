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
from album_photo.views import AddPhoto, EditPhoto, DeletePhoto, ViewPhotos, LikePhoto, UnlikePhoto, MyPhotos, LoginView, LogoutView, \
    EditPersonalInfoView, SignUpView, DeleteAccountView, CustomPasswordChangeView, CustomPasswordChangeDoneView, \
    account_settings, OnePhoto
from photoalbum.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('manager/', admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('create_account/', SignUpView.as_view(), name='signup'),
    path('account_settings/', account_settings, name="account_settings"),
    path('edit_account/', EditPersonalInfoView.as_view(), name="edit_personal_info"),
    path('delete_account/', DeleteAccountView.as_view(), name="delete_account"),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path("photo/add", AddPhoto.as_view(), name="add_photo"),
    path("photo/edit/<int:photo_id>/", EditPhoto.as_view(), name="edit_photo"),
    path("photo/delete/<int:pk>/", DeletePhoto.as_view(), name="delete_photo"),
    path('photo/like/<int:pk>', LikePhoto.as_view(), name='like'),
    path('photo/unlike/<int:pk>', UnlikePhoto.as_view(), name='unlike'),
    path("", ViewPhotos.as_view(), name="view_photos"),
    path("photos/my_photos", MyPhotos.as_view(), name="my_photos"),
    path("photo/<int:photo_id>/", OnePhoto.as_view(), name="one_photo"),
]+ static(MEDIA_URL, document_root=MEDIA_ROOT)
