import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Kenya Trade Dashboard", layout="wide")

# Dashboard title
st.title("🌍 Kenya Trade Dashboard")
st.markdown("#### Exports & Imports Analysis | 2023 – 2025")
st.markdown("---")

# Generate trade data for Kenya
def generate_trade_data():
    np.random.seed(42)
    
    # Date range: Monthly from Jan 2023 to Dec 2025
    dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="ME")
    
    # Top export products (Kenya's key exports)
    export_products = {
        "Tea": 12000,
        "Coffee": 8000,
        "Horticulture (Flowers)": 15000,
        "Horticulture (Vegetables)": 7000,
        "Textiles & Apparel": 5000,
        "Titanium Ores": 4000,
        "Soda Ash": 3500,
        "Petroleum Products": 6000,
        "Fish & Seafood": 3000,
        "Cashew Nuts": 2000
    }
    
    # Top import products (Kenya's key imports)
    import_products = {
        "Machinery & Equipment": 25000,
        "Petroleum Oil": 45000,
        "Vehicles & Parts": 18000,
        "Pharmaceuticals": 12000,
        "Plastics": 8000,
        "Iron & Steel": 10000,
        "Wheat": 6000,
        "Rice": 5000,
        "Electronic Equipment": 15000,
        "Fertilizers": 7000
    }
    
    # Trading partners
    trading_partners = ["China", "India", "UAE", "USA", "Germany", "UK", "Netherlands", "Uganda", "Tanzania", "South Africa"]
    
    data = []
    
    for date in dates:
        year = date.year
        month = date.month
        month_name = date.strftime("%b")
        
        # Seasonal factors
        if month == 12:
            season_export = 1.3
            season_import = 1.2
        elif month in [6, 7, 8]:
            season_export = 0.9
            season_import = 1.0
        elif month in [1, 2]:
            season_export = 0.7
            season_import = 0.8
        else:
            season_export = 1.0
            season_import = 1.0
        
        # Yearly growth
        growth_export = 1 + (year - 2023) * 0.08
        growth_import = 1 + (year - 2023) * 0.05
        
        # EXPORT DATA
        for product, base_value in export_products.items():
            value = base_value * season_export * growth_export * np.random.uniform(0.85, 1.15)
            value = round(value * 1000, 2)
            partner = np.random.choice(trading_partners, p=[0.25, 0.15, 0.12, 0.10, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04])
            
            data.append({
                "Date": date,
                "Year": year,
                "Month": month_name,
                "Quarter": f"Q{(month-1)//3 + 1}",
                "Product": product,
                "Category": "Export",
                "Trade_Value": value,
                "Trading_Partner": partner,
                "Volume": round(value / np.random.uniform(50, 500), 0)
            })
        
        # IMPORT DATA
        for product, base_value in import_products.items():
            value = base_value * season_import * growth_import * np.random.uniform(0.85, 1.15)
            value = round(value * 1000, 2)
            partner = np.random.choice(trading_partners, p=[0.30, 0.18, 0.12, 0.08, 0.07, 0.07, 0.06, 0.05, 0.04, 0.03])
            
            data.append({
                "Date": date,
                "Year": year,
                "Month": month_name,
                "Quarter": f"Q{(month-1)//3 + 1}",
                "Product": product,
                "Category": "Import",
                "Trade_Value": value,
                "Trading_Partner": partner,
                "Volume": round(value / np.random.uniform(100, 1000), 0)
            })
    
    df = pd.DataFrame(data)
    return df

# Load data
df = generate_trade_data()

# Calculate totals for KPIs
exports_df = df[df["Category"] == "Export"]
imports_df = df[df["Category"] == "Import"]

total_exports = exports_df["Trade_Value"].sum()
total_imports = imports_df["Trade_Value"].sum()
trade_balance = total_exports - total_imports
total_trade = total_exports + total_imports

# Best months for exports
best_export_month = exports_df.groupby("Month")["Trade_Value"].sum().idxmax()
best_export_value = exports_df.groupby("Month")["Trade_Value"].sum().max() / 1e6

# Top trading partner
top_export_partner = exports_df.groupby("Trading_Partner")["Trade_Value"].sum().idxmax()
top_import_partner = imports_df.groupby("Trading_Partner")["Trade_Value"].sum().idxmax()

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")

years = st.sidebar.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
df = df[df["Year"].isin(years)]

categories = st.sidebar.multiselect("Select Trade Type", ["Export", "Import"], default=["Export", "Import"])
df = df[df["Category"].isin(categories)]

partners = st.sidebar.multiselect("Select Trading Partner", df["Trading_Partner"].unique(), default=df["Trading_Partner"].unique())
df = df[df["Trading_Partner"].isin(partners)]

# Key Metrics Row
st.header("📊 Trade Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Total Exports", f"USD {total_exports/1e6:.1f}M")
with col2:
    st.metric("📦 Total Imports", f"USD {total_imports/1e6:.1f}M")
with col3:
    st.metric("⚖️ Trade Balance", f"USD {trade_balance/1e6:.1f}M")
with col4:
    st.metric("🌍 Total Trade Volume", f"USD {total_trade/1e6:.1f}M")
with col5:
    st.metric("📈 Best Export Month", f"{best_export_month}", delta=f"USD {best_export_value:.0f}M")

st.markdown("---")

# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trade Trends", 
    "📊 Exports vs Imports", 
    "🌍 Trading Partners",
    "🏭 Product Analysis",
    "📋 Data & Insights"
])

# TAB 1: Trade Trends
with tab1:
    st.subheader("Monthly Trade Trends (2023-2025)")
    
    monthly_trade = df.groupby(["Date", "Category"])["Trade_Value"].sum().reset_index()
    monthly_trade = monthly_trade.sort_values("Date")
    
    fig1 = px.line(
        monthly_trade,
        x="Date",
        y="Trade_Value",
        color="Category",
        title="Monthly Exports vs Imports",
        markers=True,
        color_discrete_map={"Export": "#2ecc71", "Import": "#e74c3c"}
    )
    fig1.update_layout(xaxis_title="Date", yaxis_title="Trade Value (USD)")
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        yearly_trade = df.groupby(["Year", "Category"])["Trade_Value"].sum().reset_index()
        fig2 = px.bar(
            yearly_trade,
            x="Year",
            y="Trade_Value",
            color="Category",
            title="Yearly Trade Comparison",
            barmode="group",
            text_auto=True,
            color_discrete_map={"Export": "#2ecc71", "Import": "#e74c3c"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        yearly_balance = df.pivot_table(values="Trade_Value", index="Year", columns="Category", aggfunc="sum").reset_index()
        yearly_balance["Balance"] = yearly_balance["Export"] - yearly_balance["Import"]
        
        fig3 = px.bar(
            yearly_balance,
            x="Year",
            y="Balance",
            title="Trade Balance by Year (USD)",
            text_auto=True,
            color="Balance",
            color_continuous_scale="RdYlGn"
        )
        fig3.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("Seasonal Trade Patterns")
    
    pivot_exports = df[df["Category"] == "Export"].pivot_table(
        values="Trade_Value", index="Year", columns="Month", aggfunc="sum", fill_value=0
    )
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot_exports = pivot_exports[[m for m in month_order if m in pivot_exports.columns]]
    
    fig4 = px.imshow(
        pivot_exports / 1e6,
        text_auto=True,
        aspect="auto",
        title="Export Value Heatmap (USD Millions)",
        labels={"x": "Month", "y": "Year", "color": "USD (M)"},
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig4, use_container_width=True)

# TAB 2: Exports vs Imports Analysis
with tab2:
    st.subheader("Exports vs Imports Deep Dive")
    
    monthly_stack = df.groupby(["Date", "Category"])["Trade_Value"].sum().reset_index()
    monthly_stack = monthly_stack.sort_values("Date")
    
    fig5 = px.area(
        monthly_stack,
        x="Date",
        y="Trade_Value",
        color="Category",
        title="Cumulative Trade Volume Over Time",
        color_discrete_map={"Export": "#2ecc71", "Import": "#e74c3c"},
        groupnorm=None
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_by_category = df.groupby("Category")["Trade_Value"].sum().reset_index()
        fig6 = px.pie(
            total_by_category,
            values="Trade_Value",
            names="Category",
            title="Overall Trade Distribution",
            hole=0.4,
            color="Category",
            color_discrete_map={"Export": "#2ecc71", "Import": "#e74c3c"}
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        ratio_data = df.pivot_table(values="Trade_Value", index="Year", columns="Category", aggfunc="sum").reset_index()
        ratio_data["Exp/Imp_Ratio"] = ratio_data["Export"] / ratio_data["Import"]
        
        fig7 = px.line(
            ratio_data,
            x="Year",
            y="Exp/Imp_Ratio",
            title="Export/Import Ratio by Year",
            markers=True,
            range_y=[0, ratio_data["Exp/Imp_Ratio"].max() + 0.2]
        )
        fig7.add_hline(y=1, line_dash="dash", line_color="red")
        st.plotly_chart(fig7, use_container_width=True)
    
    st.subheader("Quarterly Trade Performance")
    quarterly = df.groupby(["Year", "Quarter", "Category"])["Trade_Value"].sum().reset_index()
    
    fig8 = px.bar(
        quarterly,
        x="Quarter",
        y="Trade_Value",
        color="Category",
        facet_col="Year",
        title="Quarterly Trade by Year",
        barmode="group",
        color_discrete_map={"Export": "#2ecc71", "Import": "#e74c3c"}
    )
    st.plotly_chart(fig8, use_container_width=True)

# TAB 3: Trading Partners
with tab3:
    st.subheader("Top Trading Partners")
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_export_partners = df[df["Category"] == "Export"].groupby("Trading_Partner")["Trade_Value"].sum().sort_values(ascending=False).head(10)
        fig9 = px.bar(
            x=top_export_partners.values / 1e6,
            y=top_export_partners.index,
            orientation="h",
            title="Top 10 Export Destinations (USD Millions)",
            labels={"x": "Trade Value (USD Millions)", "y": ""},
            color=top_export_partners.values,
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        top_import_partners = df[df["Category"] == "Import"].groupby("Trading_Partner")["Trade_Value"].sum().sort_values(ascending=False).head(10)
        fig10 = px.bar(
            x=top_import_partners.values / 1e6,
            y=top_import_partners.index,
            orientation="h",
            title="Top 10 Import Sources (USD Millions)",
            labels={"x": "Trade Value (USD Millions)", "y": ""},
            color=top_import_partners.values,
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    st.subheader("Trade Balance by Partner")
    partner_balance = df.pivot_table(values="Trade_Value", index="Trading_Partner", columns="Category", aggfunc="sum").fillna(0)
    partner_balance["Balance"] = partner_balance["Export"] - partner_balance["Import"]
    partner_balance = partner_balance.sort_values("Balance", ascending=False).head(15)
    
    fig11 = px.bar(
        x=partner_balance.index,
        y=partner_balance["Balance"] / 1e6,
        title="Trade Balance by Partner (USD Millions)",
        labels={"x": "Trading Partner", "y": "Trade Balance (USD Millions)"},
        color=partner_balance["Balance"],
        color_continuous_scale="RdYlGn"
    )
    fig11.add_hline(y=0, line_dash="dash", line_color="black")
    st.plotly_chart(fig11, use_container_width=True)
    
    st.subheader("Trade Distribution Treemap")
    partner_treemap = df.groupby(["Category", "Trading_Partner"])["Trade_Value"].sum().reset_index()
    
    fig12 = px.treemap(
        partner_treemap,
        path=["Category", "Trading_Partner"],
        values="Trade_Value",
        title="Trade Value Distribution by Category and Partner",
        color="Trade_Value",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig12, use_container_width=True)

# TAB 4: Product Analysis
with tab4:
    st.subheader("Product Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_exports = df[df["Category"] == "Export"].groupby("Product")["Trade_Value"].sum().sort_values(ascending=False).head(10)
        fig13 = px.bar(
            x=top_exports.values / 1e6,
            y=top_exports.index,
            orientation="h",
            title="Top 10 Export Products (USD Millions)",
            labels={"x": "Export Value (USD Millions)", "y": ""},
            color=top_exports.values,
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig13, use_container_width=True)
    
    with col2:
        top_imports = df[df["Category"] == "Import"].groupby("Product")["Trade_Value"].sum().sort_values(ascending=False).head(10)
        fig14 = px.bar(
            x=top_imports.values / 1e6,
            y=top_imports.index,
            orientation="h",
            title="Top 10 Import Products (USD Millions)",
            labels={"x": "Import Value (USD Millions)", "y": ""},
            color=top_imports.values,
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig14, use_container_width=True)
    
    st.subheader("Key Product Growth Trends (2023-2025)")
    
    top_5_exports = df[df["Category"] == "Export"].groupby("Product")["Trade_Value"].sum().nlargest(5).index
    top_5_imports = df[df["Category"] == "Import"].groupby("Product")["Trade_Value"].sum().nlargest(5).index
    
    export_trend = df[(df["Category"] == "Export") & (df["Product"].isin(top_5_exports))].groupby(["Year", "Product"])["Trade_Value"].sum().reset_index()
    import_trend = df[(df["Category"] == "Import") & (df["Product"].isin(top_5_imports))].groupby(["Year", "Product"])["Trade_Value"].sum().reset_index()
    
    fig15 = px.line(
        export_trend,
        x="Year",
        y="Trade_Value",
        color="Product",
        title="Top 5 Export Products Growth Trends",
        markers=True
    )
    st.plotly_chart(fig15, use_container_width=True)
    
    fig16 = px.line(
        import_trend,
        x="Year",
        y="Trade_Value",
        color="Product",
        title="Top 5 Import Products Growth Trends",
        markers=True
    )
    st.plotly_chart(fig16, use_container_width=True)
    
    st.subheader("Product Category Distribution")
    product_sunburst = df.groupby(["Category", "Product"])["Trade_Value"].sum().reset_index()
    
    fig17 = px.sunburst(
        product_sunburst,
        path=["Category", "Product"],
        values="Trade_Value",
        title="Trade Value Sunburst Chart",
        color="Trade_Value",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig17, use_container_width=True)

# TAB 5: Data & Insights
with tab5:
    st.subheader("Key Trade Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📈 **Export Growth**")
        export_2023 = exports_df[exports_df["Year"] == 2023]["Trade_Value"].sum() if 2023 in exports_df["Year"].values else 0
        export_2025 = exports_df[exports_df["Year"] == 2025]["Trade_Value"].sum() if 2025 in exports_df["Year"].values else 0
        if export_2023 > 0:
            export_growth = ((export_2025 - export_2023) / export_2023) * 100
            st.metric("Export Growth (2023-2025)", f"{export_growth:.1f}%")
        
        st.info("🌍 **Top Export Destination**")
        st.metric("Leading Export Partner", top_export_partner)
        
        st.info("📦 **Top Import Source**")
        st.metric("Leading Import Partner", top_import_partner)
    
    with col2:
        st.warning("⚠️ **Trade Balance Alert**")
        if trade_balance < 0:
            deficit_pct = (abs(trade_balance) / total_imports) * 100 if total_imports > 0 else 0
            st.metric("Current Trade Balance", f"USD {trade_balance/1e6:.1f}M")
        else:
            st.success("Trade Surplus Achieved!")
        
        st.info("🍵 **Kenya's Top Export**")
        top_export = df[df["Category"] == "Export"].groupby("Product")["Trade_Value"].sum().idxmax()
        top_export_value = df[df["Category"] == "Export"].groupby("Product")["Trade_Value"].sum().max() / 1e6
        st.metric("Leading Export Product", top_export, delta=f"USD {top_export_value:.0f}M")
        
        st.info("🛢️ **Kenya's Top Import**")
        top_import = df[df["Category"] == "Import"].groupby("Product")["Trade_Value"].sum().idxmax()
        top_import_value = df[df["Category"] == "Import"].groupby("Product")["Trade_Value"].sum().max() / 1e6
        st.metric("Leading Import Product", top_import, delta=f"USD {top_import_value:.0f}M")
    
    # Raw data table
    st.subheader("Detailed Trade Data")
    display_df = df.copy()
    display_df["Trade_Value_Millions"] = display_df["Trade_Value"] / 1e6
    st.dataframe(display_df[["Year", "Month", "Category", "Product", "Trading_Partner", "Trade_Value_Millions"]].head(100), use_container_width=True)
    
    # Download button
    st.subheader("📎 Export Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Trade Data as CSV",
        data=csv,
        file_name="kenya_trade_data_2023_2025.csv",
        mime="text/csv"
    )
    
    # Summary statistics table
    st.subheader("Summary Statistics by Year")
    summary_stats = df.groupby(["Year", "Category"]).agg({
        "Trade_Value": ["sum", "mean", "count"]
    }).round(2)
    summary_stats["Total_USD_Millions"] = summary_stats["Trade_Value"]["sum"] / 1e6 if "sum" in summary_stats["Trade_Value"] else 0
    st.dataframe(summary_stats, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Kenya Trade Dashboard | Data Source: Simulated based on Kenya trade patterns | 2023-2025")
