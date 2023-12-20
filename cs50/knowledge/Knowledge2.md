# Knowledge 2

## Knowledge engineering

process of figuring out how to represent propositions and logic in AI
example codes at `src/harry.py`, `src/clue.py`, `src/mastermind.py`

## Inference rules

### Structure

<div style="text-align: center;">
<pre>
premise
--- horizontal bar ---
conclusion
</pre>
</div>

- premise: whatever knowledge we have
- conclusion: what knowledge can be generated based on premise

### Modus Ponens
 
<div style="text-align: center;">
<pre>
α → β

α
<span>------</span>
β
</pre>
</div>

### And elimination

<div style="text-align: center;">
<pre>
α ^ β
---------
α
</pre>
</div>

### Double negation elimination

<div style="text-align: center;">
<pre>
￢(￢α)
---------
α
</pre>
</div>

#### example

<div style="text-align: center;">
<pre>
It is not true that today is not sunday.
-------------------------------------------
It is sunday.
</pre>
</div>

### Implication elimination

`if then` to `or`

<div style="text-align: center;">
<pre>
α → β
---------
￢α ∨ β
</pre>
</div>

#### example

<div style="text-align: center;">
<pre>
If it is warm, then sky goes for a walk
-------------------------------------------
It is not warm or sky goes for a walk
</pre>
</div>

### Biconditional elimination

<div style="text-align: center;">
<pre>
α ↔ β
------------------
(α → β) ^ (β → α)
</pre>
</div>

#### example

<div style="text-align: center;">
<pre>
It is raining if and only if Harry is inside.
-------------------------------------------------
If it is raining, then Harry is inside,
and if Harry is inside, then it is raining
</pre>
</div>

### De Morgan's law

<div style="text-align: center;">
<pre>
￢(α ^ β)
------------
￢α ∨ ￢β
</pre>
</div>


<div style="text-align: center;">
<pre>
￢(α ∨ β)
------------
￢α ^ ￢β
</pre>
</div>

#### De Morgan's law at set

```
(A∪B)ⅽ = Aⅽ ∩ Bⅽ
(A∩B)ⅽ = Aⅽ ∪ Bⅽ
```

#### example

<div style="text-align: center;">
<pre>
It is not true that
today is sunday and today is monday.
---------------------------------------
Today is not sunday
or today is not monday.
</pre>
</div>

### Distributive property

<div style="text-align: center;">
<pre>
α ^ (β ∨ γ)
------------
(α ^ β) ∨ (α ^ γ)
</pre>
</div>

<div style="text-align: center;">
<pre>
α ∨ (β ^ γ)
------------
(α ∨ β) ^ (α ∨ γ)
</pre>
</div>

#### Distributive property in set

```
A∪(B∩C) = (A∪B)∩(A∪C)
A∩(B∪C) = (A∩B)∪(A∩C)
```

#### Associative property in set

```
(A∪B)∪C = A∪(B∪C)
(A∩B)∩C = A∩(B∩C)
```

### Theorem priving

view inference as a search problem with these properties;

- initial state: starting knowledge base
- actions: inference rules
- transition model: new knowledge base after inference
- goal test: check statement we're trying to prove
- path cost function: number of steps in proof

## Resolution

inference rule that states that if one of two atomic propositions in an Or proposition if false, the other has to be true

### Generalization

#### Case 1

<div style="text-align: center;">
<pre>
P ∨ Q ∨ Q2 ∨ ... ∨ Qn

￢P
<span>----------------------</span>
Q ∨ Q2 ∨ ... ∨ Qn
</pre>
</div>

#### Case 2

<div style="text-align: center;">
<pre>
P ∨ Q ∨ Q2 ∨ ... ∨ Qn

￢P ∨ R ∨ R2 ∨ ... ∨ Rm
<span>---------------------------------------</span>
Q ∨ Q2 ∨ ... ∨ Qn ∨ R ∨ R2 ∨ ... ∨ Rm
</pre>
</div>

### Clause

a disjunction of literals

- ex) P ∨ Q ∨ R

### Conjunctive normal form (CNF)

logical sentence that is a conjunction of clauses

- ex) (A ∨ B ∨ C) ^ (D ∨ ￢E)

#### Method

only left `^` and `∨`

1. eliminate biconditionals
    - turn `α ↔ β` into `(α → β) ^ (β → α)`

2. eliminate implications
    - turn `α → β` into `￢α ∨ β`

3. move `￢` inwards using De Morgan's laws
    - turn `￢(α ^ β)` into `￢α ∨ ￢β`

4. use distributive law to distribute `∨` wherever possible

#### Factoring

1. duplicate literal is removed
    - ex) resolution of `(P ∨ Q ∨ S) ∧ (¬P ∨ R ∨ S)`, `(Q ∨ S ∨ R ∨ S)` is factored to `(Q ∨ R ∨ S)`

2. equivalent false
    - contradiction will be replaced into the empty clause
    - ex) `¬P ^ P` is factored to `()`

### Inference by resolution

to determine if KB ⊨ α:
- convert `KB ∧ ¬α` to CNF
- keep checking to see if we can use resolution to produce a new clause
  - if produce the empty clause, equivalent to `False`; arrived at a contradiction `KB ⊨ α`
  - if contradiction is not achieved and no more clauses can be inferred, there is no entailment

## First-order logic

- constant symbol: represent objects
- predicated symbol: relations or functions that take an argument and return a true or false value

### Universal quantification

express an idea that is true for all the valuable

- `∀`: for all
- ∀x. Species(x, human) -> ¬Species(x, elephant)

### Existential quantification

some expression is going to be true for at least one value

- `∃`
- ∃x. House(x) ∧ BelongsTo(Minerva, x)

