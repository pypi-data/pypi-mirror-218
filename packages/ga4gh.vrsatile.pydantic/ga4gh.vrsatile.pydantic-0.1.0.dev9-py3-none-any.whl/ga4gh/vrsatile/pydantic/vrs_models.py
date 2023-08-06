"""Define Pydantic Class models for VRS models."""
from enum import Enum
from typing import List, Union, Literal
import re

from pydantic import Field, constr, StrictInt, StrictStr, StrictBool, validator, \
    BaseModel, Extra

from ga4gh.vrsatile.pydantic import return_value, BaseModelForbidExtra
from ga4gh.vrsatile.pydantic.core_models import CURIE, Gene, ValueEntity


class VRSTypes(str, Enum):
    """Define types used in VRS."""

    NUMBER = "Number"
    INDEFINITE_RANGE = "IndefiniteRange"
    DEFINITE_RANGE = "DefiniteRange"
    TEXT = "Text"
    GENE = "Gene"
    CHROMOSOME_LOCATION = "ChromosomeLocation"
    SEQUENCE_LOCATION = "SequenceLocation"
    LITERAL_SEQUENCE_EXPRESSION = "LiteralSequenceExpression"
    DERIVED_SEQUENCE_EXPRESSION = "DerivedSequenceExpression"
    REPEATED_SEQUENCE_EXPRESSION = "RepeatedSequenceExpression"
    COMPOSED_SEQUENCE_EXPRESSION = "ComposedSequenceExpression"
    ALLELE = "Allele"
    HAPLOTYPE = "Haplotype"
    COPY_NUMBER_COUNT = "CopyNumberCount"
    COPY_NUMBER_CHANGE = "CopyNumberChange"
    VARIATION_SET = "VariationSet"
    GENOTYPE = "Genotype"
    GENOTYPE_MEMBER = "GenotypeMember"


class Comparator(str, Enum):
    """A range comparator."""

    LT_OR_EQUAL = "<="
    GT_OR_EQUAL = ">="


class CopyChange(str, Enum):
    """The copy change (https://www.ebi.ac.uk/efo/)"""

    COMPLETE_GENOMIC_LOSS = "efo:0030069"
    HIGH_LEVEL_LOSS = "efo:0020073"
    LOW_LEVEL_LOSS = "efo:0030068"
    LOSS = "efo:0030067"
    REGIONAL_BASE_PLOIDY = "efo:0030064"
    GAIN = "efo:0030070"
    LOW_LEVEL_GAIN = "efo:0030071"
    HIGH_LEVEL_GAIN = "efo:0030072"


# =============================================================================
# BASIC TYPES (STRUCTURES)
# These types do NOT have a VRS `type` attribute
# These types are used solely within other definitions.
# =============================================================================


class HumanCytoband(BaseModelForbidExtra):
    """A character string representing cytobands derived from the *International System
    for Human Cytogenomic Nomenclature* (ISCN)
    [guidelines](http://doi.org/10.1159/isbn.978-3-318-06861-0).
    """

    __root__: constr(regex=r"^cen|[pq](ter|([1-9][0-9]*(\.[1-9][0-9]*)?))$") \
        = Field(..., example="q22.3")  # noqa: F722


class Residue(BaseModelForbidExtra):
    """A character representing a specific residue (i.e., molecular species) or
    groupings of these ("ambiguity codes"), using `one-letter IUPAC abbreviations
    <https://en.wikipedia.org/wiki/International_Union_of_Pure_and_Applied_Chemistry#Amino_acid_and_nucleotide_base_codes>`
    for nucleic acids and amino acids.
    """

    __root__: constr(regex=r"[A-Z*\-]")  # noqa: F722


class Sequence(BaseModelForbidExtra):
    """A character string of :ref:`Residues <Residue>` that represents a biological
    sequence using the conventional sequence order (5'-to-3' for nucleic acid sequences,
    and amino-to-carboxyl for amino acid  sequences). IUPAC ambiguity codes are
    permitted in Sequences.
    """

    __root__: constr(regex=r"^[A-Z*\-]*$") = Field(..., example="ACTG")  # noqa: F722


# =============================================================================
# Numerics, Comparators, and Ranges
# =============================================================================


class Number(BaseModelForbidExtra):
    """A simple number value as a VRS class."""

    type: Literal[VRSTypes.NUMBER] = VRSTypes.NUMBER
    value: StrictInt


class IndefiniteRange(BaseModelForbidExtra):
    """An indefinite range represented as a number and associated comparator.
    The bound operator is interpreted as follows: `>=` are all values greater
    than and including the value, `<=` are all numbers less than and including
    the value.
    """

    type: Literal[VRSTypes.INDEFINITE_RANGE] = VRSTypes.INDEFINITE_RANGE
    value: StrictInt
    comparator: Comparator


class DefiniteRange(BaseModelForbidExtra):
    """A bounded, inclusive range of numbers."""

    type: Literal[VRSTypes.DEFINITE_RANGE] = VRSTypes.DEFINITE_RANGE
    min: StrictInt
    max: StrictInt

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Locations


class ChromosomeLocation(ValueEntity):
    """A Location on a chromosome defined by a species and chromosome name."""

    type: Literal[VRSTypes.CHROMOSOME_LOCATION] = VRSTypes.CHROMOSOME_LOCATION
    species_id: CURIE
    chr: StrictStr
    start: HumanCytoband
    end: HumanCytoband

    _get_start_val = validator("start", allow_reuse=True)(return_value)
    _get_end_val = validator("end", allow_reuse=True)(return_value)
    _get_species_id_val = validator("species_id", allow_reuse=True)(return_value)

    @validator("chr")
    def check_chr_value(cls, v):
        """Check chr value"""
        msg = "`chr` must be 1..22, X, or Y (case-sensitive)"
        assert re.match(r"^(X|Y|([1-9]|1[0-9]|2[0-2]))$", v), msg
        return v

    class Config:
        """Class configs."""

        extra = Extra.forbid


class SequenceLocation(ValueEntity):
    """A :ref:`Location` defined by an interval on a referenced :ref:`Sequence`."""

    type: Literal[VRSTypes.SEQUENCE_LOCATION] = VRSTypes.SEQUENCE_LOCATION
    sequence_id: CURIE
    start: Union[Number, IndefiniteRange, DefiniteRange]
    end: Union[Number, IndefiniteRange, DefiniteRange]

    _get_sequence_id_val = validator('sequence_id', allow_reuse=True)(return_value)

    class Config:
        """Class configs."""

        extra = Extra.forbid


class Location(BaseModel):
    """A contiguous segment of a biological sequence."""

    __root__: Union[ChromosomeLocation, SequenceLocation]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SequenceExpression

class LiteralSequenceExpression(BaseModelForbidExtra):
    """An explicit expression of a Sequence."""

    type: Literal[VRSTypes.LITERAL_SEQUENCE_EXPRESSION] = \
        VRSTypes.LITERAL_SEQUENCE_EXPRESSION
    sequence: Sequence

    _get_sequence_val = validator('sequence', allow_reuse=True)(return_value)


class DerivedSequenceExpression(BaseModelForbidExtra):
    """An approximate expression of a sequence that is derived from a referenced
    sequence location. Use of this class indicates that the derived sequence is
    *approximately equivalent* to the reference indicated, and is typically used for
    describing large regions in contexts where the use of an approximate sequence is
    inconsequential.
    """

    type: Literal[VRSTypes.DERIVED_SEQUENCE_EXPRESSION] = \
        VRSTypes.DERIVED_SEQUENCE_EXPRESSION
    location: SequenceLocation
    reverse_complement: StrictBool


class RepeatedSequenceExpression(BaseModelForbidExtra):
    """An expression of a sequence comprised of a tandem repeating
    subsequence.
    """

    type: Literal[VRSTypes.REPEATED_SEQUENCE_EXPRESSION] = \
        VRSTypes.REPEATED_SEQUENCE_EXPRESSION
    seq_expr: Union[LiteralSequenceExpression, DerivedSequenceExpression]
    count: Union[Number, IndefiniteRange, DefiniteRange]

    @validator("count")
    def check_count_value(cls, v):
        """Check count value"""
        if v.type in {VRSTypes.NUMBER, VRSTypes.INDEFINITE_RANGE}:
            assert v.value >= 0, "`count.value` minimum is 0"
        elif v.type == VRSTypes.DEFINITE_RANGE:
            assert v.min >= 0 and v.max >= 0, "`count.min` and `count.max` minimum is 0"  # noqa: E501
        return v


class ComposedSequenceExpression(BaseModelForbidExtra):
    """An expression of a sequence composed from multiple other
    :ref:`Sequence Expressions<SequenceExpression>` objects. MUST have at least one
    component that is not a ref:`LiteralSequenceExpression`. CANNOT be composed from
    nested composed sequence expressions.
    """

    type: Literal[VRSTypes.COMPOSED_SEQUENCE_EXPRESSION] = \
        VRSTypes.COMPOSED_SEQUENCE_EXPRESSION
    components: List[Union[LiteralSequenceExpression, RepeatedSequenceExpression,
                     DerivedSequenceExpression]] = Field(..., min_items=2, unique_items=True)  # noqa: E501


class SequenceExpression(BaseModel):
    """One of a set of sequence representation syntaxes."""

    __root__: Union[LiteralSequenceExpression, DerivedSequenceExpression,
                    RepeatedSequenceExpression, ComposedSequenceExpression]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Molecular Variation


class Allele(ValueEntity):
    """The state of a molecule at a :ref:`Location`."""

    type: Literal[VRSTypes.ALLELE] = VRSTypes.ALLELE
    location: Union[CURIE, Location]
    state: SequenceExpression

    _get_loc_val = validator('location', allow_reuse=True)(return_value)
    _get_state_val = validator('state', allow_reuse=True)(return_value)

    class Config:
        """Class configs."""

        extra = Extra.forbid


class Haplotype(ValueEntity):
    """A set of non-overlapping :ref:`Allele` members that co-occur on the same
    molecule.
    """

    type: Literal[VRSTypes.HAPLOTYPE] = VRSTypes.HAPLOTYPE
    members: List[Union[Allele, CURIE]] = Field(..., min_items=2, unique_items=True)

    class Config:
        """Class configs."""

        extra = Extra.forbid


class MolecularVariation(BaseModel):
    """A :ref:`variation` on a contiguous molecule."""

    __root__: Union[Allele, Haplotype]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SystemicVariation


class CopyNumberBaseModel(ValueEntity):
    """Base model for Copy Number"""

    subject: Union[CURIE, Location, Gene]
    get_subject_val = validator('subject', allow_reuse=True)(return_value)


class CopyNumberCount(CopyNumberBaseModel):
    """The absolute count of discrete copies of a Location or Gene, within a system
    (e.g. genome, cell, etc.).
    """

    type: Literal[VRSTypes.COPY_NUMBER_COUNT] = VRSTypes.COPY_NUMBER_COUNT
    copies: Union[DefiniteRange, IndefiniteRange, Number]

    class Config:
        """Class configs."""

        extra = Extra.forbid


class CopyNumberChange(CopyNumberBaseModel):
    """An assessment of the copy number of a Location or a Gene within a system
    (e.g. genome, cell, etc.) relative to a baseline ploidy.
    """

    type: Literal[VRSTypes.COPY_NUMBER_CHANGE] = VRSTypes.COPY_NUMBER_CHANGE
    copy_change: CopyChange

    class Config:
        """Class configs."""

        extra = Extra.forbid


class CopyNumber(BaseModel):
    """A measure of the copies of a :ref:`Location` within a system (e.g. a genome)"""

    __root__: Union[CopyNumberCount, CopyNumberChange]


class GenotypeMember(BaseModelForbidExtra):
    """A class describing a :ref:`Genotype` `member`."""

    type: Literal[VRSTypes.GENOTYPE_MEMBER] = VRSTypes.GENOTYPE_MEMBER
    count: Union[Number, IndefiniteRange, DefiniteRange]
    variation: Union[Allele, Haplotype]

    class Config:
        """Class configs."""

        extra = Extra.forbid


class Genotype(ValueEntity):
    """A set of trans-phased :ref:`MolecularVariation` members, with associated
    copy counts, across a specified number of genomic locus `copies`.
    """

    type: Literal[VRSTypes.GENOTYPE] = VRSTypes.GENOTYPE
    members: List[GenotypeMember] = Field(..., min_items=1, unique_items=True)
    count: Union[Number, IndefiniteRange, DefiniteRange]

    class Config:
        """Class configs."""

        extra = Extra.forbid


class SystemicVariation(BaseModel):
    """A Variation of multiple molecules in the context of a system,
    e.g. a genome, sample, or homologous chromosomes.
    """

    __root__: Union[CopyNumberCount, CopyNumberChange, Genotype]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# UtilityVariation


class Text(ValueEntity):
    """An textual representation of variation intended to capture variation
    descriptions that cannot be parsed, but still treated as variation.
    """

    type: Literal[VRSTypes.TEXT] = VRSTypes.TEXT
    definition: StrictStr

    class Config:
        """Class configs."""

        extra = Extra.forbid


class VariationSet(ValueEntity):
    """An unconstrained set of Variation members."""

    type: Literal[VRSTypes.VARIATION_SET] = VRSTypes.VARIATION_SET
    # TODO: See if we can get Variation to work as the union
    members: List[Union[CURIE, MolecularVariation, SystemicVariation,
                        Text]] = Field(..., unique_items=True)

    _get_members_val = validator('members', allow_reuse=True)(return_value)

    class Config:
        """Class configs."""

        extra = Extra.forbid


class UtilityVariation(BaseModel):
    """A collection of :ref:`Variation` subclasses that cannot be constrained to a
    specific class of biological variation, but are necessary for some applications of
    VRS.
    """

    __root__: Union[Text, VariationSet]


# =============================================================================
# Kinds of Variation
# =============================================================================


class Variation(BaseModel):
    """A representation of the state of one or more biomolecules."""

    __root__: Union[MolecularVariation, SystemicVariation, UtilityVariation]
