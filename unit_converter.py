import streamlit as st
import pandas as pd
import os

# Set custom theme (Streamlit theming is applied via `.streamlit/config.toml` but use inline styling)
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered" )

# Custom CSS to UI
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .stTextInput, .stNumberInput, .stSelectbox { border-radius: 10px !important; }
    .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# App Title with Icon
st.markdown("<h1 style='text-align: center;'>🔄 Unit Converter Web App</h1>", unsafe_allow_html=True)

# ✅ Global list to store conversion history
conversion_history = []

# Dark Mode Toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

# Apply Dark Mode using Custom CSS
if dark_mode:
    dark_css = """
    <style>
        body, .stApp { background-color: #121212; color: white !important; }
        .stTextInput, .stNumberInput, .stSelectbox, .stSlider { background-color: #333; color: white; border-radius: 10px !important; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; border-radius: 10px; }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)

# Conversion functions
def length_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Meters': 1, 'Kilometers': 0.001, 'Miles': 0.000621371, 'Feet': 3.28084
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def weight_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Grams': 1, 'Kilograms': 0.001, 'Pounds': 0.00220462, 'Ounces': 0.035274
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def temperature_converter(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celius":
        return (value - 32) * 5/9
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    else:
        return value

def volume_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Liters': 1, 'Milliliters': 1000, 'Gallons': 0.264172, 'Cups': 4.22675
    }
    
    # Debugging: Print available keys
    print("Available keys in volume converter:", conversion_factors.keys())

    # Ensure both `from_unit` and `to_unit` exist
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        raise KeyError(f"Invalid unit selection: {from_unit} or {to_unit} not found")

    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def speed_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Meters/Second': 1, 'Kilometers/Hour': 3.6, 'Miles/Hour': 2.23694
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def time_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Seconds': 1, 'Minutes': 1/60, 'Hours': 1/3600, 'Days': 1/86400
    }

    # Debugging line
    print("Available keys in time_converter:", conversion_factors.keys())
    print("From:", from_unit, "| To:", to_unit)  # Debugging output

    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        raise KeyError(f"Invalid unit selection: {from_unit} or {to_unit} not found")

    return value * (conversion_factors[to_unit]/ conversion_factors[from_unit])

def currency_converter(value, from_currency, to_currency):
    rates = {
        "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "PKR": 277.35
    }
    return value * (rates[to_currency] / rates[from_currency])

def power_converter(value, from_unit, to_unit):
    conversion_factors = {
        'Watts': 1, 'Kilowatts': 0.001, 'Horsepower': 0.00134
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

# convert options
conversion_options = {
    "📏 Length": (length_converter, ['Meters', 'Kilometers', 'Miles', 'Feet']),
    "⚖️ Weight": (weight_converter, ['Grams', 'Kilograms', 'Pounds', 'Ounces']),
    "🌡️ Temperature": (temperature_converter, ['Celsius', 'Fahrenheit', 'Kelvin']),
    "🧪 Volume": (volume_converter, ['Liters', 'Milliliters', 'Gallons', 'Cups']),
    "🚀 Speed": (speed_converter, ['Meters/Second', 'Kilometers/Hour', 'Miles/Hour']),
    "⏳ Time": (time_converter, ['Seconds', 'Minutes', 'Hours', 'Days']),
    "💰 Currency": (currency_converter, ['USD', 'EUR', 'GBP', 'PKR']),
    "⚡ Power": (power_converter, ['Watts', 'Kilowatts', 'Horsepower']),
}

# sidebar 
st.sidebar.image("https://i.imgur.com/3V2B5Ae.png", width=250)
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Select a unit type and enter the value to convert.")

# Choose conversion type
conversion_type = st.sidebar.selectbox("Choose conversion type:", list(conversion_options.keys()))
# ✅ Available units based on category
if conversion_type == "Length":
    units = ['Meters', 'Kilometers', 'Miles', 'Feet']
    converter = length_converter
elif conversion_type == "Weight":
    units = ['Grams', 'Kilograms', 'Pounds']
    converter = weight_converter
elif conversion_type == "Temperature":
    units = ['Celsius', 'Fahrenheit', 'Kelvin']
    converter = time_converter
elif conversion_type == "Volume":
    units = ['Liters', 'Milliliters', 'Gallons', 'Cups']
    converter = weight_converter
elif conversion_type == "Speed":
    units = ['Meters/Second', 'Kilometers/Hour', 'Miles/Hour']
    converter = weight_converter
elif conversion_type == "Time":
    units = ['Seconds', 'Minutes', 'Hours', 'Days']
    converter = weight_converter
elif conversion_type == "Currency":
    units = ['USD', 'EUR', 'GBP', 'PKR']
    converter = weight_converter
elif conversion_type == "Power":
    units = ['Watts', 'Kilowatts', 'Horsepower']
    converter = weight_converter

# Get the selected conversion function and units
convert_func, units = conversion_options[conversion_type]

# User input section
st.markdown(f"<h2 class='big-font'>🔄 {conversion_type} Conversion</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", units)
with col2:
    to_unit = st.selectbox("To", units)

value = st.slider("Enter value:", min_value=0.0, max_value=1000.0, step=0.1)

result = None  

# Perform conversion
if st.button("Convert 🔄"):
    if value > 0:
        result = convert_func(value, from_unit, to_unit)
        st.success(f"✅ Converted value: **{result:.2f} {to_unit}**")

        conversion_history.append([value, from_unit, result, to_unit])

csv_filename = "conversion_history.csv"

if len(conversion_history) > 0:
    df = pd.DataFrame(conversion_history, columns=["Value", "From", "Converted Value", "To"])

    # ✅ If CSV already exists, append new conversions
    if os.path.exists(csv_filename):
        existing_df = pd.read_csv(csv_filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    # ✅ Save updated file
    df.to_csv(csv_filename, index=False)

    # ✅ Download button for updated CSV
    with open(csv_filename, "rb") as f:
        st.download_button("📥 Download Updated CSV", f, csv_filename, "text/csv")

# Download the result as a CSV
if st.button("📥 Download Result"):
    df = pd.DataFrame([[value, from_unit, result, to_unit]], columns=["Value", "From", "Converted Value", "To"])
    df.to_csv("conversion_result.csv", index=False)
    st.download_button("Download CSV", df.to_csv(index=False), "conversion_result.csv", "text/csv")

# Copy result to clipboard
st.button("📋 Copy to Clipboard")