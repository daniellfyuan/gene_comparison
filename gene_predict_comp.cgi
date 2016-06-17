#!/usr/local/bin/python3


# This script will compare gene coordinates from the GenBank entry AB011549.2 with that
# of Glimmer3 predictions. The script will first record CDS data (protein ID, 5' start,
# and 3' end) values into an object, which is then stored into a list. The script will
# then go through the prediction data one by one and compare it with the Genbank values
# stored in the list. If there's no match, the script will create a new object and store
# unmatched values there (and the object is appended to the list). The overal statistics
# are printed out (info such as # of ref genes, predicted genes, 5' matches, 3' matches,
# no overlaps) before printing out the object numbers in a table. All 'None' entries are
# replaced with a dash for easier and less cluttered viewing.


import jinja2
import re

# Tells template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

# Creates environment and loads a specific template from templates dir
# In this case 'midterm.html'
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('genecomp.html')

# Used to store a list of compInfo objects, see below for definition
list = []

match_found = False

# bunch of counters for overall data displayed before the table in the HTML file
ref_gene = 0
pred_gene = 0
exact_match = 0
five_match = 0
three_match = 0
no_overlap = 0


# Using this class to store comparison information between GenBank reference and
# Glimmer3 predictions
class CompInfo():
      # set some initial attributes
      prot_id = None
      ref_five = None
      ref_three = None
      pred_id = None
      pred_five = None
      pred_three = None
      pred_five_match = None
      pred_three_match = None
      overall_match = None
      
comp_info = CompInfo()

# We start filling in the compInfo object with the genbank reference data first -
# we only need three pieces of info from this document     
for line in open("AB011549_2.gb"):
	line = line.rstrip()
	
	# Extracting gene start and end locations from the genbank reference
	if line.startswith("     CDS"):
		ref_gene += 1
		
		m = re.search("\s{5}CDS[\s]+join\([\W]?([\d]+)\.\.[\W]?[\d]+[,][\W]?[\d]+\.\.[\W]?([\d]+)\)", line)
		if m:
			comp_info.ref_five = str(m.group(1))
			comp_info.ref_three = str(m.group(2))
			
		elif re.search("\s{5}CDS[\s]+complement\([\W]?[\d]+\.\.[\W]?([\d]+)\)", line):
			n = re.search("\s{5}CDS[\s]+complement\([\W]?([\d]+)\.\.[\W]?([\d]+)\)", line)
			comp_info.ref_five = str(n.group(1))
			comp_info.ref_three = str(n.group(2))
		else:
			p = re.search("\s{5}CDS[\s]+[\W]?([\d]+)\.\.[\W]?([\d]+)", line)
			comp_info.ref_five = str(p.group(1))
			comp_info.ref_three = str(p.group(2))
	
	# If line starts with /protein_id, we store it as our prot_id value in the compInfo
	# object. Once this is saved, we append the object to the list and start a new obj
	elif re.search("[\s]+[/]{1}protein_id[.]*", line):
		q = re.search("[\s]+[/]{1}protein_id=\"([\w.]+)\"", line)
		comp_info.prot_id = q.group(1)
		
		list.append(comp_info)
		comp_info = CompInfo()
	
	# Skip all other lines
	else: continue
	
	

# Now we compare predicted values from Glimmer3 with values from Genbank. We look for
# lines of ORF entries in the Glimmer3 output file 'run1.detail'. Since the output has
# data in a table format, we can use .split() to pick out data that we want.
for line in open("run1.detail"):
	line = line.rstrip()
	cols = line.split()
	
	# The lines that we want have 16 columns, anything not 16 cols that we ignore
	if len(cols) != 16: continue
	
	# We're looking for predictions on the positive strand, any negative strands ignored.
	# GenBank file doesn't have any reverse strand data.
	if cols[1].startswith("-"): continue
	
	pred_gene += 1
	
	# Iterate through the list of objects to see if the 5' or 3' ref and predicted
	# coordinates match. If so, add predicted values to the object. If not, append new
	# object to list after assigning unmatched values to the new object.
	for item in list:
		
		if item.ref_five == None:
			continue
		elif int(item.ref_five) == int(cols[3]):
			
			item.pred_five = cols[3]
			item.pred_three = cols[4]
			item.pred_id = cols[0]
			item.pred_five_match = "Agree"
			
			# 5' and 3' numbers match
			if int(item.ref_three) == int(cols[4]):
				item.pred_three_match = "Agree"
				item.overall_match = "Exact Match"
				exact_match += 1
				match_found = True
				break
			
			# Only 5' numbers match
			else:
				item.pred_three_match = "Disagree"
				item.overall_match = "5' Match"
				five_match += 1
				match_found = True
				break
		
		# Only 3' numbers match
		elif int(item.ref_three) == int(cols[4]):
			item.pred_three_match = "Agree"
			item.pred_five_match = "Disagree"
			item.overall_match = "3' Match"
			item.pred_three = cols[4]
			item.pred_five = cols[3]
			item.pred_id = cols[0]
			three_match += 1
			match_found = True
			break
	
	if match_found:
		match_found = False
		continue
			
	# No matches, make new object and add values. Keep in mind these are prediction
	# values that didn't match with the ref values.	
	comp_info = CompInfo()
	comp_info.pred_id = cols[0]
	comp_info.pred_five = cols[3]
	comp_info.pred_three = cols[4]
	comp_info.pred_five_match = "Disagree"
	comp_info.pred_three_match = "Disagree"
	comp_info.overall_match = "No Overlap"
	no_overlap += 1
	list.append(comp_info)


# Just going thru the list to make all None types become a dash.
# Easier on the eyes when looking at the table in output HTML file.
for item in list:
	if item.prot_id == None:
		item.prot_id = "-"
	if item.ref_five == None:
		item.ref_five = "-"
	if item.ref_three == None:
		item.ref_three = "-"	
	if item.pred_id == None:
		item.pred_id = "-"
	if item.pred_five == None:
		item.pred_five = "-"
	if item.pred_three == None:
		item.pred_three = "-"
	if item.pred_five_match == None:
		item.pred_five_match = "-"
	if item.pred_three_match == None:
		item.pred_three_match = "-"
	# Only one not empty string...if none then that means No Overlap!
	if item.overall_match == None:
		item.overall_match = "No Overlap"

	
# Required for CGI to work		
print("Content-Type: text/html\n\n")
print(template.render(refGene=ref_gene, predGene=pred_gene, exactMatch=exact_match, fiveMatch=five_match, threeMatch=three_match, noOverlap=no_overlap, list=list))
		
