import asyncio
import aioredis
import sys


name = 'test_pl'
value_score = {'a':5, 'b':2, 'c':4, 'd':1, 'e':8, 'f':3, 'g':6, 'h':7}

if len(sys.argv)>1 and sys.argv[1]=='load':
    is_load = True
else: 
    is_load = False

if len(sys.argv)>1 and sys.argv[1]=='delete':
    is_delete = True
else:
    is_delete = False


async def main():
    redis = aioredis.from_url("redis://localhost")
    if is_load:
        await redis.zadd(name, value_score)

    if is_delete:
        await redis.delete(name)
        print("sorted set is deleted")
        return
    

    number_of_elements = await redis.zcard(name)
    print("***********zscard***********")
    print(number_of_elements)
    print("\n\n")

    print("***********pipeline***********")
    async with redis.pipeline(transaction=True) as pipe:
        ok = await (pipe.zincrby(name, 2, 'c').zincrby(name, 2, 'd').execute())
    
    print(ok)






asyncio.run(main())