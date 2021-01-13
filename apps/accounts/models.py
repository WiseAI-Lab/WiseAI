from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.db import models, transaction
from django.db.models import AutoField, ForeignKey
from django.contrib.auth.models import AbstractUser
from django.forms import CharField

from base.models import TimeStampedModel


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
    agents = models.ManyToManyField(to="agents.AgentRepositoryModel", through="AgentRepoModel",
                                    through_fields=("u_id", "a_id"))
    behaviours = models.ManyToManyField(to="agents.BehaviourRepositoryModel", through="BehaviourRepoModel",
                                        through_fields=("u_id", "b_id"))
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "user"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return True if check_password(raw_password, self.password) else False


class AgentRepoModel(models.Model):
    ua_id = AutoField(primary_key=True)
    u_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    a_id = ForeignKey('agents.AgentRepositoryModel', on_delete=models.RESTRICT)

    class Meta:
        db_table = "owner_agent_repository"


class BehaviourRepoModel(models.Model):
    ub_id = AutoField(primary_key=True)
    u_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    b_id = ForeignKey('agents.BehaviourRepositoryModel', on_delete=models.RESTRICT)

    class Meta:
        db_table = "owner_behaviour_repository"
