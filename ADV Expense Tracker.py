import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

# Load or create file
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
else:
    df = pd.DataFrame(columns=["date", "expense_type", "amount"])


print("Welcome to Advanced Expense Tracker 📊")

while True:
    print("\nMenu:")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Category-wise Analysis")
    print("5. Monthly Analysis")
    print("6. Show Graph")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format! Please enter in YYYY-MM-DD format.")
            continue

        expense_type = input("Enter expense type (Food, Travel, etc): ")

        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount!")
            continue

        new_data = pd.DataFrame({
            "date": [pd.to_datetime(date)],
            "expense_type": [expense_type],
            "amount": [amount]
        })

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        print("✅ Expense Added Successfully!")

    elif choice == "2":
        if df.empty:
            print("No expenses found!")
        else:
            print(df.to_string(index=False))

    elif choice == "3":
        print("💰 Total Expense:", df["amount"].sum())

    elif choice == "4":
        if df.empty:
            print("No data available")
        else:
            print("\n📊 Category-wise Spending:")
            category_summary = df.groupby("expense_type")["amount"].sum()

            for category, total in category_summary.items():
                print(f"{category}: ₹{total}")

    elif choice == "5":
        if df.empty:
            print("No data available")
        else:
            df["month"] = df["date"].dt.to_period("M")

            print("\n📅 Monthly Spending:")
            monthly_summary = df.groupby("month")["amount"].sum()

            for month, total in monthly_summary.items():
                print(f"{month}: ₹{total}")


    elif choice == "6":

        if df.empty:
            print("No data to plot")

        else:
            category_data = df.groupby("expense_type")["amount"].sum()

            # BAR GRAPH
            plt.figure()
            category_data.plot(kind="bar")
            plt.title("Expense by Category (Bar Chart)")
            plt.xlabel("Category")
            plt.ylabel("Amount")
            plt.show()

            # PIE CHART
            plt.figure()
            category_data.plot(kind="pie", autopct='%1.1f%%')
            plt.title("Expense Distribution (Pie Chart)")
            plt.ylabel("")  # Removes unnecessary label
            plt.show()

    elif choice == "7":
        print("👋 Exiting... Thank you!")
        break

    else:
        print("Invalid choice")