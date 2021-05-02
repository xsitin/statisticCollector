class User:
    def __init__(self, user_id, group_id, group_name):
        self.user_id = user_id
        self.group_id = group_id
        self.group_name = group_name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""id:{self.user_id}|group_id:{self.group_id}|group_name:{self.group_name}"""
