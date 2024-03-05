from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import TransactionSerializer
from ..models import Transaction
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsUserOrReadOnly

class CreateTransaction(APIView):

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Transaction successful',
                    'transation': serializer.data,
                    'status': True,
                    'statusCode': status.HTTP_201_CREATED
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewTransactions(APIView):

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get(self, request):
        
        transactions = TransactionSerializer(Transaction.objects.filter(sender=request.user), many=True)
        transactions_data = {
            'transactions': transactions.data,
            'status': True,
            'statusCode': status.HTTP_200_OK
        }
        return Response(transactions_data, status=status.HTTP_200_OK)
