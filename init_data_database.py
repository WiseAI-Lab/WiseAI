"""
    Generate some basic data and run "py manage.py createsuperuser" before.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
django.setup()

user_data = {
    'username': 'dongbox',
    'password': 'dongbox'
}

category_data = [
    {
        "name": "agent",
        "parent": 0,
        "type": 1
    },
    {
        "name": "behaviour",
        "parent": 0,
        "type": 2
    },
    {
        "name": "brain",
        "parent": 0,
        "type": 2
    }, {
        "name": "transport",
        "parent": 0,
        "type": 2
    },
]

category_data_new = {
    "name": "visbb",
    "parent": 1,
    "type": 2
}
visbb_repository_behaviour = {
    "name": "FlaskVisualizationBrainBehaviour",
    "owner": 1,
    "description": "It's a Flask Visualization brain behaviour",
    "configuration_template": 2,
    "is_verify": True,
    "is_private": False,
    "is_mirror": False,
    "is_office": True,
    "num_watches": 0,
    "num_stars": 0,
    "status": 1,
    "category": 5,
    "is_template": True,
    "template_id": 1
}
# 1: base, 2: brain, 3: transport
behaviour_repository_data = [
    {
        "name": "BrainBehaviour",
        "owner": 1,
        "description": "It's a Basic brain behaviour",
        "configuration_template": 2,
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
        "configuration_template": 2,
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
        "configuration_template": 2,
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
        "configuration_template": 2,
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
    "name": "v1",
    "configuration": 1,
    "description": "Version of Behaviour",
    "url": "https://wise.agent",  # Download path
    "status": 1,
    "store_type": 2,
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
        "store_type": 2,
    }
]


def generate_category(data):
    from agents.serilizers import CategorySerializer

    agent_configs = CategorySerializer(data=data)
    if agent_configs.is_valid():
        agent_configs.save()
        print("save {} into Table: Category".format(data))


def generate_config(data):
    from agents.models import ConfigurationModel

    config = ConfigurationModel(**data)
    config.save()
    print("save {} into Table: Configuration".format(config))


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
    from accounts.serializers import ProfileSerializer
    user = ProfileSerializer(data=data)
    if user.is_valid():
        user.save()
        print("save {} into Table: UserRegister".format(data))
    else:
        print(user.errors)


def main():
    create_user(user_data)
    for d in category_data:
        generate_category(d)
    # configuration
    import json
    path = "example_launch_config.json"
    with open(path, 'r') as f:
        content = json.load(f)
    configuration = content.get("configuration")
    config_data = {
        "name": "agent-configuration-template",
        "content": configuration,
        # "required_content": behaviours
    }
    generate_config(config_data)
    behaviours = content.get("behaviours").get("FlaskVisualizationBrainBehaviour").get("configuration")
    config_data = {
        "name": "behaviour-configuration-template",
        "content": behaviours,
        # "required_content": behaviours
    }
    generate_config(config_data)
    for d in behaviour_repository_data:
        generate_behaviour(d)
    for d in agent_repository_data:
        generate_agent(d)

    generate_category(category_data_new)
    generate_behaviour(visbb_repository_behaviour)


if __name__ == '__main__':
    main()
