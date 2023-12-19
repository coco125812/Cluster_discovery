from django.db import models

# Create your models here.
class Node(models.Model):
    node_name = models.CharField(max_length=200)
    ip = models.GenericIPAddressField()
    is_master = models.BooleanField(default=False)
    last_heartbeat = models.DateTimeField(auto_now=True)
    
