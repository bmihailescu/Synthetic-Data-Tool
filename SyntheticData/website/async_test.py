import asyncio
# import time

# num = 0
 
# async def coroutine():
#     for i in range(10):
#         time.sleep(0.5)
#         num = i
#         print(num)
#         await asyncio.sleep(0.001)
#         # return i

# coroutine()

# async def print_iterator():
#     while num != 9:
#         time.sleep(0.5)
#         print("print",num)
#         await asyncio.sleep(0.001)

# async def main():
    
#     task1 = loop.create_task(coroutine())
#     task2 = loop.create_task(print_iterator())

#     await asyncio.wait([task1,task2])


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

# class Demo:
#     def __init__(self):
#         self.ltp = 0

#     async def one(self):
#         while True:
#             time.sleep(0.001)
            
#             self.ltp += 1
#             print("one",self.ltp)
#             await asyncio.sleep(0)

#     async def two(self):
#         while True:
#             time.sleep(0.5)
#             print("two",self.ltp)
#             await asyncio.sleep(0)


# async def main():
#     d = Demo()
    
#     task1 = loop.create_task(d.one())
#     task2 = loop.create_task(d.two())

#     await asyncio.wait([task1,task2])


# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(main())
# # 


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

# a = 97, z = 122
###############################################################
# from time import time as t
# val_list = []
# nowTime = t()
# for i in range(100):
#     val = i*2
#     print(val)
#     curTime = t()
#     if curTime - nowTime >= 0.1:
#         #Do your stuff
#         print("iterator",i)
#         nowTime = curTime


