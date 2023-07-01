from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/allocate', methods=['POST'])
def allocate_budget():
    data = request.get_json()
    prices_a = data['prices_a']
    prices_b = data['prices_b']

    df = pd.DataFrame({
        'Price A': prices_a,
        'Price B': prices_b,
        'RPS': np.log(np.array(prices_a) / np.array(prices_b)),
    })

    bins = [-np.inf, -0.60, -0.10, 0.10, 0.60, np.inf]
    labels = ['A HEAVY', 'A LIGHT', 'EQUAL', 'B LIGHT', 'B HEAVY']
    df['Avg RPS'] = df['RPS'].rolling(window=3, min_periods=1).mean()
    df['Alloc'] = pd.cut(df['Avg RPS'], bins=bins, labels=labels, include_lowest=True).astype(str)

    alloc_dict = {
        'A HEAVY': (0.80, 0.20),
        'A LIGHT': (0.75, 0.25),
        'EQUAL':   (0.50, 0.50),
        'B LIGHT': (0.25, 0.75),
        'B HEAVY': (0.20, 0.80)
    }
    
    allocation = alloc_dict.get(df['Alloc'].iloc[-1], (0,0))
    return jsonify({'allocation': allocation})

if __name__ == '__main__':
    app.run(debug=True)
