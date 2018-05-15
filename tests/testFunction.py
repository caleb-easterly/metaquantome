import unittest
import metaquant
import os
from definitions import DATA_DIR

class TestFunction(unittest.TestCase):
    def testSingleInt(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_single_int.tab')
        go_df = metaquant.metaquant('fn', datfile,
                                    func_colname='go', sample1_colnames='int', test=False,
                                    ontology="GO")
        self.assertEqual(go_df.loc['GO:0008150']['int'], 1)
        self.assertEqual(go_df.loc["GO:0022610"]['int'], 2/3)
        self.assertEqual(go_df.loc["GO:0008152"]['int'], 1 / 3)

    def testMultipleInt(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_multiple_int.tab')
        go_df = metaquant.metaquant('fn', datfile, func_colname='go',
                                    sample1_colnames=['int1', 'int2', 'int3'], test=False,
                                    ontology="GO")
        self.assertEqual(go_df.loc['GO:0008150']['int1'], 1)
        self.assertEqual(go_df.loc['GO:0008152']['int1'], 1/3)
        self.assertEqual(go_df.loc['GO:0022610']['int2'], 3/5)
        self.assertEqual(go_df.loc['GO:0008152']['int3'], 0.7)

    def testRedundant(self):
        """
        test that if a parent and child term are both present, the parent doesn't get double
        """
        datfile=os.path.join(DATA_DIR, 'test', 'function_multiple_go.tab')
        godf = metaquant.metaquant('fn', datfile,
                                   func_colname='go',
                                   sample1_colnames=['int1', 'int2', 'int3'],
                                   test=False,
                                   ontology="GO")
        self.assertEqual(godf.loc['GO:0008150']['int1'], 1)
        self.assertEqual(godf.loc['GO:0008152']['int1'], 1/3)
        self.assertEqual(godf.loc['GO:0022610']['int2'], 3/5)
        self.assertEqual(godf.loc['GO:0008152']['int3'], 0.7)

    def testEggnogOutput(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_eggnog_gos.tabular')
        go_df = metaquant.metaquant('fn', datfile, func_colname='go',
                                    ontology="GO",
                                    sample1_colnames=['int737WS', 'int737NS', 'int852WS',
                                                      'int852NS', 'int867WS', 'int867NS'],
                                    test=False)
        self.assertEqual(go_df.loc['GO:0008150']['int852WS'], 1)


    def testDA(self):
        datfile = os.path.join(DATA_DIR, 'test', 'function_multiple_int_ttests.tab')
        go_df = metaquant.metaquant('fn', datfile,
                                    func_colname='go',
                                    ontology="GO",
                                    sample1_colnames=['int1', 'int2', 'int3'],
                                    sample2_colnames=['int4', 'int5', 'int6'],
                                    test=True)
        # make sure all are less than 0.05
        self.assertTrue(go_df['corrected_p'].le(0.05).all())

    def testSlimDown(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_eggnog_gos.tabular')
        go_df = metaquant.metaquant('fn', datfile, func_colname='go',
                                    ontology="GO",
                                    sample1_colnames=['int737NS', 'int852NS', 'int867NS'],
                                    sample2_colnames=['int737WS', 'int852WS', 'int867WS'],
                                    test=True, slim_down=True,
                                    paired=True)

    def testCog(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_cog_single_int.tab')
        cog_df = metaquant.metaquant('fn', datfile,
                                    func_colname="cog",
                                    ontology="cog",
                                    sample1_colnames='int',
                                    test=False)
        self.assertEqual(cog_df.loc["O"]['int'], 50)
        self.assertEqual(cog_df.loc["C"]['int'], 20)

    def testCogTTest(self):
        datfile=os.path.join(DATA_DIR, 'test', 'function_cog_multiple_int_ttest.tab')
        cog_df = metaquant.metaquant('fn', datfile,
                                    func_colname="cog",
                                    ontology="cog",
                                    sample1_colnames=['int1', 'int2', 'int3'],
                                    sample2_colnames=['int4', 'int5', 'int6'],
                                    test=True)
        # make sure all are less than 0.05
        self.assertTrue(cog_df['corrected_p'].le(0.05).all())

    def testCogFiltering(self):
        # the cog category O has only 1 observation in sample1, so it should be filtered out at threshold 2
        datfile=os.path.join(DATA_DIR, 'test', 'function_cog_multiple_int_ttest_filtering.tab')
        cog_df = metaquant.metaquant('fn', datfile,
                                    func_colname="cog",
                                    ontology="cog",
                                    sample1_colnames=['int1', 'int2', 'int3'],
                                    sample2_colnames=['int4', 'int5', 'int6'],
                                    test=True,
                                    threshold=2)
        self.assertTrue("O" not in set(cog_df.index) and "C" in set(cog_df.index))

if __name__ == '__main__':
    unittest.main()