# Solana Wallet Tracker

This Python script monitors transactions for a specific Solana wallet using the Helius WebSocket API. It identifies and logs transaction details, including token transfers and swaps.

## Features

- Tracks real-time transactions for a specified Solana wallet.
- Detects token transfers and swap transactions.
- Parses transaction data to extract relevant information.
- Logs transaction details, including amount, token, and wallet addresses.
- Automatically reconnects in case of WebSocket disconnection.

## Requirements

- Python 3.x
- `asyncio` library
- `websockets` library
- `requests` library
- A valid Helius API key

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-repo/Solana-Wallet-Tracker.git
    cd Solana-Wallet-Tracker
    ```
2. **Install the required Python packages:**
    ```sh
    pip install requests websockets solana
    pip install solana asyncio requests base58
    ```

## Usage

1. **Set up your Helius API key:**
    - Replace `API_KEY` in the script with your actual Helius API key.
2. **Specify the wallet to track:**
    - Replace `TRACKED_WALLET` in the script with the desired Solana wallet address.
3. **Run the script:**
    ```sh
    python Wallet_Tracker_Solana.py
    ```

## Notes

- Ensure your system has internet access to communicate with the Helius API.
- The script listens for new transactions and automatically processes them in real-time.
- Transactions are categorized as transfers or swaps, and details are logged accordingly.

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements or bug fixes.

## License

This project is free to use and modify.

## Disclaimer

This script is for educational and informational purposes only. Users are responsible for ensuring compliance with applicable regulations and API terms of use.

## Contact

For any questions or suggestions, please open an issue.

