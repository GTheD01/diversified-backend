from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from expense.serializers import ExpenseSerializer
from expense.models import Expense

# Expenses endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expenses(request):
    if request.method == "GET":
        user = request.user
        expenses = user.expense_set.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        label = request.data.get('label')
        price = request.data.get('price')

        # Sanitize and validate input
        if not label or not price:
            return Response({'error': 'Label and price are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure label contains only alphanumeric characters
        if not label.replace(" ", "").isalnum():
            return Response({'error': 'Label should contain only alphanumeric characters'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure price is a positive number
        try:
            price = float(price)
            if price <= 0:
                return Response({'error': 'Price should be a positive number'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid price format'}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.create(
            label = request.data['label'],
            price = request.data['price'],
            created_by = request.user
        )
        serializer = ExpenseSerializer(expense, many=False)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def expense(request, id):
    expense = Expense.objects.get(pk=id)
    if request.method == "PUT":
        expense.label = request.data['label']
        expense.price = request.data['price']
        expense.save()

        serializer = ExpenseSerializer(expense, many=False)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        expense.delete()
        return Response("Expense deleted")
