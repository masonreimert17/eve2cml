class CMLLab:
    title : str
    notes : str
    description : str
    version : float

    def __init__(self, title, notes, description, version):
        self.title = title
        self.notes = notes
        self.description = description
        self.version = version

        pass

class CMLNode:
    id : str
    configuration : str
    cpuLimit : int
    cpus : int
    imageDefinition : str
    label : str
    nodeDefinition : str
    ram : int
    x : str
    y : str

    def __init__(self, id, configuration, cpuLimit, cpus, imageDefinition, label, nodeDefinition, ram, x, y):
        self.id = id
        self.configuration = configuration
        self.cpuLimit = cpuLimit
        self.cpus = cpus
        self.imageDefinition = imageDefinition
        self.label = label
        self.nodeDefinition = nodeDefinition
        self.ram = ram
        self.x = x
        self.y = y

        pass

class CMLInterface:
    id : int
    label: str
    type: str

    def __init__(self, id, label, type):
        self.id = id
        self.label = label
        self.type = type

        pass

class CMLNetwork:
    def __init__(self):
        pass

class CMLConfig:
    def __init__(self):
        pass