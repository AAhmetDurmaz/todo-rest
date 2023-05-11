from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q
from .serializers import TaskSerializer, TaskListSerializer
from .models import Task, TaskList
from django.utils import timezone 
from django.utils.dateparse import parse_date


class TaskListView(APIView):
    def get(self, request):
        try:
            conditions = Q(deleted_at=None)
            name = self.request.query_params.get('name')
            orderby = self.request.query_params.get('orderby')
            created_at_start = self.request.query_params.get('created_at_start')
            created_at_end = self.request.query_params.get('created_at_end')

            if name:
                conditions &= Q(name__icontains=name)
            if created_at_start and created_at_end:
                start_date = parse_date(created_at_start)
                end_date = parse_date(created_at_end)
                conditions &= Q(created_at__range=(start_date, end_date))
            task_lists = TaskList.objects.filter(conditions)

            if orderby in ['asc', 'desc']:
                task_lists = task_lists.order_by(f'-name' if orderby == 'desc' else 'name')
                
        except TaskList.DoesNotExist:
            raise Http404("Not found.")
        serializer = TaskListSerializer(task_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListDetailsView(APIView):
    def get(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task_lists = TaskList.objects.get(conditions)
        except TaskList.DoesNotExist:
            raise Http404("Not found.")
        serializer = TaskListSerializer(task_lists, many=False)
        return Response(serializer.data)

    def put(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task = TaskList.objects.get(conditions)
        except TaskList.DoesNotExist:
            raise Http404("Not found.")
        serializer = TaskListSerializer(
            instance=task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task_list = TaskList.objects.get(conditions)
        except TaskList.DoesNotExist:
            raise Http404("Not found.")
        task_list.soft_delete()
        conditions = Q(list_id=uuid, deleted_at=None)
        tasks = Task.objects.filter(conditions)
        tasks.update(deleted_at=timezone.now())
        return Response({
            "success": True,
            "message": "List deleted successfully."
        }, status=status.HTTP_200_OK)


class TaskView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        try:
            if serializer.is_valid():
                TaskList.objects.get(
                    creator=self.request.user.id, id=serializer.validated_data.get('list_id'))
        except TaskList.DoesNotExist:
            return Response({'message': 'Unauthorized.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            serializer.save(creator=self.request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailsView(APIView):
    def get(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task = Task.objects.get(conditions)
        except Task.DoesNotExist:
            raise Http404("Not found.")
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task = Task.objects.get(conditions)
        except Task.DoesNotExist:
            raise Http404("Not found.")
        serializer = TaskSerializer(
            instance=task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        try:
            conditions = Q(id=uuid, deleted_at=None)
            task = Task.objects.get(conditions)
        except Task.DoesNotExist:
            raise Http404("Not found.")
        task.soft_delete()
        return Response({
            "success": True,
            "message": "Task deleted successfully."
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def apiOverview(request):
    url = request.build_absolute_uri()
    api_urls = {
        "lists": url + "list",
        "tasks": url + "task",
        "login": url + "auth/login",
        "register": url + "auth/register",
        "user": url + "auth/user"
    }
    return Response(api_urls)
