from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성 (Flask 앱과 연결됨)
db = SQLAlchemy()

# 댓글(Comment) 모델 정의
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유한 댓글 ID
    post_id = db.Column(db.Integer, nullable=False)  # 댓글이 속한 게시글 ID (예시용)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # 부모 댓글 ID (대댓글일 경우)

    content = db.Column(db.String(300), nullable=False)  # 댓글 내용

    # 자기참조 관계 설정 (부모 댓글 - 자식 댓글 연결)
    replies = db.relationship(
        'Comment',  # 같은 테이블을 참조
        backref=db.backref('parent', remote_side=[id])  # 대댓글에서 .parent로 부모 댓글 접근 가능
    )