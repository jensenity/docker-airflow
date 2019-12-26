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

class EthTransaction(object):
    def __init__(self):
        self.hash = None
        self.nonce = None
        self.block_hash = None
        self.block_number = None
        self.block_timestamp = 0        # NOTE: Default (UNIX Epoch time = 0)
        self.transaction_index = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.gas = None
        self.gas_price = None
        self.input = None

        # Klaytn additional properties
        self.fee_payer = None           # Data: 20 byte, address of the fee payer.
        self.fee_payer_signatures = []  # Array: An array of fee payer's signature objects. A signature object contains three fields (V, R, and S).
        self.fee_ratio = 0              # Fee ratio of the fee payer. If it is 30, 30% of the fee will be paid by the fee payer.

        self.sender_tx_hash = None      # Data: 32 byte, Hash of the tx without the fee payer's address and signature.
        self.signatures = []            # Array: An array of signature objects. A signature object contains three fields (V, R, and S).

        self.tx_type = None             # String: A string representing the type of the transaction.
        self.tx_type_int = None         # Quantity: An integer representing the type of the transaction.


class KlaytnRawTransaction(object):
    def __init__(self):
        self.hash = None
        self.nonce = None
        self.block_hash = None
        self.block_number = None
        self.transaction_index = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.gas = None
        self.gas_price = None
        self.input = None

        self.logs = []

        self.fee_payer = None           # Data: 20 byte, address of the fee payer.
        self.fee_payer_signatures = []  # Array: An array of fee payer's signature objects. A signature object contains three fields (V, R, and S).
        self.fee_ratio = 0              # Fee ratio of the fee payer. If it is 30, 30% of the fee will be paid by the fee payer.

        self.sender_tx_hash = None      # Data: 32 byte, Hash of the tx without the fee payer's address and signature.
        self.signatures = []            # Array: An array of signature objects. A signature object contains three fields (V, R, and S).

        self.tx_type = None             # String: A string representing the type of the transaction.
        self.tx_type_int = None         # Quantity: An integer representing the type of the transaction.


class KlaytnTransaction(KlaytnRawTransaction):
    def __init__(self):
        super(KlaytnTransaction, self).__init__()

        self.block_unix_timestamp = 0.0       # timestamp with fos
        self.block_timestamp = None           # UTC timestamp
        self.receipt_gas_used = None          # gas used to execute the transaction
        self.receipt_contract_address = None  # created contact
        self.receipt_status = None            # receipt status

    @staticmethod
    def enrich(raw_transaction: KlaytnRawTransaction, block_timestamp, block_timestamp_fos, receipt_gas_used, receipt_contract_address, receipt_status):
        transaction = KlaytnTransaction()

        for k, v in raw_transaction.__dict__.items():
            if hasattr(transaction, k):
                transaction.__setattr__(k, v)

        # timestamps
        transaction.block_unix_timestamp = (block_timestamp * 1.0) + (block_timestamp_fos * 0.001)
        transaction.block_timestamp = strf_unix_dt(transaction.block_unix_timestamp)

        # receipt info
        transaction.receipt_gas_used = receipt_gas_used
        transaction.receipt_contract_address = receipt_contract_address
        transaction.receipt_status = receipt_status

        # missing to address
        transaction.to_address = raw_transaction.to_address if raw_transaction.to_address is not None else receipt_contract_address

        return transaction