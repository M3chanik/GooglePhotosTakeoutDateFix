# Fixes modification date on Google Photos takeout exports.
# Reads the photo-taken date from the Takeout JSON file and updates the file of the same name
#
# by Brian Lang

import os
import json
from datetime import datetime, timezone

path = './'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
	for file in f:
		if ('.json' in file) and ('metadata' not in file):
			files.append(os.path.join(r, file))

for f in files:
	print(f)
	with open(f) as inputfile:
		metadatajson = json.loads(inputfile.read())
		phototakentime = metadatajson['photoTakenTime']
		formatteddate = phototakentime['formatted']
		month = (formatteddate.split(' '))[0]
		if month == 'Jan':
			month = 1
		elif month == 'Feb':
			month = 2
		elif month == 'Mar':
			month = 3
		elif month == 'Apr':
			month = 4
		elif month == 'May':
			month = 5
		elif month == 'Jun':
			month = 6
		elif month == 'Jul':
			month = 7
		elif month == 'Aug':
			month = 8
		elif month == 'Sep':
			month = 9
		elif month == 'Oct':
			month = 10
		elif month == 'Nov':
			month = 11
		elif month == 'Dec':
			month = 12
		day = (formatteddate.split(' '))[1]
		day = int(day[:len(day) - 1])
		year = (formatteddate.split(' '))[2]
		year = int(year[:len(year) - 1])
		time = (formatteddate.split(' '))[3]
		hour = int((time.split(':'))[0])
		minute = int((time.split(':'))[1])
		sec = int((time.split(':'))[2])
		ampm = (formatteddate.split(' '))[4]


		# This is a kludge, I don't care about the exact hour these photos were taken, but if you do, you'll need to recode this section.
		if ampm == 'PM':
			if hour == 12:
				hour += 11
			else:
				hour += 12

		print(formatteddate)
		utcdate = datetime(year, month, day, hour, minute, sec, tzinfo=timezone.utc)
		print(utcdate)
		pstdate = utcdate.astimezone(tz=None)
		print(pstdate)
		pstdateinNS = pstdate.timestamp()
		print(pstdateinNS)

		jpgfile = f[:len(f)-5]
		print(jpgfile)
		os.utime(jpgfile, (pstdateinNS, pstdateinNS))
