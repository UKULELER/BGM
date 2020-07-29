import pandas as pd
import string

# 导入数据文件
io = "../../data/DataOfBGMAndVedio.xlsx"

# 获取BGM数据
BGM = pd.read_excel(io,sheet_name = 1,index_col= 'ID')

# 获取Vedio数据
vedio = pd.read_excel(io,sheet_name= 0,index_col= 'ID')

# 先计算出每一个Vedio的 BGM作用系数
# 通过加上一个极小的数来避免评论量和转发数为0的情况
vedio["BGM作用系数"]= vedio["点赞"]/(vedio["评论量"]+vedio["转发"]+ 0.000001)

# 删除一些不太合理的数据（初步怀疑可能是通过买赞等手段异常化了数据）
vedio= vedio.drop(vedio[vedio["BGM作用系数"] > 100].index)

# 用来保存最后生成的所有tag占比
# list里装的是 series
listOfTagProportion = []

for i in range(1, len(BGM) + 1):
    targetVedio = vedio[vedio["BGMId"] == i]
    countOfTag = pd.concat(
        [targetVedio["tag1"], targetVedio["tag2"], targetVedio["tag3"], targetVedio["tag4"], targetVedio["tag5"]],
        ignore_index=True).dropna().value_counts()

    # 加权
    proportionOfTag = countOfTag
    for j in range(0, len(proportionOfTag)):
        tag = proportionOfTag.index[j]
        proportionOfTag[j] = targetVedio.query("tag1 == @tag | tag2 == @tag | tag3 == @tag | tag4 == @tag | tag5 == @tag")["BGM作用系数"].sum()

    proportionOfTag = proportionOfTag / proportionOfTag.sum()
    proportionOfTag = proportionOfTag.sort_values(ascending=False)
    listOfTagProportion.append(proportionOfTag)


# 用来保存   Tag占比 * 对应BGM的使用量 = 在各BGM下各Tag的推荐度 （便于用来多BGM对比和推荐）
listOfTagRecommend = []
for i in range(len(listOfTagProportion)):
    listOfTagRecommend.append(listOfTagProportion[i]*BGM.loc[i+1]["使用次数"])

# 实现查询与推荐
chooseTag=input()

#实现根据tag检索出BGM列表
finalChoice=vedio[vedio["tag1"]==chooseTag]
finalChoice = finalChoice["BGMId"]
finalChoice=list(set(finalChoice))

bgmList=[]  #用来存放bgm
commendDic={}  #用来以字典形式存储数据
dataList=[]    #用来存储数据，便于比较

for i in range(len(finalChoice)):
    bgmList.append(BGM['音乐'][finalChoice[i]])
    item=listOfTagRecommend[finalChoice[i]-1]
    dataList.append(item[chooseTag])
    commendDic[item[chooseTag]]=BGM['音乐'][finalChoice[i]]

dataList.sort()
result=[]  #用来按推荐顺序存储bgm

for i in range(len(finalChoice)):
    result.append(commendDic[dataList[len(finalChoice)-1-i]])

print(bgmList)
print(dataList)
print(commendDic)
print(result)




