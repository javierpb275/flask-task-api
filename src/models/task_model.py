from src.config.db import db


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id, title, description, done):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.done = done

    def json(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_user_id_and_id(cls, user_id, _id):
        return cls.query.filter_by(user_id=user_id, task_id=_id).first()

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_all_by_user_id_and_done(cls, user_id, done):
        return cls.query.filter_by(user_id=user_id, done=done)
