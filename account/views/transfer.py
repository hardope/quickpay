from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import TransactionSerializer
from ..models import Transaction, UserProfile as User
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsUserOrReadOnly
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate

class CreateTransaction(APIView):

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def post(self, request):

        try:
            parsed_data = request.data

            if not parsed_data.get('pin'):
                return Response(
                    {
                        'message': 'No Pin',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            pin = User.objects.get(id=request.user.id).pin

            if pin != parsed_data['pin']:
                return Response(
                    {
                        'message': 'Invalid Pin',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

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
                    'message': 'Invalid Account Number',
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
        
        transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        if not transactions:
            return Response(
                {
                    'message': 'No transactions found',
                    'status': False,
                    'statusCode': status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )

        all = []

        for i in transactions:

            all.append(
                {
                    'sender': i.sender.username,
                    'receiver': i.receiver.username,
                    'amount': i.amount,
                    'created_at': datetime.datetime.strftime(i.created_at, '%Y-%m-%d'),
                }
            )

        transactions_data = {
            'transactions': all,
            'status': True,
            'statusCode': status.HTTP_200_OK
        }
        return Response(transactions_data, status=status.HTTP_200_OK)

class SetPaymentPin(APIView):

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def post(self, request):

        try:
            print(request.data['pin'])

            pin = int(request.data['pin'])
            if pin < 1000 or pin > 9999:
                return Response(
                    {
                        'message': 'Invalid pin',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            print(request.data.get('password'))

            if not(request.data.get('password')):
                return Response(
                    {
                        'message': 'Password required',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(username=request.user.username, password=request.data['password'])
            if not user:
                return Response(
                    {
                        'message': 'Invalid password',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(pk=request.user.id)
            user.pin = pin
            user.save()
            return Response(
                {
                    'message': 'Pin set successfully',
                    'status': True,
                    'statusCode': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'message': 'An error occurred',
                    'status': False,
                    'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )