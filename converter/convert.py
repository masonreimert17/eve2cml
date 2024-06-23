from EVEClasses import EVElab, EVEnode, EVEinterface
import xmltodict
import yaml


#finish by parsing out networks, and configs
def deconstructEVELab(UNLFilePath):
    with open(UNLFilePath) as f:
        xml_string = f.read()
    
    xml_dict = xmltodict.parse(xml_string)
    #print(json.dumps(xml_dict))

    lab = EVElab(xml_dict["lab"]["@name"], 
                 xml_dict["lab"]["@version"], 
                 xml_dict["lab"]["@author"], 
                 xml_dict["lab"]["description"])


    #loop though the nodes and create a node class instansiation for each node
    for XMLnode in xml_dict["lab"]["topology"]["nodes"]["node"]:

        node = EVEnode(
            id = XMLnode["@id"],
            name = XMLnode["@name"],
            type = XMLnode["@type"],
            template = XMLnode["@template"],
            image = XMLnode["@image"],
            console = XMLnode["@console"],
            cpu = XMLnode["@cpu"],
            cpuLimit = XMLnode["@cpulimit"],       
            ram = XMLnode["@ram"],
            ethernet = XMLnode["@ethernet"],
            uuid = XMLnode["@uuid"],
            firstMAC = XMLnode["@firstmac"],
            qemuOptions = XMLnode["@qemu_options"],
            qemuVersion = XMLnode["@qemu_version"],
            qemuArch = XMLnode["@qemu_arch"],
            configID = XMLnode["@config"],
            left = XMLnode["@left"],
            top = XMLnode["@top"],
        )

        for interface in XMLnode["interface"]:
            node.addInterface(EVEinterface(
                id = interface["@id"],
                name = interface["@name"],
                networkID = interface["@network_id"]
            ))
        
        lab.nodes.append(node)
            

    print(lab.name + " ", lab.version + " ", lab.author + " ", lab.description + " ")
    for node in lab.nodes:
        print (node.name + " " + node.image)
    return(lab)

def constructCMLLab(EVElabInput : EVElab):
    CMLYAML = {}

    #bootstrap YAML Tree
    CMLYAML["lab"] = {}
    CMLYAML["nodes"] = []
    CMLYAML["links"] = []
    CMLYAML["annotations"] = []

    #set global options
    CMLYAML["lab"]["title"] = EVElabInput.name
    CMLYAML["lab"]["description"] = EVElabInput.description
    CMLYAML["lab"]["version"] = "0.0." + EVElabInput.version
    CMLYAML["lab"]["notes"] = "Author(from EVE-NG): " + EVElabInput.author

    print(EVElabInput.nodes)

    idx = 0

    for node in EVElabInput.nodes:

        if int(node.cpuLimit) == 0: 
            node.cpuLimit = 100

        if node.template == "vios": 
            node.template = "iosv"

        nodeDict = {
            #add params to node

            "id" : "n" + node.id,
            "label" : node.name,
            "node_definition" : node.template,
            "image_definition" : node.image,
            "cpus" : int(node.cpu),
            "cpu_limit" : int(node.cpuLimit),
            "ram" : int(node.ram),
            "x" : int(node.left[0]), #TODO: fix this, this should not be a Touple but somewhere between XML and here it becomes one!
            "y" : int(node.top)

        }

        #add node to tree
        CMLYAML["nodes"].append(nodeDict)

        idx += 1

    return(yaml.dump(CMLYAML))
