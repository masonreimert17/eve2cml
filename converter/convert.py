from classes import EVElab, EVEnode, EVEinterface, EVEconfig
import xmltodict
import yaml
import re
import base64
import json
import argparse

def deconstructEVELab(UNLFilePath):

    xml_dict = openUNL(UNLFilePath)

    #create the lab object
    lab = createLab(xml_dict)

    #extract the configs for later use to resolve from nodes    
    extractConfigs(xml_dict, lab)

    #loop though the nodes and create a node class instansiation for each node
    extractNodes(xml_dict, lab)
            
    return(lab)

def constructCMLLab(EVElabInput : EVElab, YAMLPath):
    
    CMLYAML = bootstrapCML()

    insertCMLMetadata(CMLYAML, EVElabInput)
    
    insertCMLNodesLinks(EVElabInput, CMLYAML)

    with open(YAMLPath, 'w') as file:
        yaml.dump(CMLYAML, file, default_flow_style=False)
        return(1)

'''
| Validate Mappings | 
    only used in web version to validate a mapping exists for each node
    + UUID : UUID file in static folder from back end
'''
def validate(uuid):

    package = {}

    #get templates available
    mappings = getMappings()
    for mapping in mappings["node_definitions"]:
        package["cisco_templates_avail"].append(mapping["targetDef"])

    lab = deconstructEVELab("../static/" + uuid)

    for node in lab.nodes:
        targetDef = ""

        for mapping in mappings["node_definitions"]:
            if mapping["sourceDef"] == node.template:
                targetDef = mapping["targetDef"]

        package["nodes"].append({
            "node_id" : node.id,
            "node_name" : node.name,
            "eve_template" : node.template,
            "cisco_target" : ""
        })
    return(package)

# [-------------------- Supporting Functions --------------------]

'''
| Get Mappings |
    Get Node to Node mappings from the JSON, this should be renamed.
'''
def getMappings():
    with open('mappings.json') as json_file:
        return(json.load(json_file))

'''
| Find Max Interfaces |
    Finds the highest interface number on a specified device.
    This is needed because CML will only accept continuous interface lists.
    + inputInterfaces : a list of interface objects to enum over
    + nodeType : the pre-conversion node template, used to lookup node in mapping file
'''
def findMaxInterface(inputInterfaces, nodeType):
    maxInterface = 0

    mappings = getMappings()

    for mapping in mappings["node_definitions"]:
        if mapping["targetDef"] == nodeType:
            position = mapping["interfaces"]["source_pattern"].find('%')

    for interface in inputInterfaces:
        if int(interface.name[position]) > int(maxInterface):
            maxInterface = interface.name[position]
    
    return(maxInterface)

'''
| Create Interfaces |
    Create a config block for X number of interfaces, using % template.
    + count : number of config blocks to create, after being determined by findMaxInterface()
    + prefix : the text prefix before the interface number
    + offset : used mainly to control if the node starts its numbering at 0 or 1
'''
def createInterfaces(count, prefix, offset):
    i = 0
    interfaces = []
    while i <= int(count):
        interfaces.append({
            "id" : "i" + str(i), 
            "label" : prefix.replace("%", str(i + int(offset))),
            "type" : "physical",
            "slot" : i 
        })
        i+=1

    return(interfaces)

'''
| Create Links |
    Create link interface config blocks. 
    + imputInterfaces : the pre-conversion list of interface objects
    + nodeID : the node that we are creating links for
    + links : the running list of links
    + nodeType : the type of node (used for interface prefix)
'''
def createLinks(inputInterfaces, nodeID, links, nodeType):
    lidCounter = 0


    mappings = getMappings()
    for mapping in mappings["node_definitions"]:
        if mapping["targetDef"] == nodeType:
            position = mapping["interfaces"]["source_pattern"].find('%')

    #loop through interfaces to build links
    for interface in inputInterfaces:
       
        #connect interface to link, if link does not exist create link
        if interface.networkID in links:
            links[interface.networkID]["n2"] =  "n" + str(nodeID)
            links[interface.networkID]["i2"] =  "i" + interface.name[position]

        else:
            links[interface.networkID] = {
                "id" : "l" + str(lidCounter),
                "n1" : "n" + str(nodeID),
                "i1" : "i" + interface.name[position],
                "label" : "From EVE -> Legacy ID " + str(interface.networkID)
            }
            lidCounter+=1

    return(links)

'''
| Find Config File Name |
    Find the config file name from the mapper. CML needs a name for each file it attaches to a node.
    + node : the pre-conversion node object to lookup in mapper
'''
def findConfigFileName(node):
    mappings = getMappings()
    for mapping in mappings["node_definitions"]:
        if mapping["targetDef"] == node.template:
            return mapping["cfg_filename"]
        
# [-------------------- Extraction Functions --------------------]

'''
| Extract Configs |
    Extract Configurations From EVE-NG XML Structure
    + xml_dict : the post conversion dictionary of the EVE-NG UNL File
    + lab : the EVE lab object to place the configurations in
'''
def extractConfigs(xml_dict, lab):
    if "objects" in xml_dict["lab"]:
        for config in xml_dict["lab"]["objects"]["configs"]["config"]:
            id = config["@id"]
            encodedText = config["#text"]
            lab.configs.append(EVEconfig(id, encodedText))

'''
| Open UNL |
    Open UNL File and Convert it to Dict that is used to load into classes
    + filePath : the path of the UNL file to open
'''
def openUNL(filePath):
    with open(filePath) as f:
        xml_string = f.read()
    
    return(xmltodict.parse(xml_string))

'''
| Create Lab |
    Create the lab class object and bootstrap it with metadata from the EVE-NG lab.
    + xml_dict : dict of UNL file outputted from openUNL()
'''
def createLab(xml_dict):
    return(EVElab(xml_dict.get("lab", {}).get("@name", "EVE_CONVERTED"), 
                 xml_dict.get("lab", {}).get("@version", "0.0.1"), 
                 xml_dict.get("lab", {}).get("@author", ""),
                 xml_dict.get("lab", {}).get("@description", "")))

'''
|Extract Nodes|
    Enum through the list of nodes in the XML from EVE-NG, create an obj for each.
    Since interfaces is a sub-obj of nodes interfaces are ran here too.
    Once nodes and interfaces are done, add the nodes to the lab
    + xml_dict : dict of UNL file outputted from openUNL()
    + lab : the EVE lab object to place the nodes and interfaces in
'''
def extractNodes(xml_dict, lab):

    for XMLnode in xml_dict["lab"]["topology"]["nodes"]["node"]:

        node = EVEnode(
            id = XMLnode.get("@id", ""),
            name = XMLnode.get("@name", ""),
            type = XMLnode.get("@type", ""),
            template = XMLnode.get("@template", ""),
            image = XMLnode.get("@image", ""),
            console = XMLnode.get("@console", ""),
            cpu = XMLnode.get("@cpu", 0),
            cpuLimit = XMLnode.get("@cpulimit", 0),
            ram = XMLnode.get("@ram", 0),
            ethernet = XMLnode.get("@ethernet", ""),
            configID = XMLnode.get("@config", ""),
            left = XMLnode.get("@left", ""),
            top = XMLnode.get("@top", "")
        )

        #check if only a single interface is contained, or if it is a list of interfaces
        if isinstance(XMLnode.get("interface"), list):
            for interface in XMLnode.get("interface", []):
                node.interfaces.append(EVEinterface(
                    id = interface.get("@id", ""),
                    name = interface.get("@name", ""),
                    networkID = interface.get("@network_id", "")
                ))
        else:
            interface = XMLnode.get("interface")
            node.interfaces.append(EVEinterface(
                id = interface.get("@id", ""),
                name = interface.get("@name", ""),
                networkID = interface.get("@network_id", "")
            ))

        lab.nodes.append(node)

# [-------------------- Construction Functions--------------------]

'''
| Bootstrap CML |
    Bootstrap CML Tree Roots that are required for the YAML
    + CMLYAML : the starting YAML for the CML lab
'''
def bootstrapCML():
    CMLYAML = {}

    CMLYAML["lab"] = {}
    CMLYAML["nodes"] = []
    CMLYAML["links"] = []
    CMLYAML["annotations"] = []

    return(CMLYAML)

'''
| Insert CML Metadata |
    Insert the metadata stored in the lab class into the CMLYAML.
    CMLYAML : the starting YAML for the CML lab
'''
def insertCMLMetadata(CMLYAML, EVElabInput):
    CMLYAML["lab"]["title"] = EVElabInput.name
    CMLYAML["lab"]["description"] = EVElabInput.description
    CMLYAML["lab"]["version"] = "0.0." + EVElabInput.version
    CMLYAML["lab"]["notes"] = "Author(from EVE-NG): " + EVElabInput.author

'''
| Transfer Node Configuration |
    Transfer the node's configuration from the EVE data struct to the CML nodeDict
    + EVElabInput : input of the lab object with the pre-conversion nodes
    + node : the pre-conversion EVE-NG node
    + nodeDict : the new node's data structure
'''
def transferNodeConfiguration(EVElabInput, node, nodeDict):
            for config in EVElabInput.configs:
                if node.id == config.id:
                    nodeDict["configuration"] = []
                    bConfig = base64.b64decode(config.encodedConfig)
                    decodedConfig = bConfig.decode('ascii').replace('\\n', '\n')
                    nodeDict["configuration"].append({
                        "name" : findConfigFileName(node),
                        "content" : decodedConfig
                    })


'''
| Compile Node Dict |
    Create the branch of the YAML tree for a node, return this as a dict
    + node : the kinda pre-conversion node. The template has already been changed #TODO - this should be not like this
    + interfaces : the interfaces to add to the node, since CML stores them under the node branch
'''
def compileNodeDict(node, interfaces):
    nodeDict = {
        "id" : "n" + node.id,
        "label" : node.name,
        "node_definition" : node.template,
        "image_definition" : node.image,
        "x" : int(node.left),
        "y" : int(node.top),
        "interfaces" : interfaces
    }

    if node.cpu != 0:
        nodeDict["cpus"] = int(node.cpu)

    if int(node.cpuLimit) > 20:
        nodeDict["cpu_limit"] = int(node.cpuLimit)

    if node.ram != 0:
        nodeDict["ram"] = int(node.ram)

    return(nodeDict)
'''
| Insert CML Node Links |
    Insert Nodes & Links to the CML YAML File
    CMLYAML : the starting YAML for the CML lab
    EVElabInput : input of the lab object with the pre-conversion nodes
'''
def insertCMLNodesLinks(EVElabInput, CMLYAML):
    links = {}

    mappings = getMappings()

    for node in EVElabInput.nodes:

        #check if node is supported
        supported = False
        for mapping in mappings["node_definitions"]:
            if mapping["sourceDef"] == node.template:
                node.template = mapping["targetDef"]
                supported = True

        if supported == False:
            print("Lab contains upsupported node of type " + node.template)
            break

        #EVE-NG sees CPU Limit of 0 as unset, CML will not take this
        if int(node.cpuLimit) == 0: 
            node.cpuLimit = 100


        #find the amount of interfaces neccacry for CML to accept the interface config
        maxInterface = findMaxInterface(node.interfaces, node.template)


        links = createLinks(node.interfaces, node.id, links, node.template)

        mappings = getMappings()
        for mapping in mappings["node_definitions"]:
            if mapping["targetDef"] == node.template:
                interfaces = createInterfaces(maxInterface, mapping["interfaces"]["dest_pattern"], mapping["interfaces"]["if_offset"])

        nodeDict = compileNodeDict(node, interfaces)

        #transfer the configs from the old data structures to the new data structures
        transferNodeConfiguration(EVElabInput, node, nodeDict)


        #add node to tree
        CMLYAML["nodes"].append(nodeDict)

    linksList = [value for key, value in links.items()]

    #add links to tree
    CMLYAML["links"] = linksList


'''
| Main IF |
    For direct invocation of this file via terminal
    + -in : input file
    + -out : output file
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert EVE-NG Lab to CML Lab')
    parser.add_argument('-in', '--input_path', type=str, required=True, help='Input Lab UNL File')
    parser.add_argument('-out', '--output_path', type=str, required=True, help='Output Lab YAML File')
    
    args = parser.parse_args()
    
    input_string = args.input_path
    output_string = args.output_path
    
    EVELab = deconstructEVELab(input_string)
    CMLLab = constructCMLLab(EVELab, output_string)

    print(f"Lab saved to: {output_string}")

