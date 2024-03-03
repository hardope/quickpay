from rest_framework.views import APIView
from rest_framework import status
from ..serializers import UserSerializer
from rest_framework.response import Response
from ..utils.errors import compile_errors
from ..models import OTP, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import parse_token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CreateUser(APIView):

     serializer_class = UserSerializer

     def post(self, request):
          
          serializer = UserSerializer(data=request.data, context={'request': request})
          if serializer.is_valid():
               serializer.save()
               token = get_tokens_for_user(serializer.instance)
               token = parse_token(token)
               return Response(
                    {
                         'data': serializer.data,
                         'token': token,
                         'message': 'User created successfully',
                         'status': True,
                         'statusCode': status.HTTP_201_CREATED
                    },
                    status=status.HTTP_201_CREATED
               )
          return Response(
               {
                    'data': serializer.data,
                    'message': 'User not created',
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'errors': compile_errors(serializer.errors),
               },
               status=status.HTTP_400_BAD_REQUEST
          )

class VerifyUser(APIView):

     def post(self, request):

          try:
               username = request.data['username']
               otp = request.data['otp']
          except:
               return Response(
                    {
                         'status': False,
                         'message': 'Username and OTP required',
                         'StatusCode': '400'
                    },
                    status=status.HTTP_400_BAD_REQUEST
               )

          try:
               user = UserProfile.objects.get(username=username)
               otp = OTP.objects.get(user=user, code=otp, purpose='registration')
               user.is_active = True
               user.save()
               otp.delete()
               return Response(
                    {
                         'status': True,
                         'message': 'User verified successfully',
                         'StatusCode': '200'
                    },
                    status=status.HTTP_200_OK
               )
          except:
               return Response(
                    {
                         'status': False,
                         'message': 'Invalid OTP',
                         'StatusCode': '400'
                    },
                    status=status.HTTP_400_BAD_REQUEST
               )