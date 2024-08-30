import streamlit as st
import requests
import matplotlib.pyplot as plt

base_url = "https://marketdata.tradermade.com/api/v1/convert"
api_key = "2dc_Jal4a_phxen9t23P"

st.title("Currency Converter by Bota Mihnea")
st.image("CurrencyConverterLogo.png", width=200)

def convert_currency(amount, base_currency, target_currency):
    url = f"{base_url}?api_key={api_key}&from={base_currency}&to={target_currency}&amount={amount}"
    response = requests.get(url)
    #if the status  code is 200 , it means that the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data["quote"])
        return data["quote"], data["total"]
    else:
        return None, None

def get_currencies():
    url = "https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=2dc_Jal4a_phxen9t23P"
    response = requests.get(url)
    if response.status_code == 200:
        currencies_data = response.json()
        if "available_currencies" in currencies_data:
            currencies = currencies_data["available_currencies"]
            return list(currencies.keys())
        else:
            st.write("Error : No 'available_currencies' found in the response provided by the API.")
            return None
    else:
        st.write(f"Error : Code {response.status_code} {response.text}")

def converter():
    amount = st.number_input("Enter an integer amount for conversion:", value=1,step=1)
    currencies_list = get_currencies()
    if currencies_list is not None:
        base_currency = st.selectbox("Select the wanted base currency: ", currencies_list, index=1)
        target_currencies = st.multiselect("Select the desired target currencies: ", currencies_list)
        if st.button("Convert"):
            st.write("Converted currencies: ")
            rates = []
            labels = []
            for currency in target_currencies:
                print(currency, base_currency)
                try:
                    quote, converted_amount = convert_currency(amount, base_currency, currency)
                    if quote:
                        st.write(f"{amount} {base_currency} = {converted_amount} {currency} -> The rate is 1{base_currency} = {quote} {currency}")
                        rates.append(quote)
                        labels.append(currency)
                    else:
                        st.write(f"Something went wrong with the API provider.")
                except:
                    st.write(f"Exchange rate from {base_currency} to {currency} is not available!")

            if rates and labels:
                st.write("Currencies chart")
                fig, ax = plt.subplots()
                ax.bar(labels, rates, color='blue')
                ax.set_xlabel('Target currency')
                ax.set_ylabel(f'Rate per 1 {base_currency}')
                ax.set_title(f'Conversion rates from {base_currency}')
                st.pyplot(fig)




converter()
