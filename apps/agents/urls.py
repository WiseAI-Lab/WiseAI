from django.conf.urls import url

from agents import views
from agents.views import CategoryView

urlpatterns = [
    url(
        r"agent_configs",
        views.AgentConfigsView.as_view(),
        name="get_agent_configs",
    ), url(
        r"behaviour_configs",
        views.BehaviourConfigsView.as_view(),
        name="get_behaviour_configs",
    ),
    # -----------------------BasicAgent-------------------
    url(
        r"basic_agent_list",
        views.BasicAgentsListView.as_view(),
        name="get_basic_agent_list",
    ),
    url(
        r"basic_agent_info/(?P<agent_id>[0-9]+)",
        views.BasicAgentInfoView.as_view(),
        name="get_basic_agent_info",
    ),
    # -----------------------Behaviours------------------
    url(
        r"behaviour_list",
        views.BehaviourListView.as_view(),
        name="get_behaviour_list",
    ),
    url(
        r"behaviour_info/(?P<agent_id>[0-9]+)",
        views.BehaviourInfoView.as_view(),
        name="behaviour_info",
    ),
    # ----------------------InitialAgent---------------
    url(
        r"user_agent_list",
        views.UserAgentListView.as_view(),
        name="get_user_agent_list",
    ),
    url(
        r"user_agent_info/(?P<agent_id>[0-9]+)",
        views.UserAgentInfoView.as_view(),
        name="get_user_agent_info",
    ),
    #------------------Category-----------------
    url(
        r"categories",
        CategoryView.as_view(),
        name="get_category",
    ),
]
