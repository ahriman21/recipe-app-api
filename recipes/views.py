from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from core.models import Recipe
from .serializers import (RecipeSerializer,TagSerializer
                          ,ImageRecipeSerializer
                          ,DetailRecipeSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.authorization_services import is_owner
from core.models import Tag
from rest_framework.views import APIView
from rest_framework.decorators import action

# Create your views here.
class RecipeViewSet(viewsets.ViewSet):
    """Recipe create,retrive,update,delete Viewset"""
    queryset = Recipe.objects.all()
    serializer_class = DetailRecipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self,request):
        """get list recipes"""
        serialized_data = self.serializer_class(instance=self.queryset,many=True)
        return Response(data=serialized_data.data,status=status.HTTP_200_OK)


    def retrieve(self,request,pk):
        """get a single recipe"""
        recipe = get_object_or_404(self.queryset,pk=pk)
        serialized_data = self.serializer_class(instance=recipe)
        return Response(data=serialized_data.data,status=status.HTTP_200_OK)

    def create(self,request):
        """Create new recipe"""
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(user= request.user)
            return Response(data=serialized_data.data,status=status.HTTP_201_CREATED)
        return Response(data=serialized_data.data,status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk):
        """update recipe object"""
        recipe = get_object_or_404(self.queryset,pk=pk)
        if is_owner(recipe,request) == False:
            return Response(data={'msg':'not allowed'},status=status.HTTP_401_UNAUTHORIZED)
        serialized_data = self.serializer_class(instance=recipe,partial=True,data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(user= request.user)
            return Response(data=serialized_data.data,status=status.HTTP_200_OK)
        return Response(data=serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        """delete recipe object"""
        recipe = get_object_or_404(self.queryset,pk=pk)
        if is_owner(recipe,request) == False:
            return Response(data={'msg':'not allowed'},status=status.HTTP_401_UNAUTHORIZED)
        recipe.delete()
        msg = {'ok':'recipe deleted successfully'}
        return Response(data=msg,status=status.HTTP_200_OK)


class UploadImage(APIView):
    serializer_class = ImageRecipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Recipe.objects.all()

    def put(self,request,pk=None):
        recipe = get_object_or_404(self.queryset,pk=pk)
        if is_owner == False:
            return Response(data={'msg':'not allowed'},status=status.HTTP_401_UNAUTHORIZED)
        serialized_data = self.serializer_class(recipe,request.data,partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(data=serialized_data.data,status=status.HTTP_200_OK)
        return Response(data=serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self,request):
        serialized_data = self.serializer_class(instance=self.queryset,many=True)
        return Response(data=serialized_data.data,status=status.HTTP_200_OK)

    def create(self,request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(data=serialized_data.data,status=status.HTTP_201_CREATED)
        return Response(data=serialized_data.errors,status=status.HTTP_400_BAD_REQUEST)


    def destroy(self,request,pk):
        tag = get_object_or_404(self.queryset,pk=pk)
        if is_owner(tag,request) == False:
            return Response(data={'msg':'not allowed'},status=status.HTTP_401_UNAUTHORIZED)
        tag.delete()
        return Response(data={'SUCCESSFULL':'tag deleted'},status=status.HTTP_200_OK)