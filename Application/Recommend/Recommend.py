import pandas as pd
import string

# 导入数据文件
io = "../../data/DataOfBGMAndVideo.xlsx"

# 获取BGM数据
BGM = pd.read_excel(io,sheet_name = 1,index_col= 'ID')

# 获取Video数据
video = pd.read_excel(io,sheet_name= 0,index_col= 'ID')

# 先计算出每一个Video的 BGM作用系数
# 通过加上一个极小的数来避免评论量和转发数为0的情况
video["BGM作用系数"]= video["点赞"]/(video["评论量"]+video["转发"]+ 0.000001)

# 删除一些不太合理的数据（初步怀疑可能是通过买赞等手段异常化了数据）
video= video.drop(video[video["BGM作用系数"] > 100].index)

# 用来保存最后生成的所有tag占比
# list里装的是 series
listOfTagProportion = []

for i in range(1, len(BGM) + 1):
    targetVideo = video[video["BGMId"] == i]
    countOfTag = pd.concat(
        [targetVideo["tag1"], targetVideo["tag2"], targetVideo["tag3"], targetVideo["tag4"], targetVideo["tag5"]],
        ignore_index=True).dropna().value_counts()

    # 加权
    proportionOfTag = countOfTag
    for j in range(0, len(proportionOfTag)):
        tag = proportionOfTag.index[j]
        proportionOfTag[j] = targetVideo.query("tag1 == @tag | tag2 == @tag | tag3 == @tag | tag4 == @tag | tag5 == @tag")["BGM作用系数"].sum()

    proportionOfTag = proportionOfTag / proportionOfTag.sum()
    proportionOfTag = proportionOfTag.sort_values(ascending=False)
    listOfTagProportion.append(proportionOfTag)

# 用来保存   Tag占比 * 对应BGM的使用量 = 在各BGM下各Tag的推荐度 （便于用来多BGM对比和推荐）
listOfTagRecommend = []
for i in range(len(listOfTagProportion)):
    listOfTagRecommend.append(listOfTagProportion[i]*BGM.loc[i+1]["使用次数"])

# 实现查询与推荐
chooseTag=input("请输入你想标注的tag：")

#实现根据tag检索出BGM列表
finalChoice=video[video["tag1"]==chooseTag]
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
bgmResult=[]  #用来按推荐顺序存储bgm
result={"推荐名次":"BGM名称"}

for i in range(len(finalChoice)):
    bgmResult.append(commendDic[dataList[len(finalChoice)-1-i]])
for i in range(len(finalChoice)):
    result[i+1]=bgmResult[i]
resultSeries=pd.Series(result)


print("以下是系统为您推荐的BGM列表：")
# print(bgmList)
# print(dataList)
# print(commendDic)
# print(bgmResult)
print(resultSeries)




