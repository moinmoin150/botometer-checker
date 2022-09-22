import streamlit as st
import botometer
import pandas

rapidapi_key = st.secrets["rapidapi_key"]
twitter_app_auth = {
    'consumer_key': st.secrets["consumer_key"],
    'consumer_secret': st.secrets["consumer_secret"],
    'access_token': st.secrets["access_token"],
    'access_token_secret': st.secrets["access_token_secret"]
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

st.markdown("# Botometer Checker")
uploaded_file = st.file_uploader("Please upload a CSV spreadsheet with usernames or user IDs in a column (either with or without @ is okay)", type=["csv"])
col = st.text_input('Enter the name of the column with usernames or user iDs')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("successfully uploaded:", uploaded_file.name)

    user_l = df[col].to_list()

    accounts = user_l
    result_l = []
    for screen_name, result in bom.check_accounts_in(accounts):
        try:
            result_l.append(result['cap']['universal'])
        except:
            result_l.append('error')
        if len(result_l) % 100 == 0:
            st.write('successfully checked', len(result_l), 'accounts')

    df['botometer_result'] = result_l

    st.download_button(
        label="Download data as CSV",
        data=df,
        file_name=f'{uploaded_file.name}_bot_checked.csv',
        mime='text/csv',
    )
