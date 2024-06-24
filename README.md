# EVE-NG to Cisco Modeling Labs (CML) Converter Tool
Converter to convert labs from EVE-NG to Cisco Modeling Labs.

## Supported Node List
Below are the nodes supported for conversion. As of now other nodes will need to be removed from the EVE-NG UNL file before uploading. You can add support for nodes yourself by changing your mappings.json file if you are running the converter locally, or by subitting a PR to this repo to have us merge in new nodes to the cloud instances.
- IOSv
- IOSvL2
- IOL
- CSR1000v

## Options for Converting
### Using the Cloud Hosted Converter:
You can skip the hasstle and convert your labs for free at cml2eve.com which is ran by the maintainers of this repo and runs identical code to what you see here.

### Converting Locally (on your machine):
You can clone this repo and run the convert.py Python script to convert labs using the same code we use behind the scences in the cloud implamentation.
```Bash
#start by cloneing the repo
git clone https://github.com/masonreimert17/eve2cml.git

#install requirements via pip
python3 -m pip install -r requirements.txt

#cd into the converter folder
cd eve2cml/web/back/converter

#run the converter with the required params
python3 convert.py -in lab.unl -out lab.yaml
```
## Current Restrictions
Feel free to open a PR or reach out to us if you want to contribute to fixing any of these, we are working on them as well!
- Slot numbers for devices that use slot style interface numbering only support slot 0, ex 0/1-9, this will be fixed by 1.0.
- Only single digit interface numbers are supported (0-9), this will be fixed by 1.0.
- Anotations do not convert at this time (text + shapes).
- IOL nodes on EVE-NG are the same for L2/L3, just with a different icon. In CML they are different node types. We are working on the best way to address that so that the most situations work by default. 
