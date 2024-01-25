import requests
import tkinter as tk
from forex_python.converter import CurrencyRates


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.c = CurrencyRates()
        self.exchange_rates = self.get_latest_exchange_rates()

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = tk.Label(root, text="From Currency:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.from_currency_var = tk.StringVar()
        self.from_currency_menu = tk.OptionMenu(root, self.from_currency_var, *self.exchange_rates.keys())
        self.from_currency_menu.grid(row=1, column=1, padx=10, pady=10)

        self.to_currency_label = tk.Label(root, text="To Currency:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.to_currency_var = tk.StringVar()
        self.to_currency_menu = tk.OptionMenu(root, self.to_currency_var, *self.exchange_rates.keys())
        self.to_currency_menu.grid(row=2, column=1, padx=10, pady=10)

        self.result_label = tk.Label(root, text="Result:")
        self.result_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        self.result_var = tk.StringVar()
        self.result_label_value = tk.Label(root, textvariable=self.result_var, font=("Helvetica", 12))
        self.result_label_value.grid(row=3, column=1, padx=10, pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=4, column=1, pady=10)

    def get_latest_exchange_rates(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            response.raise_for_status()
            data = response.json()
            rates = data.get('rates', {})
            return rates
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return {}

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_var.get()
            to_currency = self.to_currency_var.get()

            rate = self.c.get_rate(from_currency, to_currency)
            converted_amount = round(amount * rate, 2)

            result_text = f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
            self.result_var.set(result_text)

        except ValueError:
            self.result_var.set("Invalid input. Please enter a valid number.")
        except requests.exceptions.RequestException as e:
            self.result_var.set(f"Error fetching exchange rates: {str(e)}")
        except Exception as e:
            self.result_var.set(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    converter = CurrencyConverter(root)
    root.mainloop()
