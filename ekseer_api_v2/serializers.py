from rest_framework import authentication, serializers, views
from .models import User, Call, Consultation, Rating
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%m-%d-%Y')
    class Meta:
        model = User
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'mobile_number', 
            'email', 
            'is_staff',
            'is_verified',
            'contract',
            'no_objection_letter',
            'additional_attachment'
        ]
        extra_kwargs = {
            'password': {'write_only':True}
        }


    def update(self, instance, validated_data):
        
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    iqama_number = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)


    def validate(self, attrs):
        iqama_number = attrs.get('iqama_number')
        password = attrs.get('password')

        if not iqama_number or not password:
            raise serializers.ValidationError("Please give both iqama_number and password.")

        if not User.objects.filter(iqama_number=iqama_number).exists():
            raise serializers.ValidationError('Iqama Number/ID not exist.')

        user = authenticate(request=self.context.get('request'), iqama_number=iqama_number,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs

class CreateCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'

    def validate(self, attrs):
        meeting_id = attrs.get('meeting_id', '').strip().lower()
        if Call.objects.filter(meeting_id=meeting_id).exists():
            raise serializers.ValidationError('Meeting id already exists.')
        return attrs

    def create_call(self, meeting_id, patient_id,doctor_id,doctor_time,patient_time,awaiting_time, **extra_fields):
        if not meeting_id:
            raise ValueError("The meeting_id is not given.")
        call = self.model(meeting_id=meeting_id,awaiting_time=awaiting_time,patient_id=patient_id,patient_time=patient_time,doctor_time=doctor_time, doctor_id=doctor_id,is_new=True, **extra_fields)
        call.save()
        return call
    
class UpdateCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class CreateConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

    def create_consultation(self, patient_id,doctor_id,call_id ,chief_complaint,history_of_illness,review_of_systems,examination,assessment,medication,sick_leave,**extra_fields):
        consultation = self.model(
            patient_id=patient_id, 
            doctor_id=doctor_id,
            chief_complaint=chief_complaint,
            history_of_illness=history_of_illness,
            review_of_systems=review_of_systems,
            examination=examination,assessment=assessment,
            medication=medication,
            call_id=call_id,
            sick_leave=sick_leave, 
            **extra_fields)
        consultation.save()
        return consultation
    
class UpdateConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    
class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def create_rating(self, patient_id,doctor_id,call_id,rating,message,**extra_fields):
        create_rating = self.model(
            patient_id=patient_id, 
            doctor_id=doctor_id,
            rating=rating,
            call_id=call_id,
            message=message,
            **extra_fields)
        create_rating.save()
        return create_rating
    
class UpdateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance