import re


class Message(object):
    """ Internal representation of a message within the framework """
    def __init__(self):
        self.__elements = list()

    @classmethod
    def build(cls, text):
        message = cls()
        token_list = text.split()
        for token in token_list:
            if re.compile("^@[A-Za-z0-9]+$").match(token):
                message.add_element(cls.Mention(token))
            elif re.compile("^#[A-Za-z0-9]+$").match(token):
                message.add_element(cls.Hashtag(token))
            else:
                message.add_element(cls.Word(token))
        return message

    def add_element(self, element):
        self.__elements.append(element)

    def find_elements(self, element_type=object):
        result = list()
        for element in self.__elements:
            if isinstance(element, element_type):
                result.append(element)
        return result

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
       """ Some plain text """
       def __new__(cls, *args, **kw):
           return str.__new__(cls, *args, **kw)

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
                tokens.append('\033[36m{}\033[0m'.format(element))
            elif isinstance(element, self.Hashtag):
                tokens.append('\033[34m{}\033[0m'.format(element))
            else:
                raise Exception('Invalid type for element')
        return ' '.join(tokens)

