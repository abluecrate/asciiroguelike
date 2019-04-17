import tcod
import textwrap

class Message:
    def __init__(self, text, color = tcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = [] # List of Messages
        self.x = x
        self.width = width
        self.height = height

    def addMessage(self, message):
        # If necessary split lines
        newMSGLines = textwrap.wrap(message.text, self.width)

        for line in newMSGLines:
            # If bugger is full, remove first line to make room
            if len(self.messages) == self.height:
                del self.messages[0]
            # Add new line
            self.messages.append(Message(line, message.color))
