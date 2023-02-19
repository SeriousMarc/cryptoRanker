from typing import List, Dict
import pandas as pd
import requests
import streamlit as st


class CryptoRanking:
    def __init__(self, token_data: List[Dict], network_data: List[Dict]):
        self.token_data = token_data
        self.network_data = network_data
        self.df_token = pd.DataFrame(token_data)
        self.df_network = pd.DataFrame(network_data)

    def rank_by_tokenomics(self, num_coins: int) -> List[str]:
        sorted_coins = self.df_token.sort_values(
            by=["market_cap_usd"], ascending=False
        )[:num_coins]
        return sorted_coins["name"].tolist()

    def rank_by_network(self, num_coins: int) -> List[str]:
        sorted_coins = self.df_network.sort_values(
            by=["active_addresses"], ascending=False
        )[:num_coins]
        return sorted_coins["name"].tolist()


@st.cache
def get_data(url: str) -> List[Dict]:
    response = requests.get(url)
    data = response.json()
    return data


def main():
    st.set_page_config(page_title="Crypto Ranking", page_icon=":money_with_wings:")

    token_url = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
    network_url = "https://api.coinlore.net/api/coin/markets/?id=1"

    token_data = get_data(token_url)["data"]
    network_data = get_data(network_url)

    ranking = CryptoRanking(token_data, network_data)

    st.title("Crypto Ranking")

    st.header("Ranking by Tokenomics")
    num_coins = st.slider("Number of coins to show:", 1, 100, 10)
    ranked_coins = ranking.rank_by_tokenomics(num_coins)
    st.write(ranked_coins)

    st.header("Ranking by Network Analysis")
    num_coins = st.slider("Number of coins to show:", 1, 100, 10)
    ranked_coins = ranking.rank_by_network(num_coins)
    st.write(ranked_coins)


if __name__ == "__main__":
    main()
