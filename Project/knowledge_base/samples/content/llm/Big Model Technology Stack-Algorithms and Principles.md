# Large Model Technology Stack - Algorithms and Principles
- 1. tokenizer method
    - word-level
    - char-level
    - subword-level
        - BPE
        - WordPiece
        - UniLM
        - SentencePiece
        - ByteBPE
- 2. position encoding
    - Absolute position encoding
        - ROPE
        - AliBi
    - Relative position encoding
        - Transformer-XL
        - T5/TUPE
        - DeBERTa
    - Other location encoding
- 3.  Attention mechanisms
    - Sparse attention
    - flash-attention
    - 
- 4. Distributed training
    - Data parallelism
        - FSDP
        - DDP
        - ZeRO
            - Model state
                - Optimizer->ZeRO1
                    - Divide the optimizer state into several parts, one for each GPU
                    - Each GPU stores a complete parameter W, after a round of foward and backward, each gets a gradient, and does an **AllReduce (reduce-scatter + all-gather)** ** on the gradient to get the complete gradient Gto do an All-Gather with W**
                - Gradient+Optimzer->ZeRO2
                    - Each GPU maintains one gradient
                    - Each GPU stores a complete parameter W, and after a round of foward and backward,  a **complete gradient is calculated, and the gradient is Reduce-Scatter once to ensure that the gradient maintained on each GPU is an aggregate gradient, and each GPU updates the corresponding W with its own corresponding O and G. After the update is completed, each GPU maintains an updated W. In the same way, do an All-Gather on W and sync W from other GPUs to yourself**
                - Parameter+Gradient+Optimizer->ZeRO3
                    - Each GPU maintains a piece of model state
                    - Only part of the parameters W are stored on each GPU, and when forward, **do an All-Gather on W to ** retrieve the W distributed on other GPUs to get a complete W **When you do backward, do an All-Gather on W to retrieve the full W, and when backward is done, immediately discard W that you don't maintain. After doing backward, calculate a complete gradient G, do a Reduce-Scatter on G, aggregate the part of the gradient that you maintain from other GPUs, and immediately discard the G that you don't maintain after the aggregation operation. With O and G which I maintain, I update W. Since only part of the W is maintained, there is no need to do any AllReduce operations on the W**
            - Residual state
                - activation->Partitioned Activation Checkpointing
                    - Only part of the activation is maintained on each GPU, and it can be aggregated from elsewhere if needed. It should be noted that the occupation of video memory by activation is generally much higher than that of the model itself, and the traffic is also huge
                - temporary buffer->Constant Size Buffer
                    - Improve bandwidth utilization. As the number of GPUs increases, so does the number of GPUs that can communicate with each other, and the amount of traffic may decrease each time (but the total amount of traffic will not change). If the data slices are small, the bandwidth will not be used well. So this buffer plays a role in accumulating data: wait for the data to accumulate to a certain size, and then communicate.
                    - Make the storage size controllable. Before each communication, the accumulated storage size is constant and is known to be controllable. It is more convenient for users to estimate the storage consumption and communication time in training
                - unusable fragment->Memory Defragmentation
                    - Reorganize the fragmented storage space to create a continuous storage space. Prevent storage requests from failing caused by sufficient total storage but insufficient continuous storage
            - offload
                - ZeRO-Offload
                    - **Forward and backward are computationally intensive** , so the parts related to them, such as the parameter W (fp16) and activation, are all put into the GPU
                    - **The update part is computationally low** , so all the parts related to it are put into the CPU. Examples include W (fp32), optimizer states (fp32) and gradients (fp16), among others
                    - ZeRO-Offload is divided into two parts: Offload Strategy and Offload Schedule, the former solves the problem of how to divide the model between the GPU and the CPU, and the latter solves the problem of how to schedule computation and communication
                - ZeRO-Infinity
                    - The first is to extend the combination of offload and ZeRO from ZeRO-2 to ZeRO-3, which solves the problem that model parameters are limited by a single GPU memory
                    - Second, it solves the problem that ZeRO-Offload is inefficient when the training batch size is small
                    - The third is to further try to use NVMe space in addition to CPU memory
    - Models are parallel
        - tensor-wise parallelism
            - Megatron-LM
        - Parallel pipelines
            - GPipe
            - PipeDream
        - layer-wise parallelism
        - sequence parallelism
- 5. PEFT
    - Lora class
        - LoRA
            - Replace the increment of the weight matrix to be updated with two low-rank matrices
        - QLoRA
            - 4 bit NormalFloat (NF4) quantization and double quantization
            - A page optimizer was introduced to prevent memory spikes during gradient checkpoints
        - AdaLoRA
            - The singular value decomposition P\Gamma Q was used instead of AB, the importance score of the diagonal value was evaluated according to the loss gradient, and the parameter budget was dynamically allocated to the weight matrix according to the score
            - AdaLoRA assigns the critical delta matrices high rank to capture more granular and task-specific information, while the less important matrices are ranked lower to prevent overfitting merging to save computational budgets.
            - Incremental updates are parameterized in the form of singular value decomposition, and unimportant singular values are trimmed out based on importance metrics while preserving singular vectors.
            - An additional penalty term is added to the training loss to normalize the orthogonality of singular matrices P and Q, thus avoiding a large number of computations for SVD and stabilizing training
        - IA3
            - The activation layer weighting is scaled by learning vectors
            - The learned vectors are injected into the Attention and FeedForward modules
        - ReLoRA
            - **ReLoRA can do a partial reset of the optimizer during merging and restarting** , and set the learning rate to 0 during subsequent warm-ups. **Specifically, the authors propose a zigzag learning rate scheduling algorithm**
            - Starting point: To achieve better training effect by continuously superimposing the LoRA training process, **first of all, the LoRA process needs to be restarted, it is not easy to restart the completed LoRA process, which requires fine adjustment of the optimizer, if the adjustment is not in place, it will lead to the divergence between the model and the previous optimization direction immediately after the restart**
    - Prompt class
        - prompt tuning
            - Add an embedding layer to the input layer
        - P-tuning
            - Add an embedding and an LSTM or MLP to the input layer
        - prefix tuning
            - Add an embedding and an MLP to each layer
        - P-tuning v2
            - Add an embedding layer to each layer
    - Adapter class
        - Adapter Tuning
            - For each Transformer layer, two adapter structures have been added (after the projection of the multi-head attention and after the second feed-forward layer)
        - Adapter Fusion
            - Optimized on top of the Adapter to improve downstream task performance by dividing the learning process into two phases
            - Knowledge Extraction Stage: Introduce their own Adapter modules under different tasks to learn information about specific tasks.
            - Knowledge Combination Stage: The parameters of the pre-trained model are fixed with the task-specific Adapter parameters, and new parameters (AdapterFusion) are introduced to learn to combine the knowledge in multiple Adapters to improve the performance of the model in the target task
        - Adapter Drop
            - Without affecting the performance of the task, the adapter is dynamically and efficiently removed to reduce the number of parameters of the model as much as possible and improve the efficiency of the model during backpropagation (training) and forward propagation (inference).
    - other
        - BitFit
            - The sparse fine-tuning method updates only the bias parameters or some of the bias parameters during training
    - Hybrid
        - MAM Adapter
            - Use a combination of parallel adapters and soft hints for the FFN layer
        - UniPELT
            - The gating is implemented as a linear layer, with GP parameters controlling the switching of the Prefix-tuning method, GL controlling the switching of the LoRA method, and GA controlling the switching of the Adapter method
- 6. compress
    - Pruning
        - OBD(Optimal Brain Damage)
            - The second derivative information is used to measure the significance of model parameters, and the parameters with small impact are cut out, which reduces the complexity of the model and improves the generalization ability
            -  ![Pictures](./img/大模型技术栈-算法与原理-幕布图片-628857-182232.jpg)
        - OBS（Optimal Brain Surgeon ）
            - OBD brutally only considers the diagonal elements of the Haysom matrix. OBS considers the global information of the Haysen matrix, and thus obtains the influence of parameters on each other.
        - OBC（OPTIMAL BRAIN COMPRESSION ）
            - OBS prunes the entire neural network, and OBC prunes or quantifies the neural network model in layers
        - ExactOBS
            - Parameter updates and cost estimation do not require the use of the entire Hasten matrix, but only the Hasten matrix of the d_col\time d_col size associated with the row of the pruning parameters.
    - Quantify ![the image](./img/大模型技术栈-算法与原理-幕布图片-454007-940199.jpg)
        - GPTQ
            - 1. It is an improvement on OBC
            - 2. The greedy algorithm is eliminated and fixed position optimization is adopted
            - 3. Group quantization, parallel acceleration
            -  ![Image](./img/大模型技术栈-算法与原理-幕布图片-729151-372321.jpg)
        - SpQR
            - The core idea: there is a strong imbalance in the importance of parameters to the model. If we protect these 1% parameters in quantization, we can greatly protect the performance of the model from being affected
            - 2. For each layer, it uses a small input dataset X, which is used to calculate the error s_ij caused by a single parameter before and after w_ij quantization. After having s_ij, the top 1% of parameters are considered to be important parameters for protection.
            - After the parameters are selected, SqQR uses a sparse matrix to store them individually, so that the accuracy of these important parameters is still fp16.
            - SqQR also observed that important parameters tend to be clustered in rows or columns, so it proposes to use smaller group_size such as 8 or 16 instead of the 128 commonly used in GPTQ
        - AWQ
            - 1. AWS is proposed on top of smoothquant
            - 2. AWQ looks for important parameters for the channel dimension, based on the input X and the absolute size of the parameter itself, W
            - 3. The way is to find a scale s, multiply W by this ratio before the parameter quantization, and enter X to divide this ratio when calculating to reduce the error
            - 4. Dividing s s into two values S_x multiplying S_w, we need that the larger the W, the smaller the s, and the larger the X, the larger the s
            -  ![Image](./img/大模型技术栈-算法与原理-幕布图片-299768-254064.jpg)
        - OBC（OPTIMAL BRAIN COMPRESSION ）
            -  ![Image](./img/大模型技术栈-算法与原理-幕布图片-19929-302935.jpg)
        - SmoothQuant
            - 1. When the model size is larger, the value of a single token varies more widely and is difficult to quantify, compared to weight, which is easier to quantify, while activation is more difficult to quantify
            - 2. The core idea of SmoothQuant is to introduce a hyperparameter to reduce the variation range of the activation value and increase the variation range of the weight, so as to balance the quantization difficulty of the two
            - 3. After obtaining the activation and weight matrices after the smooth transformation, you can use the per-token or per-tensor quantization method.
            -  ![Image](./img/大模型技术栈-算法与原理-幕布图片-81470-404273.jpg)
        - LLM.int8
            - The quantitative method of mixed-precision decomposition is adopted: several dimensions containing Emergent Features are separated from the matrix, and high-precision matrix multiplication is performed. The rest is quantified
        - ZeroQuant
            - 1. Use group quantization for weights and token quantization for activations
            - 2. A highly optimized inference backend has been developed to eliminate the expensive computational cost of quantization/dequantization operators and achieve latency acceleration of the INT8 Tensor core on modern GPU hardware
            - 3. A new layer-by-layer knowledge distillation method (LKD) for INT4/INT8 mixed-precision quantization is proposed, in which the neural network is quantized layer by layer by distillation with minimal iteration and even no access to the original training data
        - taxonomy
            - Symmetric vs. asymmetric quantization
                - Whether the quantization is balanced and whether the origin is 0
            - Dynamic quantization vs static quantization
                - The scale factor for the input is calculated differently
                - Statically quantized models have a "calibrate" process (calibrating the scale factor) before use, and the scale factor of the quantized model is adjusted according to the distribution of the input data
            - Weights quantization vs. Activation quantization
                - Feature Map (FM) is the input tensor of each layer of the network, and FeatureMap quantization is what we often call activation quantization
            - per-token vs. per-layer/per-tensor vs. per channel vs. per group vs
                - **per-token quantization** : Activates the shared quantization coefficient of the tensor corresponding to each token
                - **per-tensor quantization** : Set up a simple set of quantizations for an entire tensor
                - **per-channel quantization** : Set a quantization set for each output channel of the weight, but in practice, the whole tensor shares a scale and zeropoint, but each kernel will count a scale and a zeropoint separately (note that each kernel, not each channel of the kernel).
                - **group-wise quantization** : Combine multiple channels together with a set of quantization coefficients
    - Layer Reduction
- 7. illation
    - 7.1 Throughput and Memory Optimization
        - PagedAttention
        - Qunatized KV Cache
        - MQA/GQA
        - FlashAttention
    - 7.2 Operator fusion
    - 7.3 Latency Optimization
        - No Padding optimization
    - 7.4 Scheduling Optimization
        - Dynamic Batching
        - Async Servering
        - Inflight Batching
    - 7.5 Quantification
    - 7.6 Model Parallelism
        - tensor paralellism
    - 7.7 Request Optimization
        - rpc
        - grpc
        - http
- 8. apply
    - RAG
    - Agent
- 9. embedding model
    - taxonomy
        - Symmetry vs. Asymmetry vs. hybrid
            - Symmetry query:qestion, text:text
                - sentence-T5
            - Asymmetric: query:text
                - GTR
            -mix
                - Instructor
        - Contrastive Learning + Contrastive Learning vs. Autocoding + Contrastive Learning
            - Contrastive learning + contrastive learning
                - sentence-T5
                - GTR
                - E5
            - Self-encoding + contrastive learning
                - bge
                - retromae
        - bert-based vs. GPT-based
            - bert-based
            - LLM-based
                - PromptEOL+CSE+LLM
    - Bert-CLS,Bert-mean
        - Transformer of two-way decoder-encoder
    - T5 series
        - Sentence-T5
            - T5-encoder+mean pooling
            - Two-stage training of unlabeled contrastive learning + labeled contrastive learning
        - Jina
            - T5 is the basic architecture
            - Deduplication, language filtering, consistency
            - **A parallelization approach was used to train on multiple datasets**, but with a constraint: each training batch contained only samples from a single dataset
            - Triplet training: enchor, entainment, contraversive
        - GTR
            - Same structure as sentence-T5
            - Finetune's dataset was changed from NLI to retrieval relevance, and Baidu's rocketQA was used to obtain hard negative
            - Contrastive learning is changed to two-way contrastive learning (there are two contrastive learning losses in each batch, the first loss is to construct positive and negative samples centered on query, and the second loss is to construct positive and negative samples centered on positive document)
    - simcse
        - Unsupervised Simcse
            - For the same sentence, two different dropout masks are used in training, and the sentence pairs after the two dropouts are regarded as a set of sample pairs that are positive examples of each other, that is, similar sentence pairs
            - "Dissimilar sentence pairs" can be done by sampling the rest of the sentences in the same batch
        - There is a supervised simcse
            - NLI (natural language reasoning) is used to determine the relationship between two sentences, and the possible relationships are entailment, contradiction or neutral.
            - The entailment sentence pair is used as a positive example, and the contradiction sentence pair is used as the hard negative example
        - Derived algorithms
            - Esimcse
                - ESimCSE chooses to repeat some words randomly in a sentence as a positive sample to solve the problem that the model tends to judge that sentences of the same or similar length are more similar in expression
                - A queue was maintained, the encoding embeddings of the preceding mini-batch were reused to extend the negative pairs, and the momentum encoder was used
            - CoSENT
                - On the basis of positive and negative samples, sorting is further introduced based on circle loss
            - SNCSE
                - In order to solve the problem that the model "cannot distinguish between text similarity and semantic similarity, and prefers to have similar texts without considering the actual semantic differences", a scheme combining "explicitly adding negative words to generate soft negative samples" combined with "two-way marginal loss" was proposed.
            - EASE
                - Emphasize the importance of entities in sentence vector representation. At the data level, positive and negative entities are used instead of positive and negative samples.
            - CLAIF
                - In view of the lack of fine-grained supervised signals in the training process, that is, the similarity differences between positive sample pairs are not considered, AI feedback from LLMs is introduced to construct sample pairs with different similarities, and fine-grained similarity scores are given to these sample pairs as supervised signals to help the learning of text representation.
    - Instructor
        - 1. The GTR model is used as the base model, and it is obtained by further "instruction tuning".
        - 2. Change the model input to Task Instuction+[X]([X]代表具体的文本输入)
    - E5
        - E5 proposes a pre-trained data filtering scheme, consistency-based filter
        - An embedding model with Bert as the base
        - Prefix("query:" vs. "paragraph:") has been added to the input side of the model to let the model know the type of text, similar to the instruction of the Instructor
    - BGE
        - Based on the RetroMAE scheme
        - In the finetune phase, BGE needs to add a specific prefix for the retrieval task (only add "Represent this sentence for searching relevant passages:" on the query side)
    - RetroMAE
        - It consists of a Bert-based encoder and a one-layer Decoder
        - The Encoder side masks the original text at a ratio of 30%, and finally obtains [CLS]the vector representation of the last layer as the sentence vector
        - The Decoder side masks the original text at a 50% ratio, and combines the sentence vectors on the Encoder side to reconstruct the original
    - PromptBert
        - Using Bert as a base, by selecting the appropriate prompt("This sentence:"[X]" means [MASK] "), and then using [MASK]the vector representation of the last layer as the sentence vector, the effect can be amazing even without additional finetune
    - PromptEOL+CLS+LLM
        - The language model uses OPT and LLaMA
        - Another new prompt, "This sentence:"[X]" means in one word:", is built to generate the hidden layer state of the token as text embedding
        - In-context learning was also introduced to find an optimal demonstration for each language model, which guided the language model to generate a more compliant text embedding
        - In order to further improve the performance, the contrastive learning method can be used for further finetune
- 10. Contextual extensions
    - Alibi
    - log(n) attention scaling
    - window attention
    - RoPE improvements
        - Interpolation
            - Position Interpolation
            - Linear interpolation
        - Extrapolation
            - NTK-aware scaling RoPE
            - dynamic scale RoPE
            - consistent of Dynamically Scaled RoPE
        - mix
            - Rectified RoPE
    - **N** aive **B** ayes-based **C** ontext **E** xtension
        - You only need to modify the logits construction method in the decoding function
        - Plug-and-play, model-agnostic, no fine-tuning, linear efficiency, simple implementation
        - One of the major drawbacks of NBCE is that it is not able to recognize the input order of the Context, which may not perform well in scenarios such as story renewal
- 11. Prompt Engineering
    - **Chain of Thought**
        - Let’s Think step by step
    - **Self-Consistency**
        - Few-shot + {question} with a few similar examples with derivation steps
    - **Auto-CoT**
        - Few-shot + {question} +Chain of Thought with a similar example of derivation steps + {question} + give a specific thought process.
    - **Generation Knowledge**
        - Organize the examples in a factual + knowledge-based manner, and then ask questions at the end to ask for explanations and answers
    - **Automatic Prompt Engineer**
        - Let's work this out in a step by step way to be sure we have the right answer
    - **OPRO**
        - “Take a deep breath and think step by step.”
        - Optimization by PROmpting (OPRO) overall architecture: Enter meta-prompt at the beginning, this initial meta-prompt is basically just a description of the optimization task (there will also be few-shot examples). Once inputted, the LLM generates a solution that is evaluated and scored by the objective function. (solution, score) and add it to the meta-prompt in pairs, thus completing a loop. After multiple cycles, the solution with the highest score is selected as the optimization result.
        - The meta-prompt is divided into two parts, the problem description and the optimization track, the problem description is to describe the problem you want to optimize in natural language, such as "generate a new instruction that achieves a higher accuracy". Optimization trajectory refers to the previously mentioned (solution, score) pairs, that is, the previously generated solutions and the corresponding scores, which can be regarded as the "log" of optimization. However, it should be noted that this trajectory is not in order, but in ascending order of score. Previous studies have also found that the lower the example, the greater the impact on the output, so ranking the higher scores at the bottom is beneficial for LLMs to learn from them. [Chronological order]("https://so.csdn.net/so/search?q=%E6%97%B6%E9%97%B4%E9%A1%BA%E5%BA%8F&spm=1001.2101.3001.7020")
    - **Tree of Thought**
        - f "Given the current state of reasoning: '{state_text}', generate {k} coherent thoughts to implement the reasoning process:"
        - f"Given the current state of reasoning: '{state_text}', pessimistically evaluate its value as a floating-point number between 0 and 1 based on its potential to achieve {initial_prompt}"
        - Use the tree's traversal algorithm (BFS, DFS, MC, BF, A*) to search for the best answer.
    - **Graph of Thought**
        - The innovation point is to model the information generated by the large model as a graph, the nodes are the "LLM ideas", and the edges are the dependencies of these ideas. This method can combine arbitrary LLM ideas to extract the essence of the network.
        - **Starting point** : When solving problems, the human mind does not only chain thinking or try different chains (TOT), but builds a complex thinking network in the brain. When thinking about human beings, they will follow a chain of reasoning, go back, try a new direction, and retain the advantages of the previous chain, eliminate the disadvantages, and combine it with the direction of the current chain to generate a new solution