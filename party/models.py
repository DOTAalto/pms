from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Party(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    submission_deadline = models.DateTimeField()
    slug = models.SlugField(blank=True)

    @property
    def open_for_submissions(self):
        return timezone.now() <= self.submission_deadline

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Compo(models.Model):
    title = models.CharField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['title', 'party']

    def __str__(self):
        return f"{self.party} - {self.title}"


class Entry(models.Model):
    title = models.CharField(max_length=255)
    sub_file = models.FileField(upload_to="uploads/", blank=True)
    thumbnail = models.FileField(upload_to="uploads/", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    compo = models.ForeignKey(Compo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author} - {self.compo}"