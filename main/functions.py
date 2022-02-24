from config import client, insta, USERNAME, PASSWORD, ADMIN_ID, bot
import time
import json
import telegram


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
        print("just code: "+code)

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
        with open("main/list.json", 'a+') as f:
            pass
        with open("main/list.json", 'r') as f:
            # print(file.read())
            try:
                #data = pickle.load(f)
                data = json.loads(f.read())
            except EOFError:
                data = []
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

    def get_status(self):
        "Returns the user status of number of likes"

        # Get the susbcribers
        with open("main/subscribers.json", 'a+') as f:
            pass
        with open("main/subscribers.json", 'r') as f:
            # print(file.read())
            try:
                #data = pickle.load(f)
                subscribers = json.loads(f.read())
            except EOFError:
                return True

        if self.likes == len(subscribers) and self.comments == len(subscribers):
            return True

        elif self.user in subscribers:
            return True

        else:
            return f"You liked {self.likes} pictures and {self.comments} comments out of {len(subscribers)}"

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
            if len(current_list) >= 15:
                current_list.remove(current_list[0])
                current_list.append(user)
            elif self.media_id in media_ids:
                pass
            else:
                current_list.append(user)
        except IndexError:
            current_list.append(user)
        with open("main/list.json", "w") as f:
            json.dump(current_list, f)


class Subscriber(object):
    def __init__(self):
        self.file = ''

    def get_subscribers(self):
        "Return The List of subscribers"
        with open("main/subscribers.json", 'a+') as self.file:
            pass
        with open("main/subscribers.json", 'r') as self.file:
            # print(file.read())
            try:
                #data = pickle.load(f)
                data = json.loads(self.file.read())
            except EOFError:
                data = []
        return list(data)

    def activate(self, user_obj):
        "Adds user handle to data storage"
        user = user_obj.text
        users = self.get_subscribers()

        if user in users:
            return bot.send_message(
                int(ADMIN_ID),
                "Already a subscriber."
            )
        else:
            self.file = open("main/subscribers.json", "w")
            users.append(user)
            json.dump(users, self.file)
            self.file.close()
            return bot.send_message(
                int(ADMIN_ID),
                f"<b>{user} Subscription activated!</b>",
                parse_mode=telegram.ParseMode.HTML,
            )

    def deactivate(self, user_obj):
        "removes user handle to data storage"
        user = user_obj.text
        users = self.get_subscribers()

        if user not in users:
            return bot.send_message(
                int(ADMIN_ID),
                "This user is not a subscriber"
            )
        else:
            self.file = open("main/subscribers.json", "wb")
            users.remove(user)
            json.dump(users, self.file)
            self.file.close()
            return bot.send_message(
                int(ADMIN_ID),
                f"<b>{user} Subscription deactivated!</b>",
                parse_mode=telegram.ParseMode.HTML,
            )
