from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


def path_file_adv(instance: 'Advertisement' , filename):
    username = instance.user.username if instance.user else "anonymus"
    category_name = instance.type_adv.name.split(" "[0]) if instance else "other"
    time_now = timezone.now().date()
    return f"advertisements/category_{category_name}/{time_now}/user_{username}/{filename}"


class Category(models.Model):

    name = models.CharField(max_length=40, null=True, blank=True)
    
    slug = models.CharField(max_length=40, unique=True, null=True, blank=True)
    
    price = models.IntegerField(default=0, null=True, blank=True)  

    coin = models.IntegerField( default=5, null=True, blank=True)
    
    description = models.TextField( null=True, blank=True)
    
    limit_char = models.IntegerField( default=500, null=True, blank=True)
    
    is_active = models.BooleanField( default=True, null=True)
    
    position = models.IntegerField( null=True, blank=True, default=1)
    
    def __str__(self) -> str:
        return self.name
    

class Advertisement(models.Model):
    STATUS = (
        ('publish', 'Publish ✅'),
        ('reject', 'Reject ❌'),
        ('wait_for_pay', 'Wait For Pay 💰'),
        ('wait_for_publish', 'Wait For Publish ⌛️'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_advertisements", null=True, blank=True)
    
    category = models.ForeignKey(Category, related_name="category_advertisements", on_delete=models.CASCADE, null=True, blank=True)
    
    text = models.TextField(default=None, null=True)
    
    file = models.FileField(upload_to=path_file_adv, default=None, null=True, blank=True)
    
    contuct = models.CharField(max_length=40, default=None, null=True,)
    
    status = models.CharField(max_length=30, choices=STATUS, default="wait_for_pay", null=True, blank=True)
    
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    warning_tag = models.BooleanField(default=False, null=True, blank=True)
    
    is_expired = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.username if self.user else self.category.name if self.category else 'other' }"
    
    