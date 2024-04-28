import streamlit as st
from streamlit_lottie import st_lottie
import math
import json
import pandas as pd

# ---- CONFIG STREAMLIT ----
st.set_page_config(page_title="finCalc by Zinker©️",
                   page_icon=":1234:",
                   layout="wide",
                   initial_sidebar_state='collapsed')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---- FUNCTIONS ----


def getRate(annual_rate: float, nbr_periods: int) -> str:
    arate = annual_rate/100
    cfValue = 100 * (1 + arate)
    pctValue = (((cfValue / 100) ** (1/nbr_periods)) - 1) * 100
    return getPCTText(pctValue)


def getPCTText(value: float, decimals: int = 2) -> str:
    strValue = str(round(value, 2))
    dec = 0
    if '.' in strValue:
        dec = len(strValue.split('.')[1])
    if dec < 2:
        strValue += (decimals - dec) * '0'
    return strValue + '%'


def getDoubleText(value: float, decimals: int = 2) -> str:
    strValue = str(round(value, 2))
    dec = 0
    if '.' in strValue:
        dec = len(strValue.split('.')[1])
    else:
        strValue += '.'
    if dec < 2:
        strValue += (decimals - dec) * '0'
    return strValue


def getPeriodText(value: int) -> str:
    if value == 1:
        periodText = str(value) + f' {period[:-1]}'
    else:
        periodText = str(value) + f' {period}'
    return periodText


def addCurrency(value: float, decimals: int = 2) -> str:
    return f'{currency} ' + getDoubleText(value, decimals)


def getOutput() -> str:
    strResult = '#Error'
    new_calc = {}
    if ndx == 0:
        result = cfValue / (1+(pctValue/100)) ** nperValue
        result = round(result, 2)
        strResult = addCurrency(result)
        new_calc = {'Initial': strResult, 'Final': addCurrency(cfValue),
                    'Periods': getPeriodText(nperValue), 'Interest': getPCTText(pctValue)}
    elif ndx == 1:
        result = ciValue * (1+(pctValue/100)) ** nperValue
        result = round(result, 2)
        strResult = addCurrency(result)
        new_calc = {'Initial': addCurrency(ciValue), 'Final': strResult,
                    'Periods': getPeriodText(nperValue), 'Interest': getPCTText(pctValue)}
    elif ndx == 2:
        result = math.log(cfValue/ciValue) / \
            math.log(1+(pctValue/100))
        result = math.ceil(result)
        strResult = getPeriodText(result)
        new_calc = {'Initial': addCurrency(ciValue), 'Final': addCurrency(cfValue),
                    'Periods': result, 'Interest': getPCTText(pctValue)}
    elif ndx == 3:
        result = (((cfValue/ciValue) ** (1/nperValue)) - 1)
        result = round(result, 2)
        strResult = getPCTText(result)
        new_calc = {'Initial': addCurrency(ciValue), 'Final': addCurrency(cfValue),
                    'Periods': getPeriodText(nperValue), 'Interest': strResult}

    st.session_state.df_historical.loc[len(
        st.session_state.df_historical) + 1] = new_calc

    return strResult


def load_lottieimg(imgpath) -> json:
    with open(imgpath, 'r') as json_file:
        image_dict = json.load(json_file)
    return image_dict


# ---- LOAD ASSETS ----
result_options = ['Initial Value',
                  'Final Value', 'Periods', 'Interest Rate']
period_options = ['Days', 'Months', 'Years']
currency_options = ['USD', 'BRL', 'ARS', 'GBP']
calc_image = 'calculate3.json'
lottie_img = load_lottieimg(calc_image)
app_version = 'app v1.0.0 @2024-04-27'
dfcolumns = ['Initial', 'Final', 'Interest', 'Periods']
period_value_min = 1
period_value_max = 365
period_value = 12
invest_initial = 100.0
invest_future = 500.0
pct_value = 5.0

if 'run_counter' not in st.session_state:
    st.session_state.run_counter = 1
else:
    st.session_state.run_counter += 1

if 'df_historical' not in st.session_state:
    st.session_state.df_created = True
    st.session_state.df_historical = pd.DataFrame(columns=dfcolumns)


# ---- APPLICATION finCalc ----
st.title('🔢financial Calculator')
st.markdown(f"_{app_version}_")


with st.sidebar:
    image_path = "zinker.png"
    st.image(image_path, use_column_width=False, width=100)
    st.write('# APP finCalc')
    st.write(
        '***finCalc*** is a tool to get faster financial calculations in a liquid world!')
    st.write('## How to use it?')
    st.write('### 1. Setup')
    st.write('- Select option to be calculated')
    st.write('- Select currency')
    st.write('- Select unit of Periods')
    st.write('### 2. Inputs')
    st.write('- Define input values needed')
    st.write('_For Interest Rate use just numbers, for instance 5.2%% input 0.052_')
    st.write('Push ***CALCULATE*** button')
    st.write('### 3. Output')
    st.write('- Result will be displayed properly')
    st.write('- Set of values will be added to historical calcs dataframe')
    st.write('- In case any error on data e message will be displayed')
    st.write('---')
    st.write('## Interest Rates')
    st.write('Quick calc to get monthly and daily rates based on annual interest rate')
    st.write('- Define annual rate')
    st.write('- Push GET RATES')
    st.write('---')
    st.write('''Designed by [ZINKER©️](https://zinker.com.br/)''')
    st.image(image_path, use_column_width=False, width=100)


# ---- ROW A : SETUP / INPUTS / OUTPUT / IMAGE ----
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.header("Setup")
    opt = st.radio('What to be calculated?', options=result_options, index=1)
    currency = st.selectbox('Currency', options=currency_options, index=0)
    period = st.selectbox('Periods unit', period_options, index=1)


with col2:
    st.header('Inputs')
    if opt == result_options[0]:
        ndx = 0
        st.empty()
        ciValue = invest_initial
        cfValue = st.number_input(
            f'Final Value [{currency}]', value=invest_future, step=1.0, key='cfValueKey')
        nperValue = st.slider(f'Periods [in {period}]', min_value=period_value_min,
                              max_value=period_value_max, value=period_value, step=1, key='nperValueKey')
        pctValue = st.number_input(
            f'% Interest Rate [by {period[:-1]}]', value=pct_value, key='pctValueKey', step=0.1, min_value=0.01)
    elif opt == result_options[1]:
        ndx = 1
        ciValue = st.number_input(
            f'Initial Value [{currency}]', value=invest_initial, step=1.0, key='ciValueKey')
        st.empty()
        cfValue = invest_future
        nperValue = st.slider(f'Periods [in {period}]', min_value=period_value_min,
                              max_value=period_value_max, value=period_value, step=1, key='nperValueKey')
        pctValue = st.number_input(
            f'% Interest Rate [by {period[:-1]}]', value=pct_value, key='pctValueKey', step=0.1, min_value=0.01)
    elif opt == result_options[2]:
        ndx = 2
        ciValue = st.number_input(
            f'Initial Value [{currency}]', value=invest_initial, step=1.0, key='ciValueKey')
        cfValue = st.number_input(
            f'Final Value [{currency}]', value=invest_future, step=1.0, key='cfValueKey')
        st.empty()
        pctValue = st.number_input(
            f'% Interest Rate [by {period[:-1]}]', value=pct_value, key='pctValueKey', step=0.1, min_value=0.01)
        nperValue = period_value
    elif opt == result_options[3]:
        ndx = 3
        ciValue = st.number_input(
            f'Initial Value [{currency}]', value=invest_initial, step=1.0, key='ciValueKey')
        cfValue = st.number_input(
            f'Final Value [{currency}]', value=invest_future, step=1.0, key='cfValueKey')
        nperValue = st.slider(f'Periods [{period}]', min_value=period_value_min,
                              max_value=period_value_max, value=period_value, step=1, key='nperValueKey')
        st.empty()
        pctValue = pct_value
    st.write('')
    calc_result = st.button('CALCULATE', key='btnCalcResult')

with col3:
    st.header('Output')
    if calc_result:
        st.empty()
        resultValue = getOutput()
        st.toast('Calc done!', icon='✨')
        st.write(f'# {result_options[ndx]}')
        st.success(f'# {resultValue}')

with col4:
    # st.header('fin-Calc')
    st_lottie(lottie_img, height=200, key="image_calculator")


st.write('---')

# ---- ROW B : HISTORICAL / MONTHLY RATE ----
col1, col2 = st.columns([2, 3])
with col1:
    st.header('_Quick Interest Rates_')
    st.write('Define annual rate and then get monthly and daily interest rates')
    annual_rate = st.number_input(
        '% Annual Rate', value=15.0, min_value=0.0, step=0.1)
    calc_mrate = st.button('Get Rates', key='btnCalcMRate')
    if calc_mrate:
        st.empty()
        st.success(f'Monthly rate = {getRate(annual_rate, 12)}')
        st.success(f'Daily rate = {getRate(annual_rate, 365)}')
        st.toast('Rates calculated!', icon='✨')

with col2:
    st.header('_Log of Calculations_')
    st.dataframe(st.session_state.df_historical, use_container_width=True)


st.write('---')
st.write('''Designed by [ZINKER©️](https://zinker.com.br/)''')
st.image(image_path, use_column_width=False, width=100)
