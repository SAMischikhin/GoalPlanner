from rest_framework import serializers

from core.models import User
from core.serializers import UserRegistrationSerializer, UserModelSerializer
from goals.models import GoalCategory, Goal, Comment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    def create(self, validated_data):
        validated_data["category"] = self.validate_category(validated_data["category"])
        goal = Goal.objects.create(**validated_data)
        return goal

    class Meta:
        model = Goal
        exclude = ('is_deleted',)
        read_only_fields = ("created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        """На карточке: title, priority, due_date, category"""
        model = Goal
        exclude = ('is_deleted',)
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ("created", "updated", "user")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ("created", "updated", "user", "goal")
        fields = "__all__"
