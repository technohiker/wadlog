import os
from datetime import date, datetime
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

#Records(2)
r1 = {
  #  "user_id": user1,
  #  "mod_id": mod1,
    "date_added": "2022-01-03",
    "user_review": '',
    "user_notes": '',
    "play_status": 'Unplayed',
    "now_playing": False
}

#Comments(1)
c1 = {
  #  "user_id": 1,
  #  "target_user_id": 2,
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
        self.user1 = Users(**u1)
        self.user2 = Users(**u2)
        db.session.add_all([self.user1,self.user2])
        db.session.commit()

        # Mods:
        self.mod1 = Mods(**m1)
        db.session.add(self.mod1)
        db.session.commit()

        # Records: 
        self.record1 = Records(**r1,
            user_id = self.user1.id,
            mod_id=self.mod1.id,
        )
        db.session.add(self.record1)
        db.session.commit()

        # Comments:
        self.comm1 = Comments(
            user_id=self.user1.id,
            target_user_id=self.user2.id,
            text=c1['text']
        )
        db.session.add(self.comm1)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()


    def test_user_model(self):
        """Ensure that model has values properly assigned to it."""
        self.assertEqual(self.user1.username,u1["username"])
        self.assertEqual(self.user1.email,u1["email"])

    def test_user_repr(self):
        """This message should match what is returned when user is called."""
        self.assertEqual(str(self.user1),
            f"<User: #{self.user1.id}: {self.user1.username}, {self.user1.email}>")

    def test_user_relationship(self):
        """User should have relationship objects."""
        self.assertIn(self.record1,self.user1.records)
        self.assertIn(self.comm1,self.user1.comments)

    def test_signup(self):
        """Can the user sign up?  Their password should be salted now."""
        user3 = Users.signup(**u3)
        self.assertEqual(user3.username,u3['username'])
        self.assertEqual(user3.email,u3['email'])
        self.assertNotEqual(user3.password,u3['password'])

    def test_authenticate(self):
        """Test whether user can be properly authenticated after signing up."""
        user3 = Users.signup(**u3)
        user3.authenticate(u3['username'],u3['password'])

    def test_mod_model(self):
        """Check if info of model matches what we sent."""
        json_mod = self.mod1.serialize()

        for key in m1.keys():
            self.assertEqual(json_mod[key],m1[key])

    def test_mod_relationship(self):
        """See if relationships are working."""
        self.assertIn(self.record1,self.mod1.records)

    def test_mod_repr(self):
        """Return proper values when object is called."""
        self.assertEqual(str(Mods.query.get(self.mod1.id)),
        f"<Mod: #{self.mod1.id} Title: {self.mod1.title}>")
    
    def test_record_model(self):
        """Check if info of model matches what we sent."""
        json_record = self.record1.serialize()

        for key in r1.keys():
            self.assertEqual(json_record[key],r1[key])
        self.assertEqual(json_record['user_id'],self.record1.user_id)
        self.assertEqual(json_record['mod_id'],self.record1.mod_id)

    def test_record_repr(self):
        """Return proper values when object is called."""
        self.assertEqual(str(Records.query.get(self.record1.id)),
        f"<Record: #{self.record1.id} User: #{self.record1.user_id}, Mod: #{self.record1.mod_id}>")
    
    def test_record_relationship(self):
        """See if relationships are working."""
        self.assertEqual(self.record1.user,self.user1)
        self.assertEqual(self.record1.mod,self.mod1)

    def test_comment_model(self):
        """Check if info of model matches what we sent."""
        json_comment = self.comm1.serialize()

        for key in c1.keys():
            self.assertEqual(json_comment[key],c1[key])
        self.assertEqual(json_comment['sender'],self.user1.username)
        self.assertEqual(json_comment['receiver'],self.user2.username)

    def test_comment_repr(self):
        """Return proper values when object is called."""
        
        self.assertEqual(str(Comments.query.get(self.comm1.id)),
        f"<Comment: #{self.comm1.id} User ID: #{self.comm1.user_id}, Target User: #{self.comm1.target_user_id}, Time: {self.comm1.time}, Text: {self.comm1.text}>")
    
    def test_comment_relationship(self):
        """See if relationships are working."""
        self.assertEqual(self.comm1.sender,self.user1)
        self.assertEqual(self.comm1.receiver,self.user2)