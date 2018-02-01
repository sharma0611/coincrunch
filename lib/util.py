#!/usr/bin/env python3

def create_market_names(coin_list, quotecoin):
    market_names = [bc + "_" + quotecoin for bc in coin_list]
    return market_names

def create_market_symbols(coin_list, quotecoin):
    markets = [bc + "/" + quotecoin for bc in coin_list]
    return markets

