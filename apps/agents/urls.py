from django.conf.urls import url
from agents import views

urlpatterns = [
    # -----------------------Agent-------------------
    url(
        r"search",
        views.SearchList.as_view(),
        name="search",
    ),
    url(
        r"agent_repository/(?P<agent_id>[0-9]+)/",
        views.AgentRepositoryView.as_view(),
        name="get_agent_repository",
    ),
    url(
        r"agent_repository/(?P<agent_id>[0-9]+)/topics",
        views.AgentTopicView.as_view(),
        name="get_agent_topic",
    ),
    # -----------------------Behaviours------------------
    url(
        r"behaviour_repository/(?P<agent_id>[0-9]+)/",
        views.BehaviourRepositoryView.as_view(),
        name="get_behaviour_repository",
    ),
    url(
        r"behaviour_repository/(?P<agent_id>[0-9]+)/topics",
        views.BehaviourTopicView.as_view(),
        name="get_behaviour_topic",
    ),
    # ------------------Category-----------------
    url(
        r"categories",
        views.CategoryView.as_view(),
        name="get_category",
    ),
    # -----------------Build Agent--------------
]
