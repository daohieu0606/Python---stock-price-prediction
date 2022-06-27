# import pandas as pd
# import numpy as np

# import matplotlib.pyplot as plt

# from matplotlib.pylab import rcParams
# rcParams['figure.figsize']=20,10
# from keras.models import Sequential
# from keras.layers import LSTM,Dropout,Dense


# from sklearn.preprocessing import MinMaxScaler


# df=pd.read_csv("NSE-TATA.csv")
# df.head()


# df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")
# df.index=df['Date']

# data=df.sort_index(ascending=True,axis=0)
# new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])

# for i in range(0,len(data)):
#     new_dataset["Date"][i]=data['Date'][i]
#     new_dataset["Close"][i]=data["Close"][i]

# scaler=MinMaxScaler(feature_range=(0,1))
# final_dataset=new_dataset.values

# train_data=final_dataset[0:987,:]
# valid_data=final_dataset[987:,:]

# new_dataset.index=new_dataset.Date
# new_dataset.drop("Date",axis=1,inplace=True)
# scaler=MinMaxScaler(feature_range=(0,1))
# scaled_data=scaler.fit_transform(final_dataset)

# x_train_data,y_train_data=[],[]

# for i in range(60,len(train_data)):
#     x_train_data.append(scaled_data[i-60:i,0])
#     y_train_data.append(scaled_data[i,0])
    
# x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)

# x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))

# print(x_train_data)