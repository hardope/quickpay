from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import UserProfile
from ..serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import parse_token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class Auth(APIView):

    def post(self, request):

        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response(
                {
                    'status': False,
                    'message': 'Username and password required',
                    'StatusCode': '400'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is not None:

            user = UserProfile.objects.get(id=user.id)
            serialized = UserSerializer(user)
            token = get_tokens_for_user(user)
            token = parse_token(token)
            return Response(
                {
                    'data': serialized.data,
                    'jwt': token,
                    'status': True,
                    'message': 'Login successful',
                    'StatusCode': '200'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'status': False,
                    'message': 'Invalid username or password',
                    'StatusCode': '400'
                },
                status=status.HTTP_400_BAD_REQUEST)
