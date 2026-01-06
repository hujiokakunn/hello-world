# saxoバンクのOpenAPIを利用したFX取引（センバツ対応バージョン）
# 04：アクセストークンのリフレッシュとWebsocketの再認可を追加
import asyncio
import base64
import csv
import collections
import hashlib
import json
import math
import os
import platform
import random
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, time as dt_time
from decimal import Decimal, ROUND_HALF_UP
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional, Tuple

import requests
import websockets
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ============================================================
# 設定読み込み (.env)
# ============================================================

load_dotenv()


def _get_env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.getenv(name)
    if value is None or value == "":
        if required and default is None:
            raise RuntimeError(f"環境変数 {name} が設定されていません。")
        return default
    return value


def _get_env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip().lower()
    if raw in ("1", "true", "yes", "on", "t", "y"):
        return True
    if raw in ("0", "false", "no", "off", "f", "n"):
        return False
    return default


def _get_env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _parse_hhmmss(value: str) -> dt_time:
    parts = value.strip().split(":")
    if len(parts) == 2:
        hour, minute = map(int, parts)
        return dt_time(hour=hour, minute=minute, second=0)
    if len(parts) == 3:
        hour, minute, second = map(int, parts)
        return dt_time(hour=hour, minute=minute, second=second)
    raise RuntimeError(f"無効な時刻形式: {value} (HH:MM または HH:MM:SS 形式で指定してください)")


@dataclass
class EnvConfig:
    use_live: bool
    client_id: str
    client_secret: str
    auth_endpoint: str
    token_endpoint: str
    api_base: str
    redirect_uri: str
    streaming_ws_base: str
    saxo_username: str
    saxo_password: str
    discord_webhook_url: Optional[str]
    trades_csv_path: str
    stop_loss_pips: float
    take_profit_pips: float
    spread_pips_limit: float
    entry_retry_count: int
    entry_retry_interval: int
    exit_retry_count: int
    exit_retry_interval: int
    random_delay_sec: int
    spread_retry_count: int
    spread_retry_interval: int
    fill_timeout_seconds: int
    oauth_flow: str
    oauth_callback_timeout_seconds: int
    ws_ping_interval: int
    ws_ping_timeout: int
    ws_close_timeout: int
    ens_stale_seconds: int
    ens_monitor_interval_seconds: int
    ens_notify_thresholds: List[int]
    ens_reconnect_max_delay_seconds: int
    token_refresh_interval_seconds: int
    streaming_authorize_enabled: bool
    streaming_authorize_path: str
    streaming_authorize_param: str


def load_config() -> EnvConfig:
    use_live = _get_env_bool("USE_LIVE_OR_SIM", False)

    if use_live:
        client_id = _get_env("APP_KEY_LIVE") or _get_env("SAXO_CLIENT_ID_LIVE") or ""
        client_secret = _get_env("APP_SECRETS_1_LIVE") or _get_env("SAXO_CLIENT_SECRET_LIVE") or ""
        auth_endpoint = _get_env("AUTH_ENDPOINT_LIVE") or "https://live.logonvalidation.net/authorize"
        token_endpoint = _get_env("TOKEN_ENDPOINT_LIVE") or "https://live.logonvalidation.net/token"
        api_base = _get_env("API_BASE_LIVE") or "https://gateway.saxobank.com/openapi"
        redirect_uri = _get_env("REDIRECT_URI_LIVE") or "http://localhost:2983/saxo_live"
        streaming_ws_base = _get_env("STREAMING_WS_BASE_LIVE") or "wss://live-streaming.saxobank.com/oapi/streaming/ws"
        saxo_username = _get_env("SAXO_USERNAME_LIVE") or _get_env("SAXO_USERNAME") or ""
        saxo_password = _get_env("SAXO_PASSWORD_LIVE") or _get_env("SAXO_PASSWORD") or ""
    else:
        client_id = _get_env("APP_KEY_SIM") or _get_env("SAXO_CLIENT_ID_SIM") or ""
        client_secret = _get_env("APP_SECRETS_1_SIM") or _get_env("SAXO_CLIENT_SECRET_SIM") or ""
        auth_endpoint = _get_env("AUTH_ENDPOINT_SIM") or "https://sim.logonvalidation.net/authorize"
        token_endpoint = _get_env("TOKEN_ENDPOINT_SIM") or "https://sim.logonvalidation.net/token"
        api_base = _get_env("API_BASE_SIM") or "https://gateway.saxobank.com/sim/openapi"
        redirect_uri = _get_env("REDIRECT_URI_SIM") or "http://localhost:8083/saxo_sim"
        streaming_ws_base = _get_env("STREAMING_WS_BASE_SIM") or "wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws"
        saxo_username = _get_env("SAXO_USERNAME_SIM") or _get_env("SAXO_USERNAME") or ""
        saxo_password = _get_env("SAXO_PASSWORD_SIM") or _get_env("SAXO_PASSWORD") or ""

    discord_webhook_url = _get_env("DISCORD_WEBHOOK_URL") or _get_env("DISCORD_WEBHOOK_SAXO")

    # 誤設定の予防
    def _assert_env_match(value: str, expect_live: bool, label: str) -> None:
        lower = value.lower()
        if expect_live and "sim" in lower:
            raise RuntimeError(f"USE_LIVE_OR_SIM=TRUE なのに {label} がSIMっぽいです: {value}")
        if (not expect_live) and "live" in lower:
            raise RuntimeError(f"USE_LIVE_OR_SIM=FALSE なのに {label} がLIVEっぽいです: {value}")

    if use_live and "/sim/" in api_base:
        raise RuntimeError(f"USE_LIVE_OR_SIM=TRUE なのに API_BASE_URL がSIMです: {api_base}")
    if (not use_live) and ("/openapi" in api_base and "/sim/" not in api_base) and (
        "gateway.saxobank.com/sim/openapi" not in api_base
    ):
        raise RuntimeError(f"USE_LIVE_OR_SIM=FALSE なのに API_BASE_URL がLIVEっぽいです: {api_base}")

    _assert_env_match(auth_endpoint, use_live, "AUTH_ENDPOINT")
    _assert_env_match(token_endpoint, use_live, "TOKEN_ENDPOINT")
    _assert_env_match(streaming_ws_base, use_live, "STREAMING_WS_BASE")
    _assert_env_match(redirect_uri, use_live, "REDIRECT_URI")

    notify_thresholds = _get_env("ENS_NOTIFY_THRESHOLDS", "10,60,180")
    thresholds = []
    for raw in notify_thresholds.split(","):
        raw = raw.strip()
        if not raw:
            continue
        try:
            thresholds.append(int(raw))
        except ValueError:
            continue
    thresholds = sorted(set(thresholds)) or [10, 60, 180]

    return EnvConfig(
        use_live=use_live,
        client_id=client_id,
        client_secret=client_secret,
        auth_endpoint=auth_endpoint,
        token_endpoint=token_endpoint,
        api_base=api_base,
        redirect_uri=redirect_uri,
        streaming_ws_base=streaming_ws_base,
        saxo_username=saxo_username,
        saxo_password=saxo_password,
        discord_webhook_url=discord_webhook_url,
        trades_csv_path=_get_env("SAXO_TRADES_CSV", "saxo_trades.csv") or "saxo_trades.csv",
        stop_loss_pips=_get_env_float("SAXO_STOP_LOSS_PIPS", 1.0),  # ストップロス値
        take_profit_pips=_get_env_float("SAXO_TAKE_PROFIT_PIPS", 4000.0),  # テイクプロフィット値
        spread_pips_limit=_get_env_float("SAXO_SPREAD_PIPS_LIMIT", 3.5),  # スプレッド許容値
        entry_retry_count=_get_env_int("SAXO_ENTRY_RETRY_COUNT", 0),
        entry_retry_interval=_get_env_int("SAXO_ENTRY_RETRY_INTERVAL", 10),
        exit_retry_count=_get_env_int("SAXO_EXIT_RETRY_COUNT", 3),
        exit_retry_interval=_get_env_int("SAXO_EXIT_RETRY_INTERVAL", 10),
        random_delay_sec=_get_env_int("SAXO_RANDOM_DELAY_SEC", 3),
        spread_retry_count=_get_env_int("SAXO_SPREAD_RETRY_COUNT", 0),
        spread_retry_interval=_get_env_int("SAXO_SPREAD_RETRY_INTERVAL", 2),
        fill_timeout_seconds=_get_env_int("SAXO_FILL_TIMEOUT_SECONDS", 180),
        oauth_flow=(_get_env("SAXO_OAUTH_FLOW", "selenium") or "selenium").lower(),
        oauth_callback_timeout_seconds=_get_env_int("SAXO_OAUTH_CALLBACK_TIMEOUT", 300),
        ws_ping_interval=_get_env_int("SAXO_WS_PING_INTERVAL", 15),
        ws_ping_timeout=_get_env_int("SAXO_WS_PING_TIMEOUT", 5),
        ws_close_timeout=_get_env_int("SAXO_WS_CLOSE_TIMEOUT", 5),
        ens_stale_seconds=_get_env_int("SAXO_ENS_STALE_SECONDS", 45),
        ens_monitor_interval_seconds=_get_env_int("SAXO_ENS_MONITOR_INTERVAL_SECONDS", 10),
        ens_notify_thresholds=thresholds,
        ens_reconnect_max_delay_seconds=_get_env_int("SAXO_ENS_RECONNECT_MAX_DELAY", 30),
        token_refresh_interval_seconds=_get_env_int("SAXO_TOKEN_REFRESH_INTERVAL_SECONDS", 18 * 60),
        streaming_authorize_enabled=_get_env_bool("SAXO_STREAMING_AUTHORIZE_ENABLED", True),
        streaming_authorize_path=_get_env("SAXO_STREAMING_AUTHORIZE_PATH", "/streamingws/authorize")
        or "/streamingws/authorize",
        streaming_authorize_param=_get_env("SAXO_STREAMING_AUTHORIZE_PARAM", "contextId") or "contextId",
    )


CFG = load_config()

# 定数
TIMEZONE_TOKYO = timezone(timedelta(hours=9))
CODE_VERIFIER = secrets.token_urlsafe(32)
CODE_CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(CODE_VERIFIER.encode()).digest()).decode().rstrip("=")
MAJOR_PAIRS = [
    "USD/JPY",
    "EUR/USD",
    "EUR/JPY",
    "GBP/JPY",
    "AUD/JPY",
    "AUD/USD",
    "NZD/JPY",
    "CHF/JPY",
    "EUR/GBP",
    "GBP/USD",
    "USD/CHF",
    "USD/CAD",
    "NZD/USD",
    "CAD/JPY",
    "EUR/CHF",
]
EDGE_USER_DATA_DIR = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    auth_code: Optional[str] = None
    error: Optional[str] = None
    expected_state: Optional[str] = None
    expected_path: str = "/"
    done_event = threading.Event()

    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != OAuthCallbackHandler.expected_path:
            self.send_response(404)
            self.end_headers()
            return

        qs = urllib.parse.parse_qs(parsed.query)

        if "error" in qs:
            OAuthCallbackHandler.error = qs["error"][0]
        else:
            state = qs.get("state", [None])[0]
            if OAuthCallbackHandler.expected_state and state != OAuthCallbackHandler.expected_state:
                OAuthCallbackHandler.error = "state_mismatch"
                OAuthCallbackHandler.done_event.set()
                self.send_response(400)
                self.end_headers()
                return
            OAuthCallbackHandler.auth_code = qs.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        body = "<html><body>認証が完了しました。このウィンドウを閉じてください。</body></html>"
        self.wfile.write(body.encode())

        OAuthCallbackHandler.done_event.set()


def start_local_http_server(redirect_uri: str) -> Tuple[HTTPServer, threading.Thread]:
    parsed = urllib.parse.urlparse(redirect_uri)

    host = parsed.hostname or "localhost"
    port = parsed.port or 80
    path = parsed.path or "/"

    if host not in ("localhost", "127.0.0.1"):
        raise RuntimeError(f"redirect_uri の host は localhost/127.0.0.1 のみ許可します: {host}")

    OAuthCallbackHandler.auth_code = None
    OAuthCallbackHandler.error = None
    OAuthCallbackHandler.expected_path = path
    OAuthCallbackHandler.expected_state = None
    OAuthCallbackHandler.done_event.clear()

    httpd = HTTPServer((host, port), OAuthCallbackHandler)

    def _serve_until_done():
        httpd.timeout = 1
        try:
            while not OAuthCallbackHandler.done_event.is_set():
                httpd.handle_request()
        finally:
            httpd.server_close()

    thread = threading.Thread(target=_serve_until_done, daemon=True)
    thread.start()
    return httpd, thread

def get_jst_time_str() -> str:
    return datetime.now(TIMEZONE_TOKYO).strftime("%Y-%m-%d %H:%M:%S")


def _get_log_filename(now: Optional[datetime] = None) -> str:
    if now is None:
        now = datetime.now(TIMEZONE_TOKYO)
    date_str = now.strftime("%Y%m%d")
    weekday_map = {
        0: "mon",
        1: "tue",
        2: "wed",
        3: "thu",
        4: "fri",
        5: "fri",
        6: "fri",
    }
    weekday = weekday_map.get(now.weekday(), "fri")
    return f"saxo_fx_log_{date_str}_{weekday}.log"


def _cleanup_old_logs(log_dir: str, keep_days: int = 7) -> None:
    try:
        cutoff_date = datetime.now(TIMEZONE_TOKYO).date() - timedelta(days=keep_days - 1)
        for filename in os.listdir(log_dir):
            if not filename.startswith("saxo_fx_log_") or not filename.endswith(".log"):
                continue
            parts = filename.split("_")
            if len(parts) < 4:
                continue
            date_part = parts[3]
            try:
                file_date = datetime.strptime(date_part, "%Y%m%d").date()
            except ValueError:
                continue
            if file_date < cutoff_date:
                os.remove(os.path.join(log_dir, filename))
    except Exception as e:
        print(f"[{get_jst_time_str()}] ログファイルの整理に失敗しました: {e}")


def extract_hms_jst(ts: Optional[str]) -> str:
    if not ts:
        return "N/A"
    s = str(ts).strip()
    if not s:
        return "N/A"
    if " " in s:
        parts = s.split()
        return parts[1] if len(parts) >= 2 else parts[0]
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.astimezone(TIMEZONE_TOKYO).strftime("%H:%M:%S")
    except Exception:
        return s

def log(message: str) -> None:
    timestamp = get_jst_time_str()
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        log_dir = os.getcwd()
        log_filename = _get_log_filename()
        log_path = os.path.join(log_dir, log_filename)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        _cleanup_old_logs(log_dir)
    except Exception as e:
        print(f"[{timestamp}] ログファイル出力に失敗しました: {e}")

def _mask(s: str, keep: int = 4) -> str:
    if not s:
        return ""
    s = str(s)
    if len(s) <= keep:
        return "*" * len(s)
    return "*" * (len(s) - keep) + s[-keep:]


def _mask_url_query(url: str, keys: Tuple[str, ...] = ("code", "state")) -> str:
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    for key in keys:
        if key in qs:
            qs[key] = ["***"]
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(qs, doseq=True)))


def send_discord(message: str) -> bool:
    if not CFG.discord_webhook_url:
        log("Discord Webhook URLが設定されていません。通知をスキップします。")
        return False
    try:
        payload = {"content": message}
        response = requests.post(CFG.discord_webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        log(f"Discord通知を送信しました。ステータス: {response.status_code}")
        return response.status_code in [200, 204]
    except requests.exceptions.RequestException as e:
        log(f"Discord通知エラー: {str(e)}")
        return False
    except Exception as e:
        log(f"Discord通知中に予期せぬエラーが発生しました: {str(e)}")
        return False


def cleanup_edge_user_data_dir():
    global EDGE_USER_DATA_DIR
    if EDGE_USER_DATA_DIR and os.path.exists(EDGE_USER_DATA_DIR):
        try:
            shutil.rmtree(EDGE_USER_DATA_DIR)
            log(f"一時ディレクトリ {EDGE_USER_DATA_DIR} を削除しました。")
        except Exception as e:
            log(f"一時ディレクトリ削除エラー: {e}")
    EDGE_USER_DATA_DIR = None


def create_edge_driver() -> Optional[Tuple[webdriver.Edge, str]]:
    global EDGE_USER_DATA_DIR
    try:
        timestamp = int(time.time())
        unique_id = secrets.token_hex(4)
        base_selenium_path = "C:\\fx\\saxo"
        if not os.path.exists(base_selenium_path):
            os.makedirs(base_selenium_path, exist_ok=True)

        temp_dir = os.path.join(base_selenium_path, f"edge_user_data_{timestamp}_{unique_id}")
        EDGE_USER_DATA_DIR = temp_dir

        options = EdgeOptions()
        options.add_argument(f"--user-data-dir={temp_dir}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        try:
            service = EdgeService(executable_path=r"C:\\fx\\saxo\\msedgedriver.exe")
            driver = webdriver.Edge(service=service, options=options)
        except Exception as e_path:
            log(
                "指定されたパス C:\\fx\\saxo\\msedgedriver.exe でのEdgeDriver起動に失敗: "
                f"{e_path}。デフォルトパスを試します。"
            )
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=options)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        log("Edge WebDriverが正常に作成されました。")
        return driver, temp_dir
    except Exception as e:
        log(f"Edgeドライバーの作成に失敗: {e}")
        cleanup_edge_user_data_dir()
        return None, None


def kill_existing_edge_drivers():
    log("既存のEdgeおよびmsedgedriverプロセスの強制終了を試みています...")
    if platform.system() == "Windows":
        try:
            subprocess.call(
                "taskkill /f /im msedgedriver.exe",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.call(
                "taskkill /f /im msedge.exe",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log("プロセス強制終了コマンドを実行しました。")
        except Exception as e:
            log(f"タスクキル中のエラー: {e}")


class SaxoClient:
    def __init__(self, cfg: EnvConfig):
        self.cfg = cfg
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.account_key: Optional[str] = None
        self.client_key: Optional[str] = None
        self.base_url: str = cfg.api_base
        self.env_name: str = "LIVE" if cfg.use_live else "SIM"
        self.client_id: str = cfg.client_id
        self.client_secret: str = cfg.client_secret
        self.auth_endpoint: str = cfg.auth_endpoint
        self.token_endpoint: str = cfg.token_endpoint
        self.redirect_uri: str = cfg.redirect_uri
        self.streaming_ws_base: str = cfg.streaming_ws_base

        if not self.client_id or not self.client_secret:
            raise RuntimeError("ClientId/Secret が未設定です（APP_KEY_* / APP_SECRETS_1_* を確認）")
        if not self.redirect_uri:
            raise RuntimeError("REDIRECT_URI_* が未設定です")
        self.session = requests.Session()
        self.refresh_lock = threading.Lock()
        self.last_refresh_time: float = 0
        self.pair_uic_cache: Dict[str, Dict] = {}
        self.reauthenticate_callback: Optional[callable] = None
        self.ens_event_queue: Optional[asyncio.Queue] = None
        self._ens_waiters: List[Dict[str, Any]] = []
        self._ens_waiters_lock = asyncio.Lock()
        self._ens_event_backlog: collections.deque = collections.deque(maxlen=100)
        self.streaming_context_id: Optional[str] = None
        self.ens_subscription_id: Optional[str] = None
        self.streaming_authorize_enabled: bool = cfg.streaming_authorize_enabled
        self.related_order_labels: Dict[str, str] = {}
        self.tp_sl_order_ids_by_uic: Dict[int, set] = {}

        log(
            f"[ENV] {self.env_name} selected. API_BASE={self.base_url} AUTH={self.auth_endpoint} "
            f"TOKEN={self.token_endpoint} STREAMING={self.streaming_ws_base} CLIENT_ID={_mask(self.client_id)}"
        )

    def set_reauthenticate_func(self, func: callable):
        self.reauthenticate_callback = func

    def _get_ens_event_queue(self) -> asyncio.Queue:
        if self.ens_event_queue is None:
            self.ens_event_queue = asyncio.Queue()
        return self.ens_event_queue

    @staticmethod
    def _ens_event_matches(waiter: Dict[str, Any], event: Dict[str, Any]) -> bool:
        event_type = event.get("type")
        if not event_type or event_type not in waiter["expected_event_types"]:
            return False

        event_uic = int(event.get("uic")) if event.get("uic") is not None else None
        if event_uic != waiter["uic"]:
            return False

        if event_type in ["order_fill", "order_status_change"]:
            if not waiter["order_id"]:
                return False
            event_order_id = str(event.get("order_id")) if event.get("order_id") is not None else None
            if event_order_id != waiter["order_id"]:
                return False
            if event_type == "order_fill":
                status = str(event.get("status", "")).lower()
                return status in ["filled", "fill", "finalfill"]
            return True

        if event_type == "position_closed":
            return True

        return False

    async def _register_ens_waiter(
        self, order_id: Optional[str], uic: int, expected_event_types: List[str]
    ) -> asyncio.Future:
        future = asyncio.get_running_loop().create_future()
        waiter = {
            "future": future,
            "order_id": order_id,
            "uic": int(uic),
            "expected_event_types": set(expected_event_types),
        }
        async with self._ens_waiters_lock:
            matched_event = None
            for event in list(self._ens_event_backlog):
                if self._ens_event_matches(waiter, event):
                    matched_event = event
                    self._ens_event_backlog.remove(event)
                    break
            if matched_event is not None:
                future.set_result(matched_event)
            else:
                self._ens_waiters.append(waiter)
        return future

    async def _unregister_ens_waiter(self, future: asyncio.Future) -> None:
        async with self._ens_waiters_lock:
            self._ens_waiters = [waiter for waiter in self._ens_waiters if waiter["future"] is not future]

    async def _dispatch_ens_event(self, event: Dict[str, Any]) -> None:
        async with self._ens_waiters_lock:
            matched_waiters = [waiter for waiter in self._ens_waiters if self._ens_event_matches(waiter, event)]
            if not matched_waiters:
                self._ens_event_backlog.append(event)
                return
            for waiter in matched_waiters:
                future = waiter["future"]
                if not future.done():
                    future.set_result(event)
            self._ens_waiters = [waiter for waiter in self._ens_waiters if waiter not in matched_waiters]

    def generate_streaming_context_id(self) -> str:
        timestamp = str(int(time.time() * 1000))[-10:]
        random_part = "".join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(8))
        context_id = f"ctx-{timestamp}-{random_part}"
        self.streaming_context_id = context_id
        log(f"ストリーミング用ContextId生成: {context_id}")
        return context_id

    def _build_streaming_ws_url(self, context_id: str, message_id: Optional[int] = None) -> str:
        if not self.access_token:
            raise RuntimeError("access_token がないためStreaming URLを生成できません")
        auth_q = urllib.parse.quote(f"BEARER {self.access_token}", safe="")
        url = f"{self.streaming_ws_base}/connect?contextId={urllib.parse.quote(context_id, safe='')}&authorization={auth_q}"
        if message_id is not None:
            url = f"{url}&messageid={message_id}"
        return url

    @staticmethod
    def _mask_ws_url_for_log(url: str) -> str:
        return re.sub(r"(authorization=)[^&]+", r"\1***", url)

    def setup_ens_subscription(self) -> Optional[str]:
        log("ENSサブスクリプションを作成中...")
        endpoint = "/ens/v1/activities/subscriptions"

        context_id = self.generate_streaming_context_id()

        subscription_payload = {
            "ContextId": context_id,
            "ReferenceId": f"ENS_OrderPos_{secrets.token_urlsafe(8)}",
            "Arguments": {"Activities": ["Orders", "Positions"], "AccountKey": self.account_key, "ClientKey": self.client_key},
        }

        response = self._make_request("POST", endpoint, json_data=subscription_payload)
        if response is None:
            log("ENSサブスクリプションの作成に失敗しました。")
            return None

        self.ens_subscription_id = response.get("SubscriptionId") if isinstance(response, dict) else None

        websocket_url = self._build_streaming_ws_url(context_id)
        log(f"ENS WebSocket URL: {self._mask_ws_url_for_log(websocket_url)}")
        return websocket_url

    def delete_ens_subscription(self) -> bool:
        if not self.ens_subscription_id:
            return False
        endpoint = f"/ens/v1/activities/subscriptions/{self.ens_subscription_id}"
        response = self._make_request("DELETE", endpoint)
        if response is None:
            log(f"ENSサブスクリプション削除に失敗しました: {self.ens_subscription_id}")
            return False
        log(f"ENSサブスクリプションを削除しました: {self.ens_subscription_id}")
        self.ens_subscription_id = None
        return True

    def rebuild_streaming_url(self, message_id: Optional[int] = None) -> Optional[str]:
        if not self.streaming_context_id:
            return None
        try:
            return self._build_streaming_ws_url(self.streaming_context_id, message_id=message_id)
        except Exception as e:
            log(f"ストリーミングURL再生成に失敗: {e}")
            return None

    def authorize_streaming_context(self) -> bool:
        if not self.streaming_authorize_enabled:
            return False
        if not self.streaming_context_id:
            log("ストリーミングContextIdがありません。再認可をスキップします。")
            return False
        log(f"ストリーミング再認可を実行します: contextId={self.streaming_context_id}")
        endpoint = self.cfg.streaming_authorize_path
        param_key = self.cfg.streaming_authorize_param
        try:
            streaming_base = self.streaming_ws_base
            if streaming_base.endswith("/oapi/streaming/ws"):
                streaming_base = streaming_base[: -len("/oapi/streaming/ws")]
            parsed = urllib.parse.urlparse(streaming_base)
            scheme = "https" if parsed.scheme in ("wss", "https") else "http"
            url = parsed._replace(scheme=scheme).geturl() + endpoint
            headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}
            response = self.session.request(
                "POST",
                url,
                headers=headers,
                params={param_key: self.streaming_context_id},
                timeout=(5, 10),
            )
            if response.status_code == 404:
                log(f"ストリーミング再認可が未対応のため無効化します: {endpoint}")
                self.streaming_authorize_enabled = False
                return False
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            log(f"ストリーミング再認可に失敗しました: {e}")
            return False
        except Exception as e:
            log(f"ストリーミング再認可中に予期せぬエラー: {e}")
            return False
        log("ストリーミング再認可に成功しました。")
        return True

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        retries: int = 3,
        is_price_request: bool = False,
        retry_safe: bool = True,
    ):
        url = f"{self.base_url}{endpoint}"

        if not retry_safe:
            retries = 1

        for attempt in range(retries):
            if self.access_token is None and self.reauthenticate_callback:
                log("アクセストークンがありません。リクエスト前に再認証を試みます。")
                if not self.reauthenticate_callback():
                    log("再認証に失敗しました。リクエストを実行できません。")
                    return None

            headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}
            if method.upper() in ["POST", "PUT", "PATCH"] and json_data is not None:
                headers["Content-Type"] = "application/json"

            try:
                connect_timeout = 5
                read_timeout = 15 + attempt * 5
                if is_price_request:
                    read_timeout = min(read_timeout, 10)

                response = self.session.request(
                    method, url, headers=headers, params=params, json=json_data, timeout=(connect_timeout, read_timeout)
                )

                if response.status_code == 401:
                    log(
                        f"API {endpoint} が401を返しました。トークンリフレッシュを試みます。"
                        f"レスポンス概要: {response.text[:200]}"
                    )
                    if self.refresh_access_token():
                        log("トークンリフレッシュ成功。リクエストを再試行します。")
                        continue
                    if self.reauthenticate_callback and self.reauthenticate_callback():
                        log("完全な再認証成功。リクエストを再試行します。")
                        continue
                    log("認証の回復に失敗しました。")
                    return None

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "10"))
                    log(f"レート制限 (429)。{retry_after}秒待機後に再試行します。")
                    time.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    log(f"サーバーエラー ({response.status_code}): {endpoint} - 試行 {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        time.sleep(2**attempt)
                        continue
                    log(f"サーバーエラーが継続しています: {response.text[:200]}")
                    return None

                if response.status_code == 404:
                    log(f"APIエンドポイントが見つかりません (404): {method} {endpoint}")
                    return None

                if response.status_code == 405:
                    log(f"メソッドが許可されていません (405): {method} {endpoint}")
                    return None

                response.raise_for_status()

                if response.text:
                    try:
                        return response.json()
                    except json.JSONDecodeError as jde:
                        log(f"{endpoint} のJSONデコードに失敗: {jde} - レスポンス: {response.text[:200]}")
                        return None
                return None

            except requests.exceptions.ConnectionError as ce:
                log(f"接続エラー ({endpoint}): {str(ce)} - 試行 {attempt + 1}/{retries}")
                if attempt < retries - 1 and retry_safe:
                    wait_time = 1 + attempt * 2
                    if is_price_request:
                        wait_time = min(wait_time, 3)
                    time.sleep(wait_time)
                    continue
                log(f"{retries}回の再試行後も接続エラー: {endpoint}")
                return None

            except requests.exceptions.Timeout as te:
                log(f"タイムアウト ({endpoint}): {str(te)} - 試行 {attempt + 1}/{retries}")
                if attempt < retries - 1 and retry_safe:
                    time.sleep(1 + attempt)
                    continue
                log(f"{retries}回の再試行後もタイムアウト: {endpoint}")
                return None

            except requests.exceptions.RequestException as e:
                log(f"リクエスト例外 ({endpoint}): {e} - 試行 {attempt + 1}/{retries}")

                if hasattr(e, "response") and e.response is not None:
                    log(f"エラーレスポンス詳細 ({endpoint}): {e.response.text[:300]}")

                if attempt < retries - 1 and retry_safe:
                    time.sleep(2 + attempt)
                    continue
                log(f"{retries}回の再試行後もRequestException: {endpoint}")
                return None

        return None

    def perform_oauth_flow(self) -> bool:
        log("OAuth認証フローを開始します...")

        expected_state = secrets.token_urlsafe(16)
        auth_url_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code_challenge": CODE_CHALLENGE,
            "code_challenge_method": "S256",
            "scope": "openid TradeAccess ReadTrading ReadAccount",
            "state": expected_state,
        }
        auth_url = f"{self.auth_endpoint}?{urllib.parse.urlencode(auth_url_params)}"

        if self.cfg.oauth_flow == "manual":
            log("手動ログインモードでOAuth認証を進めます。")
            _, thread = start_local_http_server(self.redirect_uri)
            OAuthCallbackHandler.expected_state = expected_state
            log(f"認証URLをブラウザで開きます: {auth_url}")
            webbrowser.open(auth_url)
            completed = OAuthCallbackHandler.done_event.wait(timeout=self.cfg.oauth_callback_timeout_seconds)
            if not completed:
                log("OAuthコールバックがタイムアウトしました。")
                return False
            if OAuthCallbackHandler.error:
                log(f"OAuthエラー: {OAuthCallbackHandler.error}")
                return False
            if OAuthCallbackHandler.auth_code:
                return self.exchange_code_for_token(OAuthCallbackHandler.auth_code)
            log("OAuthコードが取得できませんでした。")
            return False

        driver, temp_dir = create_edge_driver()
        if not driver:
            log("OAuthフロー用のEdgeドライバー作成に失敗しました。")
            return False

        auth_code = None
        try:
            log(f"認証URLに移動します: {auth_url}")
            driver.get(auth_url)

            log("ブラウザ経由でログインしてください。必要に応じてSMSコードを待機します (最大5分)。")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "field_userid"))).send_keys(
                self.cfg.saxo_username
            )
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "field_password"))).send_keys(
                self.cfg.saxo_password
            )
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button_login"))).click()

            log(f"ログイン情報を送信しました。リダイレクトを待機中: {self.redirect_uri}")
            WebDriverWait(driver, 300).until(lambda d: self.redirect_uri in d.current_url)

            current_url = driver.current_url
            log(f"リダイレクト先: {_mask_url_query(current_url)}")
            parsed_url = urllib.parse.urlparse(current_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            state = query_params.get("state", [None])[0]
            if state != expected_state:
                log("OAuth state が一致しません。認証を中断します。")
                return False

            if "code" in query_params:
                auth_code = query_params["code"][0]
                log("認証コードを取得しました。")
            else:
                log(f"リダイレクトURLから認証コードの取得に失敗しました。クエリパラメータ: {query_params}")
                error = query_params.get("error", [None])[0]
                error_description = query_params.get("error_description", [None])[0]
                if error:
                    log(f"OAuthエラー: {error} - {error_description}")
                return False
        except Exception as e:
            log(f"OAuthブラウザ操作中のエラー: {e}")
            try:
                screenshot_path = "oauth_error_screenshot.png"
                driver.save_screenshot(screenshot_path)
                log(f"OAuthエラーのスクリーンショットを保存しました: {screenshot_path}")
            except Exception as se:
                log(f"スクリーンショットの保存に失敗: {se}")
            return False
        finally:
            if driver:
                driver.quit()
            if temp_dir:
                cleanup_edge_user_data_dir()

        if auth_code:
            return self.exchange_code_for_token(auth_code)
        return False

    def exchange_code_for_token(self, auth_code: str) -> bool:
        log("認証コードをトークンに交換しています...")
        token_url = self.token_endpoint
        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {basic}"}
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "code_verifier": CODE_VERIFIER,
        }
        try:
            response = requests.post(token_url, data=payload, headers=headers, timeout=20)
            if response.status_code != 200:
                log(f"トークン交換HTTPエラー: {response.status_code} - {response.text[:200]}")
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data.get("refresh_token")
            self.last_refresh_time = time.time()
            log("アクセストークンを正常に取得しました。")
            if not self.fetch_account_keys():
                log("トークン取得後にアカウントキーの取得に失敗しました。")
                return False
            return True
        except requests.exceptions.RequestException as e:
            log(f"トークン交換エラー: {e}")
            if hasattr(e, "response") and e.response is not None:
                log(f"トークン交換レスポンス内容(一部): {e.response.text[:300]}")
            return False

    def refresh_access_token(self) -> bool:
        with self.refresh_lock:
            if not self.refresh_token:
                log("リフレッシュトークンがありません。更新できません。")
                return False

            log("アクセストークンを更新しています...")
            token_url = self.token_endpoint
            basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
            headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {basic}"}
            payload = {"grant_type": "refresh_token", "refresh_token": self.refresh_token, "client_id": self.client_id}

            for attempt in range(3):
                try:
                    response = requests.post(token_url, data=payload, headers=headers, timeout=20)

                    if response.status_code == 401:
                        log("リフレッシュトークンが無効です。完全な再認証が必要です。")
                        return False

                    if response.status_code != 200:
                        log(f"トークン更新HTTPエラー: {response.status_code} - {response.text[:200]}")
                    response.raise_for_status()

                    token_data = response.json()
                    self.access_token = token_data["access_token"]
                    if "refresh_token" in token_data:
                        self.refresh_token = token_data["refresh_token"]
                    self.last_refresh_time = time.time()
                    log("アクセストークンを正常に更新しました。")
                    return True

                except requests.exceptions.RequestException as e:
                    log(f"トークン更新エラー (試行 {attempt + 1}/3): {e}")
                    if hasattr(e, "response") and e.response is not None:
                        log(f"トークン更新レスポンス内容(一部): {e.response.text[:300]}")

                    if attempt < 2:
                        wait_time = (attempt + 1) * 5
                        log(f"{wait_time}秒後に再試行します...")
                        time.sleep(wait_time)

            log("トークン更新に3回失敗しました。")
            return False

    def authenticate(self) -> bool:
        if self.access_token and self.validate_token():
            log("既存のトークンは有効です。")
            return True
        return self.perform_oauth_flow()

    def validate_token(self) -> bool:
        if not self.access_token:
            return False
        log("現在のアクセストークンを検証しています...")

        response_data = self._make_request("GET", "/port/v1/clients/me")

        if response_data and "ClientKey" in response_data:
            log("トークン検証成功。")
            return True
        log(f"トークン検証失敗。レスポンス: {response_data}")
        return False

    def fetch_account_keys(self) -> bool:
        log("アカウントキーを取得しています...")
        response_data = self._make_request("GET", "/port/v1/accounts/me")
        if response_data and "Data" in response_data and len(response_data["Data"]) > 0:
            for acc in response_data["Data"]:
                if "FxSpot" in acc.get("LegalAssetTypes", []) and acc.get("AccountType") != "SaxoCash":
                    self.account_key = acc.get("AccountKey")
                    self.client_key = acc.get("ClientKey")
                    log(
                        "FX AccountKey: %s, ClientKey: %s を AccountId: %s 用に選択しました。"
                        % (_mask(self.account_key), _mask(self.client_key), acc.get("AccountId"))
                    )
                    if self.account_key and self.client_key:
                        return True
            log("適切なFX口座が見つからないか、AccountKey/ClientKeyがありません。")
            return False
        log(f"アカウントキーの取得に失敗したか、データがありません。レスポンス: {response_data}")
        return False

    def get_account_balance_and_currency(self) -> Tuple[Optional[Decimal], Optional[str]]:
        if not self.account_key:
            log("AccountKeyが設定されていません。残高を取得できません。")
            if not self.fetch_account_keys():
                return None, None

        log("口座残高を取得しています...")
        endpoint = "/port/v1/balances"
        params = {"AccountKey": self.account_key, "ClientKey": self.client_key}

        response_data = self._make_request("GET", endpoint, params=params)
        if response_data:
            if "Data" in response_data and isinstance(response_data["Data"], list) and len(response_data["Data"]) > 0:
                balance_info = response_data["Data"][0]
            elif "CashBalance" in response_data and "Currency" in response_data:
                balance_info = response_data
            else:
                if isinstance(response_data, dict) and "TotalValue" in response_data:
                    balance_info = response_data
                else:
                    balance_info = (
                        response_data.get("Data", [{}])[0]
                        if isinstance(response_data.get("Data"), list) and response_data.get("Data")
                        else response_data
                    )

            cash_balance = balance_info.get("CashBalance")
            if cash_balance is None:
                cash_balance = balance_info.get("TotalValue")

            currency = balance_info.get("Currency")

            if cash_balance is not None and currency:
                log(f"口座残高: {cash_balance} {currency}")
                return Decimal(str(cash_balance)), currency
            log(f"残高レスポンスにCashBalanceまたはCurrencyが見つかりません: {balance_info}")
        else:
            log(f"口座残高の取得に失敗しました。レスポンス: {response_data}")
        return None, None

    def fetch_pair_uic_map(self, pair_list: List[str]) -> Dict[str, Dict]:
        log("通貨ペアのUICマップを取得しています...")
        pairs_to_fetch = [p for p in pair_list if p not in self.pair_uic_cache]

        if not pairs_to_fetch:
            log("すべてのUICは既にキャッシュにあります。")
            return self.pair_uic_cache.copy()

        keywords_str = " ".join([p.replace("/", "") for p in pairs_to_fetch])

        endpoint = "/ref/v1/instruments"
        params = {
            "AssetTypes": "FxSpot",
            "Keywords": keywords_str,
            "AccountKey": self.account_key,
            "IncludeNonTradable": "false",
        }

        response_data = self._make_request("GET", endpoint, params=params)

        if response_data and "Data" in response_data:
            for instrument in response_data["Data"]:
                symbol = instrument.get("Symbol")
                uic = instrument.get("Identifier")
                asset_type = instrument.get("AssetType")
                display_format = instrument.get("Format", {}).get("Decimals", 5)

                if symbol and uic and asset_type == "FxSpot":
                    if len(symbol) == 6:
                        original_pair_name = f"{symbol[:3]}/{symbol[3:]}"
                        if original_pair_name in pairs_to_fetch:
                            self.pair_uic_cache[original_pair_name] = {
                                "uic": str(uic),
                                "asset_type": asset_type,
                                "symbol": symbol,
                                "decimals": display_format,
                            }
                            log(f"UICをマッピングしました: {original_pair_name} -> {uic} (小数点以下桁数: {display_format})")
        else:
            log(f"UICマッピング用の銘柄データの取得に失敗しました。キーワード: {keywords_str}, レスポンス: {response_data}")

        for p in pairs_to_fetch:
            if p not in self.pair_uic_cache:
                log(f"警告: 通貨ペア {p} のUICが見つかりませんでした。")
                send_discord(f"⚠️ 通貨ペア {p} のUICマッピングに失敗しました。")

        return self.pair_uic_cache.copy()

    def fetch_price_infos(
        self, uic_list: List[int], asset_type: str = "FxSpot", field_groups: Optional[List[str]] = None
    ) -> Dict[int, Dict[str, Any]]:
        if not uic_list:
            log("価格取得対象のUICリストが空です。")
            return {}

        endpoint = "/trade/v1/infoprices/list"

        params = {"AccountKey": self.account_key, "Uics": ",".join(map(str, uic_list)), "AssetType": asset_type}

        if field_groups:
            params["FieldGroups"] = ",".join(field_groups)
        else:
            params["FieldGroups"] = "Quote,DisplayAndFormat,PriceInfo"

        log(
            f"価格情報を取得します。UICs: {params['Uics']}, AssetType: {params['AssetType']}, "
            f"FieldGroups: {params.get('FieldGroups')}"
        )

        response_data = self._make_request("GET", endpoint, params=params, is_price_request=True)

        price_infos_map: Dict[int, Dict[str, Any]] = {}

        if response_data and "Data" in response_data and isinstance(response_data["Data"], list):
            for item in response_data["Data"]:
                uic_from_response = item.get("Uic")
                quote_info = item.get("Quote")
                if (
                    isinstance(uic_from_response, int)
                    and quote_info
                    and quote_info.get("Bid") is not None
                    and quote_info.get("Ask") is not None
                ):
                    price_infos_map[uic_from_response] = item
                else:
                    log(f"レスポンスに無効なUIC ({uic_from_response}) または不完全な価格情報が含まれています: {item.get('Quote')}")

            for requested_uic in uic_list:
                if requested_uic not in price_infos_map:
                    log(f"警告: UIC {requested_uic} の価格情報がレスポンスに含まれていないか、不完全でした。")

        elif response_data and "ErrorInfo" in response_data:
            log(f"価格情報の取得に失敗しました (APIエラー)。ErrorInfo: {response_data['ErrorInfo']}")

        else:
            log(f"価格情報の取得に失敗しました。UICs: {params['Uics']}。レスポンスが不正か空です: {response_data}")

        return price_infos_map

    def get_price_info(self, uic: str, asset_type: str = "FxSpot") -> Optional[Dict]:
        endpoint = "/trade/v1/infoprices"
        params = {"AccountKey": self.account_key, "Uic": str(uic), "AssetType": asset_type, "FieldGroups": "Quote,DisplayAndFormat"}
        data = self._make_request("GET", endpoint, params=params, is_price_request=True)
        if data and "Data" in data and len(data["Data"]) > 0:
            if "Quote" in data["Data"][0] and data["Data"][0]["Quote"].get("Bid") is not None and data["Data"][0][
                "Quote"
            ].get("Ask") is not None:
                return data["Data"][0]
            log(f"UIC {uic} の価格情報にQuote内のBid/Askがありません: {data['Data'][0].get('Quote')}")
            return None
        if data and "Quote" in data and data["Quote"].get("Bid") is not None and data["Quote"].get("Ask") is not None:
            return data
        log(f"UIC {uic} の価格情報取得に失敗しました。レスポンス: {data}")
        return None

    def _pip_value_from_display(self, display: Optional[Dict[str, Any]]) -> float:
        if not display:
            return 0.0
        decimals = display.get("PriceDecimals") or display.get("Decimals")
        if decimals is None:
            return 0.0
        try:
            decimals_int = int(decimals)
        except (TypeError, ValueError):
            return 0.0
        if decimals_int <= 0:
            return 0.0
        return float(Decimal("1") / (Decimal("10") ** Decimal(decimals_int - 1)))

    @staticmethod
    def _round_price(value: float, display: Optional[Dict[str, Any]]) -> float:
        decimals = None
        if display:
            decimals = display.get("PriceDecimals") or display.get("Decimals")
        try:
            decimals_int = int(decimals) if decimals is not None else None
        except (TypeError, ValueError):
            decimals_int = None
        if decimals_int is None:
            return float(value)
        quant = Decimal(f"1e-{decimals_int}")
        return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

    @staticmethod
    def _infer_tp_sl_label(order_type: Optional[str]) -> str:
        if not order_type:
            return "TP/SL"
        order_type_lower = str(order_type).lower()
        if order_type_lower.startswith("limit"):
            return "TP"
        if order_type_lower.startswith("stop"):
            return "SL"
        return "TP/SL"

    def place_market_order_with_sl_tp(
        self,
        uic: int,
        buy_sell: str,
        amount: float,
        stop_loss_pips: float,
        take_profit_pips: float,
        external_reference: str,
    ) -> str:
        if self.access_token is None:
            raise RuntimeError("セッションが初期化されていません。")

        price_infos = self.fetch_price_infos([uic], asset_type="FxSpot", field_groups=["Quote", "DisplayAndFormat"])
        price_item = price_infos.get(uic)
        if not price_item:
            raise RuntimeError(f"決済価格取得に失敗しました。UIC={uic}")

        quote = price_item.get("Quote") or {}
        if quote.get("Bid") is None or quote.get("Ask") is None:
            raise RuntimeError(f"決済価格取得に失敗しました。UIC={uic} Quote={quote}")

        bid = float(quote["Bid"])
        ask = float(quote["Ask"])
        base_price = ask if buy_sell == "Buy" else bid

        display = price_item.get("DisplayAndFormat")
        pip_value = self._pip_value_from_display(display)

        if pip_value <= 0:
            log(f"pip_value<=0 のため 0.01 を使用します。pip_value={pip_value}")
            pip_value = 0.01

        if buy_sell == "Buy":
            sl_price = base_price - stop_loss_pips * pip_value
            tp_price = base_price + take_profit_pips * pip_value
        else:
            sl_price = base_price + stop_loss_pips * pip_value
            tp_price = base_price - take_profit_pips * pip_value

        body = {
            "AccountKey": self.account_key,
            "Uic": uic,
            "AssetType": "FxSpot",
            "Amount": float(amount),
            "AmountType": "Quantity",
            "BuySell": buy_sell,
            "OrderType": "Market",
            "ToOpenClose": "ToOpen",
            "OrderDuration": {"DurationType": "DayOrder"},
            "ManualOrder": False,
            "ExternalReference": external_reference,
        }

        related_orders: List[Dict[str, Any]] = []
        related_buy_sell = "Sell" if buy_sell == "Buy" else "Buy"

        if stop_loss_pips > 0:
            related_orders.append(
                {
                    "Uic": uic,
                    "AssetType": "FxSpot",
                    "BuySell": related_buy_sell,
                    "Amount": float(amount),
                    "OrderType": "Stop",
                    "OrderPrice": self._round_price(sl_price, display),
                    "OrderDuration": {"DurationType": "GoodTillCancel"},
                    "ManualOrder": False,
                }
            )
        if take_profit_pips > 0:
            related_orders.append(
                {
                    "Uic": uic,
                    "AssetType": "FxSpot",
                    "BuySell": related_buy_sell,
                    "Amount": float(amount),
                    "OrderType": "Limit",
                    "OrderPrice": self._round_price(tp_price, display),
                    "OrderDuration": {"DurationType": "GoodTillCancel"},
                    "ManualOrder": False,
                }
            )

        if related_orders:
            body["Orders"] = related_orders

        data = self._make_request("POST", "/trade/v2/orders", json_data=body, retry_safe=False)
        if isinstance(data, dict) and data.get("ErrorInfo"):
            log(f"注文エラー(ErrorInfo): {data['ErrorInfo']}")
            raise RuntimeError("注文がErrorInfoで失敗しました。")

        if data is None:
            found_order = self.find_order_by_external_reference(external_reference)
            if found_order:
                log(f"ExternalReference一致の既存注文を検出しました: {found_order}")
                return found_order["order_id"]

        if isinstance(data, dict):
            related_orders = data.get("Orders") or data.get("RelatedOrders") or []
            if isinstance(related_orders, list) and related_orders:
                log(f"関連注文を確認: {len(related_orders)}件")
                for idx, related in enumerate(related_orders):
                    if isinstance(related, dict):
                        related_order_id = related.get("OrderId")
                        related_order_type = related.get("OrderType")
                        if related_order_id:
                            label = self._infer_tp_sl_label(related_order_type)
                            self.related_order_labels[str(related_order_id)] = label
                            self.tp_sl_order_ids_by_uic.setdefault(uic, set()).add(str(related_order_id))
                            log(
                                f"✅ {label}注文が成立: OrderId={related_order_id}, Type={related_order_type}"
                            )
                        log(
                            "  関連注文{idx}: OrderId={order_id}, Status={status}, Type={order_type}".format(
                                idx=idx + 1,
                                order_id=related.get("OrderId"),
                                status=related.get("Status"),
                                order_type=related.get("OrderType"),
                            )
                        )

        order_id = data.get("OrderId") if isinstance(data, dict) else None
        if not order_id:
            orders = data.get("Orders") if isinstance(data, dict) else None
            if orders and isinstance(orders, list):
                order_id = orders[0].get("OrderId")

        if not order_id:
            log(f"注文応答に OrderId がありません: {data}")
            raise RuntimeError("OrderId が取得できませんでした。")

        log(f"Market + SL/TP 注文送信完了: OrderId={order_id}")
        return order_id

    def place_order(
        self,
        pair_name: str,
        uic: int,
        asset_type: str,
        side: str,
        amount: Decimal,
        current_price_for_sl_tp: Optional[Decimal],
        external_reference: str,
    ) -> Optional[Dict]:
        log(f"エントリー処理開始 (UIC: {uic}, Side: {side}, Amount: {amount})...")

        has_existing, existing_data = self.check_existing_positions_and_orders(uic)
        if has_existing:
            if existing_data and existing_data.get("type") == "pending_order":
                log(f"警告: {pair_name} には未約定注文 (ID: {existing_data.get('order_id')}) が存在します。")
                send_discord(f"⚠️ {pair_name} エントリー中止: 未約定注文が存在するため。")
            else:
                log(f"警告: {pair_name} には既にポジションが存在します。")
                send_discord(f"⚠️ {pair_name} エントリー中止: 既存ポジションのため。")
            return existing_data

        log("既存取引がないため、新規注文を発注します...")

        if current_price_for_sl_tp and (self.cfg.take_profit_pips > 0 or self.cfg.stop_loss_pips > 0):
            try:
                order_id = self.place_market_order_with_sl_tp(
                    uic=uic,
                    buy_sell=side,
                    amount=float(amount),
                    stop_loss_pips=self.cfg.stop_loss_pips,
                    take_profit_pips=self.cfg.take_profit_pips,
                    external_reference=external_reference,
                )
                return {"order_id": order_id, "status": "pending_fill", "external_reference": external_reference}
            except Exception as e:
                log(f"SL/TP付き注文に失敗したため通常注文へフォールバックします: {e}")

        order_data = {
            "AccountKey": self.account_key,
            "AmountType": "Quantity",
            "Uic": uic,
            "AssetType": asset_type,
            "OrderType": "Market",
            "BuySell": side,
            "Amount": float(amount),
            "OrderDuration": {"DurationType": "DayOrder"},
            "ManualOrder": False,
            "ExternalReference": external_reference,
        }

        try:
            response = self._make_request("POST", "/trade/v2/orders", json_data=order_data, retry_safe=False)

            if response and "OrderId" in response:
                order_id = response["OrderId"]
                log(f"注文受付成功: OrderID {order_id}")

                if "Orders" in response:
                    related_orders = response["Orders"]
                    log(f"関連注文も作成されました: {len(related_orders)}件")
                    for idx, related in enumerate(related_orders):
                        if "OrderId" in related:
                            log(f"  関連注文{idx + 1}: {related['OrderId']}")

                return {"order_id": order_id, "status": "pending_fill", "external_reference": external_reference}

            if response is None:
                found_order = self.find_order_by_external_reference(external_reference)
                if found_order:
                    log(f"ExternalReference一致の既存注文を検出しました: {found_order}")
                    return {
                        "order_id": found_order["order_id"],
                        "status": found_order.get("status", "unknown"),
                        "external_reference": external_reference,
                    }
                log("注文の成否が不明です。安全のため再発注しません。")
                return {"order_id": None, "status": "unknown", "external_reference": external_reference}

            if response and "ErrorInfo" in response:
                error_info = response["ErrorInfo"]
                error_code = error_info.get("ErrorCode", "Unknown")
                error_message = error_info.get("Message", "不明なエラー")
                log(f"注文発注エラー: {error_code} - {error_message}")
                send_discord(f"❌ {pair_name} 注文エラー: {error_message}")
                return None

            log(f"注文発注に失敗しました。予期しないレスポンス: {response}")
            send_discord(f"❌ {pair_name} 注文発注失敗: 予期しないレスポンス")
            return None

        except Exception as e:
            log(f"注文発注中に例外が発生: {e}")
            send_discord(f"❌ {pair_name} 注文発注中に例外: {str(e)}")
            return None

    def get_position_details_by_order_id(self, order_id: str, uic: int) -> Optional[Dict]:
        log(f"OrderID {order_id} に由来するポジションを検索中 (UIC: {uic})...")
        params = {
            "AccountKey": self.account_key,
            "ClientKey": self.client_key,
            "Uics": str(uic),
            "FieldGroups": "PositionBase,PositionView",
            "$top": 1000,
        }
        response = self._make_request("GET", "/port/v1/positions", params=params)
        if response and "Data" in response:
            for pos in response["Data"]:
                details = self._extract_position_details(pos)
                if details and details.get("source_order_id") == str(order_id):
                    log(f"★ OrderIDの一致でポジションを発見: PosId={details['position_id']}")
                    return details
        return None

    def get_position_details_by_uic(self, uic: int) -> Optional[Dict]:
        log(f"ポジション情報を検索中 (UIC: {uic})...")
        endpoint = "/port/v1/positions"
        params = {
            "AccountKey": self.account_key,
            "ClientKey": self.client_key,
            "Uics": str(uic),
            "FieldGroups": "PositionBase,PositionView",
            "$top": 1000,
        }
        positions_data = self._make_request("GET", endpoint, params=params)

        if positions_data and "Data" in positions_data and len(positions_data["Data"]) > 0:
            latest_position = sorted(
                positions_data["Data"],
                key=lambda p: p.get("PositionBase", {}).get("ExecutionTimeOpen", ""),
                reverse=True,
            )[0]
            log(f"UIC {uic} の最新ポジションを発見しました。")
            return self._extract_position_details(latest_position)

        return None

    def _extract_position_details(self, position_data: Dict) -> Optional[Dict]:
        pos_base = position_data.get("PositionBase", {})
        position_id = position_data.get("PositionId")
        open_price = pos_base.get("OpenPrice")
        amount = pos_base.get("Amount")
        source_order_id = pos_base.get("SourceOrderId")

        execution_time_utc_str = pos_base.get("ExecutionTimeOpen")

        if all(v is not None for v in [position_id, open_price, amount, execution_time_utc_str]):
            return {
                "position_id": str(position_id),
                "open_price": Decimal(str(open_price)),
                "amount": Decimal(str(amount)),
                "source_order_id": str(source_order_id) if source_order_id else None,
                "execution_time": execution_time_utc_str,
            }

        log(f"ポジション詳細の抽出に失敗: 不足している情報があります。PositionData: {position_data}")
        return None

    def close_position_market(
        self,
        position_id: str,
        pair_name: str,
        uic: int,
        asset_type: str,
        amount_to_close: Decimal,
        original_side: str,
        external_reference: str,
    ) -> Optional[str]:
        log(f"ポジション {position_id} ({pair_name}) の決済処理開始...")

        try:
            current_position = self.get_position_details_by_uic(uic)
            if not current_position:
                log(f"ポジション {position_id} が見つかりません。既に決済済みの可能性があります。")
                send_discord(f"⚠️ {pair_name} ポジション {position_id} が見つかりません（既に決済済み？）")
                return None

            if current_position.get("position_id") != position_id:
                log(f"警告: 要求されたポジションID {position_id} と現在のポジションID {current_position.get('position_id')} が一致しません。")

            current_amount = current_position.get("amount") or Decimal("0")
            if current_amount == 0:
                log(f"ポジション {position_id} は既に数量0のため決済済みと扱います。")
                return None
            if amount_to_close is None or amount_to_close <= 0:
                amount_to_close = current_amount
            amount_to_close = Decimal(str(min(abs(current_amount), abs(amount_to_close))))

            close_side = "Sell" if current_amount > 0 else "Buy"
            order_data = {
                "AccountKey": self.account_key,
                "AmountType": "Quantity",
                "Uic": uic,
                "AssetType": asset_type,
                "OrderType": "Market",
                "BuySell": close_side,
                "Amount": float(abs(amount_to_close)),
                "ToOpenClose": "ToClose",
                "OrderDuration": {"DurationType": "DayOrder"},
                "ManualOrder": False,
                "ExternalReference": external_reference,
            }

            log(f"決済注文データ: {close_side} {amount_to_close} units of UIC {uic}")

            response = self._make_request("POST", "/trade/v2/orders", json_data=order_data, retry_safe=False)

            if response and "OrderId" in response:
                order_id = response["OrderId"]
                log(f"{pair_name} の決済注文が受付されました。OrderId: {order_id}")
                return order_id

            if response is None:
                found_order = self.find_order_by_external_reference(external_reference)
                if found_order:
                    log(f"ExternalReference一致の既存注文を検出しました: {found_order}")
                    return found_order["order_id"]

            if response and "ErrorInfo" in response:
                error_info = response["ErrorInfo"]
                error_code = error_info.get("ErrorCode", "Unknown")
                error_message = error_info.get("Message", "不明なエラー")
                log(f"決済注文エラー: {error_code} - {error_message}")
                send_discord(f"❌ {pair_name} 決済注文エラー: {error_message}")
                return None

            log(f"決済注文が失敗しました。予期しないレスポンス: {response}")
            send_discord(f"❌ {pair_name} 決済注文失敗: 予期しないレスポンス")
            return None

        except Exception as e:
            log(f"決済注文実行中に例外が発生: {e}")
            send_discord(f"❌ {pair_name} 決済処理中に例外: {str(e)}")

            try:
                remaining_position = self.get_position_details_by_uic(uic)
                if not remaining_position:
                    log(f"例外発生後の確認: ポジション {position_id} は存在しません（決済済みの可能性）")
                    send_discord(f"ℹ️ {pair_name} ポジションは決済済みの可能性があります")
            except Exception as check_error:
                log(f"例外後のポジション確認も失敗: {check_error}")

            return None

    def check_order_status_via_audit_api(self, order_id: str) -> Optional[Dict]:
        log(f"フォールバック実行: 監査APIで注文 {order_id} の状態を確認します。")
        endpoint = "/cs/v1/audit/orderactivities"
        params = {"OrderId": order_id, "EntryType": "Last", "AccountKey": self.account_key, "ClientKey": self.client_key}

        for i in range(3):
            try:
                response = self._make_request("GET", endpoint, params=params)
                if response and "Data" in response and len(response["Data"]) > 0:
                    activity = response["Data"][0]
                    log(f"監査APIから応答あり: Status={activity.get('Status')}")
                    if activity.get("Status") in ["FinalFill", "Fill"] and activity.get("AveragePrice") is not None:
                        log(f"★ 監査APIにより約定を確認: 価格={activity.get('AveragePrice')}")

                        execution_time_str = activity.get("ActivityTime")
                        formatted_time_str = None
                        if execution_time_str:
                            try:
                                dt_utc = datetime.fromisoformat(execution_time_str.replace("Z", "+00:00"))
                                formatted_time_str = dt_utc.astimezone(TIMEZONE_TOKYO).strftime("%Y-%m-%d %H:%M:%S")
                            except Exception as e:
                                log(f"監査APIからの時刻変換エラー: {e}")

                        return {
                            "type": "order_fill_fallback",
                            "order_id": order_id,
                            "execution_price": Decimal(str(activity["AveragePrice"])),
                            "execution_time": formatted_time_str,
                            "position_id": activity.get("PositionId"),
                            "status": "filled",
                        }
                log(f"監査API試行 {i + 1}/3: 約定情報見つからず。5秒後に再試行...")
                time.sleep(5)
            except Exception as e:
                log(f"監査APIの呼び出し中にエラー: {e}")
                time.sleep(5)

        log(f"監査APIによる確認でも、注文 {order_id} の約定情報が見つかりませんでした。")
        return None

    def check_existing_positions_and_orders(self, uic: int) -> Tuple[bool, Optional[Dict]]:
        log(f"UIC {uic} の既存取引（ポジション/Working注文）を確認中...")

        try:
            endpoint = "/port/v1/positions"
            params = {
                "AccountKey": self.account_key,
                "ClientKey": self.client_key,
                "Uics": str(uic),
                "FieldGroups": "PositionBase,PositionView",
                "$top": 100,
            }

            positions_data = self._make_request("GET", endpoint, params=params)
            if positions_data and "Data" in positions_data:
                for position in positions_data["Data"]:
                    log(f"既存ポジションを発見: PositionId {position.get('PositionId')}")
                    return True, self._extract_position_details(position)

            endpoint = "/port/v1/orders"
            params = {"AccountKey": self.account_key, "ClientKey": self.client_key, "Uics": str(uic), "$top": 100}

            orders_data = self._make_request("GET", endpoint, params=params)
            if orders_data and "Data" in orders_data:
                for order in orders_data["Data"]:
                    if order.get("Status") in ["Working", "Placed", "Queued"]:
                        log(f"未約定注文を発見: OrderId {order.get('OrderId')}, Status: {order.get('Status')}")
                        return True, {"order_id": str(order.get("OrderId")), "status": order.get("Status"), "type": "pending_order"}

            log(f"UIC {uic} の既存取引は見つかりませんでした。")
            return False, None

        except Exception as e:
            log(f"既存取引確認中にエラー: {e}")
            return True, None

    def list_working_orders_by_uic(self, uic: int) -> List[Dict]:
        endpoint = "/port/v1/orders"
        params = {"AccountKey": self.account_key, "ClientKey": self.client_key, "Uics": str(uic), "$top": 100}
        orders_data = self._make_request("GET", endpoint, params=params)
        if not orders_data or "Data" not in orders_data:
            return []
        working_statuses = {"Working", "Placed", "Queued"}
        return [order for order in orders_data["Data"] if order.get("Status") in working_statuses]

    def cancel_order(self, order_id: str, uic: Optional[int] = None) -> bool:
        if not order_id:
            return False
        endpoint = f"/trade/v2/orders/{order_id}"
        params = {"AccountKey": self.account_key}
        response = self._make_request("DELETE", endpoint, params=params)
        if response is None:
            log(f"注文キャンセルに失敗しました: OrderId={order_id}")
            return False
        log(f"注文キャンセルを実行しました: OrderId={order_id}")
        if uic is not None:
            self.tp_sl_order_ids_by_uic.get(uic, set()).discard(str(order_id))
        return True

    def _get_tp_sl_working_orders(self, uic: int, working_orders: List[Dict]) -> List[Dict]:
        saved_ids = self.tp_sl_order_ids_by_uic.get(uic, set())
        if not saved_ids:
            return []
        return [order for order in working_orders if str(order.get("OrderId")) in saved_ids]

    def cancel_related_orders_for_uic(self, uic: int) -> None:
        working_orders = self.list_working_orders_by_uic(uic)
        if not working_orders:
            log(f"UIC {uic} のキャンセル対象注文はありません。")
            return
        cancel_candidates = self._get_tp_sl_working_orders(uic, working_orders)
        if not cancel_candidates:
            log(f"UIC {uic} のTP/SL候補注文はありません。")
            return

        log(f"UIC {uic} のTP/SL候補注文を {len(cancel_candidates)} 件キャンセルします。")
        failed_ids = set()
        for order in cancel_candidates:
            order_id = str(order.get("OrderId"))
            if not order_id:
                continue
            if not self.cancel_order(order_id, uic=uic):
                failed_ids.add(order_id)

        if failed_ids:
            log(f"TP/SLキャンセル失敗検知: {len(failed_ids)} 件。再確認します。")
            working_orders = self.list_working_orders_by_uic(uic)
            remaining = self._get_tp_sl_working_orders(uic, working_orders)
            retry_ids = {str(order.get("OrderId")) for order in remaining if order.get("OrderId")}
            if retry_ids:
                log(f"TP/SLキャンセル再試行を実行します: {len(retry_ids)} 件")
                for order_id in retry_ids:
                    self.cancel_order(order_id, uic=uic)

            working_orders = self.list_working_orders_by_uic(uic)
            remaining = self._get_tp_sl_working_orders(uic, working_orders)
            if remaining:
                log(f"TP/SLが残存しているため全注文キャンセルを実行します: {len(working_orders)} 件")
                for order in working_orders:
                    order_id = str(order.get("OrderId"))
                    if order_id:
                        self.cancel_order(order_id, uic=uic)

    def find_order_by_external_reference(self, external_reference: str) -> Optional[Dict]:
        if not external_reference:
            return None
        try:
            endpoint = "/port/v1/orders"
            params = {
                "AccountKey": self.account_key,
                "ClientKey": self.client_key,
                "$top": 1000,
            }
            orders_data = self._make_request("GET", endpoint, params=params)
            if orders_data and "Data" in orders_data:
                for order in orders_data["Data"]:
                    if order.get("ExternalReference") == external_reference:
                        return {"order_id": str(order.get("OrderId")), "status": order.get("Status")}
        except Exception as e:
            log(f"ExternalReferenceによる注文確認に失敗: {e}")
        return None

    def delete_tokens_and_keys(self):
        self.access_token = None
        self.refresh_token = None
        self.account_key = None
        self.client_key = None
        log("クライアントからトークンとアカウント/クライアントキーをクリアしました。")


class SaxoENSClient:
    def __init__(self, saxo_client, ens_url: str, access_token: str, log_func=None, notify_func=None):
        self.saxo_client = saxo_client
        self._log = log_func or getattr(saxo_client, "log", print)
        self._notify = notify_func
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.ens_url = ens_url
        self.access_token = access_token
        self.subscription_id: Optional[str] = None
        self.is_connected = False
        self.event_handlers: Dict[str, callable] = {
            "OrderFillEvent": self._handle_order_event,
            "PositionChangeEvent": self._handle_position_event,
        }
        self._listen_task: Optional[asyncio.Task] = None
        self.reconnect_task: Optional[asyncio.Task] = None
        self.last_message_timestamp: float = 0.0
        self.last_message_id: Optional[int] = None
        self.last_message_summary: Optional[str] = None
        self.last_ping_ok_timestamp: Optional[float] = None
        self.last_ping_rtt_ms: Optional[float] = None
        self._monitor_task: Optional[asyncio.Task] = None
        self.shutdown_requested = False
        self.reconnect_attempts = 0
        self.reconnect_started_at: Optional[float] = None
        self.last_disconnect_at: Optional[float] = None
        self._last_notify_seconds: Optional[int] = None
        self._binary_remainder: bytes = b""

    async def connect(self):
        self.access_token = self.saxo_client.access_token
        if not self.access_token:
            self._log("ENS接続試行時にアクセストークンがありません。")
            return

        if self.ws is not None:
            await self.ws.close()
            self.ws = None

        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
        if self._listen_task and not self._listen_task.done():
            self._listen_task.cancel()

        try:
            self._log(f"ENS WebSocket接続中: {self.saxo_client._mask_ws_url_for_log(self.ens_url)}")

            self.ws = await websockets.connect(
                self.ens_url,
                ping_interval=CFG.ws_ping_interval,
                ping_timeout=CFG.ws_ping_timeout,
                close_timeout=CFG.ws_close_timeout,
                max_queue=16,
            )
            self.is_connected = True
            self._log("ENS WebSocket接続成功")

            self.last_message_timestamp = time.time()
            self.reconnect_attempts = 0
            self.reconnect_started_at = None

            self._listen_task = asyncio.create_task(self.listen())
            self._monitor_task = asyncio.create_task(self.monitor_connection())

        except websockets.InvalidStatusCode as e:
            self._log(f"ENS WebSocket接続エラー: {e} ({type(e).__name__})")
            self.is_connected = False
            if getattr(e, "status_code", None) == 409:
                await self.reconnect(force_new_context=True)
                return
            await self.reconnect()
        except Exception as e:
            self._log(f"ENS WebSocket接続エラー: {e} ({type(e).__name__})")
            self.is_connected = False
            await self.reconnect()

    def _log_disconnect_context(self, reason: str, exc: Optional[BaseException] = None) -> None:
        now = time.time()
        last_message_at = None
        if self.last_message_timestamp:
            last_message_at = datetime.fromtimestamp(self.last_message_timestamp, tz=TIMEZONE_TOKYO).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        last_ping_at = None
        if self.last_ping_ok_timestamp:
            last_ping_at = datetime.fromtimestamp(self.last_ping_ok_timestamp, tz=TIMEZONE_TOKYO).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        detail = [f"reason={reason}"]
        if exc:
            detail.append(f"exception={type(exc).__name__}")
            if hasattr(exc, "code"):
                detail.append(f"close_code={getattr(exc, 'code', None)}")
            if hasattr(exc, "reason"):
                detail.append(f"close_reason={getattr(exc, 'reason', None)}")
        if last_message_at:
            detail.append(f"last_message_at={last_message_at}")
        if self.last_message_id:
            detail.append(f"last_message_id={self.last_message_id}")
        if last_ping_at:
            detail.append(f"last_ping_ok_at={last_ping_at}")
        if self.last_ping_rtt_ms is not None:
            detail.append(f"last_ping_rtt_ms={self.last_ping_rtt_ms:.1f}")
        if self.last_message_summary:
            detail.append(f"last_message_summary={self.last_message_summary}")
        self._log("ENS接続断の詳細: " + ", ".join(detail))

    async def reconnect(self, force_new_context: bool = False):
        if self.shutdown_requested:
            return
        if self.reconnect_task and not self.reconnect_task.done():
            self._log("既に再接続処理が進行中です。")
            return

        async def _reconnect_logic():
            reconnect_delay = 1
            max_reconnect_delay = CFG.ens_reconnect_max_delay_seconds
            self.reconnect_started_at = time.time()
            while not self.is_connected and not self.shutdown_requested:
                self.reconnect_attempts += 1
                self._log(
                    "ENS WebSocketに再接続を試みています... "
                    f"{reconnect_delay}秒後 (試行{self.reconnect_attempts})"
                )
                await asyncio.sleep(reconnect_delay)
                try:
                    if not force_new_context:
                        refreshed = await asyncio.to_thread(self.saxo_client.refresh_access_token)
                        if refreshed:
                            await asyncio.to_thread(self.saxo_client.authorize_streaming_context)
                            rebuilt = await asyncio.to_thread(self.saxo_client.rebuild_streaming_url, self.last_message_id)
                            if rebuilt:
                                self.ens_url = rebuilt
                                await self.connect()
                                if self.is_connected:
                                    self._log("ENS WebSocketへの再接続に成功しました。")
                                    break

                    self._log("ENSサブスクリプションを再作成します...")
                    new_ens_url = await asyncio.to_thread(self.saxo_client.setup_ens_subscription)

                    if not new_ens_url:
                        self._log("ENSサブスクリプションの再作成に失敗しました。")
                        raise RuntimeError("ENS subscription creation failed")

                    self.ens_url = new_ens_url
                    await self.connect()

                    if self.is_connected:
                        self._log("ENS WebSocketへの再接続に成功しました。")
                        break

                except Exception as e:
                    self._log(f"ENS再接続プロセス中にエラー: {e}")
                    if "SubscriptionLimitExceeded" in str(e):
                        deleted = await asyncio.to_thread(self.saxo_client.delete_ens_subscription)
                        if deleted:
                            self._log("サブスクリプション削除後に再試行します。")
                force_new_context = False

                reconnect_delay = min(reconnect_delay * 2, max_reconnect_delay)
                reconnect_delay += random.uniform(0, 0.5)

        self.reconnect_task = asyncio.create_task(_reconnect_logic())

    def _extract_binary_messages(self, data: bytes) -> Tuple[List[Tuple[int, str, str]], bytes]:
        messages: List[Tuple[int, str, str]] = []
        off = 0
        n = len(data)
        while off + 16 <= n:
            message_id = int.from_bytes(data[off : off + 8], "little")
            ref_id_size = data[off + 10]
            ref_start = off + 11
            ref_end = ref_start + ref_id_size
            if ref_end + 1 > n:
                break

            payload_format = data[ref_end]
            if payload_format != 0:
                self._log(f"バイナリメッセージですが、未対応のペイロード形式です: {payload_format}")
                off = n
                break

            size_start = ref_end + 1
            size_end = size_start + 4
            if size_end > n:
                break

            payload_size = int.from_bytes(data[size_start:size_end], "little")
            payload_start = size_end
            payload_end = payload_start + payload_size
            if payload_end > n:
                break

            reference_id = data[ref_start:ref_end].decode("utf-8", errors="replace")
            payload_json = data[payload_start:payload_end].decode("utf-8", errors="replace")
            messages.append((message_id, reference_id, payload_json))
            off = payload_end

        return messages, data[off:]

    def _handle_control_message(self, domain_message: Dict[str, Any], received_at: float) -> bool:
        if domain_message.get("Reason"):
            self.last_message_timestamp = received_at
            reason = domain_message.get("Reason")
            self._log(f"ENS制御メッセージ検出: Reason={reason}")
            if reason in ["SubscriptionPermanentlyDisabled", "SessionLimitExceeded", "SubscriptionDisabled"]:
                self._log("ENSハートビート: subscription系の停止を検出しました。再接続します。")
                self.is_connected = False
                return True
            return False

        message_type = str(domain_message.get("MessageType", "")).lower()
        if message_type in ["disconnect", "reset", "reset-subscriptions", "resetsubscriptions"]:
            self._log(f"ENS制御メッセージ検出: MessageType={message_type}")
            self.is_connected = False
            return True

        return False

    async def listen(self):
        self.last_message_timestamp = time.time()
        while self.is_connected:
            try:
                message_raw = await self.ws.recv()
                received_at = time.time()
                json_payloads: List[str] = []
                if isinstance(message_raw, bytes):
                    buffer = self._binary_remainder + message_raw
                    try:
                        parsed_messages, remainder = self._extract_binary_messages(buffer)
                        self._binary_remainder = remainder
                        for message_id, _ref_id, payload in parsed_messages:
                            self.last_message_id = message_id
                            if payload:
                                json_payloads.append(payload)
                    except Exception as e:
                        self._log(f"バイナリメッセージの解析中に予期せぬエラー: {e}")
                        self._binary_remainder = b""
                        continue
                else:
                    if message_raw:
                        json_payloads = [message_raw]

                if not json_payloads:
                    continue

                for json_payload in json_payloads:
                    if not json_payload or not str(json_payload).strip():
                        continue
                    if isinstance(json_payload, str) and json_payload.startswith("_heartbeat"):
                        self.last_message_timestamp = received_at
                        continue

                    try:
                        domain_message = json.loads(json_payload)

                        control_handled = False
                        if isinstance(domain_message, dict):
                            self.last_message_summary = str(list(domain_message.keys()))
                            if self._handle_control_message(domain_message, received_at):
                                await self.reconnect()
                                control_handled = True
                        elif isinstance(domain_message, list):
                            for item in domain_message:
                                if isinstance(item, dict) and ("Reason" in item or "MessageType" in item):
                                    if self._handle_control_message(item, received_at):
                                        await self.reconnect()
                                        control_handled = True
                                        break

                        if control_handled:
                            continue

                        activities = []
                        if isinstance(domain_message, dict):
                            activities = domain_message.get("Data", [])
                        elif isinstance(domain_message, list):
                            activities = domain_message

                        if activities:
                            self.last_message_timestamp = received_at

                        for item in activities:
                            if isinstance(item, dict):
                                act_type = item.get("ActivityType")
                                if act_type == "Orders":
                                    await self._handle_order_event(item)
                                elif act_type == "Positions":
                                    await self._handle_position_event(item)

                    except json.JSONDecodeError:
                        self._log(f"JSONデコードエラー。受信データ: {str(json_payload)[:200]}")
                        continue

            except websockets.ConnectionClosed as e:
                self._log("ENS WebSocket接続が閉じられました。")
                self.last_disconnect_at = time.time()
                self._log_disconnect_context("ConnectionClosed", e)
                self.is_connected = False
                if not self.shutdown_requested:
                    await self.reconnect()
                break
            except Exception as e:
                self._log(f"ENSイベントの処理中に予期せぬエラーが発生しました: {e} ({type(e).__name__})")
                self.last_disconnect_at = time.time()
                self._log_disconnect_context("ListenerError", e)
                if "Connection is already closed" not in str(e):
                    self.is_connected = False
                    if not self.shutdown_requested:
                        await self.reconnect()
                break

    async def _handle_order_event(self, event_data: Dict):
        self._log(f"ENS Orderイベント受信: {event_data}")

        status = event_data.get("Status", "").lower()
        sub_status = event_data.get("SubStatus", "").lower()
        order_id = str(event_data.get("OrderId", ""))
        related_label = self.saxo_client.related_order_labels.get(order_id)

        if status in ["fill", "finalfill"] and sub_status == "confirmed":
            amount = Decimal(str(event_data.get("Amount", "0")))
            filled_amount = Decimal(str(event_data.get("FilledAmount", "0")))
            execution_price = event_data.get("ExecutionPrice")

            is_complete_fill = status == "finalfill" or (amount > 0 and filled_amount >= amount)
            if is_complete_fill and execution_price is not None:
                if related_label:
                    self._log(
                        f"🎯 {related_label}に到達し約定: OrderID={order_id}, Price={execution_price}"
                    )
                    self.saxo_client.related_order_labels.pop(order_id, None)
                    for uic, order_ids in self.saxo_client.tp_sl_order_ids_by_uic.items():
                        order_ids.discard(order_id)
                self._log(f"✨ ENSから注文完全約定イベント: OrderID={order_id}, Price={execution_price}")
                await self.saxo_client._get_ens_event_queue().put(
                    {
                        "type": "order_fill",
                        "order_id": order_id,
                        "execution_price": Decimal(str(execution_price)),
                        "execution_time": event_data.get("ActivityTime"),
                        "filled_amount": filled_amount,
                        "amount": amount,
                        "status": "filled",
                        "uic": event_data.get("Uic"),
                        "position_id": str(event_data.get("PositionId")) if event_data.get("PositionId") else None,
                    }
                )
                await self.saxo_client._dispatch_ens_event(
                    {
                        "type": "order_fill",
                        "order_id": order_id,
                        "execution_price": Decimal(str(execution_price)),
                        "execution_time": event_data.get("ActivityTime"),
                        "filled_amount": filled_amount,
                        "amount": amount,
                        "status": "filled",
                        "uic": event_data.get("Uic"),
                        "position_id": str(event_data.get("PositionId")) if event_data.get("PositionId") else None,
                    }
                )
        elif status in ["canceled", "cancelled", "rejected", "expired"]:
            if related_label:
                self._log(f"🧹 {related_label}注文がキャンセル: OrderID={order_id}, Status={status}")
                self.saxo_client.related_order_labels.pop(order_id, None)
                for uic, order_ids in self.saxo_client.tp_sl_order_ids_by_uic.items():
                    order_ids.discard(order_id)
            self._log(f"ENSから注文ステータス変更イベント: OrderID={event_data.get('OrderId')}, Status={status}")
            await self.saxo_client._get_ens_event_queue().put(
                {
                    "type": "order_status_change",
                    "order_id": order_id,
                    "status": status,
                    "uic": event_data.get("Uic"),
                }
            )
            await self.saxo_client._dispatch_ens_event(
                {
                    "type": "order_status_change",
                    "order_id": order_id,
                    "status": status,
                    "uic": event_data.get("Uic"),
                }
            )

    async def _handle_position_event(self, event_data: Dict):
        position_id = event_data.get("PositionId")
        position_event = event_data.get("PositionEvent", "").lower()
        amount = Decimal(str(event_data.get("Amount", "0")))

        if position_event == "deleted" or amount == Decimal("0"):
            self._log(f"ENSからポジションクローズイベントを受信しました: PositionID={position_id}, Event={position_event}")
            await self.saxo_client._get_ens_event_queue().put(
                {
                    "type": "position_closed",
                    "position_id": position_id,
                    "status": "closed",
                    "uic": event_data.get("Uic"),
                    "execution_price": event_data.get("OpenPrice"),
                    "execution_time": event_data.get("ExecutionTime"),
                }
            )
            await self.saxo_client._dispatch_ens_event(
                {
                    "type": "position_closed",
                    "position_id": position_id,
                    "status": "closed",
                    "uic": event_data.get("Uic"),
                    "execution_price": event_data.get("OpenPrice"),
                    "execution_time": event_data.get("ExecutionTime"),
                }
            )
        elif position_event == "created" and amount != Decimal("0"):
            self._log(f"ENSから新規ポジションイベントを受信しました: PositionID={position_id}, Amount={amount}")

    async def _record_ping(self) -> None:
        if not self.ws:
            return
        try:
            start = time.time()
            pong_waiter = self.ws.ping()
            await asyncio.wait_for(pong_waiter, timeout=CFG.ws_ping_timeout)
            rtt = (time.time() - start) * 1000
            self.last_ping_ok_timestamp = time.time()
            self.last_ping_rtt_ms = rtt
        except Exception as e:
            self._log(f"ENS ping失敗: {e} ({type(e).__name__})")

    def _maybe_notify_stale(self, seconds_since_last: float) -> None:
        if not self._notify:
            return
        for threshold in CFG.ens_notify_thresholds:
            if seconds_since_last >= threshold and self._last_notify_seconds != threshold:
                self._last_notify_seconds = threshold
                self._notify(
                    f"⚠️ ENS無受信 {threshold}秒超過: 最終受信から{seconds_since_last:.1f}秒。"
                    f"再接続試行中={self.reconnect_task is not None and not self.reconnect_task.done()}"
                )
                break

    async def monitor_connection(self):
        self._log("ENS接続監視モニターを開始します。")
        await asyncio.sleep(5)

        while self.is_connected:
            await asyncio.sleep(CFG.ens_monitor_interval_seconds)

            time_since_last_message = time.time() - self.last_message_timestamp
            self._log(f"ENS最終受信からの経過時間: {time_since_last_message:.2f}秒")

            await self._record_ping()
            self._maybe_notify_stale(time_since_last_message)

            if time_since_last_message > CFG.ens_stale_seconds:
                self._log("警告: ENS受信が停止したとみなし、再接続を強制します。")

                if self.is_connected:
                    self.is_connected = False
                    await self._force_close_ws()
                    if self._listen_task and not self._listen_task.done():
                        self._listen_task.cancel()
                    await self.reconnect()

                break

    async def disconnect(self):
        self.shutdown_requested = True
        if self.ws:
            self._log("ENS WebSocketを切断します...")
            await self.ws.close()
            self.ws = None
            self.is_connected = False
            self._log("ENS WebSocketを切断しました。")


def normalize_currency_pair_for_api(pair_from_csv: str) -> str:
    normalized = pair_from_csv.replace("_", "/").upper()
    if "/" not in normalized and len(normalized) == 6:
        normalized = f"{normalized[:3]}/{normalized[3:]}"
    return normalized


def get_uic_for_symbol_from_map(pair_name: str, uic_map: Dict) -> Optional[Dict]:
    return uic_map.get(pair_name)


def lot_to_amount(lots: float) -> Decimal:
    return Decimal(str(lots)) * Decimal("10000")


def get_pip_value_for_pair(pair_name: str) -> Decimal:
    pair_name_upper = pair_name.upper()
    if "JPY" in pair_name_upper:
        return Decimal("0.01")
    return Decimal("0.0001")


def calculate_pips_profit(pair_name: str, entry_price: Decimal, exit_price: Decimal, trade_direction: str) -> Decimal:
    if entry_price == Decimal("0") or exit_price == Decimal("0"):
        return Decimal("0")

    price_diff = Decimal("0")
    if trade_direction.lower() == "buy":
        price_diff = exit_price - entry_price
    elif trade_direction.lower() == "sell":
        price_diff = entry_price - exit_price
    else:
        log(f"pips計算のための不明な取引方向: {trade_direction}")
        return Decimal("0")

    pip_value_unit = get_pip_value_for_pair(pair_name)

    if pip_value_unit == Decimal("0"):
        log(f"{pair_name} のpip値がゼロです。pipsを計算できません。")
        return Decimal("0")

    pips = price_diff / pip_value_unit
    return pips.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def format_price_for_display(price: Optional[Decimal], pair_name: str, uic_map: Dict) -> str:
    if price is None:
        return "-"

    pair_info = uic_map.get(pair_name)
    decimals = 5
    if pair_info:
        decimals = pair_info.get("decimals", 5 if "JPY" not in pair_name.upper() else 3)
    elif "JPY" in pair_name.upper():
        decimals = 3

    return f"{price:.{decimals}f}"


def make_external_reference(trade_id: int, kind: str) -> str:
    today = get_jst_time_str().split(" ")[0].replace("-", "")
    return f"{today}_trade_{trade_id}_{kind}_v1"


def calculate_spread_pips(pair_name: str, bid: Decimal, ask: Decimal) -> Optional[Decimal]:
    if bid == Decimal("0") or ask == Decimal("0") or bid > ask:
        log(f"スプレッド計算のための無効なbid/ask: Bid={bid}, Ask={ask} ({pair_name}用)")
        return None

    spread_value = ask - bid
    pip_value_unit = get_pip_value_for_pair(pair_name)

    if pip_value_unit == Decimal("0"):
        log(f"{pair_name} のpip値がゼロです。スプレッドpipsを計算できません。")
        return None

    spread_pips = spread_value / pip_value_unit
    return spread_pips.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


async def wait_until_time_with_random_advance(saxo_client: SaxoClient, target_time_str: str, label: str) -> bool:
    try:
        now_jst = datetime.now(TIMEZONE_TOKYO)
        target_time_obj = _parse_hhmmss(target_time_str)
        target_dt_today = datetime.combine(now_jst.date(), target_time_obj, tzinfo=TIMEZONE_TOKYO)
    except RuntimeError:
        log(f"エラー: {label} の時間形式が無効です: {target_time_str}")
        return False

    if target_dt_today < now_jst:
        log(f"{label} の時刻 {target_time_str} は既に経過しています。待機せずに即時スキップします。")
        return False

    wait_seconds = (target_dt_today - now_jst).total_seconds()
    advance_seconds = random.uniform(0, min(CFG.random_delay_sec, wait_seconds))

    final_exec_dt = target_dt_today - timedelta(seconds=advance_seconds)

    log(f"{label}: 目標時刻={target_time_str}, ゆらぎ={advance_seconds:.2f}秒, 最終実行時刻={final_exec_dt.strftime('%H:%M:%S')}")

    events = [{"time": final_exec_dt, "action": "FINAL_ACTION"}]
    now_for_ping = datetime.now(TIMEZONE_TOKYO)
    if (final_exec_dt - timedelta(seconds=30)) > now_for_ping:
        events.append({"time": final_exec_dt - timedelta(seconds=30), "action": "PING_30S"})
    if (final_exec_dt - timedelta(seconds=60)) > now_for_ping:
        events.append({"time": final_exec_dt - timedelta(seconds=60), "action": "PING_60S"})

    for event in sorted(events, key=lambda x: x["time"]):
        sleep_duration = (event["time"] - datetime.now(TIMEZONE_TOKYO)).total_seconds()
        if sleep_duration > 0:
            log(f"次のアクション '{event['action']}' まで {sleep_duration:.2f} 秒待機します...")
            await asyncio.sleep(sleep_duration)

        if event["action"].startswith("PING"):
            log(f"接続の事前確認 ({event['action']}) を行います...")
            if not await asyncio.to_thread(saxo_client.validate_token):
                log(f"エラー: 接続の事前確認に失敗しました。{label} をスキップします。")
                return False
            log(f"事前確認 ({event['action']}) 成功。")
        elif event["action"] == "FINAL_ACTION":
            log(f"{label} の実行時刻になりました。")
            break

    return True


def load_trades_from_csv(filename: str) -> List[Dict]:
    trades = []

    if not os.path.exists(filename):
        log(f"エラー: 取引ファイル '{filename}' が見つかりません。")
        send_discord(f"❌ 重要エラー: 取引ファイル '{filename}' が見つかりません。プログラムを続行できません。")
        sys.exit(1)

    try:
        weekday_map = {
            "月": 0,
            "火": 1,
            "水": 2,
            "木": 3,
            "金": 4,
            "土": 5,
            "日": 6,
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6,
        }
        today_weekday = datetime.now(TIMEZONE_TOKYO).weekday()

        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            required_keys = ["エントリー番号", "エントリー時間", "決済時間", "ロット数", "通貨ペア", "売買方向"]

            for idx, row in enumerate(reader):
                if not all(key in row and row[key] for key in required_keys):
                    log(f"CSVの {idx + 1} 行目をスキップします。必須フィールドが欠落または空です: {row}")
                    continue

                allowed_days_str = row.get("エントリー曜日") or row.get("曜日")
                if allowed_days_str:
                    allowed_days_str = allowed_days_str.strip().lower()
                    if allowed_days_str:
                        allowed_weekdays = {
                            weekday_map[day.strip()] for day in allowed_days_str.split(",") if day.strip() in weekday_map
                        }
                        if today_weekday not in allowed_weekdays:
                            log(f"取引ID {row['エントリー番号']} は本日実行対象外のためスキップします (指定曜日: {allowed_days_str})")
                            continue

                try:
                    dir_raw = str(row["売買方向"]).strip()
                    dir_norm = dir_raw.lower()
                    if dir_norm in ("long", "buy", "買"):
                        direction_api = "Buy"
                    elif dir_norm in ("short", "sell", "売"):
                        direction_api = "Sell"
                    else:
                        log(f"CSVの {idx + 1} 行目をスキップします。売買方向が不明です: {dir_raw}")
                        continue
                    trade = {
                        "id": int(row["エントリー番号"]),
                        "entry_time_str": row["エントリー時間"],
                        "exit_time_str": row["決済時間"],
                        "lot_size": float(row["ロット数"]),
                        "pair_raw": row["通貨ペア"],
                        "pair_api": normalize_currency_pair_for_api(row["通貨ペア"]),
                        "direction_raw": row["売買方向"],
                        "direction_api": direction_api,
                        "status": "Pending",
                        "entry_price": None,
                        "exit_price": None,
                        "pips_profit": Decimal("0"),
                        "position_id": None,
                        "entry_order_id": None,
                        "exit_order_id": None,
                        "entry_fill_price": None,
                        "exit_fill_price": None,
                        "entry_filled_amount": None,
                        "entry_timestamp_actual": None,
                        "exit_timestamp_actual": None,
                    }
                    trades.append(trade)
                except ValueError as ve:
                    log(f"CSVの {idx + 1} 行目をスキップします。データ変換エラー: {ve} - 行: {row}")
                except Exception as e:
                    log(f"CSVの {idx + 1} 行目処理中に予期せぬエラー: {e} - 行: {row}")

        trades.sort(key=lambda t: _parse_hhmmss(t["entry_time_str"]))

        log(f"'{filename}' から本日実行対象の {len(trades)} 件の取引を読み込み、時間順にソートしました。")

    except Exception as e:
        log(f"CSVファイル '{filename}' の読み込み中に重要エラー: {e}")
        send_discord(f"❌ 重要エラー: 取引ファイル '{filename}' の読み込みに失敗しました。プログラムを続行できません。")
        sys.exit(1)

    return trades

async def _wait_for_ens_event(
    saxo_client: SaxoClient, order_id: Optional[str], uic: int, expected_event_types: List[str], timeout_seconds: int
) -> Optional[Dict]:
    log(f"ENSイベントを監視中 (OrderID: {order_id}, UIC: {uic}, タイプ: {expected_event_types})...")

    order_id_str = str(order_id) if order_id is not None else None
    uic_int = int(uic)
    future = await saxo_client._register_ens_waiter(order_id_str, uic_int, expected_event_types)

    try:
        event = await asyncio.wait_for(future, timeout=timeout_seconds)
        log(f"★ ENSで期待するイベント({event.get('type')})を受信しました: {event}")
        return event
    except asyncio.TimeoutError:
        log(
            f"タイムアウト({timeout_seconds}秒)により、OrderID {order_id} / UIC {uic} の {expected_event_types} イベントを確認できませんでした。"
        )
        return None
    except Exception as e:
        log(f"ENSイベントの待機中にエラーが発生しました: {e}")
        return None
    finally:
        await saxo_client._unregister_ens_waiter(future)

async def confirm_flat(client: SaxoClient, uic: int, timeout_seconds: int = 60) -> bool:
    start = time.time()
    while time.time() - start < timeout_seconds:
        pos = await asyncio.to_thread(client.get_position_details_by_uic, uic)
        if not pos or pos.get("amount") == 0:
            return True
        await asyncio.sleep(1)
    return False


async def main():
    log("SAXO自動売買プログラム - 開始")
    send_discord("🚀 SAXO自動売買プログラム - 起動中")

    client = SaxoClient(CFG)

    def reauthenticate_flow_sync():
        log("致命的な認証エラー。再認証を試みます。")
        send_discord(
            "🚨 **手動での再認証が必要です！** 🚨\n\n"
            "認証トークンの自動更新に失敗しました。\n"
            "プログラムがブラウザを起動しましたので、ログインとSMS認証を完了してください。"
        )

        if not client.perform_oauth_flow():
            log("再認証にも失敗しました。プログラムを終了します。")
            send_discord("🚨🚨 **重大エラー**: 再認証に失敗しました。プログラムを停止します。")
            sys.exit(1)

        log("再認証に成功しました。処理を続行します。")
        return True

    client.set_reauthenticate_func(reauthenticate_flow_sync)

    if not client.authenticate():
        sys.exit("初期認証に失敗しました。")

    trades_from_csv = load_trades_from_csv(CFG.trades_csv_path)
    if not trades_from_csv:
        sys.exit("取引データが見つかりません。")

    all_pairs = list(set(t["pair_api"] for t in trades_from_csv))
    uic_map = client.fetch_pair_uic_map(all_pairs)
    for trade in trades_from_csv:
        pair_details = uic_map.get(trade["pair_api"])
        if pair_details:
            trade.update(pair_details)

    STATUS_FILE = "trade_status.json"

    def save_statuses(trades_data: List[Dict]):
        try:
            state_to_save = {"date": get_jst_time_str().split(" ")[0], "trades": {str(t["id"]): t for t in trades_data}}
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                json.dump(state_to_save, f, indent=2, default=str)
            log(f"取引ステータスを {STATUS_FILE} に保存しました。")
        except Exception as e:
            log(f"緊急: 状態ファイルの保存に失敗しました！: {e}")

    def load_and_reconcile_statuses(trades_data: List[Dict]):
        today_str = get_jst_time_str().split(" ")[0]
        if not os.path.exists(STATUS_FILE):
            return
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                saved_state = json.load(f)
        except Exception:
            try:
                os.remove(STATUS_FILE)
            except OSError:
                pass
            return

        if "date" not in saved_state or "trades" not in saved_state:
            try:
                os.remove(STATUS_FILE)
            except OSError:
                pass
            return

        if saved_state.get("date") == today_str:
            saved_trades = saved_state.get("trades", {})
            for trade in trades_data:
                trade_id_str = str(trade["id"])
                if trade_id_str in saved_trades:
                    saved_trade_data = saved_trades[trade_id_str]

                    for price_key in ["entry_fill_price", "exit_fill_price"]:
                        if saved_trade_data.get(price_key) is not None:
                            try:
                                saved_trade_data[price_key] = Decimal(str(saved_trade_data[price_key]))
                            except Exception as e:
                                log(
                                    "状態ロード中に価格のDecimal変換に失敗: "
                                    f"key={price_key}, value={saved_trade_data[price_key]}, error={e}"
                                )
                                saved_trade_data[price_key] = None

                    if saved_trade_data.get("pips_profit") is not None:
                        saved_trade_data["pips_profit"] = Decimal(str(saved_trade_data["pips_profit"]))

                    trade.update(saved_trade_data)
        else:
            try:
                os.remove(STATUS_FILE)
            except OSError:
                pass

    load_and_reconcile_statuses(trades_from_csv)

    ens_client = None
    token_refresh_task: Optional[asyncio.Task] = None

    try:
        ens_url = client.setup_ens_subscription()
        if ens_url:
            ens_client = SaxoENSClient(client, ens_url, client.access_token, notify_func=send_discord)
            asyncio.create_task(ens_client.connect())
            log("ENSクライアントを起動しました。")
        else:
            log("ENS初期化に失敗しました。フォールバックモードで継続します。")
    except Exception as e:
        log(f"ENS初期化エラー: {e}. ポーリングモードで継続")

    balance, currency = await asyncio.to_thread(client.get_account_balance_and_currency)
    if balance is None:
        log("警告: 起動時の口座残高取得に失敗しました。")

    async def periodic_token_refresh() -> None:
        await asyncio.sleep(CFG.token_refresh_interval_seconds)
        while True:
            try:
                refreshed = await asyncio.to_thread(client.refresh_access_token)
                if refreshed:
                    await asyncio.to_thread(client.authorize_streaming_context)
                else:
                    log("定期トークン更新に失敗しました。")
            except Exception as e:
                log(f"定期トークン更新中に予期せぬエラーが発生しました: {e}")
            await asyncio.sleep(CFG.token_refresh_interval_seconds)

    token_refresh_task = asyncio.create_task(periodic_token_refresh())

    today_str = get_jst_time_str().split(" ")[0]
    startup_msg = f"{today_str}のエントリー一覧:"

    now_time_jst_obj = datetime.now(TIMEZONE_TOKYO).time()

    for trade_def in trades_from_csv:
        status_suffix = ""
        current_status = trade_def.get("status", "Pending")
        try:
            entry_time_obj = _parse_hhmmss(trade_def["entry_time_str"])
            if current_status == "Pending" and entry_time_obj < now_time_jst_obj:
                log(f"取引ID {trade_def['id']} は起動時に時刻が経過していたため、ステータスを更新します。")
                trade_def["status"] = "スキップ (時刻経過)"

            final_status = trade_def.get("status")
            if final_status not in ["Pending", None]:
                status_suffix = f" (状態: {final_status})"
        except RuntimeError:
            status_suffix = " (時間形式エラー)"

        startup_msg += (
            f"\n{trade_def['pair_raw']} {trade_def['direction_raw']} ロット数: {trade_def['lot_size']} "
            f"エントリー時間: {trade_def['entry_time_str']} 決済時間: {trade_def['exit_time_str']}{status_suffix}"
        )

    save_statuses(trades_from_csv)

    if balance is not None and currency:
        startup_msg += f"\nFX口座残高: {balance} {currency}"
    startup_msg += f"\nストップロス: {CFG.stop_loss_pips} pips"
    startup_msg += f"\nテイクプロフィット: {CFG.take_profit_pips} pips"
    send_discord(startup_msg)

    pending_confirmation_tasks: List[asyncio.Task] = []

    async def confirm_entry_fill(trade: Dict, order_id: str, uic: int, current_bid: Decimal, current_ask: Decimal) -> None:
        trade_label = f"取引ID {trade['id']} ({trade['pair_api']} {trade['direction_api']})"
        fill_details = await _wait_for_ens_event(client, order_id, uic, ["order_fill"], CFG.fill_timeout_seconds)

        if not fill_details:
            log("ENSでの約定確認がタイムアウトしました。フォールバック機能（監査API）で確認します。")
            fill_details = await asyncio.to_thread(client.check_order_status_via_audit_api, order_id)

        if fill_details:
            log(f"✅ エントリー成功: {trade_label}")
            entry_fill_price = fill_details.get("execution_price")
            execution_time_str = fill_details.get("execution_time")
            position_id = fill_details.get("position_id")

            if not position_id:
                log("警告: 約定イベントにPositionIdが含まれていません。APIポーリングでポジションIDを取得します。")
                polled_pos_details = await asyncio.to_thread(client.get_position_details_by_order_id, order_id, uic)
                if polled_pos_details:
                    position_id = polled_pos_details.get("position_id")
                    if not entry_fill_price:
                        entry_fill_price = polled_pos_details.get("open_price")
                    if not execution_time_str:
                        exec_time_utc = datetime.fromisoformat(polled_pos_details["execution_time"].replace("Z", "+00:00"))
                        execution_time_str = exec_time_utc.astimezone(TIMEZONE_TOKYO).strftime("%Y-%m-%d %H:%M:%S")

            trade.update(
                {
                    "status": "エントリー済み",
                    "entry_fill_price": entry_fill_price,
                    "position_id": position_id,
                    "entry_timestamp_actual": execution_time_str,
                    "entry_order_id": order_id,
                    "entry_filled_amount": fill_details.get("filled_amount") if isinstance(fill_details, dict) else None,
                }
            )

            spread_at_entry = calculate_spread_pips(trade["pair_api"], current_bid, current_ask)
            entry_success_msg = (
                "エントリーしました: 通貨ペア={}, 売買方向={}, ".format(trade["pair_raw"], trade["direction_api"].upper())
                + "エントリー価格={:.{}f}, ".format(
                    entry_fill_price, uic_map.get(trade["pair_api"], {}).get("decimals", 5)
                )
                + "Bid={}, Ask={}, スプレッド={:.1f}pips, ".format(
                    current_bid, current_ask, spread_at_entry if spread_at_entry is not None else 0
                )
                + "エントリー時間={}, 決済予定時間={}".format(extract_hms_jst(execution_time_str), trade["exit_time_str"])
            )
            send_discord(entry_success_msg)
        else:
            log(f"❌ エントリー失敗 (ENS/監査API双方で確認不可): {trade_label}")
            trade["status"] = "エントリー失敗 (確認不可)"
            send_discord(
                "🚨 エントリー失敗 (ENS/監査API双方で確認不可)\n"
                f"取引: {trade_label}\n"
                f"注文ID: {order_id}\n"
                "手動でのポジション確認が必要です。"
            )

        save_statuses(trades_from_csv)

    async def confirm_exit_fill(trade: Dict, close_order_id: str) -> None:
        trade_label = f"取引ID {trade['id']} ({trade['pair_api']} {trade['direction_api']})"
        settlement_event = await _wait_for_ens_event(
            client, close_order_id, trade["uic"], ["order_fill"], CFG.fill_timeout_seconds
        )

        if not settlement_event:
            log("ENSでの決済確認がタイムアウトしました。フォールバック機能（監査API）で確認します。")
            settlement_event = await asyncio.to_thread(client.check_order_status_via_audit_api, close_order_id)

        if settlement_event:
            event_type = settlement_event.get("type")
            log(f"イベント '{event_type}' により決済を確認しました。")

            final_exit_price = settlement_event.get("execution_price")
            final_exit_time = settlement_event.get("execution_time", get_jst_time_str())

            trade.update(
                {
                    "status": "決済済み",
                    "exit_fill_price": final_exit_price,
                    "exit_timestamp_actual": final_exit_time,
                    "exit_order_id": close_order_id,
                }
            )

            is_flat = await confirm_flat(client, trade["uic"])
            if not is_flat:
                log("警告: 決済後もポジションが残っています。手動確認が必要です。")
                send_discord(f"⚠️ {trade_label} の決済後にポジションが残っています。手動確認が必要です。")

            entry_price = trade.get("entry_fill_price")
            if entry_price and final_exit_price:
                pips_profit = calculate_pips_profit(
                    trade["pair_api"], Decimal(str(entry_price)), final_exit_price, trade["direction_api"]
                )
                trade["pips_profit"] = pips_profit

                exit_time_only = extract_hms_jst(final_exit_time)
                exit_success_msg = (
                    f"予定決済しました: 通貨ペア={trade['pair_raw']}, "
                    f"売買方向={trade['direction_api'].upper()}, "
                    f"エントリー価格={format_price_for_display(entry_price, trade['pair_api'], uic_map)}, "
                    f"決済価格={format_price_for_display(final_exit_price, trade['pair_api'], uic_map)}, "
                    f"損益pips={pips_profit:.1f} "
                    f"(決済時間: {exit_time_only})"
                )
                send_discord(exit_success_msg)
            else:
                trade["status"] = "決済済み (価格不明)"
                send_discord(f"🏁 {trade_label} は決済済みですが、価格情報が取得できませんでした。")

        else:
            trade["status"] = "決済失敗 (確認不可)"
            send_discord(f"❌ {trade_label} の決済確認に失敗しました（タイムアウト）。手動確認が必要です。")

        save_statuses(trades_from_csv)

    completed_all_trades = False
    try:
        while True:
            active_trade = next(
                (
                    t
                    for t in trades_from_csv
                    if t.get("status") in ["エントリー済み", "エントリー発注済み"] and t.get("exit_order_id") is None
                ),
                None,
            )

            if active_trade:
                trade_label = f"取引ID {active_trade['id']} ({active_trade['pair_api']} {active_trade['direction_api']})"

                await wait_until_time_with_random_advance(client, active_trade["exit_time_str"], f"決済 {trade_label}")

                log(f"--- {trade_label} の決済処理開始 ---")

                current_position = await asyncio.to_thread(client.get_position_details_by_uic, active_trade["uic"])
                if not current_position:
                    log(f"ポジション {active_trade.get('position_id')} が見つかりません。既に決済済みの可能性があります。")
                    active_trade["status"] = "決済済み（事前クローズ）"
                    save_statuses(trades_from_csv)
                    continue

                amount_to_close = active_trade.get("entry_filled_amount")
                if amount_to_close is None:
                    amount_to_close = current_position.get("amount")
                if amount_to_close is None:
                    amount_to_close = lot_to_amount(active_trade["lot_size"])

                await asyncio.to_thread(client.cancel_related_orders_for_uic, active_trade["uic"])

                close_order_id = None
                for close_attempt in range(2):
                    close_order_id = await asyncio.to_thread(
                        client.close_position_market,
                        current_position["position_id"],
                        active_trade["pair_api"],
                        active_trade["uic"],
                        active_trade.get("asset_type", "FxSpot"),
                        amount_to_close,
                        active_trade["direction_api"],
                        make_external_reference(active_trade["id"], "exit"),
                    )
                    if close_order_id:
                        break
                    remaining_position = await asyncio.to_thread(client.get_position_details_by_uic, active_trade["uic"])
                    if not remaining_position or remaining_position.get("amount") == 0:
                        log(f"{trade_label} の決済失敗後、ポジションが存在しないため再試行しません。")
                        break
                    if close_attempt == 0:
                        log(f"{trade_label} の決済再試行を実行します（ポジション保持を確認）。")

                if close_order_id:
                    log(f"決済注文が受付されました。OrderID: {close_order_id}")
                    active_trade["exit_order_id"] = close_order_id
                    active_trade["status"] = "決済発注済み"
                    save_statuses(trades_from_csv)
                    task = asyncio.create_task(confirm_exit_fill(active_trade, close_order_id))
                    pending_confirmation_tasks.append(task)
                else:
                    active_trade["status"] = "決済失敗 (注文エラー)"
                    save_statuses(trades_from_csv)

            else:
                next_trade = next((t for t in trades_from_csv if t.get("status", "Pending") == "Pending"), None)
                if next_trade:
                    trade_label = f"取引ID {next_trade['id']} ({next_trade['pair_api']} {next_trade['direction_api']})"
                    if not await wait_until_time_with_random_advance(client, next_trade["entry_time_str"], f"エントリー {trade_label}"):
                        entry_dt = datetime.combine(
                            datetime.now(TIMEZONE_TOKYO).date(), _parse_hhmmss(next_trade["entry_time_str"]), tzinfo=TIMEZONE_TOKYO
                        )
                        if entry_dt < datetime.now(TIMEZONE_TOKYO):
                            log(f"{trade_label} のエントリー時刻は経過しました。スキップします。")
                            next_trade["status"] = "スキップ (時刻経過)"
                            save_statuses(trades_from_csv)
                            continue

                    log(f"--- {trade_label} のエントリー処理開始 ---")

                    if "uic" not in next_trade:
                        log(f"{next_trade['pair_api']} のUIC情報がありません。スキップします。")
                        next_trade["status"] = "スキップ (UICなし)"
                        save_statuses(trades_from_csv)
                        continue

                    uic = int(next_trade["uic"])
                    asset_type = next_trade.get("asset_type", "FxSpot")

                    price_infos_map = await asyncio.to_thread(client.fetch_price_infos, uic_list=[uic])
                    price_info = price_infos_map.get(uic)

                    if price_info and "Quote" in price_info and price_info["Quote"].get("Bid") and price_info["Quote"].get("Ask"):
                        current_bid = Decimal(str(price_info["Quote"]["Bid"]))
                        current_ask = Decimal(str(price_info["Quote"]["Ask"]))
                        current_mid_price = (current_bid + current_ask) / Decimal("2")

                        if CFG.spread_pips_limit > 0:
                            spread_pips = calculate_spread_pips(next_trade["pair_api"], current_bid, current_ask)
                            if spread_pips is None or spread_pips > Decimal(str(CFG.spread_pips_limit)):
                                log(f"スプレッドが上限({CFG.spread_pips_limit}pips)を超えました({spread_pips}pips)。スキップします。")
                                next_trade["status"] = "スキップ (スプレッド上限)"
                                send_discord(
                                    f"⚠️ {next_trade['pair_api']}はスプレッドが広いためスキップしました: {spread_pips} pips"
                                )
                                save_statuses(trades_from_csv)
                                continue

                        entry_dt = datetime.combine(
                            datetime.now(TIMEZONE_TOKYO).date(),
                            _parse_hhmmss(next_trade["entry_time_str"]),
                            tzinfo=TIMEZONE_TOKYO,
                        )
                        retry_deadline = entry_dt + timedelta(seconds=3)
                        order_result = None
                        for attempt in range(2):
                            if datetime.now(TIMEZONE_TOKYO) > retry_deadline:
                                break
                            order_result = await asyncio.to_thread(
                                client.place_order,
                                pair_name=next_trade["pair_api"],
                                uic=uic,
                                asset_type=asset_type,
                                side=next_trade["direction_api"],
                                amount=lot_to_amount(next_trade["lot_size"]),
                                current_price_for_sl_tp=current_mid_price,
                                external_reference=make_external_reference(next_trade["id"], "entry"),
                            )
                            if order_result and order_result.get("order_id"):
                                break
                            if order_result and order_result.get("status") == "unknown":
                                break
                            if attempt == 0 and datetime.now(TIMEZONE_TOKYO) <= retry_deadline:
                                log(f"{trade_label} のエントリー再試行を2秒後に実行します。")
                                await asyncio.sleep(2)
                        if order_result and order_result.get("order_id"):
                            next_trade["entry_order_id"] = order_result["order_id"]
                            next_trade["status"] = "エントリー発注済み"
                            save_statuses(trades_from_csv)
                            task = asyncio.create_task(
                                confirm_entry_fill(next_trade, order_result["order_id"], uic, current_bid, current_ask)
                            )
                            pending_confirmation_tasks.append(task)

                        elif order_result and order_result.get("status") == "unknown":
                            log(f"❌ 注文の成否が不明なため停止: {trade_label}")
                            next_trade["status"] = "エントリー失敗 (不明状態)"
                            send_discord(
                                "🚨 注文の成否が不明なため自動処理を停止します。\n"
                                f"取引: {trade_label}\n"
                                f"ExternalReference: {order_result.get('external_reference')}\n"
                                "手動での注文/ポジション確認が必要です。"
                            )
                            save_statuses(trades_from_csv)
                            break

                        else:
                            if datetime.now(TIMEZONE_TOKYO) > retry_deadline:
                                log(f"❌ エントリー失敗: {trade_label}（再発注猶予3秒を超過）")
                                next_trade["status"] = "エントリー失敗 (時間超過)"
                            else:
                                log(f"❌ エントリー失敗: {trade_label}")
                                next_trade["status"] = "エントリー失敗"

                    save_statuses(trades_from_csv)
                else:
                    if not any(t.get("status") in ["エントリー済み", "エントリー発注済み", "決済発注済み"] for t in trades_from_csv):
                        log("本日の全取引が終了しました。")
                        break

            await asyncio.sleep(1)

        if pending_confirmation_tasks:
            await asyncio.gather(*pending_confirmation_tasks, return_exceptions=True)

        log("CSV内の全取引を処理しました。サマリーを生成中...")
        final_balance, final_currency = await asyncio.to_thread(client.get_account_balance_and_currency)
        summary_msg = f"{today_str} の取引結果\n\n"
        summary_msg += "|通貨ペア | 売買方向 | エントリー価格 | 決済価格 | 損益pips |\n"
        summary_msg += "|---|---|---|---|---|\n"

        total_pips_profit = Decimal("0")
        for trade_result in trades_from_csv:
            if trade_result.get("status") in ["決済済み", "決済済み (価格不明)"]:
                pips = Decimal(str(trade_result.get("pips_profit", "0")))
                total_pips_profit += pips
                summary_msg += "| {} | {} | {} | {} | {:.1f} |\n".format(
                    trade_result["pair_raw"],
                    trade_result["direction_api"],
                    format_price_for_display(trade_result.get("entry_fill_price"), trade_result["pair_api"], uic_map),
                    format_price_for_display(trade_result.get("exit_fill_price"), trade_result["pair_api"], uic_map),
                    pips,
                )
        summary_msg += "\n合計損益pips: {:.1f}\n".format(total_pips_profit)
        if final_balance is not None and final_currency:
            summary_msg += f"FX口座残高: {final_balance} {final_currency}"
        send_discord(summary_msg)

        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)
            log(f"日次サマリー送信後、{STATUS_FILE} を削除しました。")
        completed_all_trades = True

    except KeyboardInterrupt:
        log("プログラムが手動で中断されました。")
    finally:
        log("クリーンアップ処理を行います。")

        if "trades_from_csv" in locals() and not completed_all_trades:
            save_statuses(trades_from_csv)
        cleanup_edge_user_data_dir()
        if token_refresh_task:
            token_refresh_task.cancel()
        if client:
            await asyncio.to_thread(client.delete_tokens_and_keys)
        if ens_client:
            await ens_client.disconnect()
        send_discord("🛑 SAXO自動売買プログラム - シャットダウン")

    log("プログラムを正常に終了しました。")


if __name__ == "__main__":
    asyncio.run(main())
