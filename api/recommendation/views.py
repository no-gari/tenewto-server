from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.user.serializers import ProfileSerializer
from django.db.models import Q
from asgiref.sync import sync_to_async
from django.db import transaction
from .models import RecommendationHistory
from api.user.models import User
from api.matching.models import Like, Block


class RecommendationAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    async def get_queryset(self):
        candidates = await self.get_recommendation_candidates(self.request.user)
        await self.create_recommendation_histories(candidates)
        return candidates

    @sync_to_async
    def create_recommendation_histories(self, candidates):
        with transaction.atomic():
            existing_histories = set(
                RecommendationHistory.objects.filter(
                    user=self.request.user,
                    recommended_user__in=[c.user for c in candidates]
                ).values_list('recommended_user_id', flat=True)
            )

            new_histories = [
                RecommendationHistory(
                    user=self.request.user,
                    recommended_user=candidate.user,
                    viewed=False,
                    liked=False
                )
                for candidate in candidates
                if candidate.user.id not in existing_histories
            ]

            if new_histories:
                RecommendationHistory.objects.bulk_create(new_histories)

    @sync_to_async
    def get_recommendation_candidates(user):
        # 제외할 사용자 ID 목록 만들기
        excluded_ids = set()
        excluded_ids.add(user.id)  # 자기 자신

        # 이미 좋아요를 보낸 사용자
        liked_ids = Like.objects.filter(from_user=user).values_list('to_user', flat=True)
        excluded_ids.update(liked_ids)

        # 차단한 사용자 or 차단당한 사용자
        blocked_ids = Block.objects.filter(
            Q(blocker=user) | Q(blocked_user=user)
        ).values_list('blocker', 'blocked_user')

        # blocked_ids는 튜플로 나오므로 평탄화
        for pair in blocked_ids:
            excluded_ids.update(pair)

        # 후보군 조회 (User의 profile이 있는 활성 사용자)
        candidates = User.objects.filter(
            is_active=True,
            profile__isnull=False
        ).exclude(
            id__in=excluded_ids
        ).select_related('profile')

        # 프로필 리스트로 변환
        profiles = [user.profile for user in candidates]

        return profiles


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_recommendation_viewed(request, user_id):
    """추천 사용자 조회 처리"""
    try:
        recommendation = RecommendationHistory.objects.get(
            user=request.user,
            recommended_user_id=user_id,
            viewed=False
        )
        recommendation.viewed = True
        recommendation.save()

        return Response({'success': True})
    except RecommendationHistory.DoesNotExist:
        return Response({
            'error': '해당 추천 기록을 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_recommendation_liked(request, user_id):
    """추천 사용자 좋아요 처리"""
    try:
        recommendation = RecommendationHistory.objects.get(
            user=request.user,
            recommended_user_id=user_id
        )
        recommendation.liked = True
        recommendation.save()

        return Response({'success': True})
    except RecommendationHistory.DoesNotExist:
        return Response({
            'error': '해당 추천 기록을 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)
