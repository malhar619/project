from flask import Flask, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

def generate_plots(file_name):
    df = pd.read_csv(file_name, thousands=',')

    df['BID QTY'] = pd.to_numeric(df['BID QTY'], errors='coerce')
    df['C BID QTY'] = pd.to_numeric(df['C BID QTY'], errors='coerce')
    df['OI'] = pd.to_numeric(df['OI'], errors='coerce')
    df['C OI'] = pd.to_numeric(df['C OI'], errors='coerce')

    put_call_ratio = df['BID QTY'][10:-10].sum() / df['C BID QTY'][10:-10].sum()
    put_oi_call_oi_ratio = df['OI'][10:-10].sum() / df['C OI'][10:-10].sum()

    return {
        'put_call_ratio': float(put_call_ratio),
        'put_oi_call_oi_ratio': float(put_oi_call_oi_ratio),
    }

def generate_plot(file_name, plot_name):
    df = pd.read_csv(file_name, thousands=',')

    if plot_name == 'oi':
        plot_title = 'C OI vs OI'
        x_data = df['C OI'][50:-10]
        y_data = df['OI'][50:-10]
    elif plot_name == 'volume':
        plot_title = 'C VOLUME vs VOLUME'
        x_data = df['C VOLUME'][50:-10]
        y_data = df['VOLUME'][50:-10]
    else:
        return None

    plt.figure(figsize=(12, 6))
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    plt.title(plot_title)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.grid(True)

    plot_path = f'plots/{plot_name}_plot.png'
    plt.savefig(plot_path)
    plt.close()

    return plot_path





@app.route('/get_nifty_plots')
def get_nifty_plots():
    nifty_plots_data = generate_plots('nifty.csv')
    return jsonify(nifty_plots_data)

@app.route('/get_banknifty_plots')
def get_banknifty_plots():
    banknifty_plots_data = generate_plots('banknifty.csv')
    return jsonify(banknifty_plots_data)

# New route for finnifty.csv
@app.route('/get_finnifty_plots')
def get_finnifty_plots():
    finnifty_plots_data = generate_plots('finnifty.csv')
    return jsonify(finnifty_plots_data)




@app.route('/get_nifty_plot/<plot_name>')
def get_nifty_plot(plot_name):
    plot_path = generate_plot('nifty.csv', plot_name)
    if plot_path:
        return send_file(plot_path, mimetype='image/png')
    else:
        return 'Invalid plot name', 400

@app.route('/get_banknifty_plot/<plot_name>')
def get_banknifty_plot(plot_name):
    plot_path = generate_plot('banknifty.csv', plot_name)
    if plot_path:
        return send_file(plot_path, mimetype='image/png')
    else:
        return 'Invalid plot name', 400

# New route for finnifty.csv
@app.route('/get_finnifty_plot/<plot_name>')
def get_finnifty_plot(plot_name):
    plot_path = generate_plot('finnifty.csv', plot_name)
    if plot_path:
        return send_file(plot_path, mimetype='image/png')
    else:
        return 'Invalid plot name', 400






if __name__ == '__main__':
    app.run(debug=True)