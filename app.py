import os
os.environ['QVAC_SDK_DIR'] = r'C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk'

from tetherto.qvac_sdk import Client, load_model
from tetherto.qvac_sdk.models import BERGAMOT_EN_HI

async def main():
    async with Client() as client:
        transport = client.transport
        model_id = await load_model(transport, model_src=BERGAMOT_EN_HI)
        print(f"Model loaded: {model_id}")
        
        # Translate English to Hindi
        text = "Hello, how are you today?"
        result = await client.translate(text, source_lang="en", target_lang="hi")
        print(f"Original (English): {text}")
        print(f"Translated (Hindi): {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())