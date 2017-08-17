# -*- coding: utf-8 -*-
from enum import Enum
from .models import AccountsModel

from PyQt5.QtWidgets import QMessageBox

class AlertLevel(Enum):
    INFO = QMessageBox.Information
    WARNING = QMessageBox.Warning
    ERROR = QMessageBox.Critical


class PasswordPromptResult(Enum):
    SUCCESS = 1
    CANCELED = 2
    FAILED = 3