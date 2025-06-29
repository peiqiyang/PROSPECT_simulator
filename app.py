import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime
from modules.load_coefficients import load_coefficients
from modules.prospect_d import prospect_d

# 页面配置
st.set_page_config(
    page_title="PROSPECT-D 模拟器",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("PROSPECT-D 模拟器")
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 8px;
            right: 12px;
            font-size: 1em;
            z-index: 100;
        }
    </style>
    <div class="footer">
        <b>Copyright © Peiqi Yang</b>, p.yang@njnu.edu.cn
    </div>
    """,
    unsafe_allow_html=True
)

# ========== 工具函数：生成 TXT ==========
def generate_txt(N, Cab, Car, Cw, Cm, wl, refl, tran):
    buffer = io.StringIO()
    buffer.write(f"# N={N}, Cab={Cab}, Car={Car}, Cw={Cw}, Cm={Cm}\n")
    buffer.write("Wavelength (nm)\tReflectance\tTransmittance\n")
    for i in range(len(wl)):
        buffer.write(f"{wl[i]:.2f}\t{refl[i]:.6f}\t{tran[i]:.6f}\n")
    return buffer.getvalue().encode('utf-8')


# ========== 初始化状态 ==========
if 'results_list' not in st.session_state:
    st.session_state.results_list = []

# ========== 侧边栏 ==========
# 显示选项
col1, col2 = st.sidebar.columns(2)
show_refl = col1.checkbox("显示反射率", value=True)
show_tran = col2.checkbox("显示透射率", value=True)

# 控制模拟行为
col1, col2 = st.sidebar.columns(2)
retain_previous = col1.checkbox("保留前次模拟结果", value=False)
simulate_button = col2.button("开始模拟")

# 参数输入
st.sidebar.header("模拟参数设置")
N = st.sidebar.number_input("结构参数 N", 1.0, 3.0, 1.5, step=0.1)
Cab = st.sidebar.number_input("叶绿素含量 Cab (μg/cm²)", 0.0, 100.0, 40.0, step=5.0)
Car = st.sidebar.number_input("类胡萝卜素含量 Car (μg/cm²)", 0.0, 20.0, 8.0, step=1.0)
Cw = st.sidebar.number_input("含水量 Cw (g/cm²)", 0.0, 0.05, 0.01, step=0.005)
Cm = st.sidebar.number_input("干物质含量 Cm (g/cm²)", 0.0, 0.05, 0.01, step=0.005)

# ========== 点击模拟 ==========
if simulate_button:
    if not retain_previous:
        st.session_state.results_list = []

    try:
        wl, nr, Kab, Kcar, Kw, Km = load_coefficients()
        refl, tran = prospect_d(N, Cab, Car, Cw, Cm, wl, nr, Kab, Kcar, Kw, Km)
        st.session_state.results_list.append({
            "wl": wl,
            "refl": refl,
            "tran": tran,
            "label": f"N={N}, Cab={Cab}, Car={Car}, Cw={Cw}, Cm={Cm}"
        })
    except Exception as e:
        st.error(f"模型运行失败，请检查数据文件是否存在并格式正确。\n错误信息: {e}")

# ========== 图像区域（始终显示） ==========
fig, ax = plt.subplots(figsize=(12, 6))
has_plotted = False  # 判断是否画了至少一条线

for result in st.session_state.results_list:
    if show_refl:
        ax.plot(result["wl"], result["refl"], label=f"{result['label']} - Reflectance")
        has_plotted = True
    if show_tran:
        ax.plot(result["wl"], result["tran"], label=f"{result['label']} - Transmittance")
        has_plotted = True

ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Signal")
ax.set_title("Leaf Optical Properties (PROSPECT-D)")
if has_plotted:
    ax.legend(fontsize=8)
ax.grid(True)
st.pyplot(fig)

# ========== 下载按钮 ==========
if st.session_state.results_list:
    latest = st.session_state.results_list[-1]
    txt_bytes = generate_txt(N, Cab, Car, Cw, Cm,
                             latest["wl"], latest["refl"], latest["tran"])

    filename = f"prospect_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    st.download_button(
        label="📥 下载当前模拟结果（.txt）",
        data=txt_bytes,
        file_name=filename,
        mime="text/plain"
    )
