import asyncio
import edge_tts
import json
import os

category = input("Choose a category (history, science):\n")

with open('indexes.json') as f:
    indexes = json.load(f)

start = indexes[category]

async def generate_audio():
    with open(f'qb_{category}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(f'{category}', exist_ok=True)

    voice = "en-US-AndrewMultilingualNeural"
    rate = "+0%"

    for index, item in enumerate(data):

        
        trueindex = index + 1
        if trueindex >= start:
            print(f"\033[31mQuestion {trueindex} of {len(data)}\033[0m")
            print(f"\033[92m\033[1m\033[4m\033[32mWe are {100 * float(trueindex)/float(len(data)):.4f}% of the way there!\033[0m")
            if len(item["question"]) > 1:
                print("\033[36mSaving - Question part 1:\033[0m", item["question"][0])

                success = False
                while not success:
                    try:
                        await edge_tts.Communicate(
                            text=item["question"][0],
                            voice=voice,
                            rate=rate
                        ).save(f"{category}/{category}-{trueindex}-1.mp3")
                        success = True
                    except Exception as e:
                        print(e)

                print("\033[36mSaving - Question part 2:\033[0m", item["question"][1])

                success = False
                while not success:
                    try:
                        await edge_tts.Communicate(
                            text=item["question"][1],
                            voice=voice,
                            rate=rate
                        ).save(f"{category}/{category}-{trueindex}-2.mp3")
                        success = True
                    except Exception as e:
                        print(e)
            else:
                print("\033[36mSaving - Question:\033[0m", item["question"][0])

                success = False
                while not success:
                    try:
                        await edge_tts.Communicate(
                            text=item["question"][0],
                            voice=voice,
                            rate=rate
                        ).save(f"{category}/{category}-{trueindex}-1.mp3")
                        success = True
                    except Exception as e:
                        print(e)

            print("\033[36mSaving - Answer:\033[0m", item["answer"])

            success = False
            while not success:
                try:
                    await edge_tts.Communicate(
                        text=item["answer"],
                        voice=voice,
                        rate=rate
                    ).save(f"{category}/{category}-{trueindex}-3.mp3")
                    success = True
                except Exception as e:
                    print(e)

            print("---")

asyncio.run(generate_audio())

