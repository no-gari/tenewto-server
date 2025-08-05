from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Match, Like, Block
from api.user.models import User
from .serializers import MatchSerializer, LikeSerializer, LikeResponseSerializer, BlockSerializer, BlockCreateSerializer
from api.user.models import Profile
from api.user.serializers import ProfileSerializer
from api.chat.models import Chat


class BlockViewSet(viewsets.ModelViewSet):
    """사용자 차단 관리"""
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """내가 차단한 사용자들"""
        return Block.objects.filter(blocker=self.request.user)

    def get_serializer_class(self):
        """액션에 따라 다른 시리얼라이저 사용"""
        if self.action == 'create':
            return BlockCreateSerializer
        return BlockSerializer

    def perform_create(self, serializer):
        """차단 생성 시 자동으로 blocker 설정"""
        block = serializer.save(blocker=self.request.user)
        
        # 기존 좋아요 관계가 있다면 삭제
        Like.objects.filter(
            Q(from_user=self.request.user, to_user=block.blocked_user) |
            Q(from_user=block.blocked_user, to_user=self.request.user)
        ).delete()
        
        # 기존 매칭이 있다면 삭제
        Match.objects.filter(
            Q(user1=self.request.user, user2=block.blocked_user) |
            Q(user1=block.blocked_user, user2=self.request.user)
        ).delete()

    @action(detail=True, methods=['delete'])
    def unblock(self, request, pk=None):
        """차단 해제"""
        try:
            block = Block.objects.get(
                id=pk,
                blocker=request.user
            )
        except Block.DoesNotExist:
            return Response(
                {'error': '해당 차단 기록을 찾을 수 없습니다.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        block.delete()
        return Response({'message': '차단이 해제되었습니다.'})

    @action(detail=False, methods=['get'])
    def blocked_users(self, request):
        """내가 차단한 사용자 목록"""
        blocks = self.get_queryset()
        serializer = self.get_serializer(blocks, many=True)
        return Response(serializer.data)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """내가 보낸 좋아요들"""
        return Like.objects.filter(from_user=self.request.user)

    def perform_create(self, serializer):
        """좋아요 생성 시 자동으로 from_user 설정 및 매칭 확인"""
        like = serializer.save(from_user=self.request.user)
        
        # 상대방이 나를 좋아했는지 확인
        mutual_like = Like.objects.filter(
            from_user=like.to_user,
            to_user=like.from_user,
            status='pending'
        ).first()
        
        if mutual_like:
            # 양방향 좋아요이므로 매칭 생성
            match = Match.objects.create(
                user1=like.from_user,
                user2=like.to_user
            )
            
            # 두 좋아요 모두 accepted로 변경
            like.status = 'accepted'
            mutual_like.status = 'accepted'
            like.save()
            mutual_like.save()
            
            # 채팅방 자동 생성
            chat = Chat.objects.create(match=match)
            chat.user_set.add(match.user1, match.user2)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """내가 받은 좋아요들 (pending 상태만)"""
        received_likes = Like.objects.filter(
            to_user=request.user,
            status='pending'
        )
        serializer = LikeSerializer(received_likes, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """받은 좋아요에 대한 응답 (수락/거절)"""
        try:
            like = Like.objects.get(
                id=pk,
                to_user=request.user,
                status='pending'
            )
        except Like.DoesNotExist:
            return Response(
                {'error': '해당 좋아요를 찾을 수 없거나 이미 처리되었습니다.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = LikeResponseSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            
            if action == 'accept':
                # 좋아요 수락
                like.status = 'accepted'
                like.save()

                match = Match.objects.create(
                    user1=like.from_user,
                    user2=request.user
                )

                # 채팅방 생성
                chat = Chat.objects.create(match=match)
                chat.user_set.add(match.user1, match.user2)

                return Response({
                    'status': 'matched',
                    'message': '매칭이 성사되었습니다!',
                    'match_id': match.id
                })
            
            else:
                like.status = 'rejected'
                like.save()
                return Response({
                    'status': 'rejected',
                    'message': '좋아요를 거절했습니다.'
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """매칭된 사용자들 조회 (매칭은 자동으로 생성되므로 읽기 전용)"""
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """내가 포함된 모든 매칭들"""
        return Match.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )


class RecommendViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """추천 사용자 목록"""
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {'error': '프로필을 먼저 생성해주세요.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 제외할 사용자들: 자신, 차단한/차단당한 사용자, 이미 좋아요한 사용자, 매칭된 사용자
        excluded_users = self._get_excluded_users(request.user, user_profile)
        
        # 기본 쿼리셋
        queryset = Profile.objects.exclude(user__in=excluded_users)
        
        # 필터 적용
        # queryset = self._apply_filters(queryset, request, user_profile)
        
        # 페이지네이션
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = ProfileSerializer(page, many=True, context={'request': request})
        #     return self.get_paginated_response(serializer.data)

        serializer = ProfileSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def _get_excluded_users(self, current_user, user_profile):
        """제외할 사용자 ID들 반환"""
        excluded_users = [current_user.id]
        
        # 차단한/차단당한 사용자들 (Block 모델 사용)
        blocked_users = Block.objects.filter(blocker=current_user).values_list('blocked_user_id', flat=True)
        blocked_by_users = Block.objects.filter(blocked_user=current_user).values_list('blocker_id', flat=True)
        excluded_users.extend(blocked_users)
        excluded_users.extend(blocked_by_users)
        
        # 이미 좋아요한 사용자들
        liked_users = Like.objects.filter(from_user=current_user).values_list('to_user_id', flat=True)
        excluded_users.extend(liked_users)

        # 프로필이 없는 사용자들
        no_profile_users = User.objects.filter(profile__isnull=True).values_list('id', flat=True)
        excluded_users.extend(no_profile_users)

        # 매칭된 사용자들
        # matched_users = Match.objects.filter(
        #     Q(user1=current_user) | Q(user2=current_user)
        # ).values_list('user1_id', 'user2_id')
        
        # for user1_id, user2_id in matched_users:
        #     if user1_id != current_user.id:
        #         excluded_users.append(user1_id)
        #     if user2_id != current_user.id:
        #         excluded_users.append(user2_id)
        
        return list(set(excluded_users))  # 중복 제거
    
    def _apply_filters(self, queryset, request, user_profile):
        """쿼리 파라미터에 따라 필터 적용"""
        filters = {}
        
        # 기본 필터들
        filter_mapping = {
            'nationality': 'nationality',
            'city': 'city',
            'gender': 'gender',
            'religion': 'religion',
            'smoke': 'smoke',
            'mbti': 'mbti',
            'job': 'job',
            'school_level': 'school_level',
        }
        
        for param, field in filter_mapping.items():
            value = request.query_params.get(param)
            if value:
                filters[field] = value
        
        # 범위 필터들
        min_age = request.query_params.get('min_age')
        max_age = request.query_params.get('max_age')
        min_height = request.query_params.get('min_height')
        max_height = request.query_params.get('max_height')
        
        if min_age:
            filters['age__gte'] = min_age
        if max_age:
            filters['age__lte'] = max_age
        if min_height:
            filters['height__gte'] = min_height
        if max_height:
            filters['height__lte'] = max_height
        
        queryset = queryset.filter(**filters)
        
        # 위치 기반 필터링
        # max_distance = request.query_params.get('max_distance')
        # if max_distance and user_profile.latitude and user_profile.longitude:
        #     user_location = Point(
        #         float(user_profile.longitude),
        #         float(user_profile.latitude),
        #         srid=4326
        #     )
        #     queryset = queryset.annotate(
        #         distance=Distance('location', user_location)
        #     ).filter(
        #         distance__lte=float(max_distance) * 1000  # km를 m로 변환
        #     ).order_by('distance')
        
        return queryset