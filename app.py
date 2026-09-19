import os
os.environ['QVAC_SDK_DIR'] = r'C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk'

import sys
sys.stdout.reconfigure(encoding='utf-8')

from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

async def main():
    async with Client() as client:
        transport = client.transport
        print("Loading model...")
        model_id = await load_model(transport, model_src=LLAMA_3_2_1B_INST_Q4_0)
        print(f"Model loaded: {model_id}")
        print("\nReady to translate! Type 'quit' to exit.\n")

        while True:
            text = input("Enter English text: ")
            if text.lower() == 'quit':
                break
            if not text.strip():
                continue

            print("Translating...")
            prompt = f"Translate to Hindi: {text}"
            run = completion(transport, model_id=model_id, history=[
                {"role": "user", "content": prompt}
            ])
            final = await run.final
            print(f"Hindi: {final.content_text}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())