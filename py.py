import streamlit as st
import pandas as pd

st.title("Análise de Vendas de Bicicletas")

data = pd.read_csv('bike_sales_100k.csv')

st.subheader("Dados Carregados:")
st.write(data.head())

st.write(f"Número total de entradas: {data.shape[0]}")
st.write(f"Número total de colunas: {data.shape[1]}")


if st.checkbox("Mostrar informações sobre os dados"):
    st.write(data.info())


if st.checkbox("Mostrar estatísticas descritivas"):
    st.write(data.describe())


data['Total_Sales'] = data['Price'] * data['Quantity']


total_sales_per_city = data.groupby('Store_Location')['Total_Sales'].sum().reset_index()
total_sales_per_city['Total_Sales'] = total_sales_per_city['Total_Sales'].apply(lambda x: f'${x:,.2f}')


st.subheader("Total de Vendas por Cidade:")
st.write(total_sales_per_city)


st.bar_chart(total_sales_per_city.set_index('Store_Location')['Total_Sales'].str.replace('$', '').str.replace(',', '').astype(float))


total_bikes_per_model = data.groupby('Bike_Model')['Quantity'].sum().reset_index()


st.subheader("Total de Bicicletas Vendidas por Modelo:")
st.write(total_bikes_per_model)


st.bar_chart(total_bikes_per_model.set_index('Bike_Model')['Quantity'])


ticket_medio_por_cidade = data.groupby('Store_Location').agg(
    Total_Vendas=('Total_Sales', 'sum'),
    Numero_Vendas=('Sale_ID', 'count')
).reset_index()


ticket_medio_por_cidade['Ticket_Medio'] = ticket_medio_por_cidade['Total_Vendas'] / ticket_medio_por_cidade['Numero_Vendas']


st.subheader("Ticket Médio por Cidade:")
st.write(ticket_medio_por_cidade[['Store_Location', 'Ticket_Medio']])


st.bar_chart(ticket_medio_por_cidade.set_index('Store_Location')['Ticket_Medio'])


total_sales_per_payment_method = data.groupby('Payment_Method')['Total_Sales'].sum().reset_index()
total_sales_per_payment_method['Total_Sales'] = total_sales_per_payment_method['Total_Sales'].apply(lambda x: f"${x:,.2f}")


st.subheader("Total de Vendas por Método de Pagamento:")
st.write(total_sales_per_payment_method)


st.bar_chart(total_sales_per_payment_method.set_index('Payment_Method')['Total_Sales'].str.replace('$', '').str.replace(',', '').astype(float))


bins = [0, 18, 30, 45, 60, 75, 100]
labels = ['0-18', '19-30', '31-45', '46-60', '61-75', '76+']

data['Age_Group'] = pd.cut(data['Customer_Age'], bins=bins, labels=labels, right=False)
total_bikes_per_age_group = data.groupby('Age_Group', observed=True)['Quantity'].sum().reset_index()


st.subheader("Total de Bicicletas Vendidas por Faixa Etária:")
st.write(total_bikes_per_age_group)


st.bar_chart(total_bikes_per_age_group.set_index('Age_Group')['Quantity'])
