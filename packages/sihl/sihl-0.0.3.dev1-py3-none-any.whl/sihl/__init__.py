# ruff: noqa: F401
from sihl.sihl_model import SihlModel
from sihl.timm_backbone import TimmBackbone
from sihl.torchvision_backbone import TorchvisionBackbone


try:
    from sihl.timm_backbone import TimmBackbone
except ImportError:
    pass

try:
    from sihl.lightning_module import LightningModule
except ImportError:
    pass
