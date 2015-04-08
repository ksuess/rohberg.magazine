# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase

from plone.app.contenttypes.interfaces import INewsItem
from rohberg.magazine.behaviors.headerimages import IHeaderImages


class HeaderImagesViewlet(ViewletBase):
    """ A simple viewlet which renders headerimages """

    def update(self):
        self.context = IHeaderImages(self.context)
        self.available = self.context.headerimage1 and True or False
        if INewsItem.providedBy(self.context):
            self.available = False

        scales = self.context.restrictedTraverse('@@images')
        try:
            self.headerimagescale1 = scales.scale('headerimage1', scale='headerimage')
        except Exception, e:
            print str(e)
            self.headerimagescale1 = None
        try:
            self.headerimagescale2 = scales.scale('headerimage2', scale='headerimage')
        except Exception, e:
            print str(e)
            self.headerimagescale2 = None
        try:
            self.headerimagescale3 = scales.scale('headerimage3', scale='headerimage')
        except Exception, e:
            print str(e)
            self.headerimagescale3 = None
        his = [self.headerimagescale1, self.headerimagescale2, self.headerimagescale3]
        his = [hi for hi in his if hi]
        if len(his)==3:
            self.headerimageclass = 'headerImage3'
        elif len(his)==2 :
            self.headerimageclass = 'headerImage2'
        elif len(his)==1:
            self.headerimageclass = 'headerImage1'
        else:
            self.headerimageclass = ''
        
