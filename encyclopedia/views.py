from django.shortcuts import render, redirect
from markdown import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page not found."
        })
    
    markdowner = Markdown()
    html_content = markdowner.convert(entry_content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search_entry(request):
    markdowner = Markdown()
    if request.method == "POST":
        query = request.POST.get('q','').strip().lower()
        if query == "":
            return render(request, "encyclopedia/search.html",{
                "query":query,
                "search_result":None
    })
    saved_entries = util.list_entries()

    matching_entries = [x for x in saved_entries if query in x.lower()]
    if len(matching_entries)==1 and query == matching_entries[0].lower():
        return render(request, "encyclopedia/entry.html", {
            "entry_name": query,
            "content": markdowner.convert(util.get_entry(query))
        })
    else:
        return render(request, 'encyclopedia/search.html', {
            "query": query,
            "search_results": matching_entries if matching_entries else None
        })
    return render(request, "encyclopedia/error.html", {
        "message": "Hmm, something went wrong."
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", 
                            min_length=1, 
                            max_length=50, 
                            widget=forms.TextInput(attrs={'placeholder': "Enter a descriptive title"}))
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'style': 'width: 100%', 'style': 'height: 100%', 
                                                                            'placeholder': "What do you know about this specific subject?"}))

def create_page(request):

    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                form.add_error('title', "Failed to publish new entry (already exists in Wiki database).")
                return render(request, "encyclopedia/create.html",{
                    "new_form":form
                })
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('wiki:entry', kwargs={"title":title}))
        
    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/create.html', {
        "new_form":form
    })

class EditContentForm(forms.Form):
    content = forms.CharField(label="Edit Markdown content",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'style': 'width: 100%', 'style': 'height: 100%'}))

def update_entry(request, title):

    retrieve_content = util.get_entry(title)
    if retrieve_content is None:
        return render(request, 'encyclopedia/error.html', {
            "message":"This entry does not exist."
        })
    if request.method == 'POST':
        form = EditContentForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content']
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse('wiki:entry', kwargs={"title":title}))
    else:
        form = EditContentForm(initial={'content': retrieve_content})
    return render(request, "encyclopedia/edit.html", {
        "edit_form" : form,
        "title": title
    })


def random_entry(request):
    save_entries = util.list_entries()
    if not save_entries:
        return redirect('wiki:index')
    selected_entry = random.choice(save_entries)
    return redirect(request, 'wiki:entry', title=selected_entry)