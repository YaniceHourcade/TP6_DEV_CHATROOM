import asyncio

# Fonction asynchrone qui compte jusqu'à 10 avec un délai de 0.5 seconde
async def compter_jusqua_10():
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(0.5)

async def main():
    await asyncio.gather(compter_jusqua_10(), compter_jusqua_10())

# Exécution du programme
if __name__ == "__main__":
    asyncio.run(main())
