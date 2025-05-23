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
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ✅ 打开 Google Sheet 并加载数据
sheet = client.open("Mood Bot").sheet1
df = get_as_dataframe(sheet).dropna(how='all')
df.columns = ["timestamp", "mood", "note"]
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(by="timestamp")

# 页面标题
st.title("🧠 Mood Tracker Dashboard 🎉")

# 用户选择视图模式
option = st.selectbox("Choose mood view:", ["Raw Data", "Daily Average", "3-day Rolling Average"])

# 创建每天的平均值
df["date"] = df["timestamp"].dt.date
daily_avg = df.groupby("date")["mood"].mean().reset_index()
daily_avg["rolling_avg"] = daily_avg["mood"].rolling(window=3).mean()

# 根据选择绘图
if option == "Raw Data":
    fig = px.line(df, x="timestamp", y="mood", title="Raw Mood Logs 📈", markers=True)
elif option == "Daily Average":
    fig = px.line(daily_avg, x="date", y="mood", title="Average Daily Mood 😊", markers=True)
else:
    fig = px.line(daily_avg, x="date", y="rolling_avg", title="3-Day Smoothed Mood Trend 😌", markers=True)

st.plotly_chart(fig)

# 心情频率柱状图
st.subheader("All-Time Mood Frequency 📊")
mood_counts_all = df["mood"].value_counts().reset_index()
mood_counts_all.columns = ["mood", "count"]
fig2 = px.bar(mood_counts_all, x="mood", y="count", color="mood", title="Mood Breakdown")
st.plotly_chart(fig2)

# 最近记录
st.subheader("Recent Mood Logs 📝")
st.dataframe(df.tail(10))
