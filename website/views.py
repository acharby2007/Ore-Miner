from flask import Flask, Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, username_testing=current_user.username, playerscore_testing=current_user.playerscore, osmiumscore_testing=current_user.osmiumscore, redberylscore_testing=current_user.redberylscore, tanzanitescore_testing=current_user.tanzanitescore, diamondscore_testing=current_user.diamondscore, ironscore_testing=current_user.ironscore, copperscore_testing=current_user.copperscore, prestigelevel_testing=current_user.prestigelevel, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@views.route('/mine')
@login_required
def mine():
    return render_template('mine.html', user=current_user, mine1TimeStart=current_user.mine1TimeStart, show_mining_time=True, seconds_loading_bar=current_user.mine1TimeStart, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@views.route('/home_redirectFromSettings')
@login_required
def home_redirectFromSettings():
    flash('Settings saved successfully!', category='success')
    return render_template('home.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@views.route('/privacypolicy')
def privacypolicy():
    return render_template("privacypolicy.html", user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@views.route('/acceptableusepolicy')
def acceptableusepolicy():
    return render_template("acceptableusepolicy.html", user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

