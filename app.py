import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="Prisma SASE Policy Exporter", page_icon="🛡️", layout="wide")
st.title("🛡️ Prisma SASE Security Rule Exporter")
st.markdown("This tool authenticates via OAuth2, fetches all rules across multiple pages, and exports them to a clean Excel file.")

# --- Sidebar UI ---
with st.sidebar:
    st.header("1. Authentication")
    client_id = st.text_input("Client ID", help="Paste your Client ID here")
    client_secret = st.text_input("Client Secret", type="password", help="Paste your Client Secret here")
    tsg_id = st.text_input("TSG ID", help="The Tenant Service Group ID")
    
    st.header("2. Search Parameters")
    folder = st.selectbox("Folder", [
        "Shared", "Mobile Users", "Remote Networks", 
        "Service Connections", "Mobile Users Container", 
        "Mobile Users Explicit Proxy"
    ])
    position = st.radio("Rule Position", ["pre", "post"], index=0, help="Fetch rules in the 'pre' or 'post' rulebase")

# --- Logic: Authentication ---
def get_bearer_token(cid, secret, tsg):
    auth_url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
    payload = {
        'grant_type': 'client_credentials',
        'scope': f'tsg_id:{tsg}'
    }
    try:
        response = requests.post(auth_url, data=payload, auth=(cid, secret), timeout=15)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        st.error(f"Authentication Failed: {e}")
        return None

# --- Logic: Data Flattening ---
def flatten_rule_data(data_list):
    """Parses JSON lists into comma-separated strings for Excel readability."""
    flattened = []
    for rule in data_list:
        clean_rule = {}
        for key, value in rule.items():
            # Extract nested profile settings
            if key == "profile_setting" and isinstance(value, dict):
                group = value.get("group", [])
                clean_rule["profile_group"] = ", ".join(group) if isinstance(group, list) else str(group)
            # Convert list fields (source, destination, etc.) to strings
            elif isinstance(value, list):
                clean_rule[key] = ", ".join(map(str, value))
            else:
                clean_rule[key] = value
        flattened.append(clean_rule)
    return flattened

# --- Main Execution ---
if st.button("🚀 Fetch All Rules & Export"):
    if not all([client_id, client_secret, tsg_id]):
        st.warning("Please provide all credentials in the sidebar.")
    else:
        token = get_bearer_token(client_id, client_secret, tsg_id)
        
        if token:
            api_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            
            all_rules = []
            offset = 0
            limit = 200  # API Maximum per page
            
            status_container = st.empty()
            
            with st.spinner("Fetching rules..."):
                while True:
                    params = {
                        "folder": folder,
                        "position": position,
                        "limit": limit,
                        "offset": offset
                    }
                    
                    try:
                        res = requests.get(api_url, headers=headers, params=params, timeout=30)
                        res.raise_for_status()
                        batch = res.json().get("data", [])
                        
                        if not batch:
                            break  # End of data reached
                        
                        all_rules.extend(batch)
                        offset += len(batch)
                        status_container.info(f"Retrieved {len(all_rules)} rules so far...")
                        
                        # Safety break if API returns fewer than the limit (end of list)
                        if len(batch) < limit:
                            break
                            
                    except Exception as e:
                        st.error(f"Error fetching data at offset {offset}: {e}")
                        break
            
            if all_rules:
                # Process and Display
                processed_data = flatten_rule_data(all_rules)
                df = pd.DataFrame(processed_data)
                
                # Reorder columns for a standard firewall rule view
                priority_cols = ['name', 'action', 'source', 'destination', 'application', 'service', 'from', 'to']
                existing = [c for c in priority_cols if c in df.columns]
                others = [c for c in df.columns if c not in existing]
                df = df[existing + others]

                st.success(f"✅ Success! Total rules retrieved: {len(df)}")
                st.dataframe(df.head(20)) # Show preview of first 20

                # Create Excel File in memory
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Security Rules')
                
                # Download Button
                st.download_button(
                    label="📥 Download Full Excel Report",
                    data=buffer.getvalue(),
                    file_name=f"SASE_Rules_{folder}_{position}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No rules found in the selected folder and position.")
