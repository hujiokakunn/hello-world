[2026-01-09 21:55:02] エントリー 取引ID 59 (USD/JPY Sell): 目標時刻=21:56:00, ゆらぎ=1.05秒, 最終実行時刻=21:55:58
[2026-01-09 21:55:02] 次のアクション 'PING_30S' まで 26.67 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 21:55:28] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 21:55:28] 現在のアクセストークンを検証しています...
[2026-01-09 21:55:29] トークン検証成功。
[2026-01-09 21:55:29] 事前確認 (PING_30S) 成功。
[2026-01-09 21:55:29] 次のアクション 'FINAL_ACTION' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 21:55:58] エントリー 取引ID 59 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 21:55:58] --- 取引ID 59 (USD/JPY Sell) のエントリー処理開始 ---
[2026-01-09 21:55:58] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat,PriceInfo
[2026-01-09 21:55:59] エントリー処理開始 (UIC: 42, Side: Sell, Amount: 50000.0)...
[2026-01-09 21:55:59] UIC 42 の既存取引（ポジション/Working注文）を確認中...
[2026-01-09 21:55:59] UIC 42 の既存取引は見つかりませんでした。
[2026-01-09 21:55:59] 既存取引がないため、新規注文を発注します...
[2026-01-09 21:55:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat
[2026-01-09 21:56:00] 関連注文を確認: 1件
[2026-01-09 21:56:00] ✅ SL注文が成立: OrderId=5036796924, Type=None
[2026-01-09 21:56:00]   関連注文1: OrderId=5036796924, Status=None, Type=None
[2026-01-09 21:56:00] Market + SL 注文送信完了: OrderId=5036796923
[2026-01-09 21:56:00] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 21:56:00] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 21:56:00] ENSイベントを監視中 (OrderID: 5036796923, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T12:56:00.248914Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2b2240fc-c9f6-4380-8dad-c0fd9805317e', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_59_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796923', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'RelatedOrderId': ['5036796924'], 'RelatedOrderIds': ['5036796924'], 'SequenceId': '272087375', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T12:56:00.249912Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2b2240fc-c9f6-4380-8dad-c0fd9805317e', 'Duration': {'DurationType': 'GoodTillCancel'}, 'ExternalReference': '20260109_trade_59_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796924', 'OrderRelation': 'IfDoneSlave', 'OrderType': 'Stop', 'Price': 157.71, 'RelatedOrderId': ['5036796923'], 'RelatedOrderIds': ['5036796923'], 'SequenceId': '272087376', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T12:56:00.254912Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.66, 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2b2240fc-c9f6-4380-8dad-c0fd9805317e', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.66, 'ExternalReference': '20260109_trade_59_entry_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796923', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'PositionId': '5025288222', 'RelatedOrderId': ['5036796924'], 'RelatedOrderIds': ['5036796924'], 'SequenceId': '272087377', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}
✨ ENSから注文完全約定イベント: OrderID=5036796923, Price=157.66
[2026-01-09 21:56:00] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036796923', 'execution_price': Decimal('157.66'), 'execution_time': '2026-01-09T12:56:00.254912Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288222'}
[2026-01-09 21:56:00] ✅ エントリー成功: 取引ID 59 (USD/JPY Sell)
[2026-01-09 21:56:01] Discord通知を送信しました。ステータス: 204
[2026-01-09 21:56:01] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 21:56:01] 決済 取引ID 59 (USD/JPY Sell): 目標時刻=22:06:00, ゆらぎ=0.02秒, 最終実行時刻=22:05:59
[2026-01-09 21:56:01] 次のアクション 'PING_60S' まで 538.32 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 21:56:59] アクセストークンを更新しています...
[2026-01-09 21:57:00] アクセストークンを正常に更新しました。
[2026-01-09 21:57:00] ストリーミング再認可を実行します: contextId=ctx-7962337698-r3z7held
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 21:57:01] ストリーミング再認可が未対応のため無効化します: /streamingws/authorize
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS WebSocket接続が閉じられました。
ENS接続断の詳細: reason=ConnectionClosed, exception=ConnectionClosedError, close_code=1006, close_reason=, last_message_at=2026-01-09 21:58:41, last_message_id=68, last_ping_ok_at=2026-01-09 21:58:46, last_ping_rtt_ms=0.3
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=False, contextId=ctx-7962337698-r3z7held, messageid=68
[2026-01-09 21:58:55] アクセストークンを更新しています...
ENS ping失敗: no close frame received or sent (ConnectionClosedError)
[2026-01-09 21:58:56] アクセストークンを正常に更新しました。
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7962337698-r3z7held&authorization=***&messageid=68
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: _resetsubscriptions 対象。再接続します。
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=True, contextId=ctx-7962337698-r3z7held, messageid=0
[2026-01-09 21:58:58] アクセストークンを更新しています...
[2026-01-09 21:58:59] アクセストークンを正常に更新しました。
ENSサブスクリプションを再作成します...
[2026-01-09 21:58:59] ENSサブスクリプションを作成中...
[2026-01-09 21:58:59] ストリーミング用ContextId生成: ctx-7963539681-1sm4s2lt
[2026-01-09 21:58:59] ENS WebSocket URL: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7963539681-1sm4s2lt&authorization=***
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7963539681-1sm4s2lt&authorization=***
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:04:59] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:05:00] 現在のアクセストークンを検証しています...
[2026-01-09 22:05:00] トークン検証成功。
[2026-01-09 22:05:00] 事前確認 (PING_60S) 成功。
[2026-01-09 22:05:00] 次のアクション 'PING_30S' まで 29.67 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:05:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:05:29] 現在のアクセストークンを検証しています...
[2026-01-09 22:05:30] トークン検証成功。
[2026-01-09 22:05:30] 事前確認 (PING_30S) 成功。
[2026-01-09 22:05:30] 次のアクション 'FINAL_ACTION' まで 29.71 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:05:59] 決済 取引ID 59 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 22:06:00] --- 取引ID 59 (USD/JPY Sell) の決済処理開始 ---
[2026-01-09 22:06:00] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:06:00] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:06:00] UIC 42 のSL候補注文はありません。追跡IDがないため全Working注文をキャンセルします。
[2026-01-09 22:06:00] 注文キャンセルを実行しました: OrderId=5036796924
[2026-01-09 22:06:00] ポジション 5025288222 (USD/JPY) の決済処理開始...
[2026-01-09 22:06:00] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:06:01] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:06:01] 決済注文データ: Buy 50000.0 units of UIC 42
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:06:00.740204Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2b2240fc-c9f6-4380-8dad-c0fd9805317e', 'Duration': {'DurationType': 'GoodTillCancel'}, 'ExternalReference': '20260109_trade_59_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796924', 'OrderRelation': 'StandAlone', 'OrderType': 'Stop', 'Price': 157.71, 'SequenceId': '272087553', 'Status': 'Cancelled', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
🧹 SL注文がキャンセル: OrderID=5036796924, Status=cancelled
ENSから注文ステータス変更イベント: OrderID=5036796924, Status=cancelled
[2026-01-09 22:06:01] USD/JPY の決済注文が受付されました。OrderId: 5036796940
[2026-01-09 22:06:01] 決済注文が受付されました。OrderID: 5036796940
[2026-01-09 22:06:01] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:06:01] ENSイベントを監視中 (OrderID: 5036796940, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:06:01.345392Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '25d432b6-1fab-4a12-b7a6-44757fc264a6', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_59_exit_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796940', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272087555', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:06:01.350392Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.615, 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '25d432b6-1fab-4a12-b7a6-44757fc264a6', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.615, 'ExternalReference': '20260109_trade_59_exit_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036796940', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288272', 'SequenceId': '272087556', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}     
✨ ENSから注文完全約定イベント: OrderID=5036796940, Price=157.615
[2026-01-09 22:06:02] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036796940', 'execution_price': Decimal('157.615'), 'execution_time': '2026-01-09T13:06:01.350392Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288272'}
[2026-01-09 22:06:02] イベント 'order_fill' により決済を確認しました。
[2026-01-09 22:06:02] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:06:02] 本日の全取引が終了しました。
[2026-01-09 22:06:02] ClosedPositionsに該当がなくても保有ポジションなしと判定: UIC=42
[2026-01-09 22:06:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:06:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:06:03] CSV内の全取引を処理しました。サマリーを生成中...
[2026-01-09 22:06:03] 口座残高を取得しています...
[2026-01-09 22:06:03] 口座残高: 1007295.16 EUR
[2026-01-09 22:06:04] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:06:04] 日次サマリー送信後、trade_status.json を削除しました。
[2026-01-09 22:06:04] クリーンアップ処理を行います。
[2026-01-09 22:06:04] クライアントからトークンとアカウント/クライアントキーをクリアしました。
ENS WebSocketを切断します...
ENS WebSocket接続が閉じられました。
ENS接続断の詳細: reason=ConnectionClosed, exception=ConnectionClosedOK, close_code=1000, close_reason=, last_message_at=2026-01-09 22:06:02, last_message_id=23, last_ping_ok_at=2026-01-09 22:05:56, last_ping_rtt_ms=0.5
ENS WebSocketを切断しました。
[2026-01-09 22:06:05] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:06:05] プログラムを正常に終了しました。
ENS monitor task cancelled
PS C:\Users\admin\OneDrive\ドキュメント\アノマリーFX\SAXO\自分用Saxo\saxo_bot> python -u "c:\Users\admin\OneDrive\ドキュメント\アノマリーFX\SAXO\自分用Saxo\saxo_bot\07_saxo_bot_07.py"
[2026-01-09 22:07:36] SAXO自動売買プログラム - 開始
[2026-01-09 22:07:37] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:07:37] [ENV] SIM selected. API_BASE=https://gateway.saxobank.com/sim/openapi AUTH=https://sim.logonvalidation.net/authorize TOKEN=https://sim.logonvalidation.net/token STREAMING=wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws CLIENT_ID=****************************86a0
[2026-01-09 22:07:37] OAuth認証フローを開始します...
[2026-01-09 22:07:37] 指定されたパス C:\fx\saxo\msedgedriver.exe でのEdgeDriver起動に失敗: Message: Unable to obtain driver for MicrosoftEdge; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location
。デフォルトパスを試します。

DevTools listening on ws://127.0.0.1:62956/devtools/browser/30078bb7-8c0b-41eb-9f9e-71852c17b4fe
[2026-01-09 22:07:39] Edge WebDriverが正常に作成されました。
[2026-01-09 22:07:39] 認証URLに移動します: https://sim.logonvalidation.net/authorize?response_type=code&client_id=%2A%2A%2A%2A%2A&redirect_uri=%2A%2A%2A%2A%2A&code_challenge=%2A%2A%2A%2A%2A&code_challenge_method=S256&scope=openid+TradeAccess+ReadTrading+ReadAccount&state=%2A%2A%2A%2A%2A
[8148:10892:0109/220740.184:ERROR:chrome\browser\task_manager\providers\fallback_task_provider.cc:126] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
[2026-01-09 22:07:41] ブラウザ経由でログインしてください。必要に応じてSMSコードを待機します (最大5分)。
[2026-01-09 22:07:41] ログイン情報を送信しました。リダイレクトを待機中: http://localhost:8083/saxo_sim
[8148:10892:0109/220741.696:ERROR:chrome\browser\task_manager\providers\fallback_task_provider.cc:126] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
[2026-01-09 22:07:57] リダイレクト先: http://localhost:8083/saxo_sim?code=%2A%2A%2A%2A%2A&state=%2A%2A%2A%2A%2A#/lst/1767964074284
[2026-01-09 22:07:57] 認証コードを取得しました。
[2026-01-09 22:08:00] 一時ディレクトリ C:\fx\saxo\edge_user_data_1767964057_1eb3865d を削除しました。
[2026-01-09 22:08:00] 認証コードをトークンに交換しています...
[2026-01-09 22:08:01] アクセストークンを正常に取得しました。
[2026-01-09 22:08:01] アカウントキーを取得しています...
[2026-01-09 22:08:02] FX AccountKey: ********************6Q==, ClientKey: ********************6Q== を AccountId: 21294788 用に選択しました。
[2026-01-09 22:08:02] 取引ID 0 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 1 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 2 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 3 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 4 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 5 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 6 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 7 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 8 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 9 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 10 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 11 は本日実行対象外のためスキップします (指定曜日: mon)
[2026-01-09 22:08:02] 取引ID 12 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 13 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 14 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 15 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 16 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 17 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 18 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 19 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 20 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 21 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 22 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 23 は本日実行対象外のためスキップします (指定曜日: tue)
[2026-01-09 22:08:02] 取引ID 24 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 25 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 26 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 27 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 28 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 29 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 30 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 31 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 32 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 33 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 34 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 35 は本日実行対象外のためスキップします (指定曜日: wed)
[2026-01-09 22:08:02] 取引ID 36 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 37 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 38 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 39 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 40 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 41 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 42 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 43 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 44 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 45 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 46 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 取引ID 47 は本日実行対象外のためスキップします (指定曜日: thu)
[2026-01-09 22:08:02] 'saxo_trades.csv' から本日実行対象の 12 件の取引を読み込み、時間順にソートしました。
[2026-01-09 22:08:02] 通貨ペアのUICマップを取得しています...
[2026-01-09 22:08:02] UICをマッピングしました: USD/JPY -> 42 (小数点以下桁数: 5)
[2026-01-09 22:08:02] ENSサブスクリプションを作成中...
[2026-01-09 22:08:02] ストリーミング用ContextId生成: ctx-7964082574-jt7up1ui
[2026-01-09 22:08:02] ENS WebSocket URL: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7964082574-jt7up1ui&authorization=***
[2026-01-09 22:08:02] ENSクライアントを起動しました。
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7964082574-jt7up1ui&authorization=***        
[2026-01-09 22:08:02] 口座残高を取得しています...
[2026-01-09 22:08:03] 口座残高: 1007295.16 EUR
[2026-01-09 22:08:03] 取引ID 48 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 49 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 50 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 51 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 52 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 53 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ID 54 は起動時に時刻が経過していたため、ステータスを更新します。
[2026-01-09 22:08:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:08:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:08:03] エントリー 取引ID 55 (USD/JPY Buy): 目標時刻=22:10:00, ゆらぎ=0.78秒, 最終実行時刻=22:09:59
[2026-01-09 22:08:03] 次のアクション 'PING_60S' まで 55.25 秒待機します...
ENS WebSocket接続成功
ENS接続監視モニターを開始します。
⚠️ ENS無受信 10秒超過: 最終受信から15.0秒。再接続試行中=False
[2026-01-09 22:08:20] Discord通知を送信しました。ステータス: 204
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:08:59] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:08:59] 現在のアクセストークンを検証しています...
[2026-01-09 22:08:59] トークン検証成功。
[2026-01-09 22:08:59] 事前確認 (PING_60S) 成功。
[2026-01-09 22:08:59] 次のアクション 'PING_30S' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:09:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:09:29] 現在のアクセストークンを検証しています...
[2026-01-09 22:09:29] トークン検証成功。
[2026-01-09 22:09:29] 事前確認 (PING_30S) 成功。
[2026-01-09 22:09:29] 次のアクション 'FINAL_ACTION' まで 29.68 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:09:59] エントリー 取引ID 55 (USD/JPY Buy) の実行時刻になりました。
[2026-01-09 22:09:59] --- 取引ID 55 (USD/JPY Buy) のエントリー処理開始 ---
[2026-01-09 22:09:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat,PriceInfo
[2026-01-09 22:09:59] エントリー処理開始 (UIC: 42, Side: Buy, Amount: 50000.0)...
[2026-01-09 22:09:59] UIC 42 の既存取引（ポジション/Working注文）を確認中...
[2026-01-09 22:10:00] UIC 42 の既存取引は見つかりませんでした。
[2026-01-09 22:10:00] 既存取引がないため、新規注文を発注します...
[2026-01-09 22:10:00] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat
[2026-01-09 22:10:00] リクエスト例外 (/trade/v2/orders): 400 Client Error: Bad Request for url: https://gateway.saxobank.com/sim/openapi/trade/v2/orders - 試行 1/1
[2026-01-09 22:10:00] エラーレスポンス詳細 (/trade/v2/orders): {"ErrorInfo":{"ErrorCode":"OrderNotPlaced","Message":"Order not placed as other order in request was rejected."},"ExternalReference":"20260109_trade_55_entry_v1","Orders":[{"ErrorInfo":{"ErrorCode":"WrongSideOfRelatedOrder","Message":"The order price is on the wrong side of the related order. Please
[2026-01-09 22:10:00] 1回の再試行後もRequestException: /trade/v2/orders
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:10:00.536990Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'da0f34e8-7b86-4935-91d8-c6ebd00bced2', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_55_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797006', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'RelatedOrderId': ['5036797007'], 'RelatedOrderIds': ['5036797007'], 'SequenceId': '272087621', 'Status': 'Placed', 'SubStatus': 'Rejected', 'Symbol': 'USDJPY', 'Uic': 42}
[2026-01-09 22:10:01] 注文応答に OrderId がありません: None
[2026-01-09 22:10:01] SL付き注文に失敗したため通常注文へフォールバックします: OrderId が取得できませんでした。
[2026-01-09 22:10:02] 注文受付成功: OrderID 5036797008
[2026-01-09 22:10:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:10:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:10:02] ENSイベントを監視中 (OrderID: 5036797008, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:10:02.050694Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '4c1fccf1-1d89-4cb0-9df7-626fc5588e3e', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_55_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797008', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272087628', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:10:02.055694Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.635, 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '4c1fccf1-1d89-4cb0-9df7-626fc5588e3e', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.635, 'ExternalReference': '20260109_trade_55_entry_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797008', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288398', 'SequenceId': '272087629', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}    
✨ ENSから注文完全約定イベント: OrderID=5036797008, Price=157.635
[2026-01-09 22:10:02] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797008', 'execution_price': Decimal('157.635'), 'execution_time': '2026-01-09T13:10:02.055694Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288398'}
[2026-01-09 22:10:02] ✅ エントリー成功: 取引ID 55 (USD/JPY Buy)
[2026-01-09 22:10:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:10:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:10:03] 決済 取引ID 55 (USD/JPY Buy): 目標時刻=22:20:58, ゆらぎ=2.14秒, 最終実行時刻=22:20:55
[2026-01-09 22:10:03] 次のアクション 'PING_60S' まで 592.44 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:19:55] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:19:55] 現在のアクセストークンを検証しています...
[2026-01-09 22:19:56] トークン検証成功。
[2026-01-09 22:19:56] 事前確認 (PING_60S) 成功。
[2026-01-09 22:19:56] 次のアクション 'PING_30S' まで 28.93 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:20:25] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:20:25] 現在のアクセストークンを検証しています...
[2026-01-09 22:20:26] トークン検証成功。
[2026-01-09 22:20:26] 事前確認 (PING_30S) 成功。
[2026-01-09 22:20:26] 次のアクション 'FINAL_ACTION' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:20:55] 決済 取引ID 55 (USD/JPY Buy) の実行時刻になりました。
[2026-01-09 22:20:55] --- 取引ID 55 (USD/JPY Buy) の決済処理開始 ---
[2026-01-09 22:20:55] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:20:56] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:20:56] UIC 42 のキャンセル対象注文はありません。
[2026-01-09 22:20:56] ポジション 5025288398 (USD/JPY) の決済処理開始...
[2026-01-09 22:20:56] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:20:56] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:20:56] 決済注文データ: Sell 50000.0 units of UIC 42
[2026-01-09 22:20:57] USD/JPY の決済注文が受付されました。OrderId: 5036797049
[2026-01-09 22:20:57] 決済注文が受付されました。OrderID: 5036797049
[2026-01-09 22:20:57] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:20:57] ENSイベントを監視中 (OrderID: 5036797049, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:20:56.920706Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'de4c13a1-ea06-440e-a5ea-2e1ae0725844', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_55_exit_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797049', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272087904', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:20:56.925707Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.552, 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'de4c13a1-ea06-440e-a5ea-2e1ae0725844', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.552, 'ExternalReference': '20260109_trade_55_exit_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797049', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288468', 'SequenceId': '272087905', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}    
✨ ENSから注文完全約定イベント: OrderID=5036797049, Price=157.552
[2026-01-09 22:20:57] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797049', 'execution_price': Decimal('157.552'), 'execution_time': '2026-01-09T13:20:56.925707Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288468'}
[2026-01-09 22:20:57] イベント 'order_fill' により決済を確認しました。
[2026-01-09 22:20:57] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:20:58] ClosedPositionsに該当がなくても保有ポジションなしと判定: UIC=42
[2026-01-09 22:20:59] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:20:59] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:20:59] エントリー 取引ID 56 (USD/JPY Sell): 目標時刻=22:21:02, ゆらぎ=2.93秒, 最終実行時刻=22:20:59
[2026-01-09 22:20:59] 次のアクション 'FINAL_ACTION' まで 0.02 秒待機します...
[2026-01-09 22:20:59] エントリー 取引ID 56 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 22:20:59] --- 取引ID 56 (USD/JPY Sell) のエントリー処理開始 ---
[2026-01-09 22:20:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat,PriceInfo
[2026-01-09 22:20:59] エントリー処理開始 (UIC: 42, Side: Sell, Amount: 50000.0)...
[2026-01-09 22:20:59] UIC 42 の既存取引（ポジション/Working注文）を確認中...
[2026-01-09 22:20:59] UIC 42 の既存取引は見つかりませんでした。
[2026-01-09 22:20:59] 既存取引がないため、新規注文を発注します...
[2026-01-09 22:20:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat
[2026-01-09 22:21:00] リクエスト例外 (/trade/v2/orders): 400 Client Error: Bad Request for url: https://gateway.saxobank.com/sim/openapi/trade/v2/orders - 試行 1/1
[2026-01-09 22:21:00] エラーレスポンス詳細 (/trade/v2/orders): {"ErrorInfo":{"ErrorCode":"OrderNotPlaced","Message":"Order not placed as other order in request was rejected."},"ExternalReference":"20260109_trade_56_entry_v1","Orders":[{"ErrorInfo":{"ErrorCode":"WrongSideOfRelatedOrder","Message":"The order price is on the wrong side of the related order. Please
[2026-01-09 22:21:00] 1回の再試行後もRequestException: /trade/v2/orders
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:21:00.406234Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '6d47b0af-0a68-4cf4-be17-6c940648b71c', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_56_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797050', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'RelatedOrderId': ['5036797051'], 'RelatedOrderIds': ['5036797051'], 'SequenceId': '272087907', 'Status': 'Placed', 'SubStatus': 'Rejected', 'Symbol': 'USDJPY', 'Uic': 42}
[2026-01-09 22:21:01] 注文応答に OrderId がありません: None
[2026-01-09 22:21:01] SL付き注文に失敗したため通常注文へフォールバックします: OrderId が取得できませんでした。
[2026-01-09 22:21:02] 注文受付成功: OrderID 5036797052
[2026-01-09 22:21:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:21:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:21:02] ENSイベントを監視中 (OrderID: 5036797052, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:21:01.796424Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '56433e11-e5f5-47dc-b1c5-6a5746137221', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_56_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797052', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272087909', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:21:01.801813Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.553, 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '56433e11-e5f5-47dc-b1c5-6a5746137221', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.553, 'ExternalReference': '20260109_trade_56_entry_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797052', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288470', 'SequenceId': '272087910', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}   
✨ ENSから注文完全約定イベント: OrderID=5036797052, Price=157.553
[2026-01-09 22:21:02] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797052', 'execution_price': Decimal('157.553'), 'execution_time': '2026-01-09T13:21:01.801813Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288470'}
[2026-01-09 22:21:02] ✅ エントリー成功: 取引ID 56 (USD/JPY Sell)
[2026-01-09 22:21:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:21:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:21:03] 決済 取引ID 56 (USD/JPY Sell): 目標時刻=22:31:00, ゆらぎ=1.11秒, 最終実行時刻=22:30:58
[2026-01-09 22:21:03] 次のアクション 'PING_60S' まで 535.71 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:26:03] アクセストークンを更新しています...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:26:04] アクセストークンを正常に更新しました。
[2026-01-09 22:26:04] ストリーミング再認可を実行します: contextId=ctx-7964082574-jt7up1ui
[2026-01-09 22:26:06] ストリーミング再認可が未対応のため無効化します: /streamingws/authorize
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS WebSocket接続が閉じられました。
ENS接続断の詳細: reason=ConnectionClosed, exception=ConnectionClosedError, close_code=1006, close_reason=, last_message_at=2026-01-09 22:27:45, last_message_id=67, last_ping_ok_at=2026-01-09 22:28:01, last_ping_rtt_ms=1.1
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=False, contextId=ctx-7964082574-jt7up1ui, messageid=67
[2026-01-09 22:28:06] アクセストークンを更新しています...
[2026-01-09 22:28:07] アクセストークンを正常に更新しました。
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7964082574-jt7up1ui&authorization=***&messageid=67
ENS monitor task cancelled
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: _resetsubscriptions 対象。再接続します。
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=True, contextId=ctx-7964082574-jt7up1ui, messageid=0
[2026-01-09 22:28:09] アクセストークンを更新しています...
[2026-01-09 22:28:10] アクセストークンを正常に更新しました。
ENSサブスクリプションを再作成します...
[2026-01-09 22:28:10] ENSサブスクリプションを作成中...
[2026-01-09 22:28:10] ストリーミング用ContextId生成: ctx-7965290393-hsdu6wsb
[2026-01-09 22:28:10] ENS WebSocket URL: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7965290393-hsdu6wsb&authorization=***
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7965290393-hsdu6wsb&authorization=***
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:29:58] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:29:58] 現在のアクセストークンを検証しています...
[2026-01-09 22:29:59] トークン検証成功。
[2026-01-09 22:29:59] 事前確認 (PING_60S) 成功。
[2026-01-09 22:29:59] 次のアクション 'PING_30S' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:30:28] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:30:28] 現在のアクセストークンを検証しています...
[2026-01-09 22:30:29] トークン検証成功。
[2026-01-09 22:30:29] 事前確認 (PING_30S) 成功。
[2026-01-09 22:30:29] 次のアクション 'FINAL_ACTION' まで 29.69 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:30:58] 決済 取引ID 56 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 22:30:58] --- 取引ID 56 (USD/JPY Sell) の決済処理開始 ---
[2026-01-09 22:30:58] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:30:59] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:30:59] UIC 42 のキャンセル対象注文はありません。
[2026-01-09 22:30:59] ポジション 5025288470 (USD/JPY) の決済処理開始...
[2026-01-09 22:30:59] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:30:59] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:30:59] 決済注文データ: Buy 50000.0 units of UIC 42
[2026-01-09 22:31:00] USD/JPY の決済注文が受付されました。OrderId: 5036797186
[2026-01-09 22:31:00] 決済注文が受付されました。OrderID: 5036797186
[2026-01-09 22:31:00] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:31:00] ENSイベントを監視中 (OrderID: 5036797186, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:30:59.941442Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2cc55da0-bf83-47ed-96ee-c0a10bd6ff1d', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_56_exit_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797186', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272088358', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:30:59.946442Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.662, 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '2cc55da0-bf83-47ed-96ee-c0a10bd6ff1d', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.662, 'ExternalReference': '20260109_trade_56_exit_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797186', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288616', 'SequenceId': '272088359', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}     
✨ ENSから注文完全約定イベント: OrderID=5036797186, Price=157.662
[2026-01-09 22:31:00] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797186', 'execution_price': Decimal('157.662'), 'execution_time': '2026-01-09T13:30:59.946442Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288616'}
[2026-01-09 22:31:00] イベント 'order_fill' により決済を確認しました。
[2026-01-09 22:31:00] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:31:01] ClosedPositionsに該当がなくても保有ポジションなしと判定: UIC=42
[2026-01-09 22:31:01] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:31:01] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:31:01] エントリー 取引ID 57 (USD/JPY Sell): 目標時刻=22:42:00, ゆらぎ=0.70秒, 最終実行時刻=22:41:59
[2026-01-09 22:31:01] 次のアクション 'PING_60S' まで 597.34 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:40:59] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:40:59] 現在のアクセストークンを検証しています...
[2026-01-09 22:41:00] トークン検証成功。
[2026-01-09 22:41:00] 事前確認 (PING_60S) 成功。
[2026-01-09 22:41:00] 次のアクション 'PING_30S' まで 28.95 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:41:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:41:29] 現在のアクセストークンを検証しています...
[2026-01-09 22:41:29] トークン検証成功。
[2026-01-09 22:41:29] 事前確認 (PING_30S) 成功。
[2026-01-09 22:41:29] 次のアクション 'FINAL_ACTION' まで 29.71 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:41:59] エントリー 取引ID 57 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 22:41:59] --- 取引ID 57 (USD/JPY Sell) のエントリー処理開始 ---
[2026-01-09 22:41:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat,PriceInfo
[2026-01-09 22:41:59] エントリー処理開始 (UIC: 42, Side: Sell, Amount: 50000.0)...
[2026-01-09 22:41:59] UIC 42 の既存取引（ポジション/Working注文）を確認中...
[2026-01-09 22:42:00] UIC 42 の既存取引は見つかりませんでした。
[2026-01-09 22:42:00] 既存取引がないため、新規注文を発注します...
[2026-01-09 22:42:00] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat
[2026-01-09 22:42:00] リクエスト例外 (/trade/v2/orders): 400 Client Error: Bad Request for url: https://gateway.saxobank.com/sim/openapi/trade/v2/orders - 試行 1/1
[2026-01-09 22:42:00] エラーレスポンス詳細 (/trade/v2/orders): {"ErrorInfo":{"ErrorCode":"OrderNotPlaced","Message":"Order not placed as other order in request was rejected."},"ExternalReference":"20260109_trade_57_entry_v1","Orders":[{"ErrorInfo":{"ErrorCode":"WrongSideOfRelatedOrder","Message":"The order price is on the wrong side of the related order. Please
[2026-01-09 22:42:00] 1回の再試行後もRequestException: /trade/v2/orders
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:42:00.686164Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '658e298f-5759-4f64-89a9-10e6a62c4427', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_57_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797234', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'RelatedOrderId': ['5036797235'], 'RelatedOrderIds': ['5036797235'], 'SequenceId': '272089652', 'Status': 'Placed', 'SubStatus': 'Rejected', 'Symbol': 'USDJPY', 'Uic': 42}
[2026-01-09 22:42:01] 注文応答に OrderId がありません: None
[2026-01-09 22:42:01] SL付き注文に失敗したため通常注文へフォールバックします: OrderId が取得できませんでした。
[2026-01-09 22:42:02] 注文受付成功: OrderID 5036797237
[2026-01-09 22:42:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:42:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:42:02] ENSイベントを監視中 (OrderID: 5036797237, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:42:02.038927Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'c02f2646-ac6d-4b0b-a117-183938987380', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_57_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797237', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272089658', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:42:02.044927Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.491, 'BuySell': 'Sell', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'c02f2646-ac6d-4b0b-a117-183938987380', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.491, 'ExternalReference': '20260109_trade_57_entry_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797237', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288734', 'SequenceId': '272089659', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}   
✨ ENSから注文完全約定イベント: OrderID=5036797237, Price=157.491
[2026-01-09 22:42:02] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797237', 'execution_price': Decimal('157.491'), 'execution_time': '2026-01-09T13:42:02.044927Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288734'}
[2026-01-09 22:42:02] ✅ エントリー成功: 取引ID 57 (USD/JPY Sell)
[2026-01-09 22:42:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:42:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:42:03] 決済 取引ID 57 (USD/JPY Sell): 目標時刻=22:53:00, ゆらぎ=0.32秒, 最終実行時刻=22:52:59
[2026-01-09 22:42:03] 次のアクション 'PING_60S' まで 596.23 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:44:06] アクセストークンを更新しています...
[2026-01-09 22:44:07] アクセストークンを正常に更新しました。
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS WebSocket接続が閉じられました。
ENS接続断の詳細: reason=ConnectionClosed, exception=ConnectionClosedError, close_code=1006, close_reason=, last_message_at=2026-01-09 22:48:05, last_message_id=64, last_ping_ok_at=2026-01-09 22:48:18, last_ping_rtt_ms=1.1
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=False, contextId=ctx-7965290393-hsdu6wsb, messageid=64
[2026-01-09 22:48:26] アクセストークンを更新しています...
[2026-01-09 22:48:27] アクセストークンを正常に更新しました。
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7965290393-hsdu6wsb&authorization=***&messageid=64
ENS monitor task cancelled
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: _resetsubscriptions 対象。再接続します。
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=True, contextId=ctx-7965290393-hsdu6wsb, messageid=0
[2026-01-09 22:48:29] アクセストークンを更新しています...
[2026-01-09 22:48:30] アクセストークンを正常に更新しました。
ENSサブスクリプションを再作成します...
[2026-01-09 22:48:30] ENSサブスクリプションを作成中...
[2026-01-09 22:48:30] ストリーミング用ContextId生成: ctx-7966510535-njqc2rnv
[2026-01-09 22:48:30] ENS WebSocket URL: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7966510535-njqc2rnv&authorization=***
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7966510535-njqc2rnv&authorization=***
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:51:59] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 22:51:59] 現在のアクセストークンを検証しています...
[2026-01-09 22:51:59] トークン検証成功。
[2026-01-09 22:51:59] 事前確認 (PING_60S) 成功。
[2026-01-09 22:51:59] 次のアクション 'PING_30S' まで 29.69 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:52:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:52:29] 現在のアクセストークンを検証しています...
[2026-01-09 22:52:29] トークン検証成功。
[2026-01-09 22:52:29] 事前確認 (PING_30S) 成功。
[2026-01-09 22:52:29] 次のアクション 'FINAL_ACTION' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:52:59] 決済 取引ID 57 (USD/JPY Sell) の実行時刻になりました。
[2026-01-09 22:52:59] --- 取引ID 57 (USD/JPY Sell) の決済処理開始 ---
[2026-01-09 22:52:59] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:52:59] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:53:00] UIC 42 のキャンセル対象注文はありません。
[2026-01-09 22:53:00] ポジション 5025288734 (USD/JPY) の決済処理開始...
[2026-01-09 22:53:00] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:53:00] UIC 42 の最新ポジションを発見しました。
[2026-01-09 22:53:00] 決済注文データ: Buy 50000.0 units of UIC 42
[2026-01-09 22:53:00] USD/JPY の決済注文が受付されました。OrderId: 5036797474
[2026-01-09 22:53:00] 決済注文が受付されました。OrderID: 5036797474
[2026-01-09 22:53:00] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:53:00] ENSイベントを監視中 (OrderID: 5036797474, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:53:00.790557Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '8cca68c9-8e00-4947-ab3f-56e300600dbc', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_57_exit_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797474', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272089924', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:53:00.797558Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.502, 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '8cca68c9-8e00-4947-ab3f-56e300600dbc', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.502, 'ExternalReference': '20260109_trade_57_exit_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797474', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288826', 'SequenceId': '272089925', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}     
✨ ENSから注文完全約定イベント: OrderID=5036797474, Price=157.502
[2026-01-09 22:53:01] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797474', 'execution_price': Decimal('157.502'), 'execution_time': '2026-01-09T13:53:00.797558Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288826'}
[2026-01-09 22:53:01] イベント 'order_fill' により決済を確認しました。
[2026-01-09 22:53:01] ポジション情報を検索中 (UIC: 42)...
[2026-01-09 22:53:01] ClosedPositionsに該当がなくても保有ポジションなしと判定: UIC=42
[2026-01-09 22:53:02] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:53:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:53:02] エントリー 取引ID 58 (USD/JPY Buy): 目標時刻=22:54:00, ゆらぎ=0.74秒, 最終実行時刻=22:53:59
[2026-01-09 22:53:02] 次のアクション 'PING_30S' まで 26.56 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:53:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 22:53:29] 現在のアクセストークンを検証しています...
[2026-01-09 22:53:29] トークン検証成功。
[2026-01-09 22:53:29] 事前確認 (PING_30S) 成功。
[2026-01-09 22:53:29] 次のアクション 'FINAL_ACTION' まで 29.71 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 22:53:59] エントリー 取引ID 58 (USD/JPY Buy) の実行時刻になりました。
[2026-01-09 22:53:59] --- 取引ID 58 (USD/JPY Buy) のエントリー処理開始 ---
[2026-01-09 22:53:59] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat,PriceInfo
[2026-01-09 22:53:59] エントリー処理開始 (UIC: 42, Side: Buy, Amount: 50000.0)...
[2026-01-09 22:53:59] UIC 42 の既存取引（ポジション/Working注文）を確認中...
[2026-01-09 22:54:00] UIC 42 の既存取引は見つかりませんでした。
[2026-01-09 22:54:00] 既存取引がないため、新規注文を発注します...
[2026-01-09 22:54:00] 価格情報を取得します。UICs: 42, AssetType: FxSpot, FieldGroups: Quote,DisplayAndFormat
[2026-01-09 22:54:00] リクエスト例外 (/trade/v2/orders): 400 Client Error: Bad Request for url: https://gateway.saxobank.com/sim/openapi/trade/v2/orders - 試行 1/1
[2026-01-09 22:54:00] エラーレスポンス詳細 (/trade/v2/orders): {"ErrorInfo":{"ErrorCode":"OrderNotPlaced","Message":"Order not placed as other order in request was rejected."},"ExternalReference":"20260109_trade_58_entry_v1","Orders":[{"ErrorInfo":{"ErrorCode":"WrongSideOfRelatedOrder","Message":"The order price is on the wrong side of the related order. Please
[2026-01-09 22:54:00] 1回の再試行後もRequestException: /trade/v2/orders
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:54:00.613851Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': 'c2110706-9068-455c-8a74-634358ce6ab4', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_58_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797480', 'OrderRelation': 'IfDoneMaster', 'OrderType': 'Market', 'RelatedOrderId': ['5036797481'], 'RelatedOrderIds': ['5036797481'], 'SequenceId': '272089946', 'Status': 'Placed', 'SubStatus': 'Rejected', 'Symbol': 'USDJPY', 'Uic': 42}
[2026-01-09 22:54:01] 注文応答に OrderId がありません: None
[2026-01-09 22:54:01] SL付き注文に失敗したため通常注文へフォールバックします: OrderId が取得できませんでした。
[2026-01-09 22:54:02] 注文受付成功: OrderID 5036797482
[2026-01-09 22:54:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:54:02] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:54:02] ENSイベントを監視中 (OrderID: 5036797482, UIC: 42, タイプ: ['order_fill'])...
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:54:02.054449Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '731ba0c9-4440-4fa5-9cf7-32619e179dd3', 'Duration': {'DurationType': 'DayOrder'}, 'ExternalReference': '20260109_trade_58_entry_v1', 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797482', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'SequenceId': '272089948', 'Status': 'Placed', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42}
ENS Orderイベント受信: {'AccountId': '21294788', 'AccountKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'ActivityTime': '2026-01-09T13:54:02.062450Z', 'ActivityType': 'Orders', 'Amount': 50000.0, 'AssetType': 'FxSpot', 'AveragePrice': 157.513, 'BuySell': 'Buy', 'ClientId': '21294788', 'ClientKey': 'BlWiFwr94hk7OIVC4qLb6Q==', 'CorrelationKey': '731ba0c9-4440-4fa5-9cf7-32619e179dd3', 'Duration': {'DurationType': 'DayOrder'}, 'ExecutionPrice': 157.513, 'ExternalReference': '20260109_trade_58_entry_v1', 'FillAmount': 50000.0, 'FilledAmount': 50000.0, 'HandledBy': '21294788', 'IsSecondCurrencyOrder': False, 'OrderId': '5036797482', 'OrderRelation': 'StandAlone', 'OrderType': 'Market', 'PositionId': '5025288836', 'SequenceId': '272089949', 'Status': 'FinalFill', 'SubStatus': 'Confirmed', 'Symbol': 'USDJPY', 'Uic': 42, 'ValueDate': '2026-01-14', 'Venue': 'XXXX'}    
✨ ENSから注文完全約定イベント: OrderID=5036797482, Price=157.513
[2026-01-09 22:54:02] ★ ENSで期待するイベント(order_fill)を受信しました: {'type': 'order_fill', 'order_id': '5036797482', 'execution_price': Decimal('157.513'), 'execution_time': '2026-01-09T13:54:02.062450Z', 'filled_amount': Decimal('50000.0'), 'amount': Decimal('50000.0'), 'status': 'filled', 'uic': 42, 'position_id': '5025288836'}
[2026-01-09 22:54:02] ✅ エントリー成功: 取引ID 58 (USD/JPY Buy)
[2026-01-09 22:54:03] Discord通知を送信しました。ステータス: 204
[2026-01-09 22:54:03] 取引ステータスを trade_status.json に保存しました。
[2026-01-09 22:54:03] 決済 取引ID 58 (USD/JPY Buy): 目標時刻=23:10:00, ゆらぎ=0.48秒, 最終実行時刻=23:09:59
[2026-01-09 22:54:03] 次のアクション 'PING_60S' まで 896.21 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 23:02:07] アクセストークンを更新しています...
[2026-01-09 23:02:08] アクセストークンを正常に更新しました。
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS WebSocket接続が閉じられました。
ENS接続断の詳細: reason=ConnectionClosed, exception=ConnectionClosedError, close_code=1006, close_reason=, last_message_at=2026-01-09 23:08:25, last_message_id=64, last_ping_ok_at=2026-01-09 23:08:27, last_ping_rtt_ms=0.9
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=False, contextId=ctx-7966510535-njqc2rnv, messageid=64
[2026-01-09 23:08:34] アクセストークンを更新しています...
[2026-01-09 23:08:35] アクセストークンを正常に更新しました。
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7966510535-njqc2rnv&authorization=***&messageid=64
ENS monitor task cancelled
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
ENS制御メッセージ検出: _resetsubscriptions 対象。再接続します。
ENS WebSocketに再接続を試みています... 1秒後 (試行1)
ENS再接続開始: force_new_context=True, contextId=ctx-7966510535-njqc2rnv, messageid=0
[2026-01-09 23:08:37] アクセストークンを更新しています...
[2026-01-09 23:08:38] アクセストークンを正常に更新しました。
ENSサブスクリプションを再作成します...
[2026-01-09 23:08:38] ENSサブスクリプションを作成中...
[2026-01-09 23:08:38] ストリーミング用ContextId生成: ctx-7967718602-ps7o1v69
[2026-01-09 23:08:39] ENS WebSocket URL: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7967718602-ps7o1v69&authorization=***
ENS WebSocket接続中: wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=ctx-7967718602-ps7o1v69&authorization=***
ENS WebSocket接続成功
ENS WebSocketへの再接続に成功しました。
ENS接続監視モニターを開始します。
[2026-01-09 23:08:59] 接続の事前確認 (PING_60S) を行います...
[2026-01-09 23:08:59] 現在のアクセストークンを検証しています...
[2026-01-09 23:08:59] トークン検証成功。
[2026-01-09 23:08:59] 事前確認 (PING_60S) 成功。
[2026-01-09 23:08:59] 次のアクション 'PING_30S' まで 29.70 秒待機します...
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
ENS制御メッセージ検出: Heartbeat Reason=NoNewData
[2026-01-09 23:09:29] 接続の事前確認 (PING_30S) を行います...
[2026-01-09 23:09:29] 現在のアクセストークンを検証しています...
[2026-01-09 23:09:29] トークン検証成功。
[2026-01-09 23:09:29] 事前確認 (PING_30S) 成功。
[2026-01-09 23:09:29] 次のアクション 'FINAL_ACTION' まで 29.70 秒待機します...
[2026-01-10 01:26:14] 決済 取引ID 58 (USD/JPY Buy) の実行時刻になりました。
[2026-01-10 01:26:14] --- 取引ID 58 (USD/JPY Buy) の決済処理開始 ---
⚠️ ENS無受信 60秒超過: 最終受信から8212.2秒。再接続試行中=False
[2026-01-10 01:26:14] ポジション情報を検索中 (UIC: 42)...
[2026-01-10 01:26:15] Discord通知エラー: HTTPSConnectionPool(host='discord.com', port=443): Max retries exceeded with url: /api/webhooks/1419480771034480712/aA30fO7EnxOcYfJFkMp9J1OWSExpJixNtJEmFyDPwEypQVcFppZHNUzrWYjoVLlbfjQs (Caused by NameResolutionError("HTTPSConnection(host='discord.com', port=443): Failed to resolve 'discord.com' ([Errno 11001] getaddrinfo failed)"))
警告: ENS受信が停止したとみなし、再接続を強制します。[2026-01-10 01:26:15] 接続エラー (/port/v1/positions): HTTPSConnectionPool(host='gateway.saxobank.com', port=443): Max retries exceeded with url: /sim/openapi/port/v1/positions?AccountKey=BlWiFwr94hk7OIVC4qLb6Q%3D%3D&ClientKey=BlWiFwr94hk7OIVC4qLb6Q%3D%3D&Uics=42&FieldGroups=PositionBase%2CPositionView&%24top=1000 (Caused by NameResolutionError("HTTPSConnection(host='gateway.saxobank.com', port=443): Failed to resolve 'gateway.saxobank.com' ([Errno 11001] getaddrinfo failed)")) - 試行 1/3[2026-01-10 01:26:14] アクセストークンを更新しています...

ENS listen task cancelled
ENS WebSocketに再接続を試みています... 1秒後 (試行1)

[2026-01-10 01:26:15] トークン更新エラー (試行 1/3): HTTPSConnectionPool(host='sim.logonvalidation.net', port=443): Max retries exceeded with url: /token (Caused by NameResolutionError("HTTPSConnection(host='sim.logonvalidation.net', port=443): Failed to resolve 'sim.logonvalidation.net' ([Errno 11001] getaddrinfo failed)"))
[2026-01-10 01:26:15] 5秒後に再試行します...
ENS再接続開始: force_new_context=False, contextId=ctx-7967718602-ps7o1v69, messageid=1
[2026-01-10 01:26:16] 接続エラー (/port/v1/positions): HTTPSConnectionPool(host='gateway.saxobank.com', port=443): Max retries exceeded with url: /sim/openapi/port/v1/positions?AccountKey=BlWiFwr94hk7OIVC4qLb6Q%3D%3D&ClientKey=BlWiFwr94hk7OIVC4qLb6Q%3D%3D&Uics=42&FieldGroups=PositionBase%2CPositionView&%24top=1000 (Caused by NameResolutionError("HTTPSConnection(host='gateway.saxobank.com', port=443): Failed to resolve 'gateway.saxobank.com' ([Errno 11001] getaddrinfo failed)")) - 試行 2/3
[2026-01-10 01:26:22] API /port/v1/positions が401を返しました。トークンリフレッシュを試みます。レスポンス概要: 
[2026-01-10 01:26:22] リフレッシュトークンが無効です。完全な再認証が必要です。
[2026-01-10 01:26:22] アクセストークンを更新しています...[2026-01-10 01:26:22] 定期トークン更新に失敗しました。

[2026-01-10 01:26:23] リフレッシュトークンが無効です。完全な再認証が必要です。
[2026-01-10 01:26:24] アクセストークンを更新しています...
アクセストークンの更新に失敗しました。再認証が必要です。
[2026-01-10 01:26:24] リフレッシュトークンが無効です。完全な再認証が必要です。
[2026-01-10 01:26:24] 致命的な認証エラー。再認証を試みます。
[2026-01-10 01:26:25] Discord通知を送信しました。ステータス: 204
[2026-01-10 01:26:25] OAuth認証フローを開始します...
[2026-01-10 01:26:25] 指定されたパス C:\fx\saxo\msedgedriver.exe でのEdgeDriver起動に失敗: Message: Unable to obtain driver for MicrosoftEdge; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location
。デフォルトパスを試します。

DevTools listening on ws://127.0.0.1:62780/devtools/browser/fdc7b10d-d9cc-4982-a067-2aaeb38d239e
[2026-01-10 01:26:28] Edge WebDriverが正常に作成されました。
[2026-01-10 01:26:28] 認証URLに移動します: https://sim.logonvalidation.net/authorize?response_type=code&client_id=%2A%2A%2A%2A%2A&redirect_uri=%2A%2A%2A%2A%2A&code_challenge=%2A%2A%2A%2A%2A&code_challenge_method=S256&scope=openid+TradeAccess+ReadTrading+ReadAccount&state=%2A%2A%2A%2A%2A
[2060:9836:0110/012628.821:ERROR:chrome\browser\task_manager\providers\fallback_task_provider.cc:126] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
[2026-01-10 01:26:29] ブラウザ経由でログインしてください。必要に応じてSMSコードを待機します (最大5分)。
[2060:9836:0110/012629.960:ERROR:chrome\browser\task_manager\providers\fallback_task_provider.cc:126] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
[2026-01-10 01:26:30] ログイン情報を送信しました。リダイレクトを待機中: http://localhost:8083/saxo_sim
[2026-01-10 01:26:34] OAuthブラウザ操作中のエラー: Message: invalid session id: session deleted as the browser has closed the connection
from disconnected: not connected to DevTools
  (Session info: MicrosoftEdge=143.0.3650.96); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#invalidsessionidexception
  PC画面が時間経過で消えてしまい、接続が切れた。
