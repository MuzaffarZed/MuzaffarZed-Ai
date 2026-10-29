"""
Windows Brightness Synchronizer
Sinxronizatsiya moduli: Noutbuk ichki ekrani va tashqi monitor (DDC/CI) yorug'ligini avtomatik bog'lash.
"""

from .controller import BrightnessController
from .sync_daemon import BrightnessSyncDaemon

__all__ = ["BrightnessController", "BrightnessSyncDaemon"]
