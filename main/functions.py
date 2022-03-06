from config import insta, USERNAME, PASSWORD, ADMIN_ID, bot, INITIAL_LIST, INITIAL_SUBS  # , client
import time
import json
import telegram
from .insta_login import client_session_enabled

client = client_session_enabled()


class Action(object):
    def __init__(self, username, url):
        self.user = username
        self.insta_id = ''
        self.url = url
        self.media_id = ''
        self.likes = 0  # Marking the posts the user has liked
        self.comments = 0  # Marking the posts the user has commented on

    def get_user_id(self):
        "Returns The user's Instagram ID"

        data = client.username_info(self.user)
        self.insta_id = data['user']['pk']

    def get_media_id(self):
        "Returns The Target Media ID"
        code = self.url.strip("/").split("/")[-1]

        # ## Check user feed for post relating to this code
        # data = client.user_feed(self.insta_id).get('items')

        # results = [post['id'] for post in data if post['code'] == code]
        # output = results[0] if len(results) != 0 else None

        # self.media_id = output.split("_")[0] if output is not None else None
        # return self.media_id

        ##################################################
        try:
            data = insta.get_medias_by_code(code)

        except:
            # authentication supported
            time.sleep(3)
            insta.with_credentials(USERNAME, PASSWORD)

            insta.login()
            data = insta.get_medias_by_code(code)

        self.media_id = data.identifier if data is not None else None
        return self.media_id

    def get_list(self):
        "Gets the curent list for checking"
        try:
            with open("main/list.json", 'r') as f:
                try:
                    read = f.read()
                    data = json.loads(read)
                except EOFError as e:
                    data = []
        except:
            data = INITIAL_LIST
            with open("main/list.json", 'w+') as fe:
                json.dump(data, fe)
        return data

    def check_likes(self):
        "Check the list if the user has liked them"
        data = self.get_list()
        for link in data:
            query_set = client.media_likers(
                media_id=link['media_id']).get("users")

            likers = [i['pk'] for i in query_set]
            for user in likers:
                if self.insta_id == user:
                    self.likes += 1
                else:
                    pass

    def check_comments(self):
        "Checks the list if the user has commented on them"
        data = self.get_list()
        for link in data:
            query_set = client.media_comments(
                media_id=link['media_id']).get("comments")
            comments = [i['user_id'] for i in query_set]
            for user in comments:
                if self.insta_id == user:
                    self.comments += 1
                else:
                    pass

    def remove_user(self):
        try:
            with open("main/subscribers.json", 'r') as f:
                try:
                    read = f.read()
                    subscribers = json.loads(read)
                except EOFError as e:
                    True
        except:
            subscribers = INITIAL_SUBS
        user = self.user
        users = subscribers

        try:
            with open("main/subscribers.json", "w") as f:
                users.remove(user)
                json.dump(users, f)
                f.close()
        except:
            return

    def get_status(self):
        "Returns the user status of number of likes"

        # Get the susbcribers

        try:
            with open("main/subscribers.json", 'r') as f:
                try:
                    read = f.read()
                    subscribers = json.loads(read)
                except EOFError as e:
                    True
        except:
            subscribers = INITIAL_SUBS
            with open("main/subscribers.json", 'w+') as fe:
                json.dump(subscribers, fe)
        try:
            with open("main/premium_subscribers.json", 'r') as f:
                try:
                    read = f.read()
                    premium_subscribers = json.loads(read)
                except EOFError as e:
                    True
        except:
            premium_subscribers = INITIAL_SUBS
            with open("main/premium_subscribers.json", 'w+') as fe:
                json.dump(premium_subscribers, fe)

        list = self.get_list()
        if self.likes == len(list) and self.comments == len(list):
            # self.remove_user(subscribers)
            return True

        elif self.user in subscribers:
            # self.remove_user(subscribers)
            return True
        elif self.user in premium_subscribers:
            # self.remove_user(subscribers)
            return True

        else:
            return f"You liked {self.likes} pictures and {self.comments} comments out of {len(list)}"

    def check_if_exists_in_list(self):
        current_list = self.get_list()

        media_ids = [i['media_id'] for i in current_list]
        if self.media_id in media_ids:

            return True

    def add_to_list(self):
        "Adds the user data to the list"

        # List manipulation
        current_list = self.get_list()

        media_ids = [i['media_id'] for i in current_list]
        user = {
            'media_id': self.media_id,
            'media_url': self.url
        }
        try:
            if self.media_id in media_ids:
                print("exists")
            elif len(current_list) >= 15:
                current_list.remove(current_list[0])
                current_list.append(user)
            else:
                current_list.append(user)
        except IndexError:
            current_list.append(user)
        with open("main/list.json", "w") as f:
            json.dump(current_list, f)


class Subscriber(object):
    def __init__(self):
        self.file = ''

    def get_subscribers(self, premium=False):
        "Return The List of subscribers or premium subscribers if specified"
        directory = "main/premium_subscribers.json" if premium else "main/subscribers.json"
        try:
            with open(directory, 'r') as self.file:
                try:
                    #data = pickle.load(f)
                    data = json.loads(self.file.read())
                except EOFError as e:
                    data = []
        except:
            subscribers = INITIAL_SUBS
            with open(directory, 'w+') as self.file:
                json.dump(subscribers, self.file)
        return list(data)

    def activate(self, user_obj, premium=False):
        "Adds user handle to data storage"
        user = user_obj.text
        users = self.get_subscribers()
        print("users11", users)
        directory = "main/premium_subscribers.json" if premium else "main/subscribers.json"
        if user in users:
            return bot.send_message(
                int(ADMIN_ID),
                "Already a subscriber."
            )
        else:
            self.file = open(directory, "w")
            users.append(user)
            print("users", users)
            json.dump(users, self.file)
            self.file.close()
            return bot.send_message(
                int(ADMIN_ID),
                f"<b>{user} Subscription activated!</b>",
                parse_mode=telegram.ParseMode.HTML,
            )

    def deactivate(self, user_obj, premium=False):
        "removes user handle to data storage"
        user = user_obj.text
        users = self.get_subscribers()
        directory = "main/premium_subscribers.json" if premium else "main/subscribers.json"

        if user not in users:
            return bot.send_message(
                int(ADMIN_ID),
                "This user is not a subscriber"
            )
        else:
            self.file = open(directory, "w")
            users.remove(user)
            json.dump(users, self.file)
            self.file.close()
            return bot.send_message(
                int(ADMIN_ID),
                f"<b>{user} Subscription deactivated!</b>",
                parse_mode=telegram.ParseMode.HTML,
            )
