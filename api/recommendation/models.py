from django.db import models


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
