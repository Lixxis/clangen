Ideas:
- each NPC can become an enemy
- turn exiled / lost cats into NPC's
- combine campaign and open world events ? - maybe with a boolean, failure / success will be rolled behind or not ?
- events are binded to cats?
- this is paralell to the patrols (how often a cat can be send out is 1-2)
- fast check to imitially continue with next event?

Rolls:
- Ally (helps) - multiple possible?
- Enemy (you want to stop) - multiple possible?
- Antagonist (works against you) - multiple possible?
- KillTarget (you want to kill) - multiple possible?
- SearchTarget (you want to find) - multiple possible?
Is there a difference between KillTarget and Enemy?

Patrol:
additional screen for choosing patrol
- new button, when this is choosen -> switch to a new screen for "open quests", where they can select one

World information which has to be stored:
- on what event are we (+ current cooldown)
- which NPC is used for what Role in what story
- Which cats currently work on which event
- NPC stats (also for level up?)
idea:
{story1:{event_id,decide_cooldown,start_cooldown,[NPC's]} }
{
   NPCid: [story1, Rol]
}

o - open world
c - campain

Event information "micro events", by connecting a bigger event / storyline is created:
? micro events could be used multiple times (- (c/o) MainStoryId)
- (c/o) Id
- (c/o) Trigger event - boolean ? (if so, set contraints, which should be fulfilled (e.g. a cat is lost, countdown, relationship??))
- (c/o) Roles (for that current event)
- (c/o) Introtext (shown in the patrol text)
- (c/o) challenge to pass (4 different challenges: fight/defeat enemy, find Item, find NPC, skill test)
	> success -> list of next possible ids afterwards
	> (c) decline -> nothing is happening (only for campain events?)
	> failure -> list of next possible ids afterwards
- (o) countdown (e.g range of [0-20] moons) -> if countdown is hit, challenge will be decided