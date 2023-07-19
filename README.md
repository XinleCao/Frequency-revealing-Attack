# Frequency-revealing attacks against frequency-hiding Order-preserving encryption

The full version paper is to be published in eprint and a shorter version is to be published in VLDB 2023.

Xinle Cao, Jian Liu, Yongsheng Shen, Xiaohua Ye and Kui Ren.

## Abstract

Order-preserving encryption (OPE) allows efficient comparison operations over encrypted data and thus is popular in encrypted databases. However, most existing OPE schemes are vulnerable to inference attacks as they leak plaintext frequency. To this end, some frequency-hiding order-preserving encryption (FH-OPE) schemes are proposed and claim to prevent the leakage of frequency. FH-OPE schemes are considered an important step towards mitigating inference attacks.

Unfortunately, there are still vulnerabilities in all existing FH-OPE schemes. In this work, we revisit the security of all existing FH-OPE schemes. We are the first to demonstrate that plaintext frequency hidden by them is recoverable. We present three ciphertext-only attacks named frequency-revealing attacks to recover plaintext frequency. We evaluate our attacks in three real-world datasets. They recover over 90% of plaintext frequency hidden by any existing FH-OPE scheme. With frequency revealed, we also show the potentiality to apply inference attacks on existing FH-OPE schemes.

Our findings highlight the limitations of current FH-OPE schemes. We demonstrate that achieving frequency-hiding requires addressing the leakages of both non-uniform ciphertext distribution and insertion orders of ciphertexts, even though the leakage of insertion orders is often ignored in OPE.

## Note
I am pretty sure that the codes in this repository are sufficient for reproducing our results in the paper. The names of folders and files are clear and easy to understand.

The results may be a little different as the encryption algorithms are randomized. We do not save the random seeds in our experiments. However, we are sure that the results will follow our claims in the paper even if the random seeds are picked differently, which should be guaranteed by a published paper.

Besides, if you have any problem, please contact me or present an issue. I am willing to give help on any problem about this paper. Also, I am open to any problem about OPE and other techniques in Encrypted databases including Oblivious RAM (ORAM). I will give an answer as much as possible.

Here are my gmail and homepage.

- gmail: xinlecao72@gmail.com
- Homepage: https://xinlecao.github.io/

## Packages

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [Scipy](https://scipy.org/install/)

## Code optimiztations.

Here we introduce the optimaztions in our codes in the Fisher exact test attack to reduce the number of Fisher exact testa attack. These optimizations greatly accelerate this attack as Fisher exact test is an expensive statistical test.

First, recall in POPE we get three ordered ciphertexts $\{c_1,c_2,c_3\}$ and observes $\mu$ samples inserted between the three ciphertexts, i.e., $\{(Y_1,n_1),...,(Y_{\mu},n_{\mu}\})$. Sample $(Y_i,n_i)$ means that there are total $n_i$ ciphertexts inserted between $c_1$ and $c_3$ and $Y_i$ of them are smaller than ciphertext $c_2$.

Second, we want to conduct attack by testing if these samples are under binomial distribution which have the same success probability. Suppose $$Y_i \sim \mathsf{Bin}(n_i,p_i)$$ where $\mathsf{Bin}$ is the binomial distribution and $p_i$ is the success probability.

In the best case, we should calculate this probability exactly, which is very expensive and complex. Instead, we approximate this probability by using Fisher exact test for any two distinct samples and adopt the minimal probability, i.e., $$pro = \min \{\mathop{\mathsf{Fisher}}\limits_{\forall j_1,j_2\in [\mu]}(Y_{j_1},n^{(j_1)},Y_{j_2},n^{(j_2)})\}.$$

For further optimizations, we found there are some pairs which can be free from the Fisher exact test. For example, when there are three samples $\{(100,500),(200,500),(400,500\}$. Then it is clear that the minimal probability is calculated with the pair of $(100,500)$ and $(400,500)$. **We do not need conduct the test on other pairs**. Therefore, we use some simple calculation to filter out these pairs. Roughly speaking, we find the samples which have the minimal and maximal ratios of ciphertexts smaller than $c_2$. Then we only conduct the Fisher exact test on these two samples. In this way, when there are more ciphertexts inserted and we get more samples, we only need some incremental works to filter out samples. The number of Fisher exact test conducted does not change. The time usage of these incremental works scales linear with dataset size but is very small. That's why the linear relation is not very clear in the time usage figure in our paper.

We note the optimizations make the probability calculated cannot be exactly equal to that of these samples following binomial distribution with the same success probability. But it is sufficient for us to correctly distinguish the two cases below w.h.p. 
1) these samples following binomial distributions with the same success probability;
2) these samples following binomial distributions with the distinct probabilities;



