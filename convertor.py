import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS
st.markdown("""
    <style>
        body {
            background: radial-gradient(circle at top left, #141e30, #243b55);
            color: white;
        }
        .stApp {
            background: radial-gradient(circle at top left, #141e30, #243b55);
        }
        .glassmorphism {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: 0.3s ease-in-out;
        }
        .stTextInput:hover, .stNumberInput:hover, .stSelectbox:hover {
            background: rgba(255, 255, 255, 0.25);
            border: 1px solid white;
        }
        .stButton>button {
            background: linear-gradient(135deg, #ff7eb3, #ff758c);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            transition: 0.3s;
            box-shadow: 0px 4px 10px rgba(255, 120, 150, 0.5);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #ff4e90, #ff2a68);
            transform: scale(1.05);
            box-shadow: 0px 6px 14px rgba(255, 120, 150, 0.7);
        }
        .stSuccess {
            background: rgba(0, 230, 118, 0.2);
            color: #00e676;
            padding: 12px;
            border-radius: 12px;
            font-weight: bold;
            text-align: center;
            border: 1px solid #00e676;
            box-shadow: 0px 2px 8px rgba(0, 230, 118, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# Conversion factors
data = {
    "Length": {"meter": 1, "kilometer": 0.001, "centimeter": 100, "mile": 0.000621371},
    "Weight": {"kilogram": 1, "gram": 1000, "pound": 2.20462, "ounce": 35.274},
    "Temperature": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"},
}

df = {category: pd.DataFrame(list(units.items()), columns=["Unit", "Factor"]) for category, units in data.items() if category != "Temperature"}

def convert(value, from_unit, to_unit, category):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value
    else:
        return value * data[category][to_unit] / data[category][from_unit]

st.markdown('<div class="glassmorphism">', unsafe_allow_html=True)
st.title("✨ Stylish Unit Converter")
st.write("💡 Made by Fakharuddin")

category = st.selectbox("📌 Select Category", list(data.keys()))

if category == "Temperature":
    from_unit = st.selectbox("🌡️ From Unit", list(data[category].keys()))
    to_unit = st.selectbox("🌡️ To Unit", list(data[category].keys()))
else:
    from_unit = st.selectbox("📏 From Unit", df[category]["Unit"].tolist())
    to_unit = st.selectbox("📏 To Unit", df[category]["Unit"].tolist())

value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.2f")
converted_value = convert(value, from_unit, to_unit, category)
st.success(f"✅ Converted Value: {converted_value} {to_unit}")

# Plotly Visualization
if category != "Temperature":
    fig = px.bar(df[category], x="Unit", y="Factor", title=f"📊 Conversion Factors for {category}", color="Unit")
    st.plotly_chart(fig)

st.markdown('</div>', unsafe_allow_html=True)
