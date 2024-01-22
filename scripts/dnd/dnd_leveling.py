
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game


def get_leveled_cat():
	"Returns if a cat had a level up or not."
	leveled_cat = []
	for cat_id, cat in Cat.all_cats.items():
		if cat_id in game.clan.xp and cat.experience_level != game.clan.xp[cat_id]:
			leveled_cat.append(cat)
		if not cat.faded and cat_id not in game.clan.xp:
			game.clan.xp[cat_id] = cat.experience_level
	return leveled_cat

def update_levels(leveled_cats):
	"Updates the levels of the given cats in the overall game xp documentation."
	for cat in leveled_cats:
		game.clan.xp[cat.ID] = cat.experience_level