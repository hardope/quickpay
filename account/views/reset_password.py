from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from comms.reset import send_reset_password_email
from ..models import UserProfile as User, OTP
from django.contrib.auth.password_validation import validate_password
import datetime
from datetime import timezone

class PasswordResetView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = User.objects.get(id=request.user.id)
        OTP.objects.filter(user=user, purpose='password_reset').delete()
        new_code = OTP.objects.create(user=user, purpose='password_reset')
        send_reset_password_email(user, new_code.code)
        return Response(
            {
                'message': 'Authentication Code Sent',
                'status': True,
                'statusCode': status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):

        user = User.objects.get(id=request.user.id)

        if request.data.get('password', False) and request.data.get('code', False):

            try:
                validate_password(request.data['password'])

                try:
                    code = OTP.objects.get(user=user, purpose='password_reset')
                    print("Trying")
                    assert code.created_at + datetime.timedelta(minutes=30) > datetime.datetime.now(tz=timezone.utc)
                    print(code.code, request.data['code'])
                    if code.code == request.data['code']:
                        code.delete()
                        user.set_password(request.data['password'])
                        user.save()
                        print("Saved")
                        return Response(
                            {
                                'message': 'Password Reset Successful',
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
                            'message': 'Authentication Code Expired',
                            'status': False,
                            'statusCode': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except Exception as e:
                return Response(
                    {
                        'message': 'Invalid Password',
                        'errors': e.messages,
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            

        else:
            return Response(
                {
                    'message': 'Authentication Code and New Password are required',
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ForgotPasswordView(APIView):

    def post(self, request):

        if request.data.get('email', False):

            try:
                user = User.objects.get(email=request.data['email'])
                OTP.objects.filter(user=user, purpose='password_reset').delete()
                new_code = OTP.objects.create(user=user, purpose='password_reset')
                send_reset_password_email(user, new_code.code)
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
                        'message': 'Invalid Email Address',
                        'status': False,
                        'statusCode': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'message': 'Email Address is required',
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )