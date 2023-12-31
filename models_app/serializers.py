from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from models_app.models import User,Startup,GovernmentAgency,Investor
import re



class LoginSerializer(serializers.ModelSerializer):
    # redirect_startup = 
    class Meta(object):
        model = User
        fields = ['id','email',]


class RegistrationSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta(object):
        model = User
        fields = ['id','first_name','last_name','contact_number','email','role','password','password2']

    def validate_contact_number(self, value):
        # phone_number = value['phone_number']
        # value = int(value)
        if value:
            pattern = re.compile("^[6-9]\\d{9}$")
            if not pattern.match(value):
                raise serializers.ValidationError("Phone Number Not accepted")
        return value
    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        password_confirm_data = validated_data.pop('password')
        popped_confirm = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password_confirm_data)
        user.save()
        return user

class StartUpPostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Startup
        fields = ['id','owner','startup_name','startup_description','industry_sector','founding_date','founder_bio','website_url','registration_number','contact_person','contact_number']
        

class StartUpListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Startup
        fields = ['id','owner','startup_name','startup_description','industry_sector','founding_date','founder_bio','website_url','contact_person','contact_number','banner_image']

class StartUpUpdateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Startup
        fields = ['id','owner','website_url','contact_person','contact_number']
        

class GovernmentAgencyPostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GovernmentAgency
        fields = ['id','user','agency_name','agency_description','contact_person','contact_number']

class GovernmentAgencyListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GovernmentAgency
        fields = ['id','agency_name','agency_description','contact_person','contact_number']

class GovernmentAgencyUpdateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GovernmentAgency
        fields = ['id','user','contact_person','contact_number']


class InvestorPostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Investor
        fields = ['id','user','investor_description','investment_focus','contact_person','contact_number']

class InvestorListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Investor
        fields = ['id','investor_description','investment_focus','contact_person','contact_number']

class InvestorUpdateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Investor
        fields = ['id','investor_description','investment_focus','contact_person','contact_number']