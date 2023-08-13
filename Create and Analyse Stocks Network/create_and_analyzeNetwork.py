import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Define the list of companies and their ticker symbols
companies = {
    'Amazon': 'AMZN',
    'Apple': 'AAPL',
    'Exxon': 'XOM',
    'Nike': 'NKE',
    'Pfizer': 'PFE',
    'Tesla': 'TSLA'
}

# Function to collect stock prices
def collect_stock_prices(company_symbol, start_date, end_date):
    data = yf.download(company_symbol, start=start_date, end=end_date, interval='1mo')
    return data['Adj Close']

# Function to create a network graph
def create_stock_network(data):
    G = nx.Graph()
    for company1 in companies:
        for company2 in companies:
            if company1 != company2:
                correlation = data[company1].corr(data[company2])
                G.add_edge(company1, company2, weight=correlation)
                print(company1, company2, correlation)
    return G

# Function to analyze the network and print centrality measures
def analyze_network(graph):
    print("Centrality Measures:")
    degree_centrality = nx.degree_centrality(graph)
    print("Degree Centrality:", degree_centrality)
    closeness_centrality = nx.closeness_centrality(graph)
    print("Closeness Centrality:", closeness_centrality)
    betweenness_centrality = nx.betweenness_centrality(graph)
    print("Betweenness Centrality:", betweenness_centrality)

# Main script
if __name__ == "__main__":
    start_date = "2019-08-01"
    end_date = "2023-08-01"

    stock_prices_data = {}
    for company_name, company_symbol in companies.items():
        stock_prices_data[company_name] = collect_stock_prices(company_symbol, start_date, end_date)

    stock_network = create_stock_network(stock_prices_data)
    # Create a DataFrame with stock prices
    stock_prices_df = pd.DataFrame(stock_prices_data)

    # Calculate the correlation matrix
    correlation_matrix = stock_prices_df.corr()

    # Plot the correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Stock Price Correlation Matrix")
    plt.xlabel("Company")
    plt.ylabel("Company")
    plt.show()

    # Plot the network graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(stock_network)  # Layout for better visualization
    nx.draw(stock_network, pos, with_labels=True, font_size=8, node_size=800, node_color='skyblue', edge_color='gray')
    plt.title("Stock Price Correlation Network")
    plt.show()

    # Analyze the network and print centrality measures
    analyze_network(stock_network)
