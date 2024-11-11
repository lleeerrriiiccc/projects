import json

def list(file, index='all'):
    if index == 'all':
        with open(file, 'r') as f:
            data = json.load(f)
            return data
    else:
        with open(file, 'r') as f:
            data = json.load(f)
            return data[index]
        
def write(file, data):
    obj = list(file)
    obj.append(data)
    with open(file, 'w') as f:        
        json.dump(obj, f,indent=1, separators=(',',': '))
        

def permits(file):
    obj = list(file)
    rols = {}
    for i in obj:
        admin = str(i['is_admin'])
        user = str(i['user'])
        rols[user]=admin
        print(rols) 
def search(file, key, value):
    obj = list(file)
    for i in obj:
        if i[key] == value:
            return i

def check_exist(file, key, value):    
    obj = list(file)
    for i in obj:
        if i[key] == value:
            return True
                
def delete(file, key, value):
    obj = list(file)
    for i in obj:
        if i[key] == value:
            obj.remove(i)
            with open(file, 'w') as f:
                json.dump(obj, f)

def update(file, key, value, new_data):
    obj = list(file)
    for i in obj:
        if i[key] == value:
            i[key] = new_data
            with open(file, 'w') as f:
                json.dump(obj, f)
        
            
def logged(file, datafile, activuser):
    obj = list(datafile)
    for i in obj:
        if i["user"] == activuser:
            id = i["id"]
            nowdata = list(file, 0)
            nid = nowdata["id"]
            update(file, "id", nid, id)
            return 
def whoisloged():
    obj = list("login/other/data/logeduser.json", 0)
    rn = obj["id"]    
    userdata = search("data/data.json", "id", rn)
    name = userdata["user"]
    str(name)
    print(name)
    return name
def textupdate(id, data):
    id(text=data)
    return id
def loginfun(user, password):

    if check_exist("login/other/data/data.json", "user", user) and check_exist("login/other/data/data.json", "password", password) == True:        
        
        logeduser = user
        print(logged("login/other/data/logeduser.json", "login/other/data/data.json", logeduser))
        return True
        
    else:
        return False
def isadmin(id):
    obj = search("login/other/data/data.json", "id", id)
    
    if obj["is_admin"] == "true":
        return True
    else:
        return False
def createuser(name, password, admin):
    obj = list("other/data/data.json")
    id = len(obj)+1
    new_user = {"id":str(id), "user":name, "password":password, "is_admin":admin}
    write("other/data/data.json", new_user)
    return
