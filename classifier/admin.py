from django.contrib import admin
from classifier.models import Document, Community, Tag
from classifier.models import KeyWord, Rating, Relationship

class DocumentAdmin(admin.ModelAdmin):
	prepopulated_fields = {
	'slug': ('title',)
	}
	list_display = (
		'title',
		'creator',
		'created_date',
		'edited_date',
		'language',
		'published')


class CommunityAdmin(admin.ModelAdmin):
	prepopulated_fields = {
	'slug': ('name',)
	}
	list_display = (
		'name',
		'creator',
		'created_date',
		'edited_date'
		)


class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {
	'slug': ('name',)
	}
	list_display = (
		'name',
		'creator',
		'created_date',
		'edited_date'
		)


class RatingAdmin(admin.ModelAdmin):
	list_display = (
		'document',
		'community',
		'user_generated',
		'created_date',
		'edited_date',
		)


class KeyWordAdmin(admin.ModelAdmin):
	list_display = (
		'community',
		'tag',
		'rating',
		'created_date',
		'edited_date',
		)


class RelationshipAdmin(admin.ModelAdmin):
	list_display = (
		'from_tag',
		'to_tag',
		'relationship_type',
		'rating',
		'created_date',
		'edited_date',
		)

# Register your models here.

admin.site.register(Document, DocumentAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(KeyWord, KeyWordAdmin)
admin.site.register(Relationship, RelationshipAdmin)