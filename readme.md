# WADlog

## Description:

This website allows you to look up various mods for the mid-90s PC games Doom and Doom 2, commonly distributed as WAD files. Upon booting up the website, you will be presented a form. Here, you can look up any mod by author, title, or the mod's filename. Submitting this form will pull up all of the mods that meet the given criteria. You may then add these to the application's database so they may be permanently stored for future reference. There is also an option to add the mod as a Record, which shows that you have the mod, and any notes you might want to write for it.

## Search Examples:

There are currently a few mods already available for viewing in the website. Why not use them as a starting point to see what to search for? You could search up the author of one of these mods to see what else they made.

## Tools Used:

Routes for the website were written in Python with the Flask framework, with HTML templates created with Jinja. Requests are made to https://www.doomworld.com/idgames, an archive for the vast majority of Doom mods. PostgreSQL and SQLAlchemy were used for creating and accessing the database. Python tests were handled with Unittest, and all JavaScript tests were done with Jasmine.

## How to View:

- ### **Heroku:**

  - The website may be viewed and used on [Heroku](https://doom-mod-records.herokuapp.com).

- ### **Clone Repository:**
  - If you wish to download the application yourself, clone the Git repository, and install dependencies from requirements.txt with Pip. You must create your own Postgres database in order to generate the models needed to create objects like Users and Records. There is a seed.py file to create tables and populate the database for you. Next, make a .env file with your database information as environment variables. An example file has been provided to show what the variables should look like. Once all this is set up, run Flask in the terminal, and you should not be able to run the website.

## Recollections:

Being the first project I've done on this kind of scale, I felt it was appropriate to write a more detailed summary of my experiences creating this application. This can be found [here](reflections.md).

# Image Sources:

- Default user image: https://feedback.seekingalpha.com/s/cache/8d/84/8d844a1bb966f7012aec20276f0e4283.png
- Idgames image: https://www.doomworld.com/favicon.ico
