from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Party(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural = 'parties'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CompoVotingStatus(models.TextChoices):
    UPCOMING = 'U', 'Upcoming'
    LIVE = 'L', 'Live'
    OPEN = 'O', 'Voting open'
    CLOSED = 'C', 'Voting closed'


class Compo(models.Model):
    title = models.CharField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    submission_deadline = models.DateTimeField()
    metadata_deadline = models.DateTimeField()
    voting_status = models.CharField(max_length=1, choices=CompoVotingStatus, default=CompoVotingStatus.UPCOMING)

    class Meta:
        unique_together = ['title', 'party']

    @property
    def open_for_submissions(self):
        return timezone.now() <= self.submission_deadline
    
    @property
    def can_edit_metadata(self):
        return timezome.now() <= self.metadata_deadline

    def __str__(self):
        return f"{self.party} - {self.title}"


class Entry(models.Model):
    title = models.CharField(max_length=32)
    sub_file = models.FileField(upload_to="uploads/", blank=True)
    thumbnail = models.FileField(upload_to="uploads/", blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    team = models.CharField(max_length=32)
    description = models.TextField()
    compo = models.ForeignKey(Compo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} by {self.team} - {self.compo}"