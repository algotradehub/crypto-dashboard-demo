import sys

import streamlit as st

from utils import *


def visualize_orderbook(token: str):

    binance_obs = get_binance_orderbook(token)
    binance_bids = binance_obs[binance_obs['side'] == 'buy']
    binance_asks = binance_obs[binance_obs['side'] == 'sell']

    agg_bids = convert_orderbook_tick(binance_bids, 'binance')
    agg_asks = convert_orderbook_tick(binance_asks, 'binance')

    agg_bids_df = pd.DataFrame(agg_bids)
    agg_asks_df = pd.DataFrame(agg_asks)
    print(agg_bids_df)

    agg_bids_df.sort_values(by='price', ascending=False, inplace=True, ignore_index=True)
    agg_asks_df.sort_values(by='price', ascending=True, inplace=True, ignore_index=True)

    st.subheader(f'Aggregated Orderbooks ({token}):')
    st.write(pd.concat([
        agg_bids_df.rename(columns={c: f'{c}_bid' for c in agg_bids_df.columns}),
        agg_asks_df.rename(columns={c: f'{c}_ask' for c in agg_asks_df.columns})],
        axis=1)[['quantity_bid', 'price_bid', 'exchange_bid', 'price_ask', 'quantity_ask', 'exchange_ask']])


if __name__ == '__main__':
    binance_currencies = get_binance_pre_market_currencies()

    # Add a selection button
    selected_token = st.selectbox('Select Token', list(binance_currencies['symbol']))

    # Visualize the selected token
    visualize_orderbook(selected_token)

    st.subheader(f'Binance Pre-market Tokens:')
    st.write(binance_currencies)