import dash
import base64
from dash import html
def encode_image(image_filename):
    encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('utf-8')
    return encoded_image
fraud_detection_flow_filename = './images/system.png'
system_design_filename = './images/system_design.png'
dash.register_page(__name__, path='/', name='Home', description='Home page')

layout = html.Div([
    html.H1('Home'),
    html.Br(),
    html.Div('隨著科技的進步，金融交易方式不斷地革新，帶來了許多的安全問題。異常交易行為偵測平台在此背景下應運而生，確保金融交易的安全性和真實性，並有效地防範潛在的不正常或欺詐行為。'),
    html.Br(),
    html.H2('現行痛點'),
    html.Div('現行 AML 系統未能即時判定異常交易行為，導致警示不即時，報表更待隔天才取得。系統判別異常交易行為後，仍需人為核對客戶基本資料，以專家經驗辨認客戶行為合理性，依照多維度資料綜合判斷，此是困難且耗時耗人力的。而識別異常交易行為後，警示未能自動化通知交易對象與帳戶持有者。'),
    html.Br(),
    html.Ul([html.Li("延遲的警示機制"),
             html.Li("人工審核的困境"),
             html.Li("缺乏直觀的操作界面")]),
    html.Br(),
    html.H2('設計概念'),
    html.Div('結合資料處理的技術與金融領域的知識，利用特徵工程從數據中提取有意義的信息。再透過 Xgboost 的機器學習模型，創建一個即時、精準的異常交易 AI 模型。此模型能夠連接到新光銀行的金流異常偵測平台，從而實現即時的自動警示，並推送給相關人員，確保警示到交易對象和帳戶持有者。此外，風險警示儀表板將提供一個直觀的界面，使管理者能輕鬆查看和管理異常交易偵測的結果。'),
    html.Br(),
    html.Img(src='data:image/png;base64,{}'.format(encode_image(system_design_filename)), style={'width': '50%', 'height': 'auto'}, alt='Fraud Detection Flow'),
    html.Br(),
    html.Br(),
    html.H2('系統流程架構'),
    html.Div('利用機器學習模型 Xgboost 建立即時精準識別異常交易 AI 模型，模型判讀結果串接至新光銀行異常交易行為偵測平台，落實即時自動化示警並推播給相關同仁，以達到示警交易對象與帳戶持有者，並透過風險警示儀表板提供一個直觀的操作界面，讓管理者可以方便地查看和管理異常交易偵測結果。'),
    html.Br(),
    html.Img(src='data:image/png;base64,{}'.format(encode_image(fraud_detection_flow_filename)), style={'width': '80%', 'height': 'auto'}, alt='Fraud Detection Flow'),
    html.Br(),
    html.Div('金流異常偵測平台不只是金融機構的需要，更是維護金融市場公信力和保護消費者權益的關鍵工具。隨著技術的進步和創新，結合領域知識的特徵工程和即時警示機制，這類系統將更加智慧、高效，為金融世界帶來更多的安全與信任。')
]) 
# with open('html/home.html', 'r') as file:
#     custom_layout = file.read()
# layout = custom_layout