from django.db import models

# Create your models here.

class UserManager (models.Manager):
    def validate(self, postData):
        errors={}
        if len(postData["first_name"])<2:
            errors["first_name"]="first name must be longer than 2 characters"
        if len(postData["last_name"])<2:
            errors["last_name"]="last name must be longer than 2 characters"
        if len(postData["email"])<2:
            errors["email"]="email must be longer than 2 characters"
        if len(postData["password"])<2:
            errors["password"]="password must be longer than 2 characters"
        if postData["password"] !=postData["confirm_password"]:
            errors["password_confirmation"]="password does not match"

        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    objects=UserManager()
    #confirm_password=models.CharField(max_length=255)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #user_posts
    #iked_posts

class Reef_Post(models.Model):
    message=models.CharField(max_length=255)
    poster=models.ForeignKey(User, related_name="user_posts",on_delete=models.CASCADE)
    likes=models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment=models.CharField(max_length=255)
    poster=models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    reef_post=models.ForeignKey(Reef_Post, related_name='post_comments', on_delete=models.CASCADE)
    

#User.objects.validate(request.POST)