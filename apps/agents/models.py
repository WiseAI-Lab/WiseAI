from django.contrib.postgres.fields import ArrayField
from base.models import TimeStampedModel
from django.db import models


class CategoryModel(TimeStampedModel):

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=100, db_index=True)
    parent = models.IntegerField(default=0)
    type = models.SmallIntegerField(null=False, default=1)  # 1 agent, 2 behaviour

    class Meta:
        app_label = "agents"
        db_table = "category"

    def __str__(self):
        return self.name


class VersionModel(TimeStampedModel):
    """
        Description what the agent version is.
    """

    def __init__(self, *args, **kwargs):
        super(VersionModel, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=100, db_index=True)
    previous = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        app_label = "agents"
        db_table = "version"

    def __str__(self):
        return self.name


# Agent Config.
class AgentConfigsModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(AgentConfigsModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100)
    # extra property
    extend = models.TextField(default="{}")
    # if basic agent or user's agent
    is_base = models.BooleanField(default=False, db_index=True)

    class Meta:
        app_label = "agents"
        db_table = "agent_configs"


# Behaviour config
class BehaviourConfigsModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(BehaviourConfigsModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100, db_index=True)
    # pool executors in progress or thread
    is_progress_pool = models.BooleanField(default=False)
    # default pool size.
    default_pool_size = models.IntegerField(default=5)
    # extra property
    extend = models.TextField(default="{}")
    #
    is_base = models.BooleanField(default=False, db_index=True)

    class Meta:
        app_label = "agents"
        db_table = "behaviour_configs"


# Behaviours
class BehavioursModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(BehavioursModel, self).__init__(*args, **kwargs)

    # name of behaviours
    name = models.CharField(max_length=100, db_index=True)
    # List[Category.id]
    prerequisite_behaviour_categories = ArrayField(
        models.IntegerField(), default=list, blank=True
    )
    # List[BasicAgents.id]
    prerequisite_agents = ArrayField(
        models.IntegerField(), default=list, blank=True
    )
    # Basic behaviour id.
    parent_behaviour = models.IntegerField(null=True, blank=True, default=None)
    behaviour_category = models.OneToOneField(CategoryModel, null=False, on_delete=models.RESTRICT)
    url = models.URLField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(
        "accounts.UserProfile",
        related_name="user_behaviours",
        on_delete=models.RESTRICT
    )
    description = models.TextField(null=True, blank=True)
    is_office = models.BooleanField(
        default=False, verbose_name="office or user defined", db_index=True
    )
    configs = models.ForeignKey(
        "BehaviourConfigsModel",
        related_name="config_behaviours",
        on_delete=models.RESTRICT
    )

    class Meta:
        app_label = "agents"
        db_table = "behaviours"


# Basic Agent
class BasicAgentsModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(BasicAgentsModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100)
    # Prerequisite set of behaviour for this agent.
    prerequisite_behaviour_categories = ArrayField(
        models.IntegerField(), default=list, blank=True
    )
    # Default behaviours for this agent.
    default_behaviours = ArrayField(
        models.IntegerField(), default=list, blank=True
    )
    # Parent agent id.
    parent_agent = models.IntegerField(null=True, blank=True, default=None, db_index=True)
    # agent category
    agent_category = models.ForeignKey(
        "CategoryModel",
        related_name="agent_basic_category",
        on_delete=models.RESTRICT,
        db_index=True
    )
    # url for current template.
    url = models.URLField(max_length=100, blank=True, null=True)
    # author name
    author = models.ForeignKey(
        "accounts.UserProfile",
        related_name="user_basic_agent",
        on_delete=models.RESTRICT,
        db_index=True
    )
    description = models.TextField(null=True, blank=True)
    is_office = models.BooleanField(
        default=False, verbose_name="office or user defined", db_index=True
    )
    in_docker = models.BooleanField(
        default=False, verbose_name="docker exist or not", db_index=True
    )
    # config for this.
    configs = models.ForeignKey(
        "AgentConfigsModel",
        related_name="config_agents",
        on_delete=models.RESTRICT
    )
    # current version
    version = models.OneToOneField(VersionModel, null=True, on_delete=models.RESTRICT)
    # extra support version is:
    extra_support_version = ArrayField(
        models.IntegerField(), default=list, blank=True
    )

    class Meta:
        app_label = "agents"
        db_table = "basic_agents"


# Initial Agent
class InitialAgentsModel(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super(InitialAgentsModel, self).__init__(*args, **kwargs)

    # name
    name = models.CharField(max_length=100, db_index=True)
    # behaviours in initial behaviour of
    behaviours = ArrayField(
        models.IntegerField(), default=list, blank=True
    )  # Current Behaviours' id
    basic_agent = models.IntegerField(null=False)
    # Category for initial agent, and default is inherit from basic agent.
    agent_category = models.ForeignKey(
        "CategoryModel",
        related_name="agent_initial_category",
        on_delete=models.RESTRICT,
        db_index=True
    )
    # certificate
    credit = models.CharField(max_length=100, db_index=True)
    # user
    belong_to = models.ForeignKey(
        "accounts.UserProfile",
        related_name="user_initial_agent",
        on_delete=models.CASCADE
    )
    # configs for current agent
    agent_configs = models.OneToOneField(AgentConfigsModel, null=True, on_delete=models.RESTRICT)
    # configs for current agent's behaviours
    behaviour_configs = models.OneToOneField(BehaviourConfigsModel, null=True, on_delete=models.RESTRICT)

    class Meta:
        app_label = "agents"
        db_table = "initial_agents"
