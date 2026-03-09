# 新光銀行異常交易行為偵測平台

Digital Finance Sentinel

## 專案一句話

以 AI 即時辨識異常交易，搭配風險視覺化儀表板與示警通知機制，縮短銀行查核與處置時間。

## 背景痛點

- 既有 AML 流程警示延遲，無法即時應對
- 警示後仍需人工多系統比對，耗時且仰賴經驗
- 缺乏整合式視覺化介面，不利快速判讀

## 解決方案

本平台整合「模型辨識 + 資料儀表板 + 通知機制」三層能力：

1. AI 模型判讀  
   針對台幣與外幣帳戶異常交易建立模型，輸出帳戶風險機率。

2. 風險可視化  
   將交易、餘額、行業分佈、風險旗標集中在同一平台，支援快速篩選與追查。

3. 示警通知  
   異常帳戶可透過 Email 清單通知相關查調同仁，加速作業流程。

## 平台核心頁面

- `Home`：場景、痛點、架構與流程
- `AI Model`：模型成效與風險等級分佈（高/中/低）
- `Transaction Dashboard`：帳戶交易與餘額變化
- `Industry Distribution`：SAR 與非 SAR 行業別比較
- `Risk Alarm`：帳戶旗標警示 treemap
- `Alert Notification`：示警 Email 清單管理

## 已呈現的模型成效（Repo 內展示值）

- 台幣模型：Accuracy 95.63%、Recall 71.03%、Precision 60.06%
- 外幣模型：Accuracy 99.88%、Recall 94.38%、Precision 100.00%

註：以上為目前程式頁面中的展示數值，實際成效應以正式訓練報告與最新驗證資料為準。

## 預期效益

- 縮短異常交易辨識與示警時間
- 降低人工查核負擔，提升查調效率
- 提升風險案件可見度與管理一致性
- 強化客戶資產保護與內控品質

## 快速 Demo（本機）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

瀏覽：`http://127.0.0.1:8050`

## 專案定位

這是一個可展示「金融風險偵測端到端流程」的整合原型，適合：
- 競賽/評審 Demo
- PoC（Proof of Concept）驗證
- 內部跨單位溝通與需求對齊
