import asyncio
from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

async def main():
    async with Client() as client:
        t = client.transport
        model_id = await load_model(t, model_src=LLAMA_3_2_1B_INST_Q4_0)
        print(f"Model loaded: {model_id}")
        
        print("English to Japanese Translator")
        print("Type English text to translate to Japanese, or type 'quit' to exit")
        
        while True:
            user_input = input("\nEnter English: ").strip()
            if user_input.lower() in ('quit', 'exit', 'q'):
                print("Exiting...")
                break
            if not user_input:
                continue
            
            prompt = f"Translate the following English text to Japanese. Only output the translation:\n\n{user_input}"
            result = completion(t, model_id=model_id, history=[{"role": "user", "content": prompt}])
            translation = await result.text()
            print(f"Japanese: {translation}")

if __name__ == "__main__":
    asyncio.run(main())
