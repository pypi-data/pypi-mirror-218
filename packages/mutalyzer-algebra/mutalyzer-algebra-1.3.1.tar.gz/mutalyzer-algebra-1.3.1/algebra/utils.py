"""Utility functions for sequences and variants."""


from collections import deque
import random
from . import Variant
from .variants import DNA_NUCLEOTIDES


def fasta_sequence(lines):
    """Create a single sequence from (FASTA) lines."""
    return "".join([line.strip() if not line.startswith(">") else "" for line in lines])


def vcf_variant(line):
    """Create a variant from a (simple) VCF line."""
    _, position, _, deleted, inserted, *_ = line.split()
    start = int(position) - 1
    return Variant(start, start + len(deleted), inserted)


def to_dot(reference, root):
    """The LCS graph in Graphviz DOT format."""
    def traverse():
        # breadth-first traversal
        node_count = 0
        visited = {root: node_count}
        queue = deque([root])
        while queue:
            node = queue.popleft()

            if not node.edges:
                yield f'"s{visited[node]}"' + "[shape=doublecircle]"

            for succ, variant in node.edges:
                if succ not in visited:
                    node_count += 1
                    visited[succ] = node_count
                    queue.append(succ)
                yield (
                    f'"s{visited[node]}" -> "s{visited[succ]}"'
                    f' [label="{variant.to_hgvs(reference)}"];'
                )

    return (
        "digraph {\n"
        "    rankdir=LR\n"
        "    edge[fontname=monospace]\n"
        "    node[shape=circle]\n"
        "    si[shape=point]\n"
        "    si->" + f'"s{0}"' + "\n"
        "    " + "\n    ".join(traverse()) + "\n}"
    )


def random_sequence(max_length, min_length=0, alphabet=DNA_NUCLEOTIDES, weights=None):
    """Create a random sequence.

    Parameters
    ----------
    max_length : int
        The maximal length of the sequence.
    min_length : int, optional
        The minimal length of the sequence (default: 0).

    Other Parameters
    ----------------
    alphabet : str or iterable, optional
        The symbols in the alphabet (default: `"ACGT"`).
    weights : list or None, optional
        A list of weights giving the relative frequency of the symbols.

    Returns:
        A random sequence.
    """

    return "".join(random.choices(alphabet, weights=weights, k=random.randint(min_length, max_length)))


def random_variants(reference, p=None, mu_deletion=1, mu_insertion=1):
    """Create a random list of non-overlapping variants (allele).

    Parameters
    ----------
    reference : str
        The reference sequence.
    p : float, optional
        The change per symbol of a variant (default: `1 / len(reference`).

    Other Parameters
    ----------------
    mu_deletion : float, optional
        The exponential mean length of a deletion (default: 1). Should be
        non-zero.
    mu_insertion : float, optional
        The exponential mean length of an insertion (default: 1). Should
        be non-zero.

    Returns
    -------
    list
        A sorted list of variants.
    """

    if p is None:
        p = 1 / len(reference)

    pos = 0
    while pos < len(reference):
        len_del = 0
        if random.random() <= p:
            len_del = int(random.expovariate(1 / mu_deletion))
            if pos + len_del > len(reference):
                len_del = len(reference) - pos
            len_ins = int(random.expovariate(1 / mu_insertion))

            if len_del == len_ins == 0:
                len_del = 1
                len_ins = 1

            del_seq = reference[pos:pos + len_del]
            ins_seq = ""

            if len_ins > 0:
                ins_seq = "".join(random.choice(DNA_NUCLEOTIDES.replace(ch, "")) for ch in del_seq)
                if len_ins > len(ins_seq):
                    ins_seq += "".join(random.choices(DNA_NUCLEOTIDES, k=len_ins - len(ins_seq)))

            yield Variant(pos, pos + len_del, ins_seq)

        pos += len_del + 1
