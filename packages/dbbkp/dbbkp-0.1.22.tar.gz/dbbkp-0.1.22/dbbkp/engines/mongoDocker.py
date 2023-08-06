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


def gitInitOrRegular(repoPath, message, branch, groupRepoPath, tokenFilePath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    # 1/6
    cmd1 = wrapperRegular(f'''git init --initial-branch=main''')
    utilum.system.shell(cmd1)

    # 2/6
    dstToken = utilum.file.readFile(tokenFilePath).replace("\n", "")
    rUrl = f'https://gitlab-ci-token:{dstToken}@gitlab.com/{groupRepoPath}.git'
    cmd2 = wrapperRegular(f'''git remote set-url origin {rUrl}''')
    utilum.system.shell(cmd2)

    cmd3 = wrapperRegular(f'''git add .''')
    cmd4 = wrapperRegular(f'''git commit -m "{message}"''')
    cmd5 = wrapperRegular(f'''git push origin {branch}''')

    utilum.system.shell(cmd3)
    utilum.system.shell(cmd4)
    utilum.system.shell(cmd5)

    # 6/6
    rUrlClean = f'https://gitlab.com/{groupRepoPath}.git'
    cmd6 = wrapperRegular(f'''git remote set-url origin {rUrlClean}''')
    utilum.system.shell(cmd6)

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
                     config.GIT_MESSAGE, config.GIT_BRANCH, config.GROUP_REPO_PATH, config.TOKEN_FILE_PATH)


def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
