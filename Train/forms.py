from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': '用户名必须输入'
    })
    uphone = forms.CharField(required=True, error_messages={
        'required': '手机号必须输入'
    })
    password = forms.CharField(min_length=6, required=True, error_messages={
        'required': '密码必须输入',
        'min_length': '密码至少6个字符'
    })
    password1 = forms.CharField(min_length=6, required=True, error_messages={
        'required': '密码必须输入',
        'min_length': '密码至少6个字符'
    })
    # 单个字段验证
    def clean_upaswd(self):
        password = self.cleaned_data.get('password')
        if password and password.isdigit():
            raise ValidationError('密码不能是纯数字')
        return password
    # 全局验证
    def clean(self):
        password = self.cleaned_data.get('password', None)
        password1 = self.cleaned_data.get('password1', '')
        # print(upaswd,upaswd1)
        if password != password1:
            raise ValidationError({'password1': '两次密码输入不一致'})
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': '用户名必须输入'
    })
    password = forms.CharField(min_length=6, required=True, error_messages={
        'required': '密码必须输入',
        'min_length': '密码至少6个字符'
    })
    captcha = CaptchaField(required=True, error_messages={
        'invalid': '验证码错误',
    })

class OrderForm(forms.Form):
    oname = forms.CharField(required=True, error_messages={
        'required': '姓名必须输入'
    })
    code = forms.CharField(required=True, error_messages={
        'required': '身份证号必须输入'
    })
    ophone = forms.CharField(required=True, error_messages={
        'required': '手机号必须输入'
    })

class TrainForm(forms.Form):
    from_station_name = forms.CharField(min_length=2, required=True, error_messages={
        'required': '起点站必须输入',
        'min_length': '至少2个字符'
    })
    to_station_name = forms.CharField(min_length=2, required=True, error_messages={
        'required': '终点站必须输入',
        'min_length': '至少2个字符'
    })
    date = forms.DateField(required=True, error_messages={
        'required': '日期必须输入',
    })

class ProblemForm(forms.Form):
    problem = forms.CharField(required=True, error_messages={
        'required': '必须输入,不能为空',
    })
# class ForgetForm(forms.Form):
#     uphone = forms.CharField(min_length=6, required=True, error_messages={
#         'required': '手机号必须输入',
#         'min_length': '手机号至少6位',
#     })
#     password1 = forms.CharField(min_length=6, required=True, error_messages={
#         'required': '密码必须输入',
#     })
#     captcha = CaptchaField(required=True, error_messages={
#         'invalid': '验证码错误',
#     })
