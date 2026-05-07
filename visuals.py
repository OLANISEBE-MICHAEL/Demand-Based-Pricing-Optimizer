import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Visuals:

    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.fig = make_subplots(
            rows=3,
            cols=6,
            row_heights=[0.20, 0.40, 0.40],
            vertical_spacing=0.1,
            specs=[
                [
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                ],

                [
                    {"type": "xy", "colspan": 6},
                    None,
                    None,
                    None,
                    None,
                    None,
                ],

                [
                    {"type": "xy", "colspan": 6},
                    None,
                    None,
                    None,
                    None,
                    None,
                ],



            ]


        )

        self.df["Price Elasticity (AVG)"] = pd.to_numeric(
            self.df["Price Elasticity (AVG)"],
            errors="coerce",
        )
        self.elasticity_values = self.df[(self.df["Price Elasticity (AVG)"] >= -5) & (self.df["Price Elasticity (AVG)"] <= 5)]["Price Elasticity (AVG)"]

        self.total_product = self.df.shape[0]
        self.increase_price = self.df[self.df["Final Decision"] == "Increase Price"].shape[0]
        self.decrease_price = self.df[self.df["Final Decision"] == "Decrease Price"].shape[0]
        self.keep_price = self.df[self.df["Final Decision"] == "Keep Price"].shape[0]
        self.insufficient_variations = self.df[self.df["Final Decision"] == "Insufficient Price Variation"].shape[0]
        self.monitor = self.df[self.df["Final Decision"] == "slightly reduce or monitor"].shape[0]


    def total_product_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.total_product,
                title={"text": "Total Product"},
            ),
            row=1,
            col=1,
        )


    def increase_price_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.increase_price,
                title={"text": "Increase Price"},
            ),
            row=1,
            col=2,
        )


    def decrease_price_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.decrease_price,
                title={"text": "Decrease Price"},
            ),
            row=1,
            col=3,
        )


    def keep_price_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.keep_price,
                title={"text": "Keep Price"},
            ),
            row=1,
            col=4,
        )


    def insufficient_variations_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.insufficient_variations,
                title={"text": "Insufficient Price Variations"},
            ),
            row=1,
            col=5,
        )


    def monitor_kpi(self):
        self.fig.add_trace(
            go.Indicator(
                mode="number",
                value=self.monitor,
                title={"text": "Monitor"},
            ),
            row=1,
            col=6,
        )


    def create_kpi_component(self):
        self.total_product_kpi()
        self.increase_price_kpi()
        self.decrease_price_kpi()
        self.keep_price_kpi()
        self.insufficient_variations_kpi()
        self.monitor_kpi()


    def create_bar_chart(self):
        labels = [
            "Increase Price",
            "Decrease Price",
            "Keep Price",
            "Monitor",
            "Insufficient Variation"
        ]

        counts = [
            self.increase_price,
            self.decrease_price,
            self.keep_price,
            self.monitor,
            self.insufficient_variations
        ]

        self.fig.add_trace(
            go.Bar(
                x=labels,
                y=counts,
                name="Decision Distribution",
            ),
            row=2,
            col=1,
        )


    def create_histogram(self):
        # we only need elasticity greater than 0
        self.fig.add_trace(
            go.Histogram(
                x=self.elasticity_values,
                nbinsx=15,
                name="Elasticity Histogram",
            ),
            row=3,
            col=1,
        )


    def display_visuals(self):
        self.create_kpi_component()
        self.create_bar_chart()
        self.create_histogram()
        self.fig.update_layout(height=800)
        self.fig.show()



filepath = "/Demand_based_price_optimisation/outputs/product_metrics.xlsx"
visuals = Visuals(filepath)
visuals.display_visuals()