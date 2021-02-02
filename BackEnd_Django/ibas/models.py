from django.db import models

class MemberGrade(models.Model):
    mem_grade = models.IntegerField(primary_key=True)
    class_field = models.CharField(db_column='class', max_length=20)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'member_grade'

class MemberInfo(models.Model):
    mem_no = models.AutoField(primary_key=True)
    mem_grade = models.ForeignKey(MemberGrade, models.DO_NOTHING, db_column='mem_grade', default=2)
    # 건들지마세요. 권한에 관한 것입니다.
    mem_name = models.CharField(max_length=30)
    mem_email = models.CharField(unique=True, max_length=50)
    password = models.TextField()
    stu_num = models.IntegerField(unique=True)
    mem_phone = models.CharField(unique=True, max_length=15)
    address = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'member_info'


class BoardTable(models.Model):
    board_no = models.AutoField(primary_key=True)
    mem_no = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, db_column='mem_no')
    # 회원이 삭제될 경우, 모든 멤버가 작성한 덧글, 게시글을 삭제시켜야 하므로
    # on_delete = models.CASCADE 가 들어간다.
    board_main = models.TextField()
    board_content = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'board_table'




class Review(models.Model):
    review_no = models.AutoField(primary_key=True)
    board_no = models.ForeignKey(BoardTable, on_delete=models.CASCADE, db_column='board_no')
    # 회원이 사라지면 댓글도 한번에 사라져야 함으로 on_delete 걸어놨습니다.
    mem_no = models.IntegerField()
    review_comment = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'review'
