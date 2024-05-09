from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from django import db
from ratings import cursor
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
import logging

logger = logging.getLogger(__name__)

# Create your views here.
# view function takes a request and returns a response
# request handler

class LoginAPI(generics.CreateAPIView):
    # @csrf_exempt
    # @api_view(['POST'])
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            print("ERORR")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username = serializer.data.get('username'), password = serializer.data.get('password'))
        if user:
            login(request,user)
            user = MyUser.objects.get(username=request.user.username)
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            return Response("User logged in successfully!")
        else:
            return Response("Bad Credentials!")

class LogoutAPI(generics.ListAPIView):
   #@api_view(['POST'])
    def get(self,request):
        logout(request)
        return Response("Logged Out!")

class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    print("abcd")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        print("abcde")
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = MyUser.objects.get(username = serializer.data['username'], email = serializer.data['email'])
        print(db.connection.queries)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        print(serializer.data)
        return  Response({
            'token': str(token),
            'payload' : serializer.data
        })
    

class GetCredentialsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = MyUser.objects.get(id=request.user.id) 
        serializer = DetailSerializer(user)  
        return Response(serializer.data)

class EditDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        # try:
        serializer.is_valid(raise_exception=True)
        #except serializers.ValidationError:
        user = MyUser.objects.filter(pk=request.user.id).update(username=serializer.data['username'], password=serializer.data['password'], email=serializer.data['email'])

        return Response("updated")


class MovieDetailsAPI(APIView):
    def get(self,request):
        cursor.execute("SELECT * from ratings_movies")
        row = cursor.fetchall()
        return Response(row)
    
class TopMoviesAPI(APIView):
    def get(self,request):
        logger.error("THIS IS A DEBUG MESSAGE")
        cursor.execute("Select ratings_movies.movie_name, ratings_ratings.rating from ratings_movies INNER JOIN ratings_ratings on ratings_movies.m_id = ratings_ratings.m_id_id ORDER BY ratings_ratings.rating DESC")
        row = cursor.fetchall()
        return Response(row)

class RateAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cursor.execute("Select m_id from ratings_movies where movie_name = %s",[serializer.data['movie']])
        movie_id = cursor.fetchall()
        print(movie_id)
        cursor.execute("Select user_id from ratings_myuser where username = %s",[request.user.username])
        u_id = cursor.fetchall()
        print(u_id)
        insertion = cursor.execute("INSERT INTO ratings_ratings(rating, m_id_id, user_id_id) VALUES(%s,%s,%s)",[serializer.data['rate'],movie_id,u_id])
        if insertion:
            return Response("Movie Rating Successful!")
        



        

        