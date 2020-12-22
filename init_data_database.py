"""
    Generate some basic data and run "py manage.py createsuperuser" before.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
django.setup()
from agents.models import CategoryModel

empty_configs_data = {
    "name": "empty",
    "extend": "{}",
    "is_base": True
}
user_data = {
    'username': 'dongbox',
    'password': 'dongbox'
}
category_data = [
    {
        "name": "agent",
        "parent": 0,
        "type": 1
    }, {
        "name": "online",
        "parent": 1,
        "type": 1
    }, {
        "name": "offline",
        "parent": 1,
        "type": 1
    }, {
        "name": "behaviour",
        "parent": 0,
        "type": 2
    }, {
        "name": "brain",
        "parent": 4,
        "type": 2
    }, {
        "name": "transport",
        "parent": 4,
        "type": 2
    },
]
# 1: base, 2: brain, 3: transport
behaviour_data = [
    {
        "name": "BaseBehaviour",
        "parent_behaviour": 0,
        "behaviour_category": 2,
        "url": "",
        "author": 1,
        "description": "It's a base behaviour for all.",
        "is_office": True,
        "configs": 1
    },
    {
        "name": "BrainBehaviour",
        "parent_behaviour": 1,
        "behaviour_category": 3,
        "author": 1,
        "description": "It's a brain behaviour",
        "is_office": True,
        "configs": 1
    }, {
        "name": "TransportBehaviour",
        "parent_behaviour": 1,
        "behaviour_category": 4,
        "url": "",
        "author": 1,
        "description": "It's a transport behaviour",
        "is_office": True,
        "configs": 1
    },
    # {
    #     "name": "MessageQueueTransportBehaviour",
    #     "parent_behaviour": 3,
    #     "behaviour_category": 4,
    #     "url": "",
    #     "author": 1,
    #     "description": "It's a message queue transport behaviour",
    #     "is_office": True,
    #     "configs": 1
    # }, {
    #     "name": "ConfluentKafkaMessageQueueTransportBehaviour",
    #     "parent_behaviour": 3,
    #     "behaviour_category": 4,
    #     "url": "",
    #     "author": 1,
    #     "description": "It's a confluent-kafka message queue transport behaviour",
    #     "is_office": True,
    #     "configs": 1
    # },
]

agent_data = [
    {
        "name": "BaseAgent",
        "prerequisite_behaviour_categories": [5],
        "default_behaviours": [2],
        "parent_agent": 0,
        "agent_category": 1,
        "url": "",
        "description": "It's the base agent for all agent.",
        "is_office": True,
        "in_docker": False,
        "author": 1,
        "configs": 1
    }, {
        "name": "OfflineAgent",
        "prerequisite_behaviour_categories": [5],
        "default_behaviours": [2],
        "parent_agent": 1,
        "agent_category": 1,
        "url": "",
        "description": "It's the offline agent.",
        "is_office": True,
        "in_docker": False,
        "author": 1,
        "configs": 1
    },
    {
        "name": "OnlineAgent",
        "prerequisite_behaviour_categories": [5, 6],
        "default_behaviours": [2, 3],
        "parent_agent": 1,
        "agent_category": 1,
        "url": "",
        "description": "It's the online agent.",
        "is_office": True,
        "in_docker": False,
        "author": 1,
        "configs": 1
    },

]


def generate_agent_config(data):
    from agents.serilizers import AgentConfigsSerializer

    agent_configs = AgentConfigsSerializer(data=data)
    if agent_configs.is_valid():
        agent_configs.save()
        print("save {} into Table: AgentConfigs".format(data))


def generate_behaviour_config(data):
    from agents.serilizers import BehaviourConfigsSerializer

    agent_configs = BehaviourConfigsSerializer(data=data)
    if agent_configs.is_valid():
        agent_configs.save()
        print("save {} into Table: BehaviourConfigs".format(data))


def generate_category(data):
    from agents.serilizers import CategorySerializer

    agent_configs = CategorySerializer(data=data)
    if agent_configs.is_valid():
        agent_configs.save()
        print("save {} into Table: Category".format(data))


def generate_behaviour(data):
    from agents.serilizers import CreateBehaviourSerializer

    behaviours = CreateBehaviourSerializer(data=data)
    if behaviours.is_valid():
        behaviours.save()
        print("save {} into Table: Behaviours".format(data))
    else:
        print(behaviours.errors)


def generate_agent(data):
    from agents.serilizers import CreateBasicAgentSerializer

    agents = CreateBasicAgentSerializer(data=data)
    if agents.is_valid():
        agents.save()
        print("save {} into Table: BasicAgents".format(data))
    else:
        print(agents.errors)


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
    generate_agent_config(empty_configs_data)
    generate_behaviour_config(empty_configs_data)
    for d in category_data:
        generate_category(d)
    for d in behaviour_data:
        generate_behaviour(d)
    for d in agent_data:
        generate_agent(d)


if __name__ == '__main__':
    main()
