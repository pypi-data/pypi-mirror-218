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


def manageFs(srcPath, repoPath):
    cmd = scripts.removeFsBackupFiles(repoPath)
    (out, err) = utilum.system.shellRead(cmd)

    cmd2 = scripts.copyFsBackupFiles(srcPath, repoPath)
    (out2, err2) = utilum.system.shellRead(cmd2)

    return


def flow(config):
    # Mid Function to Transfer DB Files
    manageFs(config.SRC_PATH, config.DST_PATH)

    # git config set
    gitConfig(config.GIT_NAME, config.GIT_EMAIL, config.DST_PATH)

    # Last Function to Commit
    gitInitOrRegular(config.DST_PATH,
                     config.GIT_MESSAGE, config.GIT_BRANCH)


def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
