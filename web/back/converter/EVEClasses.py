class EVElab:
    name : str
    version : float
    author : str
    description : str

    nodes : list = []
    networks : list = []
    configs : list = []

    def __init__(self, name, version, author, description):
        self.name = name
        self.version = version
        self.author = author
        self. description = description
        

class EVEnode:

    id : int
    name : str
    type : str
    template : str
    image : str
    console : str
    cpu : int
    cpuLimit : int
    ram : int
    ethernet : int
    configID : int
    left : str
    top : str
    

    # left out delay, sat, icon

    def __init__(self, id, name, type, template, image, console, cpu, cpuLimit, ram, ethernet, configID, left, top):
        self.id = id
        self.name = name
        self.type = type
        self.template = template
        self.image = image
        self.console = console
        self.cpu = cpu
        self.cpuLimit = cpuLimit
        self.ram = ram
        self.ethernet = ethernet
        self.configID = configID
        self.left = left
        self.top = top
        self.interfaces : list = []

        pass


class EVEinterface:
    id: int
    name : str
    networkID : int

    def __init__(self, id, name, networkID):
        self.id = id
        self.name = name
        self.networkID = networkID

        pass

class EVEnetwork:
    id : int
    type : str
    name : str
    visibility : int
    left : int
    top : int

    #left out styling that CML does not support

    def __init__(self):
        pass

class EVEconfig:
    id : int
    encodedConfig : str

    def __init__(self, id, encodedConfig):
        self.id = id
        self.encodedConfig = encodedConfig

        pass