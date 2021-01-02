from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
# from rest_framework.decorators import api_view, permission_classes
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
    BehaviourTopicSerializer
)
from agents.utils import (
    get_agent_repository_model,
    get_agent_topic_model,
    get_behaviour_repository_model,
    get_behaviour_topic_model
)
from base.utils import paginated_queryset, PageNumberPaginatorInspectorClass


class SearchList(generics.ListAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(security=list(),
                         paginator_inspectors=[PageNumberPaginatorInspectorClass],
                         manual_parameters=[
                             openapi.Parameter(
                                 name="type",
                                 in_=openapi.IN_PATH,
                                 type=openapi.TYPE_STRING,
                                 description="`Agent` or `Behaviour`.",
                                 required=True,
                             ),
                             openapi.Parameter(
                                 name="category",
                                 in_=openapi.IN_PATH,
                                 type=openapi.TYPE_STRING,
                                 description="Default is `all`, filter the category with the type.",
                                 required=True,
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
        repository = cur_model.objects.filter(status=1)
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
    def get(self, request, agent_id: int) -> Response:
        try:
            agent_repository = AgentRepositoryModel.objects.get(
                pk=agent_id
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
    def get(self, request, agent_id):
        try:
            agent_repository = AgentRepositoryModel.objects.get(
                pk=agent_id
            )
        except AgentRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentTopicSerializer(data=agent_repository.topics, many=True)
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
    def get(self, request, agent_id: int) -> Response:
        try:
            behaviour_repository = BehaviourRepositoryModel.objects.get(
                pk=agent_id
            )
        except BehaviourRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = BehaviourTopicSerializer(behaviour_repository)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


class BehaviourTopicView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=list(),
        responses={200: AgentTopicSerializer(many=True)})
    def get(self, request, agent_id):
        try:
            behaviour_repository = BehaviourRepositoryModel.objects.get(
                pk=agent_id
            )
        except AgentRepositoryModel.DoesNotExist:
            response_data = {
                "error": "Repository doesn't exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = BehaviourTopicSerializer(data=behaviour_repository.topics, many=True)
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
        Return a list of all users.
        """
        data = request.GET
        if data.get("id") or data.get("name"):
            category_data = CategoryModel.objects.order_by("id")
            serializer = CategorySerializer(category_data)
            names = serializer.data
        else:
            names = [cate.name for cate in CategoryModel.objects.all()]

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

# ---------------------------Initial Agent--------------------
# class UserAgentListView(APIView):
#     def get(self, request):
#         agents = InitialAgentModel.objects.filter(belong_to=request.user)
#         paginator, result_page = paginated_queryset(agents, request)
#         serializer = InitialAgentListSerializer(
#             result_page, many=True
#         )
#         response_data = serializer.data
#         return paginator.get_paginated_response(response_data)


# class BuildAgentView(APIView):
#     def post(self, request, agent_id):
#         data = get_user_agent_model(agent_id)
#         serializer = BuildAgentByIdSerializer(data)
#         response_data = serializer.data
#         return Response(response_data, status=status.HTTP_200_OK)


# class UserAgentInfoView(APIView):
#     def post(self, request, agent_id):
#         agent = get_user_agent_model(agent_id)
#
#         serializer = InitialAgentInfoSerializer(agent)
#         response_data = serializer.data
#         return Response(response_data, status=status.HTTP_200_OK)
