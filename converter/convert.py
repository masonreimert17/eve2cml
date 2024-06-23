from EVEClasses import EVElab, EVEnode, EVEinterface, EVEconfig
from CMLClasses import CMLLab, CMLNode, CMLInterface
import xmltodict
import yaml
import re
import base64

import json #temp

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



    #extract the configs for later use to resolve from nodes
    for config in xml_dict["lab"]["objects"]["configs"]["config"]:
        id = config["@id"]
        encodedText = config["#text"]
        lab.configs.append(EVEconfig(id, encodedText))



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
            print("adding " + interface["@name"] + " to " + XMLnode["@name"])
            node.interfaces.append(EVEinterface(
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

    links = {}

    # populate this with the links {legacyID, n1, n2, i1, i2}

    for node in EVElabInput.nodes:

        if int(node.cpuLimit) == 0: 
            node.cpuLimit = 100

        if node.template == "vios": 
            node.template = "iosv"


        interfaces, links = convertInterfaces(node.template,node.interfaces, node.id, links)

        nodeDict = {
            #add params to node

            "id" : "n" + node.id,
            "label" : node.name,
            "node_definition" : node.template,
            "image_definition" : node.image,
            "cpus" : int(node.cpu),
            "cpu_limit" : int(node.cpuLimit),
            "ram" : int(node.ram),
            "x" : int(node.left),
            "y" : int(node.top),
            "interfaces" : interfaces

        }

        for config in EVElabInput.configs:
            if node.configID == config.id:
                nodeDict["configuration"] = []
                bConfig = base64.b64decode(config.encodedConfig)
                decodedConfig = bConfig.decode('ascii').replace('\\n', '\n')
                nodeDict["configuration"].append({
                    "name" : "ios_config.txt",
                    "content" : decodedConfig
                })
        print(f"{decodedConfig}")


        #add node to tree
        CMLYAML["nodes"].append(nodeDict)

    linksList = [value for key, value in links.items()]

    #add links to tree
    CMLYAML["links"] = linksList

    return(yaml.dump(CMLYAML))

def convertInterfaces(nodeType, inputInterfaces, nodeID, links):
    networkIDs = []
    lidCounter = 0

    if nodeType == "iosv":
        interfaces = []
        idx = 0
        i = 0
        print(interfaces)

        for interface in inputInterfaces:

            maxInterface = 0

            #normalize interface name
            if re.search(r"Gi\d+/\d+", interface.name):
                if int(interface.name.split("/")[1]) > maxInterface:
                    maxInterface = interface.name.split("/")[1]
            idx +=1

            if interface.networkID:
                if interface.networkID in links:
                    links[interface.networkID]["n2"] =  "n" + str(nodeID)
                    links[interface.networkID]["i2"] =  "i" + interface.name.split("/")[1]
                else:
                    links[interface.networkID] = {
                        "id" : "l" + str(lidCounter),
                        "n1" : "n" + str(nodeID),
                        "i1" : "i" + interface.name.split("/")[1],
                        "label" : "From EVE -> Legacy ID " + str(interface.networkID)
                    }
                    lidCounter+=1


        while i <= int(maxInterface):
            interfaces.append({
                "id" : "i" + str(i), 
                "label" : "GigabitEthernet0/" + str(i),
                "type" : "physical",
                "slot" : i
            })
            i+=1

        print(links)
        return(interfaces, links)

