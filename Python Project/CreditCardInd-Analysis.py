import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
import os

customer=pd.read_csv("C:\\Users\\musai\\OneDrive\\Desktop\\Customer Acqusition.csv")
spend=pd.read_csv("C:\\Users\\musai\\OneDrive\\Desktop\\spend.csv")
repay=pd.read_csv("C:\\Users\\musai\\OneDrive\\Desktop\\Repayment.csv")

print(customer.head())
print(spend.head())
print(repay.head())

print(customer.shape)
print(repay.shape)
print(spend.shape)

customer.isnull().sum()
spend.isnull().sum()
repay.isnull().sum()

repay.dropna(inplace=True)
print(repay.isnull().sum())

#1
'''a'''
mean_original = customer["Age"].mean()
print("The mean of Age column is",mean_original)

#replacing age less than 18 with mean of age values
customer.loc[customer["Age"] < 18,"Age"] = customer["Age"].mean()
mean_new = customer["Age"].mean()
print("The new mean of Age column is",mean_new)

customer.loc[customer["Age"] < 18,"Age"]

'''b'''
#merging customer and spend table on the basis of "Customer" column
customer_spend = pd.merge(left=customer,right=spend,on="Customer",how="inner")
print(customer_spend.head())

#all the customers whose spend amount is more than the limit,replacing with 50% of that customer’s limit
print(customer_spend[customer_spend["Amount"] > customer_spend['Limit']])

#if customer's spend amount is more than the limit,replacing with 50% of that customer’s limit
customer_spend.loc[customer_spend["Amount"] > customer_spend["Limit"],"Amount"] = (50 * customer_spend["Limit"]).div(100)
#there are no customers left whose spend amount is more than the limit
print(customer_spend[customer_spend["Amount"] > customer_spend['Limit']])


'''c'''
#merging customer and spend table on the basis of "Customer" column
customer_repay = pd.merge(left=repay,right=customer,on="Customer",how="inner")

#all the customers where repayment amount is more than the limit.
print(customer_repay[customer_repay["Amount"] > customer_repay["Limit"]])

#customers where repayment amount is more than the limit, replacing the repayment with the limit.
customer_repay.loc[customer_repay["Amount"] > customer_repay["Limit"],"Amount"] = customer_repay["Limit"]
#there are no customers left where repayment amount is more than the limit.
print(customer_repay[customer_repay["Amount"] > customer_repay["Limit"]])


# 2
'''a'''
distinct_customers = customer["Customer"].nunique()
print("Number of distinct customers are",distinct_customers)

'''b'''
#customers from different segments
print(customer["Segment"].value_counts())

distinct_categories = customer["Segment"].nunique()
print("Number of distinct categories are",distinct_categories)

plt.figure(figsize=(8,6))
sns.countplot('Segment',data=customer)
plt.show()

'''c'''
#converting Month column of "spend" table to date time format
spend['Month'] = pd.to_datetime(spend['Month'])
print(spend.head(2))

#creating new columns which show "Month" and "Year"
spend['Monthly'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
spend['Yearly'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))
print(spend.head(2))

#grouping the dataset based on 'Yearly' and 'monthly'
customer_spend_group= round(spend.groupby(['Yearly','Monthly']).mean(),2)
print(customer_spend_group)

'''d'''
repay["Month"] = pd.to_datetime(repay["Month"])
print(repay.head(2))
repay['Monthly'] = repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
repay['Yearly'] = repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))
#grouping the dataset based on 'Yearly' and 'monthly'
customer_repay_group= round(repay.groupby(['Yearly','Monthly']).mean(),2)
print(customer_repay_group)

'''e'''
#merging all the three tables. Alreaady merged customer and spend table in 'customer_spend'. Using "customer_spend" and "repay"
#table to form the final "customer_spend_repay" table
customer_spend_repay = pd.merge(left=customer_spend,right=repay,on="Customer",how="inner")
print(customer_spend_repay.head(2))

# renaming the columns for clearity
customer_spend_repay.rename(columns={"Amount_x":"Spend_Amount","Amount_y":"Repay_Amount"},inplace=True)
print(customer_spend_repay.head())

# grouping the data based on "Yearly","Month_x" columns to get the 'Spend_Amount'and 'Repay_Amount'
interest_group = customer_spend_repay.groupby(["Yearly","Monthly"])['Spend_Amount','Repay_Amount'].sum()
print(interest_group)

# Monthly Profit = Monthly repayment – Monthly spend.
interest_group['Monthly Profit'] = interest_group['Repay_Amount'] - interest_group['Spend_Amount']
print(interest_group)

#interest earned is 2.9% of Monthly Profit
interest_group['Interest Earned'] = (2.9* interest_group['Monthly Profit'])/100
print(interest_group)


'''f'''
#top 5 product types on which customer is spending
print(spend['Type'].value_counts().head())

spend['Type'].value_counts().head(5).plot(kind='bar')
plt.show()


'''g'''
city_spend = customer_spend.groupby("City")["Amount"].sum().sort_values(ascending=False)
print(city_spend)



'''h'''
#grouping data based on "Age Group" and finding the amount spend by each age group and arranging in descending oreder
# age_spend = customer_spend.groupby("Age Group")['Amount'].sum().sort_values(ascending=False)
# print(age_spend)



'''i'''
#grouping based on "Customer" column to find top 10 customers
#customer_repay.groupby("Customer")[["Amount"]].sum().sort_values(by="Amount",ascending=False).head(10)




#3
#converting "Month" column to date time
customer_spend["Month"] = pd.to_datetime(customer_spend["Month"])
#creating new column "year"
customer_spend['Year'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))
print(customer_spend.head(2))

customer_spend_pivot = pd.pivot_table(data = customer_spend,index=["City","Year"],columns='Product',aggfunc="sum",values="Amount")
print(customer_spend_pivot)

customer_spend_pivot.plot(kind="bar",figsize=(16,4),width=0.6)
plt.ylabel("Spend Amount")
plt.title("Amount spended by customers according to year and city")
plt.show()




#4
'''a) Monthly comparison of total spends, city wise'''
customer_spend['Monthly'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
#grouping data based on "Monthly" and "City" columns
month_city = customer_spend.groupby(["Monthly","City"])[["Amount"]].sum().sort_index().reset_index()
#creating pivot table based on "Monthly" and "City" columns
month_city =pd.pivot_table(data=customer_spend,values='Amount',index='City',columns='Monthly',aggfunc='sum')
print(month_city)

month_city.plot(kind="bar",figsize=(14,4),width=0.6)
plt.show()



'''b) Comparison of yearly spend on air tickets'''
air_tickets = customer_spend.groupby(["Year","Type"])[["Amount"]].sum().reset_index()
filtered = air_tickets.loc[air_tickets["Type"]=="AIR TICKET"]
print(filtered)

plt.bar(filtered["Year"],height=filtered["Amount"],color="orange")
plt.xlabel("Year")
plt.ylabel("Amount Spent")
plt.title("Comparison of yearly spend on air tickets")
plt.show()


'''c) Comparison of monthly spend for each product (look for any seasonality that exists in terms of spend)'''
#creating pivot table based on "Monthly" and "Product" columns
product_wise = pd.pivot_table(data=customer_spend,index='Product',columns='Monthly',values='Amount',aggfunc='sum')
print(product_wise)

product_wise.plot(kind="bar",figsize=(14,4),width=0.6)
plt.ylabel("Amount Spend")
plt.title("Amount spent monthly on different products")
plt.show()


#5