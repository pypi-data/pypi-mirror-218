import numpy as np
import pandas as pd
import plotly.express as px
import boto3

# Get the Data From the AWS S3 buket

def Get_Data_from_S3_Bucket(aws_access_key_id, aws_secret_access_key, bucket_name, file_path):
    s3 = boto3.client("s3", 
                      aws_access_key_id = aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)
 
    try:
        df = pd.read_csv(obj["Body"])
        
        return df
    
    except:
        
        df = pd.read_excel(obj["Body"])
   
        return df


# Binning the Yield
def Yield_Binning(datframe,column):
    
    # Filling the Missing Values   
    datframe[column] = datframe[column].fillna(datframe[column].mean())
    
    # Calculating the yield quantiles
    col_values = list(datframe[column])
    Q_25 = np.percentile (col_values, 25) 
    Q_50 = np.percentile (col_values, 50)
    Q_75 = np.percentile (col_values, 75)

    # Creating the new column with the condtion
    for index,row in datframe.iterrows():

        if row[column] <= Q_25:
            datframe.at[index,'Category'] = 'Low'

        elif (row[column]>Q_25 and row[column] <= Q_50):
            datframe.at[index,'Category'] = 'Medium Low'

        elif (row[column]>Q_50 and row[column]<=Q_75):
            datframe.at[index,'Category'] = 'Medium High'
            
        else:
            datframe.at[index,'Category'] = 'High'

    return datframe

#################################################################

# Creating the function for Yield binning Ranges Values
def Yield_Binning_Ranges_Values(data,Yield_column_name):
    
    df_new = data[[Yield_column_name]]

    #Removing low level outliers
    df_new = df_new[(df_new[Yield_column_name] > 0)]
    
    #Removing the null values
    df_new.dropna(inplace=True)
    
    #Calculating the IQR
    col_values = list(df_new [Yield_column_name])
    
    Q_25 = np.percentile (col_values, 25) 
    Q_50 = np.percentile (col_values, 50)
    Q_75 = np.percentile (col_values, 75)
    
    # Creating the new column with the condtion
    
    for index,row in df_new.iterrows():

        if row[Yield_column_name]<=Q_25:

            df_new.at[index,'Yeild Category'] = 'Low'
            df_new.at[index,'% of Yield Range'] = '<25'

        elif (row[Yield_column_name]>Q_25 and row[Yield_column_name]<=Q_50):

            df_new.at[index,'Yeild Category'] = 'Medium Low'
            df_new.at[index,'% of Yield Range'] = '26-50'

        elif (row[Yield_column_name]>Q_50 and row[Yield_column_name]<=Q_75):

            df_new.at[index,'Yeild Category'] = 'Medium High'
            df_new.at[index,'% of Yield Range'] = '51-75'
            
        else:
            df_new.at[index,'Yeild Category'] = 'High'
            df_new.at[index,'% of Yield Range'] = '>76'
    
    df_final = df_new.groupby(['% of Yield Range','Yeild Category']).agg(min=(Yield_column_name, 'min'),max=(Yield_column_name, 'max'), mean=(Yield_column_name, 'mean'),
                                                                         median=(Yield_column_name, 'median')).sort_values('mean')
    
    return df_final

#############################################################################################################################################################################

# Creating the function for Weather changes between the low and high yield

def Weather_Change_IN_Low_Vs_High_Yield(data,Yield_column,Weather_params):

    data = Yield_Binning(data,Yield_column)
    
    data = data[(data[Yield_column] > 0)]
    
    Weather_params.insert(0,Yield_column)
    
    # This is  for Low Category
    df_low = data[data['Category'] == 'Low'].reset_index(drop=True)
    df_low = df_low[Weather_params]
    
    df_low_final = df_low.describe().T
    df_low_final = df_low_final[['min','max','mean']]

    ## This is  for High category
    df_high = data[data['Category'] == 'High'].reset_index(drop=True)
    df_high = df_high[Weather_params]

    df_high_final = df_high.describe().T
    df_high_final = df_high_final[['min','max','mean']]
    
    # Concating the low and High  dataframe
    df_low_high = pd.concat([df_low_final,df_high_final],axis=1,keys=['Weather Range with Low Yield','Weather Range with High Yield'],names= ['Weather Parameter'])
    
    # Droping the duplicate
    df_low_high = df_low_high.drop_duplicates()

    return df_low_high

####################################################################################################################################################################

# Getting the delta change for palnting and Harvest dates
def Delta_Change(data, Yield_cloumn, by, return_dataframe = True):
    
    # Copy of the original dataframe
    data = data.copy()
    
    # Storing the column Name
    column_name = by
    
    # Converting the string data type  into datetime format

    data[column_name] = pd.to_datetime(data[column_name])

    # strftime --> b for month (jan,feb) and d for day of the date
    data['Month_Date'] = data[column_name].apply(lambda x: x.strftime('%b-%d'))

     # Convert the 'dates' column to datetime format with a fake year
    data['Month_Date'] = pd.to_datetime('2020-' + data['Month_Date'], format='%Y-%b-%d')

    # Sort the DataFrame by the 'dates' column
    data = data.sort_values(by='Month_Date').reset_index(drop=True)

    # Remove the fake year from the 'dates' column
    data['Month_Date'] = data['Month_Date'].dt.strftime('%b-%d')
    
    data['Month'] =  data[column_name].apply(lambda x: x.strftime('%b'))
    
    data = data.groupby(['Month_Date','Month']).agg(Avg_yield=(Yield_cloumn, 'mean'))

    data ['Avg_yield'] = round(data['Avg_yield'],2)

    data.sort_values('Avg_yield',ascending=False,inplace=True)

    data['Delta_Change_by_max'] =  data ['Avg_yield'].max() - data['Avg_yield']

    data['Delta_Change_percent'] = round(((data['Avg_yield'].max() - data['Avg_yield']) / data['Avg_yield'].max()) * 100,2)

    data['Delta_Change_by_mean'] = round( data['Avg_yield'] - data['Avg_yield'].mean(),2)

    data['Delta_Change_percent'] = data['Delta_Change_percent'].apply( lambda x : str(x) + '%')
    
    # Resetting the Index
    data = data.reset_index()
    
   # Filtering the dataframe using top 4 month 
    
    foo = data['Month'].value_counts().index.tolist()[:4]
    data = data[data['Month'].isin(foo)]
    
    if return_dataframe == True:

        return data
    
    else:
        
        fig = px.scatter(data, x= 'Month_Date', y="Avg_yield", size='Avg_yield',color = 'Month',title= 'Delta Change by ' + column_name +' .')
        
        fig.show()

#################################################################################################################################################

# Getting the Best dates to plant and harvest
def Best_Dates(data, Yield_cloumn, by, return_dataframe = True):
    
    # Storing the name 
    column_name = by
        
    # Calculating the best planting dates
    data = data.groupby([column_name]).agg(Avg_yield=(Yield_cloumn, 'mean')).reset_index()

    # strftime --> b for month (jan,feb) and d for day of the date
    data['Month_Date'] = data[column_name].apply(lambda x: x.strftime('%b-%d'))

    data['Month'] = data[column_name].apply(lambda x: x.strftime('%b'))

    # Convert the 'dates' column to datetime format with a fake year
    data['Month_Date'] = pd.to_datetime('2020-' + data['Month_Date'], format='%Y-%b-%d')

    # Sort the DataFrame by the 'dates' column
    data = data.sort_values(by='Month_Date').reset_index(drop=True)

    # Remove the fake year from the 'dates' column
    data['Month_Date'] = data['Month_Date'].dt.strftime('%b-%d')

    data.reset_index(drop = True,inplace = True)
    
    data = data.dropna()
    
    if return_dataframe == True:

        return data

    else:

        fig = px.scatter(data, x='Month_Date', y='Avg_yield',size='Avg_yield',color = 'Month')
        fig.update_layout(title = 'Best Dates', yaxis_title = 'Average Yield') 
        fig.show()
            
################################################################################################################



