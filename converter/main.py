import convert

EVELab = convert.deconstructEVELab("sample4.unl")

CMLLab = convert.constructCMLLab(EVELab)

print(CMLLab)