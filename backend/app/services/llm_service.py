import ollama


def generate(
    model,
    prompt
):
    try:
        res=ollama.chat(

            model=model,

            options={

                "temperature":0.2,

                "num_predict":180

            },

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )

        return (
            res["message"]
            ["content"]
        )
    except:
        return "model timeout"