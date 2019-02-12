import tcod
import textwrap

class Message:
    def __init__(self, text, color = tcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def addMessage(self, message):
        newMSGLines = textwrap.wrap(message.text, self.width)
        for line in newMSGLines:
            if len(self.messages) == self.height:
                del self.messages[0]

            self.messages.append(Message(line, message.color))