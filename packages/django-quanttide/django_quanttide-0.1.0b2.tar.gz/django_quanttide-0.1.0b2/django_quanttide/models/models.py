"""
数据模型
"""

from django.db import models

from polymorphic.models import PolymorphicModel as BasePolymorphicModel

from .fields import IDField, CreatedAtField, UpdatedAtField


class Model(models.Model):
    """
    基本数据模型

    使用UUID代替integer自增字段作为默认ID字段。
    """
    id = IDField()

    class Meta:
        abstract = True


class PolymorphicModel(BasePolymorphicModel):
    """
    多态数据模型

    类型字段映射表（TYPE_FIELD_MAPPINGS）是一个键值对字典，用于将模型名称（即 ContentType 表的 model 值）映射到用户定义的类型值。
    如果需要使用类型字段映射表，请在子类中覆盖 TYPE_FIELD_MAPPINGS 属性。

    示例：

    ```
    class Project(PolymorphicModel):
        TYPE_FIELD_MAPPINGS = {
            # 项目
            'Project': 'default',
            # 项目集
            'Program': 'program',
            # 项目组合
            'ProjectPortfolio': 'project_portfolio',
        }
    ```
    """
    id = IDField()
    created_at = CreatedAtField()
    updated_at = UpdatedAtField()

    # 类型字段映射表
    TYPE_FIELD_MAPPINGS = None

    class Meta:
        abstract = True

    @property
    def type(self) -> str:
        """
        类型字段

        该属性返回多态模型的类型值。如果需要使用类型字段映射表，请在子类中覆盖 TYPE_FIELD_MAPPINGS 属性。

        :return: 类型值
        """
        # 类名转小写，方便和ContentType.model字段对应
        if self.TYPE_FIELD_MAPPINGS:
            convert_mappings = {key.lower(): value for key, value in self.TYPE_FIELD_MAPPINGS.items()}
            return convert_mappings[self.polymorphic_ctype.model]
        else:
            return self.polymorphic_ctype.model
