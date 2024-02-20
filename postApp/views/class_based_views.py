from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from ..serializers import PostModelSerializer
from ..models import Post
from django.shortcuts import get_object_or_404


class PostListCreateView(APIView):

    serializer_class=PostModelSerializer

    def get(self, request:Request):
        posts=Post.objects.all()
        serializer=self.serializer_class(instance=posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                "message":"Post created",
                "data":serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDeleteView(APIView):

    serializer_class=PostModelSerializer

    def get(self, request:Request, id:int):
        post=get_object_or_404(Post, pk=id)
        serializer=self.serializer_class(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request:Request, id:int):
        post=get_object_or_404(Post, pk=id)
        data=request.data
        serializer=self.serializer_class(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, id:int):
        post=get_object_or_404(Post, pk=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)