from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Currency Converter</title>
<style>body { font-family: Arial; max-width: 600px; margin: 20px auto; }</style>
</head>
<body>
    <h1>Currency Converter</h1>
    <form method="POST">
        <input type="number" name="amount" step="0.01" placeholder="Amount" min="0" required>
        <select name="from_currency">
            <option value="GBP">GBP</option>
            <option value="USD">USD</option>
            <option value="CAD">CAD</option>
        </select>
        to
        <select name="to_currency">
            <option value="GBP">GBP</option>
            <option value="USD">USD</option>
            <option value="CAD">CAD</option>
        </select>
        <input type="submit" value="Convert">
    </form>
    {% if result %}
        <div><h3>Result:</h3><p>{{ amount }} {{ from_currency }} = {{ result }} {{ to_currency }}</p></div>
    {% endif %}
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
</body>
</html>
"""

def get_live_rates(base_currency):
    url = f"https://open.exchangerate-api.com/v6/latest?base={base_currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'] if response.status_code == 200 and data.get('result') == 'success' else None

@app.route('/', methods=['GET', 'POST'])
def converter():
    result = None
    error = None
    amount = None
    from_currency = None
    to_currency = None
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            if amount < 0:
                raise ValueError("Amount cannot be negative")
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')
            if from_currency not in ['GBP', 'USD', 'CAD'] or to_currency not in ['GBP', 'USD', 'CAD']:
                raise ValueError("Invalid currency")
            rates = get_live_rates(from_currency)
            if rates and to_currency in rates:
                result = round(amount * rates[to_currency], 2)
            else:
                error = "Failed to fetch exchange rates"
        except ValueError as e:
            error = str(e)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, amount=amount, 
                                 from_currency=from_currency, to_currency=to_currency)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)