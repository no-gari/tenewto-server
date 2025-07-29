from django.db import models
from datetime import date


class DailyRecommendation(models.Model):
    """일일 추천 관리 모델"""
    user = models.ForeignKey('user.User', verbose_name='사용자', on_delete=models.CASCADE)
    recommended_user = models.ForeignKey('user.User', verbose_name='추천된 사용자', on_delete=models.CASCADE, related_name='recommended_to')
    date = models.DateField(verbose_name='추천 날짜', default=date.today)
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)

    class Meta:
        verbose_name = '일일 추천'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'recommended_user', 'date')
        ordering = ['-created']

    def __str__(self):
        return f"{self.user} -> {self.recommended_user} ({self.date})"


class RecommendationSettings(models.Model):
    """추천 설정 모델"""
    daily_limit = models.PositiveIntegerField(verbose_name='일일 추천 제한', default=3)
    is_active = models.BooleanField(verbose_name='활성화', default=True)
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='수정일시', auto_now=True)

    class Meta:
        verbose_name = '추천 설정'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"일일 {self.daily_limit}명 추천"


class RecommendationHistory(models.Model):
    """추천 기록 모델"""
    user = models.ForeignKey('user.User', verbose_name='사용자', on_delete=models.CASCADE)
    recommended_user = models.ForeignKey('user.User', verbose_name='추천된 사용자', on_delete=models.CASCADE, related_name='recommendation_history')
    viewed = models.BooleanField(verbose_name='조회됨', default=False)
    liked = models.BooleanField(verbose_name='좋아요', default=False)
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)

    class Meta:
        verbose_name = '추천 기록'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return f"{self.user} -> {self.recommended_user} (viewed: {self.viewed}, liked: {self.liked})"
