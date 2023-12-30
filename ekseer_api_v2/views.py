from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import User, Call, Consultation, Rating
from .serializers import CreateRatingSerializer, CreateUserSerializer, UpdateUserSerializer, LoginSerializer, UserSerializer, CreateCallSerializer, UpdateCallSerializer, CreateConsultationSerializer, UpdateConsultationSerializer,UpdateRatingSerializer
from knox import views as knox_views
from django.contrib.auth import login
import requests
from rest_framework.views import APIView
from django.core.mail import send_mail



class CreateUserAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class CreateCallAPI(CreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CreateCallSerializer
    permission_classes = (AllowAny,)

class CreateConsultationAPI(CreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = CreateConsultationSerializer
    permission_classes = (AllowAny,)

class UserViewSet(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_all_users(self, request):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

class CallViewSet(ListAPIView):
    queryset = Call.objects.all()
    serializer_class = CreateCallSerializer

    def get_all_calls(self, request):
        calls = self.queryset.all()
        serializer = self.serializer_class(calls, many=True)
        return Response(serializer.data)
    
class ConsultationViewSet(ListAPIView):
    queryset = Consultation.objects.all()
    serializer_class = CreateConsultationSerializer

    def get_all_consultations(self, request):
        consultations = self.queryset.all()
        serializer = self.serializer_class(consultations, many=True)
        return Response(serializer.data)


class UpdateUserAPI(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

class UpdateCallAPI(UpdateAPIView):
    queryset = Call.objects.all()
    serializer_class = UpdateCallSerializer

class UpdateConsultationAPI(UpdateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = UpdateConsultationSerializer

class UpdateRatingAPI(UpdateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = UpdateRatingSerializer

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)

class CreateRatingAPI(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer
    permission_classes = (AllowAny,)

class RatingViewSet(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

    def get_all_ratings(self, request):
        ratings = self.queryset.all()
        serializer = self.serializer_class(ratings, many=True)
        return Response(serializer.data)
    

class PaymentInitiationView(APIView):

    def post(self, request):
        api_url = 'https://api-test.sa.noonpayments.com/payment/v1/order'
        body = {
        "apiOperation": "INITIATE",
        "order": {
            "reference": "Ref#1234",
            "amount": "50",
            "currency": "SAR",
            "name": "Test order from noon payments' sample collection",
            "description": "This is a test order",
            "channel": "web",
            "category": "pay",
        },
        "configuration": {
            "tokenizeCc": "true",
            "returnUrl": "https://ekseer.aabdelnaby.com/payment",
            "locale": "en",
            "paymentAction": "Authorize",
        }
}
        headers = {'Content-Type': 'application/json', 'Authorization' : 'Key_Test YWxzYWhhYmEuRWtzZWVyX1BheW1lbnQ6MzBmOWYyZmM0ZDA1NDczM2FhZTAzZTk5YzJhNjA3YzE='}  # Set headers
        response = requests.post(api_url, json=body, headers=headers)
        response.raise_for_status()

        return Response(response.json())
    
class PaymentGetOrderView(APIView):

    def get(self, request, orderId):
        api_url = f'https://api-test.sa.noonpayments.com/payment/v1/order/{orderId}/'
        headers = {'Content-Type': 'application/json', 'Authorization' : 'Key_Test YWxzYWhhYmEuRWtzZWVyX1BheW1lbnQ6MzBmOWYyZmM0ZDA1NDczM2FhZTAzZTk5YzJhNjA3YzE='}  # Set headers
        response = requests.get(api_url, headers=headers)

        print(api_url)
        print(response)
        print(orderId)
        return Response(response.json())
    
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            results = User.objects.filter(iqama_number__icontains=query)
            serializer = UserSerializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Query parameter is required'}, status=400)
        
class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        fullname = request.data.get('full_name')
        mobile_number = request.data.get('mobile_number')
        email_address = request.data.get('email')
        message = request.data.get('message')
        recipient_list = ["info@alsahaba.sa"]

        try:
            send_mail(
                subject='A new message from: '+ email_address,
                message=f"\nFull Name: {fullname}\nMobile Number: {mobile_number}\n\nMessage: {message}",
                from_email="Recieved from " + email_address,
                recipient_list=recipient_list,  # Replace with actual recipient(s)
            )
            return Response({'success': True}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
