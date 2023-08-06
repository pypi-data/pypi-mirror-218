from functools import partial

from torch.utils.data import DataLoader

from weathon.base import TorchCustomDataset
from weathon.base.trainer import ConfigTrainer
from weathon.registry import TRAINERS
from weathon.utils.config.config import ConfigDict
from weathon.utils.constants import Tasks, ModeKeys, Datasets
from weathon.utils.dataset.collate_fns.cv.ocr_collate_fn import DetCollectFN
from weathon.utils.trainer_utils import worker_init_fn


@TRAINERS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class OcrDetectionTrainer(ConfigTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_dataloader(self, dataset: TorchCustomDataset, dataloader_cfg: ConfigDict, mode: str = ModeKeys.TRAIN,
                         **kwargs):
        batch_size = kwargs.get("batch_size", dataloader_cfg.get("batch_size_per_gpu", 8))
        num_workers = kwargs.get("num_workers", dataloader_cfg.get("workers_per_gpu", 0))
        drop_last = kwargs.get("drop_last", dataloader_cfg.get("drop_last", False))
        shuffle = kwargs.get("shuffle", dataloader_cfg.get("shuffle", (mode == ModeKeys.TRAIN)))
        pin_memory = kwargs.get("pin_memory", dataloader_cfg.get("pin_memory", True))
        init_fn = partial(worker_init_fn, num_workers=num_workers, rank=0,
                          seed=self.seed) if self.seed is not None else None

        collate_fn = DetCollectFN(dataset) if hasattr(dataloader_cfg, "DetCollectFN") else None

        dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers,
                                collate_fn=collate_fn, pin_memory=pin_memory, drop_last=drop_last,
                                worker_init_fn=init_fn)

        return dataloader
