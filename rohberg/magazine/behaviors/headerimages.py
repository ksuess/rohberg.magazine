# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile

from rohberg.magazine import _


class IHeaderImages(model.Schema):
    
    # HeaderImages fieldset

    model.fieldset(
        'headerimages',
        label=_(u"LeadImages"),
        fields=['headerimage1', 'headerimage1_caption','headerimage2', 'headerimage2_caption','headerimage3', 'headerimage3_caption',]
    )

    headerimage1 = namedfile.NamedBlobImage(
        title=_(u"Lead Image"),
        description=u"",
        required=False,
    )

    headerimage1_caption = schema.TextLine(
        title=_(u"Lead Image Caption"),
        description=u"",
        required=False,
    )

    headerimage2 = namedfile.NamedBlobImage(
        title=_(u"Lead Image"),
        description=u"",
        required=False,
    )

    headerimage2_caption = schema.TextLine(
        title=_(u"Lead Image Caption"),
        description=u"",
        required=False,
    )

    headerimage3 = namedfile.NamedBlobImage(
        title=_(u"Lead Image"),
        description=u"",
        required=False,
    )

    headerimage3_caption = schema.TextLine(
        title=_(u"Lead Image Caption"),
        description=u"",
        required=False,
    )

alsoProvides(IHeaderImages, IFormFieldProvider)


class HeaderImages(object):
    implements(IHeaderImages)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context