import os

def get_files(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names

folder_path = "../gene_counts_deng"
file_names = get_files(folder_path)
print(file_names)

AvsC=False
if AvsC:
    fw=open(folder_path+"/genecount_matrix-2.csv","w")
    fw.write("GeneID,A01,A02,A03,C01,C02,C03\n")
else:
    fw=open(folder_path+"/genecount_matrix-1.csv","w")
    fw.write("GeneID,A01,A02,A03,B01,B02,B03\n")
F=[]
for file in file_names:
    if AvsC:
        if not ("KFredrick007_A" in file or "KFredrick007_C" in file):
            continue
    else:
        if not ("KFredrick007_A" in file or "KFredrick007_B" in file):
            continue
    F.append(open(file, "r"))

while True:
    try:
        counts=[]
        flag=True
        for f in F:
            line=next(f)
            if flag:
                flag=False
                counts.append(line.split()[0])
            counts.append(line.split()[-1])
        fw.write(",".join(counts)+"\n")

    except StopIteration:
        break

fw.close()
for f in F:
    f.close()