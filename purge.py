import os
from threading import local


class delete(local):

    local.COVER_FOLDER = 'levels/cover/'
    local.ICON_FOLDER = 'levels/icon/'
    local.DATA_FOLDER = 'levels/data/'
    local.INFO_FOLDER = 'levels/info/'
    local.USERS_FOLDER = 'levels/users'
    local.OWNERS_FOLDER = 'levels/owners'
    local.OWNS_FOLDER = 'levels/owns'

    def Delete(FOLDER):
        for x in os.listdir(FOLDER):
            os.remove(os.path.join(FOLDER, x))

    def DeleteLevels():
        local.Delete(local.COVER_FOLDER)
        local.Delete(local.ICON_FOLDER)
        local.Delete(local.DATA_FOLDER)
        local.Delete(local.INFO_FOLDER)
        local.Delete(local.OWNERS_FOLDER)

    def DeleteUsers():
        local.Delete(local.USERS_FOLDER)
        local.Delete(local.OWNS_FOLDER)
        local.Delete(local.OWNERS_FOLDER)
