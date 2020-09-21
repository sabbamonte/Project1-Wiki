from django.shortcuts import render, redirect
from markdown2 import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if page == None:
        message = "### Page not found"
        message = markdown(message)
        return render(request, "encyclopedia/entry.html", {'message': message, "title":title})
    else:
        page = markdown(page)
        return render(request, "encyclopedia/entry.html", {'page': page, "title":title})

def search(request):
    if request.method == "GET":
        q = request.GET['q'] 
        if q in util.list_entries():
            return redirect("entry", title=q)
        else:
            results =[]
            for list in util.list_entries():
                if q.upper() in list.upper():
                    results.append(list)
            q = markdown(q)
            return render(request, "encyclopedia/search.html", {"entries": results, "result":q})

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST.get('title')
        content = request.POST.get('new')
        if title in util.list_entries():
            page = "### Page already exists"
            page = markdown(page)
            return render(request, "encyclopedia/entry.html", {"page": page, "title":title})
        if title.isalpha() == False and title.isnumeric() == False:
            page = "### Plaese enter a valid title"
            page = markdown(page)
            return render(request, "encyclopedia/new.html", {"message": page})
        if content.isalpha() == False and content.isnumeric() == False:
            page = "### Plaese enter valid content"
            page = markdown(page)
            return render(request, "encyclopedia/new.html", {"message": page})
        
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {"page":content, "title": title})

def edit(request, title):
    if request.method == "GET":
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"page":page})
    else:
        content = request.POST.get('edit')
        util.save_entry(title,content)
        content = markdown(content)
        return redirect("entry", title=title)

def rand(request):
    if request.method == "GET":
        list = util.list_entries()
        return render(request,"encyclopedia/rand.html", {"random":markdown(util.get_entry(random.choice(list)))})


            
                
