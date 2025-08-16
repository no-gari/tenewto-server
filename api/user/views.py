from api.user.serializers import ProfileSerializer, UserSocialLoginSerializer, ProfileImageSerializer, \
    UserRegisterSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from api.user.models import Profile, ProfileImage
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer


# 기존 ProfileDetailUpdateView 교체/보완
class ProfileDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    # 대표 사진 변경을 처리
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        avatar_id = request.data.get('avatarId') or request.data.get('avatar_id')

        if avatar_id:
            try:
                image = profile.images.get(id=avatar_id)
            except ProfileImage.DoesNotExist:
                raise ValidationError("해당 이미지가 존재하지 않습니다.")

            # 하나만 대표가 되도록 모델의 save 로직에 맡김
            image.is_avatar = True
            image.save()

            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # avatarId 없이 다른 필드 업데이트가 들어오면 기본 동작 수행
        return super().update(request, *args, **kwargs)


# 업로드 시 첫 이미지면 자동으로 대표 지정 (선택적 개선)
class ProfileImageUploadView(CreateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        profile = self.request.user.profile

        # 일단 저장
        obj = serializer.save(profile=profile)

        # 첫 이미지라면 자동 대표 지정
        if not profile.images.exclude(id=obj.id).exists():
            obj.is_avatar = True
            obj.save()


# 대표 사진 삭제 시 자동 재지정
class ProfileImageDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.images.all()

    def perform_destroy(self, instance: ProfileImage):
        profile = instance.profile
        was_avatar = instance.is_avatar
        # 파일 삭제 포함한 모델 delete 사용
        super().perform_destroy(instance)

        # 대표였던 걸 지웠다면 가장 최신 것으로 대표 재지정
        if was_avatar:
            new_avatar = profile.images.order_by('-created_at').first()
            if new_avatar:
                new_avatar.is_avatar = True
                new_avatar.save()
