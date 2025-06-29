
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modules.load_coefficients import load_coefficients
from modules.prospect_d import prospect_d

st.set_page_config(layout="wide")
st.title("PROSPECT-D 模拟器（修正版本）")
st.markdown("**Copyright © Peiqi Yang**, p.yang@njnu.edu.cn")

N = st.sidebar.number_input("结构参数 N", 1.0, 3.0, 1.5, step=0.1)
Cab = st.sidebar.number_input("叶绿素含量 Cab (μg/cm²)", 0.0, 100.0, 40.0)
Car = st.sidebar.number_input("类胡萝卜素含量 Car (μg/cm²)", 0.0, 20.0, 8.0)
Cw = st.sidebar.number_input("含水量 Cw (g/cm²)", 0.0, 0.05, 0.01)
Cm = st.sidebar.number_input("干物质含量 Cm (g/cm²)", 0.0, 0.05, 0.01)

try:
    wl, nr, Kab, Kcar, Kw, Km = load_coefficients()
    refl, tran = prospect_d(N, Cab, Car, Cw, Cm, wl, nr, Kab, Kcar, Kw, Km)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(wl, refl, label="Reflectance", linewidth=2)
    ax.plot(wl, tran, label="Transmittance", linewidth=2)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Value")
    ax.set_title("Leaf Optical Properties (PROSPECT-D)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

except Exception as e:
    st.error(f"模型运行失败，请检查数据文件是否存在并格式正确。\n错误信息: {e}")
