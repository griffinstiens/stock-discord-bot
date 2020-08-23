# Discord Bot: Stonks

Creating a discord bot that will have the following features (and more potentially):

- Retrieve individual ticker data on command (includes: current price, high/low for the day)
`!stonks [ticker_name] [ticker_current_price] [ticker_high] [ticker_low]`
- Create a personal watchlist that can keep track of a list of stocks, be frequently backing up that data into a database, and when desired the bot can pull all relevant data and display via direct message to the user
`!stonks watchlist most_recent`
- `most_recent` can pull the most recently backed up data from the database - What we can then do is provide another parameter that can display, say the last 15 back ups and you can pick which one you want to view
- Potential for more detail - Using Pandas, NumPy and Matplotlib we can write a cron job that will every 2 weeks (or whatever) back up all of the data for a specific user into a CSV. Then what I can do is use my Jupyter notebook code I already have, and maybe once a month that watchlist will return a report with a graph that shows you how particular tickers have been doing over time.
