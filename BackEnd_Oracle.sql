# 필요한 테이블 정리
# 테이블 제목으로 Ctrl + F 하면 쉽게 서치가능
# 서치 가능 : 테이블 생성, 외래키 설정, insert문 시작 파트

# 1. 회원 정보 테이블
# - 회원번호(PK), 권한번호(FK), 이름, 이메일(uniq), 비밀번호, 학번(uniq), 핸드폰번호(uniq), 주소
# 2. 회원 권한 테이블
# - 권한번호(PK), 권한내용 / 여기서, (1, admin), (2, member) 으로 나눌 예정, 나머지는 비 로그인으로 조회만 가능
# 3. 게시판 테이블
# - 게시글번호(PK), 회원번호(FK, 작성자 번호를 기입), 게시글 제목, 게시글 내용, 작성시간(auto_now_add 사용)
# 4. 댓글 테이블
# - 댓글번호(PK), 게시글 번호(Fk), 회원번호(본인 댓글의 번호), 댓글내용

# 이름 var(30) / 이메일 var(50) / 비밀번호 longtext(encode생각) / 주소 var(100) /
# 권한 내용 var(20) / 게시글 제목 text / 게시글 내용 longtext / 작성시간 default Now() / 댓글 내용 var(100)

# 회원 정보 테이블

show databases ;

create database BackEnd_DB; # 데이터 베이스 생성
use BackEnd_DB; # 사용 선언

############### 회원 정보 테이블 생성 ##################
# Text 사용안하고 varchar 를 쓰는 이유는 검색 속도의 상향을 위해서.

CREATE table member_info ( # 테이블 설명은 1. 회원 정보 테이블 서치 가능
mem_no int primary key auto_increment, # PK Key, 회원 번호
mem_grade int not null default 2, # 권한 번호, 회원가입이 되는 친구들은 회원으로 들어온다.
mem_name varchar(30) not null ,  # 이름
mem_email varchar(50) not null unique , # 이메일
password longtext not null , # 비밀번호
stu_num int not null unique , # 학번
mem_phone varchar(15) not null unique, # 핸드폰번호
address varchar(100) not null # 주소
);


CREATE table member_grade ( # 테이블 설명은 2. 회원 권한 테이블 서치 가능
mem_grade int primary key not null , # 권한 번호
class varchar(20) not null # 권한 내용
);


CREATE table board_table ( # 테이블 설명은 3. 게시판 테이블 서치 가능
board_no int primary key auto_increment, # 게시글 번호
mem_no int not null , # 회원번호
board_main text not null , # 게시글 제목
board_content longtext , # 게시글 내용
created_time datetime not null default NOW() # 작성시간
);


CREATE table review ( # 테이블 설명은 4. 댓글 테이블 서치 가능
review_no int primary key auto_increment, # 댓글 번호
board_no int not null , # 게시글 번호
mem_no int not null , # 회원 번호
review_comment varchar(100) not null # 댓글 내용
);

####################### 외래키 설정 ################

# 회원 정보 테이블의 권환 번호 FK KEY 설정
alter table member_info add constraint mem_grade foreign key (mem_grade) references member_grade(mem_grade);
select * from member_info;

# 게시판 테이블의 회원번호 FK KEY 설정
alter table board_table add constraint mem_no foreign key (mem_no) references member_info(mem_no);
select * from board_table;

# 댓글 테이블의 게시글 번호 FK KEY 설정
alter table review add constraint board_no foreign key (board_no) references board_table(board_no);
select * from review;


#################### 테스트 케이스 입력 (insert문) ##############

insert into member_grade(mem_grade, class) VALUES  (1, '관리자');
insert into member_grade(mem_grade, class) values  (2, '회원');
select * from member_grade;
# 위에 설명한 것 처럼 관리자는 1번, 회원은 2번 / 다른 사람들은 외부인


insert into member_info(mem_grade, mem_name, mem_email, password, stu_num, mem_phone, address)
values (1, '조용식', 'josik97@naver.com', '1234', '12184816', '01058800295', '인천광역시');
insert into member_info(mem_grade, mem_name, mem_email, password, stu_num, mem_phone, address)
values (2, '홍길동', 'Hong@naver.com', '1234', '19970212', '01012345678', '서울특별시' );
insert into member_info(mem_grade, mem_name, mem_email, password, stu_num, mem_phone, address)
values (2, '홍길동', 'king@naver.com', '1234', '19970213', '01012345677', '서울특별시' );
insert into member_info(mem_name, mem_email, password, stu_num, mem_phone, address)
values ('흥부', 'Ding@naver.com', '1234', '19970214', '01012345676', '흥부특별시' );
select * from member_info;
# 1번의 mem_grade를 가진 조용식은 관리자 아이디로 사용 가능함.
# 2번의 mem_grade를 가진 홍길동은 회원 아이디로 사용 가능함.

insert into board_table(mem_no, board_main, board_content)
VALUES(1 , '첫 게시물입니다.', '첫 게시글 내용입니다.') ;
insert into board_table(mem_no, board_main, board_content)
VALUES(2 , '두번째 게시물입니다.', '두번째 게시글 내용입니다.') ;
insert into board_table(mem_no, board_main, board_content)
VALUES(5 , '세번째 게시물입니다.', '세번째 게시글 내용입니다.') ;
select * from board_table;
# 첫 게시물과 내용을 테스트 케이스로 입력함.

insert into review(board_no, mem_no, review_comment)
values(3, 1, '첫 댓글입니다.');
select * from review;
# 첫 댓글을 테스트 케이스로 입력함.

commit ;
