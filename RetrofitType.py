def SetRetrofitFiles(RetrofitClass,externalinput_path,reret,wallRet,winRet,roofRet,groundRet):
    if reret=='Y':
        if RetrofitClass=='Min':
            retinputpath=externalinput_path + '/02_RetrofitInputFiles/03_RetrofitConstructions/MinReqCon_Edited/'
        elif RetrofitClass=='Tar':
            retinputpath=externalinput_path + '/02_RetrofitInputFiles/03_RetrofitConstructions/TarReqCon_Edited/'
    else:
        retinputpath=''


    standinputpath=externalinput_path + '/01_StandardConstructions/'

    if (wallRet == 'N') & (winRet == 'N') & (roofRet == 'N') & (groundRet == 'N'):  # No retrofit
        RetType='NoRetrofit'
    elif (wallRet == 'Y') & (winRet == 'N') & (roofRet == 'N') & (groundRet == 'N'):  # Wall retrofit
        RetType='Wall'
    elif (wallRet == 'N') & (winRet == 'Y') & (roofRet == 'N') & (groundRet == 'N'): # Window retrofit
        RetType='Win'
    elif (wallRet == 'N') (winRet == 'N') & (roofRet == 'Y') & (groundRet == 'N'): # Roof retrofit
        RetType='Roof'
    elif (wallRet == 'N') & (winRet == 'N') & (roofRet == 'N') & (groundRet == 'Y'): # Ground retrofit
        RetType='Ground'
    elif (wallRet == 'Y') & (winRet == 'Y') & (roofRet == 'N') & (groundRet == 'N'): # Wall and Window retrofit
        RetType='WallWin'
    elif (wallRet == 'Y') & (winRet == 'N') & (roofRet == 'Y') & (groundRet == 'N'): # Wall and roof retrofit
        RetType='WallRoof'
    elif (wallRet == 'Y') & (winRet == 'N') & (roofRet == 'N') & (groundRet == 'Y'): # Wall and ground retrofit
        RetType='WallGround'
    elif (wallRet == 'N') & (winRet == 'Y') & (roofRet == 'Y') & (groundRet == 'N'): # Wall and Window retrofit
        RetType='WinRoof'
    elif (wallRet == 'N') & (winRet == 'Y') & (roofRet == 'N') & (groundRet == 'Y'):  # Wall and Window retrofit
        RetType='WinGround'
    elif (wallRet == 'N') & (winRet == 'N') & (roofRet == 'Y') & (groundRet == 'Y'):  # Roof and Ground retrofit
        RetType='RoofGround'
    elif (wallRet == 'Y') & (winRet == 'Y') & (roofRet == 'Y') & (groundRet == 'N'):  # Wall, Window and roof retrofit
        RetType='WallWinRoof'
    elif (wallRet == 'Y') & (winRet == 'Y') & (roofRet == 'N') & (groundRet == 'Y'):  # Wall, Window and ground retrofit
        RetType='WallWinGround'
    elif (wallRet == 'Y') & (winRet == 'N') & (roofRet == 'Y') & (groundRet == 'Y'):  # Wall, roof and ground retrofit
        RetType='WallRoofGround'
    elif (wallRet == 'Y') & winRet == 'Y' & (roofRet == 'Y') & (groundRet == 'Y'): # Full retrofit
        RetType='Full'
    else:
        RetType='InputRetError'
    return [retinputpath,RetType]
