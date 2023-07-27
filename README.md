# Technical Debt Management

## Q&A

**1. Why is the problem relevant?**

In the beginning of each sprint of an agile software development process, the organization needs to select the tasks (new features in different epics and technical debt pay back) that can be implementable by the available resources to maximize the beneﬁt. 



**2. Who will benefit from addressing the problem?**

Product Owner, Project Manager, Developer ...



**3. What is the contribution of the proposed solution?**

The solution proposes a recommendation of selected tasks from backlog within the limit of implementation cost and maximize the short term value and future investment value.



**4. What was the plan to address the problem?**

Use search based algorithm, Ant Colony Optimization.



**5. What are the results and conclusions?**

The solution reached both high short term value and future investment value. At the same time, it considers the relevance of different features (the features in one epic will be relevant) to improve the integrity the implementing epics.

The proposed algorithm ACO can achieve high performance as the GA approach in the cited article[^1], but with reduced entropy of results, ie. the tasks selected are more relevant.



## Formulation of the problem

### Implementation Cost

$$
I C(S)=\sum_{i \in F S} c_{i}+\sum_{j \in T D} p_{j}+\sum_{i \in F S} \sum_{k \notin T D} x c_{i k}
$$


&nbsp;&nbsp;&nbsp;&nbsp;*​$S$: Current Sprint*

​&nbsp;&nbsp;&nbsp;&nbsp;*$FS$: Selected Features*

​&nbsp;&nbsp;&nbsp;&nbsp;*$TD$: Selected Technical Debt*

&nbsp;&nbsp;&nbsp;&nbsp;*$​c_i$: Feature cost*

​&nbsp;&nbsp;&nbsp;&nbsp;*$p_j$: Technical Debt pay back cost*

&nbsp;&nbsp;&nbsp;&nbsp;*$​xc_{ik}$: extra cost of Feature $i$ blocked by not selected Debt $k$*




### Short Term Value

$$
S T V(S)=\sum_{i \in F S} v_{i}
$$

​&nbsp;&nbsp;&nbsp;&nbsp;*$v_i$: bussiness value of Feature $i$*



### Future Investment Value

$$
F I V(S)=\sum_{j \in T D} f c_{j}+\sum_{i \notin F S} \sum_{j \in T D} x c_{i j}
$$

​&nbsp;&nbsp;&nbsp;&nbsp;*$fc_i$: future cost of Debt. If the feature is selected, these is no future cost*



## GA Approach

### Problem representation

```
[ 0 1 0 1 0 0 1 0 0 1 ... ]
```

### Implementation Cost Control

If $IC$ > $MAX\_IC$, set one gene 1 to 0



### Limitation

- Assumes every task is independent, ignores the relation of different tasks

```
| Epic 1
​   \ Feature 1
   \ Feature 2
   \ Feature 3
   \ Debt 1
| Epic 2
   ...
| Epic 3
   ...
```

- A lot of unmeaningful individuals kept in the population

    Desired: [ 0 1 0 1 0 0 1 0 0 1 ]

    Cases:    [ 0 0 0 1 0 0 0 0 0 0 ]    low fitness

  ​                [ 1 1 1 1 1 0 1 1 1 1 ]   high fitness, beyond ic limit



## ACO Approach

### Problem representation

```
5
5 -> 3
​5 -> 3 -> 7 ...
```


### Probability[^2]


$$
p_{x y}^{k}=\frac{\left(\tau_{x y}^{\alpha}\right)\left(\eta_{x y}^{\beta}\right)}{\sum_{z \in \operatorname{allowed}_{x}}\left(\tau_{x z}^{\alpha}\right)\left(\eta_{x z}^{\beta}\right)}
$$

*Ant from x to y*
​

&nbsp;&nbsp;&nbsp;&nbsp;*$tau_{xy}$: the amount of pheromone from $x$ to $y$*


&nbsp;&nbsp;&nbsp;&nbsp;*$\eta_{xy}$: the desirability of state transition, priori knowledge*

​		If $x$ and $y4 are related, eta can be higher

### Implementation Cost Control

  5 -> 3 -> 7 ... stops when $IC$ > $MAX\_IC$



## Evaluation

### Entropy[^3]

Entropy is a measure of the randomness or disorder in a 

$$
\mathrm{H}(X)=-\sum_{x \in \mathcal{X}} p(x) \log _{b} p(x)
$$

​		Box 1:  0 0        1 1        1 0

​		Box 2:  0 0        0 0        1 0

​		Entropy:		    1/6       4/6



### Validatation Data

​		SEM Incident Response Project


### Comparison

|     | Random | GA                                    | ACO  |
|-----| ------ | ------------------------------------- | ---- |
| STV | 238 | 252 | 257 |
| FIV | 22.7 | 34.9 | 31.2 |
| FITNESS | 260.7 | 286.9 | 288.2 |
| ENTROPY | 4.80e-08 | 3.49e-08 | 1.01e-09 |



### Reference

[^1]: S. H. Vathsavayi and K. Systä, "Technical Debt Management with Genetic Algorithms," 2016 42th Euromicro Conference on Software Engineering and Advanced Applications (SEAA), Limassol, Cyprus, 2016, pp. 50-53, doi: 10.1109/SEAA.2016.43. https://ieeexplore.ieee.org/document/

[^2]: https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms

[^3]: https://en.wikipedia.org/wiki/Entropy_(information_theory)
