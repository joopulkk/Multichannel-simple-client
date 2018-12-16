# -*- coding: utf-8 -*-
import requests, os, time, json, pprint

class client():

    def __init__(self):
        self.current_user_name = "Not logged in"
        self.current_user = {}
        self.token = ""
        self.api_address = "http://0.0.0.0:5000"

    def print_message(self,message):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(message))
        print("...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        return

    def do_login(self):
        """Try to login with given credentials"""
        username = ""
        password = ""
        
        while username == "" or password == "":
            username = input("Give username: ")
            password = input("Give password: ")
        
        headers = { 'Content-type': 'application/json'}
        data = {"username": username, "password": password}
        response = requests.post('http://0.0.0.0:5000/login', headers=headers, data=json.dumps(data))

        try:
            self.token = response.json()["access_token"]
        except Exception as e:
            self.print_message("Login failed" + str(response))
            return
        
        self.current_user_name = username
        self.current_user = self.get_user(username)
        self.print_message("Logged in as : "+username)
        return
        
    def do_logout(self):
        """Try to logout return  """
        if self.token == "":
            self.print_message("Not logged in")
            return
        else:
            headers = {'Authorization': 'Bearer '+self.token,}
            response = requests.post('http://0.0.0.0:5000/logout', headers=headers)

            try:
                self.response = response.json()["Message"]
                if response == "Logged out":
                    self.current_user = "Not logged in"
                    self.current_user_id = ""
                    self.token = ""
                    self.print_message("Logged out")
                    return
            except Exception as e:
                self.print_message("Logout failed" + str(response))
                return
        
        self.print_message("Logout failed" + str(response))
        return

    def post_user(self):
        data= {
        "username": "",
        "password": "",
        "preferred_channel": "",
        "email": "",
        "facebook":"",
        "telegram": "",
        "irc": {"username": "", "network": ""},
        "slack": {"username": "","channel": ""}
        }

        for key in data:
            if type(data[key]) == dict:
                for subkey in data[key]:
                    value = input(key+": "+subkey+":")
                    data[key][subkey] = value
            else:
                value = input(key+":")
                data[key] = value
        
        headers = {'Content-Type': 'application/json',}
        response = requests.post('http://0.0.0.0:5000/users', headers=headers, data=json.dumps(data))

        try:
            user_id = response.json()["user_id"]
        except Exception as e:
            self.print_message("User creation failed" + str(response) + str(response.json()) )
            return
        
        self.print_message("User " + data["username"] + " created")
        return
    
    def update_users(self):
        
        headers = {'Authorization': 'Bearer '+self.token,}
        response = requests.get('http://0.0.0.0:5000/users', headers=headers)

        try:
            response = response.json()['Users']
        except Exception as e:
            self.print_message("Getting users failed" + str(response) )
            return

        return response
        
    def list_users(self):

        users = self.update_users()

        try:
            for item in users:
                print("username: "+item['username']+" _id: "+item["_id"]+"\n")
        except Exception as e:
            self.print_message("Getting users failed")
            return

        temp = input("\n Press enter to continue" )
        return

    def print_user(self, user):
        try:
            for item in user:
                if item == "channels":
                    for subitem in user[item]:
                        print(str(subitem)+":")
                        for i in user[item][subitem]:
                            print("    "+str(i)+" : "+user[item][subitem][i])
                else:
                    print(item+": "+str(user[item]))
                
        except Exception as e:
            print("Error printing user data")
            return
        
        temp = input("\n Press enter to continue")
        return
        
    def get_user(self,user):
        try:
            users = self.update_users()
            user_id = None

            for i in users:
                if i['username'] == user:
                    user_id = i['_id']
                    break
                else:
                    pass
        except Exception as e:
            self.print_message("Getting user failed" + str(e) )
            return
            
        if user_id == None:
            self.print_message("No user found")
            return 
        else:
            headers = {'Authorization': 'Bearer '+self.token,}
            try:
                response = requests.get('http://0.0.0.0:5000/users/'+user_id, headers=headers)
                user = response.json()['User']
            except Exception as e:
                self.print_message("Getting user failed" + str(e) )
                return
           
            return user

    def modify_user(self):
        
        if self.current_user == {}:
            self.print_message("Error, not logged in."+str(e))
            return
        
        template= {
        "password": "",
        "preferred_channel": "",
        "email": "",
        "facebook":"",
        "telegram": "",
        "irc": {"username": "", "network": ""},
        "slack": {"username": "","channel": ""}
        }
        data={}
        prompt= input("Give values to update. Otherwise leave empty\nPress enter to continue")
        for key in template:
            if type(template[key]) == dict:
                for subkey in template[key]:
                    value = input(key+": "+subkey+":")
                    if value == "":
                        pass
                    else:
                        data[key][subkey] = value
            else:
                value = input(key+":")
                if value == "":
                    pass
                else:
                    data[key] = value
        
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+self.token,}
        response = requests.patch('http://0.0.0.0:5000/users/'+self.current_user["_id"], headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            self.print_message("Modification failed" + str(response) + str(response.json()) )
            return
        else:
            self.print_message("Modified")
        return

    def delete_user(self):

        prompt = ""
        while prompt not in ["y", "n"]:
            prompt = input("Delete currently logged in user? (y/n):")
        
        if prompt == "n":
            self.print_message("User not deleted")
            return
        else:
            headers = {'Authorization': 'Bearer '+self.token,}
            response = requests.delete('http://0.0.0.0:5000/users/'+self.current_user["_id"], headers=headers,)

            if response.status_code != 200:
                self.print_message("Error deleting user. Code: "+str(response.status_code))
                return
            else:
                self.print_message("Deleted")
                exit(0)
        return

    def print_messages(self, messages):

        try:
            for message in messages:
                print("\n")
                for item in message:
                    if item == "receivers":
                        for subitem in message[item]:
                            print(str(subitem)+" : "+ str(message[item][subitem]))
                    else:
                        print(item+" : "+message[item])
        except Exception as e:
            print("Error while printing message."+ str(e))
            time.sleep(1)
            return
        
        temp = input("\n Press enter to continue")
        return

    def new_message(self):

        while True:
            message = input("Message body: ")
            sent_to = input("Send message to (separate names with space) : ").split(" ")

            if message != "" and sent_to != "":
                break

        data = {'message' : message, 'sent_to' : sent_to }
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+self.token,}
        response = requests.post('http://0.0.0.0:5000/messages', headers=headers, data=json.dumps(data))

        try:
            message_id = response.json()["message_id"]
        except Exception as e:
            self.print_message("Message post failed " + str(response))
            return
        
        self.print_message("Message" + data["message"] + " posted.")
        return

    def get_messages(self):

        headers = {'Authorization': 'Bearer '+self.token}
        response = requests.get('http://0.0.0.0:5000/messages', headers=headers)

        try:
            messages = response.json()["Messages"]
        except Exception as e:
            self.print_message("Couldn't get messages " + str(response) + str(response.json()) )
            return

        return messages

    def get_message(self,message_id):
        
        try:
            messages = self.get_messages()
        except Exception as e:
                self.print_message("Error getting messages")
                return
        temp = ""
        for i in messages:
            if i['_id'] == message_id:
                temp = message_id
                break
            else:
                pass
        if temp == "":
                self.print_message("No message id: "+message_id )
        else:
            headers = {'Authorization': 'Bearer '+self.token}
            response = requests.get('http://0.0.0.0:5000/messages/'+message_id, headers=headers)

        try:
            messages = response.json()["Message"]
        except Exception as e:
            self.print_message("Couldn't get message " + str(response) + str(response.json()) )
            return
        
        return messages
    
    def delete_message(self, message_id):
        prompt = ""
        while prompt not in ["y", "n"]:
            prompt = input("Delete message with given id? (y/n):")
        
        if prompt == "n":
            self.print_message("Message not deleted")
            return
        else:
            headers = {'Authorization': 'Bearer '+self.token,}
            response = requests.delete('http://0.0.0.0:5000/messages/'+message_id["_id"], headers=headers,)

            if response.status_code != 200:
                self.print_message("Error deleting message. Code: "+str(response.status_code))
                return
            else:
                self.print_message("Deleted")
        return

def users_submenu(client):

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print ("***MultiChannelThingyClient***\n\nCurrent user: "+client.current_user_name+"\n1) New user \n2) List users \n3) Wiew Users \n4) Modify user \n5) Delete user \n6) Back\n\n")
            menu_select = "nothing"

            while menu_select not in ["1","2","3","4","5","6"]:
                menu_select = input("Action: ")

            if menu_select == "1":
                client.post_user()
                pass
            elif menu_select =="2":
                client.list_users()
                pass
            elif menu_select =="3":
                temp = client.get_user(input("Give username: "))
                client.print_user(temp)
                pass
            elif menu_select =="4":
                client.modify_user()
                pass
            elif menu_select =="5":
                client.delete_user()
                pass
            elif menu_select =="6":
                return

def messages_submenu(client):

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print ("***MultiChannelThingyClient***\n\nCurrent user: "+client.current_user_name+"\n1) New message \n2) List messages \n3) Wiew message \n4) Delete message \n5) Back\n\n")
            menu_select = "nothing"

            while menu_select not in ["1","2","3","4","5"]:
                menu_select = input("Action: ")

            if menu_select == "1":
                client.new_message()
                pass
            elif menu_select == "2":
                temp = client.get_messages()
                client.print_messages(temp)
                pass
            elif menu_select == "3":
                temp = client.get_message(input("Give message id: "))
                client.print_messages(temp)
                pass
            elif menu_select == "4":
                client.delete_messages(input("Give message id: "))
                pass
            elif menu_select == "5":
                return


def main():

    clnt = client()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("***MultiChannelThingyClient***\n\nCurrent user: "+clnt.current_user_name+"\n1) Login\Logout \n2) Users \n3) Messages \n4) Quit \n\n")
        menu_select = "nothing"

        while menu_select not in ["1","2","3","4"]:
            menu_select = input("Action: ")

        if menu_select == "1":
            if clnt.current_user == {}:
                clnt.do_login()
            else:
                clnt.do_logout()
            pass
        elif menu_select == "2":
            users_submenu(clnt)
            pass
        elif menu_select == "3":
            messages_submenu(clnt)
            pass
        elif menu_select == "4":
            print("Closing MultiChannelThingyClient....")
            exit(0)
        else:
            pass


if __name__ == '__main__':
    main()