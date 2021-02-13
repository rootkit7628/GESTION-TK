def cryptage(cle, infoUser):
    infoUser = infoUser.lower()
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    infoUserCrypted = ''
    
    for i in infoUser:
        if i.isdigit():
            if int(i) + cle >= 10:
                infoUserCrypted += str(int(i) + cle - 10)
            else:
                infoUserCrypted += str(int(i)+cle)
        elif i in alpha:
            if alpha.index(i) + cle >= 25:
                infoUserCrypted += alpha[alpha.index(i) + cle - 25]
            else: 
                infoUserCrypted += alpha[alpha.index(i) + cle]
        else:
            infoUserCrypted += i

    return infoUserCrypted

if __name__ == "__main__":
    file = open('ident/ident.txt',"r")
    list_crypted = []

    for line in file :
        cryptedInfoUser = cryptage(int(line[-2:]), line)
        list_crypted.append(cryptedInfoUser)
    file.close()

    file = open('ident/ident.txt',"w")
    for i in list_crypted:
        file.write(i)
    file.close()


