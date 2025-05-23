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

# ✅ 打开共享的 Google Sheet
sheet = client.open("Mood Bot").sheet1
df = get_as_dataframe(sheet).dropna(how='all')

# 预览所有 sheet（调试用）
# for s in client.openall():
#     st.write("Found sheet:", s.title)

# 数据处理
df.columns = ["timestamp", "mood", "note"]
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(by="timestamp")

# 页面显示
st.title("🧠 Mood Tracker Dashboard 🎉")

# 可视化 1：心情趋势图（历史全部）
st.subheader("Mood Trend Over Time 📈")
fig1 = px.line(df, x="timestamp", y="mood", title="Mood Over Time", markers=True)
st.plotly_chart(fig1)

# 可视化 2：心情分布柱状图（历史总计）
st.subheader("Overall Mood Frequency 📊")
mood_counts_all = df["mood"].value_counts().reset_index()
mood_counts_all.columns = ["mood", "count"]
fig2 = px.bar(mood_counts_all, x="mood", y="count", color="mood", title="All-Time Mood Breakdown")
st.plotly_chart(fig2)

# 可选：显示最近几条日志
st.subheader("Recent Mood Logs 📝")
st.dataframe(df.tail(10))
