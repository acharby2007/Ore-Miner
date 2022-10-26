from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):

    #basic user data

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)
    password = db.Column(db.String(20))
    role = db.Column(db.String(100))

    #Shown user scores

    prestigelevel = db.Column(db.Integer)
    playerscore = db.Column(db.Integer)
    osmiumscore = db.Column(db.Integer)
    redberylscore = db.Column(db.Integer)
    tanzanitescore = db.Column(db.Integer)
    diamondscore = db.Column(db.Integer)
    ironscore = db.Column(db.Integer)
    copperscore = db.Column(db.Integer)

    #User scores not shown and time mine started so user doesn't have to stay on screen when mining, but used when waiting for mine to complete

    playerscoreToCollect = db.Column(db.Integer)
    osmiumscoreToCollect = db.Column(db.Integer)
    redberylscoreToCollect = db.Column(db.Integer)
    tanzanitescoreToCollect = db.Column(db.Integer)
    diamondscoreToCollect = db.Column(db.Integer)
    ironscoreToCollect = db.Column(db.Integer)
    copperscoreToCollect = db.Column(db.Integer)
    mineInProgress = db.Column(db.Boolean)
    mine1TimeStart = db.Column(db.Integer)
    mine2TimeStart = db.Column(db.Integer)
    mine3TimeStart = db.Column(db.Integer)
    currentlyActiveMines = db.Column(db.Integer)

    #User Multipliers and Powerups; Extra Mines

    playerRarityMultiplier = db.Column(db.Float)
    amountOfMinesUnlocked = db.Column(db.Integer)

class ForumPost(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    userScore = db.Column(db.Integer)
    postDate = db.Column(db.String(31))
    content = db.Column(db.String(500))
    views = db.Column(db.Integer)
    repliesCount = db.Column(db.Integer)
    recentReplyDate = db.Column(db.String(31))
    replyUserScore = db.Column(db.Integer)