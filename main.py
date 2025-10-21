import LeituraClasses
import LeituraRaca
import Lemmatization
import Stemming

racas = [
    'dragonborn',
    'dwarf',
    'elf',
    'gnome',
    'half-elf',
    'half-orc',
    'halfling',
    'human',
    'tiefling',
]

classes = [
    'artificer',
    'barbarian',
    'bard',
    'cleric',
    'druid',
    'fighter',
    'monk',
    'paladin',
    'ranger',
    'rogue',
    'sorcerer',
    'warlock',
    'wizard',
]

def lerTodasRacas():
    for raca in racas:
        LeituraRaca.leituraRaca(raca)

def lerTodasClasses():
    for classe in classes:
        LeituraClasses.leituraClasse(classe)

def lemmatizarRacas():
    for raca in racas:
        Lemmatization.lemmatize_dnd_data_structured("raca", raca)

def lemmatizarClasses():
    for classe in classes:
        Lemmatization.lemmatize_dnd_data_structured("classe", classe)

def stemmatizarRacas():
    for raca in racas:
        Stemming.stem_dnd_data_structured("raca", raca)

def stemmatizarClasses():
    for classe in classes:
        Stemming.stem_dnd_data_structured("classe", classe)

def runAll():
    lerTodasRacas()
    lerTodasClasses()
    lemmatizarRacas()
    lemmatizarClasses()
    stemmatizarRacas()
    stemmatizarClasses()

runAll()