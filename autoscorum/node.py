import tempfile
import os

from pathlib import Path
from hashlib import sha256

from .config import Config
from . import utils


TEST_TEMP_DIR = '/tmp/autoscorum'

chain_params = {"chain_id": None,
                "prefix": "SCR",
                "scorum_symbol": "SCR",
                "sp_symbol": "SP",
                "scorum_prec": 9,
                "sp_prec": 9}


class Node(object):
    def __init__(self, config=Config(), genesis=None, logging=True):
        self._bin_path = None
        self.config = config
        self._genesis = genesis
        self.logging = logging
        self.logs = ""
        self.rpc_endpoint = None

    @staticmethod
    def check_binaries():
        bin_path = Path(utils.which(SCORUM_BIN))
        assert bin_path.exists(), "scorumd does not exists"
        assert bin_path.is_file(), "scorumd is not a file"

    def get_chain_id(self):
        if not chain_params["chain_id"]:
            for line in self.logs:
                if "node chain ID:" in line:
                    chain_params["chain_id"] = line.split(" ")[-1]
        return chain_params["chain_id"]

    def setup(self):
        dir_name = os.path.basename(tempfile.mktemp(self.config['witness'][1:-1]))

        genesis_path = os.path.join(TEST_TEMP_DIR, dir_name, 'genesis.json')
        config_path = os.path.join(TEST_TEMP_DIR, dir_name, 'config.ini')

        if not os.path.exists(os.path.dirname(genesis_path)):
            os.makedirs(os.path.dirname(genesis_path))

        with open(genesis_path, 'w') as genesis:
            g = self._genesis.dump()
            genesis.write(g)
            chain_params["chain_id"] = sha256(g.encode()).hexdigest()
        with open(config_path, 'w') as config:
            config.write(self.config.dump())

        return os.path.dirname(genesis_path)
