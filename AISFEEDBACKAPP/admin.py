from django.contrib import admin
from .models import RegisterPage,FeedbackPage



class AdminRegisterPage(admin.ModelAdmin):
    list_display=['id','user_type','User_ID','Full_Name','Email','Mobile','Address','Password1']
admin.site.register(RegisterPage,AdminRegisterPage)

class AdminFeedbackPage(admin.ModelAdmin):
    list_display=['id','Name','Concern','Help','Feedback']
admin.site.register(FeedbackPage,AdminFeedbackPage)
# Register your models here.


# Register your models here.
