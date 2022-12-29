import os
COVER_FOLDER = 'levels/cover/'
ICON_FOLDER = 'levels/icon/'
DATA_FOLDER = 'levels/data/'
INFO_FOLDER = 'levels/info/'
OWNERS_FOLDER = 'levels/owners/'

def Delete(FOLDER):
    for x in os.listdir(FOLDER): os.remove(os.path.join(FOLDER,x))

Delete(COVER_FOLDER)
Delete(ICON_FOLDER)
Delete(DATA_FOLDER)
Delete(INFO_FOLDER)
Delete(OWNERS_FOLDER)