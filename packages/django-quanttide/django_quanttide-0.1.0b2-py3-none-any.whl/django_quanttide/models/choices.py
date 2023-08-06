"""
数据模型选项
"""

from django.db import models


class StageChoices(models.IntegerChoices):
    """
    研发阶段选项

    遵循PEP541对Development Status的定义，参见：
    https://pypi.org/classifiers/
    """
    PLANNING = 1, '计划'
    PRE_ALPHA = 2, '开发'
    ALPHA = 3, '内测'
    BETA = 4, '公测'
    STABLE = 5, '稳定'
    MATURE = 6, '成熟'
    INACTIVE = 7, '废弃'
