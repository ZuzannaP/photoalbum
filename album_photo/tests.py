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

        cls.u = User.objects.create_user(username="TestUser", password="testusertestuser", email="testuser@example.com")
        cls.r = User.objects.create_user(username="TestUser2", password="testuser2testuser2", email="testuser2@example.com")
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

        cls.u = User.objects.create_user(username="TestUser", password="testusertestuser", email="testuser@example.com")
        cls.r = User.objects.create_user(username="TestUser2", password="testuser2testuser2", email="testuser2@example.com")
        cls.p = Photo.objects.create(path=img, description="This is description of test image", owner=cls.u)
        cls.c = Comment.objects.create(content="This is a test comment.", photo=cls.p, author=cls.r)

    def test_valid_custom_user_change_form(self):
        self.u = User.objects.get(username="TestUser")
        data = {"first_name": "New", "last_name": "TestUser", 'email': "testuser@example.com"}
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


class ViewsUserTestClass(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username="TestUser", password="testusertestuser",
                                                  email="testuser@example.com")

    def test_login(self):
        c = Client()
        response = c.login(username="TestUser", password="testusertestuser")
        self.assertTrue(response)

    def test_access_for_logged_in(self):
        c = Client()
        c.login(username="TestUser", password="testusertestuser")
        response = c.get(reverse("view_photos"))
        self.assertEqual(response.status_code, 200)

    def test_restrictions_for_logged_out(self):
        """ logged-out user can not access urls restricted for logged-in users """
        c = Client()
        c.logout()
        response = c.get(reverse("add_photo"))
        self.assertRedirects(response, "/login/?next=/photo/add/")

    def test_signup_view_uses_correct_template_and_has_desired_location(self):
        c = Client()
        response = c.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_EditPersonalInfoView_uses_correct_template_and_has_desired_location(self):
        self.c = Client()
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('edit_personal_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_edit_personal_info.html')

    def test_DeleteAccountView_uses_correct_template_and_has_desired_location(self):
        self.c = Client()
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_confirm_delete.html')

    def test_CustomPasswordChangeView_uses_correct_template_and_has_desired_location(self):
        self.c = Client()
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change.html')


class ViewsAppLogicTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open("photoalbum/tests_data/test_image.jpeg", "rb") as test_photo:
            img = SimpleUploadedFile('image.jpg', content=test_photo.read(), content_type='image/jpeg')

        cls.test_user = User.objects.create_user(username="TestUser", password="testusertestuser",
                                                 email="testuser@example.com")
        cls.test_user2 = User.objects.create_user(username="TestUser2", password="testuser2testuser2",
                                                  email="testuser2@example.com")
        cls.p = Photo.objects.create(path=img, description="This is description of test image", owner=cls.test_user)
        cls.c = Client()

    def test_AddPhoto_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('add_photo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_photo_tmp.html')

    def test_EditPhoto_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('edit_photo', args=(self.p.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_photo_tmp.html')

    def test_DeletePhoto_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('delete_photo', args=(self.p.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_photo_tmp.html')

    def test_LikePhoto_uses_correct_template_and_redirects_correctly(self):
        self.c.login(username="TestUser2", password="testuser2testuser2")
        response = self.c.get(reverse('like', args=(self.p.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_UnlikePhoto_uses_correct_template_and_redirects_correctly(self):
        self.c.login(username="TestUser2", password="testuser2testuser2")
        response = self.c.get(reverse('unlike', args=(self.p.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_ViewPhotos_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('view_photos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_photos_tmp.html')

    def test_MyPhotos_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('my_photos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_photos_tmp.html')

    def test_OnePhoto_uses_correct_template_and_has_desired_location(self):
        self.c.login(username="TestUser", password="testusertestuser")
        response = self.c.get(reverse('one_photo', args=(self.p.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_one_photo_tmp.html')
