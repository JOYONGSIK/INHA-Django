from django.shortcuts import render, get_object_or_404,redirect
from .forms import loginForm, signUpForm, Board, review
from .models import MemberInfo, BoardTable, Review
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

########### 코드 시작 ###############

def main(request):
    if request.session.get('mem_name') is not None : # 세션에 이름이 등록되어있으면 (로그인하면)
        context = {'mem_name' : request.session.get('mem_name') }  # 이름을 가져옵니다.
        return render(request, 'main.html', context) # 출력해줍니다.

    context = {} # 아닐경우 아무것도 돌려주지 않습니다.
    return render(request,'main.html', context)

def login(request): # 로그인 페이지에 관한 것들
    if request.method == 'POST':
        input_email = request.POST['mem_email']  # 사용자가 입력한 메일
        input_pw = request.POST['password']  # 사용자가 입력한 비밀번호
        user_List = MemberInfo.objects.all() # 회원들 정보를 다 가져온다.
        for user in user_List :  # 이렇게 하면 데이터베이스에 있는 것을 가져온다.
            if user.mem_email == input_email and user.password == input_pw:
                if user.mem_grade_id == 1 : # 만약 여기서, 관리자의 권한을 갖고 있을 경우,
                    # 관리자인 세션까지 같이 넘겨준다.
                    # 여기서 문제, mem_grade 이지만 mem_grade_id 로 받아줘야 한다.
                    request.session['mem_grade_id_admin'] = user.mem_grade_id
                    request.session['mem_no'] = user.mem_no # 관리자의 회원 번호를 세션에 넣어준다.
                else :
                    request.session['mem_grade_id'] = user.mem_grade_id
                    request.session['mem_no'] = user.mem_no # 로그인 한 사람의 회원 번호를 세션에 넣어준다.
                    # 관리자가 아니므로 mem_grade_id 는 2로 저장이 되어진다. (기본값)
                request.session['mem_name'] = user.mem_name # 이름 세션에 저장시켜준다.
                request.session.save() # 세션에 저장
                return HttpResponseRedirect('/') # 메인으로 이동

        context = {'form': loginForm(),
                   'not_login' : 0 }  # 여기는 로그인이 실행 안되었을 때,
        return render(request, 'login.html', context)  # 다시 로그인 하라고 켜줌.
         # 원래 메인 홈페이지로 이동.

    context = {'form': loginForm()} # 여기는 if 문 실행 안되었을 때 (POST X),
    return render(request, 'login.html', context) # 다시 로그인 하라고 켜줌.

def logout(request): # 로그아웃을 하려고 할때,
    request.session.clear() # 세션 초기화 = 즉 로그아웃과 같음
    return HttpResponseRedirect('/') # 메인으로 다시 돌려받아줌.

def signup(request):
    if request.method == 'POST' : # 가입버튼을 누를 경우
        form = signUpForm(request.POST) # 회원가입 폼을 입력한 것을 들고오고, 유효하면 밑을 실행시킨다.
        if form.is_valid():
            new_item = form.save() # 데이터베이스에 저장시켜준다.

            # 밑 부분은 세션 저장용
            request.session['mem_name'] = form['mem_name'].value() # 이름 저장
            request.session['mem_grade_id'] = form['mem_grade'].value() # 권한 저장
            request.session['mem_no'] = MemberInfo.objects.filter(mem_name=form['mem_name'].value())[0].mem_no
            # 로그인 한 사람의 회원번호를 저장, 복잡하게 코드 구현했음.
            request.session.save() # 등록된 이름, 권한을 세션처리한다.
            return HttpResponseRedirect('/')

        # 유효하지 않을 경우 알람을 보여준다.
        context = {'form': signUpForm(),
                   'not_signUp': 0}  # 여기는 로그인이 실행 안되었을 때,
        return render(request, 'signup.html', context)  # 다시 로그인 하라고 켜줌.

    #회원가입 하지 않았을 때
    context = {'form' : signUpForm()} # 회원가입 폼을 보여준다.
    return render(request, 'signup.html', context)

def member(request):
    members = MemberInfo.objects.exclude(mem_grade=1)
    # 관리자를 제명시킬 수는 없으므로 관리자를 뺀 나머지를 다 가져온다.
    paginator = Paginator(members, 3) #  페이지 목록에 테스트 용도로 3개만 보여준다.
    # 만약, 페이지 창에 이름이 page 로 쓰기 싫으면 밑의 코드 변경
    page = request.GET.get('page')
    item = paginator.get_page(page)

    context = {'members' : item} # 회원인 요소들 리턴으로 보내준다.
    return  render(request, 'member.html', context)

def delete(request, member_no): # 회원을 제명할 때 사용하는 것
    member = get_object_or_404(MemberInfo, pk=member_no) # 클릭이 된 회원의 정보를 가져와서,
    member.delete() # 데이터베이스에 지워준다.
    context = {'members' : MemberInfo.objects.all()} # 지우고 난 후의 데이터베이스를 리턴해준다.
    return HttpResponseRedirect('/member')
    # return render(request, 'member.html', context) # 처음 화면으로 이동시켜준다.

def board(request):
    ############## board 페이지에 글 쓰는 란, 삭제가 존재한다. ##########
    if request.method == 'POST' : # 글을 쓰게 될 경우,
        # 밑 부분 수정 필요할 수도 있음.
        form = Board(request.POST, initial={'mem_no' : request.session.get('mem_no')}) # 회원가입 폼을 입력한 것을 들고오고, 유효하면 밑을 실행시킨다.
        # 여기서, 'mem_no' 부분이 hiddenInput으로 넘어가지 않아서, html 작업했음.
        if form.is_valid():
            new_item = form.save() # 데이터베이스에 저장시켜준다.
            return HttpResponseRedirect('/board') # 글을 쓰게 되면 페이지 이동시켜준다.

    # content : board.html 으로 전송할 것임. order_by 에서 생성된 시간의 - 으로 해서 최신순으로 된다.
    ########### 현재는 미국 (us) 시간으로 setting 되어있음. 배포할 때 변경해야함. setting.py 확인 요망! ##
    content = BoardTable.objects.get_queryset().order_by('-created_time')
    # 테이블을 다 가져오기 위함
    paginator = Paginator(content, 5)  # 페이지 목록에 테스트 용도로 5개만 보여준다.

    # 나중에 페이지 변경하려고 하면 여기서 바꿔주면 된다.
    page = request.GET.get('page')
    item = paginator.get_page(page)

    # MemberInfo 를 선언한 이유가, FK 를 잡지 못했음. for 문 두개 사용했어서 그럼. 시간복잡도 커지므로 수정 요망.
    if request.session.get('mem_grade_id') is not None :
        # 회원 로그인, 멤버로 로그인 할 경우 member : 0 을 사용함
        context = {'content': item, # 페이지
                   'MemberInfo': MemberInfo.objects.all(), # 회원정보의 이름을 가져오기 위해서
                   'member' : 0, # 회원이면 0을 반환시켜준다.
                   'form': Board(), # form 사용하기 위함.
                   'loginMem': request.session.get('mem_no')} # 현재 세션(로그인)된 사람의 회원번호
        return render(request, 'board.html', context)

    elif request.session.get('mem_grade_id_admin') is not None :
        # 관리자 로그인, 관리자로 로그인 할 경우 admin : 0 을 사용함
        context = {'content': item, # 페이지
                   'MemberInfo': MemberInfo.objects.all(), # 회원정보의 이름을 가져오기 위해서
                   'admin' : 0, # 관리자일 경우 0을 반환시켜준다.
                   'form': Board(), # form을 사용하기 위함.
                   'loginMem': request.session.get('mem_no')} # 현재 세션(로그인)된 사람의 회원번호
        return render(request, 'board.html', context)

    else :
        # 비로그인, 아무것도 사용하지 않음.
        context = {'content' : item, # 페이지
                   'MemberInfo' : MemberInfo.objects.all() } # 회원정보의 이름을 가져오기 위해서
        return render(request, 'board.html', context)


def delete_board(request, board_no): # 게시판에 있는 글 지우는데 사용하려고 함
    board = get_object_or_404(BoardTable, pk=board_no) # 게시판의 글 가져와서 삭제
    board.delete() # 삭제
    context = {'board': BoardTable.objects.all()} # 반환함
    return HttpResponseRedirect('/board')

def board_detail(request, board_no, board_name): # 글을 자세히 보기
    # 여기에 댓글 수정, 삭제, 입력 넣어줘야한다. 댓글 삭제와 입력은 존재하는데 수정은 html 사용
    if board_no is not None : # 게시판 번호가 있을 경우
        item = get_object_or_404(BoardTable, pk=board_no) # PK KEY 를 이용해서 들고온다.
        reviews = Review.objects.filter(board_no=board_no) # board_no 를 통해서 댓글을 가져온다.
        if request.session.get('mem_grade_id') is not None: # 회원일 경우
            return render(request, 'board_detail.html', {'MemberInfo': MemberInfo.objects.all(), # 회원 이름
                                                         'content': item, # 게시판 테이블
                                                         'board_name': board_name, # 게시글 작성자 이름
                                                         'board_no' : board_no, # 게시글 번호
                                                         'form': review(), # 댓글 작성 form
                                                         'member' : 0, # 회원만 댓글창이 보인다.
                                                         'reviews': reviews, # 댓글들
                                                         'loginMem': request.session.get('mem_no')}) # 로그인된 회원번호
        elif request.session.get('mem_grade_id_admin') is not None: # 관리자일 경우
            return render(request, 'board_detail.html', {'MemberInfo' : MemberInfo.objects.all(), # 회원 이름
                                                         'content': item, # 게시판 테이블
                                                         'board_name' : board_name, # 게시글 작성자 이름
                                                         'board_no': board_no, # 게시글 번호
                                                         'form' : review(), # 댓글 작성 form
                                                         'admin' : 0, # 관리자만 댓글창이 보인다.
                                                         'reviews': reviews, # 댓글들
                                                         'loginMem': request.session.get('mem_no')}) # 로그인된 회원번호

        else:
            return render(request, 'board_detail.html', {'MemberInfo': MemberInfo.objects.all(), # 회원 이름
                                                         'content': item, # 게시판 테이블
                                                         'reviews': reviews, # 댓글들
                                                         'board_name': board_name}) # 직상자 이름

    return HttpResponseRedirect('/board/')

def review_create(request, board_no, board_name) : # 댓글쓰기 위한 함수
    if request.method == 'POST' : # 댓글쓰기를 누를 경우
        form = review(request.POST) #  댓글 입력한 것을 들고오고, 유효하면 밑을 실행시킨다.
        if form.is_valid():
            new_item = form.save() # 데이터베이스에 저장시켜준다.
        return redirect('board_detail', board_no=board_no, board_name=board_name)

def review_delete(request, board_no, board_name, review_no):  # 댓글 지우는데 사용
    board = get_object_or_404(Review, pk=review_no) # 게시판의 글 가져와서 삭제함
    board.delete()
    return redirect('board_detail', board_no=board_no, board_name=board_name) # 반환

def board_update(request, board_no):
    if request.method == 'POST': # 입력받으면
        item = get_object_or_404(BoardTable, pk=board_no) # 해당되는 게시글을 찾은 후,
        form = Board(request.POST, instance=item) # 원래 작성된 값을 넣어준다.
        if form.is_valid():  # 만약 바꾼게 맞으면
            item = form.save() # 저장시켜준다
        return HttpResponseRedirect('/board')

    elif request.method == 'GET' : # 값을 보여주기 위함
        item = get_object_or_404(BoardTable, pk=board_no) # 해당되는 게시글을 가져온다.
        form = Board(instance=item) # 작성된 상황을 보여준다.
        return render(request, 'update.html', {'form' : form, # forms.py 사용.
                                               'board_no' : board_no, # 파라미터로 사용
                                               'board_update' : 0, # 이게 있으면 board 를 수정, review_update 면 review를 수정
                                               'loginMem': request.session.get('mem_no')}) # 세션을 계속 보내주는 중

def review_update(request, board_no, board_name, review_no):
    if request.method == 'POST': # 입력받으면
        print('123')
        item = get_object_or_404(Review, pk=review_no) # 해당되는 댓글을 찾은 후,
        form = review(request.POST, instance=item) # 원래 작성해논 댓글을 넣어준다.
        if form.is_valid(): # 바꾼게 알맞으면
            form.save() # 데이터베이스에 저장시켜준다.
        return redirect('board_detail', board_no=board_no, board_name=board_name) # 전에 있던 페이지로 반환

    if request.method == 'GET' :
        item = get_object_or_404(Review, pk=review_no) # 해당되는 게시글을 가져온다.
        form = review(instance=item) # 작성된 상황을 보여준다.

        return render(request, 'update.html', {'form' : form, # forms.py 사용.
                                               'board_no' : board_no, # 파라미터로 사용
                                               'board_name' : board_name, # 파라미터로 사용
                                               'review_no' : review_no,
                                               'loginMem': request.session.get('mem_no'), # 세션을 계속 보내주는 중
                                               'review_update' : 0 # review_update 면 review를 수정
                                               })
