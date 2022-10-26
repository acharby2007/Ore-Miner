from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .test_timeelapsed import check_time_for_mineral, convert_time_format
from flask_mail import Message, Mail
from flask_xcaptcha import XCaptcha
from .forms import ContactForm
from .__init__ import mail
from sqlalchemy import desc
from .models import User
from . import db
import random
import time

auth = Blueprint('auth', __name__)

profanitylist = ["2g1c","2 girls 1 cup","acrotomophilia","alabama hot pocket","alaskan pipeline","anal","anilingus","anus","apeshit","arsehole","ass","asshole","assmunch","auto erotic","autoerotic","babeland","baby batter","baby juice","ball gag","ball gravy","ball kicking","ball licking","ball sack","ball sucking","bangbros","bangbus","bareback","barely legal","barenaked","bastard","bastardo","bastinado","bbw","bdsm","beaner","beaners","beaver cleaver","beaver lips","beastiality","bestiality","big black","big breasts","big knockers","big tits","bimbos","birdlock","bitch","bitches","black cock","blonde action","blonde on blonde action","blowjob","blow job","blow your load","blue waffle","blumpkin","bollocks","bondage","boner","boob","boobs","booty call","brown showers","brunette action","bukkake","bulldyke","bullet vibe","bullshit","bung hole","bunghole","busty","butt","buttcheeks","butthole","camel toe","camgirl","camslut","camwhore","carpet muncher","carpetmuncher","chocolate rosebuds","cialis","circlejerk","cleveland steamer","clit","clitoris","clover clamps","clusterfuck","cock","cocks","coprolagnia","coprophilia","cornhole","coon","coons","creampie","cum","cumming","cumshot","cumshots","cunnilingus","cunt","darkie","date rape","daterape","deep throat","deepthroat","dendrophilia","dick","dildo","dingleberry","dingleberries","dirty pillows","dirty sanchez","doggie style","doggiestyle","doggy style","doggystyle","dog style","dolcett","domination","dominatrix","dommes","donkey punch","double dong","double penetration","dp action","dry hump","dvda","eat my ass","ecchi","ejaculation","erotic","erotism","escort","eunuch","fag","faggot","fecal","felch","fellatio","feltch","female squirting","femdom","figging","fingerbang","fingering","fisting","foot fetish","footjob","frotting","fuck","fuck buttons","fuckin","fucking","fucktards","fudge packer","fudgepacker","futanari","gangbang","gang bang","gay sex","genitals","giant cock","girl on","girl on top","girls gone wild","goatcx","goatse","god damn","gokkun","golden shower","goodpoop","goo girl","goregasm","grope","group sex","g-spot","guro","hand job","handjob","hard core","hardcore","hentai","homoerotic","honkey","hooker","horny","hot carl","hot chick","how to kill","how to murder","huge fat","humping","incest","intercourse","jack off","jail bait","jailbait","jelly donut","jerk off","jigaboo","jiggaboo","jiggerboo","jizz","juggs","kike","kinbaku","kinkster","kinky","knobbing","leather restraint","leather straight jacket","lemon party","livesex","lolita","lovemaking","make me come","male squirting","masturbate","masturbating","masturbation","menage a trois","milf","missionary position","mong","motherfucker","mound of venus","mr hands","muff diver","muffdiving","nambla","nawashi","negro","neonazi","nigga","nigger","nig nog","nimphomania","nipple","nipples","nsfw","nsfw images","nude","nudity","nutten","nympho","nymphomania","octopussy","omorashi","one cup two girls","one guy one jar","orgasm","orgy","paedophile","paki","panties","panty","pedobear","pedophile","pegging","penis","phone sex","piece of shit","pikey","pissing","piss pig","pisspig","playboy","pleasure chest","pole smoker","ponyplay","poof","poon","poontang","punany","poop chute","poopchute","porn","porno","pornography","prince albert piercing","pthc","pubes","pussy","queaf","queef","quim","raghead","raging boner","rape","raping","rapist","rectum","reverse cowgirl","rimjob","rimming","rosy palm","rosy palm and her 5 sisters","rusty trombone","sadism","santorum","scat","schlong","scissoring","semen","sex","sexcam","sexo","sexy","sexual","sexually","sexuality","shaved beaver","shaved pussy","shemale","shibari","shit","shitblimp","shitty","shota","shrimping","skeet","slanteye","slut","s&m","smut","snatch","snowballing","sodomize","sodomy","spastic","spic","splooge","splooge moose","spooge","spread legs","spunk","strap on","strapon","strappado","strip club","style doggy","suck","sucks","suicide girls","sultry women","swastika","swinger","tainted love","taste my","tea bagging","threesome","throating","thumbzilla","tied up","tight white","tit","tits","titties","titty","tongue in a","topless","tosser","towelhead","tranny","tribadism","tub girl","tubgirl","tushy","twat","twink","twinkie","two girls one cup","undressing","upskirt","urethra play","urophilia","vagina","venus mound","viagra","vibrator","violet wand","vorarephilia","voyeur","voyeurweb","voyuer","vulva","wank","wetback","wet dream","white power","whore","worldsex","wrapping men","wrinkled starfish","xx","xxx","yaoi","yellow showers","yiffy","zoophilia","🖕"]

def getTimeInMS(addedMS):
    t = round(time.time()*1000)
    return round(t+int(str(addedMS)+"000"), -3)

@auth.route('/contactus', methods=["GET", "POST"])
def contactus():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Please provide a valid email.', category="error")
            return render_template('contactus.html', form=form, user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))
        else:
            msg = Message(form.subject, sender=form.email.data, recipients=['acharby2007@gmail.com'])
            #msg.body = "Username: %s\nEmail: %s\n\n\nMessage:\n%s" % (form.name.data, form.email.data, form.message.data)
            msg.html = render_template('mailtemplate.html', emailformusername=form.name.data, emailformemail=form.email.data, emailformmessage=form.message.data)
            mail.send(msg)

            return render_template('contactus.html', form=form, user=current_user, success=True, lightDarkCookie=request.cookies.get('lightdarkswitch'))

    elif request.method == 'GET':
        return render_template('contactus.html', form=form, user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', lightDarkCookie=request.cookies.get('lightdarkswitch')), 404

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Username or password is incorrect', category='error')
        else:
            flash('Username or password is incorrect', category='error')

    return render_template('login.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        for word in profanitylist:

            if word in username:
                flash(f"Username cannot contain profane phrases!", category="error")
                return render_template('sign_up.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

            else:
                continue

        user = User.query.filter_by(username=username).first()

        if user:
            flash('This username is already taken. Try another', category='error')

        elif len(username) < 4:
            flash('Username must be at least 4 characters long', category='error')

        elif len(username) > 16:
            flash("Username can't be more than 16 characters", category='error')

        elif password1 != password2:
            flash("Passwords don't match", category='error')

        elif len(password1) < 6:
            flash("Password must be at least 6 characters long", category='error')

        elif len(password1) > 20:
            flash("Password can't be more than 20 characters", category='error')

        else:
                # xcaptcha.verify()
                #if xcaptcha.verify():
                if True:
                    new_user = User(username=username, password=generate_password_hash(password1, method='sha256'), role='user', prestigelevel = 0, playerscore=0, osmiumscore=0, redberylscore=0, tanzanitescore=0, diamondscore=0, ironscore=0, copperscore=0, playerscoreToCollect=0, osmiumscoreToCollect=0, redberylscoreToCollect=0, tanzanitescoreToCollect=0, diamondscoreToCollect=0, ironscoreToCollect=0, copperscoreToCollect=0, mineInProgress=False, mine1TimeStart=None, mine2TimeStart=None, mine3TimeStart=None, amountOfMinesUnlocked=1, playerRarityMultiplier=1.0)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Account created successfully!", category='success')
                    login_user(new_user, remember=True)
                    current_user.playerscoreToCollect = 0
                    current_user.playerscore = 0
                    return redirect(url_for('views.home'))
                else:
                    flash("You must complete the captcha to sign up!", category="error")


    return render_template('sign_up.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

def check_for_mineral(seconds):

    Osmium_found = 0
    RedBeryl_found = 0
    Tanzanite_found = 0
    Diamond_found = 0
    Iron_found = 0
    Copper_found = 0
    multiplier = float(current_user.playerRarityMultiplier)

    for i in range(seconds):
        attempt_find_mineral_int = random.randint(0, 1775)
        if attempt_find_mineral_int == 1775:
            Osmium_found = Osmium_found + 1

        attempt_find_mineral_int = random.randint(0, 400)
        if attempt_find_mineral_int == 400:
            RedBeryl_found = RedBeryl_found + 1

        attempt_find_mineral_int = random.randint(0, 180)
        if attempt_find_mineral_int == 180:
            Tanzanite_found = Tanzanite_found + 1

        attempt_find_mineral_int = random.randint(0, 65)
        if attempt_find_mineral_int == 65:
            Diamond_found = Diamond_found + 1

        attempt_find_mineral_int = random.randint(0, 9)
        if attempt_find_mineral_int == 9:
            Iron_found = Iron_found + 1

        attempt_find_mineral_int = random.randint(0, 7)
        if attempt_find_mineral_int == 7:
            Copper_found = Copper_found + 1

    current_user.osmiumscoreToCollect = Osmium_found
    current_user.redberylscoreToCollect = RedBeryl_found
    current_user.tanzanitescoreToCollect = Tanzanite_found
    current_user.diamondscoreToCollect = Diamond_found
    current_user.ironscoreToCollect = Iron_found
    current_user.copperscoreToCollect = Copper_found
    current_user.mine1TimeStart = getTimeInMS(seconds)
    current_user.mineInProgress = True
    db.session.commit()

    current_user.playerscoreToCollect = (current_user.copperscoreToCollect*round(1*multiplier)) + (current_user.ironscoreToCollect*round(3*multiplier)) + (current_user.diamondscoreToCollect*round(10*multiplier)) + (current_user.tanzanitescoreToCollect*round(65*multiplier)) + (current_user.redberylscoreToCollect*round(125*multiplier)) + (current_user.osmiumscoreToCollect*round(1000*multiplier))
    db.session.commit()

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        lightDarkSetCookieVar = request.form.get('DarkLightSetName')
        resp = make_response(render_template('home.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'), settingsChanged=True))
        resp.set_cookie('lightdarkswitch', lightDarkSetCookieVar)
        return resp
    else:
        return render_template('settings.html', user=current_user, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@auth.route('/leaderboard')
def leaderboard():
    try:
        def leaderboard():
            names = []
            result = []
            result = db.session.query(User.playerscore).all()
            result = str(result).replace('(', '')
            result = result.replace(')', '')
            result = result.replace(',, ', ', ')
            result = result.replace(',]', '')
            result = result.replace('[', '')
            result = result.split(", ")
            result = [int(score) for score in result]
            result = sorted(result, key=int, reverse=True)

            for score in result:
                nameresult = db.session.query(User).filter(User.playerscore==score)
                for row in nameresult:
                    names.append(row.username)

            return [result, names]

        leaderboard = leaderboard()
        leaderboardUsernames = leaderboard[1][3:]
        leaderboardScores = leaderboard[0][3:]
        leaderboardUsernamesAll = leaderboard[1]
        leaderboardScoresAll = leaderboard[0]

        current_userRankPlacement = int(leaderboardUsernamesAll.index(current_user.username)) + 1

        return render_template('leaderboard.html', user=current_user, current_userUsername=current_user.username, userPlayerscore=current_user.playerscore, userRankPlacement=current_userRankPlacement, leaderboardscore1=leaderboard[0][0], leaderboardscore2=leaderboard[0][1], leaderboardscore3=leaderboard[0][2], leaderboardname1=leaderboard[1][0], leaderboardname2=leaderboard[1][1], leaderboardname3=leaderboard[1][2], leaderboardUsernamesSubPodium=leaderboardUsernames, leaderboardScoresSubPodium=leaderboardScores, leaderboardoffline=False, lightDarkCookie=request.cookies.get('lightdarkswitch'))

    except:
        return render_template('leaderboard.html', user=current_user, leaderboardoffline=True, lightDarkCookie=request.cookies.get('lightdarkswitch'))

@auth.route('/mine_collect', methods=["GET", "POST"])
@login_required
def mine_collect():
        current_user.osmiumscore = current_user.osmiumscore + current_user.osmiumscoreToCollect
        current_user.redberylscore = current_user.redberylscore + current_user.redberylscoreToCollect
        current_user.tanzanitescore = current_user.tanzanitescore + current_user.tanzanitescoreToCollect
        current_user.diamondscore = current_user.diamondscore + current_user.diamondscoreToCollect
        current_user.ironscore = current_user.ironscore + current_user.ironscoreToCollect
        current_user.copperscore = current_user.copperscore + current_user.copperscoreToCollect
        current_user.playerscore = current_user.playerscore + current_user.playerscoreToCollect
        current_user.mine1TimeStart = None
        current_user.mineInProgress = False
        db.session.commit()

        current_user.playerscoreToCollect = 0
        current_user.osmiumscoreToCollect = 0
        current_user.redberylscoreToCollect = 0
        current_user.tanzanitescoreToCollect = 0
        current_user.diamondscoreToCollect = 0
        current_user.iromscoreToCollect = 0
        current_user.copperscoreToCollect = 0
        db.session.commit()

        return redirect(url_for("views.mine"))

@auth.route('/mine_dev', methods=["GET", "POST"])
def mine_dev():
            if request.form.get('MiningSecSelect') == '10sec':
                currentTime = request.args.get("time")
                current_user.playerscoreToCollect = 0
                current_user.osmiumscoreToCollect = 0
                current_user.redberylscoreToCollect = 0
                current_user.tanzanitescoreToCollect = 0
                current_user.diamondscoreToCollect = 0
                current_user.iromscoreToCollect = 0
                current_user.copperscoreToCollect = 0
                current_user.mine1TimeStart = None
                db.session.commit()
                check_for_mineral(10)

                return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, currentTimeReturn = currentTime, show_mining_time=True, seconds_loading_bar=10, minesUnlocked = current_user.amountOfMinesUnlocked, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))

            if request.form.get('MiningSecSelect') == '30sec':
                currentTime = request.args.get("time")
                current_user.playerscoreToCollect = 0
                current_user.osmiumscoreToCollect = 0
                current_user.redberylscoreToCollect = 0
                current_user.tanzanitescoreToCollect = 0
                current_user.diamondscoreToCollect = 0
                current_user.iromscoreToCollect = 0
                current_user.copperscoreToCollect = 0
                current_user.mine1TimeStart = None
                db.session.commit()
                check_for_mineral(30)

                return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, currentTimeReturn = currentTime, show_mining_time=True, seconds_loading_bar=30, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))

            if request.form.get('MiningSecSelect') == '60sec':
                currentTime = request.args.get("time")
                current_user.playerscoreToCollect = 0
                current_user.osmiumscoreToCollect = 0
                current_user.redberylscoreToCollect = 0
                current_user.tanzanitescoreToCollect = 0
                current_user.diamondscoreToCollect = 0
                current_user.iromscoreToCollect = 0
                current_user.copperscoreToCollect = 0
                current_user.mine1TimeStart = None
                db.session.commit()
                check_for_mineral(60)

                return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, currentTimeReturn = currentTime, show_mining_time=True, seconds_loading_bar=60, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))

            else:
                if int(request.form.get('customSecValueInput')) + (60*int(request.form.get('customMinuteValueInput'))) + (3600*int(request.form.get('customHourValueInput'))) == 0:
                    flash('Custom mining time must be at least one second!', category="error")
                    return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, show_mining_time=True, seconds_loading_bar=60, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))

                elif int(request.form.get('customSecValueInput')) + (60*int(request.form.get('customMinuteValueInput'))) + (3600*int(request.form.get('customHourValueInput'))) > 86400:
                    flash("Custom mining time can't be more than 24 hours!", category="error")
                    return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, show_mining_time=True, seconds_loading_bar=60, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))
                else:
                    currentTime = request.args.get("time")
                    current_user.playerscoreToCollect = 0
                    current_user.osmiumscoreToCollect = 0
                    current_user.redberylscoreToCollect = 0
                    current_user.tanzanitescoreToCollect = 0
                    current_user.diamondscoreToCollect = 0
                    current_user.iromscoreToCollect = 0
                    current_user.copperscoreToCollect = 0
                    current_user.mine1TimeStart = None
                    db.session.commit()
                    secondsTotal = int(request.form.get('customSecValueInput')) + (60*int(request.form.get('customMinuteValueInput'))) + (3600*int(request.form.get('customHourValueInput')))
                    check_for_mineral(secondsTotal)

                    return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, currentTimeReturn = currentTime, show_mining_time=True, seconds_loading_bar=secondsTotal, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))

            return render_template('mine.html', user=current_user, mineFuncOutput=check_time_for_mineral(current_user.mine1TimeStart), mine1TimeStart=current_user.mine1TimeStart, currentTimeReturn = currentTime, show_mining_time=True, seconds_loading_bar=current_user.mine1TimeStart, osmium_found = current_user.osmiumscoreToCollect, redberyl_found = current_user.redberylscoreToCollect, tanzanite_found = current_user.tanzanitescoreToCollect, diamond_found = current_user.diamondscoreToCollect, iron_found = current_user.ironscoreToCollect, copper_found = current_user.copperscoreToCollect, playerscore_gained = current_user.playerscoreToCollect, mineInProgressBool = current_user.mineInProgress, total_playerscore=current_user.playerscore, lightDarkCookie=request.cookies.get('lightdarkswitch'))