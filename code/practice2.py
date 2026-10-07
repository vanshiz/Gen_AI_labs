import tiktoken

encoder= tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size", encoder.n_vocab)

text ="The cat sat on the mat"
tokens = encoder.encode(text)
print("Tokens", tokens)

# Vocab Size 200019
# Tokens [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450])
print("Decode:",decoded)