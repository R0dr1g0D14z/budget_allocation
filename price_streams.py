import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the overall budget
overall_budget = 10

# Generate x values from 0 to 2*pi with 30 evenly spaced samples
x = np.linspace(0, 2*np.pi, 30)

# Generate y values for the sine function within the desired CPC range
min_cpc = 1.00  # Minimum CPC 
max_cpc = 2.50  # Maximum CPC 
cpc_range = max_cpc - min_cpc

# Generate random noise
noise_a = np.random.normal(0, 0.1, len(x))  # noise for Channel A
noise_b = np.random.normal(0, 0.15, len(x))  # noise for Channel B

# Sinusoidal trends with different frequencies
trend_a = np.sin(x*2) * 0.2  # trend for Channel A
trend_b = np.sin(x*1.5) * 0.2  # trend for Channel B

# Generate y values for the sine function and add randomness and trend
price_a = np.sin(x) * (cpc_range/2) + (max_cpc + min_cpc)/2 + noise_a + trend_a

# Generate y values for the function similar to A, add randomness and trend
# Smaller price differences, lower optimization gains
#price_b = np.sin(x) * (cpc_range/2) + (max_cpc + min_cpc)/2 + noise_b + trend_b

# Generate y values for a function dissimilar to A, add randomness and trend
# Bigger price differences, higher optimization gains
price_b = np.cos(x) * (cpc_range/2) + (max_cpc + min_cpc)/2 + noise_b + trend_b

# Create a DataFrame
df = pd.DataFrame({
    'Price A': price_a,
    'Price B': price_b,
    'RPS': np.log(price_a / price_b),
})

# Plot the data
plt.figure(figsize=(8,5))
plt.plot(df['Price A'], label='Price A')
plt.plot(df['Price B'], label='Price B')
plt.xlabel('Sample')
plt.ylabel('Price')
plt.title('Price Trends for Channels A and B')
plt.legend()
plt.grid(True)
plt.show()

def calculate_results(df, alloc='flat'):
    if alloc == 'flat':
        df['Alloc A'] = overall_budget / 2
        df['Alloc B'] = overall_budget / 2
    elif alloc == 'optimized':
        # Define bins and labels for allocation based on average RPS
        bins = [-np.inf, -0.60, -0.10, 0.10, 0.60, np.inf]
        labels = ['A HEAVY', 'A LIGHT', 'EQUAL', 'B LIGHT', 'B HEAVY']
        
        # Calculate the moving average of the previous 3 RPS values
        df['Avg RPS'] = df['RPS'].rolling(window=3, min_periods=1).mean()

        # Assign allocation based on the average RPS
        df['Alloc'] = pd.cut(df['Avg RPS'], bins=bins, labels=labels, include_lowest=True).astype(str)

        # Assigning the allocations based on the 'Alloc' column
        alloc_dict = {
            'A HEAVY': (0.80, 0.20),
            'A LIGHT': (0.75, 0.25),
            'EQUAL':   (0.50, 0.50),
            'B LIGHT': (0.25, 0.75),
            'B HEAVY': (0.20, 0.80)
        }
        df['Alloc A'] = df['Alloc'].map(lambda x: overall_budget * alloc_dict.get(x, (0,0))[0])
        df['Alloc B'] = df['Alloc'].map(lambda x: overall_budget * alloc_dict.get(x, (0,0))[1])
        df.drop('Alloc', axis=1, inplace=True)
    
    df['Results A'] = np.floor(df['Alloc A'] / df['Price A']).astype(int)
    df['Results B'] = np.floor(df['Alloc B'] / df['Price B']).astype(int)
    return df

# Create a copy of the original DataFrame
df_flat = df.copy()
df_opt = df.copy()

# Calculate results for flat and optimized strategies
df_flat = calculate_results(df_flat, alloc='flat')
df_opt = calculate_results(df_opt, alloc='optimized')

# Calculate total Results for each strategy
results_flat_total = df_flat['Results A'].sum() + df_flat['Results B'].sum()
results_opt_total = df_opt['Results A'].sum() + df_opt['Results B'].sum()

# Calculate additional Results achieved by the optimized strategy
additional_results = results_opt_total - results_flat_total

# Calculate the percentage increase in clicks
percentage_increase = (additional_results / results_flat_total) * 100
# Calculate the percentage increase in clicks
percentage_increase = round(percentage_increase, 2)

# Print the results
print("Flat Strategy Results: ", results_flat_total)
print("Optimized Strategy Results: ", results_opt_total)
print("Delta:", additional_results)
print("Percentage Increase: ", percentage_increase, "%")
