# SKBank Fraud Detection Dashboard

English version: [README.md](./README.md)

新光銀行異常交易行為偵測平台（Dash 多頁應用），整合：
- 交易與餘額視覺化
- 產業別分佈
- 風險警示檢視
- AI 模型風險分級結果
- 示警通知 Email 清單管理

## Tech Stack

- Python 3.10+
- Dash 2.x
- Plotly
- Pandas
- Gunicorn（部署）

## 專案結構

```text
.
├── app.py                            # Dash 主入口（use_pages=True）
├── Procfile                          # web: gunicorn app:server
├── requirements.txt
├── Data/
│   ├── CFMASTER.csv
│   ├── CFMASTER_SAR.csv
│   ├── SAMASTER_SAR.csv
│   └── SATXNREC_SAR.csv
├── model_prediction/
│   ├── 20230930.csv
│   └── 20231001.csv
├── pages/
│   ├── home.py
│   ├── transaction.py
│   ├── industry_risk.py
│   ├── risk_alarm.py
│   ├── model_prediction.py
│   └── alert_notification/
│       ├── alert_notification.py
│       └── emails.json
├── images/
└── html/
```

## 安裝與啟動（本機開發）

1. 建立虛擬環境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. 安裝套件

```bash
pip install -r requirements.txt
```

3. 啟動應用

```bash
python3 app.py
```

4. 開啟瀏覽器（預設）

```text
http://127.0.0.1:8050
```

## 部署

`Procfile` 已設定：

```text
web: gunicorn app:server
```

可直接用在支援 Procfile 的平台（例如 Heroku/Render 類型部署流程）。

## 各頁面說明

- `/`：首頁與系統流程介紹
- `/ai_model`：模型成效與風險等級分佈
- `/alert_notification`：示警 Email 清單新增/刪除
- `Transaction Data Dashboard`：交易與餘額圖表（由下拉切換帳號）
- `Industry distribution`：行業別分佈（SAR 與非 SAR）
- `風險警示平台`：特徵旗標 treemap（帳號 + 日期）

## 資料需求

- `Data/` 與 `model_prediction/` 內 CSV 檔為執行必要輸入。
- 若更換資料，需維持欄位名稱一致（程式中直接以欄位名存取）。

## 注意事項

- `pages/alert_notification/emails.json` 為本地狀態檔，會在 UI 操作時被覆寫。
- 頁面中部分下拉選單使用固定預設值；若資料集中無該值，圖表初始可能為空。
- 生產環境建議關閉 debug（目前 `app.py` 以 `app.run(debug=True)` 啟動）。

## 快速檢查

可用以下指令做基本語法檢查：

```bash
python3 -m compileall -q app.py pages
```
