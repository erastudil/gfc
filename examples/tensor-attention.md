# Who looks at whom

A sentence is a line of words. Some of those words only make sense once they have seen the others. In "the bank by the river" the word *bank* needs *river*. In "the bank that holds deposits" the same spelling needs *deposits*. A model has to do that looking, for every word, over the whole line, in one shot.

Each word is already a list of numbers. Say the list has length `d`. A line of `n` words is then a grid: `n` rows, `d` columns. One row per word. One column per feature.

From that grid you make three grids of the same shape, by multiplying with three different learned tables. The three copies have three jobs:

1. what this word is looking for
2. what this word offers, if someone looks
3. what this word will add, if it is chosen

Those three jobs are the machine. The rest is arithmetic.

## Scores, then a mix

Pick word `i`. Take its looking-for row and measure how aligned it is with every word's to-be-found row. Alignment here means a dot product: multiply matching columns, add them up. You get `n` scores for word `i`. Do that for every `i` and you have an `n` by `n` grid of scores. Cell `(i, j)` is how much word `i` wants word `j`.

Raw scores grow with `d`. Add up `d` messy terms and the typical size walks like the square root of `d`. Leave them large and the next step collapses: one neighbor takes almost all of the mass, everyone else takes none, and the training signal dies. Divide every score by `sqrt(d)` first. The mix stays soft enough to learn.

Turn each row of scores into a row that adds to 1, every entry zero or more. The function that does that is softmax. Now cell `(i, j)` is a share.

For word `i`, blend the contribute-rows using those shares. The result is a new row for `i`: a mix of what the other words added, weighted by how much `i` wanted them. Do that for every word. The output is a grid the same shape as the input. The next layer can eat it.

If word `i` must not see the future, zero the scores for `j > i` before the mix. That is the causal mask. It is a restriction on who is allowed to be found, not a different machine.

## Extra axes

People stack many lines into a batch. They also split the `d` features into several independent groups so each group can look for a different kind of match. The grids pick up extra axes: which line in the batch, which group, which word, which feature.

A number grid with more than two axes is a tensor. The same mix is then two contractions of those tensors. One contraction builds the scores. One contraction blends the contributions.

In named-axis form, with `b` for batch, `h` for group, `i` and `j` for words, `d` for feature:

```
score[b, h, i, j]  = sum_d  look[b, h, i, d] * found[b, h, j, d] / sqrt(d)
share[b, h, i, j]  = softmax_over_j(score)
out[b, h, i, d]    = sum_j  share[b, h, i, j] * add[b, h, j, d]
```

You can flatten axes until this is two matrix multiplies. You can leave the axes named and write the same sums as `einsum`. The arithmetic does not change. The named form is what engineers mean by tensor attention: attention kept as contractions on the full object, not as a story about matrices that you reshape until the story fits `matmul`.

The score object, with its extra axes, is the attention tensor. It is `batch × groups × n × n`. Most of the memory, most of the FLOPs, and most of the "why is this slow" live in that cube.

Once you can see the three jobs, the usual one-liner is just names for them:

```
softmax(Q K^T / sqrt(d)) V
```

`Q` is looking-for. `K` is to-be-found. `V` is contribute. The transpose on `K` turns found-rows into columns so the dot products happen in one multiply.

## Several groups at once

Split `Q`, `K`, and `V` along the feature axis, run the same mix in each group, then concatenate the groups back into one row of length `d`. The groups do not share their scores. They share the need to look. That split is multi-head attention. The `h` axis above is the groups.

Because each new word only needs its own looking-for row, you can keep the found and contribute grids from earlier words and reuse them. That saved pair is the KV cache. It follows from the three jobs. It is not a separate invention.

Papers that factor the three grids, or contract over layout axes as well as word axes, are still this mix with extra indices. The names change. The jobs do not.

Written to the Greene Feynman Clarity standard. Check it:

```
gfc lint examples/tensor-attention.md --mode educate
```
