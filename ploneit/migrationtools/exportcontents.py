# -*- encoding: utf8 -*-
try:
    import json
except:
    import simplejson as json

from DateTime import DateTime

from OFS.ObjectManager import ObjectManager

from Products.Five import BrowserView
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.utils import getToolByName

from ploneit.migrationtools import config


class ExportContents(BrowserView):
    """Vista che permette di salvare un file in json
    contenente i contenuti del sito con i loro attributi

    see: http://dev.plone.org/collective/browser/collective.blueprint.archetypesource
    """

    def __init__(self, context, request):
        super(ExportContents, self).__init__(context, request)
        self.wftool = getToolByName(context, 'portal_workflow')
        self._root_depth = len(context.getPhysicalPath())

    def __call__(self):
        data = []
        for x in self._getItemsRecursive(self.context):
            for k, v in x.items():
                # converto gli oggetti tipo
                # image e file in semplici url
                # e le date in formato ISO
                if k in config.FILE_FIELDNAMES:
                    x[k] = v.absolute_url()
                if isinstance(v, DateTime):
                    x[k] = v.ISO()
            data.append(x)
        fh = open(config.CONTENTS_FILE,'w')
        json.dump(data, fh, indent = 2)
        fh.close()
        return 'ok'

    def _getItemsRecursive(self, item):
        if IBaseObject.providedBy(item):
            schema = item.Schema()

            # Get the schema data:
            data = dict([(x, item.getField(x).get(item)) \
                                        for x in schema.keys()])

            # Extend the data with portal type and path:
            data['_type'] = item.portal_type
            path = item.getPhysicalPath()[self._root_depth:]
            data['_path'] = '/'.join(path)

            # And also the workflow state, if any:
            transitions = []
            for wf in self.wftool.getWorkflowsFor(item):
                history = self.wftool.getHistoryOf(wf.getId(), item)
                transitions.extend([x['action'] \
                            for x in history if x['action'] is not None])

            data['_transitions'] = transitions
            yield data

        if isinstance(item, ObjectManager):
            for each in item.objectValues():
                for x in self._getItemsRecursive(each):
                    yield x
