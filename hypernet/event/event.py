import collections
import enum
import html
import logging
import re


def make_user(framework_id, kind, roles):
    user = Event.UserDiscovery(framework_id, kind, roles, None, None)
    return Event(Event.Category.USER_DISCOVERY, user)


class Event(collections.namedtuple('Event', 'category payload')):
    class Category(enum.Enum):
        MESSAGE = enum.auto()
        TICK = enum.auto()
        PRESENCE_STATUS = enum.auto()
        USER_DISCOVERY = enum.auto()
        CONNECTOR_STATUS = enum.auto()

    class Message(collections.namedtuple('Message', 'channel flags content mentions attachments')):
        class Channel(collections.namedtuple('Channel', 'sender receiver conversation network')):
            pass

    class Tick(collections.namedtuple('Tick', 'trigger date argument')):
        class Category(enum.Enum):
            ALARM = enum.auto()
            COUNTDOWN = enum.auto()
            PERIOD = enum.auto()

    class ConnectorStatus(collections.namedtuple('ConnectorCommand', 'command argument')):
        class Category(enum.Enum):
            READY = enum.auto()
            UP = enum.auto()
            DOWN = enum.auto()
            SHUTDOWN = enum.auto()

    class PresenceStatus(collections.namedtuple('PresenceStatus', 'identifier network status description')):
        def __new__(cls, identifier, network, status, description=None):
            return cls(identifier, network, status, description)

    # class UserCreation(collections.namedtuple('UserCreation' , 'framework_id kind roles network_id network')):
    # class UserAmendment(collections.namedtuple('UserAmendment' , 'framework_id kind roles network_id network')):
    class UserDiscovery(collections.namedtuple('UserDiscovery', 'framework_id kind roles network_id network')):
        def __new__(cls, framework_id, kind, roles, network_id, network=None):
            # return cls(framework_id, kind, roles, network_id, network)
            return super().__new__(cls, framework_id, kind, roles, network_id, network)


"""
    class ConnectorCommand(collections.namedtuple('ConnectorCommand' , 'command argument')):
        class Category(enum.Enum):
            KILL = enum.auto()
            REBOOT = enum.auto()
            SHUTDOWN = enum.auto()
            IGNORE = enum.auto()
            MUTE = enum.auto()
            START = enum.auto()
            STOP = enum.auto()

    class ConversationUpdate(collections.namedtuple('ConversationUpdate' , 'identifier type')):
        class Category(enum.Enum):
            OPEN = enum.auto()
            CLOSE = enum.auto()

timestamp

add_conversation
  name
  members

rem_conversation

"""


class Content(object):
    STD_RENDERER = 1
    STD_PARSER = 2

    def __init__(self, text):
        self.__content = text

    @classmethod
    def parse(cls, binary, parser=STD_PARSER):
        text = binary.decode('utf8')
        return cls(text)

    def render(self, renderer=STD_RENDERER):
        binary = bytes()
        binary += self.__content.encode('utf8')
        return binary

    """
    <<<
    !!
    &ref
    =ref
    ::
    >>>
    separator | || |||

    @mention
    #hashtag
    $cashtag
    "some utf-8 text"
    'some ascii text'
    (emoticon)
    99.999
    ascii_token

    =binary/name/type/subtype

    | opener
    [ inter
    ] closer

    yyyy-mm-dd
    hh:mm:ss.uuu
    hh:mm:ss
    hh:mm

    @@hypermention

    {format}

    mentions
    1=jojo
    2=titi

    payloads
    1=binary/type/subtype

    """


class Format(collections.namedtuple('Format', 'size color light bold italic underlined')):
    """Presentation should not contain any kind of information since it is not guaranteed to be rendered as expected"""
    class Size(enum.Enum):
        SMALL = enum.auto()
        NORMAL = enum.auto()
        LARGE = enum.auto()

    class Color(enum.Enum):
        RED = enum.auto()
        BLUE = enum.auto()
        ORANGE = enum.auto()
        GREEN = enum.auto()
        YELLOW = enum.auto()
        PURPLE = enum.auto()
        PINK = enum.auto()
        BLACK = enum.auto()
        WHITE = enum.auto()

    class Light(enum.Enum):
        DARK = enum.auto()
        NORMAL = enum.auto()
        BRIGHT = enum.auto()

    def __new__(cls, *, size=Size.NORMAL, color=Color.BLACK, light=Light.NORMAL, bold=False, italic=False, underlined=False):
        return cls(size, color, light, bold, italic, underlined)


class Message(object):
    """ Internal representation of a message within the framework """

    PATTERN_MENTION = re.compile("^@[_A-Za-z0-9]+$")
    PATTERN_HASHTAG = re.compile("^#[_A-Za-z0-9]+$")
    PATTERN_CASHTAG = re.compile("^$[_A-Za-z0-9]+$")
    PATTERN_NUMBER = re.compile("^[0-9]+([.][0-9]+)?$")
    PATTERN_INT = re.compile("^[0-9]+$")
    PATTERN_FLOAT = re.compile("^[0-9]+[.][0-9]+$")
    PATTERN_WORD = re.compile("^[A-Z_a-z0-9]+$")
    PATTERN_STRING = re.compile("^[A-Z_a-z0-9]+$")
    PATTERN_OTHER = re.compile("^[A-Z_a-z0-9]+$")

    PATTERN_DATE = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    PATTERN_TIME = re.compile("^[0-9]{2}:[0-9]{2}(:[0-9]{2}(:[0-9]{1;6})?)?$")
    # [0-23][0-23][0-9][hH](:[0-59])? [1-12](:[0-59])?(AM|PM)
    # PATTERN_EMAIL = re.compile("^[0-9]+$")
    PATTERN_SEPARATOR = re.compile("^[\n\t.,]$")

    @staticmethod
    def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

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

    """
    def set_first_mention(self, mention):
        if len(self.__elements) > 0:
            if isinstance(self.__elements[0], Message.Mention):
                self.__elements[0] = Message.Mention(mention)
            else:
                self.__elements.insert(0, Message.Mention(mention))
        else:
            self.__elements.append(Message.Mention(mention))
    """

    def increment_numbers(self):
        elements = list()
        for element in self.__elements:
            if isinstance(element, Message.Number):
                element = int(element) + 1
                elements.append(Message.Number(element))
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
