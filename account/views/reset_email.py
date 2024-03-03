from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from comms.reset import send_change_email
from ..models import UserProfile as User, OTP
from django.core.validators import validate_email
import datetime 
from datetime import timezone
from random import randint

class ChangeEmailView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        try:
            validate_email(request.data['email'])

            if User.objects.filter(email=request.data['email']).exists():
                return Response(
                    {
                        'message': 'Email Already Exists',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            user = User.objects.get(id=request.user.id)
            OTP.objects.filter(user=user, purpose='email_reset').delete()
            new_email_code = randint(100000, 999999)
            new_code = OTP.objects.create(user=user, purpose='email_reset', additional_data=f'{request.data["email"]} - {new_email_code}')
            send_change_email(user, new_code.code)
            user.email = request.data['email']
            send_change_email(user, new_email_code)
            return Response(
                {
                    'message': 'Authentication Code Sent',
                    'status': True,
                    'statusCode': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'message': 'Invalid Email',
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
            
            if request.data.get('code', False) and request.data.get('new-email-code', False):
    
                try:
                    user = User.objects.get(id=request.user.id)
                    otp = OTP.objects.get(user=user, purpose='email_reset', code=request.data['code'])
                    new_email_code = otp.additional_data.split(' - ')[1]
                    if otp.code == request.data['code'] and new_email_code == str(request.data['new-email-code']):
                        if otp.created_at < datetime.datetime.now(timezone.utc) - datetime.timedelta(minutes=30):
                            return Response(
                                {
                                    'message': 'Authentication Code Expired',
                                    'status': False,
                                    'statusCode': status.HTTP_400_BAD_REQUEST
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )   
                        user.email = otp.additional_data.split(' - ')[0]
                        otp.delete()
                        user.save()
                        return Response(
                            {
                                'message': 'Email Reset Successful',
                                'status': True,
                                'statusCode': status.HTTP_200_OK
                            },
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'message': 'Invalid Authentication Code',
                                'status': False,
                                'statusCode': status.HTTP_400_BAD_REQUEST
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except:
                    return Response(
                        {
                            'message': 'Invalid Authentication Code',
                            'status': False,
                            'statusCode': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'message': 'Authentication Code and New Email Code are required',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )