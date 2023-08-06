import time
import utilum
from . import scripts
from . import formatter


def gitConfig(name, email):
    utilum.system.shell(f'git config --global user.name {name}')
    utilum.system.shell(f'git config --global user.email {email}')


def grantPermissionFolder(dbPath):
    pCmd = "chmod 777 -R " + dbPath
    utilum.system.shell(pCmd)


def gitInitOrRegular(username, repoPath, gitPath):

    def wrapperRegular(cmd):
        return f'''su {username} -c "cd {repoPath} && {cmd}"'''

    cmd1 = wrapperRegular(f'''git init --initial-branch=main''')
    cmd2 = wrapperRegular(f'''git remote add origin {gitPath}''')
    cmd3 = wrapperRegular(f'''git add .''')
    cmd4 = wrapperRegular(f'''git commit -m "Regular Update"''')
    cmd5 = wrapperRegular(f'''git push origin main''')

    grantPermissionFolder(repoPath)

    try:
        utilum.system.shell(cmd1)
    except:
        print("")

    try:
        utilum.system.shell(cmd2)
    except:
        print("")

    utilum.system.shell(cmd3)

    utilum.system.shell(cmd4)

    utilum.system.shell(cmd5)

    return None


def grantPermissionFile(dbPath):
    def wrapperAdmin(cmd):
        return f'''sudo {cmd}'''
    pCmd = wrapperAdmin("chmod 777 " + dbPath)
    utilum.system.shell(pCmd)


def manageDatabases(username, repoPath):
    def wrapperAdmin(cmd):
        return f'''{cmd}'''

    cmd1 = wrapperAdmin(scripts.showDatabases())
    out, err = utilum.system.shellRead(cmd1)
    decoded = out.decode('utf-8')
    dbs = decoded.split("\n")
    dbs = dbs[1:-1]
    # print(dbs)

    for database in dbs:
        # print(database)
        dbPath = repoPath + database + '.sql'
        exportCmd = wrapperAdmin(scripts.exportDatabase(database, dbPath))
        # print(exportCmd)
        utilum.system.shell(exportCmd)

        # format sql dump: skipping for now
        # if(database not in ['mysql','sys','information_schema','performance_schema'] or database in ['mysql','sys']):
        # formatter.process(fileReadPath = dbPath, fileWritePath = dbPath)

        # change to 777
        grantPermissionFile(dbPath)


def flow(config):
    # First Function to Init
    if (utilum.file.isPathExist(config.STAGE_STORAGE_PATH) == False):
        utilum.system.shell(f"mkdir {config.STAGE_STORAGE_PATH}")
        utilum.system.shell(f"chmod 777 -R {config.STAGE_STORAGE_PATH}")

    # Mid Function to Transfer DB Files
    manageDatabases(config.USERNAME, config.STAGE_STORAGE_PATH)

    # git config set
    gitConfig(config.GIT_NAME, config.GIT_EMAIL)

    # Last Function to Commit
    gitInitOrRegular(
        config.USERNAME, config.STAGE_STORAGE_PATH, config.GIT_PATH)


def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
