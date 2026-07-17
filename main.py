import time

import pandas as pd

from contract_generator import ContractGenerator
from fetch_historical_data import FetchHistoricalData





if __name__ == '__main__':

    contracts_obj = ContractGenerator()
    nse_df = contracts_obj.fetch_nse_contracts()
    bse_df = contracts_obj.fetch_bse_contracts()

    fetch_hist_obj = FetchHistoricalData()
    # fetch_hist_obj.fetch_historical_data(df=nse_df, start_date="2026-04-01", end_date="2026-06-30")
    # fetch_hist_obj.fetch_historical_data(df=bse_df, start_date="2026-04-01", end_date="2026-06-30")

    # fetch_hist_obj.testing_historical_data(symbol="NSE:NIFTY30DEC24000CE" , start_date="2026-04-01", end_date="2026-06-30")

    for row in nse_df.itertuples():
        fetch_hist_obj.fetch_historical_data_2(symbol=row.Symbol, expiry_date=row.Expiry_date, underlying=row.Underlying, start_date="2026-04-01", end_date="2026-06-30")
        time.sleep(2)
