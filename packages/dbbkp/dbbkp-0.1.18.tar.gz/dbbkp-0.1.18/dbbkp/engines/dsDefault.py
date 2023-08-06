import time
import os
import utilum
from . import scripts


def gitConfig(name, email, repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''
    utilum.system.shell(wrapperRegular(
        f'git config --local user.name "{name}"'))
    utilum.system.shell(wrapperRegular(
        f'git config --local user.email "{email}"'))


def gitAdd(filePath, repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    cmd3 = wrapperRegular(f'''git add "{filePath}"''')
    utilum.system.shell(cmd3)


def gitCommit(repoPath, message, branch):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    cmd4 = wrapperRegular(f'''git commit -m "{message}"''')
    cmd5 = wrapperRegular(f'''git push origin {branch}''')

    utilum.system.shell(cmd4)
    utilum.system.shell(cmd5)

    return None


MB = 1000*1000

def manageDs(config, srcPath, repoPath, MAX_SIZE):
    cmd = scripts.removeDsBackupFiles(repoPath)
    (out, err) = utilum.system.shellRead(cmd)

    cmd2 = scripts.copyDsBackupFiles(srcPath, repoPath)
    (out2, err2) = utilum.system.shellRead(cmd2)

    commitPath = os.path.join(repoPath, 'dump')

    gBatches = []
    tBatches = []
    batches = []
    batchSize = 0
    for file in utilum.file.folderTraversal(commitPath):
        size = utilum.file.getSize(file)/(MB)
        
        if((batchSize + size) > MAX_SIZE):
            gBatches.append([batchSize, batches])
            batchSize = size
            batches = [file]
        else:
            batchSize += size
            batches.append(file)

        tBatches = [batchSize, batches]
        
    gBatches.append(tBatches)
    for igb, gb in enumerate(gBatches):
        for dFile in gb[1]:
            gitAdd(dFile, repoPath)
        gitCommit(repoPath, config.GIT_MESSAGE, config.GIT_BRANCH)
        print("*********************------------------------------------------------------*********************")
        print("[Batch/Total][Size]: ", f"[{igb+1}/{len(gBatches)}][{gb[0]}]")
        print("*********************------------------------------------------------------*********************")

    return


def flow(config):
    # Mid Function to Transfer DB Files
    manageDs(config, config.SRC_PATH, config.DST_PATH, config.GIT_MAX_PUSH_SIZE)

    # git config set
    gitConfig(config.GIT_NAME, config.GIT_EMAIL, config.DST_PATH)



def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
