from autoscorum.node import Node
from steembase.http_client import HttpClient


default_genesis = {
    "initial_timestamp": "2017-11-29T10:03:00",
    "init_supply": 1000,
    "accounts": [{
        "name": "initdelegate",
        "recovery_account": "",
        "public_key": "SCR7R1p6GyZ3QjW3LrDayEy9jxbbBtPo9SDajH5QspVdweADi7bBi",
        "scr_amount": 1000,
        "sp_amount": 0
    }, {
        "name": "alice",
        "recovery_account": "",
        "public_key": "SCR8TBVkvbJ79L1A4e851LETG8jurXFPzHPz87obyQQFESxy8pmdx",
        "scr_amount": 0,
        "sp_amount": 0
    }, {
        "name": "bob",
        "recovery_account": "",
        "public_key": "SCR7w8tySAVQmJ95xSL8SS2GJJCws9s2gCY85DSAEALMFPmaMKA6p",
        "scr_amount": 0,
        "sp_amount": 0
    }],

    "witness_candidates": [{
        "owner_name": "initdelegate",
        "block_signing_key": "SCR7R1p6GyZ3QjW3LrDayEy9jxbbBtPo9SDajH5QspVdweADi7bBi"
    }, {
        "owner_name": "alice",
        "block_signing_key": "SCR8TBVkvbJ79L1A4e851LETG8jurXFPzHPz87obyQQFESxy8pmdx"
    }, {
        "owner_name": "bob",
        "block_signing_key": "SCR7w8tySAVQmJ95xSL8SS2GJJCws9s2gCY85DSAEALMFPmaMKA6p"
    }]
}

initdelegate_private_key = "5K8ZJUYs9SP47JgzUY97ogDw1da37yuLrSF5syj2Wr4GEvPWok6"


def test_block_production():
    initdelegate = Node(genesis=default_genesis)
    initdelegate.config['rpc-endpoint'] = '0.0.0.0:8090'
    initdelegate.config['witness'] = '"initdelegate"'
    initdelegate.config['private-key'] = initdelegate_private_key
    initdelegate.run()

    rpc = HttpClient([initdelegate.addr])
    block = rpc.exec('get_block', '1')
    assert block['witness'] == initdelegate.config['witness'][1:-1]
    initdelegate.stop()
























