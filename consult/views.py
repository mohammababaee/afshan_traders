from django.shortcuts import render
from rest_framework.views import APIView
from consult.models import Consult
from consult.serializers import ConsultSerializer 
from rest_framework.response import Response
from rest_framework import status

class ConsultAPIView(APIView):
    def post(self, request):
        consult_data = request.data
        consult_serializer = ConsultSerializer(data=consult_data) 
        if consult_serializer.is_valid():
            consult = consult_serializer.save()
            return Response(consult_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(consult_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    def get(self, request):
        all_consults = Consult.objects.all()
        serializer = ConsultSerializer(all_consults, many=True)
        return Response({"consults": serializer.data})
        
