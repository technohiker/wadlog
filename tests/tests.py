import os
from unittest import TestCase
from dotenv import load_dotenv

from app import app
from models import db, Users, Mods, Records, Logs, Comments

load_dotenv()

# Now we can import app

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_TEST')


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


c1 = {
    "user_id": 1,
    "target_user": 2,
    "text": "Hey, I see you're playing Hell Revealed!  How is it?"
}

c2 = {
    "user_id": 2,
    "target_user": 1,
    "text": "Unfortunately I didn't like Hell Revealed.  It often confuses tedium for difficulty."
}
c3 = {
    "user_id": 1,
    "target_user": 2,
    "text": "Aw, that's fair.  It's an acquired taste."
}

class DoomTesting(TestCase):
    def setup(self):
        Users.query.delete()
        Mods.query.delete()
        Records.query.delete()
        Comments.query.delete()

        # Users:
        user1 = Users(**u1)
        user2 = Users(**u2)
        db.session.add_all([Users.signup(user1),Users.signup(user2)])
        db.session.commit()

        # Mods:
        mod1 = Mods(**m1)
        mod2 = Mods(**m2)
        mod3 = Mods(**m3)
        db.session.add_all([mod1,mod2,mod3])
        db.session.commit()

        # Records: 
        record1 = Records(**r1)
        record2 = Records(**r2)
        record3 = Records(**r3)
        record4 = Records(**r4)
        db.session.add_all([record1,record2,record3,record4])
        db.session.commit()

        # Comments:
        comm1 = Records(**c1)
        comm2 = Records(**c2)
        comm3 = Records(**c3)
        db.session.add_all([comm1,comm2,comm3])
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_front_page(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code,302)

    def test_search_page(self):
        with app.test_client() as client:
            resp_1 = client.get('/search')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn('Pull Doom mods from Idgames archive:',str(resp_1.data))

            resp_2 = client.post('/search',json={
                "query": "Sunlust",
                "type": "title",
                "sort": "date",
                'dir': 'asc'
            })
            self.assertIn("Dannebubinga",str(resp_2.data))

            resp_3 = client.post('/search',json={
                "query": "opdfbng",
                "type": "title",
                "sort": "date",
                'dir': 'asc'
            })
            self.assertIn("No files returned",str(resp_3.data))


# #Dummy test data taken from Springboard's test file.
# CUPCAKE_DATA = {
#     "flavor": "TestFlavor",
#     "size": "TestSize",
#     "rating": 5,
#     "image": "http://test.com/cupcake.jpg"
# }

# CUPCAKE_DATA_2 = {
#     "flavor": "TestFlavor2",
#     "size": "TestSize2",
#     "rating": 10,
#     "image": "http://test.com/cupcake2.jpg"
# }

# CUPCAKE_DATA_3 = {
#     "flavor": "TestFlavor3",
#     "size": "TestSize3",
#     "rating": 3,
#     "image": "http://test.com/cupcake3.jpg"
# }

# class CupcakeAPITesting(TestCase):
#     def setUp(self):
#         Cupcakes.query.delete()

#         cupcake_1 = Cupcakes(**CUPCAKE_DATA)
#         cupcake_2 = Cupcakes(**CUPCAKE_DATA_2)

#         db.session.add_all([cupcake_1,cupcake_2])
#         db.session.commit()

#         self.cupcake1 = cupcake_1
#         self.cupcake2 = cupcake_2

#     def tearDown(self):
#         db.session.rollback()

#     def test_get_cupcakes(self):
#         #Make GET request to API, then search for JSON info.
#         with app.test_client() as client:
#             response = client.get('/api/cupcakes')
#             self.assertEqual(response.status_code,200)
#             self.assertEqual(response.json,
#             {   "cupcakes": [{
#                 "id": self.cupcake1.id,
#                 "flavor": "TestFlavor",
#                 "size": "TestSize",
#                 "rating": 5,
#                 "image": "http://test.com/cupcake.jpg"
#             },
#             {   "id": self.cupcake2.id,
#                 "flavor": "TestFlavor2",
#                 "size": "TestSize2",
#                 "rating": 10,
#                 "image": "http://test.com/cupcake2.jpg"
#             }]
#             })
    