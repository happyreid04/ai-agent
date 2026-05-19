import std/json
import std/strutils
import std/math
proc calcSignals(btc_change: float, eth_change: float): JsonNode =
    let avg = (btc_change + eth_change) / 2.0
    let momentum = sqrt(btc_change * btc_change + eth_change * eth_change)
    let agreement = (btc_change > 0) == (eth_change > 0)
    result = %*{
        "btc_change": btc_change,
        "eth_change": eth_change,
        "avg_change": avg,
        "momentum": momentum,
        "agreement": agreement,
        "both_positive": btc_change > 0 and eth_change > 0,
        "both_negative": btc_change < 0 and eth_change < 0
    }
let input = parseJson(stdin.readLine())
let btc_change = input["btc_change"].getFloat()
let eth_change = input["eth_change"].getFloat()
let signals = calcSignals(btc_change, eth_change)
echo signals



