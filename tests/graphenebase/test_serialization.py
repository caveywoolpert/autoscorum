from binascii import hexlify

from graphenebase.types import BudgetType
from graphenebase.amount import Amount
from graphenebase.signedtransactions import SignedTransaction
from src.operations_fabric import devpool_withdraw_vesting, create_budget_operation


def test_serialize_banner_to_string():
    x = BudgetType("banner")
    assert str(x) == "banner"


def test_serialize_post_to_string():
    x = BudgetType("post")
    assert str(x) == "post"


def test_serialize_banner_to_byte():
    x = BudgetType("banner")
    assert hexlify(bytes(x)) == b'0100000000000000'


def test_serialize_post_to_byte():
    x = BudgetType("post")
    assert hexlify(bytes(x)) == b'0000000000000000'


def test_serialize_create_budget_to_byte():
    op = create_budget_operation(
        "initdelegate", "{}", Amount("10.000000000 SCR"), "2018-08-03T10:12:43", "2018-08-03T10:13:13", "post"
    )
    signed_ops = SignedTransaction.cast_operations_to_array_of_opklass([op])
    result_bin = b'1a00000000000000000c696e697464656c6567617465027b7d00e40b540200000009534352000000009b2a645bb92a645b'
    assert hexlify(bytes(signed_ops.data[0])) == result_bin


def test_serialize_devpool_withdraw_vesting_proposal_create_to_byte():
    op = devpool_withdraw_vesting("initdelegate", Amount("10.000000000 SP"), 86400)
    signed_ops = SignedTransaction.cast_operations_to_array_of_opklass([op])

    result_bin = b'1d0c696e697464656c6567617465805101000600e40b54020000000953500000000000'
    assert hexlify(bytes(signed_ops.data[0])) == result_bin
