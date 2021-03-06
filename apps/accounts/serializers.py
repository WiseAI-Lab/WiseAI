import hashlib
import random
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions, serializers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "role", "avatar", "password")
        extra_kwargs = {'password': {'write_only': True}, 'avatar_url': {'write_only': True}}

    def get_avatar(self, obj):
        styles = ['identicon', 'monsterid', 'wavatar']
        # random_str = ''.join([chr(random.randint(0x0000, 0x9fbf)) for i in range(random.randint(1, 25))])
        size = 256
        random_str = str(obj.username)
        m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
        url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
        return url


class ProfileSerializer(serializers.ModelSerializer):
    # 利用drf中的validators验证username是否唯一
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='用户已经存在')])
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="密码", label="密码", write_only=True,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)

    # 重写create方法加密密码，如果直接set的话会导致明文密码保存
    def create(self, validated_data):
        user = super(ProfileSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password")
