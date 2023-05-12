from django.test import TestCase
from django.utils import timezone
from user.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@test.com',
        )

    def test_create_user(self):
        user_count = User.objects.count()
        self.assertEquals(user_count, 1)

        self.assertEqual(self.user.email, 'testuser@test.com')
        self.assertEqual(self.user.name, None)
        self.assertIsNotNone(self.user.nickname)
        self.assertEqual(self.user.profile_image, 'basic_profile_image')
        self.assertEqual(self.user.birthday, None)
        self.assertEqual(self.user.job, None)
        self.assertEqual(self.user.career, None)

        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsInstance(self.user.created_at, timezone.datetime)
        self.assertIsInstance(self.user.updated_at, timezone.datetime)
