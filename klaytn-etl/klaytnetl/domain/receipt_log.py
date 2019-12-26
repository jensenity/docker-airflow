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

class EthReceiptLog(object):
    def __init__(self):
        self.log_index = None
        self.transaction_hash = None
        self.transaction_index = None
        self.block_hash = None
        self.block_number = None
        self.address = None
        self.data = None
        self.topics = []

class KlaytnRawReceiptLog(object):
    def __init__(self):
        self.log_index = None

        self.transaction_hash = None
        self.transaction_index = None

        self.block_hash = None
        self.block_number = None

        self.address = None
        self.data = None
        self.topics = []

    


class KlaytnReceiptLog(KlaytnRawReceiptLog):
    def __init__(self):
        super(KlaytnReceiptLog, self).__init__()

        self.block_timestamp = 0.0
        self.block_unix_timestamp = None
        self.transaction_receipt_status = None

    
    @staticmethod
    def enrich(raw_logs: KlaytnRawReceiptLog, block_timestamp, block_timestamp_fos, transaction_receipt_status):
        log = KlaytnReceiptLog()

        for k, v in raw_logs.__dict__.items():
            if hasattr(log, k):
                log.__setattr__(k, v)

        # transactions
        log.block_unix_timestamp = (block_timestamp * 1.0) + (block_timestamp_fos * 0.001)
        log.block_timestamp = strf_unix_dt(log.block_unix_timestamp)

        # receipt info
        log.transaction_receipt_status = transaction_receipt_status

        return log