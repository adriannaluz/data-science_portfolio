import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

csv_file = st.file_uploader("Por favor sube tus transacciones bancarias en"
                             "formato .csv para empezar con el analisis")

def addlabels(x,y, y_pos):
    for i in range(len(x)):
        plt.text(i+1, y_pos, y[i], ha='center')

# List of month names
month_names = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


if csv_file:
    # Loading the data
    df = pd.read_csv(csv_file)
    # Setting the index
    df.set_index("Transaction_ID", inplace=True)
    # Changin Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    st.write(f"Empezaremos con el analisis de {df.shape[0]} transacciones "
             f"realizadas entre el {df.Date.dt.strftime('%d/%m/%Y').min()} y {df.Date.dt.strftime('%d/%m/%Y').max()}")
    # Data Statistics
    st.header("Estatisticas")
    # st.write(df.describe())

    # Graficos
    st.header("Graficos")
    st.subheader("Numero de transacciones por mes")
    transactions_month = df.groupby(df.Date.dt.month).Date.count()
    fig1, ax1 = plt.subplots()
    # ax1.set_title("Numero de transacciones por mes")
    ax1.bar(transactions_month.index, transactions_month.values)
    ax1.set_xlabel("Mes del ano")
    ax1.set_ylabel("Numero de transacciones")
    st.pyplot(fig1)

    st.subheader("Gastos totales por mes")
    expenses_month = df.groupby(df.Date.dt.month).Amount.sum()
    salary = pd.Series([1800 for i in range(12)], index=[i for i in range (1,13)])

    fig2, ax2 = plt.subplots()
    ax2.bar(expenses_month.index, expenses_month.values)
    ax2.set_xlabel("Mes del ano")
    ax2.set_ylabel("Gastos totales")
    ax2.set_xticks(np.arange(len(month_names)) + 1, month_names)
    neg_balance_day = df[df.Balance_After_Transaction <= 0].Date.dt.day.values
    neg_balance_day = np.insert(neg_balance_day, 2, "31")
    addlabels(month_names, neg_balance_day, 2)

    st.pyplot(fig2)

    # Plots
    st.subheader("Dia del mes donde el balance llego a cero o menos")
    day = df[df.Balance_After_Transaction <= 0].Date.dt.day

    month = df[df.Balance_After_Transaction <= 0].Date.dt.month
    fig, ax = plt.subplots()
    ax.bar(month, day)
    ax.set_xlabel("Month")
    ax.set_ylabel("Day of the Month")
    st.pyplot(fig)

    # Data Header
    st.header("Data Header")
    st.write(df.head())

