import streamlit as st
import json

st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/web3modal"></script>
<script src="https://cdn.jsdelivr.net/npm/@walletconnect/web3-provider"></script>
<script src="https://cdn.jsdelivr.net/npm/ethereumjs-tx@2.1.2"></script>

<div id="content">
  <button id="connect">Connect Wallet</button>
  <h3 id="account"></h3>
</div>

<script>
  const Web3Modal = window.Web3Modal.default;
  const WalletConnectProvider = window.WalletConnectProvider.default;

  let web3Modal
  let provider;
  let selectedAccount;

  function init() {
    const providerOptions = {
      walletconnect: {
        package: WalletConnectProvider,
        options: {
          infuraId: "0x05EB40D03e2700B4F7551b398952ec61107768C5" // Replace YOUR_INFURA_ID with your actual Infura ID
        }
      }
    };

    web3Modal = new Web3Modal({
      cacheProvider: false,
      providerOptions, // required
      disableInjectedProvider: false,
    });

    document.getElementById('connect').addEventListener('click', onConnect);
  }

  async function onConnect() {
    try {
      provider = await web3Modal.connect();
      await provider.enable();

      const web3 = new Web3(provider);
      const accounts = await web3.eth.getAccounts();
      selectedAccount = accounts[0];
      document.getElementById('account').innerText = 'Connected: ' + selectedAccount;

      // Send account back to python using Streamlit's experimental communication feature
      window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        data: selectedAccount
      }, '*');

    } catch(e) {
      console.error(e);
    }
  }

  window.addEventListener('DOMContentLoaded', init);
</script>
""", unsafe_allow_html=True)

# Use experimental_get_query_params() to retrieve the query parameters
query_params = st.query_params

# Get 'data' parameter value
account_address = query_params.get("data", [None])[0]  # Default to None if 'data' is not present

if account_address:
    st.write(f"MetaMask Account Address: {account_address}")
else:
    st.write("No account address found.")
