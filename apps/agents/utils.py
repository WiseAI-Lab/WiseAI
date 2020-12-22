from agents.models import (
    BasicAgentsModel,
    BehavioursModel
)
from base.utils import get_model_object

get_basic_agent_model = get_model_object(BasicAgentsModel)
get_behaviour_model = get_model_object(BehavioursModel)
