class User:
    def __init__(self,id,secondName,name):
        self.id=id
        self.secondName=secondName
        self.name=name
        self.friendList=[]


    def FullName(self):
        fullName=self.secondName+" "+self.name
        return fullName

    def FillUserList(self,userList):
        for u in userList:
            self.friendList.append(u)

    def ShowUser(self,splitter):
        user =str(self.id)+splitter+ self.secondName + splitter + self.name
        return user
    def ShowUserWithFriendsId(self,splitter,friendsSplitter):
        user = str(self.id) +splitter + self.secondName + splitter + self.name+':'
        idList=[]
        for f in self.friendList:
            id=f.id
            idList.append(id)
        strIdList=""
        for i in range(0,len(idList),1):
            if i==0:
                s=str(idList[i])
                strIdList+=s
            else:
                s = friendsSplitter+str(idList[i])
                strIdList += s
        #user+=str(len(self.friendList))
        user+=strIdList
        return user
    def CreateJson(self):
        dict={}
        id=self.id
        dict['id']=id
        dict['secondName']=self.secondName
        dict['name']=self.name
        idList = []
        for f in self.friendList:
            id = f.id
            idList.append(id)
        dict['friendsIdList']=idList

        return dict