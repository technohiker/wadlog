import os
from unittest import TestCase
from dotenv import load_dotenv

from app import CURR_USER_KEY, app
from models import db, Users, Mods, Records, Comments

load_dotenv()

# Now we can import app

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_TEST')

app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()

#Users(2)

u1 = {
    "username": "testuser1",
    "email": "test@email.com",
    "password": "HASHED_PASSWORD_1"
}

u2 = {
    "username": "testuser2",
    "email": "test2@email.com",
    "password": "HASHED_PASSWORD_2",
    "image_url": "https://cdn1.epicgames.com/salesEvent/salesEvent/EGS_Quake_idSoftwareNightdiveStudios_S2_1200x1600-79b408b699f55b5ca6014447ef556226"
}
u3 = {
    "username": "testuser3",
    "email": "test3@email.com",
    "password": "HASHED_PASSWORD_3"
}

#Mods(3)

m1 = {
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

m2 = {
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

rawMod = {
    "id":18168,
    "title":"Sunlust",
    "dir":"levels/doom2/Ports/megawads/",
    "date":"2015-08-09",
    "author":"Ribbiks & Dannebubinga",
    "description":"Sunlust is a set of 32 boom-compatible maps for Doom II, designed to be played from pistol start. The maps meander through a range of themes, from traditional bases and temples to abstract hellish, void, and tech aesthetics. UV is designed primarily for ubermensch doom-gods, thus we encourage most players to start off on HMP or lower.",
    "rating":4.1147,
    "votes":218,
    "url":"https://www.doomworld.com/idgames/levels/doom2/Ports/megawads/sunlust"
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
    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        Users.query.delete()
        Mods.query.delete()
        Records.query.delete()
        Comments.query.delete()

        # Users:
        self.user1 = Users.signup(**u1)
        self.user2 = Users.signup(**u2)
        db.session.commit()

        # Mods:
        self.mod1 = Mods(**m1)
        db.session.add(self.mod1)
        db.session.commit()

        # Records: 
        self.record1 = Records(
            user_id = self.user1.id,
            mod_id=self.mod1.id,
            date_added='2022-01-03',
            play_status='Beaten',
            now_playing=False
        )
        self.record2 = Records(
            user_id = self.user2.id,
            mod_id=self.mod1.id,
            date_added='2022-01-03',
            play_status='Played',
            now_playing=True
        )
        db.session.add_all([self.record1,self.record2])
        db.session.commit()

        # Comments:
        self.comm1 = Comments(
            user_id=self.user1.id,
            target_user=self.user2.id,
            text="Hey, I see you're playing Hell Revealed!  How is it?"
        )
        self.comm2 = Comments(
            user_id=self.user2.id,
            target_user=self.user1.id,
            text="Unfortunately I didn't like Hell Revealed.  It often confuses tedium for difficulty."
        )
        db.session.add_all([self.comm1,self.comm2])
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_front_page(self):
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code,302)

    def test_search_page(self):
        with self.client as client:
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

    def test_register(self):
        """Test user registration, and ensure you can't register twice."""
        with self.client as client:
            resp_1 = client.get('/register')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn('Password',str(resp_1.data))

            resp_2 = client.post('/register',json=u3)
            self.assertEqual(resp_2.status_code,302)
            self.assertIsNotNone(Users.query.filter_by(username=u3['username']))

            resp_3 = client.post('/register',json=u2)
            self.assertEqual(resp_3.status_code,302)

    def test_login(self):
        """See if a user can login."""
        with self.client as client:
            resp_1 = client.get('/login')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn('Login',str(resp_1.data))

            resp_2 = client.post('/login',json={
                "username": "testuser1",
                "password": "HASHED_PASSWORD_1"
            })
            self.assertEqual(resp_2.status_code,302)

            resp_3 = client.get('/api/login_status')
            self.assertIn("True",str(resp_3.data))

    def test_logout(self):
        """See if a user can logout."""
        with self.client as client:
            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_3 = client.get('/api/login_status')
          #  data = json.loads(resp_3.get_data(as_text=True))
          #  self.assertEqual("True",data['status'])
            self.assertIn("True",str(resp_3.data))

            resp_1 = client.get('/logout')
            self.assertEqual(resp_1.status_code,302)

            resp_2 = client.get('/api/login_status')
            self.assertIn("False",str(resp_2.data))

    ##########################################################
    #Mods:

    def test_mod_list(self):
        """Pull the list of mods."""
        with self.client as client:

            resp_1 = client.get('/mods')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn(self.mod1.title,str(resp_1.data))
    def test_get_mod(self):
        """Test acquiring a mod page, and whether the user can add a mod to a record.
           Should only be able to add if logged in."""
        with self.client as client:

            mod2 = Mods(**m2)
            db.session.add(mod2)
            db.session.commit()

            user1_id = self.user1.id

            self.assertEqual(Records.query.filter_by(
                user_id=user1_id,mod_id=mod2.id).all(),[])

            resp_1 = client.get(f'/mods/{mod2.id}')
            self.assertEqual(resp_1.status_code,200)

            resp_2 = client.post(f'/mods/{mod2.id}')
            self.assertEqual(Records.query.filter_by(
                user_id=user1_id,mod_id=mod2.id).all(),[])

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_3 = client.post(f'/mods/{mod2.id}')
            record = Records.query.filter_by(user_id=user1_id,mod_id=mod2.id).first()
            self.assertNotEqual(record,[])

            resp_4 = client.post(f'/mods/{mod2.id}')
            record_count = len(Records.query.filter_by(user_id=user1_id,mod_id=mod2.id).all())
            self.assertEqual(record_count,1)
    
    def test_add_mod(self):
        """Adding a mod should only be done if user is logged in,
           and should check if a mod was already added."""
        with self.client as client:

            resp_1 = client.post('/api/add_mod',json=rawMod)
            self.assertIn("Unauthorized",str(resp_1.data))

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.post('/api/add_mod',json=rawMod)
            self.assertIn("Pulled!",str(resp_2.data))
            self.assertIsNotNone(Mods.query.filter_by(title='Scythe 2. Version 2.'))

            resp_3 = client.post('/api/add_mod',json=rawMod)
            self.assertIn("Already pulled.",str(resp_3.data))

    def test_delete_mod(self):
        """Have user delete a mod, if they are logged in.
           Any associated records should be deleted with it."""

        with self.client as client:
            mod_id = self.mod1.id
            resp_1 = client.post(f'/mods/{mod_id}/delete')
            self.assertNotEqual(Mods.query.get(mod_id),[])

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_1 = client.post(f'/mods/{mod_id}/delete')
            self.assertIsNone(Mods.query.get(mod_id))
    #############################################
    # Records
    
    def test_record_list(self):
        """Pull the list of records."""
        with self.client as client:
            resp_1 = client.get('/records')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn('Records',str(resp_1.data))

    def test_get_record(self):
        """Get a webpage of an individual record."""
        with self.client as client:
            resp_1 = client.get(f'/records/{self.record1.id}')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn(self.record1.mod.title,str(resp_1.data))

    def test_add_record(self):
        """Add a record.  User must be logged in."""
        with self.client as client:

            mod2 = Mods(**m2)
            db.session.add(mod2)
            db.session.commit()

            resp_1 = client.post(f'/api/add_record/{mod2.id}')
            self.assertIn("Not logged in.",str(resp_1.data))

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.post(f'/api/add_record/{mod2.id}')
            self.assertIn("Added!",str(resp_2.data))
            record = Records.query.filter_by(user_id=self.user1.id,mod_id=mod2.id).first()
            self.assertNotEqual(record,[])

            resp_3 = client.post(f'/api/add_record/{mod2.id}')
            self.assertIn("Already exists.",str(resp_3.data))
            record_count = len(Records.query.filter_by(user_id=self.user1.id,mod_id=mod2.id).all())
            self.assertEqual(record_count,1)

    def test_delete_record(self):
        """Delete a record.  User must be logged in."""

        with self.client as client:
            record_id = self.record1.id

            resp_1 = client.post(f'/records/{record_id}')
            self.assertEqual(resp_1.status_code,302)
            self.assertNotEqual(Records.query.get(record_id),[])

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.post(f'/records/{record_id}')
            self.assertEqual(resp_2.status_code,302)
            self.assertIsNone(Records.query.get(record_id))
    
    def test_edit_record(self):
        """Get a record editing form, and submit it.
           User must be logged in."""

        with self.client as client:
            edit_values = {
                "user_notes": "These are test notes.",
                "user_review": "I rate this mod 69/420.",
                "now_playing": True,
                "play_status": "Beaten",
            }
            resp_1 = client.get(f'/records/{self.record1.id}/edit')
            self.assertEqual(resp_1.status_code,302)

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.get(f'/records/{self.record1.id}/edit')
            self.assertIn('Edit',str(resp_2.data))
            self.assertEqual(resp_2.status_code,200)

            resp_3 = client.post(f'/records/{self.record1.id}/edit',json=edit_values)
            self.assertEqual(resp_3.status_code,302)
            record = Records.query.get(self.record1.id)
            self.assertEqual(record.user_notes,edit_values['user_notes'])
            self.assertEqual(record.user_review,edit_values['user_review'])
            self.assertEqual(record.play_status,edit_values['play_status'])
            self.assertEqual(record.now_playing,edit_values['now_playing'])

    ##########################################
    # Users

    def test_user_list(self):
        """Get the list of users."""
        with self.client as client:
            resp_1 = client.get('/users')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn('Users',str(resp_1.data))
    def test_get_user(self):
        """Get a webpage of an individual user."""
        with self.client as client:
            resp_1 = client.get(f'/users/{self.user1.id}')
            self.assertEqual(resp_1.status_code,200)
            self.assertIn(self.user1.username,str(resp_1.data))

    def test_edit_user(self):
        """Edit user info.  Must be logged in."""

        with self.client as client:
            user_values = {
                "email": "Thisisnotserious@outlook.com",
                "image_url": "caramelldansen.jpg"
            }
            resp_1 = client.get(f'/users/{self.user1.id}/edit')
            self.assertEqual(resp_1.status_code,302)

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.get(f'/users/{self.user1.id}/edit')
            self.assertIn('Edit Profile',str(resp_2.data))
            self.assertEqual(resp_2.status_code,200)

            resp_3 = client.post(f'/users/{self.user1.id}/edit',json=user_values)
            self.assertEqual(resp_3.status_code,302)
            users = Users.query.get(self.user1.id)
            self.assertEqual(users.email,user_values['email'])
            self.assertEqual(users.image_url,user_values['image_url'])
    #######################################
    # Comments:
    def test_add_comment(self):
        """Test adding a comment.  User must be logged in."""
        with self.client as client:
            user2_id = self.user2.id
            resp_1 = client.post(f'/api/comments/add',json=c3)
            self.assertIn('Unauthorized',str(resp_1.data))

            client.set_cookie('localhost','user',self.user1.username)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp_2 = client.post(f'/api/comments/add',json={
                "comment": c3["text"],
                "target_user": user2_id
            })
            self.assertIn('acquired',str(resp_2.data))