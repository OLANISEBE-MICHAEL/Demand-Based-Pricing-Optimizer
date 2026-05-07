
import pandas as pd

class ProcessData:

    def __init__(self, superstore_data, product_name):
        self.superstore_data = superstore_data
        self.df = self.superstore_data.copy()
        self.product_name = product_name


    def sort_data(self):
        """this method sorts the data based on the product name and the order date"""
        # we can be able to see each product and all the times they were purchased from the start to finish
        self.df = self.df.sort_values(by=["Product Name", "Order Date"])


    def get_unit_price(self):
        """this method gets the price per item"""
        self.df["Unit Price"] = round(self.df["Sales"] / self.df["Quantity"], 3)


    def get_unit_profit(self):
        """this method gets the profit to be made per item"""
        self.df["Unit Profit"] = round(self.df["Profit"] / self.df["Quantity"], 3)


    def filter_per_product(self):
        """this method filters the data based on the product name"""
        filtered_df = self.df[self.df["Product Name"] == self.product_name]
        return filtered_df


    def process_data(self):
        self.sort_data()
        self.get_unit_price()
        self.get_unit_profit()
        return self.filter_per_product()



class ProductData:

    def __init__(self, product_data: ProcessData):
        self.product_data = product_data
        self.product_df = self.product_data.process_data()
        self.df = self.product_df.copy()


    def get_previous_price(self, index):
        """this method gets the previous price of a product sold"""
        previous_price = float(self.df.loc[index, "Unit Price"])
        return previous_price


    def get_previous_quantity(self, index):
        """this method gets the previous quantity of a product"""
        previous_quantity = float(self.df.loc[index, "Quantity"])
        return previous_quantity


    def get_previous_revenue(self, index):
        """this method gets the previous revenue of a product"""
        previous_revenue = float(self.df.loc[index, "Sales"])
        return previous_revenue


    def get_previous_profit(self, index):
        """this method gets the previous profit of a product"""
        previous_profit = float(self.df.loc[index, "Unit Profit"])
        return previous_profit


    def get_price_change_percentage(self, index, previous_price):
        """this method gets the price change percentage of a product"""
        current_price = float(self.df.loc[index, "Unit Price"])
        if previous_price == 0:
            return 0
        return float((current_price - previous_price) / previous_price)


    def get_quantity_change_percentage(self, index, previous_quantity):
        """this method gets the quantity change percentage of a product"""
        current_quantity = float(self.df.loc[index, "Quantity"])
        if previous_quantity == 0:
            return 0
        return float((current_quantity - previous_quantity) / previous_quantity)


    def get_revenue_change_percentage(self, index, previous_revenue):
        """this method gets the revenue change percentage of a product"""
        current_revenue = float(self.df.loc[index, "Sales"])
        if previous_revenue == 0:
            return 0
        return float((current_revenue - previous_revenue) / previous_revenue)


    def get_profit_change_percentage(self, index, previous_profit):
        """this method gets the profit change percentage of a product"""
        current_profit = float(self.df.loc[index, "Unit Profit"])
        if previous_profit == 0:
            return 0
        return float((current_profit - previous_profit) / previous_profit)


    def calculate_price_elasticity(self, change_in_price, change_in_quantity):
        """this method calculates the price elasticity of a product using the formula %(∆Q/∆P)"""
        if change_in_price == 0 or change_in_quantity == 0:
            return 0
        return change_in_quantity / change_in_price



    def get_all_params(self):
        """this method gets all the necessary parameters we need to calculate the metrics used for the project"""

        former_index = 0
        for i, index in enumerate(self.df.index):
            if i != 0:
                previous_price = self.get_previous_price(former_index)
                previous_quantity = self.get_previous_quantity(former_index)
                previous_revenue = self.get_previous_revenue(former_index)
                previous_profit = self.get_previous_profit(former_index)
                percentage_change_in_price = self.get_price_change_percentage(index, previous_price)
                percentage_change_in_quantity = self.get_quantity_change_percentage(index, previous_quantity)
                percentage_change_in_revenue = self.get_revenue_change_percentage(index, previous_revenue)
                percentage_change_in_profit = self.get_profit_change_percentage(index, previous_profit)
                price_elasticity = self.calculate_price_elasticity(percentage_change_in_price, percentage_change_in_quantity)
            else:
                previous_price = 0
                previous_quantity = 0
                previous_revenue = 0
                previous_profit = 0
                percentage_change_in_price = 0
                percentage_change_in_quantity = 0
                percentage_change_in_revenue = 0
                percentage_change_in_profit = 0
                price_elasticity = 0

            self.df.loc[index, "Previous Price"] = previous_price
            self.df.loc[index, "Previous Quantity"] = previous_quantity
            self.df.loc[index, "Previous Revenue"] = previous_revenue
            self.df.loc[index, "Previous Profit"] = previous_profit
            self.df.loc[index, "% Change in Price"] = percentage_change_in_price
            self.df.loc[index, "% Change in Quantity"] = percentage_change_in_quantity
            self.df.loc[index, "% Change in Revenue"] = percentage_change_in_revenue
            self.df.loc[index, "% Change in Profit"] = percentage_change_in_profit
            self.df.loc[index, "Price Elasticity"] = price_elasticity
            former_index = index



class CalculateMetrics:

    def __init__(self, product_obj : ProductData):
        self.product_obj = product_obj
        self.product_obj.get_all_params()
        self.df = self.product_obj.df.copy()
        self.product_name = self.df["Product Name"].tolist()[0]
        self.average_elasticity = 0
        self.revenue_trend = None
        self.profit_trend = None
        self.decision = None

    def ignore_zero_elasticity(self):
        for index in self.df.index:
                if self.df.loc[index, "Price Elasticity"] == 0:
                    self.df = self.df.drop(index)


    def calculate_average_elasticity(self):
        # ignore outliers
        self.df = self.df[(self.df["Price Elasticity"] >= -5) & (self.df["Price Elasticity"] <= 5)]
        elasticity_values =self.df["Price Elasticity"]
        self.average_elasticity = float(elasticity_values.mean())



    def determine_revenue_trend(self):
        revenue_avg = float(self.df["% Change in Revenue"].mean())
        if revenue_avg > 0:
            self.revenue_trend = "increasing"
        elif revenue_avg < 0:
            self.revenue_trend = "decreasing"
        else:
            self.revenue_trend = "stable"


    def determine_profit_trend(self):
        profit_avg = float(self.df["% Change in Profit"].mean())
        if profit_avg > 0:
            self.profit_trend = "increasing"
        elif profit_avg < 0:
            self.profit_trend = "decreasing"
        else:
            self.profit_trend = "stable"



    def make_decision(self):
        if self.average_elasticity > 1:
            if self.revenue_trend == "decreasing":
                self.decision = "Decrease Price"
            else:
                self.decision = "slightly reduce or monitor"

        elif self.average_elasticity < 1:
            if self.profit_trend == "increasing":
                self.decision = "Increase Price"
            else:
                self.decision = "Keep Price"

        elif type(self.average_elasticity) != int or type(self.average_elasticity) != float:
            self.decision = "Insufficient Price Variation"

        else:
            self.decision = "Keep Price"



    def combine_metrics(self):
        self.ignore_zero_elasticity()
        self.calculate_average_elasticity()
        self.determine_revenue_trend()
        self.determine_profit_trend()
        self.make_decision()


        metrics = {
            "Product Name" : self.product_name,
            "Number of Sales": self.df.shape[0],
            "Price Elasticity (AVG)": self.average_elasticity,
            "Revenue Trend": self.revenue_trend,
            "Profit Trend": self.profit_trend,
            "Final Decision": self.decision,
        }

        return metrics



    def convert_to_excel(self, all_metrics):
        df = pd.DataFrame(all_metrics)
        df = df.fillna("N/A")
        df.to_excel("outputs/product_metrics.xlsx", index = False)




def run_analysis():
    filepath = "/Demand_based_price_optimisation/data/SuperStore Sales DataSet.xlsx"
    df = pd.read_excel(filepath, engine="openpyxl")
    all_unique_product = list(df["Product Name"].unique())
    all_metrics = {
        "Product Name": [],
        "Number of Sales": [],
        "Price Elasticity (AVG)": [],
        "Revenue Trend": [],
        "Profit Trend": [],
        "Final Decision": [],
    }


    # all product metrics
    for product in all_unique_product:
        process_data = ProcessData(df, product)
        product_data = ProductData(process_data)
        calc = CalculateMetrics(product_data)
        metric = calc.combine_metrics()
        print(metric)
        for metric_name in all_metrics:
            all_metrics[metric_name].append(metric[metric_name])

    calc.convert_to_excel(all_metrics)


run_analysis()


