import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# SETUP DASHBOARD
# =========================
st.set_page_config(page_title="🎁 Dashboard Self-Reward Mahasiswa Gen Z", layout="wide")
st.title("🎁 Dashboard Analisis Self-Reward Mahasiswa Gen Z")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data_self_reward_cleaned.csv")

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔍 Filter Data")
fakultas_selected = st.sidebar.multiselect(
    "Pilih Fakultas", options=df['Fakultas'].unique(), default=df['Fakultas'].unique()
)
df_filtered = df[df['Fakultas'].isin(fakultas_selected)]

# =========================
# RINGKASAN STATISTIK
# =========================
st.subheader("📊 Ringkasan Data Responden")

colA, colB, colC, colD = st.columns(4)

# 1. Total responden
total_responden = len(df_filtered)

# 2. Median budget
median_budget = df_filtered['budget_selfreward'].median()

# 3. Rata-rata frekuensi self-reward
mean_freq = df_filtered['freq_selfreward'].mean()

# 4. Persentase kepentingan tinggi (misalnya kepentingan >= 4)
high_importance_pct = (df_filtered['kepentingan_selfreward'] >= 4).mean() * 100

with colA:
    st.metric("👥 Total Responden", f"{total_responden} orang")
with colB:
    st.metric("💰 Median Budget", f"Rp {median_budget:,.0f}")
with colC:
    st.metric("🔄 Rata-rata Frekuensi", f"{mean_freq:.2f} kali")
with colD:
    st.metric("📈 Kepentingan Tinggi (≥4)", f"{high_importance_pct:.1f}%")

# =========================
# KATEGORIKAL DISTRIBUSI
# =========================
st.subheader("📌 Distribusi Kategorikal")

col1, col2 = st.columns(2)

with col1:
    st.write("**Distribusi Jenis Self-Reward**")
    jenis_counts = df_filtered['jenis_selfreward'].value_counts()
    fig, ax = plt.subplots(figsize=(6,4))
    jenis_counts.plot(kind='barh', ax=ax)
    ax.set_xlabel("Jumlah Responden")
    ax.set_ylabel("Jenis Self-Reward")
    st.pyplot(fig)

with col2:
    st.write("**Preferensi Self-Reward (Materi vs Non-Materi)**")
    preferensi_counts = df_filtered['preferensi_selfreward'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(preferensi_counts, labels=preferensi_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

# =========================
# NUMERIKAL DISTRIBUSI
# =========================
st.subheader("📊 Distribusi Numerikal")

col3, col4 = st.columns(2)

with col3:
    st.write("**Distribusi Budget Self-Reward**")
    fig3, ax3 = plt.subplots()
    ax3.boxplot(df_filtered['budget_selfreward'])
    ax3.set_ylabel("Budget (Rp)")
    st.pyplot(fig3)

with col4:
    st.write("**Histogram Frekuensi Self-Reward**")
    fig4, ax4 = plt.subplots()
    ax4.hist(df_filtered['freq_selfreward'], bins=range(0, df_filtered['freq_selfreward'].max()+2))
    ax4.set_xlabel("Frekuensi")
    ax4.set_ylabel("Jumlah Responden")
    st.pyplot(fig4)

# =========================
# ANALISIS GABUNGAN
# =========================
st.subheader("📈 Rata-rata Budget per Jenis Self-Reward")
mean_budget_per_jenis = df_filtered.groupby('jenis_selfreward')['budget_selfreward'].mean().sort_values()
fig5, ax5 = plt.subplots(figsize=(8,4))
mean_budget_per_jenis.plot(kind='barh', ax=ax5)
ax5.set_xlabel("Rata-rata Budget (Rp)")
ax5.set_ylabel("Jenis Self-Reward")
st.pyplot(fig5)

# =========================
# KORELASI NUMERIKAL
# =========================
st.subheader("🔗 Korelasi Variabel Numerikal")

# Pilih hanya kolom numerik yang relevan
num_cols = ['freq_selfreward', 'keinginan_selfreward', 'budget_selfreward', 'durasi_selfreward', 'kepentingan_selfreward']
corr_matrix = df_filtered[num_cols].corr()

fig6, ax6 = plt.subplots(figsize=(8,5))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", ax=ax6)
ax6.set_title("Heatmap Korelasi")
st.pyplot(fig6)
