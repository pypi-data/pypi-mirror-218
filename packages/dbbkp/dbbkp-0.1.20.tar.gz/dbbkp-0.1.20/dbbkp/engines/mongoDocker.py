import time
import utilum
from . import scripts


def gitConfig(name, email, repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''
    utilum.system.shell(wrapperRegular(
        f'git config --local user.name "{name}"'))
    utilum.system.shell(wrapperRegular(
        f'git config --local user.email "{email}"'))


def gitInitOrRegular(repoPath, message, branch):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    cmd3 = wrapperRegular(f'''git add .''')
    cmd4 = wrapperRegular(f'''git commit -m "{message}"''')
    cmd5 = wrapperRegular(f'''git push origin {branch}''')

    utilum.system.shell(cmd3)
    utilum.system.shell(cmd4)
    utilum.system.shell(cmd5)

    return None


def manageDatabases(repoPath, containerName):
    cmd1 = scripts.createMongoDbBackup(containerName)
    (out1, err1) = utilum.system.shellRead(cmd1)

    cmd2 = scripts.removeMongoDbBackup(repoPath)
    (out2, err2) = utilum.system.shellRead(cmd2)

    cmd3 = scripts.copyMongoDbBackupFiles(containerName, repoPath)
    (out3, err3) = utilum.system.shellRead(cmd3)

    return


def flow(config):
    # Mid Function to Transfer DB Files
    manageDatabases(config.STAGE_STORAGE_PATH,
                    config.CONTAINER_NAME)

    # git config set
    gitConfig(config.GIT_NAME, config.GIT_EMAIL, config.STAGE_STORAGE_PATH)

    # Last Function to Commit
    gitInitOrRegular(config.STAGE_STORAGE_PATH,
                     config.GIT_MESSAGE, config.GIT_BRANCH)


def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
