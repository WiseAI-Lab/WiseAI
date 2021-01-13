from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import UserProfile
from .models import (
    # AgentConfigurationModel,
    # BehaviourConfigurationModel,
    CategoryModel,
    AgentTopicModel,
    AgentRepositoryModel,
    BehaviourTopicModel,
    BehaviourRepositoryModel

)
from .utils import generate_avatar


class CategorySerializer(serializers.ModelSerializer):
    type_choice = (
        (1, 'agent'),
        (2, 'behaviour'),
    )
    type = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = CategoryModel
        fields = [
            "name",
            "parent",
            "type",
        ]

    def get_parent(self, obj):
        if obj.parent == 0:
            return "None"

    def get_type(self, obj):
        for t in self.type_choice:
            if t[0] == obj.type:
                return t[1]
            else:
                return obj.type


class RepositorySerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()

    topics = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    template_id = serializers.SerializerMethodField()
    configuration_template = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(RepositorySerializer, self).__init__(*args, **kwargs)
        self.repository = None
        self.topic_serializer = None

    class Meta:
        model = None
        abstract = True

    def get_topics(self, obj):
        topics = obj.topics.all()
        serializer = self.topic_serializer(topics, many=True)
        return serializer.data

    def get_owner(self, obj):
        owner = obj.owner
        return {
            "id": owner.id,
            "name": str(owner)
        }

    def get_template_id(self, obj):
        if obj.is_template and obj.template_id != 0:
            ss = self.repository.objects.get(id=obj.template_id)
            return {
                "id": ss.id,
                "name": ss.name
            }
        else:
            return None

    def get_configuration_template(self, obj):
        return obj.configuration_template.content

    def get_category(self, obj):
        agent_category = obj.category
        return {
            "id": agent_category.id,
            "name": agent_category.name
        }

    def get_avatar(self, obj):
        return generate_avatar(obj)


class TopicSerializer(serializers.ModelSerializer):
    configuration = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(TopicSerializer, self).__init__(*args, **kwargs)

    def get_configuration(self, obj):
        return obj.configuration.content

    def get_status(sel, obj):
        status = obj.status
        return status


# ---------------------Behaviour---------------------


class BehaviourRepositorySerializer(RepositorySerializer):

    def __init__(self, *args, **kwargs):
        super(BehaviourRepositorySerializer, self).__init__(*args, **kwargs)
        self.repository = BehaviourRepositoryModel
        self.topic_serializer = BehaviourTopicSerializer

    class Meta:
        model = BehaviourRepositoryModel
        fields = [
            "topics",
            "name",
            "category",
            "description",
            "owner",
            "configuration_template",
            "is_verify",
            "is_private",
            "is_archived",
            "is_mirror",
            "is_office",
            "num_watches",
            "num_stars",
            "status",
            "is_template",
            "template_id",
            "avatar",
        ]


class BehaviourTopicSerializer(TopicSerializer):
    def __init__(self, *args, **kwargs):
        super(BehaviourTopicSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehaviourTopicModel
        fields = [
            "name",
            "configuration",
            "description",
            "status",
            "url",
            "store_type"
        ]


class CreateBehaviourRepositorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateBehaviourRepositorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehaviourRepositoryModel
        fields = [
            "topics",
            "name",
            "category",
            "description",
            "owner",
            "configuration_template",
            "is_verify",
            "is_private",
            "is_archived",
            "is_mirror",
            "is_office",
            "num_watches",
            "num_stars",
            "status",
            "is_template",
            "template_id",
            "avatar",
        ]


class CreateBehaviourTopicSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateBehaviourTopicSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehaviourTopicModel
        fields = [
            "name",
            "configuration",
            "description",
            "url",
            "status",
        ]


# --------------------------Agent list---------------------
class AgentRepositorySerializer(RepositorySerializer):
    template_id = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(AgentRepositorySerializer, self).__init__(*args, **kwargs)
        self.repository = AgentRepositoryModel
        self.topic_serializer = AgentTopicSerializer

    class Meta:
        model = AgentRepositoryModel
        fields = [
            "topics",
            "name",
            "category",
            "description",
            "owner",
            "configuration_template",
            "is_verify",
            "is_private",
            "is_archived",
            "is_mirror",
            "is_office",
            "num_watches",
            "num_stars",
            "status",
            "is_template",
            "template_id",
            "avatar",
        ]


class AgentTopicSerializer(TopicSerializer):
    behaviours = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(AgentTopicSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentTopicModel
        fields = [
            "name",
            "behaviours",
            "configuration",
            "description",
            "url",
            "status",
        ]

    def get_behaviours(self, obj):
        behaviours = obj.behaviours.all()
        serializer = BehaviourTopicSerializer(behaviours, many=True)
        return serializer.data


class CreateAgentRepositorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateAgentRepositorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentRepositoryModel
        fields = [
            "topics",
            "name",
            "category",
            "description",
            "owner",
            "configuration_template",
            "is_verify",
            "is_private",
            "is_archived",
            "is_mirror",
            "is_office",
            "num_watches",
            "num_stars",
            "status",
            "is_template",
            "template_id",
            "avatar",
        ]


class CreateAgentTopicSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CreateAgentTopicSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentTopicModel
        fields = [
            "name",
            "behaviours",
            "configuration",
            "description",
            "url",
            "status",
        ]


# ---------------------Build Agent-----------------------------

class AgentRepositoryListSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    ALIVE = 1
    STOP = 2
    DEAD = 3
    TYPE_STATUS = [(ALIVE, 'alive'), (STOP, 'stop'), (DEAD, 'dead')]

    def __init__(self, *args, **kwargs):
        super(AgentRepositoryListSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentRepositoryModel
        fields = [
            "topics",
        ]

    def get_topics(self, obj):
        repo_name = obj.name
        topics = obj.topics.all()
        data = {}
        for top in topics:
            name = f"{repo_name}:{top.name}"
            status = top.status
            if status == self.ALIVE:
                status = 'alive'
            elif status == self.STOP:
                status = 'stop'
            else:
                status = 'dead'
            data[top.id] = {
                'name': name,
                'status': status
            }
        return data


class BuildAgentBehavioursSerializer(TopicSerializer):
    name = serializers.SerializerMethodField()
    store_type = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BuildAgentBehavioursSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = BehaviourTopicModel
        fields = [
            "name",
            "configuration",
            "description",
            "status",
            "url",
            "store_type",
            "category"
        ]

    def get_name(self, obj):
        b_repo = obj.behaviourrepositorymodel_set.first()
        b_repo_name = b_repo.name
        b_topic_name = obj.name
        name = f"{b_repo_name}_{b_topic_name}"
        return name

    def get_category(self, obj):
        b_repo = obj.behaviourrepositorymodel_set.first()
        category = b_repo.category
        category_root_name = category.name
        while True:
            if category.parent == 0:
                break
            cur_id = category.parent
            category = CategoryModel.objects.get(id=cur_id)
            prev_name = category.name
            category_root_name = f"{prev_name}.{category_root_name}"
        return category_root_name

    def get_store_type(sel, obj):
        store_type = obj.store_type
        if store_type == 1:
            return "zip"
        else:
            return "git"


class BuildAgentRepositorySerializer(RepositorySerializer):
    template_id = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BuildAgentRepositorySerializer, self).__init__(*args, **kwargs)
        self.repository = AgentRepositoryModel
        self.topic_serializer = AgentTopicSerializer

    class Meta:
        model = AgentRepositoryModel
        fields = [
            "topics",
            "name",
            "category",
            "description",
            "owner",
            "configuration_template",
            "is_verify",
            "is_private",
            "is_archived",
            "is_mirror",
            "is_office",
            "num_watches",
            "num_stars",
            "status",
            "is_template",
            "template_id",
            "avatar",
        ]

    def get_topics(self, obj):
        return obj.topics.values('id', 'name')


class BuildAgentByIdSerializer(TopicSerializer):
    behaviours = serializers.SerializerMethodField()
    repository = serializers.SerializerMethodField()
    auth_token = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    store_type = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BuildAgentByIdSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AgentTopicModel
        fields = [
            "name",
            "behaviours",
            "configuration",
            "description",
            "url",
            "status",
            "repository",
            "store_type",
            "auth_token"
        ]

    def get_auth_token(self, obj):
        data = obj.agentrepositorymodel_set.first()
        token = Token.objects.get(user=data.owner)
        return token.key

    def get_behaviours(self, obj):
        behaviours = obj.behaviours.all()
        serializer = BuildAgentBehavioursSerializer(behaviours, many=True)
        return serializer.data

    def get_repository(self, obj):
        data = obj.agentrepositorymodel_set.first()
        serializer = BuildAgentRepositorySerializer(data)
        return serializer.data

    def get_store_type(sel, obj):
        store_type = obj.store_type
        if store_type == 1:
            return "zip"
        else:
            return "git"
