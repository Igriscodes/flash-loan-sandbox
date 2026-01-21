# Flash Loan Sandbox

**Flash Loan Sandbox** is an interactive web application designed to show the world of decentralized finance (DeFi). It provides a risk-free environment to visualize how atomic transactions work, with both legitimate arbitrage opportunities and common smart contract exploit vectors.

## Features

* **Real-time Liquidity Tracking**: Monitor a mock liquidity pool that reacts to your transactions.
* **Scenario Simulation**: Toggle between different DeFi use cases:
* **Legitimate Arbitrage**: Profit from price differences across DEXs.
* **Collateral Swap**: Atomically swap underlying assets.
* **Price Manipulation**: See how bad actors attempt to trick oracles.
* **Reentrancy Attack**: Visualizes how "guards" prevent recursive borrowing.
* **Atomic Rollback Engine**: Demonstrates the "all-or-nothing" nature of flash loans—if the debt isn't repaid with interest, the entire transaction reverts.
* **Transaction Logging**: A detailed, time-stamped log of every step in the transaction lifecycle.

## Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Igriscodes/flash-loan-sandbox.git
cd flash-loan-sandbox
```


2. **Install dependencies:**
```bash
pip install streamlit pandas
```


3. **Run the application:**
```bash
streamlit run app.py
```

## How to Use

1. **Adjust Parameters**: Use the sliders to set your loan amount, the interest rate charged by the pool, and your expected profit margin.
2. **Select Scenario**: Choose a "Legitimate" or "Exploit" scenario to see how the logic branches.
3. **Execute**: Click **Execute Transaction**.
4. **Analyze**: Review the **Transaction Log** to see if the repayment was successful or if the state was rolled back due to a shortfall.

## Guide

To see how atomic transactions behave, try these specific slider configurations. Remember: A transaction only **Succeeds** if your `User Balance`  $\ge$ `Required Repayment`.

### 1. Legitimate Arbitrage

* **Success ✅**:
* **Parameters**: Loan: `$100k` | Interest: `0.05%` | Profit: `2.0%`.
* **Why**: Your 2% profit ($2,000) easily covers the $50 interest fee.


* **Failure ❌**:
* **Parameters**: Loan: `$100k` | Interest: `1.50%` | Profit: `1.0%`.
* **Why**: The profit ($1,000) is less than the interest ($1,500). The transaction reverts.



### 2. Exploit: Price Manipulation

* **Success ✅**:
* **Parameters**: Loan: `$100k` | Interest: `0.10%` | Profit: `20.0%`.
* **Why**: The code hardcodes a **15% manipulation cost**. By setting the profit to 20%, you cover the cost (15%) and the interest (0.1%), leaving a net gain.


* **Failure ❌**:
* **Parameters**: Loan: `$100k` | Interest: `0.10%` | Profit: `5.0%`.
* **Why**: A 5% profit cannot cover the 15% manipulation cost programmed into this scenario.



### 3. Exploit: Reentrancy Attack

* **Success ✅ (Neutral)**:
* **Parameters**: Loan: `$100k` | Interest: **`0.00%`** | Profit: `Any`.
* **Why**: The code triggers a **Reentrancy Guard**, setting your profit to $0. By setting interest to 0%, you can exactly repay the principal, allowing the transaction to "commit" without profit.


* **Failure ❌**:
* **Parameters**: Loan: `$100k` | Interest: `0.01%` | Profit: `Any`.
* **Why**: Since the attack is blocked (Profit = $0), you don't have the extra $10 to pay the interest. The transaction fails.



### 4. Collateral Swap

* **Success ✅ (Neutral)**:
* **Parameters**: Loan: `$100k` | Interest: **`0.00%`** | Profit: `Any`.
* **Why**: Collateral swaps in this code are "net-zero" events (User Balance = Loan Amount). With 0% interest, you break even and the transaction commits.


* **Failure ❌**:
* **Parameters**: Loan: `$100k` | Interest: `0.50%` | Profit: `Any`.
* **Why**: You have no profit to pay the $500 interest fee, triggering a rollback.

### Quick Reference Table

| Scenario | Goal | Profit Slider | Interest Slider | Result |
| --- | --- | --- | --- | --- |
| **Arbitrage** | Profit | **> Interest %** | < Profit % | **✓ Committed** |
| **Manipulation** | Profit | **> 15.1%** | 0.1% | **✓ Committed** |
| **Reentrancy** | Pass | Any % | **0.0%** | **✓ Committed** |
| **Any** | Revert | **< Interest %** | > Profit % | **❌ Reverted** |

## Acknowledgments

- I would like to thank **Claude 4.5 Sonnet** for its assistance in designing and optimizing the code.
- I would also like to thank Streamlit for providing the framework used to build this interactive sandbox.

## Disclaimer

This project is for **educational purposes only**. It is a simulation of DeFi logic and does not interact with any real blockchain networks or financial protocols.

## License
[GNU Lesser General Public License v2.1](LICENSE) - Feel free to use and modify
