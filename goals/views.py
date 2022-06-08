from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, Status, Comment
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True

        """ goal delete: Проставить ей статус «В архиве», и тогда она уйдет с доски."""
        for goal in list(Goal.objects.select_related().filter(category_id=instance.id)):
            goal.status = Status.archived
            goal.save()

        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    # queryset = Goal.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["title"]
    filterset_class = GoalDateFilter

    def get_queryset(self):


        self.queryset = Goal.objects.filter(user=self.request.user, is_deleted=False)


        return self.queryset


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["created"]
    ordering = ["-created"]
    search_fields = ["goal"]

    def get_queryset(self):
        request_goal = self.request.GET.get("goal", None)
        self.queryset = Comment.objects.all()
        if request_goal:
            self.queryset = self.queryset.filter(goal=request_goal)
        return self.queryset


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()



