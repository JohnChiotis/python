"""Unit test containing testcases for quote module"""

import os
import heapq
import unittest
import tempfile

from quote import Offer,\
                  QuoteException,\
                  get_quote,\
                  get_lenders_data


class QuoteTester(unittest.TestCase):
    """Tester class for quote module"""
    @classmethod
    def setUpClass(cls):
        # Predefined lenders data to test quote functionality
        lenders_data = [('Lender', 'Rate', 'Avail')]
        lenders_data.append(('E', '0.08', '50'))
        lenders_data.append(('A', '0.05', '200'))
        lenders_data.append(('D', '0.07', '200'))
        lenders_data.append(('C', '0.06', '50'))
        lenders_data.append(('B', '0.06', '100'))

        # Create a temporary file containing lenders data
        fobj = tempfile.NamedTemporaryFile(delete=False)
        cls.lendersfile = fobj.name
        for data_tuple in lenders_data:
            fobj.write('%s\n' % ','.join(data_tuple))
        fobj.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up lenders data file
        os.unlink(cls.lendersfile)

    def test_get_equal_quote(self):
        """test on quote that matches exactly minimum possibe of lenders"""
        ldata = get_lenders_data(self.lendersfile)
        quote = get_quote(ldata, 300, 36)
        for lender in ('A', 'B'):
            self.assertIn(lender, (o.lender for o in quote.offers))
        self.assertEqual(len(quote.offers), 2)
        for lender in ('C', 'D', 'E'):
            self.assertIn(lender, (o.lender for o in ldata))
        self.assertEqual(len(ldata), 3)

    def test_get_lenders_heap(self):
        """test correct creation of lenders offers heap"""
        ldata = get_lenders_data(self.lendersfile)
        lsort = []
        while ldata:
            offer = heapq.heappop(ldata)
            lsort.append(offer.lender)
        self.assertEqual(tuple(lsort), ('A', 'B', 'C', 'D', 'E'))

    def test_loan_bigger_than_possible(self):
        """test request of an amount that quote is unavailable"""
        ldata = get_lenders_data(self.lendersfile)
        with self.assertRaises(QuoteException):
            get_quote(ldata, 1000000, 36)

    def test_offer_representation(self):
        """test offer's string representation"""
        lender = 'A'
        rate = '0.5'
        avail = '100'
        offer = Offer(lender, rate, avail)
        for item in ('Offer', lender, rate, avail):
            self.assertEqual(str(offer).count(item), 1)

    def test_quote_rate(self):
        """test correct calculation of rate"""
        ldata = get_lenders_data(self.lendersfile)
        quote = get_quote(ldata, 550, 36)
        self.assertEqual(quote.rate, 0.06)
        self.assertEqual(quote.get_message().count('\nRate: 6.0%\n'), 1)

    def test_split_lenders_avail(self):
        """test case of part of lender's available amount exist in a quote"""
        ldata = get_lenders_data(self.lendersfile)
        quote = get_quote(ldata, 400, 36)
        for lender in ('A', 'B', 'C', 'D'):
            self.assertIn(lender, (o.lender for o in quote.offers))
        self.assertEqual(len(quote.offers), 4)
        for lender in ('D', 'E'):
            self.assertIn(lender, (o.lender for o in ldata))
        self.assertEqual(len(ldata), 2)


if __name__ == '__main__':
    unittest.main(verbosity=3)
