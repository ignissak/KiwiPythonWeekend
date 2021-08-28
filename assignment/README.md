# Jakub Bordáš - Python Weekend Task 2021
Dear Kiwi team, this is my solution of Python Weekend's entry task. Thank you for the opportunity to get into this great program.
## How to run script?

Let's say our dataset is in `data/dataset.csv` and we want to find flights from DHE and NRX 
with minimum of 2 bags and maximum price ber bag should be 9. In order to search this query we need to use:
```
python -m main data/dataset.csv DHE NRX --bags=2 --max_bag_price=9
```
First three positional arguments (`dataset file`, `origin location` and `destination location`) are required.

## All usable arguments
| Argument name     | Type | Description                                                | Notes                      |
|-------------------|------|------------------------------------------------------------|----------------------------|
| `--bags`          | int  | Number of requested bags                                   | Optional (default = 0)     |
| `--max_price`     | int  | Maximum price for trip (including required amount of bags) | Optional                   |
| `--max_bag_price` | int  | Maximum price per bag                                      | Optional                   |
| `--disable_transfer_flights` | bool | Should disable transfer flights?                | Optional (default = false) |
| `--return-flight` | bool | Should also search for a return flight(s)?                 | Optional (default = false) |
These arguments can also be viewed by using help command: `python -m main -h`.

## Example
Command 1: `python -m main data/dataset.csv DHE NRX --bags=2 --return_flight`

Result 1:
```json
[
    {
        "flights": [
            {
                "flight_no": "XD231",
                "origin": "DHE",
                "destination": "NRX",
                "departure": "2021-09-02T05:00:00",
                "arrival": "2021-09-02T08:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "IM286",
                "origin": "NRX",
                "destination": "DHE",
                "departure": "2021-09-02T12:15:00",
                "arrival": "2021-09-02T14:50:00",
                "base_price": "38.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 62.0,
        "bag_price": 36,
        "total_price": 98.0,
        "travel_time": "9:50:00"
    },
    {
        "flights": [
            {
                "flight_no": "XD231",
                "origin": "DHE",
                "destination": "NRX",
                "departure": "2021-09-02T05:00:00",
                "arrival": "2021-09-02T08:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "IM286",
                "origin": "NRX",
                "destination": "DHE",
                "departure": "2021-09-05T12:15:00",
                "arrival": "2021-09-05T14:50:00",
                "base_price": "38.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 62.0,
        "bag_price": 36,
        "total_price": 98.0,
        "travel_time": "3 days, 9:50:00"
    },
    {
        "flights": [
            {
                "flight_no": "XD231",
                "origin": "DHE",
                "destination": "NRX",
                "departure": "2021-09-02T05:00:00",
                "arrival": "2021-09-02T08:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "IM286",
                "origin": "NRX",
                "destination": "DHE",
                "departure": "2021-09-10T12:15:00",
                "arrival": "2021-09-10T14:50:00",
                "base_price": "38.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 62.0,
        "bag_price": 36,
        "total_price": 98.0,
        "travel_time": "8 days, 9:50:00"
    },
    {
        "flights": [
            {
                "flight_no": "XD231",
                "origin": "DHE",
                "destination": "NRX",
                "departure": "2021-09-02T05:00:00",
                "arrival": "2021-09-02T08:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "XD335",
                "origin": "NRX",
                "destination": "DHE",
                "departure": "2021-09-16T00:30:00",
                "arrival": "2021-09-16T02:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 48.0,
        "bag_price": 36,
        "total_price": 84.0,
        "travel_time": "13 days, 21:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "XD231",
                "origin": "DHE",
                "destination": "NRX",
                "departure": "2021-09-15T05:00:00",
                "arrival": "2021-09-15T08:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "XD335",
                "origin": "NRX",
                "destination": "DHE",
                "departure": "2021-09-16T00:30:00",
                "arrival": "2021-09-16T02:00:00",
                "base_price": "24.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 48.0,
        "bag_price": 36,
        "total_price": 84.0,
        "travel_time": "21:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "WM478",
                "origin": "DHE",
                "destination": "NIZ",
                "departure": "2021-09-01T00:40:00",
                "arrival": "2021-09-01T05:50:00",
                "base_price": "248.0",
                "bag_price": "12",
                "bags_allowed": "2"
            },
            {
                "flight_no": "IM567",
                "origin": "NIZ",
                "destination": "NRX",
                "departure": "2021-09-01T10:15:00",
                "arrival": "2021-09-01T14:25:00",
                "base_price": "51.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "IM567",
                "origin": "NRX",
                "destination": "NIZ",
                "departure": "2021-09-01T16:05:00",
                "arrival": "2021-09-01T18:15:00",
                "base_price": "51.0",
                "bag_price": "9",
                "bags_allowed": "2"
            },
            {
                "flight_no": "YYYYY",
                "origin": "NIZ",
                "destination": "DHE",
                "departure": "2021-09-01T21:00:00",
                "arrival": "2021-09-02T00:15:00",
                "base_price": "51.0",
                "bag_price": "9",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": 2,
        "bags_count": 2,
        "destination": "NRX",
        "origin": "DHE",
        "flight_price": 401.0,
        "bag_price": 78,
        "total_price": 479.0,
        "travel_time": "23:35:00"
    }
]

```

Command 2: `python -m main data/dataset.csv SML NIZ`

Result 2:
```json
[
    {
        "flights": {
            "flight_no": "IM218",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-02T04:35:00",
            "arrival": "2021-09-02T08:40:00",
            "base_price": "120.0",
            "bag_price": "9",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 120.0,
        "bag_price": 9,
        "total_price": 129.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "WM094",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-02T06:30:00",
            "arrival": "2021-09-02T10:35:00",
            "base_price": "122.0",
            "bag_price": "12",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 122.0,
        "bag_price": 12,
        "total_price": 134.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "WM094",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-03T06:30:00",
            "arrival": "2021-09-03T10:35:00",
            "base_price": "122.0",
            "bag_price": "12",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 122.0,
        "bag_price": 12,
        "total_price": 134.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "IM218",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-04T04:35:00",
            "arrival": "2021-09-04T08:40:00",
            "base_price": "120.0",
            "bag_price": "9",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 120.0,
        "bag_price": 9,
        "total_price": 129.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "WM094",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-07T06:30:00",
            "arrival": "2021-09-07T10:35:00",
            "base_price": "122.0",
            "bag_price": "12",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 122.0,
        "bag_price": 12,
        "total_price": 134.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "IM218",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-08T04:35:00",
            "arrival": "2021-09-08T08:40:00",
            "base_price": "120.0",
            "bag_price": "9",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 120.0,
        "bag_price": 9,
        "total_price": 129.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "WM094",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-12T06:30:00",
            "arrival": "2021-09-12T10:35:00",
            "base_price": "122.0",
            "bag_price": "12",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 122.0,
        "bag_price": 12,
        "total_price": 134.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "IM218",
            "origin": "SML",
            "destination": "NIZ",
            "departure": "2021-09-13T04:35:00",
            "arrival": "2021-09-13T08:40:00",
            "base_price": "120.0",
            "bag_price": "9",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 120.0,
        "bag_price": 9,
        "total_price": 129.0,
        "travel_time": "4:05:00"
    },
    {
        "flights": {
            "flight_no": "WM395",
            "origin": "SML",
            "destination": "NRX",
            "departure": "2021-09-02T01:00:00",
            "arrival": "2021-09-02T03:20:00",
            "base_price": "52.0",
            "bag_price": "12",
            "bags_allowed": "1"
        },
        "bags_allowed": 1,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 52.0,
        "bag_price": 12,
        "total_price": 64.0,
        "travel_time": "2:20:00"
    },
    {
        "flights": {
            "flight_no": "IM567",
            "origin": "NRX",
            "destination": "NIZ",
            "departure": "2021-09-02T06:05:00",
            "arrival": "2021-09-02T09:15:00",
            "base_price": "51.0",
            "bag_price": "9",
            "bags_allowed": "2"
        },
        "bags_allowed": 2,
        "bags_count": 0,
        "destination": "NIZ",
        "origin": "SML",
        "flight_price": 51.0,
        "bag_price": 9,
        "total_price": 60.0,
        "travel_time": "3:10:00"
    }
]

```