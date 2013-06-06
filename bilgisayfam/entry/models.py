from django.db import models

from djorm_pgarray.fields import ArrayField


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
    normalized = models.CharField(max_length=255, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.keyword


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

    example = models.TextField(null=True)
    """
    This is an example sentence.
    """

    entry = models.ForeignKey(Entry)
