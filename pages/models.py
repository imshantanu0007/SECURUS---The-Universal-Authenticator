from django.db import models

class person(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    mobile_number= models.CharField(max_length=10)
    user_id=models.CharField(max_length=20, default="999999")
    def __str__(self):
        return self.mobile_number
