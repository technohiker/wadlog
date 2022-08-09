#Copied & Pasted from Springboard's provided Seed file.

from app import app
from models import db, Users, Mods, Records, Logs, Comments


db.drop_all()
db.create_all()

#Users(2)

u1 = {
    "username": "okay_doomer",
    "email": "test@email.com",
    "password": "HASHED_PASSWORD_1",
    "image_url": ""
}

u2 = {
    "username": "testuser2",
    "email": "test2@email.com",
    "password": "HASHED_PASSWORD_2",
    "image_url": "https://cdn1.epicgames.com/salesEvent/salesEvent/EGS_Quake_idSoftwareNightdiveStudios_S2_1200x1600-79b408b699f55b5ca6014447ef556226"
}
db.session.add_all([Users.signup(**u1),Users.signup(**u2)])
db.session.commit()

#Mods(3)

m1 = {
    "title": "Scythe 2. Version 2",
    "file_id": 13600,
    "url": "https://www.doomworld.com/idgames/levels/doom2/Ports/megawads/scythe2",
    "description": 'This is the sequel to my old megawad "Scythe". Expect better looking and bigger levels. unfortunately, the last 3 levels are missing, because I am so lazy and I have not been satisfied with my attempts at making map28. I _might_ release the last 3 maps some time in the future, but do not count on it. (Update: the last 3 maps are now completed!)',
    "date_uploaded": "2006-06-05",
    "date_updated": "2022-01-02",
    "author": "Erik Alm",
    "category": "levels",
    "rating": 4.2431,
    "rating_count": 399
}

m2 = {
    "title": "Hell Revealed",
    "file_id": 7947,
    "url": "https://www.doomworld.com/idgames/themes/hr/hr",
    "description": "Hell Revealed is a megawad, a 32-level replacement for DooM II, created by Yonatan Donner and Haggay Niv. <br><br> In Hell Revealed, you will find: 32 new high-quality very detailed levels, many new graphics including textures, flats, skies, status bars and others, full skill-level support and additional attention to coop-players, and extreme challenge. <br><br> Hell Revealed supports single player, cooperative (with additional weapons and enemies) and several maps have special DM parts (maps 1 and 2 are especially good for deathmatch).",
    "date_uploaded": "1997-05-02",
    "date_updated": "2022-01-01",
    "author": "Yonatan Donner and Haggay Niv",
    "category": "themes",
    "rating": 2.6921,
    "rating_count": 458
}


m3 = {
    "title": "ALIENS Total Conversion",
    "file_id": 1038,
    "url": "https://www.doomworld.com/idgames/themes/aliens/alientc1",
    "description": '',
    "date_uploaded": "1994-11-03",
    "date_updated": "2022-01-05",
    "author": "Justin Fisher",
    "category": "themes",
    "rating": 3.4352,
    "rating_count": 108
}

db.session.add_all([Mods(**m1),Mods(**m2),Mods(**m3)])
db.session.commit()

#Records(4)
um1 = {
    "user_id": 1,
    "mod_id": 1,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": '',
    "now_playing": False
}

um2 = {
    "user_id": 1,
    "mod_id": 2,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": '',
    "now_playing": False
}
um3 = {
    "user_id": 2,
    "mod_id": 2,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": '',
    "now_playing": False
}
um4 = {
    "user_id": 2,
    "mod_id": 3,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": '',
    "now_playing": False
}

db.session.add_all([Records(**um1),Records(**um2),Records(**um3),Records(**um4)])
db.session.commit()

#Logs(9)

    #User1 got a mod.
    #User1 got another mod.
    #User1 started the first mod.
    #User1 finished the first mod.
    #User1 wrote a review of the first mod.
    #User2 got a mod.
    #User2 got another mod.
    #User2 started the second mod.
    #User2 deleted the second mod.

ul1 = {
    "record_id": 1,
    "date_added": '2022-01-03',
    "activity_type": 'Added Mod',
    "description": 'User added Scythe 2.'
}

ul2 = {
    "record_id": 2,
    "date_added": '2022-01-03',
    "activity_type": 'Added Mod',
    "description": 'User added Hell Revealed'
}
ul3 = {
    "record_id": 1,
    "date_added": '2022-01-03',
    "activity_type": 'Started Playing',
    "description": 'User started playing Scythe 2.'
}
ul4 = {
    "record_id": 1,
    "date_added": '2022-01-03',
    "activity_type": 'Finished Playing',
    "description": 'User finished playing Scythe 2.'
}
ul5 = {
    "record_id": 1,
    "date_added": '2022-01-03',
    "activity_type": 'Review',
    "description": 'User wrote a review for Scythe 2.'
}
ul6 = {
    "record_id": 3,
    "date_added": '2022-01-03',
    "activity_type": 'Added Mod',
    "description": 'User2 added Hell Revealed.'
}
ul7 = {
    "record_id": 4,
    "date_added": '2022-01-03',
    "activity_type": 'Added Mod',
    "description": 'User2 added ALIENS Total Conversion.'
}
ul8 = {
    "record_id": 3,
    "date_added": '2022-01-03',
    "activity_type": 'Started Playing',
    "description": 'User2 started playing Hell Revealed.'
}
ul9 = {
    "record_id": 3,
    "date_added": '2022-01-03',
    "activity_type": 'Deleted Mod',
    "description": 'User2 deleted Hell Revealed.'
}

db.session.add_all([Logs(**ul1),Logs(**ul2),Logs(**ul3),
    Logs(**ul4),Logs(**ul5),Logs(**ul6),Logs(**ul7),
    Logs(**ul8),Logs(**ul9)])
db.session.commit()

#Comments(3)
    #User1 comments on User2's mod pick.
    #User2 responds saying that he was disappointed.
    #User1 responds, saying that's unfortunate.

c1 = {
    "user_id": 1,
    "target_user": 2,
    "text": "Hey, I see you're playing Hell Revealed!  How is it?"
}

c2 = {
    "user_id": 2,
    "target_user": 1,
    "text": "Unfortunately I don't like this one.  It often confuses tedium for difficulty."
}
c3 = {
    "user_id": 1,
    "target_user": 2,
    "text": "Aw, that's fair.  It's an acquired taste."
}

db.session.add_all([Comments(**c1),Comments(**c2),Comments(**c3)])
db.session.commit()

# c1 = Cupcakes(
#     flavor="cherry",
#     size="large",
#     rating=5,
# )

# c2 = Cupcakes(
#     flavor="chocolate",
#     size="small",
#     rating=9,
#     image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
# )

# db.session.add_all([c1, c2])
# db.session.commit()