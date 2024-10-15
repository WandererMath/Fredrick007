export ref="../ref_files_for_genome_viewer/genomic.gtf"
export data_folder="../bowtie_output/"



for file in "$data_folder"*; do 
    featureCounts -M -Q 20 -T 5 -t gene -g gene_id -a $ref -o $(basename $file) $file
done



#featureCounts -M -Q 20 -T 5 -t gene -g gene_id -a $ref -o $filename.txt $file