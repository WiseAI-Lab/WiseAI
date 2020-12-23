from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.models import (
    AgentConfigsModel,
    BehaviourConfigsModel,
    CategoryModel,
    BasicAgentsModel,
    BehavioursModel, InitialAgentsModel
)
from agents.serilizers import (
    CategorySerializer,
    AgentConfigsSerializer,
    BehaviourConfigsSerializer,
    BasicAgentsListSerializer,
    BasicAgentsInfoSerializer,
    BehaviourInfoSerializer,
    BehaviourListSerializer, InitialAgentListSerializer, InitialAgentInfoSerializer
)
from agents.utils import get_basic_agent_model, get_behaviour_model, get_user_agent_model
from base.utils import paginated_queryset


# ----------------------------BasicAgent-----------------------
# The first page is all basic agents and filter
class BasicAgentsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        basic_agents = BasicAgentsModel.objects.order_by("id")
        paginator, result_page = paginated_queryset(basic_agents, request)
        serializer = BasicAgentsListSerializer(
            result_page, many=True
        )
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)


# show basic_agent info by agent_id
class BasicAgentInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, agent_id):
        agent = get_basic_agent_model(agent_id)

        serializer = BasicAgentsInfoSerializer(agent)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


# ---------------------------Initial Agent--------------------
class UserAgentListView(APIView):
    def get(self, request):
        agents = InitialAgentsModel.objects.filter(belong_to=request.user)
        paginator, result_page = paginated_queryset(agents, request)
        serializer = InitialAgentListSerializer(
            result_page, many=True
        )
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)


class UserAgentInfoView(APIView):
    def get(self, request, agent_id):
        agent = get_user_agent_model(agent_id)

        serializer = InitialAgentInfoSerializer(agent)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


# -------------------Behaviour-----------------------------
# behaviour list
class BehaviourListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        behaviours = BehavioursModel.objects.order_by("id")
        paginator, result_page = paginated_queryset(behaviours, request)
        serializer = BehaviourListSerializer(
            result_page, many=True
        )
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)


# behaviour info
class BehaviourInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, behaviour_id):
        behaviour = get_behaviour_model(behaviour_id)

        serializer = BehaviourInfoSerializer(behaviour)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


# The fourth page is to create a initial basic_agent.


class AgentConfigsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return a list of all users.
        """
        data = request.data
        if data.get("id"):
            category_data = AgentConfigsModel.objects.order_by("id")
            names = category_data.name
        else:
            names = [cate.name for cate in CategoryModel.objects.all()]

        return Response(names, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AgentConfigsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BehaviourConfigsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return a list of all users.
        """
        data = request.data
        if data.get("id"):
            category_data = BehaviourConfigsModel.objects.order_by("id")
            names = category_data.name
        else:
            names = [cate.name for cate in CategoryModel.objects.all()]

        return Response(names, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BehaviourConfigsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return a list of all users.
        """
        data = request.data
        if data.get("id") or data.get("name"):
            category_data = CategoryModel.objects.order_by("id")
            serializer = CategorySerializer(category_data)
            names = serializer.data
        else:
            names = [cate.name for cate in CategoryModel.objects.all()]

        return Response(names, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
