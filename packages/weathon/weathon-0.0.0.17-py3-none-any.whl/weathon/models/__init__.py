from weathon.utils.import_utils import is_torch_available

if is_torch_available():
    from weathon.base import TorchModel, TorchHead
