import asyncio
import edge_tts
import json
import os

category = input("Choose a category (history, science):\n")

with open('indexes.json') as f:
    indexes = json.load(f)

start = indexes[category]
voice = "en-US-AndrewMultilingualNeural"
rate = "+0%"

def log(q_num, message, color=None):
    """Helper to format output with question number prefix"""
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'cyan': '\033[36m',
        'yellow': '\033[33m',
        'reset': '\033[0m'
    }
    
    prefix = f"[Q{q_num:03d}]"  # e.g., [Q001], [Q012], [Q150]
    
    if color and color in colors:
        print(f"{colors[color]}{prefix} {message}{colors['reset']}")
    else:
        print(f"{prefix} {message}")

async def save_audio(sem, text, filepath, voice, rate, q_num, label):
    """Save audio with retry logic and consistent logging"""
    filename = os.path.basename(filepath)
    
    async with sem:  # Limit concurrent API calls
        success = False
        attempts = 0
        
        while not success:
            attempts += 1
            try:
                await edge_tts.Communicate(
                    text=text,
                    voice=voice,
                    rate=rate
                ).save(filepath)
                success = True
                log(q_num, f"✓ Saved {label}: {filename}", 'green')
            except Exception as e:
                log(q_num, f"✗ Attempt {attempts} failed for {label}: {e}", 'red')
                await asyncio.sleep(1)  # Wait before retry

async def process_item(api_sem, item, trueindex, total, category):
    """Process one item with structured logging"""
    if trueindex < start:
        return
    
    # Progress header for this question
    progress_pct = 100 * float(trueindex)/float(total)
    log(trueindex, f"STARTING ({trueindex}/{total} - {progress_pct:.1f}%)", 'yellow')
    
    # Create tasks for all audio files this question needs
    tasks = []
    
    # Handle questions (1 or 2 parts)
    if len(item["question"]) > 1:
        log(trueindex, f"Question Part 1: {item['question'][0][:60]}...", 'cyan')
        tasks.append(save_audio(
            api_sem,
            item["question"][0], 
            f"{category}/{category}-{trueindex}-1.mp3",
            voice, rate, trueindex, "Q1"
        ))
        
        log(trueindex, f"Question Part 2: {item['question'][1][:60]}...", 'cyan')
        tasks.append(save_audio(
            api_sem,
            item["question"][1], 
            f"{category}/{category}-{trueindex}-2.mp3",
            voice, rate, trueindex, "Q2"
        ))
    else:
        log(trueindex, f"Question: {item['question'][0][:60]}...", 'cyan')
        tasks.append(save_audio(
            api_sem,
            item["question"][0], 
            f"{category}/{category}-{trueindex}-1.mp3",
            voice, rate, trueindex, "Q1"
        ))
    
    # Handle answer
    log(trueindex, f"Answer: {item['answer'][:60]}...", 'cyan')
    tasks.append(save_audio(
        api_sem,
        item["answer"], 
        f"{category}/{category}-{trueindex}-3.mp3",
        voice, rate, trueindex, "Answer"
    ))
    
    # Wait for all files of this question to complete (they still respect the global API limit)
    await asyncio.gather(*tasks)
    
    log(trueindex, f"COMPLETED all files", 'green')
    print("-" * 50)

async def generate_audio():
    with open(f'qb_{category}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(f'{category}', exist_ok=True)
    
    # Semaphore to limit API calls to 10 at a time globally
    api_sem = asyncio.Semaphore(10)
    
    # Create tasks for all items
    tasks = []
    for index, item in enumerate(data):
        trueindex = index + 1
        task = asyncio.create_task(process_item(api_sem, item, trueindex, len(data), category))
        tasks.append(task)
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks, return_exceptions=True)
    print("\n" + "=" * 50)
    print("ALL QUESTIONS PROCESSED!")
    print("=" * 50)

asyncio.run(generate_audio())
