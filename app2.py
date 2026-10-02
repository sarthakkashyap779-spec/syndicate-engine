import streamlit as st

st.set_page_config(page_title="Syndicate Master Engine v33", layout="wide")

st.title("🎰 Syndicate Master Engine v33")
st.write("---")

# 1. Sidebar Inputs
st.sidebar.header("⚙️ इनपुट सेटिंग्स")
dswr_live = st.sidebar.number_input("कल सुबह का दिसावर अंक (dswr_live):", min_value=0, max_value=99, value=69)

st.sidebar.subheader("💰 प्रति जोड़ी दांव (Bets)")
stage_1_bet = st.sidebar.number_input("फरीदाबाद (Stage 1):", value=50)
stage_2_bet = st.sidebar.number_input("गाजियाबाद (Stage 2):", value=150)
stage_3_bet = st.sidebar.number_input("गली (Stage 3):", value=300)
stage_4_bet = st.sidebar.number_input("दिसावर (Stage 4):", value=500)

# 2. Logic Calculations (All Rules Included)
A = dswr_live // 10
B = dswr_live % 10
palat_live = B * 10 + A

cut_map = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
cut_A = cut_map[A]
cut_B = cut_map[B]

# 1. दोस्त का नियम
dost_ka_niyam = []
for h in [A, B]:
    for i in range(10):
        dost_ka_niyam.append(h * 10 + i)
        dost_ka_niyam.append(i * 10 + h)
dost_ka_niyam = sorted(list(set([j for j in dost_ka_niyam if 0 <= j < 100])))

# 2. बाज़ार की चाल
market_ki_chaal = [(dswr_live + k) % 100 for k in [-2, -1, 1, 2]] + [(palat_live + k) % 100 for k in [-2, -1, 1, 2]]

# 3. रवि का नियम
ravi_ka_niyam = []
for h in [cut_A, cut_B]:
    for i in range(10):
        ravi_ka_niyam.append(h * 10 + i)
        ravi_ka_niyam.append(i * 10 + h)
ravi_ka_niyam = sorted(list(set([j for j in ravi_ka_niyam if 0 <= j < 100])))

# 4. रवि का नोयम
ravi_ka_noyam = []
for j in range(100):
    j_A = j // 10
    j_B = j % 10
    if j_A in [A, B] or j_B in [A, B]:
        ravi_ka_noyam.append(j)

# 5. कट-अंक और हरूफ मिरर नियम
mirror_harufs = list(set([A, B, cut_A, cut_B]))
cut_ank_niyam = []
for h1 in mirror_harufs:
    for h2 in mirror_harufs:
        cut_ank_niyam.append(h1 * 10 + h2)
        cut_ank_niyam.append(h2 * 10 + h1)
cut_ank_niyam = sorted(list(set([j for j in cut_ank_niyam if 0 <= j < 100])))

# पंच-नियमों को मिलाकर ठीक 36 मास्टर जोड़ियाँ
master_jodi_pool = []
priority_jodis = [dswr_live, palat_live]

for j in (priority_jodis + cut_ank_niyam + dost_ka_niyam + market_ki_chaal + ravi_ka_niyam + ravi_ka_noyam):
    if j not in master_jodi_pool and 0 <= j < 100:
        master_jodi_pool.append(j)

final_36_jodis = sorted(master_jodi_pool[:36])

# 3. Output Display
st.subheader("🎰 आपकी फाइनल 36 जोड़ियों का पंच-नियम मास्टर सेट")

grid_text = ""
for i in range(0, len(final_36_jodis), 9):
    grid_text += "👉 " + ", ".join([f"`{j:02d}`" for j in final_36_jodis[i:i+9]]) + "\n\n"

st.markdown(grid_text)
st.write("---")

# 4. Loss Recovery Matrix Calculations
st.subheader("📊 📈 4-Stage Loss Recovery Matrix")

st1_inv = stage_1_bet * 36
st1_net = (stage_1_bet * 90) - st1_inv

st2_inv = stage_2_bet * 36
st2_net = (stage_2_bet * 90) - st1_inv - st2_inv

st3_inv = stage_3_bet * 36
st1_2_loss = st1_inv + st2_inv
st3_net = (stage_3_bet * 90) - st1_2_loss - st3_inv

st4_inv = stage_4_bet * 36
total_prev_loss = st1_inv + st2_inv + st3_inv
st4_net = (stage_4_bet * 90) - total_prev_loss - st4_inv

col1, col2 = st.columns(2)

with col1:
    st.info(f"**🎰 स्टेज I: फरीदाबाद (FRBD)**\n\n• दांव: ₹{stage_1_bet} | निवेश: ₹{st1_inv}\n\n• **Net Profit:** ₹{st1_net}")
    st.warning(f"**🎰 स्टेज II: गाजियाबाद (GZBD)**\n\n• दांव: ₹{stage_2_bet} | निवेश: ₹{st2_inv} | पिछला लॉस: ₹{st1_inv}\n\n• **Net Profit:** ₹{st2_net}")

with col2:
    st.error(f"**🎰 स्टेज III: गली (GALI)**\n\n• दांव: ₹{stage_3_bet} | निवेश: ₹{st3_inv} | पिछला लॉस: ₹{st1_2_loss}\n\n• **Net Profit:** ₹{st3_net}")
    st.success(f"**🎰 स्टेज IV: दिसावर (DSWR)**\n\n• दांव: ₹{stage_4_bet} | निवेश: ₹{st4_inv} | पिछला लॉस: ₹{total_prev_loss}\n\n• **Net Profit:** ₹{st4_net}")
