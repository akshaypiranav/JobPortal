import streamlit as st
import requests
import pandas as pd
import json
import io

FIREBASE_URL = "https://job-portal-523f4-default-rtdb.firebaseio.com/.json"

def fetch_data():
    res = requests.get(FIREBASE_URL)
    if res.status_code == 200 and res.json():
        raw_data = res.json()
        if isinstance(raw_data, list):
            clean_data = [item for item in raw_data if item is not None]
            df = pd.DataFrame(clean_data)
        else:
            df = pd.DataFrame.from_dict(raw_data, orient='index')
        
        column_order = [
            "companyName",
            "phoneNumber",
            "location",
            "role",
            "pythonBackend",
            "netBackend",
            "cyberSecurity",
            "aiDeveloper"
        ]
        display_names = {
            "companyName": "Company Name",
            "phoneNumber": "Phone Number",
            "location": "Location",
            "role": "Role of the Company",
            "pythonBackend": "Python Backend",
            "netBackend": ".Net Backend",
            "cyberSecurity": "Cyber Security Engineer",
            "aiDeveloper": "AI Product Developer"
        }
        df = df[column_order]
        df.rename(columns=display_names, inplace=True)
        return df
    return pd.DataFrame()

def upload_data(entry):
    current_data = requests.get(FIREBASE_URL).json() or []
    if not isinstance(current_data, list):
        current_data = []
    current_data.append(entry)
    res = requests.put(FIREBASE_URL, data=json.dumps(current_data))
    return res.status_code == 200

def main():
    st.title("💼 May 2025 Job Search Portal")

    st.header("📝 Add New Company Entry")
    with st.form("entry_form"):
        company_name = st.text_input("Company Name")
        phone_number = st.text_input("Phone Number")
        location = st.selectbox("Location", ["Coimbatore", "Hyderabad", "Bengaluru", "Chennai"])
        role = st.selectbox("Role of Company", ["Freelance", "Product Based", "Service Based"])

        st.markdown("#### Select Roles:")
        cyber_security = st.checkbox("Cyber Security Engineer")
        python_backend = st.checkbox("Python Backend")
        ai_developer = st.checkbox("AI Product Developer")
        net_backend = st.checkbox(".NET Backend")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not company_name or not phone_number:
                st.warning("⚠️ Please enter both Company Name and Phone Number.")
            else:
                entry = {
                    "companyName": company_name,
                    "phoneNumber": phone_number,
                    "location": location,
                    "role": role,
                    "cyberSecurity": cyber_security,
                    "pythonBackend": python_backend,
                    "netBackend": net_backend,
                    "aiDeveloper": ai_developer
                }
                if upload_data(entry):
                    st.success("✅ Data uploaded successfully.")
                else:
                    st.error("❌ Failed to upload data.")

    st.header("📊 View Job Database")
    df = fetch_data()
    if not df.empty:
        st.dataframe(df)

        # Export to Excel with correct order
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="📥 Download as Excel",
            data=buffer,
            file_name="job_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("ℹ️ No data found in Firebase.")

if __name__ == "__main__":
    main()
