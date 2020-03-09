import os
import shutil

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.test import Client
from django.urls import reverse

from album_photo.forms import AddPhotoForm, CustomUserChangeForm, CommentCreationForm, EditPhotoForm
from album_photo.models import Photo, Comment


TEST_DIR = 'test_data'
my_media_root = os.path.join(TEST_DIR, 'media')


class ModelTestClass(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=my_media_root)
    def setUpTestData(cls):
        with open("photoalbum/tests_data/test_image.jpeg", "rb") as test_photo:
            img = SimpleUploadedFile('image.jpg', content=test_photo.read(), content_type='image/jpeg')

        cls.u = User.objects.create_user(username="TestUser", password="testusertestuser", email="testuser@wp.pl")
        cls.r = User.objects.create_user(username="TestUser2", password="testuser2testuser2", email="testuser2@wp.pl")
        cls.p = Photo.objects.create(path=img, description="This is description of test image", owner=cls.u)
        cls.c = Comment.objects.create(content="This is a test comment.", photo=cls.p, author=cls.r)

    def test_photo(self):
        self.assertTrue(isinstance(self.p, Photo))
        self.assertEqual(self.p.__str__(), self.p.description)

    def test_comment(self):
        self.assertTrue(isinstance(self.c, Comment))
        self.assertEqual(self.c.__str__(), self.c.content)

    @classmethod
    def tearDown(cls):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class FormsTestClass(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=my_media_root)
    def setUpTestData(cls):
        with open("photoalbum/tests_data/test_image.jpeg", "rb") as test_photo:
            img = SimpleUploadedFile('image.jpg', content=test_photo.read(), content_type='image/jpeg')

        cls.u = User.objects.create_user(username="TestUser", password="testusertestuser", email="testuser@wp.pl")
        cls.r = User.objects.create_user(username="TestUser2", password="testuser2testuser2", email="testuser2@wp.pl")
        cls.p = Photo.objects.create(path=img, description="This is description of test image", owner=cls.u)
        cls.c = Comment.objects.create(content="This is a test comment.", photo=cls.p, author=cls.r)

    def test_valid_custom_user_change_form(self):
        self.u = User.objects.get(username="TestUser")
        data = {"first_name": "New", "last_name": "TestUser", 'email': "testuser@wp.pl"}
        form = CustomUserChangeForm(instance=self.u, data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_custom_user_change_form(self):
        """inserting invalid email on purpose"""

        self.u = User.objects.get(username="TestUser")
        data = {"first_name": "New", "last_name": "TestUser", 'email': "testuser"}
        form = CustomUserChangeForm(instance=self.u, data=data)
        self.assertFalse(form.is_valid())

    def test_valid_add_photo_form(self):
        with open("photoalbum/tests_data/test_image.jpeg", "rb") as test_photo:
            img = SimpleUploadedFile('image2.jpg', content=test_photo.read(), content_type='image/jpeg')
        file_data = {"path": img}
        data = {"description": "This is description of another image"}
        form = AddPhotoForm(data, file_data)
        self.assertTrue(form.is_valid())

    def test_invalid_add_photo_form(self):
        """omitting image upload on purpose"""

        data = {"description": "This is description of another image"}
        form = AddPhotoForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_edit_photo_form(self):
        data = {"description": "New description"}
        form = EditPhotoForm(instance=self.p, data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_edit_photo_form(self):
        """putting wrong form name on purpose"""

        data = {"fake_description": "New description"}
        form = EditPhotoForm(instance=self.p, data=data)
        self.assertFalse(form.is_valid())

    def test_valid_comment_creation_form(self):
        data = {"content": "New comment"}
        form = CommentCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_creation_form(self):
        """putting wrong form name on purpose"""

        data = {"fake_content": "New comment"}
        form = CommentCreationForm(data=data)
        self.assertFalse(form.is_valid())

    @classmethod
    def tearDown(cls):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
