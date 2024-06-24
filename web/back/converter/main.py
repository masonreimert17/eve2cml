import convert

EVELab = convert.deconstructEVELab("sample.unl")

CMLLab = convert.constructCMLLab(EVELab)

print(CMLLab)