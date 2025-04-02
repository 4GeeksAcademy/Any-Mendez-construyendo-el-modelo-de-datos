from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er


# Inicializar Flask-SQLAlchemy
db = SQLAlchemy()
# Tabla intermedia para la relacion de muchos a muchos (likes)
likes = Table('likes', db.Model.metadata,
        Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
        Column('post_id', Integer, ForeignKey('post.id'), primary_key=True)
        )

#User
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
#Relaciones
    posts: Mapped[list["Post"]] = relationship('Post', back_populates= 'user')
    comments: Mapped[list["Comment"]] = relationship('Comment', back_populates= 'user')
    liked_posts: Mapped[list["Post"]] = relationship('Post', secondary=likes, back_populates= 'linking_users')

    def serialize(self):
         return {"id": self.id, "username": self.username}

#Post
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(250), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False)
#Relaciones
    user: Mapped["User"] = relationship('User', back_populates='posts')
    comments: Mapped[list["Comment"]] = relationship('Comment', back_populates='post')
    linking_users: Mapped[list["User"]] = relationship('User', secondary=likes, back_populates='liked_posts')

#Comment
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[str] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[str] = mapped_column(
        Integer, ForeignKey('post.id'), nullable=False)
#Relaciones
    user: Mapped["User"] = relationship('User', back_populates='comments')
    post: Mapped["Post"] = relationship('Post', back_populates='comments')
