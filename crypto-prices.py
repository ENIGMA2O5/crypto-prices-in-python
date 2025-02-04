import time
import requests
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Function to fetch cryptocurrency price from Binance
def get_crypto_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {
        'symbol': symbol  # Cryptocurrency symbol (e.g., BTCUSDT, ETHUSDT, XRPUSDT)
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.RequestException as e:
        print(f"Error fetching cryptocurrency price: {e}")
        return None

# Function to display data for a single cryptocurrency
def display_crypto_data(crypto_name, symbol, initial_price):
    current_price = get_crypto_price(symbol)
    if current_price is None:
        return None

    price_change = current_price - initial_price
    percentage_change = (price_change / initial_price) * 100

    # Determine color for price change
    price_change_color = Fore.GREEN if price_change >= 0 else Fore.RED

    # Print current price, change, and percentage change (4 decimal places)
    print(f"\n{crypto_name} Price: ${current_price:.4f}")
    print(f"Price Change Since Start: {price_change_color}${price_change:+.4f} ({percentage_change:+.4f}%)")

    return current_price

# Main function
def main():
    # Prompt user to select a cryptocurrency or all
    print("Select a cryptocurrency to track:")
    print("1. Bitcoin (BTC)")
    print("2. Ethereum (ETH)")
    print("3. XRP")
    print("4. Solana (SOL)")
    print("5. Dogecoin (DOGE)")
    print("6. Track All (BTC, ETH, XRP, SOL, DOGE)")
    
    choice = input("Enter the number corresponding to your choice (1, 2, 3, 4, 5, or 6): ").strip()

    # Map user choice to cryptocurrency symbols
    if choice == "1":
        symbols = [("Bitcoin", "BTCUSDT")]
    elif choice == "2":
        symbols = [("Ethereum", "ETHUSDT")]
    elif choice == "3":
        symbols = [("XRP", "XRPUSDT")]
    elif choice == "4":
        symbols = [("Solana", "SOLUSDT")]
    elif choice == "5":
        symbols = [("Dogecoin", "DOGEUSDT")]
    elif choice == "6":
        symbols = [
            ("Bitcoin", "BTCUSDT"),
            ("Ethereum", "ETHUSDT"),
            ("XRP", "XRPUSDT"),
            ("Solana", "SOLUSDT"),
            ("Dogecoin", "DOGEUSDT")
        ]
    else:
        print("Invalid choice. Exiting.")
        return

    # Fetch initial prices for selected cryptocurrencies
    initial_prices = {}
    for crypto_name, symbol in symbols:
        initial_price = get_crypto_price(symbol)
        if initial_price is None:
            print(f"Failed to fetch initial {crypto_name} price. Skipping.")
            continue
        initial_prices[symbol] = initial_price
        print(f"\nInitial {crypto_name} Price: ${initial_price:.4f}")

    while True:
        time.sleep(5)  # Fetch prices every 5 seconds
        print("\n" + "=" * 50)  # Separator for clarity
        for crypto_name, symbol in symbols:
            if symbol not in initial_prices:
                continue  # Skip if initial price wasn't fetched
            current_price = display_crypto_data(crypto_name, symbol, initial_prices[symbol])
            if current_price is not None:
                initial_prices[symbol] = current_price  # Update initial price for next iteration

if __name__ == "__main__":
    main()
