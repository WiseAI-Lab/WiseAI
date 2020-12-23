import hashlib
import random

from rest_framework import serializers

from accounts.serializers import UserDetailSerializer
from .models import (
    AgentConfigsModel,
    BehaviourConfigsModel,
    CategoryModel,
    InitialAgentsModel,
    BasicAgentsModel,
    BehavioursModel
)


class AgentConfigsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AgentConfigsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentConfigsModel
        fields = "__all__"


class BehaviourConfigsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BehaviourConfigsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehaviourConfigsModel
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    type_choice = (
        (1, 'basic_agent'),
        (2, 'behaviour'),
    )

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = CategoryModel
        fields = (
            "name",
            "parent",
            "type",
        )


# ---------------------Behaviour---------------------
class BehaviourListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BehaviourListSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehavioursModel
        fields = "__all__"

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        size = 256
        random_str = str(obj.name)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url


class CreateBehaviourSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateBehaviourSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehavioursModel
        fields = "__all__"


class BehaviourInfoSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BehaviourInfoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehavioursModel
        fields = "__all__"


# --------------------------BasicAgent list---------------------
# Basic agents list
class BasicAgentsListSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()

    avatar = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    agent_category = serializers.SerializerMethodField()
    parent_agent = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BasicAgentsListSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BasicAgentsModel
        # fields = "__all__"
        exclude = ["prerequisite_behaviour_categories", "default_behaviours", "configs", "url"]

    def get_author(self, obj):
        author = obj.author
        return {
            "id": author.id,
            "name": str(author)
        }

    def get_agent_category(self, obj):
        agent_category = obj.agent_category
        return {
            "id": agent_category.id,
            "name": agent_category.name
        }

    def get_parent_agent(self, obj):
        if obj.parent_agent == 0:
            return None
        ss = BasicAgentsModel.objects.get(id=obj.parent_agent)
        return {
            "id": obj.parent_agent,
            "name": ss.name
        }

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        size = 256
        random_str = str(obj.name)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url


class CreateBasicAgentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateBasicAgentSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BasicAgentsModel
        fields = "__all__"
        # exclude = ["prerequisite_behaviour_categories", "default_behaviours", "configs", "url"]


# --------------------------BasicAgent info---------------------

class BasicAgentsInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()
    prerequisite_behaviour_categories = serializers.SerializerMethodField()
    default_behaviours = serializers.SerializerMethodField()
    agent_category = serializers.SerializerMethodField()
    configs = serializers.SerializerMethodField()
    parent_agent = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BasicAgentsInfoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BasicAgentsModel
        fields = "__all__"

    def get_author(self, obj):
        author = obj.author
        return {
            "id": author.id,
            "name": str(author)
        }

    def get_agent_category(self, obj):
        agent_category = obj.agent_category
        return {
            "id": agent_category.id,
            "name": agent_category.name
        }

    def get_prerequisite_behaviour_categories(self, obj):
        ret = obj.prerequisite_behaviour_categories
        temp = []
        for i in ret:
            category_name = CategoryModel.objects.get(id=i).name
            temp.append({"id": i, "name": category_name})
        return temp

    def get_default_behaviours(self, obj):
        ret = obj.default_behaviours
        temp = []
        for i in ret:
            behaviour_name = BehavioursModel.objects.get(id=i).name
            temp.append({"id": i, "name": behaviour_name})
        return temp

    def get_configs(self, obj):
        ss = AgentConfigsSerializer(obj.configs)
        return ss.data

    def get_parent_agent(self, obj):
        """
            Agent Tree
        :param obj:
        :return:
        """
        tree_node = {
            "name": obj.name,
            "id": obj.id,
            "children": self._fib_parent_tree(obj, [])
        }
        return tree_node

    def _fib_parent_tree(self, node, dict_info):
        parent_agent = node.parent_agent
        if parent_agent == 0:
            return dict_info
        node = BasicAgentsModel.objects.get(id=parent_agent)
        return [
            {
                "name": node.name,
                "id": node.id,
                "children": self._fib_parent_tree(node, dict_info)
            }
        ]

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        size = 256
        random_str = str(obj.name)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url


# ---------------------------InitialAgent list-----------------

class InitialAgentListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    agent_category = serializers.SerializerMethodField()
    basic_agent = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(InitialAgentListSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = InitialAgentsModel
        fields = "__all__"
        # fields = (
        #     "id",
        #     "name",
        #     "behaviours",
        #     "basic_agent",
        #     "agent_category",
        #     "credit"
        # )

    def get_agent_category(self, obj):
        agent_category = obj.agent_category
        return {
            "id": agent_category.id,
            "name": agent_category.name
        }

    def get_basic_agent(self, obj):
        if obj.basic_agent == 0:
            return None
        ss = BasicAgentsModel.objects.get(id=obj.basic_agent)
        return {
            "id": obj.basic_agent,
            "name": ss.name
        }

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        size = 256
        random_str = str(obj.name)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url


class CreateInitialAgentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateInitialAgentSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = InitialAgentsModel
        fields = "__all__"


class InitialAgentInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    in_docker = serializers.SerializerMethodField()
    belong_to = serializers.SerializerMethodField()
    behaviours = serializers.SerializerMethodField()
    agent_category = serializers.SerializerMethodField()
    agent_configs = serializers.SerializerMethodField()
    behaviour_configs = serializers.SerializerMethodField()
    basic_agent = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(InitialAgentInfoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = InitialAgentsModel
        fields = "__all__"

    def get_belong_to(self, obj):
        user = obj.belong_to
        return {
            "id": user.id,
            "name": str(user)
        }

    def get_agent_category(self, obj):
        agent_category = obj.agent_category
        return {
            "id": agent_category.id,
            "name": agent_category.name
        }

    def get_behaviours(self, obj):
        ret = obj.behaviours
        temp = []
        for i in ret:
            behaviour_name = BehavioursModel.objects.get(id=i).name
            temp.append({"id": i, "name": behaviour_name})
        return temp

    def get_agent_configs(self, obj):
        ss = AgentConfigsSerializer(obj.agent_configs)
        return ss.data

    def get_behaviour_configs(self, obj):
        ss = BehaviourConfigsSerializer(obj.behaviour_configs)
        return ss.data

    def get_basic_agent(self, obj):
        """
            Agent Tree
        :param obj:
        :return:
        """
        basic_agent = BasicAgentsModel.objects.get(id=obj.basic_agent)
        tree_node = {
            "name": basic_agent.name,
            "id": basic_agent.id,
        }
        return tree_node

    def get_in_docker(self, obj):
        basic_agent = BasicAgentsModel.objects.get(id=obj.basic_agent)
        if basic_agent.in_docker:
            return True
        return False

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        size = 256
        random_str = str(obj.name)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url
