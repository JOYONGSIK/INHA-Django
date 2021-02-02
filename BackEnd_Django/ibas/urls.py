from . import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='main'), # 기본으로 메인 홈페이지 보여준다.
    path('login/', views.login, name='login'),  # 로그인 페이지를 보여준다.
    path('logout/', views.logout, name = 'logout'), # 로그아웃을 위한 페이지.
    path('signup/', views.signup, name = 'signup'), # 회원가입 페이지.
    path('member/', views.member, name = 'member'), # 회원 관리 페이지.
    path('member/delete/<int:member_no>', views.delete, name = 'member-delete'), # 회원 제명을 위한 페이지
    path('board', views.board, name = 'board'), # 게시판 테이블
    path('board/delete/<int:board_no>', views.delete_board, name = 'board-delete'), # 게시글 삭제를 위한 페이지
    path('board/update/<int:board_no>/update', views.board_update, name = 'board-update'), # 게시글 업뎃
    path('board/<int:board_no>/<str:board_name>', views.board_detail, name = 'board_detail'), # 게시판 글 상세보기
    path('board/<int:board_no>/<str:board_name>/create', views.review_create, name = 'review_create'), # 댓글 쓰기
    path('board/<int:board_no>/<str:board_name>/<int:review_no>/detele', views.review_delete, name = 'review_delete'), # 댓글 삭제
    path('board/<int:board_no>/<str:board_name>/<int:review_no>/update', views.review_update, name = 'review_update'), # 댓글 수정
]