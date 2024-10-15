import sqlite3
import sys


def sort_1(data):
    return sorted(data, key=lambda x:x[1])

if __name__=="__main__":
    with sqlite3.connect('PROJECT.db') as CONN_REF:
        CURSOR_REF=CONN_REF.cursor()

        CURSOR_REF.execute("SELECT * FROM gene")
        genes =CURSOR_REF.fetchall() 
        genes=[[line[0], int(line[1]), int(line[2])] for line in genes]
        genes=sort_1(genes)
        

        def count_genes(seq_name):
            CURSOR_REF.execute("SELECT * FROM "+seq_name)
            seqs = CURSOR_REF.fetchall()
            seqs=[[int(j) for j in line] for line in seqs]
            seqs=sort_1(seqs)          
            counts=[0]*len(genes)


            p_gene=0
            p_seq=0
            while p_seq<len(seqs) and p_gene<len(genes):
                if seqs[p_seq][1]>=genes[p_gene][1] and seqs[p_seq][1]<=genes[p_gene][2]:
                    counts[p_gene]+=1
                    p_seq+=1
                    continue
                if seqs[p_seq][1]<genes[p_gene][1]:
                    p_seq+=1
                    continue

                if seqs[p_seq][1]>genes[p_gene][2]:
                    p_gene+=1
                    continue
                raise Exception("Forever Loop")

            with open("../gene_counts_deng/"+seq_name, "w") as f:
                for i in range(len(counts)):
                    f.write(genes[i][0]+"\t"+str(counts[i])+"\n")
        
        def get_table_names():
            CURSOR_REF.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in CURSOR_REF.fetchall()] 
        
        TABLES=get_table_names()
        TABLES.remove("gene")
        TABLES.remove("sqlite_sequence")
        print(TABLES)
        for seq in TABLES:
            print("Counting "+seq)
            count_genes(seq)
        CURSOR_REF.close()
