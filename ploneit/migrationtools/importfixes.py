# -*- encoding: utf8 -*-
try:
    import json
except:
    import simplejson as json

from DateTime import DateTime

from Products.Five import BrowserView
from ploneit.migrationtools import config


class ImportFixies(BrowserView):
    """Vista che permette alcuni fix sull'importazione dei contenuti
    """

    def __call__(self):

        fh = open(config.CONTENTS_FILE, 'r')

        data = json.loads(fh.read())
        for el in data:
            try:
                obj = self.context.restrictedTraverse(str(el['_path']))
            except:
                continue

            for df in config.DATE_FIELDS:
                if el.get(df[0]):
                    getattr(obj, df[1])(DateTime(el[df[0]]))
            for hf in config.HTML_FIELDS:
                if el.get(hf[0]):
                    getattr(obj, hf[1])(el.get(hf[0]), mimetype = 'text/html')

            # see: http://blog.isotoma.com/2011/02/setting-the-modification-date-of-an-archetype-object-in-plone
            od = obj.__dict__
            od['notifyModified'] = lambda *args: None  
            obj.reindexObject()  
            del od['notifyModified']

        return 'ok'
