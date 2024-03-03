from ..models import UserProfile as User
from rest_framework.views import APIView
from rest_framework import status
from ..serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..permissions import IsUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from ..utils.errors import compile_errors

class OneUser(APIView):

     permission_classes = [IsAuthenticated, IsUserOrReadOnly]

     def get_object(self, pk):
          obj = get_object_or_404(User, pk=pk)
          self.check_object_permissions(self.request, obj)
          return obj
          
     def get(self, request, pk):
          user = self.get_object(pk)
          serializer = UserSerializer(user, context={'request': request})
          return Response(
               {
                    'data': serializer.data,
                    'message': 'User retrieved successfully',
                    'status': True,
                    'statusCode': status.HTTP_200_OK,
               },
               status=status.HTTP_200_OK
          )

     def put(self, request, pk):
          user = self.get_object(pk)
          serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
          if serializer.is_valid():
               if request.data.get('password'):
                    return Response(
                         {
                              'errors': ['Password cannot be updated here'],
                         
                         'message': 'User not updated',
                         'status': False,
                         'statusCode': status.HTTP_400_BAD_REQUEST,
                         },
                         status=status.HTTP_400_BAD_REQUEST
                    )
               serializer.save()
               return Response(
                    {
                         'data': serializer.data,
                         'message': 'User updated successfully',
                         'status': True,
                         'statusCode': status.HTTP_200_OK,
                    },
                    status=status.HTTP_200_OK
               )
          return Response(
               {
                    'errors': compile_errors(serializer.errors),
               }, status=status.HTTP_400_BAD_REQUEST
          )

     def delete(self, request, pk):
          user = self.get_object(pk)
          user.delete()
          return Response(
               {
                    'message': 'User deleted successfully',
                    'status': True,
                    'statusCode': status.HTTP_204_NO_CONTENT,
               },
               status=status.HTTP_204_NO_CONTENT)
