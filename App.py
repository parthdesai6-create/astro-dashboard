import streamlit as st
import pandas as pd
import yfinance as yf
import ephem
from datetime import datetime
import pytz

# પેજ સેટઅપ
st.set_page_config(page_title="Vedic Astro Dashboard", layout="wide")
st.title("🌟 વૈદિક જ્યોતિષ અને માર્કેટ એનાલિસિસ ડેશબોર્ડ")

# ટાઈમઝોન
IST = pytz.timezone('Asia/Kolkata')
now = datetime.now(IST)

# ગ્રહોના હોરા ક્રમ (શનિથી શરૂ થતો ચક્ર)
hora_lords = ['શનિ', 'ગુરુ', 'મંગળ', 'સૂર્ય', 'શુક્ર', 'બુધ', 'ચંદ્ર']
planet_scores = {
    'સૂર્ય': {'Bullish': 3, 'Bearish': 1},
    'ચંદ્ર': {'Bullish': 2, 'Bearish': 2},
    'મંગળ': {'Bullish': 4, 'Bearish': 0},
    'બુધ': {'Bullish': 2, 'Bearish': 2},
    'ગુરુ': {'Bullish': 4, 'Bearish': 0},
    'શુક્ર': {'Bullish': 3, 'Bearish': 1},
    'શનિ': {'Bullish': 1, 'Bearish': 4}
}

# વર્તમાન હોરા ગણતરી
hour_idx = now.hour % 7
current_hora = hora_lords[hour_idx]

st.subheader(f"🕒 વર્તમાન સમય (IST): {now.strftime('%d-%m-%Y %H:%M:%S')}")
st.write(f"### વર્તમાન હોરા સ્વામી: **{current_hora}**")

# સ્કોરિંગ ગણતરી
score = planet_scores.get(current_hora, {'Bullish': 2, 'Bearish': 2})
bullish_score = score['Bullish']
bearish_score = score['Bearish']

col1, col2 = st.columns(2)
with col1:
    st.metric(label="🟢 બુલિશ પોઈન્ટ્સ", value=bullish_score)
with col2:
    st.metric(label="🔴 બેરિશ પોઈન્ટ્સ", value=bearish_score)

if bullish_score > bearish_score:
    st.success("🎯 નિર્ણય: માર્કેટ સેન્ટિમેન્ટ પોઝિટિવ / બુલિશ જણાય છે.")
elif bearish_score > bullish_score:
    st.error("⚠️ નિર્ણય: માર્કેટ સેન્ટિમેન્ટ નેગેટિવ / બેરિશ જણાય છે.")
else:
    st.warning("⚖️ નિર્ણય: માર્કેટ ન્યુટ્રલ અથવા વોલેટાઈલ રહી શકે છે.")

# લાઇવ માર્કેટ ડેટા
st.markdown("---")
st.subheader("📊 નિફ્ટી 50 ઇન્ડેક્સ")
try:
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="1d", interval="5m")
    if not data.empty:
        latest_price = round(data['Close'].iloc[-1], 2)
        st.metric(label="NIFTY 50 વર્તમાન ભાવ", value=latest_price)
        st.line_chart(data['Close'])
    else:
        st.info("માર્કેટ ડેટા હાલ ઉપલબ્ધ નથી.")
except Exception as e:
    st.warning("લાઇવ ડેટા મેળવવામાં ક્ષતિ આવી છે.")
