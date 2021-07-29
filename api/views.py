from api.serializers import RoomSerializer
from api.models import Room
from django.shortcuts import render
from rest_framework import generics, serializers


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


