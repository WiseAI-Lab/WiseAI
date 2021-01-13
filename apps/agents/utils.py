import hashlib
import random

from agents.models import (
    AgentRepositoryModel,
    AgentTopicModel,
    BehaviourRepositoryModel,
    BehaviourTopicModel
)
from base.utils import get_model_object

get_agent_repository_model = get_model_object(AgentRepositoryModel)
get_agent_topic_model = get_model_object(AgentTopicModel)
get_behaviour_repository_model = get_model_object(BehaviourRepositoryModel)
get_behaviour_topic_model = get_model_object(BehaviourTopicModel)


def generate_avatar(obj, only_string=False):
    styles = ['identicon', 'monsterid', 'wavatar']
    size = 256
    if only_string:
        random_str = str(obj)
    else:
        random_str = str(obj.name)
    m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
    url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
    return url
