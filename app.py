import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# --- 连接 Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ 从 secrets 中读取 GOOGLE_CREDENTIALS
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ✅ 打开共享的 Google Sheet（确保表名和共享邮箱正确）
sheet = client.open("Mood Bot").sheet1
df = get_as_dataframe(sheet).dropna(how='all')

# 数据处理
df.columns = ["timestamp", "mood", "note"]
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 只显示今天的数据
today = pd.Timestamp.now().normalize()
df_today = df[df["timestamp"] >= today]

# 页面显示
st.title("🧠 Mood of the Queue")

if not df_today.empty:
    mood_counts = df_today["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    fig = px.bar(mood_counts, x="mood", y="count", color="mood", title="Today's Mood Breakdown")
    st.plotly_chart(fig)
else:
    st.info("No moods logged today yet.")
