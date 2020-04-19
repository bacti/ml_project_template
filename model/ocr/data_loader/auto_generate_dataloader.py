import os

import numpy as np

from ..data_loader.vocab import Vocab
try:
    from trdg.generators import GeneratorFromTextFile
except:
    pass
from ..data_loader.collate import collate_wrapper
from ..data_loader.data_loaders import OCRDataLoader


class AutoGenerateDataloader:
    def __init__(self, data_dir, batch_size, **kwargs):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.kwargs = kwargs

        self.voc = Vocab()
        self.voc.build_vocab_from_char_dict_file(self.get_data_path('vocab.json'))

        self.generator = GeneratorFromTextFile(folder='./data/text', count=-1, size=40, language='vi',
                                               minimum_length=1, maximum_length=10,
                                               skewing_angle=2, random_skew=True, blur=1, random_blur=True,
                                               background_type=3, distorsion_type=-1, margins=(2, 2, 2, 2))
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        """
        We need to generate a batch of data here
        :return:
        """
        if self.index == len(self):
            self.index = 0
            raise StopIteration
        self.index += 1
        data = []

        for _ in range(self.batch_size):
            image, label = next(self.generator)
            label = self.voc.get_indices_from_label(label)
            data.append({"image": np.array(image), "label": label})

        return collate_wrapper(data)

    def __len__(self):
        valid_steps = self.kwargs.get('valid_steps')
        if valid_steps:
            return int(valid_steps)
        return 1000

    def split_validation(self):
        """
        Should we use real data for validation test?
        :return:
        """
        # val_dataloader = OCRDataLoader(data_dir='./data/',
        #                                json_path='test.json',
        #                                batch_size=self.batch_size,
        #                                training=False,
        #                                shuffle=False,
        #                                num_workers=4,
        #                                collate_fn=collate_wrapper)
        val_dataloader = AutoGenerateDataloader(data_dir='data/', batch_size=self.batch_size, valid_steps=100)

        return val_dataloader

    def get_vocab(self):
        return self.voc

    def get_data_path(self, path):
        return os.path.join(self.data_dir, path)


if __name__ == '__main__':
    import cv2

    generator = GeneratorFromTextFile(count=100, size=64, language='vi',
                                       skewing_angle=2, random_skew=True, blur=1, random_blur=True,
                                       background_type=3, distorsion_type=-1)

    for i, (img, lbl) in enumerate(generator):
        cv2.imwrite('../data/generated/' + str(i) + '.png', img)