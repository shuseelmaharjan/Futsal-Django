from django.db import models
from users.models import CustomUser

class UserDocuments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    coverletter = models.ImageField(upload_to='coverletters/', blank=True, null=True)
    registration = models.ImageField(upload_to='registrations/', blank=True, null=True)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Documents of {self.user.email}"
