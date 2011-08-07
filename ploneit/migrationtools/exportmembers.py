# -*- encoding: utf8 -*-
try:
    import json
except:
    import simplejson as json

from DateTime import DateTime

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PlonePAS.tools.groupdata import GroupDataTool
from ploneit.migrationtools import config


class ExportMembers(BrowserView):
    """see:
       http://blog.kagesenshi.org/2008/05/exporting-plone30-memberdata-and.html
    """

    def __call__(self):
        item = {}
        memberdata_tool = getToolByName(self.context, 'portal_memberdata')

        properties = ['username', '_password'] + memberdata_tool.propertyIds()
        membership=getToolByName(self.context, 'portal_membership')
        passwdlist=self.context.acl_users.source_users._user_passwords

        # see http://github.com/garbas/collective.blueprint.usersandgroups/
        def item_key(key):
            return '_user_%s' % key

        users = []
        for memberId in membership.listMemberIds():
            item = {}
            member = membership.getMemberById(memberId)
            for property in properties:
                if property == 'username':
                    item[item_key('username')] = memberId
                elif property == '_password':
                    item[item_key('_password')] = passwdlist[memberId]
                else:
                    value = member.getProperty(property)
                    if isinstance(value, DateTime):
                        value = str(value).split('.')[0]
                    item[item_key(property)] = value
            #setting global roles
            item['roles'] = member.getRoles()
            #setting groups
            item['groups'] = member.getGroups()
            users.append(item)

        fh = open(config.MEMBERS_FILE,'w')
        json.dump(users, fh, indent = 2)
        fh.close()
        return 'ok'


class ExportGroups(BrowserView):
    """see:
       http://blog.kagesenshi.org/2008/05/exporting-plone30-memberdata-and.html
    """

    def __call__(self):
        pg = getToolByName(self.context, 'portal_groups')
        data = []
        for group in pg.listGroups():
            # questo gruppo lo salto in quanto fastidioso
            if group.id == 'AuthenticatedUsers':
                continue

            tmp_item = group.__dict__
            tmp_item.update(group.getProperties())
    
            # see http://github.com/garbas/collective.blueprint.usersandgroups/
            def item_key(key):
                return '_group_%s' % key

            item = {}
            for k, v in tmp_item.items():
                if isinstance(v, GroupDataTool):
                    continue
                item[item_key(k)] = v
            del(tmp_item)
    
            #setting roles
            item['_group_roles'] = group.getRoles()

            data.append(item)

        fh = open(config.GROUPS_FILE,'w')
        json.dump(data, fh, indent = 2)
        fh.close()
        return 'ok'
