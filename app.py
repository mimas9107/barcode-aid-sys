from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Excel 檔案路徑（你自行調整）
EXCEL_FILE = "inventory.xlsx"

def load_data():
    """讀取 Excel，回傳 pandas DataFrame"""
    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame()
    df = pd.read_excel(EXCEL_FILE)
    return df

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route("/api/query", methods=["GET"])
def query():
    code = request.args.get("code", "").strip()

    if not code:
        return jsonify({"status": "error", "msg": "缺少 code"}), 400

    df = load_data()
    ## 所在位置	貨品編號	貨品名稱	貨品基本單位	庫存量

    # 假設 Excel 裡欄位名稱為：Barcode, ProductName, Qty, Location, Usage
    row = df[df["貨品編號"] == code]

    if row.empty:
        return jsonify({"status": "not_found", "msg": "查無此條碼"}), 404

    data = row.iloc[0].to_dict()

    return jsonify({
        "status": "ok",
        "barcode": code,
        "product_name": data.get("貨品名稱", ""),
        "qty": data.get("庫存量", ""),
        "location": data.get("所在位置", ""),
        "usage": data.get("Usage", "")
    })

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5002, debug=True)
    app.run(host="0.0.0.0", port=5002, ssl_context=('cert.pem', 'key.pem'))
