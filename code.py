# Python Dashboard using Streamlit
import streamlit as st
import pandas as pd
import numpy as np

# Title
st.title('Power Procurement Optimization Dashboard')

# Sidebar filters
st.sidebar.header('Dashboard Filters')
date_filter = st.sidebar.date_input('Select Date', pd.Timestamp('2025-05-25'))

# Mock Data
np.random.seed(42)
data = {
    'Hour': list(range(24)),
    'Coal': np.random.uniform(260, 280, 24),
    'Gas': np.random.uniform(120, 140, 24),
    'Renewables': np.random.uniform(150, 250, 24),
    'Market': np.random.uniform(50, 150, 24),
    'Storage': np.random.uniform(-50, 50, 24),  # Negative for charge, positive for discharge
}
df = pd.DataFrame(data)
df['Total Supplied'] = df[['Coal', 'Gas', 'Renewables', 'Market', 'Storage']].sum(axis=1)

# Costs per source (₹ per kWh)
costs = {'Coal': 6, 'Gas': 8.5, 'Renewables': 5, 'Market': 7.5, 'Storage': 1.5}

# Daily Summary
st.header('Daily Power Procurement Summary')
total_demand = 800
total_supplied = df['Total Supplied'].sum()/24
st.metric(label="Total Demand (MW)", value=total_demand)
st.metric(label="Average Supplied (MW)", value=round(total_supplied,2))

# Source Share
st.header('Power Source Share (%)')
source_share = df[['Coal', 'Gas', 'Renewables', 'Market', 'Storage']].sum().div(df['Total Supplied'].sum()) * 100
st.bar_chart(source_share)

# Hourly Demand vs Source Mix
st.header('Hourly Demand vs. Source Mix')
st.area_chart(df.set_index('Hour')[['Coal', 'Gas', 'Renewables', 'Market', 'Storage']])

# Cost Breakdown
st.header('Cost Breakdown by Source')
total_cost_by_source = {source: (df[source].sum() * costs[source] * 1000) for source in costs}
st.bar_chart(pd.Series(total_cost_by_source))
total_daily_cost = sum(total_cost_by_source.values())
st.metric(label="Total Daily Cost (₹)", value=f"₹{round(total_daily_cost,2):,}")

# Cost Analysis
st.header('Cost Optimization Tracker')
avg_cost_current = total_daily_cost / (df['Total Supplied'].sum() * 1000)
avg_cost_optimized = avg_cost_current * 0.9  # Assume 10% optimization
savings = (avg_cost_current - avg_cost_optimized) * df['Total Supplied'].sum() * 1000
st.metric(label="Current Avg. Cost (₹/kWh)", value=round(avg_cost_current,2))
st.metric(label="Optimized Avg. Cost (₹/kWh)", value=round(avg_cost_optimized,2))
st.metric(label="Estimated Daily Savings (₹)", value=f"₹{round(savings,2):,}")

# Pumped Storage Utilization
st.header('Pumped Storage Utilization')
storage_charge = abs(df[df['Storage']<0]['Storage'].sum())
storage_discharge = df[df['Storage']>0]['Storage'].sum()
round_trip_efficiency = (storage_discharge / storage_charge) * 100
storage_capacity = 250 * 24  # MW capacity for 24 hours
utilization_percentage = (storage_charge / storage_capacity) * 100

st.metric("Storage Charged (MWh)", round(storage_charge,2))
st.metric("Storage Discharged (MWh)", round(storage_discharge,2))
st.metric("Round-trip Efficiency (%)", round(round_trip_efficiency,2))
st.metric("Storage Utilization (%)", round(utilization_percentage,2))
st.metric("Total Storage Capacity (MWh)", storage_capacity)

# Open Market Purchase
st.header('Open Market Purchase Analysis')
total_market = df['Market'].sum()
st.bar_chart(df.set_index('Hour')['Market'])
st.metric(label="Total Market Purchase (MWh)", value=round(total_market,2))
