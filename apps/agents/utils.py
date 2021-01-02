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
