import collections
import enum
import html
import logging
import re


class Event(collections.namedtuple('Event', 'category data')):
    class Category(enum.Enum):
        MESSAGE = enum.auto()
        TICK = enum.auto()
        USER_STATUS_UPDATE = enum.auto()
        USER_ID_UPDATE = enum.auto()
        CONNECTOR_STATUS = enum.auto()

    Channel = namedtuple('Channel' , 'sender receiver conversation network')
    channel = Channel('olivier', 'julien', 'topic', 'symphony')

    Message = namedtuple('Message' , 'channel flags content mentions attachments')
    message = Message(channel, [], [], [], [])

    PresenceStatus = namedtuple('PresenceStatus' , 'user status description')
    presence_status = PresenceStatus('olivier', 'busy', 'I am working hard...')

    class Tick(collections.namedtuple('Tick' , 'trigger date argument')):
        class Category(enum.Enum):
            ALARM = enum.auto()
            COUNTDOWN = enum.auto()
            PERIOD = enum.auto()

    tick = Tick('alarm', 0, 'some data')


    class ConnectorCommand(collections.namedtuple('ConnectorCommand' , 'command argument')):
        class Category(enum.Enum):
            KILL = enum.auto()
            REBOOT = enum.auto()
            SHUTDOWN = enum.auto()
            IGNORE = enum.auto()
            MUTE = enum.auto()
            START = enum.auto()
            STOP = enum.auto()

    class ConnectorStatus(collections.namedtuple('ConnectorCommand' , 'command argument')):
        class Category(enum.Enum):
            READY = enum.auto()
            UP = enum.auto()
            DOWN = enum.auto()
            OK = enum.auto()
            ERROR = enum.auto()

    class UserStatus(collections.namedtuple('UserStatus' , 'identifier network status description')):
        class Category(enum.Enum):
            UNKOWN = enum.auto()
            AVAILABLE = enum.auto()
            NEARBY = enum.auto()
            BUSY = enum.auto()
            OFFLINE = enum.auto()
            HEARTBEAT = enum.auto()


    class User(collections.namedtuple('User' , 'identifier status description')):
        class Category(enum.Enum):
            UNKOWN = enum.auto()
            AVAILABLE = enum.auto()
            NEARBY = enum.auto()
            BUSY = enum.auto()
            OFFLINE = enum.auto()
            HEARTBEAT = enum.auto()

    class ConversationUpdate(collections.namedtuple('ConversationUpdate' , 'identifier type')):
        class Category(enum.Enum):
            OPEN = enum.auto()
            CLOSE = enum.auto()

USER_DISCOVERY
  network
  framework_id
  network_id
USER_CREATION
  framework_id
  kind
  roles
  network
  network_id
USER_AMENDMENT
  network
  identifier
  framework_identifier
  network_identifier




data_framework
  name 'jojo'
  identifier 12345
  kind HUMAN
  roles ['admin', 'trader', 'guest']
  network_identifiers {'symphony': 338478237829}
  presence_statuses {'symphony': 'offline'}

data_connector
  name 'jojo'
  identifier 'jojo@gmail.com'




event_framework
  name 'jojo'
  identifier 12345
  kind HUMAN
  roles ['admin', 'trader', 'guest']

event_connector
  network 'symphony'
  name '???'
  identifier 'jojo@gmail.com'




    def make_message(text):
        return Event(Event.Category.MESSAGE, text)

    def make_tick():
        return Event(Event.Category.TICK, None)

    def make_user_status(user, status, description=None):
        return Event(Event.Category.USER_STATUS_UPDATE, None)














class Message(Event):
    def __init__(self, sender, receiver, conversation, network, payload):
        self.__sender = sender
        self.__receiver = receiver
        self.__conversation = conversation
        self.__network = network
        self.__content = content



class Content(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, bytes, parser=stdparser):
        content = cls()
        return content

    def render(self, renderer=stdrenderer):
        return bytes()

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

    |
    [
    ]

    yyyy-mm-dd
    hh:mm:ss.uuu
    hh:mm:ss
    hh:mm

    @@hypermention

    {size,color,bold,noitalic}  large, medium, small ; red, blue, orange, green, yellow, purple, pink, black, white ; dark, bright

    mentions
    1=jojo
    2=titi

    payloads
    1=binary/type/subtype

    """




"""
presence statun
  user
  status
  description

timestamp

add_conversation
  name
  members

rem_conversation

"""


class Message(object):
    """ Internal representation of a message within the framework """

    PATTERN_MENTION = re.compile("^@[_A-Za-z0-9]+$")
    PATTERN_HASHTAG = re.compile("^#[_A-Za-z0-9]+$")
    PATTERN_CASHTAG = re.compile("^\$[_A-Za-z0-9]+$")
    PATTERN_INT = re.compile("^[0-9]+$")
    PATTERN_FLOAT = re.compile("^[0-9]+(\.[0-9]+)?$")
    PATTERN_WORD = re.compile("^[A-Z_a-z0-9]+$")
    PATTERN_STRING = re.compile("^[A-Z_a-z0-9]+$")
    PATTERN_OTHER = re.compile("^[A-Z_a-z0-9]+$")

    #PATTERN_DATE = re.compile("^[0-9]+$")
    #PATTERN_TIME = re.compile("^[0-9]+$") # [0-23][0-23][0-9][hH](:[0-59])? [1-12](:[0-59])?(AM|PM)
    #PATTERN_EMAIL = re.compile("^[0-9]+$")
    #PATTERN_TIME = re.compile("^[0-9]+$")
    #PATTERN_SEPARATOR = re.compile("^[\n\t.,]$")

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

