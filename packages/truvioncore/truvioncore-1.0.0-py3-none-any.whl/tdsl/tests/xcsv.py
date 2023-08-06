import csv
import os
import psutil
import pandas


def read_csv():

	# read in
	with open('qnt.csv', 'r') as csv_file:

		i = 0
		reader = csv.reader(csv_file)
		for row in reader:
			# header
			# ['QNT NUM', 'Key Code', 'Owner 1 First Name', 'Owner 1 Last Name', 'Own_CASS_Address_1',
			# 'Own_CASS_City', 'Own _CASS_State', 'Own_CASS_Zipcode', 'Own_CASS_Zip_Plus_4_Flag', 'Loan Amount 1',
			# 'QVM Value', 'Lender Name 1', 'Loan Date 1', 'LTV Curr Est Comb', 'Loan Type 1', 'QNT_ID',
			# 'Contact Cell Phone Flag', 'Contact Land Line Flag', 'Contact Email Flag', 'Owner Full Name',
			# 'Adjustable Rate Index1', 'Adjustable Rate Rider 1', 'APN', 'Assessed Improvement', 'Assessed Land',
			# 'Assessed Year', 'Assessed_Value', 'Assessor Map Ref', 'Assessor Sale BkNbr', 'Assessor Sale DocNbr',
			# 'Assessor Sale Doctyp', 'Assessor Sale PgNbr', 'Assessor Sale Price', 'Assessor Sale PriceCd',
			# 'Assessor Sale RecDate', 'Building Condition', 'Building Quality Codes', 'Building SqFt Type Ind',
			# 'BuyerIDCode1', 'BuyerVestingCode1', 'Cash Purchase 1', 'Cash Purchase 2', 'Certification Date',
			# 'Change index 1', 'City Town Mun', 'Commercial Props Owned', 'Construction Type', 'Curr Est Int Rate 1',
			# 'Curr Est Int Rate 2', 'Curr Est Int Rate 3', 'Curr Est Int Rate 4', 'Equity Credit Line 1',
			# 'Equity Credit Line 2', 'Equity Credit Line 3', 'Equity Credit Line 4', 'Equity Curr Estimated Bal',
			# 'Equity Curr Estimated Range', 'Est Monthly Interest 1', 'Est Monthly P and I 1', 'Est Monthly Principal 1',
			# 'Estimated Amount Bal 1', 'Estimated Amount Bal 2', 'FC Filing Date', 'FC Record Date', 'Financing Type 1',
			# 'Financing Type 2', 'Financing Type 3', 'Financing Type 4', 'FIPS', 'Foreclosure Status',
			# 'Interest Rate 1', 'Interest Rate 2', 'Interest Rate 3', 'Interest Rate 4', 'Lender Type 1',
			# 'Loan Recording Date 1', 'Loan Type 2', 'Loan Type 3', 'Loan Type 4', 'Loan1 Number',
			# 'Loan1 Term Month', 'Loan1 Term Year', 'Loan2 Number', 'Loan2 Term Month', 'Loan2 Term Year',
			# 'LTV Curr Estimated Range', 'Market Value Year', 'Maturity Date 1', 'Max Interest Rate 1',
			# 'Max Rate 1', 'Min Rate 1', 'Mortgage Date 2', 'Mtg Recording Data 2', 'Number of Units',
			# 'Open Lien Balance', 'Own_CASS_Address_Hygiene_Code', 'Owner Occupied Status', 'Owner Status Type',
			# 'Owner_CASS_CRRT', 'Owner_CASS_DPBC', 'Ownership_Start_Date', 'Past Book Sale', 'Past Book Transfer',
			# 'Past Distressed Sale', 'Past Distressed Transfer', 'Past Doc Nbr Sale', 'Past Doc Nbr Transfer',
			# 'Past Doc type Sale', 'Past Doc Type Transfer', 'Past Page Sale', 'Past Page Transfer',
			# 'Past Price CD Sale', 'Past Price CD Transfer', 'Past Price Sale', 'Past Price Transfer',
			# 'Past Rec Date Sale', 'Past Reco Date Sale', 'Past REO Sale', 'Past REO Transfer',
			# 'Past Sale Date Transfer', 'Phase Number', 'Prior Sales Date', 'Prop Vacant Flag',
			# 'Property Type Desc', 'Property Type Detail Tree', 'Purchase Mtg Ind 1', 'Purchase Price',
			# 'Purchase Recording Date', 'Purchase Sale Date', 'Purchase_LTV', 'Purpose of Loan 1',
			# 'Purpose of Loan 2', 'QVM Conf Score', 'QVM Value Max', 'QVM Value Min', 'QVM Value Range',
			# 'QVM Value Std Dev', 'QVM_asof_Date', 'Rate Change Frequency 1', 'Record Creation Date',
			# 'REO Deed Transfer', 'REO Purchase Sale', 'Residential Props Owned', 'Roof Construction',
			# 'Roof Cover', 'Sale Book Last Sale', 'Sale Book Last Transfer', 'Sale Doc Nbr Last Sale',
			# 'Sale Doc Type Last Sale', 'Sale Doc Type Last Transfer', 'Sale DocNbr Last Transfer',
			# 'Sale Page Last Sale', 'Sale Page Last Transfer', 'Sale Price CD last Sale', 'Sale Price Last Transfer',
			# 'Sale PriceCd Last Transfer', 'Section', 'StandAlone Refi 1', 'Step Rate Rider', 'Tax Amount',
			# 'Tax Exemption Codes', 'Tax Rate Code Area', 'Tax Year', 'TAX_ID', 'Title Company Name',
			# 'Total_Fin_History_Cnt', 'Total_Open_Lien_Balance', 'Total_Open_Lien_Count', 'Trans_asof_Date',
			# 'Transfer Recording Date', 'Transfer Sale Date', 'URN']
			print(row)
			i += 1
			if i > 1:
				# just a peek
				# ['QNT15338', '', '', 'BRYNJOLPEZ GRAND TRUST', '563 GROVE ST', 'FRAMINGHAM', 'MA', '017013720', 'Y',
				#  '600000', '949909', 'AMERICAN PACIFIC MORTGAGE CORP', '20190207', '61.4754', 'N', '20046744', '', '', '',
				#  'BRYNJOLPEZ GRAND TRUST', '', '', '041-092-015', '295800', '469200', '2020', '765000', '', '', '', '', '',
				#  '0.00', '', '', '', '', 'L', 'TR', 'AV', '0', '', '07012020', '', '', '0', '', '4.62', '', '', '', '0', '',
				#  '', '', '365949', '08', '2251.45', '3083.04', '831.59', '583960', '', '', '', 'FXO', '', '', '', '06083',
				#  '', '4.62', '', '', '', 'M', '20190222', '', '', '', '', '360', '30', '', '', '', '04', '', '20490301', '',
				#  '', '', '', '', '0', '', 'A', 'N', 'T', 'C040', '630', '20190207', '', '', '', '0', '', '2019-0002490', '',
				#  'IT', '', '', '', 'T', '', '0', '20190122', '', '', '0', '20120222', '', '', 'N', 'R', 'R1001', '1',
				#  '750000', '20190222', '20190207', '80.0000', '15', '', '92', '1030362', '869455', '19', '8', '20201104',
				#  '', '20201109', '0', '0', '1', '', '', '', '', '2019-0007042', 'GD', 'GD', '2019-0007042', '', '', 'R',
				#  '750000', 'R', '', '0', '', '8129.60', '', '2-001', '2020', '', 'FIRST AMERICAN TITLE CO', '1', '583960',
				#  '1', '20201102', '20190222', '20190207', '20046744']

				# lots of null strs!
				break


def write_csv():

	# write out
	row = ['David', 'MCE', '3', '7.8']
	row1 = ['Lisa', 'PIE', '3', '9.1']
	row2 = ['Raymond', 'ECE', '2', '8.5']

	with open('output_test.csv', 'a') as csv_file:

		writer = csv.writer(csv_file)
		writer.writerow(row)
		writer.writerow(row1)
		writer.writerow(row2)


def read_pandas():

	# using pandas, and chunks

	# check avail mem
	svmem = psutil.virtual_memory()
	print(svmem.available)

	# check size of file
	filesz = os.path.getsize('qnt.csv')
	print(f'filesz {filesz}')

	df_sample = pandas.read_csv('qnt.csv', nrows=10, low_memory=False)
	df_sample_size = df_sample.memory_usage(index=True).sum()

	# define a chunksize that would occupy a maximum of 1Gb
	# we divide by 10 because we have selected 10 lines in our df_sample
	# we then get the integer part of the result
	my_chunk = (1000000000 / df_sample_size)/10
	my_chunk = int(my_chunk//1)

	print(f'my chunk {my_chunk}')

	# create the iterator
	# lazy!! using low_memory=False.. fix by defining field types
	iter_csv = pandas.read_csv(
		'qnt.csv',
		iterator=True,
		chunksize=my_chunk,
		low_memory=False)

	ii = 0
	for chunk in iter_csv:

		print(f'Loop: {ii} - QNT NUM {chunk["QNT NUM"]} Own_CASS_Address_1 {chunk["Own_CASS_Address_1"]}')
		ii += 1

		print(f'Single row QNT {chunk["QNT NUM"][0]} Own_CASS_Andress_1 {chunk["Own_CASS_Address_1"][0]}')
		exit()

	# concatenate according to a filter to our result dataframe
	df_result = pandas.concat([chunk[chunk['QNT NUM']>10] for chunk in iter_csv])

	# read the whole thing, all be damned.
	# result = pandas.read_csv('qnt.csv', low_memory=False)
	# print(result)


def write_pandas():

	# write some data using pandas
	C = {'Programming language': ['Python', 'Java', 'C++'],
			'Designed by': ['Guido van Rossum', 'James Gosling', 'Bjarne Stroustrup'],
			'Appeared': ['1991', '1995', '1985'],
			'Extension': ['.py', '.java', '.cpp'],
		}

	df = pandas.DataFrame(C, columns=['Programming language', 'Designed by', 'Appeared', 'Extension'])
	export_csv = df.to_csv(r'program_lang.csv', index=None, header=True)

	print(f'exported {export_csv}')


if __name__ == '__main__':

	read_pandas()