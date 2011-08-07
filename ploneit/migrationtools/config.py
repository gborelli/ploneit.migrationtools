# -*- encoding: utf8 -*-
import os
try:
    from App.config import getConfiguration
    FILE_PATH = getConfiguration().product_config.get(
                'ploneit_migrationtools')['export_data_directory']
except:
    FILE_PATH = '/tmp'

CONTENTS_FILE = os.path.sep.join((FILE_PATH, "export_contents.json"))
MEMBERS_FILE = os.path.sep.join((FILE_PATH, "export_members.json"))
GROUPS_FILE = os.path.sep.join((FILE_PATH, "export_groups.json"))


FILE_FIELDNAMES = ('image', 'file')

DATE_FIELDS = [('creation_date', 'setCreationDate'),
               ('modification_date', 'setModificationDate'),
               ('effectiveDate', 'setEffectiveDate'),
               ('expirationDate', 'setExpirationDate'),
            ]

HTML_FIELDS = [('text', 'setText'),]
