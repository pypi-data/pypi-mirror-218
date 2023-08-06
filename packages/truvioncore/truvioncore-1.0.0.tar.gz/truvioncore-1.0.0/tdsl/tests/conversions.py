import sys, os
from mako.template import Template
from tdsl.orm import create_default_tablename, create_default_classname_from_tablename
from tdsl.express import singularize
import pprint


__here__ = os.path.abspath(os.path.dirname(__file__))


# el = ['QNT NUM', 'Key Code', 'Owner 1 First Name', 'Owner 1 Last Name', 'Own_CASS_Address_1', 'Own_CASS_City', 'Own _CASS_State', 'Own_CASS_Zipcode', 'Own_CASS_Zip_Plus_4_Flag', 'Loan Amount 1', 'QVM Value', 'Lender Name 1', 'Loan Date 1', 'LTV Curr Est Comb', 'Loan Type 1', 'QNT_ID', 'Contact Cell Phone Flag', 'Contact Land Line Flag', 'Contact Email Flag', 'Owner Full Name', 'Adjustable Rate Index1', 'Adjustable Rate Rider 1', 'APN', 'Assessed Improvement', 'Assessed Land', 'Assessed Year', 'Assessed_Value', 'Assessor Map Ref', 'Assessor Sale BkNbr', 'Assessor Sale DocNbr', 'Assessor Sale Doctyp', 'Assessor Sale PgNbr', 'Assessor Sale Price', 'Assessor Sale PriceCd', 'Assessor Sale RecDate', 'Building Condition', 'Building Quality Codes', 'Building SqFt Type Ind', 'BuyerIDCode1', 'BuyerVestingCode1', 'Cash Purchase 1', 'Cash Purchase 2', 'Certification Date', 'Change index 1', 'City Town Mun', 'Commercial Props Owned', 'Construction Type', 'Curr Est Int Rate 1', 'Curr Est Int Rate 2', 'Curr Est Int Rate 3', 'Curr Est Int Rate 4', 'Equity Credit Line 1', 'Equity Credit Line 2', 'Equity Credit Line 3', 'Equity Credit Line 4', 'Equity Curr Estimated Bal', 'Equity Curr Estimated Range', 'Est Monthly Interest 1', 'Est Monthly P and I 1', 'Est Monthly Principal 1', 'Estimated Amount Bal 1', 'Estimated Amount Bal 2', 'FC Filing Date', 'FC Record Date', 'Financing Type 1', 'Financing Type 2', 'Financing Type 3', 'Financing Type 4', 'FIPS', 'Foreclosure Status', 'Interest Rate 1', 'Interest Rate 2', 'Interest Rate 3', 'Interest Rate 4', 'Lender Type 1', 'Loan Recording Date 1', 'Loan Type 2', 'Loan Type 3', 'Loan Type 4', 'Loan1 Number', 'Loan1 Term Month', 'Loan1 Term Year', 'Loan2 Number', 'Loan2 Term Month', 'Loan2 Term Year', 'LTV Curr Estimated Range', 'Market Value Year', 'Maturity Date 1', 'Max Interest Rate 1', 'Max Rate 1', 'Min Rate 1', 'Mortgage Date 2', 'Mtg Recording Data 2', 'Number of Units', 'Open Lien Balance', 'Own_CASS_Address_Hygiene_Code', 'Owner Occupied Status', 'Owner Status Type', 'Owner_CASS_CRRT', 'Owner_CASS_DPBC', 'Ownership_Start_Date', 'Past Book Sale', 'Past Book Transfer', 'Past Distressed Sale', 'Past Distressed Transfer', 'Past Doc Nbr Sale', 'Past Doc Nbr Transfer', 'Past Doc type Sale', 'Past Doc Type Transfer', 'Past Page Sale', 'Past Page Transfer', 'Past Price CD Sale', 'Past Price CD Transfer', 'Past Price Sale', 'Past Price Transfer', 'Past Rec Date Sale', 'Past Reco Date Sale', 'Past REO Sale', 'Past REO Transfer', 'Past Sale Date Transfer', 'Phase Number', 'Prior Sales Date', 'Prop Vacant Flag', 'Property Type Desc', 'Property Type Detail Tree', 'Purchase Mtg Ind 1', 'Purchase Price', 'Purchase Recording Date', 'Purchase Sale Date', 'Purchase_LTV', 'Purpose of Loan 1', 'Purpose of Loan 2', 'QVM Conf Score', 'QVM Value Max', 'QVM Value Min', 'QVM Value Range', 'QVM Value Std Dev', 'QVM_asof_Date', 'Rate Change Frequency 1', 'Record Creation Date', 'REO Deed Transfer', 'REO Purchase Sale', 'Residential Props Owned', 'Roof Construction', 'Roof Cover', 'Sale Book Last Sale', 'Sale Book Last Transfer', 'Sale Doc Nbr Last Sale', 'Sale Doc Type Last Sale', 'Sale Doc Type Last Transfer', 'Sale DocNbr Last Transfer', 'Sale Page Last Sale', 'Sale Page Last Transfer', 'Sale Price CD last Sale', 'Sale Price Last Transfer', 'Sale PriceCd Last Transfer', 'Section', 'StandAlone Refi 1', 'Step Rate Rider', 'Tax Amount', 'Tax Exemption Codes', 'Tax Rate Code Area', 'Tax Year', 'TAX_ID', 'Title Company Name', 'Total_Fin_History_Cnt', 'Total_Open_Lien_Balance', 'Total_Open_Lien_Count', 'Trans_asof_Date', 'Transfer Recording Date', 'Transfer Sale Date', 'URN']
#
# lu = {}
#
# for e in el:
# 	attr_name = e.replace(' ', '_').lower()
# 	lu[attr_name] = f'{attr_name}: Column(String)'
# #pprint.pprint(lu)
#
# for k,v in lu.items():
# 	print(k, v)

# lookup tables conversion
#
#


own_cass_zip_plus_4_flag_lu = '''Own_CASS_Zip_Plus_4_Flag                                              
N                             Zip 4 Not Present                       
Y                             Zip 4 Present '''


loan_type_1_lu = '''Loan Type 1                                                           
1                             Stand Alone First                       
2                             Stand Alone Second                      
3                             ARM (Adjustable Rate Mortgage as of Augu
4                             Amount keyed is an Aggregate amount     
5                             USDA                                    
6                             Closed-end Mortgage                     
7                             Non Purchase Money Mortgage             
8                             SBA Participation Trust Deed            
#                             TBD                                     
A                             Assumption                              
B                             Building or Construction Loan           
C                             Cash                                    
D                             2nd Mortgage made to cover Down Payment 
E                             Credit Line (Revolving)                 
F                             FHA                                     
G                             Fannie Mae/Freddie Mac (Phased out becau
H                             Balloon                                 
I                             Farmers Home Administration             
J                             Negative Amortization                   
K                             Loan Amount $1-9 billion - only first 9-
L                             Land Contract (Argmt. Of Sale)          
M                             Modification - Originally designated to 
N                             New Conventional                        
O                             Commercial                              
P                             Purchase Money Mortgage                 
Q                             Undefined / Multiple Amounts            
R                             Stand Alone Refi (Refinance of Original 
S                             Seller take-back                        
T                             Loan Amount $10-99 billion - only first 
U                             Unknown (DEFAULT)                       
V                             VA                                      
W                             Future Advance Clause / Open End Mortgag
X                             Trade                                   
Y                             State Veterans                          
Z                             Reverse Mortgage (Home Equity Conversion'''


contact_cell_phone_flag_lu = '''Contact Cell Phone Flag                                               
I                             Individual Match                        
H                             Household Match '''


contact_land_line_flag_lu = '''Contact Land Line Flag                                                
I                             Individual Match                        
H                             Household Match'''


contact_email_flag_lu = '''Contact Email Flag                                                    
I                             Individual Match                        
H                             Household Match'''


adjustment_rate_index1_lu = '''Adjustable Rate Index1                                                
11THDISTRICT                  11th District                           
12MTA                         Twelve Month Average                    
1YRCMT                        1-Year Constant Maturity Treasury Index 
3YRCMT                        3-Year Constant Maturity Treasury Index 
5YRCMT                        5-Year Constant Maturity Treasury Index 
6MOCD                         6 Month CD                              
6MOT-BILL                     6 Month T-Bill (includes 26 week T-Bills
COFI                          Cost of Funds                           
FIVEYEART-BILL                Five Year T-Bill                        
LIBOR                         Libor                                   
LIBOR1MO                      1 Month Libor                           
LIBOR1YR                      1 Year Libor                            
LIBOR3MO                      3 Month Libor                           
LIBOR6MO                      6 Month Libor                           
ONEYEART-BILL                 One Year T-Bill                         
OTHER                         Other (Uncommon indices)                
PRIME                         Prime                                   
TENYEART-BILL                 Ten Year T-Bill                         
THREEYEART-BILL               Three Year T-Bill'''


adjustable_rate_rider_1_lu = '''Adjustable Rate Rider 1                                               
Y                             An Adjustable Rate Rider is recorded wit'''


building_condition_lu = '''Building Condition                                                    
E                             Excellent                               
F                             Fair                                    
G                             Good                                    
P                             Poor                                    
U                             Unsound                                 
V                             Average '''


building_quality_codes_lu = '''Building Quality Codes                                                
A                             A                                       
A-                            A-                                      
A+                            A+                                      
AA                            AA                                      
B                             B                                       
B-                            B-                                      
B+                            B+                                      
C                             C                                       
C-                            C-                                      
C+                            C+                                      
D                             D                                       
D-                            D-                                      
D+                            D+                                      
E                             E                                       
E-                            E-                                      
E+                            E+                                      
F                             F                                       
F-                            F-                                      
F+                            F+                                      
S                             S '''


building_sqft_type_ind_lu = '''Building SqFt Type Ind                                                
B                             Base Area                               
E                             Heated Area                             
J                             Adjusted Area                           
K                             Finished Area                           
L                             Living Area                             
R                             Gross Area                              
T                             Total Area  '''


buyeridcode1_lu = '''BuyerIDCode1                                                          
AB                            Alternate Beneficiary                   
AC                            Guardian/Custodian                      
AD                            Administrator                           
AE                            Assignee (Buyer/Borrower only)          
AF                            Name derived from Affidavit             
AG                            Agent                                   
AK                            Also known as (A/K/A)                   
AR                            Assignor (Seller only)                  
BE                            Beneficiary / Creditor - When Doc Type B
BU                            Builder/Developer                       
CE                            Conservatee                             
CN                            Corporation                             
CO                            Company                                 
CR                            Conservator                             
DB                            Doing business as (DBA)                 
DC                            Deceased                                
DF                            Defendant                               
DP                            Domestic Partner                        
DR                            Divorced not Remarried                  
DV                            Divorced                                
DW                            Dower Clause                            
EA                            Et al (and others)                      
ES                            Estate                                  
EX                            Executor                                
FK                            Formerly known as (F/K/A)               
FL                            Family Living Trust                     
FM                            Family Trust                            
FR                            Family Revocable Trust                  
GN                            General Partnership                     
GP                            General Partner                         
GV                            Government                              
HH                            Her Husband                             
HU                            Husband and Husband                     
HW                            Husband and Wife                        
ID                            Individual(s)                           
IL                            Irrevocable Living Trust                
IN                            incompetent                             
IR                            Irrevocable Trust                       
L2                            Seller is owner on current Assessment Fi
LC                            Limited Liability Company               
LL                            Limited Liability Partnership           
LS                            Limited Partnership                     
LP                            Limited Partner                         
LT                            Life Tenant (holds a life estate interes
LV                            Living Trust                            
LW                            Last Will and Testament                 
MC                            Married Couple                          
ME                            Member                                  
MI                            Minor, Ward or Client (Represented by Tr
MM                            Married man as his sole and separate pro
MN                            Managing Member                         
MP                            Married Person                          
MW                            Married women as her sole and separate p
NK                            Now Known as                            
NM                            Never Married Person                    
NP                            Not Provided (name blurred or missing fr
NV                            Non-Vested Spouse                       
PA                            Partnership                             
PF                            Plaintiff                               
PR                            Personal Representative (Attorney in Fac
PT                            Partner                                 
RC                            Receiver                                
RL                            Revocable Living Trust                  
RT                            Revocable Trust                         
SE                            surviving Tenant by the Entirety        
SI                            Successor in interest                   
SJ                            Surviving Joint Tenant                  
SL                            Sole Proprietorship                     
SM                            Single man                              
SO                            Sole Member                             
SP                            Single Person or Individual             
SS                            Surviving Spouse                        
ST                            Successor Trustee (LA County only)      
SW                            Single woman                            
SX                            Separated                               
TR                            Trustee                                 
TS                            Trustor/Debtor (Borrower in Default/Fore
TT                            Trust                                   
UI                            Unknown                                 
UM                            Unmarried Man                           
UN                            Unmarried                               
US                            United States                           
UW                            Unmarried Woman                         
WA                            Who Acquired Title As                   
WD                            Widow or Widower                        
WH                            His Wife                                
WW                            Wife and Wife'''


buyer_vesting_code1_lu = '''BuyerVestingCode1                                                     
AK                            Also Known As (A/K/A)                   
CO                            Company/Corporation                     
CP                            Community Property                      
CT                            Contract Owner                          
DB                            Doing Business As (DBA)                 
EA                            Et al (and others)                      
ES                            Estate                                  
EU                            Et ux (and wife)                        
EX                            Executor                                
FK                            Formerly Known As (F/K/A)               
FL                            Family Living Trust                     
FM                            Family Trust                            
FR                            Family Revocable Trust                  
GV                            Government                              
HH                            Her Husband                             
HW                            Husband and Wife                        
IL                            Irrevocable Living Trust                
IR                            Irrevocable Trust                       
JS                            Joint Tenants with Right of Survivorship
JT                            Joint Tenants                           
JV                            Joint Venture                           
LE                            Life Estate                             
LT                            Life Tenant                             
LV                            Living Trust                            
MI                            Minor/Guardian                          
MM                            Married Man as His Sole & Separate Prope
MW                            Married Woman as Her Sole & Separate Pro
PA                            Partnership                             
RL                            Revocable Living Trust                  
RS                            Right of Survivorship                   
RT                            Revocable Trust                         
SM                            Single/Unmarried Man                    
SO                            Sole Owner                              
SW                            Single/Unmarried Woman                  
TC                            Tenants in Common                       
TD                            Transfer of Death                       
TE                            Tenants by Entirety                     
TN                            Tenant                                  
TR                            Trust/Trustee/Conservator               
TS                            Trustees                                
TX                            TAX PAYER                               
WD                            Widow/Widower'''


cash_purchase_1_lu = '''Cash Purchase 1
0                             No
1                             Yes'''


cash_purchase_2_lu = '''Cash Purchase 2
0                             No
1                             Yes'''


construction_type_lu = '''Construction Type
A                             Adobe
B                             Brick
C                             Concrete
D                             Concrete Block
E                             Dome
F                             Frame
M                             Log
O                             Other
P                             Masonry
Q                             Metal
R                             Steel
S                             Stone
T                             Tilt-up (pre-cast concrete)
W                             Wood
X                             Mixed'''


equity_credit_line_1_lu = '''Equity Credit Line 1
0                             No
1                             Yes'''


equity_credit_line_2_lu = '''Equity Credit Line 2
0                             No
1                             Yes'''


equity_credit_line_3_lu = '''Equity Credit Line 3
0                             No
1                             Yes'''


equity_credit_line_4_lu = '''Equity Credit Line 4
0                             No
1                             Yes'''


equity_curr_estimated_range_lu = '''Equity Curr Estimated Range
01                            1-49, 999
02                            50, 000-99, 999
03                            100, 000-149, 999
04                            150, 000-199, 999
05                            200, 000-249, 999
06                            250, 000-299, 999
07                            300, 000-349, 999
08                            350, 000-399, 999
09                            400, 000-449, 999
10                            450, 000-499, 999
11                            500, 000-549, 999
12                            550, 000-599, 999
13                            600, 000-649, 999
14                            650, 000-699, 999
15                            700, 000-749, 999
16                            750, 000-799, 999
17                            800, 000-849, 999
18                            850, 000-899, 999
19                            900, 000-949, 999
20                            950, 000-999, 999
21                            1, 000, 000-1, 249, 999
22                            1, 250, 000-1, 499, 999
23                            1, 500, 000-1, 749, 999
24                            1, 750, 000-1, 999, 999
25                            2, 000, 000-2, 249, 999
26                            2, 250, 000-2, 499, 999
27                            2, 500, 000-2, 749, 999
28                            2, 750, 000-2, 999, 999
29                            3, 000, 000-3, 249, 999
30                            3, 250, 000-3, 499, 999
31                            3, 500, 000-3, 749, 999
32                            3, 750, 000-3, 999, 999
33                            4, 000, 000-4, 249, 999
34                            4, 250, 000-4, 499, 999
35                            4, 500, 000-4, 749, 999
36                            4, 750, 000-4, 999, 999
37                            5, 000, 000+
38                            -1-49, 999
39                            -50, 000-99, 999
40                            -100, 000-149, 999
41                            -150, 000-199, 999
42                            -200, 000-249, 999
43                            -250, 000-299, 999
44                            -300, 000-349, 999
45                            -350, 000-399, 999
46                            -400, 000-449, 999
47                            -450, 000-499, 999
48                            -500, 000-549, 999
49                            -550, 000-599, 999
50                            -600, 000-649, 999
51                            -650, 000-699, 999
52                            -700, 000-749, 999
53                            -750, 000-799, 999
54                            -800, 000-849, 999
55                            -850, 000-899, 999
56                            -900, 000-949, 999
57                            -950, 000-999, 999
58                            -1, 000, 000-1, 249, 999
59                            -1, 250, 000-1, 499, 999
60                            -1, 500, 000-1, 749, 999
61                            -1, 750, 000-1, 999, 999
62                            -2, 000, 000-2, 249, 999
63                            -2, 250, 000-2, 499, 999
64                            -2, 500, 000-2, 749, 999
65                            -2, 750, 000-2, 999, 999
66                            -3, 000, 000-3, 249, 999
67                            -3, 250, 000-3, 499, 999
68                            -3, 500, 000-3, 749, 999
69                            -3, 750, 000-3, 999, 999
70                            -4, 000, 000-4, 249, 999
71                            -4, 250, 000-4, 499, 999
72                            -4, 500, 000-4, 749, 999
73                            -4, 750, 000-4, 999, 999
74                            -5, 000, 000
NF                            Not Available - No Financing
NV                            Not Avaliable - No QVM Value'''


financing_type_1_lu = '''Financing Type 1
ADJ                           Adjustable Rate
AJO                           Adjustable Rate Override
AITD                          All Inclusive Deed of Trust
FIX                           Fixed Rate
FXO                           Fixed Rate Override
MULT                          Multiple Loan Amounts
NAM                           Negatively Amortizing Loan
OTH                           Other
STP                           Step Interest Rate
UNK                           Unknown
VAR                           Variable'''


financing_type_2_lu = '''Financing Type 2
ADJ                           Adjustable Rate
AJO                           Adjustable Rate Override
AITD                          All Inclusive Deed of Trust
FIX                           Fixed Rate
FXO                           Fixed Rate Override
MULT                          Multiple Loan Amounts
NAM                           Negatively Amortizing Loan
OTH                           Other
STP                           Step Interest Rate
UNK                           Unknown
VAR                           Variable'''


financing_type_3_lu = '''Financing Type 3
ADJ                           Adjustable Rate
AJO                           Adjustable Rate Override
AITD                          All Inclusive Deed of Trust
FIX                           Fixed Rate
FXO                           Fixed Rate Override
MULT                          Multiple Loan Amounts
NAM                           Negatively Amortizing Loan
OTH                           Other
STP                           Step Interest Rate
UNK                           Unknown
VAR                           Variable'''


financing_type_4_lu = '''Financing Type 4
ADJ                           Adjustable Rate
AJO                           Adjustable Rate Override
AITD                          All Inclusive Deed of Trust
FIX                           Fixed Rate
FXO                           Fixed Rate Override
MULT                          Multiple Loan Amounts
NAM                           Negatively Amortizing Loan
OTH                           Other
STP                           Step Interest Rate
UNK                           Unknown
VAR                           Variable'''


foreclosure_status_lu = '''Foreclosure Status
0                             None
1                             Notice of Default / Pre-Foreclosure
2                             Notice of Sale / Final Judgment'''


lender_type_1_lu = '''Lender Type 1
B                             Bank
D                             Lender / Agent role undisclosed
E                             Et al ( and others)
F                             Finance Company
G                             Government (FHA, VA, etc.)
I                             Insurance
L                             Lending institution
M                             Mortgage company
N                             Not Known
O                             Other (company or corporation)
P                             Private Party (individual)
R                             REO / Foreclosure Company
S                             Seller
U                             Credit Union
W                             Internet Storefront
X                             Subprime Lender
Z                             Reverse Mortgage Lender'''


loan_type_2_lu = '''Loan Type 2
1                             Stand Alone First
2                             Stand Alone Second
3                             ARM (Adjustable Rate Mortgage as of Augu
4                             Amount keyed is an Aggregate amount
5                             USDA
6                             Closed-end Mortgage
7                             Non Purchase Money Mortgage
8                             SBA Participation Trust Deed
#                             TBD                                     
A                             Assumption
B                             Building or Construction Loan
C                             Cash
D                             2nd Mortgage made to cover Down Payment
E                             Credit Line (Revolving)
F                             FHA
G                             Fannie Mae / Freddie Mac (Phased out becau
H                             Balloon
I                             Farmers Home Administration
J                             Negative Amortization
K                             Loan Amount $1-9 billion - only first 9-
L                             Land Contract (Argmt.Of Sale)
M                             Modification - Originally designated to
N                             New Conventional
O                             Commercial
P                             Purchase Money Mortgage
Q                             Undefined / Multiple Amounts
R                             Stand Alone Refi (Refinance of Original
S                             Seller take-back
T                             Loan Amount $10-99 billion - only first
U                             Unknown (DEFAULT)
V                             VA
W                             Future Advance Clause / Open End Mortgag
X                             Trade
Y                             State Veterans
Z                             Reverse Mortgage (Home Equity Conversion'''


loan_type_3_lu = '''Loan Type 3
1                             Stand Alone First
2                             Stand Alone Second
3                             ARM (Adjustable Rate Mortgage as of Augu
4                             Amount keyed is an Aggregate amount
5                             USDA
6                             Closed-end Mortgage
7                             Non Purchase Money Mortgage
8                             SBA Participation Trust Deed
#                             TBD                                     
A                             Assumption
B                             Building or Construction Loan
C                             Cash
D                             2nd Mortgage made to cover Down Payment
E                             Credit Line (Revolving)
F                             FHA
G                             Fannie Mae / Freddie Mac (Phased out becau
H                             Balloon
I                             Farmers Home Administration
J                             Negative Amortization
K                             Loan Amount $1-9 billion - only first 9-
L                             Land Contract (Argmt.Of Sale)
M                             Modification - Originally designated to
N                             New Conventional
O                             Commercial
P                             Purchase Money Mortgage
Q                             Undefined / Multiple Amounts
R                             Stand Alone Refi (Refinance of Original
S                             Seller take-back
T                             Loan Amount $10-99 billion - only first
U                             Unknown (DEFAULT)
V                             VA
W                             Future Advance Clause / Open End Mortgag
X                             Trade
Y                             State Veterans
Z                             Reverse Mortgage (Home Equity Conversion'''


loan_type_4_lu = '''Loan Type 4
1                             Stand Alone First
2                             Stand Alone Second
3                             ARM (Adjustable Rate Mortgage as of Augu
4                             Amount keyed is an Aggregate amount
5                             USDA
6                             Closed-end Mortgage
7                             Non Purchase Money Mortgage
8                             SBA Participation Trust Deed
#                             TBD                                     
A                             Assumption
B                             Building or Construction Loan
C                             Cash
D                             2nd Mortgage made to cover Down Payment
E                             Credit Line (Revolving)
F                             FHA
G                             Fannie Mae / Freddie Mac (Phased out becau
H                             Balloon
I                             Farmers Home Administration
J                             Negative Amortization
K                             Loan Amount $1-9 billion - only first 9-
L                             Land Contract (Argmt.Of Sale)
M                             Modification - Originally designated to
N                             New Conventional
O                             Commercial
P                             Purchase Money Mortgage
Q                             Undefined / Multiple Amounts
R                             Stand Alone Refi (Refinance of Original
S                             Seller take-back
T                             Loan Amount $10-99 billion - only first
U                             Unknown (DEFAULT)
V                             VA
W                             Future Advance Clause / Open End Mortgag
X                             Trade
Y                             State Veterans
Z                             Reverse Mortgage (Home Equity Conversion'''


ltv_curr_estimated_range_lu = '''LTV Curr Estimated Range
01                            0.01-50
02                            50.01-54.99
03                            55.00-59.99
04                            60.00-69.99
05                            70.00-74.99
06                            75.00-79.99
07                            80.00-84.99
08                            85.00-89.99
09                            90.00-94.99
10                            95.00-99.99
11                            100.00-104.99
12                            105.00-109.99
13                            110.00-124.99
14                            125+
NF                            Not Available - No Financing
NV                            Not Avaliable - No QVM Value'''


own_cass_address_hygiene_code_lu = '''Own_CASS_Address_Hygiene_Code
A                             DPV Coded
B                             Valid Non-DPV
E                             Invalid'''


owner_occupied_status_lu = '''Owner Occupied Status
Y                             Owner occupied
R                             Renter
N                             Non Owner Occupied (Unknown)'''


owner_status_type_lu = '''Owner Status Type
C                             Company
P                             PO Box
T                             Trust
I                             Investor
O                             Owner occupied'''


prop_vacant_flag_lu = '''Prop Vacant Flag
Y                             Yes, Vacant
N                             No'''


property_type_desc_lu = '''Property Type Desc
R                             Residential
C                             Commercial
A                             Agricultural'''


purchase_mtg_ind_1_lu = '''Purchase Mtg Ind 1
Y                             Yes'''


purpose_of_loan_1_lu = '''Purpose of Loan 1
01                            Non-Purchase First Trust
02                            Non-Purchase First Trust Refinance
03                            Non-Purchase First Trust Refinance Cash
04                            Non-Purchase First Trust Refinance Cash
05                            Non-Purchase First Trust Refinance Cash
06                            Non-Purchase First Trust Refinance Cash
07                            Non-Purchase First Trust Refinance Cash
08                            Non-Purchase First Trust Refinance Conso
09                            Non-Purchase First Trust Refinance Rate
10                            Non-Purchase First Trust Refinance Rate
11                            Non-Purchase First Trust Refinance Term
12                            Non-Purchase Non-First Trust Cash Out
13                            Non-Purchase Non-First Trust Refinance
14                            Non-Purchase Non-First Trust Refinance C
15                            Purchase First Trust
16                            Purchase Non-First Trust
17                            Reverse Non-Purchase First Trust Rate &
18                            Reverse Non-Purchase First Trust Rate Re
19                            Reverse Non-Purchase First Trust Refinan
20                            Reverse Non-Purchase First Trust Refinan
21                            Reverse Non-Purchase First Trust Refinan
22                            Reverse Non-Purchase First Trust Refinan
23                            Reverse Non-Purchase First Trust Refinan
24                            Reverse Non-Purchase First Trust Refinan
25                            Reverse Non-Purchase First Trust Refinan
26                            Reverse Non-Purchase First Trust Refinan
27                            Reverse Non-Purchase First Trust Refinan
28                            Reverse Non-Purchase First Trust Refinan
29                            Reverse Non-Purchase First Trust Term Re
30                            Reverse Non-Purchase Non-First Trust
31                            Reverse Non-Purchase Non-First Trust Cas
32                            Reverse Non-Purchase Non-First Trust Ref
33                            Reverse Non-Purchase Non-First Trust Ref
34                            Reverse Purchase First Trust
35                            Reverse Purchase Non-First Trust
36                            Reverse Undetermined Purchase First Trus
37                            Reverse Undetermined Purchase Undetermin
38                            Undetermined Purchase First Trust
39                            Undetermined Purchase Non-First Trust
40                            Undetermined Purchase Undetermined Trust
41                            Non-Purchase Non-First Trust Refinance C
42                            Non-Purchase Non-First Trust Refinance C
43                            Reverse Non-Purchase Non-First Trust Ref
44                            Reverse Non-Purchase Non-First Trust Ref'''


purpose_of_loan_2_lu = '''Purpose of Loan 2
01                            Non-Purchase First Trust
02                            Non-Purchase First Trust Refinance
03                            Non-Purchase First Trust Refinance Cash
04                            Non-Purchase First Trust Refinance Cash
05                            Non-Purchase First Trust Refinance Cash
06                            Non-Purchase First Trust Refinance Cash
07                            Non-Purchase First Trust Refinance Cash
08                            Non-Purchase First Trust Refinance Conso
09                            Non-Purchase First Trust Refinance Rate
10                            Non-Purchase First Trust Refinance Rate
11                            Non-Purchase First Trust Refinance Term
12                            Non-Purchase Non-First Trust Cash Out
13                            Non-Purchase Non-First Trust Refinance
14                            Non-Purchase Non-First Trust Refinance C
15                            Purchase First Trust
16                            Purchase Non-First Trust
17                            Reverse Non-Purchase First Trust Rate &
18                            Reverse Non-Purchase First Trust Rate Re
19                            Reverse Non-Purchase First Trust Refinan
20                            Reverse Non-Purchase First Trust Refinan
21                            Reverse Non-Purchase First Trust Refinan
22                            Reverse Non-Purchase First Trust Refinan
23                            Reverse Non-Purchase First Trust Refinan
24                            Reverse Non-Purchase First Trust Refinan
25                            Reverse Non-Purchase First Trust Refinan
26                            Reverse Non-Purchase First Trust Refinan
27                            Reverse Non-Purchase First Trust Refinan
28                            Reverse Non-Purchase First Trust Refinan
29                            Reverse Non-Purchase First Trust Term Re
30                            Reverse Non-Purchase Non-First Trust
31                            Reverse Non-Purchase Non-First Trust Cas
32                            Reverse Non-Purchase Non-First Trust Ref
33                            Reverse Non-Purchase Non-First Trust Ref
34                            Reverse Purchase First Trust
35                            Reverse Purchase Non-First Trust
36                            Reverse Undetermined Purchase First Trus
37                            Reverse Undetermined Purchase Undetermin
38                            Undetermined Purchase First Trust
39                            Undetermined Purchase Non-First Trust
40                            Undetermined Purchase Undetermined Trust
41                            Non-Purchase Non-First Trust Refinance C
42                            Non-Purchase Non-First Trust Refinance C
43                            Reverse Non-Purchase Non-First Trust Ref
44                            Reverse Non-Purchase Non-First Trust Ref'''


qvm_value_range_lu = '''QVM Value Range
01                            1-49, 999
02                            50, 000-99, 999
03                            100, 000-149, 999
04                            150, 000-199, 999
05                            200, 000-249, 999
06                            250, 000-299, 999
07                            300, 000-349, 999
08                            350, 000-399, 999
09                            400, 000-449, 999
10                            450, 000-499, 999
11                            500, 000-549, 999
12                            550, 000-599, 999
13                            600, 000-649, 999
14                            650, 000-699, 999
15                            700, 000-749, 999
16                            750, 000-799, 999
17                            800, 000-849, 999
18                            850, 000-899, 999
19                            900, 000-949, 999
20                            950, 000-999, 999
21                            1, 000, 000-1, 249, 999
22                            1, 250, 000-1, 499, 999
23                            1, 500, 000-1, 749, 999
24                            1, 750, 000-1, 999, 999
25                            2, 000, 000-2, 249, 999
26                            2, 250, 000-2, 499, 999
27                            2, 500, 000-2, 749, 999
28                            2, 750, 000-2, 999, 999
29                            3, 000, 000-3, 249, 999
30                            3, 250, 000-3, 499, 999
31                            3, 500, 000-3, 749, 999
32                            3, 750, 000-3, 999, 999
33                            4, 000, 000-4, 249, 999
34                            4, 250, 000-4, 499, 999
35                            4, 500, 000-4, 749, 999
36                            4, 750, 000-4, 999, 999
37                            5, 000, 000+
NV                            Not Avaliable - No QVM Value'''


rate_change_frequency_1_lu = '''Rate Change Frequency 1
2                             Two Years
3                             Three Years
4                             Four Years
A                             Annually
F                             Five Years - May be reported on document
M                             Monthly - Revolving Credit lines are alw
Q                             Quarterly
S                             Six months or Semi-annually'''


reo_deed_transfer_lu = '''REO Deed Transfer
0                             Not_Reo
1                             REO_In
2                             REO_Out
3                             Pre_FCL_last_6mos'''


reo_purchase_sale_lu = '''REO Purchase Sale
0                             Not_Reo
1                             REO_In
2                             REO_Out
3                             Pre_FCL_last_6mos'''

roof_construction_lu = '''Roof Construction
A                             GABLE
B                             BOWSTRING TRUSS
C                             REINFORCED CONCRETE
D                             DOME
E                             STEEL FRM / TRUSS
F                             FLAT
G                             GABLE OR HIP
H                             HIP
I                             IRR / CATHEDRAL
L                             GAMBREL
M                             MANSARD
P                             PRESTRESS CONCRETE
R                             RIGID FRM BAR JT
S                             SHED
T                             SAWTOOTH
W                             WOOD TRUSS'''


roof_cover_lu = '''Roof Cover
A                             Asbestos
B                             Built-up
C                             Composition Shingle
D                             Concrete
E                             Metal
F                             Slate
H                             Tar & Gravel
I                             Bermuda
J                             Masonite / Cement Shake
K                             Fiberglass
L                             Aluminum
M                             Wood Shake / Shingles
O                             Other
P                             Asphalt
R                             Roll Composition
S                             Steel
T                             Tile
U                             Urethane
V                             Shingle (Not Wood)
W                             Wood
Y                             Gypsum'''


sale_doc_type_last_sale_lu = '''Sale Doc Type Last Sale
AA                            Assignment of Sub Agreement of Sale (Haw
AB                            Assignment of Sub Lease (Hawaii)
AC                            Assignment of Commercial Lease (Hawaii)
AD                            Administrator�s Deed
AF                            Affidavit
AG                            Agreement of Sale
AH                            Assessor Sales History
AR                            Assignment of Agreement of Sale (Hawaii)
AS                            Assignment Deed ( or Assignment of Condo
AT                            Affidavit of Trust or Trust Agreement (L
AU                            Assignment of Sub Commercial Lease (Hawa
BD                            Beneficiary Deed (Buyer ID = "BE")
BS                            Bargain and Sale Deed
CA                            Commissioners Assignment of Lease (Hawai
CD                            Condominium Deed
CH                            Cash Sale Deed
CL                            Commercial Lease (Hawaii)
CM                            Commissioner�s Deed - In North Carolina
CN                            Cancellation of Agreement of Sale (Hawai
CO                            Conservator�s Deed
CP                            Corporation Deed
CR                            Correction Deed
CS                            Contract of Sale
CT                            Certificate of Transfer
DB                            Deed of Distribution
DC                            Declaration
DD                            Transfer on Death Deed
DE                            Deed
DG                            Deed of Guardian
DJ                            Affidavit of Death
DL                            Deed in Lieu of Foreclosure
DS                            Distress Sale
DT                            Affidavit of Death of Life Tenant
EC                            Exchange
EX                            Executor�s Deed
FC                            Foreclosure
FD                            Fiduciary Deed
GD                            Grant Deed
GF                            Gift Deed
GR                            Ground Lease
ID                            Individual Deed
IT                            Intrafamily Transfer & Dissolution - Due
JT                            Joint Tenancy Deed
LA                            Legal Action / Court Order
LC                            Leasehold Conv.With Agreement of Sale (
LD                            Land Contract
LE                            Lease (Hawaii)
LH                            Assignment of Lease (Leasehold Sale) (Ha
LS                            Leasehold Conv.with an Agreement of Sal
LT                            Land Court (Massachusetts)
LW                            Limited Warranty Deed
MD                            Special Master Deed
OT                            Other
PA                            Public Action - Common in Florida (Clerk
PD                            Partnership Deed
PR                            Personal Representatives Deed
QC                            Quit Claim Deed
RA                            Satisfaction of Land Contract (Wisconsin
RC                            Receiver�s Deed
RD                            Redemption Deed
RF                            Referee�s Deed - used to transfer proper
RL                            Release / Satisfaction of Agreement of Sal
RR                            Re-recorded Document
RS                            REO Sale (REO Out)
SA                            Sub Agreement of Sale (Hawaii)
SC                            Sub Commercial Lease (Hawaii)
SD                            Sheriff�s Deed - Common in New Jersey.T
SL                            Sub Lease (Hawaii)
ST                            Affidavit Death of Trustee / Successor Tru
SV                            Survivorship Deed
SW                            Special Warranty Deed
TD                            Trustee�s Deed (Certificate of Title)
VL                            Vendor�s Lien
WD                            Warranty Deed
XX                            Transaction History Record'''


standalone_refi_1_lu = '''StandAlone Refi 1
0                             No
1                             Yes'''


step_rate_rider_lu = '''Step Rate Rider
2                             Capped Two-Year ARM Rider
A                             Rate starts as Adjustable
F                             Rate starts as Fixed
V                             Rate starts as Variable
Y                             Yes'''


tax_exemption_codes_lu = '''Tax Exemption Codes
A                             Agricultural
B                             Disabled (any)
C                             Cemetery
D                             Homestead
E                             Tax Exempt
F                             Senior Citizen
G                             Government
H                             Historical
I                             Low Income
J                             Partial Exempt
K                             Head of Household
L                             Library / Museum
M                             Miscellaneous
N                             Non-profit
O                             Orphanage
P                             Public Utilities
Q                             Charity / Fraternal Org.
R                             Religious / Church
S                             School / College
T                             Hospital / Medical
U                             Redevelopment Agency
V                             Veteran
W                             Welfare
X                             Railroad
Y                             Native American
Z                             Widow / er'''


# classname = create_default_classname_from_tablename("own_cass_zip_plus_4_flag_lu")
# tablename, _ = create_default_tablename(classname)
# print(f'classname {create_default_classname_from_tablename("own_cass_zip_plus_4_flag_lu")} - tablename {tablename}')





locals = dict(locals())

print(f'# --------GENERATED MODELS --------\n')

for k,v in locals.items():
	if k.endswith('lu') and v is not None:

		# convert tablename to classname convention
		info = {
			'lookup_table_name': create_default_classname_from_tablename(k),
			'names': [],
			'display_names': [],
			'descriptions': []
		}
		for x in v.split('\n')[1:]:
			name = x[:x.index(" ")].strip()
			value = x[30:].strip()

			# tax_exemption_codes_lu - name: Z value: Widow / er
			# print(f'{k} - name: {name} value: {value}')

			info['names'].append(name)
			info['display_names'].append(value)
			info['descriptions'].append(value)

		template_path = os.path.join(os.path.dirname(__here__), 'templates', 'lookuptable.mako')

		print('\n')

		t = Template(filename=template_path)
		result = t.render(**info)

		print(result)