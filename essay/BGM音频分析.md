# BGM音频分析



## 0. 概述

##### 通过对音频本身特点提取、不同音频进行比对，结合音乐对心理因素的影响，分析抖音热门BGM的基本特征，并进行猜想：

1. BGM的旋律具有稳定性
2.  BGM偏向于快节奏，一般对应整首歌中的高光部分
3.  BGM会对原曲进行一些改变，可能加入特殊的音效

##### 分析采用了开源软件及python语言，涉及多个音频处理工具，包括：

1. 开源计算机程序**FFmpeg**，用于记录、转换数字音频、视频，并能将其转化为流。

<img src="BGM音频分析.assets/ffmpeg.jpg" alt="ffmpeg" style="zoom: 67%;" />

一些音频数据初始为mp3格式，通过这一开源程序转为WAV，便于使用python进行特征提取。



2. 音频对比软件**sound-similar**

![image-20200727154055626](BGM音频分析.assets/image-20200727154055626.png)

可以对两个WAV格式的音频进行比对，得到一个音频相似度的分析结果。



3. **pyAudioAnalysis**

这是一个用于音频分析的python包，具有丰富的功能和强大的处理能力

![image-20200727163546352](BGM音频分析.assets/image-20200727163546352.png)

与之关联的还有pydub、numpy、hmmlearn等依赖包。

通过这个python包，可以计算Zero Crossing Rate、Entropy of Energy、MFCCs等数值



4. **praat**

   ![image-20200730153032187](BGM音频分析.assets/image-20200730153032187.png)

   这是一款功能多样的音频分析软件，拥有信息提取、图像绘制等功能。虽然交互性稍有不足，但功能十分强大。

   在使用这个软件时，还可以编写相关的脚本进行音频处理。

   

##### 除了工具外，还用到一些APP及数据网站：

1. 抖音

<img src="BGM音频分析.assets/image-20200727164043847.png" alt="image-20200727164043847" style="zoom: 50%;" />

我们所作的数据分析全部基于抖音短视频，聚焦于对BGM及其外延的研究。



2. 卡思数据

![image-20200727164505774](BGM音频分析.assets/image-20200727164505774.png)

国内较大的视频数据分析平台，拥有大量MCN数据统计及良好的可视化展示。热门BGM的数据就参考了该平台数据。



3. 飞瓜数据

![image-20200727164809568](BGM音频分析.assets/image-20200727164809568.png)

一家较大的数据分析网站，主要面向抖音数据，更加重视视频数据，提供的BGM往往与高赞视频相结合。



4. TooBigData

![image-20200727171333665](BGM音频分析.assets/image-20200727171333665.png)

这一平台数据丰富，最大的特点是大部分的数据都可以免费查看，适合非机构用户使用。

5. 蝉妈妈数据

![image-20200727172358432](BGM音频分析.assets/image-20200727172358432.png)

这一平台对BGM数据有较好的可视化分析，适合用于研究外延性猜想：

<img src="BGM音频分析.assets/image-20200727172522493.png" alt="image-20200727172522493" style="zoom:50%;" />



## 1. 研究背景

短视频内容产品的崛起有其时代原因，也与移动智能设备及基建的完善等有关。在研究BGM之前，我先去了解了一下抖音、快手这类产品取得成果的原因：

```word
1.时机

抖音于2016年9月上线，当时短视频正处于高热度阶段，在移动化、碎片化消费日益盛行的当下，低门槛低成本地分享生活信息的短视频成了最应景的消费产品。

2.内容社区

抖音的内容社区保证了UGC的可持续性。具体来说就是：一方面，抖音通过签约一批网红、MCN来保证优质内容的持续产出，且成立了服务达人的经纪团队，通过广告等变现手段进行激励；另一方面，使用与今日头条一脉相承的算法分发机制，持续挖掘普通用户的爆款内容，“中心化”进行内容分发，保障优质内容的传播优先性，个性化推荐机制投其所好，精准抓取用户痒点，维持用户活跃度。

3.用户粘度

抖音很好地消解了用户无聊的时光，交互简单，即时满足，永无止境；通过下滑即可源源不断获取新内容，全屏沉浸式体验，用户的兴奋点不断被刺激，甚至难以自拔。抖音有的不仅仅是“音乐+短视频+社交”的新鲜感，真正解决的痛点是让普通年轻用户获得感官的刺激与价值观的认同，填补孤独；让拍摄者满足于炫耀，并实现变现。

4.盈利模式

盈利模式清晰有效，包括广告、直播等增值服务，生命力得到支撑和保障，如此才不会昙花一现就没落。

                                                                                                                                                                                                        --by 穆宁
```

采用几十秒的视频来为用户提供高频刺激，就需要具备丰富的内容要素，BGM是其中不可或缺的一环。好的BGM对于用户的情绪调动、快感获取、连接叙事、氛围营造等都有不可或缺的作用。

抖音的定位为音乐短视频，内容品类丰富多样，但在我们经过**50+小时**的使用后发现，常用BGM的数量很小，在形成信息茧房后约为20~30左右，且特定类型的短视频总是搭配固定的BGM。由于平台的判定方式，不同人剪辑的音乐片段会算作不同BGM（即使内容完全一样），所以对于热门的BGM单曲，原歌曲实际被使用可能远超过这个数量。

在实际的数据分析中，我们采用了手动的方式，结合各数据平台的信息，选择了**15首热门BGM**，将其中十首用作分析，五首作为检验案例，寻找其相同点，并下载了**对应的整首歌曲**进行对照分析，从整体的角度去看待BGM部分。由于短视频MCN竞争激烈，BGM中良币驱逐劣币的现象严重，再加上抖音官方的强运营政策，很难去找到所谓“不热门”或“不好”的BGM，所以只是随机找了**5首**我们认为与抖音风格有差异的歌曲进行分析。

在对抖音中音乐进行了解的过程中，发现BGM往往是随作品搭配的，这也符合创作路径中的先拍摄后配音的过程。于是，我们也对抖音的内容分布进行了统计分析。

此外，虽然各BGM的数据存在差别，但考虑到不同BGM对应于不同题材的作品，而各赛道作品数量则天然地存在差异，故没有对数据不同的BGM进行对比分析，以免得出过度拟合的结论。

在研究过程中，遇到了数据采集的诸多困难，最终未能得到大量数据进行研究，而是将目光放在数据优秀的个别作品进行小范围分析，并通过运用各数据平台已有的统计结果去验证猜想。



## 2. 数据采集

### 2.1 数据筛选

##### 抖音组音乐

**遵循规则：**

1. 有较高播放量的BGM，播放量在100w+
2. 有较高增速，这点要求是结合了数据平台统计的排名规则，方便找到符合要求的BGM
3. BGM种类尽可能多样化，由人工进行鉴别
4. 出现了至少一个超过百万赞的爆款视频
5. 该音频对应的UGC内容中，有超过10个不同作者的BGM，即一首歌曲被多个人做成了内容相近的BGM

**最终得到的数据为：**

| 序号 | 歌曲                    |
| ---- | ----------------------- |
| 1    | 旧梦一场                |
| 2    | 怎么开心怎么活          |
| 3    | 小星星                  |
| 4    | 谪仙                    |
| 5    | dance monkey            |
| 6    | 你的答案                |
| 7    | dancing with your ghost |
| 8    | 桥边姑娘                |
| 9    | 我和你                  |
| 10   | 一起长大的幸福          |
| 11   | warp me in plastic      |
| 12   | 你笑起来真好看          |
| 13   | 陪你长大                |
| 14   | 蓝色海黑色河            |
| 15   | 带你去旅行              |



##### 对照组音乐

**遵循规则：**

1. 在抖音中BGM的使用不超过10w
2. 单曲在音乐APP中的收藏量超过1w

**最终得到的数据为:**

| 序号 | 歌曲       |
| ---- | ---------- |
| 1    | All Rise   |
| 2    | 红豆       |
| 3    | 浮夸       |
| 4    | 最初的梦想 |
| 5    | 星星点灯   |



### 2.2 设计分析方法

#### 2.2.1 基本采集

通过praat进行最初的解析，得到音频数据的基本信息，包括pitch analyse、formant analyse、intensity analyse、curve等部分内容的分析。

#### 2.2.2 精细采集

由于BGM普遍为15s左右，属于短音频，故通过pyAudioAnalysis进行音频的数据分析，获取一些**短期特征**。以下为部分特征的介绍：

##### 1. 过零率

过零率体现的是信号过零点的次数，体现的是频率特性。这个特征在语音对比、语音识别和 music information retrieval 领域得到广泛使用，是对敲击声音的进行分类的主要特征。

以下为过零率的数学表达式：

![img](BGM音频分析.assets/1085343-20170505220055914-35775139.png)



##### 2.  短时能量

短时能量体现的是信号在不同时刻的强弱程度，通过每一帧语音信号的平方和表示。

以下为短时能量的数学表达式：

![img](BGM音频分析.assets/1085343-20170505220407007-256377400.png)



##### 3. 短时功率谱密度

功率谱定义为单位频带内的信号功率。它表示了信号功率随着频率的变化情况，即信号功率在频域的分布状况。

将音频信号视作周期性变换，时域与频域之间利用傅里叶变换进行关联。

![img](BGM音频分析.assets/1085343-20170506000609023-1037132746.png)

功率谱之所以可以估计，是基于两点假设：1）信号平稳; 2)随机信号具有遍历性

以下为功率谱的数学表达式：

![img](BGM音频分析.assets/1085343-20170524093414419-707819987.png)



##### 4. 谱熵

谱熵（spectral entropy ）这一概念描述了功率谱和熵率之间的关系。分布越均匀，熵越大，反应了每一帧信号的均匀程度，如说话人频谱由于共振峰存在显得不均匀，而白噪声的频谱就更加均匀，借此进行VAD便是应用之一。

以下为谱熵的数学表达式：

<img src="BGM音频分析.assets/1085343-20170506065731664-534158416.png" alt="img" style="zoom:80%;" />

其中，p（i）代表每一帧信号的频谱绝对值归一化的结果：

![img](BGM音频分析.assets/1085343-20170506065439836-1155763438.png)



##### 5. 短时自相关函数

信号处理中，自相关可以提供关于重复事件的信息，例如音乐节拍（例如，确定节奏）或脉冲星的频率（虽然它不能告诉我们节拍的位置）。另外，它也可以用来估计乐音的音高。

以下为自相关函数的数学表达式：

定义变量 X 和 Y 的相关系数：

![img](BGM音频分析.assets/20171219213515650)

相关系数越大，相关性越大，但肯定小于或者等于1。

自相关函数是描述随机信号 x(t) 在任意不同时刻 t1,t2的取值之间的相关程度，定义为：

![img](BGM音频分析.assets/20171219213856567)



##### 6. 梅尔频率倒谱系数

梅尔倒谱系数（Mel-scale Frequency Cepstral Coefficients，简称MFCC）是在Mel标度频率域提取出来的倒谱参数，Mel标度描述了人耳频率的非线性特性，它与频率的关系可用下式近似表示：

![img](BGM音频分析.assets/20140122235450406)

对连续语音使用梅尔倒谱进行分析，主要流程为：预加重、分帧、加窗、傅里叶变换、三角带通滤波器、计算每个滤波器组输出的对数能量、离散余弦变换。



##### 7. 标准差

标准差（Standard Deviation） ，是离均差平方的算术平均数的算术平方根，在概率统计中最常使用作为统计分布程度上的测量依据。标准差能反映一个数据集的离散程度。

![img](BGM音频分析.assets/8cb472ca2ceb75dff4d909d9a6301823.svg)



## 3. 猜想检验

### 3.1 数据分析

由于音频解析、音频之间的比对本身具有一定的难度，且BGM中往往有多种声音交杂导致音频数据纷杂，我们很难通过某种绝对正确的算法来得出各个音频中的共性和差异性。即便数据上存在，也难以保证是有效的结论而非巧合。

短视频受到 “人” 本身感知的影响较大，所以除了对基本的解析数据做出统计分析、假设检验等工作，我们增加了 “人” 在数据分析中的工作量，从而有效解决了音频难以与短视频内容、风格、心理影响等复杂因素进行联系的问题，避免了结论的片面性，但同时也增加了主观性。

通过对获得的BGM及其音频解析数据进行分析，得出各自比较显著的特征，再从中找到具有一定普遍性的特点作为印证猜想的论据。

*注：1.收集音频大多为双声道，故波形图由上下两部分组成。*

​       *2.BGM与创作部分的内容，视频数据统计结果来自[蝉妈妈](https://www.chanmama.com/)*



##### 旧梦一场

以下为波形图：![旧梦一场](BGM音频分析.assets/旧梦一场.png)

​                                                                                                     *旧梦一场*

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 17.357256235827663 seconds
   Total duration: 17.357256235827663 seconds
Time sampling:
   Number of frames: 1732 (1026 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02362811791383301 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 92.4347172 Hz = 85.4408092 Mel = -1.36191943 semitones above 100 Hz = 2.81002867 ERB
   16% = 92.8363898 Hz = 85.784581 Mel = -1.28685209 semitones above 100 Hz = 2.82081316 ERB
   50% = 158.354333 Hz = 139.164388 Mel = 7.9578761 semitones above 100 Hz = 4.4469203 ERB
   84% = 376.189159 Hz = 286.638116 Mel = 22.9374993 semitones above 100 Hz = 8.53518075 ERB
   90% = 429.044803 Hz = 317.16252 Mel = 25.2135397 semitones above 100 Hz = 9.32258682 ERB
Estimated spreading:
   84%-median = 217.9 Hz = 147.5 Mel = 14.99 semitones = 4.09 ERB
   median-16% = 65.55 Hz = 53.41 Mel = 9.249 semitones = 1.627 ERB
   90%-10% = 336.8 Hz = 231.8 Mel = 26.59 semitones = 6.516 ERB

Minimum 74.9860699 Hz = 70.2960957 Mel = -4.98366579 semitones above 100 Hz = 2.3306148 ERB
Maximum 597.492937 Hz = 404.47908 Mel = 30.9470599 semitones above 100 Hz = 11.4866515 ERB
Range 522.5 Hz = 334.182984 Mel = 35.93 semitones = 9.156 ERB
Average: 227.929697 Hz = 182.175284 Mel = 10.9293096 semitones above 100 Hz = 5.58054673 ERB
Standard deviation: 141.3 Hz = 95.42 Mel = 10.79 semitones = 2.667 ERB

Mean absolute slope: 1023 Hz/s = 691.9 Mel/s = 79.94 semitones/s = 19.37 ERB/s
Mean absolute slope without octave jumps: 28.14 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 高低音区分明显，在原音乐中体现为歌声与穿插的鼓点交替出现
- 音频解析后数据中的标准差较大（95.42 Mel），且音频有着大的变化范围（334.18 Mel），这也与上条的特性相照应，说明BGM的声音区分度明显，高低变化较为剧烈

此外，结合内容创作的情况，可以得到结论：

- 这个BGM一般对应照片集性质的内容，即与视觉向作品结合，作为声音上的补充。每次鼓点之间可以进行照片切换。



##### 怎么开心怎么活

以下为波形图：![praat](BGM音频分析.assets/praat.png)

​																							 *怎么开心怎么活*

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 15.633174603174604 seconds
   Total duration: 15.633174603174604 seconds
Time sampling:
   Number of frames: 1560 (424 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02158730158730215 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 81.1366077 Hz = 75.6822301 Mel = -3.61890132 semitones above 100 Hz = 2.50209327 ERB
   16% = 85.3483703 Hz = 79.3403517 Mel = -2.74277387 semitones above 100 Hz = 2.61793691 ERB
   50% = 130.517138 Hz = 117.114101 Mel = 4.61087115 semitones above 100 Hz = 3.78644575 ERB
   84% = 270.809957 Hz = 220.20533 Mel = 17.2473694 semitones above 100 Hz = 6.7571523 ERB
   90% = 300.133789 Hz = 239.511502 Mel = 19.027269 semitones above 100 Hz = 7.2835975 ERB
Estimated spreading:
   84%-median = 140.5 Hz = 103.2 Mel = 12.65 semitones = 2.974 ERB
   median-16% = 45.22 Hz = 37.82 Mel = 7.362 semitones = 1.17 ERB
   90%-10% = 219.3 Hz = 164 Mel = 22.67 semitones = 4.787 ERB

Minimum 74.9923816 Hz = 70.3016501 Mel = -4.98220863 semitones above 100 Hz = 2.3307922 ERB
Maximum 587.26647 Hz = 399.555503 Mel = 30.6481832 semitones above 100 Hz = 11.3678225 ERB
Range 512.3 Hz = 329.253852 Mel = 35.63 semitones = 9.037 ERB
Average: 173.75544 Hz = 145.268154 Mel = 6.75468618 semitones above 100 Hz = 4.54772288 ERB
Standard deviation: 111.5 Hz = 77.08 Mel = 9.426 semitones = 2.182 ERB

Mean absolute slope: 407.1 Hz/s = 288.7 Mel/s = 37.23 semitones/s = 8.261 ERB/s
Mean absolute slope without octave jumps: 10.89 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 高低音之间的差别偏小，即原声的情况较为平稳
- 波形图中出现了明显而连续的峰和谷，说明原歌曲中有明晰的声音变化（对应地，BGM中的歌词之间字字分明）
- 歌曲中存在一个持续而稳定的底音（暂不清楚为什么作者加入这一混响音），使得分析数据得出的平均绝对斜率较低，即数值上看，这段BGM呈现出更为稳定的特征

此外，结合内容创作的情况，可以得到结论：

- 这首歌曲与乡土生活结合较多，对应的短视频内容大多为此题材，具有一定的特殊性。但在与乡土有关的音乐中，可能是由于其节奏的舒缓和稳定，随之带来的情感带动、氛围营造、魔性洗脑等效果，使得它成为了最受欢迎的BGM之一。



##### 小星星

以下为波形图：![praat](BGM音频分析.assets/praat-1596001053008.png)

​																									*小星星*

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 15.032358276643992 seconds
   Total duration: 15.032358276643992 seconds
Time sampling:
   Number of frames: 1500 (845 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.0211791383219958 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 80.5280807 Hz = 75.1516774 Mel = -3.74923375 semitones above 100 Hz = 2.48525058 ERB
   16% = 83.4875256 Hz = 77.7271165 Mel = -3.12440933 semitones above 100 Hz = 2.566911 ERB
   50% = 104.351147 Hz = 95.5492185 Mel = 0.737357567 semitones above 100 Hz = 3.12538385 ERB
   84% = 305.815585 Hz = 243.17515 Mel = 19.3519432 semitones above 100 Hz = 7.38256282 ERB
   90% = 360.075804 Hz = 276.985291 Mel = 22.1796079 semitones above 100 Hz = 8.28249508 ERB
Estimated spreading:
   84%-median = 201.6 Hz = 147.7 Mel = 18.63 semitones = 4.26 ERB
   median-16% = 20.88 Hz = 17.83 Mel = 3.864 semitones = 0.5588 ERB
   90%-10% = 279.7 Hz = 202 Mel = 25.94 semitones = 5.801 ERB

Minimum 75.0794561 Hz = 70.3782713 Mel = -4.96211874 semitones above 100 Hz = 2.33323928 ERB
Maximum 596.418356 Hz = 403.963786 Mel = 30.9158959 semitones above 100 Hz = 11.4742319 ERB
Range 521.3 Hz = 333.585514 Mel = 35.88 semitones = 9.141 ERB
Average: 159.103226 Hz = 133.734 Mel = 4.96387125 semitones above 100 Hz = 4.2024469 ERB
Standard deviation: 113.2 Hz = 78.4 Mel = 9.476 semitones = 2.218 ERB

Mean absolute slope: 1013 Hz/s = 704.1 Mel/s = 89.76 semitones/s = 20.01 ERB/s
Mean absolute slope without octave jumps: 31.76 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 这首BGM的波形图非常稳定，虽然有频繁的峰谷变化，但从整体来看，声音的效果没有出现大的变化

- 抛却首尾的杂音后，可以直观地从波形图中看到，这首BGM中加入了大量的混响，甚至对歌声造成了一定的掩盖，波形密集而混杂，具有丰富的鼓点、打碟声等
- 从数据分析的结果看，音频的平均绝对斜率较高（31.76），变化范围也较大（333.59 Mel），但标准差却是较小的（78.4 Mel），这个数据结果刚好和我们对BGM波形图及歌声的判断相符

此外，结合内容创作的情况，可以得到结论：



##### 谪仙

以下为波形图：![praat](BGM音频分析.assets/praat-1596001189151.png)

​																								   	*谪仙*

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 11.427460317460318 seconds
   Total duration: 11.427460317460318 seconds
Time sampling:
   Number of frames: 1139 (552 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.023730158730158487 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 110.515949 Hz = 100.706646 Mel = 1.73105505 semitones above 100 Hz = 3.28490589 ERB
   16% = 145.374266 Hz = 128.992564 Mel = 6.47726292 semitones above 100 Hz = 4.14411116 ERB
   50% = 194.728 Hz = 166.705425 Mel = 11.5375241 semitones above 100 Hz = 5.2516041 ERB
   84% = 393.67151 Hz = 296.922918 Mel = 23.7239077 semitones above 100 Hz = 8.80243013 ERB
   90% = 437.25874 Hz = 321.757631 Mel = 25.5418467 semitones above 100 Hz = 9.43964607 ERB
Estimated spreading:
   84%-median = 199.1 Hz = 130.3 Mel = 12.2 semitones = 3.554 ERB
   median-16% = 49.4 Hz = 37.75 Mel = 5.065 semitones = 1.108 ERB
   90%-10% = 327 Hz = 221.3 Mel = 23.83 semitones = 6.16 ERB

Minimum 76.6116733 Hz = 71.7248014 Mel = -4.61236635 semitones above 100 Hz = 2.37620751 ERB
Maximum 597.606775 Hz = 404.53364 Mel = 30.950358 semitones above 100 Hz = 11.4879663 ERB
Range 521 Hz = 332.808839 Mel = 35.56 semitones = 9.112 ERB
Average: 254.314749 Hz = 201.767034 Mel = 13.7510764 semitones above 100 Hz = 6.15400509 ERB
Standard deviation: 134.7 Hz = 88.32 Mel = 9.216 semitones = 2.432 ERB

Mean absolute slope: 518.5 Hz/s = 350.8 Mel/s = 38.58 semitones/s = 9.789 ERB/s
Mean absolute slope without octave jumps: 15.6 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 除去开头时的不稳定音频后，可以看到波形图中出现了明显的音频波动情况，即歌词播放较为清晰，与背景音乐有着明显的差别。同其他BGM类似，这首曲子也有着鼓点等混响。
- 从数据中看，这首BGM的数据同其他BGM相比，处于一个较为平均的水平。稍高的标准差（88.32 Mel）也印证了波形图中音频波动的解释。

此外，结合内容创作的情况，可以得到结论：

- 这首曲子能够从音乐中带来侠客般的氛围，其实音调也偏高，多用于混剪类作品。



##### dance monkey

以下为波形图：![praat](BGM音频分析.assets/praat-1596034714362.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 14.61439909297052 seconds
   Total duration: 14.61439909297052 seconds
Time sampling:
   Number of frames: 1458 (1052 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02219954648526123 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 83.6081105 Hz = 77.8317996 Mel = -3.09942235 semitones above 100 Hz = 2.570225 ERB
   16% = 92.3384496 Hz = 85.3583866 Mel = -1.37995903 semitones above 100 Hz = 2.80744235 ERB
   50% = 364.618395 Hz = 279.723755 Mel = 22.3966482 semitones above 100 Hz = 8.35436642 ERB
   84% = 437.12956 Hz = 321.685661 Mel = 25.5367313 semitones above 100 Hz = 9.43781553 ERB
   90% = 491.86485 Hz = 351.367078 Mel = 27.5791435 semitones above 100 Hz = 10.1851444 ERB
Estimated spreading:
   84%-median = 72.55 Hz = 41.98 Mel = 3.142 semitones = 1.084 ERB
   median-16% = 272.4 Hz = 194.5 Mel = 23.79 semitones = 5.55 ERB
   90%-10% = 408.5 Hz = 273.7 Mel = 30.69 semitones = 7.619 ERB

Minimum 75.0395858 Hz = 70.3431888 Mel = -4.97131475 semitones above 100 Hz = 2.33211886 ERB
Maximum 589.114833 Hz = 400.448675 Mel = 30.7025865 semitones above 100 Hz = 11.3894057 ERB
Range 514.1 Hz = 330.105486 Mel = 35.67 semitones = 9.057 ERB
Average: 287.890266 Hz = 221.508251 Mel = 14.8263376 semitones above 100 Hz = 6.65895461 ERB
Standard deviation: 157.5 Hz = 105.9 Mel = 11.82 semitones = 2.951 ERB

Mean absolute slope: 887.8 Hz/s = 609.9 Mel/s = 71.72 semitones/s = 17.16 ERB/s
Mean absolute slope without octave jumps: 19.07 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 从波形图中，非常明显可以看出，这首BGM非常地不稳定，从原声中也可以听到，存在频繁的变调与混音。
- 从数据分析来看，高达 105.9 Mel 的标准差也说明了变化幅度的剧烈。

此外，结合内容创作的情况，可以得到结论：

- 这首BGM的使用数据较其他BGM会有一点偏底，作为英文歌，使用者常来搭配一些外国元素的内容或**鬼畜**内容，很难不去猜测，后一个题材与频繁变调的BGM节奏有着较强关联。



##### 你的答案

以下为波形图：![praat](BGM音频分析.assets/praat-1596034757337.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 37.3931746031746 seconds
   Total duration: 37.3931746031746 seconds
Time sampling:
   Number of frames: 3736 (1898 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.021587301587303927 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 77.6131936 Hz = 72.6031706 Mel = -4.3875141 semitones above 100 Hz = 2.40419945 ERB
   16% = 77.8333743 Hz = 72.796089 Mel = -4.3384703 semitones above 100 Hz = 2.41034348 ERB
   50% = 104.2197 Hz = 95.438722 Mel = 0.71553603 semitones above 100 Hz = 3.12195609 ERB
   84% = 237.264885 Hz = 197.255569 Mel = 14.9579832 semitones above 100 Hz = 6.12008108 ERB
   90% = 288.639113 Hz = 232.024208 Mel = 18.3512017 semitones above 100 Hz = 7.0804267 ERB
Estimated spreading:
   84%-median = 133.1 Hz = 101.8 Mel = 14.25 semitones = 2.999 ERB
   median-16% = 26.39 Hz = 22.65 Mel = 5.055 semitones = 0.7118 ERB
   90%-10% = 211.1 Hz = 159.5 Mel = 22.74 semitones = 4.677 ERB

Minimum 74.987393 Hz = 70.29726 Mel = -4.98336033 semitones above 100 Hz = 2.33065198 ERB
Maximum 568.939487 Hz = 390.620093 Mel = 30.0993026 semitones above 100 Hz = 11.1512437 ERB
Range 494 Hz = 320.322833 Mel = 35.08 semitones = 8.821 ERB
Average: 134.434436 Hz = 116.957118 Mel = 2.88795032 semitones above 100 Hz = 3.73061249 ERB
Standard deviation: 79.23 Hz = 58.84 Mel = 8.188 semitones = 1.715 ERB

Mean absolute slope: 225 Hz/s = 169.9 Mel/s = 25.47 semitones/s = 5.003 ERB/s
Mean absolute slope without octave jumps: 10.88 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 波形图与《小星星》有一些类似，但明显地，起伏更小，曲调、音量都非常稳定。
- 从数据中低至 58.84 Mel 的标准差就可以证明对波形图的分析。此外，可以看到分位数计算中，从50%部分一直到90%部分都保持着较低的数值（95.44 Mel ~ 232.02 Mel）。听过歌曲就会发现，这其实是是一首舒缓轻松的音乐。

此外，结合内容创作的情况，可以得到结论：

- 题材多为励志、成长等内容，贴近生活，富有人情味，与数据分析及音乐本身特点是相符的。



##### dancing with your ghost

以下为波形图：![praat](BGM音频分析.assets/praat-1596034837362.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 27.8062358276644 seconds
   Total duration: 27.8062358276644 seconds
Time sampling:
   Number of frames: 2777 (2113 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.023117913832199407 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 82.4245479 Hz = 76.8034539 Mel = -3.34624832 semitones above 100 Hz = 2.53765251 ERB
   16% = 90.0119205 Hz = 83.3626881 Mel = -1.82174425 semitones above 100 Hz = 2.74474483 ERB
   50% = 156.068175 Hz = 137.386436 Mel = 7.70611657 semitones above 100 Hz = 4.39421724 ERB
   84% = 232.267 Hz = 193.75281 Mel = 14.5894103 semitones above 100 Hz = 6.0217205 ERB
   90% = 242.21737 Hz = 200.704643 Mel = 15.3156279 semitones above 100 Hz = 6.21663702 ERB
Estimated spreading:
   84%-median = 76.22 Hz = 56.38 Mel = 6.885 semitones = 1.628 ERB
   median-16% = 66.07 Hz = 54.04 Mel = 9.53 semitones = 1.65 ERB
   90%-10% = 159.8 Hz = 123.9 Mel = 18.67 semitones = 3.68 ERB

Minimum 75.4434988 Hz = 70.6984949 Mel = -4.87837813 semitones above 100 Hz = 2.34346398 ERB
Maximum 392.563948 Hz = 296.277018 Mel = 23.6751322 semitones above 100 Hz = 8.78570564 ERB
Range 317.1 Hz = 225.578524 Mel = 28.55 semitones = 6.442 ERB
Average: 162.13448 Hz = 139.736155 Mel = 6.89454579 semitones above 100 Hz = 4.42670564 ERB
Standard deviation: 67.11 Hz = 50.5 Mel = 7.196 semitones = 1.481 ERB

Mean absolute slope: 360.9 Hz/s = 274.8 Mel/s = 39.98 semitones/s = 8.096 ERB/s
Mean absolute slope without octave jumps: 23.26 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 这首BGM有着较大的波动与变化，但相比《dance monkey》更加稳定，在波形图中，虽然整体上有过多次变化，但在变化后的一段时间里，波形是保持稳定状态的。频率较低的部分对应的是没有歌词的部分，可以看出BGM的背景音乐较低。
- 从数据的角度看，这首曲子的频率变化范围较小（225.58 Mel），这是由于最高频率较低（392.56 Mel）。在听觉感受来看，与其舒缓、温和的叙事感曲调是相符的。

此外，结合内容创作的情况，可以得到结论：

- 这首BGM往往搭配叙事、抒情、感人或场面较为平静的内容（有室内运动的高赞作品）。其温和而略带伤感的曲风，以及较小的频率变化，能够很好地带入氛围，营造叙事感。



##### 桥边姑娘

以下为波形图：![praat](BGM音频分析.assets/praat-1596034896536.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 23.70501133786848 seconds
   Total duration: 23.70501133786848 seconds
Time sampling:
   Number of frames: 2367 (1913 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02250566893423944 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 78.1306671 Hz = 73.0564644 Mel = -4.27246994 semitones above 100 Hz = 2.41863363 ERB
   16% = 86.5869194 Hz = 80.4114788 Mel = -2.493348 semitones above 100 Hz = 2.65176313 ERB
   50% = 155.824991 Hz = 137.196972 Mel = 7.67911952 semitones above 100 Hz = 4.38859546 ERB
   84% = 387.40436 Hz = 293.258052 Mel = 23.4460823 semitones above 100 Hz = 8.70743003 ERB
   90% = 398.439585 Hz = 299.694897 Mel = 23.9323318 semitones above 100 Hz = 8.87411693 ERB
Estimated spreading:
   84%-median = 231.6 Hz = 156.1 Mel = 15.77 semitones = 4.32 ERB
   median-16% = 69.26 Hz = 56.8 Mel = 10.18 semitones = 1.737 ERB
   90%-10% = 320.4 Hz = 226.7 Mel = 28.21 semitones = 6.457 ERB

Minimum 75.2435031 Hz = 70.5225954 Mel = -4.92433291 semitones above 100 Hz = 2.33784802 ERB
Maximum 574.720561 Hz = 393.454388 Mel = 30.274328 semitones above 100 Hz = 11.2200723 ERB
Range 499.5 Hz = 322.931793 Mel = 35.2 semitones = 8.882 ERB
Average: 219.801173 Hz = 177.526356 Mel = 10.4544718 semitones above 100 Hz = 5.458551 ERB
Standard deviation: 128.3 Hz = 89.46 Mel = 10.7 semitones = 2.532 ERB

Mean absolute slope: 945.5 Hz/s = 671 Mel/s = 85.64 semitones/s = 19.17 ERB/s
Mean absolute slope without octave jumps: 26.29 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 这段波形图中有着界限分明的峰与谷，说明混响较少，且音调远低于歌声。整体上看，音频呈现一种较为明显的规律性变化，排布为以一段为一组的多段相似片段，这也与曲中实际的歌词、节拍相对应。
- 分析数据来看，这首BGM的标准差很大（89.46 Mel），且平均音调较高（177.53 Mel），这说明BGM的高低音频率差距大，且高音较高。这与曲子的听觉感受也是一致的。

此外，结合内容创作的情况，可以得到结论：

- 民谣性质的BGM，常用于贴近生活的题材。曲调较为舒缓，有节奏感，整体稳定没有突变，便于营造情境与带入。



##### 我和你

以下为波形图：![praat](BGM音频分析.assets/praat-1596034927930.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 15.058480725623582 seconds
   Total duration: 15.058480725623582 seconds
Time sampling:
   Number of frames: 1502 (1307 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02424036281179209 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 78.3575936 Hz = 73.2551285 Mel = -4.22226002 semitones above 100 Hz = 2.42495722 ERB
   16% = 98.3160097 Hz = 90.4529827 Mel = -0.29402078 semitones above 100 Hz = 2.96684697 ERB
   50% = 114.749947 Hz = 104.220969 Mel = 2.38192178 semitones above 100 Hz = 3.3930853 ERB
   84% = 223.385105 Hz = 187.472363 Mel = 13.9143959 semitones above 100 Hz = 5.84458847 ERB
   90% = 301.414861 Hz = 240.339677 Mel = 19.1010066 semitones above 100 Hz = 7.30599442 ERB
Estimated spreading:
   84%-median = 108.7 Hz = 83.28 Mel = 11.54 semitones = 2.452 ERB
   median-16% = 16.44 Hz = 13.77 Mel = 2.677 semitones = 0.4264 ERB
   90%-10% = 223.1 Hz = 167.1 Mel = 23.33 semitones = 4.883 ERB

Minimum 75.8076949 Hz = 71.0186669 Mel = -4.79500558 semitones above 100 Hz = 2.35368313 ERB
Maximum 452.309996 Hz = 330.079383 Mel = 26.1277425 semitones above 100 Hz = 9.65069149 ERB
Range 376.5 Hz = 259.060716 Mel = 30.92 semitones = 7.297 ERB
Average: 153.527827 Hz = 131.845094 Mel = 5.45644875 semitones above 100 Hz = 4.17770968 ERB
Standard deviation: 84.9 Hz = 60.83 Mel = 7.728 semitones = 1.743 ERB

Mean absolute slope: 484.7 Hz/s = 361.5 Mel/s = 50.92 semitones/s = 10.56 ERB/s
Mean absolute slope without octave jumps: 26.27 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 波形图中有着明显的规律性，约为 4 s 一个周期。
- 整体数值较为平稳（相比于其他BGM）

此外，结合内容创作的情况，可以得到结论：

- 曲风明快，有较强节奏感，适合温馨题材的作品。整首BGM没有中断感，一般搭配的视频都是一镜到底。



##### 一起长大的幸福

以下为波形图：![praat](BGM音频分析.assets/praat-1596034962633.png)

以下为基本音频信息：

```python
Time domain:
   Start time: 0 seconds
   End time: 15.058480725623582 seconds
   Total duration: 15.058480725623582 seconds
Time sampling:
   Number of frames: 1502 (918 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02424036281179209 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 79.6054469 Hz = 74.3462886 Mel = -3.94873135 semitones above 100 Hz = 2.45966291 ERB
   16% = 92.662134 Hz = 85.6354705 Mel = -1.31937824 semitones above 100 Hz = 2.81613593 ERB
   50% = 122.123533 Hz = 110.28813 Mel = 3.46009472 semitones above 100 Hz = 3.57887174 ERB
   84% = 427.704771 Hz = 316.409212 Mel = 25.1593836 semitones above 100 Hz = 9.30336054 ERB
   90% = 439.655197 Hz = 323.091075 Mel = 25.6364703 semitones above 100 Hz = 9.47354502 ERB
Estimated spreading:
   84%-median = 305.7 Hz = 206.2 Mel = 21.71 semitones = 5.728 ERB
   median-16% = 29.48 Hz = 24.67 Mel = 4.782 semitones = 0.7632 ERB
   90%-10% = 360.2 Hz = 248.9 Mel = 29.6 semitones = 7.018 ERB

Minimum 74.9570157 Hz = 70.2705268 Mel = -4.99037496 semitones above 100 Hz = 2.32979813 ERB
Maximum 501.980534 Hz = 356.681386 Mel = 27.931577 semitones above 100 Hz = 10.3173836 ERB
Range 427 Hz = 286.410859 Mel = 32.92 semitones = 7.988 ERB
Average: 200.02888 Hz = 161.704974 Mel = 8.16677722 semitones above 100 Hz = 4.98622648 ERB
Standard deviation: 141.1 Hz = 96.77 Mel = 11.11 semitones = 2.717 ERB

Mean absolute slope: 763.6 Hz/s = 535.5 Mel/s = 67.47 semitones/s = 15.23 ERB/s
Mean absolute slope without octave jumps: 22.75 semitones/s
```

结合波形图及数据，我们可以对这一音频进行简单的分析，并提取出这首BGM的一些基本特性：

- 波形图中出现了一定的规律性，约 3 s 一个小周期，对应原BGM的节奏与歌词。
- 从数据中看，这首BGM高音部分较多（206.2 Mel），但最高音却又不算特别高（356.7 Mel），与歌曲中的童声相符。
- 此外，歌曲的标准差非常大（96.77 Mel），推测是因为背景音乐音调较低，同时歌手吐字分明导致的。数据中，平均绝对斜率的值非常大（535.5 Mel ，接近《dance monkey》），但无倍频程跳跃的平均绝对斜率则比较正常

此外，结合内容创作的情况，可以得到结论：

- BGM节奏为活泼平稳，常用于亲子、成长的题材。BGM整体连贯性较高，作品也多为一镜到底。



### 3.2 猜想检验

#### 3.2.1 BGM的旋律具有稳定性

##### 猜想解释：

这里的稳定性指BGM中的旋律具有某种重复性，即没有非常频繁的转折变化。

进一步讲，在短暂的BGM中，一般会持续为相近的音调节奏，或某些特殊的BGM中间会出现一次变调，起到转折的作用。从合理性的角度去分析，在用户观看短视频进行消遣时，不宜输出过于复杂庞大的信息量，这会给增加用户的疲劳程度，同时节奏多变也难以营造出一中固定氛围，来与视觉内容搭配。

##### 猜想论证：

从随机所选的十首BGM中，通过波形图及解析得到的数据可以看到，有80%的数据支持，BGM的数据是保持稳定或具有某种规律的。剩余20%的数据均为英文歌，且其中一首虽然波形图呈现了一定的不稳定，但真实听觉中整体节奏较为平缓。

这样就得到两个论据：

1. 在样本中，有80%~90%的数据支持我们的结论。
2. 样本选取虽然有一定的人为因素，但更加注重实际数据，即选取的都是具有代表性的高频使用的BGM，样本的可靠具有保障。

由此可以说，从当前样本的结果而言，结论“BGM的旋律具有稳定性”有超过80%的概率是正确的

#### 3.2.2 BGM偏向于快节奏，一般对应整首歌中的高光部分

##### 猜想解释：

由于短视频多为15 s ~ 30 s，为了更好的内容效果，对于大多数内容而言，选择快节奏的短视频是理论上的较优选择。

整首歌的高光部分指：经过前面的铺垫，而出现的高音或核心部分，一般有着较强的氛围营造感与感染力。

##### 猜想论证：

在所选的十个样本中，只有《桥边姑娘》的波形图显示连续性较弱，但其节奏仍可以达到4/4拍，仅用约20 s 的时间就完成了两个八拍的内容。采用**极大值搜索法***来估计，只需通过波形图就可以了解到：所有样本BGM均为快节奏。由于对音频数据流操控能力有限，暂未能写出通过极大值搜索法进行检验的程序。

这样，在测试集中，支持的数据为100%。

对于后半句猜想，我们寻找了BGM的原曲，通过人工检验的方式确定了其正确性。此外，也用了数据分析的方式，对《dance monkey》进行了检验，将原曲截为每段 15 s，通过绘制波形图并分析的方法证明了结论。如果读者有兴趣，可以用代码再对其他BGM进行分析验证。

在测试集中，对于猜想“BGM偏向于快节奏，一般对应整首歌中的高光部分”有着强支持（100%)。这说明该结论在多数情况下是正确的。但这一结论并非绝对正确，我们也发现有少量的反例，那一类BGM对应的是特定题材，画面本身很有沉浸感，BGM只是作为辅助。

**极大值搜索法：选取自相关序列在某一区域内的极大值出现时间间隔作为该音乐节拍的长度*

#### 3.2.3 BGM会对原曲进行一些改变,  可能加入特殊的音效

##### 猜想解释：

BGM往往是改编后的结果，与原曲相比，常常会增加音效来满足使用需求。

##### 猜想论证：

从所选的测试集分析，多首BGM在原曲的基础上增加了混响音效，旧梦一场、小星星、桥边姑娘、我和你、谪仙都是再创作后的作品。相比原曲，抖音BGM往往更喜欢经DJ混响改变后的版本（普遍数据而言）。

支持数据占到了测试集的50%，说明这一猜想存在合理性，但只有一部分的正确性。

更精细地去分析，会发现不同类型的BGM对混响的需求不同，例如《桥边姑娘》是一首民谣，混响声音偏小。而作为流行音乐的《旧梦一场》《小星星》等BGM，混响音效的声音更大。更进一步地，它们适用的短视频作品类型也有所不同。



## 4. 案例分析

#### 4.1 抖音组

##### warp me in plastic![praat](BGM音频分析.assets/praat-1596034991555.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 14.14419501133787 seconds
   Total duration: 14.14419501133787 seconds
Time sampling:
   Number of frames: 1411 (808 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.022097505668934866 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 87.5768111 Hz = 81.2660638 Mel = -2.29655011 semitones above 100 Hz = 2.6787207 ERB
   16% = 130.515315 Hz = 117.112627 Mel = 4.61062928 semitones above 100 Hz = 3.7864011 ERB
   50% = 327.60231 Hz = 257.001394 Mel = 20.5433463 semitones above 100 Hz = 7.75344947 ERB
   84% = 469.78669 Hz = 339.586763 Mel = 26.7840701 semitones above 100 Hz = 9.890335 ERB
   90% = 520.517075 Hz = 366.288329 Mel = 28.5593459 semitones above 100 Hz = 10.5552718 ERB
Estimated spreading:
   84%-median = 142.3 Hz = 82.64 Mel = 6.245 semitones = 2.138 ERB
   median-16% = 197.2 Hz = 140 Mel = 15.94 semitones = 3.97 ERB
   90%-10% = 433.2 Hz = 285.2 Mel = 30.88 semitones = 7.881 ERB

Minimum 75.0689591 Hz = 70.369035 Mel = -4.9645394 semitones above 100 Hz = 2.33294431 ERB
Maximum 599.983804 Hz = 405.671673 Mel = 31.0190827 semitones above 100 Hz = 11.5153805 ERB
Range 524.9 Hz = 335.302638 Mel = 35.98 semitones = 9.182 ERB
Average: 301.400447 Hz = 231.707318 Mel = 16.3926272 semitones above 100 Hz = 6.96153549 ERB
Standard deviation: 149.8 Hz = 97.88 Mel = 10.41 semitones = 2.696 ERB

Mean absolute slope: 1093 Hz/s = 701.3 Mel/s = 73.73 semitones/s = 19.2 ERB/s
Mean absolute slope without octave jumps: 23.85 semitones/s
```



##### 你笑起来真好看![praat](BGM音频分析.assets/praat-1596035169512.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 26.656848072562358 seconds
   Total duration: 26.656848072562358 seconds
Time sampling:
   Number of frames: 2662 (1601 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.023424036281178503 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 77.6691178 Hz = 72.6521768 Mel = -4.37504418 semitones above 100 Hz = 2.40576033 ERB
   16% = 77.8071262 Hz = 72.7730944 Mel = -4.34430961 semitones above 100 Hz = 2.40961122 ERB
   50% = 101.714011 Hz = 93.3281551 Mel = 0.294221152 semitones above 100 Hz = 3.05640153 ERB
   84% = 155.88779 Hz = 137.245905 Mel = 7.68609517 semitones above 100 Hz = 4.39004749 ERB
   90% = 263.735591 Hz = 215.444465 Mel = 16.7891073 semitones above 100 Hz = 6.62602367 ERB
Estimated spreading:
   84%-median = 54.19 Hz = 43.93 Mel = 7.394 semitones = 1.334 ERB
   median-16% = 23.91 Hz = 20.56 Mel = 4.64 semitones = 0.647 ERB
   90%-10% = 186.1 Hz = 142.8 Mel = 21.17 semitones = 4.222 ERB

Minimum 75.0018008 Hz = 70.309939 Mel = -4.98003433 semitones above 100 Hz = 2.33105693 ERB
Maximum 570.847577 Hz = 391.557191 Mel = 30.157267 semitones above 100 Hz = 11.1740138 ERB
Range 495.8 Hz = 321.247252 Mel = 35.14 semitones = 8.843 ERB
Average: 137.216497 Hz = 116.872049 Mel = 2.4128842 semitones above 100 Hz = 3.70314017 ERB
Standard deviation: 109.3 Hz = 74.69 Mel = 8.93 semitones = 2.1 ERB

Mean absolute slope: 431.2 Hz/s = 303 Mel/s = 40.08 semitones/s = 8.656 ERB/s
Mean absolute slope without octave jumps: 15.49 semitones/s
```



##### 陪你长大![praat](BGM音频分析.assets/praat-1596035239550.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 15.084603174603174 seconds
   Total duration: 15.084603174603174 seconds
Time sampling:
   Number of frames: 1505 (930 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.022301587301586708 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 77.0691003 Hz = 72.1261553 Mel = -4.50930655 semitones above 100 Hz = 2.38900152 ERB
   16% = 77.6786714 Hz = 72.6605481 Mel = -4.37291484 semitones above 100 Hz = 2.40602695 ERB
   50% = 93.6435055 Hz = 86.4747024 Mel = -1.13698984 semitones above 100 Hz = 2.84245018 ERB
   84% = 230.92034 Hz = 192.805178 Mel = 14.488743 semitones above 100 Hz = 5.99505749 ERB
   90% = 272.391716 Hz = 221.264199 Mel = 17.348194 semitones above 100 Hz = 6.78624518 ERB
Estimated spreading:
   84%-median = 137.4 Hz = 106.4 Mel = 15.63 semitones = 3.154 ERB
   median-16% = 15.97 Hz = 13.82 Mel = 3.238 semitones = 0.4367 ERB
   90%-10% = 195.4 Hz = 149.2 Mel = 21.87 semitones = 4.4 ERB

Minimum 74.9951452 Hz = 70.3040821 Mel = -4.98157066 semitones above 100 Hz = 2.33086987 ERB
Maximum 599.207147 Hz = 405.300097 Mel = 30.996658 semitones above 100 Hz = 11.5064317 ERB
Range 524.2 Hz = 334.996015 Mel = 35.98 semitones = 9.176 ERB
Average: 141.715484 Hz = 122.63661 Mel = 3.72477739 semitones above 100 Hz = 3.89966067 ERB
Standard deviation: 81.18 Hz = 60.35 Mel = 8.542 semitones = 1.763 ERB

Mean absolute slope: 413.1 Hz/s = 304.6 Mel/s = 43.85 semitones/s = 8.882 ERB/s
Mean absolute slope without octave jumps: 15.86 semitones/s
```



##### 蓝色海黑色河![praat](BGM音频分析.assets/praat-1596061858434.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 13.073174603174603 seconds
   Total duration: 13.073174603174603 seconds
Time sampling:
   Number of frames: 1304 (751 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.021587301587301263 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 80.2015183 Hz = 74.8667482 Mel = -3.81958256 semitones above 100 Hz = 2.476201 ERB
   16% = 81.6655444 Hz = 76.1429757 Mel = -3.50640692 semitones above 100 Hz = 2.51671134 ERB
   50% = 104.48749 Hz = 95.6638066 Mel = 0.759962754 semitones above 100 Hz = 3.1289381 ERB
   84% = 434.680347 Hz = 320.319334 Mel = 25.4394584 semitones above 100 Hz = 9.40304622 ERB
   90% = 447.185375 Hz = 327.260124 Mel = 25.9304761 semitones above 100 Hz = 9.57932898 ERB
Estimated spreading:
   84%-median = 330.4 Hz = 224.8 Mel = 24.7 semitones = 6.278 ERB
   median-16% = 22.84 Hz = 19.53 Mel = 4.269 semitones = 0.6126 ERB
   90%-10% = 367.2 Hz = 252.6 Mel = 29.77 semitones = 7.108 ERB

Minimum 74.9449111 Hz = 70.2598739 Mel = -4.9931709 semitones above 100 Hz = 2.32945788 ERB
Maximum 597.425941 Hz = 404.446967 Mel = 30.9451186 semitones above 100 Hz = 11.4858777 ERB
Range 522.5 Hz = 334.187093 Mel = 35.94 semitones = 9.156 ERB
Average: 195.29081 Hz = 156.412428 Mel = 6.90011106 semitones above 100 Hz = 4.8105131 ERB
Standard deviation: 156.1 Hz = 105.4 Mel = 12.12 semitones = 2.947 ERB

Mean absolute slope: 1268 Hz/s = 878.6 Mel/s = 114.4 semitones/s = 24.99 ERB/s
Mean absolute slope without octave jumps: 43.92 semitones/s
```



##### 带你去旅行![praat](BGM音频分析.assets/praat-1596061903383.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 10.04297052154195 seconds
   Total duration: 10.04297052154195 seconds
Time sampling:
   Number of frames: 1001 (573 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.021485260770974898 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 86.6825253 Hz = 80.4940744 Mel = -2.47424294 semitones above 100 Hz = 2.65436975 ERB
   16% = 87.4137016 Hz = 81.1253407 Mel = -2.32882397 semitones above 100 Hz = 2.67428348 ERB
   50% = 116.761343 Hz = 105.882643 Mel = 2.68275252 semitones above 100 Hz = 3.44409057 ERB
   84% = 263.357428 Hz = 215.188806 Mel = 16.7642658 semitones above 100 Hz = 6.61896709 ERB
   90% = 277.29822 Hz = 224.535826 Mel = 17.6572603 semitones above 100 Hz = 6.87597131 ERB
Estimated spreading:
   84%-median = 146.7 Hz = 109.4 Mel = 14.09 semitones = 3.178 ERB
   median-16% = 29.37 Hz = 24.78 Mel = 5.016 semitones = 0.7705 ERB
   90%-10% = 190.8 Hz = 144.2 Mel = 20.15 semitones = 4.225 ERB

Minimum 77.0094828 Hz = 72.0738625 Mel = -4.52270384 semitones above 100 Hz = 2.38733492 ERB
Maximum 300.341258 Hz = 239.645709 Mel = 19.0392321 semitones above 100 Hz = 7.28722797 ERB
Range 223.3 Hz = 167.571846 Mel = 23.56 semitones = 4.9 ERB
Average: 154.633121 Hz = 133.005142 Mel = 5.45573955 semitones above 100 Hz = 4.21228102 ERB
Standard deviation: 78.43 Hz = 59.33 Mel = 8.354 semitones = 1.74 ERB

Mean absolute slope: 445.3 Hz/s = 342.4 Mel/s = 51.34 semitones/s = 10.13 ERB/s
Mean absolute slope without octave jumps: 27.28 semitones/s
```



#### 4.2 对照组

##### All Rise

![praat](BGM音频分析.assets/praat-1596062495672.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 223.48950113378686 seconds
   Total duration: 223.48950113378686 seconds
Time sampling:
   Number of frames: 22345 (9645 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.024750566893421252 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 87.1202703 Hz = 80.8720918 Mel = -2.38703598 semitones above 100 Hz = 2.66629632 ERB
   16% = 97.3324548 Hz = 89.6179486 Mel = -0.468085842 semitones above 100 Hz = 2.94078303 ERB
   50% = 176.450623 Hz = 153.03873 Mel = 9.83117426 semitones above 100 Hz = 4.85499679 ERB
   84% = 295.015367 Hz = 236.190094 Mel = 18.7294813 semitones above 100 Hz = 7.1936229 ERB
   90% = 366.94613 Hz = 281.121746 Mel = 22.5068194 semitones above 100 Hz = 8.39099993 ERB
Estimated spreading:
   84%-median = 118.6 Hz = 83.16 Mel = 8.899 semitones = 2.339 ERB
   median-16% = 79.12 Hz = 63.42 Mel = 10.3 semitones = 1.914 ERB
   90%-10% = 279.8 Hz = 200.3 Mel = 24.9 semitones = 5.725 ERB

Minimum 74.9749288 Hz = 70.2862912 Mel = -4.98623818 semitones above 100 Hz = 2.33030165 ERB
Maximum 599.864698 Hz = 405.614705 Mel = 31.0156456 semitones above 100 Hz = 11.5140086 ERB
Range 524.9 Hz = 335.328414 Mel = 36 semitones = 9.184 ERB
Average: 202.214552 Hz = 165.38105 Mel = 9.35295087 semitones above 100 Hz = 5.12332672 ERB
Standard deviation: 126 Hz = 84.22 Mel = 9.672 semitones = 2.351 ERB

Mean absolute slope: 623.4 Hz/s = 424.9 Mel/s = 50.07 semitones/s = 11.95 ERB/s
Mean absolute slope without octave jumps: 17.48 semitones/s
```



##### 浮夸![praat](BGM音频分析.assets/praat-1596063157143.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 286.1572562358277 seconds
   Total duration: 286.1572562358277 seconds
Time sampling:
   Number of frames: 28612 (12870 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.023628117913834786 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 80.0270823 Hz = 74.7144904 Mel = -3.85727741 semitones above 100 Hz = 2.47136392 ERB
   16% = 82.0546865 Hz = 76.4817028 Mel = -3.42410832 semitones above 100 Hz = 2.52745308 ERB
   50% = 140.495503 Hz = 125.12015 Mel = 5.88628749 semitones above 100 Hz = 4.02799837 ERB
   84% = 337.476643 Hz = 263.155159 Mel = 21.0574519 semitones above 100 Hz = 7.91723008 ERB
   90% = 409.555532 Hz = 306.103551 Mel = 24.408709 semitones above 100 Hz = 9.03930441 ERB
Estimated spreading:
   84%-median = 197 Hz = 138 Mel = 15.17 semitones = 3.889 ERB
   median-16% = 58.44 Hz = 48.64 Mel = 9.311 semitones = 1.501 ERB
   90%-10% = 329.5 Hz = 231.4 Mel = 28.27 semitones = 6.568 ERB

Minimum 74.9383617 Hz = 70.25411 Mel = -4.99468387 semitones above 100 Hz = 2.32927377 ERB
Maximum 595.856814 Hz = 403.694317 Mel = 30.8995883 semitones above 100 Hz = 11.4677356 ERB
Range 520.9 Hz = 333.440207 Mel = 35.89 semitones = 9.138 ERB
Average: 191.436654 Hz = 156.797122 Mel = 7.78906395 semitones above 100 Hz = 4.86144279 ERB
Standard deviation: 128.3 Hz = 88.55 Mel = 10.66 semitones = 2.5 ERB

Mean absolute slope: 414.4 Hz/s = 289.2 Mel/s = 35.93 semitones/s = 8.212 ERB/s
Mean absolute slope without octave jumps: 13.65 semitones/s
```



##### 红豆![praat](BGM音频分析.assets/praat-1596063192841.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 236.1588888888889 seconds
   Total duration: 236.1588888888889 seconds
Time sampling:
   Number of frames: 23612 (13150 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02444444444444571 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 77.8814286 Hz = 72.8381843 Mel = -4.32778497 semitones above 100 Hz = 2.41168393 ERB
   16% = 82.6859864 Hz = 77.0307718 Mel = -3.29142303 semitones above 100 Hz = 2.54485612 ERB
   50% = 106.767493 Hz = 97.576482 Mel = 1.13366954 semitones above 100 Hz = 3.18819747 ERB
   84% = 181.314371 Hz = 156.70883 Mel = 10.3019193 semitones above 100 Hz = 4.96201571 ERB
   90% = 204.668022 Hz = 173.997818 Mel = 12.3994285 semitones above 100 Hz = 5.46113263 ERB
Estimated spreading:
   84%-median = 74.55 Hz = 59.13 Mel = 9.169 semitones = 1.774 ERB
   median-16% = 24.08 Hz = 20.55 Mel = 4.425 semitones = 0.6434 ERB
   90%-10% = 126.8 Hz = 101.2 Mel = 16.73 semitones = 3.05 ERB

Minimum 74.9415061 Hz = 70.2568773 Mel = -4.99395748 semitones above 100 Hz = 2.32936216 ERB
Maximum 599.492535 Hz = 405.436665 Mel = 31.0049015 semitones above 100 Hz = 11.5097209 ERB
Range 524.6 Hz = 335.179787 Mel = 36 semitones = 9.18 ERB
Average: 136.208316 Hz = 118.31395 Mel = 3.40670913 semitones above 100 Hz = 3.77587925 ERB
Standard deviation: 84.21 Hz = 58.13 Mel = 7.374 semitones = 1.65 ERB

Mean absolute slope: 254.5 Hz/s = 188.8 Mel/s = 27.82 semitones/s = 5.527 ERB/s
Mean absolute slope without octave jumps: 15.32 semitones/s
```



##### 星星电灯![praat](BGM音频分析.assets/praat-1596063217771.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 303.032358276644 seconds
   Total duration: 303.032358276644 seconds
Time sampling:
   Number of frames: 30300 (16745 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.02117913832200202 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 92.5898766 Hz = 85.573628 Mel = -1.33288358 semitones above 100 Hz = 2.81419584 ERB
   16% = 103.65518 Hz = 94.9639277 Mel = 0.621506608 semitones above 100 Hz = 3.10722244 ERB
   50% = 155.657863 Hz = 137.066725 Mel = 7.66054142 semitones above 100 Hz = 4.38473015 ERB
   84% = 276.639846 Hz = 224.097955 Mel = 17.6161076 semitones above 100 Hz = 6.8639767 ERB
   90% = 290.807063 Hz = 233.444168 Mel = 18.4807477 semitones above 100 Hz = 7.11905352 ERB
Estimated spreading:
   84%-median = 121 Hz = 87.03 Mel = 9.956 semitones = 2.479 ERB
   median-16% = 52 Hz = 42.1 Mel = 7.039 semitones = 1.278 ERB
   90%-10% = 198.2 Hz = 147.9 Mel = 19.81 semitones = 4.305 ERB

Minimum 75.423361 Hz = 70.6807859 Mel = -4.88299985 semitones above 100 Hz = 2.34289864 ERB
Maximum 594.922654 Hz = 403.245746 Mel = 30.8724254 semitones above 100 Hz = 11.4569192 ERB
Range 519.5 Hz = 332.564961 Mel = 35.76 semitones = 9.114 ERB
Average: 181.339413 Hz = 153.390499 Mel = 8.64053107 semitones above 100 Hz = 4.81688939 ERB
Standard deviation: 83.51 Hz = 59.61 Mel = 7.51 semitones = 1.707 ERB

Mean absolute slope: 439.8 Hz/s = 311.5 Mel/s = 38.33 semitones/s = 8.883 ERB/s
Mean absolute slope without octave jumps: 13.86 semitones/s
```



##### 最初的梦想![praat](BGM音频分析.assets/praat-1596063248032.png)

```python
Time domain:
   Start time: 0 seconds
   End time: 296.7107256235828 seconds
   Total duration: 296.7107256235828 seconds
Time sampling:
   Number of frames: 29668 (17271 voiced)
   Time step: 0.01 seconds
   First frame centred at: 0.020362811791391097 seconds
Ceiling at: 600 Hz

Estimated quantiles:
   10% = 77.9631766 Hz = 72.9097878 Mel = -4.30962265 semitones above 100 Hz = 2.41396387 ERB
   16% = 78.7076857 Hz = 73.561478 Mel = -4.14508291 semitones above 100 Hz = 2.43470557 ERB
   50% = 175.212674 Hz = 152.100672 Mel = 9.70928562 semitones above 100 Hz = 4.82758196 ERB
   84% = 408.97273 Hz = 305.769398 Mel = 24.3840558 semitones above 100 Hz = 9.03071017 ERB
   90% = 420.047358 Hz = 312.084638 Mel = 24.8466239 semitones above 100 Hz = 9.1927892 ERB
Estimated spreading:
   84%-median = 233.8 Hz = 153.7 Mel = 14.68 semitones = 4.203 ERB
   median-16% = 96.51 Hz = 78.54 Mel = 13.85 semitones = 2.393 ERB
   90%-10% = 342.1 Hz = 239.2 Mel = 29.16 semitones = 6.779 ERB

Minimum 74.9553218 Hz = 70.2690361 Mel = -4.99076618 semitones above 100 Hz = 2.32975052 ERB
Maximum 599.632547 Hz = 405.503652 Mel = 31.0089443 semitones above 100 Hz = 11.5113342 ERB
Range 524.7 Hz = 335.234616 Mel = 36 semitones = 9.182 ERB
Average: 217.441778 Hz = 174.06134 Mel = 9.45300289 semitones above 100 Hz = 5.33594086 ERB
Standard deviation: 143.7 Hz = 99.18 Mel = 11.9 semitones = 2.8 ERB

Mean absolute slope: 614.1 Hz/s = 423.4 Mel/s = 51.11 semitones/s = 11.95 ERB/s
Mean absolute slope without octave jumps: 17.91 semitones/s
```







## 5. 代码

*该部分内容主要为对pyAudioAnalysis的介绍*

##### ShortTermFeatures.py

- 短期时长的特征抽取：`feature_extraction()`方法

  将音频信号拆分成短期的片段/元组，然后计算每个片段/元组的特征，最终生成整段音频的特征向量的序列。

  通过这个方法可以提取出音频的多中数值特征



##### MidTermFeatures.py

- 中期时长的特征抽取：`mid_feature_extraction()`方法

  根据整段音频的短期片段的特征向量的序列，计算了一些统计值，如均值、标准差等。

  

##### audioTrainTest.py

- `classifier_wrapper()`:分类未知的样本
- `random_split_features()`:将实验样本随机拆分成训练集和测试集，用于交叉验证
- `train_knn()`, `train_svm()`, `train_SVM_RBF()`, `train_extra_trees()`, `train_random_forest()` and `train_gradient_boosting()`: 基于不同算法的训练模型
- `normalize_features()`: 将数据集进行标准化，进行0平均和归一化处理
- `load_model()`: 从文件中加载分类模型



##### audioAnalyse.py

- `dirMp3toWavWrapper(directory, samplerate, channels)`: 把mp3 转成wav
- `featureExtractionFileWrapper(wav_file, out_file, mt_win, mt_step,st_win, st_step)`:从WAV文件中提取特征
- `fileSpectrogramWrapper(wav_file)`：从WAV文件中提取频谱图
- `featureExtractionDirWrapper(directory, mt_win, mt_step, st_win, st_step)`：提取文件夹中存储的所有WAV文件的特征



##### audioBasicIO.py

- `read_audio_file(input_file)`: 读取文件，转化为信号
- `stereo_to_mono(signal)`: 信号转为单声道信号