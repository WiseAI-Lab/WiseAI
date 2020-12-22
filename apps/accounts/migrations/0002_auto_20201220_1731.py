# Generated by Django 3.1.4 on 2020-12-20 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('agents', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='userandinitialagent',
            name='ac_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='agents.initialagentsmodel'),
        ),
        migrations.AddField(
            model_name='userandinitialagent',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userandbehaviour',
            name='b_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='agents.behavioursmodel'),
        ),
        migrations.AddField(
            model_name='userandbehaviour',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userandbasicagent',
            name='ac_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='agents.basicagentsmodel'),
        ),
        migrations.AddField(
            model_name='userandbasicagent',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='basic_agents',
            field=models.ManyToManyField(through='accounts.UserAndBasicAgent', to='agents.BasicAgentsModel'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='behaviours',
            field=models.ManyToManyField(through='accounts.UserAndBehaviour', to='agents.BehavioursModel'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='initial_agents',
            field=models.ManyToManyField(through='accounts.UserAndInitialAgent', to='agents.InitialAgentsModel'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]