"""Usage example of the nortax package."""

import json

# Import the Tax class from the nortax package
from nortax import Tax

# Create a Tax object
tax = Tax(
    gross_income=25000,
    tax_table="7100",
    income_type="Pension",
    period="2 weeks",
    year=2022,
)

# Print the representation of the Tax object
print()
print(repr(tax))

# Change some attributes of the Tax object
tax.gross_income = 65625
tax.tax_table = "7107"
tax.income_type = "Wage"
tax.period = "Monthly"
tax.year = 2023

# Print the Tax object
print()
print(tax)

# Get specific values from the Tax object
print()
print(f"URL: {tax.url}")
print(f"Tax table: {tax.tax_table}")
print(f"Income type: {tax.income_type}")
print(f"Period: {tax.period}")
print(f"Year: {tax.year}")
print(f"Gross income: {tax.gross_income}")
print(f"Tax deduction: {tax.deduction}")
print(f"Net income: {tax.net_income}")
print(f"Return whole table: {json.dumps(tax.get_whole_table(), indent=4)}")
