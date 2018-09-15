import random
import User
import json
import Config as cnf
def WriteStrListToTxtFile(strList,fileName):
    f = open(fileName, 'w')
    for s in strList:
        f.write("%s\n" % s)

def ReadFromFile(fileName):
    strList=[]
    f=open(fileName,'r')
    line = f.readline()
    strList.append(line)
    while line:
        line = f.readline()
        strList.append(line)
    f.close()
    return strList
def ReadSecondNameList(path):
    secondNameList=[]
    strList= ReadFromFile(path)
    for s in strList:
        if len(s)>1:
            s=s.replace('\n','')
            secondNameList.append(s)
    return secondNameList
def CreateWomanSecondNameList(secondNameList):
   womanSecondNameList=[]
   for s in secondNameList:
       w=s+'a'
       womanSecondNameList.append(w)
   return womanSecondNameList
def CreatePerson(secondNameList,nameList):
    a=random.randint(0, len(secondNameList)-1)
    b=random.randint(0,len(nameList)-1)
    secondName=secondNameList[a]
    name=nameList[b]
    return secondName,name
def FullName(user):
    a=user.secondName
    b=user.name
    fullName=a+b
    return fullName
def CreateUsers(secondNameList,maleNamesList,femaleNamesList,countOfUsers):
    userList=[]
    womanSecondNameList = CreateWomanSecondNameList(secondNameList)
    a=random.randint(0,len(secondNameList))
    b=random.randint(0,2)
    for i in range(0,countOfUsers,1):
        r= random.randint(0, 1)
        if r==0:
            secondName, name=CreatePerson(secondNameList,maleNamesList)
            user=User.User(i,secondName, name)
            userList.append(user)
        if r==1:
            secondName, name = CreatePerson(womanSecondNameList, femaleNamesList)
            user = User.User(i,secondName, name)
            userList.append(user)
    return userList

# каждому пользователю создаем друзей
def CreateFriendsForUser(user,userList,countOfFriends):
    c=random.randint(0,min(countOfFriends,len(userList)-1))
    friendList=[]
    for i in range(0,c+1,1):
        a=random.randint(0,len(userList)-1)
        curFried=userList[a]
        friendList.append(curFried)
    user.FillUserList(friendList)



# создаем список друзей
def CreateFriendsList(userList,countOfFriends):
    for u in userList:
        CreateFriendsForUser(u, userList, countOfFriends)
# записывает список друзей в json
def CreateUsersListJson(userList,jsonPath):
    data={}
    # data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
    #         'a string': 'bla',
    #         'another dict': {'foo': 'bar',
    #                          'key': 'value',
    #                          'the answer': 42}}

    for u in userList:
        strId="'"+str(u.id)+"'"
        curDict=u.CreateJson()
        friendList=[]
        data[u.id]=curDict
    with open(jsonPath, 'w') as outfile:
        json.dump(data, outfile)
    # for u in userList:
    #     dict={}
    #     id=u['id']
    #     dict{}
def CreateUsersWithFriendsJsonFile(secondNamePath,maleNamePath,femaleNamePath,jsonPath,countOfUsers,countOfFriends):
    secondNameList = ReadSecondNameList(secondNamePath)
    maleNamesList = ReadSecondNameList(maleNamePath)
    femaleNamesList = ReadSecondNameList(femaleNamePath)
    userList = CreateUsers(secondNameList, maleNamesList, femaleNamesList, countOfUsers)
    CreateFriendsList(userList, countOfFriends)
    CreateUsersListJson(userList, jsonPath)
def CreateUsersWithFriendsJsonFileByConfig():
    secondNamePath=cnf.secondNamePath
    maleNamePath=cnf.maleNamePath
    femaleNamePath=cnf.femaleNamePath
    jsonPath=cnf.jsonPath
    countOfUsers=cnf.countOfUsers
    countOfFriends=cnf.countOfFriends
    secondNameList = ReadSecondNameList(secondNamePath)
    maleNamesList = ReadSecondNameList(maleNamePath)
    femaleNamesList = ReadSecondNameList(femaleNamePath)
    userList = CreateUsers(secondNameList, maleNamesList, femaleNamesList, countOfUsers)
    CreateFriendsList(userList, countOfFriends)
    CreateUsersListJson(userList, jsonPath)
def TestCreateUsersByConfig():
    CreateUsersWithFriendsJsonFileByConfig()
def TestCreateUsers():
    secondNamePath=r'C:\Users\Billy\PycharmProjects\TestHackZurich2018\Second_Names'
    maleNamePath=r'C:\Users\Billy\PycharmProjects\TestHackZurich2018\MaleNames'
    femaleNamePath=r'C:\Users\Billy\PycharmProjects\TestHackZurich2018\FemaleNames'
    jsonPath=r'C:\Users\Billy\PycharmProjects\TestHackZurich2018\users_json'
    secondNameList=ReadSecondNameList(secondNamePath)
    maleNamesList=ReadSecondNameList(maleNamePath)
    femaleNamesList = ReadSecondNameList(femaleNamePath)
    countOfUsers = 1000
    countOfFriends = 10
    splitter=' '
    friendsSplitter=';'
    userList=CreateUsers(secondNameList, maleNamesList, femaleNamesList, countOfUsers)
    CreateFriendsList(userList, countOfFriends)
    for u in userList:
        print(u.ShowUserWithFriendsId(splitter,friendsSplitter))
    CreateUsersListJson(userList, jsonPath)
if __name__ == '__main__':
    TestCreateUsersByConfig()
    #TestCreateUsers()