import sqlite3  
class Room:
    def __init__(self, room_id, fwd_room_id, back_room_id, 
                 l_room_id, r_room_id, background, description, game_over):
        self.room_id = room_id
        self.fwd_room_id = fwd_room_id
        self.back_room_id = back_room_id
        self.l_room_id = l_room_id
        self.r_room_id = r_room_id
        self.description = description
        self.background = background
        self.game_over = game_over
        self.step = 0
        
    def get_description(self):
        if self.step < len(self.description):
            text = self.description[self.step]
            self.step += 1
            return text
        else:
            return ''
        
    def get_game_over(self):
        return self.game_over and self.step == len(self.description)
    
        
class DataBase:
    def __init__(self, data_name):
        self.database = sqlite3.connect(data_name).cursor()
        
    def get_room_description(self, room_id, step, text):
        data = self.database.execute("""SELECT * FROM description
                            WHERE room_id = {} AND step = {}""".format(room_id, step)).fetchall()[0]
        text = data[2]
        return data[3]
    
    def get_room(self, room_id):
        room_data = self.database.execute("""SELECT * FROM rooms
                            WHERE id = {}""".format(room_id)).fetchall()[0]
        description_data = self.database.execute("""SELECT text FROM description
                             WHERE room_id = {} ORDER BY step""".format(room_id)).fetchall()
        deskription_text = [el[0] for el in description_data]
        room = Room(room_data[0], room_data[1], room_data[2], 
                    room_data[3], room_data[4], room_data[5], deskription_text, room_data[6] == 'True')
        return room
    
    def get_user(self, user_id):
        user_data = self.database.execute("""SELECT * FROM saves
                            WHERE user_id = '{}'""".format(user_id)).fetchall()
        if len(user_data) != 0:
            user = User(user_data[0][0], self.get_room(user_data[0][1]), user_data[0][2])
        else:
            self.database.execute("""INSERT INTO saves (user_id, room_id, sound)
                                 VALUES('{}', {}, {})""".format(user_id, 1, True))
            user = User(user_id, self.get_room(1), True)
        return user
    
    def update_user(self, user):
        self.database.execute("""UPDATE saves SET room_id = {}, sound = {} WHERE user_id = '{}'""".format(user.room.room_id, user.sound, user.user_id))
    
    def del_user(self, user):
        self.database.execute("""DELETE FROM saves WHERE user_id = '{}'""".format(user))
        
    
class User:
    def __init__(self, user_id, room, sound):
        self.user_id = user_id
        self.room = room
        self.sound = sound