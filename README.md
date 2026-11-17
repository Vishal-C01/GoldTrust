GoldTrust

Verify • Calculate • Trust

Team: Hactivators

GoldTrust is a simple web app that makes old-gold exchange clear and fair for both the customer and the jeweller.

The Problem

When a customer sells old jewellery to a small shop, they often cannot check the purity or understand the deductions. There is no shared record that both sides can see and keep. This causes doubt and disputes.

Our Solution

GoldTrust turns a gold exchange into a clear, itemised record:

1.Enter the item, weight and purity reading from the testing machine
2.Today's gold rate is fetched automatically (the jeweller can edit it)
3.Add each deduction with its reason
4.Customer and jeweller both approve
5.A receipt with a QR code is created. Scanning the QR code opens the full itemised receipt

Example

10 g gold chain, 22K (91.6%), rate Rs 7,000 per gram (sample)

• Pure gold value = Rs 64,120
• Melting charge = - Rs 500
• Stone removal = - Rs 300
• Final amount = Rs 63,320

Features

• Live gold rate for the day (editable)
• Gold value calculator (weight x purity x rate)
• Itemised deductions with reasons
• Customer and jeweller approval before a receipt is made
• QR code receipt with date and time

Tech Used

• Python (Flask)
• HTML
• QR code (JavaScript library)
• Free gold price API (xaus.com)

How to Run

1. Install Python
2. Download or clone this repository
3. Open a terminal in the project folder
4. Install Flask: pip install -r requirements.txt
5. Start the app: python app.py
6. Open http://127.0.0.1:5000 in your browser

Internet is needed for the live gold rate and the QR code. If the rate cannot be fetched, type it by hand.

Important Notes

• Purity is entered manually from a testing machine or hallmark. GoldTrust does not detect purity by itself.
• The live rate is the international gold price converted to rupees. Local shop rates can be slightly different, so the jeweller can edit the rate.
• In this prototype, receipts are saved in memory and clear when the app is stopped.

Future Plans

• Save receipts permanently in a database
• Read weight and purity directly from the scale and testing machine
• Keep a full history of every receipt and rate
• Support local languages

Team Hactivators

 N.Rajitha - Team Leader
 Vishal.C
 V Lasya Reddy
 Sneha S J 


