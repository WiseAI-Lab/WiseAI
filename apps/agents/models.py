from accounts.models import UserProfile
from base.models import TimeStampedModel
from django.db import models


#  -----------Category And Configuration---------------
class CategoryModel(TimeStampedModel):
    AGENT = 1
    BEHAVIOUR = 2
    TYPE_OPTIONS = [(AGENT, 'agent'), (BEHAVIOUR, 'behaviour')]

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=100)
    parent = models.IntegerField(default=0)
    type = models.SmallIntegerField(null=False, default=1, choices=TYPE_OPTIONS)  # 1 basic_agent, 2 behaviour

    class Meta:
        app_label = "agents"
        db_table = "category"

    def __str__(self):
        return self.name


class ConfigurationModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(ConfigurationModel, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=100)
    content = models.TextField(default="{}")

    class Meta:
        app_label = "agents"
        db_table = "agent_configuration"


# ---------------Behaviours------------------

class BehaviourTopicModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(BehaviourTopicModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100, db_index=True)

    configuration = models.ForeignKey(
        ConfigurationModel,
        on_delete=models.CASCADE
    )
    description = models.TextField(null=True)
    status = models.SmallIntegerField(default=1)
    # Current Behaviours' id
    url = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = "agents"
        db_table = "behaviour_topic"


class BehaviourRepositoryModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(BehaviourRepositoryModel, self).__init__(*args, **kwargs)

    topics = models.ManyToManyField(
        BehaviourTopicModel,
        through="BehaviourRepoTopicModel",
        through_fields=("repo_id", "top_id")
    )
    # tag name
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.RESTRICT,
        db_index=True
    )
    description = models.TextField(null=True)

    # user
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    configuration_template = models.ForeignKey(ConfigurationModel, on_delete=models.CASCADE)

    is_verify = models.BooleanField(null=True, db_index=True)
    is_private = models.BooleanField(null=True, db_index=True)
    is_archived = models.BooleanField(null=True, db_index=True)
    is_mirror = models.BooleanField(null=True, db_index=True)
    is_office = models.BooleanField(
        default=False, verbose_name="office or user defined", db_index=True
    )
    num_watches = models.IntegerField(11, null=True)
    num_stars = models.IntegerField(11, null=True)
    status = models.BooleanField(null=False)

    is_template = models.IntegerField(11, null=True, db_index=True)
    template_id = models.BooleanField(null=False)

    avatar = models.ImageField(null=True)

    class Meta:
        app_label = "agents"
        db_table = "behaviour_repository"


# -----------------Agents------------------------
class AgentTopicModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(AgentTopicModel, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=100, db_index=True)
    behaviours = models.ManyToManyField(
        BehaviourTopicModel,
        through="AgentBehaviourModel",
        through_fields=("a_id", "b_id")
    )
    configuration = models.ForeignKey(
        ConfigurationModel,
        on_delete=models.CASCADE
    )
    description = models.TextField(null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        app_label = "agents"
        db_table = "agent_topic"


class AgentRepositoryModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(AgentRepositoryModel, self).__init__(*args, **kwargs)

    topics = models.ManyToManyField(
        AgentTopicModel,
        through="AgentRepoTopicModel",
        through_fields=("repo_id", "top_id")
    )
    # tag name
    name = models.CharField(max_length=100, db_index=True)

    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.RESTRICT,
        db_index=True
    )
    description = models.TextField(null=True)
    # user
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    configuration_template = models.ForeignKey(ConfigurationModel, on_delete=models.CASCADE)

    is_verify = models.BooleanField(null=True, db_index=True)
    is_private = models.BooleanField(null=True, db_index=True)
    is_archived = models.BooleanField(null=True, db_index=True)
    is_mirror = models.BooleanField(null=True, db_index=True)
    is_office = models.BooleanField(
        default=False, verbose_name="office or user defined", db_index=True
    )
    num_watches = models.IntegerField(11, null=True)
    num_stars = models.IntegerField(11, null=True)
    status = models.SmallIntegerField(default=1)

    is_template = models.IntegerField(11, null=True, db_index=True)
    template_id = models.BooleanField(null=False)

    avatar = models.ImageField(null=True)

    class Meta:
        app_label = "agents"
        db_table = "agent_repository"


# --------------Many To Many------------------

class BehaviourRepoTopicModel(models.Model):
    id = models.AutoField(primary_key=True)
    repo_id = models.ForeignKey('BehaviourRepositoryModel', on_delete=models.CASCADE)
    top_id = models.ForeignKey('BehaviourTopicModel', on_delete=models.CASCADE)

    class Meta:
        app_label = "agents"
        db_table = "behaviour_repo_topic"


class AgentRepoTopicModel(models.Model):
    id = models.AutoField(primary_key=True)
    repo_id = models.ForeignKey('AgentRepositoryModel', on_delete=models.CASCADE)
    top_id = models.ForeignKey('AgentTopicModel', on_delete=models.CASCADE)

    class Meta:
        app_label = "agents"
        db_table = "agent_repo_topic"


class AgentBehaviourModel(models.Model):
    id = models.AutoField(primary_key=True)
    a_id = models.ForeignKey('AgentTopicModel', on_delete=models.CASCADE)
    b_id = models.ForeignKey('BehaviourTopicModel', on_delete=models.CASCADE)

    class Meta:
        app_label = "agents"
        db_table = "agent_behaviour"
