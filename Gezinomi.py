import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
df = pd.read_excel('gezinomi.xlsx')
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(df.head())
print(df.shape)
print(df.info())

# Q2: How many unique cities are there? What are their frequencies?
print(df["SaleCityName"].nunique())
print(df["SaleCityName"].value_counts())
# Q3: How many unique Concepts are there?
df["ConceptName"].nunique()
# Q4: How many sales have there been from which Concept?
df["ConceptName"].value_counts()
# Q5: How much was earned in total from sales by cities?
df.groupby("SaleCityName").agg({"Price": "sum"})
# Q6: How much is earned according to concept types?
df.groupby("ConceptName").agg({"Price": "sum"})
# Q7: What are the PRICE averages by city?
df.groupby(by=['SaleCityName']).agg({"Price": "mean"})
# Q8: What are the PRICE averages by concepts?
df.groupby(by=['ConceptName']).agg({"Price": "mean"})
# Q9: What are the PRICE averages in the City-Concept breakdown?
df.groupby(by=["SaleCityName", 'ConceptName']).agg({"Price": "mean"})
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)
df.head(25)
df.tail(25)

# Average prices in the City-Concept-EB Score breakdown
df.groupby(by=["SaleCityName", 'ConceptName', "EB_Score" ]).agg({"Price": ["mean", "count"]})

# Average prices in City-Concept-Season breakdown
df.groupby(by=["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})

df.groupby(by=["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})

# Sorting the output of the City-Concept-Season breakdown by PRICE
# To better see the output from the previous question, apply the sort_values method to PRICE in descending order.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
agg_df.head(20)

# All variables except PRICE in the output of the third question are index names, don't convert these names to variable names
agg_df.reset_index(inplace=True)

#Defining new level based sales and add it as a variable to the dataset and define a variable named sales_level_based and add this variable to the dataset
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)

#SEGMENTATION OF PERSONAS

# Segmentation by Price
# add segments to agg_df with "SEGMENT" naming
# describing segments
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

# Sorting the last df created by price variable
agg_df.sort_values(by="Price")

# In which segment is "ANTALYA_ALL INCLUDED_HIGH" and how much is expected? to find an answer to the question.
new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]