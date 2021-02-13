def decryptage(cle, crypteinfoUser):
    crypteinfoUser = crypteinfoUser.lower() 
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    infoUserCrypted = ''
    
    for i in crypteinfoUser:
        if i.isdigit():
            if int(i) - cle < 0:
                infoUserCrypted += str(int(i) - cle + 10)
            else:
                infoUserCrypted += str(int(i) - cle)
        elif i in alpha:
            if alpha.index(i) - cle < 0:
                infoUserCrypted += alpha[alpha.index(i) - cle + 25]
            else: 
                infoUserCrypted += alpha[alpha.index(i) - cle]
        else:
            infoUserCrypted += i
    return infoUserCrypted

