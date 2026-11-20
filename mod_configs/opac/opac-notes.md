# OPAC Notes
OPAC is very complex, so these notes are about our config, and how we understand them to work. 
A great starting guide is the mod's [modrinth page](https://modrinth.com/mod/open-parties-and-claims), 
as it has an FAQ section which is very helpful. 


# TODO:
* Make a scripted video explaining all of this
* Go through OPAC default player config in the GUI. any settings that we noticed need to get changed, change them in the player default config. 
This way its easier to see all of the settings.
Do the same for wilderness and server claims, and the main config file where stuff is allowed or disallowed. 
* When a party is disbanded, the claims revert to personal claims. need to edit the mod tweak to unclaim everything upon party deletion or make them expired or something.
* Set up expired and wilderness claims. Make sure normal claims convert to expired, and test their perms with an alt.


## Intro
If you were a player on TEAW 4, you are familiar with Towny, and its claiming system. For numerous reasons, we have switched to 
Open Parties and Claims. This is a very different system, but works better for our needs. This guide will walk you through 
how you can set up OPAC to protect your land.



## Parties, towns, and nations
maxPartyAllies is set to 8. This means each clan of players (formerly a nation) 
can have 8 parties (towns). This is a bit complicated, as instead of discrete nations, there is now a web of allies. 
Allies are now on the town level basically instead of the nation level.

Max 10 members per party, 8 allowed allies, for a total of 80 people per nation/clan (i say per clan, but as mentioned, 
allies can form a web rather than a nation/town hierarchy).

A player or party can remain inactive for 1 year per `playerClaimsExpirationTime`, upon which their claims will become expired. 
`playerClaimsConvertExpiredClaims` is true, which means claims are converted to the expired type, rather than being out right deleted.
The expired claims have no protections, amd can be reclaimed by anyone. Game Masters will periodically delete expired claims. 
One day after that, the party is deleted per `partyExpirationTime`.


## Parties cont.
Unlike claims, parties don't have a claim GUI, but are much more simple than claims.



## Party owned claims
Claims are owned by a party. A party is led by a single player. When a helper for example claims on the party's behalf, they are also
claiming as the party leader. 



The claim limit is set to 0 for individuals, but each added party member gets 100 claims. The party leader gets a bonus 24 claims.
This means you must make a party to be able to claim. 

So for a party with 10 people, the max allowable claims is 1024.

## Anchor based claims
This will be on so that there are no tiny claims everywhere, we want large masses
like we had with towny. 

Each party gets one anchor, with a range of 16 chunks or 256 blocks.
That means every claim of the town must be within 16 chunks of the anchor.

OPAC has no method of ensuring claims are touching, just that they are in range of the anchor. 
We will enforce in the rules that claims must be one single blob. (this can kind of be enforced
by making it so the max anchor distance is about the max amount of claims. If you want all of the claims, 
they need to be in a single blob.)

## Ranks
Ranks let you assign a few key roles to people with the command `/oparties member rank {rank} {player username}`.


* `ADMIN`: has near total access to the party and its options. Admins can claim, change config settings, and add or remove players.
They cannot disband or transfer party ownership.
* `MODERATOR`: has basic member management perms. They can invite or kick lower ranking players.
* `CLAIMER`: as the name states, they can claim and unclaim chunks for the party. 
* `MEMBER`: the default. You can give this to a player with a higher rank to take away their permissions for example.

## Protections
By having different player config files, we could ship more default claims. Things like embassy or mob spawner plots. 

## Groups
Groups let you bunch certain people and other groups together. Then, when you go to adjust a setting in a claim, you can toggle
that setting by that group if you wish. This is useful for creating things like a group of helpers, who can enter a certain claim or 
bypass a certain permission for example. 

## Ranks

## Sub-claim Config profiles (mob spawner, embassy, custom, etc)
Sub-config profiles let you manage claim settings, and each profile can have different settings. You can have different claims with different profiles active.
The server ships a default profile to players, which can then be modified by them, but its recommended to stick with the defaults. Its a similar to the 
townblock permission system in Towny. 

Be sure to keep track of any changes you make, as changes are only applied to the profile you currently have selected!

Players/party leaders are allowed 4 custom profiles. You can copy the main profile to create custom sub-profiles.
These can be used to claim for things like mob spawners or embassy. 

For example, if you want create a mob farm plot, create a new profile, claim with that profile, and adjust its settings to let monsters spawn.
Then be sure to switch back to your default profile so you don't accidentally claim your land with the mob farm sub-config!

## Create's deployers, harvesters, ploughs, cart contraptions, and pistons
If you were here for the the first year or two of TEAW V4, you know that these blocks did not play well with Towny's protections.
OPAC is better in this regard, but its not perfect. 

Deployers, harvesters, ploughs, cart contraptions, and pistons generally work fine inside of claims, 
except for **one block inward from the chunk boundary on a claim border.** In other words, if your Create device is in your claim, 
but _right next_ to wilderness or another claim, it will not work.

This is due to how OPAC handles grief protection, and is a feature not a bug™. If you run into this, the easiest fix is to extend your claim
by one chunk, or to move the device that isn't working one block inwards.


## TLDR:
* Parties are what used to be towns
* Parties can ally with other parties (this means allies are at the town level instead of the nation level)
* Parties can have 8 allies
* 10 people allowed per party
* You can combine groups and sub-configs to create extremely powerful and configurable permissions
* Claims and parties expire after one year of complete inactivity from a party





 


## Game Master notes
`playerConfigurablePlayerConfigOptions` in the server config is the holy grail option, it tells players what options they can/can't edit. 
You can change the option status in the player config after allowing removing an option for example to force a setting on/off.