from django.db import models

from party.models import Party


class VoteKey(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    key = models.CharField(max_length=150)

    class Meta:
        unique_together = ['party', 'key']

    def __str__(self):
        return self.key