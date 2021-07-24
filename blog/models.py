from django.db import  models


# Create your models here.
class Blogpost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50 , default='')
    content = models.CharField(max_length=1000 , default='')
    heading = models.CharField(max_length=50,default='')
    heading_content = models.CharField(max_length=1000 , default='')
    subheading = models.CharField(max_length=50,default='')
    subheading_content = models.CharField(max_length=1000 , default='')
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to = 'blog/image' , default='')

    def __str__(self):
        return self.title
