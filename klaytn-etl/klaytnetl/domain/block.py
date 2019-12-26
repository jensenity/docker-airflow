# MIT License
#
# Copyright (c) 2019 Jettson Lim, jettson.lim@groundx.xyz
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from klaytnetl.utils import strf_unix_dt

class EthBlock(object):
    def __init__(self):
        self.number = None
        self.hash = None
        self.parent_hash = None
        self.logs_bloom = None
        self.transactions_root = None
        self.state_root = None
        self.receipts_root = None
        self.size = None
        self.extra_data = None
        self.gas_limit = None
        self.gas_used = None
        self.timestamp = None
        self.timestamp_fos = None    # Quantity: The fraction of a second of the timestamp

        self.transactions = []
        self.transaction_count = 0

        self.block_score = None
        self.total_block_score = None

        self.governance_data = None  # Data: RLP encoded data
        self.vote_data = None        # Data: RLP encoded data

        self.committee = []
        self.proposer = None
        self.reward_address = None


class KlaytnRawBlock(object):
    def __init__(self):
        self.number = None
        self.hash = None
        self.parent_hash = None
        self.logs_bloom = None
        self.transactions_root = None
        self.state_root = None
        self.receipts_root = None

        self.size = None
        self.extra_data = None
        self.gas_limit = None
        self.gas_used = None
        self.timestamp = 0           # NOTE: Default (UNIX Epoch time = 0.0)
        self.timestamp_fos = 0       # Quantity: The fraction of a second of the timestamp

        self.transactions = []
        self.transaction_count = 0

        self.receipts = []

        self.block_score = None
        self.total_block_score = None

        self.governance_data = None  # Data: RLP encoded data
        self.vote_data = None        # Data: RLP encoded data

        self.committee = []
        self.proposer = None
        self.reward_address = None


class KlaytnBlock(KlaytnRawBlock):
    def __init__(self):
        super(KlaytnBlock, self).__init__()

        self.unix_timestamp = 0.0    # timestamp with fos
        self.timestamp = None        # UTC timestamp

        # delete
        del self.timestamp_fos
        del self.receipts

    @staticmethod
    def enrich(raw_block: KlaytnRawBlock):
        block = KlaytnBlock()

        for k, v in raw_block.__dict__.items():
            if hasattr(block, k):
                block.__setattr__(k, v)

        block.unix_timestamp = (raw_block.timestamp * 1.0) + (raw_block.timestamp_fos * 0.001)
        block.timestamp = strf_unix_dt(block.unix_timestamp)

        return block
