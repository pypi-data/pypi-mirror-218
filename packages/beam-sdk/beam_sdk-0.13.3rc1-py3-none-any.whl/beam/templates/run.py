def hello_world(**inputs):
    print("After deploying, you'll see these logs in the web dashboard 👀")
    return {"response": inputs["text"]}


if __name__ == "__main__":
    text = "Testing 123"
    hello_world(text=text)
