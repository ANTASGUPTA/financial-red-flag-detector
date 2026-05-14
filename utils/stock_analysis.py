import yfinance as yf
from datetime import datetime, timedelta


def get_stock_reaction(ticker, filing_date):

    try:

        filing_dt = datetime.strptime(
            filing_date,
            "%Y-%m-%d"
        )

        start_date = (
            filing_dt - timedelta(days=7)
        ).strftime("%Y-%m-%d")

        end_date = (
            filing_dt + timedelta(days=7)
        ).strftime("%Y-%m-%d")

        stock = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False
        )

        if stock.empty:
            return None

        stock = stock.reset_index()

        # Force proper columns
        stock.columns = [
            col[0] if isinstance(col, tuple)
            else col
            for col in stock.columns
        ]

        # Convert Date column
        stock['Date'] = stock['Date'].astype(str)

        filing_date_str = filing_dt.strftime(
            "%Y-%m-%d"
        )

        # Find closest trading day
        closest_index = 0
        smallest_diff = None

        for i in range(len(stock)):

            current_date = datetime.strptime(
                stock.iloc[i]['Date'],
                "%Y-%m-%d"
            )

            diff = abs(
                (
                    current_date - filing_dt
                ).days
            )

            if (
                smallest_diff is None
                or diff < smallest_diff
            ):

                smallest_diff = diff
                closest_index = i

        if closest_index == 0:
            return None

        if closest_index >= len(stock) - 1:
            return None

        previous_close = float(
            stock.iloc[closest_index - 1]['Close']
        )

        filing_close = float(
            stock.iloc[closest_index]['Close']
        )

        next_close = float(
            stock.iloc[closest_index + 1]['Close']
        )

        change_percent = (
            (
                next_close - previous_close
            )
            / previous_close
        ) * 100

        return {
            "previous_close":
                round(previous_close, 2),

            "filing_close":
                round(filing_close, 2),

            "next_close":
                round(next_close, 2),

            "change_percent":
                round(change_percent, 2)
        }

    except Exception as e:

        print("Stock reaction error:", e)

        return None
    