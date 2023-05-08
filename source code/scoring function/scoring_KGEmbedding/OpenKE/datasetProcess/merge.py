paths = [
    "./BioMCS/BioMCS1.txt",
    "./BioMCS/BioMCS2.txt",
    "./BioMCS/BioMCS3.txt",
    "./BioMCS/BioMCS4.txt",
    "./BioMCS/BioMCS5.txt",
    "./BioMCS/BioMCS6.txt",
    "./BioMCS/BioMCS7.txt",
    "./BioMCS/BioMCS8.txt",
    "./BioMCS/BioMCS9.txt",
    "./BioMCS/BioMCS10.txt",
    "./BioMCS/BioMCS11.txt",
    "./BioMCS/BioMCS12.txt",
    "./BioMCS/BioMCS13.txt",
    "./BioMCS/BioMCS14.txt"
]

Kset = set()
for path in paths:
    with open(path) as f:
        K = f.read().split("\n\n")
        for axiom in K:
            Kset.add(axiom)
        f.close()

K = list(Kset)
filename = './oriData/BioMCSallAxioms.txt'
with open (filename,'w') as file_object:
    for axiom in K:
        file_object.write(axiom)  
        file_object.write("\n")
    file_object.close()

