# -*- encoding: utf8 -*-
FILE_PATH = '/Users/giorgio/sviluppo/ploneit/data/'

CONTENTS_FILE = FILE_PATH + "export_contents.json"
MEMBERS_FILE = FILE_PATH + "export_members.json"
GROUPS_FILE = FILE_PATH + "export_groups.json"


FILE_FIELDNAMES = ('image', 'file')

DATE_FIELDS = [('creation_date', 'setCreationDate'),
               ('modification_date', 'setModificationDate'),
               ('effectiveDate', 'setEffectiveDate'),
               ('expirationDate', 'setExpirationDate'),
            ]

HTML_FIELDS = [('text', 'setText'),]
