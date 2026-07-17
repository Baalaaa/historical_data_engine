import os

import requests
import pandas as pd
from io import StringIO

class ContractGenerator:

    def __init__(self):
        self.base_path = os.getcwd()
        self.folder_name = "Contracts"
        self.nse_folder_name = "NSE"
        self.bse_folder_name = "BSE"
        self.create_folder()
        self.contract_urls = {
            "nse_contract_fo_url" :"https://public.fyers.in/sym_details/NSE_FO.csv",
            "bse_contract_fo_url" : "https://public.fyers.in/sym_details/BSE_FO.csv"
        }
        self.headers = [ "Token", "Description", "Exchange", "Lot_size", "Tick_size", "Reserved",
                         "Trading_hours", "Expiry_date", "Expiry_timestamp", "Symbol", "Segment",
                         "Instrument_type", "Symbol_token", "Underlying", "Underlying_token", "Strike_price",
                         "Option_type", "Isin", "Field1", "Field2", "Field3"
                        ]


    def create_folder(self):
        try:
            folders = [
                self.nse_folder_name,
                self.bse_folder_name
            ]
            base_folder = os.path.join(self.base_path, self.folder_name)
            os.makedirs(base_folder, exist_ok=True)

            for folder in folders:
                os.makedirs(os.path.join(base_folder, folder), exist_ok=True)

        except Exception as e:
            print(f"exception occurred while creating folder: {e} !")



    def fetch_nse_contracts(self) -> pd.DataFrame | None:
        try:
            response = requests.get(self.contract_urls.get("nse_contract_fo_url"))
            print(f"url: {response.url} | Status Code: {response.status_code} !")
            df = pd.read_csv(StringIO(response.text), header=None, names=self.headers)
            nse_contract_df = df[df["Underlying"].isin(["NIFTY", "BANKNIFTY", "FINNIFTY"])]
            path = os.path.join(self.base_path, self.folder_name, self.nse_folder_name)
            nse_contract_df.to_csv(f"{path}/nse_contract_fo.csv", index=False)
            return nse_contract_df

        except Exception as e:
            print(f"exception occurred while fetching nse contracts: {e} !")
            return None



    def fetch_bse_contracts(self) -> pd.DataFrame | None:
        try:
            response = requests.get(self.contract_urls.get("bse_contract_fo_url"))
            print(f"url: {response.url} | Status Code: {response.status_code} !")
            df = pd.read_csv(StringIO(response.text), header=None,  names=self.headers)
            bse_contract_df = df[df["Underlying"].isin(["SENSEX", "BANKEX"])]
            path = os.path.join(self.base_path, self.folder_name, self.bse_folder_name)
            bse_contract_df.to_csv(f"{path}/bse_contract_fo.csv", index=False)
            return bse_contract_df

        except Exception as e:
            print(f"exception occurred while fetching bse contracts: {e} !")
            return None
