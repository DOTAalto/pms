from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone


class Party(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, help_text='Only one party can be active at a time. Users are redirected to active party after login')
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural = 'parties'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.is_active:
            # There can only be one Party active at once
            other_active = Party.objects.filter(is_active=True).exclude(pk=self.pk)
            if other_active.exists():
                raise ValidationError('Only one party can be set active at the same time')


class CompoVotingStatus(models.TextChoices):
    UPCOMING = 'U', 'Voting is not yet open.'
    LIVE = 'L', 'Voting is live.'
    OPEN = 'O', 'Voting is open.'
    CLOSED = 'C', 'Voting has ended.'


class Compo(models.Model):
    title = models.CharField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    submission_deadline = models.DateTimeField()
    metadata_deadline = models.DateTimeField()
    voting_status = models.CharField(max_length=1, choices=CompoVotingStatus, default=CompoVotingStatus.UPCOMING)
    current_entry_pos = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['title', 'party']

    def submission_deadline_simple(self):
        # Sunday 22:30
        return timezone.localtime(self.submission_deadline).strftime('%A %H:%M')
    submission_deadline_simple.short_description = 'Submission Deadline'

    def metadata_deadline_simple(self):
        # Sunday 22:30
        return timezone.localtime(self.metadata_deadline).strftime('%A %H:%M')
    metadata_deadline_simple.short_description = 'Metadata Deadline'

    @property
    def open_for_submissions(self):
        return timezone.now() <= self.submission_deadline

    @property
    def can_edit_metadata(self):
        return timezone.now() <= self.metadata_deadline

    def __str__(self):
        return f"{self.party} - {self.title}"


class PlatformChoices(models.TextChoices):
    WEB = 'WEB', 'Chromium + web server'
    LINUX = 'LIN', 'Linux'
    WINDOWS = 'WIN', 'Windows (Proton)'
    OTHER = 'OTH', 'Other (specify below)'

class Entry(models.Model):
    title = models.CharField(max_length=32, help_text="e.g. Färjan")
    sub_file = models.FileField(upload_to="uploads/", blank=True)
    thumbnail = models.FileField(upload_to="uploads/", blank=True, help_text="Recommended 1920x1080 or 1280x720")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    team = models.CharField(max_length=32, help_text="e.g. demogroup")
    team_member_count = models.PositiveIntegerField(default=1, help_text="How many of you are there in your team?")
    technology = models.CharField(max_length=256, null=True, blank=True)
    compo = models.ForeignKey(Compo, on_delete=models.CASCADE, related_name='entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructions = models.TextField(blank=True, null=True, help_text='Should we press some button after opening your demo? Anything you want to clarify about the above? If you are not sure, feel free to ask from the organizers.')
    contact_phone = models.CharField(max_length=16, null=True, blank=True, help_text='We will contact you if we have issues testing that your demo works or if you win something and don’t show up to the award ceremony.')
    contact_telegram = models.CharField(max_length=32, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    platform = models.CharField(max_length=3, choices=PlatformChoices)
    has_audio = models.BooleanField(blank=True, null=True, help_text='If we don’t hear anything, is it a problem?')
    exits_automatically = models.BooleanField(blank=True, null=True, help_text='If not, we will try our best to guess where it ends/loops.')

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} by {self.team} - {self.compo}"