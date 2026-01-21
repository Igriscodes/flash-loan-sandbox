import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Flash Loan Sandbox", layout="wide")

if 'pool_balance' not in st.session_state:
    st.session_state.pool_balance = 1000000
    st.session_state.initial_balance = 1000000
    st.session_state.user_profit = 0
    st.session_state.transaction_history = []
    st.session_state.logs = []

def log(message, type="info"):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append({"time": timestamp, "message": message, "type": type})

def execute_flash_loan(loan_amount, interest_rate, arb_profit_pct, scenario):
    st.session_state.logs = []
    
    log(f"INITIATING FLASH LOAN", "info")
    log(f"Loan Amount: ${loan_amount:,.0f}", "info")
    
    if loan_amount > st.session_state.pool_balance:
        log(f"❌ INSUFFICIENT LIQUIDITY IN POOL", "error")
        log(f"Available: ${st.session_state.pool_balance:,.0f}", "error")
        return False
    
    temp_pool = st.session_state.pool_balance
    temp_pool -= loan_amount
    log(f"✓ Borrowed ${loan_amount:,.0f} from pool", "success")
    log(f"Pool Balance: ${temp_pool:,.0f}", "info")
    
    time.sleep(0.3)
    
    if scenario == "Legitimate Arbitrage":
        profit = loan_amount * (arb_profit_pct / 100)
        log(f"EXECUTING ARBITRAGE", "info")
        log(f"Buy low on DEX A → Sell high on DEX B", "info")
        log(f"✓ Arbitrage Profit: ${profit:,.0f}", "success")
        user_balance = loan_amount + profit
    elif scenario == "Exploit: Price Manipulation":
        manipulation_cost = loan_amount * 0.15
        profit = loan_amount * (arb_profit_pct / 100)
        log(f"ATTEMPTING PRICE MANIPULATION", "warning")
        log(f"Using flash loan to manipulate oracle price", "warning")
        log(f"Manipulation Cost: ${manipulation_cost:,.0f}", "warning")
        log(f"Extracted Value: ${profit:,.0f}", "warning")
        user_balance = loan_amount + profit - manipulation_cost
    elif scenario == "Exploit: Reentrancy Attack":
        profit = loan_amount * (arb_profit_pct / 100)
        log(f"ATTEMPTING REENTRANCY", "warning")
        log(f"Trying to call borrow() again before repayment...", "warning")
        log(f"REENTRANCY GUARD TRIGGERED", "error")
        user_balance = loan_amount
    else:
        log(f"EXECUTING COLLATERAL SWAP", "info")
        log(f"Repaying debt and swapping collateral atomically", "info")
        user_balance = loan_amount
    
    time.sleep(0.3)
    
    interest = loan_amount * (interest_rate / 100)
    required_repayment = loan_amount + interest
    
    log(f"REPAYMENT CALCULATION", "info")
    log(f"Principal: ${loan_amount:,.0f}", "info")
    log(f"Interest ({interest_rate}%): ${interest:,.0f}", "info")
    log(f"Total Required: ${required_repayment:,.0f}", "info")
    log(f"User Balance: ${user_balance:,.0f}", "info")
    
    time.sleep(0.3)
    
    if user_balance >= required_repayment:
        temp_pool += required_repayment
        net_profit = user_balance - required_repayment
        
        log(f"✓ REPAYMENT SUCCESSFUL", "success")
        log(f"Returned ${required_repayment:,.0f} to pool", "success")
        log(f"🎉 TRANSACTION COMMITTED", "success")
        log(f"Net Profit: ${net_profit:,.0f}", "success")
        
        st.session_state.pool_balance = temp_pool
        st.session_state.user_profit += net_profit
        st.session_state.transaction_history.append({
            "Scenario": scenario,
            "Loan": loan_amount,
            "Interest": interest,
            "Profit": net_profit,
            "Status": "✓ Success"
        })
        return True
    else:
        log(f"❌ REPAYMENT FAILED", "error")
        log(f"Shortfall: ${required_repayment - user_balance:,.0f}", "error")
        log(f"ROLLING BACK TRANSACTION", "error")
        log(f"All state changes reverted", "error")
        
        st.session_state.transaction_history.append({
            "Scenario": scenario,
            "Loan": loan_amount,
            "Interest": interest,
            "Profit": 0,
            "Status": "✗ Reverted"
        })
        return False

st.title("Flash Loan Sandbox")
st.markdown("Interactive demonstration of atomic transactions, arbitrage, and exploit scenarios")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Liquidity Pool")
    pool_pct = (st.session_state.pool_balance / st.session_state.initial_balance) * 100
    st.metric("Pool Balance", f"${st.session_state.pool_balance:,.0f}", 
              f"{pool_pct:.1f}% of initial")
    st.progress(min(pool_pct / 100, 1.0))

with col2:
    st.subheader("Your Profit")
    st.metric("Total Earned", f"${st.session_state.user_profit:,.0f}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Parameters")
    
    loan_amount = st.slider("Loan Amount ($)", 1000, 500000, 100000, 1000)
    interest_rate = st.slider("Interest Rate (%)", 0.0, 2.0, 0.09, 0.01)
    arb_profit = st.slider("Arbitrage Profit (%)", 0.0, 25.0, 1.5, 0.1)
    
    st.subheader("Scenario Selection")
    scenario = st.radio(
        "Choose a scenario:",
        ["Legitimate Arbitrage", 
         "Exploit: Price Manipulation", 
         "Exploit: Reentrancy Attack",
         "Collateral Swap"],
        help="Different use cases and attack vectors"
    )
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Execute Transaction", type="primary", use_container_width=True):
            execute_flash_loan(loan_amount, interest_rate, arb_profit, scenario)
            st.rerun()
    with col_b:
        if st.button("Reset Pool", use_container_width=True):
            st.session_state.pool_balance = st.session_state.initial_balance
            st.session_state.user_profit = 0
            st.session_state.transaction_history = []
            st.session_state.logs = []
            st.rerun()

with col2:
    st.subheader("Transaction Log")
    
    if st.session_state.logs:
        log_container = st.container(height=400)
        with log_container:
            for entry in st.session_state.logs:
                if entry["type"] == "success":
                    st.success(f"[{entry['time']}] {entry['message']}")
                elif entry["type"] == "error":
                    st.error(f"[{entry['time']}] {entry['message']}")
                elif entry["type"] == "warning":
                    st.warning(f"[{entry['time']}] {entry['message']}")
                else:
                    st.info(f"[{entry['time']}] {entry['message']}")
    else:
        st.info("Configure parameters and execute a transaction to see logs")

st.divider()

if st.session_state.transaction_history:
    st.subheader("Transaction History")
    df = pd.DataFrame(st.session_state.transaction_history)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    success_count = len([t for t in st.session_state.transaction_history if "Success" in t["Status"]])
    failed_count = len(st.session_state.transaction_history) - success_count
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Successful", success_count)
    with col2:
        st.metric("Reverted", failed_count)
    with col3:
        success_rate = (success_count / len(st.session_state.transaction_history)) * 100
        st.metric("Success Rate", f"{success_rate:.0f}%")

with st.expander("How Flash Loans Work"):
    st.markdown("""
    **Flash Loans** are uncollateralized loans that must be borrowed and repaid within a single atomic transaction.
    
    **Key Concepts:**
    - **Atomic Transactions**: All operations succeed or all fail together
    - **No Collateral**: Borrow millions without upfront capital
    - **Same Block**: Everything happens in one transaction block
    
    **Legitimate Uses:**
    - Arbitrage between exchanges
    - Collateral swapping
    - Debt refinancing
    
    **Exploit Scenarios:**
    - Price oracle manipulation
    - Reentrancy attacks
    - Governance manipulation
    
    **Protection Mechanisms:**
    - Reentrancy guards
    - Oracle price checks
    - Transaction rollback on failure
    """)

st.caption("Educational demonstration only. Not financial advice.")
