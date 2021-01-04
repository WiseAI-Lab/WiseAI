from rest_framework import serializers

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


class BuildAgentByIdSerializer(TopicSerializer):
    behaviours = serializers.SerializerMethodField()
    repository = serializers.SerializerMethodField()

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
            "repository"
        ]

    def get_behaviours(self, obj):
        behaviours = obj.behaviours.all()
        serializer = BehaviourTopicSerializer(behaviours, many=True)
        return serializer.data

    def get_repository(self, obj):
        data = obj.agentrepositorymodel_set.first()
        serializer = AgentRepositorySerializer(data)
        return serializer.data
# --------------------------BasicAgent info---------------------

# class AgentInfoSerializer(serializers.ModelSerializer):
#     avatar = serializers.SerializerMethodField()
#
#     author = serializers.SerializerMethodField()
#     prerequisite_behaviour_categories = serializers.SerializerMethodField()
#     default_behaviours = serializers.SerializerMethodField()
#     agent_category = serializers.SerializerMethodField()
#     # configuration = serializers.SerializerMethodField()
#     parent_agent = serializers.SerializerMethodField()
#
#     def __init__(self, *args, **kwargs):
#         super(AgentInfoSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = AgentModel
#         fields = "__all__"
#
#     def get_author(self, obj):
#         author = obj.author
#         return {
#             "id": author.id,
#             "name": str(author)
#         }
#
#     def get_agent_category(self, obj):
#         agent_category = obj.agent_category
#         return {
#             "id": agent_category.id,
#             "name": agent_category.name
#         }
#
#     def get_prerequisite_behaviour_categories(self, obj):
#         ret = obj.prerequisite_behaviour_categories
#         temp = []
#         for i in ret:
#             category_name = CategoryModel.objects.get(id=i).name
#             temp.append({"id": i, "name": category_name})
#         return temp
#
#     def get_default_behaviours(self, obj):
#         ret = obj.default_behaviours
#         temp = []
#         for i in ret:
#             behaviour_name = BehaviourModel.objects.get(id=i).name
#             temp.append({"id": i, "name": behaviour_name})
#         return temp
#
#
#     def get_parent_agent(self, obj):
#         """
#             Agent Tree
#         :param obj:
#         :return:
#         """
#         tree_node = {
#             "name": obj.name,
#             "id": obj.id,
#             "children": self._fib_parent_tree(obj, [])
#         }
#         return tree_node
#
#     def _fib_parent_tree(self, node, dict_info):
#         parent_agent = node.parent_agent
#         if parent_agent == 0:
#             return dict_info
#         node = AgentModel.objects.get(id=parent_agent)
#         return [
#             {
#                 "name": node.name,
#                 "id": node.id,
#                 "children": self._fib_parent_tree(node, dict_info)
#             }
#         ]
#
#     def get_avatar(self, obj):
#         styles = ['identicon', 'monsterid', 'wavatar']
#         size = 256
#         random_str = str(obj.name)
#         m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
#         url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
#         return url

# ---------------------------InitialAgent list-----------------

# class InitialAgentListSerializer(serializers.ModelSerializer):
#     avatar = serializers.SerializerMethodField()
#     agent_category = serializers.SerializerMethodField()
#     basic_agent = serializers.SerializerMethodField()
#
#     def __init__(self, *args, **kwargs):
#         super(InitialAgentListSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = InitialAgentModel
#         fields = "__all__"
#
#     def get_agent_category(self, obj):
#         agent_category = obj.agent_category
#         return {
#             "id": agent_category.id,
#             "name": agent_category.name
#         }
#
#     def get_basic_agent(self, obj):
#         if obj.basic_agent == 0:
#             return None
#         ss = BasicAgentModel.objects.get(id=obj.basic_agent)
#         return {
#             "id": obj.basic_agent,
#             "name": ss.name
#         }
#
#     def get_avatar(self, obj):
#         styles = ['identicon', 'monsterid', 'wavatar']
#         size = 256
#         random_str = str(obj.name)
#         m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
#         url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
#         return url
#
#
# class CreateInitialAgentSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(CreateInitialAgentSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = InitialAgentModel
#         fields = "__all__"
#
#
# class InitialAgentInfoSerializer(serializers.ModelSerializer):
#     avatar = serializers.SerializerMethodField()
#     in_docker = serializers.SerializerMethodField()
#     belong_to = serializers.SerializerMethodField()
#     behaviours = serializers.SerializerMethodField()
#     agent_category = serializers.SerializerMethodField()
#     agent_configuration = serializers.SerializerMethodField()
#     behaviour_configuration = serializers.SerializerMethodField()
#     basic_agent = serializers.SerializerMethodField()
#
#     def __init__(self, *args, **kwargs):
#         super(InitialAgentInfoSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = InitialAgentModel
#         fields = "__all__"
#
#     def get_belong_to(self, obj):
#         user = obj.belong_to
#         return {
#             "id": user.id,
#             "name": str(user)
#         }
#
#     def get_agent_category(self, obj):
#         agent_category = obj.agent_category
#         return {
#             "id": agent_category.id,
#             "name": agent_category.name
#         }
#
#     def get_behaviours(self, obj):
#         ret = obj.behaviours
#         temp = []
#         for i in ret:
#             behaviour_name = BehaviourModel.objects.get(id=i).name
#             temp.append({"id": i, "name": behaviour_name})
#         return temp
#
#     def get_agent_configuration(self, obj):
#         ss = AgentConfigurationSerializer(obj.agent_configuration)
#         return ss.data
#
#     def get_behaviour_configuration(self, obj):
#         ss = BehaviourConfigurationSerializer(obj.behaviour_configuration)
#         return ss.data
#
#     def get_basic_agent(self, obj):
#         """
#             Agent Tree
#         :param obj:
#         :return:
#         """
#         tree_node = {
#             "name": obj.basic_agent.name,
#             "id": obj.basic_agent.id,
#         }
#         return tree_node
#
#     def get_in_docker(self, obj):
#         if obj.basic_agent.in_docker:
#             return True
#         return False
#
#     def get_avatar(self, obj):
#         styles = ['identicon', 'monsterid', 'wavatar']
#         size = 256
#         random_str = str(obj.name)
#         m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
#         url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
#         return url


# class BuildAgentByIdSerializer(InitialAgentInfoSerializer):
#     is_active = serializers.ReadOnlyField()
#     auth_token = serializers.SerializerMethodField()
#
#     def __init__(self, *args, **kwargs):
#         super(BuildAgentByIdSerializer, self).__init__(*args, **kwargs)
#
#     def get_behaviours(self, obj):
#         ret = obj.behaviours.all()
#         default_behaviours = obj.basic_agent.default_behaviours
#         temp = {}
#         for behaviour in ret:
#             if behaviour.id in default_behaviours:
#                 continue
#             behaviour_name = behaviour.name
#             behaviour_url = behaviour.url
#             behaviour_category = behaviour.behaviour_category
#             download_url = "wise_agent/behaviours/{}/{}".format(behaviour_category, behaviour_name)
#             import_url = "wise_agent.behaviours.{}.{}".format(behaviour_category, behaviour_name)
#             data = {
#                 "name": behaviour_name,
#                 "download_url": download_url,
#                 "request_url": behaviour_url,
#                 "import_url": import_url,
#
#             }
#             temp[behaviour.id] = data
#         return temp
#
#     def get_basic_agent(self, obj):
#         tree_node = {
#             "id": obj.basic_agent.id,
#             "name": obj.basic_agent.name,
#             "url": obj.basic_agent.url,
#         }
#         return tree_node
#
#     def get_auth_token(self, obj):
#         user = obj.belong_to
#         return user.certificate
