from django.core.validators import MaxValueValidator
from django.db import models

from party.models import Party, Entry


class VoteKey(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    key = models.CharField(max_length=150)

    class Meta:
        unique_together = ['party', 'key']

    def __str__(self):
        return self.key



POINTS = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class Vote(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='votes')
    votekey = models.ForeignKey(VoteKey, on_delete=models.SET_NULL, null=True, db_index=True)
    points = models.PositiveIntegerField(default=0, choices=POINTS)

    class Meta:
        unique_together = ['entry', 'votekey']