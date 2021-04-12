import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

#read the csv file in current working directory
cwd = os.getcwd() + "/temperatures.csv"
data = pd.read_csv(cwd)

#conerting timestamp to datetime object
data["Zeitstempel"] = pd.to_datetime(data["Zeitstempel"], format = '%Y%m%d%H%M')     

#convert Timestep to 15-minute-intervals
data = data.set_index('Zeitstempel').resample('15T').asfreq()

#linearinterpolate the interval data
data["Produkt_Code"] = data["Produkt_Code"].interpolate(method='pad')
data["SDO_ID"] = data["SDO_ID"].interpolate(method='pad')
data["Wert"] = data["Wert"].interpolate(method='linear')
data["Qualitaet_Niveau"] = data["Qualitaet_Niveau"].interpolate(method='pad',limit=3)
data["Qualitaet_Byte"] = data["Qualitaet_Byte"].interpolate(method='pad',limit=3)
data = data.reset_index()

#creating new columns of Year and Time
data["Year"] = data["Zeitstempel"].dt.strftime("%Y")
data["Time"] = data["Zeitstempel"].dt.strftime("%H:%M")
#data["Time"] = pd.to_datetime(data["Time"], format = '%H:%M')


#function for extracting hot and cold days of year
def h_c_year(csv_f):
    df_year = csv_f.groupby('Year')    
    maxii = pd.DataFrame(columns=['hottest'])
    maxii["hottest"],h_ind   = df_year['Wert'].max(),df_year['Wert'].idxmax()
    maxii["coldest"],c_ind   = df_year['Wert'].min(),df_year['Wert'].idxmin()
    maxii["mean"] = df_year["Wert"].mean()
    maxii["timeoccurence@Hottest"] = np.nan
    maxii["timeoccurence@Coldest"] = np.nan
    maxii = maxii.reset_index()
    
    for i in range(0,len(maxii)):
        maxii.loc[i,'timeoccurence@Hottest'] = csv_f.loc[h_ind[i],'Time']   
        maxii.loc[i,'timeoccurence@Coldest'] = csv_f.loc[c_ind[i],'Time']
           
    
    
    return maxii

H_C_Year = h_c_year(data)

#creating csv file in current working directory
cwd = os.getcwd() + "/H_C_Year.csv"
H_C_Year.to_csv(cwd)  


def plot_data(H_C_data):
        plt.style.use("seaborn-paper")
        
        H_C_data["timeoccurence@Hottest"] = pd.to_datetime(H_C_data["timeoccurence@Hottest"], format = '%H:%M')
    
        H_C_data["timeoccurence@Coldest"] = pd.to_datetime(H_C_data["timeoccurence@Coldest"], format = '%H:%M')
        plt.plot(H_C_data["Year"], H_C_data["timeoccurence@Hottest"], color='r', marker='o', label= "hottest")
        plt.plot(H_C_data["Year"], H_C_data["timeoccurence@Coldest"], color='b', marker='o', label = "coldest")
        H_C_data["timeoccurence@Hottest"] = H_C_data["timeoccurence@Hottest"].dt.strftime("%H:%M")
        H_C_data["timeoccurence@Coldest"] = H_C_data["timeoccurence@Coldest"].dt.strftime("%H:%M")
        plt.title("hottest&coldest@year")
        data_format_x = mpl_dates.DateFormatter('%H:%M')
        plt.gca().yaxis.set_major_formatter(data_format_x)
        
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.show()
        
        
def plot_mean(m_data):
        plt.style.use("seaborn-paper")        
        plt.plot(m_data["Year"], m_data["mean"], color='g', marker='o', label= "mean")
        plt.title("avg temp of every year")
        plt.gcf().autofmt_xdate()
        plt.show()
        
        
plot_data(H_C_Year)
plot_mean(H_C_Year)


