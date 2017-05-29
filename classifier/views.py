from django.shortcuts import render
from classifier.models import Document, Community, Tag, Rating, Relationship, KeyWord
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


from django.http import HttpResponseRedirect
from classifier.forms import *
import json



# Create your views here.

def index(request):

    context_dict = {}

    documents = Document.objects.all().distinct()

    context_dict['documents'] = documents

    return render(request, 'classifier/index.html',
        context_dict)


def document(request, document_slug):

    context_dict = {}

    try:
        user = request.user
        document = Document.objects.get(slug=document_slug)
     
        context_dict['document'] = document

        context_dict['communities'] = Community.objects.filter(rating__document=document).distinct()
        #context_dict['tags'] = Tag.objects.filter(document=document).distinct()
        
    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/document.html', context_dict)


def tag(request, tag_slug):

    context_dict = {}

    try:
        tag = Tag.objects.get(slug=tag_slug)

        context_dict['tag'] = tag
        context_dict['communities'] = Community.objects.filter(
            keyword__tag=tag)
        context_dict['related_tags'] = Tag.objects.filter(
            relationship__tag=tag)

    except Tag.DoesNotExist:
        pass

    return render(request, 'classifier/tag.html', context_dict)


def community(request, community_slug):

    context_dict = {}

    try:
        community = Community.objects.get(slug=community_slug)

        context_dict['community'] = community
        context_dict['tags'] = Tag.objects.filter(
            keyword__tag=tag)

    except Community.DoesNotExist:
        pass

    return render(request, 'classifier/community.html', context_dict)


# Add views

def add_member(request):
    pass


@login_required
def add_document(request):

    user = request.user

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            slug = slugify(form.cleaned_data['title'])
            form.save(creator=user, commit=True)
            form.save_m2m()

            return HttpResponseRedirect("/classifier/document/{}".format(slug))

        else:
            print (form.errors)

    else:
        form = DocumentForm()

    return render(request, 'classifier/add_document.html',
        {'form': form})


def review_document(request, document_slug):

    context_dict = {}

    try:
        document = Document.objects.get(slug=document_slug)
        communities = Community.objects.all().distinct()

        context_dict['document'] = document
        context_dict['communities'] = communities


    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/review_document.html', context_dict)



@login_required
def add_community(request):

    user = request.user

    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)

        if form.is_valid():
            slug = slugify(form.cleaned_data['name'])
            form.save(creator=user, commit=True)
            form.save_m2m()

            return HttpResponseRedirect("classifier/community/{}".format(slug))

        else:
            print (form.errors)

    else:
        form = CommunityForm()

    return render(request, 'classifier/add_community.html',
        {'form': form})


@login_required
def add_tag(request):

    user = request.user

    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)

        if form.is_valid():
            slug = slugify(form.cleaned_data['name'])
            form.save(creator=user, commit=True)
            form.save_m2m()

            return HttpResponseRedirect("classifier/tag/{}".format(slug))

        else:
            print (form.errors)

    else:
        form = TagForm()

    return render(request, 'classifier/add_tag.html',
        {'form': form})



# Update and delete views

@login_required
def document_form(request, pk):
    project = Document.objects.get(pk=pk)

    form = DocumentForm(request.POST or None, request.FILES or None, instance=document)
    if form.is_valid():
        form.save(creator=project.creator)
        form.save_m2m()
        return HttpResponseRedirect('/document/{}'.format(document.slug))
    
    return render(request, 'classifier/document_form.html', {'form': form, 'object': document})


def community_form(request, pk):
    project = Community.objects.get(pk=pk)

    form = CommunityForm(request.POST or None, request.FILES or None, instance=document)
    if form.is_valid():
        form.save(creator=project.creator)
        form.save_m2m()
        return HttpResponseRedirect('/community/{}'.format(community.slug))
    
    return render(request, 'classifier/community_form.html', {'form': form, 'object': document})


def tag_form(request, pk):
    project = Tag.objects.get(pk=pk)

    form = TagForm(request.POST or None, request.FILES or None, instance=document)
    if form.is_valid():
        form.save(creator=tag.creator)
        form.save_m2m()
        return HttpResponseRedirect('/tag/{}'.format(tag.slug))
    
    return render(request, 'classifier/tag_form.html', {'form': form, 'object': document})


class DocumentDelete(DeleteView):
    model = Document


class CommunityDelete(DeleteView):
    model = Community


class TagDelete(DeleteView):
    model = Tag

