paths = [
    "../UOBM/UOBM35/MCS1",
    "../UOBM/UOBM35/MCS2",
    "../UOBM/UOBM35/MCS3",
    "../UOBM/UOBM35/MCS4",
    "../UOBM/UOBM35/MCS5",
    "../UOBM/UOBM35/MCS6",
    "../UOBM/UOBM35/MCS7",
    "../UOBM/UOBM35/MCS8",
    "../UOBM/UOBM35/MCS9",
    "../UOBM/UOBM35/MCS10",
    "../UOBM/UOBM35/MCS11",
    "../UOBM/UOBM35/MCS12",
    "../UOBM/UOBM35/MCS13",
    "../UOBM/UOBM35/MCS14",
    "../UOBM/UOBM35/MCS15",
    "../UOBM/UOBM35/MCS16"
]

Kset = set()
for path in paths:
    with open(path) as f:
        K = f.read().split("\n\n")
        for axiom in K:
            Kset.add(axiom)
        f.close()

K = list(Kset)
filename = '../oriData/UOBM35allAxioms.txt'
with open (filename,'w') as file_object:
    for axiom in K:
        file_object.write(axiom)  
        file_object.write("\n")
    file_object.close()

