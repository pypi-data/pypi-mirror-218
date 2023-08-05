from tarvis.atb import atbs
import tarvis.exchange.binance
import tarvis.exchange.dydx
import tarvis.exchange.woo
import tarvis.indicators.webapi
from tarvis.indicators.webapi import WebAPIIndicatorSource


def main():
    atbs.run(
        indicator_source_classes=[WebAPIIndicatorSource],
        exchange_classes=[
            tarvis.exchange.binance.BinanceExchange,
            tarvis.exchange.dydx.DYDXExchange,
            tarvis.exchange.woo.WooExchange,
        ],
        additional_providers=None,
        additional_modules=[tarvis.indicators.webapi],
    )


if __name__ == "__main__":
    main()
