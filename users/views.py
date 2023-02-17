from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer,AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class CreateUserApiView(APIView):
    """create new user object"""
    serializer_class = UserSerializer
    def post(self,request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(data=serialized_data.data,status=status.HTTP_201_CREATED)
        return Response(data=serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """create a token for user"""
    serializer_class = AuthTokenSerializer # our custom serializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # nice appearance


class EditUserApiView(APIView):
    """edit user object"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self,request,id):
        user = get_user_model().objects.get(id=id)
        serialized_data = self.serializer_class(instance=user,data=request.data,partial=True)
        if user != request.user :
            return Response(data={'msg':'not allowed'},status=status.HTTP_401_UNAUTHORIZED)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(data=serialized_data.data,status=status.HTTP_200_OK)
        return Response(data=serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)

class GetUserApiView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request,id):
        user = get_object_or_404(get_user_model(),id=id)
        serialized_data = self.serializer_class(instance=user)
        return Response(data=serialized_data.data,status=status.HTTP_200_OK)