class OpenAIHelper:
    """
    ChatGPT helper class.
    """

    def __init__(self, config: dict):
        self.config = config
        self.conversations: dict[int: list] = {}  # {chat_id: history}
