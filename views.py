# finance_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from .models import Transaction

food_items = ['pasta', 'burger', 'sushi', 'supermarket', 'kitchen', 'coles', 'woolworths', 'pizza', "mcdonald's", 'kfc', 'subway', 'dinner']

@csrf_exempt
def process_file(request):
    if request.method == "POST":
        try:
            file = request.FILES["file"]
            transactions = []

            with file.open() as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    date = row[0]
                    try:
                        amount = float(row[1])
                    except ValueError:
                        return JsonResponse({"success": False, "error": f"Invalid amount format in row: {row}"})
                    name = row[2]
                    category = "other"
                    net_profit = "expense" if amount < 0 else "profit"

                    if "counterpunch boxing" in name.lower():
                        category = "fitness"
                    elif any(item in name.lower() for item in food_items):
                        category = "food"
                    elif "ampol" in name.lower():
                        category = "fuel"
                    elif "transfer" in name.lower():
                        category = "transfer"
                    elif "credit" in name.lower():
                        category = "credit"
                    elif "parking" in name.lower():
                        category = "parking"

                    transaction = Transaction(
                        date=date,
                        amount=amount,
                        name=name,
                        category=category,
                        net_profit=net_profit,
                    )
                    transactions.append(transaction)

            Transaction.objects.bulk_create(transactions)

            return JsonResponse({"success": True})

        except FileNotFoundError:
            return JsonResponse({"success": False, "error": "File not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})
