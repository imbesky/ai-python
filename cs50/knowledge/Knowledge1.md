# Knowledge 1

## Terms and Definitions

### knowledge-based agents

agents that reason by operating on internal representations of knowledge

- can do logical reasoning based on the information already know

### sentence

an assertion about the world in a knowledge representation language

- how AI stores knowledge and uses it to infer new information

## Propositional logic

based on propositions, statement of the world and can be either true or false

- `proposition`: statements about the world that can be either true or false

### Propositional symbols

symbols like *P* *Q* *R* 

- represents proposition; sentence or fact about the world each

### Logical connectives

logical symbols that connect propositional symbols 

- reason in a more complex way about the world

#### ￢ not : 부정

| *P*   | ￢*P*  |
|-------|-------|
| true  | false |
| false | true  |

#### ^ and : are both operands true?

| *P*   | *Q*   | *P* ^ *Q* |
|-------|-------|-----------|
| false | false | false     |
| false | true  | false     |
| true  | false | false     |
| true  | true  | true      |

#### ∨ or : at least one of the operand is true?

| *P*   | *Q*   | *P* ∨ *Q* |
|-------|-------|-----------|
| false | false | false     |
| false | true  | true      |
| true  | false | true      |
| true  | true  | true      |

1. inclusive or
    - true if any of *P*, *Q*, or *P ∧ Q* is true
    - in case of `∨`, the intention is an inclusive Or

2. exclusive or
    - ⊕ `XOR`
    - requires only one of its arguments to be true and not both
    - if *P ∧ Q* is true, then *P ∨ Q* is false

#### →, ⇒ implication : if, then

*`P → Q`*

- *P* implies *Q*
- if *P* then *Q*

| *P*   | *Q*   | *P* → *Q* |
|-------|-------|-----------|
| true  | true  | true      |
| true  | false | false     |
| false | true  | true      |
| false | false | true      |

- *P* is a hypothesis; premise and `antecedent`
- *Q* is conclusion; `consequent`

- when `antecedent` is true, the whole implication is true in the case that the `consequent` is true
- when `antecedent` is true, the implication is false if the `consequent` is false
- when `antecedent` is false, the implication is always true, regardless of the `consequent`
  - logically, we can’t learn anything from an implication *P → Q* if the antecedent *P* is false
- when the `antecedent` is false, we say that the implication is trivially true

#### ↔ biconditional: if and only if

| *P*   | *Q*   | *P* ↔ *Q* |
|-------|-------|-----------|
| false | false | true      |
| false | true  | false     |
| true  | false | false     |
| true  | true  | true      |

- same as *P → Q* ^ *Q → P*

### model

assignment of a truth value to every proposition

- a possible world
- provides information, knowledge about the world

### knowledge base

a set of sentences known by a knowledge-based agents

- AI drives conclusion from provided information, knowledge base

### ⊨ entailment

`α ⊨ β`

- α entails β
- any world where α is true, β is true

## Inference

the process of deriving new sentences from old ones

- its ultimate goal is to know whether *`KB(knowledge base) ⊨ α`* is true or false

### Model checking

one of the algorithm to determine if  *`KB ⊨ α`*

- enumerate all possible models
- if in every model where *KB* is true, α is true, then *`KB entails α`*
- otherwise, *`KB does not entails α`*

#### example

`α` = P^￢Q -> R

- only when P, ￢Q, R is true, `α` is true
- this is the only way to say *`KB entails α`*
