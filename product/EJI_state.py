# libraries
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
import geopandas as gpd
from scipy import stats
import csv

def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width(), 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

item='RPL_THEMES'
anch='INC'
Spec='O3'

Races=['All','White','Black','Asian','Hispan','Native']

Authors=['Turner','Di']

States=['USA','Alabama','Arkansas','California','Arizona','Colorado',
 'Connecticut','District of Columbia','Delaware','Florida','Georgia',
 'Illinois','Idaho','Indiana','Kentucky','Kansas','Iowa',
 'Louisiana','Maryland','Maine','Massachusetts','Michigan','Minnesota',
 'Missouri','Mississippi','Nevada','Montana','Nebraska','New Jersey',
 'New Hampshire','New Mexico','New York','North Carolina','Ohio',
 'North Dakota','Oklahoma','Oregon','Pennsylvania','Tennessee',
 'Rhode Island','South Carolina','South Dakota','Texas','Utah','Vermont',
 'Virginia','Washington','West Virginia','Wisconsin','Wyoming']


ST_ABV=['USA','AL','AR','CA','AZ','CO','CT','DC','DE','FL','GA',
 'IL','ID','IN','KY','KS','IA','LA','MD','ME','MA','MI','MN',
 'MO','MS','NV','MT','NE','NJ','NH','NM','NY','NC','OH',
 'ND','OK','OR','PA','TN','RI','SC','SD','TX','UT','VT',
 'VA','WA','WV','WI','WY']

df_st=pd.DataFrame({'STATE_NAME':States})
df_st=df_st.set_index('STATE_NAME')
df_st['ST']=ST_ABV

fips=read_csv('EID/ROW_COL_rev_FIPS_crosswalk.csv',usecols=['STATEFP10','COUNTYFP10','FIPS','ROW','COL'])

Years=range(2002,2020)

datax={'Year':Years}

for state in States:

	df_out=pd.DataFrame(datax)
	df_out=df_out.set_index('Year')


	for race in Races:
		vnt='EJI_tu_'+race
		vnd='EJI_di_'+race
		df_out[vnt]=np.zeros(17)
		df_out[vnd]=np.zeros(17)
	df_out.to_csv('Result/'+Spec+'/EJI_'+state+'_2002_2018_Inc.csv')

for year in range(2002,2020):

	print(year)

	if year < 2011:
		EJI_file='EID/SVI2010_US.csv'
	if year >2010 and year < 2015:
		EJI_file='EID/SVI2014_US.csv'
	if year >2014 and year < 2017:
		EJI_file='EID/SVI2016_US.csv'	
	if year >2016 and year < 2019:
		EJI_file='EID/SVI2018_US.csv'
	EJI=read_csv(EJI_file,usecols=['FIPS',item,'STATE_NAME'])
	merge=pd.merge(fips,EJI,how='left',left_on=['FIPS'],right_on=['FIPS'])

	for author in Authors:

		if author == 'Turner':
			at='tu'
		else:
			at='di'

		file='New_BenMAP_Results/'+str(year)+'/'+Spec+'/'+author+'_'+anch+'_CT.shp'
		gfd=gpd.read_file(file)
		dfx=pd.merge(gfd,merge, how='left', left_on=['COL','ROW'], right_on=['COL','ROW'])

		for state in States:

			print(state)
			df_in=read_csv('Result/'+Spec+'/EJI_'+state+'_2002_2018_Inc.csv')
			df_in=df_in.set_index('Year')

			if state == 'USA':
				df_inc=dfx
			else:
				if year < 2015:
					df_inc=dfx[dfx['STATE_NAME']==state]
				if year > 2014:
					df_inc=dfx[dfx['STATE_NAME']==state.upper()]

			df_inc=df_inc.sort_values(item,ascending=[True])
			group = df_inc.groupby([item])
			for race in Races:
				vn='EJI_'+at+'_'+race
				inc=anch+'_'+race
				pop='POP_'+race
				
				Value = group[inc].agg(np.sum)
				POPS = group[pop].agg(np.sum)
				SVI = group[item].unique()

				Value=Value.to_numpy()#*inf18 change negative -1.0*
				SVI=SVI.to_numpy()
				POPS=POPS.to_numpy()

				# #work with exact population
				Frac=POPS/np.sum(POPS)#normolized
				CumS=np.cumsum(Frac)
				Area=np.sum(CumS)
				totpop=np.sum(POPS)# total population

				# #calculat suits index
				Sun=np.sum(Value) # total death
				Frac1=Value/Sun #normolized
				CumS1=np.cumsum(Frac1)
				Area1=np.sum(CumS1)
				death=Sun
				EJI=100*(Area-Area1)/Area
				df_in.at[year,vn]=EJI
			df_in.to_csv('Result/'+Spec+'/EJI_'+state+'_2002_2018_Inc.csv')
	#calculate Trends
x=range(0,17)
for state in States:
	df_out=read_csv('Result/'+Spec+'/EJI_'+state+'_2002_2018_Inc.csv')
	df_out=df_out.set_index('Year')
	for race in Races:
		vnt='EJI_tu_'+race
		vnd='EJI_di_'+race
		data=df_out[vnt].to_numpy()
		slope, intercept, r_value, p_value, std_err = stats.linregress(x,data)
		df_st.at[state,vnt]=slope

		data=df_out[vnd].to_numpy()
		slope, intercept, r_value, p_value, std_err = stats.linregress(x,data)
		df_st.at[state,vnd]=slope

	# # print(o3_min_max)
	print(df_st.loc[[state]])

df_st.to_csv('Result/'+Spec+'/EJI_slope_US_States_2002_2018_Inc.csv')