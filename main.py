

from contract_generator import ContractGenerator






if __name__ == '__main__':

    contracts_obj = ContractGenerator()
    contracts_obj.fetch_nse_contracts()
    contracts_obj.fetch_bse_contracts()







