from django.forms import ModelForm
from .models import MemberInfo, BoardTable, Review
from django import forms
from django.utils.translation import gettext_lazy as _

class loginForm(ModelForm) :
    # login.html 에서 사용중
    class Meta :
        model = MemberInfo # 모델 가져오는 부분
        fields = ['mem_email', 'password'] # 우리가 사용자에게 받을 것
        labels = {
            'mem_email': _('이메일'),
            'password': _('비밀번호')
        }
        help_texts = {
            'mem_email': _('이메일을 입력해주세요'),
            'password': _('비밀번호를 입력해주세요'),
        }
        error_messages = {
            'mem_email' : {
                'max_length': _("이메일이 너무 깁니다. 50자 아래로 써주세요")
            }
        }

class signUpForm(ModelForm):
    # signup.html 에서 사용중
    class Meta :
        model = MemberInfo
        fields = ['mem_name','mem_grade', 'mem_email', 'password', 'stu_num', 'mem_phone', 'address']
        # ##################### signUpForm 을 사용하게 된다면 mem_grade가 forms.hiddenInput이므로
        # input name='mem_grade' value = '~' 를 꼭 해주어야 한다. 안그러면 form.is_vaild() 가 실행 X
        labels = {
            'mem_name': _('이름'),
            'mem_email': _('이메일'),
            'password': _('비밀번호'),
            'stu_num': _('학번'),
            'mem_phone': _('전화번호'),
            'address' : _('주소'),
        }
        help_texts = {
            'mem_name': _('이름을 입력하세요'),
            'mem_email': _('이메일을 입력하세요'),
            'password': _('비밀번호를 입력하세요'),
            'stu_num': _('학번을 입력하세요'),
            'mem_phone': _('전화번호를 입력하세요'),
            'address': _('주소를 입력하세요'),
        }
        error_messages = {
            'mem_email': {
                'max_length': _("이메일이 너무 깁니다. 50자 아래로 써주세요")
            }
        }
        widgets = {
            'mem_grade' : forms.HiddenInput
        }

class Board(ModelForm):
    # board.html 39번줄부터 시작된다.
    # ##################### Board 을 사용하게 된다면 mem_no가 forms.hiddenInput이므로
    # input name='mem_no' value = '~' 를 꼭 해주어야 한다. 안그러면 form.is_vaild() 가 실행 X
    class Meta :
        model = BoardTable
        fields = ['mem_no', 'board_main', 'board_content']
        labels = {
            'board_main': _('제목'),
            'board_content':_('내용'),

         }
        help_texts = {
            'board_main': _('제목을 입력하세요'),
            'board_content': _('내용을 입력하세요'),

        }
        widgets = {
            'mem_no' : forms.HiddenInput()
        }

class review(ModelForm):
    # ##################### review 을 사용하게 된다면 mem_no, board_no 가 forms.hiddenInput이므로
    # input name='mem_no' value = '~' 를 꼭 해주어야 한다. 안그러면 form.is_vaild() 가 실행 X

    class Meta :
        model = Review
        fields = ['board_no', 'mem_no', 'review_comment']
        labels = {
            'review_comment' : _('댓글')
        }
        help_texts = {
            'review_comment' : _('댓글을 입력하세요')
        }
        widgets = {
            'board_no' : forms.HiddenInput,
            'mem_no' : forms.HiddenInput,
        }

