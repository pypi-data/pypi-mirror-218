import time
import os
import shutil
import utilum
# from . import scripts
from ..utils import gitlab


# def gitConfig(name, email, repoPath):
#     def wrapperRegular(cmd):
#         return f'''cd {repoPath} && {cmd}'''
#     utilum.system.shell(wrapperRegular(
#         f'git config --local user.name "{name}"'))
#     utilum.system.shell(wrapperRegular(
#         f'git config --local user.email "{email}"'))


def gitInitAndPush(dstToken, repoPath, chunkGroupRepoPath):
    rUrl = f'https://gitlab-ci-token:{dstToken}@gitlab.com/{chunkGroupRepoPath}'
    cmd1 = f'''
    cd '{repoPath}'
    git init --initial-branch=main
    git remote add origin {rUrl}
    
    git lfs install
    git lfs track "*.psd"
    git lfs track "*.mp4"
    git lfs track "*.webm"
    git lfs track "*.mkv"
    git lfs track "*.srt"
    git lfs track "*.chunk"
    git add .gitattributes
    '''
    cmd2 = f'''
    cd '{repoPath}'
    git remote set-url origin {rUrl}
    git config lfs.{rUrl}/info/lfs.locksverify true
    git add .
    git commit -m "Chunk Creation"
    git lfs push origin main
    git lfs push --all
    git push -u origin main
    git push --tags
    '''
    cmd3 = f'''
    cd '{repoPath}'
    git remote set-url origin "https://gitlab.com/{chunkGroupRepoPath}.git"
    '''
    utilum.system.shell(cmd1)
    utilum.system.shell(cmd2)
    utilum.system.shell(cmd3)
    return


def processChunk(config, chunk, uviPath, uniqueVideoIdPath):
    dstChunkFolderPath = os.path.join(uniqueVideoIdPath, chunk)
    dstChunkFilePath = os.path.join(dstChunkFolderPath, chunk) + ".chunk"
    gitChunkFolderPath = os.path.join(dstChunkFolderPath, ".git")
    if (utilum.file.isPathExist(dstChunkFolderPath) == False):
        utilum.file.createFolder(dstChunkFolderPath)

    srcChunkFilePath = os.path.join(uviPath, chunk)
    if (utilum.file.isPathExist(dstChunkFilePath) == False):
        shutil.copy2(srcChunkFilePath, dstChunkFilePath)

    uniqueVideoGroup = config.uniqueVideoGroup
    cp = gitlab.createProject({
        "name": chunk,
        "path": chunk,
        "visibility": 'private',  # !important
        "description": f'Chunk Number: {chunk}',
    }, uniqueVideoGroup["id"], config.GIT_TOKEN)
    # print("cp: ", cp)  # :debug

    chunkGroupRepoPath = config.chunkGroupRepoPath
    if (utilum.file.isPathExist(gitChunkFolderPath)):
        # [1] git repo exist
        # copy the file and push, for accounting the chance of change in chunk
        gitInitAndPush(config.GIT_TOKEN, dstChunkFolderPath,
                       chunkGroupRepoPath)
    else:
        # [2] initialize new git repo
        # init a new git-lfs and push
        gitInitAndPush(config.GIT_TOKEN, dstChunkFolderPath,
                       chunkGroupRepoPath)
    return


def processUniqueVideoId(config, uniqueVideoId, sourceEntityPath, dstEntityPath):
    rootGroup = config.rootGroup
    jsonData = {"name": uniqueVideoId,
                "path": uniqueVideoId,
                "visibility": 'private',  # !important
                "parent_id": rootGroup["id"]}
    uniqueVideoGroupResponse = gitlab.createGroup(jsonData, config.GIT_TOKEN)
    # print("uniqueVideoGroupResponse: ", uniqueVideoGroupResponse)  # :debug

    uniqueVideoRootGroupPath = os.path.join(
        config.rootGroupPath, uniqueVideoId)
    searchPath = os.path.join(config.rootGroup["full_path"], uniqueVideoId)
    uniqueVideoGroup = gitlab.getGroup(
        config.GIT_TOKEN, searchPath, uniqueVideoRootGroupPath)
    # print("uniqueVideoGroup: ", uniqueVideoGroup)  # :debug
    config.uniqueVideoGroup = uniqueVideoGroup

    uniqueVideoIdPath = os.path.join(dstEntityPath, uniqueVideoId)
    if (utilum.file.isPathExist(uniqueVideoIdPath) == False):
        utilum.file.createFolder(uniqueVideoIdPath)

    uviPath = os.path.join(sourceEntityPath, uniqueVideoId)
    chunks = os.listdir(uviPath)
    for chunk in chunks:
        chunkGroupRepoPath = os.path.join(config.uniqueVideoGroupPath, chunk)
        config.chunkGroupRepoPath = chunkGroupRepoPath
        processChunk(config, chunk, uviPath, uniqueVideoIdPath)
    # print("chunks: ", chunks)  # :debug
    return


def processRoot(config, path):
    allowedPaths = ['all', 'api', 'ui']
    if (path not in allowedPaths):
        return
    jsonData = {"name": path,
                "path": path,
                "visibility": 'private',  # !important
                "parent_id": config.GIT_GROUP_ID}
    rootGroupResponse = gitlab.createGroup(jsonData, config.GIT_TOKEN)
    # print("rootGroupResponse: ", rootGroupResponse)  # :debug
    rootGroupPath = os.path.join(config.GIT_GROUP_PATH, path)
    config.rootGroupPath = rootGroupPath

    searchPath = os.path.join(config.GIT_GROUP_PATH.split("/")[-1], path)
    rootGroup = gitlab.getGroup(config.GIT_TOKEN, searchPath, rootGroupPath)
    # print("rootGroup: ", searchPath, rootGroup)  # :debug
    config.rootGroup = rootGroup

    dstEntityPath = os.path.join(config.DST_PATH, path)
    if (utilum.file.isPathExist(dstEntityPath) == False):
        utilum.file.createFolder(dstEntityPath)

    sourceEntityPath = os.path.join(config.SRC_PATH, path)
    uniqueVideoIds = os.listdir(sourceEntityPath)
    # print("uniqueVideoIds: ", uniqueVideoIds)  # :debug
    for uniqueVideoId in uniqueVideoIds:
        uniqueVideoGroupPath = os.path.join(rootGroupPath, uniqueVideoId)
        config.uniqueVideoGroupPath = uniqueVideoGroupPath
        processUniqueVideoId(config, uniqueVideoId,
                             sourceEntityPath, dstEntityPath)


def flow(config):
    # [1] all, process root
    processRoot(config, 'all')
    
    # [2] ui, process root
    processRoot(config, 'ui')
    
    # [3] api, process root
    processRoot(config, 'api')


def start(config):
    count = 0.001

    if (utilum.file.isPathExist(config.DST_PATH) == False):
        utilum.file.createFolder(config.DST_PATH)

    GIT_TOKEN = utilum.file.readFile(config.GIT_TOKEN_PATH).replace("\n", "")
    config.GIT_TOKEN = GIT_TOKEN

    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
