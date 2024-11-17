from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task.serializers import TaskSerializer
from task.models import Task


# Tasks endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks(request):
    if request.method == 'GET':
        user = request.user
        tasks = user.task_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        label = request.data.get('label')
        description = request.data.get('description')

        # Sanitize and validate input
        if not label or not description:
            return Response({'error': 'Label and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure label contains only alphanumeric characters
        if not label.replace(" ", "").isalnum():
            return Response({'error': 'Label should contain only alphanumeric characters'}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(
            label = label,
            description = description,
            created_by = request.user
        )
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task(request, id):
    task = Task.objects.get(pk=id)

    # Not used at the moment (Put)
    if request.method == "PUT":
        task.label = request.data['label']
        task.description = request.data['description']
        task.save()

        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        task.delete()
        return Response("Task deleted")
