from django.shortcuts import render
from classifier.models import Document, File, Community, Tag, Rating, Relationship, KeyWord
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.forms import modelformset_factory

from django.core import serializers

from classifier.forms import RatingForm, DocumentForm, FileForm, TagForm, RatingForm, CommunityForm

from django.http import HttpResponseRedirect
from classifier.forms import *

from classifier.utility_scripts import load_obj
from classifier.text_preprocessing import tokenize, pre_process, find_language
from classifier.text_preprocessing import find_keywords, predict_communities
from classifier.process_document import process_document

import json


# Load classifier

multilabel_clf = load_obj("multilabel_clf")

# Create your views here.

def index(request):

    context_dict = {}

    documents = Document.objects.all().distinct().order_by('-created_date')

    context_dict['documents'] = documents

    return render(request, 'classifier/index.html',
        context_dict)


def document(request, document_slug):

    context_dict = {}

    try:
        user = request.user
        document = Document.objects.get(slug=document_slug)
     
        context_dict['document'] = document

        keywords = KeyWord.objects.filter(document=document)

        context_dict['keywords'] = keywords

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
            )        #context_dict['tags'] = Tag.objects.filter(document=document).distinct()

        context_dict['user_ratings'] = user_ratings
        context_dict['machine_ratings'] = machine_ratings

    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/document.html', context_dict)


def tag(request, tag_slug):

    context_dict = {}

    try:
        tag = Tag.objects.get(slug=tag_slug)

        context_dict['tag'] = tag

        context_dict['from_broader_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Broader term")

        context_dict['from_narrower_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Narrower term")

        context_dict['from_related_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Related term")

        context_dict['from_use_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Use")

        context_dict['from_use_for_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Used for")

        context_dict['from_translation_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Translation")

        context_dict['from_subject_category_relationships'] = Relationship.objects.filter(
            from_tag=tag,
            relationship_type="Subject category")

        context_dict['to_broader_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Broader term")

        context_dict['to_narrower_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Narrower term")

        context_dict['to_related_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Related term")

        context_dict['to_use_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Use")

        context_dict['to_use_for_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Used for")

        context_dict['to_translation_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Translation")

        context_dict['to_subject_category_relationships'] = Relationship.objects.filter(
            to_tag=tag,
            relationship_type="Subject category")

        context_dict['keyword_documents'] = KeyWord.objects.filter(
            tag=tag)

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
@login_required
def add_member(request):
    pass


@login_required
def add_document(request, pk=None):

    user = request.user
    title = None

    if pk:
        file = File.objects.get(pk=pk)

        title = file.name
        text = process_document(file.file.url)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            slug = slugify(form.cleaned_data['title'])
            text = form.cleaned_data['content']
            user_keywords = form.cleaned_data['user_keywords']

            low_keywords = user_keywords.lower()
            split_keywords = low_keywords.split(",")

            processed_keywords = ", ".join(split_keywords)

            language = find_language(text)
            rake_keywords = find_keywords(text)

            form.save(creator=user,
                language=language,
                user_keywords=processed_keywords,
                rake_keywords=rake_keywords,
                commit=True)

            form.save_m2m()

            text = form.cleaned_data['content']

            processed_text = pre_process(text)
            predicted_values = multilabel_clf.predict_proba(processed_text)
            predicted_output = predict_communities(predicted_values)

            document = Document.objects.get(slug=slug)
            tags = Tag.objects.all()

            tag_slugs = [tag.slug for tag in tags]

            # Associate tags from user and rake keywords
            
            for keyword in split_keywords:
                if slugify(keyword) in tag_slugs:
                    try:
                        kw = KeyWord(
                            document=document,
                            tag=Tag.objects.get(slug=slugify(keyword)))
                        kw.save()
                    except Tag.DoesNotExist:
                        pass

            for keyword in rake_keywords:
                if slugify(keyword) in tag_slugs:
                    try:
                        kw = KeyWord(
                            document=document,
                            tag=Tag.objects.get(slug=slugify(keyword)))
                        kw.save()
                    except Tag.DoesNotExist:
                        pass

            rating = Rating(
                creator=user,
                document=document,
                atip_community = predicted_output['ATIP'],
                materiel_community = predicted_output['materiel_management'],
                procurement_community = predicted_output['procurement_specialists'],
                real_property_community = predicted_output['real_property'],
                evaluator_community = predicted_output['evaluators'],
                communication_community = predicted_output['communication'],
                regulator_community = predicted_output['regulators'],
                financial_community = predicted_output['financial_officers'],
                im_community = predicted_output['information_management'],
                it_community = predicted_output['information_technology'],
                auditor_community = predicted_output['internal_auditors'],
                security_community = predicted_output['security_specialist'],
                hr_community = predicted_output['human_resources'],
                policy_community = predicted_output['policy'],
                science_community = predicted_output['fed_science_tech'],
                service_community = predicted_output['services'],
                user_generated=False,
                )

            rating.save()

            return HttpResponseRedirect("/classifier/document/{}".format(slug))

        else:
            print (form.errors)

    else:
        if title:
            form = DocumentForm(initial={'title':title, 'content':text})
        else:
            form = DocumentForm()

    return render(request, 'classifier/add_document.html',
        {'form': form})


@login_required
def upload_file(request):

    user = request.user

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            
            new_file = form.save(creator=user, commit=True)

            file_pk = new_file.pk

            return HttpResponseRedirect(f"/classifier/add_document/{new_file.pk}")

        else:
            print (form.errors)

    else:
        form = FileForm()

    return render(request, 'classifier/upload_file.html',
        {'form': form})

@login_required
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
        context_dict['num_user_ratings'] = len(user_ratings)
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

        try:
            context_dict['atip_community'] = context_dict['atip_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['atip_community'] = 0

        try:
            context_dict['materiel_community'] = context_dict['materiel_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['materiel_community'] = 0

        try:
            context_dict['procurement_community'] = context_dict['procurement_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['procurement_community'] = 0

        try:
            context_dict['real_property_community'] = context_dict['real_property_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['real_property_community'] = 0

        try:
            context_dict['evaluator_community'] = context_dict['evaluator_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['evaluator_community'] = 0

        try:
            context_dict['communication_community'] = context_dict['communication_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['communication_community'] = 0

        try:
            context_dict['regulator_community'] = context_dict['regulator_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['regulator_community'] = 0

        try:
            context_dict['financial_community'] = context_dict['financial_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['financial_community'] = 0

        try:
            context_dict['im_community'] = context_dict['im_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['im_community'] = 0

        try:
            context_dict['it_community'] = context_dict['it_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['it_community'] = 0

        try:
            context_dict['auditor_community'] = context_dict['auditor_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['auditor_community'] = 0

        try:
            context_dict['security_community'] = context_dict['security_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['security_community'] = 0

        try:
            context_dict['hr_community'] = context_dict['hr_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['hr_community'] = 0

        try:
            context_dict['policy_community'] = context_dict['policy_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['policy_community'] = 0

        try:
            context_dict['science_community'] = context_dict['science_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['science_community'] = 0
        try:
            context_dict['service_community'] = context_dict['service_community'] / num_user_ratings
        except ZeroDivisionError:
            context_dict['service_community'] = 0

        context_dict['document'] = document

    except Document.DoesNotExist:
        pass

    return render(request, 'classifier/document_results.html', context_dict)


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

