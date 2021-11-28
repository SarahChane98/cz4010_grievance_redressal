from django.db import models
from users.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_of_post')
    related_authority = models.ForeignKey(User, on_delete=models.PROTECT, related_name='target_authority')
    is_resolved = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    reply_by_authority = models.TextField(blank=True, default='')
    post_sig = models.TextField()
    reply_sig = models.TextField()
    ring_members = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
