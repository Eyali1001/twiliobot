import xlrd

book = xlrd.open_workbook("example.xls")
sheet = book.sheet_by_name("DataBase")
finalmessage =""



def twilio_post(message):
	print "got it"
	for i in range(1,sheet.nrows):
		if sheet.cell(i,0).value == message:
			for j in range(1,sheet.ncols):
				global finalmessage
				if(str(sheet.cell(i,j)) == "no"):
						continue
				finalmessage += str(sheet.cell(0,j).value) + ": " + str(sheet.cell(i,j).value) + ", "
	print finalmessage
	
twilio_post(raw_input())