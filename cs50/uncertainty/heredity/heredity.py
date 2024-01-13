import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    """
    joint = dict()
    inherit = {
        0: 0,
        1: 0.5,
        2: 1
    }

    def inheritance(mother, father): # 부모에게서 n개의 gene이 유전되었을 확률
        result = dict()
        mother_chance = 0
        father_chance = 0
        for i in range(3):
            mother_chance += mother[i] * (inherit[i] * (1 - PROBS["mutation"]) + (1 - inherit[i]) * PROBS["mutation"])
            father_chance += father[i] * (inherit[i] * (1 - PROBS["mutation"]) + (1 - inherit[i]) * PROBS["mutation"])
        result[0] = (1 - mother_chance) * (1 - father_chance)
        result[1] = mother_chance * (1 - father_chance) + (1 - mother_chance) * father_chance
        result[2] = mother_chance * father_chance
        return result

    def gene_number(target): # gene이 n 개일 확률
        # TODO: 우선순위 고려
        """
        부모 양쪽의 trait
        자신의 trait
        어느 쪽이 먼저?
        """
        gene_prob = dict()
        mother_trait = people[target["mother"]]["trait"] if target["mother"] in people else None
        father_trait = people[target["father"]]["trait"] if target["father"] in people else None
        if target["trait"] is not None:  # 자신의 trait을 알 때
            this_trait = target["trait"]
            total = PROBS["trait"][0][this_trait] + PROBS["trait"][1][this_trait] + PROBS["trait"][2][this_trait]
            for i in range(3):
                gene_prob[i] = PROBS["trait"][i][this_trait] / total
        elif mother_trait is not None and father_trait is not None:
            inherited = inheritance(gene_number(people[target["mother"]]), gene_number(people[target["father"]]))
            for i in range(3):
                gene_prob[i] = inherited[i]
        elif mother_trait is not None or father_trait is not None:
            known = people[target["mother"]] if mother_trait is not None else people[target["father"]]
            inherited = inheritance(gene_number(known), PROBS["gene"])
            for i in range(3):
                gene_prob[i] = inherited[i]
        else:  # 아는 정보가 없을 때
            for i in range(3):
                gene_prob[i] = PROBS["gene"][i]
        return gene_prob

    def trait_assumption(gene, target_trait):
        result = 0
        """
        trait 이 t일 확률= ["target"][n][t] / gene_prob[n] 의 합(n = 0~2)
        """
        for i in range(3):
            result += PROBS["trait"][i][target_trait] / gene[i]
        return result

    for person in people:
        joint[person] = {}
        # 1. 예상되는 gene의 각 확률 구함
        genes = gene_number(people[person])

        if person in one_gene:
            joint[person]["gene"] = genes[1]
        elif person in two_genes:
            joint[person]["gene"] = genes[2]
        else:
            joint[person]["gene"] = genes[0]

        trait = people[person]["trait"]
        if person in have_trait:
            if trait is None:
                joint[person]["trait"] = trait_assumption(genes, True)
            elif trait:
                joint[person]["trait"] = 1
            else:
                joint[person]["trait"] = 0
        else:
            if trait is None:
                joint[person]["trait"] = trait_assumption(genes, False)
            elif trait:
                joint[person]["trait"] = 0
            else:
                joint[person]["trait"] = 1

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] = p[person]["gene"]
        elif person in two_genes:
            probabilities[person]["gene"][2] = p[person]["gene"]
        else:
            probabilities[person]["gene"][0] = p[person]["gene"]

        if person in have_trait:
            probabilities[person]["trait"][True] = p[person]["trait"]
        else:
            probabilities[person]["trait"][False] = p[person]["trait"]


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        if total != 1:
            for i in range(3):
                probabilities[person]["gene"][i] /= total
        total = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        if total != 1:
            probabilities[person]["trait"][True] /= total
            probabilities[person]["trait"][False] /= total


if __name__ == "__main__":
    main()
