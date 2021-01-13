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
    required_content = models.TextField(default="{}")  # IF Exist that it's required.

    class Meta:
        app_label = "agents"
        db_table = "agent_configuration"


# ------------Abstract Model--------------

class TopicModel(TimeStampedModel):
    ZIP_TYPE = 1
    GIT_TYPE = 2
    TYPE_STORE = [(ZIP_TYPE, 'zip'), (GIT_TYPE, 'git')]

    ALIVE = 1
    STOP = 2
    DEAD = 3
    TYPE_STATUS = [(ALIVE, 'alive'), (STOP, 'stop'), (DEAD, 'dead')]

    def __init__(self, *args, **kwargs):
        super(TopicModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100, db_index=True)

    configuration = models.ForeignKey(
        ConfigurationModel,
        on_delete=models.CASCADE
    )
    description = models.TextField(null=True)
    status = models.SmallIntegerField(default=1, choices=TYPE_STATUS)
    # Current Behaviours' id
    url = models.URLField(max_length=200, blank=True, null=True)
    store_type = models.SmallIntegerField(default=2, choices=TYPE_STORE)

    class Meta:
        abstract = True


class RepositoryModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(RepositoryModel, self).__init__(*args, **kwargs)

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

    is_template = models.BooleanField(null=False, default=False)
    template_id = models.IntegerField(11, null=True, db_index=True, default=0)

    avatar = models.URLField(null=True)

    class Meta:
        abstract = True


# ---------------Behaviours------------------

class BehaviourTopicModel(TopicModel):
    def __init__(self, *args, **kwargs):
        super(BehaviourTopicModel, self).__init__(*args, **kwargs)

    class Meta:
        app_label = "agents"
        db_table = "behaviour_topic"


class BehaviourRepositoryModel(RepositoryModel):
    def __init__(self, *args, **kwargs):
        super(BehaviourRepositoryModel, self).__init__(*args, **kwargs)

    topics = models.ManyToManyField(
        BehaviourTopicModel,
        through="BehaviourRepoTopicModel",
        through_fields=("repo_id", "top_id")
    )

    class Meta:
        app_label = "agents"
        db_table = "behaviour_repository"


# -----------------Agents------------------------
class AgentTopicModel(TopicModel):
    def __init__(self, *args, **kwargs):
        super(AgentTopicModel, self).__init__(*args, **kwargs)

    behaviours = models.ManyToManyField(
        BehaviourTopicModel,
        through="AgentBehaviourModel",
        through_fields=("a_id", "b_id")
    )

    class Meta:
        app_label = "agents"
        db_table = "agent_topic"


class AgentRepositoryModel(RepositoryModel):
    def __init__(self, *args, **kwargs):
        super(AgentRepositoryModel, self).__init__(*args, **kwargs)

    topics = models.ManyToManyField(
        AgentTopicModel,
        through="AgentRepoTopicModel",
        through_fields=("repo_id", "top_id")
    )

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
