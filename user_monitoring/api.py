from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from flask import Blueprint, current_app, request, jsonify

api = Blueprint("api", __name__)

#class declaration for incoming and outgoing requests
@dataclass
class UserRequest:
    transaction_type: str
    amount: str
    user_id: int
    time: int

@dataclass
class ReturnRequest:
    alert: bool
    alert_codes: List[int]
    user_id: int

#creates user_transaction dictionary (holds the requests by user_id)
user_transactions: Dict[int, List[UserRequest]] = defaultdict(list)


@api.post("/event")
def handle_user_event() -> dict:
    current_app.logger.info("Handling user event")

    data = request.get_json()
    if not data:
        return {"error": "Invalid JSON data", "status_code": 400}

    try:
        user_request = UserRequest(
            transaction_type=data["type"],
            amount=data["amount"],
            user_id=data["user_id"],
            time=data["time"]
        )
    except KeyError as e:
        return {"error": f"Missing key: {str(e)}", "status_code": 400}

    current_app.logger.info(f"Received request: {user_request}")

    user_transactions[user_request.user_id].append(user_request)

    #calls the alert check for the request
    return_request = alert_check(user_request)

    return return_request.__dict__


def alert_check(user_request: UserRequest) -> ReturnRequest:
    #creates the default return
    return_request = ReturnRequest(
        alert=False,
        alert_codes=[],
        user_id=user_request.user_id
    )
    #calls the checks individually
    return_request = withdrawal_limit(user_request, return_request)
    return_request = consecutive_withdrawals(user_request, return_request)
    return_request = consecutive_large_deposits(user_request, return_request)
    return_request = total_deposits_in_window(user_request, return_request)

    return return_request


# checks if the transaction is a withdrawal and is > 100
def withdrawal_limit(user_request: UserRequest, return_request: ReturnRequest) -> ReturnRequest:
    if user_request.transaction_type == "withdrawal" and float(user_request.amount) > 100:
        return_request.alert = True
        return_request.alert_codes.append(1100)
    return return_request


# checks if the user's last 3 transactions have been withdrawals
def consecutive_withdrawals(user_request: UserRequest, return_request: ReturnRequest) -> ReturnRequest:
    transactions = user_transactions[user_request.user_id]
    #if its < 3 then they don't have 3 transactions to compare
    if len(transactions) >= 3:
        last_three = transactions[-3:]
        if all(tx.transaction_type == "withdrawal" for tx in last_three):
            return_request.alert = True
            return_request.alert_codes.append(30)
    return return_request

def consecutive_large_deposits(user_request: UserRequest, return_request: ReturnRequest) -> ReturnRequest:
    transactions = user_transactions[user_request.user_id]
    # filter the transactions to get only deposits
    deposits = [tx for tx in transactions if tx.transaction_type == "deposit"]
    #if its < 3 then they don't have 3 transactions to compare
    if len(deposits) >= 3:
        last_three = deposits[-3:]
        if float(last_three[0].amount) < float(last_three[1].amount) < float(last_three[2].amount):
            return_request.alert = True
            return_request.alert_codes.append(300)
    return return_request


def total_deposits_in_window(user_request: UserRequest, return_request: ReturnRequest) -> ReturnRequest:
    transactions = user_transactions[user_request.user_id]
    # filter the transactions to get only deposits
    deposits = [tx for tx in transactions if tx.transaction_type == "deposit"]
    # filters the transactions to get the transactions within the last 30
    recent_deposits = [tx for tx in deposits if user_request.time - tx.time <= 30]
    total_amount = sum(float(tx.amount) for tx in recent_deposits)

    if total_amount > 200:
        return_request.alert = True
        return_request.alert_codes.append(123)

    return return_request