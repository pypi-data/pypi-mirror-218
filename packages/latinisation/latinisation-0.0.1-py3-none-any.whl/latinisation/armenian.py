def armenian_latinisation(prompt):
    # For example, you can use Flask to create a route that accepts POST requests with user input
    
    lst = []
    text = prompt
    wordChars = list(text)

    for i in range(len(wordChars)): # Making an array using the string.

        lst.append(wordChars[i])

    if (text.isascii() == False):

        for i in range (len(wordChars)): # Finding and changing the letters in the array.

            # Lower case letters here.

            if (lst[i] == "ա"): # 1
                lst[i] = "a"
      
            elif (lst[i] == "բ"): # 2
                lst[i] = "b"

            elif (lst[i] == "գ"): # 3
                lst[i] = "g"

            elif (lst[i] == "դ"): # 4
                lst[i] = "d"

            elif (lst[i] == "ե"): # 5
                lst[i] = "e"

            elif (lst[i] == "զ"): # 6
                lst[i] = "z"

            elif (lst[i] == "է"): # 7
                lst[i] = "e"

            elif (lst[i] == "ը"): # 8
                lst[i] = "y"

            elif (lst[i] == "թ"): # 9
                lst[i] = "t"

            elif (lst[i] == "ժ"): # 10
                lst[i] = "j"

            elif (lst[i] == "ի"): # 11
                lst[i] = "i"

            elif (lst[i] == "լ"): # 12
                lst[i] = "l"

            elif (lst[i] == "խ"): # 13
                lst[i] = "kh"

            elif (lst[i] == "ծ"): # 14
                lst[i] = "ts"

            elif (lst[i] == "կ"): # 15
                lst[i] = "k"

            elif (lst[i] == "հ"): # 16
                lst[i] = "h"

            elif (lst[i] == "ձ"): # 17
                lst[i] = "dz"

            elif (lst[i] == "ղ"): # 18
                lst[i] = "gh"

            elif (lst[i] == "ճ"): # 19
                lst[i] = "ch"

            elif (lst[i] == "մ"): # 21
                lst[i] = "m"

            elif (lst[i] == "յ"): # 22
                lst[i] = "y"

            elif (lst[i] == "ն"): # 23
                lst[i] = "n"

            elif (lst[i] == "շ"): # 24
                lst[i] = "sh"

            elif (lst[i] == "ո" and lst[i + 1] == "ւ"): # 35
                lst[i] = "u"
                lst[i + 1] = ""

            elif (lst[i] == "ո"): # 25
                if (i == 0 or lst[i - 1] == " "):
                    lst[i] = "vo"
                else:
                    lst[i] = "o"

            elif (lst[i] == "չ"): # 26
                lst[i] = "ch"

            elif (lst[i] == "պ"): # 27
                lst[i] = "p"

            elif (lst[i] == "ջ"): # 28
                lst[i] = "j"
  
            elif (lst[i] == "ռ"): # 29
                lst[i] = "r"

            elif (lst[i] == "ս"): # 30
                lst[i] = "s"

            elif (lst[i] == "վ"): # 31
                lst[i] = "v"

            elif (lst[i] == "տ"): # 32
                lst[i] = "t"

            elif (lst[i] == "ր"): # 33
                lst[i] = "r"

            elif (lst[i] == "ց"): # 34
                lst[i] = "c"

            elif (lst[i] == "փ"): # 36
                lst[i] = "p"

            elif (lst[i] == "ք"): # 37
                lst[i] = "q"

            elif (lst[i] == "և"): # 38
                lst[i] = "ev"

            elif (lst[i] == "օ"): # 39
                lst[i] = "o"

            elif (lst[i] == "ֆ"): # 40
                lst[i] = "f"

            # Higher case letters here.

            elif (lst[i] == "Ա"): # 1
                lst[i] = "A"
        
            elif (lst[i] == "Բ"): # 2
                lst[i] = "B"

            elif (lst[i] == "Գ"): # 3
                lst[i] = "G"

            elif (lst[i] == "Դ"): # 4
                lst[i] = "D"

            elif (lst[i] == "Ե"): # 5
                lst[i] = "E" 

            elif (lst[i] == "Զ"): # 6
                lst[i] = "Z"

            elif (lst[i] == "Է"): # 7
                lst[i] = "E"

            elif (lst[i] == "Ը"): # 8
                lst[i] = "Y"

            elif (lst[i] == "Թ"): # 9
                lst[i] = "T"

            elif (lst[i] == "Ժ"): # 10
                lst[i] = "J"

            elif (lst[i] == "Ի"): # 11
                lst[i] = "I"

            elif (lst[i] == "Լ"): # 12
                lst[i] = "L"

            elif (lst[i] == "Խ"): # 13
                lst[i] = "Kh"

            elif (lst[i] == "Ծ"): # 14
                lst[i] = "Ts"

            elif (lst[i] == "Կ"): # 15
                lst[i] = "K"

            elif (lst[i] == "Հ"): # 16
                lst[i] = "H"

            elif (lst[i] == "Ձ"): # 17
                lst[i] = "Dz"

            elif (lst[i] == "Ղ"): # 18
                lst[i] = "Gh"

            elif (lst[i] == "Ճ"): # 19
                lst[i] = "Ch"

            elif (lst[i] == "Մ"): # 21
                lst[i] = "M"

            elif (lst[i] == "Յ"): # 22
                lst[i] = "Y"

            elif (lst[i] == "Ն"): # 23
                lst[i] = "N"

            elif (lst[i] == "Շ"): # 24
                lst[i] = "Sh"

            elif (lst[i] == "Ո" and (lst[i + 1] == "ւ" or lst[i + 1] == "Ւ")): # 35
                lst[i] = "U"
                lst[i + 1] = ""

            elif (lst[i] == "Ո"): # 25
                if (i == 0 or lst[i - 1] == " "):
                    lst[i] = "Vo"
                else:
                    lst[i] = "O"

            elif (lst[i] == "Չ"): # 26
                lst[i] = "Ch"

            elif (lst[i] == "Պ"): # 27
                lst[i] = "P"

            elif (lst[i] == "Ջ"): # 28
                lst[i] = "J"
    
            elif (lst[i] == "Ռ"): # 29
                lst[i] = "R"

            elif (lst[i] == "Ս"): # 30
                lst[i] = "S"

            elif (lst[i] == "Վ"): # 31
                lst[i] = "V"

            elif (lst[i] == "Տ"): # 32
                lst[i] = "T"

            elif (lst[i] == "Ր"): # 33
                lst[i] = "R"

            elif (lst[i] == "Ց"): # 34
                lst[i] = "C"

            elif (lst[i] == "Փ"): # 36
                lst[i] = "P"

            elif (lst[i] == "Ք"): # 37
                lst[i] = "Q"

            elif (lst[i] == "Օ"): # 39
                lst[i] = "O"

            elif (lst[i] == "Ֆ"): # 40
                lst[i] = "F"

    listtostring = ''.join([str(elem) for i, elem in enumerate(lst)]) # Back to a string form.

    # Return the user's input as a string
    return listtostring