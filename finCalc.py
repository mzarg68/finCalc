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


def getMonthlyRate(annual_rate: str) -> str:
    annual_rate = annual_rate.replace('%', '')
    arate = float(annual_rate)/100
    cfValue = 100 * (1 + arate)
    pctValue = (((cfValue / 100) ** (1/12)) - 1) * 100
    return str(round(pctValue, 2)) + '%'


def isNumber(value: str) -> bool:
    value = value.replace('%', '')
    try:
        float(value)
        return True
    except ValueError:
        return False


def getPCTText(value: float) -> str:
    return str(round(value * 100, 2)) + '%'


def getResult() -> str:
    strResult = '#Error'
    new_calc = {}
    pctValue2 = pctValue
    if ' ' in pctValue2:
        pctValue2 = pctValue2.replace(' ', '')
    if '%' in pctValue2:
        pctValue2 = pctValue2.replace('%', '')
        pctnbr = float(pctValue2)/100
    else:
        pctnbr = float(pctValue2)

    if ndx == 0:
        result = float(cfValue) / (1+pctnbr) ** nperValue
        strResult = str(round(result, 2))
        new_calc = {'Initial': strResult, 'Final': cfValue,
                    'Periods': nperValue, 'Interest': getPCTText(pctnbr)}
    elif ndx == 1:
        result = float(ciValue) * (1+pctnbr) ** nperValue
        strResult = str(round(result, 2))
        new_calc = {'Initial': ciValue, 'Final': strResult,
                    'Periods': nperValue, 'Interest': getPCTText(pctnbr)}
    elif ndx == 2:
        result = math.log(float(cfValue)/float(ciValue)) / \
            math.log(1+pctnbr)
        strResult = str(math.ceil(result))
        new_calc = {'Initial': ciValue, 'Final': cfValue,
                    'Periods': strResult, 'Interest': getPCTText(pctnbr)}
    elif ndx == 3:
        result = (((float(cfValue)/float(ciValue)) ** (1/nperValue)) - 1) * 100
        strResult = str(round(result, 2)) + '%'
        new_calc = {'Initial': ciValue, 'Final': cfValue,
                    'Periods': nperValue, 'Interest': strResult}

    st.session_state.df_historical.loc[len(
        st.session_state.df_historical)] = new_calc
    return strResult


def load_lottieimg(imgpath) -> json:
    with open(imgpath, 'r') as json_file:
        image_dict = json.load(json_file)
    return image_dict


# ---- LOAD ASSETS ----
result_options = ['Initial Value',
                  'Final Value', 'Periods', 'Interest Rate']
period_options = ['Days', 'Months', 'Years']
calc_image = 'calculate.json'
lottie_img = load_lottieimg(calc_image)
app_version = 'Prototype v0.1.0 @2024-04-12'
dfcolumns = ['Initial', 'Final', 'Periods', 'Interest']

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
    st.write('Select option to be calculated')
    st.write('### 2. Inputs')
    st.write('Define input values needed')
    st.write('_For Interest Rate use just numbers, for instance 5.2%% input 0.052_')
    st.write('Push ***CALCULATE*** button')
    st.write('### 3. Output')
    st.write('Result will be displayed properly')
    st.write('Set of values will be added to historical calcs dataframe')
    st.write('In case any error on data e message will be displayed')
    st.write('---')
    st.write('''Designed by [ZINKER©️](https://zinker.com.br/)''')

# ---- ROW A : SETUP / INPUTS / OUTPUT / IMAGE ----
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.header("Setup")
    opt = st.radio('What to be calculated?', options=result_options, index=1)
    period = st.selectbox('Periods unit', period_options, index=1)


with col2:
    st.header('Inputs')
    if opt == result_options[0]:
        ndx = 0
        st.empty()
        ciValue = '0.0'
        cfValue = st.text_input('Final Value', value='500.0', key='cfValueKey')
        nperValue = st.slider(f'Periods [{period}]', min_value=1,
                              max_value=100, value=12, step=1, key='nperValueKey')
        pctValue = st.text_input(
            'Interest Rate', value='5.00%', key='pctValueKey', placeholder='5.00%')
    elif opt == result_options[1]:
        ndx = 1
        ciValue = st.text_input(
            'Initial Value', value='100.0', key='ciValueKey')
        st.empty()
        cfValue = '0.0'
        nperValue = st.slider(f'Periods [{period}]', min_value=1,
                              max_value=100, value=12, step=1, key='nperValueKey')
        pctValue = st.text_input(
            'Interest Rate', value='5.00%', key='pctValueKey', placeholder='5.00%')
    elif opt == result_options[2]:
        ndx = 2
        ciValue = st.text_input(
            'Initial Value', value='100.0', key='ciValueKey')
        cfValue = st.text_input(
            'Final Value', value='500.0', key='cfValueKey')
        st.empty()
        pctValue = st.text_input(
            'Interest Rate', value='5.00%', key='pctValueKey', placeholder='5.00%')
    elif opt == result_options[3]:
        ndx = 3
        ciValue = st.text_input(
            'Initial Value', value='100.0', key='ciValueKey')
        cfValue = st.text_input(
            'Final Value', value='500.0', key='cfValueKey')
        nperValue = st.slider(f'Periods [{period}]', min_value=1,
                              max_value=100, value=12, step=1, key='nperValueKey')
        st.empty()
        pctValue = '5.00%'
    st.write('')
    calc_result = st.button('CALCULATE', key='btnCalcResult')

with col3:
    st.header('Output')
    if calc_result:
        st.empty()
        if not isNumber(ciValue):
            st.error('Initial value is not valid!')
        elif not isNumber(cfValue):
            st.error('Final value is not valid!')
        elif not isNumber(pctValue):
            st.error('Interest rate is not valid!')
        else:
            st.toast('Calc done!', icon='✨')
            resultValue = getResult()
            st.success(f'# {result_options[ndx]} {resultValue}')

with col4:
    st_lottie(lottie_img, height=200, key="image_calculator")

st.write('---')
# ---- ROW B : HISTORICAL / MONTHLY RATE ----
col1, col2 = st.columns(2)
with col1:
    st.header('_Historical_')
    st.dataframe(st.session_state.df_historical)

with col2:
    st.header('_Get monthly rate_')
    annual_rate = st.text_input(
        'Annual Rate', value='15.0%', placeholder='10.0%', max_chars=7)
    calc_mrate = st.button('Get Rate', key='btnCalcMRate')
    if calc_mrate:
        st.empty()
        if isNumber(annual_rate):
            st.success(f'Monthly rate = {getMonthlyRate(annual_rate)}')
        else:
            st.error('📢Is not a number!!!')
            st.toast(annual_rate, icon='🧨')
st.write('---')
st.write('''Designed by [ZINKER©️](https://zinker.com.br/)''')
