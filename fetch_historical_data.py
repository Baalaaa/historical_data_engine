import os
import csv
import time

import pandas as pd
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

load_dotenv()


class FetchHistoricalData:

    def __init__(self):
        self.payload = {}
        self.resolution = "1"
        self.dateformat = "1"
        self.content_flag = "1"
        self.CLIENT_ID = os.getenv('FYERS_CLIENT_ID')
        self.ACCESS_TOKEN = os.getenv('FYERS_ACCESS_TOKEN')
        self.fyers = fyersModel.FyersModel(client_id=self.CLIENT_ID, token=self.ACCESS_TOKEN, is_async=False, log_path="")


    def fetch_historical_data(self, df: pd.DataFrame, start_date: str, end_date: str) -> None:
        try:
            global exchange

            if df.empty:
                print(f"Dataframe is Empty: {df} !")
                return None

            if "Symbol" not in df.columns:
                print(f"Symbol columns not found for {df.columns} !")
                return None

            if "Underlying" not in df.columns:
                print(f"Underlying columns not found in: {df.columns} !")
                return None

            if "Expiry_date" not in df.columns:
                print(f"Expiry_date columns not found in {df.columns} !")
                return None

            for row in df.itertuples():
                # print(row.Symbol)
                self.data = {
                    "symbol": row.Symbol,
                    "range_from": start_date,
                    "range_to": end_date,
                    "resolution": self.resolution,
                    "date_format": self.dateformat,
                    "cont_flag": self.content_flag,
                }

                response = self.fyers.history(data=self.data)
                # print(response)
                if response.get('S') != "ok":
                    print(f"failed to fetch historical data for : {row.Symbol} !")

                elif response.get("candles"):
                   print(f"no historical data for: {row.Symbol} !")

                elif response.get('s') == "no_data":
                   print(f"no data for this symbol: {row.Symbol} !")
                else:

                    if row.Symbol.startswith("NSE*"):
                        exchange = "NSE"
                    else:
                        exchange = "BSE"

                    os.makedirs(f"Data/{exchange}", exist_ok=True)
                    with open(f"Data/{exchange}/{row.Underlying}_{row.Expiry_date}_.csv", mode="w", newline="") as f:
                        writer = csv.writer(f)

                        writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                        writer.writerows(response.get("candles"))

                    print(f"data fetched successfully for: {row.Symbol} !")
                print(f"{row.Symbol} & {row.Expiry_date}")
                time.sleep(2)
        except Exception as e:
            print(f"exception occurred while fetching historical data: {e} !")
            return None


    def testing_historical_data(self, symbol: str, start_date: str, end_date: str) -> None:
        try:
            self.payload = {
                "symbol": symbol,
                "range_from": start_date,
                "range_to": end_date,
                "resolution": self.resolution,
                "date_format": self.dateformat,
                "cont_flag": self.content_flag,
            }
            response = self.fyers.history(data=self.payload)
            print(response)

        except Exception as e:
            print(f"exception occurred while fetching historical data: {e} !")


    def fetch_historical_data_2(self, symbol: str, start_date: str, end_date: str, expiry_date: str, underlying: str) -> None:
        try:
            global exchange

            self.data = {
                "symbol": symbol,
                "range_from": start_date,
                "range_to": end_date,
                "resolution": self.resolution,
                "date_format": self.dateformat,
                "cont_flag": self.content_flag,
            }

            response = self.fyers.history(data=self.data)

            status = response.get("s")

            if status == "no_data":
                print(f"no historical data for: {symbol} !")
                return None

            if status != "ok":
                print(f"failed to fetch historical data for : {symbol} !")
                return None

            if symbol.startswith("NSE"):
                exchange = "NSE"
            else:
                exchange = "BSE"

            candles = response.get("candles", [])

            filename = f"Data/{exchange}/{underlying}_{expiry_date}_.csv"
            with open(filename, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                writer.writerows(candles)

            print(f"data fetched successfully for: {symbol} && Number of candles: {len(candles)} !")

        except Exception as e:
            print(f"exception occurred while fetching historical data: {e} !")
            return None