import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

data = pd.read_csv("C:\\Users\\Kartik kartik\\Desktop\\food delivery project\\data\\talabat_enhanced_orders.csv")
df = pd.DataFrame(data)
#to get the first 20 rows of the dataset
print(df.head(20))

#to get structure of the dataset
print(df.info())

#to get the statistical summary of the dataset
print(df.describe())

#to check null values
print(df.isnull().sum())
#there are no null values in the dataset

#converting order_time and delivery_time to datetime
df['Order_Time'] = pd.to_datetime(df['Order_Time'])
df['Delivery_Time'] = pd.to_datetime(df['Delivery_Time'])

#creating new columns for hour, day and month of the order time
df['hour'] = df['Order_Time'].dt.hour 
df['day'] = df['Order_Time'].dt.day_name()
df['month'] = df['Order_Time'].dt.month

#CREATING A NEW COLUM FOR DELIVERY TIME IN MINUTES
df['cal_delivery_time'] = (df['Delivery_Time'] - df['Order_Time']).dt.total_seconds() / 60


print(df.head())


import sqlite3
conn = sqlite3.connect('food_delivery.db')
df.to_sql('orders', conn, if_exists='replace', index = False)
#to check the data in the database
query = "SELECT * FROM orders"
result = pd.read_sql(query, conn)
print(result.head(5))

#to reterve all data from the database
pd.read_sql("select * from orders",conn)

#to get total sales
total_sales = pd.read_sql('select sum(total_price) as total_sales from orders', conn)
print(total_sales)

#to get no of orders
no_of_orders = pd.read_sql('select count(*) as total_orders from orders', conn)
print(no_of_orders)

#avg price of the orders
avg_price = pd.read_sql('select avg(total_price) as avg_price from orders', conn)
print(avg_price)

#avg min duration of delivery
avg_delivery_time = pd.read_sql('select avg(cal_delivery_time) as avg_delivery_time from orders', conn)
print(avg_delivery_time)

#most selling item
most_selling_item = pd.read_sql('select item_name, sum(total_price) as total_sale from orders group by item_name order by total_sale desc limit(1)', conn)
print(most_selling_item)

#peak hour for orders
peak_hour = pd.read_sql('select hour, count(*) as orders from orders group by hour order by orders desc limit(1)', conn)
print(peak_hour)

#which resturant dominates the sales
top_restaurant = pd.read_sql('select restaurant_id, sum(total_price) as total_sale from orders group by restaurant_id order by total_sale desc limit(1)', conn)
print(top_restaurant)

#total revenue
total_revenue = pd.read_sql(
    "select sum(Total_price) as Total_revenue from orders"
    ,conn)
print(total_revenue)

revenue_by_item = pd.read_sql("select item_name , sum(Total_price) as Total_revenue from orders group by item_name order by Total_revenue desc",conn)
print(revenue_by_item)

peak_hour = pd.read_sql("select hour ,count(*) as orders from orders group by hour order by orders desc limit(1)", conn)
print(peak_hour)

delivery_time_as_hour = pd.read_sql("select cal_delivery_time/60 as delivery_time_in_hour from orders order by delivery_time_in_hour desc", conn)
print(delivery_time_as_hour)

per = 3060271.73/ total_revenue['Total_revenue'][0] * 100
print(per)

df.to_csv("C:\\Users\\Kartik kartik\\Desktop\\food delivery project\\data\\enhanced_orders.csv", index = False)
