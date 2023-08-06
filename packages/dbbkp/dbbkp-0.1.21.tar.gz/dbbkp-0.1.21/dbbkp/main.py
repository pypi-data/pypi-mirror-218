from .engines import mysqlDefault
from .engines import mysqlDocker
from .engines import mongoDocker
from .engines import fsDefault
from .engines import dsDefault
from .engines import dsDefault2
from .engines import svrDefault
from .engines import vsDefault
# Entry Function


def start(config):
    DB_ENGINE = config.DB_ENGINE
    MsqModule = ''

    if (DB_ENGINE == 'mysql'):
        MsqModule = mysqlDefault
    elif (DB_ENGINE == 'mysqlDocker'):
        MsqModule = mysqlDocker
    elif (DB_ENGINE == 'mongoDocker'):
        MsqModule = mongoDocker
    elif (DB_ENGINE == 'fsDefault'):
        MsqModule = fsDefault
    elif (DB_ENGINE == 'dsDefault'):
        MsqModule = dsDefault
    elif (DB_ENGINE == 'dsDefault2'):
        MsqModule = dsDefault2
    elif (DB_ENGINE == 'svrDefault'):
        MsqModule = svrDefault
    elif (DB_ENGINE == 'vsDefault'):
        MsqModule = vsDefault
    else:
        MsqModule = mysqlDefault

    MsqModule.start(config)


# Example Call Below ***-----------***-----------***-----------***-----------***
class Config:
    DB_ENGINE = 'mysql'
    STAGE_STORAGE_PATH = '/home/un4/Reponere/Drive' + '/mysqlBackup/'
    GIT_PATH = 'GIT_PATH_HERE'
    USERNAME = 'un4'
    GIT_NAME = 'GIT_NAME_HERE'
    GIT_EMAIL = 'GIT_EMAIL_HERE'
    INTERVAL = 60*15  # seconds


# config = Config()
# dbbkp.main.start(config)
# NOTE: Run As/With sudo
