from django.db.models.query import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.inspectors.query import DjangoRestResponsePagination
from agents.models import (
    CategoryModel,
    AgentTopicModel,
    AgentRepositoryModel,
    BehaviourTopicModel,
    BehaviourRepositoryModel
)
from agents.serilizers import (
    CategorySerializer,
    AgentRepositorySerializer,
    RepositorySerializer,
    AgentTopicSerializer,
    BehaviourRepositorySerializer,
    BehaviourTopicSerializer, BuildAgentByIdSerializer
)

from base.utils import paginated_queryset, PageNumberPaginatorInspectorClass


# ---------------- Common---------------------
class SearchList(generics.ListAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(security=list(),
                         paginator_inspectors=[PageNumberPaginatorInspectorClass],
                         manual_parameters=[
                             openapi.Parameter(
                                 name="type",
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING,
                                 description="`Agent` or `Behaviour`.",
                                 required=True,
                             ),
                             openapi.Parameter(
                                 name="category",
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING,
                                 description="Default is `all`, filter the category with the type.",
                                 required=False,
                             ),
                         ],
                         responses={status.HTTP_200_OK: openapi.Response(
                             description="",
                             schema=openapi.Schema(
                                 type=openapi.TYPE_OBJECT,
                                 properties={
                                     "count": openapi.Schema(
                                         type=openapi.TYPE_STRING,
                                         description="Count of values on the leaderboard",
                                     ),
                                     "next": openapi.Schema(
                                         type=openapi.TYPE_STRING,
                                         description="URL of next page of results",
                                     ),
                                     "previous": openapi.Schema(
                                         type=openapi.TYPE_STRING,
                                         description="URL of previous page of results",
                                     ),
                                     "results": openapi.Schema(
                                         type=openapi.TYPE_ARRAY,
                                         description="Array of results object",
                                         items=openapi.Schema(
                                             type=openapi.TYPE_OBJECT,
                                             properties={
                                                 "name": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Repository Name.",
                                                 ),
                                                 "category": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Category for this Repository.",
                                                 ),
                                                 "description": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Introduce basic information for this "
                                                                 "repository and give a abstract.",
                                                 ),
                                                 "owner": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Owner for this repository.",
                                                 ),
                                                 "configuration_template": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Basic configuration.",
                                                 ),
                                                 "is_verify": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="When user upload that our officer will check it and "
                                                                 "set it verify if correct as say.",
                                                 ),
                                                 "is_private": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="Private or Public.",
                                                 ),
                                                 "is_archived": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="Not update(maybe static) and archived.",
                                                 ),
                                                 "is_mirror": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="Docker exist or not.",
                                                 ),
                                                 "is_office": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="Weather office or user.",
                                                 ),
                                                 "num_watches": openapi.Schema(
                                                     type=openapi.TYPE_INTEGER,
                                                     description="Number of watch.",
                                                 ),
                                                 "num_stars": openapi.Schema(
                                                     type=openapi.TYPE_INTEGER,
                                                     description="Number of star.",
                                                 ),
                                                 "is_template": openapi.Schema(
                                                     type=openapi.TYPE_BOOLEAN,
                                                     description="Whether template or other.",
                                                 ),
                                                 "avatar": openapi.Schema(
                                                     type=openapi.TYPE_STRING,
                                                     description="Avatar for this repository.",
                                                 ),
                                             },
                                         ),
                                     )}
                             )
                         )}
                         )
    def get(self, request):
        data = request.GET
        type = data.get('type')
        category = data.get('category')
        if type is None:
            response_data = {
                "error": "Bad Request."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Check the category
        category_check = None
        if category and category != 'all':
            category_check = CategoryModel.objects.filter(name=category)
            if not category_check:
                response_data = {
                    "error": f"Bad Request."
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # Check the type, then confirm the model and serializer.
        if type == "agent":
            cur_model = AgentRepositoryModel
            cur_serializer = AgentRepositorySerializer
        elif type == "behaviour":
            cur_model = BehaviourRepositoryModel
            cur_serializer = BehaviourRepositorySerializer
        else:
            response_data = {
                "error": "Bad Request."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        # Get the data from database.
        repository = cur_model.objects.filter(status=1, is_private=False)
        if category and category != 'all':
            repository = repository \
                .filter(category__in=category_check) \
                .order_by("id")
        else:
            repository = repository.order_by("id")
        # Paginate
        paginator, result_page = paginated_queryset(repository, request)
        serializer = cur_serializer(
            result_page, many=True
        )
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)


# -----------------Agent-----------------------

class AgentRepositoryView(APIView):
    """
        Get the Agent repository list.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(security=list(),
                         paginator_inspectors=[PageNumberPaginatorInspectorClass],
                         responses={200: AgentRepositorySerializer(many=True)})
    def get(self, request, repository_id: int) -> Response:
        try:
            agent_repository = AgentRepositoryModel.objects.get(
                pk=repository_id
            )
        except AgentRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = AgentRepositorySerializer(agent_repository)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


class AgentTopicView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=list(),
        responses={200: AgentTopicSerializer(many=True)})
    def get(self, request, repository_id):
        try:
            agent_repository = AgentRepositoryModel.objects.get(
                pk=repository_id
            )
        except AgentRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentTopicSerializer(agent_repository.topics, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


# -------------------Behaviour------------------
class BehaviourRepositoryView(APIView):
    """
        Get the Agent repository list.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(security=list(),
                         paginator_inspectors=[PageNumberPaginatorInspectorClass],
                         responses={200: BehaviourRepositorySerializer(many=True)})
    def get(self, request, repository_id: int) -> Response:
        try:
            behaviour_repository = BehaviourRepositoryModel.objects.get(
                pk=repository_id
            )
        except BehaviourRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = BehaviourRepositorySerializer(behaviour_repository)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


class BehaviourTopicView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=list(),
        responses={200: AgentTopicSerializer(many=True)})
    def get(self, request, repository_id):
        try:
            behaviour_repository = BehaviourRepositoryModel.objects.get(
                pk=repository_id
            )
        except BehaviourRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = BehaviourTopicSerializer(behaviour_repository.topics, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


# -------------------Category-------------------
class CategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=list(),
        responses={200: CategorySerializer(many=True)})
    def get(self, request):
        """
            Return category depend on request.
        """
        data = request.GET
        category_id = data.get("id")
        category_name = data.get("name")
        if category_id or category_name:
            if category_id:
                category_data = CategoryModel.objects.get(id=category_id)
            else:
                category_data = CategoryModel.objects.get(name=category_name)
            serializer = CategorySerializer(category_data)
            names = serializer.data
        else:
            category_data = CategoryModel.objects.all()
            serializer = CategorySerializer(category_data, many=True)
            names = serializer.data

        return Response(names, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        security=list(),
        responses={201: CategorySerializer()})
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------User Agent--------------------

class UserAgentRepositoryListView(APIView):
    def get(self, request):
        try:
            agents = AgentRepositoryModel.objects.filter(owner=request.user)
            topic_list = QuerySet()
            for a in agents:
                topics = a.topics.all()
                topic_list.union(topics)
            paginator, result_page = paginated_queryset(agents, request)
            serializer = AgentRepositorySerializer(
                result_page, many=True
            )
            response_data = serializer.data
            return paginator.get_paginated_response(response_data)
        except AgentRepositoryModel.DoesNotExist:
            error_data = {
                'error': 'Not Found.'
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)


class UserAgentRepositoryInfoView(APIView):
    def get(self, request, repository_id):
        try:
            agents = AgentRepositoryModel.objects.get(owner=request.user, id=repository_id)
            serializer = AgentRepositorySerializer(
                agents
            )
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        except AgentRepositoryModel.DoesNotExist:
            error_data = {
                'error': 'Not Found.'
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)


class UserAgentTopicListView(APIView):
    def get(self, request, repository_id):
        repository = AgentRepositoryModel.objects.get(id=repository_id, owner=request.user)
        topics = repository.topics.all()
        paginator, result_page = paginated_queryset(topics, request)
        serializer = AgentTopicSerializer(
            result_page, many=True
        )
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)


class UserAgentTopicInfoView(APIView):
    def get(self, request, topic_id):
        # TODO change here
        try:
            topic = AgentRepositoryModel.objects.filter(owner=request.user, topics_id=topic_id).first()
            serializer = AgentTopicSerializer(topic)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        except AgentRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Bad Found."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class BuildAgentView(APIView):
    def post(self, request, topic_id):
        repository = AgentRepositoryModel.objects.filter(topics__id=topic_id, owner=request.user)
        if not repository:
            error_data = {
                'error': "Sorry, you are not authorized for this Agent."
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        topic = AgentTopicModel.objects.get(id=topic_id)
        serializer = BuildAgentByIdSerializer(topic)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
