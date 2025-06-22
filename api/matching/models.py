from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Like(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),  # 좋아요 받은 사람이 수락
        ('rejected', 'Rejected'),  # 좋아요 받은 사람이 거절
    ]
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('좋아요')
        verbose_name_plural = verbose_name
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"


class Match(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # 양방향 좋아요가 성사되면 자동으로 매치 생성되므로 별도 status 불필요

    class Meta:
        verbose_name = _('매칭')
        verbose_name_plural = verbose_name
        unique_together = ('user1', 'user2')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user1} - {self.user2}"
    
    @property
    def other_user(self):
        """현재 요청한 사용자의 상대방 반환하는 헬퍼 메서드"""
        # 이 메서드는 views에서 request.user와 함께 사용
        pass