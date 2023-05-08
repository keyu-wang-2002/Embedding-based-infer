paths = [
    "../UOBM/UOBM36/MCS1",
    "../UOBM/UOBM36/MCS2",
    "../UOBM/UOBM36/MCS3",
    "../UOBM/UOBM36/MCS4",
    "../UOBM/UOBM36/MCS5",
    "../UOBM/UOBM36/MCS6",
    "../UOBM/UOBM36/MCS7",
    "../UOBM/UOBM36/MCS8",
    "../UOBM/UOBM36/MCS9",
    "../UOBM/UOBM36/MCS10",
    "../UOBM/UOBM36/MCS11",
    "../UOBM/UOBM36/MCS12",
    "../UOBM/UOBM36/MCS13",
    "../UOBM/UOBM36/MCS14",
    "../UOBM/UOBM36/MCS15",
    "../UOBM/UOBM36/MCS16",
    "../UOBM/UOBM36/MCS17",
    "../UOBM/UOBM36/MCS18",
    "../UOBM/UOBM36/MCS19",
    "../UOBM/UOBM36/MCS20",
    "../UOBM/UOBM36/MCS21",
    "../UOBM/UOBM36/MCS22",
    "../UOBM/UOBM36/MCS23",
    "../UOBM/UOBM36/MCS24",
    "../UOBM/UOBM36/MCS25",
    "../UOBM/UOBM36/MCS26",
    "../UOBM/UOBM36/MCS27",
    "../UOBM/UOBM36/MCS28",
    "../UOBM/UOBM36/MCS29",
    "../UOBM/UOBM36/MCS30",
    "../UOBM/UOBM36/MCS31",
    "../UOBM/UOBM36/MCS32",
    "../UOBM/UOBM36/MCS33",
    "../UOBM/UOBM36/MCS34",
    "../UOBM/UOBM36/MCS35",
    "../UOBM/UOBM36/MCS36",
    "../UOBM/UOBM36/MCS37",
    "../UOBM/UOBM36/MCS38",
    "../UOBM/UOBM36/MCS39",
    "../UOBM/UOBM36/MCS40"
]

Kset = set()
for path in paths:
    with open(path) as f:
        K = f.read().split("\n\n")
        for axiom in K:
            Kset.add(axiom)
        f.close()

K = list(Kset)
filename = '../oriData/UOBM36allAxioms.txt'
with open (filename,'w') as file_object:
    for axiom in K:
        file_object.write(axiom)  
        file_object.write("\n")
    file_object.close()

