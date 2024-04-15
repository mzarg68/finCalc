import streamlit as st


def isNumber(value: str) -> bool:
    value = value.replace('%', '')
    try:
        float(value)
        return True
    except ValueError:
        return False


def getResult(annual_rate: str) -> str:
    annual_rate = annual_rate.replace('%', '')
    arate = float(annual_rate)/100
    cfValue = 100 * (1 + arate)
    pctValue = (cfValue / 100) ** (1/12)
    return str(round(pctValue, 2)) + '%'


with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    annual_rate = col1.text_input(
        'Annual Rate', value='15.0%', placeholder='10.0%', max_chars=7)
    calc = col2.button('Monthly Rate', key='calcButton')
    if calc:
        col3.empty()
        if isNumber(annual_rate):
            col3.success(f'Monthly rate={getResult(annual_rate)}')
        else:
            col3.error('📢Is not a number')
            st.toast(annual_rate, icon='🧨')

# st.balloons()
# st.snow()
# st.toast('Warning up...', icon='🧨')
# st.error('Error message')
# st.warning('Warning message')
# st.info('Info message')
# st.success('Success message')
