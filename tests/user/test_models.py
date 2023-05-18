from django.test import TestCase
from django.utils import timezone
from user.models import User


# 회원가입시 유저 모델 생성 테스트
class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
        )

    def test_create_user(self):
        user_count = User.objects.count()
        self.assertEquals(user_count, 1)

        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.name, None)
        self.assertIsNotNone(self.user.nickname)
        self.assertEqual(self.user.birthday, None)
        self.assertEqual(self.user.job, None)
        self.assertEqual(self.user.career, None)

        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsInstance(self.user.created_at, timezone.datetime)
        self.assertIsInstance(self.user.updated_at, timezone.datetime)


# 최초 로그인 입력값 테스트
class UserFirstLogin(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            name='test',
            nickname='nick name',
            birthday='2000-12-11',
            job='BACKEND',
            career='취준생'
        )

    def test_name_label(self):
        max_length = self.user._meta.get_field("name").max_length
        value_length = len(self.user.nickname)

        self.assertLessEqual(value_length, max_length)

    def test_nickname_label(self):
        max_length = self.user._meta.get_field("nickname").max_length
        value_length = len(self.user.nickname)

        self.assertLessEqual(value_length, max_length)

    def test_birthday_label(self):
        expected_format = r"\d{4}-\d{2}-\d{2}"
        value = self.user.birthday

        self.assertRegex(value, expected_format)

    def test_job_label(self):
        valid_jobs = ['PRONTEND', 'BACKEND', 'DESIGN']
        value = self.user.job

        self.assertIn(value, valid_jobs)

        max_length = self.user._meta.get_field("job").max_length
        value_length = len(self.user.job)

        self.assertLessEqual(value_length, max_length)

    def test_career_label(self):
        n = 100  # 총 경력 레벨의 수
        valid_careers = [f"{i}년차" for i in range(1, n + 1)] + ['취준생']

        career_value = self.user.career

        self.assertIn(career_value, valid_careers)

