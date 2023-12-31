# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
from pathlib import Path
from typing import Dict, Any, Optional

from chat_core.core.common.registry import register
from chat_core.core.data.dataset_reader import DatasetReader
from chat_core.core.data.utils import download_decompress


@register('squad_dataset_reader')
class SquadDatasetReader(DatasetReader):
    """
    Downloads dataset files and prepares train/valid split.

    SQuAD:
    Stanford Question Answering Dataset
    https://rajpurkar.github.io/SQuAD-explorer/
    
    SQuAD2.0:
    Stanford Question Answering Dataset, version 2.0
    https://rajpurkar.github.io/SQuAD-explorer/

    SberSQuAD:
    Dataset from SDSJ Task B
    https://www.sdsj.ru/ru/contest.html

    MultiSQuAD:
    SQuAD dataset with additional contexts retrieved (by tfidf) from original Wikipedia article.

    MultiSQuADRetr:
    SQuAD dataset with additional contexts retrieved by tfidf document ranker from full Wikipedia.

    """

    url_squad = 'http://files.deepchat.ai/datasets/squad-v1.1.tar.gz'
    url_sber_squad = 'http://files.deepchat.ai/datasets/sber_squad-v1.1.tar.gz'
    url_multi_squad = 'http://files.deepchat.ai/datasets/multiparagraph_squad.tar.gz'
    url_squad2 = 'http://files.deepchat.ai/datasets/squad-v2.0.tar.gz'

    def read(self, data_path: str, dataset: Optional[str] = 'SQuAD', url: Optional[str] = None, *args, **kwargs) \
            -> Dict[str, Dict[str, Any]]:
        """

        Args:
            data_path: path to save data
            dataset: default dataset names: ``'SQuAD'``, ``'SberSQuAD'`` or ``'MultiSQuAD'``
            url: link to archive with dataset, use url argument if non-default dataset is used

        Returns:
            dataset split on train/valid

        Raises:
            RuntimeError: if `dataset` is not one of these: ``'SQuAD'``, ``'SberSQuAD'``, ``'MultiSQuAD'``.
        """
        if url is not None:
            self.url = url
        elif dataset == 'SQuAD':
            self.url = self.url_squad
        elif dataset == 'SberSQuAD':
            self.url = self.url_sber_squad
        elif dataset == 'MultiSQuAD':
            self.url = self.url_multi_squad
        elif dataset == 'SQuAD2.0':
            self.url = self.url_squad2
        else:
            raise RuntimeError(f'Dataset {dataset} is unknown')

        data_path = Path(data_path)
        if dataset == "SQuAD2.0":
            required_files = [f'{dt}-v2.0.json' for dt in ['train', 'dev']]
        else:
            required_files = [f'{dt}-v1.1.json' for dt in ['train', 'dev']]
        data_path.mkdir(parents=True, exist_ok=True)

        if not all((data_path / f).exists() for f in required_files):
            download_decompress(self.url, data_path)

        dataset = {}
        for f in required_files:
            with data_path.joinpath(f).open('r', encoding='utf8') as fp:
                data = json.load(fp)
            if f in {'dev-v1.1.json', 'dev-v2.0.json'}:
                dataset['valid'] = data
            else:
                dataset['train'] = data

        return dataset


@register('multi_squad_dataset_reader')
class MultiSquadDatasetReader(DatasetReader):
    """
    Downloads dataset files and prepares train/valid split.

    MultiSQuADRetr:
    Multiparagraph SQuAD dataset with additional contexts retrieved by tfidf document ranker from full En Wikipedia.

    MultiSQuADRuRetr:
    Multiparagraph SberSQuAD dataset with additional contexts retrieved by tfidf document ranker from  Ru Wikipedia.

    """

    url_multi_squad_retr = 'http://files.deepchat.ai/datasets/multi_squad_retr_enwiki20161221.tar.gz'
    url_multi_squad_ru_retr = 'http://files.deepchat.ai/datasets/multi_squad_ru_retr.tar.gz'

    def read(self, data_path: str, dataset: Optional[str] = 'MultiSQuADRetr', url: Optional[str] = None, *args,
             **kwargs) -> Dict[str, Dict[str, Any]]:
        """

        Args:
            data_path: path to save data
            dataset: default dataset names: ``'MultiSQuADRetr'``, ``'MultiSQuADRuRetr'``
            url: link to archive with dataset, use url argument if non-default dataset is used

        Returns:
            dataset split on train/valid

        Raises:
            RuntimeError: if `dataset` is not one of these: ``'MultiSQuADRetr'``, ``'MultiSQuADRuRetr'``.
        """
        if url is not None:
            self.url = url
        elif dataset == 'MultiSQuADRetr':
            self.url = self.url_multi_squad_retr
        elif dataset == 'MultiSQuADRuRetr':
            self.url = self.url_multi_squad_ru_retr
        else:
            raise RuntimeError(f'Dataset {dataset} is unknown')

        data_path = Path(data_path)
        required_files = [f'{dt}.jsonl' for dt in ['train', 'dev']]
        if not data_path.exists():
            data_path.mkdir(parents=True)

        if not all((data_path / f).exists() for f in required_files):
            download_decompress(self.url, data_path)

        dataset = {}
        for f in required_files:
            if 'dev' in f:
                dataset['valid'] = data_path.joinpath(f)
            else:
                dataset['train'] = data_path.joinpath(f)

        return dataset
