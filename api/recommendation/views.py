from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Exists, OuterRef
from datetime import date, datetime, timedelta
import random

from .models import DailyRecommendation, RecommendationSettings, RecommendationHistory
from .serializers import (
    DailyRecommendationSerializer,
    RecommendationHistorySerializer,
    RecommendationResponseSerializer
)
from api.user.models import User
from api.matching.models import Like, Block


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_recommendations(request):
    """일일 추천 사용자 목록 조회"""
    user = request.user
    today = date.today()

    # 추천 설정 조회
    settings = RecommendationSettings.objects.first()
    if not settings or not settings.is_active:
        return Response({
            'error': '추천 서비스가 비활성화되어 있습니다.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # 오늘 이미 받은 추천 수 확인
    today_recommendations = DailyRecommendation.objects.filter(
        user=user,
        date=today
    ).count()

    remaining_count = max(0, settings.daily_limit - today_recommendations)

    if remaining_count == 0:
        # 다음 리셋 시간 (다음날 00:00)
        next_reset = datetime.combine(today + timedelta(days=1), datetime.min.time())
        next_reset = timezone.make_aware(next_reset)

        return Response({
            'users': [],
            'remaining_count': 0,
            'next_reset_time': next_reset,
            'message': '오늘의 추천을 모두 받으셨습니다.'
        })

    # 추천할 사용자 선택 로직
    recommended_users = _get_recommendation_candidates(user, remaining_count)

    # 추천 기록 저장
    for recommended_user in recommended_users:
        DailyRecommendation.objects.get_or_create(
            user=user,
            recommended_user=recommended_user,
            date=today
        )

        RecommendationHistory.objects.create(
            user=user,
            recommended_user=recommended_user
        )

    # 응답 데이터 구성
    remaining_count_after_recommendation = max(0, remaining_count - len(recommended_users))
    next_reset = datetime.combine(today + timedelta(days=1), datetime.min.time())

    serializer = RecommendationResponseSerializer({
        'users': recommended_users,
        'remaining_count': remaining_count_after_recommendation,
        'next_reset_time': timezone.make_aware(next_reset)
    })

    return Response(serializer.data)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_history(request):
    """추천 기록 조회"""
    history = RecommendationHistory.objects.filter(user=request.user)
    serializer = RecommendationHistorySerializer(history, many=True)
    return Response(serializer.data)


def _get_recommendation_candidates(user, count):
    """추천 후보 사용자 선택 로직"""
    # 제외할 사용자들
    excluded_users = set()

    # 자기 자신 제외
    excluded_users.add(user.id)

    # 이미 좋아요한 사용자들 제외
    liked_users = Like.objects.filter(from_user=user).values_list('to_user_id', flat=True)
    excluded_users.update(liked_users)

    # 내가 차단한 사용자
    i_blocked = Block.objects.filter(from_user=user).values_list('to_user_id', flat=True)
    excluded_users.update(i_blocked)

    # 나를 차단한 사용자
    blocked_me = Block.objects.filter(to_user=user).values_list('from_user_id', flat=True)
    excluded_users.update(blocked_me)

    # 오늘 이미 추천받은 사용자들 제외
    today_recommended = DailyRecommendation.objects.filter(
        user=user,
        date=date.today()
    ).values_list('recommended_user_id', flat=True)
    excluded_users.update(today_recommended)

    # 추천 후보 쿼리
    candidates = User.objects.exclude(id__in=excluded_users).filter(
        is_active=True
    )

    # 성별 기반 필터링
    if user.preferred_gender != 'ALL':
        candidates = candidates.filter(gender=user.preferred_gender)

    # 상대방의 선호 성별도 고려 (양방향 매칭)
    # 내 성별을 선호하거나('ALL'), 모든 성별을 선호하는('ALL') 사용자
    candidates = candidates.filter(
        Q(preferred_gender=user.gender) | Q(preferred_gender='ALL')
    )

    # 랜덤 선택 (실제로는 더 정교한 추천 알고리즘을 사용할 수 있음)
    candidate_list = list(candidates)
    random.shuffle(candidate_list)

    return candidate_list[:count]
