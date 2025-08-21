import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Load datasets
claims = pd.read_csv("claims_data.csv")
foods = pd.read_csv("food_listings_data.csv")
providers = pd.read_csv("providers_data2.csv")
receivers = pd.read_csv("receivers_data.csv")
final = pd.read_csv("full_data.csv")

# Dashboard Title
st.title("🍴 Local Food Wastage Management System Dashboard")

# Create Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📑 Claims Data", "🥗 Food Listings", "🏭 Providers", "🙋 Receivers", "📊 Final Data"]
)

# ----------------- TAB 1: Claims -----------------
with tab1:
    st.subheader("Claims Data Preview")
    st.dataframe(claims.head())

   

# ----------------- TAB 2: Foods -----------------
with tab2:
    st.subheader("Food Listings Preview")
    st.dataframe(foods.head())

   
# ----------------- TAB 3: Providers -----------------
with tab3:
    st.subheader("Providers Data Preview")
    st.dataframe(providers.head())

    provider_counts = providers["Type"].value_counts().reset_index()
    provider_counts.columns = ["Type", "Count"]


    fig = px.bar(
    provider_counts,
    x="Type",
    y="Count",
    title="Distribution of Provider Type",
    text="Count"
    ) 

    st.plotly_chart(fig, use_container_width=True)


# ----------------- TAB 4: Receivers -----------------
with tab4:
    st.subheader("Receivers Data Preview")
    st.dataframe(receivers.head())
    
    receiver_counts = receivers["Type"].value_counts().reset_index()
    receiver_counts.columns = ["Type", "Count"]


    fig = px.bar(
    receiver_counts,
    x="Type",
    y="Count",
    title="Distribution of Receiver Type",
    text="Count"
    ) 

    st.plotly_chart(fig, use_container_width=True)
   

# ----------------- TAB 5: Final Data -----------------
with tab5:
    st.subheader("Final Data (Merged)")
    st.dataframe(final.head())

   
     
    st.subheader("🔍 Filter Data")


    with st.sidebar:
      st.header("Filters")

    # Filter by Provider Type
    provider_type = st.multiselect(
        "Select Provider Type",
        options=final["Provider_Type"].unique(),
        default=final["Provider_Type"].unique()
    )

    # Filter by Receiver Type
    receiver_type = st.multiselect(
        "Select Receiver Type",
        options=final["Receiver_Type"].unique(),
        default=final["Receiver_Type"].unique()
    )

    # Filter by Status
    status = st.multiselect(
        "Select Status",
        options=final["Status"].unique(),
        default=final["Status"].unique()
    )

    # Filter by Meal Type
    meal_type = st.multiselect(
        "Select Meal Type",
        options=final["Meal_Type"].unique(),
        default=final["Meal_Type"].unique()
    )

    # Filter by City
    provider_city = st.multiselect(
        "Select Provider City",
        options=final["Provider_City"].unique(),
        default=final["Provider_City"].unique()
    )


    filtered_data = final[
       (final["Provider_Type"].isin(provider_type)) &
       (final["Receiver_Type"].isin(receiver_type)) &
       (final["Status"].isin(status)) &
       (final["Meal_Type"].isin(meal_type)) &
       (final["Provider_City"].isin(provider_city))
    ]

    st.subheader("📂 Filtered Dataset")
    st.dataframe(filtered_data, use_container_width=True)


    
    # --- Example KPI Cards with Filtered Data ---
    st.subheader("📊 KPIs (Based on Filters)")
    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric("Total Claims", filtered_data["Claim_ID"].nunique())

    with col2:
     st.metric("Completed Claims", (filtered_data["Status"] == "Completed").sum())

    with col3:
     st.metric("Total Quantity", int(filtered_data["Quantity"].sum()))






    st.subheader("Food Quantity by Provider Type and Food Name")

    # Group and sort data
    p3 = (
        filtered_data.groupby(["Provider_Type", "Food_Name"])["Quantity"]
        .sum()
        .reset_index(name="Total_Quantity")
        .sort_values(by="Total_Quantity", ascending=False)
    )

    
    fig = px.bar(
        p3,
        x="Provider_Type",
        y="Total_Quantity",
        color="Food_Name",
        title="Food Quantity by Provider Type",
        barmode="group"  # side-by-side bars
    )

    

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    
    p17 = final.groupby(["Days_To_Expiry"])["Quantity"].mean().reset_index()

    # Interactive line chart
    fig = px.line(
    p17,
    x="Days_To_Expiry",
    y="Quantity",
    markers=True,
    title="Average Quantity Available by Days to Expiry"
    )

    # Add expiry line
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Expiry Date")

    fig.update_layout(height=500, width=1000)

    st.plotly_chart(fig, use_container_width=True)






    st.subheader("⏰ Claims by Hour and Status")

    p8 = (
    filtered_data.groupby(["Hour", "Status"])["Claim_ID"]
    .count()
    .reset_index()
    )


    fig = px.line(
    p8,
    x="Hour",
    y="Claim_ID",
    color="Status",
    markers=True,
    title="Claims by Hour (with Status Breakdown)"
    )

    # Customize layout
    fig.update_layout(
    xaxis=dict(tickmode="linear", dtick=1, title="Hour of Day"),
    yaxis_title="Number of Claims",
    legend_title="Status",
    width=1000,
    height=500
    )

    # Show in Streamlit
    st.plotly_chart(fig, use_container_width=True)



    p5 = final.groupby(["Provider_Type", "Status"])["Provider_ID"].count().reset_index()

    # Interactive stacked bar
    fig = px.bar(
    p5,
    x="Provider_Type",
    y="Provider_ID",
    color="Status",
    title="Status wise Provider Count",
    barmode="stack",
    text_auto=True
    )

    fig.update_layout(height=600, width=900, xaxis_title="Provider Type", yaxis_title="Provider Count")

    st.plotly_chart(fig, use_container_width=True)



    p18 = filtered_data.groupby(["Food_Name","Days_To_Expiry"])["Quantity"].sum().reset_index()


    st.title("📊 Food Item Quantity by Days to Expiry")


    food_filter = st.multiselect("Select Food Items", options=p18["Food_Name"].unique(), default=p18["Food_Name"].unique())

    filtered_data = p18[p18["Food_Name"].isin(food_filter)]


    fig = px.bar(
    filtered_data,
    x="Days_To_Expiry",
    y="Quantity",
    color="Food_Name",
    barmode="group",
    title="Total Food Item Quantity Available by Days to Expiry"
    )


    fig.add_vline(x=0, line_dash="dash", line_color="red")

    st.plotly_chart(fig, use_container_width=True)



    p12 = final.pivot_table(index="Food_Name", columns="Status", values="Quantity", aggfunc="sum", fill_value=0).reset_index()

 
    p12_melted = p12.melt(id_vars="Food_Name", var_name="Status", value_name="Quantity")

 
    fig = px.density_heatmap(
    p12_melted,
    x="Status",
    y="Food_Name",
    z="Quantity",
    text_auto=True,
    color_continuous_scale="YlGnBu",
    title="Food Item Quantity wise Status"
    )

    st.plotly_chart(fig, use_container_width=True)





    st.subheader("🔥 Provider Type vs Receiver Type")

    # Create pivot table
    p4 = final.pivot_table(
    index="Provider_Type",
    columns="Receiver_Type",
    values="Provider_ID",
    aggfunc="count",
    fill_value=0
    ).reset_index()

    # Melt pivot table for Plotly (long format)
    p4_melted = p4.melt(id_vars="Provider_Type", var_name="Receiver_Type", value_name="Count")

    # Interactive Heatmap
    fig = px.density_heatmap(
    p4_melted,
    x="Receiver_Type",
    y="Provider_Type",
    z="Count",
    color_continuous_scale="Spectral",
    text_auto=True,  # show values inside cells
    title="Provider Type vs Receiver Type"
    )

    fig.update_layout(
    xaxis_title="Receiver Type",
    yaxis_title="Provider Type",
    width=800,
    height=500
    )

  # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    



    p15 = final.pivot_table(index="Provider_Name", columns="Status", values="Quantity", aggfunc="sum").fillna(0)
    p15["Total"] = p15.sum(axis=1)


    p16 = p15.sort_values(by="Total", ascending=False).head(30).reset_index()

    # Melt to long format
    p16_melted = p16.melt(id_vars=["Provider_Name","Total"], var_name="Status", value_name="Quantity")

    # 🔹 Keep Provider order same as sorted p16
    provider_order = p16["Provider_Name"].tolist()

   # Interactive heatmap
    fig = px.density_heatmap(
    p16_melted,
    x="Status",
    y="Provider_Name",
    z="Quantity",
    text_auto=True,
    color_continuous_scale="Plasma",
    title="Top Food Providers by Food Status",
    category_orders={"Provider_Name": provider_order}  # ✅ Fix row order
    )

 
    fig.update_layout(height=1500, width=1000)

    st.plotly_chart(fig, use_container_width=True)





   
    p13 = final.pivot_table(index="Receiver_Name", columns="Status", values="Quantity", aggfunc="sum").fillna(0)
    p13["Total"] = p13.sum(axis=1)

    # Top 30 receivers
    p14 = p13.sort_values(by="Total", ascending=False).head(30).reset_index()

    # Melt to long format for Plotly
    p14_melted = p14.melt(id_vars=["Receiver_Name","Total"], var_name="Status", value_name="Quantity")

    # 🔹 Keep Receiver order same as sorted p14
    receiver_order = p14["Receiver_Name"].tolist()

   # Interactive heatmap
    fig = px.density_heatmap(
    p14_melted,
    x="Status",
    y="Receiver_Name",
    z="Quantity",
    text_auto=True,
    color_continuous_scale="RdBu",
    title="Top Receivers by Food Claim Status",
    category_orders={"Receiver_Name": receiver_order}  # ✅ Fix row order
    )


    fig.update_layout(height=1500, width=1000)

    st.plotly_chart(fig, use_container_width=True)






 # ------------------------
# Tab 1 - Claims
# ------------------------
with tab1:
    
    
    # Pie Chart for Claim Status
    claim_status = claims['Status'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(claim_status, labels=claim_status.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# ------------------------
# Tab 2 - Foods
# ------------------------
with tab2:
   

    # Food type distribution
    fig2 = px.histogram(foods, x="Food_Type", color="Meal_Type", barmode="group", title="Food Type Distribution by Meal")
    st.plotly_chart(fig2, use_container_width=True)

