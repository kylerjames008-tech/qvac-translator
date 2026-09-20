import asyncio
import os
from pathlib import Path

# Try to find QVAC SDK automatically
SDK_PATHS = [
    Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "@qvac" / "sdk",
    Path(r"C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk"),
]

for sdk_path in SDK_PATHS:
    if sdk_path.exists():
        os.environ["QVAC_SDK_DIR"] = str(sdk_path)
        break

from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

async def main():
    async with Client() as client:
        t = client.transport
        model_id = await load_model(t, model_src=LLAMA_3_2_1B_INST_Q4_0)
        
        print("=" * 50)
        print("  Translator - QVAC AI")
        print("=" * 50)
        print("  Type English text to translate to Japanese")
        print("  Type 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n[English] ").strip()
                if user_input.lower() in ('quit', 'exit', 'q'):
                    print("Goodbye!")
                    break
                if not user_input:
                    continue
                
                print("[Japanese] ", end="", flush=True)
                
                prompt = f"Translate to Japanese. Only output the translation.\n\n{user_input}\nJapanese:"
                result = completion(t, model_id=model_id, history=[{"role": "user", "content": prompt}])
                translation = await result.text()
                print(translation)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break

if __name__ == "__main__":
    asyncio.run(main())
