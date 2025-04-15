import streamlit as st
import pandas as pd

# ----------------------------
# Function to load & clean data
# ----------------------------
def load_and_clean_excel(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
    return df


# ----------------------------
# Load Excel files
# ----------------------------
transactions = load_and_clean_excel("2024_1.xlsx", "Sheet1")
customers = load_and_clean_excel("CUSTOMER_TABLE NEW.xlsx", "Sheet1")
items = load_and_clean_excel("ITEM_LIST.xlsx", "ITEM_LIST")
locations = load_and_clean_excel("location.xlsx", "Sheet1")

# ----------------------------
# Role selection
# ----------------------------
st.title("🧾 Retail Management Dashboard")

role = st.sidebar.selectbox("Login as", ["Super Admin", "Admin", "Cashier"])

st.success(f"✅ Logged in as {role}")

# ----------------------------
# SUPER ADMIN VIEW
# ----------------------------
if role == "Super Admin":
    st.header("📊 Complete Data Overview")

    with st.expander("🧾 Transactions"):
        st.dataframe(transactions)

    with st.expander("👥 Customers"):
        st.dataframe(customers)

    with st.expander("📦 Items"):
        st.dataframe(items)

    with st.expander("📍 Locations"):
        st.dataframe(locations)

# ----------------------------
# ADMIN VIEW
# ----------------------------
elif role == "Admin":
    st.header("📋 Transactions Overview")

    st.subheader("🔍 All Transactions")
    st.dataframe(transactions[['TID', 'CID', 'IID', 'TOTAL_PRICE', 'DATE']])

    st.subheader("📦 Items Summary")
    st.dataframe(items[['ITEM_ID', 'ITEM_NAME', 'ITEM__PRICE', 'GROUP']])

    st.subheader("👥 Customer Info")
    st.dataframe(customers[['CUSTOMER_ID', 'CUSTOMER_PH_NUMBER']])

# ----------------------------
# CASHIER VIEW
# ----------------------------
elif role == "Cashier":
    st.header("💵 Cashier's View")

    st.subheader("Add New Transaction")

    # Form to add a new transaction
    with st.form("add_txn"):
        tid = st.number_input("Transaction ID", min_value=1)
        cid = st.selectbox("Customer ID", customers['CUSTOMER_ID'])
        iid = st.selectbox("Item ID", items['ITEM_ID'])
        iqnt = st.number_input("Quantity", min_value=1)
        ip = items[items['ITEM_ID'] == iid]['ITEM__PRICE'].values[0]
        total_price = ip * iqnt
        submit = st.form_submit_button("Submit")

    if submit:
        # Simulating saving the transaction to the existing dataset
        new_transaction = {
            "TID": tid,
            "CID": cid,
            "IID": iid,
            "QUANTITY": iqnt,
            "TOTAL_PRICE": total_price,
            "DATE": pd.to_datetime('today')
        }
        transactions = transactions.append(new_transaction, ignore_index=True)
        st.success(f"✅ Transaction Recorded: TID={tid}, Total={total_price}")

    # Show Today's Transactions
    st.subheader("🧾 Today's Transactions")
    today = pd.to_datetime('today').normalize()
    transactions['DATE'] = pd.to_datetime(transactions['DATE'])

    today_trans = transactions[transactions['DATE'].dt.date == today.date()]
    st.dataframe(today_trans[['TID', 'CID', 'IID', 'TOTAL_PRICE', 'DATE']])
