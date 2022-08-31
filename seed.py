#Copied & Pasted from Springboard's provided Seed file.

from csv import DictReader, excel
from app import db
from models import Users, Mods, Records, Comments


db.drop_all()
db.create_all()

    

#Users(2)

u1 = {
    "username": "okay_doomer",
    "email": "test@email.com",
    "password": "HASHED_PASSWORD_1"
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
r1 = {
    "user_id": 1,
    "mod_id": 1,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": 'Unplayed',
    "now_playing": False
}

r2 = {
    "user_id": 1,
    "mod_id": 2,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": 'Beaten',
    "now_playing": False
}
r3 = {
    "user_id": 2,
    "mod_id": 2,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": 'Unplayed',
    "now_playing": True
}
r4 = {
    "user_id": 2,
    "mod_id": 3,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": 'Played',
    "now_playing": False
}

db.session.add_all([Records(**r1),Records(**r2),Records(**r3),Records(**r4)])
db.session.commit()

#Comments(3)
    #User1 comments on User2's mod pick.
    #User2 responds saying that he was disappointed.
    #User1 responds, saying that's unfortunate.

c1 = {
    "user_id": 1,
    "target_user_id": 2,
    "text": "Hey, I see you're playing Hell Revealed!  How is it?"
}

c2 = {
    "user_id": 2,
    "target_user_id": 1,
    "text": "Unfortunately I didn't like Hell Revealed.  It often confuses tedium for difficulty."
}
c3 = {
    "user_id": 1,
    "target_user_id": 2,
    "text": "Aw, that's fair.  It's an acquired taste."
}

db.session.add_all([Comments(**c1),Comments(**c2),Comments(**c3)])
db.session.commit()