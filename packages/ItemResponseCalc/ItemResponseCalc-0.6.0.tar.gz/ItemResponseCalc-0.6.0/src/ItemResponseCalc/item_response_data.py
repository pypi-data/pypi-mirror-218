"""This module defines help classes to access responses to questionnaire items.
Data may be stored in various file formats.

*** Class Overview:

ItemResponseDataSet: reference to all response data for selected group(s),
    to be used as input for statistical analysis.
    Response data input must be an iterable over response records.
    A Response Record is a 1D array-like with ordinal responses from ONE subject,
    with one ordinal index value for each Questionnaire Item.
    The input data for one group may be
    1) a single list of subject response lists,
    2) an ir_source.ItemResponseTable (subclass) instance, defining ONE data source,
    3) an ir_source.Tables instance, chaining input from SEVERAL sources.

Questionnaire: description of a questionnaire, usually with several items

Item: description of a single item (question and answer alternatives)

*** Input Source Formats:
Data may be accessed from simple lists, or from any type of source that Pandas can handle,
e.g., csv or xlsx files, or SQL database(s).
pandas.read_xxx(...), or similar user-defined function, can be used for actual reading.

Each source may have responses encoded in a specific way, different from other sources.
Allowed response alternatives must be specified by user, for each input source.

*** Usage Example:

q_file = string or Path identifying questionnaire text (utf8) file
r_file_xxx = string or Path identifying a response file

group0_table = item_response_table(source=r_file0, items=...)
group1_table = item_response_table(r_file1, items=...)
group2A_table = item_response_table(r_file2A, items=...)
group2B_table = item_response_table(r_file2B, items=...)

In each source, items = a dict with elements (column header, list of ordinal response categories)
exactly as encoded in that data source.
Any other value is interpreted as a missing response.
Length of items must agree with number of questionnaire items.

ids = ItemResponseDataSet.load(questionnaire=Questionnaire.load(q_file),
        groups={'Group0': group0_table,
                'Group1': group1_table,
                'Group2', Tables(group2A_table, group2B_table)
                }
        )

This data-set can then be used as input to create an analysis model.
See run_irt.py for a complete example.

An index_col may be defined for a column with respondent IDs in each input table.
Duplicate indices will then be removed on reading, but only within each input data chunk.

*** Version History:

* Version 0.6.0:
2023-07-09, use pandas.read_sql to access database source.
2022-09-15, use pandas.read_xxx functions to access input data files.

* Version 0.5:
2019-07-23, functional version, may need some cleanup
2019-07-29, new version with general table_reader interface
2019-08-25, minor cleanup
"""
# *** use subject_ID for individual displays?
# *** use item_ID for item displays ?

import numpy as np
from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
class Item:
    """Information describing ONE questionnaire item.
    """
    def __init__(self, question, responses, reverse=False):
        """
        :param question: string with explicit question text
        :param responses: list of ordinal response categories, one for each possible response
            as presented in the questionnaire
        :param reverse: boolean = True if responses should be indexed in reverse order
            NOTE: Response data files may or may not already have recoded
            the responses by ordinal indices in the desired analysis order.
        """
        self.question = question
        self.responses = responses
        self.reverse = reverse

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t'
                + ',\n\t'.join((f'{k}={repr(v)}' for (k, v) in self.__dict__.items()))
                + ')')

    @property
    def n_response_levels(self):
        return len(self.responses)

    @property
    def ordinal_responses(self):
        """Responses in order of increasing underlying trait
        :return: iterator over ordinal response categories (NOT a copy)
        """
        return reversed(self.responses) if self.reverse else self.responses

    # def response_int(self):
    #     """Response categories coded as integers 1, ..., n_response_levels
    #     """
    #     return list(range(1, 1 + self.n_response_levels))

    def response_codes(self):
        """Response categories as code values in range(n_response_levels)
        :return: list
        """
        return list(range(self.n_response_levels))


class Questionnaire:
    """Container for a questionnaire with several items,
    required to specify number of items and number of response levels for each item,
    even if the actual questions and response alternatives are not included.
    """
    def __init__(self, header=None, items=None, item_response_levels=None):
        """
        :param header: (optional) string describing the questionnaire
        :param items: (optional) list of Item instances
        :param item_response_levels: (optional) used only if items is None:
            list with
            item_response_levels[i] = integer number of response levels for i-th item
        """
        self.header = header
        if items is None:
            self.items = [Item(question=f'Question {i+1}',
                               responses=list(range(1, n_levels +1)))
                          for (i, n_levels) in enumerate(item_response_levels)]
            # self.item_response_levels = item_response_levels
        else:
            self.items = items

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t'
                + ',\n\t'.join((f'{k}={repr(v)}' for (k,v) in self.__dict__.items()))
                + '\n\t)')

    # @property
    # def item_response_levels(self):  # ******** needed ?
    #     return [len(item.responses) for item in self.items]

    @property
    def n_items(self):
        return len(self.items)

    @classmethod
    def load(cls, file, sep='\t'):
        """Read questions and answers from given file
        :param file: string or Path object identifying input file
        :param sep: (optional) string, separator between response alternatives
        :return: cls instance
        """
        strip = ' \n'  # chars to strip away from end of input lines
        with Path(file).open('rt', encoding='utf8') as f:
            header = f.readline()
            items = []
            while True:
                q = f.readline()
                a = f.readline()
                reverse = f.readline()
                if a == '':
                    break  # even if ioiha_q is non-empty
                else:
                    items.append(Item(question=q.rstrip(strip),
                                      responses=(a.rstrip(strip)).split(sep),
                                      reverse='rev' in reverse))
        return cls(header.rstrip(strip), items)


# ------------------------------------------------------------
class ItemResponseDataSet:
    """All result data for one complete item response analysis,
    including one or several groups of subjects.
    There should be at least one group with complete individual response data,
    otherwise the analysis cannot reveal correlations between items.
    """
    def __init__(self, questionnaire, groups):
        """
        :param questionnaire: single Questionnaire object
        :param groups: dict with elements (g_name, g_subjects), where
            g_name = string identifying the group
            g_subjects = iterable of responses, either,
                (1) a simple list or array,
                (2) OR an ir_source.ItemResponseTable subclass instance,
                (3) OR an ir_source.Tables instance
                    with several join-ed ir_source.ItemResponseTable objects.  **************************
            Each input table yields a sequence of response_record, one for each subject.
                response_record = a 1D list with
                response_record[i] = integer ordinal index of response to i-th item
                encoded with origin == 0.
                Missing responses are indicated as -1.
        """
        assert questionnaire is not None, 'Must have a Questionnaire object'
        self.questionnaire = questionnaire
        if groups is None:
            groups = dict()
        self.groups = groups

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + f'\n\t questionnaire= {self.questionnaire.__class__.__name__} '
                + f'object with {self.questionnaire.n_items} items,'
                + '\n\t groups= {\n\t\t'
                + ',\n\t\t'.join(f'{g_key}: {g.__class__.__name__} object with {len(g)} respondent records'
                                 for (g_key, g) in self.groups.items()) + '}'
                + ')')

    # @property
    # def n_response_levels(self):  # ******** needed ?
    #     return self.questionnaire.item_response_levels

    @property
    def n_items(self):   # ******** needed
        return self.questionnaire.n_items

    @property
    def n_groups(self):
        return len(self.groups)

    def response_counts(self, normalize=False):
        """Tabulate distributions of response counts by items and groups
        :param normalize: (optional) True: present relative frequencies,
            False: absolute response counts
        :return: list of pd.DataFrame objects,
            one count table for each item, each with one column for each group
        """
        res_df = [pd.DataFrame(index=pd.CategoricalIndex(item.ordinal_responses,
                                                         copy=True,
                                                         ordered=True,
                                                         name='Response'),
                               columns=[], dtype=int)  # empty df
                  for item in self.questionnaire.items]
        # = space for results
        for (g, g_table) in self.groups.items():
            g_codes = np.array([row for row in g_table])
            for (i, item) in enumerate(self.questionnaire.items):
                gi_series = pd.Series(pd.Categorical.from_codes(g_codes[:, i],
                                                                categories=item.responses,
                                                                ordered=True))
                gi_count = gi_series.value_counts(sort=False,
                                                  normalize=normalize)
                res_df[i][g] = gi_count.reindex(item.responses, fill_value=0)
        return res_df

    def item_response_count(self):
        """Number of response counts for each item,
        summed across all groups.
        :return: c = list of response count arrays, with
            c[i] = 1D array for i-th item,
            with responses encoded with origin == 0, i.e.,
            c[i][l] = count of l-th ordinal response alternative for this item
        """
        return [c_i.sum(axis=1).to_numpy()
                for c_i in self.response_counts()]

    def item_total_count(self):
        """Total number of response counts for each item,
        summed across all response alternatives and all groups.
        :return: c = list of total response counts,
            c[i] = scalar integer for i-th item
        """
        return [c_i.sum().sum()
                for c_i in self.response_counts()]


# -------------------------------------------------------- Module TEST:
if __name__ == '__main__':
    from ItemResponseCalc.ir_source import item_response_table, Tables
    from sqlalchemy import create_engine

    HAQ_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry/IRT-IOI-HA/IOI-HA-Data'
    # ioiha_data_path = HAQ_PATH / 'IRT-IOI-HA' / 'IOI-HA-data'
    # to ioi-ha data sets OTHER THAN the Swedish Quality Registry

    print('*** Test Load Questionnaire:\n')
    ioiha_q = Questionnaire.load(HAQ_PATH / 'IOI-HA-English.txt')
    print(ioiha_q)
    # ------------------------------------------------------------------

    print('\n*** Testing Table from Excel with Hickson data set:\n')
    work_path = HAQ_PATH
    test_file = HAQ_PATH / 'Hickson' / 'Short_Eartrak AUS.xlsx'

    irf = item_response_table(source=test_file,
                              items={f'Q0{i}': range(1, 6)
                                     for i in range(1, 8)},
                              index_col=0  # integer for read_excel, but string also seems to work
                              )
    print('printing a few records:')
    for (i, r) in enumerate(irf):
        print(r)
        if i > 10:
            break
    print('printing first few records again:')
    for (i,r) in enumerate(irf):
        print(r)
        if i > 5:
            break

    all_r = [r for r in irf]
    print('number of records=', len(all_r))
    print(f'len(irf) = ', len(irf))

    print('\n*** Test item_response_table using SQLAlchemy engine ***')
    sql_path = work_path / 'test_sql'
    engine = create_engine("sqlite+pysqlite:///" + str(sql_path / 'testHickson.db'))
    ir_sql = item_response_table(source=engine,
                                 sql='ioiha',  # *** "SELECT * FROM ioiha",
                                 index_col='EarRowId',
                                 items={f'Q0{item}': [str(i) for i in range(1, 6)]
                                        for item in range(1, 8)},
                                 )  # NOTE: string-encoded integers here

    # ---------------------------------------------------- Test Hickson in data set:
    print('\n*** Testing using Hickson file(s) in an ItemResponseDataSet object:\n')

    ids = ItemResponseDataSet(questionnaire=ioiha_q, #  Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
                              groups={'HicksonEarTrak': irf,
                                      'Hickson_sql': ir_sql,
                                      'Hickson_joined': Tables(irf, ir_sql)})

    print(ids)
    print('\nResponse Counts:')
    for (i, (q_i, c_df)) in enumerate(zip(ids.questionnaire.items,
                                          ids.response_counts())
                                      ):
        print(f'\nQuestion: ' + q_i.question)
        print(c_df)

    print('\nitem_response_count=\n', ids.item_response_count())
    # all items have same n_response_levels:
    print('item_total_counts: ', ids.item_total_count())


    # # ----------------------------------------- test Kramer SPSS data set:
    #
    # print('\n*** Testing ItemResponseTable with Kramer data set:\n')
    #
    # kramer_file = ItemResponseTable(HAQ_PATH / 'Kramer' / 'moeder_final - kopieforArne.sav',
    #                                 items={f'ioi_v{i}': range(1, 6)
    #                                          for i in range(1, 8)},
    #                                 )
    #
    # print(f'Using {kramer_file} with {len(kramer_file)} records')
    # print('printing a few records:')
    # for (i, r) in enumerate(kramer_file):
    #     if i > 10:
    #         break
    #     print(r)
    #
    # kramer2_columns = {'T2IOIHA1': range(5),  # coded as 0,.., 4
    #                    'T2IOIHA2': range(1, 6),  # coded as 1,.., 5
    #                    'T2IOIHA3': range(1, 6),
    #                    'T2IOIHA4': range(5),  # coded as 0,.., 4
    #                    'T2IOIHA5': range(1, 6),
    #                    'T2IOIHA6': range(1, 6),
    #                    'T2IOIHA7': range(1, 6)}
    # kramer_file2 = ItemResponseTable(HAQ_PATH / 'Kramer' / 'NLSH-Kramer-T2IOI-HA.csv',  # sav',
    #                                  items=kramer2_columns,
    #                                  )
    #
    # print(f'Using {kramer_file2} with {len(kramer_file2)} records')
    # print('printing a few records:')
    # for (i, r) in enumerate(kramer_file2):
    #     if i > 10:
    #         break
    #     print(r)
    #
    # print(f'Testing {kramer_file} in ItemResponseDataSet')
    # ids = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
    #                           groups={'Kramer': kramer_file})
    #
    # print(ids)
    # print('response_count=\n', ids.item_response_count)
    # print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])
    #
    # # -------------------- test using Dillon-2010 file
    # print('\n*** Testing ItemResponseTable with Dillon data set:\n')
    # dillon10_file = HAQ_PATH / 'Dillon' / 'Final processed file - deidentified_IOIHA.xlsx'
    # print(f'AU-D-10: Using {dillon10_file}')
    #
    # # header = [f'Question{i}' for i in range(1, 8)]
    # # dillon10 = item_response_table(dillon10_file,
    # #                                fields=header,
    # #                                field_types=str,
    # #                                missing_values=['', 'NS', 'N/A'],
    # #                                header_row=1,
    # #                                sample_factor=sample_factor,
    # #                                accept_row=accept_record,
    # #                                recode_fcns=[recode_responses, recode_missing])
    #
    # dillon10_columns = {f'Question{i+1}': ioiha_q.items[i].responses.copy()
    #                     for i in range(7)}
    # dillon10_columns['Question1'][1] = 'less than 1 hour per day'
    # dillon10_columns['Question1'][2] = '1-4 hours per day'
    # dillon10_columns['Question1'][3] = '4-8 hours per day'
    # dillon10_columns['Question2'][0] = 'did not help at all'
    #
    # def set_lower_case(v):
    #     """Ensure lower case in reading strings from Dillon-2010:
    #     :param v: string cell value
    #     :return: lower case
    #     """
    #     return str(v).lower()
    #
    # dillon10 = ItemResponseTable(dillon10_file,
    #                              items=dillon10_columns,
    #                              converters={c: set_lower_case
    #                                          for c in dillon10_columns.keys()})
    #
    # print(f'Using {dillon10} with {len(dillon10)} records')
    # print('printing a few records:')
    # for (i, r) in enumerate(dillon10):
    #     if i > 50:
    #         break
    #     print(f'{i+2}: ', r)
    #
    # print(f'Testing {dillon10} in ItemResponseDataSet')
    # ids = ItemResponseDataSet(questionnaire=ioiha_q,
    #                           groups={'Dillon10': dillon10})
    #
    # print(ids)
    # print('response_count=\n', ids.item_response_count)
    # print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])


# ------------------------------------------------------- Check using Swedish data set:
#     print('\n*** Testing table_reader_sqlite with haq data set:\n')
#
#     def accept_record(r):
#         """Inclusion_crit for accepting a record
#         :param r: dict with all record fields
#         :param f: list of record field keys to be used
#         :return: boolean == True if record is acceptable
#         """
#         n_missing = sum(r_i is None for r_i in r)
#         within_range = all((r_i is None) or 1 <= r_i <= 5
#                            for r_i in r)
#         return n_missing <= 3 and within_range
#     # -------------------------------------------------------------------
#
#     HAQ_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry/ircData'
#     db_file = str(HAQ_PATH / 'development.sqlite3')
#
#     SELECT_FROM = ("prescriptions where " +
#                     "Respondent = 't' " +
#                     "AND article_company IS NOT NULL " +
#                     "AND date >= '2016-01-01' AND date <= '2016-01-30' "
#                    )
#
#     haq = item_response_table(file_path=db_file,
#                               select_from=SELECT_FROM,
#                               fields=[f'Q{i}' for i in np.arange(3,10)],
#                               accept_row=accept_record,
#                               recode_fcns=recode_missing_as_0)
#     # *** missing data is already coded as 0
#
#     print(f'len(haq) = ', len(haq))
#     print('*** First few records selected for analysis:')
#     n_rec = 10
#     for r in haq:
#         print(r)
#         n_rec -= 1
#         if n_rec <= 0:
#             break
#
#     print('\n*** Testing ItemResponseDataSet with sqlite dataset:\n')
#     ids = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                               groups={'HAQregistry': haq})
#
#     print(ids)
#
#     print('response_count=\n', ids.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])
#
#     # -------------------------------------------------------------------
#     print('\n*** Testing ItemResponseDataSet with three sources:\n')
#
#     ids3 = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                                groups={'AU': irf,
#                                                   'NL': kramer_file,
#                                                   'SE': haq})
#
#     print(ids3)
#
#     print('response_count=\n', ids3.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids3.item_response_count])
