word1=input("Enter the string1: ")
word2=input("Enter the string2: ")


for i in word1:
    for j in word2:
        if i==j:
            word1=word1.replace(i,'#')
            word2=word2.replace(j,'#')
            break


found=True
for i in word1:
        for j in word2:
            if i!=j:

                print(f"{word1}{word2} is not anagram ")
                found=False
                break
        if found==False:
         break

if found==True:
     print("It is anagram")
