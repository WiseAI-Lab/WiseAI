"""
    Generate some basic data and run "py manage.py createsuperuser" before.
"""
import copy
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
django.setup()

config = {
    "name": "Empty",
    "content": {
        "version": "v1",
        "feature": ["Test"],
        "pool_size": 0,
        "is_process": True
    }
}
user_data = {
    'username': 'dongbox',
    'password': 'dongbox'
}

category_data = [
    {
        "name": "online",
        "parent": 0,
        "type": 1
    }, {
        "name": "offline",
        "parent": 0,
        "type": 1
    }, {
        "name": "brain",
        "parent": 0,
        "type": 2
    }, {
        "name": "transport",
        "parent": 0,
        "type": 2
    },
]
# 1: base, 2: brain, 3: transport
behaviour_repository_data = [
    {
        "name": "BrainBehaviour",
        "owner": 1,
        "description": "It's a Basic brain behaviour",
        "configuration_template": 1,
        "is_verify": True,
        "is_private": False,
        "is_mirror": False,
        "is_office": True,
        "num_watches": 0,
        "num_stars": 0,
        "status": 1,
        "category": 3,
        "is_template": False,
        "template_id": 0
    },
    {
        "name": "TransportBehaviour",
        "category": 4,
        "owner": 1,
        "description": "It's a Basic Transport behaviour",
        "configuration_template": 1,
        "is_verify": True,
        "is_private": False,
        "is_mirror": False,
        "is_office": True,
        "num_watches": 0,
        "num_stars": 0,
        "status": 1,
        "is_template": True,
        "template_id": 0
    },
    {
        "name": "MessageQueueTransportBehaviour",
        "category": 4,
        "owner": 1,
        "description": "It's a message queue transport behaviour",
        "configuration_template": 1,
        "is_verify": True,
        "is_private": False,
        "is_mirror": False,
        "is_office": True,
        "num_watches": 0,
        "num_stars": 0,
        "status": 1,
        "is_template": True,
        "template_id": 2
    },
    {
        "name": "ConfluentKafkaMessageQueueTransportBehaviour",
        "category": 4,
        "owner": 1,
        "description": "It's a confluent-kafka message queue transport behaviour",
        "configuration_template": 1,
        "is_verify": True,
        "is_private": False,
        "is_mirror": False,
        "is_office": True,
        "num_watches": 0,
        "num_stars": 0,
        "status": 1,
        "is_template": False,
        "template_id": 3
    },
]

behaviour_topic_data = {
    "name": "0.1",
    "configuration": 1,
    "description": "Version of Behaviour",
    "url": "https://wise.agent",  # Download path
    "status": 1,
}

agent_repository_data = [
    {
        "name": "BasicAgent",
        "category": 1,
        "owner": 1,
        "description": "It's a Basic Agent that contains Offline And OnlineAgent",
        "configuration_template": 1,
        "is_verify": True,
        "is_private": False,
        "is_mirror": False,
        "is_office": True,
        "num_watches": 0,
        "num_stars": 0,
        "status": 1,
        "is_template": True,
        "template_id": 0
    },
]

agent_topics_data = [
    {
        "name": "v1",
        "behaviours": [1],
        "configuration": 1,
        "description": "Version of Basic Agent",
        "url": "https://wise.agent",  # Download url
        "status": 1,
    }
]


def generate_category(data):
    from agents.serilizers import CategorySerializer

    agent_configs = CategorySerializer(data=data)
    if agent_configs.is_valid():
        agent_configs.save()
        print("save {} into Table: Category".format(data))


def generate_config():
    from agents.models import ConfigurationModel

    data = ConfigurationModel(**config)
    data.save()
    print("save {} into Table: Configuration".format(data))


def generate_behaviour(data):
    from agents.serilizers import CreateBehaviourRepositorySerializer, CreateBehaviourTopicSerializer
    from agents.utils import generate_avatar

    avatar = data.get("avatar", None)
    if not avatar:
        data["avatar"] = generate_avatar(data.get("name"), only_string=True)
    serializer = CreateBehaviourRepositorySerializer(data=data)
    serializer.is_valid(raise_exception=True)
    model = serializer.save()

    serializer = CreateBehaviourTopicSerializer(data=behaviour_topic_data)
    serializer.is_valid(raise_exception=True)
    topic_model = serializer.save()
    model.topics.add(topic_model)

    print("save {} into Table: Behaviours".format(data))


def generate_agent(data):
    from agents.serilizers import CreateAgentRepositorySerializer, CreateAgentTopicSerializer
    from agents.utils import generate_avatar

    avatar = data.get("avatar", None)
    if not avatar:
        data["avatar"] = generate_avatar(data.get("name"), only_string=True)
    serializer = CreateAgentRepositorySerializer(data=data)
    serializer.is_valid(raise_exception=True)
    model = serializer.save()

    serializer = CreateAgentTopicSerializer(data=agent_topics_data[0])
    serializer.is_valid(raise_exception=True)
    topic_model = serializer.save()
    model.topics.add(topic_model)
    print("save {} into Table: Agents".format(data))


def create_user(data):
    from accounts.serializers import UserRegisterSerializer
    user = UserRegisterSerializer(data=data)
    if user.is_valid():
        user.save()
        print("save {} into Table: UserRegister".format(data))
    else:
        print(user.errors)


def main():
    create_user(user_data)
    generate_config()
    for d in category_data:
        generate_category(d)
    for d in behaviour_repository_data:
        generate_behaviour(d)
    for d in agent_repository_data:
        generate_agent(d)


if __name__ == '__main__':
    main()
