import re
from django.db.models import query
from django.http import response
from api.serializers import CreateRoomSerializer, RoomSerializer
from api.models import Room
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwargs = 'code'

    def get(self,request,format=None):
        code = request.GET.get(self.lookup_url_kwargs)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) >0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data,status=status.HTTP_200_OK)
            return Response({'Bad Request':'invalid data'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad request':'Code parameters not found'},status=status.HTTP_400_BAD_REQUEST)   


class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({'message':'Room Joined!'},status=status.HTTP_200_OK)
            return Response({'Bad request':'Invalid room code'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad request':'Invalid post data, did not find a code key'},status=status.HTTP_400_BAD_REQUEST) 


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause','votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data,status.HTTP_201_CREATED)
            else:
                room = Room(host=host,guest_can_pause=guest_can_pause,votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data,status=status.HTTP_200_OK)
        return Response({'Bad request':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
