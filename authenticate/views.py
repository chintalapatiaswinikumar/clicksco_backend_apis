from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.http import JsonResponse
from django.core import serializers
from passlib.hash import pbkdf2_sha256
import jwt
import json
from clickverse_main.settings import SECRET_KEY
from django.db import IntegrityError
from django.http import HttpResponse



# Create your views here.

class RegisterView(APIView):

    def createJwtToken(self,body):
        payload = {}
        payload['email'] = body['email']
        payload['username'] = body['username']
        token = jwt.encode(payload,SECRET_KEY)
        return token

    def decodeJwtToken(self,token):
        oldToken = jwt.decode(token,SECRET_KEY, algorithms=['HS256'])
        return oldToken


    def post(self,request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            userExsist = list(ClickverseUser.objects.filter(username = body['username']))
            user = ClickverseUser()
            user.username = body['username']
            user.password = pbkdf2_sha256.encrypt(body['password'],rounds=12000,salt_size=32)
            user.email = body['email']
            # user.first_name = body['first_name']
            # user.last_name = body['last_name']
            # user.email = body['email']
            user.is_staff = body['is_staff']
            user.is_active = body['is_active']
            user.is_super_user = body['is_super_user']
            user.last_login = body['last_login']
            user.date_joined = body['date_joined']
            # payload = {}
            # payload['email'] = body['email']
            # payload['username'] = body['username']
            #token = jwt.encode(payload,SECRET_KEY)
            token = self.createJwtToken(body)
            response = {}
            response['username'] = body['username']
            response['email'] = body['email']
            response['token'] = token
            user.save()
            # else:
            # return JsonResponse({'Error':'User already exsist'})
            return JsonResponse({"user":response})
        except IntegrityError as ex:
            error = HttpResponse(ex).content.decode()
            if error.__contains__("email"): 
                return JsonResponse({"Error":"Email already exsists"})
            else:
                return JsonResponse({"Error":"Username already exsists"})
    
    def put(self,request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            oldToken = self.decodeJwtToken(request.headers['Authorization'].split()[1])
            user = ClickverseUser.objects.get(id = oldToken['id'])
            user.email = body['email']
            user.save()
            payload = {}
            payload['email'] = user.email
            payload['username'] = user.username
            token = self.createJwtToken(payload)
            response ={}
            response['email'] = user.email
            response['username'] = user.username
            response['token'] = token

            return JsonResponse({"user":response})
        except Exception as ex:
            return JsonResponse({"error":"some error occured"})

    def get(self,request):
        try:
            oldToken = self.decodeJwtToken(request.headers['Authorization'].split()[1])
            user = ClickverseUser.objects.get(username = oldToken['username'])
            payload = {}
            payload['email'] = user.email
            payload['username'] = user.username
            token = self.createJwtToken(payload)
            response = {}
            response['email'] = user.email
            response['username'] = user.username
            response['token'] = token
            return JsonResponse({"user":response})
        
        except Exception as ex:
            return JsonResponse({"Error":"No user exsits"})



class LoginView(APIView):
    def post(self,request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = ClickverseUser.objects.get(email=body['email'])
            if user:
                isPasswordMatched = pbkdf2_sha256.verify(body['password'],user.password)
                if isPasswordMatched == True:
                    payload = {}
                    payload['email'] = body['email']
                    payload['id'] = user.id
                    token = jwt.encode(payload,SECRET_KEY)
                    response =  {}
                    response['email'] = user.email
                    response['username'] = user.username
                    response['token'] = token
                    return JsonResponse({"user":response})
                else:
                    return JsonResponse({'Error':"your password did'nt match with the username provided"})
            else:
                return JsonResponse({'Error':'user name is not found in data base,please register before login'})
        except Exception as ex:
            return JsonResponse({'Error':"user name is not found in data base,please register before login"})

# class UserGroupView(APIView):
    # def get(self,request):
        # try:
            # jwtToken = request.headers['Authorization'].split()[1]
            # decodedPayload = jwt.decode(jwtToken,SECRET_KEY, algorithms=['HS256'])
            # query = 'SELECT * FROM authenticate_UserHasGroups JOIN authenticate_ClickverseUser ON authenticate_UserHasGroups.group_id = authenticate_ClickverseUser.id join authenticate_ClickverseUserGroups on authenticate_ClickverseUserGroups.id = authenticate_UserHasGroups.group_id'
            # groups = list(UserHasGroups.objects.raw(query))
            # return JsonResponse({"error":"NA","group_names":'1'})
        # except Exception as ex:
            # return JsonResponse({"Error":"some error occured"})
# 