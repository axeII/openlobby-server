# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthenticated 1'] = {
    'data': {
        'reportDrafts': [
        ]
    }
}

snapshots['test_authenticated 1'] = {
    'data': {
        'reportDrafts': [
            {
                'body': 'Not finished yet.',
                'date': '2018-01-09 00:00:00+00:00',
                'id': 'UmVwb3J0OjQ=',
                'otherParticipants': '',
                'ourParticipants': '',
                'providedBenefit': '',
                'published': '2018-01-11 00:00:00+00:00',
                'receivedBenefit': '',
                'title': 'The Silmarillion'
            }
        ]
    }
}
