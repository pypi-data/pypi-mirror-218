import os
import requests

null = None
true = True
false = False
GITLAB_BASE_URL = 'https://gitlab.com/api/v4'
GROUPS = 101
SUB_GROUPS = 101

def getFileSize(filePath):
    return os.path.getsize(filePath)


def parseJson(jsonString):
    obj = eval(jsonString)
    return obj


def getProject(projectId, token):
    project = requests.get(f'''{GITLAB_BASE_URL}/projects/{str(projectId)}?statistics=true''', headers={"PRIVATE-TOKEN": token})
    projectT = eval(project.text)
    return projectT


def getGroupProjects(groupId, projectSearch, page, pageSize, token):
    projects = requests.get(f'''{GITLAB_BASE_URL}/groups/{str(groupId)}/projects?search={projectSearch}&include_subgroups=true&owned=true&per_page={str(pageSize)}&page={str(page)}''', headers={"PRIVATE-TOKEN": token})
    projects = eval(projects.text)
    return projects


def getGroups(token):
    groups = requests.get(f'''{GITLAB_BASE_URL}/groups/?per_page={str(GROUPS)}&top_level_only=true''', headers={"PRIVATE-TOKEN": token})
    groupsT = eval(groups.text)
    return groupsT

def getGroup(token, search, fullPath):
    groups = requests.get(f'''{GITLAB_BASE_URL}/groups/?per_page={str(GROUPS)}&search={search}''', headers={"PRIVATE-TOKEN": token})
    groupsT = eval(groups.text)
    if(len(groupsT) >= 1 and (type('stream') != type(groupsT))):
        # print("groupsT: ", groupsT) # :debug
        for gr in groupsT:
            # print("gr: ", gr) # :debug
            fp = gr["full_path"].lower()
            # print("fp-l: ", fp) # :debug
            # print("fp-r: ", fullPath.lower()) # :debug
            if(fp == fullPath.lower()):
                return gr
        return {}
    else:
        return {}

def getSubGroups(groupId, token):
    subGroups = requests.get(f'''{GITLAB_BASE_URL}/groups/{str(groupId)}/subgroups?per_page={str(SUB_GROUPS)}''', headers={"PRIVATE-TOKEN": token})
    subGroups = eval(subGroups.text)
    return subGroups


def createGroup(json, token):
    subGroups = requests.post(f'''{GITLAB_BASE_URL}/groups/''', json=json, headers={"PRIVATE-TOKEN": token})
    subGroups = eval(subGroups.text)
    return subGroups
# {'message': 'Failed to save group {:path=>["can contain only letters, digits, \'_\', \'-\' and \'.\'. Cannot start with \'-\' or end in \'.\', \'.git\' or \'.atom\'."]}'}    

def createProject(json, namespace_id, token):
    project = requests.post(f'''{GITLAB_BASE_URL}/projects/?namespace_id={namespace_id}''', json=json, headers={"PRIVATE-TOKEN": token})
    project = eval(project.text)
    return project
