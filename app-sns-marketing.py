import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="📱 SNS Marketing Analytics", layout="wide", page_icon="📊")

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #f59e0b, #ef4444);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 20px; font-size: 1.1rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border-radius: 10px; padding: 15px; border-left: 4px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# ── Helper Functions ─────────────────────────────────────────
def calc_engagement(likes, shares, comments, followers):
    if followers == 0:
        return 0
    return ((likes + shares + comments) / followers) * 100

def calc_roi(revenue, budget):
    if budget == 0:
        return 0
    return (revenue - budget) / budget * 100

def roi_color(roi):
    if roi >= 100: return "🟢"
    elif roi >= 0: return "🟡"
    else: return "🔴"

def roi_label(roi):
    if roi >= 100: return "Excellent"
    elif roi >= 50: return "Good"
    elif roi >= 0: return "Break-even"
    else: return "Loss"

PLATFORM_ICONS = {
    "Instagram": "📸",
    "TikTok": "🎵",
    "YouTube": "🎬",
    "Twitter/X": "🐦",
    "Facebook": "👤",
}

PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "TikTok": "#00f2ea",
    "YouTube": "#FF0000",
    "Twitter/X": "#1DA1F2",
    "Facebook": "#4267B2",
}

# ── Session State ────────────────────────────────────────────
if "campaigns" not in st.session_state:
    st.session_state.campaigns = [
        {
            "Campaign": "Summer Art Exhibition",
            "Platform": "Instagram",
            "Budget": 500_000,
            "Revenue": 1_800_000,
            "Followers": 12_000,
            "Likes": 4_500,
            "Shares": 890,
            "Comments": 320,
            "Weekly": [320, 480, 610, 890, 1200, 1450, 1600],
        },
        {
            "Campaign": "Dance Workshop Promo",
            "Platform": "TikTok",
            "Budget": 300_000,
            "Revenue": 950_000,
            "Followers": 8_500,
            "Likes": 12_000,
            "Shares": 3_200,
            "Comments": 1_800,
            "Weekly": [800, 1500, 2800, 3500, 4200, 5100, 5800],
        },
        {
            "Campaign": "Portfolio Showcase",
            "Platform": "YouTube",
            "Budget": 800_000,
            "Revenue": 600_000,
            "Followers": 3_200,
            "Likes": 450,
            "Shares": 120,
            "Comments": 85,
            "Weekly": [50, 80, 110, 95, 130, 105, 120],
        },
    ]

# ── Sidebar: Add Campaign ────────────────────────────────────
with st.sidebar:
    st.markdown("## ➕ Add New Campaign")
    st.markdown("---")

    with st.form("add_campaign", clear_on_submit=True):
        name = st.text_input("📋 Campaign Name")
        platform = st.selectbox("📱 Platform", ["Instagram", "TikTok", "YouTube", "Twitter/X", "Facebook"])
        budget = st.number_input("💸 Budget (₩)", min_value=0, value=500_000, step=50_000)
        revenue = st.number_input("💰 Revenue (₩)", min_value=0, value=0, step=50_000)
        st.markdown("**📊 Engagement Numbers:**")
        followers = st.number_input("👥 Followers", min_value=0, value=1_000, step=100)
        likes = st.number_input("❤️ Likes", min_value=0, value=0, step=100)
        shares = st.number_input("🔁 Shares", min_value=0, value=0, step=50)
        comments = st.number_input("💬 Comments", min_value=0, value=0, step=10)

        submitted = st.form_submit_button("✅ Add Campaign", use_container_width=True)
        if submitted and name:
            weekly = sorted([random.randint(50, likes // 7 + 50) for _ in range(7)])
            st.session_state.campaigns.append({
                "Campaign": name, "Platform": platform,
                "Budget": budget, "Revenue": revenue,
                "Followers": followers, "Likes": likes,
                "Shares": shares, "Comments": comments,
                "Weekly": weekly,
            })
            st.success(f"🎉 Added **{name}**!")

    st.markdown("---")
    st.markdown(f"📦 **Total campaigns:** {len(st.session_state.campaigns)}")
    total_budget = sum(c["Budget"] for c in st.session_state.campaigns)
    total_revenue = sum(c["Revenue"] for c in st.session_state.campaigns)
    st.markdown(f"💸 **Total budget:** ₩{total_budget:,}")
    st.markdown(f"💰 **Total revenue:** ₩{total_revenue:,}")

# ── Main Area ────────────────────────────────────────────────
st.markdown('<p class="big-title">📱 SNS Marketing Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track, analyze, and optimize your social media campaigns</p>', unsafe_allow_html=True)

# ── Build DataFrame ──────────────────────────────────────────
data = []
for c in st.session_state.campaigns:
    eng = calc_engagement(c["Likes"], c["Shares"], c["Comments"], c["Followers"])
    roi = calc_roi(c["Revenue"], c["Budget"])
    data.append({
        "Campaign": c["Campaign"],
        "Platform": c["Platform"],
        "Budget": c["Budget"],
        "Revenue": c["Revenue"],
        "Followers": c["Followers"],
        "Likes": c["Likes"],
        "Shares": c["Shares"],
        "Comments": c["Comments"],
        "Engagement %": round(eng, 1),
        "ROI %": round(roi, 1),
        "Status": roi_label(roi),
        "Icon": roi_color(roi),
    })
df = pd.DataFrame(data)

# ── Top Metrics ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

total_eng = df["Engagement %"].mean()
total_roi = calc_roi(df["Revenue"].sum(), df["Budget"].sum())
best = df.loc[df["ROI %"].idxmax()]

m1.metric("📊 Campaigns", len(df))
m2.metric("💰 Total Revenue", f"₩{df['Revenue'].sum():,.0f}",
          delta=f"₩{df['Revenue'].sum() - df['Budget'].sum():,.0f} profit")
m3.metric("📈 Avg Engagement", f"{total_eng:.1f}%",
          delta=f"{'Above' if total_eng > 5 else 'Below'} 5% benchmark")
m4.metric("🏆 Best Campaign", best["Campaign"],
          delta=f"ROI {best['ROI %']:.0f}%")

st.markdown("---")

# ── Campaign Cards ───────────────────────────────────────────
st.subheader("📋 Campaign Performance")

cols = st.columns(len(df))
for i, (_, row) in enumerate(df.iterrows()):
    with cols[i]:
        icon = PLATFORM_ICONS.get(row["Platform"], "📱")
        roi_emoji = row["Icon"]

        if row["ROI %"] >= 50:
            border_color = "#22c55e"
        elif row["ROI %"] >= 0:
            border_color = "#f59e0b"
        else:
            border_color = "#ef4444"

        st.markdown(f"""
        <div style="border:2px solid {border_color}; border-radius:12px; padding:15px;
                    background: linear-gradient(135deg, #ffffff, #f8fafc); text-align:center;">
            <h4 style="margin:0; color:#1e293b;">{icon} {row['Campaign']}</h4>
            <p style="color:#64748b; margin:5px 0;">{row['Platform']}</p>
            <h2 style="margin:5px 0; color:{border_color};">{roi_emoji} ROI {row['ROI %']:.0f}%</h2>
            <p style="margin:0; color:#64748b; font-size:0.85rem;">
                Engagement: {row['Engagement %']:.1f}% | {row['Status']}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── Charts Row ───────────────────────────────────────────────
left, right = st.columns(2)

# Weekly Performance Line Chart
with left:
    st.subheader("📈 Weekly Engagement Trend")
    weeks = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fig_line = go.Figure()
    for c in st.session_state.campaigns:
        color = PLATFORM_COLORS.get(c["Platform"], "#6366f1")
        fig_line.add_trace(go.Scatter(
            x=weeks, y=c["Weekly"],
            mode="lines+markers",
            name=f"{PLATFORM_ICONS.get(c['Platform'], '')} {c['Campaign']}",
            line=dict(color=color, width=3),
            marker=dict(size=8),
        ))
    fig_line.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2),
        xaxis_title="Day", yaxis_title="Engagement (interactions)",
        margin=dict(l=10, r=10, t=10, b=60),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Budget vs Revenue Bar Chart
with right:
    st.subheader("💰 Budget vs Revenue")
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        name="💸 Budget", x=df["Campaign"], y=df["Budget"],
        marker_color="#94a3b8", text=df["Budget"].apply(lambda x: f"₩{x/1000:.0f}K"),
        textposition="outside",
    ))
    fig_budget.add_trace(go.Bar(
        name="💰 Revenue", x=df["Campaign"], y=df["Revenue"],
        marker_color=df["ROI %"].apply(lambda x: "#22c55e" if x >= 0 else "#ef4444").tolist(),
        text=df["Revenue"].apply(lambda x: f"₩{x/1000:.0f}K"),
        textposition="outside",
    ))
    fig_budget.update_layout(
        barmode="group", height=400,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2),
        yaxis_title="Amount (₩)",
        margin=dict(l=10, r=10, t=10, b=60),
    )
    st.plotly_chart(fig_budget, use_container_width=True)

# ── Platform Distribution ────────────────────────────────────
st.markdown("---")
left2, right2 = st.columns(2)

with left2:
    st.subheader("📱 Platform Breakdown")
    platform_data = df.groupby("Platform").agg({
        "Engagement %": "mean", "ROI %": "mean"
    }).reset_index()
    fig_platform = px.bar(
        platform_data, x="Platform", y=["Engagement %", "ROI %"],
        barmode="group", color_discrete_sequence=["#6366f1", "#f59e0b"],
    )
    fig_platform.update_layout(
        height=350,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2), yaxis_title="Percentage (%)",
        margin=dict(l=10, r=10, t=10, b=60),
    )
    st.plotly_chart(fig_platform, use_container_width=True)

with right2:
    st.subheader("📊 Engagement Breakdown")
    total_likes = df["Likes"].sum()
    total_shares = df["Shares"].sum()
    total_comments = df["Comments"].sum()
    fig_eng = px.pie(
        values=[total_likes, total_shares, total_comments],
        names=["❤️ Likes", "🔁 Shares", "💬 Comments"],
        hole=0.45,
        color_discrete_sequence=["#ec4899", "#6366f1", "#14b8a6"],
    )
    fig_eng.update_traces(textinfo="percent+label", textfont_size=13)
    fig_eng.update_layout(
        height=350,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_eng, use_container_width=True)

# ── Data Table ───────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Full Campaign Data")
display = df.copy()
display["Budget"] = display["Budget"].apply(lambda x: f"₩{x:,}")
display["Revenue"] = display["Revenue"].apply(lambda x: f"₩{x:,}")
display["Followers"] = display["Followers"].apply(lambda x: f"{x:,}")
display["Likes"] = display["Likes"].apply(lambda x: f"{x:,}")
display["Shares"] = display["Shares"].apply(lambda x: f"{x:,}")
display["Comments"] = display["Comments"].apply(lambda x: f"{x:,}")
display["ROI %"] = display.apply(lambda r: f"{r['Icon']} {r['ROI %']}%", axis=1)
display["Engagement %"] = display["Engagement %"].apply(lambda x: f"{x}%")
show_cols = ["Campaign", "Platform", "Budget", "Revenue", "Followers",
             "Likes", "Shares", "Comments", "Engagement %", "ROI %", "Status"]
st.dataframe(display[show_cols], use_container_width=True, hide_index=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#94a3b8; font-size:0.9rem; padding:10px;">'
    '🎓 Arts and Big Data — Week 09 | Prof. Jahwan Koo | Sungkyunkwan University'
    '</div>',
    unsafe_allow_html=True
)
