import math

s = "this is a string"
chars = ['s', 'a', 't']
char_hash = {
	's': 0,
	'a': 0,
	't': 0
}

char_length = 3
count = 0

j = 0
W = len(s)
for i in range(len(s)):
	if s[i] in char_hash:
		char_hash[s[i]] += 1
		if char_hash[s[i]] == 1:
			count += 1

	while (count == char_length):
		W = min(i - j + 1, W)
		print "\t-{}-{}".format(s[j:i + 1], W)
		if s[j] in char_hash:
			char_hash[s[j]] -= 1
			if char_hash[s[j]] == 0:
				count -= 1
		j += 1

print W

	

