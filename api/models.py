from django.db import models
from django.contrib.postgres.fields import JSONField


STATUS_CHOICES = (
    ('win', 'WIN'),
    ('loose', 'LOOSE')
)


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    game_history = JSONField()
    owner = models.ForeignKey(
        'auth.User',
        related_name='api_game',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField()
    status = models.TextField(
        max_length=5, choices=STATUS_CHOICES, default='win'
    )

