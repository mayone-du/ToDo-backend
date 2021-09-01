from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models


def upload_task_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['tasks', str(instance.create_user.id)+str(instance.title)+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        try:
            if not email:
                raise ValueError('email is must')
            user = self.model(email=self.normalize_email(email))
            if username is not None:
                user.username = username
            user.set_password(password)
            user.save(using=self._db)
            # ユーザー作成時にメールを送信
            send_mail(subject='サンプルアプリ | 本登録のお知らせ', message=f'ユーザー作成時にメール送信しています' + email, from_email="sample@email.com",
                recipient_list=[email], fail_silently=False)
            return user
        except:
            raise ValueError('create_user_error')

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ユーザー
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Task(models.Model):
    create_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='target_user',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=1000, default='',null=False, blank=False)
    task_image = models.ImageField(
        blank=True, null=True, upload_to=upload_task_path)
    is_done = models.BooleanField(null=False, blank=False, default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.create_user
