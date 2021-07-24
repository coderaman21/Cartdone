from django.shortcuts import render
from .models import Blogpost
# Create your views here.
def index(request):
    blogs = Blogpost.objects.all()
    return render(request, 'blog/index.html',{'blogs':blogs})

def blogpost(request , myid):
    blogpost = Blogpost.objects.filter(blog_id = myid)
    return render(request, 'blog/blogpost.html',{'blogpost':blogpost[0]})

def blogsearch(request):
    if request.method == 'GET':
        query = request.GET.get('blogsearch')
        print(query)
        allblogs = Blogpost.objects.all()   #fetch all blogs  
        blog_list = []                     #empty list of all blogs
            # serach blog by name
        for blog in allblogs:
            name=blog.title 
            if query in name.lower():
                blog_list.append(blog)

        # check if we could find searched product or not 
        if blog_list and len(query)>3:
            params ={'blog_list':blog_list,'query':query , 'result':True}
        else:
            params = {'query':query ,'result':False}

    return render(request,'blog/search.html',params)