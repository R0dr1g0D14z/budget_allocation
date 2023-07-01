# Budget Allocation Flask API

This is a Flask API that determines the allocation of budget between two channels, A and B, based on their latest prices and a metric called Relative Price Strength (RPS), calculated as the natural logarithm of the ratio of the prices of channels A and B.

The RPS provides an indication of which channel is performing better price-wise. A positive RPS suggests that channel A's price is outperforming channel B's price, and conversely, a negative RPS suggests that channel B's price is outperforming channel A's price.

The RPS is then averaged over a lookback window (e.g., the last three prices) to help filter out short-term price fluctuations and highlight longer-term trends.

By using a moving average of RPS, the strategy is less sensitive to sudden price changes and more attuned to longer-term trends. However, the allocation can still adjust dynamically as the trend changes. This is crucial for leveraging the best performing channel while protecting from sudden price shifts in either of the channels.

This average RPS is then used to classify into different allocation bands, each indicating a different state of relative price performance and dictating a different allocation of budget between the two channels.

- __A HEAVY__: Channel A's price performance is significantly better than that of channel B. Hence, a larger portion of the budget should be allocated to A.
- __A LIGHT__: Channel A's price performance is slightly better than that of channel B. A somewhat larger portion of the budget should be allocated to A.
- __EQUAL__: Channels A and B perform similarly. Hence, the budget is split equally.
- __B LIGHT__: Channel B's price performance is slightly better than that of channel A. A somewhat larger portion of the budget should be allocated to B.
- __B HEAVY__: Channel B's price performance is significantly better than that of channel A. Hence, a larger portion of the budget should be allocated to B.

These allocation bands provide a framework for adapting the budget allocation strategy to different market conditions. However, it's crucial that the specific ranges of RPS corresponding to each band and the allocation ratios within each band, as well as the lenght of the lookback window, are  thoroughly backtested with actual campaign data. Backtesting allows for an assessment of the strategy's performance under realistic conditions and enables fine-tuning of these framework settings to achieve optimal results.

## Prerequisites

This project requires Python 3.7 or later and the following Python libraries installed:

- Flask
- numpy
- pandas

## File Descriptions

- `app.py`: This is the main file that runs the Flask server and handles the API endpoints.
- `price_streams.py`: This file simulates price trends for two channels (A and B) over 30 units of time, calculates budget allocations and results for both flat and optimized strategies, and finally compares the performance of these two strategies.

## Running the server

In a terminal or command window, navigate to the top-level project directory (that contains this README) and run the following command:

`python app.py`

This will start the Flask server on your local machine, and it will listen for incoming connections at `http://localhost:5000`.

## API Endpoints

The server has one endpoint: 

### POST /allocate

This endpoint accepts a JSON object that includes two arrays of prices for channels A and B, respectively. The length of these arrays represents the number of time units used in the lookback window for calculating the average Relative Price Strength (RPS). The endpoint then returns the optimal allocation of the budget between the two channels, based on this average RPS.

### Example request

<pre>curl -X POST -H "Content-Type: application/json" -d '{"prices_a": [1.00, 1.20, 1.10], "prices_b": [1.30, 1.35, 1.25]}' http://localhost:5000/allocate</pre>

### Example response

The endpoint responds with a JSON object containing one key: `allocation`. The value of this key is a tuple of two numbers indicating the allocation of budget between channel A and channel B.

<pre>
{
"allocation": [0.75, 0.25]
}
</pre>

This indicates that 75% of the budget should be allocated to channel A and 25% should be allocated to channel B.
