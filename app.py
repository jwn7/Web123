from flask import Flask, render_template, request, redirect, url_for
from models import db, Comment  # Comment 모델 및 DB 객체 임포트

# Flask 앱 생성
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'  # SQLite DB 사용
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # SQLAlchemy 초기화

# 📄 메인 페이지: 댓글 목록 보여줌
@app.route('/')
def index():
    # 부모 댓글만 가져옴 (즉, 대댓글은 replies를 통해 하위에서 표시)
    comments = Comment.query.filter_by(parent_id=None).all()
    return render_template('post.html', comments=comments)

# 📝 댓글 또는 대댓글 작성
@app.route('/comment', methods=['POST'])
def add_comment():
    content = request.form['content']  # 입력된 댓글 내용
    post_id = 1  # 게시글 ID는 고정 (예제용)
    parent_id = request.form.get('parent_id')  # 대댓글일 경우 부모 ID가 존재

    # 새 댓글 객체 생성
    comment = Comment(
        content=content,
        post_id=post_id,
        parent_id=int(parent_id) if parent_id else None
    )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))  # 작성 후 메인으로 리다이렉트

# ✏️ 댓글 수정
@app.route('/edit/<int:comment_id>', methods=['POST'])
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)  # 해당 댓글 찾기
    if comment:
        comment.content = request.form['content']  # 내용 업데이트
        db.session.commit()
    return redirect(url_for('index'))

# 🗑️ 댓글 삭제
@app.route('/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        if comment.replies:
            # 대댓글이 있으면 내용만 '삭제된 댓글입니다.'로 표시
            comment.content = '삭제된 댓글입니다.'
        else:
            # 대댓글이 없다면 댓글 자체를 DB에서 삭제
            db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('index'))

# 🏁 앱 실행 (서버 시작)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # DB 테이블 생성
    app.run(debug=True)
