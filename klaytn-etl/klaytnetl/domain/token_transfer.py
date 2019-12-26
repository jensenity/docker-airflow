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

class EthTokenTransfer(object):
    def __init__(self):
        self.token_address = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.transaction_hash = None
        self.log_index = None
        self.block_number = None

class KlaytnRawTokenTransfer(object):
    def __init__(self):
        self.token_address = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.log_index = None
        self.transaction_hash = None
        self.transaction_index = None
        self.block_hash = None
        self.block_number = None

class KlaytnTokenTransfer(KlaytnRawTokenTransfer):
    def __init__(self):
        super(KlaytnTokenTransfer, self).__init__()

        self.block_timestamp = None
        self.block_unix_timestamp = 0.0
        self.transaction_receipt_status = None

    @staticmethod
    def enrich(raw_token_transfers: KlaytnRawTokenTransfer, block_timestamp, block_timestamp_fos, transaction_receipt_status):
        token_transfer = KlaytnTokenTransfer()

        for k, v in raw_token_transfers.__dict__.items():
            if hasattr(token_transfer, k):
                token_transfer.__setattr__(k, v)

        # transactions
        token_transfer.block_unix_timestamp = (block_timestamp * 1.0) + (block_timestamp_fos * 0.001)
        token_transfer.block_timestamp = strf_unix_dt(token_transfer.block_unix_timestamp)

        # receipt info
        token_transfer.transaction_receipt_status = transaction_receipt_status

        return token_transfer