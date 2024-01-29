from django.db import models

class RegisterPage(models.Model):
    USER_TYPES=(
    ('customer','Customer'),
    ('admin','Admin'),
    )
    user_type=models.CharField(max_length=50,choices=USER_TYPES,default='customer')
    Full_Name=models.CharField(max_length=50)
    User_ID=models.CharField(max_length=50)
    Email=models.EmailField(max_length=50)
    Mobile=models.BigIntegerField()
    Address=models.CharField(max_length=60)
    Password1=models.CharField(max_length=50)
    Password2=models.CharField(max_length=50)

class FeedbackPage(models.Model):
    Name=models.CharField(max_length=50)
    #User_ID=models.CharField(max_length=50)
    Concern=models.CharField(max_length=50)
    Help=models.CharField(max_length=60)
    Feedback=models.CharField(max_length=50)
