from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name= models.CharField(max_length=100)
    designation= models.CharField(max_length=100)
    email= models.EmailField()
    phone=models.CharField(max_length=15)
    linkedin= models.URLField()
    github= models.URLField()
    summary= models.TextField()
    location= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}"

# class Project(models.Model):
#     projectname=models.CharField(max_length=100)
#     description=models.TextField()
#     technologies=models.CharField(max_length=200)
#     githuburl=models.URLField(max_length=100)

#     resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class Education(models.Model):
    degree= models.CharField(max_length=100)
    course= models.CharField(max_length=100)
    college= models.CharField(max_length=100)
    completed_year= models.IntegerField()
    grade= models.CharField(max_length=100)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.degree} - {self.course}"

class Project(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField()
    tools= models.CharField(max_length=100)

    resume=models.ForeignKey(Resume,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Experience(models.Model):
    company=models.CharField(max_length=100)
    role= models.CharField(max_length=100)
    start_date= models.CharField(max_length=100)
    end_date= models.CharField(max_length=100)
    role_description= models.TextField()

    resume=models.ForeignKey(Resume,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company}"

category_choices = [('languages',"languages"),('frontend','Frontend'),('backend','Backend'),('tools','Tools'),('database','Database'),('methodologies','Methodologies')]

class Skill(models.Model):
    name=models.CharField(max_length=100)
    category = models.CharField(max_length=100,choices= category_choices, null=True)
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Certifications(models.Model):
    name= models.CharField(max_length=100)
    resume= models.ForeignKey(Resume,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Language(models.Model):
    name= models.CharField(max_length=100)
    resume= models.ForeignKey(Resume,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

