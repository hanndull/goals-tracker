# Goal Tracker

A practice take-home assignment from Hackbright Academy

## The Challenge

Build a goal tracking app. It should allow users to view, save, and edit goals. Users should only be able to see their own goals. Use Firebase as your database, but all other technology is up to you. Given that this will have private user data, security is important.

## My App

![alt text](/static/goaltracker.gif "GIF of site features")

## The Stack 

Firebase, Firestone, Python, Flask, JavaScript, jQuery, AJAX, HTML, Jinja, Bootstrap

## NoSQL Database Design

In the design for the Firestone db I made a users collection of user info documents, and a parallel goals collection with goal info documents (each goal doc contains a valid username from the user documents). 

#### Users Collection
    User documents -- username, password(encrypted)
#### Goals Collection
    Goal documents -- goal, goal completion date, username

## Security

I chose to "lock" access to my Firestone db instance. This rids of the visible query string on the user's end, and prevents users from accessing the data other than through my server routes. As for passwords, I decided to encrypt them upon registration. I hash and encrypt with the SHA256 algorythm using the passlib library. Whenever a user creates a new goal under their same account, or checks their saved goals, their input password is encrypted and validated against the encrypted password stored in the db. I would also plan to deploy this site in https.

On a related note, for db security, I selected a multi-region location data storage, nam5(US-Central), which Firebase docs say "can withstand the loss of entire regions and maintain availability without losing data" better than specific region selections.

#### Please check out myapproach.txt for further info 