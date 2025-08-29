class Message:
    id_counter = -1

    @staticmethod
    def get_id():
        Message.id_counter += 1
        return Message.id_counter

    def __init__(self, role, message):
        self.ID = self.get_id()
        self._role = role
        self._message = message

    def is_user_message(self):
        return self._role == "user"

    def is_assistant_message(self):
        return self._role == "assistant"

    def is_system_message(self):
        return self._role == "system"

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = message

    def get_as_dict(self):
        message = {"role": self._role, "content": self._message}
        return message

    def __str__(self):
        return f"{{'role': '{self._role}', 'content': '{self._message}'}}"