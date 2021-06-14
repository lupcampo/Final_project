#from my_app.models import User
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt



def index (request):
   return render(request,'index.html')

def success (request):
    if not "user_id" in request.session:
        return redirect("/")

    context = {
        "posts": Reef_Post.objects.all()
    }
    return render(request,'success.html',context)


def register(request):

    if request.method== "POST":

        errors=User.objects.validate(request.POST)

        for error in errors.values():
            messages.error(request,error)
            return redirect('/')

        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)

        request.session["user_id"]=user.id
        request.session["user_name"]=f"{user.first_name} {user.last_name}"

        return redirect('/success')

    return redirect('/')



def login(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        
        logged_user=User.objects.filter(email=email)

        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session["user_id"]=logged_user.id
                request.session["user_name"]=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect("/success")
            else:
                return redirect('/')
        else:
            return redirect('/')
    
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


# message=models.CharField(max_length=255)
# poster=models.ForeignKey(User, related_name="user_posts",on_delete=models.CASCADE)
# likes=models.ManyToManyField(User, related_name='liked_posts')
def create_post(request):
    message=request.POST["message"]
    poster = User.objects.get(id=request.session["user_id"])
    
    Reef_Post.objects.create(message=message,poster=poster)


    return redirect('/success')

def like(request,id):

    user=User.objects.get(id=request.session["user_id"])
    post=Reef_Post.objects.get(id=id)

    post.likes.add(user)

    return redirect('/success')
