from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.db import models, transaction
from django.db.models import AutoField, ForeignKey
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.forms import CharField

from base.models import TimeStampedModel


class UserStatus(TimeStampedModel):
    """
    Model representing the status of a user being invited by
    other user to host/participate in a competition
    .. note::
        There are four different status:
            - Unknown.
            - Denied.
            - Accepted
            - Pending.
    """

    UNKNOWN = "unknown"
    DENIED = "denied"
    ACCEPTED = "accepted"
    PENDING = "pending"
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "accounts"


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username,and password.
        """
        if not username:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                hash_password = make_password(password)
                user.set_password(hash_password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)


class UserProfile(AbstractUser, TimeStampedModel):
    objects = UserManager()
    phone = CharField(max_length=64)
    avatar = models.CharField(max_length=100, null=True, blank=True, verbose_name="avatar")
    role = models.CharField(max_length=10, default=1, verbose_name="role")
    initial_agents = models.ManyToManyField(to="agents.InitialAgentsModel", through="UserAndInitialAgent",
                                            through_fields=("user_id", "ac_id"))
    basic_agents = models.ManyToManyField(to="agents.BasicAgentsModel", through="UserAndBasicAgent",
                                          through_fields=("user_id", "ac_id"))
    behaviours = models.ManyToManyField(to="agents.BehavioursModel", through="UserAndBehaviour",
                                        through_fields=("user_id", "b_id"))

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "user"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return True if check_password(raw_password, self.password) else False


class UserAndInitialAgent(models.Model):
    ua_id = AutoField(primary_key=True)
    user_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    ac_id = ForeignKey('agents.InitialAgentsModel', on_delete=models.RESTRICT)


class UserAndBasicAgent(models.Model):
    ua_id = AutoField(primary_key=True)
    user_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    ac_id = ForeignKey('agents.BasicAgentsModel', on_delete=models.RESTRICT)


class UserAndBehaviour(models.Model):
    ua_id = AutoField(primary_key=True)
    user_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    b_id = ForeignKey('agents.BehavioursModel', on_delete=models.RESTRICT)
