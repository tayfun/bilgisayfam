from django.db import models

from djorm_pgarray.fields import ArrayField

from qhonuskan_votes.models import (VotesField, ObjectsWithScoresManager,
                                    SortByScoresManager)


class Entry(models.Model):
    tags = ArrayField(dbtype="varchar(255)")
    """
    tags is a list of tag strings related to the word. Ex. "isim".
    """

    extra_info = ArrayField(dbtype="varchar(255)")
    """
    extra_info is a list of strings that contain info that is not
    a tag.
    Ex. "ingilizce typhoon"
    """

    keyword = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dictionary(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField()
    description = models.TextField()


class Meaning(models.Model):
    tags = ArrayField(dbtype="varchar(255)")
    """
    Each meaning also can have different tags associated with it. Such as
    /isim/, /meteoroloji/ etc.
    """
    content = models.TextField()
    """
    This is the content of the meaning.
    """
    entry = models.ForeignKey(Entry)
    dictionary = models.ForeignKey(Dictionary)
    """
    Where did we get this meaning from? TDK? Eksi? etc.
    """

    votes = VotesField()
    """
    Each meaning has associated vote. Vote is just like a favorite addition.
    """
    objects = models.Manager()

    objects_with_scores = ObjectsWithScoresManager()
    sort_by_score = SortByScoresManager()
