import html
import logging
import re


class Message(object):
    """ Internal representation of a message within the framework """

    PATTERN_MENTION = re.compile("^@[A-Z_a-z0-9]+$")
    PATTERN_HASHTAG = re.compile("^#[A-Z_a-z0-9]+$")
    PATTERN_NUMBER = re.compile("^[0-9]+$")
    PATTERN_WORD = re.compile("^[A-Z_a-z0-9]+$")

    def __init__(self):
        self.__elements = list()

    @classmethod
    def build(cls, text):
        message = cls()
        for token in text.split():
            if Message.PATTERN_MENTION.match(token):
                message._add_element(cls.Mention(token[1:]))
            elif Message.PATTERN_HASHTAG.match(token):
                message._add_element(cls.Hashtag(token[1:]))
            elif Message.PATTERN_NUMBER.match(token):
                message._add_element(cls.Number(token))
            elif Message.PATTERN_WORD.match(token):
                message._add_element(cls.Word(token))
            else:
                logging.debug('\033[31m{}\033[0m should maybe escaped as \033[32m{}\033[0m?'.format(token, html.escape(token)))
                raise ValueError('{} is not a valid element value'.format(token))
        return message

    def _add_element(self, element):
        self.__elements.append(element)

    def find_elements(self, element_type=object):
        result = list()
        for element in self.__elements:
            if isinstance(element, element_type):
                result.append(element)
        return result

    def set_first_mention(self, mention):
        if len(self.__elements) > 0:
            if isinstance(self.__elements[0], Message.Mention):
                self.__elements[0] = Message.Mention(mention)
            else:
                self.__elements.insert(0, Message.Mention(mention))
        else:
            self.__elements.append(Message.Mention(mention))

    def increment_numbers(self):
        elements = list()
        for element in self.__elements:
            if isinstance(element, Message.Number):
                element += 1
                elements.append(Message.Number(str(element)))
            else:
                elements.append(element)
        self.__elements = elements

    class Element(object):
        """ A kind of token, part of a message """
        def __init__(self, content, form=None):
            self.content = content
            self.form = form

    class Mention(str):
       """ A user mentioned such @user """
       def __new__(cls, *args, **kw):
            return str.__new__(cls, *args, **kw)

    class Hashtag(str):
       """ A topic mentioned such #topic """
       def __new__(cls, *args, **kw):
            return str.__new__(cls, *args, **kw)

    class Word(str):
       """ Some plain text such blablabla """
       def __new__(cls, *args, **kw):
            return str.__new__(cls, *args, **kw)

    class Number(int):
       """ Some number such 409812 """
       def __new__(cls, *args, **kw):
            return int.__new__(cls, *args, **kw)

    class Form(object):
        def __init__(self):
            self.bold = False
            self.italic = False
            self.underlined = False
            self.size = 1.
            self.fgcolor = (255, 255, 255)
            self.bgcolor = (0, 0, 0)

    def __str__(self):
        tokens = list()
        for element in self.find_elements():
            if isinstance(element, self.Word):
                tokens.append('\033[35m{}\033[0m'.format(element))
            elif isinstance(element, self.Mention):
                tokens.append('\033[36m@{}\033[0m'.format(element))
            elif isinstance(element, self.Hashtag):
                tokens.append('\033[34m#{}\033[0m'.format(element))
            elif isinstance(element, self.Number):
                tokens.append('\033[33m{}\033[0m'.format(element))
            else:
                raise TypeError('{} is not a valid element type'.format(type(element)))
        return ' '.join(tokens)

