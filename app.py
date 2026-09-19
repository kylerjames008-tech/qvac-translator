import os
os.environ['QVAC_SDK_DIR'] = r'C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk'

from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

async def main():
    async with Client() as client:
        transport = client.transport
        model_id = await load_model(transport, model_src=LLAMA_3_2_1B_INST_Q4_0)
        print(f"Model loaded: {model_id}")
        
        # Use the LLM to translate English to Hindi
        text = "Hello, how are you today?"
        prompt = f"Translate the following English text to Hindi: {text}"
        run = completion(transport, model_id=model_id, history=[
            {"role": "user", "content": prompt}
        ])
        final = await run.final
        print(f"Original (English): {text}")
        print(f"Translated (Hindi): {final.content_text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())