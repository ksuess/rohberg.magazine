# -*- coding: utf-8 -*-
# importBernArticles

from datetime import date, datetime
import os
import codecs
import simplejson as json
# from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
import urllib2
from StringIO import StringIO
from plone.namedfile import NamedBlobFile, NamedBlobImage 
from plone.app.textfield.value import RichTextValue

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
    """
    
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
        - BernArticleBlock Anzeige als Portlet unterscheiden
        + Workflow Stati unterscheiden (private, visible, published)
        + BernArticleBlockLink
        + Leadimages
        + nein! Seite in Navigation anzeigen oder nicht (Blöcke nicht)
        - anmeldeformular-mittagstisch
        """
        if item['portal_type'] in ['Folder',]:
            print "*** WARNING: Folder found"
            return
        elif item['portal_type'] in ['BernArticle',]:
            parent.invokeFactory('Folder', id=item['id'], title=item['title'], description=item['description'])
            folder1 = getattr(parent, item['id'], None)
            # print "[el in item['children'] if el['portal_type']!='BernArticle'] ", item['url']
            # print [el['portal_type'] for el in item['children'] if el['portal_type']!='BernArticle']
            if [el['portal_type'] for el in item['children'] if el['portal_type']!='BernArticle']: # Es existieren Blöcke
                # print "Es EXISTIEREN Blöcke für ", item['url']
                folder1.invokeFactory('Folder', id='blocks', title=item['title'], description=item['description'])
                folder2 = getattr(folder1, 'blocks')
                folder2.invokeFactory('Document', id=item['id'], title=item['title'], description=item['description'])
                document = getattr(folder2, item['id'])
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
                # print "Es existieren KEINE Blöcke für ", item['url']
                folder1.invokeFactory('Document', id=item['id'], title=item['title'], description=item['description'])
                document = getattr(folder1, item['id'])
                document.text = RichTextValue(unicode(item['text']), 'text/html', 'text/x-html-safe', 'utf-8')
                folder1.setDefaultPage(item['id'])
                for child in item['children']: # Subarticles
                    createObject(folder1, child)  
            # Bilder anlegen
            for idx,val in enumerate(item['images'].values()):
                # print "url image ", val
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
            if not item['text']: # mehrere Bilder
                pass
                # if item['review_state']=='private':
                #     myid = item['id']+'-images'
                #     parent.invokeFactory('Folder', id=myid, title='Images')
                #     folder = getattr(parent, myid, None)
                # else:
                #     folder = parent
                # for idx,val in enumerate(item['images'].values()):
                #     # print "url image ", val
                #     if val:
                #         response = urllib2.urlopen(val)
                #         data = response.read()
                #         content_type= response.info().getheader('Content-Type')
                #         filename = u"image"+str(idx+1)+"-"+item['id']
                #         image = NamedBlobImage(data, content_type, filename)
                #         folder.invokeFactory("Image", id=filename, title=parent.Title(), image=image)
                #         response.close()
            else:
                # print "Block mit Text ", item['url'], " erstellt in ", parent
                myid = parent.id + "-" + item['id']
                parent.invokeFactory('Document', id=myid, title=item['title'], description=item['description'])
                document = getattr(parent, myid)
                document.text = RichTextValue(unicode(item['text']), 'text/html', 'text/x-html-safe', 'utf-8')
                for idx,val in enumerate(item['images'].values()):
                    # print "url image ", val
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
                
            # print "BernArticleBlock ", item['url']
        elif item['portal_type'] in ['BernArticleBlockFile']:
            response = urllib2.urlopen(item['url']+"/file")
            # print "BernArticleBlockFile ID und URL %s  %s " % (unicode(item['id']),item['url'])
            data = response.read()
            content_type= response.info().getheader('Content-Type')
            filename = "." in item['id'] and unicode(item['id']) or  item['id']+"."+unicode(content_type.split("/")[1])
            file = NamedBlobFile(data, content_type, filename) #, "text/html", u"text.html")
            parent.invokeFactory('File', id=item['id'], title=item['title'], description=item['description'], file=file)
            fl = getattr(parent, item['id'])
            response.close()
        elif item['portal_type'] in ['BernArticleBlockLink']:
            parent.invokeFactory('Link', id=item['id'], title=item['title'], description=item['description'])
            linkobj = getattr(parent, item['id'])
            linkobj.remoteUrl = item['remoteUrl']
        else:
            print "*** WARNING: portal_type not found: ", item['portal_type'], item['url']
            return
        if item['review_state']=='private':
            if "document" in locals():
                wf_tool.doActionFor(document, 'retract')
            else:
                print "no document created for ", str(item)
        
    
    wf_tool = getToolByName(self, 'portal_workflow')
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    print "*** importBernArticles ", now
    print "root ", self
    if not self.portal_type=="Folder":
        return
    rootid = "import-"+now # Es wird ein Folder mit dieser ID erstellt und alles importierte hier erstellt
    # rootid = "import-urdorf"

    url = 'http://127.0.0.1:8080/Plone/moosmatt/exportBernArticles'
    url = 'http://127.0.0.1:8080/Plone/moosmatt/projekte-und-veranstaltungen/archiv-2013-14/exportBernArticles'
    # url = 'http://127.0.0.1:8080/Plone/moosmatt/lernen/exportBernArticles'
    # url = 'http://127.0.0.1:8080/Plone/moosmatt/lernen/lernpartnerschaften/exportBernArticles'
    f = urllib2.urlopen(url)
    exp = f.read()
    # print exp
    result = json.loads(exp)
    f.close()
    # pp.pprint(result)
    
    # Bevor ein neuer Import-Folder erstellt wird, erst den löschen, der die selbe ID hat.
    if hasattr(self, rootid):
        self.manage_delObjects([rootid])
    self.invokeFactory('Folder', id=rootid, title=rootid)
    importfolder = getattr(self, rootid, None)
    
    print "import from ", dict(result)['url']
    createObject(importfolder, result)
    
    msg = u"importBernArticles done for " + url + " at " + datetime.now().strftime("%Y%m%d%H%M%S")
    print msg
    return msg
    

