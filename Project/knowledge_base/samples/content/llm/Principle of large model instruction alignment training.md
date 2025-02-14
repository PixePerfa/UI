# The principle of instruction alignment training for large models
- RLHF
    - SFT
    - RM
    - PPO
- AIHF-based
    - RLAIF
        - The core lies in supervising other AI models through the AI model, i.e., in the SFT phase, sampling from the initial model, then generating self-criticism and corrections, and then fine-tuning the original model based on the modified responses. In the RL phase, samples are sampled from a fine-tuned model, one model is used to evaluate the resulting samples, and a preference model is trained from this AI preference dataset. The RL is then trained using the preference model as a reward signal
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-17565-176537.jpg)
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-95996-523276.jpg)
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-349153-657791.jpg)
    - RRHF
        - RRHF( **R** ank **R** esponse from **H** uman **F** eedback) does not require reinforcement learning and can utilize responses generated by different language models, including ChatGPT, GPT-4, or the current trained model. RRHF aligns responses with human preferences by scoring them and by ranking losses. RRHF aligns scores with human preferences (or agents' reward models) through rank loss. RRHF trained models can be used as both generative language models and reward models. 
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-805089-731888.jpg)
- SFT-only
    - LIMA
        - LIMA (Less Is More for Alignment) is the shallow alignment hypothesis, which states that a **model's knowledge and abilities are learned almost entirely in pre-training, while alignment teaches it how to choose subdistributions when interacting with users** . If the hypothesis is correct and the alignment is primarily about learning style, then a corollary of the hypothesis is that one can adequately tune a pre-trained language model with a fairly small number of samples. Therefore, **the working hypothesis is that alignment can be a simple process in which the model learns the style or format of interaction with the user to reveal the knowledge and abilities that have been acquired in the pre-training. **
    - LTD Instruction Tuning
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-759487-923925.jpg)
- Reward-only
    - DPO
        - Direct Preference Optimization (DPO) proposes a method to use binary cross-entropy targets to accurately optimize LLM to replace RL HF-based optimization goals, thereby greatly simplifying the preference learning pipeline. That is, it is entirely possible to optimize the language model directly to achieve human preferences without the need for explicit reward models or reinforcement learning.
        - DPO also relies on theoretical preference models, such as the Bradley-Terry model, to measure how well a given reward function fits empirical preference data. However, existing methods use preference model definition preference loss to train a reward model and then train a strategy that optimizes the learned reward model, while DPO uses changes in variables to directly define preference loss as a function of the strategy. Given the human preference dataset for model responses, DPOs can therefore use a simple binary cross-entropy target to optimize the strategy without explicitly learning the reward function or sampling from the policy during training.
    - RAFT
        -  ![Image](./img/大模型指令对齐训练原理-幕布图片-350029-666381.jpg)
- References
    -  [Reflect on RLHF]("https://mp.weixin.qq.com/s/e3E_XsZTiNMNYqzzi6Pbjw")
    -  [RLHF Notes]("https://mathpretty.com/16017.html")
    -  [hf-blog]("https://huggingface.co/blog/zh/rlhf")
    - ** [RLHF code explained in detail]("https://zhuanlan.zhihu.com/p/624589622")