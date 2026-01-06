SAXOバンクOpenAPI仕様
########## OCO注文(TP/SL)の実行確認 ##########
https://www.developer.saxo/openapi/referencedocs/port/v1/closedpositions
\nReference Docs  Portfolio（GETのみ、POSTとDELETEは除外）
ClosedPositions\nRead only end points serving closed positions and the underlying closed positions making up the net closed position. The set of closed positions is restricted by the supplied query parameters as well as whether or not the identity represented by the authorization token has access to the account on which the positions are posted.\n\nA user of a client will have access to accounts under that client\nA user of an IB or WLC will have access to accounts on that client or clients there under\nAn employee has access to all accounts\nA request containing a TradingFloor "Federated Access" token will have access to the account specified in that token.\nIf access is granted on the basis of the TradingFloor "Federated Access" token, then the number of fields will be a subset of the full set of fields shown in the specification for the response.\nEndpoints\nGet closed positions for a client, accountGroup or account\nReturns a list of closed positions fulfilling the criteria specified by the query string parameters.\n\n https://gateway.saxobank.com/sim/openapi/port/v1/closedpositions?$skip={$skip}&$top={$top}&AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&ClientKey={ClientKey}&ClosedPositionId={ClosedPositionId}&FieldGroups={FieldGroups}\n\nGet a single position\nGet a single position.\n\n https://gateway.saxobank.com/sim/openapi/port/v1/closedpositions/{ClosedPositionId}?AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&ClientKey={ClientKey}&FieldGroups={FieldGroups}\n\nGet closed positions for a client, to which the logged in user belongs\nReturns a list of closed positions fulfilling the criteria specified by the query string parameters.\n\n https://gateway.saxobank.com/sim/openapi/port/v1/closedpositions/me?$skip={$skip}&$top={$top}&FieldGroups={FieldGroups}

https://www.developer.saxo/openapi/referencedocs/cs/v1/historicalreportdata-trades
Reference Docs  Client Services
Historical Report Data - Trades\nTrades Report Data.\n\nEndpoints\nGets all trades for dates or tradeId.\nGets all trades for dates or tradeId.\n\n https://gateway.saxobank.com/sim/openapi/cs/v1/reports/trades/{ClientKey}?$skip={$skip}&$skiptoken={$skiptoken}&$top={$top}&AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&FromDate={FromDate}&MockDataId={MockDataId}&ToDate={ToDate}&TradeId={TradeId}

https://www.developer.saxo/openapi/referencedocs/cs/v1/audit-orderactivities
Reference Docs  Client Services
Audit - OrderActivities\nEnd point for querying order activities\n\nEndpoints\nQuery Order activities history\nQuery Order activities history\n\nThe __nextPoll link is present when relevant and MUST be used for continuously polling\n\nOur preferred option for continuously fetching order activities is to stream it out of ENS\n\n https://gateway.saxobank.com/sim/openapi/cs/v1/audit/orderactivities?$skiptoken={$skiptoken}&$top={$top}&AccountKey={AccountKey}&ClientKey={ClientKey}&CorrelationKey={CorrelationKey}&EntryType={EntryType}&FieldGroups={FieldGroups}&FromDateTime={FromDateTime}&IncludeSubAccounts={IncludeSubAccounts}&OrderId={OrderId}&Status={Status}&ToDateTime={ToDateTime}

########## OCO注文(TP/SL)のJSON構造 ##########
https://openapi.help.saxo/hc/en-us/articles/4418479465361-How-do-I-place-related-orders-via-OpenAPI

How do I place related orders via OpenAPI?\nUpdated 3 years ago\nIt is possible to place related orders (for example take profit or stop loss orders) via the endpoint POST /trade/v2/orders/trade/v2/orders. The order object that you post to this endpoint holds a field called Orders. Inside this array you can place order objects for the related orders you wish to place. You can find examples of doing so in the resources below. \n\nRelated Orders are both validated when placed with Saxo, and when the main order has been filled. This is to avoid orders being placed on the wrong side of the market, but there are some scenarios to be familiar with.\n\nWith main orders that have a defined entry price different from the current market price such as a Stop Limit Order, some related orders may not be on the correct side of the market when placed, but will be once they the main order is filled. In this scenario, validation of these related orders uses the entry order price as the assumed market price, so you can properly apply a stop loss and take profit on the assumed entry point, with validation to ensure there no related order on the wrong side of the market.\n\n \n\nMore Resources\n\nLearn page - Order Placement
https://www.developer.saxo/openapi/learn/order-placement

It is possible to place orders on all asset types except for Fx Options, which are not currently tradable via OpenAPI. When placing orders using OpenAPI, it is important to understand that not all order types and parameters are supported for all asset classes or even across one asset type traded on different exchanges. In order to place an order it is usually required to look up some of the underlying instrument's constraints through instrument services in Reference Data and to get a price through a separate request or through a subscription already set up. 
\nOrder Properties\nAssetType & Uic (mandatory)\n\nSpecifies the instrument and how it is traded.\n\nAccountKey (recommended)\n\nUsed to indicate what account the resulting position is on. For clients with sub clients, the order can also be placed on a sub client's account.\n\nAmount (mandatory)\n\nWhen choosing an amount there are certain rules to obey\n\nIf the amount is very small or very large the order may fail\nFor exchange based asset types, if the value of the order is too small, the order will fail\nFor asset types traded in lots, there may be rules around whether odd lot sizes are allowed - this can be looked up by the instrument's LotSizeType\nIn general the amount is always in the base unit of the instrument\nNote that for some instrument types amounts can be fractional. \nOrderType (mandatory)\n\nMost common types are market, limit and stop. See the full overview in the article on Core Business Concepts.\n\nOrderPrice\n\nMust be provided on all order types other than market orders. See section on rounding.\n\nStopLimitPrice\n\nMust be provided for StopLimitOrders. Controls the stop level part of the stoplimit.\n\nToOpenClose\n\nThis value is only relevant and mandatory for StockIndexOption, StockOption and FuturesOption. By setting this value you indicate the desired netting behavior of the resulting position. \n\nManualOrder (mandatory for most applications)\n\nIndicates if the order is originated by a manual or automatic action. While currently optional, this field will soon be made mandatory for almost all applications. Please follow the definition below when deciding how to set this value.\n\nManualOrder Field Value	Meaning\nFalse	\nIndicates an automatic order entry.\n\nAutomated order entry refers to orders that are generated and/or routed without human intervention. This includes any order generated by a computer system as well as orders that are routed using functionality that manages order submission through automated means (i.e. execution algorithm).\n\nTrue	\nIndicates a manual order entry\n\nManual order entry refers to orders that are submitted by an individual directly entering the order into a front-end system, typically via keyboard, mouse or touch screen, and which is routed in its entirety to the match engine at the time of submission. A order that is generated automatically, but ultimately confirmed by the user before being sent to market is considered manual.\n\n\n\nPlacing Single Orders\nNot all instruments support all order types or even all duration types. To find out what order types are supported, look at the instrument data returned by Reference Data. Most instrument support market orders with a duration of the current day. This is demonstrated by this example placing a market order on the EURUSD instrument.\n\nMarket\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n	"AccountKey": "1ZsMyKSda2eB2GCMrUCKHw==",\n	"Amount": 10000.0,\n	"BuySell": "Buy",\n	"OrderType": "Market",\n	"ManualOrder": true,\n	"Uic": 21,\n	"AssetType": "FxSpot",\n	"OrderDuration": {\n		"DurationType": "DayOrder"\n	}\n}\nMarket orders are executed when the market is open and on whatever price there is in the market at the time of execution. This makes market orders unsuited for instruments with low liquidity. Especially when also having a long duration time.\n\nLimit\n\nIn order to place a limit order we need a target order price at a reasonable distance to the market. A price can be obtained from a price subscription or simply by requesting:\n\nGET https://gateway.saxobank.com/sim/openapi/trade/v1/infoprices?uic=21&AssetType=FxSpot \n{\n	"AccountKey": "1ZsMyKSda2eB2GCMrUCKHw==",\n	"AssetType": "FxSpot",\n	"Quote": {\n		"Ask": 1.06337,\n		"Bid": 1.06317,\n		"DelayedByMinutes": 0\n	},\n	"Uic": 21\n}\nLet's say we want to place a limit order 50 pips away from the market, then the target price would be 1.06287. However for EURUSD valid tick sizes are rounded to nearest 0.00005, so the target order price becomes 1.06285. The order would then be:\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n	"AccountKey": "1ZsMyKSda2eB2GCMrUCKHw==",\n	"Amount": 10000.0,\n	"BuySell": "Buy",\n	"OrderType": "Limit",\n	"OrderPrice": 1.06285,\n	"ManualOrder": true,\n	"Uic": 21,\n	"AssetType": "FxSpot",\n	"OrderDuration": {\n		"DurationType": "DayOrder"\n	}\n}\nDecimals, TickSize and Tick Size Schemes\nCalculating a correct OrderPrice value is easy for Fx, but complicated for other asset types where there are explicit rules for what values are valid and how they are rounded. Those rules are controlled by the instrument's tick size and tick size scheme. For instruments that does not have a tick size or tick size scheme, order prices simply need to be rounded to the instrument's number of decimals. For the few instruments are quoted in fractions, the order price must conform to the tick size on the instrument.\n\nDecimals\n\nA price is always denoted in the the number of decimals supported by the instrument. The number of decimals can be found on the instrument data looked up in the Reference Data. However for certain Fx crosses the number is one higher if the format has the flag AllowDecimalPips.\n\nWhen there is no tick size scheme\n\nThe order price has to be rounded to the number of decimals of the instrument and then adjusted to the tick size of the instrument. In the above example EURUSD has 4 (+1) decimals and a tick size of 0.00005. This means that a price like 1.062873 should be rounded to 1.06287 due to the number of decimals, but since the tick size is 0.00005, the correct rounding is 1.06285.\n\nWhen there is a tick size scheme\n\nCertain instruments have more complex price rounding rules. That is indicated by the tick size scheme on the instrument. It gives specific tick sizes depending on a price range. If the actual price of the instrument is above the maximum price value in the tick size scheme, the above normal rounding rules apply. The use of tick size schemes are illustrated by this example:\n\n\n\nExample: Suggesting an OrderPrice for a CFD on International Consolidated Airlines Group SA (IAG:xlon)\n\nAssume you want to place a buy limit order for IAG:xlon at 2% away from the market, you need to know the tick size scheme for IAG:xlon as well as the current market price. Right now it is traded at bid 446.1, ask 446.4. \n\nThe tick size scheme for the instrument looked up in reference data is this:\n\nHigh Price\nTick Size\n0.4999	0.0001\n0.9995	0.0005\n4.999	0.001\n9.995	0.005\n49.99	0.01\n99.95	0.05\n499.9	0.1\n999.5	0.5\n4999.0	1.0\n9995.0	5.0\nSince the desired price is in the ]99.99; 499.9] range, we need to round the price to nearest 0.1. Also known as the tick size relevant for the desired order price. In the end the formula for selecting a price n percent away from the market becomes: \n\norderPrice = Round((currentPrice- currentPrice*n/100)/tickSize)*tickSize\nSo filling in the values for a buy order we get\n\ncurrentPrice = 446.4 // currentPrice is the ask side since we are placing an order to buy\nn = 2 \ntickSize = 0.1 \norderPrice = Round((446.4-446.5*2/100)/0.1)*0.1 => orderPrice = 437.5\nSupport for Related Orders\nIt is possible to relate orders to an entry order or position for most asset types. The exceptions are StockIndex (which is not tradable), FutureContracts and FutureStrategies. For the other asset types support for related orders can be deduced from the supported order types retrieved on the instrument. Related orders can be placed together with the entry order or one by one.\n\nThrottling of order placement is per request\nPlacing Multiple Related Orders\nIt is possible to place up to three orders together in a relation. For instance to place an entry order together with a non-working order to guard the resulting position against a drop-off in price.\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n	"Amount": 10000.0,\n	"BuySell": "Buy",\n	"OrderPrice": 1.06375,\n	"OrderType": "Limit",\n	"Uic": 21,\n	"AssetType": "FxSpot",\n	"ManualOrder": true,\n	"OrderDuration": {\n		"DurationType": "DayOrder"\n	},\n	"Orders": [\n	{\n		"BuySell": "Sell",\n		"OrderPrice": 1.05875,\n		"OrderType": "Stop",\n        "ManualOrder": true,\n		"OrderDuration": {\n			"DurationType": "GoodTillCancel"\n		}\n	}\n	]\n}\nThe service support placing two related orders to an entry order, but the related orders have to be one limit order and one of the various supported stop order types. The result of succesfully placing the above structure is a result containing the resulting two order ids:\n\nHTTP/1.1 200 OK\n{\n	"OrderId": 49036233,\n	"Orders": [\n	{\n		"OrderId": 49036234\n	}\n	]\n}\nAdding a Related Order to an Existing Order\nIt is recommended to place multiple related orders together as one operation. However, if there already is an existing order it too can be done:\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n	"OrderId": 49036233,\n	"Orders": [\n	{\n		"Uic": 21,\n		"BuySell": "Sell",\n		"Amount": 10000,\n		"ManualOrder": true,\n		"OrderPrice": 1.06575,\n		"AssetType": "FxSpot",\n		"OrderType": "Limit",\n		"OrderDuration": {\n			"DurationType": "GoodTillCancel"\n		}\n	}\n	]\n}\nThe above example adds a second related order to the entry order + stop order from the previous example. It does so, by providing a new order in the related orders collection and referring to the entry order instead of having a full order structure. If it is desired to add two related orders to an entry order it is recommended to do that as one operation, but a second order can be appended later. The request to add the second related order needs to refer to the order id of the entry order as well the first related order. The request that needs to be sent contains the entire structure of a three way order, but where the two first orders are only referred to by id.\n\n{\n	"OrderId": 49036233,\n	"Orders": [\n	{\n		"OrderId": 49026234\n	},\n	{\n		"Uic": 21,\n		"BuySell": "Sell",\n		"Amount": 10000,\n		"OrderPrice": 1.06075,\n		"AssetType": "FxSpot",\n		"OrderType": "Stop",\n		"ManualOrder":true,\n		"OrderDuration": {\n			"DurationType": "GoodTillCancel"\n		}\n	}\n	]\n}\nIt is important to be aware of some pitfalls of doing this:\n\nIt is an error to provide an orderid together with any other parameters. You are either providing a reference to an order or an order placement request\nRelating orders to an already existing order increases the risk that the entry order has been executed when the new related order is entered\nYou can only add two related orders and only one of them can be a limit order\nThe above example does not explicitly use an accountkey to identify the account the order should be on. In this case the client's default account is then used. However, if the entry order had explicitly been placed on another account, the related order should also explicitly be placed on that account. In general it is better to be very explicit about what account a given order is placed on\nWhile amount on the related order can be different between entry and related order, that is not recommended. The related orders are intended to guard the entire resulting position and cannot be used to control netting.\nAdding a Related Order to an Existing Position\nThis only works for clients on End-of-Day netting mode.\nThis is very similar to how an order is added to an existing entry order. The only difference is that instead of providing a reference to the entry order id, a reference to the PositionID must be provided instead. The same concerns as for related orders apply here as well.\n\nPlace an Order to Close a Position\nThere are two ways of closing a position. The most simple one is to open a position for the same amount in the opposite direction and let the netting process remove them. If the client is on End-of-Day-netting it happens overnight - on Intraday-netting the process should be immediate. In some cases you'll want to explicitly control netting by relating an order to the position (again: this can only be done for clients on End-of-Day-netting).\n\nAn order to close is often something you want done now and is no different from placing any other related order. The rules that a position can only have two related orders where a maximum of one is a limit order still apply. So if the goal is to explicitly close a position now, the most simple way is to a) ensure that the position has no related orders and b) relate a market order (or aggressive limit order) to the position. Assuming the position has no related order, the request looks like this:\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders \n{\n	"PositionId": 1275430,\n	"Orders": [\n	{\n		"Uic": 21,\n		"BuySell": "Sell",\n		"Amount": 30000,\n		"AssetType": "FxSpot",\n		"OrderType": "Market",\n		"ManualOrder": true,\n		"OrderDuration": {\n			"DurationType": "DayOrder"\n		}\n	}\n	]\n}\nThe catch is that a position can only be related to one other position, so if this method is used to partially close a position, it can never be fully explicitly closed.\n\nPlacing OCO Orders\nOCO orders are a special case where there is no single entry order, but instead is a list of (two) equally valid entry orders.\n\nPOST https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n	"Orders": [\n	{\n		"Uic": 21,\n		"BuySell": "Buy",\n		"Amount": 30000,\n		"OrderPrice": 1.05375,\n		"AssetType": "FxSpot",\n		"OrderType": "Limit",\n 	 	"ManualOrder": true,\n		"OrderDuration": {\n			"DurationType": "GoodTillCancel"\n		}\n	},\n	{\n		"Uic": 21,\n		"BuySell": "Buy",\n		"Amount": 30000,\n		"OrderPrice": 1.06875,\n		"AssetType": "FxSpot",\n		"OrderType": "Stop",\n		"ManualOrder": true,\n		"OrderDuration": {\n			"DurationType": "GoodTillCancel"\n		}\n	}\n	]\n}\nCancelling Orders\nCancelling orders involves calling DELETE with both an OrderId and and AccountKey of the order that is to be deleted\n\nDELETE https://gateway.saxobank.com/sim/openapi/trade/v2/orders/49039256?AccountKey=1ZsMyKSda2eB2GCMrUCKHw==\nIf a delete is issued against an entry order, that can lead to a silent cascading delete on the related orders as well. Multiple orders can be cancelled in one call by providing a comma separated list of OrderIds as long as the orders are on the same account. However, the orders are attempted cancelled one by one and cancellation will stop if an error is encountered.\n\nIt is not guaranteed that an order can always be cancelled. Right before an order is about to be executed it is locked for a short while. While it is in that state cancelling will lead to an error.\nEditing Orders\nEditing orders involves calling PATCH and providing an OrderId in addition to the new values for the fields. For instance changing the target order price of an existing order can look like this.\n\nPATCH https://gateway.saxobank.com/sim/openapi/trade/v2/orders\n{\n    "AccountKey": "zsnh|NO42RmzjC4oPovKGA==",\n	"Amount": 10000.0,\n	"BuySell": "Buy",\n	"OrderType": "Limit",\n	"OrderPrice": 1.06270,\n	"OrderId": 49039256,\n	"Uic": 21,\n	"AssetType": "FxSpot",\n	"OrderDuration": {\n		"DurationType": "DayOrder"\n	}\n}\nIf an order is changed, all fields relevant for that order must be provided. Order editing can be done as a single operation by providing the entire order structure.\n\nHandling Timeouts\nFor orders on exchange based products, order placement will once in a while timeout with a TradeNotCompleted. The status TradeNotCompleted simply means that the request terminated without knowing the status of the resulting order, which is often placed just fine. If an OrderId is also present in the the response, that serves as a reference to the order's status which can then be queried through the Portfolio.\n\nPreventing duplicate orders\nOpenAPI has some level of protection against duplicate orders. For example placing exactly the same order within 15 seconds without specifying a different x-request-id header will be rejected (see Rate Limiting). However, especially when providing an x-request-id header, the calling application should also implement de-bouncing ensure only requesting order placement, when the client actually intends to place an order. Finally, a calling application must wait until a call to OpenAPI returns. Most of the time the call to /trade/v2/orders will return within less than one second. But in the rare cases where the call does not return quickly, because we are awaiting confirmation from an external entity, the calling application should not make a second call to "re-try" placing the same order.\n\nCommon Error Messages\nMessage	Comment\nOrderRelatedPositionMissMatch	Usually happens when a related order is placed on a different account from the position or the position does not exist\nPriceExceedsAggressiveTolerance	Can occur when placing a limit order where the condition for the order is already met by a huge distance\nTooFarFromMarket	Can occur when placing a limit order where the condition for the order is unlikely to be met\nOnWrongSideOfMarket	Occurs when relating an order to a position, and the order's target price is on the wrong side of the current market price\nPriceNotInTickSizeIncrements	Occurs when an order price does not confirm to tick size or formatting rules\n\n\nSee also the live sample for placing orders (with source).

########## オーダークローズ ##########
https://www.developer.saxo/openapi/learn/trading-service-group-queries

Trading Service Group Queries
How to close positions with multiple related orders?
This article explains how to explicitly close a position, which as related orders.

However, please beware that Saxo Bank is no longer encouraging the practice to explicitly linking individual orders to individual positions.

Also please beware the in the future clients will be able to choose between two different netting modes:

Traditional netting, which still allows linking orders to individual positions
Real Time netting, where orders can not be not be linked to individual positions.




Below is an example of a position with a related take-profit limit order and stop-loss stop order. In your user interface, you may want to allow the user to "close the position". To do this, the first inclination would probably be to place a new (market or aggressive limit) order and specify the position you want to close in the "PositionId" field of this new market order.



Something like:

POST /../openapi/trade/v2/orders
{
....
     "OrderType":"Market",
	 "PositionId":"Id of position to close"
}
This will work well, if the position has no related orders.

If the position already has related orders:

Placing an additional related (closing) order can be done, if there is only one related order, but it is somewhat complicated
Placing an additional related (closing) order cannot be done at all if there are two related orders as shown in the example above.
A better approach is therefore:

If the position has one related order, change that order to become the closing order (see below).
If the position has two related orders, change the limit order to become the closing order (see below).
The closing order, is an order, which you expect will be filled, resulting in an opposite position, thus in effect closing the open position. The closing order can either be a market order or an aggressive limit order. For some asset types (e.g. stock options) it is only possible to place limit orders.



Example using market order
Consider the position information returned from port/v1/positions:

{
      "NetPositionId": "AAPL:xswx__Share",
      "PositionBase": {
        "AccountId": "Demo_612895",
        "Amount": 100,
        "AssetType": "Stock",
        "CanBeClosed": true,
        "ClientId": "612895",
        "CloseConversionRateSettled": false,
        "CorrelationKey": "685f8368-7b19-45db-80d9-6826bf00222a",
        "ExecutionTimeOpen": "2018-03-28T14:12:52.768000Z",
        "OpenPrice": 161,
        "RelatedOpenOrders": [
          {
            "Amount": 100,
            "Duration": {
              "DurationType": "GoodTillCancel"
            },
            "OpenOrderType": "Limit",
            "OrderId": "71693527",
            "OrderPrice": 170
          },
          {
            "Amount": 100,
            "Duration": {
              "DurationType": "GoodTillCancel"
            },
            "OpenOrderType": "StopIfTraded",
            "OrderId": "71693525",
            "OrderPrice": 150
          }
        ],
        "SourceOrderId": "71693519",
        "Status": "Open",
        "Uic": 7516928,
        "ValueDate": "2018-04-03T00:00:00.000000Z"
      },


Notice the two related orders: 71693527 (limit) and 7163525 (stop).

To close this position, we will modify the limit order to a market order:

PATCH /../openapi/trade/v2/orders
{
    "AssetType":"Stock",
    "AccountKey":"KDP9uS3Re3uwk1aBA2PdCw==",
    "OrderId":"71693527",
    "OrderType":"Market",
    "OrderDuration":{
        "DurationType":"DayOrder"
    }
}
Returning: 200 OK
{
  "OrderId": "71693527"
}

########## ENSの仕組み・購読手順・切断時の挙動 ##########
https://www.developer.saxo/openapi/learn/streaming
Streaming
Introduction
OpenAPI Streaming provides real time updates on quotes, positions, orders, balances etc. to client application without having to poll the OpenAPI at high frequencies. Streaming is a feature where our servers push the content to connected clients instantly as it becomes available. The result is less network traffic and lower latency.

The streaming connection uses a plain WebSocket connection with data in binary frames, optionally using the Protobuf protocol.




Introduction
Plain WebSocket streams in Saxo Bank OpenAPI
Samples
Connecting to the WebSocket server
Subscription example
Receiving messages
Disconnecting
Reconnecting
Resetting subscriptions
Re-authorizing
Control messages
What state do I need to keep
Updates
Plain WebSocket streams in Saxo Bank OpenAPI
Much of the information available through the Saxo Bank OpenAPI changes frequently. This is information such as quotes, positions, orders, balances etc. Having to poll this information with high frequency is not a viable solution. The IO overhead alone will make such a solution undesirable. To solve this problem Saxo Banks OpenAPI offers up WebSocket streams for delivering such information, allowing the server to push information when it changes. The result is less IO usage and lower latency.

Setting up a WebSocket stream means setting up the stream and a number of subscriptions that tells the Saxo Bank OpenAPI what information you want updates on. 



In this document you will learn:

How to connect to the WebSocket server
How to disconnect from the WebSocket server
How to reconnect when the connection is lost
How to understand and parse the messages you receive
It is important to understand the difference between WebSocket streams and the subscriptions that generate data for those streams, and how they work together. The WebSocket stream is the delivery channel for the updates you have asked for. Subscriptions are where you ask for specific updates to be sent out. A stream can deliver data for multiple subscriptions. Streams are identified by a context id and subscriptions are identified by a reference id.

Samples
It is not easy to start coding, based on the information below. For that reason we've provided samples in different languages.

Javascript: Live sample with source on GitHub;
C#: source on GitHub;
If you've created a sample in a different language which you want to share, let us know.

Connecting to the WebSocket server
To connect to the WebSocket server the client must go through the following steps:

Obtain an access token 
In order to create a WebSocket connection the client has to obtain an access token. Read more about how to obtain an access token.

Create a ContextId 
The client must also create an identifier of the streaming connection, which is called the ContextId. The context id must identify the streaming connection within the client session, so if the client has multiple streaming connections those connections must have different context id. Context Ids must not be re-used, unless reconnecting to an already existing websocket.
Initiate the WebSocket request 
The client must then initiate the WebSocket connection handshake. Most of the protocol handling is normally performed by the WebSocket library, but a few points must be observed:
The context id must be specified as a query string parameter with the name ContextId. It can be at most 50 characters (a-z, A-Z, -, and 0-9).
The access token must be sent in the WebSocket request. The access token can be sent either in the Authorization header or as part of the query string depending on what is supported by the client platform. The preferred method is to send the access token in the Authorization header.

Create subscriptions
In order to start receiving data you have to set up a subscription for the data you want. Subscriptions can be set up on a number of resources. 
The server will buffer messages, so it is possible to create subscriptions and initiate the web socket request in parallel.
To set up a subscription you need to provide a context id, reference id and an access token. 
The context id is the same context id used to initiate the web socket request and tells the API to send messages out on that web socket connection.
The reference id identifies messages from a specific subscription when they are sent out on a web socket connection. This enables you to set up multiple subscriptions on the same web socket connection.
The access token must be sent as an Authorization header in the POST request.
Here is an example connection request where the access token is sent as an HTTP header:

GET https://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=MyConnection
Connection: Upgrade
Upgrade: WebSocket
Sec-WebSocket-Key: gnPAlQRoyFI3zMnCgm3vlQ==
Sec-WebSocket-Version: 13
Authorization: BEARER [TOKEN]
Host: streaming.saxobank.com
And here is an example connection request where the access token is sent in the query string:

GET https://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId=MyConnection&authorization=BEARER [TOKEN]
Connection: Upgrade
Upgrade: WebSocket
Sec-WebSocket-Key: gnPAlQRoyFI3zMnCgm3vlQ==
Sec-WebSocket-Version: 13
Host: streaming.saxobank.com
Make sure that the value of the authorization parameter has a space between BEARER string and the [TOKEN] value 





If the connection can be established the server responds with HTTP status 101 Switching Protocols according to the WebSocket protocol:

HTTP/1.1 101 Switching Protocols
Cache-Control: private
Upgrade: WebSocket
Server: Microsoft-IIS/8.5
Sec-WebSocket-Accept: fqGuSI/6utSRex2gWkBHfWGKDLo=
Connection: Upgrade
If the connection cannot be established the server responds with an HTTP status code different from 101 Switching Protocols. The following 4xx range codes may be returned from the WebSocket server:

HTTP status	Possible reasons
400 Bad Request	
The context id is missing.

The specified context id is not correctly formatted.

401 Unauthorized	
The access token was not sent as part of the connection request.

The access token has an invalid format.

The access token has expired.

409 Conflict	The client session already has a WebSocket connection with the same context id.
426 Upgrade Required	The WebSocket version is different from 13. All lower versions are preliminary, but a few older client libraries use them.
429 Too Many Requests	The client session already has the allowed number of WebSocket connections. The number depends on the throttling profile assigned to the application.
How errors are handled in the client code typically depends on the WebSocket client library and the client code may not have direct access to the HTTP status code.

Subscription example
Here is an example of a subscription request. The example is a request for a price subscription. The request always has a ContextId and a ReferenceId along with some optional subscription parameters, and then a list of Arguments that are specific to a subscription.

When the subscription is successfully created a 201 response is returned and a Location header is set. This header is important to read and keep for the lifetime of the subscription. This is the location that should be used when deleting the subscription again.

POST https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions
Authorization: BEARER [TOKEN]
Host: streaming.saxobank.com
{
  "Arguments": {
    "AssetType": "FxSpot",
    "Uic": 22
  },
  "ContextId": "20180712075219681",
  "ReferenceId": "IP44964",
  "RefreshRate": 1000
}
Receiving messages
When a WebSocket connection has been established the client can start receiving messages from subscriptions, for example price subscriptions."BEARER+[token]

Data messages are sent as a stream over a series of binary WebSocket frames. Each WebSocket frame can contain multiple data messages, but a data message can also be split over several WebSocket frames in which case a WebSocket continuation frame will follow. In the illustration below there are three WebSocket frames (A, B, and C) and four data messages (1, 2, 3, and 4). 

                 +----------------+----------------+----------------+
WebSocket frame: |     A    FIN=0 |     B    FIN=1 |      C   FIN=1 |
                 +---------+------+----------------+--------+-------+
Data message:    |    1    |           2           |   3    |   4   |
                 +---------+-----------------------+--------+-------+
The client receives the WebSocket frames one at a time and in order so the first frame received is A, then B is received, and finally C:

Frame A contains message 1 and the first part of message 2 so its FIN flag will be 0 (see the The WebSocket Protocol section 5.2) to indicate that more frames will follow to complete the message.
Frame B contains the remainder of message 2 and its FIN flag is 1 to indicate that the message is complete.
Frame C contains messages 3 and 4 and its FIN flag 1 to indicate that the message is complete.
The data messages indicate their own size so the client must parse the data message to identify the boundaries between messages. For example, the client receives frame C and notes that the total size of the WebSocket frame payload is 1000 bytes. It then reads message 3 according to the format specified below. Assume that message 3 is 600 bytes long. Since only 600 of the 1000 bytes have been read to complete message 3, the client should read another message from the same frame and keep on doing so until the whole frame has been read. In the example message 4 would be 400 bytes long.

Individual data messages have the following layout:

Byte index	Size in bytes	Description
0	8	
Message identifier

64-bit little-endian unsigned integer identifying the message. The message identifier is used by clients when reconnecting. It may not be a sequence number and no interpretation of its meaning should be attempted at the client.

8	2	
Reserved

This field is reserved for future use and it should be ignored by the client.

10	1	
Reference id size (Srefid)

The number of characters/bytes in the reference id that follows.

11	Srefid	
Reference id

ASCII encoded reference id for identifying the subscription associated with the message. The reference id identifies the source subscription or type of control message.

11+Srefid	1	
Payload format

8-bit unsigned integer identifying the format of the message payload. Currently the following formats are defined:

0: The payload is a UTF-8 encoded text string containing JSON.

1: The payload is a binary protobuffer message.

The format is selected when the client sets up a streaming subscription so the streaming connection may deliver a mixture of message format. Control messages such as subscription resets are not bound to a specific subscription and are always sent in JSON format.

12+Srefid	4	
Payload size (Spayload)

32-bit unsigned integer indicating the size of the message payload.

16+Srefid	Spayload	
Payload

Binary message payload with the size indicated by the payload size field. The interpretation of the payload depends on the message format field.

Disconnecting
When the client wants to disconnect it will have to send a WebSocket close frame to the server. The server will then respond with a close frame of its own. Disconnecting will clean up your subscriptions on the server and free up connections and subscriptions, so they do not count against you when we throttle connections.  

Reconnecting
In case of errors that occur on the transport level, you will want to reconnect to the socket. To make sure this has as low an impact as possible the server keeps a small buffer of the latest messages sent to the client. When reconnecting you can specify the last message id you have received which will tell the server to start sending from that message. If you specify message id 10 as your last seen message, then the first message you will see after a reconnect is the message that comes after message 10. Do not assume that the message ids are ordered. They are merely ids and we can restart the sequence at any time if we need to. 

Example of a re-connection request where the last seen message id is provided in the query string parameter messageid.

GET https://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect/connect?contextId=MyConnection&messageid=10
Connection: Upgrade
Upgrade: WebSocket
Sec-WebSocket-Key: gnPAlQRoyFI3zMnCgm3vlQ==
Sec-WebSocket-Version: 13
Authorization: BEARER [TOKEN]
Host: streaming.saxobank.com
Resetting subscriptions
In the event that the Web Socket server detects a message loss or other error, it will send a Reset Subscription control message on the Web Socket connection. This message tells you that you have to recreate the subscriptions. The reset subscription messages may include a list of reference ids, that should be reset. If it does not include such a list or the list is empty, you will have to reset all subscriptions.
When resetting a subscription be sure to first delete the old subscriptions so these don't count against you when we throttle connections.

An example of a reset subscriptions control message is shown below. Like all control messages the reference id starts with an underscore. 

{
  "ReferenceId": "_resetsubscriptions",
  "Timestamp": "2018-07-19T11:47:41.841522Z",
  "TargetReferenceIds": [
    "IP44964"
  ]
}
There are two ways to delete a subscription and create a new one (delete must come first, to prevent reaching subscription limits).

The most efficient way is to issue a new subscription request, and use the ReplaceReferenceId field to remove the existing one. The backend will handle the delete request. This minimizes the window without an active subscription.

Alternatively, when you want to control this yourself (or if you want to replace multiple subscriptions by one new subscription, you can do a delete request:

To delete a subscription you will need to send a DELETE request to the location of the subscription resource. This location was returned in the Location header when creating the response and will be constructed by url where you subscribed, but with the context id and reference id appended as url segments (/{_contextId}/{_referenceId}) as shown in the example shown below.

DELETE https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions/20180712075219681/IP44964
Authorization: BEARER [TOKEN]
Then followed by issuing a new subscription request with a new resource id but the same context id as show below

POST https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions
Authorization: BEARER [TOKEN]
Host: streaming.saxobank.com
{
  "Arguments": {
    "AssetType": "FxSpot",
    "Uic": 22
  },
  "ContextId": "20180712075219681",
  "ReferenceId": "IP55784",
  "ReplaceReferenceId": "IP44964",  // In case you skipped the DELETE request
  "RefreshRate": 1000
}
Re-authorizing
Tokens issued from our OAuth2 server only have a limited lifetime. Along with the access token we also issue a refresh token. You need this refresh token to get a new access token before the current one expires. With normal http requests, you would just replace your access token once it has been renewed and include the new token in all subsequent requests. But Web Socket Streams don't work like regular HTTP requests, so the server only knows the token you had when you initiated the streaming connection. Once you have refreshed your token, you will have to let the server know that you have a new and valid token. Otherwise the server will disconnect the streaming connection once the initial token expires.

Doing this is quite simple. You need to get a new access token from our OAuth2 server and then execute a PUT request with a correct Authorization header and a context id in the querystring (/streaming/ws/authorize?contextid={contextid}). The server will return a 202 Accepted status code if the new access token is valid. The server will return 202 even if the context ids do not match any current connections.

Example of a re-authorization request.

PUT https://sim-streaming.saxobank.com/sim/oapi/streaming/ws/authorize?contextid=20180712075219681
Authorization: BEARER [TOKEN]

Control messages
In addition to the messages that you have chosen to subscribe to, the server might also need to send you messages that tell you about the state of the subscriptions you have set up. Some of these require actions from you, and other are just informational.

Common for all control messages is that their reference id always starts with an underscore. For now the control messages you can expect to receive are these

ReferenceId	Payload	Description	Action Required by the client
_heartbeat	
[
  {
    "ReferenceId": "_heartbeat",
    "Heartbeats": [
      {
        "OriginatingReferenceId": "IP44964",
        "Reason": "NoNewData"
      }
    ]
  }
]
Heartbeat messages

Heartbeat messages are sent when no data is sent for a while on a subscription, streaming server starts sending out heartbeats to let the client know that it is still active.

Heartbeats can be bundled for a connection, so you can get one for each of the subscriptions on that connection. The list of possible reasons for a heartbeat are:

NoNewData
This reason indicates that there just isn't any new data available, but we are still alive and will send out data when something is available.
SubscriptionTemporarilyDisabled
No data is currently being sent due to a recoverable error on the server, e.g. failure to connect to a database or internal service. The client should accept that data is not available at the expected rate and disable functions accordingly until data is available again. The subscription will continue to deliver heartbeats until data is available again.
SubscriptionPermanentlyDisabled
No data will be available on the subscription. Most likely this is due to a misconfiguration. The client should not attempt to reset the subscription and should not expect any data on it. The subscription will continue to deliver heartbeats until the subscription is removed.
Keep track of when you last received a message or a heartbeat message. If you stop receiving messages you should reconnect and tell the server what the last message id you saw was. [ADD APPROPRIATE CLIENT TIMEOUT]

If the heartbeat reason is SubscriptionPermanentlyDisabled you will need to remove the subscriptions defined by the OriginatingReferenceId.

_disconnect	
[
  {
    "ReferenceId": "_disconnect"
  }
]
Disconnect messages

It is possible that a websocket will be closed by the server. This can happen if a user changes their account password for example. When this happens a "_disconnect" instruction will be sent out on the streams opened by that user and after that no more messages will be sent on those connections. The client cannot create a new subscription after receiving a disconnect message because they have been logged out. All subsequent requests will be rejected with a 401 - Unauthorized response from the server until the user is logged out and logs back in. The message will be sent to all open connections at the same time.

Prompt user to log in again and after that recreate the WebSocket connection and set up subscriptions again.
_resetsubscriptions	
[
  {
    "ReferenceId": "_resetsubscriptions",
    "TargetReferenceIds": [
      "IP44964"
    ]
  }
]
Subscription reset messages

In some scenarios, the streaming server may send subscription reset messages to instruct the client to reset a given subset of its subscriptions. In this case, value of ReferenceId in the stream data will be "_resetsubscriptions" and reference ids of the subscriptions which should be reset is sent in parameter TargetReferenceIds.

If the list is empty, or the property is not present, all subscriptions on the websocket must be reset. 

Resetting a subscription means that the subscription should be deleted and another one created in its place using a new reference id. Any update received for a subscription after a reset instruction must be ignored.

Delete subscriptions specified by the array of reference ids in the TargetReferenceIds array.

To delete a subscription you will need to send a DELETE request to the location of the subscription resource. This location was returned in the Location header when creating the response.

Create new subscriptions to replace the old subscriptions and start from new by applying updates using the snapshot received from these new subscriptions.

What state do I need to keep
When consuming our streaming services, some tracking of state is necessary.

The first thing you need to keep track of are the ids. Your WebSocket connection is defined by a context id and messages are identified by a message id and a reference id. You will need these to effectively route messages to the right place when you receive them. The messages are composed in a way that enables you to route messages without deserializing them first. You can deserialize the header without deserializing the payload.

You also need to keep track of the latest message id you have received. In case you need to reconnect to the WebSocket you will need to pass this to the WebSocket server in order to pick up messages where you left off.

The messages you receive are only updates. So you need to store the original snapshot with all received updates applied. The messages you receive are ordered and need to be applied to the snapshot in that order.

Updates
The messages you receive from the WebSocket stream are not complete messages. The complete messages can be very big, and in order to optimize the network utilization all messages are delta compressed. This means that only the properties whose values have changed are contained in the messages you receive. To assemble the complete message you will need to apply the update received to the original snapshot. 

Because messages are are only updates it is important that you preserve the order in which you have received the messages, and that you apply deltas in that order. If you change the order, the message will become corrupt and you will not be able to trust that the state is correct.
It is also a likely scenario that updates will arrive before the snapshot. In that case it is important to queue up messages and apply them when the snapshot arrives. If not all updates are applied the message will become corrupt and you will not be able to trust that the state is correct.

Do not assume that the message ids are ordered. They are arbitrary ids and we can restart the sequence at any time if we need to.


The order is now changed to a market order, and if the market is open, the order will be executed and the position will be closed.

############################################
########## ポジションと注文の監視１ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/positions/get__port__me
Reference Docs  Portfolio  Positions
Get positions for the logged-in client
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/positions/me?$skip={$skip}&$top={$top}&FieldGroups={FieldGroups}

Endpoint Description
Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
$skip	Integer	Query-String	The number of entries to skip from the beginning of the collection
$top	Integer	Query-String	The number of entries to return from the beginning of the collection
FieldGroups	PositionFieldGroup []	Query-String	Optional. Specifies which data to return. Default is [PositionBase, PositionView]
Response Parameters
View Response Codes
HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
InvalidRequest	Default error code returned when it cannot be determined which part of the request is malformed.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
__count	Number	The total count of items in the feed.
__next	String	The link for the next page of items in the feed.
Data	PositionResponse []	The collection of entities for this feed.
MaxRows	Number	The maximum number of rows that can be returned (if applicable).
Request Example
Request URL
 /port/v1/positions/me?$skip=1&$top=1&FieldGroups=DisplayAndFormat
Response Example
Response body
{
  "__next": "/openapi/port/....../?$top=1&$skip=1",
  "Data": [
    {
      "NetPositionId": "GBPUSD_FxSpot",
      "PositionBase": {
        "AccountId": "192134INET",
        "Amount": 100000,
        "AssetType": "FxSpot",
        "CanBeClosed": true,
        "ClientId": "654321",
        "CloseConversionRateSettled": false,
        "ExecutionTimeOpen": "2016-09-02T10:25:00Z",
        "IsForceOpen": false,
        "IsMarketOpen": false,
        "LockedByBackOffice": false,
        "OpenPrice": 1.32167,
        "SpotDate": "2016-09-06T00:00:00Z",
        "Status": "Open",
        "Uic": 31,
        "ValueDate": "2017-05-04T00:00:00Z"
      },
      "PositionId": "1019942425",
      "PositionView": {
        "Ask": 1.2917,
        "Bid": 1.29162,
        "CalculationReliability": "Ok",
        "CurrentPrice": 1.29169,
        "CurrentPriceDelayMinutes": 0,
        "CurrentPriceType": "Bid",
        "Exposure": 100000,
        "ExposureCurrency": "GBP",
        "ExposureInBaseCurrency": 129192,
        "InstrumentPriceDayPercentChange": 0.26,
        "ProfitLossOnTrade": -2998,
        "ProfitLossOnTradeInBaseCurrency": -2998,
        "SettlementInstruction": {
          "ActualRolloverAmount": 0,
          "ActualSettlementAmount": 10,
          "Amount": 10,
          "IsSettlementInstructionsAllowed": false,
          "Month": 7,
          "SettlementType": "FullSettlement",
          "Year": 2020
        },
        "TradeCostsTotal": 0,
        "TradeCostsTotalInBaseCurrency": 0
      }
    }
  ]
}

############################################
########## ポジションと注文の監視２ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/positions/get__port__positionid
Reference Docs  Portfolio  Positions
Get a single position
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/positions/{PositionId}?AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&ClientKey={ClientKey}&FieldGroups={FieldGroups}&StrategyGroupingEnabled={StrategyGroupingEnabled}

Endpoint Description
Get a single position

Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
AccountGroupKey	AccountGroupKey	Query-String	The key of the account group to which the net positions belongs.
AccountKey	AccountKey	Query-String	The key of the account to which the net positions belongs.
ClientKey	ClientKey	Query-String	The key of the client to which the net positions belongs.
FieldGroups	PositionFieldGroup []	Query-String	Specifies which data to return. Default is [PositionBase,PositionView]
PositionId	String	Route	Unique ID of the position.
StrategyGroupingEnabled	Boolean	Query-String	Specifies if the positions should be grouped by strategy.
Response Parameters
View Response Codes
HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
InvalidClientId	Indicates that the requested client id was invalid.
PositionIdNotSpecified	Position not specified.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
Costs	PositionCost	Trading costs associated with opening/closing a position.
DisplayAndFormat	InstrumentDisplayAndFormat	Information about the position instrument and how to display it.
Exchange	InstrumentExchangeDetails	Information about the instrument's exchange and trading status.
Greeks	Greeks	Greeks, only available for options, i.e. FX Options, Contract Options, and Contract Options CFDs.
NetPositionId	String	The id of the NetPosition, to which this position is belongs. All positions in the same instrument have the same NetPositionId.
PositionBase	PositionStatic	Static part of position information.
PositionId	String	Unique id of this position.
PositionView	PositionDynamic	Dynamic part of position information.
UnderlyingDisplayAndFormat	InstrumentDisplayAndFormat	Information about the underlying instrument of the net position and how to display it.
Request Example
Request URL
 /port/v1/positions/167968381?AccountGroupKey=stringValue&AccountKey=01b64edf-da03-4145-bf33-ae21527d4c86&ClientKey=493b43a5-fe85-4d1f-9071-dd4a9d4e42a4&FieldGroups=DisplayAndFormat&StrategyGroupingEnabled=True
Response Example
Response body
{
  "NetPositionId": "GBPUSD_FxSpot",
  "PositionBase": {
    "AccountId": "192134INET",
    "Amount": 100000,
    "AssetType": "FxSpot",
    "CanBeClosed": true,
    "ClientId": "654321",
    "CloseConversionRateSettled": false,
    "ExecutionTimeOpen": "2016-09-02T10:25:00Z",
    "IsForceOpen": false,
    "IsMarketOpen": false,
    "LockedByBackOffice": false,
    "OpenPrice": 1.32167,
    "SpotDate": "2016-09-06T00:00:00Z",
    "Status": "Open",
    "Uic": 31,
    "ValueDate": "2017-05-04T00:00:00Z"
  },
  "PositionId": "1019942425",
  "PositionView": {
    "Ask": 1.2917,
    "Bid": 1.29162,
    "CalculationReliability": "Ok",
    "CurrentPrice": 1.29169,
    "CurrentPriceDelayMinutes": 0,
    "CurrentPriceType": "Bid",
    "Exposure": 100000,
    "ExposureCurrency": "GBP",
    "ExposureInBaseCurrency": 129192,
    "InstrumentPriceDayPercentChange": 0.26,
    "ProfitLossOnTrade": -2998,
    "ProfitLossOnTradeInBaseCurrency": -2998,
    "SettlementInstruction": {
      "ActualRolloverAmount": 0,
      "ActualSettlementAmount": 10,
      "Amount": 10,
      "IsSettlementInstructionsAllowed": false,
      "Month": 7,
      "SettlementType": "FullSettlement",
      "Year": 2020
    },
    "TradeCostsTotal": 0,
    "TradeCostsTotalInBaseCurrency": 0
  }
}
############################################
########## ポジションと注文の監視３ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/positions/get__port
Reference Docs  Portfolio  Positions
Get positions for a client, account group, account or a position
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/positions?$skip={$skip}&$top={$top}&AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&ClientKey={ClientKey}&FieldGroups={FieldGroups}&NetPositionId={NetPositionId}&PositionId={PositionId}&StrategyGroupingEnabled={StrategyGroupingEnabled}&WatchlistId={WatchlistId}

Endpoint Description
Returns a list of positions fulfilling the criteria specified by the query string parameters.

Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
$skip	Integer	Query-String	The number of entries to skip from the beginning of the collection
$top	Integer	Query-String	The number of entries to return from the beginning of the collection
AccountGroupKey	AccountGroupKey	Query-String	The key of the account group to which the net positions belongs.
AccountKey	AccountKey	Query-String	The key of the account to which the net positions belongs.
ClientKey	ClientKey	Query-String	The key of the client to which the net positions belongs.
FieldGroups	PositionFieldGroup []	Query-String	Specifies which data to return. Default is [PositionBase,PositionView]
NetPositionId	String	Query-String	The id of the netposition to which the position belongs
PositionId	String	Query-String	The id of the position.
StrategyGroupingEnabled	Boolean	Query-String	Specifies if the positions should be grouped by strategy.
WatchlistId	String	Query-String	Selects only positions those instruments belongs to the given watchlist id
Response Parameters
View Response Codes
HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
InvalidClientId	Indicates that the requested client id was invalid.
NoValidInput	No valid input values passed.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
__count	Number	The total count of items in the feed.
__next	String	The link for the next page of items in the feed.
Data	PositionResponse []	The collection of entities for this feed.
MaxRows	Number	The maximum number of rows that can be returned (if applicable).
Request Example
Request URL
 /port/v1/positions?$skip=1&$top=1&AccountGroupKey=stringValue&AccountKey=01b64edf-da03-4145-bf33-ae21527d4c86&ClientKey=493b43a5-fe85-4d1f-9071-dd4a9d4e42a4&FieldGroups=DisplayAndFormat&NetPositionId=stringValue&PositionId=stringValue&StrategyGroupingEnabled=True&WatchlistId=stringValue
Response Example
Response body
{
  "__next": "/openapi/port/....../?$top=1&$skip=1",
  "Data": [
    {
      "NetPositionId": "GBPUSD_FxSpot",
      "PositionBase": {
        "AccountId": "192134INET",
        "Amount": 100000,
        "AssetType": "FxSpot",
        "CanBeClosed": true,
        "ClientId": "654321",
        "CloseConversionRateSettled": false,
        "ExecutionTimeOpen": "2016-09-02T10:25:00Z",
        "IsForceOpen": false,
        "IsMarketOpen": false,
        "LockedByBackOffice": false,
        "OpenPrice": 1.32167,
        "SpotDate": "2016-09-06T00:00:00Z",
        "Status": "Open",
        "Uic": 31,
        "ValueDate": "2017-05-04T00:00:00Z"
      },
      "PositionId": "1019942425",
      "PositionView": {
        "Ask": 1.2917,
        "Bid": 1.29162,
        "CalculationReliability": "Ok",
        "CurrentPrice": 1.29169,
        "CurrentPriceDelayMinutes": 0,
        "CurrentPriceType": "Bid",
        "Exposure": 100000,
        "ExposureCurrency": "GBP",
        "ExposureInBaseCurrency": 129192,
        "InstrumentPriceDayPercentChange": 0.26,
        "ProfitLossOnTrade": -2998,
        "ProfitLossOnTradeInBaseCurrency": -2998,
        "SettlementInstruction": {
          "ActualRolloverAmount": 0,
          "ActualSettlementAmount": 10,
          "Amount": 10,
          "IsSettlementInstructionsAllowed": false,
          "Month": 7,
          "SettlementType": "FullSettlement",
          "Year": 2020
        },
        "TradeCostsTotal": 0,
        "TradeCostsTotalInBaseCurrency": 0
      }
    }
  ]
}
############################################
########## ポジションと注文の監視４ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/orders/get__port
Reference Docs  Portfolio  Orders
Get all open orders for a client or an account
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/orders?$skip={$skip}&$top={$top}&AccountGroupKey={AccountGroupKey}&AccountKey={AccountKey}&ClientKey={ClientKey}&FieldGroups={FieldGroups}&OrderId={OrderId}&Status={Status}&WatchlistId={WatchlistId}

Endpoint Description
You can use this operation to get all the open orders on an account or a client.

Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
$skip	Integer	Query-String	The number of entries to skip from the beginning of the collection
$top	Integer	Query-String	The number of entries to return from the beginning of the collection
AccountGroupKey	AccountGroupKey	Query-String	The key of the account group to which the order belongs.
AccountKey	AccountKey	Query-String	Unique key identifying the account that owns the orders.
ClientKey	ClientKey	Query-String	Unique key identifying the client that owns the orders.
FieldGroups	OrderFieldGroup []	Query-String	Specifies which data to return. Default is empty, meaning Display and Formatting information is not included.
OrderId	String	Query-String	The id of the order
Status	OrderStatusFilter	Query-String	Selects only a subset of open orders to be returned. Default is to return working orders only.
WatchlistId	String	Query-String	Selects only orders those instruments belongs to the given watchlist id
Response Parameters
View Response Codes

HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
InvalidClientId	Indicates that the requested client id was invalid.
InvalidInput	An error was encountered when processing given input parameters.
NoValidInput	No valid input values passed.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
__count	Number	The total count of items in the feed.
__next	String	The link for the next page of items in the feed.
Data	OrderResponse []	The collection of entities for this feed.
MaxRows	Number	The maximum number of rows that can be returned (if applicable).
Request Example
Request URL
 /port/v1/orders?$skip=1&$top=1&AccountGroupKey=stringValue&AccountKey=01b64edf-da03-4145-bf33-ae21527d4c86&ClientKey=493b43a5-fe85-4d1f-9071-dd4a9d4e42a4&FieldGroups=DisplayAndFormat&OrderId=stringValue&Status=All&WatchlistId=stringValue
Response Example
Response body
{
  "__next": "/openapi/port/....../?$top=1&$skip=1",
  "Data": [
    {
      "AccountId": "192134INET",
      "AccountKey": "LZTc7DdejXODf-WSl2aCyQ==",
      "Amount": 250000,
      "AssetType": "FxSpot",
      "BuySell": "Buy",
      "CalculationReliability": "Ok",
      "ClientKey": "7m4I|vtYLUnEGg77o9uQhw==",
      "CurrentPrice": 1.09062,
      "CurrentPriceDelayMinutes": 0,
      "CurrentPriceType": "Ask",
      "DistanceToMarket": 0.04062,
      "Duration": {
        "DurationType": "GoodTillCancel"
      },
      "IsForceOpen": false,
      "IsMarketOpen": false,
      "MarketPrice": 1.09062,
      "NonTradableReason": "None",
      "OpenOrderType": "Limit",
      "OrderAmountType": "Quantity",
      "OrderId": "49318458",
      "OrderRelation": "StandAlone",
      "OrderTime": "2017-04-12T07:56:00Z",
      "Price": 1.05,
      "Status": "Working",
      "Uic": 21
    }
  ]
}
############################################
########## ポジションと注文の監視５ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/orders/get__port__me
Reference Docs  Portfolio  Orders
Get all open orders for the client to which the logged-in user belongs
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/orders/me?$skip={$skip}&$top={$top}&FieldGroups={FieldGroups}&MultiLegOrderId={MultiLegOrderId}&Status={Status}

Endpoint Description
You can use this operation to get all open orders across all accounts for the client to which the logged-in user belongs.

Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
$skip	Integer	Query-String	The number of entries to skip from the beginning of the collection
$top	Integer	Query-String	The number of entries to return from the beginning of the collection
FieldGroups	OrderFieldGroup []	Query-String	Optional. Specification of FieldGroups to be included in response model. Defaults to "ExchangeInfo" if not provided.
MultiLegOrderId	String	Query-String	Return only multi-leg orders with the given common MultiLegOrderId.
Status	OrderStatusFilter	Query-String	Optional. Selects only a subset of open orders to be returned based on status of the open order. Default is "Working" (i.e. orders related to working orders are excluded).
Response Parameters
View Response Codes
HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
InvalidRequest	Default error code returned when it cannot be determined which part of the request is malformed.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
__count	Number	The total count of items in the feed.
__next	String	The link for the next page of items in the feed.
Data	OrderResponse []	The collection of entities for this feed.
MaxRows	Number	The maximum number of rows that can be returned (if applicable).
Request Example
Request URL
 /port/v1/orders/me?$skip=1&$top=1&FieldGroups=DisplayAndFormat&MultiLegOrderId={MultiLegOrderId}&Status=Working
Response Example
Response body
{
  "__next": "/openapi/port/....../?$top=1&$skip=1",
  "Data": [
    {
      "AccountId": "192134INET",
      "AccountKey": "LZTc7DdejXODf-WSl2aCyQ==",
      "Amount": 250000,
      "AssetType": "FxSpot",
      "BuySell": "Buy",
      "CalculationReliability": "Ok",
      "ClientKey": "7m4I|vtYLUnEGg77o9uQhw==",
      "CurrentPrice": 1.09062,
      "CurrentPriceDelayMinutes": 0,
      "CurrentPriceType": "Ask",
      "DistanceToMarket": 0.04062,
      "Duration": {
        "DurationType": "GoodTillCancel"
      },
      "IsForceOpen": false,
      "IsMarketOpen": false,
      "MarketPrice": 1.09062,
      "NonTradableReason": "None",
      "OpenOrderType": "Limit",
      "OrderAmountType": "Quantity",
      "OrderId": "49318458",
      "OrderRelation": "StandAlone",
      "OrderTime": "2017-04-12T07:56:00Z",
      "Price": 1.05,
      "Status": "Working",
      "Uic": 21
    }
  ]
}
############################################
########## ポジションと注文の監視６ ##########
############################################
https://www.developer.saxo/openapi/referencedocs/port/v1/orders/get__port__clientkey_orderid
Reference Docs  Portfolio  Orders
Get a single open order
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/port/v1/orders/{ClientKey}/{OrderId}?FieldGroups={FieldGroups}

Endpoint Description
Call this operation to get a specific open order of a client.

Endpoint Access Level
Required Permissions:
Community : Read
Personal : Read

Endpoint Parameters
Request parameters
Name	Type	Origin	Description
ClientKey	ClientKey	Route	Unique id of the client.
FieldGroups	OrderFieldGroup []	Query-String	Optional. Specification of FieldGroups to be included in response model. Defaults to "ExchangeInfo" if not provided.
OrderId	String	Route	Unique id of the order.
Response Parameters
View Response Codes
HTTP Code	Description	
200	OK	OK
400	Bad Request	
Error Code	Description
OrderIdNotSpecified	Order not specified.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
__count	Number	The total count of items in the feed.
__next	String	The link for the next page of items in the feed.
Data	OrderResponse []	The collection of entities for this feed.
MaxRows	Number	The maximum number of rows that can be returned (if applicable).
Request Example
Request URL
 /port/v1/orders/U8SNV3JLdN4gzcQfmThXJA==/5007186409?FieldGroups=DisplayAndFormat
Response Example
Response body
{
  "__next": "/openapi/port/....../?$top=1&$skip=1",
  "Data": [
    {
      "AccountId": "192134INET",
      "AccountKey": "LZTc7DdejXODf-WSl2aCyQ==",
      "Amount": 250000,
      "AssetType": "FxSpot",
      "BuySell": "Buy",
      "CalculationReliability": "Ok",
      "ClientKey": "7m4I|vtYLUnEGg77o9uQhw==",
      "CurrentPrice": 1.09062,
      "CurrentPriceDelayMinutes": 0,
      "CurrentPriceType": "Ask",
      "DistanceToMarket": 0.04062,
      "Duration": {
        "DurationType": "GoodTillCancel"
      },
      "IsForceOpen": false,
      "IsMarketOpen": false,
      "MarketPrice": 1.09062,
      "NonTradableReason": "None",
      "OpenOrderType": "Limit",
      "OrderAmountType": "Quantity",
      "OrderId": "49318458",
      "OrderRelation": "StandAlone",
      "OrderTime": "2017-04-12T07:56:00Z",
      "Price": 1.05,
      "Status": "Working",
      "Uic": 21
    }
  ]
}

############################################
######### 監査と履歴 (最終状態の確認) ########
############################################
https://www.developer.saxo/openapi/referencedocs/cs/v1/audit-orderactivities
Reference Docs  Client Services
Audit - OrderActivities
End point for querying order activities

Endpoints
Query Order activities history
Query Order activities history

The __nextPoll link is present when relevant and MUST be used for continuously polling

Our preferred option for continuously fetching order activities is to stream it out of ENS

 https://gateway.saxobank.com/sim/openapi/cs/v1/audit/orderactivities?$skiptoken={$skiptoken}&$top={$top}&AccountKey={AccountKey}&ClientKey={ClientKey}&CorrelationKey={CorrelationKey}&EntryType={EntryType}&FieldGroups={FieldGroups}&FromDateTime={FromDateTime}&IncludeSubAccounts={IncludeSubAccounts}&OrderId={OrderId}&Status={Status}&ToDateTime={ToDateTime}

#################################################
## ENS (Event Notification Service) のセットアップ
#################################################
https://www.developer.saxo/openapi/referencedocs/root/v1/sessions/post__root__events_subscriptions
Reference Docs  Root Services  Sessions
Create a session capabilities subscription
Endpoint Url
 https://gateway.saxobank.com/sim/openapi/root/v1/sessions/events/subscriptions

Endpoint Description
Sets up a new session capabilities subscription. The data stream will deliver updates from this point.

Endpoint Access Level
Endpoint Parameters
Request parameters
Name	Type	Origin	Description
ContextId	String	Body	The streaming context id that this request is associated with. This parameter must only contain letters (a-z) and numbers (0-9) as well as - (dash) and _ (underscore). It is case insensitive. Max length is 50 characters.
Format	String	Body	Optional Media type (RFC 2046) of the serialized data updates that are streamed to the client. Currently only application/json and application/x-protobuf is supported. If an unrecognized format is specified, the subscription end point will return HTTP status code 400 - Bad format.
ReferenceId	String	Body	Mandatory client specified reference id for the subscription. This parameter must only contain alphanumberic characters as well as - (dash) and _ (underscore). Cannot start with _. It is case insensitive. Max length is 50 characters.
RefreshRate	Integer	Body	Optional custom refresh rate, measured in milliseconds, between each data update. Note that it is not possible to get a refresh rate lower than the rate specified in the customer service level agreement (SLA).
ReplaceReferenceId	String	Body	Reference id of the subscription that should be replaced.
Tag	String	Body	Optional client specified tag used for grouping subscriptions.
Response Parameters
View Response Codes
HTTP Code	Description	
201	Created	Created
400	Bad Request	
Error Code	Description
InvalidModelState	Error code returned when model state is invalid.
UnsupportedSubscriptionFormat	Error code returned when a subscription format that isn't supported by the publisher is requested.
401	Unauthorized	Indicates that the request was rejected because the 'Authorization' header was missing in the request or contained an invalid security token.
409	Conflict	
Error Code	Description
SubscriptionLimitExceeded	Error code returned when more than the maximum allowed number of subscriptions for a specified type, is exceeded.
429	Too Many Requests	The request was rejected due to rate limit being exceeded.
503	Service Unavailable	Service Unavailable.

Name	Type	Description
ContextId	String	The streaming context id that this response is associated with.
Format	String	The media type (RFC 2046), of the serialized data updates that are streamed to the client.
InactivityTimeout	Integer	The time (in seconds) that the client should accept the subscription to be inactive before considering it invalid.
ReferenceId	String	The reference id that (along with streaming context id and session id) identifies the subscription (within the context of a specific service/subscription type)
RefreshRate	Integer	Actual refresh rate assigned to the subscription according to the customers SLA.
Snapshot	SessionSubscriptionStreamedState	Snapshot of the current data on hand, when subscription was created.
State	String	This property is kept for backwards compatibility.
Tag	String	Client specified tag assigned to the subscription, if specified in the request.
Streaming Response Parameters
Name	Type	Description
AuthenticationLevel	AuthenticationLevel	Gets or sets the authentication level.
DataLevel	DataLevel	Gets or sets the data level.
TradeLevel	TradeLevel	Gets or sets the trade level.
Request Example
Request URL
 /root/v1/sessions/events/subscriptions
Request Body
{
  "ContextId": "20251206055501800",
  "ReferenceId": "S48648",
  "RefreshRate": 1000,
  "Tag": "PAGE1"
}
Response Example
Response body
{
  "ContextId": "20251206055501800",
  "Format": "application/json",
  "InactivityTimeout": 120,
  "ReferenceId": "S48648",
  "RefreshRate": 1000,
  "Snapshot": {
    "AuthenticationLevel": "Authenticated",
    "DataLevel": "Standard",
    "TradeLevel": "OrdersOnly"
  },
  "State": "Active"
}
Streaming Response Example
Response body
{
  "AuthenticationLevel": "Authenticated",
  "DataLevel": "Standard",
  "TradeLevel": "OrdersOnly"
}

############################################
## ステータスコードと制限 (409, LimitExceeded)
############################################
https://www.developer.saxo/openapi/learn/openapi-request-response
OpenAPI Request/Response

This article provides guidelines for performing simple request/response operations against OpenAPI endpoints. The first part discusses OpenAPI requests and the second part deals with OpenAPI responses, including the possible HTTP response codes being returned.

The article uses Fiddler for taking snapshots of of actual request/responses, but any other web debugging tools such as curl or postman can also be used.

To follow the examples in the article, you will need an OpenAPI access token. When building a real application you would have followed one of the authorization flow described under OAuth Based Authentication Flows for getting the access token.

Structure of an OpenAPI request (headers, body, authorization)
The complete list of available OpenAPI endpoints is provided in the reference documentation. Using this information we decide to send a request to get the balance for the client associated with the current login user. A snapshot of the most simple request & response is given below. (Please note here that we are sending Authorization header with the access token, this is required since using this access token only OpenAPI Service will give access to publicly exposed endpoints):




Headers
HTTP headers are the core part of HTTP requests and responses, and they carry information about the client browser, the requested page, the server and more. Some important HTTP headers in the context of OpenAPI Services are described below:

Accept-Encoding

Consumers of OpenAPI services can indicate through this header in the HTTP request what encoding schemes they support. OpenAPI only supports gzip & deflate compression. If a client sends an Accept-Encoding for an unsupported compression like "sdch" then it ignores the compression header and sends an uncompressed response.

The example shown below sends a GET request for fetching the details of current logged in user and specified Accept-Encoding as deflate , as can be seen in the below response snapshot the request sent by the server is encoded.

 





Authorization

Authorization header should be set with a valid Bearer token for accessing OpenAPI services, More info on this can be found here. Snapshot of a sample request is shown below:





Content-Type 

Consumers need to specify this header for POST,PUT,PATCH requests as this indicates what type of data is getting posted back to the server. In the snapshot shown below since JSON object (request body) is getting posted back , you have to specify Content-Type header as application/json. Content-Type headers are also used for specifying batch requests, More information can be found here.



Supported Verbs
The reference documentation list all the supported Http verbs for a particular resource, so prior to sending the request please refer reference documentation to find out whether that verb is available or not.

Verbs not allowed by firewalls and proxies
Some firewalls and proxies are known to block PUT, PATCH, and DELETE requests and return HTTP status code 405 to the client before the request reaches the server. To work around that, OpenAPI supports HTTP method overrides so that a POST request can be used to simulate a PUT, PATCH, or DELETE request.

To simulate a PUT request, the client should create a POST request with the following extra header:

    X-HTTP-Method-Override: PUT

instructing the OpenAPI service to interpret the request as a PUT. The same pattern applies to PATCH and DELETE.

There is a live sample on diagnostics and method overrides (with source).

CORS(Cross Origin Resource Sharing)
All OpenAPI Services have CORS enabled for all origins, headers and methods.

Query Options
OpenAPI provides query options like top, skip, next etc on based on OData protocol on some endpoints (To find out which endpoints support query option and what options it support please refer to OpenAPI reference documentation). Let's take examples on how to use querying option while querying OpenAPI Services:

Using top & skip option
Example : getting top 3 exchanges after skipping 2 records (request and Response snapshot shown below), don't worry about the _next link shown in the response it is described in detail in the response section of the article.





There is a live sample on query options (with source).

Using fieldGroups
FieldGroups provide a option to send a list or a single fieldGroup column which is desired in the response. Let's explore this with the examples given below:

example 1: project positions data based on DisplayAndFormat fieldGroup, request/response snapshot given below:

As can be seen in the below snapshots we are sending filter 'fieldGroups=DisplayAndFormat' in the request and getting the fieldGroup DisplayAndFormat in the response.





example 2 : lets send multiple fieldGroup DisplayAndFormat,PositionView in the fieldGroups filter and check the response, request/response snapshot given below.As can be seen in the below snapshots we are sending filter 'fieldGroups=DisplayAndFormat,PositionView' in the request and getting both the fieldGroup data in the response.







OpenAPI Request Examples 
GET 
Request/Response snapshot of a sample Get request to the Vas service is given below. This request will bring the price alerts data for current logged in user





POST
Post request for creating a new pricealert definition is shown in the snapshot below.





PUT
Put request for updating the IsRecurring field of price alert definition with id = 532997. (PS: In this request we are sending the full price alert request object in the body)





PATCH
Patch request for changing the culture from "en-GB" to "en-US" is shown below.
(Please note that we are not passing the full object as was the case with the PUT example above - hence PATCH is considered to be more efficient than PUT):



DELETE
Delete request for removing a price alert definition with id= 532875 is shown below:



Structure of an OpenAPI Response
We need to refer to reference documentation for finding out the OpenAPI Response structure. The Reference documentation has detailed information about the response structure as well as samples to get you started. Let's say you want to get the exchange from OpenAPI Service, then go to the reference documentation  and click exchanges under resources section (on the left hand side) as is shown below:



The above snapshot shows two endpoints exposed on this resource. The first is to get all the exchanges and second is to get a specific exchange. Let's say you are interested in getting all the exchanges and find out more about this endpoint as to what the request parameters are going to be and what's the response structure going to be, Click Quick view to see the response structure as shown below:



Versioning Policy
Please refer Versioning and Obsolescence Policy page to know about the versioning policy of OpenAPI.

”Null fields are generally ‘left out’”
Response from OpenAPI Services generally ignores null fields and those do not get serialized. For example, in the above snapshot of Exchanges, if the service did not have a value for the "Name" field, then there would not be a "Name" property in the response object.

When writing a client application always take into consideration that some fields may not be returned in the response object. Your application should be able to handle this gracefully.

__next... /Data...
while using OpenAPI Query options(like $top,$skip etc) as is specified above in OpenAPI Request section, OpenAPI response sends response packed into two fields

a.  Data: this will give data based on the request and filtering options specified in the request.

b. _next: will give the link for accessing the next page of items in the feed, So if we send a request https://developer.saxobank.com/sim/openapi/ref/v1/exchanges?$top=3&$skip=2 (for getting top 3 items after skipping first 2) next link will be https://developer.saxobank.com/sim/openapi/ref/v1/exchanges?$top=3&$skip=5 ( since next page will be top 3 items after skipping 5 items).





Response Codes
OpenAPI end points may return any of the following HTTP response codes:

Response code	Domain Error Code	Description
200	
Ok, for GET and Options requests.
201	
Created, for POST requests. Additional data is returned in the response.
204	
Succes, No content for DELETE, PATCH and PUT requests.
400	Yes	Bad Request, See domain error code for additional information.
401	
Unauthorized.
403	
Forbidden
404	
Not Found
429	
Too many requests. Returned if request quotas are exceeded. 
500	
Internal service error.
503	
Service Unavailable.


Responses with response code 400 return additional information in the response body in the form of an error structure as outlined below:

HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
  
{
  "ErrorCode":"InvalidModelState",  
  "Message":"One or more properties of the request are invalid!",
  "ModelState":
   {
     "$skip":["Invalid $skip query parameter value: 2s"]
   },
}
ErrorCode and Message are always returned, where as ModelState is only returned for a few specific error codes.

If included, the ModelState, is an object containing key value pairs of fields with invalid contents along with an array of error texts relevant for the individual field.



Generic and domain specific error codes
Error codes are either generic or domain specific. The generic ones are listed below., They may be returned from any endpoint.

Error code	Include model state	Description
InvalidRequest	No	Default error code returned when it cannot be determined which part of the request is malformed.
InvalidRequestHeader	Yes	
Error code returned when one or more of the request headers are invalid.
Used when the specific request header cannot be determined.

InvalidMediaTypeHeader	Yes	Error code returned when the Accept or Content-Type headers contains an invalid media type or is malformed.
InvalidAcceptLanguageHeader	Yes	Error code returned when the Accept-Language header contains an invalid language or is malformed.
InvalidQueryParameters	Yes	Error code returned from query end points, when query parameters are invalid.
InvalidModelState	Yes	Error code returned when model state is invalid.
TypeConversionError	Yes	Error code returned when type-conversion failed (TypeConverter's and ModelBinder's).
SubscriptionLimitExceeded	No	Error code returned when more than the maximum allowed number of subscriptions for a specified type, is exceeded
RateLimitExceeded	No	Error code returned when a throttling policy quota has been exceeded.
FeatureNotEnabled	No	Error code returned when an Open Api feature has been disabled via Front Office.
InternalTimeout	No	Error code returned when a timeout occurs internally in the application.
UnsupportedSubscriptionFormat	Yes	Error code returned when a subscription format that isn't supported by the publisher is requested.
RequestNotAllowed	No	Error code returned if a request is not allowed.
DomainValidationError	Yes	Error code returned when domain validation fails.


Documentation of Error Codes in the reference documentation
The Response Codes section of the reference documentation provides an overview of the possible response codes for a specific operation.

For reasons of brevity the list does not include the full list of generic error codes.

With respect to the domains specific errors, we only list the most frequently occurring error codes as well those, where it may make sense for the receiving application to make a decision. There may be more error codes returned than those listed, but for the client application, the only sensible action is really to log and/or display such errors.

HTTP Expect: 100 Continue NOT supported
A few client libraries may implement the transmission of an HTTP Expect: 100-Continue request header. The expectation is that the server will respond with a 100-Continue, and the client will subsequently send the actual request body. This two-step process is intended to save bandwidth between the client and server if the payload to be transmitted is very large (such as a file upload). In such situations the server could - for example - check for invalid authentication and reject the initial 100-Continue request, thus avoiding the subsequent file upload and thereby save bandwidth.

In our experience the same two-step process has been difficult to get to work reliable, especially as we support clients world wide, who connect to us through a multitude of network gateways and proxies. We also find that the actual bandwidth savings for the majority of API requests are limited, since most requests are quite small.

We therefore strongly recommend against using the Expect:100-Continue header, and expect you to make sure your client library does not rely on this mechanism.



See also the live sample on error handling (with source).
############################################
########## ポジションと注文の監視１ ##########
############################################
############################################
########## ポジションと注文の監視１ ##########
############################################
