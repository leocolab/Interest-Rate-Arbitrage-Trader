import pandas as pd
import numpy as np
from poly import polyOddsForNoChange
from bondMktOdds import bondOddsForNoChange
from datetime import datetime
from inputs import dateTime, buyTokenId, sellTokenId
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
pd.set_option('display.max_rows', None)      # Show all rows

# Load the CSV file
file_path = 'Historical Data.csv'
data = pd.read_csv(file_path)
data.columns = ['Days_Out', 'Spread', 'Abs_Value']  # Renaming columns for simplicity

# Creating a Cycle ID based on resets at Days_Out = 0
data['Cycle_ID'] = (data['Days_Out'] == 0).cumsum()

# Calculating historical rolling volatility within each cycle
# Rolling volatility based on absolute values
rolling_window = 5

# Calculate rolling volatility
for cycle in data['Cycle_ID'].unique():
    mask = data['Cycle_ID'] == cycle
    data.loc[mask, 'Rolling_Volatility'] = data.loc[mask, 'Abs_Value'].rolling(window=rolling_window).std()

# Calculate coefficient to multiply Days_Out to predict expected rolling volatility
X = data['Days_Out'].values.reshape(-1, 1)
y = data['Rolling_Volatility'].values

# Fit linear regression model
from sklearn.linear_model import LinearRegression
model = LinearRegression()
filtered_data = data.dropna(subset=['Rolling_Volatility']) #Dropping NAN values
X = filtered_data['Days_Out'].values.reshape(-1, 1)
y = filtered_data['Rolling_Volatility'].values
model.fit(X, y)

# Coefficient for expected rolling volatility
volatility_coefficient = model.coef_[0]

# Weight the Z-score based on expected volatility
mean_value = 0  # Use 0 as mean for Z-score calculation
stdev_value = np.std(data['Spread'])

# Calculate expected volatility from days out
expected_volatility = volatility_coefficient * data['Days_Out']

# Adjust Z-score using expected volatility weighting and explore historical data; this helps us decide the z-score threshold
z_scores = (data['Spread'] - mean_value) / stdev_value
weighted_z_scores = z_scores * (1 + (expected_volatility/32))

# Set Variance Threshold
zScoreThresh = 1

# Calculate z-score of the current spread
currentDate = datetime.today().date()
futureDate = datetime(int(dateTime[8:12]), datetime.strptime(dateTime[0:3], "%b").month, int(dateTime[4:6])).date()
currentSpread = bondOddsForNoChange - polyOddsForNoChange
currentDaysOut = (futureDate - currentDate).days

currentZScore = (currentSpread - mean_value) / stdev_value
currentExpectedVolatility = currentDaysOut * volatility_coefficient
weightedZScore = currentZScore * (1 + (currentExpectedVolatility/32))

# Make trading decision (buy or sell polymarket bet 'No Change')
buy = False # To bet on no rate change
sell = False # To sell is really to buy the inverse (to bet on a rate change)
if weightedZScore > 1:
    buy = True
elif weightedZScore < 1:
    sell = True

# Place Poly Market Order
host: str = ""
key: str = ""
chain_id: int = 137

# Initialization of a client that trades directly from an EOA
client = ClobClient(host, key=key, chain_id=chain_id)

if buy == True or sell == True:
    if buy:
        price = polyOddsForNoChange
        tokenId = buyTokenId
    if sell:
        price = 100 - polyOddsForNoChange
        tokenId = sellTokenId
    # Create and sign a limit order buying 1000 tokens of 'No Change' or 'X% Change' at current market prices
    order_args = OrderArgs(
        price=price,
        size=1000.0,
        side=BUY,
        token_id=tokenId,
    )
    signed_order = client.create_order(order_args)

    ## GTC Order
    resp = client.post_order(signed_order, OrderType.GTC)
    print(resp)
