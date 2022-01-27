from re import search
from django.db.models import query
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from .models import *
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, generics,permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import filters

from django.shortcuts import render
from app.forms import ContactMeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
# Create your views here.


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
# def index(request):
    

#     return render (request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):  
    search_fields = ['email','username']
    # filter_backends = (filters.SearchFilter)
    queryset = User.objects.all()
    serializer_class = UserSerializer




'''
    custom api view to post user, generate token, confim token and login users
'''
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "role": user.role,
                "email": user.email,
                "username": user.username,
            }
        )


'''
user view for serilizers
'''   

class ContactViewSet(viewsets.ModelViewSet):
    search_fields=['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer      

class PartnerViewSet(viewsets.ModelViewSet):
    search_fields = ['user']
    filter_backends = (filters.SearchFilter,)
    queryset = PartnerInfo.objects.all()
    serializer_class = PartnerInfoSerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    search_fields = ['user']
    filter_backends = (filters.SearchFilter,)
    queryset = VolunteerInfo.objects.all()
    serializer_class = VolunteerInfoSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    search_fields = ['user']
    filter_backends = (filters.SearchFilter,)
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer    




def email(request):
    form = ContactMeForm()
    if request.method == 'POST':
        form = ContactMeForm(request.POST)
        if form.is_valid():
            # form.save()
            # send_mail(subject, message[fname, lname, email, phonenumber, subject, message], sedner, recipient)
            subject = "Contact form inquiry"
            body = {
                # 'first_name': form.cleaned_data['first_name'],
                # 'last_name':form.cleaned_data['last_name'],
                'email': form.cleaned_data['emailid'],
                # 'phonenumber': form.cleaned_data['phone_number'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = '\n'.join(body.values())
            # message = 'welcome to mwangaza little'
            sender = 'machariad196@gmail.com'
            recipient = form.cleaned_data['emailid'],
            try:
                send_mail(subject, message, sender, recipient, fail_silently=True)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your respoce has been submited successfully")
    context = {
        'form':form,
    }
    return render(request, "index.html", context)
