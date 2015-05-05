#!/usr/bin/python

import re
import sys

A_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. ([\w\s\-]+) получает ([\d\s]+) ед\. урона")
A_TO_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. Вы получ(аете|или) ([\d\s]+) ед\. урона")
DOT_ATK_TO_A = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): ([\w\s\-]+) получает ([\d\s]+) ед\. урона\.\s*\Z")

A_TO_B_AUTO = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) наносит ([\d\s]+) ед\. урона цели ([\w\s\-]+)")
A_TO_BB_AUTO = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) наносит персонажу ([\w\s\-]+) ([\d\s]+) ед\. урона")
A_TO_ME_AUTO = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) наносит вам ([\d\s]+) ед\. урона")
ME_TO_A_AUTO = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы нанесли ([\d\s]+) ед\.( критического)? урона цели ([\w\s\-]+)")

POISON_TO_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): вы отравлены и получаете ([\d\s]+) ед\. урона")
A_POISING_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. Вы отравлены")
POISON_SHOT = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) получает ([\d\s]+) урона и отравление от умения ([\w\s\-:]+)")
A_POISING_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. ([\w\s\-]+)  ощущает действие яда")
ME_POISIING_A = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): ([\w\s\-]+) чувствует действие яда")

DOT_ON_ME_OR_OTHER = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): вы получаете ([\d\s]+) ед\. урона\.")
USING_A_SKILL = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\.\s*\Z")

EFFECT_UZ_ME_TO_A = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы использовали: ([\w\s\-:]+)\. ([\w\s\-]+) получает эффект неотвратимых уз\.")
EFFECT_UZ_A_TO_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. Вы получаете эффект неотвратимых уз\.")
EFFECT_UZ_A_TO_A = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+), накладывая на себя неотвратимые узы\.")
EFFECT_UZ_A_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. ([\w\s\-]+) получает эффект неотвратимых уз\.")

DRAIN_ME_TO_SELF = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): вы получаете продолжительный урон\.")
DRAIN_ME_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): ([\w\s\-]+) получает продолжительный урон\.")
DRAIN_A_TO_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. Вы получаете продолжительный урон\.")
DRAIN_A_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. ([\w\s\-]+) постоянно получает урон\.")

FLASH_ME_TO_A = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы используете: ([\w\s\-:]+)\. ([\w\s\-]+) получает эффект неотвратимой вспышки\.")
FLASH_A_TO_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. Вы получаете эффект неотвратимой вспышки\.")
FLASH_A_TO_SELF = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-:]+): ([\w\s\-]+) получает урон\.")
FLASH_A_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) использует: ([\w\s\-:]+)\. ([\w\s\-]+) получает эффект неотвратимой вспышки\.")

REFLECT_SKILL_ME_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы получили ([\d\s]+) ед\. урона от отражения умения ([\w\s\-:]+), использованного против цели ([\w\s\-]+)\.")
REFLECT_SKILL_A_to_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы отразили умение ([\w\s\-:]+) и нанесли ([\d\s]+) ед\. урона цели ([\w\s\-]+)\.")
REFLECT_SKILL_A_to_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) отражает умение \"([\w\s\-:]+)\" и наносит ([\d\s]+) ед\. урона цели ([\w\s\-]+)\.")

REFLECT_ATK_ME_TO_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) отражает атаку и наносит ([\d\s]+) ед\. урона\.")
REFLECT_ATK_A_to_ME = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?Вы отразили умение и нанесли персонажу ([\w\s\-]+) ([\d\s]+) ед\. урона\.")
REFLECT_ATK_A_to_B = re.compile("\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d : (Критический удар! )?([\w\s\-]+) отражает атаку и наносит персонажу ([\w\s\-]+) ([\d\s]+) ед\. урона\.")


GS = re.compile("магический урон")
dmgcutter = re.compile("[^0-9]")
roman = re.compile("([\w\s\-]+)(\s[IXV]+)\Z")

class TargetDamage:
	critical = False
	skillname = ""
	skillStrip = ""
	dmg = 0
	dot = False
	
class TargetInfo:
	dps = 0
	dmgList = None

class CharDamage:
	targets = None
	charName = ""
	dps = 0
	
def ParseDotsFile(filename):
	fl = open(filename, "rb")
	dotsNames = set()
	splitter = re.compile(",?\d+:")
	while True:
		fl.readline()
		dotsline = fl.readline().decode("CP1251").rstrip()
		if (not dotsline):
			break
		
		for skill in splitter.split(dotsline):
			if (skill):
				dotsNames.add(skill.lower())
		
	fl.close
	return dotsNames
	
Actors = dict()
SkillLast = dict()
PassiveSkill = dict()
DotsNames = None

def stripRoman(skillname):
	ps = roman.match(skillname)
	if (ps):
		return ps.group(1)
	return skillname
	
def skillUsed(target, skill, actor):
	dotTgt = SkillLast.get(target)
	if (dotTgt == None):
		dotTgt = dict()
		SkillLast[target] = dotTgt
	
	dotTgt[skill] = actor
	
def effectUsed(who, target, skill):
	actor = Actors.get(who)
	if (actor == None):
		actor = CharDamage()
		actor.targets = dict()
		actor.charName = who
		Actors[who] = actor
	
	skillUsed(target, skill, actor)

def skillDamage(who, skill, sskill, target, dmg, crit, dot = False):
	actor = Actors.get(who)
	if (actor == None):
		actor = CharDamage()
		actor.targets = dict()
		actor.charName = who
		Actors[who] = actor
	
	tgtDmg = actor.targets.get(target)
	if (tgtDmg == None):
		tgtDmg = TargetInfo()
		tgtDmg.dmgList = list()
		tgtDmg.dps = 0
		tgtDmg.dot = dot
		actor.targets[target] = tgtDmg
	
	damage = TargetDamage()
	damage.dmg = dmg
	damage.critical = crit
	damage.skillname = skill
	damage.skillStrip = sskill
	
	tgtDmg.dmgList.append(damage)
	tgtDmg.dps += dmg
	actor.dps += dmg
	
	#Запоминаем кто последний давал скил
	skillUsed(target, sskill, actor)
	
def dotDamage(skill, sskill, target, dmg, crit):
	tgt = SkillLast.get(target)
	actor = None
	if (tgt):
		actor = tgt.get(sskill)
		
	if (actor == None):
		act = PassiveSkill.get(sskill)
		if (act):
			actor = Actors.get(act)
		
	if (actor == None):
		skillDamage("\" \"", skill, sskill, target, dmg, crit, True)
	else:
		skillDamage(actor.charName, skill, sskill, target, dmg, crit, True)
	
def skillPassive(who, skill):
	PassiveSkill[skill] = who
	
def dmgcut(dmgstr):
	return int(dmgcutter.sub("",dmgstr))




def REFLECT_SKILL(txline):
	#Отражение урона скилла по нам
	ps = REFLECT_SKILL_ME_TO_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(4)
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		target = "Вы"
		dmg = dmgcut(ps.group(2))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
		
	#Отражение урона скилла в кого-то
	ps = REFLECT_SKILL_A_to_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = "Вы"
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()
		target = ps.group(4)
		dmg = dmgcut(ps.group(3))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
		
	#Отражение кем-то урона скилла в кого-то
	ps = REFLECT_SKILL_A_to_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(2)
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		target = ps.group(5)
		dmg = dmgcut(ps.group(4))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
	return False




	
def REFLECT_ATK(txline):
	#Отражение урона атакой по нам
	ps = REFLECT_ATK_ME_TO_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(2)
		skill = "атака"
		sskill = stripRoman(skill).lower()
		target = "Вы"
		dmg = dmgcut(ps.group(3))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
		
	#Отражение урона атакой в кого-то
	ps = REFLECT_ATK_A_to_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = "Вы"
		skill = "атака"
		sskill = stripRoman(skill).lower()
		target = ps.group(3)
		dmg = dmgcut(ps.group(4))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
		
	#Отражение кем-то урона атакой в кого-то
	ps = REFLECT_ATK_A_to_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(2)
		skill = "атака"
		sskill = stripRoman(skill).lower()
		target = ps.group(3)
		dmg = dmgcut(ps.group(4))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
	return False





def EFFECT_UZ(txline):
	#Эффект уз Мы на кого-то
	ps = EFFECT_UZ_ME_TO_A.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()	
		who = "Вы"	
		target = ps.group(3)
		effectUsed(who, target, sskill)			
		return True
		
	#Эффект уз Кто-то на нас
	ps = EFFECT_UZ_A_TO_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = "Вы"
		effectUsed(who, target, sskill)
		return True
		
	#Эффект уз Кто-то на себя
	ps = EFFECT_UZ_A_TO_A.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = who
		effectUsed(who, target, sskill)
		return True
		
	#Эффект уз Кто-то на Кого-то
	ps = EFFECT_UZ_A_TO_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = ps.group(4)
		effectUsed(who, target, sskill)
		return True
	return False






def FLASH(txline):
	#Вспышка мы по кому-то
	ps = FLASH_ME_TO_A.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()
		who = "Вы"
		target = ps.group(3)
		effectUsed(who, target, sskill)
		return True
	
	#Вспышка кого-то на меня
	ps = FLASH_A_TO_ME.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = "Вы"
		effectUsed(who, target, sskill)
		return True
	
	#Вспышка кого-то на самого-себя
	ps = FLASH_A_TO_SELF.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()
		who = ps.group(3)
		target = who
		effectUsed(who, target, sskill)
		return True
		
	#Вспышка кого-то на кого-то
	ps = FLASH_A_TO_B.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = ps.group(4)
		effectUsed(who, target, sskill)
		return True
	return False





def DRAIN(txline):
	#Продолжнительный урон сам на себя
	ps = DRAIN_ME_TO_SELF.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()
		who = "Вы"
		target = who
		effectUsed(who, target, sskill)
		return True
		
	#Продолжнительный урон на нас
	ps = DRAIN_A_TO_ME.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = "Вы"
		effectUsed(who, target, sskill)
		return True
		
	#Продолжнительный урон мы на кого-то
	ps = DRAIN_ME_TO_B.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()
		who = "Вы"
		target = ps.group(3)
		effectUsed(who, target, sskill)
		return True
		
	#Продолжнительный урон кто-то на кого-то
	ps = DRAIN_A_TO_B.match(txline)

	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		who = ps.group(2)
		target = ps.group(4)
		effectUsed(who, target, sskill)
		return True
	return False





def AUTO_ATK(txline):
	#Авто-атака кто-то по цели
	ps = A_TO_B_AUTO.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = "атака"
		sskill = stripRoman(skill).lower()		
		target = ps.group(4)
		dmg = dmgcut(ps.group(3))
		who = ps.group(2)
		skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
	
	#Авто-атака кто-то по персонажу
	ps = A_TO_BB_AUTO.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = "атака"
		sskill = stripRoman(skill).lower()		
		target = ps.group(3)
		dmg = dmgcut(ps.group(4))
		who = ps.group(2)
		skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
		
	#Авто-атака кого-то по нам
	ps = A_TO_ME_AUTO.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = "атака"
		sskill = stripRoman(skill).lower()		
		target = "Вы"
		dmg = dmgcut(ps.group(3))
		who = ps.group(2)
		skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
		
	#Наша авто-атака по цели
	ps = ME_TO_A_AUTO.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = "атака"
		sskill = stripRoman(skill).lower()		
		target = ps.group(4)
		dmg = dmgcut(ps.group(2))
		who = "Вы"
		skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
		
	return False





def POISON(txline):
	#Действие яда на нас
	ps = POISON_TO_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()		
		target = "Вы"
		dmg = dmgcut(ps.group(3))
		dotDamage(skill, sskill, target, dmg, crit)
			
		return True
	
	#Отравили нас
	ps = A_POISING_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()		
		who = ps.group(2)
		target = "Вы"
		effectUsed(who, target, sskill)
			
		return True
	
	#Умение с отравлением от нас
	ps = POISON_SHOT.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(4)
		sskill = stripRoman(skill).lower()		
		who = "Вы"
		target = ps.group(2)
		dmg = dmgcut(ps.group(3))
		skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
		
	#A травит B
	ps = A_POISING_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()		
		who = ps.group(2)
		target = ps.group(4)
		effectUsed(who, target, sskill)
			
		return True
		
	#Мы травим A
	ps = ME_POISIING_A.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()		
		who = "Вы"
		target = ps.group(3)
		effectUsed(who, target, sskill)
			
		return True
	return False


def SKILL(txline):
	#Скилл по мне
	ps = A_TO_ME.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(2)
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		target = "Вы"
		dmg = dmgcut(ps.group(5))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
		
	#Чей-то скилл по цели
	ps = A_TO_B.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		who = ps.group(2)
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()
		target = ps.group(4)
		dmg = dmgcut(ps.group(5))
		
		skillDamage(who, skill, sskill, target, dmg, crit)
		return True
	
	#Дот или наша атака скилом на кого-то или ГС
	ps = DOT_ATK_TO_A.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()		
		target = ps.group(3)
		dmg = dmgcut(ps.group(4))
		who = ""
		if (sskill in DotsNames): # Дот
			dotDamage(skill, sskill, target, dmg, crit)
		elif ( GS.match(sskill) ): # ГС
			skillDamage(skill, skill, sskill, target, dmg, crit)
		else: # Наш скил
			who = "Вы"
			skillDamage(who, skill, sskill, target, dmg, crit)
			
		return True
	
	#Маг дот, вроде, по нам
	ps = DOT_ON_ME_OR_OTHER.match(txline)
		
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(2)
		sskill = stripRoman(skill).lower()		
		target = "Вы"
		dmg = dmgcut(ps.group(3))
		dotDamage(skill, sskill, target, dmg, crit)
		return True
	
	return False



def USING_SKILL(txline):
	#Просто использует
	ps = USING_A_SKILL.match(txline)
	
	if (ps):
		crit = ps.group(1) != None
		skill = ps.group(3)
		sskill = stripRoman(skill).lower()	
		who = ps.group(2)		
		skillPassive(who, sskill)	
		return True
		
	return False

	
def matcher(txline):

	if (REFLECT_SKILL(txline)):
		return

	if (REFLECT_ATK(txline)):
		return
	
	if (EFFECT_UZ(txline)):
		return
	
	if (FLASH(txline)):
		return
		
	if (DRAIN(txline)):
		return
		
	if (POISON(txline)):
		return
		
	if (AUTO_ATK(txline)):
		return
		
	if (SKILL(txline)):
		return
		
	if (USING_SKILL(txline)):
		return
	


options = dict()
options["log"] = "Chat.log"
options["wrkdir"] = "./"

verbose = 0
mode = 0
monster = ""

# Рабочий каталог
for idx, p in enumerate(sys.argv):
	if (re.match("-w\Z", p)):
		if (len(sys.argv) >= idx + 2):
			options["wrkdir"] = sys.argv[idx + 1]		
			

#### Читаем опции
opts = open(options["wrkdir"] + "/" + "options.txt","rb")
if (opts):
	optln = opts.readline()
	while(optln):
		optln = optln.decode("CP1251")
		
		p = optln.split("=")
		
		if (len(p) == 2):
			options[p[0].strip()] = p[1].strip()
		
		optln = opts.readline()
	
	opts.close()
	
#Опции 
for idx, p in enumerate(sys.argv):
	if (re.match("-v+\Z", p)):
		verbose = p.count("v")
	elif (re.match("-m\Z", p)):
		if (len(sys.argv) >= idx + 2):
			mode = 1
			monster = sys.argv[idx + 1].lower()
	elif (re.match("-k\Z", p)):
		if (len(sys.argv) >= idx + 2):
			mode = 2
			monster = sys.argv[idx + 1]
	elif (re.match("-l\Z", p)):
		if (len(sys.argv) >= idx + 2):
			options["log"] = sys.argv[idx + 1]	
	
	
#### Читаем названия дотов
	
DotsNames = ParseDotsFile(options["wrkdir"] + "/" + "dots.txt")

#### Парсим лог-файл

chatlog = open(options["log"],"rb")
line = chatlog.readline()
while (line):

	line = line.decode("CP1251")
	
	matcher(line)
	
	line = chatlog.readline()

chatlog.close()



#Вывод дпса
if (mode == 0):
	for (Who, info) in sorted(Actors.items(), key=lambda x: x[1].dps):
		print(Who + " : " + str(info.dps))
		
		if (verbose >= 1):
			for (Tgt, dmginfo) in sorted(info.targets.items(), key=lambda x: x[1].dps):
				print ("\t" + Tgt + "\t " + str(dmginfo.dps))
				
				if ( (verbose >= 2 and Who == "\" \"") or verbose >= 3):
					for i in dmginfo.dmgList:
						if (i.critical):
							print ("\t\t" + i.skillname + " : " + str(i.dmg) + " \t Critical")
						else:
							print ("\t\t" + i.skillname + " : " + str(i.dmg)  + " ")

elif (mode == 1):
	for (Who, info) in Actors.items():		
		for (Tgt, dmginfo) in info.targets.items():
			if (Tgt.lower() == monster):
				print(Who)
				print ("\t" + Tgt + "\t " + str(dmginfo.dps))
				if ( (verbose >= 1 and Who == "\" \"") or verbose >= 2):
					for i in dmginfo.dmgList:
						if (i.critical):
							print ("\t\t" + i.skillname + " : " + str(i.dmg) + " \t Critical")
						else:
							print ("\t\t" + i.skillname + " : " + str(i.dmg)  + " ")
elif (mode == 2):
	Who = monster
	info = Actors.get(Who)
	if (info):
		print(Who + " : " + str(info.dps))
		
		for (Tgt, dmginfo) in sorted(info.targets.items(), key=lambda x: x[1].dps):
			print ("\t" + Tgt + "\t " + str(dmginfo.dps))
				
			if ( verbose >= 1):
				for i in dmginfo.dmgList:
					if (i.critical):
						print ("\t\t" + i.skillname + " : " + str(i.dmg) + " \t Critical")
					else:
						print ("\t\t" + i.skillname + " : " + str(i.dmg)  + " ")
