import csv
import os, sys
import io
from optparse import OptionParser
import psutil
import uuid
import datetime, time
import random
import string
from mako.template import Template
import collections
import decimal
import gzip
import zipfile
import itertools
import traceback
import multiprocessing
import logging
import json
import mako
import redis
import sqlalchemy
from sqlalchemy.sql import expression as sa_exp
from sqlalchemy.schema import CreateTable
import sqlparse
from tdsl import dinj
from tdsl import sql as dsl_sql
from tdsl.express import STATES_ABV

def parse_args(args=None):
	'''
		Example: -c "config.yaml" < --test >
	'''
	usage = "usage: %prog [options] arg"
	parser = OptionParser()

	parser.add_option(
		"-c", dest="CONFIG",
		help="Absolute path to main dependency injection file")

	(options, args) = parser.parse_args()
	if len(args) > 1:
		parser.error("incorrect number of arguments.")
		sys.exit(0)
	return options

OPTS = parse_args()
runtime = dinj.Runtime(opts=OPTS)

import tdsl
from tdsl import *
from tdsl.codify import *
from tdsl.processes import *

from tdsl.orm import *
from tdsl.server.api import *

# can safely import models after runtime
from Kasayama import domain as models
from Kasayama import mixes
from Kasayama.recordtypes.quantarium import *
from Kasayama.feeds import *
from Kasayama.feeds.input.quantarium_ftp import QuantariumFTP


print(f'. loaded models {models}')


@memoize_exp(expiration=5)
def lut_fctry(model, session=None):
	return LutValues(model=model, session=session)


def get_session():
	return SQLAlchemySessionFactory().Session


def load_session_factory():
	# global models
	model_list = [v for k, v in models.__dict__.items() if k in models.__all__]
	SQLAlchemySessionFactory(
		base=models.Base if 'Base' in models.__dict__ else None,
		reflbase=models.ReflBase if 'ReflBase' in models.__dict__ else None,
		create_all=False,
		reflect=True,
		models=model_list,
		models_module=models,
		max_overflow=runtime.CONFIG.Resources.ORM.MaxOverflow,
		pool_size=runtime.CONFIG.Resources.ORM.PoolSize,
		echo=True, #runtime.CONFIG.Resources.ORM.Echo,
		convert_unicode=runtime.CONFIG.Resources.ORM.ConvertUnicode,
		user=runtime.CONFIG.Resources.Database.User,
		psswd=runtime.CONFIG.Resources.Database.Password,
		host=runtime.CONFIG.Resources.Database.Host,
		port=runtime.CONFIG.Resources.Database.Port,
		db=runtime.CONFIG.Resources.Database.Schema)



if __name__ == '__main__':

	load_session_factory()
	print(f'. session loaded.')

	engine = SQLAlchemySessionFactory().Engine
	session = SQLAlchemySessionFactory().Session

	r_srv = redis.Redis() # local

	cslu = None
	loan_t_lu = None
	sdv_t_lu = None
	C, PL, PLWS, PLxC, PLxC2021Q3Q4 = ~models.Campaign, ~models.PropertyLoan, \
		~models.PropertyLoanWorkSet, ~models.PropertyLoanXCampaign,  ~models.PropertyLoanXCampaignBk2021Q3Q4

	cslu = lut_fctry(models.CampaignStatusLookup, session=session)
	loan_t_lu =  lut_fctry(models.LoanTypeLookup, session=session)
	sdv_t_lu =  lut_fctry(models.SourceDataVendorTypeLookup, session=session)

	c = session.query(C).filter(C.id==1340).first()
	if not c:
		raise ('Campaign does not exist')

	pLs = (session.query(
			PLxC.id,
			PLxC.campaign_id,
			PL.first_name.label('Owner_1_First_Name'),
			PL.last_name.label('Owner_1_Last_Name'),
			PL.own_cass_address_1,
			PL.own_cass_city,
			PL.own_cass_state,
			PL.own_cass_zipcode,
			PL.loan_amount_1,
			PL.original_date_of_contract.label('Loan_Date_1'),
			PL.lender_name_1,
			PL.curr_est_int_rate,
			PL.curr_est_bal.label('Estimated_Amount_Bal_1'),
			PL.source_vendor_id.label('source_vendor_id_label'),
			PL.id.label('etfdata_pl_id'),
			PL.note,
			PL.source_data_vendor_type_id,
			PL.phone_number,
			PL.email_address,
			PL.loan_type_id,
			PL.guid_matrix,
			PL.annotations,
			PLxC.banker_note,
			PLxC.sequence
		)
		.join(
			PLxC, PL.id == PLxC.property_loan_id
		)
		.join(
			C, PLxC.campaign_id == C.id
		)
		.filter(
			PLxC.campaign_id==1340,
			PL.is_suppressed==False
		)
		.order_by(PLxC.property_loan_id.desc()
		)).all()

	print(pLs[0])
	print('  ')
	print(dir(pLs[0]))

	campaign_key = 'campaign_key:' + pLs[0].sequence.split('-')[0]

	for row in pLs:

		# stop doing this and null in a different way
		# so we can use dot completion.
		row = [r or "" for r in row]

		sdv_display_name = sdv_t_lu.get_display_name(row[16]) if row[16] else 'NA'
		if sdv_t_lu.get_display_name(row[16]).lower() == 'boss':
			sdv_display_name = 'I-DATA'

		owner_id, lead_source, lead_id = 'NA', 'NA', 'NA'

		rec = dict(
				Artwork_Note=c.artwork_note,
				Phone_Number=c.phone_number,
				Sequence=row[23],
				Owner_1_First_Name=row[2],
				Owner_1_Last_Name=row[3],
				Company=row[3] +'.'+ row[2],
				Own_CASS_Address_1=row[4],
				Own_CASS_City=row[5],
				Own_CASS_State=row[6],
				Own_CASS_Zipcode=row[7],
				Own_Phone_Number=row[17],
				Own_Email_Address=row[18].lower() if row[18] else None,
				Loan_Amount_1=row[8],
				Loan_Date_1=row[9],
				Lender_name_1=row[10],
				Curr_Est_Int_Rate=float(row[11]) if row[11] else 'NA',
				Curr_Est_Balance=row[12],
				Source_Vendor_Id=row[13],
				SourceNote=c.note,
				Channel_Note='X',
				ETF_PLXC_ID=row[0],
				ETF_C_ID=row[1],
				ETF_PL_ID=row[14],
				Note=c.note,
				Source_Data_Vendor_Type=sdv_display_name.upper(),
				Loan_Type=loan_t_lu.get_name(row[19]) if row[19] else 'NA',
				WebLead_note=row[22],
				Matched_OwnerId=owner_id if owner_id else 'NA',
				Matched_LeadSource=lead_source if lead_source else 'NA',
				Matched_LeadId=lead_id if lead_id else 'NA'
				)

		r_srv.set(f'sequence:{row[23]}', json.dumps(rec))
		r_srv.sadd(campaign_key, row[23])

	print('done.')








