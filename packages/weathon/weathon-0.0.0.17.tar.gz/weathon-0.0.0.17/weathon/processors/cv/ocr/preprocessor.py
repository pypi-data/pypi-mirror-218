from typing import Dict, Any

from torchvision import transforms

from weathon.base import BaseProcessor
from weathon.registry import PREPROCESSORS
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks, Datasets, ModeKeys
from weathon.utils.processor.preprocessors.cv.ocr.process_module.augment import ResizeShortSize
from weathon.utils.processor.preprocessors.cv.ocr.process_module.iaa_augment import IaaAugment
from weathon.utils.processor.preprocessors.cv.ocr.process_module.make_border_map import MakeBorderMap
from weathon.utils.processor.preprocessors.cv.ocr.process_module.make_shrink_map import MakeShrinkMap
from weathon.utils.processor.preprocessors.cv.ocr.process_module.random_crop_data import EastRandomCropData


@PREPROCESSORS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class Icdar2015Preprocessor(BaseProcessor):

    def __init__(self, preprocessor_cfg: Config = None, *args, **kwargs):
        preprocessor_cfg = preprocessor_cfg if preprocessor_cfg else dict()

        self.processes = kwargs.get("processes", preprocessor_cfg.get("transforms", None))
        self.filter_keys = kwargs.get("filter_keys", [])
        self._mode = kwargs.get('mode', preprocessor_cfg.get('mode', ModeKeys.TRAIN))
        self.is_training = (self._mode == ModeKeys.TRAIN)
        self.mean = kwargs.get("mean", preprocessor_cfg.get("mean", [0.485, 0.456, 0.406]))
        self.std = kwargs.get("std", preprocessor_cfg.get("std", [0.229, 0.224, 0.225]))
        self.tranforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean, std=self.std)
        ])

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.processes and not self.tranforms:
            return data
        if hasattr(self.processes, "IaaAugment"):
            data_process0 = IaaAugment(self.processes.IaaAugment)
            data = data_process0(data)

        if hasattr(self.processes, "EastRandomCropData"):
            data_process1 = EastRandomCropData(**self.processes.EastRandomCropData)
            data = data_process1(data)

        if hasattr(self.processes, "MakeShrinkMap"):
            data_process2 = MakeShrinkMap(**self.processes.MakeShrinkMap)
            data = data_process2(data)

        if hasattr(self.processes, "MakeBorderMap"):
            data_process3 = MakeBorderMap(**self.processes.MakeBorderMap)
            data = data_process3(data)

        if hasattr(self.processes, "ResizeShortSize"):
            data_process4 = ResizeShortSize(**self.processes.ResizeShortSize)
            data = data_process4(data)

        data["img"] = self.tranforms(data["img"])

        if self.is_training:
            for key in self.filter_keys:
                del data[key]
        return data
