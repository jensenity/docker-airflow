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


from datetime import datetime, timedelta

from klaytnetl.domain.block import EthBlock
from klaytnetl.domain.block import KlaytnBlock, KlaytnRawBlock
from klaytnetl.mappers.transaction_mapper import EthTransactionMapper
from klaytnetl.mappers.transaction_mapper import KlaytnTransactionMapper
from klaytnetl.mappers.receipt_mapper import KlaytnReceiptMapper
from klaytnetl.utils import hex_to_dec, to_normalized_address, strf_unix_dt

from typing import Union

class EthBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = EthTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = EthBlock()
        block.number = hex_to_dec(json_dict.get('number'))
        block.hash = json_dict.get('hash')
        block.parent_hash = json_dict.get('parentHash')
        # block.nonce = json_dict.get('nonce')
        # block.sha3_uncles = json_dict.get('sha3Uncles')
        block.logs_bloom = json_dict.get('logsBloom')
        block.transactions_root = json_dict.get('transactionsRoot')
        block.state_root = json_dict.get('stateRoot')
        block.receipts_root = json_dict.get('receiptsRoot')
        # block.miner = to_normalized_address(json_dict.get('miner'))
        # block.difficulty = hex_to_dec(json_dict.get('difficulty'))
        # block.total_difficulty = hex_to_dec(json_dict.get('totalDifficulty'))
        block.size = hex_to_dec(json_dict.get('size'))
        block.extra_data = json_dict.get('extraData')
        block.gas_limit = hex_to_dec(json_dict.get('gasLimit'))
        block.gas_used = hex_to_dec(json_dict.get('gasUsed'))
        block.timestamp = hex_to_dec(json_dict.get('timestamp'))

        # Klaytn additional properties
        block.block_score = hex_to_dec(json_dict.get('blockscore'))
        block.total_block_score = hex_to_dec(json_dict.get('totalBlockScore'))

        block.timestamp_fos = hex_to_dec(json_dict.get('timestampFoS'))
        block.governance_data = json_dict.get('governanceData')
        block.vote_data = json_dict.get('voteData')

        block.committee = json_dict.get('committee')
        block.proposer = json_dict.get('proposer')
        block.reward_address = json_dict.get('reward')

        if 'transactions' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx, block_timestamp=block.timestamp)
                for tx in json_dict['transactions']
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])

        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'number': block.number,
            'hash': block.hash,
            'parent_hash': block.parent_hash,
            # 'nonce': block.nonce,
            # 'sha3_uncles': block.sha3_uncles,
            'logs_bloom': block.logs_bloom,
            'transactions_root': block.transactions_root,
            'state_root': block.state_root,
            'receipts_root': block.receipts_root,
            # 'miner': block.miner,
            # 'difficulty': block.difficulty,
            # 'total_difficulty': block.total_difficulty,
            'size': block.size,
            'extra_data': block.extra_data,
            'gas_limit': block.gas_limit,
            'gas_used': block.gas_used,
            'timestamp': block.timestamp,
            'transaction_count': block.transaction_count,

            # Klaytn additional properties
            'block_score': block.block_score,
            'total_block_score': block.total_block_score,

            'timestamp_fos': block.timestamp_fos,
            'governance_data': block.governance_data,
            'vote_data': block.vote_data,

            'committee': block.committee,
            'proposer': block.proposer,
            'reward_address': block.reward_address
        }


class KlaytnBlockMapper(object):
    def __init__(self, transaction_mapper=None, receipt_mapper=None, enrich: bool=False):
        if transaction_mapper is None:
            self.transaction_mapper = KlaytnTransactionMapper(enrich=enrich)
        else:
            self.transaction_mapper = transaction_mapper

        if not enrich and receipt_mapper is None:
            self.receipt_mapper = KlaytnReceiptMapper()
        else:
            self.receipt_mapper = receipt_mapper

        self.enrich = enrich

    def json_dict_to_block(self, json_dict) -> Union[KlaytnRawBlock, KlaytnBlock]:
        _block = KlaytnRawBlock()
        _block.number = hex_to_dec(json_dict.get('number'))
        _block.hash = json_dict.get('hash')
        _block.parent_hash = json_dict.get('parentHash')
        _block.logs_bloom = json_dict.get('logsBloom')
        _block.transactions_root = json_dict.get('transactionsRoot')
        _block.state_root = json_dict.get('stateRoot')
        _block.receipts_root = json_dict.get('receiptsRoot')

        _block.size = hex_to_dec(json_dict.get('size'))
        _block.extra_data = json_dict.get('extraData')
        _block.gas_limit = hex_to_dec(json_dict.get('gasLimit'))
        _block.gas_used = hex_to_dec(json_dict.get('gasUsed'))
        _block.timestamp = hex_to_dec(json_dict.get('timestamp'))
        _block.timestamp_fos = hex_to_dec(json_dict.get('timestampFoS'))

        # Klaytn additional properties
        _block.block_score = hex_to_dec(json_dict.get('blockscore'))
        _block.total_block_score = hex_to_dec(json_dict.get('totalBlockScore'))

        _block.governance_data = json_dict.get('governanceData')
        _block.vote_data = json_dict.get('voteData')

        _block.committee = json_dict.get('committee')
        _block.proposer = json_dict.get('proposer')
        _block.reward_address = json_dict.get('reward')

        if 'transactions' in json_dict:
            _block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx,
                    block_timestamp=_block.timestamp,
                    block_timestamp_fos=_block.timestamp_fos,
                    enrich=self.enrich)
                for tx in json_dict['transactions']
                if isinstance(tx, dict)
            ]
            _block.transaction_count = len(json_dict['transactions'])

            if not self.enrich:
                _block.receipts = [self.receipt_mapper.json_dict_to_receipt(tx) for tx in json_dict['transactions']]
            else:
                del _block.receipts

        return _block if not self.enrich else KlaytnBlock.enrich(_block)

    def block_to_dict(self, block: Union[KlaytnBlock, KlaytnRawBlock]) -> dict:
        block_dict = {
            'type': 'block',
            'number': block.number,
            'hash': block.hash,
            'parent_hash': block.parent_hash,
            'logs_bloom': block.logs_bloom,
            'transactions_root': block.transactions_root,
            'state_root': block.state_root,
            'receipts_root': block.receipts_root,
            'size': block.size,
            'extra_data': block.extra_data,
            'gas_limit': block.gas_limit,
            'gas_used': block.gas_used,
            'timestamp': block.timestamp,
            'transaction_count': block.transaction_count,

            # Klaytn additional properties
            'block_score': block.block_score,
            'total_block_score': block.total_block_score,

            'governance_data': block.governance_data,
            'vote_data': block.vote_data,

            'committee': block.committee,
            'proposer': block.proposer,
            'reward_address': block.reward_address
        }

        if self.enrich and isinstance(block, KlaytnBlock):
            block_dict['unix_timestamp'] = block.unix_timestamp
        else:
            block_dict['timestamp_fos'] = block.timestamp_fos

        return block_dict
