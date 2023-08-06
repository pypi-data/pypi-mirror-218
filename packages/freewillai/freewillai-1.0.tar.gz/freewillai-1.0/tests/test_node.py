import logging
import asyncio
import numpy as np
from typing import Optional, List

import pytest
from freewillai.common import IPFSBucket, OnnxModel, TestDataset
from freewillai.utils import get_url


class Global_test: 
    csv_path = 'bucket/test/datasets/keras_testing_dataset.csv'
    image_path = 'bucket/test/datasets/cat.png'
    numpy_path = 'bucket/test/datasets/cat_img_pytorch.npy'
    model_path = 'bucket/test/models/test_model.onnx'

    dataset_hashes: Optional[List] = None
    model_hash: Optional[str] = None
    
    hashes = dict(
        Keras_onnx_model = 'Qmd8zXu5Z8QZ7RYxnzjSW4zquwzu5M155o3mXV8MB4MQGi',
        dataset_keras_csv = 'QmPodbGqLsvbqczgMWarztX6tqhGMQiYEfUQPM7ph2tu2Q',
        # sklearn_onnx_model = 'QmXV7rnpNYf5VHxLhDmtwnZRJo6ebttqZSmBpwADGryzfN',
        sklearn_onnx_model = 'QmTgXsSDajjTzv3Qx7FH5d5TRFbzVNEwVeCcACnsc1L5cX',
        dataset_sklearn_csv = 'QmQSUgZVonJa7g1AQFvcztNeWw67bUeP7U85BQvCXhLsLQ',
        pytorch_onnx_model = 'QmTFTNdrcYYErtjA9hNysZv8VeneCvdLLxGWkRhEdfER7V',
        Image_path_pytorch = 'QmVQ8p73epScpKknQzW4VkSbgq1sFdZhfRFuZ6cqibU2BU',
        pil_image_pytorch = 'QmbfDdE1kHHSJFEJ7eySKv9UpzqmHxSRiPvyhjpqoiD8Bf',
        image_pytorch_tensor = 'QmeUKjDGzHzU2dLvrMfWaap9nVxRJQvSDVuiRQcxBa9wy7',
        

    )



class TestIPFS:
    # WARNING: DO NOT ADD VARIABLES HERE. PYTEST WILL RESET THEM BEFORE RUNNING THE NEXT TEST
    def test_upload_dataset(self):
        async def _upload_files():
            tasks = [
                IPFSBucket.upload(Global_test.csv_path, file_type='dataset'),
                IPFSBucket.upload(Global_test.image_path, file_type='dataset'),
                IPFSBucket.upload(Global_test.numpy_path, file_type='dataset')]
            Global_test.dataset_hashes = await asyncio.gather(*tasks)
        asyncio.run(_upload_files())

    def test_upload_model(self):
        async def _upload_files():
            Global_test.model_hash = await IPFSBucket.upload(Global_test.model_path, file_type='model')
        asyncio.run(_upload_files())

    def test_download_dataset(self):
        assert Global_test.dataset_hashes is not None
        async def _download_files():
            tasks = [
                IPFSBucket.download(hash, file_type='dataset')
                for hash in Global_test.dataset_hashes
            ]
            await asyncio.gather(*tasks)
        asyncio.run(_download_files())

    def test_download_model(self):
        assert Global_test.model_hash is not None
        async def _download_files():
            task = await IPFSBucket.download(Global_test.model_hash, file_type='model')
        asyncio.run(_download_files())

    def test_download_all(self):
        logging.warning(Global_test.hashes.values())
        async def _download_files():
            tasks = [
                IPFSBucket.download(hsh)
                for hsh in Global_test.hashes.values()
            ]
            await asyncio.gather(*tasks)

        asyncio.run(_download_files())


class TestInference:

    def test_sklearn_csv(self):
        model_url = get_url(Global_test.hashes['sklearn_onnx_model'])
        dataset_url = get_url(Global_test.hashes['dataset_sklearn_csv'])
        wanted = np.array([1,1,1,0,0,0])

        dataset = TestDataset(dataset_url)
        logging.warning(dataset.numpy())
        model = OnnxModel(model_url)

        actual = model.inference(dataset)

        assert actual == wanted
