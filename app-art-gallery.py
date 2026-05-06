
import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="🎨 Art Gallery Dashboard", layout="wide", page_icon="🖼️")

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #6366f1, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 20px; font-size: 1.1rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border-radius: 10px; padding: 15px; border-left: 4px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# ── Helper ───────────────────────────────────────────────────
def classify_period(year):
    if year < 1800: return "🏛️ Classical"
    elif year < 1870: return "🌹 Romantic"
    elif year < 1910: return "🌊 Impressionism"
    elif year < 1945: return "🎭 Modern"
    else: return "💡 Contemporary"

PERIOD_COLORS = {
    "🏛️ Classical": "#6366f1",
    "🌹 Romantic": "#ec4899",
    "🌊 Impressionism": "#14b8a6",
    "🎭 Modern": "#f59e0b",
    "💡 Contemporary": "#ef4444",
}

# ── Session State ────────────────────────────────────────────
if "artworks" not in st.session_state:
    st.session_state.artworks = [
        {"Title": "Starry Night", "Artist": "Vincent van Gogh",
         "Year": 1889, "Medium": "Oil on canvas", "Price": 100_000_000},
        {"Title": "The Kiss", "Artist": "Gustav Klimt",
         "Year": 1907, "Medium": "Oil and gold leaf", "Price": 150_000_000},
        {"Title": "Water Lilies", "Artist": "Claude Monet",
         "Year": 1906, "Medium": "Oil on canvas", "Price": 80_000_000},
        {"Title": "Campbell's Soup Cans", "Artist": "Andy Warhol",
         "Year": 1962, "Medium": "Synthetic polymer", "Price": 12_000_000},
        {"Title": "Girl with a Pearl Earring", "Artist": "Johannes Vermeer",
         "Year": 1665, "Medium": "Oil on canvas", "Price": 200_000_000},
    ]

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ➕ Add New Artwork")
    st.markdown("---")

    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("🖼️ Title")
        artist = st.text_input("👤 Artist")
        year = st.number_input("📅 Year", min_value=1000, max_value=2026, value=2024)
        medium = st.selectbox("🎨 Medium", [
            "Oil on canvas", "Acrylic", "Watercolor", "Digital",
            "Sculpture", "Photography", "Mixed media", "Other"])
        price = st.number_input("💰 Price (₩)", min_value=0, value=10_000_000, step=1_000_000)
        submitted = st.form_submit_button("✅ Add to Gallery", use_container_width=True)

        if submitted and title and artist:
            st.session_state.artworks.append({
                "Title": title, "Artist": artist, "Year": year,
                "Medium": medium, "Price": price})
            st.success(f"🎉 Added **{title}**!")

    st.markdown("---")
    st.markdown(f"📦 **Total artworks:** {len(st.session_state.artworks)}")
    total = sum(a["Price"] for a in st.session_state.artworks)
    st.markdown(f"💎 **Collection value:** ₩{total:,}")

# ── Main Area ────────────────────────────────────────────────
st.markdown('<p class="big-title">🎨 Art Gallery Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore, search, and analyze your art collection</p>', unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.artworks)
df["Period"] = df["Year"].apply(classify_period)

# ── Metrics Row ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("🖼️ Total Artworks", len(df))
c2.metric("💰 Total Value", f"₩{df['Price'].sum():,.0f}")
c3.metric("📈 Average Price", f"₩{df['Price'].mean():,.0f}")
most_expensive = df.loc[df["Price"].idxmax()]
c4.metric("🏆 Most Expensive", most_expensive["Title"])

st.markdown("---")

# ── Search ───────────────────────────────────────────────────
search = st.text_input("🔍 Search by artist name", placeholder="e.g. van Gogh, Monet, Klimt...")

if search:
    filtered = df[df["Artist"].str.contains(search, case=False, na=False)]
    st.caption(f"Found **{len(filtered)}** artwork(s) matching '{search}'")
else:
    filtered = df

# ── Data Table ───────────────────────────────────────────────
st.subheader(f"📋 Collection ({len(filtered)} works)")
display = filtered.copy()
display["Price"] = display["Price"].apply(lambda x: f"₩{x:,}")
st.dataframe(
    display[["Title", "Artist", "Year", "Medium", "Period", "Price"]],
    use_container_width=True, hide_index=True,
    column_config={
        "Title": st.column_config.TextColumn("🖼️ Title", width="medium"),
        "Artist": st.column_config.TextColumn("👤 Artist", width="medium"),
        "Year": st.column_config.NumberColumn("📅 Year", format="%d"),
        "Medium": st.column_config.TextColumn("🎨 Medium"),
        "Period": st.column_config.TextColumn("📚 Period"),
        "Price": st.column_config.TextColumn("💰 Price", width="medium"),
    }
)

st.markdown("---")

# ── Charts ───────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("📊 Artwork Prices")
    sorted_df = filtered.sort_values("Price", ascending=True)
    fig_bar = px.bar(
        sorted_df, x="Price", y="Title", orientation="h",
        color="Period", color_discrete_map=PERIOD_COLORS,
        text=sorted_df["Price"].apply(lambda x: f"₩{x/1_000_000:.0f}M")
    )
    fig_bar.update_layout(
        showlegend=False, height=400,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis_title="", xaxis_title="Price (₩)",
        font=dict(size=12),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    st.subheader("🥧 Distribution by Art Period")
    period_data = filtered["Period"].value_counts().reset_index()
    period_data.columns = ["Period", "Count"]
    fig_pie = px.pie(
        period_data, values="Count", names="Period", hole=0.45,
        color="Period", color_discrete_map=PERIOD_COLORS,
    )
    fig_pie.update_traces(textinfo="percent+label", textfont_size=13)
    fig_pie.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Timeline Chart ───────────────────────────────────────────
st.markdown("---")
st.subheader("📅 Artworks Through Time")
fig_timeline = px.scatter(
    filtered, x="Year", y="Price", size="Price",
    color="Period", color_discrete_map=PERIOD_COLORS,
    hover_name="Title", hover_data=["Artist", "Medium"],
    size_max=40,
)
fig_timeline.update_layout(
    height=350,
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Year", yaxis_title="Price (₩)",
    margin=dict(l=10, r=10, t=10, b=40),
)
st.plotly_chart(fig_timeline, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#94a3b8; font-size:0.9rem; padding:10px;">'
    '🎓 Arts and Big Data — Week 09 | Prof. Jahwan Koo | Sungkyunkwan University'
    '</div>',
    unsafe_allow_html=True
)
