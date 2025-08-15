from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from api.user.models import Profile, ProfileImage
from api.user.serializers import ProfileSerializer, UserSocialLoginSerializer, ProfileImageSerializer, \
    UserRegisterSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer


class ProfileDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ProfileImageUploadView(CreateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.images.count() >= 3:
            raise ValidationError("이미지는 최대 3장까지 업로드할 수 있습니다.")
        serializer.save(profile=profile)


class ProfileImageDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.images.all()
