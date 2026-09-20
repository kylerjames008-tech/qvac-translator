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
                
                # Stricter prompt with few-shot examples
                prompt = f"""Translate English to Japanese. ONLY output the translation.

Examples:
- hello → こんにちは
- thank you → ありがとう
- how are you → お元気ですか

Now translate:
{user_input}
Japanese:"""
                result = completion(t, model_id=model_id, history=[{"role": "user", "content": prompt}])
                
                translation = await result.text()
                # Clean up the output - remove any repetition
                print(translation.strip())
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
