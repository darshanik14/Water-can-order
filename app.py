from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

# UPI Details
UPI_ID = "darshanikdhanasekeran@okaxis"
PAYEE_NAME = "Darshanik.T.D"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    quantity = int(request.form['quantity'])
    payment_option = request.form['payment']
    
    if payment_option == "UPI":
        return render_template(
            "upi_payement.html",
            upi_id=UPI_ID,
            payee_name=PAYEE_NAME,
            amount= quantity * 30  # Example: price per water can = ₹20
        )
    else:
        return f"Order received! Name: {name}, Address: {address}, Quantity: {quantity}, Payment: {payment_option}"

@app.route('/generate_qr/<amount>')
def generate_qr(amount):
    upi_link = f"upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am={amount}&cu=INR"
    qr = qrcode.make(upi_link)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
