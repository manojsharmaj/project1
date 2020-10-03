from django import forms
from django.shortcuts import render
import markdown2,re,random

from . import util

"""  index function provide entry for GET request 
     and matches substring for search box"""

def index(request):
    if request.method =="GET":      # Create list of all entries
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        title=request.POST.get('q')    # Getting substring from search box 
        if title:
            entries=util.list_entries()
            thislist=[]
            for entry in entries:
                if re.search(title, entry, re.IGNORECASE):  # Match for substring
                    thislist.append(entry)
            return render(request,"encyclopedia/index.html",{   # Return matched substring titles
                "entries":thislist
            })  
        else:
            return render(request,"encyclopedia/error.html",{   # if user press return with search box left blank
                "mesg":"!!!Please Type Title of Page"
            })


""" entry function provide entry as per user demand """
def entry(request,title):
    if request.method == "GET":
        headings=util.list_entries()
        for heading in headings:
            if heading.lower()==title.lower():  # Check user typed heading match with saved entries
                data = util.get_entry(title)
                test = markdown2.markdown(data)
                return render(request,"encyclopedia/entry.html",{       # return entry if heading matched
                    "entry":test,"name":heading
                })
        return render(request,"encyclopedia/error.html",{        # return message if page does not exist 
            "mesg":"Page Not Found"
        })
    
""" new_entry function create new entry page """           
def new_entry(request):
    if request.method == "POST":
        title = request.POST.get('title')       # Getting title of entry
        content = request.POST.get('content')   # Getting content from user to be saved 
        entries = util.list_entries()
        if title:
            for entry in entries:
                if entry.lower() == title.lower():  # check entry already exist or not
                    return render(request,"encyclopedia/error.html",{
                        "mesg":"Title already exist"
                        })
                else:
                    util.save_entry(title, content)  # Save new entry          
    return render(request,"encyclopedia/new.html")


""" edit function alter old entries """
def edit(request,name):
    if request.method=="GET":
        data=util.get_entry(name)   # Get old entry to display to user during editing 
        return render(request,"encyclopedia/edit.html",{
            "entry":data, "name":name
        })
    else:
        content=request.POST.get('cont')    # Get edited content of entry
        util.save_entry(name,content)       # Save edited content
        return render(request,"encyclopedia/index.html",{  #retuun new list of entries  
            "entries": util.list_entries()  
        }) 


""" Random function displays random entries"""
def rand(request):
    entries=util.list_entries()         # Getting list of all entries
    title=random.choice(entries)        # Randomly select any one entry
    content=util.get_entry(title)       # Getting content of selected entry 
    content=markdown2.markdown(content)     # Convert content from markdown to HTML
    return render(request,"encyclopedia/random.html",{
        "title":title ,"content":content
    })                        
    
