def cryptage(cle, infoUser):
    infoUser = infoUser.lower()
    # list = a.split('*')
    # for i in range(0,len(list)):
    #     for j in list[i]:

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

print(cryptage(5,'654654*13131*Arlème-Jonhson*25'))