# rename BAT export to HNB naming conventions
# 04-SEPT-2015
# Author: Miguel Castro
# Collaborator: Patrick Nowicki

import csv
import sys
import re

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

def renamePT ( pt ):
	if pt == "Cluster DN Presence Allowed":
		pt = "STAGING_DN_PT"
	elif pt == "Cluster DN Presence Denied":
		pt = "STAGING_DN_PT"
	return pt

def renameDevPool ( devpool ):
	devpool = devpool.upper()
	devpool = devpool.replace (" ", "_")
	devpool = devpool + "_DP"
	return devpool

def renameLocation ( location ):
	location = location.upper()
	location = location.replace (" ", "_")
	location = location + "_LOC"
	return location

def renameMRGL ( mrgl ):
	mrgl = mrgl.upper()
	mrgl = mrgl.replace (" ", "_")
	return mrgl
	
def renameVMP ( vmp ):
	if vmp == "ExchangeUM":
		vmp = "HNB-Standard-VM"
	return vmp
	
def renameBLF ( blf ):
	blf = re.sub(r"(.*) Cluster DN Presence (.*)", r'\1 STAGING_DN_PT', blf)
	return blf

f = open(sys.argv[1], 'rb') # open input CSV file
try:
	reader = csv.reader(f)	# creates reader object
	rownum = 0
	outputfile = open ('phone-updated.csv', 'wb')
	a = csv.writer(outputfile)
	for row in reader:		# iterates rows from input CSV file in order
		if rownum == 0:
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
					partidx.append(header.index('Route Partition ' + str(linenum)))
					vmpidx.append(header.index('Voice Mail Profile ' + str(linenum)))
					linecssidx.append(header.index('Line CSS ' + str(linenum)))
					fwdallcssidx.append(header.index('Forward All CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward Busy Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward Busy External CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward No Answer Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward No Answer External CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward No Coverage Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward No Coverage External CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward on CTI Failure CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward Unregistered Internal CSS ' + str(linenum)))
					fwdcssidx.append(header.index('Forward Unregistered External CSS ' + str(linenum)))
				except ValueError:
					break
			## BLF-specific parameters
			blfidx = []
			for blfnum in range (1, 199):
				try:
					blfidx.append(header.index('Busy Lamp Field Directory Number ' + str(blfnum)))
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
finally:
	f.close()
	outputfile.close()