import asyncio
import edge_tts
import json
import os

async def generate_audio(category):
    with open(f'qb_{category}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(f'{category}', exist_ok=True)

    voice = "en-US-AndrewMultilingualNeural"
    rate = "+0%"

    for index, item in enumerate(data):
        trueindex = index + 1 
        print(f"\033[31mQuestion {trueindex} of {len(data)}\033[0m")
        print(f"\033[92m\033[1m\033[4m\033[32mWe are {100 * float(trueindex)/float(len(data)):.4f}% of the way there!\033[0m")
        if len(item["question"]) > 1:
            print("\033[36mSaving - Question part 1:\033[0m", item["question"][0])
            await edge_tts.Communicate(
                text=item["question"][0],
                voice=voice,
                rate=rate
            ).save(f"{category}/{category}-{trueindex}-1.mp3")

            print("\033[36mSaving - Question part 2:\033[0m", item["question"][1])
            await edge_tts.Communicate(
                text=item["question"][1],
                voice=voice,
                rate=rate
            ).save(f"{category}/{category}-{trueindex}-2.mp3")
        else:
            print("\033[36mSaving - Question:\033[0m", item["question"][0])
            await edge_tts.Communicate(
                text=item["question"][0],
                voice=voice,
                rate=rate
            ).save(f"{category}/{category}-{trueindex}-1.mp3")

        print("\033[36mSaving - Answer:\033[0m", item["answer"])
        await edge_tts.Communicate(
            text=item["answer"],
            voice=voice,
            rate=rate
        ).save(f"{category}/{category}-{trueindex}-3.mp3")

        print("---")

asyncio.run(generate_audio("history"))
asyncio.run(generate_audio("science"))

