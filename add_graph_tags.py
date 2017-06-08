
# coding: utf-8

# ## Parsing Core Subject Thesaurus

# Import django project

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from classifier.models import Relationship, Tag
from gc_classifier.users.models import User

from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When

from django.template.defaultfilters import slugify
# In[1]:

import xml.etree.ElementTree as ET
import networkx as nx
from collections import defaultdict

# In[2]:

data_dir = "/home/chris/data/Thesaurus"

xml = "CST20160704.xml"


# In[3]:

tree = ET.parse(os.path.join(data_dir, xml))

root = tree.getroot()


# In[4]:

subject_categories = defaultdict(int)
descriptors = []
non_descriptors = []
relationships = []
existing_slugs = []

for concept in root:
    
    data = []
    for child in concept:
        data.append((child.tag, child.text))
        
    descriptor = data[0][1]
        
    if data[0][0]  == "DESCRIPTOR":
        if slugify(descriptor) not in existing_slugs:
            tag = Tag.objects.get_or_create(name=descriptor,
                creator=User.objects.get(pk=1),
                user_generated=False,
                slug=slugify(descriptor))
            existing_slugs.append(slugify(descriptor))

        
    elif data[0][0] == "NON-DESCRIPTOR":
        if slugify(descriptor) not in existing_slugs:
            tag = Tag.objects.get_or_create(name=descriptor,
                creator=User.objects.get(pk=1),
                user_generated=False,
                approved=False,
                slug=slugify(descriptor))
            existing_slugs.append(slugify(descriptor))

    for category, text in data:
        
        if category == "French":
            relationships.append((text, descriptor, "Translation"))
        elif category == "Use":
            relationships.append((descriptor, text, "Use"))
        elif category == "UsedFor":
            relationships.append((text, descriptor, "Used for"))
        elif category == "BroaderTerm":
            relationships.append((descriptor, text, "Broader term"))
        elif category == "NarrowerTerm":
            relationships.append((text, descriptor, "Narrower term"))
        elif category == "RelatedTerm":
            relationships.append((text, descriptor, "Related term"))
        elif category == "SubjectCategory":
            relationships.append((descriptor, text, "Subject category"))
        elif category == "HistoryNote":
            relationships.append((descriptor, text, "History note"))
        else:
            pass


for term1, term2, relationship in relationships:

    if slugify(term1) not in existing_slugs:
        tag = Tag.objects.get_or_create(name=term1,
                creator=User.objects.get(pk=1),
                slug=slugify(term1))
        existing_slugs.append(slugify(term1))

    if slugify(term2) not in existing_slugs:
        tag = Tag.objects.get_or_create(name=term2,
                creator=User.objects.get(pk=1),
                slug=slugify(term2))
        existing_slugs.append(slugify(term2))

    print(term1, term2, relationship)

    tag_relationship = Relationship.objects.get_or_create(
        from_tag=Tag.objects.get(slug=slugify(term1)),
        to_tag=Tag.objects.get(slug=slugify(term2)),
        relationship_type=str(relationship)
        )
