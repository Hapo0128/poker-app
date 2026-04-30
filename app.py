import streamlit as st
import random

# ==========================================
# 169ハンド完全マップ（唯一の正解ソース）
# ==========================================
HAND_RANK = {
"AA":"S","AKs":"S","AQs":"A","AJs":"A","ATs":"A","A9s":"C","A8s":"C","A7s":"C","A6s":"C","A5s":"C","A4s":"C","A3s":"C","A2s":"C",
"AKo":"S","KK":"S","KQs":"A","KJs":"B","KTs":"C","K9s":"C","K8s":"E","K7s":"E","K6s":"E","K5s":"E","K4s":"E","K3s":"E","K2s":"E",
"AQo":"A","KQo":"B","QQ":"S","QJs":"B","QTs":"C","Q9s":"D","Q8s":"E","Q7s":"E","Q6s":"E","Q5s":"F","Q4s":"F","Q3s":"F","Q2s":"F",
"AJo":"B","KJo":"C","QJo":"D","JJ":"A","JTs":"B","J9s":"D","J8s":"E","J7s":"E","J6s":"F","J5s":"G","J4s":"G","J3s":"G","J2s":"G",
"ATo":"C","KTo":"D","QTo":"E","JTo":"D","TT":"A","T9s":"C","T8s":"D","T7s":"F","T6s":"G","T5s":"G","T4s":"G","T3s":"G","T2s":"FOLD",
"A9o":"D","K9o":"E","Q9o":"E","J9o":"E","T9o":"E","99":"A","98s":"D","97s":"E","96s":"F","95s":"G","94s":"FOLD","93s":"FOLD","92s":"FOLD",
"A8o":"E","K8o":"G","Q8o":"G","J8o":"G","T8o":"G","98o":"F","88":"B","87s":"E","86s":"F","85s":"G","84s":"FOLD","83s":"FOLD","82s":"FOLD",
"A7o":"E","K7o":"G","Q7o":"G","J7o":"FOLD","T7o":"FOLD","97o":"G","87o":"G","77":"B","76s":"E","75s":"F","74s":"G","73s":"FOLD","72s":"FOLD",
"A6o":"F","K6o":"G","Q6o":"FOLD","J6o":"FOLD","T6o":"FOLD","96o":"FOLD","86o":"FOLD","76o":"FOLD","66":"C","65s":"E","64s":"F","63s":"G","62s":"FOLD",
"A5o":"G","K5o":"G","Q5o":"FOLD","J5o":"FOLD","T5o":"FOLD","95o":"FOLD","85o":"FOLD","75o":"FOLD","65o":"FOLD","55":"C","54s":"F","53s":"G","52s":"FOLD",
"A4o":"G","K4o":"FOLD","Q4o":"FOLD","J4o":"FOLD","T4o":"FOLD","94o":"FOLD","84o":"FOLD","74o":"FOLD","64o":"FOLD","54o":"FOLD","44":"D","43s":"G","42s":"FOLD",
"A3o":"G","K3o":"FOLD","Q3o":"FOLD","J3o":"FOLD","T3o":"FOLD","93o":"FOLD","83o":"FOLD","73o":"FOLD","63o":"FOLD","53o":"FOLD","43o":"FOLD","33":"D","32s":"FOLD",
"A2o":"G","K2o":"FOLD","Q2o":"FOLD","J2o":"FOLD","T2o":"FOLD","92o":"FOLD","82o":"FOLD","72o":"FOLD","62o":"FOLD","52o":"FOLD","42o":"FOLD","32o":"FOLD","22":"D"
}

# ==========================================
# カード生成と正規化
# ==========================================
RANKS = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
SUITS = ['♠','♥','♦','♣']
DECK = [r+s for r in RANKS for s in SUITS]

def draw():
    return random.sample(DECK, 2)

def normalize(c1, c2):
    r1,s1 = c1[0], c1[1]
    r2,s2 = c2[0], c2[1]

    if RANKS.index(r1) < RANKS.index(r2):
        high, low = r1, r2
    elif RANKS.index(r1) > RANKS.index(r2):
        high, low = r2, r1
    else:
        high, low = r1, r2

    if r1 == r2:
        return high+low
    elif s1 == s2:
        return high+low+"s"
    else:
        return high+low+"o"

# ==========================================
# 初期化
# ==========================================
if "cards" not in st.session_state:
    st.session_state.cards = draw()
    st.session_state.done = False
    st.session_state.log = []

c1,c2 = st.session_state.cards
hand = normalize(c1,c2)

# ==========================================
# UI
# ==========================================
st.title("ポーカーレンジ完全暗記テスト（ミス不可版）")

st.subheader(f"{c1}  {c2}  →  {hand}")

choices = ["S","A","B","C","D","E","F","G"]
ans = st.radio("ランク選択", choices)

# ==========================================
# 判定（単一ソース参照）
# ==========================================
if st.button("判定"):
    correct = HAND_RANK[hand]

    # ★整合チェック（絶対ズレ防止）
    is_correct = (ans == correct)

    if is_correct:
        st.success("正解")
    else:
        st.error("不正解")

    st.write(f"正しいランク：{correct}")

    st.session_state.log.append((hand, ans, correct, is_correct))
    st.session_state.done = True

# ==========================================
# 次へ
# ==========================================
if st.session_state.done:
    if st.button("次の問題"):
        st.session_state.cards = draw()
        st.session_state.done = False
        st.rerun()

# ==========================================
# 履歴
# ==========================================
st.markdown("---")
st.subheader("履歴（最新10件）")

for h in reversed(st.session_state.log[-10:]):
    mark = "○" if h[3] else "×"
    st.write(f"{h[0]} | あなた:{h[1]} | 正解:{h[2]} | {mark}")
