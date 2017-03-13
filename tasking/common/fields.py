# coding: utf-8

from rest_framework import serializers

import phonenumbers


EMPTY_VALUES = (None, '', [], (), {})


class PhoneField(serializers.CharField):
    default_error_messages = {
        'required': '请输入手机号码'
    }

    def to_internal_value(self, data):
        # phonenumbers.parse()方法不允许传入空值
        if data in list(EMPTY_VALUES):
            return data
        try:
            data = phonenumbers.parse(data, 'CN')
            if phonenumbers.is_valid_number(data):
                data = str(phonenumbers.format_number(data, phonenumbers.PhoneNumberFormat.NATIONAL)).replace(' ', '')
            else:
                raise serializers.ValidationError('手机号码不合法')
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError('手机号码不合法')
        return data
