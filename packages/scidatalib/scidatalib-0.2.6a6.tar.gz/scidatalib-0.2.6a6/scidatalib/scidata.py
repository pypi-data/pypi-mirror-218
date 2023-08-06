"""Python library for writing SciData JSON-LD files"""
from datetime import datetime


# noinspection PyTypeChecker
class SciData:
    """
    This class is used to create and populate a SciData object, to be
    output as a SciData JSON-LD document

    A SciData object is created by calling the SciData class
    i.e. SciDataObject = SciData(<uid>)

    The meta variable defines the keys that make up the backbone structure of
    the JSON-LD document. Class methods are called to populate the meta keys
    """

    def __init__(self, uid: str):
        """Initialize the instance using a unique id"""

        self.meta = {
            "@context": [
                "https://stuchalk.github.io/scidata/contexts/scidata.jsonld",  # noqa
                {"sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"},  # noqa
                {}
            ],  # def base
            "@id": "",  # def docid
            "generatedAt": "",  # autopopulated
            "version": "",  # def version
            "@graph": {
                "@id": "",  # autopopulated
                "@type": "sdo:scidataFramework",
                "uid": "",  # def graph_uid
                "title": "",  # def title
                "authors": [],  # def author
                "description": "",  # def description
                "publisher": "",  # def publisher
                "version": "",  # def graphversion
                "keywords": [],  # def keywords
                "starttime": "",  # def starttime
                "permalink": "",  # def permalink
                "related": [],  # def related
                "toc": [],  # autopopulated
                "ids": [],  # def ids
                "scidata": {
                    "@id": "scidata/",
                    "@type": "sdo:scientificData",
                    "discipline": "",  # def discipline
                    "subdiscipline": "",  # def subdiscipline
                    "methodology": {
                        "@id": "methodology/",
                        "@type": "sdo:methodology",
                        "evaluation": "",  # def evaluation
                        "aspects": []},  # def aspects OR def scidatapacket
                    "system": {
                        "@id": "system/",
                        "@type": "sdo:system",
                        "facets": []},  # def facets OR def scidatapacket
                    "dataset": {
                        "@id": "dataset/",
                        "@type": "sdo:dataset",
                        "datapoint": [],  # def datapoint OR def scidatapacket
                        "scope": ""},  # def scope
                },
                "sources": [],  # def sources
                "rights": []  # def rights
                }
        }
        self.contexts = []
        self.nspaces = {}
        self.baseurl = {}
        self.meta['@graph']['uid'] = uid
        self.uidindex = []

    # public class methods
    def context(self, context: [str, list], replace=False) -> list:
        """
        Add to or replace the list of external context files

        :param context: context URL string or list of context URL strings
        :param replace: boolean to replace or not the existing data

        When called, the content URL content of the @context JSON object will
        be replaced or updated with the supplied list of context urls

        Example:

        .. code-block:: python

            SciDataObject.context(
            ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld'])
        """

        if replace:
            self.meta['@context'][:-2] = []
            self.contexts = []
            if isinstance(context, str):
                self.contexts = [context]
            if isinstance(context, list):
                self.contexts = context
        if not replace:
            self.contexts += self.meta['@context'][:-2]
            if isinstance(context, str):
                self.contexts.append(context)
            if isinstance(context, list):
                self.contexts += context
        self.contexts = sorted(list(set(self.contexts)))
        self.__make_context()
        return self.contexts

    def namespaces(self, namespaces: dict, replace=False) -> dict:
        """
        Add to or replace the dictionary of namespaces within @context.
        Namespaces are needed for values in a file that reference external
        resources that define something (vocabulary/taxonomy/ontology entries).

        :param namespaces: dictionary of namespaces (key->ns, val->URI start)
        :param replace: boolean to replace or not the existing data

        When called, the dictionary of namespaces within the @context key
        of the meta variable will be replaced or updated with the supplied
        dictionary of namespaces

        Example:

        .. code-block:: python

          SciDataObject.namespaces(
            {
              "sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"
            }
          )
        """
        if isinstance(namespaces, dict):
            if replace:
                self.meta['@context'][-2] = {}
                self.nspaces = {}
                self.nspaces = namespaces
            if not replace:
                self.nspaces.update(self.meta['@context'][-2])
                self.nspaces.update(namespaces)
        self.__make_context()
        return self.nspaces

    def base(self, base: str) -> dict:
        """
        Assign the JSON-LD @base URL
        (also defines '@id' under '@graph' for consistency)
        See: https://www.w3.org/TR/json-ld/#base-iri

        :param base: @base URL for a JSON-LD file

        Defines the base url for all internal unique identifiers
        (defined though '@id' keyword fields). For consistency, the
        code also sets the '@id' field under '@graph' so that all
        triple subjects are unique and associated with the same graph

        Example:

        .. code-block:: python

            SciDataObject.graph_uid("<uniqueidentifier>")
        """
        if isinstance(base, str):
            if base == "":
                base = "https://scidata.unf.edu/update_your_base_URL"
            self.baseurl = {"@base": base}
        self.__make_context()
        self.__graphid(base)
        return self.baseurl

    def __make_context(self) -> dict:
        """
        Recreates the context when something is added to contexts,
        namespaces or base. The method is called as part of
        the contexts, namespaces and base methods.
        """

        self.contexts += self.meta['@context'][:-2]
        self.contexts = sorted(list(set(self.contexts)))
        c = self.contexts
        self.nspaces.update(self.meta['@context'][-2])
        n = self.nspaces
        b = self.baseurl
        self.meta["@context"] = c + [n, b]
        return self.meta["@context"]

    def docid(self, docid: str) -> dict:
        """
        Assign the document identifier.  This will become the
        graph name if the file is uploaded to a graph database

        :param docid: the root level @id value
        """
        if isinstance(docid, str):
            self.meta['@id'] = docid
        return self.meta['@id']

    def version(self, version: str) -> dict:
        """
        Assign the version of this file (not the version of the data)

        :param version: the top level 'version' value
        """
        if isinstance(version, str):
            self.meta['version'] = version
        return self.meta['version']

    def graph_uid(self, guid: str) -> dict:
        """
        Assign the uid value within the @graph JSON object

        :param guid: the @graph uid value

        Normally the same as the unique id used in the @graph @id
        value and used to easily find the data in a file system.

        Example:

        .. code-block:: python

            SciDataObject.graph_uid("<uniqueidentifier>")
        """
        if isinstance(guid, str):
            self.meta['@graph']['uid'] = guid
        return self.meta['@graph']['uid']

    def author(self, authors: list, replace=False) -> list:
        """
        Add to or replace the list of authors within the @graph authors section

        :param authors: list of names, or list of dicts with multiple fields
        :param replace: boolean to replace or not the existing data

        Add the list of authors of a set of data with the following defined
        fields in the SciData context file: name, address, organization,
        email, orcid.

        Expects either:

        1)  a list of dictionaries where each dictionary contains
        at minimum of a key that is 'name'

        Example:

        .. code-block:: python

            SciDataObject.author(
            [{'name': 'George Washington', 'ORCID': 1},
            {'name': 'John Adams', 'ORCID': 2}])

        2)  a list of strings which are author names

        Example:

        .. code-block:: python

            SciDataObject.author(['George Washington', 'John Adams'])
        """
        if isinstance(authors, list):
            a = []
            if not replace:
                a += self.meta['@graph']['authors']
            for au in authors:
                auth = {'@id': ('author/' + str(len(a) + 1) + '/')}
                auth.update({'@type': 'dc:creator'})
                if isinstance(au, dict):
                    if 'name' in au:
                        auth.update(au)
                elif isinstance(au, str):
                    auth.update({'name': au})
                a.append(auth)
            self.meta['@graph']['authors'] = a
        return self.meta['@graph']['authors']

    def title(self, title: str) -> str:
        """
        Used to create or replace title key within @graph

        :param title: descriptive title of the dataset

        For a data source such as a journal article, this would
        typically be the title of the article

        Example:

        .. code-block:: python

            SciDataObject.title("The Hitchhiker's Guide to the Galaxy")
        """
        if isinstance(title, str):
            self.meta['@graph']['title'] = title
        return self.meta['@graph']['title']

    def description(self, description: str) -> str:
        """
        Assign the description field within @graph

        :param description: textual description of the dataset

        Used as a brief description of the type of data. For a
        journal article, this might house the abstract

        Example:

        .. code-block:: python

            SciDataObject.description('a brief description')
        """
        if isinstance(description, str):
            self.meta['@graph']['description'] = description
        return self.meta['@graph']['description']

    def publisher(self, publisher: str) -> str:
        """
        Assign the publisher field within @graph
        :param publisher - the name or title of the publisher of the data

        This is a person, project, research group, organization etc.

        Example:

        .. code-block:: python

            SciDataObject.publisher('The Daily Prophet')
        """
        if isinstance(publisher, str):
            self.meta['@graph']['publisher'] = publisher
        return self.meta['@graph']['publisher']

    def graphversion(self, version: str) -> str:
        """
        Assign the data version

        :param version: the version assigned to the data

        If a version is not available, the date it was accessed online
        can be used to indicate the 'state' of the data as downloaded

        Example:

        .. code-block:: python

            SciDataObject.graphversion('ChEMBL database v28')
        """
        if isinstance(version, str):
            self.meta['@graph']['version'] = version
        return self.meta['@graph']['version']

    def keywords(self, keywords: [str, list], replace=False) -> list:
        """
        Add to or replace the keywords of the instance

        :param keywords: important keywords to improve data findability
        :param replace: boolean to replace or not the existing data

        Example:

        .. code-block:: python

            SciDataObject.keywords('important')
        """
        keys = []
        if not replace:
            keys = self.meta['@graph']['keywords']
        if isinstance(keywords, str):
            keys.append(keywords)
        elif isinstance(keywords, list):
            keys += keywords
        keys.sort()
        self.meta['@graph']['keywords'] = keys
        return self.meta['@graph']['keywords']

    def starttime(self, stime: str) -> str:
        """
        Assign the start time

        :param stime: datetime string

        Typically in "%m-%d-%y %H:%M:%S" format

        Example:

        .. code-block:: python

            SciDataObject.starttime('04-05-21 06:14:53')
        """
        if isinstance(stime, str):
            self.meta['@graph']['starttime'] = stime
        return self.meta['@graph']['starttime']

    def permalink(self, link: str) -> dict:
        """
        Assign the document permanent link

        :param link: URL to the location where this document can be found

        Example:

        .. code-block:: python

            SciDataObject.permalink('https://permanent.link.com/data1')
        """
        if isinstance(link, str):
            self.meta['@graph']['permalink'] = link
        return self.meta['@graph']['permalink']

    def related(self, related: [str, list], replace=False) -> list:
        """
        Add to or replace the related URLs

        :param related: URLs to other data related to this dataset
        :param replace: boolean to replace or not the existing data

        Example:

        .. code-block:: python

            SciDataObject.related('https://example.com/greatdata.jsonld')
        """
        rels = []
        if not replace:
            rels = self.meta['@graph']['related']
        if isinstance(related, str):
            rels.append(related)
        elif isinstance(related, list):
            rels += related
        self.meta['@graph']['related'] = rels
        return self.meta['@graph']['related']

    def ids(self, ids: [str, list]) -> list:
        """
        Add to the ids list

        :param ids: string or list of strings that are
         external references to ontological concepts

        When called the contents of 'ids' is added to the ids list.
        Note that when the output function is called it iterates
        over instance content to find any values that are ontological
        references, in the format "<namespace>:<uniquevalue>", and
        adds them to ids. Only ids provided in this format will be added
        and duplicates are ignored. Remember to add namespaces for ids.

        Example:

        .. code-block:: python

            SciDataObject.ids(['chebi:00001','qudt:GM'])

        (requires the addition of the 'chebi' namespace)
        """
        curr_ids = self.meta['@graph']['ids']
        if isinstance(ids, list):
            for idee in ids:
                if ':' in idee:
                    if idee.split(':')[0] not in self.nspaces.keys():
                        print('Note: Namespace <'
                              + idee.split(':')[0]
                              + "> not set. A crosswalk "
                                "url prefix is likely not "
                                "matched with it's linked namespace")
                        # raise EnvironmentError
                    curr_ids.append(idee)
        elif isinstance(ids, str):
            if ':' in ids:
                if ids.split(':')[0] not in self.nspaces.keys():
                    print('Note: Namespace <' + ids.split(':')[0]
                          + "> not set. A crosswalk url prefix is "
                            "likely not matched with it's linked namespace")
                    # raise EnvironmentError
                curr_ids.append(ids)
        self.meta['@graph']['ids'] = sorted(set(curr_ids))
        return self.meta['@graph']['ids']

    def discipline(self, disc: str) -> str:
        """
        Assign the discipline area of the data'

        :param disc: a discipline name or identifier (preferred)

        Best practice is to use and entry in an ontology,
        i.e. the Modern Science Ontology (https://w3id.org/skgo/modsci#)

        Example:

        .. code-block:: python

            SciDataObject.discipline('w3i:Chemistry')

        (requires the addition of the 'w3i' namespace)
        """
        if isinstance(disc, str):
            if ":" in disc:
                self.__addid(disc)
            self.meta['@graph']['scidata']['discipline'] = disc
        return self.meta['@graph']['scidata']['discipline']

    def subdiscipline(self, subdisc: str) -> str:
        """
        Assign the subdiscipline area of the data

        :param subdisc: a subdiscipline name or identifier (preferred)

        Best practice is to use and entry in an ontology,
        i.e. the Modern Science Ontology (https://w3id.org/skgo/modsci#)

        Example:

        .. code-block:: python

            SciDataObject.subdiscipline('w3i:AnalyticalChemistry')
        """
        if isinstance(subdisc, str):
            if ":" in subdisc:
                self.__addid(subdisc)
            self.meta['@graph']['scidata']['subdiscipline'] = subdisc
        return self.meta['@graph']['scidata']['subdiscipline']

    def evaluation(self, evaln: str) -> str:
        """
        Assign the evaluation field

        :param evaln: the method of evaluation of research data

        Recommended values of this field are:
        experimental, theoretical, computational

        Example:

        .. code-block:: python

            SciDataObject.evaluation('experimental')
        """
        if isinstance(evaln, str):
            if ":" in evaln:
                self.__addid(evaln)
            self.meta['@graph']['scidata']['methodology']['evaluation'] = evaln
        return self.meta['@graph']['scidata']['methodology']['evaluation']

    def aspects(self, aspects: list) -> list:
        """Add to or replace the aspects of the file

        Example:

        .. code-block:: python

            SciDataObject.aspects(
            [{"@id": "assay",
             "@type": "sdo:assay",
             "description": "Inhibition of human ERG "
                            "by MK499 binding assay",
             "assay_organism": "Homo sapiens"}])

        Method also accepts keyword '#intlinks'.
        See documentation for def scidatapackage.
        """
        new_aspects = []
        scidata: dict = self.meta['@graph']['scidata']
        methodology: dict = scidata['methodology']
        curr_aspects: list = methodology['aspects']
        for listentry in aspects:
            intlinklist = None
            if '#intlinks' in listentry.keys():
                intlinklist = listentry.pop('#intlinks')
            rootitem = self.__iterate_function(listentry)
            rootitemid = rootitem['@id']
            itemlist = [rootitem]
            if intlinklist:
                for intlinkentry in intlinklist:
                    intitem = (self.__iterate_function(intlinkentry))
                    intitem.update({'aspects#': [rootitemid]})
                    itemlist.append(intitem)
            for n, item in enumerate(itemlist):
                item_noid = {k: item[k] for k in
                             set(list(item.keys())) - {'@id'} - {'aspects#'}}
                matched_aspect = 0
                for aspectitem in curr_aspects:
                    aspect_item_noid = {
                        k: aspectitem[k] for k in
                        set(list(aspectitem.keys())) - {'@id'} - {'aspects#'}}
                    if aspect_item_noid == item_noid:
                        if n == 0:
                            rootitemid = aspectitem['@id']
                        if aspectitem.get('aspects#', None):
                            item['aspects#'] = [rootitemid]
                            if item['aspects#'][0] not in \
                                    aspectitem['aspects#']:
                                aspectitem['aspects#'] \
                                    .append(item['aspects#'][0])
                        matched_aspect = aspectitem
                if matched_aspect:
                    self.uidindex.remove(item['@id'])
                    new_aspects.append(matched_aspect)
                else:
                    new_aspects.append(item)
                    curr_aspects.append(item)
        methodology['aspects'] = curr_aspects
        scidata['methodology'] = methodology
        self.meta['@graph']['scidata'] = scidata
        return new_aspects

    def facets(self, facets: list) -> list:
        """Add to or replace the facets of the file

        Example:

        .. code-block:: python

            SciDataObject.facets(
            [{"@id": "compound",
            "@type": "sdo:compound",
            "mw_freebase": "491.52",
            "full_molformula": "C26H26FN5O4"}])

        Method also accepts keyword '#intlinks'.
        See documentation for def scidatapackage.
        """
        new_facets = []
        scidata: dict = self.meta['@graph']['scidata']
        system: dict = scidata['system']
        curr_facets: list = system['facets']
        for listentry in facets:
            intlinklist = None
            if '#intlinks' in listentry.keys():
                intlinklist = listentry.pop('#intlinks')
            rootitem = self.__iterate_function(listentry)
            rootitemid = rootitem['@id']
            itemlist = [rootitem]
            if intlinklist:
                for intlinkentry in intlinklist:
                    intitem = self.__iterate_function(intlinkentry)
                    intitem.update({'facets#': [rootitemid]})
                    itemlist.append(intitem)
            for n, item in enumerate(itemlist):
                item_keys = set(list(item.keys()))
                item_noid = {
                    k: item[k] for k in item_keys - {'@id'} - {'facets#'}
                }
                matched_facet = 0
                for facetitem in curr_facets:
                    facet_item_noid = {
                        k: facetitem[k] for k in
                        set(list(facetitem.keys())) - {'@id'} - {'facets#'}}
                    if facet_item_noid == item_noid:
                        if n == 0:
                            rootitemid = facetitem['@id']
                        if facetitem.get('facets#', None):
                            item['facets#'] = [rootitemid]
                            facetitem['facets#'].append(item['facets#'][0])
                            facet_list = list(set(facetitem['facets#']))
                            facetitem['facets#'] = facet_list
                        matched_facet = facetitem
                if matched_facet:
                    self.uidindex.remove(item['@id'])
                    new_facets.append(matched_facet)
                else:
                    new_facets.append(item)
                    curr_facets.append(item)
        system['facets'] = curr_facets
        scidata['system'] = system
        self.meta['@graph']['scidata'] = scidata
        return new_facets

    def scope(self, scope: [str, list]) -> str:
        """
        Assign what thing(s) the dataset relates to

        :param scope: str or list of internal unique id()s of
         entity(ies) in the system to which the data describes

        The scope of a datasets should be described in the 'system' 'facets'
        section, e.g. chemical system, organism, specimen, should be included
        as a scope using the defined unique '@id' for that section

        Example:

        .. code-block:: python

            SciDataObject.scope('chemicalsystem/1/')
        """
        if isinstance(scope, str) or isinstance(scope, list):
            self.meta['@graph']['scidata']['dataset']['scope'] = scope
        return self.meta['@graph']['scidata']['dataset']['scope']

    def attribute(self, attributes: list) -> list:
        """Add one or more attributes"""
        new_attributes = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'attribute' in dataset.keys():
            curr_attributes: list = dataset['attribute']
        else:
            curr_attributes = []
        for listentry in attributes:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_attribute = 0
            for attributeitem in curr_attributes:
                attribute_item_noid = {
                    k: attributeitem[k] for k in set(
                        list(
                            attributeitem.keys())) - {'@id'}}
                if attribute_item_noid == item_noid:
                    matched_attribute = attributeitem
            if matched_attribute:
                new_attributes.append(matched_attribute)
                self.uidindex.remove(item['@id'])
            else:
                new_attributes.append(item)
                curr_attributes.append(item)

        dataset['attribute'] = curr_attributes
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_attributes

    def datapoint(self, points: list) -> list:
        """Add one or more datapoints

        Example:

        .. code-block:: python

            SciDataObject.datapoint(
            [{"@id": "datapoint",
             "@type": "sdo:datapoint",
             "data": [{"@id": "datum",
                       "@type": "sdo:exptdata",
                       "type": "IC50",
                       "value": "15.2",
                       "units": "uM"}]}])

        """
        new_points = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']

        curr_points: list = dataset['datapoint']

        for listentry in points:
            item = self.__iterate_function(listentry)
            new_points.append(item)
            curr_points.append(item)

        dataset['datapoint'] = curr_points
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_points

    def dataseries(self, series: list) -> list:
        """Add one or more dataseries"""
        new_series = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'dataseries' in dataset.keys():
            curr_series: list = dataset['dataseries']
        else:
            curr_series = []
        for listentry in series:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_serie = 0
            for serieitem in curr_series:
                serie_item_noid = {
                    k: serieitem[k] for k in set(
                        list(
                            serieitem.keys())) - {'@id'}}
                if serie_item_noid == item_noid:
                    matched_serie = serieitem
            if matched_serie:
                new_series.append(matched_serie)
                self.uidindex.remove(item['@id'])
            else:
                new_series.append(item)
                curr_series.append(item)

        dataset['dataseries'] = curr_series
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_series

    def datagroup(self, group: list) -> list:
        """Add one or more datagroups"""
        new_group = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'datagroup' in dataset.keys():
            curr_group: list = dataset['datagroup']
        else:
            curr_group = []
        for listentry in group:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_group = 0
            for groupitem in curr_group:
                group_item_noid = {
                    k: groupitem[k] for k in set(
                        list(
                            groupitem.keys())) - {'@id'}}
                if group_item_noid == item_noid:
                    matched_group = groupitem
            if matched_group:
                new_group.append(matched_group)
                self.uidindex.remove(item['@id'])
            else:
                new_group.append(item)
                curr_group.append(item)

        dataset['datagroup'] = curr_group
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_group

    def scidatapackage(self, package):
        """
        Add a package of data where the datapoints are linked with the
        associated aspects and facets.
        A package contains one or more 'packets' of associated aspects,
        facets and datapoints.

        Template:

        .. code-block:: python

            package = [
                {'aspects':{},'facets':{},'datapoints':{}},
                {'aspects':{},'facets':{},'datapoints':{}}
                ]

        Example:

        .. code-block:: python

          SciDataObject.scidatapackage([{
            "aspects": [{
              "@id": "assay/",
              "@type": "sdo:assay",
              "description": "Inhibition of human ERG by MK499 binding assay",
              "assay_organism": "Homo sapiens"
            }],
            "facets": [
              {
                "@id": "compound/",
                "@type": "sdo:compound",
                "mw_freebase": "491.52",
                "full_molformula": "C26H26FN5O4",
                "#intlinks": [{
                  "@id": "identifier/",
                  "@type": "sdo:identifier",
                  "standard_inchi_key": "OINHUVBCKUJZAG-UHFFFAOYSA-N"
                }]
              },
              {
                "@id": "target/",
                "@type": "sdo:target",
                "pref_name": "HERG",
                "tax_id": 9606,
                "organism": "Homo sapiens"
              }
            ],
            "datapoints": [{
              "@id": "datapoint/",
              "@type": "sdo:datapoint",
              "data":[{
                "@id": "datum",
                "@type": "sdo:exptdata",
                "type": "IC50",
                "value": "15.2",
                "units": "uM"
              }]
            }]
          }])

        """
        for packet in package:
            packet['facets'] = self.facets(packet['facets'])
            packet['aspects'] = self.aspects(packet['aspects'])
            atfacet = [a_dict["@id"] for a_dict in packet['facets']]
            ataspect = [a_dict["@id"] for a_dict in packet['aspects']]
            for dp in packet['dataset']:
                if atfacet:
                    dp.update({'facets#': atfacet})
                if ataspect:
                    dp.update({'aspects#': ataspect})
            self.datapoint(packet['dataset'])

    def sources(self, sources: list, replace=False) -> dict:
        """
        Add to or replace the source reference list

        :param sources: information about where the data came from
        :type sources: list
        :param replace: replace (True) or add to the existing sources (False)
        :type replace: bool (default: False)

        Add a list of sources with any of the available defined fields
        in the SciData context file: citation, reftype, url, doi

        Example:

        .. code-block:: python

            SciDataObject.sources([
            {'citation': 'Chalk, S.J. SciData: a data model and
            ontology for semantic representation of scientific data.
            J Cheminform 8, 54 (2016)',
            doi': https://doi.org/10.1186/s13321-016-0168-9'}])
        """
        srcs = []
        if not replace:
            srcs = self.meta['@graph']['sources']
        for x in sources:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        return self.meta['@graph']['sources']

    def rights(self, holder: str, lic: str) -> dict:
        """
        Add the rights section to the file (max: 1 entry)

        :param holder: the entity that holds the license to this data
        :param lic: the assigned license

        """
        rights = []
        if isinstance(holder, str) and isinstance(lic, str):
            rights = [{
                '@id': 'rights/1/',
                '@type': 'dc:rights',
                'holder': holder,
                'license': lic,
            }]
        self.meta['@graph']['rights'] = rights
        return self.meta['@graph']['rights']

    # private class functions
    def __addid(self, text: str) -> bool:
        """
        Adds entry to ids list if string contains ':'
        """
        if isinstance(text, str):
            if '://' in text:
                return False
            elif len(text.split(':')) > 1:
                return False
            elif ':' in text:
                self.ids(text)
                return True
        else:
            return False

    def __graphid(self, gid: str) -> bool:
        """
        Assigns the @id value within the @graph JSON object.
        """
        self.meta['@graph']['@id'] = gid
        return True

    def __addtoc(self):
        """ adds entries to the toc list"""

        def tocdict(a):
            """ get the @type entry from a dictionary """
            for k, v in a.items():
                if k == '@type':
                    if isinstance(v, list):
                        self.meta['@graph']['toc'].extend(v)
                    else:
                        self.meta['@graph']['toc'].append(v)
                if isinstance(v, list):
                    toclist(v)
                if isinstance(v, dict):
                    tocdict(v)

        def toclist(a):
            """ process lists """
            for x in a:
                if isinstance(x, dict):
                    tocdict(x)
                if isinstance(x, list):
                    toclist(x)

        for key, value in self.meta['@graph'].items():
            if key == '@type':
                self.meta['@graph']['toc'].append(value)
            if isinstance(value, dict):
                tocdict(value)
            if isinstance(value, list):
                toclist(value)

        self.meta['@graph']['toc'] = sorted(set(self.meta['@graph']['toc']))
        return

    def __iterate_function(self, it, uid=False):
        if isinstance(it, str):
            self.__addid(it)
            return it
        if isinstance(it, list):
            if not all(isinstance(item, dict) for item in it):
                return it
        prev_uid = uid

        # Set the category
        if '@id' in it:
            category = it['@id']
        else:
            category = 'undefined'

        if prev_uid:
            uid = prev_uid + category + '/1/'
        else:
            uid = category + '/1/'

        def enumuid(uidstr):
            """
            function to create unique internal id ('@id')
            for each section of the file.
            """
            uidsplit = uidstr.rsplit('/', 2)
            uidstr = uidsplit[0] + '/' + str(int(uidsplit[1]) + 1) + '/'
            return uidstr

        while uid in self.uidindex:
            uid = enumuid(uid)
        self.uidindex.append(uid)

        temp: dict = {'@id': uid, '@type': 'sdo:' + category}
        for key, value in it.items():
            if key != '@id':
                if isinstance(value, list):
                    if not all(isinstance(item, dict) for item in value):
                        temp[key] = value
                    else:
                        listuid = uid
                        for i, listentry in enumerate(value):
                            value[i] = self.__iterate_function(
                                listentry, listuid)
                        temp[key] = value

                elif isinstance(value, dict):
                    temp[key] = self.__iterate_function(
                        value, uid)

                else:
                    temp[key] = value
                    self.__addid(value)
        return temp

    @property
    def output(self) -> dict:
        """
        Completes and cleans a Scidata Object (instance of this class)
        before its output.
        """

        # add the generatedAt date
        today = datetime.today()
        self.meta['generatedAt'] = today.strftime("%m-%d-%y %H:%M:%S")

        # clean @graph
        for key in list(self.meta['@graph']):
            if not self.meta['@graph'][key]:
                if key != 'toc':
                    del self.meta['@graph'][key]

        # clean scidata
        for key in list(self.meta['@graph']['scidata']):
            value = self.meta['@graph']['scidata'][key]
            if not value or value == "":
                del self.meta['@graph']['scidata'][key]

        # clean methodology, if exists
        if 'methodology' in self.meta['@graph']['scidata']:
            methodology = self.meta['@graph']['scidata']['methodology']

            if methodology.get('aspects', False):
                for key in list(methodology):
                    if not methodology[key] or methodology[key] == "":
                        del methodology[key]
            else:
                # as 'aspects' is empty, delete the methodology section
                del methodology

            # clean system, if exists
        if 'system' in self.meta['@graph']['scidata']:
            system = self.meta['@graph']['scidata']['system']
            if system.get('facets', False):
                for key in list(system):
                    if not system[key] or system[key] == "":
                        del system[key]
            else:
                # as 'facets' is empty, delete the system section
                del system

        # remove data set if not data
        if 'dataset' in self.meta['@graph']['scidata']:
            dataset = self.meta['@graph']['scidata']['dataset']
            if not dataset.get('dataseries', False):
                if not dataset.get('datagroups', False):
                    if not dataset.get('datapoints', False):
                        del dataset

        # clean dataset, if exists
        if 'dataset' in self.meta['@graph']['scidata']:
            dataset = self.meta['@graph']['scidata']['dataset']
            if dataset:
                for key in list(dataset):
                    if not dataset[key] or dataset[key] == "":
                        del dataset[key]

                # clean dataseries
                if 'dataseries' in dataset.keys():
                    if dataset.get('dataseries', False):
                        dataseries = dataset["dataseries"]
                        for seridx, series in enumerate(dataseries):
                            for key in list(series):
                                if not series[key]:
                                    del dataseries[seridx][key]
                    else:
                        # delete if present but empty
                        del dataseries

                # clean datagroups
                if 'datagroups' in dataset.keys():
                    if dataset.get('datagroups', False):
                        datagroups = dataset["datagroups"]
                        for grpidx, series in enumerate(datagroups):
                            for key in list(series):
                                if not series[key]:
                                    del datagroups[grpidx][key]
                    else:
                        # delete if present but empty
                        del datagroups

                # clean datapoints
                if 'datapoints' in dataset.keys():
                    if dataset.get('datapoints', False):
                        datapoints = dataset["datapoints"]
                        for pntidx, series in enumerate(datapoints):
                            for key in list(series):
                                if not series[key]:
                                    del datapoints[pntidx][key]
                    else:
                        # delete if present but empty
                        del datapoints

        # add the toc to the output
        self.__addtoc()

        return self.meta
