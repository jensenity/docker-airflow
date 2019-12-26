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


from klaytnetl.domain.receipt_log import EthReceiptLog
from klaytnetl.domain.receipt_log import KlaytnReceiptLog, KlaytnRawReceiptLog
from klaytnetl.utils import hex_to_dec

from typing import Union

class EthReceiptLogMapper(object):

    def json_dict_to_receipt_log(self, json_dict):
        receipt_log = EthReceiptLog()

        receipt_log.log_index = hex_to_dec(json_dict.get('logIndex'))
        receipt_log.transaction_hash = json_dict.get('transactionHash')
        receipt_log.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))
        receipt_log.block_hash = json_dict.get('blockHash')
        receipt_log.block_number = hex_to_dec(json_dict.get('blockNumber'))
        receipt_log.address = json_dict.get('address')
        receipt_log.data = json_dict.get('data')
        receipt_log.topics = json_dict.get('topics')

        return receipt_log

    def web3_dict_to_receipt_log(self, dict):

        receipt_log = EthReceiptLog()

        receipt_log.log_index = dict.get('logIndex')

        transaction_hash = dict.get('transactionHash')
        if transaction_hash is not None:
            transaction_hash = transaction_hash.hex()
        receipt_log.transaction_hash = transaction_hash

        block_hash = dict.get('blockHash')
        if block_hash is not None:
            block_hash = block_hash.hex()
        receipt_log.block_hash = block_hash

        receipt_log.block_number = dict.get('blockNumber')
        receipt_log.address = dict.get('address')
        receipt_log.data = dict.get('data')

        if 'topics' in dict:
            receipt_log.topics = [topic.hex() for topic in dict['topics']]

        return receipt_log

    def receipt_log_to_dict(self, receipt_log):
        return {
            'type': 'log',
            'log_index': receipt_log.log_index,
            'transaction_hash': receipt_log.transaction_hash,
            'transaction_index': receipt_log.transaction_index,
            'block_hash': receipt_log.block_hash,
            'block_number': receipt_log.block_number,
            'address': receipt_log.address,
            'data': receipt_log.data,
            'topics': receipt_log.topics
        }

    def dict_to_receipt_log(self, dict):
        receipt_log = EthReceiptLog()

        receipt_log.log_index = dict.get('log_index')
        receipt_log.transaction_hash = dict.get('transaction_hash')
        receipt_log.transaction_index = dict.get('transaction_index')
        receipt_log.block_hash = dict.get('block_hash')
        receipt_log.block_number = dict.get('block_number')
        receipt_log.address = dict.get('address')
        receipt_log.data = dict.get('data')

        topics = dict.get('topics')
        if isinstance(topics, str):
            if len(topics.strip()) == 0:
                receipt_log.topics = []
            else:
                receipt_log.topics = topics.strip().split(',')
        else:
            receipt_log.topics = topics

        return receipt_log


class KlaytnReceiptLogMapper(object):
    def __init__(self, enrich=False):
        self.enrich = enrich

    def json_dict_to_receipt_log(self, json_dict, **kwargs) -> Union[KlaytnRawReceiptLog, KlaytnReceiptLog]:
        _receipt_log = KlaytnRawReceiptLog()

        _receipt_log.log_index = hex_to_dec(json_dict.get('logIndex'))
        _receipt_log.transaction_hash = json_dict.get('transactionHash')
        _receipt_log.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))

        _receipt_log.block_hash = json_dict.get('blockHash')
        _receipt_log.block_number = hex_to_dec(json_dict.get('blockNumber'))

        _receipt_log.address = json_dict.get('address')
        _receipt_log.data = json_dict.get('data')
        _receipt_log.topics = json_dict.get('topics')

        return _receipt_log if not self.enrich else KlaytnReceiptLog.enrich(_receipt_log,
            block_timestamp=kwargs.get('block_timestamp'),
            block_timestamp_fos=kwargs.get('transaction_receipt_status'),
            transaction_receipt_status=kwargs.get('transaction_receipt_status'))

    def receipt_log_to_dict(self, receipt_log: Union[KlaytnRawReceiptLog, KlaytnReceiptLog]) -> dict:
        log_dict = {
            'type': 'log',
            'log_index': receipt_log.log_index,
            'transaction_hash': receipt_log.transaction_hash,
            'transaction_index': receipt_log.transaction_index,
            'block_hash': receipt_log.block_hash,
            'block_number': receipt_log.block_number,
            'address': receipt_log.address,
            'data': receipt_log.data,
            'topics': receipt_log.topics
        }

        if self.enrich and isinstance(log_dict, KlaytnReceiptLog):
            log_dict['block_timestamp'] = log_dict.block_timestamp
            log_dict['block_unix_timestamp'] = log_dict.block_unix_timestamp
            log_dict['transaction_receipt_status'] = log_dict.transaction_receipt_status

        return log_dict

    def dict_to_receipt_log(self, dict) -> Union[KlaytnRawReceiptLog, KlaytnReceiptLog]:

        # TODO
        _receipt_log = KlaytnRawReceiptLog()

        _receipt_log.log_index = dict.get('log_index')
        _receipt_log.transaction_hash = dict.get('transaction_hash')
        _receipt_log.transaction_index = dict.get('transaction_index')
        _receipt_log.block_hash = dict.get('block_hash')
        _receipt_log.block_number = dict.get('block_number')
        _receipt_log.address = dict.get('address')
        _receipt_log.data = dict.get('data')

        topics = dict.get('topics')
        if isinstance(topics, str):
            if len(topics.strip()) == 0:
                _receipt_log.topics = []
            else:
                _receipt_log.topics = topics.strip().split(',')
        else:
            _receipt_log.topics = topics

        if not self.enrich:
            return _receipt_log
        else:
            log = KlaytnReceiptLog()

            for k, v in _receipt_log.__dict__.items():
                if hasattr(log, k):
                    log.__setattr__(k, v)

            log.block_timestamp = dict.get('block_timestamp')
            log.block_unix_timestamp = dict.get('block_unix_timestamp')
            log.transaction_receipt_status = dict.get('transaction_receipt_status')

            return log
