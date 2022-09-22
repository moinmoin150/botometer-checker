import streamlit as st
import botometer as boto
import pandas as pd

@st.cache
def convert_df_to_csv(df):
  return df.to_csv().encode('utf-8-sig')

rapidapi_key = st.secrets["rapidapi_key"]
twitter_app_auth = {
    'consumer_key': st.secrets["consumer_key"],
    'consumer_secret': st.secrets["consumer_secret"],
    'access_token': st.secrets["access_token"],
    'access_token_secret': st.secrets["access_token_secret"]
  }
bom = boto.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

st.markdown("# Botometer Checker")
uploaded_file = st.file_uploader("Please upload a CSV spreadsheet with usernames or user IDs in a column (either with or without @ is okay)", type=["csv"])
col = st.text_input('Enter the name of the column with usernames or user iDs (case sensitive)')
btn = st.button("Run!")

if (uploaded_file is not None) and (len(col)>0) and (btn == 1):
    df = pd.read_csv(uploaded_file)
    filename = uploaded_file.name
    st.write("successfully uploaded:", filename)

    user_l = df[col].to_list()

    accounts = user_l
    result_l = []
    cap_l = []
    for screen_name, result in bom.check_accounts_in(accounts):
        if result['user']['majority_lang'] == 'en':
            try:
                result_l.append(result['display_scores']['english']['overall'])
                cap_l.append(result['cap']['english'])
            except:
                cap_l.append('error')
                result_l.append('error')
        else:
            try:
                result_l.append(result['display_scores']['universal']['overall'])
                cap_l.append(result['cap']['universal'])
            except:
                cap_l.append('error')
                result_l.append('error')
        if len(result_l) % 10 == 0:
            st.write('successfully checked', len(result_l), 'accounts')

    df['botometer_result'] = result_l
    df['CAP'] = cap_l

    btn = st.download_button(
        label="Download data as CSV",
        data=convert_df_to_csv(df),
        file_name=f"{filename.lower().replace('.csv','')}_bot_checked.csv",
        mime='text/csv',
    )
                     
