from messages.message import Message


class MessageHistory:
    def __init__(self):
        self._message_history: list[Message] = []
        self._assistant_message_history: list[Message] = []
        self._user_message_history: list[Message] = []
        self._system_message_history: list[Message] = []

        self.last_ai_message_id = None

    def add_message(self, message: Message):
        self._message_history.append(message)
        if message.is_user_message():
            self._user_message_history.append(message)
        elif message.is_assistant_message():
            self._assistant_message_history.append(message)
            self.last_ai_message_id = message.ID
        elif message.is_system_message():
            self._system_message_history.append(message)

    def update_message(self, message_id, content):
        for message in self._message_history:
            if message.ID == message_id:
                message.set_message(content)
                return True
        return False

    def remove_message(self, message_id):
        message_history = [message for message in self._message_history if message.ID != message_id]
        user_messages_history = [message for message in self._user_message_history if message.ID != message_id]
        assistant_message_history = [message for message in self._assistant_message_history if message.ID != message_id]
        system_message_history = [message for message in self._system_message_history if message.ID != message_id]
        self._message_history = message_history
        self._user_message_history = user_messages_history
        self._assistant_message_history = assistant_message_history
        self._system_message_history = system_message_history

    def remove_last_ai_message(self):
        last_ai_message = self._assistant_message_history.pop()
        self._message_history.remove(last_ai_message)

    def remove_last_user_message(self):
        last_user_message = self._user_message_history.pop()
        self._message_history.remove(last_user_message)

    def remove_last_system_message(self):
        last_system_message = self._system_message_history.pop()
        self._message_history.remove(last_system_message)

    def get_messages_as_json_string(self):
        return [message.get_as_dict() for message in self._message_history]

    def get_last_ai_message(self):
        return self._assistant_message_history[-1]

    def __str__(self):
        return ", ".join(map(lambda message: str(message), self._message_history))
