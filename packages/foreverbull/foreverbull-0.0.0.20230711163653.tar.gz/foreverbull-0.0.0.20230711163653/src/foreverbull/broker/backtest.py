import requests

from .http import api_call


@api_call
def create(backtest_service: str) -> requests.Request:
    return requests.Request(
        method="PUT",
        url="/api/v1/backtests",
        json={"backtest_service": backtest_service},
    )


@api_call
def get(id: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/backtests/{id}",
    )


@api_call
def get_execution(execution_id: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/backtests/executions/{execution_id}",
    )
