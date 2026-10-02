import streamlit as st

st.set_page_config(page_title="Syndicate Engine v43", page_icon="🎯", layout="centered")
st.title("🎯 सिंडिकेट MASTER ENGINE v43.0")

def run_syndicate_engine(frbd_live, last_24h_res=None):
    if frbd_live < 10:
        frbd_live = int(f"{frbd_live:02d}")
        
    cut_map = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
    rashi_map = {1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4, 0: 5}
    
    A, B = frbd_live // 10, frbd_live % 10
    palat_live = B * 10 + A
    cut_A, cut_B = cut_map[A], cut_map[B]
    
    final_pool = []
    all_used = set()
    
    def add_to_pool(jodi_list):
        for jodi in jodi_list:
            if 0 <= jodi <= 99 and jodi not in all_used and len(final_pool) < 40:
                all_used.add(jodi)
                final_pool.append(jodi)

    add_to_pool([A * 11, B * 11, cut_A * 11, cut_B * 11])

    if last_24h_res:
        repeat_pool = []
        for r in last_24h_res:
            r_A, r_B = r // 10, r % 10
            repeat_pool.extend([r, r_B * 10 + r_A, cut_map[r_A] * 10 + r_B])
        add_to_pool(repeat_pool)

    add_to_pool([10, 19, 28, 37, 43, 46, 57, 64, 73])

    tiya_cycle = [i for i in range(100) if i // 10 == 3 or i % 10 == 3]
    frbd_core = [frbd_live, palat_live, cut_A * 10 + B, A * 10 + cut_B, cut_A * 10 + cut_B]
    add_to_pool(frbd_core + tiya_cycle)

    mirror_harufs = list(set([A, B, cut_A, cut_B]))
    crossing_pool = [h1 * 10 + h2 for h1 in mirror_harufs for h2 in mirror_harufs]
    add_to_pool(crossing_pool)

    sum_val = A + B
    f_sum = sum_val if sum_val < 10 else (sum_val // 10 + sum_val % 10)
    target_sums = [f_sum, rashi_map.get(f_sum, 5)]
    
    yogh_pool = [jodi for jodi in range(100) if (jodi//10 + jodi%10 if (jodi//10 + jodi%10)<10 else (jodi//10 + jodi%10)//10 + (jodi//10 + jodi%10)%10) in target_sums]
    add_to_pool(yogh_pool)

    add_to_pool([i for i in range(100) if i // 10 == 0 or i % 10 == 0])

    if len(final_pool) < 40:
        add_to_pool(range(100))

    return sorted(final_pool), A * 10 + cut_B

frbd_input = st.number_input("फरीदाबाद लाइव बेस नंबर (FRBD):", min_value=0, max_value=99, value=47, step=1)
past_res_input = st.text_input("पिछले 24 घंटे के नंबर (जैसे: 23, 89):", value="")

if st.button("40 जोड़ियाँ निकालें", type="primary"):
    past_list = []
    if past_res_input.strip():
        try:
            past_list = [int(x.strip()) for x in past_res_input.split(",") if x.strip().isdigit()]
        except:
            st.warning("पिछले नंबर सही दर्ज करें।")

    jodis, single_pred = run_syndicate_engine(frbd_input, past_list)
    
    st.success(f"मुख्य सिंगल प्रेडिक्शन पॉइंट: {single_pred:02d}")
    st.subheader(f"कुल तैयार चक्र ({len(jodis)} Jodis Set):")
    
    cols = st.columns(5)
    for index, jodi in enumerate(jodis):
        cols[index % 5].metric(label=f"#{index+1}", value=f"{jodi:02d}")