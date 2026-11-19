# OPAC Notes
OPAC is very complex, so these notes are about our config, and how we understand them to work. 
A great starting guide is the mod's [modrinth page](https://modrinth.com/mod/open-parties-and-claims), 
as it has an FAQ section which is very helpful. 


## Parties, towns, and nations
maxPartyAllies is set to 8. This means each clan of players (formerly a nation) 
can have 8 parties (towns). This is a bit complicated, as instead of discrete nations, there is now a web of allies. 
Allies are now on the town level basically instead of the nation level.

Max 10 members per party, 8 allowed allies, for a total of 80 people per nation/clan (i say per clan, but as mentioned, 
allies can form a web rather than a nation/town hierarchy).

partyExpirationTime is set to 60 days. Every 60 days at least someone in the party must log on to prevent party deletion (I think??).
Upon party deletion, the claims fall back to their default owner, the party owner. 

A player or party can remain inactive for 1 year (playerClaimsExpirationTime), upon which their claims will become expired. 
playerClaimsConvertExpiredClaims is true, which means claims are converted to the expired type, rather than being out right deleted.


## Party owned claims
Claims are owned by a party. A party is led by a single player. When a helper for example claims on the party's behalf, they are also
claiming as the party leader. 

The claim limit is set to 500. With party owned claims, this effectively serves as the claim limit per party
(what used to be how many chunks you could have as a town if you come from the Towny system). 


## Anchor based claims
This will be on so that there are no tiny claims everywhere, we want large masses
like we had with towny. 

Each party gets one anchor, with a range of 16 chunks or 256 blocks.
That means every claim of the town must be within 16 chunks of the anchor.

OPAC has no method of ensuring claims are touching, just that they are in range of the anchor. 
We will enforce in the rules that claims must be one single blob. (this can kind of be enforced
by making it so the max anchor distance is about the max amount of claims. If you want all of the claims, 
they need to be in a single blob.)


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
by one chunk, or to move the device that isnt working one block inwards.


## TLDR:
* Parties are what used to be towns
* Parties can ally with other parties
* This means allies are at the town level instead of the nation level
* Parties can have 8 allies, so what used to be called a nation can now have 8 towns
* 10 people allowed per party

* You can combine groups and sub-configs to create extremely powerful and configurable permissions
