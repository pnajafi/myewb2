"""myEWB GroupTopic forms

This file is part of myEWB
Copyright 2009 Engineers Without Borders (Canada) Organisation and/or volunteer contributors
Some code derived from Pinax, copyright 2008-2009 James Tauber and Pinax Team, licensed under the MIT License

Created on: 2009-08-13
@author: Joshua Gorner
"""

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from group_topics.models import GroupTopic
from tag_app.models import TagAlias

class GroupTopicForm(forms.ModelForm):
    
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'tinymce '}))

    class Meta:
        model = GroupTopic
        fields = ('title', 'body', 'tags', 'send_as_email')
        
    # Check tag aliases: see tag_app.TagAlias
    # (should we delegate this to tag_app? seems to fit better there...)
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')

        # the jquery autocomplete enforces the commas, but django's tagging
        # is actually much more flexible (supports quotes, etc).  If we take 
        # advantage of that, we'll need to update our multiple tag recognition
        # as well
        taglist = tags.split(',')
        tags = ""
        for tag in taglist:
            tag = tag.strip()
            
            # look up alias - if one exists, use the real tag
            try:
                alias = TagAlias.objects.get(alias=tag)
                tags += alias.tag.name
                # should the alias just store the tag's text, instead of a 
                # reference to the object, for db efficiency?
                
            # otherwise, leave it as is...
            except ObjectDoesNotExist:
                tags += tag + ","
        
        return tags
        