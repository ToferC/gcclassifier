from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from classifier.views import DocumentDelete, CommunityDelete, TagDelete
from . import views

# URL patterns

urlpatterns = [
	url(r'^$', views.index, name='classifier_index'),

	# Model urls
	url(r'^document/(?P<document_slug>[\w\-]+)/$',
		views.document, name='document'),
	url(r'^review_document/(?P<document_slug>[\w\-]+)/$',
		views.review_document, name='review_document'),
	url(r'^document_results/(?P<document_slug>[\w\-]+)/$',
		views.document_results, name='document_results'),
	url(r'^community/(?P<community_slug>[w\-]+)/$',
		views.community, name='community'),
	url(r'^tag/(?P<tag_slug>[\w\-]+)/$',
		views.tag, name='tag'),

	# Add object urls
	url(r'^add_document/(?P<pk>\d+)/$',
		views.add_document, 
		name='add_document'),
	url(r'^add_document/$',
		views.add_document, 
		name='add_document'),
	url(r'^upload_file/$',
		views.upload_file, 
		name='upload_file'),
	url(r'^add_community/$',
		views.add_community, 
		name='add_community'),
	url(r'^add_tag/$',
		views.add_tag, 
		name='add_tag'),

	# Formviews for editing
	url(r'^document_form/(?P<pk>\d+)/$',
		views.document_form,
		name='document_form'),
	url(r'^community_form/(?P<pk>\d+)/$',
		views.community_form,
		name='community_form'),
	url(r'^tag_form/(?P<pk>\d+)/$',
		views.tag_form,
		name='tag_form'),

	# Delete views

	url(r'^document_delete/(?P<pk>[0-9]+)/$',
		DocumentDelete.as_view(),
        name="deocument-delete"),
	url(r'community_delete/(?P<pk>[0-9]+)/$',
		CommunityDelete.as_view(),
        name="community-delete"),
	url(r'tag_delete/(?P<pk>[0-9]+)/$',
		TagDelete.as_view(),
        name="tag-delete"),


]