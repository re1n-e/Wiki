from django.shortcuts import render
import markdown2
from . import util
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


def md_to_html(title):
    try:
        entry = util.get_entry(title)
        if entry is not None:
            mark_d = markdown2.markdown(entry)
            return mark_d
        else:
            return None
    except Exception as e:
        print(f"An error occured: {str(e)}")
        return None 


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            titles_lower = [entry.lower() for entry in util.list_entries()]
            if title.lower() in titles_lower:
                return render(
                    request, "encyclopedia/error.html", {"error": "Page already exists"}
                )
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse("encyclopedia:wiki_page", args=[title])
                )
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": "Title and content are required"},
            )
    else:
        return render(request, "encyclopedia/newpage.html")


def edit_page(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        filename = f"entries/{title}.md"
        try:
            with open(filename, "r") as f:
                content = f.read()
            return render(
                request,
                "encyclopedia/editpage.html",
                {"content": content, "title": title},
            )
        except FileNotFoundError:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": "Page not found"},
            )
        except Exception as e:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": f"Error reading file: {str(e)}"},
            )
    else:
        return render(
            request, "encyclopedia/error.html", {"error": "Invalid request method"}
        )

def save(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = request.POST.get("content")

        if title and content:
            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse("encyclopedia:wiki_page", args=[title])
            )
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": "Title and content are required"},
            )

def randoom(request):
    random_page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:wiki_page", args=[random_page]))

def wiki_entry(request,title):
    try:
        response = md_to_html(title)
        if response is None:
            return render(request,"encyclopedia/error.html",{
                "error": "Page doesn't exist"
            })
        else:
            return render(request, "encyclopedia/entry.html",{
                "title" : title.title(),
                "message": response
            })
    except Exception as e:
        print(f"An error occurred: {str(e)}")  
        return render(request, "encyclopedia/error.html", {
            "error": "An error occurred while processing the request"
        })

def exist(title, pages):
    a, res = len(title) - 1, []
    for entry in pages:
        for j in range(len(entry)-a):
            if title[0] == entry[j]:
                if title == entry[j:j+a+1]:
                    res.append(entry)
    return res                


@csrf_exempt
def querry_entry(request):
    try:
        title = request.GET.get('q', '').lower().strip()
        if title:
            pages = [page.lower() for page in util.list_entries()]
            if title in pages:
                response = md_to_html(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title.title(),
                    "message": response
                })
            elif res := exist(title, pages):
                return render(request, "encyclopedia/search.html",{
                    "entries": res
                })
        return render(request, "encyclopedia/error.html", {
            "error": "Page doesn't exist"
        })
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render(request, "encyclopedia/error.html", {
            "error": "An error occurred while processing the request"
        })
