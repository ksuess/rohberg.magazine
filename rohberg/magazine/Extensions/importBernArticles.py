# -*- coding: utf-8 -*-
# importBernArticles

import random
from datetime import date, datetime
import os
import codecs
from zExceptions import BadRequest
import html2text
import simplejson as json
# from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
import urllib2
from StringIO import StringIO
from plone.namedfile import NamedBlobFile, NamedBlobImage 
from plone.app.textfield.value import RichTextValue
from logging import getLogger


logger = getLogger('importBernArticles')

import pprint
pp = pprint.PrettyPrinter(indent=3)

def testimport(self):
    catalog = self.portal_catalog
    results = catalog.searchResults({'portal_type': 'File'})
    for item in results:
        print item.getObject().file.filename
    return "testimport done."

def importBernArticles(self):
    """ Import
    
    BernArticle: Seite
    
    aufrufen mit  http://127.0.0.1:10380/schuleurdorf/importBernArticles
    """
    
    def invokeFactoryFunction(obj, ptype, id, title, description=""):
        try:
            obj.invokeFactory(ptype, id=id, title=title, description=description)
        except BadRequest, e:
            logger.error(str(e))
            obj.invokeFactory(ptype, id=id+str(random.randint(1000000, 9999999)), title=title, description=description)
    
    def createObject(parent, item):
        """ legt Dexterity-Objekte an
        
        parent ist Folder 
        item ist Dictionary mit id, title, ...
        
        Wenn BernArticle;
        Erzeuge Folder 1 (mit SubArticles (Documents)) und
        wenn Children Blöcke enthalten: 
            erzeuge Folder 2 darin,
            erzeuge darin Document mit Attributen des BernArticles
            erzeuge darin Blöcke (Documents), 
            setze Ansicht von Folder 2 auf folder_full_view,
            mache Folder 2 zur Default-Page von Folder1
        wenn nicht:
            erzeuge Document mit Attributen des BernArticles, 
            mache Document zur Default-Page
        
        TODO
        + BernArticleBlock Anzeige als Portlet unterscheiden
        + Workflow Stati unterscheiden (private, visible, published)
        + BernArticleBlockLink
        + Leadimages
        + nein! Seite in Navigation anzeigen oder nicht (Blöcke nicht)
        + anmeldeformular-mittagstisch
        + BernArticleBlockTeaser
        - BernArticleBlockEvent, BernArticleBlockNews
        - ATFolder
        """
        # nicht migrieren:
        if item['id'] in ['archiv-nicht-migrieren', ]:
            return
        # if not item['portal_type'][:4] == 'Bern':
        #     print "*** WARNING: no BernArticle, no Folder"
        #     return
        elif item['portal_type'] in ['BernArticle', 'Folder']:
            invokeFactoryFunction(parent, 'Folder', id=item['id'], title=item['title'], description=item['description'])
            folder1 = getattr(parent, item['id'], None)
            # print "[el in item['children'] if el['portal_type']!='BernArticle'] ", item['url']
            # print [el['portal_type'] for el in item['children'] if el['portal_type']!='BernArticle']
            if [el['portal_type'] for el in item['children'] if el['portal_type'][:16]=='BernArticleBlock']: # Es existieren Blöcke
                print "Es EXISTIEREN Blöcke für ", item['url']
                invokeFactoryFunction(folder1, 'Folder', id='blocks', title=item['title'], description=item['description'])
                folder2 = getattr(folder1, 'blocks')
                invokeFactoryFunction(folder2, 'Document', id=item['id'], title=item['title'], description=item['description'])
                document = getattr(folder2, item['id'])
                # TODO: safe html, keine inline Bilder!
                document.text = RichTextValue(unicode(item['text']), 'text/html', 'text/x-html-safe', 'utf-8')
                for child in item['children']:
                    # print "child: ", child['url'], " ", child['portal_type']
                    if child['portal_type']=='BernArticle': # BernArticle
                        createObject(folder1, child)
                    else: # Block
                        createObject(folder2, child)
                folder2.setLayout("folder_full_view")
                folder1.setDefaultPage('blocks')
            else: # Es existieren keine Blöcke
                print "Es existieren KEINE Blöcke für ", item['url']
                invokeFactoryFunction(folder1, 'Document', id=item['id'], title=item['title'], description=item['description'])
                document = getattr(folder1, item['id'])
                document.text = RichTextValue(unicode(item['text']), 'text/html', 'text/x-html-safe', 'utf-8')
                folder1.setDefaultPage(item['id'])
                for child in item['children']: # Subarticles
                    createObject(folder1, child)  
            # Bilder anlegen
            for idx,val in enumerate(item['images'].values()):
                if val:
                    response = urllib2.urlopen(val)
                    data = response.read()
                    content_type= response.info().getheader('Content-Type')
                    filename = u"image"+str(idx+1)+"-"+item['id']
                    image = NamedBlobImage(data, content_type, filename)
                    if idx == 0:
                        document.headerimage1 = image
                    elif idx == 1:
                        document.headerimage2 = image
                    else:
                        document.headerimage3 = image
                    response.close()             
            if item['review_state']=='private':
                wf_tool.doActionFor(folder1, 'retract')
        elif item['portal_type'] in ['BernArticleBlock']:
            if False: #not item['text']: # mehrere Bilder
                pass
            else:
                myid = item['id'] # parent.id + "-" + item['id']
                invokeFactoryFunction(parent, 'Document', id=myid, title=item['title'], description=item['description'])
                document = getattr(parent, myid)
                document.text = RichTextValue(unicode(item['text']), 'text/html', 'text/x-html-safe', 'utf-8')
                for idx,val in enumerate(item['images'].values()):
                    if val:
                        response = urllib2.urlopen(val)
                        data = response.read()
                        content_type= response.info().getheader('Content-Type')
                        filename = u"image"+str(idx+1)+"-"+item['id']
                        image = NamedBlobImage(data, content_type, filename)
                        if idx == 0:
                            document.headerimage1 = image
                        elif idx == 1:
                            document.headerimage2 = image
                        else:
                            document.headerimage3 = image
                        response.close()
        elif item['portal_type'] in ['BernArticleBlockFile']:
            response = urllib2.urlopen(item['url']+"/file")
            data = response.read()
            content_type= response.info().getheader('Content-Type')
            filename = "." in item['id'] and unicode(item['id']) or  item['id']+"."+unicode(content_type.split("/")[1])
            file = NamedBlobFile(data, content_type, filename) #, "text/html", u"text.html")
            txt = html2text.html2text(item['text']).strip()
            # logger.info("html2text.html2text(item['text']) " + txt)
            description = item['description'].strip()
            description = description + ((description and txt) and " - " or "") + txt
            invokeFactoryFunction(parent, 'File', id=item['id'], title=item['title'], description=description)
            fileobj = parent[item['id']]
            fileobj.file=file
            response.close()
        elif item['portal_type'] in ['BernArticleBlockLink']:
            invokeFactoryFunction(parent, 'Link', id=item['id'], title=item['title'], description=item['description'])
            linkobj = getattr(parent, item['id'])
            linkobj.remoteUrl = item['remoteUrl']
                
        else:
            print "*** WARNING: portal_type not found: ", item['portal_type'], item['url']
            return
        if item['review_state']=='private':
            if "document" in locals():
                wf_tool.doActionFor(document, 'retract')
        
    
    wf_tool = getToolByName(self, 'portal_workflow')
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    print "*** importBernArticles ", now
    print "root ", self
    if not (self.portal_type=="Folder" or self.portal_type=="Plone Site"):
        return "Please switch to folder."
    rootid = "import-"+now # Es wird ein Folder mit dieser ID erstellt und alles importierte hier erstellt
    # rootid = "import-urdorf"
    # Bevor ein neuer Import-Folder erstellt wird, erst den löschen, der die selbe ID hat.
    if hasattr(self, rootid):
        self.manage_delObjects([rootid])
    self.invokeFactory('Folder', id=rootid, title=rootid)
    importfolder = getattr(self, rootid, None)
    
    navitems = ['home','behoerde','allgemein','schulen','bahnhofstrasse','embri','feld','copy_of_zentrum','moosmatt',
'weihermatt',
'zentrum',
'kindergarten',
'mittagstisch',
'kooperationsschule',
'intern',
'forum',
'diskussionen',
'pendent',
'links']
    # Debug
    navitems = ['zentrum', ]
    navitems = ['bahnhofstrasse/berichte-aus-dem-schulhaus-bahnhofstrasse/archiv-bahnhofsstrasse', 'moosmatt/archiv-moosmatt']
    for navitem in navitems:
        url = 'http://127.0.0.1:8080/Plone/%s/exportBernArticles' % navitem
        print "url ", url
        f = urllib2.urlopen(url)
        exp = f.read()
        # print exp
        result = json.loads(exp)
        f.close()
        # pp.pprint(result)
            
        print "import from ", dict(result)['url']
        createObject(importfolder, result)
    
        msg = u"importBernArticles done for " + url + " at " + datetime.now().strftime("%Y%m%d%H%M%S")
        print msg

    msg = u"***importBernArticles done for " + str(navitems) + " at " + datetime.now().strftime("%Y%m%d%H%M%S")
    print msg
    print
    return msg
    

