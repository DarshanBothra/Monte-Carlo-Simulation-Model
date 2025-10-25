import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class MonteCarloGBMSimulator:
    def __init__(self, df: pd.DataFrame, initial_capital: float, n_days: int, n_simulations: int, volatility_multiplier: float = 1.0):
        """
        Monte Carlo Simulator using Geometric Brownian Motion (GBM)

        Args:
            strategy_csv (str): Path to CSV file with 'pnl_pct' column (daily return in decimal)
            initial_capital (float): Starting capital for the simulation
            n_days (int): Number of trading days to simulate
            n_simulations (int): Number of Monte Carlo simulation paths
        """
        df = df
        if "pnl_pct" not in df.columns:
            if "close" not in df.columns:
                raise ValueError("CSV must contain either 'pnl_pct' or 'close' column.")
            df["pnl_pct"] = df["close"].pct_change()

        self.returns = df["pnl_pct"].dropna().astype(float)
        self.mu = self.returns.mean()
        self.sigma = self.returns.std() * volatility_multiplier
        self.initial_capital = initial_capital
        self.n_days = n_days
        self.n_simulations = n_simulations

        self.simulated_paths = None

    def simulate(self):
        """
        Run the Monte Carlo simulation using GBM.

        Returns:
            np.ndarray: Simulated capital paths of shape (n_days, n_simulations)
        """
        dt = 1  
        drift = (self.mu - 0.5 * self.sigma**2) * dt
        shock = self.sigma * np.random.randn(self.n_days, self.n_simulations) * np.sqrt(dt)
        log_returns = drift + shock
        cumulative_returns = np.cumsum(log_returns, axis=0)
        price_paths = self.initial_capital * np.exp(cumulative_returns)

        self.simulated_paths = price_paths
        return price_paths

    def plot(self):
        """
        Plot the simulated Monte Carlo paths.
        """
        if self.simulated_paths is None:
            raise ValueError("Run simulate() before plotting.")

        plt.figure(figsize=(12, 6))
        plt.plot(self.simulated_paths, alpha=0.3)
        plt.title("Monte Carlo Simulation (GBM) of Strategy Performance")
        plt.xlabel("Days")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def summary(self):
        """
        Print statistics on the final portfolio values across simulations.
        """
        print("\n========== Simulation Summary ==========\n")
        print(f"Initial Capital: ₹{ self.initial_capital:,.2f}")
        print("Days: ", self.n_days)
        print("Simulations: ", self.n_simulations)
        if self.simulated_paths is None:
            raise ValueError("Run simulate() before summary().")

        final_vals = self.simulated_paths[-1]
        print("\n========== Final Portfolio Value Distribution ==========")
        print(f"Min             : ₹{final_vals.min():,.2f}")
        print(f"Max             : ₹{final_vals.max():,.2f}")
        print(f"Mean            : ₹{final_vals.mean():,.2f}")
        print(f"Std Dev         : ₹{final_vals.std():,.2f}")
        print(f"5th Percentile  : ₹{np.percentile(final_vals, 5):,.2f}")
        print(f"80th Percentile : ₹{np.percentile(final_vals, 80):,.2f}")

if __name__ == "__main__":
    filedirectory = os.path.join(os.path.dirname(__file__), "historical-data")

    current_dir = os.getcwd()
    os.chdir(filedirectory)

    df_list = []
    subfolders = os.listdir()

    for subfolder in subfolders:
        subfolder_path = os.path.join(filedirectory, subfolder)
        if os.path.isdir(subfolder_path):
            parquet_files = [f for f in os.listdir(subfolder_path) if f.endswith('.parquet')]
            for file in parquet_files:
                file_path = os.path.join(subfolder_path, file)
                df = pd.read_parquet(file_path)
                df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)
   
    sim = MonteCarloGBMSimulator(
        df = df,
        initial_capital=25000,
        n_days=252,
        n_simulations=50,
        volatility_multiplier= 0.8
    )

    sim.simulate()
    sim.plot()
    sim.summary()
    os.chdir(current_dir)
