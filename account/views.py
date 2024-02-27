from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import MyUserSerializer,LoginSerializer,ProfileSerializer,Changepasswordserializer,SendPassResetEmailSerializer,UserPassResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=MyUserSerializer(data=request.data)
        if serializer.is_valid():
         user=serializer.save()
         token=get_tokens_for_user(user)
         return Response({'msg':'Registration Success!','token':token},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
   renderer_classes=[UserRenderer]
   def post(self,request,format=None):
      serializer=LoginSerializer(data=request.data)
      if serializer.is_valid():
         email=serializer.data.get('email')
         password=serializer.data.get('password')
         user=authenticate(email=email,password=password)
         if user is not None:
            token=get_tokens_for_user(user)
            return Response({'msg':'Login Success!','token':token},status=status.HTTP_200_OK)
         return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
class UserProfileView(APIView):
  renderer_classes=[UserRenderer]
  permission_classes=[IsAuthenticated]
  def get(self,request,format=None):
    serializer=ProfileSerializer(request.user)
    return Response(serializer.data,status=status.HTTP_200_OK)
  

class UserChangePassword(APIView):
     renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def post(self,request,format=None):
        context={'user':request.user}
        serializer=Changepasswordserializer(data=request.data,context=context)
        if serializer.is_valid():
         return Response({'msg':'Password Change Success!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmail(APIView):
     renderer_classes=[UserRenderer]
     
     def post(self,request,format=None):
        serializer=SendPassResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Password Reset link sent check your email!'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
           

class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
       serializer=UserPassResetSerializer(data=request.data,context={'uid':uid,'token':token})
       if serializer.is_valid():
         return Response({'msg':'Password Change Success!'},status=status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
          

        
           
   
       