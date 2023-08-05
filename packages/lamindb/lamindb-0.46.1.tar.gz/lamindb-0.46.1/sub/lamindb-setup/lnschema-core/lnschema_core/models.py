import builtins
from typing import (  # noqa
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    NamedTuple,
    Optional,
    Union,
    overload,
)

from django.db import models
from django.db.models import PROTECT, CharField, Manager, TextField

from lnschema_core.types import ListLike, StrField

from ._queryset import QuerySet
from .ids import base62_8, base62_12, base62_20
from .types import TransformType
from .users import current_user_id

if TYPE_CHECKING:
    import pandas as pd

is_run_from_ipython = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if is_run_from_ipython else TransformType.pipeline


class ORM(models.Model):
    """LaminDB's base ORM.

    Is based on `django.db.models.Model`.
    """

    def add_synonym(self, synonym: Union[str, ListLike], force: bool = False):
        """Add synonyms to a record."""
        pass

    def remove_synonym(self, synonym: Union[str, ListLike]):
        """Remove synonyms from a record."""
        pass

    @classmethod
    def from_values(cls, identifiers: ListLike, field: StrField, **kwargs):
        """Parse values for an identifier (a name, an id, etc.) and create records.

        This method helps avoid problems around duplication of entries,
        violation of idempotency, and performance when creating records in bulk.

        Guide: :doc:`/biology/registries`.

        Args:
            identifiers: `ListLike` A list of values for an identifier, e.g.
                `["name1", "name2"]`.
            field: `StrField` If `iterable` is `ListLike`, an `ORM` field to look
                up, e.g. `lb.CellMarker.name`.
            **kwargs: Can contain `species`. Either `"human"`, `"mouse"`, or any other
                `name` of `Bionty.Species`. If `None`, will use default species in
                bionty for each entity.

        Returns:
            A list of records.

        For every `value` in an iterable of identifiers and a given `ORM.field`,
        this function performs:

        1. It checks whether the value already exists in the database
        (`ORM.select(field=value)`). If so, it adds the queried record to
        the returned list and skips step 2. Otherwise, proceed with 2.
        2. If the `ORM` is from `lnschema_bionty`, it checks whether there is an
        exact match in the underlying ontology (`Bionty.inspect(value, field)`).
        If so, it creates a record from Bionty and adds it to the returned list.
        Otherwise, it creates a record that populates a single field using `value`
        and adds the record to the returned list.
        """
        pass

    @classmethod
    def inspect(
        cls,
        identifiers: ListLike,
        field: StrField,
        *,
        case_sensitive: bool = False,
        inspect_synonyms: bool = True,
        return_df: bool = False,
        logging: bool = True,
        **kwargs,
    ) -> Union["pd.DataFrame", Dict[str, List[str]]]:
        """Inspect if a list of identifiers are mappable to existing values of a field.

        Args:
            identifiers: `ListLike` Identifiers that will be checked against the
                field.
            field: `StrField` The field of identifiers.
                    Examples are 'ontology_id' to map against the source ID
                    or 'name' to map against the ontologies field names.
            case_sensitive: Whether the identifier inspection is case sensitive.
            inspect_synonyms: Whether to inspect synonyms.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary of "mapped" and "unmapped" identifiers
            - If `return_df`: A DataFrame indexed by identifiers with a boolean `__mapped__`
                column that indicates compliance with the identifiers.

        Examples:
            >>> import lnschema_bionty as lb
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> lb.Gene.inspect(gene_symbols, field=lb.Gene.symbol)
        """
        pass

    @classmethod
    def lookup(cls, field: Optional[StrField] = None) -> NamedTuple:
        """Return an auto-complete object for a field.

        Args:
            field: `Optional[StrField] = None` The field to
                look up the values for. Defaults to first string field.

        Returns:
            A `NamedTuple` of lookup information of the field values with a
            dictionary converter.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lookup = lb.Gene.lookup()
            >>> lookup.adgb_dt
            >>> lookup_dict = lookup.dict()
            >>> lookup['ADGB-DT']
        """
        pass

    @classmethod
    def map_synonyms(
        cls,
        synonyms: Iterable,
        *,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: str = "synonyms",
        synonyms_sep: str = "|",
        field: Optional[str] = None,
        **kwargs,
    ) -> Union[List[str], Dict[str, str]]:
        """Maps input synonyms to standardized names.

        Args:
            synonyms: `Iterable` Synonyms that will be standardized.
            return_mapper: `bool = False` If `True`, returns `{input_synonym1:
                standardized_name1}`.
            case_sensitive: `bool = False` Whether the mapping is case sensitive.
            species: `Optional[str]` Map only against this species related entries.
            keep: `Literal["first", "last", False] = "first"` When a synonym maps to
                multiple names, determines which duplicates to mark as
                `pd.DataFrame.duplicated`

                    - "first": returns the first mapped standardized name
                    - "last": returns the last mapped standardized name
                    - `False`: returns all mapped standardized name
            synonyms_field: `str = "synonyms"` A field containing the concatenated synonyms.
            synonyms_sep: `str = "|"` Which separator is used to separate synonyms.
            field: `Optional[str]` The field representing the standardized names.

        Returns:
            If `return_mapper` is `False`: a list of standardized names. Otherwise,
            a dictionary of mapped values with mappable synonyms as keys and
            standardized names as values.

        Examples:
            >>> import lnschema_bionty as lb
            >>> gene_synonyms = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> standardized_names = lb.Gene.map_synonyms(gene_synonyms, species="human")
        """

    @classmethod
    def select(cls, **expressions) -> Union[QuerySet, Manager]:
        """Query records.

        Guide: :doc:`/guide/select`.

        Args:
            ORM: An ORM class.
            expressions: Fields and values passed as Django query expressions.

        Returns:
            A `QuerySet` or Django `Manager`.
        """
        from lamindb._select import select

        return select(cls, **expressions)

    @classmethod
    def search(
        cls,
        string: str,
        *,
        field: Optional[StrField] = None,
        top_hit: bool = False,
        case_sensitive: bool = True,
        synonyms_field: Optional[Union[str, TextField, CharField]] = "synonyms",
        synonyms_sep: str = "|",
    ) -> Union["pd.DataFrame", "ORM"]:
        """Search the table.

        Args:
            string: `str` The input string to match against the field ontology values.
            field: `Optional[StrField] = None` The field
                against which the input string is matching.
            top_hit: `bool = False` If `True`, return only the top hit or hits (in
                case of equal scores).
            case_sensitive: `bool = False` Whether the match is case sensitive.
            synonyms_field: `bool = True` Also search synonyms. If `None`, is ignored.

        Returns:
            A sorted `DataFrame` of search results with a score in column
            `__ratio__`. If `top_hit` is `True`, the best match.
        """
        pass

    class Meta:
        abstract = True


# A note on required fields at the ORM level
#
# As Django does most of its validation on the Form-level, it doesn't offer functionality
# for validating the integrity of an ORM object upon instantation (similar to pydantic)
#
# For required fields, we define them as commonly done on the SQL level together
# with a validator in ORM (validate_required_fields)
#
# This goes against the Django convention, but goes with the SQLModel convention
# (Optional fields can be null on the SQL level, non-optional fields cannot)
#
# Due to Django's convention where CharField has pre-configured (null=False, default=""), marking
# a required field necessitates passing `default=None`. Without the validator it would trigger
# an error at the SQL-level, with it, it triggers it at instantiation

# A note on class and instance methods of core ORM
#
# All of these are defined and tested within lamindb, in files starting with _{orm_name}.py


class User(ORM):
    """Users.

    All data in this table is synched from the cloud user account to ensure a
    universal user identity, valid across DB instances, email & handle changes.
    """

    id = models.CharField(max_length=8, primary_key=True, default=None)
    """Universal id, valid across DB instances."""
    handle = models.CharField(max_length=30, unique=True, db_index=True, default=None)
    """Universal handle, valid across DB instances (required)."""
    email = models.CharField(max_length=255, unique=True, db_index=True, default=None)
    """Email address (required)."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name (optional)."""  # has to match hub specification, where it's also optional
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""


class Storage(ORM):
    """Storage locations.

    Either S3 or GCP buckets or local storage locations.
    """

    id = models.CharField(max_length=8, default=base62_8, db_index=True, primary_key=True)
    """Universal id, valid across DB instances."""
    root = models.CharField(max_length=255, db_index=True, default=None)
    """Root path of storage, an s3 path, a local path, etc. (required)."""
    type = models.CharField(max_length=30, db_index=True)
    """Local vs. s3 vs. gcp etc."""
    region = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Cloud storage region, if applicable."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_storages")
    """Creator of record, a :class:`~lamindb.User`."""


class Tag(ORM):
    """Tags."""

    id = models.CharField(max_length=8, default=base62_8, primary_key=True)
    """A universal random id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True, default=None)
    """Name or title of tag."""
    files = models.ManyToManyField("File", related_name="tags")
    """:class:`~lamindb.File` records in tag."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_tags")
    """Creator of record, a :class:`~lamindb.User`."""


class Project(ORM):
    """Projects."""

    id = models.CharField(max_length=8, default=base62_8, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True, default=None)
    """Project name or title."""
    external_id = models.CharField(max_length=40, db_index=True, null=True, default=None)
    """External id (such as from a project management tool)."""
    tags = models.ManyToManyField("Tag", related_name="projects")
    """Project tags."""
    files = models.ManyToManyField("File", related_name="projects")
    """Project files."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_projects")
    """Creator of record, a :class:`~lamindb.User`."""


class Transform(ORM):
    """Transformations of files (:class:`~lamindb.File`).

    Pipelines, workflows, notebooks, app-based transformations.

    A pipeline is versioned software that transforms data.
    This can be anything from typical workflow tools (Nextflow, Snakemake,
    Prefect, Apache Airflow, etc.) to simple (versioned) scripts.
    """

    id = models.CharField(max_length=14, db_index=True, primary_key=True, default=None)
    """Universal id, composed of stem_id and version suffix."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Transform name or title, a pipeline name, notebook title, etc..
    """
    short_name = models.CharField(max_length=128, db_index=True, null=True, default=None)
    """A short name.
    """
    stem_id = models.CharField(max_length=12, default=base62_12, db_index=True)
    """Stem of id, identifying transform up to version."""
    version = models.CharField(max_length=10, default="0", db_index=True)
    """Version, defaults to `"0"`.

    Use this to label different versions of the same pipeline, notebook, etc.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    type = models.CharField(
        max_length=20,
        choices=TransformType.choices(),
        db_index=True,
        default=TRANSFORM_TYPE_DEFAULT,
    )
    """Transform type.

    Defaults to `notebook` if run from ipython and to `pipeline` if run from python.

    If run from the app, it defaults to `app`.
    """
    reference = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Reference for the transform, e.g., a URL.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_transforms")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("stem_id", "version"),)


class Run(ORM):
    """Runs of transformations (:class:`~lamindb.Transform`).

    Typically, a run has inputs and outputs:

    - References to outputs are stored in :class:`~lamindb.File` in the `run` field.
      This is possible as every given file has a unique run that created it. Any
      given `Run` can output multiple `files`: `run.outputs`.
    - References to inputs are stored in the :class:`~lamindb.File` in the
      `input_of` field. Any `file` might serve as an input for multiple `runs`.
      Similarly, any `run` might have many `files` as inputs: `run.inputs`.
    """

    id = models.CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name or title of run."""
    external_id = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """External id (such as from a workflow tool)."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    inputs = models.ManyToManyField("File", related_name="input_of")
    """The input files for the run."""
    # outputs on File
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    run_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_runs")
    """Creator of record, a :class:`~lamindb.User`."""


class Dataset(ORM):
    """Datasets: measurements of features.

    Datasets are measurements of features (aka observations of variables).

    1. A feature can be a “high-level” feature, i.e., it has meaning, can label
       a column in a DataFrame, and can be modeled as a Feature or another ORM.
       Examples: gene id, protein id, phenotype name, temperature,
       concentration, treatment label, treatment id, etc.
    2. In other cases, a feature might be a “low-level” feature without semantic
       meaning. Examples: pixels, single letters in sequences, etc.

    LaminDB typically stores datasets as files (`.files`), either as

    1. serialized `DataFrame` or `AnnData` objects (for high-level features)
    2. a set of files of any type (for low-level features, e.g., a folder of
       images or fastqs)

    In simple cases, a single serialized DataFrame or AnnData object (`.file`)
    is enough.

    One might also store a dataset in a SQL table or view, but this is not yet
    supported by LaminDB.
    """

    id = models.CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name or title of dataset (required)."""
    description = models.TextField(null=True, default=None)
    """A description."""
    hash = models.CharField(max_length=86, db_index=True, null=True, default=None)
    """Hash of dataset content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="datasets")
    """The feature sets measured in this dataset."""
    file = models.ForeignKey("File", on_delete=PROTECT, null=True, unique=True, related_name="datasets")
    """Storage of dataset as a one file."""
    files = models.ManyToManyField("File", related_name="datasets")
    """Storage of dataset as multiple file."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_datasets")
    """Creator of record, a :class:`~lamindb.User`."""


class Feature(ORM):
    """Features: column names of DataFrames.

    Note that you can use Bionty ORMs to manage common features like genes,
    pathways, proteins & cell markers.

    Similarly, you can define custom ORMs to manage features like gene sets, nodes, etc.

    This ORM is a way of getting started without using Bionty or a custom schema.
    """

    id = models.CharField(max_length=12, default=base62_12, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name or title of feature (required)."""
    type = models.CharField(max_length=96, null=True, default=None)
    """A way of grouping features of same type."""
    description = models.TextField(null=True, default=None)
    """A description."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="features")
    """Feature sets linked to this gene."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_features")
    """Creator of record, a :class:`~lamindb.User`."""


class FeatureSet(ORM):
    """Feature sets: sets of features.

    A feature set is represented by the hash of the id set for the feature type.

    The current supported feature types are `lnschema_bionty.Gene`,
    `lnschema_bionty.Protein`, and `lnschema_bionty.CellMarker`.

    Guides:

    - :doc:`/biology/scrna`
    - :doc:`/biology/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> feature_set = ln.FeatureSet.from_values(adata.var["ensemble_id"], Gene.ensembl_gene_id)
    >>> feature_set.save()
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq")
    >>> file.save()
    >>> file.featuresets.add(featureset)

    """

    id = models.CharField(max_length=64, primary_key=True, default=None)
    """A universal id, valid across DB instances, a hash of the linked set of features."""
    type = models.CharField(max_length=64)
    """A feature entity type."""
    files = models.ManyToManyField("File", related_name="feature_sets")
    """Files linked to the feature set."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_featuresets")
    """Creator of record, a :class:`~lamindb.User`."""


class File(ORM):
    """Test."""

    id = models.CharField(max_length=20, primary_key=True)
    """A universal random id (20-char base62), valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """A name or title for the file, mostly useful if no key is provided."""
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    suffix = models.CharField(max_length=30, db_index=True, null=True, default=None)
    """File suffix.

    This is a file extension if the `file` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """
    size = models.BigIntegerField(null=True, db_index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash = models.CharField(max_length=86, db_index=True, null=True, default=None)
    """Hash of file content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    run = models.ForeignKey(Run, PROTECT, related_name="outputs", null=True)
    """:class:`~lamindb.Run` that created the `file`."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="files", null=True)
    """:class:`~lamindb.Transform` whose run created the `file`."""
    storage: "Storage" = models.ForeignKey(Storage, PROTECT, related_name="files")
    """:class:`~lamindb.Storage` location of `file`, see `.path()` for full path."""
    # tags from Tags.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_files")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("storage", "key"),)
