import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from csv_check import check_header, format_columns


csv_file = st.file_uploader(
    "Por favor sube tus transacciones bancarias en"
    "formato .csv para empezar con el analisis"
)

if csv_file is None:
    # loading .env
    load_dotenv()

    # Getting .csv file path
    csv_file = os.getenv("path")

    # Loading the data
    df = pd.read_csv(csv_file)

else:
    # Loading the data
    df = pd.read_csv(csv_file)


def load_csv(path):
    try:
        if csv_file is None:
            # loading .env
            load_dotenv()

            # Getting .csv file path
            csv_file = os.getenv("path")

            # Loading the data
            df = pd.read_csv(csv_file)

        else:
            # Loading the data
            df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("File not found.")

    return df


def addlabels(x, y, y_pos):
    for i in range(len(x)):
        plt.text(i + 1, y_pos, y[i], ha="center")


# List of month names
month_names = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


if csv_file:
    # Check headers and change columns names
    df.columns = check_header(df.columns)

    # Give the right format to each column
    df = format_columns(df)

    # Trick to print df.info() in streamlit
    # buffer = io.StringIO()
    # df.info(buf=buffer)
    # s = buffer.getvalue()
    # st.text(s)

    st.markdown(
        f"#### Empezaremos con el analisis de {df.shape[0]} transacciones "
        f"realizadas entre el {df.Date.dt.strftime('%d-%m-%Y').min()} y "
        f"{df.Date.dt.strftime('%d-%m-%Y').max()}"
    )
    # Data Statistics
    st.header("Estatisticas")
    total_money = df.Amount.sum()
    # st.write(df.head())

    # === Grafico 1 === #
    st.header("Graficos")
    st.subheader("1) Numero de transacciones por mes")
    transactions_month = df.groupby(df.Date.dt.month).Date.count()

    fig1, ax1 = plt.subplots()
    # ax1.set_title("Numero de transacciones por mes")
    ax1.bar(transactions_month.index, transactions_month.values)
    ax1.set_xlabel("Mes del ano")
    ax1.set_ylabel("Numero de transacciones")
    ax1.set_xticks(np.arange(len(month_names)) + 1, month_names)
    st.pyplot(fig1)

    st.subheader("Data Summary")
    try:
        dict = ["count", "mean", "min", "max", "sum"]
        des_amount = df.groupby(df.Date.dt.month)["Amount"].agg(dict)
        des_amount.index = month_names
        st.markdown(
            "#### Del grafico anterior se observar que en el mes de agosto "
            "se realizaron la mayoria de las compras del ano 2023"
        )
        st.write(des_amount)
    except BaseException:
        st.write("Summary can't be display due to lack of data")
        pass

    # === Grafico 2 === #
    try:
        st.subheader("2) Gasto total por mes")
        transactions_month = df.groupby(df.Date.dt.month).Amount.sum()
        # print(f"{df.groupby(df.Date.dt.month).sum()}")
        fig2, ax2 = plt.subplots()
        ax2.bar(transactions_month.index, transactions_month.values)
        ax2.set_xlabel("Mes del ano")
        ax2.set_ylabel("Gasto total")
        ax2.set_xticks(np.arange(len(month_names)) + 1, month_names)
        st.pyplot(fig2)

        st.markdown(
            "#### Del grafico anterior se observar que en el mes de agosto"
            "se realizaron la mayoria de las compras del ano 2023"
        )
    except BaseException:
        st.write("Something went wrong in plot 2")

    # === Grafico 3 === #
    try:
        st.subheader("3) Categorias")
        cat_exp = df.groupby(df.Category).Date.count()
        st.write(f"There are {len(cat_exp)} categorias")
        cat_exp = cat_exp.sort_values(ascending=False)[:5]

        fig3, ax3 = plt.subplots()
        ax3.set_title("Gastos por categoria")
        ax3.pie(cat_exp, labels=cat_exp.index, autopct="%1.1f%%")
        st.pyplot(fig3)
    except BaseException:
        st.write("Something went wrong in plot 3")

    # === Grafico 4 === #
    try:
        st.subheader("4) Tipos de transacciones")
        typ_exp = df.groupby(df.Type).Date.count()
        st.write(f"Hay {len(typ_exp)} diferentes tipos de transaccion")
        typ_exp = typ_exp.sort_values(ascending=False)[:5]

        fig4, ax4 = plt.subplots()
        per_typ_exp = typ_exp.values / (typ_exp.values).sum() * 100
        hbars = ax4.bar(typ_exp.index, per_typ_exp)
        ax4.bar_label(
            hbars, fmt="%.2f", labels=[f"{e.get_height():.2f}%" for e in hbars]
        )
        ax4.set_xlabel("Tipo de transaccion")
        ax4.set_ylabel("Porcentaje de las transacciones")
        st.pyplot(fig4)
    except BaseException:
        st.write("Something went wrong in plot 4")
