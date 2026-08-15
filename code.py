import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv('customer_shopping_behavior.csv')
print(df.head()) #used for checking the first 5 rows of the dataset
print(df.info()) #used for checking the data types and null values in the dataset
#  #   Column                  Non-Null Count  Dtype  
# ---  ------                  --------------  -----  
#  0   Customer ID             3900 non-null   int64  
#  1   Age                     3900 non-null   int64  
#  2   Gender                  3900 non-null   object 
#  3   Item Purchased          3900 non-null   object 
#  4   Category                3900 non-null   object 
#  5   Purchase Amount (USD)   3900 non-null   int64  
#  6   Location                3900 non-null   object 
#  7   Size                    3900 non-null   object 
#  8   Color                   3900 non-null   object 
#  9   Season                  3900 non-null   object 
#  10  Review Rating           3863 non-null   float64
#  11  Subscription Status     3900 non-null   object 
#  12  Shipping Type           3900 non-null   object 
#  13  Discount Applied        3900 non-null   object 
#  14  Promo Code Used         3900 non-null   object 
#  15  Previous Purchases      3900 non-null   int64  
#  16  Payment Method          3900 non-null   object 
#  17  Frequency of Purchases  3900 non-null   object 
# dtypes: float64(1), int64(4), object(13)
# memory usage: 548.6+ KB
# None

print(df.describe()) #used for checking the statistical summary of the dataset
#        Customer ID          Age  Purchase Amount (USD)  Review Rating  Previous Purchases
# count  3900.000000  3900.000000            3900.000000    3863.000000         3900.000000
# mean   1950.500000    44.068462              59.764359       3.750065           25.351538
# std    1125.977353    15.207589              23.685392       0.716983           14.447125
# min       1.000000    18.000000              20.000000       2.500000            1.000000
# 25%     975.750000    31.000000              39.000000       3.100000           13.000000
# 50%    1950.500000    44.000000              60.000000       3.800000           25.000000
# 75%    2925.250000    57.000000              81.000000       4.400000           38.000000
# max    3900.000000    70.000000             100.000000       5.000000           50.000000

print(df.describe(include='all')) #used for checking the statistical summary of the dataset including categorical columns
                                # it's the string columns that are included in the summary, and the count, unique, top, and freq values are displayed for those columns.

print(df.isnull().sum()) #used for checking the number of null values in each column of the dataset
# [11 rows x 18 columns]
# Customer ID                0
# Age                        0
# Gender                     0
# Item Purchased             0
# Category                   0
# Purchase Amount (USD)      0
# Location                   0
# Size                       0
# Color                      0
# Season                     0
# Review Rating             37
# Subscription Status        0
# Shipping Type              0
# Discount Applied           0
# Promo Code Used            0
# Previous Purchases         0
# Payment Method             0
# Frequency of Purchases     0
# dtype: int64

df['Review Rating']= df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.mean())) 
#used for filling the null values in the 'Review Rating' column with the mean value of the respective category
print(df.isnull().sum())

#convert column names to lower case and replace spaces with underscores
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
print(df.columns)

#change column name 'purchase_amount_(usd)' to 'purchase_amount'
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

# create column age_group using qcut
lables=['Younge Age','Adult','Middle Age','Senior']
df['age_group'] = pd.qcut(df['age'],q=4,labels=lables)
print(df[['age','age_group']].head(10))
#   age   age_group
# 0   55  Middle Age
# 1   19  Younge Age
# 2   50  Middle Age
# 3   21  Younge Age
# 4   45  Middle Age
# 5   46  Middle Age
# 6   63      Senior
# 7   27  Younge Age
# 8   26  Younge Age
# 9   57  Middle Age

# Create column purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))
#  purchase_frequency_days frequency_of_purchases
# 0                       14            Fortnightly
# 1                       14            Fortnightly
# 2                        7                 Weekly
# 3                        7                 Weekly
# 4                      365               Annually
# 5                        7                 Weekly
# 6                       90              Quarterly
# 7                        7                 Weekly
# 8                      365               Annually
# 9                       90              Quarterly

# Check if the values in the 'discount_applied' and 'promo_code_used' columns are the same
(df['discount_applied'] == df['promo_code_used']).all()
# True

# Since the values in the 'discount_applied' and 'promo_code_used' columns are the same,
# we can drop one of them to avoid redundancy. In this case, we will drop the 'promo_code_used' column.
df = df.drop('promo_code_used', axis=1)
print(df.columns)

#load the data into SQL Server database using SQLAlchemy
server = "LAPTOP-D83L8KGR"
database = "DataAnalyst"

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

df.to_sql(
    "customer_data",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")