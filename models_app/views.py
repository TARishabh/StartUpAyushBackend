from django.shortcuts import render
from models_app.models import User,Startup,GovernmentAgency,Investor
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from models_app.serializers import LoginSerializer, RegistrationSerializer, StartUpPostSerializer, StartUpListSerializer,StartUpUpdateSerializer,GovernmentAgencyPostSerializer,GovernmentAgencyListSerializer, GovernmentAgencyUpdateSerializer, InvestorPostSerializer,InvestorListSerializer,InvestorUpdateSerializer
from rest_framework import status
from rest_framework import viewsets
import json
import pdb
from rest_framework import serializers
from django.http import Http404

# Create your views here.
def responsegenerator(status, results=None, message=None, errors=None):
    response_data = {"statusCode": status}
    
    if results is not None:
        response_data["results"] = results

    if message is not None:
        response_data["message"] = message

    if errors is not None:
        response_data["errors"] = errors

    return response_data


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name + "@" + domain_part.lower()
    return email

class LoginUser(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        # pdb.set_trace()
        try:
            email = normalize_email(email)
            user = User.objects.get(email=email)
            auth = authenticate(username=email,password=password)
            print(auth)
            if auth is None:
                actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,message="Please Check Email or Password.")
                return Response(actual_response)
            response = get_tokens_for_user(user)
            serializer = LoginSerializer(user)
            response_data = serializer.data
            response_data['email'] = user.email
            actual_response = responsegenerator(status=status.HTTP_200_OK,results=response_data,)
            actual_response['tokens'] = response
            return Response(actual_response)
        
        except User.DoesNotExist:
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,message="Email is not registered or wrong. Please register or check your Email")
            return Response(actual_response)

class RegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            test = serializer.save()
            user = User.objects.get(id=int(test.id))
            # location = data.get('location')
            # if location is not None:
            #     saving_location = {}
            #     location = location.split(',')
            #     saving_location['latitude'] = location[0]
            #     saving_location['longitude'] = location[1]
            #     saving_location = json.dumps(saving_location)
            #     user.location = saving_location
            #     user.save()
            response = get_tokens_for_user(user)
            actual_response = responsegenerator(status=status.HTTP_201_CREATED,results=serializer.data,message="User Registered Successfully")
            actual_response['tokens'] = response
            return Response(actual_response)
        actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST,errors=serializer.errors)
        return Response(actual_response)


class StartUpViewset(viewsets.ModelViewSet):
    queryset = Startup.objects.all()
    http_method_names = ['get', 'post','patch', 'head', 'options', 'delete']
    
    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'create':
            return StartUpPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return self.get_partial_serializer_class()
        else:
            return StartUpListSerializer   # Adjust as needed for other

    def get_partial_serializer_class(self):
        return StartUpUpdateSerializer if self.request.method == 'PATCH' else StartUpListSerializer

    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            actual_response = responsegenerator(
                status=status.HTTP_201_CREATED,
                results=serializer.data,
                message="Startup created successfully."
            )
            return Response(actual_response, headers=headers)
        except serializers.ValidationError as e:
            errors = {}
            for field, field_errors in e.detail.items():
                errors[field] = field_errors[0]  # Take the first error for each field
            actual_response = responsegenerator(
                status=status.HTTP_400_BAD_REQUEST,
                errors=errors
            )
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            actual_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data)
            return Response(actual_response)
        except Http404:
            actual_response = responsegenerator(status=status.HTTP_404_NOT_FOUND, message="Not found.")
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # return Response(serializer.data)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data, message='Updated Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            actual_response = responsegenerator(status=status.HTTP_204_NO_CONTENT, message='Deleted Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)


class GovernmentAgencyViewset(viewsets.ModelViewSet):
    queryset = GovernmentAgency.objects.all()
    http_method_names = ['get', 'post','patch', 'head', 'options', 'delete']

    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'create':
            return GovernmentAgencyPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return self.get_partial_serializer_class()
        else:
            return GovernmentAgencyListSerializer   # Adjust as needed for other

    def get_partial_serializer_class(self):
        return GovernmentAgencyUpdateSerializer if self.request.method == 'PATCH' else GovernmentAgencyListSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            actual_response = responsegenerator(
                status=status.HTTP_201_CREATED,
                results=serializer.data,
                message="Agency created successfully."
            )
            return Response(actual_response, headers=headers)
        except serializers.ValidationError as e:
            errors = {}
            for field, field_errors in e.detail.items():
                errors[field] = field_errors[0]  # Take the first error for each field
            actual_response = responsegenerator(
                status=status.HTTP_400_BAD_REQUEST,
                errors=errors
            )
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            actual_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data)
            return Response(actual_response)
        except Http404:
            actual_response = responsegenerator(status=status.HTTP_404_NOT_FOUND, message="Not found.")
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # return Response(serializer.data)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data, message='Updated Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            actual_response = responsegenerator(status=status.HTTP_204_NO_CONTENT, message='Deleted Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

class InvestorViewset(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    http_method_names = ['get', 'post','patch', 'head', 'options', 'delete']

    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'create':
            return InvestorPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return self.get_partial_serializer_class()
        else:
            return InvestorListSerializer   # Adjust as needed for other

    def get_partial_serializer_class(self):
        return InvestorUpdateSerializer if self.request.method == 'PATCH' else InvestorListSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            actual_response = responsegenerator(
                status=status.HTTP_201_CREATED,
                results=serializer.data,
                message="Investor created successfully."
            )
            return Response(actual_response, headers=headers)
        except serializers.ValidationError as e:
            errors = {}
            for field, field_errors in e.detail.items():
                errors[field] = field_errors[0]  # Take the first error for each field
            actual_response = responsegenerator(
                status=status.HTTP_400_BAD_REQUEST,
                errors=errors
            )
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            actual_response = responsegenerator(status=status.HTTP_200_OK,results=serializer.data)
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data)
            return Response(actual_response)
        except Http404:
            actual_response = responsegenerator(status=status.HTTP_404_NOT_FOUND, message="Not found.")
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # return Response(serializer.data)
            actual_response = responsegenerator(status=status.HTTP_200_OK, results=serializer.data, message='Updated Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            actual_response = responsegenerator(status=status.HTTP_204_NO_CONTENT, message='Deleted Successfully')
            return Response(actual_response)
        except Exception as e:
            print(e)
            actual_response = responsegenerator(status=status.HTTP_400_BAD_REQUEST, message='Something Went Wrong')
            return Response(actual_response)

