from rest_framework import serializers
from .models import Task, TaskList


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('deleted_at',)


class TaskListSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('get_tasks_from_list')

    def get_tasks_from_list(self, tasklist):
        list_tasks = Task.objects.filter(deleted_at=None, list_id=tasklist.pk)
        serializer = TaskSerializer(list_tasks, many=True)
        return map(lambda x: {k: v for k, v in x.items() if k != 'list_id'}, serializer.data)

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'completion_percentage', 'tasks', 'creator', 'created_at', 'updated_at')