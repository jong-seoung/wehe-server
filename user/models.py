from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.shortcuts import redirect
from django.db import models
from core.models import TimeStampedModel
from skills.models import Skill
from roles.models import Role
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            error_message = "이메일을 설정해야 합니다"
            return redirect("error_page")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            error_message = "슈퍼유저 권한을 부여하려면 is_staff 필드가 True여야 합니다."
            return redirect("error_page")

        if extra_fields.get("is_superuser") is not True:
            error_message = "슈퍼유저 권한을 부여하려면 is_superuser 필드가 True여야 합니다."
            return redirect("error_page")

        return self._create_user(email, password, **extra_fields)


class UserImage(TimeStampedModel, models.Model):
    file_size = models.BigIntegerField(blank=True, null=True)
    image = models.ImageField(
        _("profile image"),
        upload_to="profile_images/",
        blank=True,
        default="basic_profile_image",
    )


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=10, blank=True, null=True)
    nickname = models.CharField(
        _("nickname"), max_length=15, unique=True, blank=True, null=True
    )
    birthday = models.DateField(_("birthday"), max_length=10, blank=True, null=True)
    skills = models.ManyToManyField(Skill)
    roles = models.ManyToManyField(Role)
    user_image = models.OneToOneField(
        UserImage, on_delete=models.CASCADE, related_name="user"
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log " "into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.id:
            user_image = UserImage.objects.create()
            self.user_image = user_image

        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"
