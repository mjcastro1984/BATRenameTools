# rename BAT Phones export to new naming conventions
# 04-SEPT-2015
# Author: Miguel Castro
# Collaborator: Patrick Nowicki

import csv
import sys
import re

print "Renaming objects in BAT Phones export"

## the following functions complete individual rename tasks for the specific
## object referenced

# rename Calling Search Spaces
def renameCSS ( css ):
	if css == '':
		css = ''
		return css
	else:
		css = css.replace (" ", "_")
		css = css.upper()
		css = css + "_CSS"
		css = css[:50]
		return css

# rename Partitions
def renamePT ( pt ):
	if pt == "Cluster DN Presence Allowed":
		pt = "STAGING_DN_PT"
	elif pt == "Cluster DN Presence Denied":
		pt = "STAGING_DN_PT"
	return pt

# rename Device Pools
def renameDevPool ( devpool ):
	devpool = devpool.upper()
	devpool = devpool.replace (" ", "_")
	devpool = devpool + "_DP"
	return devpool

# rename Locations
def renameLocation ( location ):
	location = location.upper()
	location = location.replace (" ", "_")
	location = location + "_LOC"
	return location

# rename MRGLs
def renameMRGL ( mrgl ):
	mrgl = mrgl.upper()
	mrgl = mrgl.replace (" ", "_")
	return mrgl

# rename Voice Mail Profiles
def renameVMP ( vmp ):
	if vmp == "ExchangeUM":
		vmp = "HNB-Standard-VM"
	return vmp

# modify BLF Directory Number field Partition references
def renameBLF ( blf ):
	blf = re.sub(r"(.*) Cluster DN Presence (.*)", r'\1 STAGING_DN_PT', blf)
	return blf

# open file based on parameters passed on script execution
print "Opening input file"
f = open(sys.argv[1], 'rb') # open input CSV file
try:
	reader = csv.reader(f)	# creates reader object
	rownum = 0
	outputfilename = 'phone-updated.csv'
	outputfile = open ( outputfilename, 'wb')	# creates writer object
	print "Output file is %s" % outputfilename
	a = csv.writer(outputfile)
	## iterate rows in order
	for row in reader:
		# the if statements check whether working on first row; if first row,
		# it gets treated as a header and built appropriately; other rows are
		# built as "records"
		if rownum == 0:
			# when row number is 0, this row is built as the header
			header = row
			partidx = []
			vmpidx = []
			linecssidx 	= []
			fwdallcssidx = []
			fwdcssidx = []
			devicepoolidx = header.index('Device Pool')
			mrglidx = header.index('Media Resource Group List')
			devicecssidx = header.index('CSS')
			deviceaarcssidx = header.index('AAR CSS')
			locationidx = header.index('Location')
			cssrerouteidx = header.index('CSS Reroute')
			subscribecssidx = header.index('Device Subscribe CSS')
			# Line-specific parameters
			for linenum in range(1, 50):
				try:
					partidx.append(header.index(
						'Route Partition ' + str(linenum)))
					vmpidx.append(header.index(
						'Voice Mail Profile ' + str(linenum)))
					linecssidx.append(header.index(
						'Line CSS ' + str(linenum)))
					fwdallcssidx.append(header.index(
						'Forward All CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward Busy Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward Busy External CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward No Answer Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward No Answer External CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward No Coverage Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward No Coverage External CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward on CTI Failure CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward Unregistered Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index(
						'Forward Unregistered External CSS ' + str(linenum)))
				except ValueError:
					break
			## BLF-specific parameters
			blfidx = []
			for blfnum in range (1, 199):
				try:
					blfidx.append(header.index(
						'Busy Lamp Field Directory Number ' + str(blfnum)))
				except ValueError:
					break
			## remove the following fields which will not work in 10.5
			### User ID x
			removeidx = []
			for useridnum in range(1, 10):
				try:
					removeidx.append(header.index('User ID ' + str(useridnum)))
				except ValueError:
					break
			for userid in range (1,10):
				try:
					header.remove('User ID ' + str(userid))
				except ValueError:
					break
			a.writerows([header])
		else:
			# for all other rows, process each column as per indexes created
			# in header step
			colnum = 0
			phone = []
			for col in row:
				if colnum not in removeidx:
					if colnum == devicepoolidx:
						col = renameDevPool(col)
					elif colnum == mrglidx:
						col = renameMRGL(col)
					elif colnum == locationidx:
						col = renameLocation(col)
					elif colnum == devicecssidx:
						col = renameCSS(col)
					elif colnum == deviceaarcssidx:
						col = renameCSS(col)
					elif colnum == cssrerouteidx:
						col = renameCSS(col)
					elif colnum == subscribecssidx:
						col = renameCSS(col)
					elif colnum in partidx:
						col = renamePT(col)
					elif colnum in vmpidx:
						col = renameVMP(col)
					elif colnum in linecssidx:
						col = renameCSS(col)
					elif colnum in fwdallcssidx:
						col = renameCSS(col)
					elif colnum in fwdcssidx:
						col = renameCSS(col)
					elif colnum in blfidx:
						col = renameBLF(col)
					phone.append(col)
				colnum += 1
			a.writerows([phone])
		rownum += 1
# end of script
finally:
	f.close()	# close the input file
	outputfile.close()	# close the output file
