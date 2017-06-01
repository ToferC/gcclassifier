from django.shortcuts import render
from classifier.models import Document, Community, Tag, Rating, Relationship, KeyWord
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.forms import modelformset_factory

from django.core import serializers

from classifier.forms import RatingForm, DocumentForm, TagForm, RatingForm, CommunityForm

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

        context_dict['ratings'] = Rating.objects.filter(document=document).distinct()
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
        machine_ratings = serializers.serialize( "python",
            Rating.objects.filter(document=document, user_generated=False),
            fields=(
                'atip_community',
                'materiel_community',
                'procurement_community',
                'real_property_community',
                'evaluator_community',
                'communication_community',
                'regulator_community',
                'financial_community',
                'im_community',
                'it_community',
                'auditor_community',
                'security_community',
                'hr_community',
                'policy_community',
                'science_community',
                'service_community',)
            )
        user_ratings = serializers.serialize( "python",
            Rating.objects.filter(document=document, user_generated=True),
            fields=(
                'atip_community',
                'materiel_community',
                'procurement_community',
                'real_property_community',
                'evaluator_community',
                'communication_community',
                'regulator_community',
                'financial_community',
                'im_community',
                'it_community',
                'auditor_community',
                'security_community',
                'hr_community',
                'policy_community',
                'science_community',
                'service_community',)
            )
        
        context_dict['document'] = document
        context_dict['user_ratings'] = user_ratings
        context_dict['machine_ratings'] = machine_ratings

        if request.method == 'POST':

            form = RatingForm(request.POST)

            if form.is_valid():

                form.save(creator=request.user, document=document,
                    user_generated=True, commit=True)
                form.save_m2m()

                return HttpResponseRedirect("/classifier/document/{}".format(document.slug))


            else:
                print("Form validation error")

        else:
            form = RatingForm()
            context_dict['form'] =  form

    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/review_document.html',
        context_dict)


def document_results(request, document_slug):

    context_dict = {}

    try:
        document = Document.objects.get(slug=document_slug)
        machine_ratings = Rating.objects.filter(document=document).filter(user_generated=False)
        user_ratings = Rating.objects.filter(document=document).filter(user_generated=True)

        num_user_ratings = len(user_ratings)
        num_machine_ratings = len(machine_ratings)

        context_dict['num_user_ratings'] = num_user_ratings
        context_dict['num_machine_ratings'] = num_machine_ratings

        context_dict['atip_community'] = 0
        context_dict['materiel_community'] = 0
        context_dict['procurement_community'] = 0
        context_dict['real_property_community'] = 0
        context_dict['evaluator_community'] = 0
        context_dict['communication_community'] = 0
        context_dict['regulator_community'] = 0
        context_dict['financial_community'] = 0
        context_dict['im_community'] = 0
        context_dict['it_community'] = 0
        context_dict['auditor_community'] = 0
        context_dict['security_community'] = 0
        context_dict['hr_community'] = 0
        context_dict['policy_community'] = 0
        context_dict['science_community'] = 0
        context_dict['service_community'] = 0

        for rating in user_ratings:
            context_dict['atip_community'] += rating.atip_community
            context_dict['materiel_community'] += rating.materiel_community
            context_dict['procurement_community'] += rating.procurement_community
            context_dict['real_property_community'] += rating.real_property_community
            context_dict['evaluator_community'] += rating.evaluator_community
            context_dict['communication_community'] += rating.communication_community
            context_dict['regulator_community'] += rating.regulator_community
            context_dict['financial_community'] += rating.financial_community
            context_dict['im_community'] += rating.im_community
            context_dict['it_community'] += rating.it_community
            context_dict['auditor_community'] += rating.auditor_community
            context_dict['security_community'] += rating.security_community
            context_dict['hr_community'] += rating.hr_community
            context_dict['policy_community'] += rating.policy_community
            context_dict['science_community'] += rating.science_community
            context_dict['service_community'] += rating.service_community

        context_dict['atip_community'] = context_dict['atip_community'] / len(user_ratings)
        context_dict['materiel_community'] = context_dict['materiel_community'] / len(user_ratings)
        context_dict['procurement_community'] = context_dict['procurement_community'] / len(user_ratings)
        context_dict['real_property_community'] = context_dict['real_property_community'] / len(user_ratings)
        context_dict['evaluator_community'] = context_dict['evaluator_community'] / len(user_ratings)
        context_dict['communication_community'] = context_dict['communication_community'] / len(user_ratings)
        context_dict['regulator_community'] = context_dict['regulator_community'] / len(user_ratings)
        context_dict['financial_community'] = context_dict['financial_community'] / len(user_ratings)
        context_dict['im_community'] = context_dict['im_community'] / len(user_ratings)
        context_dict['it_community'] = context_dict['it_community'] / len(user_ratings)
        context_dict['auditor_community'] = context_dict['auditor_community'] / len(user_ratings)
        context_dict['security_community'] = context_dict['security_community'] / len(user_ratings)
        context_dict['hr_community'] = context_dict['hr_community'] / len(user_ratings)
        context_dict['policy_community'] = context_dict['policy_community'] / len(user_ratings)
        context_dict['science_community'] = context_dict['science_community'] / len(user_ratings)
        context_dict['service_community'] = context_dict['service_community'] / len(user_ratings)

        context_dict['document'] = document

    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/review_document.html',
        context_dict)

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

