import sqlite3
import sys
import os

def get_file_paths(folder_path):
  """Gets all absolute paths of files in a given folder.

  Args:
    folder_path: The path to the folder.

  Returns:
    A list of absolute paths of files in the folder.
  """

  file_paths = []
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      file_path = os.path.join(root, file)
      file_paths.append(file_path)
  return file_paths

# Example usage:
folder_path = sys.argv[1]
PATHS = get_file_paths(folder_path)
print(PATHS)

#PATH="../bowtie_output/KFredrick007_A01_332_240807_S1-bowtie2.txt"
REF_PATH="../ref_files_for_genome_viewer/genomic.gtf"




def readData(f):
    N=10
    try:
        line= next(f)
    except StopIteration:
        return None
    
    data:list=line.split()
    if len(data)<N:
        return readData(f)
    if data[2]!="gene":
        return readData(f)

    try:
        start=int(data[3])
        end=int(data[4])
        gene_id=data[9][1:-2]
    except:
        return readData(f)
    return (gene_id, start, end)

def read_seq(f):
    N=6
    try:
        line= next(f)
    except StopIteration:
        return None
    
    data:list=line.split()
    if len(data)<N:
        return read_seq(f)
    if data[2]!="NZ_CP009273.1":
        return read_seq(f)

    try:
        start=int(data[3])
        end=start+int(data[5].split("M")[0])
    except:
        return read_seq(f)
    return (start, end)


with sqlite3.connect("PROJECT.db") as CONN:
    CURSOR=CONN.cursor()


    def get_table_names():
        CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in CURSOR.fetchall()] 

    TABLES=get_table_names()
    print(TABLES)

    def gtf():
        if "gene" in TABLES:
            return
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS gene (
                gene_id TEXT PRIMARY KEY,
                start INTEGER,
                end INTEGER
            )
        ''')


        with open(REF_PATH, "r") as f:
            while(True):
                data=readData(f)
                if data is None:
                    break
                #print(data)
                CURSOR.execute("INSERT INTO gene (gene_id, start, end) VALUES (?, ?, ?)", data)
        
        CONN.commit()

    def seq(seq_name):
        table_name=seq_name.split("/")[-1].split(".")[0].split("-")[0]
        if table_name in TABLES:
            return 
        
        CURSOR.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start INTEGER,
                end INTEGER
            )
        '''
        )

        with open(seq_name, "r") as f:
            while(True):
                data=read_seq(f)
                if data is None:
                    break
                #print(data)
                CURSOR.execute(f"INSERT INTO {table_name} (start, end) VALUES (?, ?)", data)
        
        CONN.commit()

    if __name__=="__main__":
        gtf()
        for seq_name in PATHS:
            seq(seq_name)
        CURSOR.close()