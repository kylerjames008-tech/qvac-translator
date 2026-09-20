import asyncio
import sys
from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

async def main():
    async with Client() as client:
        t = client.transport
        model_id = await load_model(t, model_src=LLAMA_3_2_1B_INST_Q4_0)
        
        print("=" * 50)
        print("  QVAC English to Japanese Translator")
        print("=" * 50)
        print("  Type English text, get Japanese translation")
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
                
                prompt = f"Translate to Japanese. Be accurate and natural. Output ONLY the Japanese text, no romanization or explanations.\n\nEnglish: {user_input}\nJapanese: "
                result = completion(t, model_id=model_id, history=[{"role": "user", "content": prompt}])
                
                translation = ""
                async for chunk in result.events:
                    print(chunk.text, end="", flush=True)
                    translation += chunk.text
                
                print()  # newline after translation
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
