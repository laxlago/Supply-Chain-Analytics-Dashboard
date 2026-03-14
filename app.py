import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# LOAD DATA
df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin1")
df.columns = df.columns.str.replace(" ", "_")

# KPI METRICS
total_sales = df["Sales_per_customer"].sum()
total_orders = df.shape[0]
total_profit = df["Benefit_per_order"].sum()


# PROFIT VS SALES

profit_sales = df.groupby("Category_Name")[["Sales_per_customer","Benefit_per_order"]].sum().reset_index()

profit_sales_fig = px.scatter(
    profit_sales,
    x="Sales_per_customer",
    y="Benefit_per_order",
    size="Sales_per_customer",
    color="Category_Name",
    title="Profit vs Sales by Category",
    template="plotly_dark"
)

profit_sales_fig.update_layout(transition_duration=500)


# GLOBAL MAP

country_orders = df.groupby("Order_Country").size().reset_index(name="Orders")

map_fig = px.choropleth(
    country_orders,
    locations="Order_Country",
    locationmode="country names",
    color="Orders",
    color_continuous_scale="Blues",
    title="Customer Orders by Country",
    template="plotly_dark"
)

map_fig.update_layout(transition_duration=500)


# DELIVERY PERFORMANCE

delivery_status = df["Delivery_Status"].value_counts().reset_index()
delivery_status.columns = ["Status","Count"]

delivery_fig = px.pie(
    delivery_status,
    names="Status",
    values="Count",
    hole=0.45,
    title="Delivery Performance",
    template="plotly_dark"
)

delivery_fig.update_layout(transition_duration=500)

# TOP PRODUCTS

top_products = df.groupby("Product_Name")["Sales_per_customer"].sum().reset_index()

top_products = top_products.sort_values(
    by="Sales_per_customer",
    ascending=False
).head(10)

top_products_fig = px.bar(
    top_products,
    x="Sales_per_customer",
    y="Product_Name",
    orientation="h",
    color="Sales_per_customer",
    color_continuous_scale="Blues",
    title="Top 10 Products by Sales",
    template="plotly_dark"
)

top_products_fig.update_layout(transition_duration=500)


# DASH APP

app = dash.Dash(__name__)


# LAYOUT

app.layout = html.Div([

html.H1(
"📦 Supply Chain Analytics Dashboard",
style={
"textAlign":"center",
"color":"#3B82F6",
"marginBottom":"40px"
}
),

# DROPDOWN
html.Div([

html.Label(
"Select Product Category",
style={"color":"white","fontSize":"18px"}
),

dcc.Dropdown(
id="category_filter",
options=[{"label":c,"value":c} for c in df["Category_Name"].unique()],
value=df["Category_Name"].unique()[0]
)

], style={
"width":"40%",
"margin":"auto",
"marginBottom":"40px"
}),

# KPI CARDS
html.Div([

html.Div([
html.H4("💰 Total Sales"),
html.H2(f"${total_sales:,.0f}")
], style={
"background":"#1DA1F2",
"padding":"25px",
"borderRadius":"12px",
"textAlign":"center",
"color":"white",
"flex":"1",
"margin":"10px",
"boxShadow":"0px 0px 20px rgba(29,161,242,0.6)"
}),

html.Div([
html.H4("📦 Total Orders"),
html.H2(total_orders)
], style={
"background":"#2563EB",
"padding":"25px",
"borderRadius":"12px",
"textAlign":"center",
"color":"white",
"flex":"1",
"margin":"10px",
"boxShadow":"0px 0px 20px rgba(37,99,235,0.6)"
}),

html.Div([
html.H4("📈 Total Profit"),
html.H2(f"${total_profit:,.0f}")
], style={
"background":"#1E40AF",
"padding":"25px",
"borderRadius":"12px",
"textAlign":"center",
"color":"white",
"flex":"1",
"margin":"10px",
"boxShadow":"0px 0px 20px rgba(30,64,175,0.6)"
})

], style={
"display":"flex",
"justifyContent":"space-between",
"gap":"20px",
"marginBottom":"40px"
}),

# ROW 1
html.Div([

html.Div([
dcc.Graph(id="sales_chart")
], style={"width":"48%","display":"inline-block"}),

html.Div([
dcc.Graph(figure=profit_sales_fig)
], style={"width":"48%","display":"inline-block"})

]),

# ROW 2
html.Div([

html.Div([
dcc.Graph(figure=map_fig)
], style={"width":"48%","display":"inline-block"}),

html.Div([
dcc.Graph(figure=delivery_fig)
], style={"width":"48%","display":"inline-block"})

]),

# TOP PRODUCTS
dcc.Graph(figure=top_products_fig)

], style={
"backgroundColor":"#0F172A",
"padding":"40px",
"fontFamily":"Segoe UI"
})


# CALLBACK

@app.callback(
Output("sales_chart","figure"),
Input("category_filter","value")
)
def update_chart(selected_category):

    filtered_df = df[df["Category_Name"] == selected_category]

    product_sales = filtered_df.groupby("Product_Name")["Sales_per_customer"].sum().reset_index()

    product_sales = product_sales.sort_values(
        by="Sales_per_customer",
        ascending=False
    ).head(10)

    fig = px.bar(
        product_sales,
        x="Sales_per_customer",
        y="Product_Name",
        orientation="h",
        color="Sales_per_customer",
        color_continuous_scale="Blues",
        title="Top Products in Selected Category",
        template="plotly_dark"
    )

    fig.update_layout(transition_duration=500)

    return fig


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)