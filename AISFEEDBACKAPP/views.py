from django.shortcuts import render,redirect
from .models import RegisterPage,FeedbackPage
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np





user1=""
def loginpage(request):
    if request.method == "GET":
        return render(request, 'loginpage.html')

    else:
        global user1
        user1 = request.POST.get('userid').lower()
        password1 = request.POST.get('password')
        print(user1,password1)

        client = authenticate(username=user1, password=password1)
        if client is not None:

            login(request, client)
            if client.is_staff:  # Check if the user is an admin
                return redirect('admin_page')  # Redirect to the admin panel
            else:
                return redirect('feedbackpage') 
               
             # Redirect to the customer feedback page
        else:
            messages.error(request, 'Invalid login credentials. Please try again')
            return redirect('loginpage')

            

def registerpage(request):
    if request.method == 'GET':
        rdata = RegisterPage.objects.all()
        return render(request, 'registerpage.html', {'rdata': rdata})
    else:
        usertype = request.POST.get('usertype')

        fname = request.POST.get('fullname')
        userid = request.POST.get('userid').lower()
        email = request.POST.get('emailid')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-=_+<>?]).{8,}$')

        if password1 == password2 and password_pattern.match(password1):
            user = User.objects.create_user(username=userid, email=email, password=password1)
            user.is_staff = True if usertype == 'admin' else False
            user.save()
            

            RegisterPage(
                user_type=usertype,
                Full_Name=fname,
                User_ID=userid,
                Email=email,
                Mobile=mobile,
                Address=address,
                Password1=password1,
                Password2=password2,
             ).save()

            messages.success(request, 'Registration successful please login here!')

            if usertype == 'admin' or usertype == 'customer':
                return redirect('loginpage')
            

            
        else:
            if password1 != password2:
                messages.error(request, 'Password and confirm password must be the same.')
            if not password_pattern.match(password1):
                messages.error(request, 'Password must contain lowercase, uppercase, special character, and digits.')

            return render(request, 'registerpage.html')

the_user=None
@login_required(login_url='loginpage')


def feedbackpage(request):
    if request.method == "GET":
        global the_user
        the_user = RegisterPage.objects.get( User_ID=user1)
        print(the_user)
        return render(request, 'feedbackpage.html',{'user':the_user})
    else:
        name = request.POST.get('name')
        userid = request.POST.get('userid')  
        concern = request.POST.get('concern')
        help1 = request.POST.get('help')
        feedback = request.POST.get('feedback')
        FeedbackPage(
            Name=the_user.Full_Name,
            #User_ID=userid,  
            Concern=concern,
            Help=help1,
            Feedback=feedback
        ).save()
        return render(request, 'submission.html')

    


@login_required(login_url='loginpage')
def admin_page(request):
    if request.method == "GET":
        data1 = FeedbackPage.objects.all()
        total_feedbacks = data1.count()
        data = RegisterPage.objects.all()
        total_registrations = data.count()
        total_customers = RegisterPage.objects.count()
        total_feedbacks = FeedbackPage.objects.count()
        the_user = RegisterPage.objects.get(User_ID=request.user.username)

        labels = ['Customers', 'Feedbacks']
        sizes = [total_customers, total_feedbacks]
        colors = ['purple', 'orange']
        
        # Plotting the pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Saving the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Embedding the image in the HTML response
        image_uri = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        context = {'image_uri': image_uri}

        # Set a larger figure size
        fig, ax = plt.subplots(figsize=(5, 5))  # Adjust width and height as needed

        # Create a bar graph with different colors
        labels = ['Feedbacks', 'Registrations']
        counts = [total_feedbacks, total_registrations]
        colors = ['blue', 'darkgreen']  # Specify colors for each bar

        bars = plt.bar(labels, counts, color=colors)
        plt.xlabel('Categories')
        plt.ylabel('Counts')
        plt.title('Feedbacks vs Registrations')

        # Add count annotations above each bar
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.1, str(count), ha='center')

        # Saving the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Embedding the image in the HTML response
        image_uri = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        context1 = {'image_uri': image_uri}
        return render(request, 'adminpage.html', {'the_user':the_user,'data1': data1, 'context1':context1, 'context':context, 'total_feedbacks': total_feedbacks, 'total_registrations': total_registrations})

@login_required(login_url='loginpage')
def admin_panel(request):
    if request.method=="GET":
        #data=RegisterPage.objects.all()
        data1= FeedbackPage.objects.all()
        total_feedbacks = data1.count()    
        the_user = RegisterPage.objects.get(User_ID=request.user.username)
       
        
        return render(request, 'AdminPageFeedbackData.html',{'the_user':the_user,'data1':data1,'total_feedbacks': total_feedbacks})

@login_required(login_url='loginpage')
def admin_panel1(request):
    if request.method=="GET":
        data=RegisterPage.objects.all()
        total_registrations = data.count()
        #data1= FeedbackPage.objects.all()
        the_user = RegisterPage.objects.get(User_ID=request.user.username)

        return render(request, 'AdminPageRegisterData.html',{'the_user': the_user,'data':data, 'total_registrations':total_registrations})

def submissionpage(request):
    return render(request,'submission.html')



    



def logoutpage(request):
    logout(request)
    return redirect('loginpage')  
      

            
                
           

