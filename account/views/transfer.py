from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import TransactionSerializer
from ..models import Transaction, UserProfile as User
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsUserOrReadOnly

class CreateTransaction(APIView):

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def post(self, request):

        try:
            parsed_data = request.data

            if not parsed_data.get('acc'):
                return Response(
                    {
                        'message': 'Receiver account number is required',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            receiver = User.objects.get(acc_no=parsed_data['acc'])

            if not receiver:
                return Response(
                    {
                        'message': 'Receiver not found',
                        'status': False,
                        'statusCode': status.HTTP_404_NOT_FOUND
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            parsed_data['sender'] = User.objects.get(pk=request.user.id)
            parsed_data['receiver'] = receiver

        except:
            return Response(
                {
                    'message': 'Receiver not found',
                    'status': False,
                    'statusCode': status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(data=parsed_data)
        if serializer.is_valid():

            if parsed_data['sender'].wallet_balance < serializer.validated_data['amount']:
                return Response(
                    {
                        'message': 'Insufficient funds',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.validated_data['sender'] = User.objects.get(pk=request.user.id)
            parsed_data['sender'].wallet_balance -= serializer.validated_data['amount']
            parsed_data['sender'].save()

            receiver = serializer.validated_data['receiver']
            receiver.wallet_balance += serializer.validated_data['amount']
            receiver.save()

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
        
        transactions = Transaction.objects.filter(sender=request.user)
        if not transactions:
            return Response(
                {
                    'message': 'No transactions found',
                    'status': False,
                    'statusCode': status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )

        transactions = TransactionSerializer(transactions, many=True)

        transactions_data = {
            'transactions': transactions.data,
            'status': True,
            'statusCode': status.HTTP_200_OK
        }
        return Response(transactions_data, status=status.HTTP_200_OK)
