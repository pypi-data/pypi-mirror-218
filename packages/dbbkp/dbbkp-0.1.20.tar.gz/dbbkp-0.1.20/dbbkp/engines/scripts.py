import os

################################################ -------------------------------################################################
# [1/4] MySQL


def showDatabases():
    return '''sudo mysql -u root -e 'show databases';'''


def exportDatabase(dbName, dbPath):
    return f'''sudo mysqldump -u root {dbName} > '{dbPath}' --skip-dump-date --extended-insert=FALSE;'''
    # return f'''sudo mysqldump -u root {dbName} > '{dbPath}' --skip-dump-date --extended-insert | sed 's/),(/),\n(/g' > '{dbPath}' ;'''


def showDatabasesDocker(containerName, passwordFilePath):
    return f'''
    PASSWORD_PATH='{passwordFilePath}'
    PASSWORD=`cat $PASSWORD_PATH`
    docker exec {containerName} mysql -u root --password=$PASSWORD -e "SHOW DATABASES";
    '''


def exportDatabaseDocker(containerName, passwordFilePath, databaseName, outputPath):
    return f'''
    PASSWORD_PATH='{passwordFilePath}'
    PASSWORD=`cat $PASSWORD_PATH`
    docker exec {containerName} /usr/bin/mysqldump -u root --password=$PASSWORD {databaseName} > {outputPath} --skip-dump-date --extended-insert=FALSE;
    '''


################################################ -------------------------------################################################
# [2/4] MongoDb

def createMongoDbBackup(containerName):
    return f'''
    docker exec {containerName} sh -c 'mongodump -o /backup'
    '''


def removeMongoDbBackup(repoPath):
    return f'''
    rm -rf {os.path.join(repoPath, 'dump')}
    '''


def copyMongoDbBackupFiles(containerName, repoPath):
    return f'''
    docker cp {containerName}:/backup/ {os.path.join(repoPath, 'dump')}
    '''


################################################ -------------------------------################################################
# [3/4] Fs

def removeFsBackupFiles(repoPath):
    return f'''
    rm -rf {os.path.join(repoPath, 'dump')}
    '''


def copyFsBackupFiles(srcPath, repoPath):
    return f'''
    cp -r {srcPath} {os.path.join(repoPath, 'dump')}
    '''

################################################ -------------------------------################################################
# [4/4] DS

def removeDsBackupFiles(repoPath):
    return f'''
    rm -rf {os.path.join(repoPath, 'dump')}
    '''


def copyDsBackupFiles(srcPath, repoPath):
    return f'''
    cp -r {srcPath} {os.path.join(repoPath, 'dump')}
    '''
