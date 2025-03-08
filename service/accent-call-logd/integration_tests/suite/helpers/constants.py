# Copyright 2023 Accent Communications

import datetime

EXPORT_SERVICE_ID = 'export-service-id'
EXPORT_SERVICE_KEY = 'export-service-key'

UNKNOWN_UUID = '00000000-0000-4000-8000-000000000000'
NON_USER_TOKEN = 'non-user-token'

ACCENT_UUID = '613747fd-f7e7-4329-b115-3869e44a05d2'

SERVICE_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee1'

MASTER_TENANT = '4eb57648-b914-446b-a69f-58643ae08dd4'
MASTER_USER_UUID = '5b6e5030-0f23-499a-8030-4a390392aad2'
MASTER_TOKEN = 'cfe6dd71-5d0e-41c8-9178-0ce6578b5a71'

USERS_TENANT = 'f0fe8e3a-2d7a-4dd7-8e93-8229d51cfe04'
USER_1_UUID = 'b17d9f99-fcc7-4257-8e89-3d0e36e0b48d'
USER_1_TOKEN = '756b980b-1cab-4048-933e-f3564ac1f5fc'
USER_2_UUID = 'f79fd307-467c-4851-b614-e65bc8d922fc'
USER_2_TOKEN = 'df8b0b7e-2621-4244-87f8-e85d27fe3955'
USER_3_UUID = '2ab10cc9-3c80-4781-b050-8481fcfc2b31'

OTHER_TENANT = '0a5afd22-6325-49b1-8e35-b04618e78b58'
OTHER_USER_UUID = '35faa8d3-3d89-4a72-b897-0706125c7a35'
OTHER_USER_TOKEN = '2c369402-fa85-4ea5-84ed-933cbd1002f0'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'  # 2019-02-05 21:09:48
NOW = datetime.datetime.now()
MINUTES = datetime.timedelta(minutes=1)
SECONDS = datetime.timedelta(seconds=1)

ALICE = {
    'exten': '101',
    'context': 'internal',
    'id': 'ce19b2c3-17a6-4f62-a48b-c663aaa8d62c',
    'line_id': '11',
    'name': 'Alice',
}
BOB = {
    'exten': '102',
    'context': 'internal',
    'id': 'e25c7096-312d-4d9e-93b0-b8d7fc6b9477',
    'line_id': '22',
    'name': 'Bob',
}
CHARLES = {
    'exten': '103',
    'context': 'internal',
    'id': 'a0124923-2b2d-42c6-8637-f7e308ee6008',
    'line_id': '33',
    'name': 'Charles',
}
