import time
import os
import pandas as pd
import requests
import urllib.parse
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# ==========================================
# 環境変数の読み込みと設定
# ==========================================
# .envファイルをロード
load_dotenv()

# 環境切替フラグの取得 (文字列判定)
use_live = os.getenv("USE_LIVE_OR_SIM", "FALSE").upper() == "TRUE"

# 環境に応じた変数のマッピング
if use_live:
    AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT_LIVE")
    # TOKEN_ENDPOINTはImplicit Flowでは直接使用しませんが、構成として読み込んでおきます
    TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT_LIVE")
    API_BASE_URL = os.getenv("API_BASE_LIVE") # 例: .../openapi
    REDIRECT_URI = os.getenv("REDIRECT_URI_LIVE")
    APP_KEY = os.getenv("APP_KEY_LIVE")
    # Implicit Flow(SeleniumでのURL取得)ではSecretは不要ですが、取得しておきます
    APP_SECRET = os.getenv("APP_SECRETS_1_LIVE")
    ENV_NAME = "LIVE"
else:
    AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT_SIM")
    TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT_SIM")
    API_BASE_URL = os.getenv("API_BASE_SIM")
    REDIRECT_URI = os.getenv("REDIRECT_URI_SIM")
    APP_KEY = os.getenv("APP_KEY_SIM")
    APP_SECRET = os.getenv("APP_SECRETS_1_SIM")
    ENV_NAME = "SIMULATION"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CSV_FILE_PATH = "Stock_Trade_v2.csv"

# ==========================================
# Discord通知機能
# ==========================================
def send_discord(message):
    """Discordにメッセージを送信する"""
    if not DISCORD_WEBHOOK_URL:
        return

    print(f"[Discord送信]: {message}")
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Discord通知エラー: {e}")

# ==========================================
# 認証処理 (Edgeブラウザ使用)
# ==========================================
def get_access_token():
    msg = f"🚀 **処理開始**\n環境: {ENV_NAME}\nブラウザで認証を開始します..."
    send_discord(msg)
    
    # Edge WebDriverの起動
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)

    # 認証用URL作成 (Implicit Flow)
    params = {
        "response_type": "token", 
        "client_id": APP_KEY,
        "redirect_uri": REDIRECT_URL,
        "state": "init_trade"
    }
    url = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    
    driver.get(url)
    print("★ブラウザでログインを完了させてください...")
    
    access_token = None
    try:
        while True:
            current_url = driver.current_url
            # 設定されたリダイレクトURIと一致するか確認
            if current_url.startswith(REDIRECT_URL):
                parsed = urllib.parse.urlparse(current_url)
                fragment = urllib.parse.parse_qs(parsed.fragment)
                if 'access_token' in fragment:
                    access_token = fragment['access_token'][0]
                    print("認証成功: トークンを取得しました。")
                    send_discord("✅ **認証成功**: トークンを取得しました。")
                    break
            time.sleep(1)
    except Exception as e:
        err_msg = f"❌ **認証エラー**: {e}"
        print(err_msg)
        send_discord(err_msg)
    finally:
        driver.quit()
        
    return access_token

# ==========================================
# API操作クラス
# ==========================================
class SaxoTrader:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        # 末尾のスラッシュ処理などを安全にする
        self.base_url = API_BASE_URL.rstrip('/')

    def search_instrument(self, type_flag, symbol, expiry=None, strike=None, option_type=None):
        endpoint = "/ref/v1/instruments/"
        
        if type_flag == "Option":
            keywords = f"{symbol} {expiry} {strike} {option_type}"
            asset_types = "StockOption"
        else:
            keywords = symbol
            asset_types = "Stock,Etf"

        params = {
            "Keywords": keywords,
            "AssetTypes": asset_types,
            "IncludeNonTradable": False
        }
        
        try:
            # .envのAPI_BASEには /openapi などが含まれるため、エンドポイントを結合
            full_url = self.base_url + endpoint
            
            response = self.session.get(full_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['Data'] and len(data['Data']) > 0:
                instrument = data['Data'][0]
                return instrument['Identifier'], instrument['AssetType'], instrument['Description']
            else:
                print(f"銘柄見つからず: {keywords}")
                return None, None, None
        except Exception as e:
            print(f"検索例外: {e}")
            return None, None, None

    def place_market_order(self, uic, asset_type, action, quantity, description):
        buy_sell = "Buy" if action.lower() == "buy" else "Sell"
        endpoint = "/trade/v2/orders"
        
        payload = {
            "Uic": uic,
            "AssetType": asset_type,
            "BuySell": buy_sell,
            "Amount": quantity,
            "OrderType": "Market",
            "OrderDuration": {"DurationType": "DayOrder"}
        }
        
        try:
            full_url = self.base_url + endpoint
            response = self.session.post(full_url, json=payload)
            
            if response.status_code in [200, 201]:
                res_json = response.json()
                order_id = res_json.get('OrderId', 'Unknown')
                msg = f"📈 **注文成功**\nID: `{order_id}`\n銘柄: {description}\n売買: {buy_sell} {quantity}"
                print(msg)
                send_discord(msg)
                return True
            else:
                err_msg = f"⚠️ **注文失敗**\n銘柄: {description}\nCode: {response.status_code}\n詳細: {response.text}"
                print(err_msg)
                send_discord(err_msg)
                return False
        except Exception as e:
            err_msg = f"❌ **注文例外**: {e}"
            print(err_msg)
            send_discord(err_msg)
            return False

# ==========================================
# メイン処理
# ==========================================
def main():
    token = get_access_token()
    if not token:
        return

    trader = SaxoTrader(token)

    try:
        df = pd.read_csv(CSV_FILE_PATH).fillna("")
        print(f"{len(df)} 件のデータを読み込みました。")
    except FileNotFoundError:
        err_msg = f"❌ **エラー**: CSVファイル({CSV_FILE_PATH})が見つかりません。"
        print(err_msg)
        send_discord(err_msg)
        return

    for index, row in df.iterrows():
        type_flag = str(row['Type']).strip()
        symbol = str(row['Symbol']).strip()
        action = str(row['Action']).strip()
        quantity = int(row['Quantity'])
        expiry = str(row['Expiry']).strip()
        strike = str(row['Strike']).strip()
        option_type = str(row['OptionType']).strip()

        print(f"\n--- レコード {index + 1} ---")
        
        # 銘柄検索
        uic, asset_type, description = trader.search_instrument(
            type_flag, symbol, expiry, strike, option_type
        )
        
        if uic:
            # 注文実行
            trader.place_market_order(uic, asset_type, action, quantity, description)
        else:
            send_discord(f"⏩ **スキップ**: 銘柄が見つかりませんでした ({symbol})")
        
        time.sleep(1)

    send_discord("🏁 **処理完了**: すべての行の処理が終了しました。")

if __name__ == "__main__":
    main()
