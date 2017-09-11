# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from logging_app.serializers import UsersSerializer,SessionSerializer,EventsSerializer
from logging_app.models import Users,Session,Events 
from datetime import datetime
from django.http import JsonResponse
from django.http import QueryDict
import uuid
import json

class UsersView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Users.objects.get(username=serializer.validated_data['username'])
                if user is not None:
                    return JsonResponse('User already exists', status=status.HTTP_400_BAD_REQUEST,safe=False)
            except Users.DoesNotExist:
                ''
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse('Invalid user details', status=status.HTTP_400_BAD_REQUEST,safe=False)
    
    def get(self, request, format=None):
        users=Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return JsonResponse(serializer.data,safe=False)

class SessionView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def get(self, request):
        try:
            if request.session.has_key('username') and request.session.has_key('sessionId'):
                username = request.session['username']
                sessionId = request.session['sessionId']
            elif request.GET.get('username') is not None and request.GET.get('sessionId') is not None:
                username = request.GET.get('username')
                sessionId = request.GET.get('sessionId')
            else:
                return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
            if sessionId is not None:
                session = Session.objects.get(id=sessionId)
            if username is not None and sessionId is not None and session.status is True:
                history = Session.objects.filter(username=username)
                serializer = SessionSerializer(history,many=True)
                return JsonResponse(serializer.data,safe=False)  
            else:
                return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
        except Session.DoesNotExist:
            return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)

class EventsView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def get(self, request):
        try:
            username = request.GET.get('username',None)
            if username is not None:
                events = Events.objects.filter(username=username)
                serializer = EventsSerializer(events,many=True)
                return JsonResponse(serializer.data,safe=False)
            else:  
                events = Events.objects.all()
                serializer = EventsSerializer(events,many=True)
                return JsonResponse(serializer.data,safe=False)
        except Events.DoesNotExist:
            return JsonResponse('No events has been logged', status=status.HTTP_400_BAD_REQUEST ,safe=False)
    
    def post(self, request, format=None):
        try:
            content = json.loads(request.body)
            if request.session.has_key('username') and request.session.has_key('sessionId'):
                username = request.session['username']
                sessionId = request.session['sessionId']
            elif content['username']is not None and content['sessionId'] is not None:
                username = content['username']
                sessionId = content['sessionId']
            else:
                return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
            if sessionId is not None:
                session = Session.objects.get(id=sessionId)
            if username is not None and sessionId is not None and session.status is True:
                event = Events()
                event.username = Users.objects.get(username=username)
                event.sessionId = Session.objects.get(id=sessionId)
                event.action = content['action']
                event.attribute = content['attribute']
                event.eventTime = datetime.now()
                serializer = EventsSerializer(event,context={'request': request})
                event.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED,safe=False)
            else:
                return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
        except:
            return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)

class LoginView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            Users.objects.get(username=username,password=password)
            session = Session()
            session.id = str(uuid.uuid4())
            session.username = Users.objects.get(username=username)
            session.status = True
            session.save()
            serializer = SessionSerializer(session,context={'request': request})
            if not request.session.session_key:
                request.session.create()
            request.session['username'] = username
            request.session['sessionId'] = session.id
            request.session.modified = True
            print serializer.data
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except Users.DoesNotExist:
            return JsonResponse('Invalid Username / Password', status=status.HTTP_400_BAD_REQUEST,safe=False)

class LogoutView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def put(self, request, format=None):
        put = QueryDict(request.body)
        if request.session.has_key('username') and request.session.has_key('sessionId'):
            uname = request.session['username']
            sessionId = request.session['sessionId']
        elif put.get('username')  is not None and put.get('sessionId')  is not None:
            uname = put.get('username') 
            sessionId = put.get('sessionId') 
        else:
            return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
        if uname is not None and sessionId is not None:
            session = Session.objects.get(id=sessionId)
            session.logoutTime = datetime.now()
            session.status = False
            serializer = SessionSerializer(session,context={'request': request})
            session.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse('Invalid session', status=status.HTTP_400_BAD_REQUEST,safe=False)
        