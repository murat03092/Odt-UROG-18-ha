#!/usr/bin/env python3


import asyncio
import time
import math
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed, VelocityNedYaw)


async def run():
    
    
    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial:///dev/ttyACM0:57600")
    print("bağlantı bekleniyor")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"SERÇEDES Bulundu....")
            break

    print("-- Arm Oluyor..")
    await drone.action.arm()
    print("-- Kalkıyor....")
    await drone.action.takeoff()
    await asyncio.sleep(4)
    time.sleep(6)

    print("-- Başlangıç Boktası Ayarlandı..")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Offboard Mode Başlatıldı")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboar mode baslatılması : \
              {error._result.result} nedeniyle hata verdi.. ")
        print("-- Motorlar Duruyor..")
        await drone.action.disarm()
        return

#######################BİRİNCİ GÖREV-- KÜP ÇİZİMİ###########################
    ilerigeri = [1,0,-1,0,0,1,0,-1,0,1,0,0,0,-1,0]
    sagsol=[0,1,0,-1,0,0,1,0,-1,0,0,1,0,0,0]
    yukariasagi = [0,0,0,0,-1,0,0,0,0,0,1,0,-1,0,1]
    hizyatay = 3.3
    hizdikey = 2.9
    zaman = [hizyatay,hizyatay,hizyatay,hizyatay,hizdikey,hizyatay,hizyatay,hizyatay,
             hizyatay,hizyatay,hizdikey,hizyatay,hizdikey,hizyatay,hizdikey]
    yönerge =["ileri","sag","geri","sol","yukari","ileri","sag","geri","sol","ileri","asagi (1. dikme)","sag",
                 "yukari (2. dikme)","geri","asagi (3. Dikme )"]
    for sira in range(0,15,1):
           print(f'5 metre {yönerge[sira]} gidecek')
           await drone.offboard.set_velocity_body(
              VelocityBodyYawspeed(ilerigeri[sira], sagsol[sira], yukariasagi[sira], 0.0))
           await asyncio.sleep(zaman[sira])
           print("-- 2 sn bekle")
           await drone.offboard.set_velocity_body(
              VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
           await asyncio.sleep(2.0)


    print("-- KARE TAMAMLANDI, İKİNCİ GÖREVE 3sn Sonra GEÇİLECEK...")
    print("-- 2 sn bekle")
    await drone.offboard.set_velocity_body(
       VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1.0)
######################İKİNCİ GÖREV-- EŞKENAR ÜÇGEN ÇİZİMİ######################
    for tur in range (1,6,1):
                print(f'{tur}. Tur Yapılıyor..')
                for a in range (0,9,1):
                        aci = (60*(math.sin(a*10*(math.pi/180))))
                        hiz = 0.77+0.073*(math.cos(a*10*(math.pi/180)))
                        await drone.offboard.set_velocity_ned(
                              VelocityNedYaw(hiz*0.866, -hiz*0.5, 0.0, aci))
                        await asyncio.sleep(0.32)
                        #print("Uçgen-1 Yazılan Açı:", aci)
                
                for b in range (10,19,1):
                        aci2 = (60*(2-(math.sin(b*10*(math.pi/180)))))
                        hiz2 = 0.77+0.073*(math.cos(b*10*(math.pi/180)))
                        await drone.offboard.set_velocity_ned(
			   VelocityNedYaw(hiz2*0.866, -hiz2*0.5, 0.0, aci2))
                        await asyncio.sleep(0.32)
                await drone.offboard.set_velocity_body(
                     VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
                await asyncio.sleep(1.5)
#####-----------------------------------------------------------------------------
                for c in range (0,9,1):
                        aci3 = (120+(60*(math.sin(c*10*(math.pi/180)))))
                        hiz3 = 0.79+(0.275*(math.cos(c*10*(math.pi/180))))
                        await drone.offboard.set_velocity_ned(
			   VelocityNedYaw(0.0, hiz3, 0.0, aci3))
                        await asyncio.sleep(0.335)
                        #print("Uçgen-1 Yazılan Açı:", aci)
                for d in range (10,19,1):
                        aci4 = (120+(60*(2-(math.sin(d*10*(math.pi/180))))))
                        hiz4 = 0.79+(0.275*(math.cos(d*10*(math.pi/180))))
                        await drone.offboard.set_velocity_ned(
			   VelocityNedYaw(0.0, hiz4, 0.0, aci4))
                        await asyncio.sleep(0.335)   
                await drone.offboard.set_velocity_body(
                     VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
                await asyncio.sleep(1.5) 
####--------------------------------------------------------------------------------
                for e in range (0,9,1):
                        aci5 = 240+60*(math.sin(e*10*(math.pi/180)))
                        hiz5 = 0.71+(0.3230*(math.cos(3*10*(math.pi/180))))
                        await drone.offboard.set_velocity_ned(
			   VelocityNedYaw(-hiz5*0.866, -hiz5*0.5, 0.0, aci5))
                        await asyncio.sleep(0.34)
                        #print("Uçgen-1 Yazılan Açı:", aci5)
                for f in range (10,19,1):
                        aci6 = (240+(60*(2-(math.sin(f*10*(math.pi/180))))))
                        hiz6 = 0.71+(0.3230*(math.cos(f*10*(math.pi/180))))
                        await drone.offboard.set_velocity_ned(
			   VelocityNedYaw(-hiz6*0.866, -hiz6*0.5, 0.0, aci6))
                        await asyncio.sleep(0.34)
                print("-- Tur Arası 0.5 Sn Ara verildi..")
                await drone.offboard.set_velocity_body(
                     VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
                await asyncio.sleep(0.5)
                tur=tur+1
####------------------------------------------------------------------------------
    print("Görevler Tamamlandı, SERÇEDES İniyor..")
    print("-- 1 sn Bekle")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1)

    print("-- Offboar Mode Durdu")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Offboar mode baslatılması : \
              {error._result.result} nedeniyle hata verdi..")
    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
