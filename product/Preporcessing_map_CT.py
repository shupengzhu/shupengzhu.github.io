# libraries
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
import geopandas as gpd
from scipy import stats
import seaborn as sns
from matplotlib import cm
import matplotlib
from tqdm import tqdm
import warnings
import os
import shutil
warnings.filterwarnings('ignore')

# read dataset

gpd_st=gpd.read_file('map/USA_CT_Grids_Dissolve.shp', crs="epsg:4326")

Races=['White','Black','Asian','Hispanic','Native']

Years=range(2002,2020)

for year in Years:
   print(year)

   df_inc=read_csv('./PM2.5/'+str(year)+'.CSV',usecols=['Column','Row','Race','Ethnicity','Author','Population','Endpoint','Mean'])

   df=df_inc[df_inc['Endpoint'] != 'Population Weighted Delta'].reset_index()
   df0=df.query("Race != 'ALL' and Author == 'Turner et al.'")

   pm_tu=df0.groupby(['Column','Row']).sum().reset_index()
   pm_tu['Rate']=100000*pm_tu['Mean']/pm_tu['Population']
   merge0=pd.merge(gpd_st,pm_tu,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
   merge0=merge0.drop(columns=['Column','Row'])
   merge0=merge0.rename(columns={'Mean':'INC_All','Population':'POP_All','Rate':'RT_All'})
   for race in Races:
      inc='INC_'+race
      pop='POP_'+race
      rate='RT_'+race
      if race == 'White':
         dfs=df0[df0['Ethnicity'] == 'NON-HISPANIC']
      if race == 'Black':
         dfs=df0[df0['Race'] == 'BLACK']
      if race == 'Asian':
         dfs=df0[df0['Race'] == 'ASIAN']
      if race == 'Hispanic':
         dfs=df0[df0['Ethnicity'] == 'HISPANIC']
      if race == 'Native':
         dfs=df0[df0['Race'] == 'NATAMER']
      dfs['Rate']=100000*dfs['Mean']/dfs['Population']
      merge=pd.merge(gpd_st,dfs,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
      merge=merge.drop(columns=['Column','Row'])
      merge0[inc]=merge['Mean']
      merge0[pop]=merge['Population']
      merge0[rate]=merge['Rate']
   merge0.to_file('./PM2.5/Age_30'+str(year)+'.shp')

   print('PM Turner Finished!')

   df1=df.query("Race != 'ALL' and Author == 'Di et al.'")
   pm_di=df1.groupby(['Column','Row']).sum().reset_index()
   pm_di['Rate']=100000*pm_di['Mean']/pm_di['Population']
   merge1=pd.merge(gpd_st,pm_di,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
   merge1=merge1.drop(columns=['Column','Row'])
   merge1=merge1.rename(columns={'Mean':'INC_All','Population':'POP_All','Rate':'RT_All'})
   for race in Races:
      inc='INC_'+race
      pop='POP_'+race
      rate='RT_'+race
      if race == 'White':
         dfs=df1[df1['Ethnicity'] == 'NON-HISPANIC']
      if race == 'Black':
         dfs=df1[df1['Race'] == 'BLACK']
      if race == 'Asian':
         dfs=df1[df1['Race'] == 'ASIAN']
      if race == 'Hispanic':
         dfs=df1[df1['Ethnicity'] == 'HISPANIC']
      if race == 'Native':
         dfs=df1[df1['Race'] == 'NATAMER']
      dfs['Rate']=100000*dfs['Mean']/dfs['Population']
      merge=pd.merge(gpd_st,dfs,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
      merge=merge.drop(columns=['Column','Row'])
      merge1[inc]=merge['Mean']
      merge1[pop]=merge['Population']
      merge1[rate]=merge['Rate']
   merge1.to_file('./PM2.5/Age_65'+str(year)+'.shp')
   print('PM Di Finished!')

   dfo_inc=read_csv('./O3/'+str(year)+'CSV',usecols=['Column','Row','Race','Ethnicity','Author','Population','Endpoint','Mean'])
   dfo=dfo_inc[df_inc['Endpoint'] != 'Population Weighted Delta'].reset_index()
   df2=dfo.query("Race != 'ALL' and Author == 'Turner et al.'")
   o3_tu=df2.groupby(['Column','Row']).sum().reset_index()
   o3_tu['Rate']=100000*o3_tu['Mean']/o3_tu['Population']
   merge2=pd.merge(gpd_st,o3_tu,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
   merge2=merge2.drop(columns=['Column','Row'])
   merge2=merge2.rename(columns={'Mean':'INC_All','Population':'POP_All','Rate':'RT_All'})
   for race in Races:
      inc='INC_'+race
      pop='POP_'+race
      rate='RT_'+race
      if race == 'White':
         dfs=df2[df2['Ethnicity'] == 'NON-HISPANIC']
      if race == 'Black':
         dfs=df2[df2['Race'] == 'BLACK']
      if race == 'Asian':
         dfs=df2[df2['Race'] == 'ASIAN']
      if race == 'Hispanic':
         dfs=df2[df2['Ethnicity'] == 'HISPANIC']
      if race == 'Native':
         dfs=df2[df2['Race'] == 'NATAMER']
      dfs['Rate']=100000*dfs['Mean']/dfs['Population']
      merge=pd.merge(gpd_st,dfs,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
      merge=merge.drop(columns=['Column','Row'])
      merge2[inc]=merge['Mean']
      merge2[pop]=merge['Population']
      merge2[rate]=merge['Rate']   
   merge2.to_file('./O3/Age_30'+str(year)+'.shp')   
   print('O3 Turner Finished!')

   df3=dfo.query("Race != 'ALL' and Author == 'Di et al.'")
   o3_di=df3.groupby(['Column','Row']).sum().reset_index()
   o3_di['Rate']=100000*o3_di['Mean']/o3_di['Population']
   merge3=pd.merge(gpd_st,o3_di,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
   merge3=merge3.drop(columns=['Column','Row'])
   merge3=merge3.rename(columns={'Mean':'INC_All','Population':'POP_All','Rate':'RT_All'})
   for race in Races:
      inc='INC_'+race
      pop='POP_'+race
      rate='RT_'+race
      if race == 'White':
         dfs=df3[df3['Ethnicity'] == 'NON-HISPANIC']
      if race == 'Black':
         dfs=df3[df3['Race'] == 'BLACK']
      if race == 'Asian':
         dfs=df3[df3['Race'] == 'ASIAN']
      if race == 'Hispanic':
         dfs=df3[df3['Ethnicity'] == 'HISPANIC']
      if race == 'Native':
         dfs=df3[df3['Race'] == 'NATAMER']
      dfs['Rate']=100000*dfs['Mean']/dfs['Population']
      merge=pd.merge(gpd_st,dfs,how='left', left_on=['COL','ROW'], right_on=['Column','Row'])
      merge=merge.drop(columns=['Column','Row'])
      merge3[inc]=merge['Mean']
      merge3[pop]=merge['Population']
      merge3[rate]=merge['Rate']  
   merge3.to_file('./O3/Age_65'+str(year)+'.shp')
   print('O3 Di Finished!')