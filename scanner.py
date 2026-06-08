import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os
stock_name = input("Enter the stock ticker for which you want to detect the breakouts: ").upper() + ".NS"
file_path = f"./data/{stock_name}.csv"
if os.path.exists(file_path):
    # Loading the file
    data = pd.read_csv(file_path)
else:
    
    # Downloading the data from yfinance --> Just put the stockname.ns to get the details of the desired stock
    data = yf.download(stock_name,start="2021-01-01",end="2026-05-31")
    data.columns = data.columns.droplevel(1)
    data.columns.name = None #Set the name of  the columns

    # Saving the downloaded data to a file
    data.to_csv(file_path)
    #Loading the file
    data = pd.read_csv(file_path)

#Modifying the data frame
data.drop(columns=["Open","High","Low"],inplace=True)
data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date",inplace=True)
data.rename(columns={"Close":"Closing_Price"},inplace=True)

# Handling the invalid/null data
data.dropna(inplace=True)
data.drop(data[data["Volume"]==0].index,inplace=True)

# Calculating the 20 Day SMA(Simple Moving Average)
data["Price_Moving_Average"] = data["Closing_Price"].rolling(20).mean()
data["Volume_Moving_Average"] = data["Volume"].rolling(20).mean()
data["Breakout/Breakdown"] = data["Volume"]>3*data["Volume_Moving_Average"]
data.dropna(inplace=True)
breakout = data[data["Breakout/Breakdown"]==True].copy()
breakout["Vol_increase_by"] = (breakout["Volume"]/breakout["Volume_Moving_Average"])

#Printing the breakout data
print(breakout) 
# print(data.index) #Prints a List of all the dates

# Visualization using matplotlib

#Graph for 20 Day SMA for price

# plt.plot(data.index,data["Price_Moving_Average"],label="20 Days MA(Price)",color="Red",alpha=0.7)
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.legend()
# plt.show()

#Graph for 2 Day SMA for volume
# plt.plot(data.index,data["Volume_Moving_Average"],label = "20 Days MA(Volume)",color = "Green",alpha = 0.7)
# plt.xlabel("Date")
# plt.ylabel("Volume")
# plt.legend()
# plt.show()

#Plotting the 20 DMA for price and volume and stack them together, Price on Top, Volume on the bottom

# --------------METHOD 1------------
# Create the master canvas with 2 rows and 1 column(rows-->y_axis,columns-->x_axis)
# sharex = True fuses the x-axes(date) of both the graphs together

# fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1,figsize=(12,8),sharex=True)

# #Top Chart(ax1): Plot the Price Moving Average
# ax1.plot(data.index,data["Closing_Price"],color="Blue",label="Price on each day")
# ax1.plot(data.index,data["Price_Moving_Average"],color="Green")
# ax1.set_ylabel("Price Moving Average")
# ax1.set_title("Market Sniper Scan : Price vs Volume Breakouts")
# # ax1.set_xlabel("Date") #We can also label this x axis but its taking extra space on the graph

# #Bottom chart(ax2) : Plot the Volume Moving Average
# ax2.plot(data.index,data["Volume_Moving_Average"]/1000000,color="Red")
# ax2.set_ylabel("Volume Moving Average(Millions)")
# ax2.set_xlabel("Date")

# #Clean up the spacing between the two plots
# plt.tight_layout()
# #Show whatever has been plotted
# plt.show()



# -----------------------METHOD 2 --------------------------
#twin Y axis in a single graph

#Create the master canvas(fig) and the first axis(ax1 - y axis on left side)
fig,ax1 = plt.subplots(figsize=(12,8))

#Plot the  Price Moving Average on the left axis
ax1.plot(data.index,data["Price_Moving_Average"],color="Green",label="Price MA")
ax1.plot(data.index,data["Closing_Price"],color="Blue",label="Price")
ax1.set_xlabel("Date")
ax1.set_ylabel("Price",color="Blue")
ax1.tick_params(axis="y",labelcolor="blue")
ax1.scatter(breakout.index,breakout["Closing_Price"],color="Red",label="Breakout Trigger",s=100,zorder=5)
ax1.legend()

#Create the twin y axis(RIGHT SIDE)

ax2 = ax1.twinx() #This clones the X-axis(dates) but creates a brand new y axis scale on the right side

#Plot the volume moving average on the right axis
ax2.plot(data.index,data["Volume_Moving_Average"]/1000000,color="Orange",label="Volume MA")
ax2.set_ylabel("Volume(Millions)",color="Orange")
ax2.legend()
ax2.tick_params(axis="y",labelcolor= "orange") #​tick_params: By coloring the text of the Y-axis labels to match the lines (blue for price, orange for volume), you prevent yourself from getting confused about which line belongs to which scale when you are analyzing the data.
ax1.set_facecolor("#FDF6E3")
plt.title("PRICE MA vs VOLUME MA",color="Black",weight="bold")
fig.set_facecolor("#EAE7DC")
plt.show()