from flask import Flask
from flask import *
from uuid import uuid1
import game_eng

app = Flask(__name__)
users = {}
app.secret_key = 'my_game'
@app.route('/')
@app.route('/menu')
def menu():
    global users
    database = game_eng.DataBase('game_data.db')
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = str(uuid1())
        session['user_id'] = user_id
    if not user_id in users:
        users[user_id] = database.get_user(user_id)
    tmp_sound = request.args.get('sound', '')
    if tmp_sound != '':
        if tmp_sound == 'on':
            users[user_id].sound = True
        elif tmp_sound == 'off':
            users[user_id].sound = False
        database.update_user(users[user_id])
    if users[user_id].sound:
        sound = 'on'
    else:
        sound = 'off'
    if users[user_id].room.game_over:
        users[user_id].room = database.get_room(1)
        database.update_user(users[user_id])
    return render_template('menu.html', sound_mode=sound)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/play')
def play():
    step = 0
    if not 'user_id' in session:
        return redirect(url_for('menu'))
    user_id = session['user_id']
    database = game_eng.DataBase('game_data.db')
    if not user_id in users:
        users[user_id] = database.get_user(user_id)    
    tmp_move = request.args.get('move', '')
    if tmp_move != '' and not users[user_id].room.game_over:
        if tmp_move == 'up':
            users[user_id].room = database.get_room(users[user_id].room.fwd_room_id)
        elif tmp_move == 'down':
            users[user_id].room = database.get_room(users[user_id].room.back_room_id)
        elif tmp_move == 'left':
            users[user_id].room = database.get_room(users[user_id].room.l_room_id)
        elif tmp_move == 'right':
            users[user_id].room = database.get_room(users[user_id].room.r_room_id)
        database.update_user(users[user_id])
    tmp_step = request.args.get('step', '')
    if tmp_step != '':
        step = int(tmp_step)
    params = {}
    params['room_id'] = url_for('static', filename='background/room_{}.png'.format(users[user_id].room.room_id))
    params['sound'] = users[user_id].sound
    params['is_left'] = users[user_id].room.l_room_id != None
    params['is_right'] = users[user_id].room.r_room_id != None
    params['is_up'] = users[user_id].room.fwd_room_id != None
    params['is_down'] = users[user_id].room.back_room_id != None
    params['text'] = users[user_id].room.description[step]
    params['step'] = step + 1
    params['moretext'] = len(users[user_id].room.description) > step + 1
    #if users[user_id].room.game_over:
    #    database.del_user(user_id)
    #    del users[user_id]
    #    print('del')
    return render_template('play.html', **params)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')