#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent= db.Column(db.Boolean,nullable=True)
    website = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    address=db.Column(db.String())
    seeking_description = db.Column(db.String(120))
    artists = db.relationship('Artist', secondary='shows')
    ##seeking talent will be nullable later ;; 
    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'
    def get_venues(self):
        ## it will return avv venues ;; 
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),  ## to convert it into list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
         }
      
    
   

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    address = db.Column(db.String())
    seeking_description = db.Column(db.String(120))
    venues = db.relationship('Venue', secondary='shows',backref=db.backref('artist',lazy=True))
    Show = db.relationship('Show',backref='artist',lazy=True)
    def get_artist(self):
      
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),  
            # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
        }
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'  
 ##show is an ass table that has two forgin keys from Artist table and from venue table ;;  


class Show(db.Model):
   __table_name__='shows'
   id = db.Column(db.Integer,primary_key=True)
   artist_id = db.Column(db.Integer,db.ForeignKey('artists.id'),nullable=True) ## i wll change the constrains later 
   venue_id = db.Column(db.Integer,db.ForeignKey('venues.id'),nullable=True)
   start_time = db.Column(db.DateTime,nullable=False)
   venue = db.relationship('Venue')
   artist= db.relationship('Artist')
   def show_artist(self):
     ## it will return many artists 
     return{
       'artist_id':self.artist_id,
       'artist_name': self.artist.name,
       'artist_image_link': self.artist.image_link,
       'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
     }
     
     def __repr__(self):
        return f'<Show {self.id} {self.name}>'  

   def show_venue(self):
      ## same above i wll show an venues 
      return{
           'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            # convert datetime to string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
      }
   
      


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
   # TODO: replace with real venues data.
   # num_shows should be aggregated based on number of upcoming shows per venue.
   venues = Venue.query_order_by(Venue.state,Venue.city).all()
   data=[]
   holder = {}
   previous_state = None
   previous_city = None
   for venue in venues:
        venue_information = {
        'id' : venue.id,
        'name' : venue.name,
        'num_up_coming_shows': len(list(filter(lambda n: n.start_time > 
        datetime.tody(), venue.show)))
        }
        if venue.city == previous_city and venue.state == previous_state:
            holder['venues'].append(venue_information)
        else:
           if previous_city is not None:
              data.append(holder)
              holder['city'] = venue.city
              holder['state']= venue.state
              holder['venues'] = [venue_information]
           previous_city = venue.city
           previous_state = venue.state
        data.append(holder)
   return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
   search_term = request.form.get('search_term')
   result = Venue.query.filter(
   Artist.name.ilike('%{}%'.format(search_term))).all()
   response= {}
   response['count'] = len(result)
   response['data'] = result
   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  up_coming_shows = list(filter(lambda n: n.start_time > datetime.today(),venus.shows))
  past_shows = list(map(lambda z: z.show_artist(),past_shows))
  past_shows = list(filter(lambda n: n.start_time < 
  datetime.tody(),venue.shows))
  up_coming_shows= list(mab(lambda z: z.show_artist(),up_coming_shows))
  data = venue.get_venues()
  data['past_shows'] = past_shows
  data['up_coming_shows'] = up_coming_shows
  data['past_shows_count'] = len(past_shows)
  data['up_coming_shows_count'] = len(up_coming_shows)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  form = VenueForm()
  try:
     venue = Venue()
     venue.name = request.form['name']
     venue.city = request.form['city']
     venue.state = request.form['state']
     venue.phone = request.form['phone']
     venue.address= request.form['address']
     list_of_genres = request.form.getlist('genres')
     venue.genres = ','.join(list_of_genres)
     venue.website = request.form['website']
     venue.image_link = request.form['image_link']
     venue.facebook_link = request.form['facebook_link']
     venue.seeking_description = request.form['seeking_description']
     db.session.add(venue)
     db.session.commit()
  except : 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
     db.session.close()
     if error:
       # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
     else:
         flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.') 
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
   # TODO: Complete this endpoint for taking a venue_id, and using
   # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
   # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
   # clicking that button delete it from the db then redirect the user to the homepage
   error = False 
   venue = Venue.query.get(venue_id)
   try: 
      db.session.delete(venue)
      db.session.commit()
   except:
      error= True
      db.session.rollback()
      print(sys.exc_info())
   finally:
        db.session.colse()
        if error :
          flash('An error occurred. Venue '+ venue.name + ' was not deleted')
        else: 
           flash('Venue '+ venue.name + ' was deleted')
   return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
   # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
   # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
   # search for "band" should return "The Wild Sax Band".
   search_term = request.form.get('search_term')
   result = Artist.query.filter(
   Artist.name.ilike('%{}%'.format(search_term))).all()
  
   response= {}
   response['count'] = len(result)
   response['data'] = result
   return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)

  ''' it will filter the shows depends on the date of to day  and it will get the data then will be displayed'''
  past_shows = list(filter(lambda t: 
   t.start_time < datetime.today(), artist.shows
   ))

    ## same above ;; 
  up_coming_shows = list(filter(lambda t:
        t.start_time > datetime.today(), artist.shows
   ))

  past_shows = list(map(lambda t: t.show_venue(),past_shows))
  up_coming_shows = list (map(lambda t: t.show_venue(),up_coming_shows))

  data = artist.get_artist() ## collecting all the data ;;
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  data['up_coming_shows'] = up_coming_shows
  data['up_coming_shows_count'] = len(up_coming_shows)
  
  data = list(filter(lambda d: d['id'] == artist_id, Artist.query.filter_by(id=artist_id)))
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
   request = forms()
   form = request.ArtistForm(artist_id)
   artist = Artist.query.get()
   # TODO: populate form with fields from artist with ID <artist_id>
   return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
   artist = Artist.query.get(artist_id)
   error = False
   try:
     artist.name = request.form['name']
     artist.city = request.form['city']
     artist.state= request.form['state']
     artist.phone= request.form['phone']
     list_of_genres= request.form.getlist('genres')
     artist.genres = ','.join(list_of_genres)
     artist.website = request.form['website']
     artist.image_link=request.form['image_link']
     artist.facebook_link= request.form['facebook_link']
     artist.seeking_description = request.form['seeking_description']
     db.session.add(artist)
     db.session.commit()
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()
      # on successful db insert, flash success
      if error : 
       flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
       # TODO: on unsuccessful db insert, flash an error instead.
       # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      else: 
         flash('Artist ' + request.form['name'] +
          ' was successfully updated')
   return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id).get_venues
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
      error = False
      venue = Venue.query.get(venue_id)
      # TODO: take values from the form submitted, and update existing
      # venue record with ID <venue_id> using the new attributes
      try:
       venue.name = request.form['name']
       venue.city = request.form['city']
       venue.state = request.form['state']
       venue.address = request.form['address']
       venue.phone = request.form['phone']
       list_of_genres = request.form.getlist('genres')
       venue.genres = ','.join(list_of_genres)
       venue.facebook_link= request.form['facebook_link']
       db.session.add(venue)
       db.session.commit()
      except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
      finally:
       db.session.close()
       if error : 
          flash('An error occurred. Venue ' +
           request.form['name'] + ' could not be updated.')
       else: 
           flash('Venue ' +
           request.form['name'] + ' is updated.')
       return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  error = False
  try:
    artist = Artist()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state= request.form['state']
    artist.phone= request.form['phone']
    list_of_genres= request.form.getlist('genres')
    artist.genres = ','.join(list_of_genres)
    artist.website = request.form['website']
    artist.image_link=request.form['image_link']
    artist.facebook_link= request.form['facebook_link']
    artist.seeking_description = request.form['seeking_description']
    db.session.add(artist)
    db.session.commit()
  except:
     error = True
     db.session.rollback()
     print(sys.exc_info())
  finally:
     db.session.close()
     # on successful db insert, flash success
     if error : 
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
     else: 
        flash('Artist ' + request.form['name'] +
          ' was successfully listed!')

  return render_template('pages/home.html')
 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data=[]
  for show in shows: 
    data.append({
      'venue_id':show.venue.id,
      'venue_name': show.venue.name,
      'artist_id': show.artist.id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.isformat()
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  error = False
  try:
    show = Show()
    show.artist_id = request.form['artist_id']
    show.venue_id = request.form['venue_id']
    show.start_time = request.form['start_time']
    db.session.add(show)
    db.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally : 
      db.session.close()
      if error:
        # on successful db insert, flash success
        flash('An error occurred. Show could not be listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      else: 
        flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
