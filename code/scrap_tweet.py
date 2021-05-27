#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import absolute_import, print_function

# Import modules
import tweepy
import dataset
from sqlalchemy.exc import ProgrammingError
import general_settings

search_terms = ["endeudado", 
                "endeudada",
                "atraso pago",
                "atraso crédito",
                "atraso credito",
                "debo crédito",
                "debo el credito", 
                "debo el crédito", 
                "debo credito",
                "debo tarjeta", 
                "debo la tarjeta",
                "atraso cuotas",
                "debo cuota",
                "debo la cuota",
                "debo cuotas",
                "debo las cuotas",
                "atraso alquiler", 
                "debo alquiler",
                "debo el alquiler",
                "atraso servicios",
                "atraso los servicios",
                "atraso luz",
                "atraso edesur",
                "atraso empe",
                "atraso edenor",
                "atraso agua",
                "atraso aysa",
                "atraso ABL",
                "atraso municipal",
                "atraso metrogas",
                "atraso gas",
                "atraso patentes",
                "atraso rentas",
                "atraso monotributo",
                "debo servicios",
                "debo los servicios",
                "debo luz",
                "debo edesur", 
                "debo edenor", 
                "debo empe", 
                "debo agua",
                "debo aysa",
                "debo ABL",
                "debo municipal",
                "debo metrogas",
                "debo gas",
                "debo patentes",
                "debo rentas",
                "debo monotributo",
                "atraso pago proveedores",
                "atraso pago salarios",
                "atraso sueldo",
                "atraso pago trabajadores",
                "sueldo atrasado",
                "pedí prestado",
                "pedi prestado",
                "pedí prestamo", 
                "pedi prestamo", 
                "pedí préstamo", 
                "pedí credito", 
                "pedi credito", 
                "pedí crédito", 
                "pedi crédito",
                "Inquilinos", 
                "inquilno",
                "inquilinas",
                "inquilina",
                "propietario",
                "propietarios",
                "propietaria",
                "propietarias", 
                "#LeydeAlquileres"]
#%%

db = dataset.connect(general_settings.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
         
    def on_status(self, status):
        id_str = status.id_str
        in_reply_to_status_id = status.in_reply_to_status_id
        in_reply_to_user_id = status.in_reply_to_user_id
        created = status.created_at
        retweeted = status.retweeted
        lang = status.lang
        source = status.source
        user_name = status.user.screen_name
        user_location = status.user.location
        
        if status.coordinates is None:
            lon, lat = None, None
        else:
            lon, lat = status.coordinates['coordinates']
            
        if status.place is None:
            place_name, place_country, place_type = None, None, None
        else:
            place_name = status.place.full_name
            place_country = status.place.country_code
            place_type = status.place.place_type
            
        user_followers = status.user.followers_count
        user_description = status.user.description
        user_created = status.user.created_at
        user_statuses_count = status.user.statuses_count
        user_verified = status.user.verified
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
        fav = status.favorite_count
        friends_count = status.user.friends_count
        rt_count = status.retweet_count 
        text = status.text
        
        table = db[general_settings.TABLE_NAME]
            
        try:
            table.insert(dict(id_str = id_str,
                  in_reply_to_status_id = in_reply_to_status_id,
                  in_reply_to_user_id = in_reply_to_user_id,
                  created = created,
                  retweeted = retweeted,
                  language = lang,
                  source = source, 
                  lon = lon,
                  lat = lat,
                  place_name = place_name,
                  place_country = place_country,
                  place_type = place_type,
                  user_name = user_name,
                  user_location = user_location,
                  user_followers = user_followers,
                  friends_count = friends_count, 
                  user_description = user_description,
                  user_created = user_created,
                  user_statuses_count = user_statuses_count,
                  user_verified = user_verified,
                  tweet = tweet,
				  text = text,
                  n_favorites = fav,
                  n_retweets = rt_count
                  ))
            #print(tw)
            #table.insert(tw)
            
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            return False


auth = tweepy.OAuthHandler(general_settings.CONSUMER_KEY, 
                           general_settings.CONSUMER_SECRET)

auth.set_access_token(general_settings.ACCESS_TOKEN, 
                      general_settings.ACCESS_TOKEN_SECRET)

stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
stream = tweepy.Stream(auth=auth, listener=stream_listener, tweet_mode='extended')
stream.filter(track=search_terms, languages=["es"])
