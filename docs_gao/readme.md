我就是想给llamafactory的cli加一个配置 --random_vision.如果启用，则把tokenize后的多模态输入里的vision padding给random化，其余的sft同原始的llamafactory。这会涉及到去改llamafactory的源吗，所以你得针对这个设置plan

现在的洗好的llamafactory数据(json格式)`/mnt/xlab-nas-wm/gaozhe.gz/codes/DeepEyes/scripts/step_0_sft_prepare/cot_24k.json`里会有image/视频路径，但是我现在不想要这个路径，你random化一个就行。