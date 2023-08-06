"""
数据模型字段
"""

import uuid

from django.db import models
from django.contrib.auth import get_user_model


class IDField(models.UUIDField):
    """
    ID字段

    微服务系统内全局唯一。

    默认作为主键使用；
    不作为主键、作为关联ID使用时，设置`primary_key=False`，
    同时建议自定义`verbose_name`，格式为"<关联模型名称>ID"。

    :param primary_key: 是否作为主键，默认为True
    :type primary_key: bool
    :param editable: 是否可编辑，默认为非主键字段可编辑
    :type editable: bool
    :param default: 默认值，默认为uuid.uuid4
    :type default: callable
    :param verbose_name: 字段名称，默认为'ID'
    :type verbose_name: str
    """
    description = 'ID字段'

    def __init__(self, **options):
        options.setdefault('primary_key', True)
        options.setdefault('editable', not options['primary_key'])
        options.setdefault('default', uuid.uuid4)
        options.setdefault('verbose_name', 'ID')
        super().__init__(**options)


class NumberField(models.IntegerField):
    """
    编号字段
    """
    description = "编号字段"

    def __init__(self, **options):
        options['editable'] = False
        options['unique'] = True
        options.setdefault('verbose_name', '编号')
        super().__init__(**options)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            # 如果字段值为空，则生成一个自增的值
            queryset = model_instance.__class__.objects.all()
            if queryset:
                last_object = queryset.latest(self.attname)
                value = getattr(last_object, self.attname) + 1
            else:
                value = 1
            setattr(model_instance, self.attname, value)
        return value


class NameField(models.SlugField):
    """
    标识字段

    租户内同模型唯一。

    用于表示名称或标题的标识符字段，通常用于生成URL Slug。

    :param max_length: 字段允许的最大长度，默认为100个字符。
    :type max_length: int
    :param unique: 字段的值是否在整个模型中唯一，默认为True。
    :type unique: bool
    :param verbose_name: 字段的可读名称，默认为“标识”。
    :type verbose_name: str
    """
    description = "标识字段"

    def __init__(self, **options):
        # ChatGPT建议的值是50-70，这里取了一个稍大的值。
        options.setdefault('max_length', 100)
        options.setdefault('unique', True)
        options.setdefault('verbose_name', '标识')
        super().__init__(**options)


class VerboseNameField(models.CharField):
    """
    名称字段

    :param max_length: 字段允许的最大长度，默认为100个字符。
    :type max_length: int
    :param default: 字段的默认值，默认为空字符串。
    :type default: str
    :param blank: 如果为True，则该字段允许为空值，默认为True。
    :type blank: bool
    :param null: 如果为True，则该字段允许为NULL值，默认为True。
    :type null: bool
    :param verbose_name: 字段的可读名称，默认为“标题”。
    :type verbose_name: str
    """
    description = "名称字段"

    def __init__(self, **options):
        options.setdefault('max_length', 100)
        options.setdefault('default', None)
        options.setdefault('blank', True)
        options.setdefault('null', True)
        options.setdefault('verbose_name', '标题')
        super().__init__(**options)


class TitleField(models.CharField):
    """
    标题字段

    :param max_length: 字段允许的最大长度，默认为255个字符。
    :type max_length: int
    :param default: 字段的默认值，默认为空字符串。
    :type default: str
    :param blank: 如果为True，则该字段允许为空值，默认为True。
    :type blank: bool
    :param null: 如果为True，则该字段允许为NULL值，默认为True。
    :type null: bool
    :param verbose_name: 字段的可读名称，默认为“标题”。
    :type verbose_name: str
    """
    description = "标题字段"

    def __init__(self, **options):
        options.setdefault('max_length', 255)
        options.setdefault('default', None)
        options.setdefault('blank', True)
        options.setdefault('null', True)
        options.setdefault('verbose_name', '标题')
        super().__init__(**options)


class DescriptionField(models.TextField):
    """
    描述字段

    :param default: 字段的默认值，默认为空字符串。
    :type default: str
    :param blank: 如果为True，则该字段允许为空值，默认为True。
    :type blank: bool
    :param null: 如果为True，则该字段允许为NULL值，默认为True。
    :type null: bool
    :param verbose_name: 字段的可读名称，默认为“描述”。
    :type verbose_name: str
    """
    description = "描述字段"

    def __init__(self, **options):
        options.setdefault('default', None)
        options.setdefault('blank', True)
        options.setdefault('null', True)
        options.setdefault('verbose_name', '描述')
        super().__init__(**options)


class TypeField(models.CharField):
    """
    类型字段

    描述系统中而非用户自定义的分类，每个类型通常对应一个子类。
    """
    description = "类型字段"

    def __init__(self, choices, default, **options):
        options.setdefault('max_length', 50)
        options.setdefault('choices', choices)
        options.setdefault('default', default)
        options.setdefault('verbose_name', '类型')
        super().__init__(**options)


class StatusField(models.CharField):
    """
    状态字段

    描述系统中而非用户自定义的状态，用状态的变化来描述生命周期。
    """
    def __init__(self, choices, default=None, **options):
        options.setdefault('max_length', 50)
        options.setdefault('choices', choices)
        options.setdefault('default', default)
        options.setdefault('verbose_name', '状态')
        super().__init__(**options)


class StageField(models.IntegerField):
    """
    研发阶段字段

    遵循PEP541对Development Status的定义，参见：
    https://pypi.org/classifiers/
    """
    description = "研发阶段字段"

    def __init__(self, **options):
        from .choices import StageChoices
        options.setdefault('choices', StageChoices.choices)
        options.setdefault('default', StageChoices.PLANNING)
        super().__init__(**options)


class CreatedAtField(models.DateTimeField):
    """
    创建时间字段

    :param auto_now_add: 如果为True，则字段将在对象第一次保存到数据库时自动设置为当前时间。默认为True。
    :type auto_now_add: bool
    :param verbose_name: 字段的可读名称，默认为“创建时间”。
    :type verbose_name: str
    """
    description = "创建时间字段"

    def __init__(self, **options):
        options.setdefault('auto_now_add', True)
        options.setdefault('verbose_name', '创建时间')
        super().__init__(**options)


class UpdatedAtField(models.DateTimeField):
    """
    更新时间字段

    :param auto_now: 如果为True，则字段将在每次保存对象时自动设置为当前时间。默认为True。
    :type auto_now: bool
    :param verbose_name: 字段的可读名称，默认为“更新时间”。
    :type verbose_name: str
    """
    description = "更新时间字段"

    def __init__(self, **options):
        options.setdefault('auto_now', True)
        options.setdefault('verbose_name', '更新时间')
        super().__init__(**options)


class CreatedByField(models.ForeignKey):
    """
    创建者字段

    该字段用于记录创建该记录的用户。

    :param to: 外键关联的用户模型。默认为 settings.AUTH_USER_MODEL。
    :type to: str
    :param on_delete: 外键关联的删除行为。默认为 PROTECT。
    :type on_delete: ~typing.Optional[Callable[[], Any]]
    :param null: 是否允许为空。默认为 True。
    :type null: bool
    :param verbose_name: 字段的可读名称。默认为“创建者”。
    :type verbose_name: str
    """
    description = "创建者字段"

    def __init__(self, **options):
        user_model = options.pop('to', get_user_model())
        on_delete = options.pop('on_delete', models.PROTECT)
        options.setdefault('null', True)
        options.setdefault('verbose_name', '创建者')
        super().__init__(user_model, on_delete, **options)


class UpdatedByField(models.ForeignKey):
    """
    更新者字段

    该字段用于记录最后一次更新该记录的用户。

    :param to: 外键关联的用户模型。默认为 settings.AUTH_USER_MODEL。
    :type to: str
    :param on_delete: 外键关联的删除行为。默认为 PROTECT。
    :type on_delete: ~typing.Optional[Callable[[], Any]]
    :param null: 是否允许为空。默认为 True。
    :type null: bool
    :param verbose_name: 字段的可读名称。默认为“更新者”。
    :type verbose_name: str
    """
    description = "更新者字段"

    def __init__(self, **options):
        user_model = options.pop('to', get_user_model())
        on_delete = options.pop('on_delete', models.PROTECT)
        options.setdefault('null', True)
        options.setdefault('verbose_name', '更新者')
        super().__init__(user_model, on_delete, **options)
