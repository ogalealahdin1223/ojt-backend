from django.contrib.auth.models import User
from rest_framework import serializers

from .models import OJTProfile


class AdminUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    required_hours = serializers.DecimalField(
        source="ojtprofile.required_hours",
        max_digits=6,
        decimal_places=2,
        read_only=True,
    )
    start_date = serializers.DateField(source="ojtprofile.start_date", read_only=True)
    end_date = serializers.DateField(source="ojtprofile.end_date", read_only=True)
    trainee_id = serializers.CharField(source="ojtprofile.trainee_id", read_only=True)
    intern_type = serializers.CharField(source="ojtprofile.intern_type", read_only=True)
    program = serializers.CharField(source="ojtprofile.program", read_only=True)
    institution = serializers.CharField(source="ojtprofile.institution", read_only=True)
    department = serializers.CharField(source="ojtprofile.department", read_only=True)
    supervisor = serializers.CharField(source="ojtprofile.supervisor", read_only=True)
    profile_image = serializers.ImageField(source="ojtprofile.profile_image", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "full_name",
            "required_hours",
            "start_date",
            "end_date",
            "trainee_id",
            "intern_type",
            "program",
            "institution",
            "department",
            "supervisor",
            "profile_image",
        ]

    def get_full_name(self, obj):
        profile = getattr(obj, "ojtprofile", None)
        if profile and profile.full_name:
            return profile.full_name

        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username


class AdminInternCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    full_name = serializers.CharField(source="ojtprofile.full_name", required=False, allow_blank=True)
    required_hours = serializers.DecimalField(
        source="ojtprofile.required_hours",
        max_digits=6,
        decimal_places=2,
        required=False,
    )
    start_date = serializers.DateField(source="ojtprofile.start_date", required=False, allow_null=True)
    end_date = serializers.DateField(source="ojtprofile.end_date", required=False, allow_null=True)
    trainee_id = serializers.CharField(source="ojtprofile.trainee_id", required=False, allow_blank=True)
    intern_type = serializers.CharField(source="ojtprofile.intern_type", required=False, allow_blank=True)
    program = serializers.CharField(source="ojtprofile.program", required=False, allow_blank=True)
    institution = serializers.CharField(source="ojtprofile.institution", required=False, allow_blank=True)
    department = serializers.CharField(source="ojtprofile.department", required=False, allow_blank=True)
    supervisor = serializers.CharField(source="ojtprofile.supervisor", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "is_active",
            "full_name",
            "required_hours",
            "start_date",
            "end_date",
            "trainee_id",
            "intern_type",
            "program",
            "institution",
            "department",
            "supervisor",
        ]

    def validate_username(self, value):
        username = str(value).strip()

        if not username.isdigit():
            raise serializers.ValidationError("Username must be a 5-digit numeric ID.")

        if len(username) != 5:
            raise serializers.ValidationError("Username must be exactly 5 digits.")

        if username[0] not in ["4", "5", "6", "7", "8", "9"]:
            raise serializers.ValidationError("Intern ID must start with 4, 5, 6, 7, 8, or 9.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username already exists.")

        return username

    def create(self, validated_data):
        profile_data = validated_data.pop("ojtprofile", {})
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data.get("username"),
            password=password,
            email=validated_data.get("email", ""),
            is_active=validated_data.get("is_active", True),
        )

        profile, _ = OJTProfile.objects.get_or_create(user=user)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return user


class AdminInternUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="ojtprofile.full_name", required=False, allow_blank=True)
    required_hours = serializers.DecimalField(
        source="ojtprofile.required_hours",
        max_digits=6,
        decimal_places=2,
        required=False,
    )
    start_date = serializers.DateField(source="ojtprofile.start_date", required=False, allow_null=True)
    end_date = serializers.DateField(source="ojtprofile.end_date", required=False, allow_null=True)
    trainee_id = serializers.CharField(source="ojtprofile.trainee_id", required=False, allow_blank=True)
    intern_type = serializers.CharField(source="ojtprofile.intern_type", required=False, allow_blank=True)
    program = serializers.CharField(source="ojtprofile.program", required=False, allow_blank=True)
    institution = serializers.CharField(source="ojtprofile.institution", required=False, allow_blank=True)
    department = serializers.CharField(source="ojtprofile.department", required=False, allow_blank=True)
    supervisor = serializers.CharField(source="ojtprofile.supervisor", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "email",
            "is_active",
            "full_name",
            "required_hours",
            "start_date",
            "end_date",
            "trainee_id",
            "intern_type",
            "program",
            "institution",
            "department",
            "supervisor",
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("ojtprofile", {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile, _ = OJTProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance