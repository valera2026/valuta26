import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x500")

        # Список валют (можно расширить)
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'RUB', 'INR']

        # Поля выбора валют
        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=10, pady=10)
        self.from_currency = ttk.Combobox(root, values=self.currencies)
        self.from_currency.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=10, pady=10)
        self.to_currency = ttk.Combobox(root, values=self.currencies)
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)

        # Поле ввода суммы
        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_button = ttk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=("From", "To", "Amount", "Result"), show="headings")
        self.history_tree.heading("From", text="Из валюты")
        self.history_tree.heading("To", text="В валюту")
        self.history_tree.heading("Amount", text="Сумма")
        self.history_tree.heading("Result", text="Результат")
        self.history_tree.column("From", width=100)
        self.history_tree.column("To", width=100)
        self.history_tree.column("Amount", width=100)
        self.history_tree.column("Result", width=120)
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Загрузка истории при запуске
        self.load_history()

    def get_exchange_rate(self, from_curr, to_curr):
        api_key = "YOUR_API_KEY"  # Замените на ваш API‑ключ
        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка HTTP‑ошибок
            data = response.json()
            rate = data["rates"][to_curr]
            return rate
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить курс: {e}")
            return None
        except KeyError:
            messagebox.showerror("Ошибка", "Неверная валюта или курс недоступен")
            return None

    def load_history(self):
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
                for record in history:
                    self.history_tree.insert("", "end", values=record)
        except FileNotFoundError:
            pass

    def save_history(self, record):
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        history.append(record)
        with open("history.json", "w") as f:
            json.dump(history, f, indent=4)

    def validate_input(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return False
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            return False

    def convert(self):
        if not self.validate_input():
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        amount = float(self.amount_entry.get())

        if not from_curr or not to_curr:
            messagebox.showerror("Ошибка", "Выберите валюты для конвертации")
            return

        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return

        result = amount * rate

        # Добавляем в историю
        record = (from_curr, to_curr, amount, f"{result:.2f}")
        self.history_tree.insert("", "end", values=record)
        self.save_history(record)

        messagebox.showinfo("Результат", f"{amount} {from_curr} = {result:.2f} {to_curr}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
