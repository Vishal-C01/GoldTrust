# GoldTrust - easy version
# Run:  python app.py   then open http://127.0.0.1:5000

import json
import urllib.request
from datetime import datetime
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# All saved receipts are kept here (in memory). Key = receipt number.
receipts = {}

# Free API: today's 24K gold price in Rs per gram (no key needed)
RATE_URL = "https://xaus.com/api/v1/spot?currency=INR&unit=gram&compact=1"


def get_gold_rate():
    """Get today's gold rate from the internet. Returns "" if it fails."""
    try:
        data = json.loads(urllib.request.urlopen(RATE_URL, timeout=6).read())
        return round(float(data["xau"]["price"]), 2)
    except Exception:
        return ""


# ---------- Page 1: the form ----------
FORM_PAGE = """
<h1>GoldTrust</h1>
<p style="color:red">{{ error }}</p>
<form method="post" action="/create">
  Item: <input name="item" value="Gold chain"><br><br>
  Weight (grams): <input name="weight" value="10"><br><br>
  Purity label: <input name="label" value="22K"><br><br>
  Purity % (from testing machine): <input name="purity" value="91.6"><br><br>
  Today's gold rate (Rs/gram): <input name="rate" value="{{ rate }}"><br><br>
  Deduction 1: <input name="reason1" value="Melting charge">
  Rs <input name="amount1" value="500"><br><br>
  Deduction 2: <input name="reason2" value="Stone removal">
  Rs <input name="amount2" value="300"><br><br>
  <input type="checkbox" name="customer_ok"> Customer approves<br>
  <input type="checkbox" name="jeweller_ok"> Jeweller approves<br><br>
  <button>Create QR Receipt</button>
</form>
"""

# ---------- Page 2: the receipt with QR code ----------
RECEIPT_PAGE = """
<h1>GoldTrust Receipt</h1>
<p>Date: {{ r.date }}</p>
<p>Item: {{ r.item }} - {{ r.weight }} g</p>
<p>Purity: {{ r.label }} ({{ r.purity }}%)</p>
<p>Gold rate: Rs {{ r.rate }} per gram</p>
<p>Pure gold value: Rs {{ r.gold_value }}</p>
<p>{{ r.reason1 }}: - Rs {{ r.amount1 }}</p>
<p>{{ r.reason2 }}: - Rs {{ r.amount2 }}</p>
<h2>FINAL AMOUNT: Rs {{ r.final }}</h2>
<p>Approved by: Customer and Jeweller</p>
<div id="qr"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>new QRCode(document.getElementById("qr"), window.location.href);</script>
<p><a href="/">New transaction</a></p>
"""


@app.route("/")
def home():
    return render_template_string(FORM_PAGE, rate=get_gold_rate(), error="")


@app.route("/create", methods=["POST"])
def create():
    f = request.form

    # Read the numbers from the form
    try:
        weight = float(f["weight"])
        purity = float(f["purity"])
        rate = float(f["rate"])
        amount1 = float(f["amount1"] or 0)
        amount2 = float(f["amount2"] or 0)
    except ValueError:
        return render_template_string(FORM_PAGE, rate=f["rate"], error="Please enter numbers only.")

    # Both people must approve
    if not (f.get("customer_ok") and f.get("jeweller_ok")):
        return render_template_string(FORM_PAGE, rate=rate, error="Both must approve.")

    # The main calculation
    gold_value = round(weight * purity / 100 * rate, 2)
    final = round(gold_value - amount1 - amount2, 2)

    # Save the receipt
    number = str(len(receipts) + 1)
    receipts[number] = {
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "item": f["item"], "weight": weight, "label": f["label"],
        "purity": purity, "rate": rate, "gold_value": gold_value,
        "reason1": f["reason1"], "amount1": amount1,
        "reason2": f["reason2"], "amount2": amount2, "final": final,
    }
    return redirect("/receipt/" + number)


@app.route("/receipt/<number>")
def receipt(number):
    r = receipts.get(number)
    if r is None:
        return "Receipt not found"
    return render_template_string(RECEIPT_PAGE, r=r)


app.run(host="0.0.0.0", port=5000)
