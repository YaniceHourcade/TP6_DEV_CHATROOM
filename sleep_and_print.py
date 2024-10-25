import time

# Fonction qui compte jusqu'à 10
def compter_jusqua_10():
    for i in range(1, 11):
        print(i)
        time.sleep(0.5)

# Appel de la fonction deux fois
compter_jusqua_10()
compter_jusqua_10()
