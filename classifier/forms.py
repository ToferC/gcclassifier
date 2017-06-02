from django import forms
from django.forms import widgets, BaseModelFormSet
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from classifier.models import Document, File, Community, Tag, Rating, KeyWord, Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineField

# Forms

class DocumentForm(forms.ModelForm): 
    """Form for users to add images"""

    class Meta:
        model = Document
        fields = "__all__"
        exclude = ['creator', 'created_date', 'edited_date',
        'language', 'rake_keywords', 'file', 'slug']

    def __init__(self, *args, **kwargs):

        super(DocumentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<br><a committment="button" class="btn btn-default"
                    ref="classifier/document/{{ document.slug }}">Cancel</a> """),
                Submit('save', 'Save'),))

    def save(self, creator, language, rake_keywords, commit=False):
        instance = super(DocumentForm, self).save(commit=False)
        instance.creator=creator
        instance.language=language
        instance.rake_keywords=rake_keywords
        instance.save()
        return instance


class FileForm(forms.ModelForm): 
    """Form for users to add images"""

    class Meta:
        model = File
        fields = "__all__"
        exclude = ['creator', 'created_date', 'edited_date']

    def __init__(self, *args, **kwargs):

        super(FileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<br><a committment="button" class="btn btn-default"
                    ref="classifier/add_document">Cancel</a> """),
                Submit('save', 'Save'),))

    def save(self, creator, commit=False):
        instance = super(FileForm, self).save(commit=False)
        instance.creator=creator
        instance.save()
        return instance

class CommunityForm(forms.ModelForm): 
    """Form for users to add images"""

    class Meta:
        model = Community
        fields = "__all__"
        exclude = ['creator',
        'created_date', 'edited_date', 'slug']

    def __init__(self, *args, **kwargs):

        super(CommunityForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<br><a committment="button" class="btn btn-default"
                    ref="classifier/document/{{ document.slug }}">Cancel</a> """),
                Submit('save', 'Save'),))

    def save(self, creator, commit=False):
        instance = super(CommunityForm, self).save(commit=False)
        instance.creator=creator
        instance.save()
        return instance


class TagForm(forms.ModelForm): 
    """Form for users to add images"""

    class Meta:
        model = Tag
        fields = "__all__"
        exclude = ['creator', 'user_generated',
        'created_date', 'edited_date', 'slug']

    def __init__(self, *args, **kwargs):

        super(TagForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<br><a committment="button" class="btn btn-default"
                    ref="classifier/tag/{{ tag.slug }}">Cancel</a> """),
                Submit('save', 'Save'),))

    def save(self, creator, commit=False):
        instance = super(TagForm, self).save(commit=False)
        instance.creator=creator
        instance.save()
        return instance


class RatingForm(forms.ModelForm):
    """Form for users to add images"""

    class Meta:
        model = Rating
        fields = "__all__"
        exclude = ["creator", "document", "user_generated",
        "created_date", "edited_date"]

    def __init__(self, *args, **kwargs):

        super(RatingForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<br><a committment="button" class="btn btn-default"
                    ref="classifier/">Cancel</a> """),
                Submit('save', 'Save'),))

    def save(self, creator, document, user_generated=False, commit=False):
        instance = super(RatingForm, self).save(commit=False)
        instance.creator=creator
        instance.document=document
        instance.user_generated=user_generated
        instance.save()
        return instance
