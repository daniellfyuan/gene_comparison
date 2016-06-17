# gene_comparison
Comparing genbank genes with that from Glimmer3 (gene prediction software) for E. coli accession AB011549.2

This project directory has a directory called "Template", which is where genecomp.html is stored. The CGI file "gene_predict_comp.cgi" is found outside of the Template directory. The genbank file "AB011549_2.gb" is extracted from NCBI and is located where the CGI file is. The Glimmer3 result "run1.detail" is also with the CGI and genbank files.

I did not include the genbank file in this repository, however, it is accessible by searching the NCBI database for accession AB011549.2.

This script will compare gene coordinates from the GenBank entry AB011549.2 with that
of Glimmer3 predictions. The script will first record CDS data (protein ID, 5' start,
and 3' end) values into an object, which is then stored into a list. The script will
then go through the prediction data one by one and compare it with the Genbank values
stored in the list. If there's no match, the script will create a new object and store
unmatched values there (and the object is appended to the list). The overal statistics
are printed out (info such as # of ref genes, predicted genes, 5' matches, 3' matches,
no overlaps) before printing out the object numbers in a table. All 'None' entries are
replaced with a dash for easier and less cluttered viewing.

The file "test.html" is the output of the script, after it parsed and analyzed both the genbank file and the Glimmer3 output file.
