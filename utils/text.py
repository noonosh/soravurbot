import json

j = json.load(open("app.json", "r", encoding="utf-8"))['app_data']


def text(key: str, language: str):
    """b Function that gets the text for the bot from text.json
    Args:
        key (str): [key for the json to find the right piece of text]
    Returns:
        [str]: [Text from text.json]
    """
    text = j["texts"][key]
    try:
        header = text["emoji"] + " "
    except KeyError:
        header = ""
        
    return header + text[language]


def button(key: str, language: str):
    """b Function that gets the text of a button in the bot from text.json
    Args:
        key (str): [key for the json to find the right piece of text]
    Returns:
        [str]: [Text from text.json]
    """
    button = j["buttons"][key]
    return button[language]
