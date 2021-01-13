from django.conf.urls import url
from agents import views

urlpatterns = [
    # -----------------------Agent-------------------
    url(
        r"search/",
        views.SearchList.as_view(),
        name="search",
    ),
    url(
        r"agent_repository/(?P<repository_id>[0-9]+)/topics",
        views.AgentTopicView.as_view(),
        name="get_agent_topic",
    ),
    url(
        r"agent_repository/(?P<repository_id>[0-9]+)/",
        views.AgentRepositoryView.as_view(),
        name="get_agent_repository",
    ),
    # -----------------------Behaviours------------------
    url(
        r"behaviour_repository/(?P<repository_id>[0-9]+)/topics",
        views.BehaviourTopicView.as_view(),
        name="get_behaviour_topic",
    ),
    url(
        r"behaviour_repository/(?P<repository_id>[0-9]+)/",
        views.BehaviourRepositoryView.as_view(),
        name="get_behaviour_repository",
    ),
    # ------------------Category-----------------
    url(
        r"category",
        views.CategoryView.as_view(),
        name="get_category",
    ),
    # -----------------User Agent--------------
    url(
        r"user_agent_list",
        views.UserAgentListView.as_view(),
        name="get_user_agents",
    ),
    url(
        r"user_repository/(?P<repository_id>[0-9]+)/topics",
        views.UserAgentTopicListView.as_view(),
        name="get_user_topic",
    ),
    url(
        r"user_repository/(?P<repository_id>[0-9]+)/",
        views.UserAgentRepositoryInfoView.as_view(),
        name="get_user_repository",
    ),
    url(
        r"user_repository/",
        views.UserAgentRepositoryListView.as_view(),
        name="get_user_repositories",
    ),
    url(
        r"build_agent/(?P<topic_id>[0-9]+)/",
        views.BuildAgentView.as_view(),
        name="build_agent",
    ),
]
