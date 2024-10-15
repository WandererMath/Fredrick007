import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import sys

PATH_AB="../gene_counts_feature/A-vs-B.csv"
PATH_AC="../gene_counts_feature/A-vs-C.csv"
threshold=float(sys.argv[1])

def analysis(path):
    up=[]
    down=[]
    data=pd.read_csv(path)
    #print(data.head())
    #print(data["Unnamed: 0"][:5])
    #print(type(data["log2FoldChange"][2]))
    for i in range(len(data["Unnamed: 0"])):
        if data["log2FoldChange"][i]>=threshold and data["pvalue"][i]<=0.05 :
            gene=data["Unnamed: 0"][i]
            up.append(gene)
        if data["log2FoldChange"][i]<=-threshold and data["pvalue"][i]<=0.05 :
            gene=data["Unnamed: 0"][i]
            down.append(gene)
    return up, down


B_p, B_m=analysis(PATH_AB)
C_p, C_m=analysis(PATH_AC)
#print(B_p, "\n",B_m)
venn2([set(B_p), set(C_m)],("B_upregulated", "C_downregulated"))
plt.plot()
plt.savefig("venn1.png")
plt.cla()

venn2([set(B_m), set(C_p)],("B_downregulated", "C_upregulated"))
plt.plot()
plt.savefig("venn2.png")
plt.cla()


def save(genes, path):
    with open (path, "w") as f:
        for gene in genes:
            f.write(gene+"\n")

genes=[B_p, B_m, C_p, C_m]
paths=["B_p.txt", "B_m.txt", "C_p.txt", "C_m.txt"]

for gene, path in zip(genes, paths):
    save(gene, path)