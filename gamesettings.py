
#screen and map settings
DELTA_GAME = 50
SCREEN_SIZE = (1200, 1000)
SCREEN_FULLSCREEN = False
ENDLESS_MODE = False
MAX_FLOOR = 22

BOSS_FLOOR = 6
BLOCK_SPEED = 2
BLOCK_SIZE = 60

CAMERA_SPEED = 0
SHOOT_SPEED = 1000
SPAWN_SPEED = 15000

#settings
PLAYER_SPAWN = (SCREEN_SIZE[0] // 2 + 200, SCREEN_SIZE[1] - 300)
PLAYER_INITIAL_NEXT_LEVEL = 100
PLAYER_LEVEL_MULTIPLIER = 0.2
PLAYER_SIZE = (25,25)
PLAYER_INITIAL_DAMAGE = 50
PLAYER_INITIAL_HEALTH = 1000
PLAYER_INITIAL_MAX_HEALTH = 1000
PLAYER_INITIAL_SPEED = 4
PLAYER_INITIAL_DASH = 0
PLAYER_INITIAL_SHOOT = 0
PLAYER_INITIAL_LS = 0

PLAYER_WEAPON_SIZE = (100, 80)


#enemies settings
ENEMY_FLOOR_MULTIPLIER = 0.2

WEAKMOV_SIZE = (25, 100)
WEAKMOV_INITIAL_HEALTH = 100
WEAKMOV_INITIAL_DAMAGE = 20
WEAKMOV_INITIAL_SPEED = 2
WEAKMOV_SIGHT_RADIUS = 200
WEAKMOV_XP = 20

STRMOV_SIZE = (50, 100)
STRMOV_INITIAL_HEALTH = 200
STRMOV_INITIAL_DAMAGE = 30
STRMOV_INITIAL_SPEED = 1
STRMOV_SIGHT_RADIUS = 200
STRMOV_XP = 40

SHOOT_SIZE = (50, 50)
SHOOT_INITIAL_HEALTH = 50
SHOOT_INITIAL_DAMAGE = 15
SHOOT_TIMER = 5
SHOOT_SIGHT_RADIUS = 600
SHOOT_XP = 30

BOSS_SHOOT_SIZE = (50, 50)
BOSS_SHOOT_INITIAL_HEALTH = 200
BOSS_SHOOT_INITIAL_DAMAGE = 30
BOSS_SHOOT_MAX_OFFSET = 2
BOSS_SHOOT_XP = 50

BOSS_SIZE = (100, 100)
BOSS_INITIAL_HEALTH = 10000
BOSS_INITIAL_MAX_HEALTH = 10000
BOSS_INITIAL_DAMAGE = 10
BOSS_MAX_OFFSET = 2
BOSS_ATTACK2_PROJECTS = 20
BOSS_XP = 1000


#buffs settings
NUMBER_BUFFS = 4

DAMAGE_EFFECT = 0.2
DAMAGE_PROB = 20

JUMP_EFFECT = 1
JUMP_PROB = 10

SHOOT_EFFECT = 1
SHOOT_PROB = 15

HEALTH_EFFECT = 0.1
HEALTH_PROB = 20

VEL_EFFECT = 0.1
VEL_PROB = 15

DASH_EFFECT = 1
DASH_PROB = 10

LS_EFFECT = 0.1
LS_PROB = 10

#sprites
PLAYER_WEAPON_SPRITE = "../sprites/player/weapon.png"
PLAYER_SECRET_WEAPON = "../sprites/player/secretweapon.png"
PLAYER_IDLE_SPRITE = "../sprites/player/idle.png"
PLAYER_RUN_SPRITE = "../sprites/player/run.png"
PLAYER_BULLET_SPRITE = "../sprites/player/bullet.png"
PLAYER_JUMP_SPRITE = "../sprites/player/jump.png"

SHOOT_ENEMIES_BULLET_SPRITE = "../sprites/shotenemy/bullet.png"
SHOOT_ENEMIES_IDLE_SPRITE = "../sprites/shotenemy/Idle.png"
SHOOT_ENEMIES_ATTACK_SPRITE = "../sprites/shotenemy/Shot.png"
SHOOT_ENEMIES_DEATH_SPRITE = "../sprites/shotenemy/Dead.png"

WEAKMOV_IDLE_SPRITE = "../sprites/weakenemy/Idle.png"
WEAKMOV_ATTACK_SPRITE = "../sprites/weakenemy/Attack_1.png"
WEAKMOV_DEATH_SPRITE = "../sprites/weakenemy/Dead.png"
WEAKMOV_WALK_SPRITE = "../sprites/weakenemy/Walk.png"

STRMOV_IDLE_SPRITE = "../sprites/strongenemy/Idle.png"
STRMOV_ATTACK_SPRITE = "../sprites/strongenemy/Attack_1.png"
STRMOV_DEATH_SPRITE = "../sprites/strongenemy/Dead.png"
STRMOV_WALK_SPRITE = "../sprites/strongenemy/Walk.png"

BOSS_BULLET_SPRITE = "../sprites/boss/bullet.png"
BOSS_IDLE_SPRITE = "../sprites/boss/idle.png"
BOSS_BIRTH_SPRITE = "../sprites/boss/birth.png"
BOSS_ATTACK2_SPRITE = "../sprites/boss/attack2.png"
BOSS_DEATH_SPRITE = "../sprites/boss/death.png"

BOSS_SHOOT_BULLET_SPRITE = "../sprites/bossenemy/bullet.png"
BOSS_SHOOT_IDLE = "../sprites/bossenemy/idle.png"
BOSS_SHOOT_SHOT = "../sprites/bossenemy/shot.png"
BOSS_SHOOT_DEAD = "../sprites/bossenemy/dead.png"

DAMAGE_SPRITE = "../sprites/buffs/damage.png"
JUMP_SPRITE = "../sprites/buffs/jump.png"
SHOOT_SPRITE = "../sprites/buffs/shoot.png"
HEALTH_SPRITE = "../sprites/buffs/health.png"
VEL_SPRITE = "../sprites/buffs/speed.png"
DASH_SPRITE = "../sprites/buffs/dash.png"
LS_SPRITE = "../sprites/buffs/lifesteal.png"


KEY_SPRITE = "../sprites/grass.png"


#sfx e musica
BACKGROUND_MUSIC = "../sfx/background.mp3"
BACKGROUND2_MUSIC = "../sfx/background2.mp3"
DEATH_MUSIC = "../sfx/deathmusic.mp3"

PLAYER_ATTACK_SFX = "../sfx/player/takedamage.mp3"
PLAYER_LEVEL_SFX = "../sfx/player/levelup.mp3"
PLAYER_JUMP_SFX = "../sfx/player/jump.mp3"
PLAYER_RUN_SFX = "../sfx/player/run.mp3"
PLAYER_DEATH_SFX = "../sfx/player/death.mp3"
PLAYER_GET_SFX = "../sfx/player/getdamage.mp3"
PLAYER_SPECIAL_SFX = "../sfx/player/special.mp3"
PLAYER_SECRETATTACK_SFX = "../sfx/player/secretattack.mp3"

ENEMY_GET_SFX = "../sfx/strenemy/getdamage.mp3"

WEAKENEMY_DEATH_SFX = "../sfx/weakenemy/weakdeath.mp3"
STRENEMY_DEATH_SFX = "../sfx/strenemy/strdeath.mp3"
SHOOTENEMY_DEATH_SFX = "../sfx/shootenemy/shootdeath.mp3"

BOSS_DEATH_SFX = "../sfx/boss/bossdeath.mp3"
BOSS_BIRTH_SFX = "../sfx/boss/birthsound.mp3"