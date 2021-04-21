# Logang_Shooter
Testing my PyGame knowledge by trying to recreate Logan's game idea

"Space shooter where the amount of asteroids spawning increase overtime to the point where it overwhelms the player"

(Logan clearly just likes to see people lose)

Hi Future Logan (23:04 | 12/04/21)


UPDATE: (19/04/21)

Okay I've finished coding the game to its 'completed' state.

And when I say completed - I mean there's one massive bug that I - for the life of me - cannot figure out

The asteroid spawn rate does not reset when a new game session is started

So, the instant you start a new game session, a fuckton of asteroids just show up on screen and then you die immediately lel

I know what's causing the issue - I just don't know how to implement a workable solution - and believe me, I've tried plenty

Guess I'm too smol brain to figure it out smh

So uhhh, good luck Logan lmao


UPDATE: (21/04/21)

I am officially the biggest brain person in the whole fucking galaxy

I fixed the asteroid cluster issue lolol

Fucking finally

Anyways it turns out what I had to do to fix the asteroid clusters that would appear on the screen the instant you start a new game session was to restart the spawn_asteroid function after pausing it in the first game loop

So, just a single line of 'spawn_asteroid(2000, 7)' fixed the whole issue, apparently

Ofc I had to figure out the giga brain idea to pause the first spawn asteroid function in the first place, which I did in the previous commit

Man am I a genius

Anyways Logan, here's your finalised game
