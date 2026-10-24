from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    place = models.CharField(max_length=100)


class Marks(models.Model):
    marks = models.IntegerField()


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    feed_back = models.TextField()

    class Meta:
        db_table = 'teacher'
class StudentDetails(models.Model):
    name = models.CharField(max_length = 200)
    valid = models.BooleanField(default = False)
    image = models.ImageField(upload_to = 'student/')
